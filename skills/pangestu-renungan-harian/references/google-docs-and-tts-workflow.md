> ⚠️ **CATATAN HISTORIS (SUPERSEDED / OUTDATED)**:
> Berkas ini adalah dokumentasi alur lama (V1–V7). Standar operasional resmi saat ini mengacu pada **SOP Produksi Video Sinematik V8** (`references/sop-produksi-video-sinematik-v8.md`) dan tab Google Sheet **`Master Produksi V8`** (22 kolom). Jangan menggunakan instruksi tab 'Rekap Renungan' atau formula '=HYPERLINK' dari berkas ini.

---

# Alur Google Docs, Web Deep-Linking, Gemini Dual-Voice Audio & Video YouTube Renungan Harian

Referensi ini mendokumentasikan tata cara otomatisasi penyimpanan renungan harian Pangestu ke Google Drive (Google Doc), integrasi Web Portal Deep-Linking, pembuatan versi audio narasi alami ekspresif menggunakan Google Gemini 2.5 Audio Modality (Dual-Voice Character), serta pipa render video hard-subtitles dan upload otomatis ke YouTube channel `@siswatalkstv`.

---

## 1. Alur Google Drive & Google Doc (Penyimpanan Rapi & Tipografi Profesional)

Setiap kali renungan dibentuk, selain disimpan di server lokal, berkas harus diunggah juga ke Google Drive di folder **"Renungan Harian"** (Folder ID: `1Ei8R28btJH6rjCC1lKrfkaCC-KxmKeNW`).

### Standar Tipografi Profesional & Integrasi Poster
Google Doc renungan WAJIB diformat dengan tata letak profesional (bukan plain text mentah):
1. **Tipografi & Font**: Menggunakan font **Georgia** (serif yang anggun dan mudah dibaca).
2. **Hierarki Judul**:
   - Tanggal: Center, 10pt, Bold, Gray (`#718096`).
   - Kategori ("RENUNGAN PENYISWAAN"): Center, 12pt, Bold, Navy (`#0D3B66`).
   - Judul Utama: Center, 18pt, Bold, Navy (`#0D3B66`).
   - Tautan YouTube Video: Center, 10.5pt, Bold Blue (`#2B6CB0`).
3. **Pemasangan Poster Infografis (Inline Image)**:
   - Jika tersedia berkas poster infografis yang sesuai, pasang gambar poster **langsung di dalam Google Doc** tepat setelah Judul / Link Video sebelum naskah Uraian dimulai.
   - Gunakan `insertInlineImage` via Google Docs API dengan URI web publik (`https://kontemplasi.satyaaditech.web.id/renungan/poster-*.png`) dan lebar `460pt`.
4. **Pethikan Sabda & Kutipan**:
   - Format *Italic*, 10.5pt, warna `#2D3748`, dengan indentasi kiri-kanan 24pt (`indentStart: 24`, `indentEnd: 24`) dan spasi baris 1.25x.
5. **Uraian & Paragraf**:
   - Regular, 11pt, warna `#2D3748`, line spacing 1.35x, spasi bawah 8pt.
6. **Praktik & Aplikasi**:
   - Poin bernomor dengan indentasi rapi (`indentStart: 20`).
7. **Pengaturan Izin Akses**:
   - `role`: `'reader'`, `type`: `'anyone'`.

---

## 2. Pembuatan Versi Audio Narasi Alami (Google Gemini 2.5 Dual-Voice Engine)

Para kadang kesiswaan (terutama para sesepuh) menyukai renungan berformat audio yang ekspresif, hangat, dan alami (bukan suara robot TTS datar). Gunakan **Google Gemini 2.5 Flash Preview TTS API** (`models/gemini-2.5-flash-preview-tts`):

