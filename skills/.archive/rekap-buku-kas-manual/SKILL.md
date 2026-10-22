---
name: rekap-buku-kas-manual
description: "Use when digitizing handwritten ledgers to Google Sheets."
version: 1.0.0
author: Sinox
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Ledger, BukuTulis, Pinjaman, PRK, Kas, GoogleSheets, Accounting, OCR]
---

# Rekap Kontrol Pinjaman & Kas Buku Tulis Manual ke Google Sheets

Skill ini digunakan saat mendigitasi, mentranskrip, merekonsiliasi, dan mengaudit catatan keuangan fisik dari buku tulis manual (buku folio/kas bergaris tulisan tangan) seperti kontrol pinjaman rekening koran (PRK/baki debet) dan mutasi kas simpanan toko ke dalam Google Spreadsheet multi-tab.

## Konfigurasi & Handle Tetap

- **Folder Google Drive**: `Laporan Bank` (`1Rnsy7DuxI_2jHv2aGeDD-leNmOCBoggK`)
- **OAuth Token**: `/home/satyaaditech/.hermes/google_token.json` (`drive`, `spreadsheets` scopes)
- **Komunikasi**: Basa Jawi Krama Alus santun dan profesional.

---

## ⚠️ Aturan Kerja Utama (Single-Page Progressive Workflow)

1. **KEJUJURAN & VERBATIM 100% (STRICT VERBATIM & NO HALUSINASI)**:
   - **Mboten Pareng Gawe-Gawe / Halusinasi**: Dilarang keras memaksakan atau memodifikasi angka di kolom saldo fisik buku hanya demi mengejar status `MATCH`. Saldo fisik buku wajib mencerminkan 100% goresan tinta asli apa adanya.
   - **Jika Ragu, WAJIB Bertanya**: Jangan menerka-nerka atau memanipulasi angka. Lebih baik terus terang bertanya kepada Pak Satya jika ada tulisan yang buram, tanda coretan, atau angka yang meragukan. Kejujuran adalah nomor satu.
   - **Kolom Kosong Tetap Kosong (Blank Means Blank)**: Jika di kertas buku kas kolom saldo fisik tidak diisi/kosong oleh penulis aslinya, di spreadsheet kolom Saldo Fisik WAJIB dikosongkan (jangan diisi angka rumus atau estimasi). Status ditandai dengan strip (`-`).
   - **Jika Terjadi Selisih Matematis**: Tampilkan apa adanya sebagai `SELISIH` (merah) dan isi nominal pambidang pada **Kolom I (`NOMINAL SELISIH`)**. Jangan takut melaporkan selisih.

2. **STRUKTUR STANDAR 10 KOLOM SPREADSHEET**:
   - **Kolom A**: `TANGGAL` (format DD/MM/YY atau DD-MM-YYYY, rata tengah).
   - **Kolom B**: `NO. REF / BILYET` (rata tengah).
   - **Kolom C**: `KETERANGAN` (rata kiri).
   - **Kolom D**: `PENARIKAN / BUNGA (+)` (format `#,##0`).
   - **Kolom E**: `SETORAN / ANGSURAN (-)` (format `#,##0`).
   - **Kolom F**: `SALDO BAKI DEBET (RUMUS)` (`=F{prev}+D{curr}-E{curr}`).
   - **Kolom G**: `SALDO FISIK BUKU (VERBATIM)` (100% verbatim goresan tinta fisik).
   - **Kolom H**: `STATUS MATCH / SELISIH` (`=IF(ISBLANK(G{row}), "-", IF(F{row}=G{row}, "MATCH", "SELISIH"))`).
   - **Kolom I**: `NOMINAL SELISIH (RUMUS - FISIK)` (`=IF(ISBLANK(G{row}), "-", IF(F{row}=G{row}, "-", F{row}-G{row}))`).
   - **Kolom J**: `BUKTI FOTO FISIK` (`=HYPERLINK("DRIVE_URL", "Foto XX (Buka Bukti)")`).

3. **INTEGRASI BUKTI VISUAL GOOGLE DRIVE (KOLOM J)**:
   - Buat/gunakan subfolder `Foto Bukti Fisik Buku Kas` di dalam folder `Laporan Bank`.
   - Unggah semua foto asli beresolusi tinggi dengan penamaan runtut (`Foto_01_BukuKas_Sep-Okt2022.jpg`, dst.).
   - Set permission share `anyone with link (reader)`.
   - Pasang rumus `=HYPERLINK(url, "Foto XX (Buka Bukti)")` pada Kolom J untuk setiap baris transaksi yang bersumber dari foto tersebut.

