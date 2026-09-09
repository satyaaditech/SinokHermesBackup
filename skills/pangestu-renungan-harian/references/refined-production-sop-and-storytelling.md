# Panduan Baku SOP Produksi Renungan Harian & Human Creative Storytelling

## 1. Alur Kerja 6 Langkah Baku (Refined SOP)

### Langkah 1: Draft Awal Bahasa Indonesia (Wajib Format Code Block)
- Sinox menyusun draf naskah awal **HANYA dalam Bahasa Indonesia**.
- Draf naskah **WAJIB selalu disajikan di dalam format code block (` ```text `)** tersendiri agar mudah di-copy-paste oleh Pak Satya.
- Belum membuat versi bahasa lain sebelum naskah Indonesia di-kurasi/di-ACC.
- Setelah draf disetujui (ACC), Sinox wajib bertanya/menawarkan versi bahasa apa yang ingin dibuat selanjutnya (Indonesia saja, English, Jawa, atau kombinasi).

### Langkah 2: Naskah Komplit Polos Tanpa Link (DILARANG Buat Doc/Web Terlebih Dahulu)
- **Sebelum ACC**: DILARANG membuat Google Doc resmi dan DILARANG memasukkan ke Web Library/GitHub untuk menghindari pekerjaan berulang jika ada revisi redaksi.
- Setelah ACC & bahasa dipilih: Sajikan naskah lengkap dalam format ```text code block terpisah untuk masing-masing bahasa yang diminta.
- **Penting**: Pada tahap ini di dalam code block **BELUM ADA LINK APAPUN** (tanpa link YouTube, tanpa link Google Doc, tanpa link Web Library).

### Langkah 3: Produksi Audio & Poster oleh Pak Satya
- **Audio Voiceover**: Diproduksi mandiri oleh Pak Satya via **Gemini Canvas App** (Dual-Voice Charon & Aoede).
- **Poster Infografis**: Diproduksi mandiri oleh Pak Satya via **ChatGPT / DALL-E**.

### Langkah 4: Pemrosesan Aset & Kondisi Khusus (Audio Ada vs Audio Kosong)
- Pak Satya mengirimkan file Poster (`.png`/`.jpg`) dan file Audio (`.wav`/`.mp3` jika ada) ke chat Telegram.
- **Jika Audio Ada**:
  1. Render video Full HD 1080p dengan audio Gemini Canvas + hard-sub rapi di bagian bawah (`Alignment: 2`, `MarginV: 80-120`).
  2. Upload video ke YouTube `@siswatalkstv` dan ambil link share `https://youtu.be/...`.
- **Jika Audio Tidak Ada (Hanya Gambar Poster)**:
  - Lewati (skip) proses render video dan upload YouTube.
  - Jangan menambahkan baris YouTube di header/footer naskah.
- **Untuk Poster**:
  - Salin file poster ke `/home/satyaaditech/kontemplasi/renungan/poster-<topic>-<lang>-<date>.png`.
  - Rebuild pustaka web (`python3 build_pustaka.py`) agar poster otomatis muncul di header artikel saat kartu artikel diklik (tersedia fitur lightbox zoom).
- **Untuk Dokumen & Web**:
  - Buat Google Doc resmi dengan format teks bersih (tanpa simbol markdown mentah seperti `*`, `**`, `###`).
  - Update `.md` di `/home/satyaaditech/kontemplasi/renungan/` dan sync ke GitHub Pages (`bash sync_to_github.sh`).
  - Catat riwayat aset di Master Google Sheet `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`.

### Langkah 5: Pengiriman Naskah Final (WhatsApp-Ready Code Block)
- Sajikan naskah final di dalam ```text code block lengkap dengan semua link aktif yang relevan:
  - Header: Tanggal + `*RENUNGAN PENYISWAAN*` + Judul Tematik (+ `📺 Video YouTube` jika ada video).
  - Body: Salam, Sabda Hari Ini, Uraian, Praktik, Renungan, Aplikasi, Penutup `Satuhu. 🙏`.
  - Footer: Tautan Google Doc, Web Library (+ YouTube jika ada).

---

## 2. Standar Gaya Bahasa "Human Creative" (Anti-AI Slop)

1. **Hindari Kalimat Klise AI**:
   - ❌ *\"Dalam panggung kehidupan yang serba cepat dan dinamis...\"*
   - ❌ *\"Merupakan pilar fundamental yang sangat krusial...\"*
   - ❌ *\"Mari kita selami lebih dalam esensi dari ajaran ini...\"*
   - ✔️ Gunakan pembuka yang langsung menyapa pengalaman batin pembaca (*relatable, reflective, conversational*).

2. **Analogi Sederhana & Kisah Nyata Inspiratif**:
   - Selalu hubungkan ajaran falsafah/spiritual dengan analogi membumi (misalnya: ketelitian pembuat jam mekanik, kejernihan air danau, pohon beringin yang kokoh menahan badai) atau pemeo/kisah integritas tokoh ternama (Warren Buffett, tokoh sejarah, perajin tradisional).

3. **Flow Enak & Tidak Menggurui**:
   - Tulisan mengalir hangat, penuh kebajikan (*wisdom*), bersahabat (*companionable*), namun tetap menyentuh kesadaran batin (*deep insight*).

4. **Paresikan Redaksi Wajib**:
   - ❌ DILARANG menyertakan kalimat: `\"✅ Dapat dipraktikkan di mana saja dan kapan saja...\"`
   - ❌ DILARANG menyertakan kalimat penutup: `\"📖 Waos naskah jangkep wonten ing Pustaka Kontemplasi: ...\"`
