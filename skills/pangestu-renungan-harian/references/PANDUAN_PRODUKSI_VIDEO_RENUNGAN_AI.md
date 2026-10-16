# PANDUAN STANDAR OPERASIONAL (SOP) PRODUKSI VIDEO RENUNGAN KONTEMPLATIF AI (V8 BAKU)

> **Status Dokumen**: **LOCKED & PRODUCTION-VERIFIED** (Disetujui Resmi Pak Satya Adi Dharma — Oktober 2026)  
> **Format Output**: Vertikal **9:16 (1080 x 1920 Full HD)** YouTube Shorts, TikTok, dan Instagram Reels  
> **Durasi Baku**: 3 s.d. 5 Menit (Kontemplasi Meditatif Utuh)  
> **Kanal Publikasi**: YouTube `@siswatalkstv`, Web Pustaka `kontemplasi.satyaaditech.web.id`, dan Arsip Google Drive  

---

## 1. Arsitektur Alur Kerja Produksi (End-to-End Workflow)

```
[ Naskah Renungan 4 Babak Disetujui Pak Satya (Status: ACC) ]
                           │
                           ▼
[ Tahap 1: Sintesis Vokal Dual-Voice (Edge-TTS) ]
  • Sabda Basa Jawa verbatim : jv-ID-DimasNeural (Tempo -20%, Pitch -3Hz)
  • Seluruh Narasi Indonesia : id-ID-ArdiNeural (Tempo -22%, Pitch -3Hz)
  • Dynamic Sacred Pauses    : Jeda hening bernapas 2.0s s.d. 3.0s (anullsrc)
                           │
                           ▼
[ Tahap 2: Ekstraksi Subtitle WebVTT & Semantic Chunking ]
  • Native Edge-TTS Cues     : Sinkronisasi 100% presisi (Zero-Desync Guarantee)
  • Semantic Chunking        : Maksimal 7–10 kata per slide (batas mutlak 11 kata)
  • Balanced 2-Line Split    : 3–5 kata baris atas, 3–5 kata baris bawah
                           │
                           ▼
[ Tahap 3: Tipografi ASS & Overlay Box Kontras ]
  • Font Terpilih            : Montserrat (SemiBold / Bold) Size 62
  • Geometri Posisi          : Alignment: 5 (Middle-Center, tepat di Y=960)
  • Dual-Tone Color Scheme   : Baris 1 Champagne Gold (#F2D091)
                               Baris 2 Warm Ivory White (#F8F9FA)
  • Translucent Overlay Box  : drawbox=x=70:y=790:w=940:h=340:color=black@0.65
                           │
                           ▼
[ Tahap 4: Visual AI Dinamis & Ken Burns Motion ]
  • OmniRoute (Imagen 3)     : 4 Gambar 9:16 resolusi tinggi sesuai metafora naskah
  • Ken Burns Sumbu Z        : Sub-pixel Bicubic Zoom In & Zoom Out (Tanpa Pan Horizontal)
  • Cross-Dissolve           : Transisi xfade fade 1.0 detik tepat di jeda hening
                           │
                           ▼
[ Tahap 5: Multi-Platform Publishing & Sinkronisasi ]
  • YouTube Channel          : @siswatalkstv (Title <= 95 char, Hook 150 char)
  • Master Google Sheet      : Tab 'Master Produksi V8' Baris rilis (22 Kolom Lean)
  • Web Pustaka & Docs       : GitHub Pages deploy & Google Docs publik
  • Salinan File Mac         : Disalin ke ~/Downloads/ laptop Pak Satya
```

---

## 2. Standar Kalibrasi Vokal Dual-Voice & Sacred Pauses

### A. Pembagian Peran Vokal
* **Petikan Sabda Jawa Verbatim (`jv-ID-DimasNeural`)**:
  Digunakan **HANYA** untuk membaca kutipan Sabda asli Bahasa Jawa dari kitab kanonikal. Karakter vokal medhok alami, tenang, berwibawa, dan menghadirkan aura sakral.
* **Seluruh Narasi Indonesia (`id-ID-ArdiNeural`)**:
  Digunakan untuk Salam Karahayon, Pengantar Pustaka, Terjemahan Sabda, Pangilon Rasa (Refleksi 2 Paragraf), Laku Panyiswan (Latihan Somatik 30 Detik), Mutiara Rasa, dan Doa Penutup Satuhu. Karakter bariton hangat, teduh, mengalir, dan menenangkan jiwa.

