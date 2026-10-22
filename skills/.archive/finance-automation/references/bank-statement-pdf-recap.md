# Bank Statement PDF Recap Workflow

## Overview
Workflow for processing bank statement PDFs (mutasi rekening), archiving original PDFs to Google Drive, parsing all transactions with 100% mathematical precision, and recording into a master Google Spreadsheet with monthly tabs.

## Google Drive Target & Hierarchy
- Dedicated folder: **Laporan Bank** (Folder ID: `1maRGm6UcCWxQYygk8WWxH3QcJO-jHMQK`)
- Always copy/upload the received PDF to this folder first before extraction.
- **Single Master Spreadsheet per Year/Account**:
  - Name: `Rekap Simpanan BNI 2022` (Spreadsheet ID: `1qYLKwSpFH9iDTEEBpfxhDuGW6JrMHCHn2cNbf7v0iD4`)
  - Each month is recorded as a dedicated **TAB / Sheet** inside this master spreadsheet (e.g. `Januari 2022`, `Februari 2022`).
  - DO NOT create a new spreadsheet file for each month. Add a new tab to the existing master spreadsheet.
- **Sharing Permissions**:
  - Set public view-only access:
    ```bash
    python3 ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py drive share --role reader --type anyone <SPREADSHEET_ID>
    ```

## Simplified Table Format (5 Columns)
User explicitly standardizes on a clean 5-column layout (per image reference):

| Column | Name | Format & Alignment | Rule |
|---|---|---|---|
| A | `TANGGAL` | `DD/MM/YY` (e.g. `04/01/22`), Left-aligned | Date only, strip time |
| B | `KETERANGAN` | Text, Left-aligned, Wrap text | Full clean transaction description |
| C | `DEBET` | Integer `#,##0`, Right-aligned | If no debit, fill with `0` (do NOT leave blank) |
| D | `KREDIT` | Integer `#,##0`, Right-aligned | If no credit, fill with `0` (do NOT leave blank) |
| E | `SALDO` | Integer `#,##0`, Right-aligned | Running balance after transaction |

### Formatting Guidelines:
- Row 1: Headers (`TANGGAL`, `KETERANGAN`, `DEBET`, `KREDIT`, `SALDO`), gray background (`#f2f2f2`), bold, centered.
- Freeze row 1 (`frozenRowCount: 1`).
- Numbers: Integer format `#,##0` without `.00` decimals, comma thousand separator.
- Zero values: Must be explicitly written as `0`, not blank.
- Bottom Row: Summary row `TOTAL` with `=SUM(...)` for Debet & Kredit, and final ending balance.

## PDF Extraction Architecture (BNI / Corporate Statements)

### 1. Anchor Baselines
In BNI statements, the following fields share the exact same vertical baseline ($y_0$):
- **Posting Date** ($x \approx 20\dots120$)
- **Effective Date** ($x \approx 125\dots230$)
- **Journal Number** ($x \approx 295\dots335$)
- **Amount** ($x \approx 500\dots580$)
- **DB/CR Indicator** ($x \approx 570\dots610$): `D` or `K`
- **Balance** ($x \approx 615\dots720$)

Use `s['text'] in ('D', 'K')` within $x \in [570, 610]$ as the primary row anchor.

### 2. Multi-Line & Page-Spillover Handling
The only two columns that span multiple lines are:
1. **Branch** ($x \in [230, 295]$): Multi-line (e.g. `DIVISI TRANSACTIONAL BANKING SERVICES (TBS)`), centered around the anchor $y$.
2. **Transaction Description** ($x \in [335, 500]$): Can span multiple lines and frequently crosses page breaks.

**Critical Pattern for Descriptions**:
Every transaction description begins with a known prefix:
- `TRANSFER DARI`
- `TRANSFER KE`
- `TRF/PAY/TOP-UP`
- `BY TRX`
- `BV TRK`
- `JASA GIRO`
- `PPH`
- `BIAYA ADM`

Any description lines appearing at the top of a page (before the first transaction description start pattern) belong to the **last transaction of the previous page**.

### 3. Verification Protocol
Always verify before writing to Sheets:
1. `count(D)` and `count(K)` match statement footer.
2. `sum(D)` and `sum(K)` match statement footer to the exact rupiah.
3. Balance check: `saldo_awal + sum(K) - sum(D) == ending_balance`.
