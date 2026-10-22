# COA Keyword-to-Account Mapping

Deterministic classification rules for Indonesian personal/professional bookkeeping.
All patterns are case-insensitive. Punctuation in descriptions is normalized to dots before matching.

## ASET (Assets)

| Code | Account | Keywords (regex) |
|------|---------|------------------|
| 1000 | Kas | `kas`, `tarik tunai`, `setor tunai` |
| 1100 | Bank BCA | `transfer bca`, `bca`, `setor bca` |
| 1200 | Bank Mandiri | `transfer mandiri`, `mandiri`, `setor mandiri` |
| 1300 | Piutang | `piutang`, `utang pelanggan`, `pinjaman dibayar` |
| 2000 | Peralatan | `printer`, `laptop`, `peralatan`, `elektronik`, `projector`, `komputer` |
| 2100 | Kendaraan | `motor`, `mobil`, `kendaraan`, `service kendaraan` |

## KEWAJIBAN (Liabilities)

| Code | Account | Keywords (regex) |
|------|---------|------------------|
| 3000 | Utang Usaha | `utang supplier`, `utang dagang`, `hutang usaha` |
| 3100 | Utang Bank | `utang bank`, `pinjaman bank`, `kpr`, `kredit` |

## EKUITAS (Equity)

| Code | Account | Keywords (regex) |
|------|---------|------------------|
| 4000 | Modal | `modal`, `setoran awal`, `investasi pribadi` |
| 4100 | Prive/Penarikan | `prive`, `tarik tunai pribadi`, `penarikan` |

## PENDAPATAN (Income)

| Code | Account | Keywords (regex) |
|------|---------|------------------|
| 5000 | Gaji/Pendapatan Utama | `gaji`, `salary`, `payroll`, `upah` |
| 5100 | Pendapatan Sampingan | `sampingan`, `freelance`, `jualan`, `side income` |
| 5200 | Pendapatan Investasi | `investasi`, `deposito`, `bunga`, `dividen` |

## BEBAN (Expenses)

| Code | Account | Keywords (regex) |
|------|---------|------------------|
|| 6000 | Beban Makanan | `makan`, `makanan`, `kopi`, `snack`, `catering`, `warteg`, `bubur`, `soto`, `bakso`, `nasi`, `mie`, `ayam`, `sarapan`, `sop`, `dawet`, `es`, `wedang`, `minuman`, `jajan`, `pecel`, `ketoprak`, `gendar` |
| 6100 | Beban Transportasi | `bensin`, `parkir`, `toll`, `gojek`, `grab`, `transport`, `taksi`, `commuting` |
| 6200 | Beban Listrik & Air | `listrik`, `pln`, `air`, `pam` |
| 6300 | Beban Internet & Pulsa | `internet`, `wifi`, `pulsa`, `kuota`, `paket data` |
| 6400 | Beban Pendidikan | `kursus`, `bimbel`, `seminar`, `pelatihan`, `buku`, `pendidikan` |
| 6500 | Beban Kesehatan | `dokter`, `obat`, `rumah sakit`, `klinik`, `bpjs` |
| 6600 | Beban Pakaian | `baju`, `sepatu`, `tas`, `pakaian`, `laundry` |
| 6700 | Beban Hiburan | `nonton`, `game`, `hiburan`, `spotify`, `netflix`, `bioskop`, `jalan jalan` |
| 6800 | Beban Amal/Sedekah | `sedekah`, `infaq`, `zakat`, `amal`, `donasi` |
| 6900 | Beban Lain-lain | *(fallback if no pattern matches)* |

## Classification Algorithm

```python
def classify_coa(description):
    desc_lower = re.sub(r'[^\w\s]', '.', description.lower())
    for pattern, name, code, tipe in COA_RULES:
        if re.search(pattern, desc_lower):
            return name, code, tipe
    return "Beban Lain-lain", "6900", "Pengeluaran"
```

## Notes

- Order of rules matters. More specific patterns should come before generic ones.
- Descriptions like "transfer 5jt" are ambiguous (could be Bank BCA, Bank Mandiri, or Kas). Always ask for clarification.
- The pattern `prive` can overlap with `modal` or `kas`. Ensure `prive` is checked after `modal` if both keywords appear.
