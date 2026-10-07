# Berburu Foto Tempo Dulu Lokasi Indonesia (Wikimedia/Tropenmuseum/KITLV)

Workflow terbukti (2026-08, episode vlog Simpang Joglo Solo) untuk mencari foto sejarah lokasi Indonesia sebagai B-roll/galeri. Semua sumber WAJIB dicatat (koleksi + lisensi) untuk kredit.

## Arsip utama & lisensi
- **Wikimedia Commons** — agregator; pakai ini duluan. Kaya arsip **Tropenmuseum** (CC BY-SA 3.0) & **KITLV Leiden** (CC BY 4.0).
- **KITLV/Wereldculturen langsung** (collectie.wereldculturen.nl) — server SERING down; kalau gagal, cari cerminnya di Commons.
- **ANRI** (anri.go.id) — sering kena Cloudflare challenge; jangan buang waktu lama.
- **Internet Archive** — berguna untuk dokumen, jarang untuk foto lokasi spesifik Indonesia.
- **Peta lama**: Geographicus via Commons (Public Domain), e.g. peta aeronautika Jepang 1943 Surakarta (resolusi kecil — referensi saja).

## Kata kunci Belanda (kunci sukses!)
Arsip kolonial pakai ejaan lama; cari dengan beberapa variasi:
- Soerakarta (bukan Surakarta), Solo, Djèbès (Jebres), Goendih (Gundih), Mangkoe Negoro (Mangkunegara), Pakoe Boewono (Pakubuwono), Kassian Céphas.
- Topik: overweg (perlintasan/palang), spoorweg/spoorbrug (rel/jembatan rel), station, verkeersplein (simpang), bestrating (paving), stoomwals (mesin gilas uap).
- NIS = Nederlandsch-Indische Spoorweg Maatschappij — perhatikan ejaan lama **-sch** (Nederlandsch) saat menyalin nama file, bukan -s.

## 1. Cari (API search)
```bash
curl -sL --max-time 30 "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<QUERY>&srnamespace=6&srlimit=8&format=json" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for x in d.get('query',{}).get('search',[]): print('-',x['title'])
"
```
- `srnamespace=6` = hanya File:.
- Coba banyak variasi ejaan (Belanda/Indonesia/Inggris) — tiap query hasil beda.
- Rate limit API ketat (429 "You are making too many requests"): `sleep 4-8` antar panggilan.

## 2. Unduh — GUNAKAN Special:FilePath, BUKAN API
API kena rate limit cepat; `Special:FilePath` langsung serve file:
```bash
URL=$(python3 -c "import urllib.parse; print('https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote('File:<NAMA PERSIS>', safe=''))")
curl -sL --max-time 60 -A "Mozilla/5.0" "$URL" -o out.jpg
```
- Nama file harus PERSIS (salin dari hasil search). Kurung `()`, koma, spasi wajib di-encode — `urllib.parse.quote(..., safe='')`.
- Banyak arsip berupa TIFF besar (30MB+) → konversi JPEG.

## 3. Konversi TIFF→JPG
```bash
pip install pillow   # sekali per env
python3 -c "
from PIL import Image
im=Image.open('x.tiff'); im=im.convert('RGB')
im.thumbnail((1600,1600)); im.save('x.jpg','JPEG',quality=85)"
```

## 4. VERIFIKASI ISI — wajib, jangan percaya nama file
`vision_analyze` tiap foto SEBELUM menulis keterangan: siapa orangnya, pakaian, era, detail. Nama file bisa menyesatkan; vision model bisa salah identifikasi lokasi (kasus nyata: foto jembatan Solo diidentifikasi sebagai LRT Cikunir) — kalau ragu, minta konfirmasi user, jangan klaim.

## 5. Metadata (tanggal, lisensi, kredit) — 1 panggilan API untuk banyak file
```bash
TITLES=$(python3 -c "import urllib.parse; print('|'.join(urllib.parse.quote(t) for t in [...titles...]))")
curl -sL "https://commons.wikimedia.org/w/api.php?action=query&titles=$TITLES&prop=imageinfo&iiprop=url|extmetadata&format=json"
```
Ambil: ImageDescription, DateTimeOriginal, Artist, LicenseShortName. Sertakan di keterangan foto & kredit deskripsi YouTube.

## 6. Kirim galeri → caption NATIVE via Bot API
`MEDIA:/path` di pesan agent mengirim foto TANPA caption menempel (keterangan jadi pesan terpisah — user komplain). Kirim via Bot API:
```bash
curl -s -F "chat_id=$CHAT" -F "message_thread_id=$THREAD" -F "photo=@<file>.jpg" -F "caption=<keterangan>" "https://api.telegram.org/bot${TOKEN}/sendPhoto"
```
Caption ≤1024 karakter; sertakan sumber + lisensi; cek respons `"ok":true`.

## 7. Laporan jujur kalau foto era lama TIDAK ADA
Foto spesifik lokasi kecil (simpang/desa/kampung) era 1980-an/Belanda biasanya TIDAK tersedia di arsip publik online. JANGAN mengarang:
- Cari visual TERDEKAT: kereta era sama, jalan era kolonial, peta lama.
- Sebut arsip fisik yang perlu dikontak (ANRI, KITLV Leiden) atau koleksi pribadi/wartawan senior.
- Gali **ingatan user sendiri** ("dulu cuma ada 1 palang pintu") — itu harta narasi; jadikan cerita di script, bukan gap foto.
