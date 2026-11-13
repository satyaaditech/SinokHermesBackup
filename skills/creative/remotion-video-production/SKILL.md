---
name: remotion-video-production
description: Use when creating explainer videos with Remotion and React.
category: creative
---

# Remotion Video Production Pipeline

A robust, code-first video production workflow for creating high-quality explainer videos, educational animations, and kinetic motion graphics using Remotion (React + TypeScript) on Linux servers.

## When to Use
- User asks for animated explainer videos using Remotion, Hyperframe, or React-based motion graphics.
- Creating modular, component-driven educational videos (e.g. science explanations, children's stories, system architecture walkthroughs).
- Programmatic video rendering requiring precise audio-visual synchronization, kinetic typography, and procedural assets.

---

## Production Procedure & Architecture

```
[Audio Narration] (Edge-TTS / Recorded Voice)
       │
       ▼ (Measure Exact Duration in Seconds)
[Procedural BGM] (Python wave synthesis / verified local audio)
       │
       ▼
[Remotion Composition] (Root.tsx: durationInFrames = Math.ceil(durationInSeconds * fps))
       │
       ├── Background Layer (Pastel gradients, rolling hills, floating particles)
       ├── Subject & Illustration Layer (SVG / HTML Canvas / React Spring / Hyperframe)
       ├── Kinetic Typography (Captions, highlighted keywords, synchronized pulses)
       └── Audio Tracks (<Audio src={staticFile(...)} volume={...} />)
       │
       ▼
[Benchmark Slice Probe] (Render 60-300 frames to measure FPS and memory)
       │
       ▼
[Full Render / Fast Delivery Mux] (Remotion CLI --concurrency=4 --gl=angle)
```

### Step 1: Narration & Duration Anchor
1. Synthesize narration first using Edge-TTS or provide clean voiceover.
2. Probe exact duration using `ffprobe`:
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3
   ```
3. Set Remotion composition `durationInFrames = Math.ceil(durationInSeconds * fps)`. Never guess frame counts without checking audio duration.

### Step 2: Procedural BGM Generation (Avoid Download Traps)
* **Pitfall**: External web downloads for stock BGM (e.g., Mixkit, FreeMusicArchive) frequently fail due to rate limits, CAPTCHAs, or socket read timeouts on headless servers.
* **Standard**: Synthesize cheerful, melodic background music procedurally in Python using standard library `wave` and `math` (e.g. marimba/glockenspiel in C-Major, 116 BPM, I-V-vi-IV progression), or use pre-cached local assets.
* **Audio Balance**: Set BGM volume between `0.15` and `0.22` so speech narration remains crisp and intelligible.

### Step 3: Kid-Friendly & Cheerful Visual Design Rules
* **Background Atmosphere**:
  - Sky: Soft sky-blue to warm pastel gradient (`linear-gradient(180deg, #38bdf8 0%, #bae6fd 60%, #e0f2fe 100%)`).
  - Rolling Hills: Layered overlapping radial-gradient circles at the bottom (`#4ade80`, `#22c55e`, `#16a34a`).
  - Dynamic Elements: Floating rainbow sparkles, soft bubbles, and a smiling, gently rotating cartoon sun.
* **Kinetic Typography**:
  - Bold, friendly sans-serif fonts (e.g., Poppins, Montserrat, Fredoka).
  - High contrast text boxes with semi-transparent backdrops (`rgba(15, 23, 42, 0.75)` or clean white cards with colored borders).
  - Limit text to 6–10 words per slide for maximum retention.

### Step 4: Remotion Component Structure
In the React composition component:
```tsx
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

export const ExplainerVideo = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f172a' }}>
      {/* 1. Audio Narration & BGM */}
      <Audio src={staticFile('narration.mp3')} volume={1.0} />
      <Audio src={staticFile('bgm_cheerful.mp3')} volume={0.18} />

      {/* 2. Background Scene */}
      <BackgroundScene frame={frame} />

      {/* 3. Visual Motion Rig */}
      <VisualStoryScene frame={frame} fps={fps} />
    </AbsoluteFill>
  );
};
```

### Step 5: Server CLI Rendering & Performance Optimization
On CPU-only Linux servers (e.g. AMD APU or VPS without dedicated GPU):
1. **Benchmark Before Full Render**:
   Always test-render a 60–100 frame slice first:
   ```bash
   npx remotion render src/index.ts CompositionName out/test_slice.mp4 --frames=0-60 --concurrency=4 --gl=angle
   ```
   Calculate FPS: `FPS = frames / time_taken`. Use this to estimate full render time.
2. **Headless Chrome Flags**:
   - Use `--gl=angle` for optimal software/OpenGL rasterization on Linux.
   - Use `--concurrency=4` (match physical core count; exceeding core count degrades Puppeteer performance).
3. **Fast Delivery Strategy**:
   If an existing video stream was previously rendered and only audio/BGM changed, use FFmpeg to immediately remux audio in ~2 seconds for instant user review, while launching the full multi-frame re-render in the background with `terminal(background=true, notify=true)`:
   ```bash
   ffmpeg -y -i video.mp4 -i bgm.mp3 -filter_complex "[0:a]volume=1.0[a1];[1:a]volume=0.20[a2];[a1][a2]amix=inputs=2:duration=first[aout]" -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k out.mp4
   ```

---

## Common Pitfalls & Rules
1. **Audio Static File Paths**: In Remotion, files referenced with `staticFile('filename.mp3')` MUST reside directly inside the `public/` directory of the Remotion root. Subdirectories or external paths throw bundling errors.
2. **Framerate Consistency**: Stick strictly to 30 FPS for web/mobile explainer content. 60 FPS doubles render time on CPU without noticeable benefit for 2D explainer graphics.
3. **Puppeteer Zombie Prevention**: If a render process is cancelled or times out, check for orphaned Chromium processes (`pgrep -f chrome`) to avoid memory leaks on long-running servers.
