# OmniRoute DB & call-log introspection

## DB

- Path: `/home/satyaaditech/.omniroute/storage.sqlite`
- `sqlite3` CLI is NOT installed on the box — use python3 stdlib:
  `python3 -c "import sqlite3; ..."`

### Key tables

- `combos` (id, name, data JSON, sort_order, created_at, updated_at, system_message,
  tool_filter_regex, context_cache_protection) — custom combos. `data` JSON keys:
  name, description, models[], strategy, config, isHidden, sortOrder, version.
- `model_combo_mappings` (id, pattern, combo_id, priority, enabled, description) —
  glob pattern → combo. Usually empty until you add remaps.
- `provider_connections` (id, provider, name, is_active, auth, default_model, ...) —
  active/inactive provider accounts.
- `provider_nodes` (id, type, name, prefix, api_type, base_url, chat_path, ...) —
  upstream endpoints, e.g. `OpenCode Go` prefix `opencode-go` base
  `https://opencode.ai/zen/go/v1`.
- `key_value` (namespace, key, value) — settings live under `namespace='settings'`.
- `session_model_history`, `tier_assignments`, `model_intelligence` — usually EMPTY
  (auto-assessment is in-memory, not persisted).

### Settings of note (namespace `settings`)

- `blockedProviders` — array of provider aliases (may already include "opencode").
- `comboConfigMode` — "guided" default.
- `comboAutoPromoteEnabled` — false default.
- `requireLogin` — true (dashboard auth). Chat API uses a bearer key; the management
  API (`/api/*`) needs a machine token, NOT the chat key (`sk-...`).

## Call logs — see real routing

- Dir: `/home/satyaaditech/.omniroute/call_logs/YYYY-MM-DD/*.json`
- Each file top-level keys: `summary`, `requestBody`, `responseBody`, `error`.
- Useful `summary.*` fields: `model` (resolved upstream model), `requestedModel`,
  `provider`, `account`, `comboName`, `apiKeyName` / `apiKeyId`.

Distribution one-liner (run from n8nserver):

```python
import json, glob
from collections import Counter
files = sorted(glob.glob('/home/satyaaditech/.omniroute/call_logs/2026-08-12/*.json'))
prov=Counter(); model=Counter(); combo=Counter(); acc=Counter()
for f in files:
    try: d=json.load(open(f))
    except: continue
    s=d.get('summary') or {}
    combo[s.get('comboName','?')]+=1
    prov[s.get('provider','?')]+=1
    model[s.get('model','?')]+=1
    acc[s.get('account','?')]+=1
print('combo:', combo.most_common())
print('provider:', prov.most_common())
print('model:', model.most_common(25))
print('account:', acc.most_common())
```

Interpretation: `comboName` shows which virtual/custom combo handled the call;
`provider` + `account` reveal free-vs-paid; `model` shows the concrete upstream
model. A spike of `account='noauth'` + `comboName='auto/cheap'` means free-model
fallback is active (usually balance exhaustion on the paid primary).

## CLI

- Binary: `/home/satyaaditech/.nvm/versions/node/v22.22.2/bin/omniroute`
  (not on PATH unless `source ~/.nvm/nvm.sh`).
- `omniroute combo list|create <name> --strategy priority|switch|delete|suggest`.
- `omniroute status` shows data dir, base URL, and whether the CLI is authenticated
  to the management API.
