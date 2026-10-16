# Master Google Sheet & Video Production Standards (V8 Standar Baku)

Dokumen ini mendokumentasikan spesifikasi teknis dan standar operasional untuk integrasi Google Sheet `Master Produksi V8`, standarisasi rendering video vertikal 9:16 sinematik YouTube Shorts, serta standarisasi subtitle, tipografi Montserrat 62, Ken Burns motion, dan vokal dual-voice kontemplatif.

---

## 1. Master Google Sheet Produksi (V8 Lean 22-Kolom)

Seluruh aset produksi renungan harian dicatat secara terpusat pada Google Sheet master:
* **Spreadsheet ID**: `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`
* **URL**: `https://docs.google.com/spreadsheets/d/1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0/edit`
* **Tab Resmi**: `Master Produksi V8` *(Catatan: Tab lama 'Rekap Renungan' 12-kolom sampun superseded/ditutup)*

### Skema 22 Kolom Baku (A - V):
1. **No** (A)
2. **Tanggal Rilis WA** (B): `YYYY-MM-DD`
3. **Hari & Pasaran** (C): Contoh `Sabtu Kliwon`
4. **Bulan** (D)
5. **Tema Bulanan** (E)
6. **Tema Mingguan** (F)
7. **Judul Renungan** (G)
8. **Rujukan Kitab** (H): Kode kitab kanonikal + Bab/Pasal
9. **Kutipan Asli** (I): Sabda verbatim 100%
10. **Terjemahan** (J): Terjemahan Indonesia
11. **Pangilon Rasa** (K): 2 paragraf padat (Human Hook + Bedhah Kasunyatan)
12. **Laku Panyiswan** (L): Latihan 30 detik aplikatif
13. **Mutiara Rasa** (M): Aforisme paradoks 1 kalimat
14. **Pertanyaan Refleksi** (N): Sentence case
15. **Status Naskah** (O): `Menunggu ACC Manual Pak Satya` (Draf) -> `ACC` (Disetujui Pak Satya)
16. **Status Audio TTS** (P): `Render` (DILARANG "Selesai Render")
17. **Status Video MP4** (Q): `Rendered` (DILARANG "Selesai Render")
18. **Status Upload YT** (R): `Uploaded` (DILARANG "Uploaded (Public)")
19. **Link YouTube** (S): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://youtu.be/[video_id]`). **DILARANG menggunakan formula `=HYPERLINK`**.
20. **Link Web Pustaka** (T): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://kontemplasi.satyaaditech.web.id/#[slug]`). **DILARANG menggunakan formula `=HYPERLINK`**.
21. **Link Google Docs** (U): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://docs.google.com/document/d/[doc_id]/edit`). **DILARANG menggunakan formula `=HYPERLINK`**.
22. **Status Siar WA/TG** (V): `Siap Siar` (sebelum siaran) / `Done` (setelah penyiaran selesai).

---

## 2. Standar Rendering Video & Tipografi Subtitle Baku (Montserrat 62 & Ken Burns)

* **Format Resolusi**: Vertikal **9:16 (1080 x 1920 Full HD)** untuk YouTube Shorts & Reels.
* **Geometri Posisi**: **Alignment: 5** (Middle-Center, tepat di tengah layar Y=960).
* **Overlay Box Kontras**: Kotak hitam transparan 65% (`color=black@0.65`) berukuran `w=940, h=340, x=70, y=790`. Menjaga keterbacaan teks tetap nyaman di atas latar dinamis apapun.
* **Font Terpilih**: **Montserrat** (Bold / SemiBold).
* **Ukuran Font**: **Size 62** (disetujui Pak Satya, proporsi ideal layar HP).
* **Skema Warna Dual-Tone Editorial**:
  - **Baris 1 (Atas)**: Champagne Gold (`#F2D091` / ASS: `{\c&H0091D0F2&}`)
  - **Baris 2 (Bawah)**: Warm Ivory White (`#F8F9FA` / ASS: `{\c&H00F8F9FA&}`)
  - Outline: Hitam murni tebal 2px, Shadow 2px.
* **Aturan Pemenggalan Kata (Semantic Chunking)**:
  - Maksimal **7–10 kata per tampilan layar** (batas maksimal 11 kata). DILARANG menampilkan 1-2 kalimat panjang sekaligus.
  - Terbagi menjadi 2 baris pendek seimbang (3–5 kata baris 1, 3–5 kata baris 2).
* **Gerakan Kamera Ken Burns (Sumbu Z - Tanpa Pan Horizontal)**:
  - Menggantikan geser samping (Pan Left/Right) yang sempit pada layar vertikal 9:16.
  - Pola bergantian antar babak:
    - **Scene 1 (Sabda Jawa)**: `Slow Zoom In` (fokus melangkah ke kedalaman batin)
    - **Scene 2 (Pangilon Rasa)**: `Slow Zoom Out` (membuka kelapangan pandangan hidup)
    - **Scene 3 (Laku Panyiswan)**: `Slow Zoom In` (menarik fokus ke rongga dada & napas hening)
    - **Scene 4 (Jangkar Batin & Berkah)**: `Slow Zoom Out` (pasrah sumarah & memancarkan berkah keselamatan)
* **Kalibrasi Audio Kontemplatif (Edge-TTS)**:
  - **Sabda Jawa**: `jv-ID-DimasNeural`, rate **`-20%`**, pitch **`-3Hz`**, jeda hening **2.5s – 3.0s**.
  - **Narasi Indonesia**: `id-ID-ArdiNeural`, rate **`-22%`**, pitch **`-3Hz`**, jeda hening **2.0s**.
* **Anti-Emoji di Subtitle**: Hapus seluruh emoji mentah dari naskah `.ass` agar tidak merender kotak rusak (`⧠`).
* **Durasi Rendering**: Selalu verifikasi durasi video cocok dengan durasi master audio via `ffprobe`.

---

## 3. Ketentuan Bahasa Naskah (V8 Monolingual Naskah + Verbatim Sabda)

* Seluruh naskah renungan (Terjemahan, Pangilon Rasa, Laku Panyiswan, Mutiara Rasa, Pertanyaan, Doa Satuhu) **WAJIB 100% BAHASA INDONESIA**.
* HANYA kutipan Sabda asli yang ditulis dalam Basa Jawa kanonikal verbatim 100%.
* Tidak ada lagi produksi versi bahasa terpisah (English/Jawa); ekosistem resmi V8 berfokus pada bahasa Indonesia yang hangat, komunikatif, dan jernih.