### B. Parameter Akustik & Tempo Bicara (LOCKED)
| Bagian Naskah | Model Suara | Tempo (Rate) | Nada (Pitch) | Durasi Sacred Pause Setelahnya |
| :--- | :--- | :---: | :---: | :--- |
| **Salam & Judul Renungan** | `id-ID-ArdiNeural` | **`-22%`** | **`-3Hz`** | `2.0 detik` |
| **Pengantar Pustaka Kitab** | `id-ID-ArdiNeural` | **`-22%`** | **`-3Hz`** | `1.5 detik` |
| **Kutipan Sabda Jawa Verbatim** | `jv-ID-DimasNeural` | **`-20%`** | **`-3Hz`** | **`2.5 s.d. 3.0 detik`** *(ruang mengendapkan getaran sabda)* |
| **Terjemahan Bahasa Indonesia** | `id-ID-ArdiNeural` | **`-22%`** | **`-3Hz`** | `2.0 detik` |
| **Pangilon Rasa Paragraf 1 & 2** | `id-ID-ArdiNeural` | **`-22%`** | **`-3Hz`** | `2.0 s.d. 2.5 detik` |
| **Laku Panyiswan (30 Detik)** | `id-ID-ArdiNeural` | **`-22%`** | **`-3Hz`** | `2.0 detik` *(memberi ruang bernapas raga)* |
| **Mutiara Rasa & Doa Satuhu** | `id-ID-ArdiNeural` | **`-22%`** | **`-3Hz`** | `2.5 detik` |

> [!IMPORTANT]
> **Sintaks CLI Edge-TTS**: Nilai negatif pada argumen CLI wajib menggunakan tanda sama dengan (contoh: `f"--rate={rate}"`, `f"--pitch={pitch}"`), karena jika dipisah spasi akan memicu galat parser CLI `unrecognized arguments: -22%`.

---

## 3. Sistem Tipografi Baku & Desain Subtitle (.ASS)

### A. Parameter Styling Subtitle ASS
```ini
[Script Info]
Title: Renungan Sinematik Pangestu V8 (Centered Subtitles)
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: RenunganBaku,Montserrat,62,&H00F8F9FA,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,2,5,70,70,0,1
```

* **Font Terpilih**: **`Montserrat`** (SemiBold / Bold). Elegan, modern, kontras tinggi, dan nyaman dibaca di smartphone.
* **Ukuran Font**: **`Size 62`** (Disetujui Pak Satya, proporsional sempurna terhadap layar 1080x1920).
* **Posisi Geometri**: **`Alignment: 5`** (Middle-Center, tepat di tengah layar `Y=960`).
* **Outline & Shadow**: Hitam pekat murni 2px (`&H00000000`) untuk ketajaman teks maksimal di atas latar apapun.

### B. Palet Warna Baku (Dual-Tone Editorial Styling)
Dua nada warna yang konsisten di seluruh video (tanpa campur aduk warna-warni pelangi):
* **Baris 1 (Atas)**: **`Champagne Gold (#F2D091)`** *(ASS: `{\c&H0091D0F2&}`)* — Memberikan sentuhan agung, hangat, sakral, dan berkelas.
* **Baris 2 (Bawah)**: **`Warm Ivory White (#F8F9FA)`** *(ASS: `{\c&H00F8F9FA&}`)* — Bersih, tajam, kontras tinggi, dan mudah dicerna mata.

### C. Translucent Contrast Overlay Box
Untuk melindungi keterbacaan teks di atas gambar latar belakang yang dinamis dan bertekstur, video menggunakan filter kotak hitam transparan 65%:
```text
drawbox=x=70:y=790:w=940:h=340:color=black@0.65:t=fill
```
* Posisi: Berada tepat di tengah vertikal `Y=960` (mulai dari `Y=790` hingga `Y=1130`).
* Dimensi: Lebar 940px, tinggi 340px, margin horizontal kiri-kanan masing-masing 70px.
* Memberikan ruang bernapas vertikal ~95px di atas dan di bawah teks 2 baris berukuran 62.

### D. Aturan Pemenggalan Kata (Semantic Chunking)
* **Aturan Baku**: Setiap slide **WAJIB terdiri dari 7 s.d. 10 kata** (batas mutlak maksimal 11 kata).
* **DILARANG KERAS**: Menampilkan 1–2 kalimat panjang atau satu paragraf penuh sekaligus di layar.
* **Pembagian Baris Seimbang**: Setiap tampilan dibagi menjadi 2 baris pendek seimbang:
  * **Baris 1 (Gold)**: 3 s.d. 5 kata pertama.
  * **Baris 2 (White)**: 3 s.d. 5 kata berikutnya.
