---
name: youtube-shorts-clipper
description: Complete automated pipeline for YouTube Shorts vertical video clipping (Full 9:16 portrait zoom, verbatim Indonesian hardsubs, complete narrative arcs, Google Sheets tracker, 3-tier fallback midnight scanner, storage clean-up policy, scheduled publishing, and YouTube Data API v3 direct upload to @siswatalkstv).
version: 1.4.0
category: youtube-operations
---

# YouTube Shorts Clipper & Publisher Pipeline

Automated engine to discover golden moments from long-form YouTube videos, crop to pure 9:16 portrait, generate Indonesian hardsubs, track in Google Sheets, schedule/publish to YouTube (@siswatalkstv), and automatically clean up server disk storage.

## 1. Frozen & Immutable Visual Rules
- **Framing:** Full 1080x1920 (9:16 portrait edge-to-edge). No black bars, no blur fills.
- **FFmpeg Filter:** `scale=3414:1920:flags=lanczos,crop=1080:1920:(in_w-1080)/2:0,setsar=1`.
- **Subtitle Styling:** Arial Bold Yellow (`&H0000FFFF`), thick black stroke (`Outline=2.5`), lower third (`MarginV=60`, `Alignment=2`).
- **Narrative Arc:** Complete 3-stage story arc (Hook -> Exploration -> Key Insight, 1-3 minutes).

## 2. Language & Description Protocols
- **Internal Communication:** Basa Jawi Krama Alus.
- **Public Assets (YouTube Title/Description):** 100% Bahasa Indonesia baku. Never use Javanese terms like "dudutan emas" in public text. Use `💡 Kesimpulan Penting:`.
- **Mandatory Attribution:** Must include `Credit: <Channel Source>` at the footer of descriptions.

## 3. Upload Cadence & Scheduling Protocol (Anti-Spam / Max Reach)
- **Optimal Daily Volume:** 2 to 3 Shorts per day per channel (Strict max: 4 per day).
- **Time Spacing (Jeda Antar Upload):** 3 to 4 hours apart to prevent algorithm cannibalization.
- **Golden Time Slots (WIB):**
  - Slot 1 (Siang): 11.30 – 12.30 WIB (Lunch break browsing).
  - Slot 2 (Sore): 16.30 – 17.30 WIB (Commute/after-work browsing).
  - Slot 3 (Malam/Prime): 19.30 – 20.30 WIB (Peak engagement).
- **Scheduled Publishing:** Use `publishAt` ISO 8601 parameter in `youtube_uploader.py` for automated queueing.

## 4. Midnight Watchdog & 3-Tier Fallback Scanner (00:00 WIB)
- **Tier 1 (Utama):** Scan channels with status `AKTIF MONITORED` (Kurzgesagt, TED-Ed, Big Think) for newly uploaded videos.
- **Tier 2 (Cadangan):** If no new uploads on Tier 1, scan channels with status `CADANGAN` (Sprouts, The School of Life, AsapSCIENCE, Einzelgänger, MinutePhysics, Veritasium, Psych2Go).
- **Tier 3 (Arsip Evergreen):** If still no new uploads across all channels, pull unprocessed high-value archive/past videos from the target channels.
- **Output Action:** Extract Golden Moments -> Report detailed breakdown to Telegram -> Append to Google Sheets with status `DITEMUKAN`.

## 5. Google Sheets Control Center
- **Spreadsheet ID:** `1d6Iyj0rZ22_m9CmwJn9XXDoAFqbWoWKKo96Uppsn4Ok`
- **Tab 1 (Pipeline):** Status Dropdown: `DITEMUKAN`, `SIAP RENDER`, `SUDAH DIRENDER`, `ACC`, `SUDAH TAYANG (LIVE)`, `DIABAIKAN`.
- **Tab 2 (Direktori):** Top 10 Target Channels with Monitoring Status (`AKTIF MONITORED`, `CADANGAN`, `DIJEDA`).

## 6. Server Storage Clean-up Policy (Zero-Bloat Lifecycle)
1. **Clip Clean-up:** Immediately after a short clip is successfully uploaded and live/scheduled on YouTube, delete its local `.mp4` from the server.
2. **Raw Source Clean-up:** Once all small clips from a source video have been processed/uploaded/deleted, delete the large raw source video (`video.mp4`/`video.webm`) from the server.
3. **Persistent Records:** Transcripts, metadata, and live URLs remain permanently stored in Google Sheets and Obsidian LLM Wiki.
