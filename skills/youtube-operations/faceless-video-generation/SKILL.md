---
name: faceless-video-generation
description: "Use when producing faceless AI shorts or vertical reels."
version: 1.0.0
category: youtube-operations
---

# Faceless AI Video Generation Pipeline

Automated, 100% self-hosted engine to produce high-retention faceless vertical videos (YouTube Shorts, Instagram Reels, Facebook Reels) without third-party subscription wrappers.

---

## 1. Pipeline Overview

A self-hosted alternative to SaaS wrappers (like Loopra). The pipeline orchestrates:
1. **Script Reconstruction**: 3-act narrative arc (Hook, Escalation, Climax/Twist) optimized for US audience retention.
2. **Consistent Visuals**: Anchor character identity across scenes via detailed physical descriptions in OmniRoute image generation.
3. **Voiceover**: Crystal clear US English narration via Edge-TTS.
4. **Cinematic Motion**: Dynamic Ken Burns pan/zoom via FFmpeg filtergraph.
5. **Dynamic Hardsubs**: High-contrast yellow subtitles with bold black stroke burned at the lower third.

---

## 2. Step-by-Step Procedure

### Step 1: Script & Storyboard Breakdown
Break any 15–30 second topic or viral hook into 3 distinct scenes:
* **Scene 1 (0–4s, Hook)**: Introduce subject with an intriguing premise.
* **Scene 2 (4–9s, Action/Escalation)**: Immediate conflict, goal, or high-stakes action.
* **Scene 3 (9–15s, Climax/Twist)**: Satisfying punchline, conclusion, or surprise.

### Step 2: Consistent Character Visual Generation
Generate native 9:16 vertical images via OmniRoute (`http://localhost:20128/v1/images/generations`):
* **Model**: `antigravity/gemini-3.1-flash-image`
* **Native 9:16 Size**: Specify `"size": "1024x1792"` (or `"768x1344"`) in the API payload to avoid horizontal squeezing or vertical stretching ("penyet kanan-kiri").
* **Prompt Framing**: Prefix every prompt with `"Vertical 9:16 composition, [full shot / wide shot / medium shot] of..."` so the AI models the scene with correct mobile vertical headroom and ground plane.
* **Prompt Anchoring Rule**: Keep core character attributes identical in every scene prompt (e.g., *"The same cute fluffy ginger kitten with bright green eyes wearing a tiny red apron..."*).
* **Style Anchor**: Append consistent aesthetic tokens to all scenes (e.g., `8k photorealistic, Pixar style, vivid cinematic lighting`).

### Step 3: Natural Speech Narration & Subtitle Single Source of Truth
Never maintain separate text variables for TTS audio and hardsubs. Subtitles must be programmatically derived from the exact strings spoken by TTS.

1. **Clause-by-Clause Segmentation**:
   Define scenes as arrays of concise 2–3 second clauses:
   ```python
   SCENE = {
       "clauses": [
           "Ferrari literally does not care if you have a hundred million dollars.",
           "If you break their unspoken rules, you are banned for life."
       ]
   }
   ```
2. **Deterministic Timestamping**:
   Generate audio per clause via Edge-TTS, pad with a 0.3s natural pause between clauses, and concatenate. This provides mathematically exact start/end timestamps for each ASS subtitle line.
3. **TTS Invocation**:
   ```bash
   edge-tts --voice en-US-ChristopherNeural --rate=+4% \
     --text "Ferrari literally does not care if you have a hundred million dollars." \
     --write-media /path/to/clause1.mp3
   ```
   Query exact audio duration using `ffprobe`:
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /path/to/clause1.mp3
   ```

### Step 4: Anti-Jitter Cinematic Motion (Ken Burns via FFmpeg)
Direct `zoompan` on 1080x1920 causes visible frame-to-frame jitter due to subpixel integer snapping. To achieve 100% smooth motion without jitter:
1. Scale image to high-res canvas (e.g., `scale=2160:3840`).
2. Apply `zoompan` at 4K resolution with gentle increments (`0.0003`–`0.0005` per frame) matching `frames = int(duration_sec * 30)`.
3. Downscale back to 1080x1920 using `scale=1080:1920:flags=lanczos`.

```bash
# Smooth Zoom-In (Hook / Scene 1):
ffmpeg -y -loop 1 -i scene1.png -i scene1.mp3 \
  -filter_complex "[0:v]scale=2160:3840,zoompan=z='min(zoom+0.0004,1.10)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=128:s=2160x3840:fps=30,scale=1080:1920:flags=lanczos[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -c:a aac -shortest clip1.mp4

