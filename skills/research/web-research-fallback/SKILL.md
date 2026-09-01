---
name: web-research-fallback
description: Curl research when search tools fail (Brave, detik).
---

# Web Research Fallback (curl-only)

## References & Tools
- Referensi Pola Scraping Yahoo Search: [references/yahoo-search-scraping.md](references/yahoo-search-scraping.md)
- Script Ekstraksi URL Standalone (zero-dependency / tanpa bs4): `scripts/extract_url_text.py <URL>`

Pola riset web saat `web_search`/`web_extract` gagal (error API key, 401, dll) atau semua mesin pencari kena captcha. Teruji di sesi riset lokasi Solo (vlog & berita lokal).

## Rantai fallback (urutkan, jangan retry yang gagal berulang)

1. `web_search`/`web_extract` (Firecrawl) — coba dulu, tapi siap gagal
1b. **Direct URL Text Extraction (saat `web_extract` unconfigured/gagal)**:
   - Gunakan script helper zero-dependency:
     ```bash
     python3 ~/.hermes/skills/research/web-research-fallback/scripts/extract_url_text.py "https://example.com/article"
     ```
   - Pola ini menggunakan Python stdlib (`urllib` + `html.parser.HTMLParser`) untuk membuang tag `<script>`, `<style>`, `<nav>`, `<footer>`, `<header>` secara deterministik tanpa ketergantungan paket pihak ketiga (`bs4` / `trafilatura` yang sering belum terinstal).
2. **Wikipedia API via curl** — paling andal, data terstruktur:
   ```bash
   # Extract teks artikel (param &redirects wajib utk halaman redirect)
   curl -sL "https://id.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&redirects&titles=NAMA_PAGE" \
     | python3 -c "import json,sys; d=json.load(sys.stdin); p=list(d['query']['pages'].values())[0]; print(p.get('extract','NO EXTRACT'))"
   # Ringkasan pendek (auto-follow redirect)
   curl -sL -A "Mozilla/5.0" "https://id.wikipedia.org/api/rest_v1/page/summary/NAMA_PAGE"
   ```
   - Redirect (mis. Kotagede → Kotagede, Yogyakarta): REST summary atau `&redirects`; tanpa itu extract kosong/JSON error.
   - Rate limit: JSONDecodeError → `sleep 2` sebelum retry.
   - Halaman daftar/kategori (mis. "Arsitektur dan peninggalan sejarah di Surakarta") = tambang emas: daftar lengkap objek + sejarah.

2b. **Google News RSS + Direct Site Search Fallback (Bypass Captchas & Obfuscated Redirects)**
   - **Metode**: Saat Google/Brave search memblokir request dengan Captcha atau 429, Google News RSS (XML format) dapat digunakan secara bebas tanpa kunci API untuk riset berita terbaru.
   - **Langkah 1 (Ambil Judul saking RSS)**:
     ```python
     import urllib.request, urllib.parse, xml.etree.ElementTree as ET
     rss_url = f"https://news.google.com/rss/search?q={urllib.parse.quote_plus(query)}&hl=id&gl=ID&ceid=ID:id"
     req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
     with urllib.request.urlopen(req) as res:
         root = ET.fromstring(res.read())
         items = [{'title': item.find('title').text, 'link': item.find('link').text} for item in root.findall('./channel/item')]
     ```
   - **Langkah 2 (Cari Direct Link)**: Amargi tautan redirect Google News terenkripsi dhateng client-side, gunakaken judul berita bersih saking RSS kagem nggoleki langsung ing mesin pencari internal media lokal (kados `https://search.kompas.com/search/?q=<judul>` utawi `https://search.detik.com/search?query=<judul>`) ngagem `urllib.request`.
   - **Langkah 3 (Ekstraksi Paragraf)**:
     - Kagem Kompas.com, tambahkan parameter `?page=all` dhateng URL kagem memuat sedaya artikel wonten ing satunggal kaca.
     - Ekstrak paragraf ngagem regex `re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)` lan bersihkan boilerplate/JS kanthi nyaring baris ingkang ngandung keyword skrip (kados `var`, `document.`, `{`, lan `}`).
3. **Brave Search HTML** — paling toleran; Bing/DDG/Mojeek/searx/Reddit biasanya kena captcha/blok:
   ```bash
   curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0" "https://search.brave.com/search?q=<query>"
   ```
   Judul hasil bisa di-parse dari atribut `title` atau href.
