---
name: vlog-sejarah-lokasi
description: Use for history-location vlogs (verified timeline + script).
---

# Vlog Sejarah Lokasi (Jalan Pagi Sejarah)

Workflow untuk seri vlog "Jalan Pagi Sejarah" — Pak Satya jalan pagi sambil bercerita sejarah lokasi olahraga (Solo & sekitarnya). Semua fakta WAJIB terverifikasi.

## Trigger
- User minta script/bikin konsep vlog lokasi bersejarah
- User sebut lokasi baru buat episode (Sriwedari, Balekambang, Pasar Gede, dll)
- User minta timeline sejarah tokoh/tempat
- User kirim FOTO lokasi & minta "jadi detektif" / cari fakta menarik + foto menarik (MODE DETEKTIF)

## Mode Detektif — paket deliverable WAJIB (urutan)
1. **Identifikasi lokasi** dari foto (vision_analyze) — koreksi user lebih valid dari vision; jangan ragu verifikasi ulang.
2. **Fakta terverifikasi**: Wikipedia API (curl), Google News RSS, r.jina.ai, arsip web (web.archive.org CDX untuk artikel hilang).
3. **Foto tempo dulu**: cari di Wikimedia Commons (search api) — arsip Tropenmuseum (CC BY-SA 3.0) & KITLV (CC BY 4.0) paling kaya; unduh via `commons.wikimedia.org/wiki/Special:FilePath/<File>` (hindari rate limit API); konversi TIFF→JPG (PIL); verifikasi isi foto dengan vision_analyze; ambil metadata (tanggal, lisensi, kredit) dari imageinfo API.
4. **Kirim galeri**: foto + keterangan nempel via Bot API sendPhoto (pola di atas), caption ≤1024, sertakan sumber & lisensi.
5. **Script template** (hook 10 detik, 5W+1H, fun fact, cliffhanger, CTA) + timeline riset.
6. **Judul + deskripsi + tags YOUTUBE SIAP COPY-PASTE** — user tinggal salin; sertakan timestamp, fakta, kredit foto arsip, hashtag.
7. Simpan semua di folder episode: script, timeline, foto_tempo_dulu/, galeri md, thumbnail, judul_deskripsi_youtube.md.

## Format yang disukai user (PENTING)
- **Long video 10-15 menit**, walk & talk santai
- **Point per point, label 5W+1H (APA/SIAPA/KAPAN/DIMANA/MENGAPA/BAGAIMANA)** — user hafal script lewat struktur ini; JANGAN rombak jadi narasi mengalir ala v2 (user tolak, balik ke v1)
- Data komplit, JANGAN dikurangi
- Fun fact per lokasi (fakta jarang diketahui orang)
- File .md bisa di-download. **Struktur folder: `/home/satyaaditech/yt-automation/Vlog/<N>. Episode <Nama>/`** — tiap episode 1 folder berisi: `vlog_<lokasi>_episode<N>_funfacts.md` (script final) + `timeline_<tokoh/lokasi>.md` (riset) + bonus (jika ada). Template di `templates/template_vlog_sejarah_lokasi.md`.
- Tambahan retensi yang disetujui user: hook 10 detik, cliffhanger 1 kalimat tiap segmen, CTA komentar
- Bahasa Indonesia, narasi lisan santai

## Kirim galeri foto ke Telegram (keterangan nempel di tiap foto)

MEDIA:/path di pesan Hermes mengirim foto TANPA caption menempel (keterangan jadi pesan terpisah). Kalau user minta "foto di atas, keterangan di bawahnya", kirim via Bot API langsung dengan caption native:

```bash
TOKEN="<bot token>"; CHAT="<chat_id>"; THREAD="<message_thread_id>"
curl -s -F "chat_id=$CHAT" -F "message_thread_id=$THREAD" -F "photo=@<file>.jpg" -F "caption=<keterangan>" "https://api.telegram.org/bot${TOKEN}/sendPhoto"
```

- CHAT/THREAD ambil dari konteks sesi (grup & topik saat itu), jangan hardcode.
- Cek respons `"ok":true` + message_id untuk verifikasi.
- Caption ≤1024 karakter.

## Workflow

