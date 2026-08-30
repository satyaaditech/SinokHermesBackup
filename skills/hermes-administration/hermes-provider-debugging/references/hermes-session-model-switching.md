# Hermes Session Model Switching — Deep Dive

## The Mechanism

When the primary provider (e.g., OmniRoute `custom` backend) returns an error, Hermes does NOT just retry the same provider. It searches its model catalog and switches the session to an alternative model/provider. This switch is PERMANENT per session — the session will never go back to the original provider unless manually reset.

The catalog it searches includes:
- Models from the configured provider (`/v1/models`)
- Models from `delegation.model` + `delegation.base_url` configuration
- Any other discovered providers

## Session State

The switch is stored in `~/.hermes/state.db` in the `sessions` table:

| Column | Before Switch | After Switch |
|--------|--------------|--------------|
| `model` | `auto/best-reasoning` | `glm-5.2` (or whatever it cascaded to) |
| `model_config.gateway_runtime.provider` | (absent) | `opencode-go` |
| `model_config.gateway_runtime.base_url` | (absent) | `https://opencode.ai/zen/go/v1` |
| `model_config.gateway_runtime.fallback_active` | (absent) | `false` |

The `gateway_runtime` field overrides the global provider config. Once set, all future turns in that session use this runtime, completely bypassing OmniRoute.

## Real-World Example (2026-08-11)

**Timeline for session `20260811_100403_7d0eadcc`:**

```
10:04 — Session created: model=auto/best-reasoning, provider=custom (OmniRoute)
        → Works fine for 9 turns

12:32 — OmniRoute fails (oc/ free models all dead; "All models failed")
12:32:42 — Hermes switches: auto/best-reasoning → deepseek-v4-pro (opencode-go)
           Agent log: "[Note: model was just switched from auto/best-reasoning 
           to deepseek-v4-pro via OpenCode Go...]"

12:33 — deepseek-v4-pro fails: HTTP 401 "Insufficient balance"
12:33:46 — Cascades: deepseek-v4-pro → deepseek-v4-flash (still opencode-go, still 401)
12:41:20 — Cascades: deepseek-v4-flash → default (moa)
12:42:02 — Cascades: default → deepseek-v4-flash (opencode-go again)
13:06:52 — Cascades: deepseek-v4-flash → glm-5.2 (opencode-go)

17:34 — OmniRoute fixed (restarted, dead connections removed)
        → But session STILL on glm-5.2/opencode-go — permanent switch!
```

**Root cause**: `delegation` config in `config.yaml` pointed directly to `opencode.ai/zen/go/v1` with `deepseek-v4-pro`. This put opencode-go models in Hermes's model catalog, making them candidates for the switch.

## Detection Queries

### Find all switched sessions today

```bash
python3 -c "
import sqlite3, json, os, time
db = sqlite3.connect(os.path.expanduser('~/.hermes/state.db'))
today = time.time() - 86400
rows = db.execute('SELECT id, model, model_config FROM sessions WHERE started_at > ?', (today,)).fetchall()
for r in rows:
    cfg = json.loads(r[2])
    gw = cfg.get('gateway_runtime', {})
    provider = gw.get('provider', 'default')
    if provider and provider != 'custom':
        print(f'  {r[0]} → model={r[1]} provider={provider}')
"
```

### Find switch events in agent log

```bash
grep "model was just switched" ~/.hermes/logs/agent.log | grep "$(date +%Y-%m-%d)" | grep -oP "session=\\S+" | sort -u
```

## Reset Query

Replace `SESSION_ID` with the stuck session:

```python
import sqlite3, json, os

db = sqlite3.connect(os.path.expanduser('~/.hermes/state.db'))
new_cfg = json.dumps({
    'max_iterations': 90,
    'reasoning_config': {'enabled': True, 'effort': 'medium'},
    'max_tokens': None
    # NO gateway_runtime → uses global provider config
})
db.execute(
    "UPDATE sessions SET model=?, model_config=? WHERE id=?",
    ('auto/best-reasoning', new_cfg, 'SESSION_ID')
)
db.commit()
```

If the default model is NOT `auto/best-reasoning`, read the global config first:

```bash
hermes config get model.default
```

## Prevention Checklist

1. Route delegation through OmniRoute, not direct provider URLs
2. Ensure `fallback_providers` chain uses models served by OmniRoute
3. After fixing OmniRoute, ALWAYS check for switched sessions
4. Monitor `api_max_retries` — short retries trigger premature switching
