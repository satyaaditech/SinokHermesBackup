# PANDUAN STANDAR OPERASIONAL (SOP) PRODUKSI VIDEO RENUNGAN KONTEMPLATIF AI
**Format**: Vertikal 9:16 (1080 x 1920 Full HD)  
**Tujuan**: Menghasilkan video renungan spiritual/reflektif harian dengan vokal kontemplatif alami (Dual-Voice), sinkronisasi subtitle 100% presisi (*Zero-Desync*), visual AI sinematik (Google Imagen 3), dan animasi kamera halus tanpa jitter (*Sub-pixel Bicubic Motion*).  
**Target Pembaca**: Manusia (Kreator/Operator) & Agen AI (LLM / Automation Agent).

---

## 1. Arsitektur Alur Kerja Lengkap (End-to-End Workflow)

```
[ Naskah Renungan 4 Babak ]
           │
           ▼
[ Tahap 1: Dual-Voice TTS ] ──► edge-tts (jv-ID-DimasNeural + id-ID-ArdiNeural)
           │                    + Jeda Hening (anullsrc sacred pauses 1.5s - 2.5s)
           ▼
[ Tahap 2: Whisper AI Sync ] ──► Faster-Whisper (Ekstraksi Timestamp Nyata per Kata/Frasa)
           │
           ▼
[ Tahap 3: Subtitle .ASS ] ──► Segment Grouping (83 Segmen Whisper -> 27 Slide Dialogue)
           │                   + Styling Tipografi DéjàVu Sans Emas, Cyan, Mint, Putih
           ▼
[ Tahap 4: AI Visual Imagen ] ──► Google Imagen 3 (4 Gambar 768x1376 Native 9:16)
           │
           ▼
[ Tahap 5: FFmpeg Engine ] ──► Sub-Pixel Bicubic Interpolation (perspective filter)
           │                   + Cross-Dissolve Transitions (xfade at sacred pauses)
           │                   + Color Grading (-10% Brightness, +15% Contrast)
           ▼
[ Tahap 6: Distribusi & Logging ] ─► Upload YouTube (upload_youtube.py --privacy public)
                                  + Buat Google Doc via Drive API → masukkan naskah lengkap + footer links
                                  + Tulis .md ke /share/renungan/ + /kontemplasi/renungan/ + jalankan sync_to_github.sh
                                  + Update Master Produksi V8 kolom S (Link YT), T (Link Web Pustaka), U (Link Google Docs) dengan URL mentah langsung (DILARANG =HYPERLINK)
                                  + Set kolom P=Render, Q=Rendered, R=Uploaded
                                  + Kolom V (Status Siar WA/TG) diisi Siap Siar (sebelum siar) atau Done (setelah penyiaran selesai)
```

---

## 2. Pedoman Naskah & Segmentasi Kontekstual

Setiap naskah renungan dianalisis dan dibagi ke dalam segmen/babak narasi batin (biasanya 3 s.d. 4 segmen). **Objek visual latar tidak ditentukan kaku di awal**, melainkan **sepenuhnya menyesuaikan naskah dan tema renungan** yang sedang diangkat.

Contoh struktur 4 babak narasi batin:

| Babak | Peran Narasi | Bahasa & Model Suara | Konsep Visual Latar (Dinamis Sesuai Naskah) | Arah Gerak Kamera |
| :--- | :--- | :--- | :--- | :--- |
| **Babak 1** | **Sabda Tuntunan Luhur** | Basa Jawa (`jv-ID-DimasNeural`) | Ilustrasi bernuansa sakral/asal mula tradisi sesuai teks Sabda | **Slow Tilt Down / Up** |
| **Babak 2** | **Pangilon Rasa / Refleksi** | Bahasa Indonesia (`id-ID-ArdiNeural`) | Metafora visual pergolakan batin / realitas pikiran sesuai narasi | **Slow Pan Left** |
| **Babak 3** | **Laku Panyiswan / Latihan Batin** | Bahasa Indonesia (`id-ID-ArdiNeural`) | Metafora visual keheningan, napas, atau kepasrahan raga | **Slow Tilt Down** |
| **Babak 4** | **Jangkar Batin & Berkah** | Bahasa Indonesia (`id-ID-ArdiNeural`) | Metafora visual fajar pencerahan, kedamaian, atau berkah sejati | **Slow Pan Right** |

---

## 3. Standar Voice Over Dual-Voice & Sacred Pauses

