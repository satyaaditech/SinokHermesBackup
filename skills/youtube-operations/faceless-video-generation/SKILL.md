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
Generate 1024x1024 scene images via OmniRoute (`http://localhost:20128/v1/images/generations`):
* **Model**: `antigravity/gemini-3.1-flash-image`
* **Prompt Anchoring Rule**: Keep core character attributes identical in every scene prompt (e.g., *"The same cute fluffy ginger kitten with bright green eyes wearing a tiny red apron..."*).
* **Style Anchor**: Append consistent aesthetic tokens to all scenes (e.g., *"3D Pixar animation style, warm bakery lighting, cinematic 8k"*).

### Step 3: Natural Speech Narration (Edge-TTS)
Generate audio with Microsoft Edge-TTS (fast, zero API cost):
```bash
edge-tts --voice en-US-ChristopherNeural --rate=+5% \
  --text "Meet Milo, the tiniest kitten with the biggest dream in town." \
  --write-media /path/to/scene1.mp3 \
  --write-subtitles /path/to/scene1.vtt
```
Query exact audio duration using `ffprobe`:
```bash
ffprobe -v quiet -print_format json -show_format /path/to/scene1.mp3
```

### Step 4: Cinematic Motion (Ken Burns via FFmpeg)
To convert 1024x1024 square images into full 1080x1920 (9:16) portrait without stretching or black bars:
1. Scale image to 1920x1920.
2. Center-crop to 1080x1920.
3. Apply `zoompan` matching the exact frame count of the audio duration (`frames = int(duration_sec * 30)`).

```bash
# Slow Zoom-In (Hook / Scene 1):
ffmpeg -y -loop 1 -i scene1.png -i scene1.mp3 \
  -filter_complex "[0:v]scale=1920:1920,crop=1080:1920:(1920-1080)/2:0,zoompan=z='min(zoom+0.0012,1.20)':d=128:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset fast -pix_fmt yuv420p -c:a aac -shortest clip1.mp4

# Dynamic Pan/Zoom (Action / Scene 2):
ffmpeg -y -loop 1 -i scene2.png -i scene2.mp3 \
  -filter_complex "[0:v]scale=1920:1920,crop=1080:1920:(1920-1080)/2:0,zoompan=z='if(lte(zoom,1.0),1.18,max(1.0,zoom-0.0011))':d=163:x='(iw-iw/zoom)*(on/163)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset fast -pix_fmt yuv420p -c:a aac -shortest clip2.mp4
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

- **Antigravity Multi-Account Failover for Images**: OmniRoute routes image generation (`/v1/images/generations`) to the connection with highest priority. If an account returns `429 RESOURCE_EXHAUSTED` (`You have exhausted your capacity on this model`), OmniRoute may stick to that account unless marked. Set `rate_limited_until` in `~/.omniroute/storage.sqlite` for the exhausted account to force failover to sibling accounts with fresh quotas.
- **Match Exact Audio Frames in Zoompan**: Always calculate `d = int(duration * fps)`. A mismatch causes `zoompan` to freeze or jitter at the transition boundary.
- **Center-Weighted Prompting for 9:16 Cropping**: Since square 1024x1024 images lose 420px on the sides when center-cropped to 9:16 portrait, always specify *"centered main subject"* in the prompt so crucial character elements are not cropped out.