4. **STRUKTUR TAB TAHUNAN & PARTITIONING**:
   - Master data dibagi menjadi tab tahunan terpisah (`Rekap 2022`, `Rekap 2023`, `Rekap 2024`, `Rekap 2025`, `Rekap 2026`).
   - Baris pertama setiap tab tahunan berisi `SALDO AWAL` / `Saldo Pindahan Akhir Tahun Sebelumnya`.
   - Baris non-transaksi / memo catatan ditandai dengan formula `(Memo Catatan)` dan status `-`, serta formula baris transaksi berikutnya harus melompati baris memo agar tidak merusak kalkulasi.
   - Header seluruh tab wajib konsisten Navy `#1E3A5F` dengan teks putih tebal. pernah "mengoreksi" saldo fisik agar rumus cocok.

2. **DILARANG PEMROSESAN MASSAL (NO BULK BATCHING)**:
   - Jangan pernah memproses banyak foto halaman buku tulis sekaligus dalam satu kali jalan. OCR tulisan tangan pada kumpulan batch rentan salah membaca nominal/angka (halusinasi angka), yang menyebabkan status `MATCH` palsu atau selisih terselubung.
3. **PROSES SATU PER SATU (PAGE-BY-PAGE MONITORING)**:
   - Proses **satu halaman/foto saja per giliran**.
   - Tampilkan tabel transkrip hasil pembacaan foto secara detail dan jelas di chat Telegram (No, Tanggal, Ref/No. Bilyet, Keterangan/Rekanan, Tarik, Setor, Saldo Tertulis).
   - Berikan kesempatan kepada Pak Satya untuk memonitor dan mengoreksi jika ada salah baca nominal sebelum atau saat dimasukkan ke spreadsheet.
4. **DOUBLE-CHECK KOLOM KODE REF / NO BILYET & KETERANGAN**:
   - Periksa dengan teliti kode bilyet (misal `BRI 930xxx` vs `BRI 30xxx`, `CY xxx`, `TRF OB`, `TUNAI`), jangan hanya fokus pada nominal angka. Kode bilyet dan nama rekanan/keterangan harus verbatim sesuai goresan pena.
5. **KOLOM I: NOMINAL SELISIH (RUMUS - FISIK)**:
   - Wajib sertakan Kolom I (`NOMINAL SELISIH (RUMUS - FISIK)`) di sebelah kolom Status.
   - Rumus Kolom I: `=IF(ISBLANK(G{row}), "-", IF(F{row}=G{row}, "-", F{row}-G{row}))`.
   - Format: `#,##0;(#,##0);"-"` dengan alignment kanan dan bold.
   - Ini memastikan jika ada selisih, berapa selisih persisnya langsung transparan terlihat tanpa harus menghitung manual.
3. **KOLOM SALDO FISIK BUKU WAJIB 100% VERBATIM (GROUND TRUTH REFERENCE)**:
   - Tulisan saldo berjalan di sebelah kanan buku fisik adalah tulisan yang paling jelas dibaca dan menjadi **kunci utama verifikasi**.
   - Kolom `SALDO FISIK BUKU (VERBATIM)` **WAJIB ditulis apa adanya persis sesuai angka yang tercantum di kertas buku baris per baris**.
   - **DILARANG KERAS** menyesuaikan, mengubah, atau menyamakan kolom saldo fisik dengan hasil hitungan kolom sebelumnya.
   - **DILARANG KERAS** memasukkan angka saldo fiktif/halusinasi yang tidak tertulis pada kertas (misal memasukkan angka hasil kurangan kalkulasi padahal tidak ada di buku).
4. **AUDIT TRANSPARAN STATUS MATCH / SELISIH**:
   - Kolom `SALDO BAKI DEBET (RUMUS)` menghitung otomatis: `=F{prev}+D{curr}-E{curr}` (Pinjaman) atau `=F{prev}+D{curr}-E{curr}` (Kas).
   - Kolom status mengevaluasi: `=IF(F{row}=G{row}, "MATCH", "SELISIH")`.
   - Jika perhitungan rumus tidak cocok dengan saldo fisik buku, **BIARKAN DAN HARUS BERTANDA `SELISIH` (Merah)**. Jangan pernah merekayasa saldo fisik agar berstatus MATCH palsu.
5. **INTEGRITAS KELENGKAPAN BARIS (TIDAK BOLEH ADA BARIS TERLEWAT)**:
   - Setiap baris transaksi di buku fisik (termasuk setoran susulan, transaksi ganda pada tanggal yang sama, biaya bunga, meterai, dan pelunasan bertanda khusus) wajib ditulis lengkap per baris tanpa digabung atau dilewati.readsheet.
