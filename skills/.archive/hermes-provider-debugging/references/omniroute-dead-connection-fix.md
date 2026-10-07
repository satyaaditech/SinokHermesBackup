# OmniRoute Dead-Connection Fix

## Problem: "All models failed" from OmniRoute

OmniRoute's virtual combo (e.g., `auto/best-reasoning`) dynamically discovers models from ALL provider connections. If a connection (like `opencode` free tier) provides models that return 401/403, OmniRoute tries them in sequence, correctly fails over, but eventually runs out of candidates.

## Diagnosis

```bash
# 1. Check OmniRoute logs for the pattern
grep "All models failed" ~/.omniroute/logs/application/app.log

# 2. Identify which models are failing
grep "Model.*failed, trying next" ~/.omniroute/logs/application/app.log | \
  sed 's/.*Model //; s/ failed.*//' | sort | uniq -c | sort -rn

# 3. Map model prefixes to connections
# oc/* → opencode (free tier, often dead)
# opencode-go/* → OpenCodePro (paid tier, reliable)
# antigravity/* → antigravity (reliable)
```

## OmniRoute DB Structure

Key tables in `~/.omniroute/storage.sqlite`:

| Table | Purpose |
|---|---|
| `provider_connections` | API keys, auth, `is_active`, `test_status` |
| `provider_nodes` | Base URLs, paths |
| `combos` | Named routing combos (virtual combos are dynamic, not stored) |
| `model_combo_mappings` | Static model→combo assignments (empty in v16.x — virtual only) |
| `session_account_affinity` | LKGP session→provider bindings |

## Fix: Remove Dead Connection

```python
import sqlite3, os
db = sqlite3.connect(os.path.expanduser('~/.omniroute/storage.sqlite'))

# 1. Identify dead connection
rows = db.execute('''
  SELECT id, provider, name, is_active, test_status 
  FROM provider_connections 
  WHERE test_status != "active" OR is_active = 0
''').fetchall()
for r in rows:
    print(f'id={r[0]} provider={r[1]} name={r[2]} active={r[3]} test={r[4]}')

# 2. Delete it
db.execute('DELETE FROM provider_connections WHERE provider="<PROVIDER>"')
db.commit()

# 3. Restart OmniRoute
# Find active PID: ps aux | grep "[o]mniroute"
# SIGTERM triggers clean auto-restart (v16.2+): kill <PID>
# Verify: ps aux | grep "[o]mniroute"  (new PID expected)
# Confirm: omniroute providers list  (dead connection gone)
# Confirm: omniroute models | grep "oc/"  (should be empty)
```

## Provider Prefixes (from OmniRoute logs)

OmniRoute routing log format: `MODEL → PROVIDER/MODEL`

| Prefix | Connection | Status |
|---|---|---|
| `oc/` | opencode (free tier) | ❌ DEAD — 401/403 |
| `opencode-go/` | OpenCodePro (paid) | ✅ Working |
| `antigravity/` | antigravity | ✅ Working |
| `openai-compatible-chat-6e7128ad.../` | OpenCodePro by UUID | ✅ Working |

## OmniRoute CLI Quick Reference

```bash
omniroute providers list    # List all provider connections
omniroute models            # List available models
omniroute combo list        # List named combos (may be empty — virtual combos are dynamic)
omniroute providers test-all # Test all connections
```
