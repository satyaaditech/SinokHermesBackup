# Panduan Produksi Renungan Harian: 6-Langkah Baku & Standar Human Creative

Dokumen ini memuat standar operasional prosedur (SOP) baku 6-langkah dan panduan penulisan gaya *human creative* untuk produksi renungan harian Pangestu (Telegram Thread 1096).

---

## 🔄 1. SOP Alur Kerja 6-Langkah Baku

### Langkah 1: Draft Awal Bahasa Indonesia Saja (Wajib Code Block)
* **Aturan**:
  - Sinox HANYA menyusun draf naskah awal dalam **Bahasa Indonesia**.
  - Draf naskah **WAJIB selalu disajikan di dalam format code block (` ```text `)** agar rapi dan mudah di-copy paste oleh Pak Satya.
  - TIDAK membuat versi bahasa lain sebelum draf Indonesia mendapatkan ACC.
  - Jangan menyisipkan tautan apa pun pada tahap draf awal ini.

### Langkah 2: Kurasi & Pemilihan Versi Bahasa (Polos Tanpa Link)
* **Aturan**:
  - **DILARANG** membuat Google Doc dan **DILARANG** memasukkan konten ke Web Library/GitHub sebelum ACC diberikan.
  - Setelah Pak Satya memberikan **ACC**, Sinox wajib menawarkan pilihan versi bahasa:
    1. Bahasa Indonesia saja
    2. Bahasa Indonesia & English
    3. Bahasa Indonesia, English, & Basa Jawi
  - Setelah bahasa dipilih, sajikan naskah lengkap dalam **code block (` ```text `) terpisah untuk masing-masing bahasa**.
  - **PENTING**: Pada tahap ini, di dalam code block **BELUM ADA LINK APAPUN** (tanpa Google Doc, tanpa Web Library, tanpa link YouTube). Naskah murni teks lengkap.

### Langkah 3: Produksi Audio & Poster oleh Pak Satya
* **Audio Narasi**: Diproduksi mandiri oleh Pak Satya menggunakan **Gemini Canvas App** (Dual-Voice Charon/Aoede).
* **Poster Infografis**: Diproduksi mandiri oleh Pak Satya menggunakan **ChatGPT / DALL-E**.

### Langkah 4: Pemrosesan Berkas & Asèt oleh Sinox
* Pak Satya mengirimkan file Audio (`.wav`/`.mp3`) dan file Poster (`.png`/`.jpg`) ke Telegram.
* **Tugas Sinox**:
  1. Render video MP4 Full HD 1080p dengan audio kiriman + hardsub estetik di bagian bawah layar (`Alignment: 2`, `MarginV: 80-120`, font kontras, tanpa karakter emoji mentah).
  2. Upload video ke kanal YouTube `@siswatalkstv` dan ambil tautan bagikan (`https://youtu.be/...`).
  3. Simpan berkas poster ke folder repositori web (`/home/satyaaditech/kontemplasi/renungan/`), update `build_pustaka.py` jika perlu, dan rebuild web library agar poster otomatis muncul di header artikel saat kartu diklik (mendukung fitur lightbox zoom).
  4. Buat dokumen Google Doc resmi berformat bersih (tanpa markdown mentah `*`, `**`, `###`).
  5. Sinkronisasi perubahan web ke GitHub Pages (`sync_to_github.sh`).
  6. Catat rekap ke Master Google Spreadsheet (`1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`).

### Langkah 5: Final Delivery WhatsApp-Ready
* Sinox menyajikan naskah akhir dalam format code block (` ```text `) lengkap dengan seluruh tautan aktif:
  - Header: Tanggal tebal + Judul + `📺 Video YouTube : https://youtu.be/...` (sesuai bahasa)
  - Isi: Sabda Suci + Terjemahan + Uraian + Praktik + Renungan + Aplikasi + Satuhu.
  - Footer: Tautan Google Doc + Tautan Web Library.

### Langkah 6: Pembersihan Redaksi Wajib
* **DILARANG MENAMPILKAN**:
  - ❌ `"📖 Waos naskah jangkep wonten ing Pustaka Kontemplasi: ..."` (Dihapus total).
  - ❌ `"✅ Dapat dipraktikkan di mana saja dan kapan saja..."` (Dihapus total).

---

## ✍️ 2. Standar Gaya Penulisan: Human Creative & Anti-AI Slop

### A. Karakteristik Tulisan Human Creative
1. **Nge-flow & Bersahabat**: Mengalir luwes seperti percakapan hangat seorang sahabat pembelajar, bukan kuliah akademis atau khotbah yang kaku.
2. **Menghindari Klise AI**:
   - Hindari: *"Dalam panggung kehidupan yang serba cepat dan kompetitif..."*
   - Hindari: *"Merupakan pilar fundamental yang sangat krusial..."*
   - Hindari: *"Mari kita renungkan betapa pentingnya..."*
   - Gunakan: Pembuka yang langsung menyentuh pengalaman nyata sehari-hari (*"Pernahkah kita merasa gelisah sepanjang hari hanya karena satu hal sepele..."*).
3. **Analogi Sederhana & Kisah Nyata Inspiratif**:
   - Jelaskan konsep spiritual abstrak dengan metafora nyata (perajin jam mekanik, tukang kayu kuno, aliran air sungai, pohon beringin, nelayan, dll.).
   - Angkat keteladanan tokoh sejarah/publik (Warren Buffett, ilmuwan, filsuf) mengenai integritas, kesabaran, dan ketulusan.
4. **Deep Insight Tanpa Menggurui**:
   - Sajikan perenungan mendalam dengan nada mengajak berefleksi bersama, bukan menghakimi atau menggurui.
   - Sambungkan ajaran Sang Guru Sejati (SGS) dengan solusi atas kegelisahan batin manusia modern.

---

## 📝 3. Contoh Template WhatsApp Code Block

```text
*HARI, TANGGAL TAHUN*

*RENUNGAN PENYISWAAN*

⚖️🕯️ *JUDUL TEMATIK LENGKAP* 🛡️🕊️✨

_Salam Bahagia Bp/Ibu/Sdr semuanya,_

*📖 SABDA HARI INI :*

[Sumber Buku & Bab] : _"[Kutipan Sabda Verbatim 100%]"_

Terjemahan : _"[Terjemahan Bahasa Indonesia yang laras]"_

💭 *URAIAN :*

[Pembuka relatable / kisah nyata / analogi sederhana]

[Uraian ajaran Sang Guru Sejati yang mendalam dan solutif]

[Refleksi batin yang menenangkan dan membebaskan]

🧘 *PRAKTIK :*

Langkah hening melatih batin hari ini:
1. [Poin praktik 1 yang terukur dan aplikatif] ⏰
2. [Poin praktik 2 tentang integritas/tindakan nyata] 🛡️
3. [Poin praktik 3 tentang keheningan tutur kata/pikiran] 🕯️

🎯 *RENUNGAN :*

[Kalimat sari pati kebijaksanaan 1-2 baris]

📝 *APLIKASI :*

1. [Pertanyaan refleksi 1] 💭
2. [Pertanyaan refleksi 2]
3. [Pertanyaan refleksi 3]

🙏 Semoga kita semua senantiasa dalam Lindungan dan Bimbingan Kasih Sang Guru Sejati. Satuhu. 🙏
```
