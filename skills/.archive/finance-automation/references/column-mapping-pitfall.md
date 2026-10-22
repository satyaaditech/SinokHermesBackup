# Pitfall: Column I vs Column J Confusion

## The Mistake

When uploading a receipt photo to Google Drive and recording the transaction, I initially placed the **Google Drive photo link** into **Column I (No Ref)** instead of **Column J (Catatan)**.

This caused:
- The No Ref field to be overwritten with a URL
- The Catatan field to remain empty
- Confusion in the spreadsheet structure

## The Fix

| Column | Header | Content | What Goes Here |
|--------|--------|---------|----------------|
| I | No Ref | Invoice / faktur number | e.g., `HT26050366`, `0001#7599`, `TRF-001` |
| J | Catatan | Notes + Google Drive links | e.g., `https://drive.google.com/file/d/.../view` |

## Verification Query

After writing a transaction, always verify with:

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
$GAPI sheets get <SPREADSHEET_ID> "'Transaksi Harian'!A1:J<last_row>"
```

Check that:
- Column I contains the invoice number (not a URL)
- Column J contains the Drive link (if a photo was uploaded)

## User Correction Record

User explicitly corrected: "Link Drive selalu di kolom J (Catatan), bukan I"

This happened because I misread the column mapping. Spreadsheet header row:
- A=No, B=Tanggal, C=Keterangan, D=Tipe, E=Kode COA, F=Nama Akun, G=Jumlah, H=Metode, I=No Ref, J=Catatan