3b. **r.jina.ai reader vs search**:
   - **Reader (`https://r.jina.ai/<url>`)**: Tetap gratis dan bisa digunakan untuk mengekstrak konten markdown dari URL berita/Wikipedia tanpa API key.
   - **Search (`https://s.jina.ai/<query>`)**: Membutuhkan API key (HTTP 401 jika tanpa auth). Jangan gunakan sebagai search engine fallback kosong.

4. **Yahoo Search & Google News Fallbacks**:
   - Jika Brave Search kena 429 / CAPTCHA dan DuckDuckGo bermasalah (SSL atau diblok), gunakan **Yahoo Search** via curl/python:
     `https://search.yahoo.com/search?p=<query>`
     Ekstrak link asli dari atribut `href` yang mengandung redirect `RU=` (misal parse parameter `RU` lalu unquote).
   - Gunakan **Google News RSS** untuk pencarian berita lokal indonesia terupdate:
     `https://news.google.com/rss/search?q=<query>&hl=id-ID&gl=ID&ceid=ID:id`
3c. **DDG via r.jina.ai** (teruji sesi riset Pangestu 2026) — Google via jina = 403, DDG via curl langsung = rate-limit/kosong. Pakai jina utk DDG:
   ```bash
   curl -sL "https://r.jina.ai/https://duckduckgo.com/html/?q=<QUERY_URLENCODED>" -A "Mozilla/5.0" --max-time 90
   ```
   - Output jina berupa markdown: judul hasil = baris `## [Title](url)` → daftar cepat dengan `grep -E '^## \['`.
   - Link hasil dibungkus redirect `duckduckgo.com/l/?uddg=<urlencoded>` → **dekode param `uddg`** utk URL asli (jangan pakai URL wrapper). Regex: `uddg=([^&]+)` + urllib.parse.unquote.
   - Jangan retry DDG curl langsung berulang saat hasil kosong — langsung beralih ke jina (rate limit berbasis IP).
3d. **Situs SPA / JS-rendered** (teruji pangestu.or.id, CodeIgniter): curl balik HTTP 200 tapi isi kosong/nav-only karena konten dirender JS; sitemap.xml sering 404. Solusi:
   - `curl -sL "https://r.jina.ai/<url>"` → render JS jadi markdown.
   - Jangan menebak path halaman — **gali URL dari menu navigasi** di halaman mana pun yang kebuka (submenu Sejarah/Kegiatan/Arsip sering memuat path lengkap).
