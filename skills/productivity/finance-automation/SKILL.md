---
name: finance-automation
description: "Auto-classify financial transactions to COA, record to Google Sheets, and store receipts in organized Google Drive folders. Built on Google Workspace."
version: 1.1.0
author: Satya Adi Dharma
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [finance, accounting, COA, transactions, google-sheets, google-drive, automation]
    related_skills: [google-workspace]
---

# Finance Automation

## References
- [Reconciling and Calculating Should-Be Balances](references/reconcile-balance-from-mutasi.md) - Workflow for calculating current balance based on sheets and bank statements.
- [Bank Statement PDF Recap Workflow](references/bank-statement-pdf-recap.md) - Workflow for parsing bank mutasi PDFs, archiving to Drive, and generating formatted Google Sheets.

End-to-end automation for personal/professional bookkeeping: classify transactions using keyword-to-COA mapping, append to Google Sheets, and upload receipt images to matching Google Drive folders. Originally built for Indonesian accounting terminology.

## Triggers

Load this skill when the user mentions any of:
- finance, accounting, bookkeeping, COA, chart of accounts
- transaction, expense, income, receipt, invoice, nota, kuitansi
- pengeluaran, pemasukan, catat transaksi, rekap keuangan
- upload nota, simpan kuitansi, arsip keuangan
- spreadsheet keuangan, laporan laba rugi, neraca, arus kas
- rekap mutasi bank, laporan bank pdf, rekap laporan bank

## User Preferences (CRITICAL — embed in every response)

This user has explicitly demanded minimal, token-efficient responses for finance tasks:

1. **After adding a transaction**: ONLY show the transaction details (No, Tanggal, Penjual/Item, Total, Status). NO auto-recap of totals, NO auto-summary of saldo, NO "Total Pengeluaran", NO "Saldo" 
2. **Calculating Balance from Mutasi**: When asked to calculate from mutasi pictures, default to calculating the net of the visible image entries. Do not mix it with the spreadsheet balance unless explicitly instructed or clarify scope first. unless the user explicitly asks.
2. **Use emoji tags** per transaction type for quick scanning:
   - 📥 / 🏦 = Modal
   - 📥 / 💼 = Gaji
   - 💸 / ⚡ = Listrik & Air
   - 💸 / 🍽️ = Makanan
   - 💸 / ⛽ = Transportasi
   - 🔧 = Peralatan
3. **Only provide data the user asks for.** If they ask "pengeluaran bulan ini", just list expenses. Do NOT append income summary, balance, or comparison unless requested.
4. **Never auto-recap after a single action.** If user says "tambah transaksi X", respond with confirmation of that transaction only. Full recaps are only for explicit requests like "ringkasan" or "rekap".
5. **When asked for lists**: prefer simple key-value or minimal table format. No decorative ASCII borders that break on Telegram mobile.

## Architecture

### Simple Transaction (single item / no receipt)
```
User input (text)
    ↓
Keyword-based COA classifier (deterministic)
    ↓
Append transaction to Google Sheets "Transaksi Harian"
    ↓
Minimal confirmation response (details only, no recap)
```

### Multi-Item Receipt (foto nota dengan banyak item)
```
User input (photo + caption / text list)
    ↓
Extract items, qty, unit price from receipt
    ↓
Append HEADER (total) to "Transaksi Harian"
    ↓
Append ITEMS (per line) to "Detail Item" sheet
    ↓
If photo attached: upload to Google Drive folder matching COA
    ↓
Minimal confirmation response
```

## Assets

- **Spreadsheet**: `13W8pmkqdXwv_Nv4x-reIrw7m0JXOGVWENmXEtgrjG7U` (SINGLE FILE)
  - Sheets: COA, Transaksi Harian, Dashboard, Laba Rugi, Neraca, Arus Kas, Buku Besar
  - "Transaksi Harian" structure: Row 1 = instructions, Row 2 = empty, Row 3 = headers, Row 4+ = data
  - **"Detail Item"** (created 2026-08-12, verified): item-level breakdown for multi-item receipts, columns = `No Ref | Tanggal | Nama Item | Qty | Harga Satuan | Total Item | Kategori Item | Penjual/Lokasi`. Tab did NOT exist initially — first receipt created it via batchUpdate addSheet. Full flow in `scripts/record_multi_item_receipt.py`.
- **Google Drive root**: `1Rnsy7DuxI_2jHv2aGeDD-leNmOCBoggK` (folder `finance/2026/`)
- **Navigator doc**: https://docs.google.com/document/d/1eNOOCM7A7qR8hvQ_AFmAePNij_268b-DrM_YZNJtonA/edit
- **Folder map file**: `~/.hermes/finance_drive_folders.json`

