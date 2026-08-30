---
name: finance-auto-track
description: "Auto-classify transactions from text/photo, record to Google Sheets, and upload receipt to matching Google Drive COA folder."
version: 1.0.0
author: Satya Adi Dharma
platforms: [linux]
---

# Finance Auto Track

Auto-track expenses/income: classify COA → record to Sheets → upload receipt to Drive.

## Setup

1. Google Sheets accounting spreadsheet with columns:
   A=No, B=Tanggal, C=Keterangan, D=Tipe, E=Kode COA, F=Nama Akun, G=Jumlah, H=Metode, I=No Ref, J=Catatan

2. Google Drive folders: `finance/2026/<COA-name>/`

3. Folder map saved at `~/.hermes/finance_drive_folders.json`

4. Auto-classify script: `scripts/auto_finance.py`
5. **Reference:** `references/column-mapping-pitfall.md` — details on correct column usage for No Ref vs Catatan

## Input Format

**Text:**
```
Hari ini beli kopi 30rb pakai cash
```

**Photo + text:**
```
[foto nota]
Bensin motor 45rb
```

## Output Format (MANDATORY — exact template)

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

## Workflow

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

## Rules

1. Auto-detect COA from keywords (no manual selection)
2. Upload receipt photo to matching Drive folder: `finance/2026/<COA-name>/`
3. **Column I (No Ref)** = invoice/faktur number only. Never put Drive links here.
4. **Column J (Catatan)** = notes + Google Drive photo links. Always put Drive links here.
5. **NO auto-recap / total / saldo / summary** after adding a transaction unless user explicitly asks.
6. Use Indonesian accounting terms
7. Rekap nota first → then ask user "Mau saya catat ke spreadsheet?" → only proceed after user confirms "Iya"