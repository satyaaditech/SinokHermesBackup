---
name: code-motion-graphics
description: Use when creating code-driven motion graphics video (MP4).
category: creative
---

# Code-Driven Motion Graphics Pipeline

A zero-dependency, ultra-fast pipeline to produce cinema-grade motion graphic explainer videos, kinetic typography, and animated scientific diagrams directly in Python and FFmpeg without Adobe After Effects or heavy GPU rendering farms.

## When to Use
- User asks for motion graphic videos, animated explainers, or kinetic diagrams (e.g. physics concepts, spiritual anatomy, philosophical frameworks).
- Creating viral social media educational shorts (YouTube Shorts, Instagram Reels, TikTok) in the style of code animations (Remotion, Manim, Canvas).
- Visualizing multi-stage dynamic processes: light refraction/reflection, data flow, consciousness ladders, algorithm execution.

## Core Architecture & Workflow

```
[Thematic Audio Narration] (Edge-TTS Chunks + FFmpeg Concat)
           │
           ▼ (Exact Duration Anchor)
[Mathematical Storyboard] (Time, Easing & Virtual Camera Zoom)
           │
           ▼
[Vector / Frame Generation] (Python PIL Memory Buffers)
           │
           ▼ (Direct In-Memory Stdin Pipe)
[FFmpeg Encoder] (libx264, 30/60 FPS, yuv420p, CRF 17)
           │
           ▼
[Master MP4 Video] ──► Telegram Inline Playback (MEDIA:/path.mp4)
                    ──► Local HTTP Server (http://192.168.0.112:8000/path.mp4)
```

---

## Production Rules & User Preferences

### 1. Pacing, Duration, & Framerate Tradeoffs
- **Explainer Duration**: Paced for complete comprehension without rushing. Explainer shorts can run from 30s up to 2–3 minutes (120s–180s) when explaining detailed science or educational concepts.
- **Framerate vs Timeout Guard**:
  - Always use **30 FPS** (`TOTAL_FRAMES = 30 * duration`) for any video >10s. At 30 FPS, ~4,000 frames (2m13s) renders in only ~25s via PIL stdin pipe, well within tool timeout limits while ensuring smooth motion.
  - Reserve 60 FPS only for ultra-short micro-loops (<10s).

### 2. Tone & Visual Styling Presets
Choose the visual preset based on audience and topic:
- **Preset A: Contemplative / Adult Scientific**
  - Background: Deep slate/dark navy (`#0B0F19`), neon cyan (`#38BDF8`) & gold (`#EAB308`) accents.
  - Voice: `id-ID-ArdiNeural` or `id-ID-DimasNeural` (pitch -20%, rate -2%).
  - Text Cards: Dark glass boxes (`(15, 23, 42, 235)`) with neon borders.
