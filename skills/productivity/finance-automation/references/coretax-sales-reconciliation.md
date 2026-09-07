# Coretax Sales Invoice Reconciliation Workflow

## Overview
Reconciliation workflow for auditing sales invoices against Coretax upload logs (e.g. `2022.xlsx` monthly tabs) to identify un-uploaded or failed transactions, highlight them in spreadsheets, and upload marked copies back to Google Drive.

## Data Sources & Column Mapping
1. **Coretax Upload Log (`2022.xlsx`)**:
   - Organized by monthly tabs (e.g., `Maret`, `April`, etc.). Always restrict matching to the requested month tab.
   - **Column C (Index 2)**: Nomor Faktur Pajak (`010.004-22.xxxxxxxx` / `010.005-22.xxxxxxxx`).
   - **Column O (Index 14)**: Nomor Invoice (`3452203xxx`).
2. **AR Invoice List (`List of AR Invoice <month> <year>.xlsx`)**:
   - Sorted primarily by Faktur Pajak.
   - **Column B (Index 1 / Col 2 in 1-based)**: Invoice No.
   - **Column T (Index 19 / Col 20 in 1-based)**: Faktur Pajak No.
   - Header is typically at row 13; data starts row 15.
3. **Sales Summary Report (`<month> penjualan <month> <year>.xls`)**:
   - Sorted by Invoice No.
   - **Column H (Index 7)**: Invoice No.
   - Header typically at row 21; negative gross amounts indicate sales returns (Credit Notes).

## Matching Rules
- Extract unique Faktur numbers (Column C) and unique Invoice numbers (Column O) from the target Coretax sheet.
- For each transaction in the source sales/AR report:
  - Match via `Invoice No` OR `Faktur Pajak No` against Coretax sets.
  - A transaction is marked **FAILED / MISSING** if neither its Invoice No nor its Faktur Pajak No is found in the Coretax upload sheet.
- Note: Sales returns (negative numbers) might not be uploaded to standard outgoing VAT sheets and should be reported separately.

## Highlighting & Export
- Use `openpyxl.styles.PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")` to highlight the entire row of failed transactions.
- Save marked results with suffix `_Marked_GagalUpload.xlsx`.
- Upload marked files back to the parent Google Drive folder via Google Drive API (`MediaFileUpload`).
