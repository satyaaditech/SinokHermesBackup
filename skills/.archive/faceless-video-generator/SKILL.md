---
name: faceless-video-generator
description: Use when generating 3D and realistic AI Shorts.
category: youtube-operations
---

# Faceless & Realistic AI Video Generator (Loopra Alternative)

A complete, zero-cost, server-side pipeline to produce high-retention 9:16 vertical videos (YouTube Shorts, Reels, TikTok) without third-party subscription tools.

## Supported Genres & Golden Baselines
- **3D Pixar Animation (Milo Baseline):** `/home/satyaaditech/shorts_factory/restore_points/milo_v1_baseline/`
- **Photorealistic Satir / Drama (Budi & Siti Baseline):** `/home/satyaaditech/shorts_factory/restore_points/budi_siti_v2_finetuned/`

*Rule:* Never mix or overwrite restore points. Keep each genre's scripts and assets isolated in its dedicated baseline directory.

---

## 1. Visual Generation & Character DNA Consistency
- **Endpoint:** OmniRoute Gemini Image (`antigravity/gemini-3.1-flash-image`) via `http://localhost:20128/v1/images/generations`.
- **Character DNA Anchoring:**
  - *3D Animation:* Describe exact species, fur color, eye color, and fixed clothing (e.g., *"cute fluffy ginger tabby kitten with emerald green eyes wearing a miniature Captain America helmet and star suit... 3D Pixar animation style"*).
  - *Photorealistic Human:* State exact age, ethnic features, skin undertone, facial shape, eye shape, hairstyle/parting, signature jewelry, and exact outfit (e.g., *"A 30-year-old Indonesian woman named Siti with identical facial features: warm golden-tan skin, oval face, arched dark eyebrows, almond dark-brown eyes, shoulder-length dark brown wavy hair parted on left, wearing a casual light pastel-blue blouse, tiny gold stud earrings"*).
- **Universal Quality Modifiers:** `Photorealistic, cinematic lighting, 8k resolution, ultra detailed, depth of field`.
- **Failover / Quota Handling:** If HTTP 429 occurs, adjust `priority` or set `is_active = 0` on exhausted accounts in `~/.omniroute/storage.sqlite` (`provider_connections` table) so traffic routes to active accounts.

---

## 2. Voice Acting & Indonesian Flow (Edge-TTS)
- **Voice Models:**
  - English Narration: `en-US-ChristopherNeural` (+8% rate).
  - Indonesian Male (e.g. Budi): `id-ID-ArdiNeural` (+5% to +6% rate).
  - Indonesian Female (e.g. Siti): `id-ID-GadisNeural` (+5% to +6% rate).
- **TTS Punctuation & Natural Flow (CRITICAL):**
  - Do **NOT** use ellipses (`...`) or commas directly before vocatives (e.g., avoid `"... , Dek!"` or `"Besok... tolong"`). This causes robotic 1.5-second silences.
  - Write text as clean, natural spoken dialogue (e.g., *"Ehh, itu investasi masa depan alat transportasi Dek!"* and *"Besok tolong siapkan bantal dan guling di teras ya Dek."*).

---

## 3. Motion Engine (Pillow Subpixel + SmoothStep)
Never use FFmpeg's native `zoompan` for slow Ken Burns (it calculates with integer pixels, causing micro-jitter, and snaps/glitches ("jeglek") on zoom boundaries).

**The Proven Python Frame Generator Pattern:**
```python
import subprocess
from PIL import Image

# For each scene:
img = Image.open(scene_img).convert("RGB")
W, H = img.size
base_crop_w, base_crop_h = H * (9.0 / 16.0), H
fps = 30
total_frames = int(duration * fps)

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo", "-vcodec", "rawvideo",
    "-s", "1080x1920", "-pix_fmt", "rgb24", "-r", str(fps),
    "-i", "-", "-i", scene_audio,
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-t", f"{duration:.3f}", out_clip_path
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for f in range(total_frames):
    t = f / float(max(1, total_frames - 1))
    ease = 3.0 * (t ** 2) - 2.0 * (t ** 3)  # Cubic SmoothStep
    cur_zoom = start_zoom + (end_zoom - start_zoom) * ease
    cur_w, cur_h = base_crop_w / cur_zoom, base_crop_h / cur_zoom
    cx, cy = W / 2.0, H / 2.0
    box = (cx - cur_w / 2.0, cy - cur_h / 2.0, cx + cur_w / 2.0, cy + cur_h / 2.0)
    
    frame = img.resize((1080, 1920), resample=Image.Resampling.BICUBIC, box=box)
    proc.stdin.write(frame.tobytes())

proc.stdin.close()
proc.wait()
```

---

## 4. Hardcoded Subtitles (.ass)
Burn synchronized ASS subtitles at the lower third:
- **Font:** DejaVu Sans, Size 54
- **Primary Color:** Yellow (`&H0000FFFF`)
- **Outline:** Thick Black (`&H00000000`, 4.5px)
- **Shadow:** Semi-transparent Black (`&H80000000`)
- **Alignment:** 2 (Bottom-Center), `MarginV=260`
- **Two-line break:** Use `\N` for multi-line dialogue to avoid edge clipping.
