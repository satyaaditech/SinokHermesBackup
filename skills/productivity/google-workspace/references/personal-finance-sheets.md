# Personal Finance Tracking via Google Sheets + Telegram

Workflow: User manages personal finances through a Google Sheets spreadsheet with COA (Chart of Accounts) structure, interacted with via Telegram.

## Spreadsheet Structure

Typical multi-sheet setup:
1. **COA** — Chart of Accounts (Kode, Nama Akun, Tipe, Kelompok)
2. **Transaksi Harian** — Main input sheet (No, Tanggal, Keterangan, Tipe, Kode COA, Nama Akun, Jumlah, Metode, No Ref, Catatan)
3. **Dashboard** — Auto-calculated summary (formulas)
4. **Laba Rugi** — Income statement per period
5. **Neraca** — Balance sheet
6. **Arus Kas** — Cash flow statement
7. **Buku Besar** — Per-account ledger view

## COA Standard Structure (Indonesian)

| Kode | Tipe | Kelompok |
|------|------|----------|
| 1xxx | Aset | Aset Lancar / Tetap |
| 3xxx | Kewajiban | Jangka Pendek / Panjang |
| 4xxx | Ekuitas | Modal, Prive |
| 5xxx | Pendapatan | Gaji, Sampingan, Investasi |
| 6xxx-7xxx | Beban | Operasional / Lain |

## Telegram Response Format

After adding a transaction, ONLY return the transaction details. NO auto-recap/total/saldo unless user explicitly asks.

```
Transaksi berhasil ditambahkan ✅
📄 Info Faktur:
• No: {no_ref}
• Tanggal: {DD/MM/YYYY}
• Penjual: {vendor}
• Item: {description}
• Total: Rp {amount}
• Status: {LUNAS / BELUM LUNAS}
```

For query responses (e.g. "pengeluaran saya bulan ini"):
```
📅 28-05-2026
💸 ⚡ Bayar listrik — Rp 450.000
💸 🍽️ Beli makan siang — Rp 50.000

📥 🏦 Saldo Awal Modal — Rp 5.000.000
📥 💼 Gaji Bulan Mei — Rp 10.000.000
```

## Key Formulas in Sheets

- Dashboard totals: `SUMIF` / `SUMIFS` on Transaksi Harian sheet
- Laba Rugi: Sum Pendapatan - Sum Beban
- Neraca: Aset = Kewajiban + Ekuitas (balance check)
- Arus Kas: SUM Kas masuk - SUM Kas keluar

## API Commands

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"

# Append transaction
$GAPI sheets append SHEET_ID "'Transaksi Harian'!A:J" --values '[["5","2026-05-30","Beli bensin","Pengeluaran","6100","Beban Transportasi","150000","Cash","STRK-005","Full tank"]]'

# Read COA
$GAPI sheets get SHEET_ID "'COA'!A1:D30"

# Read all transactions
$GAPI sheets get SHEET_ID "'Transaksi Harian'!A1:J100"
```

## User Preferences

- Prefer emoji per transaction type (⚡listrik 🍽️makan 💼gaji 🏦modal 💸keluar 📥masuk)
- Prefer simple bullet lists over ASCII tables in Telegram
- Concise, token-efficient responses
- No auto-recap after adding transactions