# Indonesian Chart of Accounts (COA) Template

Complete 23-account COA for personal/small-business finance tracking in Indonesia. Paste directly into the `COA` sheet starting at A1.

## Header Row
| Column | Content |
|--------|---------|
| A | Kode |
| B | Nama Akun |
| C | Tipe |
| D | Kelompok |
| E | Saldo Awal |

## Full COA Table

| Kode | Nama Akun | Tipe | Kelompok | Saldo Awal |
|------|-----------|------|----------|------------|
| 1000 | Kas | Aset | Aset Lancar | 0 |
| 1100 | Bank BCA | Aset | Aset Lancar | 0 |
| 1200 | Bank Mandiri | Aset | Aset Lancar | 0 |
| 1300 | Piutang | Aset | Aset Lancar | 0 |
| 2000 | Peralatan | Aset | Aset Tetap | 0 |
| 2100 | Kendaraan | Aset | Aset Tetap | 0 |
| 3000 | Utang Usaha | Kewajiban | Kewajiban Jangka Pendek | 0 |
| 3100 | Utang Bank | Kewajiban | Kewajiban Jangka Panjang | 0 |
| 4000 | Modal | Ekuitas | Ekuitas | 0 |
| 4100 | Prive/Penarikan | Ekuitas | Ekuitas | 0 |
| 5000 | Gaji/Pendapatan Utama | Pendapatan | Pendapatan | 0 |
| 5100 | Pendapatan Sampingan | Pendapatan | Pendapatan | 0 |
| 5200 | Pendapatan Investasi | Pendapatan | Pendapatan | 0 |
| 6000 | Beban Makanan | Beban | Beban Operasional | 0 |
| 6100 | Beban Transportasi | Beban | Beban Operasional | 0 |
| 6200 | Beban Listrik & Air | Beban | Beban Operasional | 0 |
| 6300 | Beban Internet & Pulsa | Beban | Beban Operasional | 0 |
| 6400 | Beban Pendidikan | Beban | Beban Operasional | 0 |
| 6500 | Beban Kesehatan | Beban | Beban Operasional | 0 |
| 6600 | Beban Pakaian | Beban | Beban Operasional | 0 |
| 6700 | Beban Hiburan | Beban | Beban Operasional | 0 |
| 6800 | Beban Amal/Sedekah | Beban | Beban Lain | 0 |
| 6900 | Beban Lain-lain | Beban | Beban Lain | 0 |

## Extending COA

To add a new account:
1. Pick the next available code in the appropriate range
2. Add a row to the COA sheet
3. Add a corresponding SUMIFS row to Laba Rugi (if Beban/Pendapatan) or Neraca (if Aset/Kewajiban/Ekuitas)

## Common Adaptations

| For | Add/Modify |
|-----|------------|
| Business inventory | Add 1400 Persediaan (Aset Lancar) |
| Employee salaries | Add 7000 Beban Gaji (Beban Operasional) |
| Depreciation | Add 2300 Akumulasi Penyusutan (contra-asset) |
| Tax tracking | Add 3200 Utang Pajak (Kewajiban) |
| Investment portfolio | Add 1400 Investasi Saham, 1500 Reksadana (Aset Lancar) |
