# Riset Berita & Objek Lokal Indonesia — Recipe Detail + Studi Kasus

## Recipe lengkap yang terbukti jalan

### 1. Wikipedia API (utama)
```bash
# Extract teks artikel — &redirects WAJIB untuk halaman redirect (mis. Kotagede → Kotagede, Yogyakarta)
curl -sL "https://id.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&redirects&titles=NAMA_PAGE" | python3 -c "import json,sys; d=json.load(sys.stdin); p=list(d['query']['pages'].values())[0]; print(p.get('extract','NO EXTRACT'))"

# Ringkasan (auto-follow redirect, lebih ringan):
curl -sL -A "Mozilla/5.0" "https://id.wikipedia.org/api/rest_v1/page/summary/NAMA_PAGE"

# Search judul:
curl -sL "https://id.wikipedia.org/w/api.php?action=query&list=search&srsearch=KATA%20KUNCI&srlimit=10&format=json"
```
- Tanpa `&redirects` (atau `&redirects=1` yang kadang diabaikan), halaman redirect mengembalikan extract KOSONG atau JSONDecodeError → selalu pakai `&redirects` polos atau REST summary.
- Gagal JSON → `sleep 2` lalu retry (rate limit).
- Baca extract sampai habis: fakta emas sering ada di akhir (etimologi nama, trivia budaya, kutipan lagu).

### 2. detik.com search
```bash
curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0" "https://www.detik.com/search/searchall?query=bendung%20tirtonadi" -o /tmp/detik.html
```
Parse (python):
```python
import re, html
t = open('/tmp/detik.html', encoding='utf-8', errors='ignore').read()
txt = re.sub(r'<script.*?</script>', '', t, flags=re.S)
txt = re.sub(r'<style.*?</style>', '', txt, flags=re.S)
txt = re.sub(r'<[^>]+>', ' ', txt); txt = html.unescape(txt); txt = re.sub(r'\s+', ' ', txt)
# konteks keyword:
idxs = [m.start() for m in re.finditer('NAMA_KUNCI', txt)]
# URL artikel:
links = re.findall(r'href="(https://[^"]*detik\.com/[^"]+)"[^>]*>(.*?)</a>', t, re.S)
```

### 3. Ambil isi artikel detik
```python
# body di class itp_bodycontent (fallback detail__body-text)
m = re.search(r'class="itp_bodycontent">(.*?)<div class="detail_', t, re.S)
body = m.group(1) if m else t
body = re.sub(r'<[^>]+>', ' ', body); body = html.unescape(body); body = re.sub(r'\s+', ' ', body)
```
- Artikel `/fototravel/` = kumpulan caption foto, sering padat fakta (tanggal, nama lokasi, fungsi, tahun revitalisasi).
- Catatan: terkadang artikel menyebut dua nama untuk objek sama (mis. Kali Pepe vs Kali Anyar) — catat keduanya, jangan pilih salah satu tanpa bukti.

## Matriks sumber (hasil uji langsung)

| Sumber | Status | Catatan |
|--------|--------|---------|
| id.wikipedia.org API | ✅ Jalan | Wajib `&redirects`; REST summary untuk redirect |
| detik.com search | ✅ Jalan | Fallback terbaik topik lokal |
| Bing html | ❌ CAPTCHA | "Please solve the challenge" |
| DuckDuckGo (html & lite) | ❌ Kosong | Balasan kosong/blocked |
| Tribun search | ❌ Kosong | JS-render, perlu login |
| Kompas search | ❌ Tidak kebaca | 0 hasil relevan via curl |
| Solopos (?s=) | ❌ Blocked | File ~5KB = bukan halaman hasil |

## Studi kasus: Bendung Tirtonadi, Solo (episode vlog 2)

Konteks: Wikipedia tidak punya halaman "Bendung Tirtonadi"; hanya ada `Terminal_Tirtonadi`, `Tirtonadi` (film), `Bengawan_Solo`, `Kota_Surakarta`.

Fakta yang ditemukan & sumbernya:
- **Taman Bendung Tirtonadi** — bantaran Sungai Kali Pepe, revitalisasi 2022, favorit sunset & nunggu buka puasa → detikcom fototravel 6 Apr 2022
- **Bendung karet** di aliran Kali Anyar; insiden busa misterius 2019 (DPRD minta DLH selidiki) → detikcom news 13 Nov 2019
- **Embung Tirtonadi** rencana 2016 (APBN): penampungan air, air baku minum, wisata air Kalianyar, ±300 KK direlokasi, jembatan gantung → detikcom news 22 Apr 2016
- **Solo = pertemuan 5 sungai** (Bengawan Solo, Kali Pepe, Kali Anyar, Kali Gajah Putih, Kali Premulung) + normalisasi PUPR/BBWS 2017 → detikcom finance 15 Mar 2017
- **Emas dari Wikipedia `Terminal_Tirtonadi`**: arti nama "Tirtonadi" = taman permai era Mangkunegaran (tanah bekas swapraja) di sisi selatan Kali Pepe + lagu Gesang *"Tirtonadi yang permai, di tepi sungai"* → hook utama episode
- **Bengawan Solo** (Wikipedia): sungai terpanjang di Jawa ±600 km, lagu Gesang 1940 dipakai film Kurosawa (Stray Dog 1949), Ichikawa (1951), Ozu (1962), In the Mood for Love; kanal Belanda 1890 (12 km) alihkan delta; fosil Manusia Jawa di Sangiran
- **Nama "Solo"** (Wikipedia `Kota_Surakarta`): dari Desa Sala, Pakubuwana II beli tanah 10.000 ringgit dari Kyai Sala (1745)

Hal yang TIDAK ditemukan (jujur ditandai):
- Tahun pembuatan bendung asli → ⚠️ di naskah; saran cek papan info lokasi/tanya petugas BBWS
- Posisi persis bendung (Kali Pepe vs Kali Anyar) → verifikasi lapangan

Hasil akhir tersimpan: `output/timeline_bendung_tirtonadi.md` & `output/vlog_tirtonadi_episode2_funfacts.md` (di /home/satyaaditech/yt-automation/).
