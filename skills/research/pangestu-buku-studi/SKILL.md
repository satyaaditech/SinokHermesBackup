---
name: pangestu-buku-studi
description: Use when studying Pangestu books from Satya's SNB Elibrary.
---

# Studi Buku Pangestu (SNB Elibrary)

User (Satya Adi Dharma) sedang digitalisasi & mempelajari pustaka Paguyuban Ngesti Tunggal (Pangestu). Buku-buku ditaruh di GitHub Pages pribadi. Tugas recurring: baca buku, pahami ajaran, buat catatan studi + ringkasan untuk konten (thread TG 1096 Pangestu).

## Sumber

- Indeks perpustakaan: `https://satyaaditech.github.io/perpustakaan/`
- Semua buku di bawah: `https://satyaaditech.github.io/perpustakaan/book/pangestu/<slug>.html`

## Katalog buku (slug → judul)

| Slug | Judul |
|---|---|
| spra.html | SABDA PRATAMA (IND) |
| spra_jawa.html | SABDA PRATAMA (JAWA) |
| ssj.html | SASANGKA JATI (JAWA) |
| ssj_ind.html | SASANGKA JATI (INDONESIA) |
| skh.html | SABDA KHUSUS (BHS.INDONESIA) |
| brsr.html | BAWA RAOS ING SALEBETING RAOS |
| asbs.html | ARSIP SARJANA BUDI SANTOSA |
| olahrasa.html | OLAHRASA |
| ukk.html | ULASAN KANG KELANA |
| tkl.html | TAMAN KAMULYAN LANGGENG |
| wsj.html | WAHYU SASANGKA JATI |
| uujm.html | ULAR-ULAR JURU MENGETI |

Cek selalu indeks untuk katalog terbaru (bisa bertambah).

## Ekstraksi teks (Sphinx/Jupyter Book HTML)

```bash
curl -sL -A "Mozilla/5.0" "<url>" -o /tmp/buku.html
```
```python
import re, html
t = open('/tmp/buku.html', encoding='utf-8').read()
m = re.search(r'<article[^>]*>(.*?)</article>', t, re.S)
body = m.group(1) if m else t
body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
body = re.sub(r'<[^>]+>', '\n', body)
body = html.unescape(body)
lines = [l.strip() for l in body.splitlines() if l.strip()]
text = '\n'.join(lines)
open('/tmp/buku.txt','w').write(text)
print(len(text))
```
Catatan: 20-30 baris pertama = menu/nav (SNB Elibrary, KOLEKSI BUKU, dll). Isi dimulai setelah blok "This Book is Still Under Heavy Development" (jika ada). Cari penanda khas isi (mis. tanggal Jawa/hari) untuk menemukan awal konten.

## Delegasi untuk buku tebal (pelajaran penting)

Saat buku >100K chars, jangan baca semua di parent context. Delegasikan tapi dengan aturan:
1. **Rentang kecil**: maks ~200 baris / ~25K chars per subagent (500 baris = timeout).
2. **Instruksi eksplisit**: HANYA read_file — JANGAN terminal/execute_code (butuh approval → hang).
3. **Peringatkan truncation**: read_file menampilkan ~8-12 baris/panggilan jika baris panjang; strategi: offset = baris terakhir tampil + 1, baca berlapis.
4. **Minta tulis ke /tmp/<nama>.md** via write_file, lalu parent verifikasi kutipan dengan grep + susun file final.
5. Maks 3 subagent paralel (konfigurasi); pakai 2 gelombang jika perlu.
6. Kutipan subagent bisa salah gabung antar baris — selalu verifikasi ke naskah sumber.

## Format catatan studi (wajib, simpan ke ~/share/pangestu_studi/bukuN_<slug>.md)

Folder utama: `~/share/pangestu_studi/` (disajikan HTTP :8000, jangan taruh di tempat lain).
Konvensi penamaan: `00_riset_organisasi.md` (dossier), `buku1_sabda_pratama.md`, `buku2_sasangka_jati.md` (ringkasan gabungan), per-kitab: `buku2_kitabN_<nama>.md`. README.md = index & progres — UPDATE setiap selesai buku/kitab.

Struktur isi tiap file:
1. INTISARI BUKU (2-4 kalimat)
2. KERANGKA ISI (bagian per bagian, kutip sabda penting verbatim)
3. POKOK AJARAN YANG DAPAT DIAMBIL (untuk renungan/konten — bullet)
4. ISTILAH KUNCI (glosarium istilah Jawa/Pangestu)
5. CATATAN KRONOLOGI (tanggal penting, termasuk kalender Jawa jika ada)

Untuk buku tebal (mis. Sasangka Jati IND ~148K chars / 516 baris): bagi per kitab dan kerjakan paralel via delegate_task (subagent membaca rentang baris file /tmp/ssj_ind.txt, menulis /tmp/studi_X.md, lalu saya verifikasi kutipan dgn grep sebelum dipindah ke folder).

Setelah file: kirim ringkasan LENGKAP ke Telegram (preferensi user: konten lengkap, bukan ringkasan tipis) + link IP langsung `http://192.168.0.112:8000/pangestu_studi/<file>` (LAN) / `http://100.92.237.45:8000/...` (Tailscale). JANGAN pakai MagicDNS n8nserver.tailf595e8.ts.net (user tolak).

## Konteks ajaran (untuk pemahaman)

- Sang Guru Sejati = Suksma Sejati, Utusan Tuhan abadi; Suksma Kawekas = Tuhan Sejati (Allah Ta'ala); Tripurusa = keadaan satu bersifat tiga (Suksma Kawekas, Suksma Sejati, Roh Suci)
- Kitab utama: Sasangka Djati (sabda 1932-33); Sabda Khusus (1949-61); Sabda Pratama = catatan peristiwa wahyu pertama 14 Feb 1932, ditandatangani Soenarto 14 Feb 1957
- Term: Pepadang (terang), Tuntunan, Jalan Rahayu, panembah/pameleng (hening), alam luyut (tenang)
- Kronologi kunci: 14 Feb 1932 wahyu pertama (Widuran Solo); 19/20 Mei 1932 Hardjoprakoso datang; 27/28 Mei 1932 Soemodihardjo datang → mulai pencatatan Sasangka Djati
- Riset latar organisasi: lihat ~/share/pangestu_riset.md (dossier lengkap)

## Pitfall

- Halaman SPA resmi pangestu.or.id butuh r.jina.ai (render JS); GitHub Pages ini statis, curl langsung cukup
- Web search tools kadang nonaktif → pakai skill web-research-fallback (Wikipedia API, Brave, DDG via r.jina.ai)
- Naskah digitalisasi masih "Under Heavy Development" → typo mungkin ada; jangan koreksi isi ajaran, hanya catat
