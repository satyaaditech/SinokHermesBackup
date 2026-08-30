# Multi-Sheet Accounting Architecture

This describes the exact sheet structure, column layout, and formula patterns used in the automated accounting spreadsheet.

## Sheet 1: Transaksi Harian

**Columns (A-J):**

| Col | Header | Example | Notes |
|-----|--------|---------|-------|
| A | No | 1, 2, 3... | Sequential |
| B | Tanggal | 2026-05-28 | ISO 8601 for reliable sorting |
| C | Keterangan | Beli makan siang | Free text |
| D | Tipe | Pemasukan / Pengeluaran | Must be exact; used in SUMIF |
| E | Kode COA | 6000 | Must match COA column A |
| F | Nama Akun | Beban Makanan | Must match COA column B |
| G | Jumlah (Rp) | 50000 | Plain number, format as currency |
| H | Metode | Cash / Transfer | For cash flow tracking |
| I | No Ref | Struk-001 | Invoice/receipt number |
| J | Catatan | Makan di luar | Free text |

**Row 1**: Instruction text (merged or A1)
**Row 2**: Blank
**Row 3**: Headers
**Row 4+**: Data

## Sheet 2: COA

**Columns (A-E):**

| Col | Header | Content |
|-----|--------|---------|
| A | Kode | 1000, 1100, ... |
| B | Nama Akun | Kas, Bank BCA, ... |
| C | Tipe | Aset / Kewajiban / Ekuitas / Pendapatan / Beban |
| D | Kelompok | Aset Lancar / Aset Tetap / ... |
| E | Saldo Awal | Numeric opening balance |

## Sheet 3: Dashboard

Key formulas (adjust ranges as transaction list grows):

```
A1: "DASHBOARD KEUANGAN"
A2: "Periode:"     B2: =TEXT(TODAY(),"MMM YYYY")
A4: "RINGKASAN"
A5: "Total Pemasukan"     B5: =SUMIF('Transaksi Harian'!D:D,"Pemasukan",'Transaksi Harian'!G:G)
A6: "Total Pengeluaran"   B6: =SUMIF('Transaksi Harian'!D:D,"Pengeluaran",'Transaksi Harian'!G:G)
A7: "Saldo"               B7: =B5-B6
```

## Sheet 4: Laba Rugi (Income Statement)

Structure:
```
A1: "LAPORAN LABA RUGI"
A2: "Periode"   B2: =TEXT(TODAY(),"MMM YYYY")
A4: "PENDAPATAN"
A5: "Gaji/Pendapatan Utama"   B5: =SUMIFS(...)
A6: "Pendapatan Sampingan"    B6: =SUMIFS(...)
A7: "Pendapatan Investasi"    B7: =SUMIFS(...)
A8: "TOTAL PENDAPATAN"        B8: =SUM(B5:B7)
A10: "BEBAN OPERASIONAL" (list each expense account)
A20: "TOTAL BEBAN"            B20: =SUM(B11:B19)
A22: "LABA/RUGI BERSIH"       B22: =B8-B20
```

**Expense SUMIFS pattern:**
```
=SUMIFS('Transaksi Harian'!G:G,'Transaksi Harian'!F:F,"Beban Makanan",'Transaksi Harian'!D:D,"Pengeluaran")
```

## Sheet 5: Neraca (Balance Sheet)

Key balance check formula:
```
A27: "TOTAL ASET"                      B27: =B10+B15
A28: "TOTAL KEWAJIBAN & EKUITAS"       B28: =B20+B26
A29: "BALANCE CHECK"                   B29: =IF(B27=B28,"BALANCE","ERROR")
```

**Asset formula pattern** (saldo awal + pemasukan - pengeluaran):
```
=COA!E2 + SUMIFS('Transaksi Harian'!G:G,'Transaksi Harian'!F:F,"Kas",'Transaksi Harian'!D:D,"Pemasukan") - SUMIFS('Transaksi Harian'!G:G,'Transaksi Harian'!F:F,"Kas",'Transaksi Harian'!D:D,"Pengeluaran")
```

## Sheet 6: Arus Kas (Cash Flow)

```
A4: "SALDO AWAL KAS"   B4: =COA!E2+COA!E3+COA!E4  (sum of all cash/bank opening balances)
A6: "ARUS KAS MASUK" (list each income source)
A11: "Jumlah Arus Kas Masuk"   B11: =SUM(B7:B10)
A13: "ARUS KAS KELUAR" (operational, debt payment, prive)
A17: "Jumlah Arus Kas Keluar"  B17: =SUM(B14:B16)
A19: "PERUBAHAN KAS BERSIH"    B19: =B11-B17
A20: "SALDO AKHIR KAS"         B20: =B4+B19
```

## Sheet 7: Buku Besar (General Ledger)

Per-account view using QUERY. Example for "Kas":
```
=QUERY('Transaksi Harian'!A:G,"SELECT B,C,G WHERE F='Kas' ORDER BY B",1)
```

Or using FILTER for running balance:
```
=FILTER('Transaksi Harian'!B:B,'Transaksi Harian'!F:F="Kas")
```

## Important Formula Notes

- **Sheet names with spaces** must be wrapped in single quotes in formulas: `'Transaksi Harian'!G:G`
- **Whole-column references** (`A:A`) work up to ~1000 rows. Beyond that, use explicit ranges like `A3:A1000`.
- **USER_ENTERED vs RAW**: When writing formulas via API, always use `valueInputOption=USER_ENTERED` so Sheets evaluates the formula. `RAW` stores the literal text `=SUM(...)`.
- **Date filtering in SUMIFS**: Use `DATEVALUE("2026-05-01")` comparisons or add helper columns with `=MONTH(B2)&YEAR(B2)` for monthly filtering.
