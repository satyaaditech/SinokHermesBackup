---
name: pangestu-renungan-harian
description: Produce Pangestu renungan harian for TG thread 1096. Agentic 3-role workflow (Research→Write→Edit) + format, persona, & anti-halusinasi rules.
---

# Renungan Harian Pangestu (Daily Bread)

> **Supporting References**:
> - Matriks Kontemplasi Universal & Anti-Shortcut: `references/matriks-kontemplasi-universal.md`
> - Standar Kualitas Prosa Humanis & Siar TG: `references/standar-kualitas-prosa-humanis.md`
> - SOP Produksi Video Sinematik V8 (End-to-End Pipeline): `references/sop-produksi-video-sinematik-v8.md`
> - Dual-Voice TTS Spec (DimasNeural + ArdiNeural): `references/dual-voice-tts-spec.md`
> - Gemini Canvas Web App (LEGACY — replaced by server-side Edge-TTS): `references/gemini_tts_prompts.md`

## 📅 PAUGERAN PENJADWALAN & KURIKULUM (MASTER SHEET LOCK)
- **Sumber Jadwal Wajib**: Setiap pembuatan renungan harian WAJIB mengambil jadwal tema, rujukan pustaka, dan babon kanonikal dari Google Sheet `Master Produksi V8` (`1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`) berdasarkan tanggal hari ini (atau baris urut berikutnya yang berstatus Belum ACC). DILARANG menentukan atau memilih tema acak di luar kurikulum Master Sheet yang sudah dirancang.

## 📌 MANDAT 1: STANDAR ALUR KERJA 2-TAHAP (DRAF NASKAH & ACC MANUAL CHECKPOINT)
Setiap kali Pak Satya memberikan perintah:
👉 **"Buatkan Renungan Hari Ini"** (atau **"Buatkan Renungan Hari Ini [tanggal/topik]"**)

Hermes/Sinox **WAJIB MENJALANKAN ALUR KERJA 2-TAHAP SECARA BERURUTAN**:

### 🛡️ TAHAP 1: PENYUSUNAN DRAF NASKAH & CHECKPOINT ACC (STOP & TUNGGU)
1. **Periksa Jadwal**: Cek baris tanggal hari ini pada tab `Master Produksi V8` (Google Sheet ID: `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`).
2. **Jalankan True Multi-Agent Editorial Council Engine (`hermes_editorial_council.py`)**:
   - DILARANG KERAS bermain peran sandiwara palsu (theatrical single-agent roleplaying) di mana 1 model pura-pura menjadi 4 agen dalam satu obrolan chat.
   - Sinox WAJIB mengeksekusi engine multi-agent independen via terminal menggunakan runtime Python 3.10:
     `/usr/bin/python3.10 ~/.hermes/skills/pangestu-renungan-harian/scripts/hermes_editorial_council.py [--row N | --date YYYY-MM-DD]`
     *(Wajib gunakan `/usr/bin/python3.10` karena modul `google.oauth2` terpasang di sana, bukan di Python 3.14 default).*
   - **DILARANG KERAS SINGLE-AGENT SHORTCUT / BYPASS**: Jika Pak Satya mengkritik naskah kurang humanis, dangkal, atau belum world-class, DILARANG menulis ulang secara manual sebagai agen tunggal. Wajib tetap menjalankan True Multi-Agent Council dengan menyuntikkan Matriks Kontemplasi Universal (`references/matriks-kontemplasi-universal.md`).
   - Engine ini secara otonom mengorkestrasi agen-agen terpisah melalui OmniRoute (`localhost:20128`):
     * **Step 1: Deterministic Redundancy & Historical Scanner**:
       - Memindai riwayat 7 hari terakhir dari Master Sheet untuk mengidentifikasi props/analogi lama (misal: layar HP, laptop, desah napas Huuuh, arisan keluarga, dsb) dan memasukkannya ke dalam blacklist aktif.
       - Mengunci fakta sejarah kanonikal: Ajaran Sang Guru Sejati diwahyukan pertama kali pada 14 Februari 1932 di Surakarta kepada Bp. R. Soenarto Mertowardojo (belum genap 1 abad; dilarang keras menyebut "berabad-abad lampau").
       - Memastikan judul baku: `Renungan Penyiswaan`.
       - Memastikan berkah penutup kanonikal resmi: `Semoga kita semua senantiasa berlimpah dengan sih, tuntunan, pepadang, dan pangayoman dari Sang Guru Sejati. Satuhu. 🙏`.
     * **Step 2: Agent 1 (Writer: Master Educator & Sastrawan Rohani)**:
       - Proses mandiri (4096 token, model `auto/best-chat`).
       - Menulis draf 4-Pilar Lean Murni dengan kedalaman 5 Pilar Bobot Mutu (insight non-klise "aha-moment", relate modern & pemahaman kasunyatan Ajaran SGS secara luas selaras Pustaka Pangestu, sudut pandang segar/unik, bernyawa *kanca lumaku* tanpa kata menggurui "kamu", serta jero nanging wening kanggé awam).
     * **Step 3: Agent 2 (Critic: Ruthless Gatekeeper)**:
       - Proses terpisah secara adversarial (`temperature=0.1`).
       - Membongkar cacat tanpa ampun menggunakan checklist ketat, dan mengeluarkan output JSON murni berisi status (`PASS` atau `REVISE`), skor mutu (0-100), daftar cacat (*defects found*), dan instruksi perbaikan konkret.
     * **Step 4: Adversarial Revision Loop (Maksimal 3 Ronde)**:
       - Jika status `REVISE` atau skor < 95, kritik dikembalikan ke Agent Writer untuk ditulis ulang secara paripurna hingga tuntas dan lulus standar dewan redaksi.
     * **Step 5: Komit & Sinkronisasi Ekosistem**:
       - Memperbarui Google Sheet `Master Produksi V8` Kolom G s.d. N.
       - Kolom 15 [Status Naskah] diset ke `Menunggu ACC Manual Pak Satya` (atau mempertahankan status `ACC` bila sebelumnya telah disetujui Pak Satya).
       - Menyimpan arsip lokal naskah ke `/home/satyaaditech/share/renungan/[date]_[slug].md`.
       - Menyimpan riwayat audit lengkap ke `/home/satyaaditech/share/renungan/[date]_audit_dossier.json`.
3. **Lapor ke Telegram Pak Satya**:
   - Kirimkan draf naskah lengkap hasil dewan redaksi beserta ringkasan audit skor ke Telegram pribadi Pak Satya (`777961507`) dan Group Thread 1096.
   - 🛑 **STOP & DILARANG MELANJUTKAN KE RENDER AUDIO/VIDEO SEBELUM DI-ACC OLEH PAK SATYA!** Tahap 1 selesai dan Sinox wajib menunggu persetujuan (ACC manual) dari Pak Satya.

---

### 🚀 TAHAP 2: PRODUKSI AUDIOVISUAL & PUBLIKASI (SETELAH ACC PAK SATYA)
*Hanya dijalankan setelah Pak Satya memberikan konfirmasi ACC:*
1. **Ubah Kolom 15 [Status Naskah]** menjadi **`ACC`**.
2. **Racik 4 Prompt Visual 9:16**: Terjemahkan 4 babak naskah ke prompt fotografi photorealistic (standar 6-Layer Architecture: 9:16 vertikal, pencahayaan fajar, tekstur alam berembun, lensa 35mm f/1.4, bebas CGI/watermark).
3. **Eksekusi Engine make_cinematic_video.py**:
   - Generate otomatis 4 gambar baru via OmniRoute (`antigravity/gemini-3.1-flash-image`).
   - Sintesis audio Dual-Voice (`jv-ID-DimasNeural` untuk Sabda Jawa + `id-ID-ArdiNeural` untuk refleksi Indonesia) lengkap dengan Dynamic Sacred Pauses jeda hening 1.5–2.5 detik.
   - Ekstraksi subtitle frame-by-frame via Faster-Whisper (.ass).
   - Render MP4 subpixel bicubic motion + crossfade (1080x1920 Full HD).
4. **Upload YouTube**: Unggah ke channel `@siswatalkstv` dengan status publik (`privacy="public"`), judul resmi (maksimal 100 karakter), deskripsi ber-hook, link ekosistem, dan 15 hashtag.
5. **Publikasi Ekosistem**: Terbitkan ke Google Docs (folder `1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U`, permission anyone with link as writer) dan Web Kontemplasi (`sync_kontemplasi.sh` ke GitHub Pages).
6. **Mandat Master Produksi V8 & Laporan**: Lengkapi Kolom 16 s.d. 22 di tab `Master Produksi V8`:
   - Col 16 (P) `Status Audio TTS` -> Tulis teks: `"Render"` (DILARANG "Selesai Render")
   - Col 17 (Q) `Status Video MP4` -> Tulis teks: `"Rendered"` (DILARANG "Selesai Render")
   - Col 18 (R) `Status Upload YT` -> Tulis teks: `"Uploaded"` (DILARANG "Uploaded (Public)")
   - Col 19 (S) `Link YouTube` -> Tulis langsung URL mentah lengkap yang dapat diklik (DILARANG menggunakan formula `=HYPERLINK`)
   - Col 20 (T) `Link Web Pustaka` -> Tulis langsung URL mentah lengkap yang dapat diklik (DILARANG menggunakan formula `=HYPERLINK`)
   - Col 21 (U) `Link Google Docs` -> Tulis langsung URL mentah lengkap yang dapat diklik (DILARANG menggunakan formula `=HYPERLINK`)
   - Col 22 (V) `Status Siar WA/TG` -> Tulis teks: `"Siap Siar"` (sebelum siar) atau `"Done"` (setelah penyiaran selesai).
7. Kirimkan laporan final beserta seluruh tautan aktif ke Telegram Pak Satya (thread 1096).

## 📌 MANDAT 2: BATASAN BAHASA & PAUGERAN DOA MUTLAK (STRICT BOUNDARY)
1. **SATU-SATUNYA** bagian yang menggunakan Bahasa Jawa adalah kolom/bagian `[Kutipan Sabda Jawa]` (100% teks kanonikal verbatim).
2. **SELURUH** uraian naskah lainnya (Terjemahan Sabda, Pangilon Rasa Paragraf 1 & 2, Laku Penyiswaan, Jangkar Batin / Mutiara Rasa, Deskripsi YouTube, Google Docs, dan Web Kontemplasi) **WAJIB 100% MENGGUNAKAN BAHASA INDONESIA** yang komunikatif, hangat, jernih, dan mengalir.
3. **PAUGERAN DOA & BERKAH KANONIKAL**:
   - DILARANG KERAS membuat pilar atau section tersendiri berisi "Doa Ritual / Doa Permohonan".
   - TETAPI di akhir Jangkar Batin, **WAJIB MENYERTAKAN KALIMAT BERKAH KANONIKAL RESMI**:
     `Semoga kita semua senantiasa berlimpah dengan sih, tuntunan, pepadang, dan pangayoman dari Sang Guru Sejati. Satuhu. 🙏`
     (DILARANG KERAS menghapus atau membuang kalimat berkah resmi ini!).
4. **Istilah Resmi**: Wajib menggunakan **`Renungan Penyiswaan`** (dengan 'e', bukan Panyiswaan atau Panyiswaan Pangestu).
5. **Akurasi Fakta Sejarah**: Ajaran Sang Guru Sejati diturunkan pertama kali pada **14 Februari 1932** di Surakarta kepada Bapak R. Soenarto Mertowardojo (belum genap 1 abad). DILARANG KERAS menulis klaim halusinasi seperti "berabad-abad lampau / lalu".
6. **PANTANGAN KERAS**: DILARANG KERAS menulis satu paragraf pembahasan utuh dalam Bahasa Jawa!
7. **Penggunaan Istilah**: Istilah spiritual/filosofi Jawa (seperti *eling*, *angen-angen*, *heneng-hening*, *catur nepsu*, *pamasrahan*, dll.) sangat dianjurkan diselipkan sebagai konsep batin, tetapi struktur dan susunan kalimatnya tetap kalimat Bahasa Indonesia utuh.
8. **Persona Chat vs Naskah**: Persona santun Basa Jawi Krama Alus HANYA digunakan saat membalas obrolan sehari-hari dengan Pak Satya di Telegram. JANGAN PERNAH dibiarkan merembes masuk ke dalam teks naskah renungan publik!




## 📌 MANDAT 3: 4 PAUGERAN PENYUSUNAN NASKAH & KUTIPAN KANONIKAL (FINE-TUNING DISIPLIN)
Berdasarkan arahan mutlak Pak Satya Adi Dharma (Oktober 2026), seluruh penyusunan naskah renungan WAJIB mematuhi paugeran ini:

1. **Disiplin Konteks & Presisi Atribusi Penutur (PANTANGAN ASAL COMOT / CHERRY-PICKING)**:
   - DILARANG KERAS hanya mencocokkan kata kunci (*keyword matching*) lalu langsung mencaplok kalimat tanpa membaca konteksnya secara mendalam!
   - Sinox WAJIB membaca 1–2 babak utuh di sekitar teks yang akan dikutip untuk memahami:
     - **Siapa penuturnya**: Wajib membedakan secara tegas antara:
       - *Sabda langsung Sang Guru Sejati* (terutama di `[SSJ]` *Serat Sasangka Jati* dan `[SPRA]` *Sabda Pratama*).
       - *Wejangan Bimbingan Olahrasa Bapak Pangrasa* kepada para siswa (di `[BRSR]` *Bawa Raos Ing Salebeting Raos*).
       - *Refleksi Kang Kelana* (di `[UKK]` *Ulasan Kang Kelana*).
       - *Ular-ular Panuntun Juru Mengeti / Pakde Narto* (di `[UUJM]` *Ular-Ular Juru Mengeti*).
       - *Kajian ilmiah kedokteran jiwa Prof. Dr. dr. Soemantri* (di `[CJI]` *Candrajiwa Indonesia*).
     - **Kepada siapa diucapkan dan apa latar belakang masalahnya**: Apakah bimbingan pribadi kepada siswa (misal kepada Prabawa/Kemayan), atau renungan umum.
     - **Presisi Penyebutan dalam Naskah**: Dilarang menyebut *"Sang Guru Sejati berpesan..."* jika yang berbicara adalah Bapak Pangrasa atau tokoh lain. Atribusi penutur harus 100% jujur, jernih, dan akurat.

2. **Kutipan Sabda 100% VERBATIM MUTLAK (PANTANGAN SPLICING & ANTI-PARAPHRASING)**:
   - DILARANG KERAS memotong tengah kalimat, meringkas anak kalimat, atau menyambung dengan kata-kata karangan AI sendiri!
   - Setiap kata, tanda baca, koma, dan titik WAJIB 100% identik karakter per karakter dengan berkas fisik pustaka di `/home/satyaaditech/share/pangestu_studi/`.
   - Jika mengambil kalimat, ambil kalimat utuh tanpa membuang kata di dalamnya. Menghilangkan atau mengganti satu frasa saja sudah tergolong menyusupkan pikiran AI ke dalam teks kanonikal, dan ini adalah PELANGGARAN FATAL.