### A. Alasan Pemilihan Vokal
* **Bahasa Jawa (Sabda Tuntunan)**: Harus menggunakan model **`jv-ID-DimasNeural`**.  
  *Mengapa?* Model vokal Indonesia biasa melafalkan kosakata Jawa secara kaku, salah penekanan suku kata (*swara miring/jejeg*), dan menghilangkan aura sakral. Model Dimas menghasilkan pelafalan Jawa medok alami, tenang, dan berwibawa.
* **Bahasa Indonesia (Pangilon Rasa, Laku, Refleksi)**: Menggunakan model **`id-ID-ArdiNeural`**.  
  *Mengapa?* Memiliki warna suara bariton hangat, teduh, dan sangat cocok untuk narasi *mindfulness* / kontemplasi batin.

### B. Parameter Akustik & Tempo Bicara (Kalibrasi Kontemplatif Baku)
| Bagian Konten | Model Suara | Rate (Tempo) | Pitch | Sacred Pause |
| :--- | :--- | :--- | :--- | :--- |
| **Kutipan Sabda Jawa** | `jv-ID-DimasNeural` | **`-20%`** | `-3Hz` | `2.5s - 3.0s` (setelah Sabda) |
| **Narasi Refleksi & Teori** | `id-ID-ArdiNeural` | **`-22%`** | `-3Hz` | `2.0s` |
| **Laku Panyiswan (Latihan Fisik/Napas)** | `id-ID-ArdiNeural` | **`-22%`** | `-3Hz` | `2.0s - 2.5s` |
| **Doa Penutup & Mutiara Rasa** | `id-ID-ArdiNeural` | **`-22%`** | `-3Hz` | `2.5s` (sebelum Doa) |

### C. Dynamic Sacred Pauses (Jeda Hening Bernapas)
Jangan biarkan narator membaca teks secara terus-menerus tanpa jeda hening audio (`anullsrc`):
* **Antar Subjudul / Bagian**: `1.5 detik`
* **Setelah Sabda Jawa**: `2.5 detik` (memberi waktu batin pendengar untuk meresapkan petikan sabda).
* **Latihan Jeda Raga / Laku**: `2.0 s.d. 2.5 detik` (memberi ruang bagi pendengar menarik napas dalam dan merilekskan bahu).

---

## 4. Metodologi Sinkronisasi Subtitle 100% Presisi (Zero-Desync)

### A. Akar Masalah Keterlambatan Terdahulu
1. **Estimasi Durasi Statis**: Menghitung durasi subtitle berdasarkan rata-rata 7–8 detik per baris menyebabkan akumulasi selisih waktu bicara narator. Pada menit ke-2, subtitle terlambat hingga 10–15 detik.
2. **Kelemahan Index Mapping 1-to-1**: Jika transkrip Whisper menghasilkan 83 segmen kata/frasa pendek, sedangkan naskah teks dipecah menjadi 27 slide:
   - ⚠️ **KESALAHAN FATAL**: Memetakan `slide[i]` ke `segment[i]` menyebabkan slide ke-27 selesai di detik ke-65, padahal audio masih berjalan hingga menit ke-3.

### B. Solusi: Grouped Whisper Segments (*Segment Grouping Pattern*)
Petakan rentang indeks segmen Whisper `(start_idx, end_idx)` untuk setiap slide teks:

```python
# Format: (start_seg_idx, end_seg_idx, style, text)
groups = [
    (0, 0, "Title", "RENUNGAN PENYISWAAN"),
    (
        1,
        2,
        "TitleHighlight",
        "BANGUN DARI MODE OTOPILOT:\\NMengapa Otak Kita Lelah Terjebak DMN?",
    ),
    (3, 3, "Normal", "_Salam Karahayon_"),
    (
        4,
        7,
        "TitleHighlight",
        "[ KUTIPAN TUNTUNAN ]\\nSerat Sasangka Jati (Tri Sila: Eling)",
    ),
    (
        8,
        10,
        "Sabda",
        '"Mungguh elinge marang Tripurusa mau,\\ning saben dinane padha'
        ' diparsudia kang nganti kulina..."',
    ),
    (
        11,
        13,
        "Sabda",
        '"...pepindhane kaya dene wong luwe,\\nelinge marang pangan kang ora'
        ' susah mawa pangatage luamah."',
    ),
    # ... dipetakan berurutan hingga segmen terakhir (82, 82)
]

for s_idx, e_idx, style, text in groups:
  st_sec = segments[s_idx]["start"]
  en_sec = segments[e_idx]["end"] + 0.3  # Buffer kenyamanan baca
  # Masukkan ke format Dialogue baris ASS
```

