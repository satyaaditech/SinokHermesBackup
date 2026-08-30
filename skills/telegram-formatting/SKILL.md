---
name: telegram-formatting
description: Format messages and tables for Telegram — avoid broken markdown, use readable layouts, and follow platform constraints.
trigger: When sending formatted content to Telegram (news, reports, data, lists, tables)
---

# Telegram Formatting

Class-level skill for producing readable, mobile-friendly formatted content on Telegram.

## 1. Message Formatting (from telegram-message-formatting)

### ⚠️ CRITICAL: DO NOT USE MARKDOWN TABLES

Telegram does NOT render markdown tables (`| col | col |`) properly. They appear as raw text and look broken/berantakan.

**NEVER DO THIS:**
```markdown
| # | Title | Date |
|---|-------|------|
| 1 | News  | Jan  |
```

### ✅ RECOMMENDED FORMATS

**Format 1: Bullet Points with Emoji (RECOMMENDED)**
```
▸ **Title** (Date)
   Sumber: Source
   → Brief description or key point

▸ **Title** (Date)
   Sumber: Source
   → Brief description or key point
```

**Format 2: Numbered List with Divider**
```
1️⃣ Title
   📅 Date | 📰 Source
   └─ Description

2️⃣ Title
   📅 Date | 📰 Source
   └─ Description
```

**Format 3: Simple Key-Value**
```
• Key: Value
• Key: Value
```

---

## 2. Table Formatting (from telegram-table-formatter)

When tabular data is unavoidable, use Telegram-friendly layouts.

### ⚠️ AVOID ASCII Box Style

ASCII/box-drawing tables (`┌─┬─┐│`) often render broken or misaligned on mobile. The user has explicitly rejected this format.

If borders are needed, use simple dash separators:
```
Column1 | Col2   | Col3
--------|--------|------
Data1   | Value2 | Yes
Data2   | Value3 | No
```

But prefer emoji or simple list formats below.

### ✅ RECOMMENDED TABLE FORMATS

**Emoji Style (RECOMMENDED for Telegram)**
```
📊 Table Title

👤 Satya  ➡ 👑 Admin   ✅
👤 Budi   ➡ 👤 User    ✅
👤 Anon   ➡ 🚫 Blocked ❌
```

**Simple List (RECOMMENDED for 2–4 columns)**
```
• Item 1  → Value A
• Item 2  → Value B
• Item 3  → Value C
```

**Code Block (for data-heavy tables)**
```
```
Name      | Role   | Status
----------|--------|-------
Alice     | Admin  | active
Bob       | User   | active
Charlie   | Guest  | pending
```
```

## General Rules

1. Never use markdown tables (`|`)
2. Never use ASCII box-drawing borders
3. Prefer emoji or simple lists for 2–4 columns
4. Use code blocks only when data density is high
5. Test readability on mobile (narrow screens)
