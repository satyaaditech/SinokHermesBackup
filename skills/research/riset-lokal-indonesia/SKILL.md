---
name: riset-lokal-indonesia
description: Use when researching Indonesian local topics or Indonesian content websites (Blogger etc.) via curl.
---

# Riset Topik Lokal Indonesia (via curl, tanpa web tools)

Workflow riset fakta untuk topik lokal Indonesia (tempat bersejarah, bendung/taman/jembatan, tokoh daerah, event kota) saat web tools (`web_search`/`web_extract`) error atau Wikipedia tidak punya halaman topiknya. Output selalu riset TERVERIFIKASI + penandaan jujur untuk yang belum bisa dibuktikan.

## Trigger
- User minta konten/script/riset soal lokasi atau objek lokal Indonesia
- Wikipedia API mengembalikan "NO EXTRACT"/tidak ada halaman
- Butuh fakta sejarah lokal yang tidak ada di sumber mainstream
- User minta riset materi dari website/blog konten Indonesia (mis. putunepaktani.com) → teknik enumerasi post + ekstraksi isi: `references/blogger-site-research.md`
- User minta ringkasan artikel → format BULAT POIN (bukan paragraf panjang): 🎯 inti → penjelasan per bagian → ⚠️ verifikasi/poin kunci → 🛠️ solusi praktis → 🚫 yang TIDAK dilakukan → 📌 takeaway. Bahasa Indonesia.
- User minta FOTO TEMPO DULU / foto arsip lokasi Indonesia untuk konten (B-roll vlog, galeri) → teknik berburu di Wikimedia Commons (Tropenmuseum/KITLV): `references/foto-arsip-wikimedia.md`
- User minta thumbnail YouTube / judul-deskripsi siap copy-paste → teknik PIL + paket packaging: `references/thumbnail-dan-packaging-youtube.md`
- User minta riset organisasi spiritual/kepercayaan Indonesia (Pangestu dll, topik TG th 1096 🕊️) → dossier terverifikasi + sumber: `references/pangestu-dossier.md` (file lengkap: ~/share/pangestu_riset.md, tersedia via HTTP :8000). Situs resmi SPA → render via r.jina.ai (lihat skill web-research-fallback).

## Sumber utama (urut prioritas)

### 1. Wikipedia API — selalu coba duluan
```bash
# Extract teks artikel — param &redirects WAJIB (tanpa itu extract kosong/JSON error untuk halaman redirect)
curl -sL "https://id.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&redirects&titles=NAMA_PAGE" | python3 -c "import json,sys; d=json.load(sys.stdin); p=list(d['query']['pages'].values())[0]; print(p.get('extract','NO EXTRACT'))"
# Ringkasan pendek (auto-follow redirect) — untuk cek judul sebenarnya
curl -sL -A "Mozilla/5.0" "https://id.wikipedia.org/api/rest_v1/page/summary/NAMA_PAGE"
# Cari halaman dengan keyword
curl -sL "https://id.wikipedia.org/w/api.php?action=query&list=search&srsearch=KATA%20KUNCI&srlimit=10&format=json"
```
- Rate limit: JSONDecodeError → `sleep 2` lalu retry.
- Halaman Wikipedia Indonesia yang kaya fakta lokal (kasus Solo): `Kota_Surakarta`, `Bengawan_Solo`, `Terminal_Tirtonadi` — sering memuat etimologi nama + sejarah lokal yang jadi emas konten.
- Cek bagian akhir extract (sering ada etimologi/arti nama, trivia budaya) — jangan berhenti di 3000 chars pertama.

### 2. Search berita detik.com — fallback utama saat Wikipedia kosong
```bash
curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0" "https://www.detik.com/search/searchall?query=NAMA%20TOPIK" -o /tmp/detik.html
```
- Parse: strip `<script>/<style>`, hapus tag, unescape, collapse whitespace → cari konteks keyword → ekstrak URL artikel `href="(https://[^"]*detik\.com/[^"]+)"`.
- Artikel body: cari `class="itp_bodycontent"` (fallback `detail__body-text`), strip tag, unescape, potong 2000-4000 chars. Artikel `/fototravel/` berisi caption penuh fakta (tanggal, nama, fungsi).
- Detail lengkap + studi kasus: `references/riset_berita_indonesia.md`

### 3. Yang TIDAK reliable — jangan buang retry
- **Bing** html: CAPTCHA ("Please solve the challenge")
- **DuckDuckGo** (html & lite): kosong/blocked
- **Tribun search**: hasil kosong (JS-render/login)
- **Kompas search / Solopos** (WordPress `?s=`): hasil tidak kebaca / ter-block
→ Langsung detik.com; jangan ulang search engine yang gagal (tool loop warning).

## Aturan anti-halusinasi (wajib)
1. Objek fisik kecil (bendung, taman, jembatan) sering TIDAK punya data sejarah terverifikasi online (mis. tahun pembuatan). JANGAN mengarang angka/tahun → tandai ⚠️, sampaikan apa adanya, dan rekomendasikan verifikasi di lokasi (papan info, tanya petugas/warga).
2. Sumber menyebut dua nama untuk satu objek → sampaikan keduanya + rekomendasi cek lapangan. Jangan pilih satu tanpa bukti.
3. Klaim kuat ("pertama/terbesar/tertua") wajib cross-check sebelum diucapkan.
4. Lokasi geografis yang tidak terverifikasi (mis. nama sungai/desa) → sebut per sumber atau tandai ±, jangan mengarang posisi.
5. Sertakan daftar SUMBER di akhir dokumen (nama sumber + tanggal/artikel), biar bisa diverifikasi ulang.

## Output
- Dokumen timeline (kronologi + lokasi dipetakan ke kondisi modern) bila konteks sejarah.
- Daftar fakta terverifikasi + penandaan ⚠️/±.
- Pointer ke skill lain: untuk konten vlog sejarah lokasi → skill user-owned `vlog-sejarah-lokasi` (butuh `hermes curator adopt` agar bisa dikurasi); untuk scraping headline harian → `scrape-indonesian-news` (juga user-owned).