---

## 5. Sistem Desain Subtitle (.ASS)

* **Resolusi Proyeksi**: `PlayResX: 1080`, `PlayResY: 1920`
* **WrapStyle**: `0` (Smart wrapping)
* **Font Teruji**: `DejaVu Sans` (Tersedia default di Ubuntu Linux server, bebas masalah fontconfig).

### Palet Warna & Styling ASS
| Style | Warna Utama (&HBBGGRR) | Visual Warna | Fungsi | Font Size | Shadow / Outline |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Badge** | `&H0000E6FF` | Kuning Emas Cerah | Label Kategori Atas | 42 | Outline 3, Shadow 2 |
| **TitleHighlight** | `&H0000E6FF` | Kuning Emas | Judul / Babak Baru | 58 | Outline 5, Shadow 3 |
| **Sabda** | `&H0000FFFF` | Kuning Sakral | Petikan Sabda Basa Jawa | 54 | Outline 5, Shadow 3 |
| **Action** | `&H0080FF80` | Hijau Mint Tenang | Langkah Latihan Laku | 52 | Outline 5, Shadow 3 |
| **Highlight** | `&H0050E0FF` | Cyan Biru Terang | Poin Penawar & Refleksi | 54 | Outline 5, Shadow 3 |
| **Normal** | `&H00FFFFFF` | Putih Bersih | Narasi Penjelasan | 52 | Outline 5, Shadow 3 |

> [!IMPORTANT]
> **Larangan Penggunaan Emoji di File ASS**: Emoji (misal: 📖, 💭, 🧘) memicu peringatan `fontselect: failed to find any fallback with glyph ...` pada `libass` di setiap frame, memperlambat rendering hingga 3x lipat. Gunakan tag teks rapi seperti `[ KUTIPAN TUNTUNAN ]` atau `[ LAKU PANYISWAN ]`.

## 6. Pembangkitan Latar Visual Dinamis via Nano Banana / Imagen 3

### A. Prinsip Utama: Fleksibilitas Kontekstual Berbasis Naskah
> [!IMPORTANT]
> **Objek visual latar TIDAK ditentukan kaku di awal**. Jangan membatasi gambar hanya pada Joglo atau Otak. Yang terpenting adalah: **gambar harus di-generate oleh AI (Nano Banana / Imagen) sesuai dengan konteks dan metafora segmen naskah yang ingin diilustrasikan**.

Setiap naskah renungan baru memiliki pesan spiritual yang berbeda. Misalnya:
* Jika naskah bertema **"Samudera Pangapura / Pengampunan"**: Latar dapat berupa deburan ombak laut yang tenang di kala senja, karang kokoh yang diterpa air, dan lentera mercusuar di malam berkabut.
* Jika naskah bertema **"Rela & Melepaskan / Pasrah Sumarah"**: Latar dapat berupa dedaunan musim gugur yang melayang jatuh perlahan ke sungai jernih, kepulan asap dupa tipis, dan cakrawala lapang tanpa batas.
* Jika naskah bertema **"Tri Sila Eling & Neurosains DMN"** (kasus video ini): Latar menggunakan metafora pendopo joglo sakral, visualisasi artistik neuron otak berpijar, mangkuk riak air hening, dan danau cermin bersimbah fajar.

### B. Prosedur Perumusan Visual per Segmen (Untuk AI & Kreator)
1. **Analisis Segmen Naskah**: Bagi narasi ke dalam 3 s.d. 4 babak tematik.
2. **Ekstraksi Metafora Batin**: Tentukan satu simbol visual kunci untuk masing-masing babak yang merefleksikan emosi pendengar pada detik tersebut.
3. **Pembangkitan Gambar via Nano Banana / Imagen 3**:
   * **Rasio Wajib**: Vertikal **9:16** (resolusi dasar 768 x 1376 atau 1080 x 1920).
   * **Aturan Komposisi**: Pastikan area sepertiga tengah dan bawah gambar memiliki kontras yang tenang (tidak terlalu padat/ramai) agar teks subtitle tetap terbaca jelas (*legible*).
   * **Aturan Negatif**: Selalu sertakan perintah `no text, no letters, no watermark, no UI` agar gambar murni seni visual tanpa artefak teks bawaan model AI.