## Scripts

- `scripts/auto_finance.py` — standalone CLI for auto-classify + Sheets append + Drive upload. Run with `--date`, `--desc`, `--amount`, `--method`, and optional `--file`.
- `scripts/record_multi_item_receipt.py` — multi-item receipt recorder: creates "Detail Item" tab if missing, uploads photo to the Drive COA folder (mapped via `~/.hermes/finance_drive_folders.json`), appends header row to Transaksi Harian with No auto-computed, appends per-item rows, verifies. Verified 2026-08-12 (No 47, Pawon Pendopo Manahan).

### Getting the new row "No" after append (PITFALL)

`auto_finance.py` output does NOT include the new row number, but the mandatory confirmation format requires `• No: [nomor faktur]`. After a successful append, fetch column A and compute:

```bash
python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py sheets get "13W8pmkqdXwv_Nv4x-reIrw7m0JXOGVWENmXEtgrjG7U" "'Transaksi Harian'!A:A"
```

Display `No = len(rows) - 2` (rows 1–3 are preamble: instructions, empty, headers; data starts row 4 with No=1). Verified 2026-08-06: len=36 → No 34.

**Better (manual REST appends, verified 2026-08-12):** compute No BEFORE the append as `max(existing numeric A values) + 1` and include it in the appended row's column A. Appending with empty A then backfilling is a wasted second write. If you DO backfill via `PUT .../values/...!A{row}`, the URL MUST carry `?valueInputOption=USER_ENTERED` or you get HTTP 400 `'valueInputOption' is required`. If you read data from `A4` (no preamble) instead of `A1`, `No = row_number - 3`, NOT `len(rows) - 2` — mixing the two bases miscounts.

## References

- `references/coa-keyword-mapping.md` — complete keyword-to-COA mapping table
- `references/user-finance-preferences.md` — condensed user preference rules for finance responses
- `references/session-keyword-additions.md` — running log of COA keyword additions per session
- `references/google-sheets-rest-api.md` — exact REST API pattern for reads/writes from Hermes
- `references/multi-item-receipt-tracking.md` — item-level tracking workflow, sheet schema, and example

## Usage Examples

### From Telegram / chat

User sends:
> "Hari ini beli kopi 30rb pakai cash"

Agent response (minimal):
```
Transaksi berhasil ditambahkan ✅
📄 Info:
• No: 6
• Tanggal: 30/05/2026
• Item: Beli kopi
• Total: Rp 30.000
• Status: Cash
```

User sends photo + caption:
> [foto struk bensin] "Bensin motor 45rb"

Agent response:
```
Transaksi berhasil ditambahkan ✅
📄 Info:
• No: 7
• Tanggal: 30/05/2026
• Item: Bensin motor
• Total: Rp 45.000
• Status: LUNAS
📁 Nota tersimpan di Drive
```

### From terminal

```bash
python ~/.hermes/skills/productivity/finance-automation/scripts/auto_finance.py \
  --date "2026-05-30" \
  --desc "beli kopi" \
  --amount 30000 \
  --method "Cash"
```

With receipt:
```bash
python ~/.hermes/skills/productivity/finance-automation/scripts/auto_finance.py \
  --date "2026-05-30" \
  --desc "bensin motor" \
  --amount 45000 \
  --method "Cash" \
  --file /path/to/nota.jpg
```

## COA Classification Rules

The classifier uses regex patterns on the description (case-insensitive, punctuation ignored). See `references/coa-keyword-mapping.md` for the full table.

Quick reference:
| Keywords | COA Name | Code | Type |
|----------|----------|------|------|
| gaji, salary, payroll | Gaji/Pendapatan Utama | 5000 | Pemasukan |
| sampingan, freelance, jualan | Pendapatan Sampingan | 5100 | Pemasukan |
| investasi, deposito, bunga | Pendapatan Investasi | 5200 | Pemasukan |
| modal, setoran awal | Modal | 4000 | Pemasukan |
| prive, tarik tunai pribadi | Prive/Penarikan | 4100 | Pengeluaran |
| makan, kopi, snack, warteg | Beban Makanan | 6000 | Pengeluaran |
| bensin, parkir, toll, gojek | Beban Transportasi | 6100 | Pengeluaran |
| listrik, pln, air, pam | Beban Listrik & Air | 6200 | Pengeluaran |
| internet, wifi, pulsa, kuota | Beban Internet & Pulsa | 6300 | Pengeluaran |
| kursus, bimbel, buku | Beban Pendidikan | 6400 | Pengeluaran |
| dokter, obat, rs, bpjs | Beban Kesehatan | 6500 | Pengeluaran |
| baju, sepatu, laundry | Beban Pakaian | 6600 | Pengeluaran |
| nonton, netflix, spotify | Beban Hiburan | 6700 | Pengeluaran |
| sedekah, zakat, infaq | Beban Amal/Sedekah | 6800 | Pengeluaran |
| printer, laptop, peralatan | Peralatan | 2000 | Pengeluaran |
| motor, mobil, service | Kendaraan | 2100 | Pengeluaran |
| (fallback) | Beban Lain-lain | 6900 | Pengeluaran |