3. **Uraian Pangilon Rasa Wajib Memuat 'Inner Shifting' & Pedagogi Anti-Dogma (Pergeseran Kesadaran Somatik yang Nyata)**:
   - **Anti-Dogma & Humanis**: Hindari instruksi klise atau dogma hampa (seperti *"pejamkan mata dan berpasrahlah"* tanpa penjelasan mekanisme nyata). Memejamkan mata tidak serta-merta membuat pikiran istirahat dari dunia; jika kesadaran masih 'berkemah' di dalam kepala, kegelapan di balik mata justru menjadi panggung bioskop bagi keliaran pikiran (*Default Mode Network* / *angen-angen*).
   - **Mekanisme Pergeseran Kesadaran yang Sengaja (*Intentional Awareness Shift*)**:
     - *Menyadari Posisi Kesadaran*: Sadari bahwa perhatian sedang terkunci tegang di area dahi, mata, atau tempurung kepala (*utek*).
     - *Memutus Kreteg Otak (Shift Down)*: Secara sengaja dan sadar, jatuhkan titik perhatian turun ke bawah: pindahkan kesadaran dari kepala menuju rongga dada (*telenging ati / rasa hening*).
     - *Berlabuh pada Sensasi Fisik Napas*: Alih-alih memikirkan konsep tenang, rasakan secara fisik aliran udara sejuk masuk dan hangat keluar di bagian tengah dada.
     - *Sikap Heneng (Saksi Hening)*: Dari ruang dada, pandanglah pikiran di kepala seperti kendaraan yang lewat di jalan raya jauh di luar rumah. Jangan didebat, jangan dikejar, jangan dinaiki.
     - *Nalar Lerem Menuju Hening*: Ketika perhatian berhenti menyuplai bahan bakar ke sirkuit otak di kepala, nalar dengan sendirinya akan mengendap (*lerem*) menuju keheningan sejati (*hening*).
   - **Bahasa Mengalir (*Nge-flow*), Membumi, dan Humanis**: Tulislah dengan empati mendalam laksana seorang sahabat seperjalanan (*mirror, not megaphone*), mengakui kerapuhan dan kelelahan manusiawi pembaca di era digital, bukan menggurui.

4. **Korelasi Kuat, Sumber Fleksibel & Bebas Jawa jika Pustaka Asli Bahasa Indonesia**:
   - Sumber kutipan TIDAK HARUS selalu dari *Serat Sasangka Jati* [SSJ]. Boleh dari seluruh buku kanonikal Paguyuban Ngesti Tunggal (`[BRSR]`, `[SKH]`, `[UUJM]`, `[TKL]`, `[SPRA]`, `[CJI]`, `[UKK]`, `[OLHR]`, `[WSJ]`, `[ASBS]`).
   - Jika rujukan yang dipilih berasal dari buku yang aslinya berbahasa Indonesia (misal *Sabda Khusus* [SKH], *Candrajiwa Indonesia* [CJI]), kutipan diperbolehkan **HANYA DALAM BAHASA INDONESIA** tanpa memaksakan terjemahan Jawa buatan.


## 🔄 ALGORITMA 4-TAHAP KURASI KANONIKAL SINOX (CONTEXTUAL RETRIEVAL & VERIFICATION LOOP)
*Wajib dijalankan secara ketat oleh Sinox pada setiap penyusunan draf renungan harian:*

1. **Tahap 1: Deep Scanning Multititik (Pindai Seluruh Pustaka)**:
   - Berdasarkan judul dan tema renungan, Sinox memindai direktori `/home/satyaaditech/share/pangestu_studi/` yang memuat seluruh pustaka kanonikal ([SSJ], [BRSR], [SKH], [UUJM], [TKL], [SPRA], [CJI], [UKK], [OLHR], [WSJ], [ASBS]).
   - Cari kata kunci dan topik yang berpotensi relevan.

2. **Tahap 2: Jendela Baca Minimal 1 Halaman (Context Window Expansion ±1.500–2.000 Karakter)**:
   - Begitu menemukan kata atau paragraf yang relevan, **DILARANG LANGSUNG MENCAPLOK KALIMAT ITU!**
   - Sinox WAJIB membuka dan membaca minimal 1 halaman penuh (kurang lebih 1.500–2.000 karakter, atau beberapa paragraf ke atas dan ke bawah).
   - Telusuri judul bab, situasi percakapan, dan siapa subjek penuturnya (Sang Guru Sejati, Bapak Pangrasa, siswa seperti Prabawa/Kemayan yang sedang bertanya, atau penutur lainnya).

3. **Tahap 3: Uji Resonansi Konteks & Filter Loop (Context Matching Loop)**:
   - Sinox menguji: Apakah konteks pembicaraan pada halaman tersebut benar-benar sejalan dengan pesan batin yang akan diuraikan pada renungan hari ini?
   - **JIKA BELUM COCOK / KONTEKS BEDA**: Tolak kandidat teks tersebut! Lanjutkan pencarian (*looping*) ke bab lain atau buku lain. Ulangi proses hingga menemukan babak yang konteksnya benar-benar beresonansi kuat.
   - **JIKA SUDAH COCOK & RESONAN**: Kunci rujukan dan tentukan siapa penutur aslinya untuk atribusi jujur di Pangilon Rasa.

4. **Tahap 4: Ekstraksi Verbatim Utuh & Presisi (Boundary & Verbatim Integrity)**:
   - Ambil 2–3 kalimat yang paling tajam dengan syarat:
     - **Kalimat Utuh**: Tidak boleh memotong anak kalimat di tengah jalan. Struktur kalimat harus lengkap dan maknanya tuntas.
     - **100% Verbatim**: Huruf, kata, tanda baca persis apa adanya dari berkas fisik. Dilarang keras splicing atau menyelipkan kata karangan AI sendiri.
     - **Mudah Dipahami**: Penggalan kalimat enak dibaca dan dipahami oleh orang awam.


## 🎙️ STANDAR VOKAL DUAL-VOICE (LOCKED — Oktober 2026)

Produksi vokal resmi menggunakan **Edge-TTS server-side otomatis** (bukan Gemini Canvas manual):

| Suara | Peran | Kalibrasi Kontemplatif (LOCKED) |
|---|---|---|
| `jv-ID-DimasNeural` | **Khusus petikan Sabda Jawa verbatim** — medhok, wibawa, khidmat, hening | Tempo **`-20%`**, Pitch **`-3Hz`** |
| `id-ID-ArdiNeural` | **Seluruh narasi Indonesia** — Salam, Jarwa, Pangilon Rasa, Laku Penyiswaan, Jangkar Batin | Tempo **`-22%`**, Pitch **`-3Hz`** |

- **Dynamic Sacred Pauses (Jeda Hening Bernapas)**:
  * Jeda setelah Judul/Salam: `2.0 detik`
  * Jeda setelah Sabda Jawa selesai: **`2.5 s.d. 3.0 detik`** (wajib lapang agar getaran sabda mengendap di rongga dada sebelum narasi refleksi dimulai).
  * Jeda antara Pangilon Rasa dan Laku Penyiswaan: `2.0 s.d. 2.5 detik`
  * Jeda sebelum Mutiara Rasa / Salam Penutup: `2.0 detik` (TIDAK ADA materi doa ritual)
- **Engine script resmi**: `scripts/make_cinematic_video.py` — Ken Burns Sub-Pixel Bicubic Zoom Motion + cross-dissolve xfade.
- **Pitfall CLI edge-tts**: Nilai negatif pada argumen CLI (misal tempo `-13%` atau pitch `-3Hz`) memicu error parser jika dipisah spasi (`unrecognized arguments: -13%`). Wajib gunakan format tanda sama dengan: `f"--rate={rate}"`, `f"--pitch={pitch}"`, `f"--voice={voice}"`.
- **Python Runtime Environment**: Eksekusi pipeline script yang memerlukan `googleapiclient`, `faster-whisper`, atau `edge-tts` wajib menggunakan venv hermes `/home/satyaaditech/.hermes/installs/a362db0e5ab40a5f/environments/b81016b623d94985b9b22f73d36f59e0/venv/bin/python3`, bukan Python sistem `/usr/bin/python3`.
- **Status Transisi YouTube (Unlisted ke Public)**: Token OAuth `token.json` hanya memiliki scope `upload` & `readonly`. Mengubah status video via API `videos().update` akan gagal (403 PERMISSION_DENIED). Rekomendasikan Pak Satya toggle visibility di YouTube Studio (link tetap utuh), atau re-upload otomatis dengan parameter `public` lalu perbarui link di Sheet, Docs, Web, dan teks siar WA.
- **Preset FFmpeg**: Gunakan `veryfast` + `-threads 0` pada server 4-core. Preset `fast` terlalu lambat (0.4x realtime).

---

## 🎬 STANDAR VIDEO VERTICAL & TIPOGRAFI SUBTITLE (LOCKED — Oktober 2026)
*Berdasarkan persetujuan resmi Pak Satya Adi Dharma*:

* **Font Subtitle Baku**: `Montserrat` (SemiBold / Bold) — dipasang di server Hermes (`/usr/share/fonts/truetype/montserrat/`).
* **Ukuran Font**: **Size 62** (proporsi ideal dan sangat nyaman dibaca di smartphone).
* **Posisi Subtitle**: `Alignment: 5` (Middle-Center, tepat di tengah layar Y=960).
* **Translucent Contrast Box**: `w=940, h=340, x=70, y=790, color=black@0.65` (melindungi keterbacaan teks di atas gambar AI dinamis).
* **Palet Warna Baku (Dual-Tone Editorial Styling)**:
  - **Baris 1 (Atas)**: `Champagne Gold (#F2D091)` / ASS: `{\c&H0091D0F2&}`
  - **Baris 2 (Bawah)**: `Warm Ivory White (#F8F9FA)` / ASS: `{\c&H00F8F9FA&}`
  - Outline: Hitam murni tebal 2px, Shadow 2px.
* **Aturan Pemenggalan Kata (Semantic Chunking)**:
  - Maksimal **7–10 kata per slide** (batas mutlak 11 kata). DILARANG menampilkan 1-2 kalimat panjang sekaligus.
  - Dibagi seimbang menjadi 2 baris pendek (3–5 kata baris 1 Gold, 3–5 kata baris 2 White).
* **Gerakan Kamera (Ken Burns Sumbu Z - Tanpa Pan Left/Right)**:
  - Layar vertikal 9:16 sangat sempit horizontal sehingga Pan Left/Right terasa memusingkan (*jarring*) dan menarik mata menjauhi teks di tengah.
  - Standar baku mengadopsi **Ken Burns Slow Zoom In / Zoom Out (Sumbu Z)** bergantian antar scene:
    - **Scene 1 (Sabda Jawa)**: `Slow Zoom In` (fokus ditarik masuk ke kedalaman sabda suci)
    - **Scene 2 (Pangilon Rasa)**: `Slow Zoom Out` (membuka kelapangan pandangan hidup)
    - **Scene 3 (Laku Panyiswan)**: `Slow Zoom In` (menarik perhatian ke rongga dada & napas hening)
    - **Scene 4 (Jangkar Batin & Berkah)**: `Slow Zoom Out` (pasrah sumarah & memancarkan berkah keselamatan)

---

## 📊 STANDAR STATUS & PENGISIAN MASTER PRODUKSI V8 (LOCKED SPEC)
*Disepakati bersama Pak Satya Adi Dharma (Oktober 2026)*:

Urutan Kolom (22 Kolom Baku):
1. `[No]` : Mengikuti urutan nomor sebelumnya (1, 2, 3, ...)
2. `[Tgl Rilis WA]` : Format YYYY-MM-DD
3. `[Hari & Pasaran]` : Hari Jawa (contoh: Senin Pahing)
4. `[Bulan]` : Bulan dan Tahun (contoh: Oktober 2026)
5. `[Tema Bulanan]` : Payung tema besar bulanan
6. `[Tema Mingguan]` : Sub-tema mingguan (4 facet per bulan)
7. `[Judul Renungan]` : Judul magnetik sains/kekinian + tujuan rohani
8. `[Rujukan Kitab & Bab]` : Kitab kanonikal terkunci ([SSJ], [SKH], dll.)
9. `[Kutipan Sabda Jawa]` : 100% verbatim teks Jawa kanonikal
10. `[Terjemahan Sabda]` : Terjemahan bahasa Indonesia resmi/selaras
11. `[Pangilon Rasa]` : 2 paragraf (Hook sains modern & Bedhah Kasunyatan SGS)
12. `[Laku Panyiswan]` : Latihan 30 detik + Somatic habit trigger
13. `[Mutiara Rasa]` : Aforisme paradoks 1 kalimat
14. `[Pertanyaan Refleksi]` : Pertanyaan refleksi Sentence Case
15. `[Status Naskah]` :
    - Teks: `Menunggu ACC Manual Pak Satya` (saat draf dibuat) -> berubah menjadi `ACC` (Hijau) setelah disetujui Pak Satya.
16. `[Status Audio TTS]` :
    - Teks: `Render` (Hijau) — DILARANG menulis "Selesai Render" atau "Belum Render".
17. `[Status Video MP4]` :
    - Teks: `Rendered` (Hijau) — DILARANG menulis "Selesai Render" atau "Belum Rendered".
18. `[Status Upload YT]` :
    - Teks: `Uploaded` (Hijau) — DILARANG menulis "Uploaded (Public)" atau "Not Uploaded".
19. `[Link YouTube]` :
    - Tulis langsung URL mentah lengkap yang dapat diklik: `https://youtu.be/[video_id]`. **DILARANG menggunakan formula `=HYPERLINK`**.
20. `[Link Web Pustaka]` :
    - Tulis langsung URL mentah lengkap yang dapat diklik: `https://kontemplasi.satyaaditech.web.id/#[slug]`. **DILARANG menggunakan formula `=HYPERLINK`**.
21. `[Link Google Docs]` :
    - Tulis langsung URL mentah lengkap yang dapat diklik: `https://docs.google.com/document/d/[doc_id]/edit`. **DILARANG menggunakan formula `=HYPERLINK`**.
22. `[Status Siar WA/TG]` :
    - Teks: `Siap Siar` (sebelum penyiaran dimulai) -> berubah menjadi `Done` (Hijau) setelah penyiaran selesai.