- **Preset B: Kids / Casual Educational / Viral Gen-Z (Pak Satya's Favorite)**
  - Background: Bright daytime sky gradient (Sky Blue `#87CEEB` to Airy White `#EBF8FF`), drifting fluffy cartoon clouds, smiling animated Sun with rotating/pulsating rays.
  - Characters: Kawaii/friendly personification (e.g. "Si Droplet" with specular shine, anime eyes, pink blush `#F472B6`).
  - Narrative & Language: Casual, conversational Indonesian with punchy metaphors ("jaket putih 7 superhero", "trampolin boing", "wush! melambat").
  - Comic Accents: Action bubble tags (`[ WUSH! ]`, `[ BOING! ]`), protractor angles, bouncing candy mnemonic pills (`[ME][JI][KU]...` with harmonic sine bounce offset `sin(8t + k)`).
  - Outro: Celebration confetti particles & "Kamu Jagoan Sains!" banner.
  - Voice: `id-ID-GadisNeural` (speed `+5%` to `+8%`, pitch `+2Hz`), enthusiastic and friendly.

### 2. Anti-Squint Typography & Mobile Sizing Rules
Viewer must **never have to squint** on mobile vertical screens:
- **Header / Stage Title**: 44px–52px bold.
- **Main Explainer / HUD Badge**: 34px–42px bold.
- **Body & Subtitle Labels**: Minimum 28px–32px.
- **High-Contrast Enclosures**: Text must always sit inside dark contrast cards (`(15, 23, 42, 235)` with 2–3px glowing neon borders) so moving animated elements never obscure legibility.

### 3. Dynamic Virtual Camera (Pan & Zoom per Stage)
Never keep the camera static when explaining multi-step diagrams with fine details.
- Implement a 2D camera coordinate transformer:
  ```python
  def world_to_screen(wx, wy, cx, cy, cz):
      sx = WIDTH / 2 + (wx - cx) * cz
      sy = HEIGHT / 2 + (wy - cy) * cz
      return int(sx), int(sy)
  ```
- **Interpolation**: Use cubic bezier or smooth ease-in-out between keyframe tuples `(time_sec, cam_x, cam_y, cam_zoom)`.
- **Zoom In (2.0x–2.5x)**: Magnify the active focal area (e.g. entry boundary, reflection wall, focal nodes) during detailed step explanations.
- **Zoom Out (0.8x–1.0x)**: Return to wide-angle panoramic view for intro setup and the final grand conclusion.

### 4. Synchronized Voiceover / TTS Integration
- Split narration into logical blocks (8–12 seconds each) to avoid Microsoft Edge-TTS WebSocket 429 errors:
  ```bash
  /home/satyaaditech/.local/bin/edge-tts --voice id-ID-ArdiNeural --text "..." --write-media part1.mp3
  ```
- Stitch audio blocks with micro-pauses (300–600ms) using FFmpeg `filter_complex adelay/concat` to establish the exact master duration.
- Multiplex final video and audio:
  ```bash
  ffmpeg -y -i raw_video.mp4 -i full_narration.mp3 -c:v copy -c:a aac -b:a 192k -shortest final_video.mp4
  ```

### 5. Direct In-Memory Streaming (Zero Disk I/O)
Never save individual PNG frames to disk. Stream raw RGB bytes directly to FFmpeg standard input:
```python
cmd = [
    FFMPEG_BIN, '-y',
    '-f', 'rawvideo', '-vcodec', 'rawvideo',
    '-s', f'{WIDTH}x{HEIGHT}', '-pix_fmt', 'rgb24',
    '-r', str(FPS), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-preset', 'fast', '-crf', '17',
    RAW_VIDEO_TMP
]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for frame in frames:
    proc.stdin.write(im.tobytes())
proc.stdin.close()
proc.wait()
```

---

## Delivery Standard
1. Deliver the video file natively to Telegram via `MEDIA:/path/to/final_video.mp4`.
2. Copy to `/home/satyaaditech/<filename>.mp4` so it is instantly streamable via local HTTP server `http://192.168.0.112:8000/<filename>.mp4`.

---

## Remotion & Hyperframe Architecture

For rich React-based web motion graphics, interactive components, dynamic kinetic typography, and multi-track audio, use the local Remotion engine:
* **Workspace Location**: `/home/satyaaditech/remotion-workspace/`
* **Root Compositions**: `src/Root.tsx` registers all compositions with dimensions, FPS, and frame durations.
* **Inspect Compositions**: `npx remotion compositions src/index.ts` lists all registered compositions, durations, and resolutions.
* **Render Command**:
  ```bash
  npx remotion render src/index.ts <CompositionId> out/<output_name>.mp4 --concurrency=4 --gl=angle
  ```

### 1. Mandatory Dual-Track Audio (Voiceover + Thematic BGM)
* **Never Ship Voice-Only**: Explainer videos without background music sound dry, hollow, and unfinished.
* **Ducking Standard**: Layer background music (BGM) at volume `0.15`–`0.22` beneath the narration track (`volume=1.0`).
* **In Remotion Component**:
  ```tsx
  <Audio src={staticFile('narasi.mp3')} />
  <Audio src={staticFile('bgm_ceria.mp3')} volume={0.16} />
  ```
* **In FFmpeg Post-Mix**:
  ```bash
  ffmpeg -y -i video.mp4 -i bgm.mp3 \
    -filter_complex "[0:a]volume=1.0[a1];[1:a]volume=0.20[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
    -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k output.mp4
  ```

### 2. Hyperframe Multi-Layer Visual Depth
For educational, explainer, or kid-friendly content, avoid flat static backgrounds:
* **Dynamic Skies**: Time-interpolated gradients (`linear-gradient(180deg, #38bdf8 0%, #bae6fd 55%, #fef08a 100%)`).
* **Living Scenery**: Drifting fluffy clouds, smiling rotating sun with pulsing rays, rolling cartoon hills at the bottom (`radial-gradient` circles), and floating rainbow sparkles/bubbles.
* **Spring Physics**: Use Remotion `spring()` with `damping: 12, mass: 0.5` for cartoon badge bounce and kinetic text punch-in.

### 3. Rapid Muxing vs Full Background Re-Render
* **Performance Budget**: Remotion renders at ~8.5 FPS on 4-core CPUs (~8–10 minutes for 4,500 frames).
* **Instant Turnaround**: When visual frames are already rendered and only BGM, audio mix, or track volume needs updating, use FFmpeg audio stream muxing (`-c:v copy`) to produce the deliverable in seconds, while launching the full visual re-render in the background (`terminal(background=true, notify=true)`).