3e. **PDF resmi = tambang data**: buletin/majalah organisasi sering jadi satu-satunya sumber data resmi (hasil kongres, statistik cabang, keputusan). Unduh + ekstrak:
   ```bash
   pip install pypdf -q   # pdftotext sering tidak terpasang
   python3 -c "from pypdf import PdfReader; r=PdfReader('file.pdf'); open('out.txt','w').write('\n'.join((p.extract_text() or '') for p in r.pages))"
   ```
   lalu grep kata kunci (mis. hasil kongres, nama pejabat, jumlah cabang). Cari PDF via DDG dengan `site:domain` + kata kunci.ngan retry)
   # Bing via r.jina.ai = markdown bersih, JALAN (terbukti 2026-08):
   curl -s "https://r.jina.ai/https://www.bing.com/search?q=<query>"
   # Halaman web mana pun juga bisa di-render ke markdown:
   curl -s "https://r.jina.ai/https://<url>"
   ```
   Catatan: hasil Bing kadang berisi sampah (hasil tak relevan); grep filter kata kunci. Kalau butuh fakta kunci yang terdokumentasi (tanggal historis, weton, konversi kalender), langsung cek Wikipedia id via API — biasanya sudah punya contoh eksplisit.
4. **Google News RSS** — mesin pencari berita paling andal saat Brave/DDG/Bing kena blok (terbukti 2026-08, semua engine lain kosong/captcha):
   - Link artikel = redirect `news.google.com/rss/articles/...` yang TIDAK resolve via curl -IL (loop). Jangan buang waktu: langsung tebak URL langsung situs (pola `<domain>/<slug>-<id>`) lalu cari di Wayback CDX (lihat #6), atau fetch via r.jina.ai.

## r.jina.ai — baca isi artikel (bypass sebagian blok)

```bash
curl -sL --max-time 45 "https://r.jina.ai/https://<domain>/<path>" 
```
- JALAN: tribunnews.com, hutamakarya.com, kebanyakan portal daerah. GAGAL (403 Cloudflare/CAPTCHA): solopos.com/espos.id. Kalau r.jina.ai balik 403/521 karakter → langsung fallback ke Wayback snapshot (di bawah).
- Isi artikel tribun ada di baris `**TRIBUNSOLO.COM, SOLO** ...` — parse kalimat polos (bukan menu/nav), cari kata kunci + konteks ±300 karakter.
- JANGAN pakai r.jina.ai untuk Google/Bing search: Google kena 403 AbuseAlleviation (rate limit IP), Bing di-hijack ke hasil sampah (iklan Prancis dll).

## Wayback CDX — cari URL artikel lama & baca isi yang 403/Cloudflare

```bash
# Cari URL artikel lama di satu domain (wildcard + filter kata kunci)
curl -sL "https://web.archive.org/cdx/search/cdx?url=<domain>&matchType=domain&filter=original:.*<pattern>.*&output=text&limit=30&collapse=urlkey&fl=timestamp,original"
# Contoh: url=solo.tribunnews.com&filter=original:.*simpang-joglo.*
```
- WAJIB `https://` (bukan http — ke trigger security scan). `filter` + `fl=timestamp,original` = dapat daftar URL + tanggal snapshot sekaligus. Ini cara paling cepat menemukan URL artikel lama yang sudah hilang dari Google News.
- Baca isi snapshot: `curl -sL "https://web.archive.org/web/<timestamp>/<url>"` lalu strip HTML pakai python (hapus `<script>/<style>` dulu, lalu `<[^>]+>` → spasi, `html.unescape`). Ini lebih andal daripada r.jina.ai ke web.archive.org (yang sering cuma balik 521 byte).

## Foto arsip historis — Wikimedia Commons (Tropenmuseum/KITLV)

> ⚠️ **PITFALL identifikasi lokasi dari foto**: vision model bisa salah-kenal tempat dengan percaya diri tinggi (struktur rel layang merah Simpang Joglo Solo dikira "jembatan LRT Cikunir Bekasi" — halusinasi teks "LRT JABODEBEK"). Selalu anggap hasil vision = HIPOTESIS: cek ciri khas lokal (rambu, nama jalan, bangunan ikonik) dan KONFIRMASI ke user sebelum riset mendalam. Kalau user koreksi lokasi, validasi ulang semua fakta dari awal — jangan pakai data hasil identifikasi yang salah.

Koleksi zaman kolonial Tropenmuseum (Amsterdam) & KITLV (Leiden) di-upload massal ke Commons dengan lisensi CC — sumber foto "tempo dulu" untuk konten sejarah. Teruji sesi Simpang Joglo (foto MN VII, PB X, stasiun NIS, pesawat era kolonial).

```bash
# 1) Cari file (srnamespace=6 = namespace File)
curl -sL "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<query>&srnamespace=6&srlimit=8&format=json"
# Query kuat: "COLLECTIE TROPENMUSEUM <topik>", "KITLV <topik>", ejaan lama Belanda (Soerakarta, Mangkoe Negoro, Pakoe Boewono, spoorweg, vliegtuig)

# 2) UNDUH TANPA API (hindari rate limit!) — pakai Special:FilePath
curl -sL -A "Mozilla/5.0" "https://commons.wikimedia.org/wiki/Special:FilePath/File:<nama_file_urlencoded>" -o out.jpg

# 3) Metadata (tanggal, lisensi, kredit) — SATU panggilan API untuk banyak file (pisah dengan |), sleep 5-8s antar panggilan
curl -sL "https://commons.wikimedia.org/w/api.php?action=query&titles=File:A|File:B|File:C&prop=imageinfo&iiprop=url|size|extmetadata&format=json"
```
- **Rate limit Commons**: respons "You are making too many requests" (plain text, bukan JSON) → sleep 5-8 detik antar request, batch sebanyak mungkin dalam satu query, unduh via Special:FilePath bukan imageinfo url.
- **TIFF besar** (KITLV sering .tiff 30MB) → konversi JPEG: `pip install pillow` lalu `Image.open(...).convert('RGB').thumbnail((1600,1600)).save(...,quality=85)` (ffmpeg juga bisa).
- **VERIFIKASI WAJIB sebelum dikirim**: tiap foto dicek vision_analyze (siapa/pakaian/suasana) supaya keterangan akurat; cek extmetadata (licensi + author) untuk kredit di deskripsi YouTube.
- Foto peristiwa spesifik (mis. "pesawat pertama 1911") sering TIDAK tersedia — pakai foto era terdekat + keterangan jujur "foto asli tidak tersedia, ini visual era yang sama".
   ```bash
   curl -skL -A "Mozilla/5.0" "https://news.google.com/rss/search?q=<query>&hl=id&gl=ID&ceid=ID:id"
   ```
   - Parse `<item>` → `<title>`, `<source>`, `<pubDate>`. Query pakai kata kunci + kutipan (`"Taman Bendung Tirtonadi"`), tambah `(panjang OR meter)` utk cari angka.
   - Link hasil = redirect gnews (`news.google.com/rss/articles/CBMi...`) — **tidak bisa di-resolve curl biasa** (JS). Teruskan ke r.jina.ai (langkah 5).