*Warna Visual Dashboard (Conditional Formatting)*:
- Status 'Belum' / 'Not' -> Latar Belakang Oranye Lembut (#FFE0B2), teks tebal cokelat jingga.
- Status 'ACC' / 'Selesai' -> Latar Belakang Hijau Segar (#C8E6C9), teks tebal hijau gelap.

*Mandat Mengikuti Jadwal Google Sheet (Master Produksi V8)*:
- DILARANG keras mengarang/memilih topik sendiri atau bertanya kepada pengguna "apakah sudah ada topik/ayat yang ingin dipilih?".
- Setiap pembuatan renungan harian WAJIB membaca jadwal yang sudah tersusun di Google Sheet Master (`1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`) tab `Master Produksi V8` berdasarkan tanggal hari ini (atau baris berikutnya yang berstatus `Belum ACC`).
- Seluruh tema bulanan, tema mingguan, judul, rujukan pustaka, dan sabda harus selaras dengan jadwal di Master Produksi V8.

*Mandat Pembaruan Mandiri Spreadsheet (Aturan Baku Kolom 16 s.d. 22)*:
- Asisten (Hermes/Sinox) WAJIB mengisi dan memperbarui seluruh 22 kolom di tab `Master Produksi V8` secara komplit tanpa ada yang terlewat, dengan aturan nilai teks baku sebagai berikut:
  * **Col 16 (P)** `Status Audio TTS` -> Tulis teks: `"Render"` (DILARANG menulis "Selesai Render")
  * **Col 17 (Q)** `Status Video MP4` -> Tulis teks: `"Rendered"` (DILARANG menulis "Selesai Render")
  * **Col 18 (R)** `Status Upload YT` -> Tulis teks: `"Uploaded"` (DILARANG menulis "Uploaded (Public)")
  * **Col 19 (S)** `Link YouTube` -> Tulis langsung URL lengkap yang dapat diklik: `https://youtu.be/[video_id]` (DILARANG menggunakan formula `=HYPERLINK`)
  * **Col 20 (T)** `Link Web Pustaka` -> Tulis langsung URL lengkap yang dapat diklik: `https://kontemplasi.satyaaditech.web.id/#[slug]` (DILARANG menggunakan formula `=HYPERLINK`)
  * **Col 21 (U)** `Link Google Docs` -> Tulis langsung URL lengkap yang dapat diklik: `https://docs.google.com/document/d/[doc_id]/edit` (DILARANG menggunakan formula `=HYPERLINK`)
  * **Col 22 (V)** `Status Siar WA/TG` -> Tulis teks: `"Siap Siar"` (sebelum siar dimulai) atau `"Done"` (setelah penyiaran selesai)
- Transisi Status: Draf dibuat -> `Menunggu ACC Manual Pak Satya` (Orange); Disetujui -> `ACC` (Hijau); Audio/Video/Upload selesai -> `Render` / `Rendered` / `Uploaded` + URL mentah langsung yang dapat diklik (DILARANG =HYPERLINK); Status Siar -> `Siap Siar`; Siar selesai -> `Done` (Hijau).

*Mandat Teks Siar WhatsApp & Telegram (Struktur Link Baku)*:
- Bagian Atas / Header (di bawah Judul Tema sebelum Salam Karahayon): WAJIB menyematkan link YouTube (`🎧 *Dengarkan di YouTube*: [URL]`).
- Bagian Bawah / Footer (di bawah Jangkar Batin & Salam Karahayon): WAJIB menyematkan 2 tautan ekosistem digital:
  1. `🌐 *Baca Selengkapnya di Web Pustaka*: [URL Web Kontemplasi]`
  2. `📄 *Versi Dokumen Google Docs*: [URL Google Doc]`

*Mandat Deskripsi YouTube (Keren, Menggigit & Viral — Anti-Lempeng)*:
- Baris 1–2 (Magnetic Hook): Pertanyaan atau dilema psikologis/neurosains yang sangat relate dengan keseharian (ditampilkan di 150 karakter pertama sebelum tombol Show More / Lainnya).
- Paragraf 2–3 (Pangilon Rasa / Bedhah Kasunyatan): Mengupas akar masalah (misal overthinking, mode otopilot DMN, burnout mental) dan menghubungkannya dengan solusi Ajaran Sang Guru Sejati (Kusir Angen-angen vs Tripurusa).
- Kutipan Pethikan Sabda Kanonikal: Sabda Jawa kanonikal verbatim beserta terjemahan bahasa Indonesianya.
- Laku Praktis (Micro-Habit 30 Detik): Panduan aplikatif konkrit yang bisa langsung dicoba penonton hari ini.
- Mutiara Rasa: 1 kalimat aforisme paradoks mendalam.
- Ekosistem Digital: Tautan lengkap ke Web Kontemplasi (`https://kontemplasi.satyaaditech.web.id/#[slug]`) dan Google Docs.
- Salam Penutup Karahayon: 1 kalimat berkah sejuk (DILARANG narasi/paragraf doa ritual panjang).
- Hashtags Viral & High-Traffic (10–15 tags): Kombinasi spiritualitas, mindfulness, sains, filosofi Jawa, dan Shorts (contoh: `#Eling #DefaultModeNetwork #Mindfulness #Overthinking #OlahRasa #Pangestu #SangGuruSejati #FilosofiJawa #StoikismeJawa #KetenanganBatin #KesadaranDiri #SadarJiwa #KesehatanMental #Shorts #RenunganHarian`).
- 🚫 **PANTANG MUTLAK**: DILARANG KERAS mencantumkan nama model TTS / AI teknis (seperti `jv-ID-DimasNeural`, `id-ID-ArdiNeural`, teks prompt, atau backend engine) pada deskripsi YouTube publik. Deskripsi adalah sarana edukasi dan siar rohani, bukan catatan teknis sistem.

## 🎬 ALUR PRODUKSI VIDEO SINEMATIK V8 (NANO BANANA + SUBPIXEL MOTION)
*Panduan Eksekusi Mandiri untuk Hermes Agent (Oktober 2026)*

Hermes bertindak sebagai Orkestrator Utama produksi video renungan vertikal 9:16 (1080x1920 Full HD).

### 1. Kapan Video Diproduksi?
Hermes memantau baris Google Sheet Master V8 (`1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`).
Trigger eksekusi terjadi ketika:
* `[Status Naskah]` = **`ACC`** (kolom 15), DAN
* `[Status Video MP4]` = **`Belum Rendered`** (kolom 17).
* **Trigger Perintah Chat (Shortcut Baku)**: Ketika Pak Satya memberikan perintah chat:
  `"Buatkan Renungan Hari Ini..."` (atau variasi: `"Buatkan Renungan Hari Ini [tgl/topik]"`), Sinox WAJIB menjalankan Alur Kerja 2-Tahap: Tahap 1 menyusun draf naskah 4-Pilar Lean, mengisi kolom H–N di Master Sheet V8, menandai Kolom 15 `Menunggu ACC Manual Pak Satya`, melapor ke Telegram (thread 1096 & pribadi), lalu STOP dan WAJIB menunggu persetujuan (ACC manual) dari Pak Satya sebelum melanjutkan ke Tahap 2 (produksi audio, video, dan publikasi).

### 2. Langkah 1: Ekstraksi Metafora Visual & Prompting 9:16 (Tahap 2 Setelah ACC)
* **Aturan Kunci**: Latar visual latar **100% DINAMIS dan UNIK** di setiap renungan. Sinox merumuskan 4 prompt gambar 9:16 yang langsung merefleksikan 4 babak renungan (Babak 1 Sabda, Babak 2 Masalah/Otopilot Batin, Babak 3 Laku Hening, Babak 4 Resolusi Kasampurnan).
* **Standar Arsitektur Prompting (6-Layer Photorealistic Architecture)**:
  Sinox menyusun prompt dalam Bahasa Inggris sinematik teknis merujuk skill `creative/photorealistic-image-generation`:
  1. `Layer 1 (Framing)`: Vertical 9:16 composition, medium wide shot / intimate macro close-up.
  2. `Layer 2 (Core Subject)`: Simbol alam/batin nyata (misal: aged teakwood joglo pillar, mossy river stone in crystal clear stream, earthenware bowl catching rainwater, morning dew on lotus leaf). DILARANG fantasi/mistis.
  3. `Layer 3 (Micro-Materiality)`: Authentic rough textures, natural dampness, micro wood grain, fine cracks.
  4. `Layer 4 (Lighting Physics)`: Diffused dawn ambient glow, volumetric god rays, candlelight chiaroscuro, natural shadow falloff.
  5. `Layer 5 (Camera Optics)`: Shot on Hasselblad H6D-100c / Leica M11, 35mm f/1.4 or 80mm f/2.8 lens, shallow depth of field, creamy natural background bokeh.
  6. `Layer 6 (Reality Anchor)`: Raw documentary photojournalism, authentic textures, no CGI gloss, no artificial sheen, no text, no watermark.

### 3. Langkah 2: Eksekusi Engine Video Sinematik (make_cinematic_video.py)
Hermes menyusun file konfigurasi `/tmp/renungan_config.json` yang memuat `audio_blocks` dan `scenes` (berisi 4 `prompt` visual yang telah diracik), lalu memanggil engine produksi resmi:
```bash
python3 /home/satyaaditech/.hermes/skills/pangestu-renungan-harian/scripts/make_cinematic_video.py --config /path/to/devotional_config.json
```
Skrip ini secara otomatis memproses:
1. **Otomatis Generate 4 Gambar Visual 9:16**: Engine langsung memanggil OmniRoute (`http://127.0.0.1:20128/v1/images/generations`, model `antigravity/gemini-3.1-flash-image`). OmniRoute secara otomatis mem-bypass akun usia terbatas (`kentutkubukanboongan@gmail.com`) dan menggunakan akun Google terverifikasi, menghasilkan 4 gambar 9:16 photorealistic berkualitas tinggi dalam ~16 detik.
2. **Dual-Voice Edge-TTS**: Mensintesis `jv-ID-DimasNeural` (Sabda Jawa) + `id-ID-ArdiNeural` (Narasi refleksi Indonesia) lengkap dengan **Dynamic Sacred Pauses** (jeda 1.5s - 2.5s).
3. **Penyelarasan Durasi Dinamis**: Menghitung durasi riil audio dan membagi durasi 4 scene secara presisi dan seimbang.
4. **Whisper AI Subtitle Alignment**: Mengekstrak timestamp kata/frasa nyata dan menyusun subtitle `.ass` berkontras tinggi (emas, cyan, mint, putih, bebas emoji).
5. **FFmpeg Sub-Pixel Motion & Crossfade**: Me-render video dengan filter `perspective=...:interpolation=cubic` (zero-jitter) dan transisi `xfade` halus 1 detik di setiap jeda babak.
6. **Transfer & Storage Hygiene**: Menyimpan video final di `/home/satyaaditech/share/viral_sample/`, opsional transfer ke Mac `~/Downloads/`, dan membersihkan file sementara.

### 4. Langkah 3: Update Sheet & Laporan ke Pengguna
* Hermes mengubah kolom 17 `[Status Video MP4]` menjadi **`Rendered`**.
* Hermes mengirim notifikasi ke chat Telegram pengguna bahwa video siap dinikmati.
* Referensi teknis lengkap: `references/sop-produksi-video-sinematik-v8.md`.

## 🎓 STANDAR PEDAGOGI & PROSEDUR RISET RENUNGAN (MASTER EDUCATOR)
*Disepakati bersama Pak Satya Adi Dharma (Oktober 2026)*:

1. **Riset Matriks Silang Pustaka (Deep Cross-Reference Matrix)**:
   - Satu tema besar bulanan (misal: "Sabar") wajib diriset silang menyeluruh di 11 pustaka kanonikal terkunci (SSJ, SKH, BRSR, UUJM, TKL, SPRA, WSJ, ASBS, UKK, OLHR, CJI).
   - Setiap renungan harian mengangkat sudut pandang (facet) berbeda dengan kutipan sabda/wejangan yang bervariasi dan non-redundant.

2. **Pendekatan Master Educator (Sistematis A - Z)**:
   - Menjabarkan topik secara pedagogis: dari fondasi awal, anatomi batin/nafsu, friksi relasi sosial, ujian hidup/karier, hingga puncak kasampurnan pamasrahan batin.

3. **Jembatan Sains Modern & Konteks Kekinian**:
   - Menghubungkan ajaran SGS dengan ilmu pengetahuan mutakhir (neurosains: lonjakan hormon kortisol, pembajakan amigdala, aktivasi parasimpatetis; psikologi modern: burnout, kecemasan digital, validasi semu medsos).
   - Menjelaskan bagaimana laku heneng-hening & olahrasa SGS menyelesaikan akar masalah biologis dan psikologis tersebut.

4. **Formula Judul Magnetik (Kekinian/Sains + Solusi Kasampurnan)**:
   - Judul menggabungkan fenomena modern/sains dengan tujuan rohani (contoh: *Seni Mematikan Api Sebelum Menjadi Kebakaran: Waspadai Lonjakan Hormon Kortisol Anda 🌿*).
   - Menarik dan menggugah rasa penasaran pembaca awam, humanis, namun ANTI-CLICKBAIT (relevan dan murni berakar pada isi naskah).
   - Menjaga wibawa spiritual: hindari tanda seru ganda (!!), gunakan emoji sejuk dan kalimat reflektif.

5. **5 Pilar Bobot Mutu Baku (Mandat Pak Satya — Continuous Elevation)**:
   Setiap pembuatan renungan harian WAJIB lolos kurasi 5 pilar sebelum diajukan ke Pak Satya:
   - **Pilar 1: Sugih Insight ("Aha-Moment", Bukan Nasihat Klise)**: Mengupas akar psikologis dan spiritual terdalam, menyingkap ilusi nalar/ego, bukan sekadar wejangan moral normatif.
   - **Pilar 2: Relate Kehidupan Modern & Sains Modern**: Masuk lewat situasi nyata abad ke-21 (overthinking, screen fatigue, media sosial, beban kerja) dan dianyam dengan sains modern sebagai cermin logis.
   - **Pilar 3: Sudut Pandang Selalu Segar (Fresh Perspective)**: Mengangkat sudut pandang unik dan paradoks dari setiap sabda (pantang formula monoton atau sudut pandang yang sama berturut-turut).
   - **Pilar 4: Bernyawa, Luwes, & Nge-Flow (Organic Cadence)**: Irama bernapas, kanca lumaku di warung kopi, runtun, hangat, menyentuh rasa, bebas dari gaya robot AI atau penceramah mimbar.
   - **Pilar 5: Jero Nanging Wening kanggé Awam (Deep yet Crystal Clear)**: Bagaikan telaga yang sangat dalam namun berair bening kristal sehingga dasarnya mudah dipahami oleh siapa saja tanpa kebingungan kognitif.

## 🌟 CITHAKAN STANDAR EMAS (GOLDEN TEMPLATE V8 - LEAN 4-PILAR)
*Disepakati bersama Pak Satya Adi Dharma (Oktober 2026)*:
- Format acuan: `references/GOLDEN_SAMPLE_v8_SABAR.md` dan `templates/format-baku.md`.
- **Struktur 4 Pilar**:
  1. `*📖 KUTIPAN TUNTUNAN :*` (Sabda Jawa Verbatim 100% + Terjemahan Indonesia tepat di bawahnya dalam tanda kurung miring).
  2. `💭 *PANGILON RASA :*` (2 Paragraf padat: Paragraf 1 The Human Hook / kahanan nyata -> Paragraf 2 Bedhah kasunyatan Catur Nepsu & pepadhang Sabda).
  3. `🧘 *LAKU PANYISWAN :*` (Latihan 30 Detik: Jeda Raga -> Mengheningkan Batin -> Bertindak Selaras Tuntunan; wajib ditautkan pada pemicu fisik / situasi nyata).
  4. `🎯 *JANGKAR BATIN :*` (Mutiara Rasa 1 baris + Pertanyaan Refleksi 1 baris).
- **Audio-First**: Link YouTube diletakkan persis di bawah judul tema di atas salam pembuka (`🎧 *Dengarkan di YouTube*: ...`).
- **Aturan Tipografi & Whitespace**:
  * Wajib 1 baris kosong (blank line) di bawah setiap subjudul seksi agar layout bernapas dan tidak tampak terlalu padat.
  * Label `Pertanyaan Refleksi` WAJIB ditulis Sentence Case (DILARANG huruf kapital semua `PERTANYAAN REFLEKSI`).
  * Gunakan istilah Bahasa Indonesia yang mudah dipahami (`Jeda Raga`, `Mengheningkan Batin`, `Bertindak Selaras Tuntunan`, `(Latihan 30 Detik)`).
- **Keseimbangan Visual (Emoji Guardrails)**:
  * Batasi 10–12 emotikon pilihan bernilai rasa (menjaga wibawa spiritual, hindari kesan spammy).
- **Footer Baku**:
  * Doa Penutup: `🙏 Semoga Kita Senantiasa Berlimpah dengan Sih, Tuntunan, Pepadang, Pangayoman dari Sang Guru Sejati. Satuhu 🙏`
  * Link Web: `🌐 *Baca Selengkapnya di Web Pustaka*: https://kontemplasi.satyaaditech.web.id/#[slug]`
  * Link GDoc: `📄 *Versi Dokumen Google Docs*: [Link GDoc]`

## ⚠️ Golden Rules & Pitfalls Format Baku (WAJIB DIPATUHI)
1. **Aturan Teologis & Larangan Istilah (STRICT THEOLOGICAL GUARDRAILS)**:
   * ❌ **DILARANG KERAS** menggunakan istilah: `ajaran Pangestu`, `agama Pangestu`.
   * ✅ **WAJIB**: Pangestu adalah **PAGUYUBAN / WADAH SISWA**. Ajarannya adalah **Ajaran Sang Guru Sejati** / **Piwulang Sang Guru Sejati** / **Piwulang Kasampurnan**.
   * ❌ **DILARANG KERAS** menggunakan istilah mistik/kejawen non-kanonikal seperti `lawang hawa sanga`.
   * ✅ **WAJIB**: Gunakan istilah kanonikal Serat Sasangka Jati: `pancadriya` / `indriya` / `hawa napsu patang prakara` (aluamah, amarah, supiyah, mutmainah) / `angen-angen`.
   * ❌ **DILARANG KERAS** menggunakan kata ganti `beliau` untuk Sang Guru Sejati (karena Sang Guru Sejati adalah Suksma Sejati / Roh Suci / Imateriil / Tunggal Allah).
   * ❌ **DILARANG KERAS COCOKLOGI**: Jangan memaksakan istilah luar (misal Socrates / filsafat barat) disangkutpautkan secara paksa merusak definisi baku Tri Sila (Eling, Pracaya, Mituhu) atau Hasta Sila. Saringan luar cukup dipaparkan sebagai analogi olah rasa tanpa mengubah atau menempelkan label palsu pada ajaran baku.
   * ❌ **DILARANG KERAS MEMODIFIKASI / MEMBUMBUI KUTIPAN SABDA (STRICT VERBATIM CANONICAL)**: Kutipan Sabda/wejangan WAJIB 100% VERBATIM sama persis dengan naskah kanonikal asli (`buku_ssj_jawa.txt`, `buku_brsr.txt`, `buku_skh.txt`, `buku_tkl.txt`). Dilarang memparafrasekan, mengarang istilah, atau menyisipkan kata sendiri.
   * 🛑 **KEKEBALAN NASKAH ACC (STRICT IMMUTABILITY OF APPROVED DRAFTS)**: Begitu naskah/draft renungan disetujui Pak Satya (misal: "aku sudah okey nox", "oke kita buat versi ini"), isi teks tersebut **DIKUNCI / FROZEN 100%**. DILARANG KERAS merombak, memparafrasekan ulang, mengganti susunan poin praktik/aplikasi, atau mengedit narasi Uraian di putaran berikutnya saat merakit GDoc/YouTube/Web/Broadcast. Naskah yang disetujui WAJIB disalin persis 100% ke seluruh aset output.
   * 🔗 **DAFTAR TAUTAN WAJIB LENGKAP (FOOTER LINKS)**: Format broadcast akhir WAJIB selalu menyertakan blok tautan lengkap di bagian bawah:
     ```text
     ---
     📖 Tautan Pustaka Digital & Dokumen:
     • 📺 Video YouTube : https://youtu.be/...
     • 📄 Google Doc : https://docs.google.com/document/d/.../edit
     • 🌐 Pustaka Web Kontemplasi : https://kontemplasi.satyaaditech.web.id/#<anchor>
     ```
   * 🎬 **FFMPEG STILLIMAGE VIDEO PARAMETER GUARD**: Saat merender video dari poster + audio:
     - WAJIB cantumkan `-framerate 2` SEBELUM `-i poster.png` agar FFmpeg tidak mengasumsikan input 25fps yang menyebabkan video terpotong (misal 6 menit terpotong jadi 2 menit).
     - Perintah baku: `ffmpeg -y -loop 1 -framerate 2 -i poster.png -i audio.mp3 -c:v libx264 -tune stillimage -preset ultrafast -c:a aac -b:a 192k -pix_fmt yuv420p -shortest output.mp4`
     - WAJIB validasi durasi video dengan `ffprobe` sebelum diunggah ke YouTube.
   * ✅ **TULISAN HUMANIS, BERNYAWA & MEMBUMI (RELATABLE)**: Bagian Uraian dan Renungan WAJIB menyentuh pergulatan batin konkret dalam kehidupan sehari-hari (misal: beban pikiran saat bangun pagi, reaktivitas emosi saat pesan di gawai menyinggung perasaan, dinamika di kantor/keluarga). Hindari gaya khotbah teoretis yang kaku atau menggurui; buat uraian terasa hangat, bernyawa, dan aplikatif.
   * ✅ **PENYELESAIAN PRODUKSI TUNTAS (END-TO-END PIPELINE)**: Setelah naskah di-ACC, selesaikan seluruh rantai produksi secara tuntas (Render Video MP4 -> Upload YouTube @siswatalkstv -> Format Google Doc rapi -> Sync Web GitHub Pages -> Log Master Sheet) dan sajikan output akhir lengkap beserta seluruh tautan aktif (YouTube, Docs, Web).al: dilarang mengganti *kamar-kamaran* menjadi *senthong*). Format wajib kutipan: **Bold Italic** (`#1B365D`) untuk isi Sabda dan **Bold Only** (`#0E4A6F`) untuk rujukan sumber.
2. **Dilarang Mengubah Nama Section**:
   * Section introspeksi 3 poin WAJIB bernama `📝 *APLIKASI* :`. DILARANG KERAS menggantinya menjadi `PERTANYAAN REFLEKSI`, `REFLEKSI DIRI`, dll.
   * Baris penutup di dalam `🧘 *PRAKTIK* :` wajib diakhiri kalimat standard: `✅ Latihan ini menumbuhkan ketenteraman batin dan menjaga kita tetap eling lan waspada di setiap langkah.`
2. **Kutipan Relevan & Padat (Condensation Guardrail)**:
   * Ambil pethikan sabda/buku kanonikal yang paling padat dan langsung relevan dengan tema inti (2–4 kalimat kunci). Hindari kutipan yang terlalu panjang atau melebar jika poin esensialnya sudah terwakili.
3. **Uraian Humanis, Membumi, & Relatable (Anti-Monoton)**:
   * ❌ **DILARANG**: Penjelasan yang kaku, dingin, abstrak, atau teoretis monoton.
   * ✅ **WAJIB**: Sentuh dinamika pergulatan batin manusia di kehidupan nyata sehari-hari (contoh: rasa lelah setelah bekerja, waktu/tenaga yang terasa dirampas saat rekan/keluarga minta bantuan mendadak, rasa kesal spontan ego/Sang Aku, godaan hitung-hitungan untung-rugi).
   * Sertakan analogi bersahaja dan contoh konkret laku sederhana (contoh: mendengarkan keluh kesah teman 15 menit tanpa menghakimi, membantu pekerjaan rumah tangga tanpa mengeluh, senyum tulus tanpa pamrih).
4. **Kelengkapan Tautan Teks WhatsApp Siap Sebar (Langkah 6)**:
   * Saat menyajikan naskah WhatsApp untuk disebarkan, pastikan selalu menyertakan blok tautan digital aktif di bagian bawah:
     - 📄 Google Doc
     - 🌐 Pustaka Web Kontemplasi (dengan anchor slug tanggal & tema, e.g. `https://kontemplasi.satyaaditech.web.id/#<slug>`)
     - 📺 Video YouTube (bila video sudah diunggah/tersedia).
5. **Signature Footer Mutlak**:
   * Signature penutup doa WAJIB verbatim dalam Bahasa Indonesia baku:
     `🙏 Semoga kita semua senantiasa berlimpah Tuntunan dan Perlindungan, Sih dari Sang Guru Sejati. Satuhu 🙏`
   * DILARANG KERAS menerjemahkan signature ini ke Bahasa Jawa atau menambahkan improvisasi kalimat penutup lainnya.
3. **Pemisahan Peran Produksi V8 (Otomasi Penuh Sinox/Hermes)**:
   * **Pak Satya**: Meninjau naskah di Google Sheet V8 dan mengubah status kolom 15 `[Status Naskah]` menjadi `ACC`.
   * **Sinox & Engine Otomatis**: Sinox memproses seluruh alur produksi secara mandiri via `make_cinematic_video.py` tanpa merepotkan Pak Satya membuat audio manual di browser:
     - **Dual-Voice Audio**: `jv-ID-DimasNeural` (Sabda Jawa medok khidmat) + `id-ID-ArdiNeural` (Narasi refleksi bariton sejuk hangat). Suara wanita dinilai kurang khidmat dan resmi diganti Ardi.
     - **Visual Nano Banana**: 4 gambar dinamis sesuai naskah (9:16 vertikal).
     - **Animasi Kamera**: Sub-pixel bicubic motion (bebas jitter) + cross-dissolve 1.0 detik.
     - **Distribusi**: Upload YouTube, GDoc, sync Web Kontemplasi, update Master Sheet V8, dan delivery video MP4 ke Mac `~/Downloads/`.
4. **FFmpeg Video Rendering & Durasi Utuh (WAJIB Portrait / Vertikal)**:
   * **Format Video Baku**: Mulai September 2026, format video renungan WAJIB menggunakan **rasio portrait/vertikal murni** (sesuai dimensi poster, e.g. 1024x1536 atau 9:16) agar tampilan optimal, cetha, dan penuh
   * **n8n Automation Runner**: Eksekusi rendering dan YouTube upload dipicu melalui automation runner service port 8089 (`http://172.17.0.1:8089/api/render-video`).
   * **Code Node HTTP Helper**: Di dalam n8n Code Node, gunakan `await this.helpers.httpRequest(...)`, bukan `fetch()`. saat disimak di layar HP. DILARANG memaksakan rasio landscape 16:9 dengan letterbox/blur kecuali diminta khusus.
   * **YouTube Python API Helper Return**: Script `upload_youtube.py` return object berupa dictionary `{"video_id": video_id, "url": share_url}`. Gunakan `res["video_id"]` atau `res["url"]` (bukan `res.get("id")`).
   * **Google Docs Inline Image Insertion**: Gambar poster yang disisipkan via `insertInlineImage` wajib diunggah ke Google Drive dengan permission `reader` for `anyone` terlebih dahulu dan menggunakan URI direct link `https://lh3.googleusercontent.com/d/<drive_id>`.
   * **3-Layer Quality Guard agar Video TIDAK PERNAH Terpotong**:
     1. **Pre-Probe Durasi Audio Eksak**: Gunakan `ffprobe` untuk membaca durasi audio mentah secara presisi (contoh: `400.04` detik).
     2. **Render Ultrafast Portrait Still-Image**: Gunakan `-preset ultrafast -r 2 -t <durasi_audio_eksak>`. Dengan `-r 2`, render video 7 menit selesai dalam 2-3 detik (jauh di bawah batas timeout terminal/n8n):
        `ffmpeg -y -loop 1 -i poster.png -i audio.mp3 -c:v libx264 -tune stillimage -preset ultrafast -r 2 -c:a aac -b:a 192k -pix_fmt yuv420p -t <duration> output.mp4`
     3. **Post-Render Verification Gate**: Sebelum mengunggah ke YouTube, sistem wajib memeriksa durasi output video dengan `ffprobe`. Jika selisih durasi video dengan audio `> 1.0 detik`, proses otomatis DIBATALKAN (abort upload) agar video cacat/terpotong tidak pernah terunggah ke YouTube.
   * Hindari default preset tanpa limit framerate/preset yang lambat karena akan terkena *command timeout* dan menghasilkan video terpotong (misal 60 detik padahal audio 400 detik).
   * **WAJIB verifikasi**: Selalu cek `ffprobe -v error -show_entries format=duration ...` pada file video dan audio untuk memastikan durasi sama persis sebelum diunggah ke YouTube.
5. **Orkestrasi Pipeline n8n**:
   * Saat workflow n8n (`u8DSPYtI7LNdDZbk`) aktif, jalankan seluruh rantai eksekusi melalui webhook trigger `POST https://n8n.satyaaditech.web.id/webhook/renungan-pipeline` (atau `http://localhost:5678/webhook/renungan-pipeline`) agar seluruh log 11 node tercatat rapi di dashboard n8n, jangan di-bypass lewat CLI manual.

## ⚠️ Konvensi Terminologi Utama (PENTING)
*   **Sang Guru Sejati (SGS)** punika ingkang kagungan piwulang utawi ajaran.
*   **Pangestu** (Paguyuban Ngesti Tunggal) punika namung wadhah utawi organisasi para siswa ingkang nyinaoni piwulang.
*   **Panyebutan ingkang Leres**: Wajib ngginakaken tembung **"piwulang Sang Guru Sejati"** utawi **"ajaran Sang Guru Sejati"**. Boten pareng babar pisan nyebataken **"piwulang Pangestu"** utawi **"ajaran Pangestu"**.
*   **Hakikat Sang Guru Sejati**: Sang Guru Sejati punika Suksma Sejati (Roh Suci), peranganing Tunggal Allah ingkang asipat imateriil lan langgeng. Sampun ngantos ngginakaken tembung sulih manungsa kados *"beliau"*, kedah dipun-sebat jangkep **"Sang Guru Sejati"**.
*   **Pembedaan Sabda vs Wejangan Tokoh (BRSR / TKL)**: Wonten ing Kitab *Bawa Raos Ing Salebeting Raos (BRSR)* utawi *Taman Kamulyan Langgeng (TKL)*, kathah wedharan ingkang awujud dialog/wejangan tokoh (tuladhanipun Bapak Pangrasa marang Prabawa ing BRSR Bab XIV utawi Bapak Pangrasa marang Sadherek Jatmika ing TKL). Pethikan punika sanes Sabda langsung, pramila dipun-serat minangka *Pethikan Dinten Punika* kanthi nyebutaken tokoh penuturipun (tuladha: `Taman Kamulyan Langgeng (TKL) (Wejangan Bapak Pangrasa marang Sadherek Jatmika) :`).
*   **Gaya Bahasa & Rasa Basa (Luwes, Lemes, Sastrawi)**: Draf uraian wajib menggunakan bahasa yang sangat halus, luwes, santun, sastrawi, dan meresap ke sanubari pembaca (menghindari gaya bahasa kaku, dangkal, mekanis, atau terjemahan harfiah AI). Selalu rujuk arsip draf renungan sebelumnya di `wiki/renungan/` sebagai standar emas (gold standard).
*   **Wajib Buka Vault & Wiki Terlebih Dahulu**: Sebelum menyusun draf, agen WAJIB memeriksa `references/buku-pangestu-wiki.md` dan arsip kanon di `/home/satyaaditech/shorts_factory/obsidian/BukuPangestu/books/` untuk mengambil kutipan verbatim 100% asli, bukan mengarang atau merangkum bebas dari ingatan model.
*   **Struktur Baku 6 Bagian**:
    1. Header (Hari, Weton/Tanggal, Edisi, Judul Puitis + Emojis 🌿🕊️, Salam Karahayon).
    2. PETHIKAN DINTEN PUNIKA (Sumber Bab detail & nama tokoh penutur jika BRSR/TKL) + Terjemahan.
    3. URAIAN (Mendalam, mengaitkan laku batin & kehidupan nyata).
    4. PRAKTIK SEHARI-HARI (3 poin konkret dengan ikon 🌾🌿🌅).
    5. RENUNGAN (Inti perenungan singkat).
    6. PERTANYAAN REFLEKSI (3 pertanyaan batin penuntun mawas diri 💭) + Doa Penutup (`🙏 Mugi kita sedaya tansah pinaringan Berkah, Pitedah, Sih Tuntunan tuwin Pangayomaning Sang Guru Sejati. Satuhu. 🙏`).
*   **Kemurnian Kutipan Sabda / Referensi (VERBATIM MUTLAK)**: DILARANG KERAS menyisipkan pikiran, kata-kata buatan sendiri, kesimpulan cipta, atau parafrase ke dalam blok kutipan Sabda/buku. Kutipan wajib 100% murni apa adanya persis dari teks sumber. Uraian, pemahaman, dan kontekstualisasi HANYA boleh ditempatkan di bagian pembahasan/uraian terpisah.
*   **Panjang & Relevansi Kutipan**: Pilih kutipan Sabda yang padat, ringkas, dan langsung menyentuh esensi tema (tidak bertele-tele / jangan terlalu panjang), sehingga sangat *relate* dengan dinamika batin pembaca atau fenomena sosial/viral yang sedang dibedah. Pustaka digital dapat diakses via `https://satyaaditech.github.io/perpustakaan/book/pangestu/<slug>.html`.
*   **Penyalinan ke Vault Obsidian (exFAT)**: Hindari `shutil.copy2()` karena memicu EPERM pada exFAT; gunakan `shutil.copyfile()` atau I/O langsung. Lihat `references/google-docs-and-tts-workflow.md`.
*   **Web Library & GitHub Pages (`kontemplasi.satyaaditech.web.id`)**: Setiap selesai menerbitkan/memperbarui renungan baru di `~/share/renungan/`, WAJIB menyalin berkas ke `/home/satyaaditech/kontemplasi/renungan/` dan menjalankan script sinkronisasi ke GitHub: `/home/satyaaditech/kontemplasi/sync_to_github.sh` agar otomatis terindeks dan live di `https://kontemplasi.satyaaditech.web.id/`.
*   **Master Google Sheet Produksi (V8 Lean 22-Kolom)**: `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0` (https://docs.google.com/spreadsheets/d/1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0/edit).
    - Tab Resmi: `Master Produksi V8` (22 kolom: A s.d. V).
    - Status Produksi Baku:
      * Col 15 (O): `Menunggu ACC Manual Pak Satya` (Draf) -> `ACC` (Disetujui Pak Satya)
      * Col 16 (P): `Render` (Audio TTS) — DILARANG "Selesai Render"
      * Col 17 (Q): `Rendered` (Video MP4) — DILARANG "Selesai Render"
      * Col 18 (R): `Uploaded` (YouTube) — DILARANG "Uploaded (Public)"
      * Col 19 (S): Link YouTube -> Tulis langsung URL mentah lengkap: `https://youtu.be/[video_id]` (DILARANG menggunakan formula `=HYPERLINK`)
      * Col 20 (T): Link Web Pustaka -> Tulis langsung URL mentah lengkap: `https://kontemplasi.satyaaditech.web.id/#[slug]` (DILARANG menggunakan formula `=HYPERLINK`)
      * Col 21 (U): Link Google Docs -> Tulis langsung URL mentah lengkap: `https://docs.google.com/document/d/[doc_id]/edit` (DILARANG menggunakan formula `=HYPERLINK`)
      * Col 22 (V): `Siap Siar` (sebelum siar) atau `Done` (setelah siar selesai).

*   **Penerbitan Google Docs Resmi (Format Bersih & Rapi)**:
    - Target Folder: `1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U` (Materi Olahrasa, permission *Anyone with link as writer*).
    - Perhitungan Index Karakter: Wajib menggunakan **UTF-16 code units** (`len(text.encode('utf-16-le')) // 2`) agar karakter emoji tidak menggeser formatting.
    - Halaman 1: Tanggal, Kategori `RENUNGAN PENYISWAAN`, Judul Tema, Cover/Poster 9:16 (Center Aligned, width ~320pt) diakhiri dengan *Page Break*.
    - Halaman 2: Salam Karahayon, Naskah 4-Pilar Lean (Kutipan Sabda Jawa indent 24pt + Terjemahan, Pangilon Rasa, Laku Panyiswan 30 Detik, Jangkar Batin & Mutiara Rasa, Doa Penutup Satuhu), diakhiri Tautan Pustaka Digital (YouTube & Web Kontemplasi).

*   **Penerbitan Web Pustaka Kontemplasi (`kontemplasi.satyaaditech.web.id`)**:
    - Salin berkas markdown naskah ke `/home/satyaaditech/kontemplasi/renungan/`.
    - Eksekusi skrip sinkronisasi GitHub Pages: `/home/satyaaditech/kontemplasi/sync_to_github.sh`.
    - Web Library otomatis menampilkan naskah dengan kartu baca, modal reader, dan tautan YouTube.

*   **Format Teks Siar WhatsApp & Telegram (Siap Sebar)**:
    - Header (di bawah Judul Tema): Wajib menyematkan link YouTube (`🎧 *Dengarkan di YouTube*: https://youtu.be/...`).
    - Footer (di bawah Doa Penutup Satuhu): Wajib menyematkan tautan lengkap:
      ```text
      ---
      📖 Tautan Pustaka Digital & Dokumen:
      • 📺 Video YouTube: https://youtu.be/...
      • 📄 Google Doc: https://docs.google.com/document/d/.../edit
      • 🌐 Pustaka Web Kontemplasi: https://kontemplasi.satyaaditech.web.id/#<slug>
      ```

*   **Kanonisitas & Singkatan Serat Utama**: Serat-serat baku utami inggih punika: SSJ (*Sasangka Jati*), SKH (*Sabda Khusus*), BRSR (*Bawa Raos ing Salebeting Raos*), TKL (**Taman Kamulyan Langgeng** — *AJA NGANTI klentu dipun-sebat 'Tutur Kelem'*), WSJ (*Wahyu Sasangka Jati*), UUJM (*Ular-Ular Juru Mengeti*), ASBS (*Arsip Sarjana Budi Santosa*), UKK (*Ulasan Kang Kelana*), CJI (*Candrajiwa Indonesia*), OLHR (*Olah Rasa*).
*   **Pemisahan Sumber Utama vs Referensi Tambahan**: Materi saking seminar, YouTube (umpaminipun kanal *Bowo Raos* / pemaparan narasumber kados ta Ibu Dewi Tristantini ngenani *Novelty Budi Darma*), utawi cathetan diskusi kedah dipun-kategoriaken minangka **referensi tambahan / kontekstualisasi tematik** wonten ing `wiki/referensi_tambahan/` utawi `references/`, boten kenging dipun-campuraken utawi dipun-anggep minangka serat utama (*buku kanonik*).

## ⚠️ Jajaran Kosakata Krama Alus (Vocabulary Safeguards)
Tansah gunakaken tembung Krama Alus ingkang leres nalika guneman kaliyan Pak Satya. Kedah murni Krama Alus/Inggil lan boten pareng dipun-campur kaliyan tetembungan utawi tembung panyambung basa Indonesia. Sampun ngginakaken tembung Ngoko, tembung mixed Indo-Jawa, utawi panyebutan ingkang klentu:
*   *sakdurungipun* / *sadurunge* -> Kedah dipun-serat **sakderengipun** (sebelum/sebelumnya).
*   *menyang* / *menyang dhateng* -> Kedah dipun-serat **dhateng** (ke/kepada).
*   *goleki* / *madosi* -> Kedah dipun-serat **padosi** utawi **dipun-padosi** (mencari/dicari).
*   *mirsani* / *ningali* -> Kagem dhiri piyambak (AI/Sinox) ngginakaken **ningali** (melihat) utawi **midangetaken** (mendengarkan). Kagem dipun-aturaken dhateng Pak Satya ngginakaken **mirsani** (melihat) utawi **mirengaken** (mendengarkan).
*   *pastikan* -> Kedah dipun-pesthikaken / dipun-temtokaken.
*   *boso* -> Kedah dipun-serat **basa**.
*   *kosakata* -> Kedah dipun-serat **tembung** utawi **tetembungan**.
*   *kecampur* / *campur* -> Kedah dipun-serat **dipun-campur**.

Tujuan: renungan harian ala Daily Bread versi Pangestu → TG thread 1096.
Sumber: 7 buku Pangestu IND (Sasangka Jati, Sabda Khusus, Ulasan Kang Kelana, dll).
Catatan studi: `/home/satyaaditech/share/pangestu_studi/buku1..7_*.md`.
Quick-ref lokasi sumber per tema: `references/sumber-quickref.md` — pakai saat audit untuk cek baris spesifik.
Catatan khusus tema Panembah vs Serat Panembah: references/sumber-panembah.md — berisi esensi, perbandingan naskah Jawa/Indo, dan rincian khotbah/doa.
Panduan penyusunan Materi Khotbah/Ulasan & Google Drive integration: references/materi-khotbah.md
Panduan unggah Google Drive & konversi Google Doc: references/google-drive-upload.md
Panduan Audio TTS & Integrasi Telegram: references/audio-tts-telegram.md
Panduan Format Renungan Basa Jawi Krama: references/krama-renungan-format.md
Relevansi Tema Ekonomi Nyata: references/relevansi-tema-ekonomi.md — panduan agar tema kecemasan ekonomi membumi dan tidak abstrak.
Panduan Buletin Bulanan "Olahrasa": references/buletin-olohrasa-format.md — panduan penyusunan ulasan & 20 halaman rubrikasi buletin.
OmniRoute Quota Tracking: references/omniroute-quota-tracking.md — cara ngawasi kuota lan pangginaan model ing OmniRoute.
Panduan Infografis & Cover Pilihan: references/infografis-cover-pilihan.md — panduan ndamel infografis programmatik (Pillow), generatif (AI), saha hibrida.
Desain & Rendering Newsletter Kreatif (HTML/CSS + Puppeteer): references/newsletter-html-rendering.md
Integrasi LLM Wiki kagem Buku Pangestu (Cathetan Konsep lan Renungan Harian): references/llm-wiki-integration.md
Arsitektur LLM Wiki Buku Pangestu: references/llm-wiki-architecture.md — panduan struktur folder, alur ingest, dan relasi wiki.
Setup & Struktur Basis Kawruh Wiki Buku Pangestu: references/buku-pangestu-wiki.md
Panduan Rendering & Tata Letak Halaman (PDF Cetak A4 / HP Carousel): references/newsletter-rendering-pitfalls.md — panduan penanganan pembagian halaman, penataan border, dan perbaikan bug emoji Puppeteer. — petunjuk rendering otomatis e-card/newsletter digital visual "selevel Canva".
GOLD STANDARD Renungan Pagi: references/gold-standard-renungan-pagi.md — DISETUJUI Pak Satya 17-08-2026 (renungan Kamardikan Sejati). Semua renungan pagi WAJIB mengikuti struktur & gaya file ini.
Refleksi Tematik (Tuntunan, Metapor lawa/rembulan, & Nderek Paduka): references/contoh-rembulan-sejati.md — memadukan ajaran Pangestu dengan psikologi populer/mindfulness sacara laras
Otomatisasi Publikasi Renungan (Google Drive + TTS + Telegram): scripts/publish_renungan.py — naskah & audio renungan harian langsung dipublikasikan.
Studi & Pemetaan (NPD vs. Ajaran SGS): references/sains-npd-vs-sgs.md — menguraikan korelasi klinis narsisisme (NPD) dengan watak kumingsun batin. sarta panafsiran metapor kelelawar ingkang leres.
Scripts pembantu pembuatan gambar cover: `scripts/render_cover.py` — script Python Pillow kagem dandan e-card cover (latar padhang/terang, mawi font warna kontras biru/ireng areng, sarta mbusak tembung "Pangestu").
Provider & model: `references/provider-opencode-deepseek.md` — setup dan cara pakai DeepSeek V4 Pro via OpenCode Go.

## 🔴 PITFALL #1: SABDA SPLICING (baca sebelum nulis!)

JANGAN menyambung fragmen dari beberapa paragraf sumber dengan `...` jadi satu quote panjang. Ini cherry-picking yang mendistorsi

## 🔴 PITFALL #2: RAW WIKILINKS & METADATA IN USER OUTPUTS

*   **Google Doc (HTML)**: Pastikan YAML frontmatter dan tanda kurung siku ganda `[[ ]]` dihilangkan sepenuhnya saat konversi HTML. Google Doc harus tampil bersih untuk dibaca langsung pemilik.
*   **Alur Cepat Tanpa Audio & E-Card**: Jika workflow hanya membutuhkan penerbitan teks Indonesia di Google Doc dan lokal, gunakan skrip `publish_renungan_simple.py`. Hindari pembuatan berkas audio (TTS) dan gambar penutup (cover e-card) kecuali diminta secara khusus oleh pemilik.
*   **Batasan Emotikon & Penggunaan Tanda Seru**: Batasi jumlah emotikon dalam teks renungan harian antara 8 hingga 14 emotikon universal secara total. Hindari penggunaan tanda seru (!) dalam teks renungan guna menjaga stabilitas batin.
*   **Share/Telegram Output**: Pastikan output teks yang disalin ke chat maupun file di direktori `share/` bersih dari markdown `[[ ]]` wikilinks. Gunakan konversi/regex (misal: `[[Concept|alias]]` -> "alias", `[[Concept]]` -> "Concept").
*   **Wiki Vault (Obsidian)**: Tahan format wikilinks hanya untuk berkas yang disimpan di dalam direktori `wiki/renungan/` untuk menjaga database relasi Obsidian tetap terhubung. struktur asli meskipun setiap kata nyata adanya. Setiap Sabda HARUS verbatim dari SATU paragraf utuh di sumber.

## 🔴 PITFALL #2: METADATA LEAKAGE & RAW WIKILINKS (Wajib Bersih!)

1. **Google Doc & Output WA/TG Tanpa Metadata**: Google Doc serta teks salinan di Telegram/WA tidak boleh memuat YAML frontmatter (metadata seperti `title:`, `date:`, `tags:`, `language:`). Teks di Doc dan salinan WA/TG harus langsung dimulai dari header tanggal (misalnya `*KAMIS, 27 AGUSTUS 2026*`).
2. **Hilangkan Kurung Wikilink `[[ | ]]`**: Untuk teks salinan Telegram/WA dan tampilan Google Doc, hilangkan semua braket double `[[` dan `]]` (format `[[Concept|alias]] -> alias` and `[[Concept]] -> Concept`). Kurung siku pranala wiki hanya boleh ada di file Obsidian `.md` di dalam folder `wiki/renungan/` untuk kebutuhan basis pengetahuan.

## 🔴 PITFALL #3: GAYA FLAT, ROBOTIK, DAN PENCAMPURAN BAHASA

1. **Gaya Bahasa Humanis dan Kreatif**: Hindari penjelasan yang terlampau teoritis dan kaku. Gunakan metafora yang hidup, emosional, dan membumi langsung dari isi kitab (contohnya perumpamaan beban 100 kg tampak ringan dan minuman pahit yang tak terasa pahit di lidah dari BRSR VII).
2. **Bahasa Indonesia yang Utuh**: Jika diminta menulis versi Bahasa Indonesia, pastikan bagian Uraian, Praktik, dan Pertanyaan menggunakan Bahasa Indonesia yang mengalir, alami, dan bebas dari sisipan istilah Jawa Krama di tengah kalimat secara acak (kecuali istilah ajaran resmi seperti *mituhu*, *eling*, *rila*, atau *Sang Guru Sejati*).

❌ Contoh salah: `"Sabar — sebaik-baiknya watak... Bukan putus asa... Jangan picik: merdekakanlah pikiranmu... Sabar ibarat jamu pahit..."` (4 fragmen dari baris 53, 54, 55, 56 disambung jadi satu)

✅ Contoh benar: `"Sabar ibarat jamu pahit — menyembuhkan kesusahan; sabar itu bukan niat yang hanya berhenti pada pengharapan... tetapi bertindak sesuai dengan kemampuan secara teratur dan teliti."` (SATU paragraf utuh dari baris 56)

Jika satu paragraf tidak cukup untuk membangun Uraian, pakai quote pendukung dari buku lain di tengah Uraian — jangan menyambung di Sabda.

---

## 🔴 PITFALL #2: BAHASA — TERLALU PUITIS ATAU TERLALU GENERIK (Writer)

Dua kesalahan yang sama-sama ditolak user:

**❌ Kesalahan A: Bahasa puitis/tasawuf berat.** 
User feedback: "bahasa yang digunakannya pun juga bukan yang mudah dipahami orang setiap hari. saya inginnya sekalipun memiliki makna yang dalam dan relate dengan kehidupan kita sehari-hari gunakan bahasa yang sederhana nyaman untuk dibaca."

Contoh ditolak: "mati dari pengharapan", "menyeberangi lautan pamrih", "pedang melawan pamrih", "jiwa merdeka dari mengharap balasan", "di sanalah sabar menempa jiwa menjadi lautan"

❌ JANGAN pakai diksi puitis, tasawuf, atau sastrawi.

**❌ Kesalahan B: Bahasa generik/informatif tanpa rasa.**
User feedback: "terlalu umum generik tidak begitu mengena di hati."

**✅ YANG DITERIMA:** Bahasa Indonesia SEHARI-HARI — sederhana, hangat, mengalir seperti obrolan. Bisa dipahami tukang bakso, guru SD, ibu rumah tangga. Makna dalam DISAMPAIKAN dengan kata-kata ringan.

Contoh diterima: "Anak sudah dua minggu tidak menelepon. Ditunggu-tunggu, hape dicek terus... lalu ingat: sabar bukan berarti diam, tapi menerima dan tetap membuka pintu." — relatable, nyata, tidak menggurui.

**PRINSIP**: bahasa obrolan warung kopi, bukan bahasa mimbar atau bahasa puisi. Contoh nyata > metafora abstrak. "Nggak enak, tapi menyembuhkan" > "jamu pahit yang hanya bisa diteguk jiwa-jiwa teguh".

**SOLUSI**: Writer harus menulis dengan bahasa Indonesia SEHARI-HARI — sederhana, hangat, mengalir seperti obrolan. Bisa dipahami tukang bakso, guru SD, ibu rumah tangga. Makna dalam DISAMPAIKAN dengan kata-kata ringan. Metafora dari kitab (lautan, jamu pahit, petani & padi) boleh dipakai tapi TETAP dijelaskan dengan bahasa sehari-hari, bukan puisi. Target: pembaca merasa "ini bicara tentang diri saya" dan langsung bisa dipraktikkan hari ini.

**Diksi**: "berlapang dada", "menunggu dengan tenang", "tidak membalas dengan marah", "menerima kenyataan" — bukan "sabar itu penting" tapi juga bukan "menyeberangi lautan pamrih". Konkret, praktis, bisa langsung dilakukan.

---

## 🔴 PITFALL #3: ATRIBUSI KOLEKTIF (Writer + Editor)

Ketika ajaran menyebut beberapa unsur bekerja BERSAMA, jangan atribusikan ke satu unsur saja.

❌ Contoh salah: "sabarlah yang memutus tali pamrih" — padahal Jalan Rahayu baris 117 jelas: keempat watak (rela, narima, jujur, sabar) BERSAMA-SAMA yang memutuskan tali pamrih.

✅ Contoh benar: "keempat watak inilah — rela, narima, jujur, sabar — yang bersama-sama memutus tali pamrih."

---

## 🔴 PITFALL #4: TARGET PEMBACA & GAYA ILUSTRASI (Universal & Relatable)

* **Sasaran Universal**: Renungan ditujukan untuk seluruh siswa dan masyarakat luas secara universal — **HINDARI dikotomi usia, stereotip pensiunan, atau pengotakan usia**.
* **Ilustrasi Nyata & Wajar**: Gunakan contoh dinamika batin sehari-hari (interaksi keluarga, lingkungan kerja, relasi sosial, ruang digital/media sosial) yang wajar dan membumi.
* **Hindari Ilustrasi Ekstrem**: Jangan menggunakan contoh kasus ekstrem/tragis (kriminalitas berat, penyakit terminal, kekerasan) guna menjaga kestabilan batin pembaca.
* **Bahasa Human Creative**: Bahasa sederhana, hangat, mengalir seperti obrolan sehari-hari, bukan bahasa mimbar yang menggurui.

---

## 🔴 PITFALL #5: FOOTER & 3 TAUTAN DIGITAL WAJIB (Format WA Code Block)

Setiap naskah final WhatsApp (Langkah 5 & 6) WAJIB memuat 3 tautan digital lengkap di bagian footer:
1. `• 📺 Video YouTube : https://youtu.be/...`
2. `• 📄 Versi Google Doc : https://docs.google.com/document/d/...`
3. `• 🌐 Pustaka Web Kontemplasi : https://kontemplasi.satyaaditech.web.id/#<slug>`

❌ **DILARANG MUNCUL**:
- `\"📖 Waos naskah jangkep wonten ing Pustaka Kontemplasi: ...\"` (Dihapus total).
- `\"✅ Dapat dipraktikkan di mana saja dan kapan saja...\"` (Dihapus total).
- Footer tanpa link web kontemplasi atau link yang hilang salah satu.

---

## 🔴 PITFALL #6: STANDAR GOOGLE DOC (Paginasi 2 Halaman Rapi)

1. **Halaman 1 (Cover)**: Header tanggal, `RENUNGAN PENYISWAAN`, Judul Utama, dan **Poster Infografis proporsional (lebar 320pt / 70-75%)** dipusatkan (center), diakhiri **Page Break**.
2. **Halaman 2 (Isi)**: Salam Karahayon, Pethikan Sabda/Wejangan (indent 24pt italic), Uraian, Praktik (3 poin), Renungan, Aplikasi (3 pertanyaan), Penutup Satuhu, dan Footer 3 tautan aktif.
3. Teks di Google Doc bersih tanpa karakter markdown mentah (`*`, `**`, `###`).

---

User feedback: "enggak ada emotikon nya aturan di mana setiap konten dilengkapi dengan emotikon yang menarik itu enggak ada semua gitu"

- ✅ SETIAP section HARUS ada emotikon — Uraian, Praktik, Renungan, Aplikasi
- ✅ Target: minimal 8-10 emotikon di seluruh renungan
- ✅ Emotikon harus relevan dengan konten (bukan random)
- ❌ Section tanpa emoji = REJECT

---

## 🔴 PITFALL #6: REFLEKSI SAJA, TANPA MOTIVASI (Writer)

Renungan tidak boleh hanya "melihat ke dalam" lalu selesai. Harus ada DORONGAN untuk bertindak — optimis, membangun, "ayo kita bisa."

❌ Contoh refleksi saja (ditolak): "Begitulah kita, sering tidak sabar. Mari kita renungkan." — pasif, tidak menggerakkan.

✅ Contoh reflektif + memotivasi (diterima): "Sabar bukan kelemahan — justru di situlah kekuatan kita sebagai orang yang sudah makan asam garam kehidupan. Hari ini, mari kita buktikan."

**PRINSIP**: Setiap renungan = cermin + kompas. Cermin untuk melihat diri, kompas untuk melangkah lebih baik. Tutup selalu dengan nada harapan dan keyakinan bahwa perubahan itu mungkin — hari ini juga.

---

## 🔴 PITFALL #7: DUAL-MAKNA ISTILAH — JANGAN MENJUDGE NEGATIF (Writer)

Beberapa istilah Jawa/Pangestu punya DUA makna — satu luhur, satu rendah. Jangan kaprah menulis makna negatif saja. Kasus nyata (feedback user 12 Ags 2026):

- **Pasrah** ❌ Salah: "pasrah itu buruk, menyerah, diam" — user: *"pasrah itu ada 2 arti: positif (kesadaran bahwa semua dalam kekuasaan Tuhan, kondisi jiwa yang sadar betul) dan negatif (paralysis, tidak mau berbuat apa-apa). Arti positifnya baik dan malah sering digunakan dalam terminologi baik."*
- ✅ Benar: pasrah sejati = kesadaran jiwa matang; **ikhtiar dulu, lalu menyerah dengan rela kepada Hukum Keadilan Tuhan** (Sabda Khusus baris 1419: *"setelah menjalankan ikhtiar dan syarat-syarat yang engkau anggap berguna, dalam rasa hatimu menyerahlah dengan rela kepada Hukum Keadilan Tuhan"*). Pasrah negatif = menyerah SEBELUM berusaha (paralysis). Kunci pembeda: **URUTAN** — ikhtiar mendahului pasrah.
- Pasrah sejati & sabar = satu rumpun (sabar = keteguhan sambil berikhtiar), BUKAN lawan.

Istilah rawan lain yang harus dicek makna positifnya di kitab dulu: narima, ikhlas, tawakal, nrimo ing pandum.

## 🔴 PITFALL #8: JANGAN ULANG METAFORA LAMA + DEEP ≠ DAFTAR CONTOH (Writer)

Feedback user 12 Ags 2026: *"flow bacanya kurang enak, materi sedikit redundant dengan sebelumnya, kurang deep — inginnya deep, aplikatif tapi bahasa tetap mudah dimengerti."*

- ✅ Sebelum menulis, CEK renungan terdahulu di `~/share/renungan/renungan-*.md` (Sabar v5 = jamu pahit, Sabar v6 = lautan, Rela v1 = kosong dari pamrih/tangan kosong, Rela v2 = mengabdi tanpa lekat/bukan lari ke gunung). JANGAN pakai metafora atau sudut pandang yang sudah dipakai.
- ✅ "Deep" ≠ mendaftar banyak contoh kehidupan (anak, tensi, cabe, arisan...). Deep = masuk ke PERGULATAN BATIN: bedakan dua konsep yang mirip (pasrah vs menyerah; sabar vs menunggu), apa kunci pemahamannya, apa rasanya di dada. Satu gagasan besar diurai, bukan tiga contoh diparalelkan.
- ✅ Flow enak = tiap paragraf menyambung ke satu alur pemikiran, bukan paragraf-contoh yang berdiri sendiri.
- ✅ **TOPIK SAMA DIMINTA ULANG** (mis. user minta "Sabar" lagi, atau "Rela" lagi): WAJIB sudut pandang, Sabda/kutipan, metafora, DAN contoh SEMUANYA berbeda dari versi sebelumnya. Satu topik bisa dilihat dari banyak perspektif — cari Sabda di baris/buku lain, angkat pergulatan batin yang belum tersentuh. Selalu hadirkan tulisan fresh. Langkah wajib: `grep` daftar `~/share/renungan/renungan-*.md` dulu, catat semua sudut + Sabda + metafora yang sudah dipakai, lalu cari yang BELUM dipakai.

## 🔴 PITFALL #9: REPLACE GLOBAL & GLIF EMOJI DEGRADASI (Headless Render)

- **Replace Global / replaceAll**: Nalika ngganti placeholder wonten ing template Node.js/Python (kados `{DATE_STR}`), ngginakaken regex global `/{DATE_STR}/g` utawi `replaceAll()`. Menawi ngginakaken `.replace()` biasa, namung kemunculan kapisan ingkang kegantos.
- **Emoji Degradasi dhateng OS Headless**: Emoji unicode (kados `🧘`, `🎯`, `📝`) asring dipun-render dados kothak dokumen `🗎` utawi glif risak wonten ing headless browser amargi server Linux mboten nggadhahi font emoji. Gantos emoji kasebat mawi **Ikon Vektor SVG Inline** supados cetha lan premium.
- **Tinggi Konten A4 PDF & Carousel Spacing**: Kertas A4 nggadhahi inggil kaku (`297mm`). Menawi teks naskah kebeken, bodi badhe kagiles (`overflow: hidden`). Pecah bodi HTML dados 3 halaman proporsional kanthi wates margin aman (15mm) lan padding bottom (80px).

---

## 🏆 STANDAR EMAS — ANTI-REGRESI

**Writer WAJIB baca GOLDEN_SAMPLE_v7.md sebelum mulai menulis.** Editor WAJIB audit hasil Writer terhadap sample ini.

### Checklist Anti-Regresi (Writer centang sebelum kirim ke Editor)

- [ ] Sabda = SATU paragraf utuh verbatim? (bukan sambungan fragmen `...`)
- [ ] Contoh spesifik dan universal? (proyek ditolak, rencana batal, barang kesayangan, kecemasan masa depan, keluarga)
- [ ] Bahasa obrolan warung kopi? (buka: "Siapa yang belum pernah...?")
- [ ] Minimal 8 emotikon tersebar di SEMUA section?
- [ ] TIDAK ada kata "kamu" di mana pun?
- [ ] TIDAK ada tanda seru (!) di seluruh naskah renungan?
- [ ] Section urut: Uraian→Praktik→Renungan→Aplikasi?
- [ ] Praktik = langkah konkret spesifik? (bukan "perbanyak sabar")
- [ ] Renungan = SATU kalimat tajam membekas? (bukan paragraf quote)
- [ ] Renungan memotivasi? (ada nada "ayo bisa", optimis, bukan hanya "inilah masalah kita")
- [ ] Aplikasi = pertanyaan reflektif menusuk pengalaman? (bukan perintah)
- [ ] Closing PERSIS template? ("Semoga kita semua... Satuhu")

### Kalau hasil Writer GAGAL checklist → Editor TOLAK tanpa revisi. Dispatch ulang Writer.

---

## Preferensi & Aturan Pengiriman (WAJIB)

- **Workflow default**: FORWARD (single-pass Researcher→Writer→Editor). JANGAN pakai iterasi (multi-ronde Writer→Editor→Writer) kecuali user eksplisit minta.
- **MODEL WAJIB**: Writer + Editor HARUS pakai `deepseek-v4-pro` via OpenCode Go. Setup: `delegation.base_url` + `delegation.api_key` (literal string, bukan env var) + `delegation.model` — lihat `references/provider-opencode-deepseek.md`. Cek saldo dulu sebelum dispatch — kalau habis, tulis langsung tanpa delegasi.
- **Panjang**: total ±350–450 kata (bisa dibaca ±3 menit). Jangan terlalu panjang. ⚠️ KALIBRASI: golden sample yang DISETUJUI user = 493 (v5), 620 (v6) & 490 (v7) kata — jangan pangkas habis-habisan cuma karena klaim Editor "batas keras 450". Rentang aman ±490–620.
- **Kirim**: forward SEKALI SAJA ke thread 1096. Jangan kirim berkali-kali.
- **Format final**: selalu code block dengan markup WA (`*bold*`, `_italic_`). Jangan kirim teks langsung — Telegram parse `*` tidak konsisten.
- **Template baku**: lihat `templates/format-baku.md` — struktur SABDA→URAIAN→PRAKTIK→RENUNGAN→APLIKASI. Urutan dan nama section WAJIB persis.
- **Salam**: "_Salam Karahayon 🙏_" (tanpa tanda seru `!`)
- **Closing**: "🙏 Semoga kita semua senantiasa berlimpah dengan Tuntunan dan Perlindungan, Sih dari Sang Guru Sejati. Satuhu 🙏" — PERSIS, jangan diparafrase
- **Ulasan / Khotbah / Kesiswaan**: Ketika mengulas bab atau menyusun kerangka khotbah (terutama terkait tema *Panembah*), tonjolkan relasi **Siswa (Roh Suci)** dengan **Guru Sejati (Suksma Sejati)**, luruhkan kehendak ego (*karep*) menjadi Kehendak Suci (*Karsa*), dan lakukan cross-reference lintas buku (Sasangka Jati, Sabda Khusus Peringatan 2 & 8, ASBS, dan Ulasan Kang Kelana Bab XIV).
- **Batasan Bahasa Naskah Mutlak (STRICT LANGUAGE BOUNDARY)**:
  * **HANYA** bagian `[Kutipan Sabda Jawa]` yang ditulis dalam Bahasa Jawa (100% teks Jawa kanonikal verbatim).
  * **SELURUH** uraian pembahasan lainnya (Terjemahan Sabda, `Pangilon Rasa` Paragraf 1 & 2, `Laku Panyiswan`, `Jangkar Batin` / Mutiara Rasa, Doa Penutup Satuhu, Deskripsi YouTube, Google Docs, dan Web Kontemplasi) **WAJIB 100% MENGGUNAKAN BAHASA INDONESIA** yang komunikatif, jernih, dan hangat.
  * **PANTANGAN KERAS**: DILARANG KERAS menulis satu paragraf pembahasan utuh dalam Bahasa Jawa! Istilah filosofi/spiritual Jawa (seperti *eling, angen-angen, heneng-hening, catur nepsu, pamasrahan*, dll.) boleh diselipkan sewajarnya sebagai kata konsep, tetapi struktur kalimat pengantarnya tetap Bahasa Indonesia utuh.
  * **Alasan Vokal & Publik**: Narasi renungan disuarakan oleh AI TTS `id-ID-ArdiNeural` (Indonesian Voice Model). Kalimat Jawa dalam narasi akan merusak artikulasi vokal dan terdengar aneh bagi pendengar/pembaca umum.
- **Persona Chat**: Gunakan terus Basa Jawi Krama (bahasa Jawa alus) yang santun dalam menanggapi pesan obrolan sehari-hari dengan Pak Satya (sebagai bentuk unggah-ungguh), namun DILARANG MEMBIARKAN Basa Jawi Krama merembes masuk ke dalam teks naskah renungan publik.
- **Audio/Voice Bubble**: Jika pengguna menghendaki/menyepakati versi audio renungan harian, generate berkas audio (`.mp3` atau `.ogg`) menggunakan `text_to_speech_ide`. Teks input pembacaan harus dibersihkan terlebih dahulu dari simbol format WhatsApp (`*` sarta `_`) agar pengucapannya alami. Simpan hasil audio ke folder share server `/home/satyaaditech/share/renungan/renungan-<tema>-<tanggal>.mp3` agar bisa diakses lewat browser (LAN/Tailscale), dan kirimkan mawi tag MEDIA agar terunggah sebagai pesan suara bergelembung di Telegram.
- **Emotikon**: WAJIB di setiap section. Minimal 8-10 emotikon menarik di seluruh renungan. Tanpa emoji = reject.
- **Target**: pembaca universal (semua usia, hindari dikotomi pensiun/50+). Contoh harus nyata dari kehidupan sehari-hari.
- **Contoh**: NYATA dari kehidupan sehari-hari orang Indonesia (pekerjaan kantoran, barang kesayangan, kecemasan, gawai, masa depan). JANGAN metafora abstrak, kisah tokoh dunia, atau ilustrasi ekstrem (seperti meninggalkan keluarga/menjauh dari dunia wadak).
- **LARANGAN**: JANGAN pakai kata "kamu" di mana pun — gunakan "kita", "Bapak, Ibu", atau bentuk pasif; serta JANGAN pernah menggunakan tanda seru (!) di bagian mana pun dalam naskah renungan (gunakan tanda titik atau tanda tanya sesuai intonasi).
- **Gambar Cover (E-Card)**: Gunakan gambar sampul berformat persegi (1200x1200px). Latar belakang wajib **terang/padhang** (krem hangat/putih gading) dan font harus **kontras tinggi** menggunakan warna-warna tua (seperti biru tua, merah tua, atau hitam). Hapus/tiadakan kata "Pangestu" dari header sampul (menyisakan "RENUNGAN PENYISWAAN"). Script pembuat cover berada di `scripts/render_cover.py`.
- **Ekspor Audio TTS**: Kategori pemaos renungan Indonesia wajib menggunakan model suara aksen Indonesia asli (`id-ID-GadisNeural` di Edge TTS). Setel secara permanen mawi CLI: `hermes config set tts.edge.voice id-ID-GadisNeural`.
- **Integrasi WhatsApp**: Kirim audio mawi jenis (*message type*) `audio` (bukan `document`) supados saged dipun-puter sacara *real-time* (voice note format mawi waveform) wonten ing obrolan WhatsApp.
- **LARANGAN**: JANGAN pakai kata "kamu" di mana pun — gunakan "kita" or bentuk pasif.
- **Sabda**: SATU paragraf utuh dari sumber, verbatim. Format: "Nama Kitab : _\"quote\"_". JANGAN "— Sang Guru Sejati, Nama Kitab".
- **Format final**: selalu code block dengan markup WA (`*bold*`, `_italic_`). Jangan kirim teks langsung — Telegram parse `*` tidak konsisten.
- **Panyaringan Emoji & Setup Audio (TTS)**: Sadurunge teks renungan di-TTS, resiki sedaya emoji saking teks batin kersanipun narator mboten maos nama latin emoji. Gunakaken swanten Basa Indonesia `id-ID-GadisNeural` (estri alus) kagem edisi Indonesia, sarta `jv-ID-DimasNeural` (jaler medok wibawa) utawa `jv-ID-SitiNeural` (estri alus) kagem edisi Jawi. Konversi berkas `.mp3` dados `.ogg` format Opus mrihari gelombang *voice note* mawi `ffmpeg -c:a libopus`.
- **Desain Cover Monokrom Jawi**: Latar terang (krem gading), bingkai sarta seratan warna **Hitam Pekat** (no gold/kuning), pigura pojok mawi ornamen **kelopak bunga Kawung Jawi** ingkang medhot manis kaliyan garis pinggir. Header murni `"RENUNGAN PENYISWAAN"` (tanpa tembung "Pangestu"), sarta font size judhul dipun-set **raksasa (size 62)** supados cetha katitik saking *tamel (thumbnail)*.
- **Pangiriman Berkas Fisik (Telegram Bot API)**: Ngirim berkas audio (`.ogg` & `.mp3`) langsung minangka lampiran fisik (attach file) lumantar Telegram Bot API ngginakaken curl (token dipundhut saking `~/.hermes/.env`), boten namung paring teks `MEDIA:/path` utawi pranala. Chat ID: `-1003256146835`, thread: `1096`.
- **Topik Ganda ing Dina Sami**: Manawi nggarap topic utawa tema ingkang sami ing dinten kasebut, wenehana tandha versi `(v1)`, `(v2)`, `(v3)` ing sawingkingipun judhul, lan sastra kontene (sudut, sabda, lan conto) wajib beda wetah (unik).
- **Visual E-Card (Cover)**: Latar belakang wajib terang (krem/ivory gradasi lembut), teks kontras tinggi (biru tua, hitam arang), hindari warna emas/kuning. Bingkai tepi menggunakan ornamen motif Jawi minimalis (seperti kelopak Kawung ing 4 pojok), header murni "RENUNGAN PENYISWAAN" (tanpa kata "Pangestu"), sarta ukuran font judul raksasa (size 62) agar terbaca langsung saking njawi (tampilan thumbnail).
- **Pengolahan Audio (TTS)**: Suara wajib aksen Basa Indonesia ingkang alus (`id-ID-GadisNeural`). Sebelum dikirim dhumateng mesin TTS, resiki sedaya emoji saking teks ing memori/script kagem saringan (supados narator mboten maos nama latin emoji), ananging sampun ngrusak emoji ing file teks aslinya (.md). Jalur pangirimanipun wajib ngintun berkas fisik secara langsung dhumateng obrolan chat ngginakaken Telegram Bot API (sendVoice/sendAudio), sampun namung maringi teks tag media utawi tautan kemawon.

## Dua Workflow Input

### 1. User Kasih TEMA → Kita Cari Quote
User: "Bikin renungan tema Sabar."
Proses: `search_files` di `/tmp/` cari quote dari buku Pangestu mana pun (Sasangka Jati, UKK, Olahrasa, Riwayat Hidup Pakde Narto, dll) → kembangkan renungan.

### 2. User Kasih QUOTE → Kita Pelajari Intinya + Cari Sabda Selaras
User memberikan kutipan dari buku Pangestu (bisa dari Sasangka Jati, Riwayat Hidup Pakde Narto, UKK, dll).
Proses:
- Pelajari inti cerita/kutipan — apa pesan utamanya?
- Jika quote user adalah Sabda dari buku tertentu, gunakan langsung sebagai **📖 SABDA HARI INI**.
- Jika quote user adalah kisah historis (bukan Sabda), cari Sabda dari buku Pangestu mana pun yang selaras dengan inti cerita.
- Quote/kisah user menjadi **inspirasi uraian** (kisah nyata wajib).
- Kembangkan dengan pola: Sabda (Sasangka Jati) + Uraian (kisah user + konteks kekinian) + Praktik + Renungan + Aplikasi.
- Sabda dari buku Pangestu mana pun (Sasangka Jati, UKK, Olahrasa, Riwayat Hidup Pakde Narto, dll) — KECUALI user minta spesifik sumber tertentu, ikuti permintaan user.

Keduanya output akhir: code block WhatsApp-compatible, ikuti template baku.
Template lengkap: `references/template-renungan.md`.

## Aturan Sabda (CRITICAL)

1. **VERBATIM dari SATU paragraf utuh.** Jangan menyambung fragmen dari paragraf/baris berbeda dengan "...". Ini cherry-picking — mendistorsi struktur asli meskipun setiap kata nyata. Jika perlu quote dari dua baris berbeda, gunakan pemisah eksplisit "[...]" dan pastikan tidak melewati isi penting di antaranya. Lebih baik: kutip HANYA SATU baris utuh dan letakkan quote pendukung dari buku lain di uraian.
2. **Sumber jelas.** Cantumkan buku sumber, nomor baris/halaman.
3. **Spesifik ke tema.** Sabda harus tentang tema, bukan sekadar menyebut tema dalam daftar (contoh: untuk tema Narima, Sabda harus tentang Narima spesifik, bukan "Panca Sila: sabar, narima, jujur...").

## RONDE Revisi

Setelah user menerima draft, Editor/User bisa meminta revisi. Proses revisi mengikuti pola: kesalahan WAJIB (harus diperbaiki) + insight OPTIONAL (pertimbangan kualitas). Detail di `references/ronde-revision.md`.

## Workflow Agentic (Tim Redaksi 3 Personel)

Untuk hasil maksimal, jalankan alur agentic dengan 3 subagent + 1 orchestrator. Prompt spesialis tiap role disimpan di `references/prompt-*.md`. Cara membaca output delegasi yang terpotong (`subagent-summary-0-*.txt`, live transcript, manifest) ada di `references/delegation-output-retrieval.md`.

### Alur Orchestrator

```
USER beri tema
    │
    ▼
[RESEARCHER] delegate_task → cari 2 Sabda dari 7 kitab
    │ output: Sabda utama + Sabda pendukung + alasan
    ▼
[WRITER] delegate_task → tulis draft renungan (diberi Sabda Researcher)
    │ output: draft code block lengkap
    ▼
[EDITOR] delegate_task → audit draft Writer (diberi draft Writer)
    │ output: laporan audit (✅ ❌ 💡)
    ▼
[ORCHESTRATOR] terapkan revisi Editor → FINAL → kirim ke user
```

**Waktu total: ±60-90 detik.** Orchestrator hanya menerapkan revisi — tidak menulis ulang dari nol.

### Personel & Skill Set

#### 1. Researcher — Pencari Sabda
- **Prompt**: `references/prompt-researcher.md`
- **Tool**: `search_files` (grep kitab Pangestu), `read_file` (konteks)
- **Pengetahuan**: hafal isi 7 kitab, tahu istilah kunci per buku
- **Output**: 1 Sabda utama + 1 Sabda pendukung + nomor baris + buku sumber + alasan cocok dengan tema
- **Kriteria**: Sabda harus spesifik ke tema (bukan generik), lebih baik pendek-tajam daripada panjang-lebar

#### 2. Writer — Penulis Renungan
- **Prompt**: `references/prompt-writer.md`
- **Persona**: praktisi kejiwaan berpengalaman, banyak insight, paham psikologi awam
- **Kedalaman Bahasa**: WAJIB deep dan terasa di hati — bukan sekadar informatif. Hindari contoh generik/klise (macet, penjual gorengan, ibu bangun pagi). Gunakan analogi dari kehidupan batin: konflik melawan ego, momen hening di tengah badai, pergulatan antara keinginan dan kenyataan. Tulis seolah pembaca sedang bercermin pada dirinya sendiri. Nada rendah hati, mengajak, bukan menggurui.
- **Struktur URAIAN**: buka dengan pertanyaan reflektif (bukan skenario klise) → dalami makna Sabda → tutup dengan ajakan kontemplatif sebelum masuk ke LAKU.
- **Input**: tema + Sabda dari Researcher
- **Output**: draft renungan lengkap (code block WhatsApp-ready)
- **Skill inti**: hook relatable, kisah nyata TERVERIFIKASI, analogi konkret, tone akrab-tidak-menggurui

#### 3. Editor — Auditor Daily Bread
- **Prompt**: `references/prompt-editor.md`
- **Persona**: editor senior 10+ tahun — dingin, tajam, tidak sungkan membongkar
- **Input**: draft Writer
- **Output**: laporan audit (✅ yang bagus / ❌ harus diperbaiki / 💡 insight)
- **Cek wajib**: quote nyambung? kisah autentik? praktik bisa dikerjakan? tidak ada "kamu"? fakta terverifikasi?

### Aturan Orchestrator

Setelah ketiga subagent selesai:

1. Baca laporan Editor — prioritas ❌ (harus diperbaiki), lalu 💡 (insight peningkatan)
2. **VERIFIKASI semua klaim ❌ Editor** — JANGAN langsung percaya. Cek ulang ke file sumber di `/tmp/` menggunakan `read_file` atau `search_files`. Editor bisa halusinasi sumber atau klaim "tidak ditemukan" padahal quote ada. Juga bisa halusinasi ATURAN FORMAT: kasus 12 Ags 2026 — Editor klaim quote Sabda wajib `_\"*...*\"_` (bold dalam italic), padahal template baku & golden sample v5/v6 yang disetujui user memakai italic saja `_\"...\"_`. Format klaim Editor SELALU cross-check ke `templates/format-baku.md` + golden sample sebelum diterapkan.
   - **Editor juga bisa halusinasi aturan FORMAT**, bukan cuma fakta. Pernah ia menolak format italic `_\"...\"_` dan memaksa `_\"*...*\"_` (bold dalam italic), padahal template baku & golden sample pakai italic saja. Saat Editor bilang "format harus X", SELALU cek ulang ke `templates/format-baku.md` + `references/GOLDEN_SAMPLE_v7.md` dulu — ikuti template, bukan klaim Editor.
   - **Jangan buta ikut batas panjang Editor.** Skill nyebut ±350-450 kata, TAPI golden sample yang disetujui user justru 493 (v5), 620 (v6), & 490 (v7) kata. Rentang yang diterima kira-kira **490-620 kata**. Hitung ulang sendiri (strip markdown `*_` dulu) dan bandingkan ke golden sample, bukan ke angka 450 dari Editor.
3. Terapkan revisi pada draft Writer — **jangan tulis ulang dari nol**
4. Jika Editor menilai draft harus ditulis ulang total: jalankan ulang Writer dengan catatan Editor
5. Final: code block WhatsApp-ready → kirim ke user
6. Jika user minta revisi tambahan setelah final: editing manual, tidak perlu jalankan ulang seluruh alur

### Pitfall & Pelajaran

#### 🔴 Editor Bisa Halusinasi — VERIFIKASI SELALU

**Kejadian nyata (demo Jujur):** Editor mengklaim 2 ❌:
1. "Sabda dari Hasta Sila, bukan Sasangka Jati" → ❌ SALAH. Sabda ada di `/tmp/ssj_ind.txt` baris 155-158.
2. "Quote pendukung 'Taatlah...' tidak ditemukan" → ❌ SALAH. Quote ada di `/tmp/asbs.txt` baris 780-782.

Editor hanya mencari di `/home/satyaaditech/share/pangestu_studi/` (catatan studi) tapi TIDAK mencari di `/tmp/` (file mentah kitab). **Orchestrator WAJIB verifikasi semua ❌ dengan `read_file` ke `/tmp/` sebelum menerima vonis Editor.**

#### 💡 Kisah Legendaris → Framing "Konon"

Kisah seperti Lincoln "jalan bermil-mil kembalikan receh" bersifat apokrifal — tidak ada sumber primer. Jangan dibuang, tapi JANGAN diframing sebagai fakta keras. Gunakan: _"Konon...", "Dikisahkan...", "Ada cerita dari..."_ — lalu dukung dengan fakta yang benar-benar tercatat (Lincoln tolak klien bersalah → terverifikasi).

### Fallback: Mode Cepat

Jika user minta cepat atau tema sederhana: orchestrator bisa tangani sendiri (Researcher + Writer + Editor dalam satu agent) tanpa delegate_task. Hasil tetap ikuti template baku.ngan lengkap dengan persona praktisi kejiwaan
3. **Editor** — audit draft dengan standar Daily Bread internasional

Prompt template tiap role: `references/agentic-workflow.md`.
Checklist audit Editor: `references/audit-checklist.md`.

Alur: Researcher → Writer → Editor → Orchestrator terapkan revisi → FINAL.

## 🔴 PITFALL #9: Panggilan Script Utilitas (scripts/)
Script `scripts/publish_renungan.py` dan `scripts/render_cover.py` didefinisikan sebagai fungsi python (tanpa antarmuka CLI `if __name__ == "__main__"`). Untuk menjalankannya, buatlah python script pembungkus temporer (misal di `/tmp/run_publish.py`), import fungsinya, lalu panggil secara langsung dengan parameter yang sesuai.

## 🔴 PITFALL #10: PUBLISH FOREGROUND → TIMEOUT → LINK GOOGLE DOC HILANG (WAJIB!!)

Recipe aman lengkap (background invoke + verifikasi link) + tandha kegagalan: `references/publish-safe-runner.md`.

**Kacathet 26-08-2026.** Nalika `publish()` dipunpanggil ing script ingkang dipun-dalani **foreground**, TTS+ffmpeg (audio jawa+ind wadose ±6 menit) nglangkungi wates wekdal tool (60 detik) → process dipunpejahi ing tengah → langkah panyisipan link Google Doc mboten kalampahan → file `.md` lumintu `[DOC_URL]` lan lapor marang Pak Satya tanpa link Drive.

**Aturan wajib:**
1. **`publish()` (utawi script publish ingkang kalebet TTS) WAJIB dipunpanggil ing `background=true` + `notify_on_complete=true`.** Tansah — mboten nate foreground. Cetak output publish menyang `/tmp/run_publish.log`.
2. Sasampunipun rampung, **pereksa baris pungkasan file `.md`** (`~/share/renungan/renungan-<tema>-<tgl>.md`) — mesti wonten `Google Doc: https://...` — **saderengipun** maringi laporan. Boten nyarios "sampun rampung" dumugi link kabukti wonten ing file.
3. Menawi file mboten wonten `Google Doc:` (taksih `[DOC_URL]`), penetes publish mboten rampung → jalankna malih ing background lan priksa `/tmp/run_publish.log` kanggé eror.
4. Mboten nggabungaken cover+publish dadi siji script foreground ala improvisasi ingkang mboten kauji. Nderek prosedur, input `jawa_out_path`, `ind_out_path`, `ogg_jawa_path`, `ogg_ind_path`, `date_str`, `date_iso`.

## 🔴 PITFALL #11: LANGKAHI WORKFLOW RESERACHER→WRITER→EDITOR + BASHA CAMPUR NGOKO

**Kacathet 26-08-2026.** Kula nyerat renungan langsung (nyamethi prosedur 3-peran) lan mboten ngogram basa per `references/krama-renungan-format.md` → kualitas mudhun + Basa Jawi kecampuran ngoko/madya.

**Aturan wajib:**
1. Nderek prosedur SKILL menika (Researcher sabda verbatim → Writer → Editor audit). Boten nyamethi.
2. Basa JAWI WAJIB **Krama Alus resik**: saganten/beteng (sanes segara), manah, siyang (sanes siang), sonten (sanes sore), dalu, wangsul (sanes kondur), matur (sanes ngendika) kagem dhiri, caosaken/aturaken (sanes paring) kagem maringi dhateng sesepuh, punapa→punapa, sedaya (sanes sadaya). Mriksa ulang dumugi resik saderengipun dikirim.
3. Versi Indonesia: labels `SABDA HARI INI` / `URAIAN` / `PRAKTIK SEHARI-HARI` / `RENUNGAN` / `APLIKASI`.
4. Emotikon ±10-14, boten wonten tandha `!`, salam `_Sugeng Enjang, Salam Karahayon_`, tutup `Satuhu 🙏`, header `RENUNGAN PENYISWAAN`.
Fase Editor WAJIB — Writer tidak boleh mengaudit dirinya sendiri.

### Mode Iterasi vs Forward

Dua mode tersedia:

**Forward (1 ronde):** Researcher → Writer → Editor → Orchestrator final.
Cocok untuk renungan rutin. Cepat (±7 menit), murah. Risiko: kesalahan faktual kecil bisa lolos.

**Iterasi (max 3 ronde):** 
```
Ron 1: Writer v1 → Editor → verdict
Ron 2: Writer v2 (bekal kritik) → Editor → verdict
Ron 3: Writer v3 → Editor → final
```
Cocok untuk edisi khusus atau presisi tinggi. Lebih mahal (±15 menit, 2-3x token). Kualitas lebih tinggi: splicing Sabda, fakta medis keliru, dan detail naratif tertangkap sebelum naik.

**Kapan pakai:** Forward untuk harian biasa. Iterasi jika tema rumit, ada kisah nyata dengan detail faktual kompleks, atau user minta presisi tinggi.

**Aturan iterasi:** Max 3 ronde. Orchestrator verifikasi SEMUA klaim Editor sebelum meneruskan ke Writer — Editor bisa salah (false alarm sumber, folder pencarian berbeda).

Studi kasus perbandingan: `references/forward-vs-iterasi.md`.

### Editor Pitfalls (dari audit nyata)

- ❌ Sabda terlalu generik — menyebut tema dalam daftar, bukan mendefinisikan
- ❌ Editor bisa salah klaim sumber (pernah: klaim Sabda dari "Hasta Sila" padahal ada di Sasangka Jati). **Orchestrator WAJIB verifikasi klaim Editor sebelum meneruskan ke Writer.**
- ❌ Editor bisa salah klaim "quote tidak ditemukan" — pastikan mencari di folder yang benar (`/tmp/` untuk file mentah, `/home/satyaaditech/share/pangestu_studi/` untuk catatan studi). Verifikasi dengan read_file langsung.
- ❌ Sabda splicing — Writer menyambung fragmen dengan "..." melompati baris di antaranya. Ini cherry-picking, BUKAN verbatim. Aturan: satu paragraf utuh, atau pemisah eksplisit `[...]`.
- ❌ Detail faktual kisah nyata — organ tubuh, tanggal spesifik, lokasi persis rentan salah meski kisahnya terverifikasi. Jika ragu: gunakan istilah umum (contoh: "merusak kesehatannya" BUKAN "merusak paru-parunya").
- ❌ Kisah nyata tidak mapping ke tema — inspiring tapi beda makna (Hawking = overcoming limitation, bukan narima)
- ❌ Tidak ada Sabda pendukung di uraian (cross-reference)
- ✅ Narima: kisah Jiro Ono (10 kursi, tidak perlu waralaba, tidak iri) — mapping tepat

## Persona & Nada

- Praktisi kejiwaan, paham cara pikir manusia, punya banyak insight pengalaman — **bukan teoritis**.
- WAJIB sisipkan langkah praktis konkret (teknik napas, latihan hening, lakukan X) — minimal 1 per renungan.
- Gunakan "Kita" atau "Anda" — JANGAN PERNAH pakai "kamu" (tidak sopan, tidak menggurui).
- Jika memungkinkan, sisipkan kisah nyata inspirasional di uraian — agar pembaca yakin bahwa ajaran ini benar dan bisa dilakukan.
- ZERO HALUSINASI: semua fakta, kisah, dan quote harus diverifikasi dari sumber asli. Jangan mengarang.
- Bahasa sederhana, kata sehari-hari, relate kehidupan nyata.
- Konten BERSIH — NO komentar/kata-kata Sinok.

## Format Baku (Final — WhatsApp Compatible)

```
*SENIN, 10 AGUSTUS 2026*           ← bold, KAPITAL, blank line setelah

*RENUNGAN PENYISWAAN*              ← bold, blank line setelah

*EMOJI SUBJUDUL KAPITAL: Subtitle EMOJI*  ← bold, diapit emoji yang sesuai tema

_Salam Bahagia Bp/Ibu/Sdr semuanya,_        ← italic, koma di akhir, TANPA tanda seru

*📖 SABDA HARI INI :*              ← emoji + label dalam bold, blank line setelah

Buku Sasangka Jati, Sabda Sang Guru Sejati : _"*quote verbatim*."_   ← "Buku", bukan "Kitab"; sebut "Sabda Sang Guru Sejati"
                                         ← blank line setelah

💭 *URAIAN* :                      ← emoji polos + label bold, KOLON DI LUAR bold
                                    ← 2-3 paragraf pendek, kata sederhana, relate hidup
                                    ← SISIPKAN emoji sesuai konteks di tengah paragraf
                                    ← istilah kunci TANPA bold/italic (heneng-hening-eling, bukan *heneng*)
                                    ← SETIAP kutipan (dari buku manapun) WAJIB miring: _"..."_
                                    ← blank line setelah

🧘 *PRAKTIK* :                      ← emoji polos + label bold, KOLON DI LUAR bold
                                    ← WAJIB: langkah konkret yang bisa langsung dilakukan
*Nama Latihan* — deskripsi:
1. Langkah 1.
2. Langkah 2.
3. Langkah 3.
✅ Kapan & di mana dilakukan.
                                    ← blank line setelah

🎯 *RENUNGAN* :                    ← SATU baris aforisme kontras
                                    ← blank line setelah

📝 *APLIKASI* :                    ← 3 pertanyaan refleksi: apa → mengapa → bagaimana
1. ...
2. ...
3. ...
                                    ← blank line setelah

🙏 Semoga kita semua senantiasa berlimpah dengan Tuntunan dan Perlindungan, Sih dari Sang Guru Sejati. Satuhu 🙏
```

## Aturan Detail (7 koreksi final)

| No | Aturan | Contoh |
|----|--------|--------|
| 1 | Blank line antar header | `*SENIN...*\n\n*RENUNGAN...*\n\n*SUBJUDUL*` |
| 2 | Subjudul: bold + KAPITAL | `*PANEMBAHAN: Keheningan...*` |
| 3 | Emoji SABDA masuk bold | `*📖 SABDA HARI INI :*` |
| 4 | Quote sabda: italic-wrap + bold dalam | `_"*teks quote*."_` |
| 5 | Label (URAIAN/RENUNGAN/APLIKASI): kolon di LUAR bold | `💭 *URAIAN* :` bukan `💭 *URAIAN :*` |
| 6 | Istilah kunci di uraian: TANPA format | `heneng-hening-eling` bukan `*heneng-hening-eling*` |
|| 7 | Kutip buku lain di uraian: WAJIB miring | `_"Hendaklah berusaha..."_` bukan `"Hendaklah..."` |

## Bedakan: Buku vs Ajaran (WAJIB)

Sasangka Jati adalah **BUKU kumpulan Sabda** — bukan sumber ajaran itu sendiri. Sumber ajarannya adalah **Sang Guru Sejati**.

| ❌ SALAH | ✅ BENAR |
|---|---|
| "Buku Sasangka Jati mengajarkan..." | "Ajaran Sang Guru Sejati mengajarkan..." |
| "Sasangka Jati menjanjikan..." | "Ajaran Sang Guru Sejati menunjukkan..." |
| "Menurut Sasangka Jati..." | "Menurut Ajaran Sang Guru Sejati..." |

Satu-satunya saat boleh menyebut "Buku Sasangka Jati":
- Baris sumber Sabda: 📖 SABDA HARI INI
- Saat mengutip verbatim dalam uraian: "Masih dalam buku yang sama..."

## Sumber Sabda

- Quote dari buku Pangestu mana pun (Sasangka Jati/Sabda Khusus/UKK/Olahrasa/Riwayat Hidup Pakde Narto/dll) — KECUALI user minta spesifik sumber, ikuti.
- Buku penguat (uraian): Ulasan Kang Kelana, Olahrasa, Wahyu Sasangka Jati, Bimbingan Roh Suci, Tali Kang Kelana.
- File mentah di `/tmp/ssj_ind.txt`, `/tmp/spra.txt`, `/tmp/ukk.txt`, dll.

## Cara Kirim ke Pengguna

Output akhir WAJIB dalam **code block** (triple backtick) — jangan kirim teks mentah. Telegram tidak konsisten mem-parse `*bold*` dan `_italic_` saat dikirim langsung. Code block menjaga semua markup tetap utuh, pengguna tinggal copy-paste ke WhatsApp.

## Langkah Praktis (PRAKTIK)

Wajib ada — bukan opsional. Formula: teknik sederhana 1-2 menit yang bisa langsung dicoba.
Jenis: teknik napas (4-2-6), latihan hening fokus satu kata, cara berdialog dengan hati, latihan narima, latihan eling di sela aktivitas.
Label: `🧘 *PRAKTIK* :` — sub-judul latihan pakai bold `*Nama Latihan*`, langkah bernomor polos, akhir: ✅ waktu/lokasi.

## File Pendukung

| File | Fungsi |
|---|---|
| `templates/renungan-kosong.txt` | Template kosong siap copy-paste |
| `references/kisah-nyata.md` | Katalog kisah nyata terverifikasi untuk uraian |

## 🔒 DAFTAR BAKU & KUNCI SINGKATAN PUSTAKA KANONIKAL PANGESTU (LOCKED MASTER)
Setiap kutipan, rujukan, atau sitasi buku yang menggunakan singkatan WAJIB mengacu pada daftar baku ini:
- **[SSJ]**   : *Serat Sasangka Jati*
- **[SKH]**   : *Sabda Khusus*
- **[BRSR]**  : *Bawa Raos Ing Salebeting Raos*
- **[UUJM]**  : *Ular-Ular Juru Mengeti*
- **[TKL]**   : *Taman Kamulyan Langgeng*
- **[SPRA]**  : *Sabda Pratama*
- **[WSJ]**   : *Wahyu Sasangka Jati*
- **[ASBS]**  : *Arsip Sarjana Budi Santosa*
- **[UKK]**   : *Ulasan Kang Kelana*
- **[OLHR]**  : *Olahrasa (Buku Olahrasa)*
- **[CJI]**   : *Candrajiwa Indonesia sebagai Dasar Psikoterapi* (Disertasi Prof. Dr. dr. R. Soemantri Hardjoprakoso, Leiden 1956)
