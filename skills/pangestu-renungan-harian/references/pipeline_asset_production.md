# Supporting Reference: End-to-End Asset Production & Multi-Platform Pipeline

When Pak Satya provides audio (`.mp3`/`.wav`) and poster infografis image (`.png`/`.jpg`):

## 1. Dual-Voice Audio Script Format (for Gemini Audio Canvas)
- **Aoede**: Warm, clear female narration for intros, explanations, practical exercises, reflection questions, real-life applications, and closing.
- **Charon**: Deep, calm, authoritative male voice for verbatim holy scripture recitation.
- Audio script must be clean plain text without markdown links or formatting artifacts.

## 2. Poster Infografis (9:16 Portrait)
- Dimensions: 1200x2000 px or 1024x1536 px.
- Structure: Header badge, massive central title, visual focal illustration (lantern, tree, nature), clean essence blocks, practical points, footer credits.

## 3. Automation Execution Steps
1. **Save Files**:
   - Copy audio to `~/share/renungan/audio_YYYY-MM-DD.mp3`
   - Copy poster to `~/share/renungan/poster-<slug>-YYYY-MM-DD.png` and `~/kontemplasi/renungan/`
2. **Video Rendering (FFmpeg)**:
   - Probe exact audio duration using `ffprobe`.
   - Render video using ultrafast preset, `-r 2`, `-pix_fmt yuv420p`, `-t <duration>` to `~/share/renungan/renungan_YYYY-MM-DD.mp4`.
   - Verify generated video duration matches audio within 1.0s.
3. **YouTube Upload**:
   - Call `/home/satyaaditech/kontemplasi/upload_youtube.py` with title (<95 chars) and description containing holy scripture excerpt, summary, and links.
4. **Google Doc Generation**:
   - Upload poster to Google Drive folder *Materi Olahrasa* (`1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U`) and set permissions `anyone:reader`.
   - Create Google Doc with title `Renungan Penyiswaan - <TITLE> (<DATE>)`.
   - Page 1: Date + Category + Title + Center 320pt Poster Image + PageBreak.
   - Page 2: Salam + Scripture (indented 24pt) + Uraian + Praktik + Renungan + Aplikasi + Closing + Footer Links.
   - Set font to Georgia, 1.35x line spacing, professional coloring.
5. **Pustaka Web Sync**:
   - Save markdown to `~/kontemplasi/renungan/renungan-<slug>-ind-YYYY-MM-DD.md`.
   - Run `python3 /home/satyaaditech/kontemplasi/build_pustaka.py`.
   - Run `/home/satyaaditech/kontemplasi/sync_to_github.sh`.
6. **Master Sheet Logging**:
   - Append new row to `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0` tab `Rekap Renungan`.
7. **WhatsApp Broadcast Delivery**:
   - Send complete text block inside ` ```text ` with all 3 active links (YouTube, Google Doc, Web).
