# OmniRoute SQLite Schema

OmniRoute stores all configuration in `~/.omniroute/storage.sqlite`. Direct SQLite access is faster than API calls when the dashboard is password-protected.

## Key Tables

### `combos`
- `name` — combo identifier (e.g. `auto/antigravity`)
- `data` — JSON: models array with provider, connectionId, model, weight

### `provider_connections`
- `id` — UUID
- `provider` — provider type (`opencode`, `antigravity`, `nvidia`, `openai-compatible-chat-*`)
- `is_active` — 0/1
- `default_model` — only set for `openai-compatible-chat-*` providers (e.g. `opencode-go/deepseek-v4-pro`)

### `key_value`
- `key` — routing maps (e.g. `auto/best-reasoning:virtual-auto-smart-*-...`)
- `value` — JSON: `{provider, connectionId}` mapping virtual route to provider

### `model_combo_mappings`
- `pattern` — request model pattern (e.g. `auto/best-reasoning`)
- `combo_id` — UUID of combo
- `enabled` — 0/1

## Common Queries

```python
import sqlite3, json
con = sqlite3.connect(f'{HOME}/.omniroute/storage.sqlite')
cur = con.cursor()

# Active combos
cur.execute('SELECT name FROM combos')

# Active providers with IDs
cur.execute('SELECT id, provider, default_model FROM provider_connections WHERE is_active=1')

# Routing for auto/best-reasoning
cur.execute("SELECT key FROM key_value WHERE key LIKE 'auto/best-reasoning%'")

# Provider details for a specific combo
cur.execute("SELECT data FROM combos WHERE name='auto/antigravity'")
row = cur.fetchone()
data = json.loads(row[0]) if row and row[0] else {}
for model in data.get('models', []):
    print(model.get('model'), model.get('providerId'))
```

## Call Logs

Each API call logged as JSON in `~/.omniroute/call_logs/<date>/`. Structure:
```json
{
  "summary": {
    "model": "deepseek-v4-pro",
    "requestedModel": "opencode-go/deepseek-v4-pro",
    "provider": "openai-compatible-chat-...",
    "comboName": "auto/best-reasoning",
    "tokens": {"in": ..., "out": ..., "cacheRead": ...}
  }
}
```

## Pitfalls

- `provider_connections.is_active` alone is not enough — also check `key_value` for which virtual-auto routes are mapped
- `opencode` and `antigravity` providers don't have `default_model` — models are resolved at runtime through combo routing
- The `auto/best-reasoning` combo uses virtual-auto-smart routes: OmniRoute tries each mapped provider in priority order until one succeeds

## SQL Diagnostics (via call_logs table)

The `call_logs` table (distinct from per-day JSON files) stores flat records for quick querying:

```sql
-- Schema columns
SELECT * FROM PRAGMA table_info(call_logs);
-- timestamp, status, model, requested_model, provider, connection_id, duration,
-- tokens_in, tokens_out, tokens_cache_read, tokens_reasoning, tokens_compressed

-- Recent failures (401=auth, 429=rate limit)
SELECT timestamp, status, model, provider 
FROM call_logs WHERE status >= 400 
ORDER BY rowid DESC LIMIT 10;

-- Model diversity
SELECT DISTINCT model FROM call_logs;

-- Auth failure audit trail
SELECT timestamp, model, provider FROM call_logs 
WHERE status = 401 ORDER BY rowid DESC LIMIT 5;

-- Rate limit audit trail
SELECT timestamp, model, provider FROM call_logs 
WHERE status = 429 ORDER BY rowid DESC LIMIT 5;
```

**Pattern**: `auto/best-reasoning` probes free providers first — 401s on free + 200 on paid = normal fallback. Fix: disable failing free providers from the combo in OmniRoute dashboard.
