---
name: pangestu-materi-ulasan
description: Use when membuat materi ulasan/khotbah Pangestu (SSJ/SKH).
---

# Materi Ulasan/Khotbah Pangestu

## Referensi & Sumber Kunci
- **Standar Format Tabel Komparasi, Novelties, & Laku Nyata**: Lihat `references/format_komparasi_tabel_dan_novelties.md` berisi aturan baku 4 pilar per novelty (Tabel 2 Kolom, Deep Insight, Laku Padintenan, Sabda Verbatim), serta aturan tegas native table pada HTML dan Google Docs.
- **Korelasi NPD (Narcissistic Personality Disorder) dengan Ajaran SGS**: Lihat `references/npd_vs_sgs.md` berisi detail pemetaan kriteria klinis DSM-5 terhadap konsep *kumingsun* (*lager-zelf* / Pribadi Asor), *watak angen-angen*, spiritual narsisme (SKH Lin 977), serta formulasi terapinya (Panalangsa dan Andhap Asor).
- **Sasangka Jati — Serat Panembah Bab 5 Key Insights**: Lihat `references/panembah_bab5_insights.md` berisi 5 insight mendalam (Eling tanpa ngeling-eling, Pasemon Sang Patih & 7 Kamar Batin, Kuwajiban Lair/Budi Darma minangka Panembah, Wewangian/Aromaterapi vs Sesaji, Sucining Ati vs Sucining Angen-angen).

User (Pak Satya) mendapat tugas mengulas materi Pangestu (mis. Sasangka Jati Serat Panembah Bab 2/3) untuk presentasi 60–90 menit. Standar kualitas (permintaan user, 2026-08-17): deep insight, cross-reference menyambung, mengalir & bernyawa, kata-kata membumi, mudah dipahami, contoh sehari-hari, punya "wow effect" — insight baru yang tak terpikir orang biasa. Simpan di `~/share/materi_khotbah/`; folder Drive 'Materi Olahrasa' (ID 1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U) sebagai Google Doc bila diminta.

## Alur kerja

0. **Kamus Buku Babon & Pustaka Kanonikal (Dilarang Mengarang Nama Baru)**:
   - **SSJ**: *Sasangka Jati* (atau *Serat Sasangka Jati*)
   - **SPRA**: *Sabda Pratama*
   - **SKH**: *Sabda Khusus* (atau *Sasangka Kinelar*)
   - **BRSR**: *Bawa Raos ing Salebeting Raos* (DILARANG: *Sabda-sabda Rasul*)
   - **TKL**: *Taman Kamulyan Langgeng* (DILARANG: *Titihan Kang Linuwih*)
   - **UUJM**: *Ular-ular Juru Mengeti* (DILARANG: *Usul-usuling Jiwa Manungsa*)
   - **WSJ**: *Wahyu Sasangka Jati* (atau *Wadining Suksma Jati*)
   - **ASBS**: *Arsip Sarjana Budi Santosa*
   - **Olah Rasa** & **Ulasan Kang Kelana**au *Sasangka Kinelar*)
   - **BRSR**: *Bawa Raos ing Salebeting Raos* (DILARANG menyebut *Sabda-sabda Rasul*)
   - **TKL**: *Taman Kamulyan Langgeng* (DILARANG mengarang nama *Titihan Kang Linuwih*)
   - **UUJM**: *Ular-ular Juru Mengeti* (DILARANG mengarang nama *Usul-usuling Jiwa Manungsa*)
   - **WSJ**: *Wahyu Sasangka Jati* (atau *Wadining Suksma Jati*)
   - **ASBS**: *Arsip Sarjana Budi Santosa*
   - **Kutipan Verbatim Wajib Utuh/Lengkap**: Dilarang memotong sabda suci menjadi terlalu pendek sehingga merusak konteks pemahaman teologis.

