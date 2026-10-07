---
name: hermes-provider-debugging
description: Diagnose "model provider failed" errors in Hermes.
version: 1.1.0
author: Sinox
platforms: [linux]
---

# Hermes Provider Debugging

Class-level skill for diagnosing "model provider failed after retries" / "Provider auth failed" errors when Hermes can't reach its model backend. Covers health checks, log analysis, config review, and OmniRoute-specific patterns.

## When to Use

- User sees "model provider failed after retries" / "Provider auth failed" in chat
- Hermes works in some chats/topics but fails in others (intermittent)
- First message after daily session reset fails, subsequent messages work
- Hermes session hangs or errors mid-response
- Suspect custom provider (OmniRoute, vLLM, llama.cpp, OpenRouter) is down or misrouted
- User asks "kenapa error lagi" / "provider kok gagal terus"

## Triggers

- `⚠️ The model provider failed after retries`
- `Provider auth failed`
- `model.*fail` / `non-200` in gateway logs
- Responses consisting entirely of hardcoded deprecation notices (e.g., "Gemini 3 Pro is no longer available")

## 🔴 PITFALL: Model Deprecation Notices as 200 OK Responses
Sometimes, downstream providers (or proxy endpoints) sunset a model and, instead of returning a 4xx HTTP error (which auto-triggers failovers), they return a `200 OK` with a hardcoded deprecation message injected as the chat response text. This breaks the experience but bypasses standard error handlers.

**Fix for OmniRoute Combos:**
1. Connect to the OmniRoute database via Python SQLite: `~/.omniroute/storage.sqlite`.
2. Query the `combos` table.
3. Parse the `data` column (JSON) for each row.
4. Replace the deprecated model strings in the `models` array (e.g., `gemini-3.5-flash` -> `gemini-3.7-flash`).
5. Re-serialize back to string using `json.dumps(data)`.
6. Run `UPDATE combos SET data = ? WHERE id = ?` for modified rows and `commit()` the transaction.

## Probing: which model is actually serving (resolve auto/* aliases)

`/v1/models` on OmniRoute lists ALIASES (`auto/best-reasoning`, `auto/best-vision`, ...) but NOT the concrete backend each alias resolves to. To see the real model, POST a minimal chat completion with the alias and read the `model` field from the first SSE chunk:

```bash
curl -s -o /tmp/probe.txt http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer <key>" -H "Content-Type: application/json" \
  -d '{"model":"auto/best-reasoning","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'
grep -o '"model":"[^"]*"' /tmp/probe.txt | head -1
```

PITFALLS:
- OmniRoute streams SSE (`data: {...}` lines) — the response is NOT valid JSON. Do NOT pipe to `json.loads` (throws JSONDecodeError). Grep the raw file instead.
- `curl | python3` triggers Hermes security scanner (HIGH: pipe to interpreter). Always `curl -s -o file` first, inspect separately.

## Testing a capability (e.g. image generation) through OmniRoute

To check whether an image-capable model actually returns image bytes via the chat-completions path:

```bash
curl -s -o /tmp/img_test.txt http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer <key>" -H "Content-Type: application/json" \
  -d '{"model":"antigravity/gemini-3.1-flash-image","messages":[{"role":"user","content":"Create an image: cute cat with red hat"}],"max_tokens":300}'
grep -c 'data:image' /tmp/img_test.txt        # >0 = real image bytes delivered
grep -o '"image_url"[^}]*' /tmp/img_test.txt
```

If only `reasoning_content` chunks stream and no `data:image`/`image_url` part appears, the binary image is NOT delivered through that path. Findings like "gemini-3.1-flash-image returned no image bytes" are time/version-specific — RE-TEST before concluding a model can't generate; also check `/v1/models` for alternative aliases and whether ComfyUI is up (localhost:8188).

## Important: OmniRoute FAILOVER WORKS — check combo quality first

