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

## Output Format (concise)

📄 Info Faktur:
• No: [nomor]
• Tanggal: [DD/MM/YYYY]
• Penjual: [nama]
• Item: [barang/jasa]
• Total: Rp [jumlah]
• Status: [LUNAS/BELUM LUNAS]

## Rules

1. Auto-detect COA from keywords (no manual selection)
2. Upload receipt photo to matching Drive folder
3. Save Drive link to column J (Catatan), never column I
4. No auto-recap/total/saldo unless user asks
5. Use Indonesian accounting terms