# Master Google Sheet & Video Subtitle Production Standards

Dokumen ini mendokumentasikan spesifikasi teknis dan standar operasional untuk integrasi Master Google Sheet Rekap Renungan, standarisasi rendering video hard-subtitle YouTube, serta arsitektur pemisahan video multi-bahasa.

---

## 1. Master Google Sheet Rekap Renungan

Seluruh aset produksi renungan harian dicatat secara terpusat pada Google Sheet master:
* **Spreadsheet ID**: `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`
* **URL**: `https://docs.google.com/spreadsheets/d/1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0/edit`
* **Tab**: `Rekap Renungan`

### Skema Kolom (A - L):
1. **No** (A): Nomer urut publikasi (1, 2, 3, ...)
2. **Tanggal** (B): `YYYY-MM-DD` (contoh: `2026-09-08`)
3. **Hari & Pasaran** (C): Contoh `Selasa Pon`
4. **Bahasa** (D): `Indonesia` / `English` / `Jawa`
5. **Judul Tematik** (E): Judul lengkap renungan
6. **Sumber Kitab & Bab** (F): Contoh `BRSR Bab XXVII (Sura Dira Jayaningrat Lebur Dening Pangastuti)`
7. **Pethikan Sabda Suci** (G): Teks kutipan verbatim sabda
8. **Link Google Doc** (H): URL publik reader Google Doc
9. **Link YouTube Video** (I): URL `https://youtu.be/...` pada channel `@siswatalkstv`
10. **Link Web Kontemplasi** (J): URL deep-link `https://kontemplasi.satyaaditech.web.id/`
11. **Link Audio / Media** (K): URL hosting lokal `http://100.92.237.45:8000/renungan/...`
12. **Status** (L): `Published` / `ACC` / `Draft`

### Otomatisasi Penambahan Baris:
Gunakan `google_api.py sheets append` atau Google Sheets API v4 untuk menyisipkan baris baru setelah video YouTube terunggah.

---

## 2. Standar Rendering Video Hard-Sub & Subtitle (.ass)

### Posisi & Tipografi Subtitle:
* **Alignment**: Wajib `Alignment: 2` (bottom-center). DILARANG menggunakan `Alignment: 5` (center) yang bertabrakan dengan header dan judul di layar ponsel.
* **Vertical Margin (`MarginV`)**: Diset pada `90 - 110` piksel dari tepi bawah.
* **Font**: `DejaVu Sans`, ukuran 44–48pt, tebal, warna teks putih (`&H00FFFFFF`) dengan kotak latar gelap transparan (`BorderStyle=3`, `BackColour=&HB00A1520`, `Outline=12`).
* **Speaker Badge Style**: `DejaVu Sans`, 24–26pt, warna cyan (`&H0099DDFF`), `MarginV: 240 - 260`.

### Pencegahan Font Rusak (Missing Glyphs):
* **Hapus Seluruh Emoji Mentah**: Font FFmpeg Linux default (`DejaVu Sans`) tidak memiliki glyph untuk emoji Unicode modern (seperti 📱, 🌿, 🛑, 🌊, 🙏). Emoji di teks subtitle ASS akan dirender sebagai kotak rusak `⧠`.
* **Gunakan Label Teks Bersih**:
  - `[INTRODUKSI & SALAM]`
  - `[PETHIKAN SABDA JAWI - BRSR]`
  - `[TERJEMAHAN INDONESIA]` / `[ENGLISH TRANSLATION]`
  - `[URAIAN & REFLEKSI]`
  - `[LAMPAH PRAKTIK HARIAN]` / `[DAILY PRACTICE]`
  - `[APLIKASI & REFLEKSI]` / `[DAILY REFLECTION]`
  - `[PENUTUP - SATUHU]`

### Verifikasi Durasi Rendering (Anti-Truncation):
* Sebelum mengunggah ke YouTube, SELALU verifikasi durasi file `.mp4` menggunakan `ffprobe`:
  ```bash
  ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output_video.mp4
  ```
* Pastikan durasi video cocok 100% dengan durasi master audio (misal: 4.8 menit = ~290s, 6.7 menit = ~401s), bukan terpotong di 60-90 detik akibat timeout proses.

---

## 3. Isolasi Bahasa Video YouTube Multi-Bahasa

* **Versi Indonesia**:
  - Narasi Sabda: Charon (Jawa)
  - Narasi Uraian: Aoede (Indonesia)
  - Subtitle: Bahasa Indonesia
  - Tautan YouTube di naskah: Wajib mengarah ke video Indonesia.
* **Versi English**:
  - Narasi Sabda: Charon (Jawa)
  - Narasi Uraian: Aoede (English)
  - Subtitle: English
  - Tautan YouTube di naskah: Wajib mengarah ke video English terpisah.
* Dilarang mencampur tautan video antar versi bahasa.
