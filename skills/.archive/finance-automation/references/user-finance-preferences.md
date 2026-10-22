# User Finance Response Preferences

**User**: Satya Adi Dharma (satyaaditech)  
**Platform**: Telegram  
**Priority**: Token efficiency above all else.

## Golden Rule

> After any single finance action (add transaction, upload receipt), ONLY confirm that specific action. NEVER append automatic summaries, totals, balances, or recaps unless the user explicitly asks for them.

## Response Templates

### After adding one transaction

```
Transaksi berhasil ditambahkan ✅
📄 Info:
• No: <number>
• Tanggal: <DD/MM/YYYY>
• Penjual/Item: <description>
• Total: Rp <amount>
• Status: <LUNAS/Cash/Transfer>
```

If a receipt was uploaded, add one line:
```
📁 Nota tersimpan di Drive
```

And stop. Do NOT add:
- ❌ "Total Pengeluaran: ..."
- ❌ "Saldo: ..."
- ❌ "Rekap bulan ini: ..."
- ❌ Any comparison with income

### When user asks for a list

Use minimal format. Preferred:

```
**Pengeluaran Mei 2026:**

• ⚡ Bayar listrik — Rp 450.000
• 🍽️ Beli makan siang — Rp 50.000
• 🔧 Beli Projector + Tripod — Rp 5.800.000

Total: Rp 6.300.000
```

NOT:
- ❌ ASCII box-drawing tables (break on mobile)
- ❌ Extra decorative lines
- ❌ Unrequested "vs Pemasukan" sections

### Emoji Guide

| Emoji | Meaning |
|-------|---------|
| 📥 🏦 | Modal / equity injection |
| 📥 💼 | Gaji / primary income |
| 📥 💵 | Sampingan / side income |
| 📥 📈 | Investasi / investment income |
| 💸 ⚡ | Listrik & Air |
| 💸 🍽️ | Makanan |
| 💸 ⛽ | Transportasi |
| 💸 📡 | Internet & Pulsa |
| 💸 🏥 | Kesehatan |
| 💸 📚 | Pendidikan |
| 💸 🎮 | Hiburan |
| 💸 🤲 | Amal / Sedekah |
| 🔧 | Peralatan / electronics |
| 🚗 | Kendaraan |

## What Triggers a Full Recap

Only provide comprehensive summaries when user EXPLICITLY says:
- "rekap", "ringkasan", "summary"
- "total pengeluaran DAN pemasukan"
- "laba rugi", "neraca", "arus kas"
- "semua transaksi"

## Frustration Signals to Avoid

If user says any of these, immediately switch to minimal mode:
- "ini tidak perlu diinformasikan"
- "hemat token"
- "kecuali saya tanya"
- "tidak seperti ini" (when showing verbose/format-heavy output)
- "bisa lebih ringkas?"

## One-Off vs Recurring

- One transaction add → One confirmation line per field + done
- Multiple queries in one message → Answer each minimally
- "How much did I spend?" → Just the number + item list. No "you also earned..." additions.
