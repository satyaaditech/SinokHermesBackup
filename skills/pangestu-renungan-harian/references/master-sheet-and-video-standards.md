# Master Google Sheet & Video Production Standards (V8 Standar Baku)

Dokumen ini mendokumentasikan spesifikasi teknis dan standar operasional untuk integrasi Google Sheet `Master Produksi V8`, standarisasi rendering video vertikal 9:16 sinematik YouTube Shorts, serta standarisasi subtitle dan vokal dual-voice kontemplatif.

---

## 1. Master Google Sheet Produksi (V8 Lean 22-Kolom)

Seluruh aset produksi renungan harian dicatat secara terpusat pada Google Sheet master:
* **Spreadsheet ID**: `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`
* **URL**: `https://docs.google.com/spreadsheets/d/1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0/edit`
* **Tab Resmi**: `Master Produksi V8` *(Catatan: Tab lami 'Rekap Renungan' 12-kolom sampun superseded/ditutup)*

### Skema 22 Kolom Baku (A - V):
1. **No** (A)
2. **Tanggal Rilis WA** (B): `YYYY-MM-DD`
3. **Hari & Pasaran** (C): Contoh `Sabtu Kliwon`
4. **Bulan** (D)
5. **Tema Bulanan** (E)
6. **Tema Mingguan** (F)
7. **Judul Renungan** (G)
8. **Rujukan Kitab** (H): Kode kitab kanonikal + Bab/Pasal
9. **Kutipan Asli** (I): Sabda verbatim 100%
10. **Terjemahan** (J): Terjemahan Indonesia
11. **Pangilon Rasa** (K): 2 paragraf padat (Human Hook + Bedhah Kasunyatan)
12. **Laku Panyiswan** (L): Latihan 30 detik aplikatif
13. **Mutiara Rasa** (M): Aforisme paradoks 1 kalimat
14. **Pertanyaan Refleksi** (N): Sentence case
15. **Status Naskah** (O): `Menunggu ACC Manual Pak Satya` (Draf) -> `ACC` (Disetujui Pak Satya)
16. **Status Audio TTS** (P): `Render` (DILARANG "Selesai Render")
17. **Status Video MP4** (Q): `Rendered` (DILARANG "Selesai Render")
18. **Status Upload YT** (R): `Uploaded` (DILARANG "Uploaded (Public)")
19. **Link YouTube** (S): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://youtu.be/[video_id]`). **DILARANG menggunakan formula `=HYPERLINK`**.
20. **Link Web Pustaka** (T): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://kontemplasi.satyaaditech.web.id/#[slug]`). **DILARANG menggunakan formula `=HYPERLINK`**.
21. **Link Google Docs** (U): Tulis langsung URL mentah lengkap yang dapat diklik (misal: `https://docs.google.com/document/d/[doc_id]/edit`). **DILARANG menggunakan formula `=HYPERLINK`**.
22. **Status Siar WA/TG** (V): `Siap Siar` (sebelum siaran) / `Done` (setelah penyiaran selesai).

---

## 2. Standar Rendering Video & Subtitle (.ass)

* **Format**: Vertikal 9:16 (1080 x 1920 Full HD) Shorts / Reels.
* **Vokal Dual-Voice**: `jv-ID-DimasNeural` (Sabda Jawa) + `id-ID-ArdiNeural` (Narasi refleksi Indonesia) via Edge-TTS lokal.
* **Alignment Subtitle**: `Alignment: 2` (bottom-center) dengan margin vertikal (`MarginV: 90 - 110`).
* **Anti-Emoji di Subtitle**: Hapus seluruh emoji mentah dari naskah `.ass` agar tidak merender kotak rusak (`⧠`).
* **Durasi Rendering**: Selalu verifikasi durasi video cocok dengan durasi master audio via `ffprobe`.

---

## 3. Ketentuan Bahasa Naskah (V8 Monolingual Naskah + Verbatim Sabda)

* Seluruh naskah renungan (Terjemahan, Pangilon Rasa, Laku Panyiswan, Mutiara Rasa, Pertanyaan, Doa Satuhu) **WAJIB 100% BAHASA INDONESIA**.
* HANYA kutipan Sabda asli yang ditulis dalam Basa Jawa kanonikal verbatim 100%.
* Tidak ada lagi produksi versi bahasa terpisah (English/Jawa); ekosistem resmi V8 berfokus pada bahasa Indonesia yang hangat, komunikatif, dan jernih.