## Multi-Item Receipts (Item-Level Tracking)

When a receipt contains **multiple different items** (e.g. supermarket shopping, Indomaret, hardware store), the user wants per-item price history tracking. This requires TWO writes:

1. **"Transaksi Harian"** — one row with the **total** amount (financial reporting, COA classification)
2. **"Detail Item"** — one row **per item** with qty and unit price (price tracking, historical queries)

### "Detail Item" Sheet Schema

| Column | Name | Example |
|--------|------|---------|
| A | No Ref | `INV-001` or link to Transaksi Harian `No` |
| B | Tanggal | `01/06/2026` |
| C | Nama Item | `Sabun Lifebuoy` |
| D | Qty | `2` |
| E | Harga Satuan | `12500` |
| F | Total Item | `25000` |
| G | Kategori Item | `Kebutuhan Rumah Tangga` (not COA) |
| H | Penjual / Lokasi | `Indomaret Ngemplak` |

### Workflow

1. User shares receipt photo or lists items
2. Extract each item, qty, and unit price from the receipt
3. Ask user if unclear (blurry photo, missing prices)
4. Append HEADER row to "Transaksi Harian" with total and COA
5. Append ITEM rows to "Detail Item" (same spreadsheet, separate sheet tab)
6. Upload receipt photo to Google Drive COA folder

### Example

User sends:
> [foto nota Indomaret] "Belanja Indomaret 85rb"

Agent extracts:
- Sabun Lifebuoy 2 × Rp 12.500 = Rp 25.000
- Mie Instan 5 × Rp 3.000 = Rp 15.000
- Susu UHT 1L 2 × Rp 22.500 = Rp 45.000

Writes:
- Transaksi Harian: No 23, 01/06/2026, "Belanja Indomaret", Pengeluaran, 6900, Beban Lain-lain, Rp 85.000, QRIS
- Detail Item: 3 rows (one per item above)

### Query Patterns Enabled

With item-level data the agent can answer:
- "Berapa rata-rata harga sabun 3 bulan terakhir?"
- "Harga beras bulan lalu vs sekarang?"
- "Belanja Indomaret paling sering item apa?"

## Auto-Track Workflow (from finance-auto-track)

For single transactions via chat (text or photo):

```
User sends text or photo nota
        ↓
[1] REKAP NOTA → extract: No, Tanggal, Penjual, Item, Total, Status
        ↓
[2] AUTO-KLASIFIKASI COA → match keywords to COA account
        ↓
[3] CATAT KE SPREADSHEET → append row to 'Transaksi Harian'
        ↓
[4] UPLOAD NOTA KE DRIVE → save photo to finance/2026/<COA-folder>/
        ↓
[5] SIMPAN LINK DRIVE → write link to column J (Catatan)
        ↓
[6] KONFIRMASI → reply with Info Faktur format (step 1 data)
```

### Confirmation Output Format (MANDATORY)

After recording a transaction, reply ONLY with this exact format. NO extra lines. NO auto-recap. NO totals/saldo unless user explicitly asks.

```
📄 Info Faktur:
• No: [nomor faktur]
• Tanggal: [DD/MM/YYYY]
• Penjual: [nama penjual/vendor]
• Item: [nama barang/jasa]
• Total: Rp [jumlah]
• Status: [LUNAS / BELUM LUNAS]
```

**CRITICAL:** Never add "Total Pengeluaran", "Total Pemasukan", "Saldo", or any recap below this. If the user wants a summary, they must ask explicitly.

### Column Rules

1. **Column I (No Ref)** = invoice/faktur number only. Never put Drive links here.
2. **Column J (Catatan)** = notes + Google Drive photo links. Always put Drive links here.
3. Use Indonesian accounting terms.
4. Rekap nota first → then ask user "Mau saya catat ke spreadsheet?" → only proceed after user confirms "Iya".

---

## Updating / Correcting a Recorded Transaction