Before debugging Hermes retries: OmniRoute's virtual combo failover mechanism is usually working correctly. The REAL problem is often that **all candidates in the combo are dead models**. OmniRoute exhausts its internal fallback list and returns an error to Hermes.

Always check OmniRoute's own logs BEFORE touching Hermes config:

```bash
# Check if OmniRoute did proper failover but ran out of working models
grep "All models failed\\|Model.*failed, trying next" \
  ~/.omniroute/logs/application/app.log | tail -20

# Count which models fail most often
grep "Model.*failed, trying next" \
  ~/.omniroute/logs/application/app.log | \
  sed 's/.*Model //; s/ failed.*//' | sort | uniq -c | sort -rn | head -10
```

### Removing dead connections from OmniRoute

When free-tier or expired connections poison the virtual combo, delete them from OmniRoute's DB:

```bash
# Find dead connections
python3 -c "
import sqlite3, os
db = sqlite3.connect(os.path.expanduser('~/.omniroute/storage.sqlite'))
rows = db.execute('SELECT id, provider, name, is_active FROM provider_connections').fetchall()
for r in rows:
    print(f'{r[0][:8]} | {r[1]:20} | active={r[3]}')
"

# Delete by provider name (e.g., 'opencode' free tier)
python3 -c "
import sqlite3, os
db = sqlite3.connect(os.path.expanduser('~/.omniroute/storage.sqlite'))
db.execute(\"DELETE FROM provider_connections WHERE provider='opencode'\")
db.commit()
print(f'Deleted {db.total_changes} rows')
"
# Then restart OmniRoute: kill <PID> (auto-restarts cleanly)
```

---

## Hermes Session Model Switching — the hidden "DM works, group stuck" root cause

When the primary provider fails, Hermes has a built-in model-switching mechanism: it searches the model catalog for alternatives and **permanently switches the session** to a different model/provider. This is separate from the configured `fallback_providers` chain.

### Why this breaks some chats but not others

Each Telegram chat/topic gets its own Hermes session. If session A's OmniRoute request fails during a model-switch window, that session permanently switches to an alternative (e.g., `opencode-go/deepseek-v4-pro`). Session B (started when OmniRoute was healthy) stays on OmniRoute. Result: **"DM works, group stuck"**.

Sessions keep cascading: deepseek-v4-pro → deepseek-v4-flash → glm-5.2 → ... never returning to OmniRoute even after OmniRoute is healthy again.

### Detecting switched sessions

The switch is visible in agent logs:

```bash
grep "model was just switched" ~/.hermes/logs/agent.log | grep "$(date +%Y-%m-%d)"
```

And in state.db:

```bash
python3 -c "
import sqlite3, json, os
db = sqlite3.connect(os.path.expanduser('~/.hermes/state.db'))
rows = db.execute(\"SELECT id, model, model_config FROM sessions WHERE started_at > $(date -d 'today 00:00' +%s)\").fetchall()
for r in rows:
    cfg = json.loads(r[2])
    gw = cfg.get('gateway_runtime', {})
    if gw.get('provider') != 'custom':
        print(f'SWITCHED: {r[0][:30]} model={r[1]} gw_provider={gw.get(\"provider\")}')
"
```

### Resetting a stuck session

Update the session's model back to the default and remove the `gateway_runtime` override:

```bash
python3 -c "
import sqlite3, json, os
db = sqlite3.connect(os.path.expanduser('~/.hermes/state.db'))
new_cfg = json.dumps({
    'max_iterations': 90,
    'reasoning_config': {'enabled': True, 'effort': 'medium'},
    'max_tokens': None
})
db.execute(\"UPDATE sessions SET model='auto/best-reasoning', model_config=? WHERE id='SESSION_ID'\", (new_cfg,))
db.commit()
print(f'Reset: {db.total_changes} row(s)')
"
```

### Preventing: delegation config leak