3. **ANTI-SPIKE KUOTA**:
   - Pemrosesan bertahap satu per satu mencegah lonjakan kuota (*rate-limit spike*) pada vision/LLM Antigravity.

---

## Model Akuntansi & Logika Rumus

Selalu identifikasi model pambidangan buku sebelum menerapkan formula:

1. **Model Pinjaman / Rekening Koran PRK (Baki Debet)**:
   - Saldo mencerminkan pokok hutang/pinjaman bank.
   - Penarikan bilyet giro (`Bp. 058.xxx`), pencairan, bunga, biaya administrasi menambah baki debet (`+`).
   - Setoran tunai/angsuran mengurangi baki debet (`-`).
   - Formula: $\text{Saldo}_{t} = \text{Saldo}_{t-1} + \text{Penarikan/Bunga}_{t} - \text{Setoran}_{t}$
   - Rumus Google Sheets: `=F2+D3-E3`

2. **Model Kas Simpanan / Saldo Giro Positif**:
   - Saldo mencerminkan uang kas toko yang tersedia.
   - Setoran/penerimaan uang menambah saldo kas (`+`).
   - Pengeluaran/pembayaran/tarikan bilyet mengurangi saldo kas (`-`).
   - Formula: $\text{Saldo}_{t} = \text{Saldo}_{t-1} + \text{Setoran}_{t} - \text{Penarikan}_{t}$
   - Rumus Google Sheets: `=F2+E3-D3`

---

## Format Kolom Standar Google Sheets

| Kolom | Header | Format | Penjelasan |
|---|---|---|---|
| **A** | `TANGGAL` | `DD/MM/YY` | Rata tengah. |
| **B** | `NO. REF / BILYET` | Teks | No. Bilyet Giro/Cek/Nota (`Bp. xxx`, `BRI xxx`, `CY xxx`) atau `TUNAI`. Rata tengah. |
| **C** | `KETERANGAN` | Teks | Nama rekanan / keterangan transaksi (`SETOR`, `PINDAH TABUNGAN`, nama toko). Rata kiri. |
| **D** | `PENARIKAN / BUNGA (+)` | `#,##0` | Nominal penarikan / bunga pinjaman. Nilai `0` jika kosong. |
| **E** | `SETORAN / ANGSURAN (-)` | `#,##0` | Nominal setoran / angsuran pinjaman. Nilai `0` jika kosong. |
| **F** | `SALDO BAKI DEBET (RUMUS)` | `#,##0` | Rumus: `=F{row-1}+D{row}-E{row}`. Rata kanan. |
| **G** | `SALDO FISIK BUKU (VERBATIM)` | `#,##0` | Nilai tercatat di buku fisik. 100% verbatim. Jika di kertas kosong, kosongkan (jangan diisi angka gaib). |
| **H** | `STATUS MATCH / SELISIH` | Teks | `=IF(ISBLANK(G{row}), "-", IF(F{row}=G{row}, "MATCH", "SELISIH"))`. Rata tengah, tebal. Hijau jika MATCH, merah jika SELISIH, strip jika kosong. |
| **I** | `NOMINAL SELISIH (RUMUS - FISIK)` | `#,##0;(#,##0);"-"` | `=IF(ISBLANK(G{row}), "-", IF(F{row}=G{row}, "-", F{row}-G{row}))`. Rata kanan, tebal. Menampilkan angka nominal selisih secara transparan. |

---

## Standar Styling & Tab Spreadsheet

- **Tab sheet terpisah per tahun**: `Rekap 2022`, `Rekap 2023`, `Rekap 2024`, `Rekap 2025`, `Rekap 2026`.
- Urutan baris per baris transaksi di setiap tab tahunan harus persis sama dengan urutan fisik buku kas asli.
- Saldo awal baris pertama di setiap tab tahunan mengambil saldo penutup tab tahun sebelumnya (sambungan kontinu).
- **Header Row**: Background Navy Blue (`#1E3A5F`), teks putih, tebal (*bold*), rata tengah, vertikal tengah.
- **Number Formatting**: Format angka ribuan integer `#,##0` pada kolom D, E, F, G, dan format `#,##0;(#,##0);"-"` pada kolom I.
- **Frozen Rows**: Freeze baris 1 (Header).
- **Auto Resize**: Kolom A s/d I disesuaikan lebarnya secara otomatis.
