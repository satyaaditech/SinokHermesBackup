# Riset Website/Blog Konten Indonesia (khusus Blogger)

Teknik terverifikasi 2026-08-06 saat riset putunepaktani.com. Tanpa dependency — curl + python3 stdlib.

## Deteksi Blogger
- Endpoint feed ada: `/feeds/posts/default` (Atom) atau `/feeds/posts/default?alt=rss`.
- HTML post pakai `<div class='post-body'>`; footer "Powered by Blogger".
- URL sering ganda (`situs.com` vs `www.situs.com`) — coba dua-duanya kalau 404/redirect aneh.

## 1. Enumerasi SEMUA post via feed JSON (1 request saja)
```bash
curl -sL -A "Mozilla/5.0" "https://www.SITUS.com/feeds/posts/default?alt=json&max-results=150" -o feed.json
```
```python
import json
d = json.load(open('feed.json'))
for e in d['feed']['entry']:
    title = e['title']['$t']
    link = [l['href'] for l in e['link'] if l['rel']=='alternate'][0]
    pub = e['published']['$t'][:10]
    print(f'{pub} | {title} | {link}')
```
- Naikkan `max-results` (150–500) untuk blog besar; feed punya pagination (`openSearch:next`).
- PITFALL: `summary` di feed Blogger SERING KOSONG — jangan andalkan. Fetch halaman post langsung.
- PITFALL: jangan andalkan grep link artikel di homepage — template sering render hanya 1–2 post terbaru.
- PITFALL: regex `<div class='post-body[^>]*>` bisa GAGAL di sebagian artikel/template (class digabung `post-body entry-content`, posisi atribut beda, atau marker post-footer beda). Fallback: `start = h.find("class='post-body entry-content")` lalu potong `h[start:start+N]` sampai marker `post-footer` atau `blog-pager`.
- PITFALL: teks hasil strip HTML sering jadi SATU BARIS super panjang — `read_file` tak berguna (terbaca 1 baris raksasa / total_lines aneh). Baca per-chunk via python: print `t[a:b]` dengan b−a ≈ 6000, naikkan offset bertahap.

## 2. Ekstraksi isi post (curl + python3 stdlib)
```python
import subprocess, re, html
r = subprocess.run(["curl","-sL","-A","Mozilla/5.0","--max-time","30",url],
                   capture_output=True, text=True)
h = r.stdout
m = re.search(r"<div class='post-body[^>]*>(.*?)<div class='post-footer", h, re.S)
body = m.group(1) if m else h
# heading h2/h3 = struktur artikel (daftar isi tersirat) — bagus untuk saring relevansi
heads = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', body, re.S)
heads = [html.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in heads]
# teks bersih
text = re.sub(r'<script.*?</script>',' ',body,flags=re.S)
text = re.sub(r'<[^>]+>',' ',text)
text = html.unescape(re.sub(r'\s+',' ',text)).strip()
```
- Preview cukup `text[:700]` + daftar heading per artikel — tidak perlu full text untuk menyaring.
- Kalau regex `post-body` gagal (template beda): fallback strip semua tag dari HTML utuh.

## 3. Verifikasi & sajian hasil
- Verifikasi klaim kunci (sitasi jurnal, angka) sebelum dipakai jadi materi konten — jangan copas mentah.
- Kategorisasi artikel sesuai kebutuhan user (mis. praktis/cepat panen, DIY murah, sains, komoditas).
- Catat struktur monetisasi blog (e-Book, afiliasi) — sinyal niche yang bisa jadi bahan diskusi/riset lanjutan.

## Contoh terverifikasi: putunepaktani.com
- "Berkebun Organik di Rumah | Tips Tanam Gratis & Mudah" — Blogger, 24 post (Jul–Agu 2026), konten urban farming organik rumahan, gaya sains (sitasi UGM, Netherlands J Agricultural Science, jurnal internasional).
- Kategori: Pupuk/Fungisida/Pestisida/Herbisida/Booster Organik + e-Book.
- Feed: `https://www.putunepaktani.com/feeds/posts/default?alt=json&max-results=150`
- Artikel unggulan (untuk materi urban farming): kangkung ratoon (panen 5x), kucai tumbuh lagi 7 hari, bayam brazil balkon, seledri petik luar, serum LAB komposter bebas bau, companion planting cabai+bawang putih, rizofagi/PGPR, mikoriza-glomalin-wood wide web, biochar charging.