The `delegation.model` and `delegation.base_url` in `config.yaml` can become model-switching targets. If `delegation` points directly to a provider with depleted credits (e.g., `opencode.ai/zen/go/v1`), switched sessions will hit 401 indefinitely. Route delegation through OmniRoute to avoid this:

```yaml
delegation:
  model: auto/best-reasoning
  base_url: http://localhost:20128/v1
  api_key: ${OMNIROUTER_API_KEY}
```

# Count which models fail most often
grep "Model.*failed, trying next" \
  ~/.omniroute/logs/application/app.log | \
  sed 's/.*Model //; s/ failed.*//' | sort | uniq -c | sort -rn | head -10
```

If you see patterns like `oc/minimax-m3-free`, `oc/nemotron-3-super-free`, `oc/deepseek-v4-flash-free` ALL failing with 401/403 in sequence → **the virtual combo contains dead free-tier models**. Fix is in OmniRoute, NOT Hermes.

---

## 1. Quick Health Check (30 seconds)

Run these in parallel:

```bash
# 1. Can Hermes reach the provider?
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:20128/v1/models

# 2. Is the provider process alive?
ps aux | grep -i omniroute | grep -v grep

# 3. Which process owns the port?
ss -tlnp | grep <PORT>
```

If HTTP non-200 or no process: provider is down → go to §2.
If HTTP 200 but Hermes errors intermittently (works in some chats, fails in others): session affinity / LKGP issue → go to §3.
If HTTP 200 but Hermes always errors: routing/config issue → go to §4.

---

## 2. Provider Process Investigation

### OmniRoute-specific checks

```bash
# Find all OmniRoute processes with start time
ps -eo pid,lstart,etime,cmd | grep omniroute | grep -v grep

# Check port ownership
ss -tlnp | grep -E "20128|omniroute"

# Test actual inference (not just /v1/models)
curl -s http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OMNIROUTER_API_KEY" \
  -d '{"model":"auto/best-reasoning","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'
```

### Zombie process pattern (OmniRoute auto-update)

OmniRoute can auto-update via npm. When this happens:
- New process (vX.Y.Z) starts and takes over port 20128
- Old process stays alive but loses port binding — becomes zombie
- Brief outage during transition (~seconds) can trigger Hermes retries

**Fix**: kill the old PID after confirming it holds no ports:
```bash
ss -tlnp | grep <OLD_PID>  # should return nothing
kill <OLD_PID>              # safe to kill
```

---

## 3. Gateway Log Analysis

Gateway logs live at `~/.hermes/logs/gateway.log`.

```bash
# Count stale session warnings (session ended but still live)
grep -c "ended in state.db but still live" ~/.hermes/logs/gateway.log

# Find all provider/error/retry patterns
grep -n -i "provider.fail\|api.error\|retry\|non.200\|auth.fail" ~/.hermes/logs/gateway.log | tail -20

