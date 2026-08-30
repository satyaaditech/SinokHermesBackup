# Panduan Pembuatan Infografis & Cover Renungan

Panduan ini berisi metode pembuatan kartu infografis (baik secara programmatik/Pillow, generatif/AI, maupun metode gabungan Hibrida) untuk mendukung rilis Renungan Pagi Pangestu dan materi presentasi di grup/thread.

---

## 1. Infografis Programmatik (Pillow Python)
Metode ini adalah pilihan utama (**Gold Standard**) untuk bagan dan infografis informatif karena menghasilkan teks yang tajam, presisi, bebas dari kesalahan ejaan (typo), serta mengikuti estetika tradisional Jawa yang bersih.

### Prinsip Desain:
* **Dimensi**: Paling ideal menggunakan rasio **1200 x 1000 px** (atau 1200 x 800 px) agar cermat dan mudah dibaca di ponsel.
* **Warna**: Menggunakan warna latar belakang terang/lembut (seperti Cream `#FAF9F6` atau Light Gray `#F3F4F6`). Hindari warna yang terlalu gelap/mencolok. Penegas menggunakan Navy Blue (`#1E3A8A`) dan Accent Blue (`#3B82F6`).
* **Bingkai/Border**: Gunakan bingkai ganda minimalis dengan aksen ornamen Jawi (seperti motif kelopak kembang Kawung) di setiap sudutnya.
* **Tipografi**: Judul utama besar dan tebal, sub-informasi (tanggal/kitab) lebih kecil, dan kutipan ayat dimasukkan dalam kotak khusus (*Quote Box*) berkelir biru muda (`#EFF6FF`).
* **Struktur Alur**: Untuk menjelaskan materi (*Andharan*), bagi konten menjadi 3 kolom atau langkah berurutan secara horizontal dengan konektor anak panah yang cermat.

---

## 2. Infografis Kreatif (AI Generative)
Metode ini menggunakan model AI seperti `gemini-3.1-flash-image` untuk menghasilkan poster artistik bertema spiritual.
* **Kelebihan**: Visual sangat indah, estetis, dan modern. Cocok untuk cover dekoratif.
* **Kelemahan**: Ejaan teks dalam gambar akan berantakan/rusak (AI text generation belum sempurna). Hanya berkas visual mentah yang dihasilkan.

---

## 3. Metode Hibrida (Background AI + Overlay Programmatik)
Metode terbaik untuk menggabungkan visual estetis dengan kejelasan seratan. Latar belakang dibuat menggunakan AI generatif, sementara teks Jangkep (Indonesia/Jawa) ditumpuk di atasnya secara programmatik menggunakan Python Pillow.

### Panduan Teknis Penyesuaian Koordinat:
1. **Pengukuran Piksel Otomatis**: Jika visual latar belakang bergeser, gunakan deteksi warna piksel (misal, tingkat kegelapan/kecerahan) untuk menentukan batas kolom secara programmatik daripada memasukkan nilai koordinat statis.
2. **Koordinat Batas Kolom (3 Kolom standar)**:
   * Kolom 1: `col1_x0 = 80`, `col1_x1 = 370` (lebar maks ~290px)
   * Kolom 2: `col2_x0 = 370`, `col2_x1 = 650` (lebar maks ~280px)
   * Kolom 3: `col3_x0 = 650`, `col3_x1 = 944` (lebar maks ~294px)
   * Batas atas teks (`y_top`): Biasanya berkisar di `507` hingga `515` piksel, tergantung tumpang tindih dengan ilustrasi bulat di bagian atas.
3. **Pembersihan/Penutupan Artefak AI**: Gambar hasil generate AI sering kali memiliki artefak berupa garis horizontal kecil di bawah visual sferis/bulat. Atur `y_top` sedikit lebih naik (misal dari 515 ke 507) untuk menutup garis tersebut dengan kotak background teks programmatik atau elemen shape agar terlihat rapi dan bebas cacat.

### Endpoint OmniRoute (mesin Google Image):
`POST http://localhost:20128/v1/images/generations` — body `{"model": "antigravity/gemini-3.1-flash-image", "prompt": "...", "n":1, "size":"1024x1024"}` → JSON `data[0].b64_json` (base64 JPEG). **Wajib `base64.b64decode()` lalu tulis ke file** — API tidak mengembalikan URL, hanya string base64. Gambar bisa lambat (30–70 detik); pakai `timeout >= 120` dan kompilasi ulang (retry) bila 503/timed-out.

### Pitfall penting (teruji 2026-08-19):
Jangan pernah percaya teks yang digambar langsung oleh model AI untuk API — selalu salah eja/berantakan (mis. "PENYERAHAH", "SEGAI A"), dobel heading, artefak garis di tepi kolom. Dua pola yang direkomendasikan:
1. **AI sebatas latar kosong**: prompt minta *"clean empty background, no text or words at all"*, lalu komposit SEMUA teks programmatik dengan Pillow. Ini hasil paling rapi.
2. **Patch template AI**: bila user ingin memakai template infografis AI yang sudah ada (tiga kolom + ilustrasi), timpa area placeholder dengan persegi warna latar yang di-sampling dari piksel di sekitarnya, lalu tulis teks real di atasnya. **Fragile** — artefak tetap muncul di tepi kolom/pembatas dan sulit dihilangkan sekalipun dengan loop `vision_analyze` berulang. Untuk hasil final yang bersih, sarankan user memilih pola 1 (programmatik murni) atau AI-sebagai-latar.

---

## 3. Infografis Hibrida (AI Background + Teks Pillow)
Metode ini **menggabungkan kelebihan keduanya**: latar belakang yang artistik dari AI, ditumpuk dengan teks jangkep yang presisi menggunakan Python Pillow. Ini disukai oleh Pak Satya karena isinya lengkap dan keterbacaan teksnya sempurna.

### Alur Implementasi:
1. **Generate Textless Background**: Minta AI membuat latar belakang spiritual Jawa kosong tanpa teks sama sekali.
   * *Prompt*: `"A beautiful, clean, spiritual Javanese background design for a poster. Soft textured cream background with light-blue and golden watercolor splashes. Minimalist Kawung batik line art in borders. Center is empty, no text."`
2. **Robustness & Fallback**:
   * API dari upstream kadangkala lambat atau mengembalikan status 503. Gunakan terminal background task (`background=True`, `notify_on_complete=True`) dan loop retry exponential backoff.
   * Miliki *programmatic fallback* (warna latar polos `#FAF9F6`) jika API gagal total agar rilis infografis tidak terhenti.
3. **Pillow Overlay**:
   * Muat gambar background hasil AI dan lakukan resize ke resolusi target (1200x1200px).
   * Lakukan *light Gaussian Blur* pada background agar teks menonjol.
   * Gambar kothak *semi-transparent overlay card* dengan warna putih (`#FFFFFFEE` atau `#FFFFFFDD`) sebagai latar belakang teks dan kutipan/quote box.
   * Tumpuk teks asli dengan TrueType font secara presisi dan gunakan `textwrap.fill()` untuk merapikan teks.
