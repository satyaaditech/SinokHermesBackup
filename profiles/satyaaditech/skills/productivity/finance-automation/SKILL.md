---
name: finance-automation
description: "Auto-classify financial transactions to COA, record to Google Sheets, and store receipts in organized Google Drive folders. Built on Google Workspace."
version: 1.0.0
author: Satya Adi Dharma
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [finance, accounting, COA, transactions, google-sheets, google-drive, automation]
    related_skills: [google-workspace]
---

# Finance Automation

End-to-end automation for personal/professional bookkeeping: classify transactions using keyword-to-COA mapping, append to Google Sheets, and upload receipt images to matching Google Drive folders. Originally built for Indonesian accounting terminology.

## Triggers

Load this skill when the user mentions any of:
- finance, accounting, bookkeeping, COA, chart of accounts
- transaction, expense, income, receipt, invoice, nota, kuitansi
- pengeluaran, pemasukan, catat transaksi, rekap keuangan
- upload nota, simpan kuitansi, arsip keuangan
- spreadsheet keuangan, laporan laba rugi, neraca, arus kas

## User Preferences (CRITICAL — embed in every response)

This user has explicitly demanded minimal, token-efficient responses for finance tasks:

1. **After adding a transaction**: ONLY show the transaction details (No, Tanggal, Penjual/Item, Total, Status). NO auto-recap of totals, NO auto-summary of saldo, NO "Total Pengeluaran", NO "Saldo" unless the user explicitly asks.
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

```
User input (text or photo)
    ↓
Keyword-based COA classifier (no LLM needed — deterministic)
    ↓
Append transaction to Google Sheets "Transaksi Harian"
    ↓
If photo attached: upload to Google Drive folder matching COA
    ↓
Minimal confirmation response (details only, no recap)
```

## Assets

- **Spreadsheet**: `13W8pmkqdXwv_Nv4x-reIrw7m0JXOGVWENmXEtgrjG7U`
  - Sheets: COA, Transaksi Harian, Dashboard, Laba Rugi, Neraca, Arus Kas, Buku Besar
- **Google Drive root**: `1Rnsy7DuxI_2jHv2aGeDD-leNmOCBoggK` (folder `finance/2026/`)
- **Navigator doc**: https://docs.google.com/document/d/1eNOOCM7A7qR8hvQ_AFmAePNij_268b-DrM_YZNJtonA/edit
- **Folder map file**: `~/.hermes/finance_drive_folders.json`

## Scripts

- `scripts/auto_finance.py` — standalone CLI for auto-classify + Sheets append + Drive upload. Run with `--date`, `--desc`, `--amount`, `--method`, and optional `--file`.

## References

- `references/coa-keyword-mapping.md` — complete keyword-to-COA mapping table
- `references/user-finance-preferences.md` — condensed user preference rules for finance responses

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

## Pitfalls

1. **DO NOT auto-recap after adding a single transaction.** The user explicitly hates this. Only confirm the specific transaction that was added.
2. **DO NOT show ASCII tables with box-drawing borders on Telegram.** They render poorly on mobile. Use simple bullet lists or minimal pipe-less tables.
3. **COA classification is keyword-based, not semantic.** If the user writes ambiguous descriptions like "transfer 5jt", ask for clarification rather than guessing.
4. **Always check `finance_drive_folders.json` exists** before attempting Drive uploads. If missing, folders must be recreated.
5. **Spreadsheet formulas are fragile.** Appending rows to "Transaksi Harian" must preserve the header and empty row structure. Always append below existing data.

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
