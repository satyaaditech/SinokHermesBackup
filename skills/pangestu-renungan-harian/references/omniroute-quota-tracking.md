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

## 2. Multi-Account Antigravity Cluster & Quota Tracking

OmniRoute manages a cluster of **3 Google AI Pro (Antigravity)** accounts:
1. `thefullstackprogrammer@gmail.com` (Main / Active)
2. `siswatalks.tv@gmail.com` (Backup 1 / Active)
3. `satyaaditech@gmail.com` (Backup 2 / Active)

OmniRoute stores connection states and quota snapshots in `~/.omniroute/storage.sqlite`. When reporting Antigravity status to the user, **ALWAYS query and report all 3 accounts in a detailed table** (never summarize as only 1 account).

### Python Script to Query All 3 Accounts & Quotas

```python
import sqlite3
import os
import json

conn = sqlite3.connect(os.path.expanduser("~/.omniroute/storage.sqlite"))
c = conn.cursor()

# 1. Fetch all Antigravity accounts from provider_connections
accounts = c.execute("""
    SELECT id, name, email, is_active, test_status, last_error, updated_at
    FROM provider_connections
    WHERE provider = 'antigravity'
""").fetchall()

# 2. Fetch call logs breakdown per account
calls_by_acc = dict(c.execute("""
    SELECT account, count(*), sum(tokens_in), sum(tokens_out)
    FROM call_logs
    WHERE account IS NOT NULL
    GROUP BY account
""").fetchall())

# 3. Fetch latest quota snapshot per account connection_id
for acc in accounts:
    conn_id, name, email, active, status, last_err, updated = acc
    print(f"\nAccount: {email} (Status: {status}, Active: {active})")
    
    total_calls, tokens_in, tokens_out = calls_by_acc.get(email, (0, 0, 0))
    print(f"Total historical requests: {total_calls} ({tokens_in or 0:,} in / {tokens_out or 0:,} out)")
    
    snaps = c.execute("""
        SELECT s.window_key, s.remaining_percentage, s.is_exhausted, s.next_reset_at
        FROM quota_snapshots s
        INNER JOIN (
            SELECT connection_id, window_key, MAX(created_at) as max_created
            FROM quota_snapshots
            WHERE connection_id = ?
            GROUP BY connection_id, window_key
        ) m ON s.connection_id = m.connection_id AND s.window_key = m.window_key AND s.created_at = m.max_created
        ORDER BY s.window_key
    """, (conn_id,)).fetchall()
    
    for snap in snaps:
        print(f"  - {snap[0]}: {snap[1]:.2f}% remaining (reset: {snap[3]})")
```
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