### Konfigurasi Wajib Anti-Redundansi / Anti-Looping:
1. **`temperature: 0.0`**: Wajib diset `0.0` agar generasi audio 100% presisi verbatim sesuai teks, tanpa perulangan kalimat atau variasi acak.
2. **`systemInstruction`**:
   `"You are a professional voiceover narrator. Read the provided text aloud exactly as written, verbatim, word-for-word. Do not repeat any sentence, phrase, or word. Do not add introductory or concluding commentary."`
3. **Pemisahan 2 Karakter (Dual-Voice Character & 2-Call Batching)**:
   - **Karakter 1 (`Charon`)**: Khusus membaca **Pethikan Sabda Suci Basa Jawa** murni (Panggilan API 1).
   - **Karakter 2 (`Aoede`)**: Membaca Introduksi, Uraian, Praktik, Renungan, dan Penutup (Bahasa Indonesia / English) (Panggilan API 2).
4. **Pantangan Mutlak Fallback Suara Robot**:
   - DILARANG KERAS beralih (fallback) ke Edge-TTS (jv-ID-DimasNeural, id-ID-GadisNeural) saat Gemini API terkena rate limit/kuota habis. Suara sintetis dinilai kaku dan robotik.
   - Bila kuota habis (Free Tier maks 10 req/hari), sampaikan secara jujur kendala kuota kepada Pak Satya agar dapat di-update dengan API key billing atau menunggu reset harian.
   - **Jedha Wening**: Silent pause 1.5 detik (`silence.wav`).
   - **Karakter 2 (`Aoede` / fallback `id-ID-GadisNeural` / `en-US-GuyNeural`)**: Membaca **Pembuka, Terjemahan Sabda, Uraian Mendalam, Langkah Praktik, Renungan Inti, hingga Penutup Satuhu** (Bahasa Indonesia atau Bahasa Inggris).

### Resilient Audio Pipeline (Gemini TTS & Edge-TTS Fallback)
Jika API Gemini TTS mengalami limit kuota (HTTP 429) atau timeout, segera fallback ke `edge-tts` yang berjalan lokal dan sangat stabil:
```python
import edge_tts
import asyncio

# Javanese Sabda: jv-ID-DimasNeural (rate: -5%, pitch: -2Hz)
# Indonesian Uraian: id-ID-GadisNeural (rate: -4%, pitch: +0Hz)
# English: en-US-GuyNeural / en-US-JennyNeural
async def generate_edge_tts(text, voice, out_mp3, rate="-4%", pitch="+0Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_mp3)
```

---\n\n## 3. Video Hard-Subtitles & YouTube Upload (@siswatalkstv)
1. Render background 1920x1080 (deep ocean gradient) via Pillow.
2. Buat file subtitle `.ass` dengan penanda speaker badge dan timing akurat per segmen audio.
3. Render video MP4 menggunakan FFmpeg:
   ```bash
   ffmpeg -y -loop 1 -i bg_template.png -i master_audio.mp3 -vf "ass=subs.ass" -c:v libx264 -tune stillimage -preset veryfast -crf 22 -c:a aac -b:a 192k -pix_fmt yuv420p -shortest output_video.mp4
   ```
4. Upload otomatis ke YouTube channel `@siswatalkstv`:
   ```bash
   python3 /home/satyaaditech/kontemplasi/upload_youtube.py --file output_video.mp4 --title "Judul Renungan" --desc "Deskripsi jangkep" --privacy public
   ```

4. **Stitching FFmpeg**: Gabungkan Part 1 + Silence + Part 2 ke file `.mp3` dan `.ogg` (voice note).

---

## 3. Pipa Render Video Hard-Subtitle (FFmpeg Lokal) & Upload YouTube

