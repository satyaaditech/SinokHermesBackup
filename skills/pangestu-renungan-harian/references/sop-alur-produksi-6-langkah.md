# SOP Produksi Renungan Harian (6 Langkah Baku) & Panduan Human Creative

Panduan ini mengatur standar alur kerja (workflow) dan standar penulisan *Human Creative* untuk produksi Renungan Penyiswaan Pangestu.

---

## 1. Alur Produksi 6 Langkah Baku (SOP Wajib)

### Langkah 1: Draft Awal Bahasa Indonesia (Wajib Code Block)
* Sinox menyusun draf naskah awal **HANYA dalam Bahasa Indonesia**.
* Draf disajikan murni di dalam format ` ```text ` code block agar mudah di-copy paste oleh Pak Satya.
* DILARANG membuat versi bahasa lain sebelum draf Bahasa Indonesia di-ACC.
* Kirimkan draf ke chat dan tunggu kurasi dari Pak Satya.
* Setelah Pak Satya memberikan **ACC**, Sinox WAJIB bertanya/menawarkan pilihan versi bahasa yang ingin diproduksi (Indonesia saja / English / Jawa / Kombinasi).

### Langkah 2: Naskah Polos Tanpa Link (DILARANG Buat Doc/Web Sebelum ACC)
* **SEBELUM ACC**: DILARANG membuat Google Doc dan DILARANG memasukkan ke Web Library/GitHub Pages. Hal ini mencegah kerja berkali-kali jika ada revisi redaksi.
* Setelah ACC & pemilihan bahasa: Sinox menyajikan naskah lengkap dalam format ` ```text ` code block tersendiri untuk masing-masing bahasa yang diminta.
* **PENTING**: Di dalam code block pada tahap ini **BELUM ada link apa pun** (tidak ada link Google Doc, Web Library, atau YouTube). Konten sudah komplit murni teks.

### Langkah 3: Produksi Audio & Poster oleh Pak Satya
* **Audio**: Dihasilkan oleh Pak Satya via **Gemini Canvas App** (Dual-Voice Charon/Aoede).
* **Poster Infografis**: Dihasilkan oleh Pak Satya via **ChatGPT / DALL-E**.

### Langkah 4: Pemrosesan Asèt oleh Sinox
* Pak Satya mengirimkan berkas Audio (`.wav`/`.mp3`) dan Poster (`.png`/`.jpg`) ke chat Telegram.
* **Jika Audio ada**:
  1. Render video MP4 HD 1080p (background dari poster, audio dari Canvas, subtitle `.ass` bottom-center).
  2. Upload ke YouTube channel `@siswatalkstv` via `upload_youtube.py` (`--privacy public`) dan ambil share link `https://youtu.be/...`.
* **Jika Audio tidak ada**:
  - Langkah render video dan upload YouTube dilewati (*skipped*).
* **Pengolahan Poster & Web**:
  - Simpan poster ke `kontemplasi/renungan/poster-<topic>-<date>.png`.
  - Update `build_pustaka.py` agar poster muncul di bagian atas artikel saat kartu diklik (dengan fitur lightbox zoom).
* **Pengolahan Google Doc**:
  - Buat Google Doc resmi dengan teks bersih tanpa simbol markdown mentah (`*`, `**`, `###`).
* **Sinkronisasi**:
  - Build web `build_pustaka.py` dan jalankan `sync_to_github.sh`.
  - Update Master Google Sheet `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`.

### Langkah 5: Produk Akhir (Final Delivery WhatsApp-Ready)
* Sinox menyajikan naskah final di dalam format ` ```text ` code block terpisah per versi bahasa, lengkap dengan seluruh tautan aktif:
  - Header: Tanggal, Judul, dan Tautan YouTube (jika ada video).
  - Body: Salam, Sabda Hari Ini, Terjemahan, Uraian, Praktik, Renungan, Aplikasi, dan Penutup Satuhu.
  - Footer: Tautan YouTube (jika ada), Google Doc, dan Web Library.

### Langkah 6: Paresikan Redaksi Wajib (DILARANG Ditampilkan)
* ❌ `"📖 Waos naskah jangkep wonten ing Pustaka Kontemplasi: ..."` (Dihapus total).
* ❌ `"✅ Dapat dipraktikkan di mana saja dan kapan saja..."` (Dihapus total).

---

## 2. Standar Gaya Penulisan Human Creative (Anti-AI Slop)

1. **Anti-AI Slop**:
   - Hindari frasa pembuka klise buatan AI seperti *"Dalam panggung kehidupan yang serba cepat..."*, *"Merupakan pilar fundamental..."*, *"Di era modern yang penuh hiruk pikuk..."*.
   - Awali dengan pertanyaan reflektif atau situasi nyata sehari-hari yang dekat dengan pengalaman manusia (*relatable & conversational*).

2. **Storytelling & Analogi Nyata**:
   - Sertakan analogi nyata (misal: ketelitian perajin jam mekanik klasik, metafora alam seperti samudra/pohon beringin) atau kutipan/kisah tokoh inspiratif (seperti integritas Warren Buffett, ketenangan tokoh sejarah).
   - Analogi berfungsi menjembatani teori kasampurnan/olah rasa agar mudah dipahami tanpa mengurangi kedalaman maknanya.

3. **Nge-flow & Tidak Menggurui**:
   - Bahasa mengalir luwes, hangat, penuh rasa persaudaraan dan welas asih.
   - Tidak bersikap menggurui, menghakimi, atau terjebak dalam dikotomi usia/profesi.
   - Tetap membawa *deep insight* batin yang bersumber dari kemurnian ajaran Sang Guru Sejati.
