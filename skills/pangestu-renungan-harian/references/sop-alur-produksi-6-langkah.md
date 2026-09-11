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
* **Audio Canvas Web App**: Dihasilkan via aplikasi Gemini Audio Canvas: [https://share.gemini.google/Etzg5qoQXqxr](https://share.gemini.google/Etzg5qoQXqxr) (Dual-Voice: Charon kagem Sabda Jawi, Aoede kagem Uraian/Indo/Eng).
* **Poster Infografis**: Dihasilkan oleh Pak Satya via **ChatGPT / DALL-E**.

### Langkah 4: Pemrosesan Asèt oleh Sinox
* Pak Satya mengirimkan berkas Audio (`.wav`/`.mp3`) dan Poster (`.png`/`.jpg`) ke chat Telegram.
* **Jika Audio ada**:
  1. Render video MP4 HD 1080p (background poster infografis beresolusi tinggi + audio Gemini Canvas; tanpa hardsub karena poster sudah memuat teks infografis lengkap).
  2. Upload ke YouTube channel `@siswatalkstv` (status *Public*).
* **Jika Audio tidak ada**:
  - Langkah render video dan upload YouTube dilewati (*skipped*).
* **Pengolahan Poster & Web**:
  - Simpan poster ke `/home/satyaaditech/share/renungan/poster-<topic>-<date>.png`.
  - Update pustaka web via `python3 /home/satyaaditech/share/pustaka/build_pustaka.py`.
* **Pengolahan Google Doc Baku**:
  - Buat Google Doc resmi di folder *Materi Olahrasa* (`1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U`).
  - **Halaman 1**: Header tanggal, `RENUNGAN PENYISWAAN`, Judul Utama, dan **Poster Infografis proporsional (lebar 320pt / 70-75%)** dipusatkan (center), diakhiri **Page Break**.
  - **Halaman 2**: Salam, Pethikan Sabda/Wejangan (indent 24pt italic), Uraian, Praktik, Renungan, Aplikasi, Penutup Satuhu, dan Footer link aktif.
* **Sinkronisasi**:
  - Update Master Google Sheet `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0` (tab *Rekap Renungan*).

### Langkah 5: Produk Akhir (Final Delivery WhatsApp-Ready)
* Sinox menyajikan naskah final di dalam format ` ```text ` code block terpisah per versi bahasa, lengkap dengan 3 tautan digital wajib:
  - Header: Tanggal, `RENUNGAN PENYISWAAN`, Judul Tematik, dan Tautan YouTube.
  - Body: Salam Karahayon, Pethikan Sabda/Wejangan BRSR, Terjemahan, Uraian, Praktik, Renungan, Aplikasi, dan Penutup Satuhu.
  - Footer (3 Tautan Digital Wajib):
    `• 📺 Video YouTube : https://youtu.be/...`
    `• 📄 Versi Google Doc : https://docs.google.com/document/d/...`
    `• 🌐 Pustaka Web Kontemplasi : https://kontemplasi.satyaaditech.web.id/#<slug>`

### Langkah 6: Paresikan Redaksi Wajib (DILARANG Ditampilkan)
* ❌ `"📖 Waos naskah jangkep wonten ing Pustaka Kontemplasi: ..."` (Dihapus total).
* ❌ `"✅ Dapat dipraktikkan di mana saja dan kapan saja..."` (Dihapus total).
* ❌ Label footer berantakan / tidak ada link web kontemplasi. Tiga link (YouTube, Doc, Web) wajib selalu lengkap.

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
