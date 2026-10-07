# Thumbnail YouTube (PIL) + Paket Judul/Deskripsi Siap Copy-Paste

Workflow terbukti (2026-08, episode vlog Simpang Joglo). User suka paket lengkap: thumbnail + pilihan judul + deskripsi + tags siap salin.

## 1. Thumbnail via PIL
```bash
pip install pillow   # sekali per env
```
Resep terbukti:
- Crop foto ke 16:9 (hitung target ratio, crop tengah), resize 1280x720 LANCZOS.
- Gelapkan brightness ~0.88 biar teks kontras.
- Overlay gradasi gelap di 1/3 bawah (alpha naik bertahap) untuk zona teks.
- Font: `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` (Bold) & `DejaVuSans.ttf` — standar Ubuntu.
- Teks: badge kecil atas (kuning, outline hitam), judul BESAR putih outline hitam tebal (stroke_width ~12), sub judul kuning di bawahnya. **Letakkan teks di BAWAH** biar subjek (jembatan/lengkung) tetap terlihat.
- Padding aman dari tepi (safe zone layar HP) — jangan mepet.

**WAJIB vision-review hasil** (vision_analyze): cek keterbacaan, tumpang tindih dengan subjek, dan TYPO (kasus nyata: "NONTO" → "NONTON" ketahuan review). Iterasi sampai bersih. Simpan varian cadangan dengan nama `_v2`.

## 2. Judul — 4 pilihan, rekomendasi yang SEO
- 1 judul panjang-informatif (kata kunci kuat + tahun/sejarah), 2-3 alternatif.
- Format: `NAMA TEMPAT: [hook sejarah] (tahun) + [ikon modern]`.

## 3. Deskripsi — struktur siap copy-paste
- 2 paragraf hook (tempat + misteri/cerita + janji isi).
- ⏱️ TIMESTAMP per segmen (cocokkan script).
- 📌 FAKTA YANG KAMU DAPET (bullet, angka kuat).
- 🗺️ LOKASI, 💬 ajakan komentar, 🔔 subscribe + teaser episode berikut.
- Hashtag (#NamaTempat #Sejarah dll).
- **KREDIT FOTO ARSIP wajib** (koleksi Tropenmuseum/KITLV + lisensi).

## 4. Tags — dipisah koma
Campur: nama tempat, nama alternatif, kata kunci sejarah, nama tokoh, nama era, istilah lokal, tema kota.

## 5. Simpan semua di folder episode
`judul_deskripsi_youtube.md` + `thumbnail_*.jpg` + script + timeline + galeri foto.
