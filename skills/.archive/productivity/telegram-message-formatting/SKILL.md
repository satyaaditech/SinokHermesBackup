---
name: telegram-message-formatting
description: Best practices for formatting messages to Telegram — avoid tables, use bullet points, test readability.
trigger: When sending formatted content to Telegram (news, reports, data, lists)
---

# Telegram Message Formatting

## ⚠️ CRITICAL: DO NOT USE MARKDOWN TABLES

Telegram does NOT render markdown tables (`| col | col |`) properly. They appear as raw text and look broken/berantakan.

**NEVER DO THIS:**
```markdown
| # | Title | Date |
|---|-------|------|
| 1 | News  | Jan  |
```

## ✅ RECOMMENDED FORMATS

### Format 1: Bullet Points with Emoji (RECOMMENDED)
```
▸ **Title** (Date)
   Sumber: Source
   → Brief description or key point

▸ **Title** (Date)
   Sumber: Source
   → Brief description or key point
```

### Format 2: Numbered List with Divider
```
1️⃣ Title
   📅 Date | 📰 Source
   └─ Description

2️⃣ Title
   📅 Date | 📰 Source
   └─ Description
```

### Format 3: Code Block (Monospace)
```
[TITLE]
    Tgl: Date
    Sumber: Source
    Info: Description with
          multi-line support
```

### Format 4: Plain Text with Bold
```
🔹 Title — Date (Source)
   Description line 1
   Description line 2
```

### Format 5: Compact Single-Line
```
🗞️ Date | Title | Source
   → Key point
```

## 📋 FORMAT SELECTION WORKFLOW

1. **Test multiple formats** — Send 2-3 format variants to user's Telegram
2. **Ask for preference** — Let user choose which looks best on their device
3. **Save preference** — Store user's format choice in memory or skill
4. **Use consistently** — Apply chosen format for all future Telegram messages

## 🎯 BEST PRACTICES

✅ **DO:**
- Use bullet points (▸, •, 🔹) or numbered lists (1️⃣, 2️⃣)
- Use emoji for visual scanning (📅, 📰, 🗞️, →)
- Keep lines under 60 characters for mobile readability
- Use bold for titles/highlights
- Use code blocks for structured data that needs consistent spacing
- Add separator lines (━━━━━) between sections

❌ **DON'T:**
- Use markdown tables (`| col | col |`)
- Use complex nested formatting
- Assume desktop rendering — test on mobile
- Send long paragraphs without breaks

## 🔧 VERIFICATION

Before sending formatted content to Telegram:
1. Check for any `|` table syntax
2. Ensure line breaks are clear
3. Verify emoji render correctly
4. Test on actual Telegram (not just preview)

## 📝 USER-SPECIFIC NOTES (Satya)

- User Satya Adi Dharma (@satya_aditechnology) prefers clean, readable formats
- Has explicitly complained about table formatting before
- **CRITICAL LESSON: ASCII / box-drawing tables (┌─┬─┐) render broken/berantakan in Telegram. ALWAYS use emoji-bullet lists for tabular data.**
- For finance reports: after adding a transaction, ONLY output the transaction details in invoice-style format (No, Tanggal, Penjual/Item, Total, Status). NO auto-recap/summary/total/saldo unless user explicitly asks.
- Approved format example:
  ```
  Transaksi berhasil ditambahkan ✅
  📄 Info Faktur:
  • No: HT26050366
  • Tanggal: 22/05/2026
  • Penjual: ANDALAS COMPUTER
  • Item: Projector Epson EB E600 + Tripod 70x70
  • Total: Rp 5.800.000
  • Status: LUNAS
  ```
- Requires data accuracy — never hallucinate real-time data
- YouTube automation workflow needs consistent formatting for daily reports
- Always prefer token-efficient responses

## 🧪 TESTING PROCEDURE

When unsure about format preference:

1. Send 3-5 format variants with labels (Format 1/5, Format 2/5, etc.)
2. Ask user: "Format mana yang paling rapi?"
3. Wait for user confirmation
4. Save chosen format as standard for future messages
5. Reference this skill for all subsequent Telegram sends
