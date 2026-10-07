---
name: photo-document-append
description: "Use when user sends photos to append to one .md file."
version: 1.0.0
author: Sinok (Hermes Agent)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [foto, markdown, document, append, vision]
    related_skills: [health-metrics-logging, google-workspace]
---

# Photo → Markdown Document Append

Class: user sends photos ("baca fotonya, buat dokumen yang terus diupdate") → read each photo, extract info, append a structured entry to a SINGLE persistent .md file. File grows per photo; NEVER create a new file per photo.

## Triggers

- "buat dokumen yang terus diupdate / akan terus ditambah"
- "tiap foto yang kukirim, tambah/append ke file .md yang sama"
- User sends multiple photos over time for one topic (e.g. FGD Sekolah Herbal)

## Format rule (hasil koreksi user)

Ketika user bilang "**satu file saja**" + "dokumen" + foto → DEFAULT ke satu file **.md** dengan append per entri. JANGAN default ke Google Sheet (itu pola tensi/finance, konteks beda). Tanya format hanya kalau benar-benar ambigu; "dokumen foto satu file" = markdown.

## Current instances

- FGD Sekolah Herbal → `/home/satyaaditech/FGD_Sekolah_Herbal.md`

## Steps

1. **Pastikan path file** — buat baru jika belum ada. Struktur awal:
   `# <Judul>` + catatan singkat + marker komentar HTML: `<!-- ENTRI FOTO DI-TAMBAHKAN DI BAWAH GARIS INI -->`
2. **Baca tiap foto** — vision_analyze (atau vision native) → ekstrak SEMUA info: teks, angka, tanggal/jam yang tampak di foto.
3. **Get timestamp via code, never mental** (ZERO TOLERANCE rule): `python3 -c "from datetime import datetime; print(datetime.now().strftime('%Y-%m-%d %H:%M'))"`
4. **Append entri** (bukan overwrite): read file → write_file dengan konten lama + entri baru, atau patch untuk sisip di depan marker. Format entri (H3 per foto) — lihat `templates/photo_entry.md`.
5. **Tetap pakai file yang sama** untuk semua foto berikutnya pada topik itu. Simpan path + topik ke memory biar sesi berikutnya nyambung.
6. **Deliver**: kirim path file + isi LENGKAP .md ke Telegram (user mobile — bukan ringkasan).

## Pitfalls

- Jangan buat Google Sheet untuk "dokumen foto satu file" — user memilih .md (terkoreksi sesi FGD).
- Jika salah buat artefak (spreadsheet dkk.), bersihkan: `python3 <skill google-workspace>/google_api.py drive delete <fileId>` (masuk trash, bukan permanen).
- Jangan buat file baru per foto; jangan tanya ulang format yang sudah dikoreksi.
