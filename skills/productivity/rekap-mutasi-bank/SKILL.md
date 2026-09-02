---
name: rekap-mutasi-bank
description: "Use when user sends bank statement PDFs to recap to Sheets."
version: 1.0.0
author: Sinox
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Bank, Mutasi, BNI, Rekening, PDF, Google Sheets, Google Drive, Finance]
---

# Rekap Mutasi Bank ke Google Sheets

Skill ini digunakan ketika Pak Satya mengirimkan berkas laporan mutasi rekening bank berformat PDF (seperti rekening koran BNI Simpanan CV Sinar Remaja) untuk diarsipkan di Google Drive dan direkap ke dalam master Google Spreadsheet multi-tab.

## Konfigurasi & Handle Tetap

- **Folder Google Drive**: `Laporan Bank`
  - Folder ID: `1maRGm6UcCWxQYygk8WWxH3QcJO-jHMQK`
  - URL: `https://drive.google.com/drive/folders/1maRGm6UcCWxQYygk8WWxH3QcJO-jHMQK`
- **Master Spreadsheet**: `Rekap Simpanan BNI 2022`
  - Spreadsheet ID: `1qYLKwSpFH9iDTEEBpfxhDuGW6JrMHCHn2cNbf7v0iD4`
  - URL: `https://docs.google.com/spreadsheets/d/1qYLKwSpFH9iDTEEBpfxhDuGW6JrMHCHn2cNbf7v0iD4/edit`
  - Sharing Permission: `anyoneWithLink` role `reader` (Viewer only, edit ditutup).

## Format Rekap Standar (5 Kolom Sederhana)

Kolom disesuaikan dengan template ringkas yang diinginkan Pak Satya:

| Kolom | Format | Penjelasan |
|---|---|---|
| **`TANGGAL`** | `DD/MM/YY` | Format tanggal ringkas 2-digit tahun (contoh: `01/02/22`). Rata kiri. |
| **`KETERANGAN`** | Teks | Uraian transaksi lengkap (wrap text, rata kiri). |
| **`DEBET`** | Integer `#,##0` | Nominal pengeluaran. **Wajib diisi `0` jika tidak ada debet** (tidak boleh kosong/blank). |
| **`KREDIT`** | Integer `#,##0` | Nominal penerimaan. **Wajib diisi `0` jika tidak ada kredit** (tidak boleh kosong/blank). |
| **`SALDO`** | Integer `#,##0` | Saldo berjalan (*running balance*) riil rekening. Rata kanan. |

### Aturan Format & Styling Google Sheets:
1. **Header Row (Baris 1)**: Bold, background abu-abu terang (`#F2F2F2`), rata tengah.
2. **Freeze Row**: Baris 1 dibekukan (`frozenRowCount: 1`).
3. **Format Angka**: Pola `#,##0` (pemisah ribuan koma, tanpa angka desimal/sen).
4. **Lebar Kolom Rekomendasi**:
   - TANGGAL: 95 px
   - KETERANGAN: 520 px
   - DEBET: 140 px
   - KREDIT: 140 px
   - SALDO: 150 px
5. **Baris TOTAL**: Baris terbawah berisi `=SUM(C2:C{n})`, `=SUM(D2:D{n})`, dan saldo akhir dengan background lembut dan teks bold.

---

## SOP Pemrosesan Mutasi Baru

Setiap kali menerima berkas PDF mutasi rekening baru:

### Langkah 1: Unggah PDF Asli ke Google Drive
Simpan berkas PDF asli ke folder "Laporan Bank" di Google Drive menggunakan `google_api.py`:
```bash
python3 /home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts/google_api.py drive upload \
  "<path_ke_file_pdf>" \
  --parent 1maRGm6UcCWxQYygk8WWxH3QcJO-jHMQK \
  --name "<nama_file_asli>.pdf"
```

### Langkah 2: Ekstraksi & Rekonsiliasi Data PDF
Gunakan PyMuPDF (`pymupdf`) untuk membaca transaksi rekening koran BNI:
1. **Anchor**: Temukan baris transaksi berdasarkan indikator `D` atau `K` pada koordinat x DB/CR (570-610 pt).
2. **Tanggal & Jam**: Ambil `Posting Date` pada koordinat x (20-125 pt), ubah dari `DD/MM/YYYY HH.MM.SS` menjadi `DD/MM/YY`.
3. **Keterangan Transaksi**:
   - Identifikasi awal baris transaksi berdasarkan pola umum (`TRANSFER DARI`, `TRANSFER KE`, `TRF/PAY/TOP-UP`, `BY TRX`, `BV TRK`, `JASA GIRO`, `PPH`, `BIAYA ADM`).
   - Gabungkan teks uraian multi-baris dan tangani teks *spillover* antar halaman (jika terpotong batas halaman).
4. **Debet / Kredit**:
   - Jika `db_cr == 'D'`: Debet = nominal, Kredit = 0.
   - Jika `db_cr == 'K'`: Debet = 0, Kredit = nominal.
5. **Verifikasi Saldo (Wajib 100% Cocok)**:
   - Hitung beruntun: `Saldo Awal + SUM(Kredit) - SUM(Debet) == Saldo Akhir`.
   - Cocokkan dengan ringkasan mutasi di halaman terakhir PDF (*Total Debet, Total Credit, Ending Balance*).

### Langkah 3: Buat TAB Baru di Master Spreadsheet
1. Cek nama tab baru (misal: `Februari 2022`, `Maret 2022`).
2. Tambahkan tab baru menggunakan Google Sheets API `batchUpdate` -> `addSheet`.
3. Masukkan data ke tab baru tersebut (`A1:E{n}`).
4. Terapkan pemformatan (freeze header, lebar kolom, format angka `#,##0`, borders, dan baris TOTAL).

### Langkah 4: Laporan Hasil ke Pak Satya
Sampaikan ringkasan dalam bahasa Jawa Krama Alus:
- Tautan PDF asli di Drive
- Tautan tab baru di Spreadsheet
- Ringkasan mutasi: Saldo Awal, Total Debet, Total Kredit, Saldo Akhir, dan jumlah transaksi.

## Aturan Khusus Pemrosesan Massal (Batch Processing)
Bila menerima beberapa berkas PDF sekaligus:
- **Jeda Acak (Random Delay)**: Berikan jeda waktu acak antara 1 sampai 3 menit (60 s.d. 180 detik, termasuk detiknya dibuat acak misal 74s, 115s, 153s) sebelum memproses berkas berikutnya (`time.sleep(random.uniform(60, 180))`).
- **Tujuan**: Mencegah terkena batasan kuota / *rate limit* (HTTP 429) pada Google Drive & Sheets API, menjaga kestabilan kunci API, serta membuat pola panggilan lebih aman dan alami.