5. **r.jina.ai reader proxy** — satu-satunya cara baca artikel berita Indonesia yang JS-rendered (Kompas, Espos/Solopos, detik = SPA; curl langsung cuma dapat ~13 char shell):
   ```bash
   curl -skL "https://r.jina.ai/<URL_LENGKAP>"
   ```
   - Balikin Markdown bersih + URL asli + publish time. Browser-based, jadi bisa resolve redirect gnews juga. Gratis tanpa API key (rate-limit).
   - Pitfall: ekstrak angka pakai grep konteks (`meter|hektare|panjang|miliar` + 200-300 char konteks), bukan cari kata kunci tunggal.
6. **Cross-verifikasi angka WAJIB** — angka dari satu artikel jangan langsung dipakai: minimal 2 sumber (contoh: normalisasi Kali Pepe = "1,5 km" Kompas 2018 vs "1.566 meter" Solopos 2020 — cocok, layak dipakai). Kalau beda jauh, tandai ⚠️ dan bilang ke user.
7. **Detik search** — untuk berita lokal Indonesia (Jateng, kota):
   ```bash
   curl -sL -A "Mozilla/5.0 ... Chrome/120.0" "https://www.detik.com/search/searchall?query=<kata+kunci>"
   ```
   - Ambil link artikel: `re.findall(r'href="(https://[^\"]*detik\.com/[^\"]+)"[^>]*>(.*?)</a>', html, re.S)` — filter URL berisi kata kunci.
   - **JANGAN tebak URL artikel** (slug unik; tebakan gagal = artikel lain). Selalu ambil dari hasil search.
   - Body artikel: cari `class="itp_bodycontent">(.*?)<div class="detail_` (fallback `detail__body-text`), strip script/style/tag, unescape, kolaps spasi. Kalau regex body gagal: strip semua tag seluruh halaman, cari titik awal (`txt.find('Kota -')` dll).
5. **Google News RSS** — proxy trending/topik tanpa API key:
   ```bash
   curl -s "https://news.google.com/rss/search?q=QUERY&hl=id-ID&gl=ID&ceid=ID:id"
   ```

## Pitfalls
- Search engine HTML berubah: cek LEN halaman dulu, kalau <2KB = kena blok/captcha, ganti sumber.
- Jangan retry mesin yang sama >2x — loop warning; langsung lompat ke fallback berikutnya.
- Media sosial (X/Twitter, Facebook) umumnya butuh auth/API key (xurl + OAuth, login FB) — jangan buang waktu di-scrape; sebut keterbatasan jujur ke user + tawarkan setup.
- Verifikasi silang klaim kuat (tahun, klaim "pertama/tertua") antar sumber; kalau beda versi (mis. tahun benteng 1745 vs 1755), pakai yang paling banyak sumber & tandai perbedaan.

## Referensi terkait
- `scrape-indonesian-news` — pola scraping portal berita Indonesia (Kompas dll)
- `vlog-sejarah-lokasi` — contoh penerapan: riset sejarah lokasi Solo (episode Manahan, Tirtonadi, Laweyan)
