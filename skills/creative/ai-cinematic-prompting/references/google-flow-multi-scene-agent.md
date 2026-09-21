# Google Flow Multi-Scene Generation via Agent Mode

Panduan teknis dan template prompt untuk mengeksekusi produksi video berseri/multi-scene (misal sketsa komedi 3 scene @ 10 detik) secara otomatis dalam **sekali copy-paste** menggunakan **Google Flow Agent**.

---

## 1. Arsitektur Dua Mode Kerja di Google Flow

| Fitur | Standard Prompt Box | Google Flow Agent (`Agent` Toggle ON) |
| :--- | :--- | :--- |
| **Karakteristik** | Menghasilkan 1 klip tunggal per prompt (5s / 10s). | Asisten sutradara kreatif bawaan Google Flow. |
| **Multi-Scene** | **Tidak bisa** memproses banyak scene sekaligus (akan glitch/terpotong). | **Bisa** membaca storyboard berurutan dan memproduksi rentetan klip berurutan. |
| **Batching** | Manual (harus generate satu per satu). | Otomatis batch generation ke dalam asset project aktif. |
| **Kebutuhan Prompt** | Potongan per scene dimasukkan terpisah. | Satu Master Director Prompt utuh sekali kirim. |

---

## 2. Setelan Kunci Pre-Flight (Wajib Sebelum Input Prompt)

Agar Google Flow Agent berjalan 100% otonom tanpa mandheg meminta konfirmasi manual per clip:

1. **Aktifkan Mode Agent**:
   - Di kolom prompt Google Flow, klik tombol **Agent** hingga ikon robot/bintang aktif.
2. **Ubah Konfirmasi Kredit ke `Never`**:
   - Klik menu **Settings** di pojok bawah kolom prompt Agent.
   - Pada opsi *"Confirm before generating"*, ubah dari *Always* menjadi **`Never`**.
   - *Catatan penting:* Jika disetel *Always*, Agent akan berhenti di tiap scene untuk meminta izin memotong kuota kredit AI. Jika disetel *Never*, seluruh scene akan dieksekusi berturut-turut tanpa jeda.
3. **Pilih Default Aspect Ratio**:
   - Pilih **9:16** untuk YouTube Shorts / TikTok / Reels.
   - Pilih **16:9** untuk video horizontal standar YouTube.
4. **Agent Instructions (Opsional untuk Konsistensi Tinggi)**:
   - Klik *Agent Instructions -> Add instruction* di bawah prompt box. Masukkan referensi gambar karakter/gaya agar dipertahankan di seluruh session proyek.

---

## 3. Struktur Master Director Prompt (1x Copy-Paste)

Gunakan struktur modular ini saat menyusun prompt sekali tempel:

```text
[ROLE & WORKFLOW DIRECTIVE]
You are a master film director and cinematographer executing a complete [N]-scene [genre/theme] video sequence (Total runtime: [X] seconds, structured as [N] sequential [Y]-second video clips).

Execute the generation of ALL [N] video clips sequentially into my project canvas right now. Maintain absolute character visual identity, wardrobe consistency, and environment across all generated scenes.

---

[GLOBAL ASSET DEFINITIONS]
- Character 1 ([Name/Role]): [Age]-year-old [Ethnicity], [Hair/Facial details], [Wardrobe/Clothing], [Persona & default expression].
- Character 2 ([Name/Role]): [Age]-year-old [Ethnicity], [Hair/Facial details], [Wardrobe/Clothing], [Persona & default expression].
- Environment: [Setting description, furniture, key props, lighting temperature (e.g. 3200K warm), camera optics, photorealistic 8K, 24fps].

---

[SCENE 1: [TITLE] - [START_TIME] to [END_TIME]]
- Target Duration: [Y] seconds
- Shot Type & Camera: [Shot framing, lens mm, aperture, camera motion directive (push-in, pan, tracking)].
- Visual Action: [Specific actions, body posture, changes in blocking].
- Dialogue & Acting Cue: [Character name] delivers: "[Indonesian dialogue]" ([Description of lip & facial movement naturally matching speech tone]).
- Render Command: Generate Video Clip 1 now.

---

[SCENE 2: [TITLE] - [START_TIME] to [END_TIME]]
- Target Duration: [Y] seconds
- Shot Type & Camera: [Shot framing, lens mm, aperture, dramatic camera effect (e.g. vertigo dolly-zoom)].
- Visual Action: [Intense facial reaction, physical response, comedic timing].
- Dialogue & Acting Cue: [Internal monologue/dialogue cue matching expression].
- Render Command: Generate Video Clip 2 now.

---

[SCENE 3: [TITLE] - [START_TIME] to [END_TIME]]
- Target Duration: [Y] seconds
- Shot Type & Camera: [Shot framing, lens mm, transition motion (e.g. snap whip-pan)].
- Visual Action: [Climax/punchline action, slapstick comedy, final pose].
- Dialogue & Acting Cue: [Punchline dialogue cue matching physical action].
- Render Command: Generate Video Clip 3 now.
```

---

## 4. Alur Dialog & Audio (Post-Production Workflow)

### Fakta Teknis Engine:
Google Flow / Veo adalah **mesin visual**. Ia merender gerakan mulut, ekspresi muka berbicara (*talking facial expressions*), dan gestur tubuh secara sangat meyakinkan, namun **belum menghasilkan track audio percakapan bahasa Indonesia yang sinkron secara langsung**.

### Dua Jalur Eksekusi Dialog:

#### Jalur A: Dubbing / Voiceover Komedi (Standar YouTube Shorts & TikTok) — *Sangat Direkomendasikan*
1. Download file video klip hasil render Google Flow.
2. Buka di editor video (**CapCut** Mobile / Desktop).
3. Urutkan klip di timeline (Scene 1 ➔ Scene 2 ➔ Scene 3).
4. Tambahkan audio dialog:
   - **Opsi TTS:** Masukkan teks naskah bahasa Indonesia ➔ gunakan fitur *Text-to-Speech* CapCut (pilih suara santai/lucu).
   - **Opsi Dubbing Suara:** Rekam dubbing sendiri langsung di CapCut dengan intonasi kocak/ekspresif.
5. Tambahkan **Auto Captions (Keterangan Otomatis)** warna kuning tebal di tengah bawah layar.
6. Beri layer sound effects (SFX): jam berdetak, deg-degan, record scratch, brass sting komedi, atau suara tawa (*laugh track*).

#### Jalur B: Phonetic AI Lip-Sync (Bibir Menyesuaikan Tiap Suku Kata)
1. Buat track dialog audio terlebih dahulu (rekaman vokal atau ElevenLabs).
2. Masukkan klip video dari Google Flow + file audio ke tools AI Lip-Sync (seperti **Hedra**, **LivePortrait**, atau **Kling Lip-Sync**).
3. Ekspor video yang sudah sinkron bibirnya ke CapCut untuk final cut dan subtitle.

---

## 5. Quality Guardrails & Pitfalls

- **Durasi Ideal**: Batasi durasi tiap klip antara **5 hingga 10 detik**. Klip di atas 10 detik rentan mengalami degradasi visual (*morphing/hallucination*).
- **Format Bahasa Prompt**: Prompt directive visual dan setting karakter **wajib dalam bahasa Inggris** agar dipahami sempurna oleh AI model (Veo/Imagen), sementara kalimat dialog disematkan di dalam *acting cue* tanda kutip.
- **Konfirmasi Mandheg**: Jika Google Flow tampak berhenti setelah Scene 1, periksa kembali menu *Settings* -> pastikan *Confirm before generating* disetel **Never**.