* **Durasi Baca**: Setiap slide tayang selama 3.0 s.d. 4.5 detik, mengikuti irama tarikan napas pembaca.

---

## 4. Gerakan Kamera Meditatif Ken Burns (Sumbu Z)

### A. Mengapa Menghilangkan Pan Left / Pan Right Horizontal?
Pada layar vertikal 9:16 (lebar hanya 1080px vs tinggi 1920px), gerakan kamera geser ke samping (*pan left/right*) terasa sangat sempit dan memicu *visual conflict*: mata penonton ditarik ke kiri/kanan, padahal teks renungan berada di tengah. Gerakan geser horizontal juga rentan terlihat tersendat (*jitter/stuttering*).

### B. Solusi: Ken Burns Smooth Zoom (Sumbu Z)
Gerakan kamera bergerak secara simetris dari atau menuju **titik pusat (Center/Z-axis)**. Karena teks renungan berada di tengah, efek Zoom In/Out bekerja harmonis mengalir di sekeliling teks tanpa mengganggu fokus membaca.

### C. Alur 4 Babak Gerakan Kamera
| Babak / Scene | Bagian Renungan | Gerakan Kamera | Nuansa Rasa Kontemplatif |
| :---: | :--- | :---: | :--- |
| **Scene 1** | **Sabda Jawa Kanonikal** | **`Slow Zoom In`** | Kamera melangkah masuk perlahan ke relung keheningan batin (*nyawiji*) |
| **Scene 2** | **Pangilon Rasa (Refleksi)** | **`Slow Zoom Out`** | Kamera mundur perlahan memperlihatkan luasnya cakrawala, membuka kelapangan rasa |
| **Scene 3** | **Laku Panyiswan (Hening Raga)** | **`Slow Zoom In`** | Menarik fokus kesadaran turun dari kepala menuju napas dada |
| **Scene 4** | **Jangkar Batin & Doa Berkah** | **`Slow Zoom Out`** | Kepasrahan total (*sumarah*) dan memancarkan berkah keselamatan ke semesta |

### D. Formula Matematis FFmpeg Sub-Pixel Bicubic Perspective
Canvas gambar di-*upsample* ke **1350 x 2400** (1.25x dari 1080x1920). Dengan total frame $F = \text{Durasi} \times 24$:

* **Slow Zoom In (Push In)**:
  ```text
  x0='135*in/F': y0='240*in/F'
  x1='1350-135*in/F': y1='240*in/F'
  x2='135*in/F': y2='2400-240*in/F'
  x3='1350-135*in/F': y3='2400-240*in/F'
  ```
* **Slow Zoom Out (Pull Out)**:
  ```text
  x0='135*(1-in/F)': y0='240*(1-in/F)'
  x1='1350-135*(1-in/F)': y1='240*(1-in/F)'
  x2='135*(1-in/F)': y2='2400-240*(1-in/F)'
  x3='1350-135*(1-in/F)': y3='2400-240*(1-in/F)'
  ```
* **Filtergraph FFmpeg Lengkap**:
  ```text
  scale=1350:2400,perspective=[coord]:interpolation=cubic:eval=frame,scale=1080:1920
  ```
* **Transisi Antar Babak**: Filter `xfade=transition=fade:duration=1.0:offset=[t]` tepat terjadi di saat jeda hening (*sacred pause*) narator.

---

## 5. Pembangkitan Latar Visual Dinamis via AI (OmniRoute / Imagen 3)

### A. Prinsip Metafora Visual Kontekstual
* Objek visual latar **TIDAK KAKU**.
* Jangan membatasi latar hanya pada motif joglo atau gambar otak. Visual harus di-*generate* oleh AI sesuai dengan pesan spiritual dan metafora dari masing-masing babak naskah (contoh: jam pasir antik, jendela berembun hujan, riak air tenang, lentera malam, kabut fajar pegunungan).

### B. Formula Universal Prompting 9:16
```text
Vertical 9:16 composition, [Subjek & Metafora Visual Kontekstual Sesuai Naskah],
[Pencahayaan: soft golden morning dawn sunlight / mystical twilight / warm candlelight / atmospheric dust motes],
[Suasana: tranquil, serene contemplative spiritual atmosphere, deep depth of field],
[Kamera & Lensa: Shot on Leica M11 with Summilux 35mm f/1.4 / Hasselblad H6D-100c, authentic documentary realism, delicate creamy bokeh, zero CGI gloss],
[Aturan Negatif: no people, no text, no letters, no watermark, no UI]
```