# Smooth Zoom-Out (Action / Scene 2 with frame-1 initialization):
ffmpeg -y -loop 1 -i scene2.png -i scene2.mp3 \
  -filter_complex "[0:v]scale=2160:3840,zoompan=z='if(lte(on,1),1.10,max(1.001,zoom-0.00035))':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=163:s=2160x3840:fps=30,scale=1080:1920:flags=lanczos[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -c:a aac -shortest clip2.mp4
```

### Step 5: Merge & Burn Dynamic Hardsubs
1. Concatenate individual clips with `concat` demuxer:
```bash
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy raw_merged.mp4
```
2. Prepare ASS subtitle file (`subtitles.ass`) with high-retention styling:
```ini
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,58,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4.5,0,2,60,60,260,1
```
3. Burn subtitles into final production video:
```bash
ffmpeg -y -i raw_merged.mp4 -vf "ass=subtitles.ass" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy final_short.mp4
```

---

## 3. Critical Pitfalls & Operational Rules

- **Single Source of Truth for Voiceover & Subtitles**: Subtitle text must be programmatically derived from the exact same strings passed to TTS. Never write separate hardsub and speech variables in scripts, which causes word omission, phrasing drift, and hardsub desynchronization.
- **Aspect Ratio & Anti-Squish Rule**: Never scale 1:1 or non-9:16 images directly to 2160x3840/1080x1920 without aspect preservation. Always generate native 9:16 vertical images (`"size": "1024x1792"`) via OmniRoute. If processing square legacy assets, apply strict center-crop: `scale=-1:3840,crop=2160:3840:(iw-2160)/2:0`.
- **Anti-Jitter 4K Canvas Rule**: Never run `zoompan` directly on 1080x1920 without 4K upscaling. Subpixel coordinate rounding causes vibrating/jittery output.
- **100% Verbatim Subtitle Rule**: Subtitle text must match the voiceover audio word-for-word. Never paraphrase, summarize, or alter proper names/numbers between the TTS script and hardsubs.
- **2–3s Dynamic Chunking Rule**: Split scene subtitles into 2–3 second phrases aligned with natural audio pauses (via `silencedetect` or clause breaks). Do not display a single long paragraph for 8–10 seconds.
- **Authority Voice Matching for Tier-1 Niches**: For Business Warfare, Wealth Secrets, and Dark Psychology, use deep authoritative narrator voices (`en-US-ChristopherNeural` / `en-US-GuyNeural`) to mask synthetic cadence and project native credibility.

- **Antigravity Multi-Account Failover for Images**: OmniRoute routes image generation (`/v1/images/generations`) to the connection with highest priority. If an account returns `429 RESOURCE_EXHAUSTED` (`You have exhausted your capacity on this model`), OmniRoute may stick to that account unless marked. Set `rate_limited_until` in `~/.omniroute/storage.sqlite` for the exhausted account to force failover to sibling accounts with fresh quotas.
- **Match Exact Audio Frames in Zoompan**: Always calculate `d = int(duration * fps)`. A mismatch causes `zoompan` to freeze or jitter at the transition boundary.
- **Center-Weighted Prompting for 9:16 Cropping**: Since square 1024x1024 images lose 420px on the sides when center-cropped to 9:16 portrait, always specify *"centered main subject"* in the prompt so crucial character elements are not cropped out.
