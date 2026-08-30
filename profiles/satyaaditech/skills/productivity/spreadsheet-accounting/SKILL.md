---
name: spreadsheet-accounting
description: "Build automated personal/small-business accounting systems in Google Sheets with COA (Chart of Accounts), daily transaction logging, and auto-calculating financial reports (Income Statement, Balance Sheet, Cash Flow)."
version: 1.0.0
author: Satya Adi Dharma (Hermes session)
platforms: [linux, macos, windows]
requires_skills: [google-workspace]
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token from google-workspace setup
trigger: When user wants to track personal finances, build an accounting spreadsheet, create COA, or generate automated financial reports (Laba Rugi, Neraca, Arus Kas) in Google Sheets
---

# Spreadsheet Accounting

Build a complete automated accounting system inside Google Sheets. Designed for personal finance or small business use with Indonesian accounting terminology (Laba Rugi, Neraca, Arus Kas), but easily adapted to any language.

## References

- `references/coa-id-template.md` — Complete Indonesian COA (Chart of Accounts) with 23 standard accounts, codes, and formulas
- `references/sheet-architecture.md` — Multi-sheet architecture and SUMIFS formula patterns

## What This Builds

A 7-sheet Google Spreadsheet:

| Sheet | Purpose |
|-------|---------|
| **Transaksi Harian** | Daily input — date, description, type (Pemasukan/Pengeluaran), COA code, account name, amount, method, ref, notes |
| **COA** | Chart of Accounts — code, name, type, group, opening balance |
| **Dashboard** | Auto summary — total income, total expense, net balance, per-account balances |
| **Laba Rugi** | Income Statement — revenue breakdown, expense breakdown, net profit/loss |
| **Neraca** | Balance Sheet — current assets, fixed assets, liabilities, equity, balance check |
| **Arus Kas** | Cash Flow — opening balance, cash in, cash out, net change, closing balance |
| **Buku Besar** | General Ledger — per-account transaction view using QUERY/FILTER |

## Architecture Pattern

### 1. Single Source of Truth

All data entry happens in **Transaksi Harian**. Every other sheet reads from it via formulas. Never hardcode numbers in report sheets.

### 2. COA Structure (Indonesian Standard)

| Code Range | Category | Examples |
|------------|----------|----------|
| 1xxx | Aset Lancar | Kas, Bank BCA, Bank Mandiri, Piutang |
| 2xxx | Aset Tetap | Peralatan, Kendaraan |
| 3xxx | Kewajiban | Utang Usaha, Utang Bank |
| 4xxx | Ekuitas | Modal, Prive/Penarikan |
| 5xxx | Pendapatan | Gaji, Sampingan, Investasi |
| 6xxx-7xxx | Beban | Makanan, Transportasi, Listrik, Internet, Pendidikan, Kesehatan, Pakaian, Hiburan, Amal, Lain-lain |

### 3. Key Formulas

**Total Pemasukan** (Dashboard):
```
=SUMIF('Transaksi Harian'!D:D,"Pemasukan",'Transaksi Harian'!G:G)
```

**Total per Akun** (Laba Rugi / Neraca):
```
=SUMIFS('Transaksi Harian'!G:G,'Transaksi Harian'!F:F,"Beban Makanan",'Transaksi Harian'!D:D,"Pengeluaran")
```

**Laba/Rugi Bersih** (Laba Rugi):
```
=Total_Pendapatan - Total_Beban
```

**Balance Check** (Neraca):
```
=Total_Aset = (Total_Kewajiban + Total_Ekuitas)
```

**Saldo Akhir Kas** (Arus Kas):
```
=Saldo_Awal + Arus_Masuk - Arus_Keluar
```

## When CLI Wrapper is Limited

The `google_api.py` CLI from `google-workspace` skill supports basic CRUD but may lack features like:
- Multi-sheet creation with formulas
- Batch updates with complex formula injection
- Advanced formatting

**Fallback: Use raw Google Sheets API via HTTP:**

```python
import requests, json, os

# Load token from google-workspace setup
token_path = os.path.expanduser("~/.hermes/google_token.json")
with open(token_path) as f:
    token_data = json.load(f)
access_token = token_data["token"]

headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

# Create spreadsheet
url = "https://sheets.googleapis.com/v4/spreadsheets"
body = {"properties": {"title": "My Accounting"}}
r = requests.post(url, headers=headers, json=body)
spreadsheet_id = r.json()["spreadsheetId"]

# Batch add sheets
batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate"
body = {"requests": [{"addSheet": {"properties": {"title": "COA"}}}]}  # etc
requests.post(batch_url, headers=headers, json=body)

# Write values with formulas
values_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Sheet1!A1:C3?valueInputOption=USER_ENTERED"
body = {"values": [["Header1","Header2","Header3"],["=SUM(A:A)","data","data"]]}
requests.put(values_url, headers=headers, json=body)
```

**Important**: Use `valueInputOption=USER_ENTERED` (not `RAW`) when writing formulas so Google Sheets evaluates them.

## Rules

1. **Always use `USER_ENTERED`** when writing formulas via API. `RAW` treats formulas as plain text.
2. **Never edit report sheets manually** — they are 100% formula-driven from Transaksi Harian.
3. **Keep COA consistent** — if you add a new expense category, add it to COA AND update Laba Rugi / Neraca formulas.
4. **Use ISO dates** in Transaksi Harian (`YYYY-MM-DD`) for reliable sorting and filtering.
5. **Always confirm auth** with `setup.py --check` before any Sheets API operation.

## Extending the System

| Want to add | How |
|-------------|-----|
| New expense category | Add to COA sheet, add row to Laba Rugi with SUMIFS |
| Budget tracking | Add "Budget" column to COA, add variance formula in Dashboard |
| Monthly reports | Duplicate Laba Rugi/Neraca sheets, change formulas to filter by month using `SUMIFS` with date range |
| Multiple bank accounts | Add new COA entries (e.g., 1250 Bank BNI), update Neraca |
| Receivable tracking | Add "Status" column to Transaksi Harian (Lunas/Belum), use FILTER for aging |

## Pitfalls

- **Currency formatting**: Set cell format to Rp currency manually or via API (`userEnteredFormat.numberFormat`). Default is plain number.
- **Formula overflow**: If transaction list grows >1000 rows, use named ranges or query the specific range instead of whole-column references like `A:A`.
- **Sheet name spaces**: In formulas, wrap sheet names with spaces in single quotes: `'Transaksi Harian'!G:G`
- **Timezones**: Calendar events need explicit timezone (`+07:00` for WIB). Sheets store plain dates but may shift if user locale differs.
