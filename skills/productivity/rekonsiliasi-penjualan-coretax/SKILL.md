---
name: rekonsiliasi-penjualan-coretax
description: "Use when rekonsiliasi data penjualan vs upload Coretax."
---

# Rekonsiliasi Data Penjualan vs Coretax

Alur kerja otomatis untuk mencocokkan data transaksi penjualan harian/bulanan (dari laporan internal SAP/ERP/distributor seperti `List of AR Invoice` dan `03 penjualan`) dengan data hasil upload Faktur Pajak Keluaran pada **Coretax** (`2022.xlsx`), mengidentifikasi transaksi yang gagal terupload, menandai baris dengan highlight merah, serta membuat tab ringkasan eksekutif secara detail.

---

## 1. Struktur Sumber Data & Lokasi

1. **Folder Google Drive:** `Data KAO 2022` (ID: `1tx0V-tpxHBdoIAKfItRTJL_3DvQ7gFJH`)
2. **File Coretax (`2022.xlsx`):**
   - Berisi hasil upload faktur pajak per tab/sheet bulanan (`Maret`, `April`, `Mei`, dst.).
   - **Kolom C (Index 2):** Nomor Faktur Pajak (contoh: `010.004-22.41596359`).
   - **Kolom O (Index 14):** Nomor Invoice Penjualan (contoh: `3452203234`).
3. **File Penjualan Internal:**
   - **`List of AR Invoice <bulan> <tahun>.xlsx`:** Diurutkan berdasarkan No Faktur Pajak. Berisi No Invoice (Kolom B/2), Customer (Kolom E/5), Total (Kolom H/8), Faktur Pajak No (Kolom T/20).
   - **`03 penjualan <bulan> <tahun>.xls`:** Diurutkan berdasarkan No Invoice. Berisi Customer Code, Name, Salesman, Whs, Date, Invoice No, Gross, Discount, Net/DPP, VAT/PPN, Total Amount.

---

## 2. Alur Kerja (Standard Operating Procedure)

### Langkah 1: Ekstraksi Data Coretax (Bulan Tertentu Saja)
Baca hanya tab bulan yang diminta (misal `Maret`). Simpan set `coretax_faktur` dan `coretax_invoices`.

### Langkah 2: Dual-Key Matching (Pencocokan Dua Kunci)
Untuk setiap transaksi di file penjualan:
1. Cocokkan `Invoice No` ke `coretax_invoices`.
2. Jika tidak cocok, lakukan cross-reference dengan `Faktur Pajak No` ke `coretax_faktur`.
3. Transaksi dinyatakan **SUKSES** jika salah satu cocok. Transaksi dinyatakan **GAGAL UPLOAD** jika kedua kunci tidak ditemukan.

### Langkah 3: Pemisahan Invoice Reguler vs Retur
- **Invoice Reguler (Gross > 0):** Transaksi penjualan murni yang wajib memiliki faktur pajak keluaran.
- **Retur Penjualan (Gross < 0):** Nota retur yang terpisah dari faktur pajak keluaran reguler.

### Langkah 4: Highlight & Pembuatan Tab Ringkasan
1. Berikan highlight merah muda (`PatternFill(start_color="FFCCCC", fill_type="solid")`) pada baris-baris data transaksi gagal upload.
2. Buat tab baru di urutan pertama bernama **`Ringkasan Gagal Upload`** yang berisi:
   - **Header & Judul Laporan**
   - **Kartu KPI Ringkasan Eksekutif** (Total Transaksi, Total Sukses, Total Gagal, Total Nilai DPP/PPN/Nominal).
   - **Bagian 1:** Tabel Daftar Invoice Reguler Gagal Upload (No, Tgl, Inv, FP, Cust, Salesman, Whs, Gross, Disc, DPP, PPN, Total).
   - **Bagian 2:** Tabel Daftar Retur Penjualan (jika ada).
   - **Baris Total dengan Formula Excel** (`=SUM(...)`).
3. Simpan dan unggah kembali file bertanda `_Marked_GagalUpload.xlsx` ke Google Drive.

---

## 3. Script Python Acuan

```python
import os, openpyxl, xlrd
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load Coretax Tab Bulan
wb_coretax = openpyxl.load_workbook("2022.xlsx", data_only=True)
ws_coretax = wb_coretax["Maret"]

coretax_faktur = set()
coretax_invoices = set()

for row in ws_coretax.iter_rows(values_only=True):
    faktur = str(row[2]).strip() if len(row) > 2 and row[2] else None
    inv = row[14] if len(row) > 14 and row[14] else None
    if faktur: coretax_faktur.add(faktur)
    if inv:
        try: coretax_invoices.add(str(int(float(inv))))
        except: coretax_invoices.add(str(inv).strip())
```

---

## 4. Pitfalls & Hal Penting yang Harus Diperhatikan

1. **Hanya Cek Tab Bulan yang Relevan:** Jangan mencampuradukkan data Coretax lintas bulan kecuali diminta eksplisit.
2. **Filter Subtotal & Header:** Pada file AR Invoice, abaikan baris yang bukan transaksi (seperti string `Subtotal Date ...` atau header salesman) dengan memvalidasi panjang dan format angka invoice.
3. **Penyelarasan Format Angka Invoice:** Angka invoice bisa bertipe string atau float (misal `3.452203e+09`). Selalu konversi melalui `str(int(float(val)))`.
4. **Formula Excel Otomatis:** Baris total wajib menggunakan formula Excel asli (`=SUM(...)`) agar dinamis dan dapat diaudit oleh pengguna.
