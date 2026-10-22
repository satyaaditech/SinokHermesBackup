# Handwritten Bank Loan & Giro Ledger Digitization Workflow

Workflow for digitizing, transcribing, reconciling, and structuring multi-year handwritten bank loan / overdraft (PRK / Baki Debet) and cash ledger notebooks into Google Sheets.

## Core Characteristics & Models

### 1. Model A: Pinjaman Rekening Koran (PRK / Baki Debet)
- **Account Nature**: Liability / Loan facility balance.
- **Penarikan / BG / Bunga (+)**: Increases debt liability balance (`+`).
- **Setoran / Pembayaran (-)**: Decreases debt liability balance (`-`).
- **Formula**: `Saldo[t] = Saldo[t-1] + Penarikan[t] - Setoran[t]`.
- **Month-end Adjustments**: Look for interest charges (`Bunga + Meterai + Admin`), unrecorded check adjustments (`2 Lbr BG Susulan`), or credit line renewal fees.

### 2. Model B: Buku Kas / Simpanan Giro Positif
- **Account Nature**: Asset / Cash balance.
- **Setoran (+)**: Increases cash balance (`+`).
- **Penarikan (-)**: Decreases cash balance (`-`).
- **Formula**: `Saldo[t] = Saldo[t-1] + Setoran[t] - Penarikan[t]`.

## Pacing & Batch Processing Protocol
- **Batch Processing**: When user sends multiple photos at once, organize them chronologically first by matching opening balances to previous page closing balances.
- **Rate-Limit Pacing**: Process images with pacing between API requests to prevent Antigravity quota spikes.
- **Verification Rule**: Use `=IF(Formula_Cell = Written_Cell, "MATCH", "SELISIH")` in Google Sheets to guarantee 100% audit accuracy.
