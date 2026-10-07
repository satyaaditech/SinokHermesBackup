# Riset Berita/Artikel Indonesia — Fallback Chain Terverifikasi (8 Agu 2026)

Skenario: `web_search`/`web_extract` mati (FIRECRAWL_API_KEY tidak ada), halaman live
diblokir Cloudflare (solopos.com → 403), r.jina.ai gagal di Google (403 abuse) &
Bing (hasil di-hijack jadi job listing Prancis) & Kompas ("halaman tidak ditemukan").

## 1. Google News RSS — PALING ANDAL, coba pertama
```bash
curl -sL --max-time 30 "https://news.google.com/rss/search?q=%22Simpang%20Joglo%22&hl=id&gl=ID&ceid=ID:id" | python3 -c "
import sys,re
t=sys.stdin.read()
items=re.findall(r'<item>(.*?)</item>',t,re.S)
for it in items[:10]:
    ti=re.search(r'<title>(.*?)</title>',it,re.S)
    pu=re.search(r'<pubDate>(.*?)</pubDate>',it,re.S)
    src=re.search(r'<source[^>]*>(.*?)</source>',it,re.S)
    print('-',ti.group(1) if ti else '?')
    print('  ',pu.group(1) if pu else '?','|',src.group(1) if src else '?')
"
```
- Presisi: frasa pakai `%22...%22` (kutip). Tambah `&hl=id&gl=ID&ceid=ID:id`.
- Judul headline + tanggal + sumber cukup untuk fakta inti & penemuan artikel kunci.
- Link `<link>` adalah redirect news.google.com yang TIDAK bisa di-resolve (loop). Cari URL asli via step 2.

## 2. Wayback CDX API — temukan URL asli artikel yang diblokir
```bash
curl -sL --max-time 30 "https://web.archive.org/cdx/search/cdx?url=<domain>&matchType=domain&filter=original:.*<pola>.*&output=text&limit=30&collapse=urlkey&fl=timestamp,original"
```
- `filter=original` pakai regex — wajib `.*` di kedua sisi pola.
- Contoh kerja: `solopos.com` + `.*sejarah-simpang-joglo.*` → snapshot `20240125120633` + URL asli; `solopos.espos.id` + `.*simpang-joglo.*` → banyak snapshot (termasuk "5 Fakta Menarik").
- CDX domain-wide bisa lama/ERR di domain besar (tribunnews.com) — pakai subdomain (solo.tribunnews.com) atau pola lebih spesifik.

## 3. Ambil isi arsip — DIRECT CURL (bukan r.jina.ai)
r.jina.ai pada web.archive.org GAGAL (balas ~521 char). Yang jalan:
```bash
curl -sL --max-time 60 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  "https://web.archive.org/web/<timestamp>/<url-asli>" > /tmp/art.html
python3 << 'EOF'
import re,html
t=open('/tmp/art.html',errors='ignore').read()
t=re.sub(r'<script.*?</script>','',t,flags=re.S)
t=re.sub(r'<style.*?</style>','',t,flags=re.S)
t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t); t=re.sub(r'\s+',' ',t)
print(t)
EOF
```
- Cara cepat: curl langsung halaman live juga oke kalau bukan Cloudflare.

## 4. r.jina.ai — SELEKTIF
- ✅ JALAN: `solo.tribunnews.com` (artikel lengkap ~30-40KB), `hutamakarya.com` (perlu grep keyword di body — banyak menu di awal).
- ❌ GAGAL: Google search (403 AbuseAlleviationError), Bing (hasil hijack), Kompas regional, web.archive.org (521 char), CNBC/detik (hanya logo).
- Parsing tribun: isi di markdown sekitar marker `TRIBUNSOLO.COM, SOLO`; ambil paragraf via regex `\*\*([^*]{150,})\*\*`.

## 5. Fakta historis tetap Wikipedia API (curl) — rute utama
`https://id.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&redirects&titles=<Judul_With_Underscores>`
- Sumber sejarah Indonesia bagus: halaman jalur KA, kelurahan, tokoh (Gibran, Respati Ardi), bandara.

## Prinsip pencatatan sumber
Fakta = judul artikel + isi arsip yang terbaca. Kalau cuma judul yang terlihat (RSS),
catat di daftar sumber sebagai "via Google News RSS (headline)" — jangan dianggap isi penuh.
