# Ground-truth model routing inspection

When "what model am I actually on" must be answered with certainty (not the
`auto/*` alias), don't trust the virtual combo name. Two reliable sources, in
order of trust.

## 1. Call logs — ground truth (use this FIRST)

OmniRoute writes one JSON per request to
`/home/satyaaditech/.omniroute/call_logs/YYYY-MM-DD/*.json`.

Each file's `summary` carries the resolved model + provider:

- `summary.model` — actual model that served the request (e.g. `deepseek-v4-pro`)
- `summary.requestedModel` — full prefixed id (e.g. `opencode-go/deepseek-v4-pro`)
- `summary.provider` — provider id (e.g. `openai-compatible-chat-...`)
- `summary.account` / `summary.connectionId` — which connection served it
- `summary.comboName` — the virtual alias (e.g. `auto/best-reasoning`)
- `summary.comboStepId` — position in the router chain (e.g. `virtual-auto-smart-2-opencode`)
- `summary.status`, `summary.duration`, `summary.tokens`

Aggregate the stack for one combo with python (call_logs/ holds 1000+ files/day —
never read them one by one):

```bash
python3 -c "
import json, glob
from collections import Counter
files = sorted(glob.glob('/home/satyaaditech/.omniroute/call_logs/2026-08-12/*.json'))
c = Counter()
for f in files:
    try: d = json.load(open(f))
    except: continue
    s = d.get('summary') or {}
    if s.get('comboName') == 'auto/best-reasoning':
        c[(s.get('provider'), s.get('model'))] += 1
for (p,m),n in c.most_common(): print(n, p, '->', m)
"
```

## 2. SQLite DB — config/connections (NOT always populated)

DB: `/home/satyaaditech/.omniroute/storage.sqlite`

**`sqlite3` CLI is NOT installed on n8nserver.** Use python3 stdlib:

```bash
python3 -c "import sqlite3; c=sqlite3.connect('/home/satyaaditech/.omniroute/storage.sqlite'); ..."
```

Useful tables:

- `provider_connections` — active accounts (id, provider, name): mimocode,
  antigravity (`thefullstackprogrammer@gmail.com`), OpenCodePro, nvidia, openrouter.
- `provider_nodes` — provider endpoint definitions (type, name, prefix, base_url),
  e.g. `opencode-go` → `https://opencode.ai/zen/go/v1`.
- `combos` — ONLY user-created combos (e.g. `auto/antigravity`). Built-in `auto/*`
  combos are NOT here.
- `key_value` — runtime settings (semantic cache, quotas, and model aliases like
  `gemini-3-pro-high` → `agy/gemini-3.1-pro-high`).

Tables that are OFTEN EMPTY in practice — do NOT rely on them for "what model am I
on": `model_combo_mappings`, `model_intelligence`, `tier_assignments`,
`session_model_history`. Use call_logs (section 1) instead.

## 3. Built-in combo catalog (source, not DB)

Built-in `auto/*` aliases live in the OmniRoute install:

- `.../lib/node_modules/omniroute/open-sse/services/autoCombo/builtinCatalog.ts`
  → `AUTO_TEMPLATE_VARIANTS`: `auto/best-reasoning` → `"smart"`,
  `auto/best-coding` → `"coding"`, `auto/best-fast` → `"fast"`, etc.
- `.../lib/node_modules/omniroute/src/domain/assessment/types.ts`
  → `AUTO_COMBO_TEMPLATES`: per-combo `categories`, `tiers`, `strategy`.
  `auto/best-reasoning` = categories `[reasoning_deep, reasoning]`, tier
  `[premium]`, strategy `weighted` (minFitness 0.85).

## Observed stack (2026-08-12)

`auto/best-reasoning` resolved (weighted, with fallback) to:

- primary: `deepseek-v4-pro` (OpenCodePro) — dominant load
- secondary: `big-pickle` (OpenCode noauth)
- free-tier fallbacks when OpenCode Pro balance is empty: `deepseek-v4-flash-free`,
  `minimax-m3-free`, `nemotron-3-super-free`, `minimax-m2.5-free`,
  `qwen3.6-plus-free`, `ling-2.6-1t-free`, `trinity-large-preview-free`.
