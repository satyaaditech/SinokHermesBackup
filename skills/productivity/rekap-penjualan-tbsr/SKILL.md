---
name: rekap-penjualan-tbsr
description: Use when processing TB.SR daily sales photos to Sheets.
---

# Rekap Penjualan TB.SR

Workflow to extract handwritten daily sales ledger photos for TB.SR and record them into monthly tabs within the master Google Spreadsheet.

## Master Spreadsheet
- **Spreadsheet Title:** `rekap penjualan TB.SR tahun 2023`
- **Spreadsheet ID:** `1_a4ddqjobKaZZ0cTGbRHGGi7oWENCZMcMmTmwonmLyM`
- **Link:** `https://docs.google.com/spreadsheets/d/1_a4ddqjobKaZZ0cTGbRHGGi7oWENCZMcMmTmwonmLyM/edit`

## Tab Structure
- Each month has its own tab named after the month in Indonesian: `Januari`, `Februari`, `Maret`, `April`, `Mei`, `Juni`, `Juli`, `Agustus`, `September`, `Oktober`, `November`, `Desember`.
- One-sheet master file; never create separate files for new months.

## Column Layout & Schema
1. **Column A (Tanggal):** Date format `DD/MM/YYYY` (Center aligned).
2. **Column B (Uang di Laci):** Cash remaining in drawer (Right aligned, Currency format `Rp #,##0`).
3. **Column C (Pendapatan Total):** Gross daily income (Right aligned, Currency format `Rp #,##0`).
4. **Column D (Uang Disetor ke Owner):** Formula `=C{row}-B{row}` (Right aligned, Currency format `Rp #,##0`).

### Summary Rows
- **Total:** `=SUM(B2:B{n})`, `=SUM(C2:C{n})`, `=SUM(D2:D{n})`
- **Rata-rata:** `=AVERAGE(B2:B{n})`, `=AVERAGE(C2:C{n})`, `=AVERAGE(D2:D{n})`

## Step-by-Step Execution

### 1. Vision Extraction & Math Verification
1. Read the handwritten entries from the image using vision analysis.
2. Ledger formula in handwritten notes: `[Tanggal] : [Uang Laci] - [Pendapatan Total] = Rp [Setor ke Owner]`.
3. Verify each row: `Pendapatan Total - Uang di Laci == Uang Disetor`. Flag any discrepancy if found.

### 2. Google Sheets API Update
Use Python script with Google Workspace API service (`google_api.py`):
1. Check if the tab for the target month exists. If not, create tab with `addSheet` request.
2. Write Header, Data Rows, Total, and Average rows with `valueInputOption="USER_ENTERED"`.
3. Apply styling via `batchUpdate`:
   - Freeze row 1.
   - Header: Dark Navy (`#1A365D`), White Bold text, centered, vertical centered.
   - Column A: Centered.
   - Columns B, C, D: Currency `\"Rp \"#,##0`.
   - Summary rows: Soft blue/gray background (`#F1F5F9`), bold text, solid top border, double bottom border on average row.
   - Table borders: Light gray gridlines.
   - Column widths: A: 130px, B: 150px, C: 170px, D: 210px.

### 3. Response Delivery
- Respond in Basa Jawi Krama Alus.
- Present clean Markdown table with all daily entries.
- Highlight key totals: Total Laci, Total Pendapatan, Total Setor ke Owner, Rata-rata per hari.
- Provide the clickable link to the master Google Sheet.
