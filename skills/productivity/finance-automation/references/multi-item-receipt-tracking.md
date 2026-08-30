# Multi-Item Receipt Tracking

## Purpose

When a receipt contains **multiple different items**, track each item separately for historical price analysis while keeping the financial total in "Transaksi Harian".

## Sheet: "Detail Item" (same spreadsheet as Transaksi Harian)

| Column | Header | Type | Example |
|--------|--------|------|---------|
| A | No Ref | String (link to TH No) | `18` or `INV-001` |
| B | Tanggal | Date (DD/MM/YYYY) | `01/06/2026` |
| C | Nama Item | String | `Sabun Lifebuoy` |
| D | Qty | Number | `2` |
| E | Harga Satuan | Number (Rp) | `12500` |
| F | Total Item | Formula/Number | `=D*E` → `25000` |
| G | Kategori Item | String (free text) | `Kebutuhan Rumah Tangga` |
| H | Penjual / Lokasi | String | `Indomaret Ngemplak` |

## Dual-Write Workflow

```
User sends receipt (photo or text list)
    ↓
Extract items, qty, unit prices
    ↓
Ask clarification if blurry / ambiguous
    ↓
APPEND to Transaksi Harian: 1 row = total amount, COA classification
    ↓
APPEND to Detail Item: N rows = 1 per item
    ↓
Upload receipt photo to Drive COA folder
    ↓
Confirm with item list (minimal recap)
```

## When to Use

| Scenario | Action |
|----------|--------|
| Single item ("parkir 2rb") | Transaksi Harian ONLY |
| Multi-item receipt (supermarket, hardware, restaurant bill with breakdown) | Transaksi Harian + Detail Item |
| Photo unreadable / no price breakdown | Ask user to type item list |

## Example

**Input**: Foto nota Indomaret total Rp 85.000

**Extracted items**:
- Sabun Lifebuoy 2 × Rp 12.500 = Rp 25.000
- Mie Instan 5 × Rp 3.000 = Rp 15.000
- Susu UHT 1L 2 × Rp 22.500 = Rp 45.000

**Writes**:

*Transaksi Harian*:
| No | Tanggal | Keterangan | Tipe | Kode COA | Nama Akun | Jumlah | Metode |
|----|---------|------------|------|----------|-----------|--------|--------|
| 23 | 01/06/2026 | Belanja Indomaret | Pengeluaran | 6900 | Beban Lain-lain | 85000 | QRIS |

*Detail Item*:
| No Ref | Tanggal | Nama Item | Qty | Harga Satuan | Total Item | Kategori Item | Penjual/Lokasi |
|--------|---------|-----------|-----|--------------|------------|---------------|----------------|
| 23 | 01/06/2026 | Sabun Lifebuoy | 2 | 12500 | 25000 | Kebutuhan Rumah Tangga | Indomaret Ngemplak |
| 23 | 01/06/2026 | Mie Instan | 5 | 3000 | 15000 | Makanan | Indomaret Ngemplak |
| 23 | 01/06/2026 | Susu UHT 1L | 2 | 22500 | 45000 | Makanan | Indomaret Ngemplak |

## Query Patterns Enabled

With item-level data, the agent can answer:
- "Berapa rata-rata harga sabun 3 bulan terakhir?"
- "Harga beras bulan lalu vs sekarang?"
- "Item apa yang paling sering dibeli di Indomaret?"
- "Total pengeluaran untuk mie instan tahun ini?"

## Notes

- "Detail Item" must be a **sheet tab** inside the SAME spreadsheet (`13W8pmkqdXwv...`), NOT a separate file.
- Kategori Item is free-text (not COA) — use whatever makes sense for price tracking.
- Qty and Harga Satuan should be filled explicitly; do NOT leave blank even if qty=1.
- When adding the "Detail Item" sheet tab via API, use `sheets batchUpdate` with `addSheet` request.
