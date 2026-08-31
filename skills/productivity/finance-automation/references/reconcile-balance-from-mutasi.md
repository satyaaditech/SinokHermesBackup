# Reconciling and Calculating 'Should-Be' Balance from Bank Statement (Mutasi)

Use this reference when the user provides a screenshot/text of recent bank statement transactions (mutasi) and asks to calculate what their balance should be (`kalkulasi seharusnya saya punya saldo berapa`).

## Scope Clarification: Image-only vs. Sheet Reconciliation

Before proceeding with calculations, clarify if the user wants:
1. **Image-only Calculation (Default Fallback)**: Summing and netting only the transacation entries clearly visible in the provided screenshot(s). This is common when the user wants to check the math of the statement itself (debits vs credits, or total spent in that batch).
2. **Spreadsheet Reconciliation**: Netting the new transaction entries against the lifetime historical balance currently tracked in their Google Sheets.

If ambiguous, present the **Image-only Calculation** first to keep the response extremely concise and aligned with the visual context, and ask if they desire reconciliation with their Google Sheet.

## Workflow Steps

1. **Query Sheet Net Balance**:
   - Run the Google Workspace API helper to retrieve all transaction rows from the `Transaksi Harian` sheet:
     ```bash
     python3 ./hermes-backup/skills/productivity/google-workspace/scripts/google_api.py sheets get <spreadsheed_id> "'Transaksi Harian'!A4:J300"
     ```
   - Calculate the total of all recorded `Pemasukan` and subtract all `Pengeluaran` to find the net balance currently recorded in the sheet.

2. **Extract Mutasi Transactions**:
   - Identify new transactions from the user's input/image that are NOT yet recorded in the sheet (typically post-dating the latest sheet transaction).
   - Categorize the transactions (e.g. Shopee Ind, ATM withdrawals, SPBU, Domainesia) and sum up their total debit/credit amounts.

3. **Compute 'Should-Be' Balance**:
   - Subtract the new mutation expenses from the sheet's net balance:
     $$\text{Saldo Akhir Seharusnya} = \text{Saldo Sheet} - \text{Total Pengeluaran Mutasi}$$

4. **Response Formatting (Krama Alus & Concise)**:
   - Always respect the user's preferred language and tone: **Jawi Krama Alus ingkang jangkep**.
   - Keep the reply clean, listing the starting sheet balance, itemized new mutasi entries, and the final corrected should-be balance.
   - Example:
     ```
     Sugeng [enjang/siang/sore/dalu], Pak Satya.

     Kalkulasi saldo sakmenika:
     • Saldo sheet (<tanggal>): Rp <jumlah>
     • Pengeluaran mutasi:
       - <Deskripsi 1>: Rp <jumlah>
       - <Deskripsi 2>: Rp <jumlah>
       - **Total**: Rp <jumlah>
     • **Saldo sakmesthinipun**: **Rp <jumlah>**

     Punapa transaksi mutasi punika kedah dipun-serat wonten spreadsheet? Matur nuwun.
     ```