### C. Formula Universal Prompting
Gunakan pola prompt berikut untuk Nano Banana / Imagen 3:
```text
[Subjek / Metafora Visual Kontekstual Sesuai Naskah Segmen], 
[Pencahayaan Khidmat & Remang Kontemplatif: soft golden god rays / mystical twilight / warm candlelight / bioluminescent glow], 
[Suasana: sacred, tranquil, contemplative mindfulness atmosphere, deep depth of field], 
[Gaya: cinematic 8k, photorealistic, elegant fine art], 
[Format: 9:16 vertical orientation, no people, no text, no watermark]
```

## 7. Solusi Anti-Jitter: Animasi Sub-Pixel Bicubic Interpolation

### A. Mengapa Filter `crop=x:y` Menghasilkan Gerakan Patah-Patah?
Pada gerakan kamera lambat (misalnya Scene 2 berdurasi 80,5 detik dengan 1.932 frame pada 24 fps):
* Jarak geser = $1350 - 1080 = 270\text{ px}$.
* Kecepatan = $270 \div 1932 = \mathbf{0{,}1397\text{ px/frame}}$.
* Karena filter `crop` FFmpeg **hanya menerima bilangan bulat (integer)**, koordinat $x$ bernilai sama persis selama **7 frame berturut-turut (~0,3 detik diam)**, lalu melompat 1 piksel di frame ke-8. Pola *diam $\to$ loncat $\to$ diam* ini terlihat jelas sebagai getaran/patah-patah (*jitter*).

### B. Solusi: Matriks Koordinat `perspective` Sub-Pixel Bicubic
Gunakan filter `perspective` dengan parameter `eval=frame:interpolation=cubic` dan variabel frame input `in`:

```
Input: scale=1350:2400 (Canvas ekstra 1.25x dari 1080:1920)
       ↓
Filter: perspective=x0='...':y0='...':x1='...':y1='...':
                    x2='...':y2='...':x3='...':y3='...':
                    interpolation=cubic:eval=frame
       ↓
Output: scale=1080:1920
```

### C. Rumus Koordinat 4 Gerakan Kamera Utama:
Biarkan $W_{in} = 1350$, $H_{in} = 2400$, lebar target $W = 1080$, tinggi target $H = 1920$, dan total frame $F = \text{Durasi} \times 24$.

1. **Slow Pan Left** (Kamera bergeser ke kiri, jendela sumber bergerak ke kanan):
   * $x(in) = 270 \cdot \frac{in}{F}$
   * $y(in) = 240$ (Tengah vertikal: $(2400-1920)/2$)
   * Koordinat:
     `x0='270*in/F': y0='240'`  
     `x1='270*in/F+1080': y1='240'`  
     `x2='270*in/F': y2='240+1920'`  
     `x3='270*in/F+1080': y3='240+1920'`

2. **Slow Pan Right** (Kamera bergeser ke kanan, jendela sumber bergerak ke kiri):
   * $x(in) = 270 \cdot \left(1 - \frac{in}{F}\right)$
   * $y(in) = 240$

3. **Slow Tilt Down** (Kamera turun, jendela sumber bergerak turun):
   * $x(in) = 135$ (Tengah horizontal: $(1350-1080)/2$)
   * $y(in) = 480 \cdot \frac{in}{F}$

4. **Slow Tilt Up** (Kamera naik, jendela sumber bergerak naik):
   * $x(in) = 135$
   * $y(in) = 480 \cdot \left(1 - \frac{in}{F}\right)$

---

## 8. Template Skrip Otomasi Lengkap (`build_cinematic_devotional_video.py`)

Skrip produksi berikut dapat langsung dijalankan untuk video-video renungan selanjutnya:

