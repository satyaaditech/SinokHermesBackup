# Panduan Rancang Bangun Presentasi Web Interaktif (HTML5 Presentation Deck)

Nalika Pak Satya nyuwun materi khotbah/ulasan kadamel dados materi presentasi versi web ("versi web wae ya nox, tapi sing apik ya"), rancang satunggaling aplikasi web presentasi interaktif tunggal (*single-file standalone HTML5 deck*) ingkang nggadhahi standar visual-first & eksekutif:

---

## 1. Prinsip Utama: Visual-First, Minimal Teks, & High-Impact Infografis
- **Tampilan Slide Bersih & Punchy (LOW-TEXT, HIGH-VISUAL)**:
  - Layar slide **TIDAK BOLEH penuh kata-kata atau paragraf panjang**.
  - Tampilkan hanya **poin-poin inti (bullet points singkat/punchy)** dan konsep kunci.
  - Font berukuran besar, tebal, dan sangat jelas terbaca dari kejauhan (proyektor).
  - Perkecualian detail naratif: **Pembicara akan menjelaskan sendiri secara lisan saat presentasi**, sehingga layar slide berfungsi sebagai penuntun visual dan pengunci konsep, bukan naskah bacaan.
- **Kaya Visualisasi, Infografis, Diagram, & Emotikon**:
  - Setiap slide wajib diperkaya elemen visual: Bento Cards, Icon/Emotikon representatif, Diagram Alir (Flow), Blueprint Kamar Batin, Stepping Ladder (3 Tataran), dan Matriks Ringkas.
- **Pethikan Sabda Ringkas ing Layar + Speaker Notes Lengkap**:
  - Di layar slide, kutipan Sabda Suci cukup ditampilkan ringkas 1–2 baris emas di footer/belakang kartu dengan badge sumber kanonikal yang jelas, karena teks lengkapnya akan dibacakan langsung oleh pembicara.
  - Teks lengkap dan panduan alur bicara dimasukkan ke dalam **Panel Pandom Pambicara (Speaker Notes / shortcut tombol `N`)** agar pembicara dapat membacanya setiap saat tanpa mengotori layar presentasi.

---

## 2. Prinsip Teologis & Komparasi: Anti-Cocoklogi & Menghormati Ajaran Lain
- **DILARANG Menjelekkan Agama / Ajaran Lain**:
  - Ajaran Sang Guru Sejati adalah **SESULUH (penerang / penjelas hakikat batiniah)** dan **TEKEN (panyengkuyung)**, bukan untuk mencela, menjelekkan, atau meremehkan ajaran lain.
  - Hindari asumsi negatif atau kata-kata peyoratif seperti "dogma kaku", "ritual kosong", "lelamisan", dsb.
- **Standar Format Perbandingan yang Arif & Bermartabat**:
  - Kolom 1: **Tataran Pamikir Umum / Syariat Formal / Simbolis** (Fokus pada tata laku lahiriah, simbol fisik, dan aturan umum).
  - Kolom 2: **Tataran Kasampurnan lumantar Piwulang Sang Guru Sejati** (Kedalaman makna batiniah, transformasi jiwa nyata, dan pengamalan hidup).
- **DILARANG Cocoklogi / Memaksakan Sabda**:
  - Setiap poin pembaruan harus **nyata, otentik, dan dasar sabdanya jelas** sesuai teks asli *Serat Sasangka Jati, BRSR, TKL, SKH, UUJM*. Jangan memaksakan sabda ke konsep yang tidak ada di dalam teks kanonikal.

---

## 3. Standar Visual & Estetika (Executive Aesthetics)
- **Tema & Palèt Werni**:
  - *Dark Theme Primary*: Deep Obsidian / Navy (`#040812`, `#070D18`, `#0F172A`, `#1E293B`).
  - *Accent & Highlights*: Imperial Gold (`#D4AF37`, `#F59E0B`), Luminous Teal (`#14B8A6`, `#2DD4BF`), Soft Amber.
  - *Card Glassmorphism*: `bg-slate-900/80 backdrop-blur-md border border-gold/30 rounded-2xl`.
- **Tipografi**:
  - Judul & Header: *Cinzel* / *Georgia* (Serif Elegan & Berwibawa).
  - Isi Poin & Label: *Plus Jakarta Sans* / *Inter* (Sans-serif Modern, Kontras Tinggi).
  - Sabda Emas: *Font-serif italic gold*.

---

## 4. Fitur Interaktif Standar Deck Web
1. **Navigasi Keyboard Penuh**:
   - `Arrow Right` / `Space` / `PageDown`: Slide salajengipun.
   - `Arrow Left` / `PageUp`: Slide sadèrèngipun.
   - `F`: Toggle Fullscreen.
   - `O`: Toggle Overview Modal (Grid seluruh slide untuk lompat cepat).
   - `N`: Toggle Speaker Notes Drawer (Pandom Pambicara).
   - `Esc`: Tutup seluruh modal/overlay.
2. **Top & Bottom Bar Responsif**:
   - Header: Judul topik, live animated dot, progress bar visual, indikator slide (`01 / 22`), tombol aksi (Daftar `O`, Pandom `N`, Layar Kebak `F`).
   - Footer: Tombol navigasi manual, shortcut helper hint, judul slide aktif.
3. **Penyimpanan Berkas**:
   - Path utama: `/home/satyaaditech/share/materi_khotbah/presentasi_panembah.html` (dan `index.html`).
   - Akses lokal: `http://192.168.0.112:8000/materi_khotbah/presentasi_panembah.html`.
