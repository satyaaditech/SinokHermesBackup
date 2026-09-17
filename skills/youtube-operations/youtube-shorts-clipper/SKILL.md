---
name: youtube-shorts-clipper
description: Complete automated pipeline for YouTube Shorts vertical video clipping (Full 9:16 portrait zoom, verbatim Indonesian hardsubs, complete narrative arcs, local fine-tuning discipline, pure Indonesian public metadata).
category: youtube-operations
---

# YouTube Shorts Clipper Playbook

## Core Principles & Hard Constraints
1. **Full 9:16 Edge-to-Edge Portrait Fill:**
   * MUST fill entire vertical screen (1080x1920) without black bars, letterboxing, pillarboxing, or blur backgrounds.
   * Locked scaling & center crop: `scale=3414:1920:flags=lanczos,crop=1080:1920:(in_w-1080)/2:0,setsar=1`.
2. **Accurate Verbatim Indonesian Hardsubs:**
   * Font: Arial Bold, Yellow (`&H0000FFFF`), thick black border (`Outline=2.5`), placed at bottom third (`MarginV=60`, `Alignment=2`).
   * Subtitle text must translate verbatim and synchronize strictly with spoken dialogue.
3. **Complete Story Arc (No Mid-Thought Cutoffs):**
   * High retention Golden Moments MUST include:
     - **Hook:** Engaging question/problem.
     - **Body:** Case study/process/mechanism.
     - **Resolution/Punchline:** Complete answer/insight.
   * Flexible duration: 60s to 180s (1 to 3 minutes) — prioritize complete story over rigid timestamps.
4. **Language Protocol for Public vs Internal:**
   * **Basa Jawi Krama Alus:** STRICTLY for internal communication with Pak Satya.
   * **Bahasa Indonesia Baku:** STRICTLY for public-facing assets (YouTube Titles, Descriptions, Community Posts, Captions). NEVER use Javanese terms like "dudutan emas" in YouTube descriptions — use "💡 Kesimpulan Penting:" or "💡 Poin Kunci:".
5. **Local Fine-Tuning Discipline (STRICT NO OVER-REACTING):**
   * When asked to tweak a specific parameter (e.g. timeframe/duration or description wording), ONLY adjust that single parameter locally.
   * NEVER alter approved working filters, crop math, styling, or video templates that already passed inspection.
6. **Telegram Delivery Optimization:**
   * Encode with `-crf 26-28` to keep file size under 8 MB so Telegram Bot API delivers instantly without hitting the 20s network timeout.

## Proven Production Scripts
- Video Generator: `/home/satyaaditech/youtube_clipper_lab/shorts_generator.py`
- End-to-End Pipeline: `/home/satyaaditech/youtube_clipper_lab/auto_clipper_pipeline.py`
- YouTube Uploader: `/home/satyaaditech/youtube_clipper_lab/youtube_uploader.py`
