---
name: faceless-video-generator
description: Use when generating Faceless 3D Shorts (Loopra alt).
category: youtube-operations
---

# Faceless Video Generator (Loopra Alternative)

A complete, zero-cost, server-side pipeline to generate 9:16 high-retention Faceless Animation Shorts.
Golden restore point and reference scripts are stored in `/home/satyaaditech/shorts_factory/restore_points/milo_v1_baseline/`.

## Core Pipeline & Parameters
- **Visuals:** Gemini Image (`antigravity/gemini-3.1-flash-image`) via OmniRoute. Use fixed anchor prompts for consistent characters (e.g. "cute fluffy ginger tabby kitten... 3D Pixar animation style").
- **Audio:** `edge-tts` (`en-US-ChristopherNeural` at `+8%` rate) for exact `.mp3` and `.vtt` timing.
- **Subtitles:** ASS format burned via ffmpeg (`DejaVu Sans`/`Arial`, size 56, yellow `&H0000FFFF`, thick black outline `4.5`, lower third `MarginV=260`).
- **Motion (CRITICAL - The Micro-Jitter Trap):** 
  Do **NOT** use FFmpeg's native `zoompan` for slow Ken Burns (it inherently causes integer-pixel stutter/micro-jitter). Pak Satya has a very sharp visual eye and will reject jittery outcomes.
  **Solution:** Calculate frames using the **Python Pillow Subpixel Pipeline** (`Image.Resampling.BICUBIC` with a floating-point box + SmoothStep curve `3x^2 - 2x^3`). Pipe raw `rgb24` bytes directly into `ffmpeg -f rawvideo` for cinema-quality, buttery-smooth zooming.

## Quota & Failover Handling
- OmniRoute Google CloudCode image quotas exhaust at ~123h delays. If encountering HTTP 429 "RESOURCE_EXHAUSTED" mid-generation, edit `~/.omniroute/storage.sqlite` table `provider_connections` to set `is_active = 0` on the exhausted account so traffic successfully fails over to the next priority helper account.

## Workflow Rules
1. **Mandatory Restore Points:** Always create a frozen baseline backup of the script and assets (like `milo_v1_baseline`) **BEFORE** modifying or fine-tuning any motion params or configurations.
2. Verify all framing inside 1080x1920 boundaries via test extractions.