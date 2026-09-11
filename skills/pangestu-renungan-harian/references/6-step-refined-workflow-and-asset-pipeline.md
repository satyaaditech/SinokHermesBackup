# SOP Produksi Renungan Harian (6 Langkah Baku & Asset Pipeline)

## 📌 6 Langkah Baku (Wajib Dipatuhi Runtut & Tanpa Lompat)

### Langkah 1: Draft Awal Bahasa Indonesia Saja (Review & Kurasi)
- Susun draf naskah awal **HANYA dalam Bahasa Indonesia**.
- DILARANG membuat versi bahasa Inggris/Jawa sebelum naskah Indonesia di-ACC.
- **DILARANG membuat Google Doc** dan **DILARANG memasukkan ke Web Library / GitHub Pages**.
- Draf disajikan ke chat Telegram untuk ditinjau oleh Pak Satya.
- Setelah Pak Satya memberikan **ACC**, Sinox **wajib bertanya/menawarkan**:
  > *"Versi bahasa apa saja yang ingin diproduksi dinten punika? (Indonesia saja / English / Jawa / Dua-duanya / Ketiganya)?"*

---

### Langkah 2: Naskah Polos Tanpa Link (Menunggu Aset Media)
- Setelah Pak Satya memilih versi bahasa yang diinginkan, Sinox menyajikan naskah lengkap masing-masing bahasa dalam format code block ```text.
- **PENTING**: Di dalam code block pada tahap ini **BELUM ada tautan apa pun** (TIDAK ada link Google Doc, Web Library, atau YouTube).
- Isi teks sudah komplit (Sabda verbatim, terjemahan, uraian, 3 praktik harian, renungan, 3 aplikasi, doa penutup).
- **Aturan Redaksi Bersih**:
  - ❌ **HAPUS TOTAL**: Baris `"📖 Waos naskah jangkep wonten ing Pustaka Kontemplasi: ..."`
  - ❌ **HAPUS TOTAL**: Baris `"✅ Dapat dipraktikkan di mana saja dan kapan saja..."`

---

### Langkah 3: Produksi Audio & Poster oleh Pak Satya (Eksternal)
- **Audio Dual-Voice**: Pak Satya memproses naskah di **Gemini Canvas App** (suara Charon untuk Sabda Jawi, suara Aoede untuk narasi Indonesia/Inggris). Menghasilkan file audio (`.wav` / `.mp3`).
- **Poster Infografis**: Pak Satya membuat poster gambar di **ChatGPT / DALL-E**. Menghasilkan file poster (`.png` / `.jpg`).

---

### Langkah 4: Pemrosesan Aset & Audiovisual oleh Sinox
Pak Satya mengirimkan file Audio dan Poster ke chat Telegram. Sinox menjalankan otomasi:
1. **Render Video HD (FFmpeg 1080p Still-Image Optimization)**:
   - Background blurred 1920x1080 + Foreground centered portrait poster (tinggi 1000px):
     ```bash
     ffmpeg -y -loop 1 -framerate 1 -i poster.png -i audio.mp3 \
       -filter_complex "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=20:10[bg];[0:v]scale=-1:1000[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
       -r 5 -c:v libx264 -preset ultrafast -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest output.mp4
     ```
2. **Upload YouTube Channel `@siswatalkstv`**:
   - Jalankan `upload_youtube.py` (status: `public`).
   - Ambil tautan video YouTube (`https://youtu.be/...`).

---

### Langkah 5: Penerbitan Google Doc, Web Library & Master Sheet
1. **Google Docs Resmi**:
   - Upload poster ke Google Drive folder `1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U` (Materi Olahrasa) dan share viewer (`reader/anyone`).
   - Masukkan gambar via Docs API `insertInlineImage` (`https://lh3.googleusercontent.com/d/<file_id>`, 320pt x 480pt centered).
   - **Halaman 1**: Judul H1 + Poster Infografis (center) + *Page Break*.
   - **Halaman 2**: Konten artikel (Sabda indent 24pt, Uraian, Praktik, Renungan, Aplikasi, Satuhu) + Link aktif YouTube & Web di footer.
2. **Pustaka Web & Build (Sync GitHub Pages)**:
   - Simpan `.md` ke `/home/satyaaditech/share/renungan/renungan-<slug>-<lang>-YYYY-MM-DD.md`.
   - Jalankan `/home/satyaaditech/kontemplasi/sync_to_github.sh` (otomatis rsync asèt, build `index.html`, commit, lan push menyang GitHub Pages `kontemplasi.satyaaditech.web.id`).
3. **Master Google Sheet Auto-Append**:
   - Catat seluruh metadata dan aset ke Google Sheet `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0` tab `Rekap Renungan` (No, Tanggal, Hari & Pasaran, Bahasa, Judul Tematik, Sumber Kitab, Pethikan Sabda, GDoc, YouTube, Web, Audio, Status).

---

### Langkah 5: Produk Akhir WhatsApp-Ready (Semua Tautan Aktif)
Sinox mengembalikan naskah final dalam format ```text code block siap sebar ke WhatsApp dengan tautan lengkap:
- **Header**: Tanggal + Judul Tematik + `📺 Video YouTube : https://youtu.be/...`
- **Isi**: Salam, Sabda Verbatim, Terjemahan, Uraian, Praktik, Renungan, Aplikasi, Penutup.
- **Footer (3 Tautan Digital Wajib)**:
  ```text
• 📺 Video YouTube : https://youtu.be/...
• 📄 Versi Google Doc : https://docs.google.com/document/d/.../edit
• 🌐 Pustaka Web Kontemplasi : https://kontemplasi.satyaaditech.web.id/#slug
  ```