```python
import os
import subprocess

WORKDIR = "/home/satyaaditech/share/viral_sample"
SCENE1 = f"{WORKDIR}/scene1.jpg"
SCENE2 = f"{WORKDIR}/scene2.jpg"
SCENE3 = f"{WORKDIR}/scene3.jpg"
SCENE4 = f"{WORKDIR}/scene4.jpg"
AUDIO = f"{WORKDIR}/renungan_eling_master.mp3"
ASS_SUBS = f"{WORKDIR}/subtitles_renungan_eling.ass"
OUTPUT_VIDEO = f"{WORKDIR}/renungan_eling_cinematic.mp4"

# Durasi Scene mengunci pada Sacred Pauses narator:
D1, D2, D3, D4 = 45.5, 80.5, 45.5, 35.5
F1, F2, F3, F4 = int(D1 * 24), int(D2 * 24), int(D3 * 24), int(D4 * 24)
OFFSET1, OFFSET2, OFFSET3 = 44.5, 124.0, 168.5


def build_video():
  filter_complex = (
      # Scene 1: Slow Tilt Up
      f"[0:v]fps=24,scale=1350:2400,"
      f"perspective=x0='135':y0='480*(1-in/{F1})':"
      f"x1='135+1080':y1='480*(1-in/{F1})':"
      f"x2='135':y2='480*(1-in/{F1})+1920':"
      f"x3='135+1080':y3='480*(1-in/{F1})+1920':"
      f"interpolation=cubic:eval=frame,scale=1080:1920[v1];"
      # Scene 2: Slow Pan Left (Subpixel Bicubic Anti-Jitter)
      f"[1:v]fps=24,scale=1350:2400,"
      f"perspective=x0='270*in/{F2}':y0='240':"
      f"x1='270*in/{F2}+1080':y1='240':"
      f"x2='270*in/{F2}':y2='240+1920':"
      f"x3='270*in/{F2}+1080':y3='240+1920':"
      f"interpolation=cubic:eval=frame,scale=1080:1920[v2];"
      # Scene 3: Slow Tilt Down
      f"[2:v]fps=24,scale=1350:2400,"
      f"perspective=x0='135':y0='480*in/{F3}':"
      f"x1='135+1080':y1='480*in/{F3}':"
      f"x2='135':y2='480*in/{F3}+1920':"
      f"x3='135+1080':y3='480*in/{F3}+1920':"
      f"interpolation=cubic:eval=frame,scale=1080:1920[v3];"
      # Scene 4: Slow Pan Right
      f"[3:v]fps=24,scale=1350:2400,"
      f"perspective=x0='270*(1-in/{F4})':y0='240':"
      f"x1='270*(1-in/{F4})+1080':y1='240':"
      f"x2='270*(1-in/{F4})':y2='240+1920':"
      f"x3='270*(1-in/{F4})+1080':y3='240+1920':"
      f"interpolation=cubic:eval=frame,scale=1080:1920[v4];"
      # Cross-Dissolve Transitions (1.0 detik di jeda hening)
      f"[v1][v2]xfade=transition=fade:duration=1.0:offset={OFFSET1}[x1];"
      f"[x1][v3]xfade=transition=fade:duration=1.0:offset={OFFSET2}[x2];"
      f"[x2][v4]xfade=transition=fade:duration=1.0:offset={OFFSET3}[bg];"
      # Color Grading Kontemplatif & Bakar Subtitle ASS
      f"[bg]eq=brightness=-0.10:contrast=1.15,ass={ASS_SUBS}[outv]"
  )

  cmd = [
      "ffmpeg",
      "-y",
      "-loop",
      "1",
      "-t",
      str(D1),
      "-i",
      SCENE1,
      "-loop",
      "1",
      "-t",
      str(D2),
      "-i",
      SCENE2,
      "-loop",
      "1",
      "-t",
      str(D3),
      "-i",
      SCENE3,
      "-loop",
      "1",
      "-t",
      str(D4),
      "-i",
      SCENE4,
      "-i",
      AUDIO,
      "-filter_complex",
      filter_complex,
      "-map",
      "[outv]",
      "-map",
      "4:a",
      "-t",
      "201.5",
      "-c:v",
      "libx264",
      "-preset",
      "fast",
      "-crf",
      "20",
      "-c:a",
      "aac",
      "-b:a",
      "192k",
      "-pix_fmt",
      "yuv420p",
      OUTPUT_VIDEO,
  ]
  subprocess.run(cmd, check=True)
  print("SUCCESS:", OUTPUT_VIDEO)


if __name__ == "__main__":
  build_video()
```

---

## 9. Prosedur Server Hygiene & Pengelolaan Disk

1. **Prinsip Utama**: Server Linux `n8nserver` hanya digunakan sebagai mesin komputasi rendering. Penyimpanan video permanen berada di Mac lokal.
2. **Transfer Otomatis**:
   ```bash
   scp satyaaditech@n8nserver:/home/satyaaditech/share/viral_sample/renungan_eling_cinematic.mp4 /Users/satyaadidharma/Downloads/
   ```
