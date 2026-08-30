# Panduan Rendering Newsletter Multi-Halaman (A4 & HP Carousel)

Berikut adalah panduan teknis dan estetika hasil evaluasi pembuatan newsletter renungan kesiswaan berbasis HTML-to-Image/PDF (menggunakan Puppeteer).

---

## 1. Bahasa Humanis & Kesan Piwulang (Anti-Flat) 🎭

* **Judul Tema**: Wajib menyematkan nama metafora piwulang Sang Guru Sejati dari kitab (seperti *Sungai Nafsu*, *Air Angen-Angen*, *Jalan Rahayu*, *Tri Sila*) untuk memperkuat identitas kepangestuan.
* **Pembuka Uraian**: Hindari penjelasan teoritis atau langsung masuk ke struktur ajaran di awal paragraf yang menyebabkannya terasa "flat" dan kering. Mulailah dengan cerita/kisah nyata sehari-hari yang hangat (misal obrolan dengan tetangga atau saudara seputar masalah ekonomi riil), baru kemukakan solusinya secara bertahap melalui petunjuk Sang Guru Sejati.

---

## 2. Multi-halaman & Penanganan Pemotongan Konten (Border Collision) 📏

* **Jumlah Halaman**: Jika teks renungan panjang secara keseluruhan (terdiri atas Sabda, Uraian, Praktik, Renungan, dan Aplikasi), pisahkan konten secara proporsional menjadi **3 Halaman**. Jangan memaksakan konten masuk ke 2 halaman yang berakibat teks tertutup border bawah/terpotong (overflow-hidden).
* **Ukuran Standar**:
  * **HP Carousel (PNG)**: Lebar `1200px` dan tinggi `1950px` per halaman.
  * **PDF Cetak A4**: Lebar `210mm` dan tinggi `297mm` per halaman.
* **Margin & Spacing**:
  * Atur padding bottom `.content-wrapper` minimal `80px` (untuk HP) atau `15mm` (untuk A4) agar pertanyaan refleksi atau doa penutup tidak menabrak ornamen lingkaran sudut bawah dan garis border luar.
  * Gunakan `page-break-after: always;` di CSS pada kontainer halaman cetak PDF.

---

## 3. Penanganan Bug Emoji Headless Browser (Unicode Fallback) 🐛

* **Masalah**: Chrome Headless di OS Linux VM sering kali tidak memiliki font emoji bawaan (Noto Color Emoji). Akibatnya, emoji unicode standar seperti `🧘`, `🎯`, `📝`, atau `😟` akan di-render sebagai karakter default sistem yang aneh—seperti lambang kertas/berkas dokumen (`🗎`) atau kotak glif kosong.
* **Solusi**: Gantikan emoji unicode utama di template HTML dengan **inline SVG Icon** minimalis yang tertata rapi. Penggunaan SVG menjamin ikon ter-render dengan tajam pada resolusi apa pun tanpa bergantung pada font sistem.
  * *Contoh SVG Book*: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>`

---

## 4. Penggantian Variabel Dinamis (Replacement) 🔄

* **Global Replacement**: Jika variabel (seperti `{DATE_STR}`) muncul di lebih dari satu tempat (misal di header masing-masing halaman), jangan gunakan `.replace('{DATE_STR}', dateStr)` di JavaScript karena hanya mengganti kemunculan pertama.
* **Solusi**: Gunakan regex global untuk penggantian menyeluruh:
  `html = html.replace(/{DATE_STR}/g, dateStr);`
