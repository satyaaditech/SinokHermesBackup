---
name: ai-shorts-video-factory
description: "Use when generating automated 9:16 AI Shorts & Reels."
version: 1.0.0
category: youtube-operations
---

# AI Shorts Video Factory

A production-grade, 100% self-hosted pipeline to generate high-retention 9:16 vertical videos (YouTube Shorts, Instagram Reels, TikTok) across high-RPM niches (Business Warfare, Wealth Secrets, Dark Psychology).

---

## 1. Core Architecture: The 4 Pillars

```
[Single Source of Truth Script] (Clauses)
            │
            ├───► 1. Edge-TTS Audio Generation ──► Clause Duration Measurement (Miliseconds)
            │                                               │
            │                                               ▼
            └───► 2. Synchronized ASS Subtitles ◄── Matched Timestamps (+0.35s Breathing Silence)
                                                            │
[Native 9:16 Visuals] ──► 3. 4K Canvas Ken Burns ──► 4. Merged & Hardsub Burn ──► [Master Video MP4]
 (1024x1792 OmniRoute)       (Push/Pan/Tilt Lanczos)      (1080x1920 CRF 17)
```

---

## 2. Standard Operating Procedure

### Step 1: Script Structuring & Single Source of Truth
Break every 30–50s Short into 4 scenes. Break each scene into 1–2 line **clauses**.
*Never maintain separate variables for TTS voiceover and hardsub text.*

```python
SCENES_DATA = [
    {
        "id": 1,
        "name": "Hook - Dramatic Push-in",
        "clauses": [
            "If you walk into a Rolex boutique with ten thousand dollars in cash,",
            "they will politely refuse to sell you a watch."
        ],
        "motion": "push_in"
    },
    ...
]
```

### Step 2: Native 9:16 Visual Generation
Generate photorealistic images via OmniRoute (`http://localhost:20128/v1/images/generations`):
* **Model**: `antigravity/gemini-3.1-flash-image`
* **Size**: Explicitly pass `"size": "1024x1792"` (native 9:16).
* **Prompt Rule**: Always start prompt with `"Vertical 9:16 composition, ..."` to ensure subject is naturally framed vertically without side distortion.
* **Failover Handling**: When encountering HTTP 429 (Resource Exhausted), update connection priority in `~/.omniroute/storage.sqlite` to switch to an active sibling account.

### Step 3: Precise Audio Timing & Silence Padding
Generate TTS per clause and measure exact duration using `ffprobe`:
```python
def get_audio_duration(path):
    p = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ], capture_output=True, text=True, check=True)
    return float(p.stdout.strip())

# Loop through clauses, generate mp3, calculate timestamps, append 0.35s silence between clauses
```

### Step 4: Multi-Axis Smooth Motion Engine (Jitter Prevention)
Standard FFmpeg `zoompan` at 1080x1920 causes integer subpixel snapping (jitter). Always:
1. Upscale input to a 4K canvas (`2160x3780`).
2. Apply distinct, perceptible multi-axis motions:
   * **Push-In (+25% Zoom)**:
     `zoompan=z='1.00+0.25*(on/{frames})':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s=2160x3780:fps=30`
   * **Pan Left-to-Right**:
     `zoompan=z='1.18-0.08*(on/{frames})':x='(iw-iw/zoom)*(on/{frames})':y='(ih-ih/zoom)/2':d={frames}:s=2160x3780:fps=30`
   * **Pan Right-to-Left + Zoom**:
     `zoompan=z='1.10+0.15*(on/{frames})':x='(iw-iw/zoom)*(1-on/{frames})':y='(ih-ih/zoom)*0.75':d={frames}:s=2160x3780:fps=30`
   * **Tilt Upward + Zoom**:
     `zoompan=z='1.08+0.16*(on/{frames})':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*(1-on/{frames})':d={frames}:s=2160x3780:fps=30`
3. Downscale to `1080:1920` with Lanczos filtering: `scale=1080:1920:flags=lanczos`.

### Step 5: ASS Subtitle Burn-In
Generate ASS subtitle file using the verbatim clauses, formatted to 2 lines per screen with high contrast yellow font (`&H0000FFFF`) and black outline (`&H00000000`, Outline: 5.0, MarginV: 340). Burn directly onto video with FFmpeg.

---

## 3. Pitfalls & Troubleshooting

* **Horizontal Squeeze ("Penyet Kanan-Kiri")**:
  * *Cause*: Forcing 1:1 square images into 9:16 without aspect-preserving crop.
  * *Fix*: Always request `1024x1792` natively from OmniRoute. If given 1:1, center-crop (`scale=3780:3780,crop=2160:3780:(iw-2160)/2:0`) before zoompan.
* **Subtitles Disagree with Voice**:
  * *Cause*: Separate string definitions for TTS and Subtitles or manual transcription.
  * *Fix*: Enforce Single Source of Truth where clause strings generate both TTS audio and ASS subtitle events.
* **Zoompan Shaking / Micro-Jitter**:
  * *Cause*: FFmpeg integer coordinate truncation at standard 1080p resolution.
  * *Fix*: Render `zoompan` at 4K resolution (`2160x3780`) and downscale using Lanczos filter.
* **Sluggish / Imperceptible Movement**:
  * *Cause*: Subtle zoom changes (<8%) look static on mobile screens.
  * *Fix*: Target 15–25% zoom delta and use horizontal/vertical camera pans to track across subjects.