3. **Pembersihan Wajib**:
   ```bash
   ssh satyaaditech@n8nserver "rm -f /home/satyaaditech/share/viral_sample/renungan_eling_cinematic.mp4 /tmp/test_*.mp4"
   ```

---

## 10. Checklist Kualitas untuk Eksekusi AI & Manusia

Sebelum menyerahkan hasil video akhir ke pengguna:
- [x] **Dual Voice Terverifikasi**: Sabda Basa Jawa oleh Dimas (`jv-ID-DimasNeural`), Refleksi Indonesia oleh Ardi (`id-ID-ArdiNeural`).
- [x] **Zero Desync Terverifikasi**: Teks subtitle muncul dan hilang persis bersamaan dengan getaran vokal narator.
- [x] **Sub-Pixel Motion Terverifikasi**: Pergeseran gambar menggunakan `perspective=...:interpolation=cubic` tanpa ada jeda loncat 1 piksel.
- [x] **Cross-Dissolve Terverifikasi**: Transisi antar babak terjadi tepat pada saat narator hening bernapas.
- [x] **File Tersimpan di Mac**: Tersedia di `/Users/satyaadidharma/Downloads/`.
- [x] **Server Bersih**: File MP4 hasil render di server Linux langsung dihapus.

---

---

## 11. STANDAR METADATA YOUTUBE (JUDUL, DESKRIPSI VIRAL & TAGS)

Setiap pengunggahan video renungan ke YouTube channel `@siswatalkstv`, format judul, deskripsi, dan tag WAJIB mengikuti formula berikut:

### 1. Judul Video YouTube (Maksimal 100 Karakter)
Formula: `[Judul Magnetik Ber-Hook Sains / Refleksi] 🧠 | Renungan Ajaran Sang Guru Sejati`
Contoh:
`Bangun dari Mode Otopilot: Mengapa Otak Lelah Terjebak Default Mode Network? 🧠 | Renungan SGS`

### 2. Deskripsi YouTube (Struktur Menggigit, Relate & High-Converting)
Deskripsi DILARANG ditulis datar/lempeng. Wajib memiliki struktur berikut:

1. **Baris 1–2 (The Magnetic Hook)**:
   - Kalimat pancingan / rasa sakit / pertanyaan psikologis-neurosains yang langsung mengena di 150 karakter pertama (sebelum penonton menekan tombol *Show More*).
2. **Paragraf 2–3 (Pangilon Rasa / Bedhah Masalah)**:
   - Mengupas fenomena modern (kelelahan mental, overthinking, ilusi waktu) dan menjembataninya dengan ajaran Sang Guru Sejati (Kusir Angen-angen vs Tripurusa).
3. **Pethikan Sabda Kanonikal yang Sakral**:
   - Teks Sabda Jawa verbatim 100% dan terjemahan resmi bahasa Indonesia.
4. **Laku Praktis Hari Ini (Micro-Habit 30 Detik)**:
   - 3 langkah aplikatif konkrit (Jeda Raga, Hening Batin, Laku Sadar).
5. **Mutiara Rasa**:
   - 1 kalimat aforisme paradoks yang menancap kuat di benak penonton.
6. **Ekosistem Digital (Link Lengkap)**:
   - `• 🌐 Baca Naskah Lengkap di Web Pustaka: https://kontemplasi.satyaaditech.web.id/#[slug]`
   - `• 📄 Versi Dokumen Google Docs: https://docs.google.com/document/d/[DocID]/edit`
7. **Doa Berkat Resmi**:
   - `Semoga Kita Senantiasa Berlimpah dengan Sih, Tuntunan, Pepadang, dan Pangayoman dari Sang Guru Sejati. Satuhu. 🙏🌿`
8. **Hashtags Viral (12–15 Tags)**:
   - `#Eling #DefaultModeNetwork #Mindfulness #Overthinking #OlahRasa #Pangestu #SangGuruSejati #FilosofiJawa #StoikismeJawa #KetenanganBatin #KesadaranDiri #SadarJiwa #KesehatanMental #Shorts #RenunganHarian`

🚫 **PANTANG MUTLAK**:
- DILARANG KERAS mencantumkan rincian teknis backend atau nama model AI/TTS (`jv-ID-DimasNeural`, `id-ID-ArdiNeural`, Edge-TTS, prompt teknis) di deskripsi publik YouTube.