---

## 6. Standar Integrasi Google Sheet Master Produksi V8

Seluruh rekaman produksi dicatat pada spreadsheet master:
* **Spreadsheet ID**: `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`
* **Tab Resmi**: `Master Produksi V8` *(Tab lama 'Rekap Renungan' 12-kolom telah ditutup)*

### Skema 22 Kolom Lean (A - V):
1. **No** (A)
2. **Tanggal Rilis WA** (B): `YYYY-MM-DD`
3. **Hari & Pasaran** (C): Contoh `Jumat Legi`
4. **Bulan** (D): Contoh `Oktober 2026`
5. **Tema Bulanan** (E)
6. **Tema Mingguan** (F)
7. **Judul Renungan** (G)
8. **Rujukan Kitab** (H): Kode kanonikal + Bab/Pasal
9. **Kutipan Asli** (I): Sabda Jawa verbatim 100%
10. **Terjemahan** (J): Terjemahan Bahasa Indonesia
11. **Pangilon Rasa** (K): 2 paragraf padat (Hook sains + Bedhah Kasunyatan)
12. **Laku Panyiswan** (L): Latihan 30 detik aplikatif
13. **Mutiara Rasa** (M): Aforisme paradoks 1 kalimat
14. **Pertanyaan Refleksi** (N): Pertanyaan refleksi
15. **Status Naskah** (O): `Menunggu ACC Manual Pak Satya` (Draf) ➔ `ACC` (Disetujui Pak Satya)
16. **Status Audio TTS** (P): `Render` (DILARANG "Selesai Render")
17. **Status Video MP4** (Q): `Rendered` (DILARANG "Selesai Render")
18. **Status Upload YT** (R): `Uploaded` (DILARANG "Uploaded (Public)")
19. **Link YouTube** (S): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://youtu.be/[video_id]`). **DILARANG menggunakan formula `=HYPERLINK`**.
20. **Link Web Pustaka** (T): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://kontemplasi.satyaaditech.web.id/#[slug]`). **DILARANG menggunakan formula `=HYPERLINK`**.
21. **Link Google Docs** (U): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://docs.google.com/document/d/[doc_id]/edit`). **DILARANG menggunakan formula `=HYPERLINK`**.
22. **Status Siar WA/TG** (V): `Siap Siar` (sebelum siaran) ➔ `Done` (setelah penyiaran selesai).

---

## 7. Perintah Eksekusi CLI di Server Hermes

### A. Menjalankan Engine Produksi Video:
```bash
python3 /home/satyaaditech/.hermes/skills/pangestu-renungan-harian/scripts/make_cinematic_video.py \
  --config /home/satyaaditech/share/viral_sample/config_[tanggal].json \
  --output-name renungan_[tanggal]_cinematic.mp4
```

### B. Mengunggah Video ke YouTube:
```bash
python3 /home/satyaaditech/kontemplasi/upload_youtube.py \
  --file /home/satyaaditech/share/viral_sample/renungan_[tanggal]_cinematic.mp4 \
  --title "[Judul Renungan]" \
  --desc "[Deskripsi ber-hook]" \
  --privacy public
```

### C. Menyalin Video ke Laptop Mac Pak Satya:
```bash
scp satyaaditech@100.92.237.45:/home/satyaaditech/share/viral_sample/renungan_[tanggal]_cinematic.mp4 /Users/satyaadidharma/Downloads/
```

---

## 8. Checklist Kualitas Akhir (Quality Gate)

Sebelum video dinyatakan siap siar:
- [x] **Vokal Kontemplatif**: Sabda Jawa oleh Dimas (`-20%`), Narasi Indonesia oleh Ardi (`-22%`).
- [x] **Zero-Desync**: Subtitle muncul dan berganti tepat mengikuti artikulasi kata narator.
- [x] **Tipografi Montserrat 62**: Baris 1 Gold, Baris 2 White, tepat di dalam box hitam transparan 65% di tengah layar.
- [x] **Semantic Chunking Terpenuhi**: Tidak ada slide yang memuat lebih dari 11 kata. Teks mengalir 7–10 kata per slide.
- [x] **Ken Burns Sumbu Z Halus**: Gerakan Zoom In dan Zoom Out berjalan mulus tanpa getaran pixel dan tanpa pan horizontal.
- [x] **Sinkronisasi Sempurna**: Tautan YouTube aktif tercatat di Master Sheet Kolom S, Web Pustaka telah ter-deploy, dan salinan MP4 tersedia di laptop Pak Satya.