When the user asks to update a transaction already recorded (change penjual, metode, jumlah, deskripsi):

1. **Locate the row** — the sheet has no stable unique ID beyond the display `No`; row index = 3 + No (row 1 = instructions, row 2 = empty, row 3 = headers, row 4 = No 1). Or read the date's rows via `sheets get <ID> "'Transaksi Harian'!A4:J100"` and match the Keterangan.
2. **Update in place** with the `sheets update` subcommand (NOT append — append always creates a new row):
   ```
   python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py sheets update <SPREADSHEET_ID> "'Transaksi Harian'!C36:H36" --values '[["Bensin - POM Bensin Pabelan","Pengeluaran","6100","Beban Transportasi","150000","QRIS"]]'
   ```
   Column map for the update range: A No, B Tanggal, C Keterangan, D Tipe, E Kode COA, F Nama Akun, G Jumlah (Rp), H Metode, I No Ref, J Catatan.
3. **Vendor/penjual has NO dedicated column** — embed it in Keterangan (e.g. `Bensin - POM Bensin Pabelan`, `Makan malam di wedangan KPU`). The Info Faktur confirmation splits Penjual/Item out of Keterangan for display only.
4. **Verify** with a targeted read of the updated row before confirming.

Also after any `auto_finance.py` append: read the appended row (`A<last>:H<last>`) to report the accurate display No — the script returns success but not the No.

**Classifier pitfall**: COA rules match bare substrings. `air` in `perbaikan sumur air di rumah` routes to Beban Listrik & Air (6200) even though it's a repair, not a utility bill. When a description contains ambiguous substrings (air, es, motor, mobil), check which keyword matched before finalizing; ask the user if the COA feels wrong.

---

## Spreadsheet Accounting System (from spreadsheet-accounting)

For users building the spreadsheet from scratch or extending it.

### 7-Sheet Architecture

| Sheet | Purpose |
|-------|---------|
| **Transaksi Harian** | Daily input — date, description, type (Pemasukan/Pengeluaran), COA code, account name, amount, method, ref, notes |
| **COA** | Chart of Accounts — code, name, type, group, opening balance |
| **Dashboard** | Auto summary — total income, total expense, net balance, per-account balances |
| **Laba Rugi** | Income Statement — revenue breakdown, expense breakdown, net profit/loss |
| **Neraca** | Balance Sheet — current assets, fixed assets, liabilities, equity, balance check |
| **Arus Kas** | Cash Flow — opening balance, cash in, cash out, net change, closing balance |
| **Buku Besar** | General Ledger — per-account transaction view using QUERY/FILTER |

### Key Formula Patterns

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

### Extending the System

| Want to add | How |
|-------------|-----|
| New expense category | Add to COA sheet, add row to Laba Rugi with SUMIFS |
| Budget tracking | Add "Budget" column to COA, add variance formula in Dashboard |
| Monthly reports | Duplicate Laba Rugi/Neraca sheets, change formulas to filter by month using `SUMIFS` with date range |
| Multiple bank accounts | Add new COA entries (e.g., 1250 Bank BNI), update Neraca |
| Receivable tracking | Add "Status" column to Transaksi Harian (Lunas/Belum), use FILTER for aging |

### Building from Scratch via API

When the `google_api.py` CLI lacks features like multi-sheet creation or complex formula injection, use raw Google Sheets API:

```python
import requests, json, os

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

# Write values with formulas (USER_ENTERED so Sheets evaluates them)
values_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Sheet1!A1:C3?valueInputOption=USER_ENTERED"
body = {"values": [["Header1","Header2","Header3"],["=SUM(A:A)","data","data"]]}
requests.put(values_url, headers=headers, json=body)
```

**Important**: Use `valueInputOption=USER_ENTERED` (not `RAW`) when writing formulas so Google Sheets evaluates them.

### COA Template

See `references/coa-id-template.md` for the full 23-account Indonesian COA table.

### Sheet Architecture Detail

See `references/sheet-architecture.md` for exact column layouts, formula placements, and QUERY patterns for each sheet.

---

## Pitfalls

