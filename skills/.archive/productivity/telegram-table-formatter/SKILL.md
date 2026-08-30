---
name: telegram-table-formatter
description: Format data into Telegram-friendly table layouts with multiple styles (ASCII, emoji, simple, code block)
trigger: When user needs to display tabular data in Telegram, format lists/dicts as tables, or ask about table formatting in Telegram
---

# Telegram Table Formatter

Format data into readable tables for Telegram messaging platform.

## Supported Formats

### 1. ASCII Box Style — ⚠️ AVOID in Telegram

**WARNING:** ASCII/box-drawing tables (using `┌─┬─┐│` characters) often render broken or misaligned in Telegram, especially on mobile. The user has explicitly rejected this format.

If you must use borders, use simple dash separators:
```
Column1 | Col2   | Col3
--------|--------|------
Data1   | Value2 | Yes
Data2   | Value3 | No
```

But prefer emoji or simple list formats below.

### 2. Emoji Style (RECOMMENDED for Telegram)
```
📊 Table Title

👤 Satya  ➜ 👑 Admin   ✅
👤 Budi   ➜ 👤 User    ✅
👤 Anon   ➜ 🚫 Blocked ❌
```

### 3. Simple List (RECOMMENDED for 2–4 columns)
```
• Item 1  → Value A
• Item 2  → Value B
• Item 3  → Value C
```

### 4. Code Block Monospace (Preserves alignment)
```
```text
Name       Role      Status
───────── ───────── ───────
Satya      Admin     ✅
Budi       User      ✅
```
```

## Python Helper Function

```python
def format_telegram_table(data, headers=None, style="ascii"):
    """
    Format data as Telegram table
    
    Args:
        data: List of lists or list of dicts
        headers: List of column headers (optional)
        style: "ascii", "emoji", "simple", or "code"
    
    Returns:
        Formatted string ready for Telegram
    """
    if style == "ascii":
        return _format_ascii(data, headers)
    elif style == "emoji":
        return _format_emoji(data, headers)
    elif style == "simple":
        return _format_simple(data, headers)
    else:
        return _format_code(data, headers)

def _format_ascii(data, headers):
    # Calculate column widths
    all_rows = ([headers] if headers else []) + data
    widths = [max(len(str(row[i])) for row in all_rows) 
              for i in range(len(all_rows[0]))]
    
    # Build table
    lines = []
    sep = "┌" + "┬".join("─" * (w + 2) for w in widths) + "┐"
    lines.append(sep)
    
    for i, row in enumerate(all_rows):
        formatted = "│ " + " │ ".join(
            str(cell).ljust(widths[j]) for j, cell in enumerate(row)
        ) + " │"
        lines.append(formatted)
        
        if i == 0 and headers:
            lines.append("├" + "┼".join("─" * (w + 2) for w in widths) + "┤")
    
    lines.append("└" + "┴".join("─" * (w + 2) for w in widths) + "┘")
    return "\n".join(lines)

def _format_emoji(data, headers):
    lines = [f"📊 {headers[0] if headers else 'Data'}"]
    for row in data:
        lines.append(f"👤 {row[0]}  ➜ {row[1]}  {row[2] if len(row) > 2 else ''}")
    return "\n".join(lines)

def _format_simple(data, headers):
    lines = []
    for row in data:
        lines.append(f"• {row[0]}  → {row[1]}")
    return "\n".join(lines)

def _format_code(data, headers):
    all_rows = ([headers] if headers else []) + data
    lines = ["```text"]
    for row in all_rows:
        lines.append("  ".join(str(cell).ljust(12) for cell in row))
    lines.append("```")
    return "\n".join(lines)
```

## Usage Examples

### Permission Matrix
```python
data = [
    ["Admin", "✅ All", "✅ All", "✅ All"],
    ["User", "✅ Read", "❌ Write", "❌ Execute"],
    ["Guest", "❌ None", "❌ None", "❌ None"]
]
headers = ["Role", "Read", "Write", "Execute"]
print(format_telegram_table(data, headers, "ascii"))
```

### User List
```python
users = [
    ["Satya", "777961507", "Admin"],
    ["Budi", "123456789", "User"]
]
print(format_telegram_table(users, ["Name", "ID", "Role"], "emoji"))
```

## Quick Reference

| Style | Best For | Mobile Friendly | Telegram Safe |
|-------|----------|----------------|---------------|
| Simple | 2–4 column data, finance reports | ⭐⭐⭐⭐⭐ | ✅ Yes |
| Emoji | User lists, status display | ⭐⭐⭐⭐⭐ | ✅ Yes |
| Code | Technical data, alignment | ⭐⭐⭐⭐ | ✅ Yes |
| ASCII | ⚠️ Avoid — renders broken on Telegram | ⭐⭐ | ❌ No |

## Tips

1. **AVOID ASCII/box-drawing tables** — They look broken in Telegram mobile
2. **For finance/tabular data** — Use simple emoji-bullet lists (• No, • Tanggal, • Total)
3. **Keep columns narrow** — Telegram wraps text on mobile
4. **Use emoji indicators** — ✅ ❌ 🟢 🔴 👤 👑 💸 📥
5. **Add blank line** before/after sections for readability
6. **For very wide tables** — consider splitting into multiple messages