### 1. Riset — web tools SERING MATI, pakai curl + Wikipedia API
`web_search`/`web_extract` error FIRECRAWL_API_KEY. Fallback yang sudah terbukti jalan:
```bash
# Extract teks artikel (handle redirect dengan &redirects)
curl -sL "https://id.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&redirects&titles=NAMA_PAGE" | python3 -c "import json,sys; d=json.load(sys.stdin); p=list(d['query']['pages'].values())[0]; print(p.get('extract','NO EXTRACT'))"
# Ringkasan pendek (otomatis follow redirect)
curl -sL -A "Mozilla/5.0" "https://id.wikipedia.org/api/rest_v1/page/summary/NAMA_PAGE"
```
- Untuk halaman yang redirect (mis. Kotagede → Kotagede, Yogyakarta): REST summary atau param `&redirects` Wajib, kalau tidak extract kosong/JSON error.
- Rate limit: kalau JSONDecodeError, tambah `sleep 2` sebelum retry.

### 2. Verifikasi & tandai
- Fakta tanpa sumber → tandai `±` (perkiraan) atau omits.
- Lokasi yang belum terverifikasi → sebut apa adanya per sumber, jangan mengarang (contoh: Bengawan Sore, lokasinya tidak dipastikan).
- Cek hal-hal yang harus dicek di lapangan (akses petilasan dll) → catat di tips produksi.

### 3. Bangun dokumen timeline (template utama user)
- Tahapan kronologis: TAHAP 0 (latar keluarga) → dst, tiap tahap: tabel (Poin | Detail | Lokasi sekarang)
- Lokasi harus dipetakan ke kondisi modern (desa kuno → kabupaten/kota sekarang)
- Peta ASCII alur + tabel posisi relatif semua lokasi
- Bahan cerita untuk vlog (alur dramatis terbaik, koneksi ke penonton lokal)
- Sumber lengkap di akhir

### 4. Tulis script narasi
Struktur: HOOK 10 detik → INTRO → SEGMEN 1..4 (5W+1H + FUN FACT + CLIFFHANGER) → CLOSING (recap + CTA komentar + teaser episode berikutnya)
- Tiap segmen: narasi + blok FUN FACT + [CLIFFHANGER] 1 kalimat
- Tandai [B-ROLL]/[CUT]/[ZOOM] di narasi untuk panduan syuting
- 5W+1H checklist per segmen (checkbox)
- Bank FUN FACT tabel (verified)
- Tips produksi + SUMBER

### 5. Simpan
- Nama file: `vlog_<lokasi>_episode<N>_<versi>.md` di `/home/satyaaditech/yt-automation/output/`
- Kirim ke user: MEDIA:/path + ringkasan struktur di chat
- Contoh jadi: `vlog_manahan_episode1_funfacts.md` & `timeline_ki_ageng_pamanahan.md` (referensi lengkap)

## Pitfalls
- Jangan kurangi isi versi lama saat revisi — user cek komplit/tidak. Tambah saja.
- Jangan tulis label 5W+1H keluar dari narasi (mis. "sekarang bagian SIAPA") — itu struktur HAFALAN user, bukan yang dibaca keras.
- Jangan klaim "stadion pertama/tertua" tanpa verifikasi (klaim kuat = cek sumber).
- Jangan sebut lokasi yang belum pasti; jujur tandai.
- Web tools error berulang → langsung beralih curl, jangan retry web_search berkali-kali (tool loop warning).
- **Koreksi geografi dari user WAJIB diutamakan** — user kenal lokasinya. Saat user mengoreksi (mis. "bendung di Kali Pepe, bukan Bengawan Solo"), terima, verifikasi ulang sumber, perbaiki file, jangan memaksakan klaim dari berita. Contoh: episode 2 Tirtonadi — Kali Pepe membelah kota & bermuara ke Bengawan Solo di Sangkrah; Bengawan Solo di sisi timur, jauh dari bendung.
- Contoh workflow lengkap terverifikasi: sesi episode 1 Manahan (lihat `timeline_ki_ageng_pamanahan.md` di output/).
- **Kawasan Tirtonadi (episode 2) = klaster spot**: Bendung & Taman Tirtonadi (pinggir Kali Pepe, bukan Bengawan Solo), Masjid Raya Sheikh Zayed (hibah UEA 2022, bekas depot Pertamina Gilingan, karpet batik, 81 kubah), Tugu Keris di Jembatan Tirtonadi (2019, kontroversi pakem), Terminal Tirtonadi (1975), Makam Putri Cempo (tanggul aliran Kali Anyar). Rute 5 segmen ±2-2,5 km. Semua file di output/.