1. **Latar Visual (Pillow 1920x1080)**:
   - Desain latar gradasi *midnight-navy to deep-ocean* tenang (#0f172a ke #092e38).
   - Header: `RENUNGAN PENYISWAAN` di dalam rounded box estetik.
   - Judul Besar & Subjudul tematik + kitab rujukan (misal BRSR XXVII).
   - Footer: `kontemplasi.satyaaditech.web.id • Ajaran Sang Guru Sejati • @siswatalkstv`.
   - Garis pemisah tipis elegan.

2. **Format Subtitel (.ass) & Standar Tipografi Anti-Tabrakan**:
   - **Posisi Ngandhap (`Alignment: 2` / bottom-center)**: Margin vertikal `MarginV: 80 - 120`. Subtitel wajib berada di sepertiga bawah layar agar TIDAK MENUMPUK dengan header/judul di atas.
   - **Pencegahan Karakter Kotak Rusak (`⧠`)**: Dilarang menggunakan raw Unicode emojis di teks `.ass` karena font sistem (DejaVu Sans) tidak merendernya. Gunakan label teks bersih seperti `[SABDA JAWI - BRSR]`, `[TERJEMAHAN]`, `[URAIAN & REFLEKSI]`, `[PRAKTIK HARIAN]`, `[PENUTUP - SATUHU]`.
   - Ukuran font 44–48pt, font bold, dengan background kotak semi-transparan gelap (`BorderStyle=3`, `BackColour=&HB00A1520`).
   - **Sinkronisasi Timestamp via Faster-Whisper**: Jika menerima berkas audio utuh (misal dari Canvas Studio), transkripsikan menggunakan `faster_whisper` (model base/small) untuk mengekstrak timestamp tiap kalimat secara presisi.

3. **Render FFmpeg & Verifikasi Durasi Utuh**:
   - Perintah Render:
     ```bash
     ffmpeg -y -loop 1 -i bg_template.png -i master_audio.wav -vf "ass=subs.ass" -c:v libx264 -tune stillimage -preset veryfast -crf 22 -c:a aac -b:a 192k -pix_fmt yuv420p -t <durasi_detik> output_video.mp4
     ```
   - **Verifikasi Durasi Mutlak**: Selalu periksa durasi output video dengan `ffprobe` sebelum mengunggah. Pastikan durasi video sama persis dengan durasi master audio (jangan sampai terpotong akibat timeout runner).

4. **Multi-Language Video Routing**:
   - Versi Bahasa Indonesia WAJIB menyematkan tautan YouTube video versi Bahasa Indonesia.
   - Versi English WAJIB menyematkan tautan YouTube video versi English (narasi & subtitle bahasa Inggris).
   - Dilarang keras mencampur tautan video antar versi bahasa.

5. **Unggah Otomatis YouTube (@siswatalkstv)**:
   - Gunakan `/home/satyaaditech/kontemplasi/upload_youtube.py` dengan opsi `--file`, `--title`, `--desc`, `--privacy public`.
   - Salin ID video dan tautan `https://youtu.be/<video_id>` ke header dan footer naskah renungan terkait.
   - Footer: `kontemplasi.satyaaditech.web.id • Ajaran Sang Guru Sejati`.
2. **Subtitles & Badges (.ass)**:
   - Format Advanced SubStation Alpha (`.ass`).
   - **Posisi Bawah Layar (`Alignment: 2` / bottom-center)**: Wajib diletakkan di bagian bawah layar (`MarginV: 80 - 120`) agar tidak bertabrakan dengan judul/badge header.
   - **Bebas Emoji Rusak**: DILARANG menyertakan emoji Unicode mentah di dalam teks subtitle `.ass` karena font sistem FFmpeg (seperti DejaVu Sans) tidak merender emoji dan akan memunculkan kotak karakter rusak (`⧠`). Gunakan label teks ASCII bersih seperti `[SABDA JAWI]`, `[URAIAN & REFLEKSI]`, `[PRAKTIK]`.
   - Ukuran font besar (44-48pt), kontras tinggi dengan semi-transparent dark backing box (`BorderStyle=3`) agar sangat mudah dibaca oleh sesepuh di layar HP.
3. **Render Command (FFmpeg) & Verifikasi Durasi**:
   ```bash
   # 1. Verifikasi durasi audio sebelum render
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 master_audio.wav

   # 2. Render video 1080p dengan subtitle hardcoded (.ass)
   ffmpeg -y -loop 1 -i bg_template.png -i master_audio.wav \
     -vf "ass=subs.ass" \
     -c:v libx264 -tune stillimage -preset veryfast -crf 22 \
     -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \
     output_video.mp4

   # 3. Verifikasi durasi video setelah render agar tidak terpotong prematur
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output_video.mp4
   ```

---

## 4. Master Google Sheet Backup & Asset Catalog

Setiap selesai siklus produksi naskah, audio, dan video, tambahkan baris data ke **Master Google Spreadsheet Rekap Renungan**:
- **Spreadsheet ID**: `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`
- **URL**: `https://docs.google.com/spreadsheets/d/1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0/edit`
- **Tab**: `Rekap Renungan`

### Skema Baris Rekap (12 Kolom):
1. `No` (Integer berurutan)
2. `Tanggal` (`YYYY-MM-DD`)
3. `Hari & Pasaran` (misal `Selasa Pon`)
4. `Bahasa` (`Indonesia` / `English` / `Jawa`)
5. `Judul Tematik` (Judul renungan lengkap)
6. `Sumber Kitab & Bab` (misal `BRSR Bab XXVII`)
7. `Pethikan Sabda Suci` (Kutipan verbatim Sabda)
8. `Link Google Doc` (URL Google Doc)
9. `Link YouTube Video` (URL `https://youtu.be/...` sesuai bahasa)
10. `Link Web Kontemplasi` (Deep-link web)
11. `Link Audio / Media` (URL share server / Drive)
12. `Status` (`Published` / `ACC` / `Draft`)

### Script Python Append Data:
```python
import subprocess, json

sheet_id = "1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0"
row_data = [
    new_no, "2026-09-08", "Selasa Pon", "Indonesia",
    "JUDUL RENUNGAN", "SUMBER KITAB", "PETHIKAN SABDA",
    doc_url, yt_url, web_url, audio_url, "Published"
]

cmd = [
    "python3", "/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts/google_api.py",
    "sheets", "append", sheet_id, "'Rekap Renungan'!A:L",
    "--values", json.dumps([row_data])
]
subprocess.run(cmd, check=True)
```

### 4. Routing Video YouTube Multibahasa:
- **Naskah Indonesia**: Wajib ditautkan ke video YouTube Bahasa Indonesia (Charon + Aoede ID + Subtitle ID).
- **Naskah English**: Wajib ditautkan ke video YouTube English terpisah (Charon + Aoede/Jenny EN + Subtitle EN).
- DILARANG menempelkan link video Indonesia ke naskah English atau sebaliknya.
   *Render 4–5 menit memakan waktu hanya ~15–25 detik di laptop server (sangat ringan).*

---

## 4. Upload Otomatis YouTube (@siswatalkstv)

- **Target Channel**: `siswatalks tv` (`@siswatalkstv`, Channel ID: `UC_5RC62vCuO5rKurQAf0OnQ`).
- **OAuth Token**: `/home/satyaaditech/.config/youtube/token.json` (terhubung permanen).
- **Script Uploader**: `/home/satyaaditech/kontemplasi/upload_youtube.py`
  ```bash
  python3 /home/satyaaditech/kontemplasi/upload_youtube.py \
    --file /path/to/renungan_video.mp4 \
    --title "🌊 JUDUL RENUNGAN 🕊️" \
    --desc "Pethikan Sabda Suci saking Serat Sasangka Jati...\n\nWaos naskah jangkep: https://kontemplasi.satyaaditech.web.id/#..." \
    --privacy public
  ```
- **Shareable Link**: Script mengembalikan link pendek `https://youtu.be/<VIDEO_ID>` yang langsung disisipkan ke pesan WhatsApp / Telegram dan web portal.
