# Rekap Penjualan Toko dari Catatan Tangan (Handwritten Sales Ledger)

## Overview
Workflow untuk mengekstraksi foto buku kas/catatan harian penjualan manual (tulisan tangan) Toko Bangunan / Usaha (TB.SR) dan menyimpannya secara terstruktur ke Google Sheets master tahunan dengan tab per bulan.

---

## 1. Konfigurasi Master Spreadsheet
- **Asma Berkas**: `rekap penjualan TB.SR tahun 2023`
- **Spreadsheet ID**: `1_a4ddqjobKaZZ0cTGbRHGGi7oWENCZMcMmTmwonmLyM`
- **Tautan**: `https://docs.google.com/spreadsheets/d/1_a4ddqjobKaZZ0cTGbRHGGi7oWENCZMcMmTmwonmLyM/edit`
- **Struktur Tab**: Setiap bulan memiliki tab tersendiri (`Januari`, `Februari`, `Maret`, dst.) dalam satu spreadsheet yang sama.

---

## 2. Struktur Kolom Baku & Rumus

| Kolom | Judul Kolom | Tipe / Formula | Perataan & Format |
|---|---|---|---|
| **A** | `Tanggal` | Teks / Tanggal (`DD/MM/YYYY`) | Rata Tengah (Center) |
| **B** | `Uang di Laci` | Numerik | Rata Kanan, Format `"Rp "#,##0` |
| **C** | `Pendapatan Total` | Numerik | Rata Kanan, Format `"Rp "#,##0` |
| **D** | `Uang Disetor ke Owner` | Formula `=C{row}-B{row}` | Rata Kanan, Format `"Rp "#,##0` |

### Baris Ringkasan (Bawah)
- **Baris `Total`**:
  - Kolom A: `Total` (Bold, Center)
  - Kolom B: `=SUM(B2:B{n})`
  - Kolom C: `=SUM(C2:C{n})`
  - Kolom D: `=SUM(D2:D{n})`
- **Baris `Rata-rata`**:
  - Kolom A: `Rata-rata` (Bold, Center)
  - Kolom B: `=AVERAGE(B2:B{n})`
  - Kolom C: `=AVERAGE(C2:C{n})`
  - Kolom D: `=AVERAGE(D2:D{n})`

---

## 3. Langkah Kerja Otomasi & Script Python

Gunakan library Google API bawaan di `/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts/google_api.py`:

```python
import sys, json
sys.path.insert(0, '/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts')
from google_api import build_service

sheets = build_service('sheets', 'v4')
drive = build_service('drive', 'v3')
sheet_id = '1_a4ddqjobKaZZ0cTGbRHGGi7oWENCZMcMmTmwonmLyM'
month_name = 'Februari'  # sesuaikan nama tab

# 1. Tambah tab baru jika belum ada
meta = sheets.spreadsheets().get(spreadsheetId=sheet_id).execute()
sheet_tab_id = None
for s in meta.get('sheets', []):
    if s['properties']['title'] == month_name:
        sheet_tab_id = s['properties']['sheetId']
        break

if sheet_tab_id is None:
    res = sheets.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={'requests': [{'addSheet': {'properties': {'title': month_name}}}]}
    ).execute()
    sheet_tab_id = res['replies'][0]['addSheet']['properties']['sheetId']

# 2. Susun Data & Formula
headers = ['Tanggal', 'Uang di Laci', 'Pendapatan Total', 'Uang Disetor ke Owner']
# data: list of [tgl, laci, total, f'=C{row}-B{row}']
# total_row: ['Total', f'=SUM(B2:B{n})', f'=SUM(C2:C{n})', f'=SUM(D2:D{n})']
# avg_row: ['Rata-rata', f'=AVERAGE(B2:B{n})', f'=AVERAGE(C2:C{n})', f'=AVERAGE(D2:D{n})']
```

---

## 4. Standar Styling & Formatting Google Sheets

Terapkan `batchUpdate` dengan gaya visual profesional:
1. **Freeze Header**: `frozenRowCount: 1`
2. **Lebar Kolom**:
   - Kolom A: 130 px
   - Kolom B: 150 px
   - Kolom C: 170 px
   - Kolom D: 210 px
3. **Header Styling**:
   - Background Navy (`#1A365D`, RGB: `0.10, 0.21, 0.36`)
   - Teks Putih Bold (`#FFFFFF`), Ukuran 11, Center, Wrap text
   - Border bawah tebal (`SOLID_MEDIUM`)
4. **Number Formatting**:
   - Kolom B, C, D diformat Currency: `"Rp "#,##0`
5. **Baris Ringkasan (Total & Rata-rata)**:
   - Background Soft Gray (`#F1F5F9`, RGB: `0.94, 0.96, 0.98`)
   - Teks Bold
   - Border atas solid medium, border bawah double line pada baris rata-rata/total.
