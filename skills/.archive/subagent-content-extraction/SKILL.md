---
name: subagent-content-extraction
description: Use when delegating doc reading/extraction to subagents.
---

# Subagent Content Extraction & Verification

Delegasi paralel untuk membaca/mengekstrak/meringkas dokumen besar via `delegate_task`, dengan verifikasi WAJIB atas output subagent (kutipan bisa dikarang — self-report bukan fakta).

## Trigger
- Dokumen/buku besar perlu dipelajari atau diringkas (100K+ karakter, mis. kitab, arsip, riset)
- Banyak bagian independen yang bisa diparalelkan
- Output berupa kutipan/fakta yang harus akurat untuk konten lanjutan

## Recipe
1. **Ekstrak teks dulu ke /tmp/<doc>.txt** (curl + python hapus tag HTML; untuk Sphinx/Jupyter Book: ambil blok `<article>`, buang `<script>/<style>`, ganti tag → newline, unescape HTML)
2. **Petakan batas bagian**: `grep -n` judul/header tiap bagian → dapatkan nomor baris
3. **Dispatch delegate_task batch** (maks 3 paralel; jangan nested). Tiap subagent dapat: path file, rentang baris, template output, aturan tegas
4. **VERIFIKASI sebelum percaya** (script di bawah) — baru kemudian simpan ke folder final
5. Jika ada subagent gagal → kerjakan bagian itu sendiri, jangan retry berulang

## Aturan instruksi subagent (WAJIB — kegagalan terbukti di lapangan)
- **GUNAKAN HANYA `read_file` + `write_file`** (dari hermes_tools)
- **JANGAN terminal/sed/curl/grep** — subagent TIDAK bisa mendapat persetujuan terminal interaktif; perintah yang memicu 'Command required approval' menggantung sampai timeout 600 dtk (terjadi: 1 dari 3 subagent gagal padahal subagent lain yang hanya pakai read_file/write_file sukses)
- Suruh tulis output ke `/tmp/<hasil>.md`, lalu balas dengan: path + jumlah karakter + daftar 5 kutipan terpenting BESERTA nomor barisnya di sumber
- Untuk kutipan: WAJIB verbatim persis dari file — dilarang parafrase/mengubah/menambah kata; dilarang menambah interpretasi/pengetahuan luar

## Verifikasi kutipan (anti-halusinasi)
Script ini membandingkan blok kutipan (`> ...`) di catatan studi vs sumber, dengan normalisasi spasi. Simpan sebagai `scripts/verify_quotes.py`:

```python
#!/usr/bin/env python3
"""Verifikasi blok kutipan catatan vs sumber. Usage: python3 verify_quotes.py <source.txt> <study_note.md>"""
import re, sys

def norm(s): return re.sub(r'\s+', ' ', s).strip()

src = norm(open(sys.argv[1], encoding='utf-8').read())
note = open(sys.argv[2], encoding='utf-8').read()

# blok kutipan = baris berawalan '>' (gabungkan baris '>' berurutan menjadi satu blok)
blocks, cur = [], []
for line in note.splitlines():
    m = re.match(r'^\s*>\s?(.*)$', line)
    if m: cur.append(m.group(1).strip())
    elif cur: blocks.append(' '.join(cur)); cur = []
if cur: blocks.append(' '.join(cur))

ok = bad = 0
for b in blocks:
    nb = norm(b)
    if len(nb) < 15: continue
    if nb in src: ok += 1
    else: bad += 1; print('MISMATCH:', nb[:140])
print(f'{sys.argv[2]}: {ok} cocok, {bad} tidak cocok')
```

Catatan penting:
- Kutipan yang **membentang antar-baris di sumber** akan GAGAL match naif → normalisasi spasi adalah wajib, bukan opsional
- Cek silang nomor baris yang dilaporkan subagent (grep kata kunci kutipan di sumber)
- Mismatch bisa berarti subagent mengarang ATAU hanya beda pemenggalan baris — cek konteks sumber sebelum menuduh

## Pitfall
- 1 dari N subagent bisa gagal (timeout approval) → jangan blokir seluruh alur; sisa bagian dikerjakan manual
- Subagent yang melaporkan "selesai" pun bisa salah kutip → verifikasi SELALU, tanpa kecuali
- Jangan langsung memindahkan file subagent ke folder final sebelum verifikasi
- Delegasi `delegate_task` jalan di background; hasil masuk sebagai pesan baru saat SEMUA selesai — jangan polling
- Skill terkait: `pangestu-buku-studi` (pakai recipe ini untuk buku Pangestu; catatan studi disimpan di ~/share/pangestu_studi/)