# Check exit diagnostic logs
tail -30 ~/.hermes/logs/gateway-exit-diag.log
tail -30 ~/.hermes/logs/gateway-shutdown-diag.log
```

Also check session history for recurring patterns:
```
session_search(query="provider failed", sort="newest", limit=3)
```

---

## 3. Session Affinity & LKGP (Provider UP, Intermittent Failures)

When the provider responds to curl health checks and some sessions work while others fail, the issue is often OmniRoute's **last-known-good-provider (LKGP)** session affinity — not a provider outage.

### Pattern Recognition

- "Provider failed" in one Telegram topic, but other topics work fine
- Error occurs on **first message after daily session reset** (~04:00 WIB)
- **Pesan berikutnya di topik yang sama selalu sukses** — LKGP sudah terbentuk

### Root Cause

1. Daily `session_reset` (~04:02) clears all session affinity caches
2. Next message in any topic needs OmniRoute to **re-discover** the working provider
3. LKGP has no cached target → tries candidates in the `auto/*` combo
4. First attempt may hit a candidate that responds slowly or errors
5. Hermes exhausts `api_max_retries` before LKGP finds a working candidate
6. **Subsequent messages succeed** because LKGP now has a cached provider

### Fix: Increase api_max_retries

```bash
hermes config set agent.api_max_retries 8
```

This gives OmniRoute more recovery time during session re-discovery (~8 retries with backoff ≈ ~60s total).

### Deep Diagnostics

For full OmniRoute DB investigation and log analysis, see `references/omniroute-session-affinity.md`.

Quick checks:

```bash
# Check active OmniRoute providers
python3 -c "
import sqlite3, os
db = sqlite3.connect(os.path.expanduser('~/.omniroute/storage.sqlite'))
rows = db.execute('SELECT provider, name, is_active, test_status FROM provider_connections ORDER BY is_active DESC').fetchall()
for r in rows:
    print(f'{\"✅\" if r[2]==1 else \"❌\"} {r[0]:45s} | {r[1]:25s} | test={r[3]}')
"

# Check OmniRoute routing decisions
grep "COMBO\|LKGP\|affinity\|ROUTING" ~/.omniroute/logs/application/app.log | tail -20

# Check gateway session recovery
grep "is ended in state.db\|dropping stale\|recovering" ~/.hermes/logs/gateway.log | tail -20
```

---

## 4. Config Review

Key fields in `~/.hermes/config.yaml`:

| Field | Effect | Recommendation |
|-------|--------|----------------|
| `agent.api_max_retries` | Retries before user sees error | 3 is default; increase to 5 for flaky providers |
| `fallback_providers` | Backup if primary fails | **Empty = no fallback**. Add OpenRouter or secondary endpoint |
| `agent.gateway_timeout` | Max session time (seconds) | 1800 (30 min) is default |
| `model.base_url` | Provider endpoint | Verify port and host are correct |

**Critical**: empty `fallback_providers: []` means NO resilience. If primary provider has any hiccup, user sees the error immediately after retries exhaust.

---

## 6. OmniRoute Model Routing Issues

Previous investigation (Aug 10, 2026) found: OmniRoute's `auto/best-reasoning` can route to dead `oc/` free-tier models that all return 401/403 → "All models failed". See `references/omniroute-dead-connection-fix.md` for full fix procedure.

If provider is UP but intermittent failures persist (works in some chats, fails in others), the root cause is typically **session affinity / LKGP** — not dead providers. See §3 and `references/omniroute-session-affinity.md` for full diagnostics.

---

## 7. Dead Provider Connection Cleanup (OmniRoute)

**Pattern**: OmniRoute virtual combos include models from dead provider connections. All candidates fail → OmniRoute returns error to Hermes despite correct internal failover.

**Quick fix** (see `references/omniroute-dead-connection-fix.md` for full procedure):

```bash
# Diagnose: count failing models
grep "Model.*failed, trying next" ~/.omniroute/logs/application/app.log | \
  sed 's/.*Model //; s/ failed.*//' | sort | uniq -c | sort -rn | head -10

# Fix: delete dead connection from OmniRoute DB
python3 -c "
import sqlite3, os
db = sqlite3.connect(os.path.expanduser('~/.omniroute/storage.sqlite'))
db.execute('DELETE FROM provider_connections WHERE provider=\"opencode\"')
db.commit()
print('Deleted — restart OmniRoute to apply')
"
```

**Common dead models**: `oc/minimax-m3-free`, `oc/nemotron-3-super-free`, `oc/deepseek-v4-flash-free` — all from `opencode` free tier, return 401/403.

To verify which providers are active/inactive:

Workaround: pin a specific model instead of `auto/*` if the issue persists.

---

## Pitfalls

- **Don't assume provider is down if `/v1/models` returns 200** — test actual inference with a chat completion
- **Don't kill processes blindly** — verify with `ss -tlnp` first that the PID holds no ports
- **Silent session resets**: daily schedule can reset a session mid-error, making the failure look like a new-session problem
- **Port conflicts during update**: OmniRoute v16.2.10+ can briefly conflict if old process hasn't released the port
