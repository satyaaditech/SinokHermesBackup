# Creating a custom combo in OmniRoute (verified 2026-08-13)

The CLI has **no `combo` subcommand** (checked `omniroute --help`, v16.2.10). Combos
are created via the dashboard OR by direct SQLite insert. `omniroute simulate` also
won't resolve a combo from the CLI — it talks to the management API, which wants a
machine token, NOT the chat `sk-...` key (returns "No matching combo found" otherwise).
Direct insert is reliable and instant, and needs no restart (combos resolve per-request).

## Recipe (direct SQLite insert)

1. **Backup first** — WAL-aware (plain `cp` can miss WAL pages):

```python
import sqlite3
src = sqlite3.connect('/home/satyaaditech/.omniroute/storage.sqlite')
dst = sqlite3.connect('/home/satyaaditech/.omniroute/db_backups/storage-before-X.sqlite')
with dst:
    src.backup(dst)
```

2. **`combos` table schema** (from `PRAGMA table_info(combos)`):
   `id` TEXT, `name` TEXT NOT NULL, `data` TEXT(JSON) NOT NULL, `sort_order` INT,
   `created_at` TEXT, `updated_at` TEXT (ISO `%Y-%m-%dT%H:%M:%S.%fZ`),
   `system_message` NULL, `tool_filter_regex` NULL, `context_cache_protection` 0.

3. **`data` JSON shape** (match existing combos exactly — top-level keys in order):
   `name, description, models[], strategy, config, id, isHidden, sortOrder,
   createdAt, updatedAt, version`.

```json
{
  "name": "daily-chat",
  "description": "Daily chat & light tasks (priority fallback)",
  "models": [
    {"id": "daily-chat-1", "kind": "model", "model": "antigravity/gemini-3.5-flash-high",
     "providerId": "antigravity", "connectionId": "<antigravity-conn-id>", "weight": 0,
     "label": "thefullstackprogrammer@gmail.com"},
    {"id": "daily-chat-2", "kind": "model", "model": "opencode-go/deepseek-v4-flash",
     "providerId": "opencode-go", "connectionId": "<opencode-go-conn-id>", "weight": 0,
     "label": "Account 1"}
  ],
  "strategy": "priority",
  "config": {"maxRetries": 2, "retryDelayMs": 1500, "handoffThreshold": 0.85,
             "handoffModel": "", "maxMessagesForSummary": 30, "trackMetrics": true,
             "reasoningTokenBufferEnabled": true, "zeroLatencyOptimizationsEnabled": false},
  "id": "<same-uuid-as-row-id>",
  "isHidden": false,
  "sortOrder": 3,
  "createdAt": "<iso-ms>", "updatedAt": "<iso-ms>", "version": 2
}
```

- `strategy: priority` + `maxRetries` = ordered fallback: try model[0], on failure /
  403 / 429 drop to model[1], then model[2]. This is the "fallback jalan" mechanism.
- `connectionId` is optional (`best-reasoning-v2` omits it and still resolves via the
  default connection) but include it to be explicit about the account.
- model `id` values just need to be unique within the combo (`dailychat-1`, etc.).

## Known connection IDs (VERIFY first — they change)

From `provider_connections WHERE is_active=1`:
- antigravity: `5038649b-5021-49f1-80ad-ac8b236f3a2c` (thefullstackprogrammer@gmail.com)
- opencode-go: `7a3868a9-3cc2-49b3-b04f-7062fb1f6823` (main)

## Verify (no restart needed — combos resolve per-request)

Probe the chat API, then read the **flat `call_logs` table**. The SSE `"model"` field
in the raw response shows OmniRoute's internal alias (`gemini-default`,
`gemini-pro-default`) — NOT the real upstream model. Only `call_logs` tells the truth:

```sql
SELECT timestamp, status, model, requested_model, provider, combo_name, connection_id
FROM call_logs ORDER BY rowid DESC LIMIT 10;
```

Success = a row with `combo_name='daily-chat'`, `model='gemini-3.5-flash-high'`,
`requested_model='antigravity/gemini-3.5-flash-high'`, `status=200`.
Fallback proof = a row with status 403/429 on model[0] immediately followed by a
status-200 row on model[1] under the same `combo_name`.

## Point Hermes at it (task-based routing pattern)

```bash
hermes config set model.default daily-chat          # chat utama → flash combo
hermes config set delegation.model best-reasoning-v2  # renungan/subagent → pro combo
```

Config reloads live (mtime cache) — no gateway restart. `auxiliary.vision` should stay
on a real multimodal model (`antigravity/gemini-3.5-flash-low`), never a text-only
combo.
