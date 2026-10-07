# OmniRoute Session Affinity & LKGP — Deep Diagnostics

When OmniRoute responds to health checks (`HTTP 200` on `/v1/models`) but Hermes still shows "model provider failed after retries" intermittently, the issue is nearly always **session affinity loss** — not a dead provider.

## Mechanism

OmniRoute uses **LKGP (Last Known Good Provider)** strategy for `auto/*` virtual combos:

1. Each session gets an **affinity key** (`session_key=input:sha256:...`)
2. After the first successful model call, LKGP caches: `session → provider`
3. On the next message in the same session, LKGP hits the cache → fast routing
4. Daily **session_reset** (~04:02 WIB) clears all caches → affinity lost
5. Next message must re-discover — LKGP has no target, tries candidates sequentially
6. If the first candidate is slow/errors, Hermes retries exhaust before LKGP finds a working one

## Key Files & Locations

| Resource | Path |
|----------|------|
| OmniRoute logs | `~/.omniroute/logs/application/app.log` |
| OmniRoute DB | `~/.omniroute/storage.sqlite` |
| Hermes gateway log | `~/.hermes/logs/gateway.log` |
| Hermes state DB | `~/.hermes/state.db` |
| Hermes config | `~/.hermes/config.yaml` |

## OmniRoute DB Schema

### `provider_connections` — Active/inactive providers

```sql
SELECT provider, name, is_active, test_status, api_key, error_code
FROM provider_connections
ORDER BY is_active DESC;
```

- `is_active: 1` = used by OmniRoute; `0` = excluded
- `test_status: 'active'` = last health check passed; `'unknown'` = never tested
- `api_key` stored encrypted: `enc:v1:...` — **cannot be extracted for direct use**

### `provider_nodes` — Base URLs and routing

```sql
SELECT pn.name, pn.base_url, pn.chat_path, pn.api_type
FROM provider_nodes pn;
```

Key finding from 11 Aug 2026:
- OpenCode Go chat API: `https://opencode.ai/zen/go/v1` (NOT `api.opencode.ai/v1`)
- `OPENCODE_API_KEY` env var is for OpenCode **CLI coding tool**, not the chat API

### `combos` — Only `auto/antigravity` stored persistently

```sql
SELECT id, name, data FROM combos;
```

All other `auto/*` combos (`auto/best-reasoning`, `auto/best-coding`, `auto/cheap`, `auto/best-fast`) are **virtual** — generated dynamically by OmniRoute v16.x. The virtual combos auto-include all compatible active providers.

## OmniRoute Log Patterns

### Routing decisions (grep for these)

```bash
grep "COMBO\|LKGP\|affinity\|ROUTING" ~/.omniroute/logs/application/app.log | tail -30
```

Key log lines:
- `Auto selection: ... | strategy=lkgp | LKGP: using last known good provider ...` — happy path
- `Trying model 1/1: ...` — candidate attempt
- `succeeded (Nms, 0 fallbacks)` — working
- `no available affinity target` — session re-discovery needed

### Auth / session issues

```bash
grep "AUTH\|affinity target" ~/.omniroute/logs/application/app.log | tail -20
```

## Gateway Session Recovery

When Hermes gateway restarts (or OmniRoute restarts triggering gateway reconnection), state.db marks sessions as `ended` but the runtime `sessions.json` still holds stale references:

```
routing key 'agent:main:telegram:group:-1003256146835:1096' → SESSION_ID is ended in state.db but still live in sessions.json
```

Gateway auto-recovers: drops stale entry → creates new session. But the FIRST message during recovery can fail if OmniRoute hasn't built LKGP affinity yet.

### Check session state

```bash
# How many stale session warnings?
grep "is ended in state.db" ~/.hermes/logs/gateway.log | wc -l

# Which sessions recovered?
grep "dropping stale entry and recovering" ~/.hermes/logs/gateway.log | tail -10
```

## Config Pitfalls

### `hermes config set` with lists

`hermes config set` wraps list values as JSON strings — **not valid YAML**:

```bash
# ❌ Sets fallback_providers to a JSON STRING: '[{...}]'
hermes config set fallback_providers '[{...}]'

# ✓ Use Python to write proper YAML list
python3 -c "
import yaml
with open('/home/satyaaditech/.hermes/config.yaml') as f:
    config = yaml.safe_load(f)
config['fallback_providers'] = []
with open(path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False)
"
```

### Direct config.yaml writes blocked

`patch` tool refuses to write to `~/.hermes/config.yaml`:
> "Refusing to write to Hermes config file. Edit directly or use 'hermes config' instead."

### `api_max_retries`

```bash
hermes config set agent.api_max_retries 8    # ✅ works for scalar values
```

## Provider Inventory (11 Aug 2026)

```
✅ openai-compatible-chat-6e7128ad... | OpenCodePro               | test=active
✅ antigravity                          | ...                      | test=active
❌ openrouter                           | MyOpenRouter              | test=active (but is_active=0)
❌ nvidia                               | Nvidia                    | test=active (but is_active=0)
❌ mimocode                             | MiMoCode Account 1        | test=unknown
❌ opencode                             | OpenCode Account 1         | test=unknown
```

Only OpenCodePro and Antigravity are active. The `opencode` (free) provider is already `is_active=0` — it does NOT participate in routing. Misrouting to free providers is NOT the cause of intermittent failures.

## Debugging Workflow for Intermittent Failures

1. Confirm provider is UP: `curl -s -o /dev/null -w "%{http_code}" http://localhost:20128/v1/models`
2. If UP → check for session affinity pattern (works in some chats, fails in others)
3. If affinity pattern → increase `api_max_retries` from 3 to 8
4. If still failing → check OmniRoute logs for routing errors
5. If persistent → add a separate fallback provider (OpenRouter, Anthropic direct, etc.)
