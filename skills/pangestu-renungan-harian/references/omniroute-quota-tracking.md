# OmniRoute Quota & Usage Tracking Guide

This guide details how to track model quotas, remaining limits, and API usage within the local OmniRoute gateway environment on the server.

---

## 1. Checking Active Models & Endpoints

OmniRoute exposes standard OpenAI-compatible endpoints on `http://localhost:20128/v1`. To get a list of active models:

```python
import urllib.request, json
res = urllib.request.urlopen('http://localhost:20128/v1/models')
data = json.loads(res.read().decode())
for model in data['data']:
    print(model['id'])
```

Common model namespaces:
* `antigravity/*` — Google Gemini models mapped via OAuth or workspace accounts.
* `opencode-go/*` — DeepSeek / Qwen / Kimi models.

---

## 2. Tracking Quotas in SQLite

OmniRoute stores quota snapshots in `~/.omniroute/storage.sqlite`. Since command-line `sqlite3` may not be installed, query the database using Python.

### Querying Latest Quota Snapshots (Remaining Quota & Reset Timers)

The `quota_snapshots` table tracks remaining percentages of rate-limits or daily limits for keys. To fetch the latest status per active model:

```python
import sqlite3
from datetime import datetime, timezone

conn = sqlite3.connect('/home/satyaaditech/.omniroute/storage.sqlite')
cursor = conn.cursor()

# Get the latest snapshot per window_key for active providers (e.g., antigravity)
cursor.execute('''
    SELECT s.window_key, s.remaining_percentage, s.is_exhausted, s.next_reset_at, s.created_at
    FROM quota_snapshots s
    INNER JOIN (
        SELECT window_key, MAX(created_at) as max_created
        FROM quota_snapshots
        WHERE provider = 'antigravity' AND created_at > datetime('now', '-1 day')
        GROUP BY window_key
    ) m ON s.window_key = m.window_key AND s.created_at = m.max_created
    WHERE s.provider = 'antigravity'
''')

now = datetime.now(timezone.utc)
for row in cursor.fetchall():
    model, remaining, exhausted, reset_at_str, checked = row
    
    # Parse reset_at_str (e.g. 2026-08-20T01:49:49.000Z)
    reset_at = datetime.fromisoformat(reset_at_str.replace('Z', '+00:00'))
    time_left = reset_at - now
    
    total_seconds = int(time_left.total_seconds())
    if total_seconds < 0:
        time_left_str = 'Expired (awaiting update)'
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        time_left_str = f'{hours}h {minutes}m'
        
    print(f'Model: {model} | Remaining: {remaining:.2f}% | Reset in: {time_left_str}')
```

---

## 3. Querying Historical Usage (Token Consumption)

The `usage_history` table records total requests, input tokens, and output tokens. 

### Get Daily Aggregated Token Usage

```python
import sqlite3
conn = sqlite3.connect('/home/satyaaditech/.omniroute/storage.sqlite')
cursor = conn.cursor()

cursor.execute('''
    SELECT 
        SUBSTR(timestamp, 1, 10) as date,
        COUNT(*) as total_requests,
        SUM(tokens_input) as total_input,
        SUM(tokens_output) as total_output
    FROM usage_history 
    WHERE provider = 'antigravity'
    GROUP BY date
    ORDER BY date DESC
    LIMIT 7
''')
for row in cursor.fetchall():
    print(f'Date: {row[0]} | Requests: {row[1]} | Input: {row[2]:,} | Output: {row[3]:,}')
```

---

## 4. User Interaction Guidelines (Indonesian / Javanese)

When displaying quota reports directly to **Pak Satya**:
1. Default to **Basa Jawi Krama Alus** (unless explicitly told otherwise).
2. Follow standard terms defined in `references/krama-renungan-format.md` (e.g., use `sapunika` for current/now, `kula` for self, and respect Krama Inggil style).
3. Do not output raw JSON; present tables using clean Markdown lists or simple key-value blocks.