1. **Cadangkan Dokumen Sebelum Overhaul**: Sebelum melakukan perubahan/revisi menyeluruh pada Google Doc atau draf materi yang sudah ada, selalu buat salinan cadangan (*duplicate/backup*) di Drive folder `Materi Olahrasa` (`[BACKUP] ...`) dan salinan `.md` lokal.
2. **Konsistensi Basa Krama Alus, Kutipan Verbatim, & Anti-Cocoklogi**: Seluruh narasi pengantar, penjelasan materi, dan tinjauan filosofis wajib menggunakan Basa Jawi Krama Alus murni (tidak campur ngoko). Kutipan Sabda (SSJ, BRSR, SKH, TKL, UUJM) wajib 100% VERBATIM tanpa diubah. DILARANG membuat asumsi yang menjelekkan agama/ajaran lain (Piwulang Sang Guru Sejati adalah SESULUH dan TEKEN) dan DILARANG memaksakan sabda ke konsep yang tidak cocok (cocoklogi). TKL, UUJM) wajib 100% **VERBATIM** apa adanya tanpa diparafrase.
3. **Cek anti-redundansi dulu**: search_files di `~/share/materi_khotbah/` (mis. pattern `*panembah*`). Kalau topik sudah ada file ulasan, materi baru WAJIB sudut berbeda (deepen), bukan salin. File lama = acuan gaya & daftar sandingan yang sudah dipakai (hindari mengulang verbatim).
2. **Sumber teks**: ekstraksi HTML & katalog slug buku ada di skill `pangestu-buku-studi` (user-owned — baca untuk cara fetch: curl + strip `<article>`). Sumber: `https://satyaaditech.github.io/perpustakaan/book/pangestu/<slug>.html`.
3. **Ekstrak bab persis**: setelah teks penuh ke file, cari judul bab dengan `re.finditer` (mis. `Teges-teges kang Gegandhengan`), potong `txt[start : start + re.search(r'\nBab N\b', txt[start:]).start()]`, simpan `/tmp/<buku>_bab<N>.txt` untuk dibaca bertahap.
4. **⚠️ Terjemahan Indonesia SSJ tidak lengkap**: `ssj_ind.html` berhenti SEBELUM Serat Panembah. Kutipan wajib dari teks Jawa (`ssj.html`) + terjemahan sendiri yang baku dan cermat.
5. **Mining cross-reference**: fetch SEMUA buku kanon (loop curl; **URL pakai double-quote** supaya `${slug}` ke-expand — single-quote menghasilkan file literal `b_${slug}.html`), ekstrak, grep istilah kunci (`panembah|sembah|eling|sasmita|Baitullah|sujud|kandas|...`) dengan context window ±300–700 char. Hanya pakai kutipan yang TERVERIFIKASI dari teks asli — jangan hafalan.
6. **Struktur materi**: tabel rencana menit di bagian atas (0–10 hook pembukaan → tiap adeg/bab → refleksi → penutup); kutipan Jawa + terjemahan inline; cross-ref menyatu inline di tiap bagian; SETIAP bagian langsung disusul aplikasi sehari-hari; sisipkan insight wow (sudut pandang baru, mis. "panembah = kamus sasmita", "teknologi anti-lupa", "miniatur perjalanan hidup").
7. **Simpan & verifikasi**: `~/share/materi_khotbah/ulasan_<topik>_<YYYY-MM-DD>.md`; cek `curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/materi_khotbah/<file>` → harus 200; beri link user `http://192.168.0.112:8000/materi_khotbah/<file>`.
8. Tawarkan upload Google Doc (format asli docs, tanpa markdown) ke folder 'Materi Olahrasa'.

## Pitfall

- Output tool gampang terpotong untuk teks Jawa panjang → print slice 4–6K char per pemanggilan (execute_code) atau baca bertahap (read_file offset).
- Jangan pakai referensi sinkretis (Dalai Lama, Tao, Sufi, Zen) dalam materi Pangestu — jaga kemurnian ajaran; cross-ref hanya dari buku kanon Pangestu.
- Nama bab di TOC vs badan buku bisa beda penulisan — cari judul di badan, bukan hanya TOC.

## Referensi

- `references/ssj-panembah-bab2.md` — kutipan terverifikasi Serat Panembah Bab 2 (Jawa + terjemahan), peta cross-ref (SKH/ASBS/UKK/BRSR/TKL/SPRA), inventaris insight wow, lokasi file hasil.