1. **DO NOT auto-recap after adding a single transaction.** The user explicitly hates this. Only confirm the specific transaction that was added.
0. **`auto_finance.py` fails on descriptions with apostrophes (`'`).** The `--values` JSON string is shell-quoted with single quotes, so any embedded `'` (e.g. "McDonald's") breaks the command. When the script returns `success: false`, fall back to the direct GAPI `sheets append` call with the same parameters — it handles quoting correctly.
2. **DO NOT show ASCII tables with box-drawing borders on Telegram.** They render poorly on mobile. Use simple bullet lists or minimal pipe-less tables.
3. **COA classification is keyword-based, not semantic.** If the user writes ambiguous descriptions like "transfer 5jt", ask for clarification rather than guessing.
4. **Always check `finance_drive_folders.json` exists** before attempting Drive uploads. If missing, folders must be recreated.
5. **Spreadsheet formulas are fragile.** Appending rows to "Transaksi Harian" must preserve the header and empty row structure. Always append below existing data.
6. **VERIFY data authenticity before reporting.** New spreadsheets or recently set up systems may contain dummy/test data. The user explicitly expects you to ask or check before presenting totals. If the user says "hapus data dummy" or corrects reported figures, immediately inspect the sheet and remove non-real entries.
7. **Google Sheets REST API is the reliable access method from Hermes.** `gspread` is not available in the Hermes sandbox / venv (no `pip`). Use `execute_code` with `requests` + manual OAuth token refresh instead. See `references/google-sheets-rest-api.md` for the exact pattern.
8. **"Transaksi Harian" sheet structure has a preamble.** Row 1 = instructions text, Row 2 = empty, Row 3 = actual column headers (`No`, `Tanggal`, `Keterangan`, `Tipe`, `Kode COA`, `Nama Akun`, `Jumlah (Rp)`, `Metode`, `No Ref`, `Catatan`). Data starts at Row 4. Account for this offset in all reads and writes.
9. **When `auto_finance.py` returns `success: false`**: the `append_to_sheets` subprocess failed. Fall back to direct GAPI append:
   ```
   python <gapi_path> sheets append <sheet_id> "'Transaksi Harian'!A:I" --values '[[<no>,<date>,<desc>,<tipe>,<coa_code>,<coa_name>,<amount>,<method>,"-"]]'
   ```
   Then verify with `sheets get` on the last few rows. Common cause was a broken subprocess invocation in `get_next_row_no()` (fixed 2026-05-26).
10. **Food descriptions may still fall through if keywords are missing.** The Beban Makanan regex has been expanded over multiple sessions (e.g. `bubur`, `soto`, `bakso`, `nasi`, `mie`, `ayam`, `sarapan`, `sop`). If a new food word mis-classifies to "Beban Lain-lain", add it to `COA_RULES` in `scripts/auto_finance.py` and update `references/coa-keyword-mapping.md` immediately — do NOT wait for the user to ask twice.
11. **Electronics and accessories default to "Beban Lain-lain" unless user specifies otherwise.** Items like "casing HP", "charger", "screen protector" are ambiguous between Peralatan (2000) and Beban Lain-lain (6900). The user has explicitly confirmed they prefer such items in Beban Lain-lain. Always ask: "Mau dimasukkan ke Peralatan atau biarkan di Lain-lain?" and honor their choice.
12. **Non-food items also mis-classify when keywords are absent.** E.g. "casing HP iPhone" falls to "Beban Lain-lain" because "casing" is not mapped. Be proactive: when the user tells you what category a mis-classified item belongs to (or you can infer it from context), add the keyword to the mapping right away. See `references/session-keyword-additions.md` for the running list of added keywords per session.
13. **"Detail Item" must be a SHEET (tab) inside the SAME spreadsheet — NOT a separate spreadsheet file.** The user explicitly confirmed this. Do not create a new Google Sheets file. Use `sheets batchUpdate` to add a new sheet tab named "Detail Item" inside `13W8pmkqdXwv_Nv4x-reIrw7m0JXOGVWENmXEtgrjG7U`.
14. **Item-level tracking is ONLY for multi-item receipts.** Simple single-item transactions (e.g. "parkir 2rb", "kopi 30rb") do NOT need a Detail Item entry. Only receipts with 2+ distinct items trigger the dual-write workflow.
15. **When reading a receipt photo, ask for clarification if prices are blurry or ambiguous.** Do NOT guess unit prices. If the photo is unreadable, ask the user to type the item list instead.

## Setup (one-time)

Requires `google-workspace` skill to be authenticated first.

```bash
# Verify auth
python ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check

# Create folder structure
python ~/.hermes/skills/productivity/finance-automation/scripts/auto_finance.py --setup-only
```

## Verification

```bash
# Test classification (dry run)
python ~/.hermes/skills/productivity/finance-automation/scripts/auto_finance.py \
  --desc "beli kopi" --amount 30000 --dry-run

# Test Sheets connectivity
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
$GAPI sheets get 13W8pmkqdXwv_Nv4x-reIrw7m0JXOGVWENmXEtgrjG7U "'Transaksi Harian'!A1:I3"
```
