---
name: omniroute-gateway
description: Use to introspect the OmniRoute gateway on n8nserver.
version: 1.0.0
author: Sinox
platforms: [linux]
---

# OmniRoute Gateway (n8nserver)

Operate and introspect the local **OmniRoute** AI gateway that fronts Hermes' model
routing (and Honcho, renungan, etc.). Answers: "what model am I actually on",
"what's inside `auto/X`", "which providers are active", "why did routing pick X".

- **Multi-Account Failover & Load Balancing**: `references/multi-account-failover.md` — details how sibling provider connections backup/failover via LRU/LKGP.
- **Image Generation Guide**: `references/image-generation.md` — details `/v1/images/generations` and model/provider mapping.
- **Mixture of Agents Guide**: `references/mixture-of-agents.md` — details MoA presets, Reference Models, and Aggregator settings in the dashboard.
- **Quota Monitoring**: `references/quota-monitoring.md` (and `scripts/track_quota_telegram.py`) — details how to query, format, and check remaining quotas for proxy providers like Antigravity. **CRITICAL RULE**: When asked for quota (e.g. 'status quota antigravity'), ALWAYS run `python3 /home/satyaaditech/.hermes/skills/hermes-administration/omniroute-gateway/scripts/track_quota_telegram.py` and present the exact visual progress bar format inside monospace code blocks (`██████████ 96%`), never raw unformatted markdown tables.
- **Gemini Context Caching & Quota**: `references/gemini-caching.md` — details Gemini context caching setup via Google AI Studio and Vertex API requirements.
- **Troubleshooting Broken Combos**: `references/troubleshooting-combos.md` — exact workflow to fix chat errors when upstream models are deleted, and headless enumeration of SQLite combos/API models.

## Where it runs

- Host: `n8nserver` (SSH via Tailscale `100.92.237.45`, or LAN `192.168.0.112`).
- Service: systemd `omniroute.service`; binary `node .../bin/omniroute serve --port 20128` (v16.2.10+).
- Gateway endpoint: `http://100.92.237.45:20128/v1` (OpenAI-compatible). Hermes calls it
  as `http://localhost:20128/v1` via Tailscale route, provider `custom`.
- Dashboard: `http://100.92.237.45:20128/dashboard`.

## Operational gotchas (learned 2026-08)

- **Custom combos do NOT appear in `/v1/models`.** That endpoint lists only built-in
  `auto/*` aliases + raw provider models. So a custom combo (e.g. `best-reasoning-v2`,
  `auto/antigravity`) won't show in Hermes' model dropdown — but it DOES resolve by name
  via `getComboForModel` (exact match on the `combos` table).

## Antigravity Quota Checking and Reporting

For tracking and reporting the remaining quota of the `antigravity` provider:
- **Database Query**: Query the `quota_snapshots` and `provider_connections` tables in `~/.omniroute/storage.sqlite`. Get the latest snapshot per connection and model window.
- **Formatting Style (Strict Preference)**: Report the quota using a preformatted clear table and specific template:
  - Header: `📊 LAPORAN SISA KUOTA ANTIGRAVITY`
  - Waktu: `Waktu: YYYY-MM-DD HH:MM:SS WIB`
  - Emoticon and Account Header: `🔹 Akun: email@domain.com`
  - The model names should be mapped for display (e.g., `gemini-` -> `g-`, `claude-` -> `c-`), left-aligned to a width of 21 characters, followed by a 10-character progress bar, a 3-character rounded/integer percentage, and the reset time indicator `(Xh Ym)` if available.
  - Template row format: `c-opus-4-6-thinking  ██████████ 100% (4h 56m)`
- **Dynamic Decryption**: Fields like `access_token` and `refresh_token` in `provider_connections` are encrypted using AES-256-GCM. To decrypt them for manual curl testing of upstream Vertex APIs, derive the key using `crypto.scryptSync(secret, "omniroute-field-encryption-v1", 32)` where `secret` is the `STORAGE_ENCRYPTION_KEY` in `~/.omniroute/.env`. Set it in config directly.
- **`model.default` must equal the EXACT combo name.** Typo `auto/best-reasoning2` ≠ combo
  `best-reasoning-v2` → OmniRoute returns HTTP 400 "not a valid combo or provider",
  breaking the chat group. Custom combos carry no `auto/` prefix unless named that way.
- **Restarting hermes-gateway from inside the gateway is BLOCKED** (SIGTERM kills the
  command). Schedule a detached restart:
  `systemd-run --user --on-active=5s /path/restart.sh` (script body: `sleep 4; systemctl --user restart hermes-gateway`).
- **Editing `~/.hermes/config.yaml` is blocked by file tools** → use `hermes config set <key> <value>`.
- **DB**: `~/.omniroute/storage.sqlite` — query via `python3 -c "import sqlite3..."` (no
  `sqlite3` CLI installed). Tables: `combos` (id,name,`data` JSON), `model_combo_mappings`
  (pattern→combo_id; empty by default — use it to remap e.g. `auto/best-reasoning`→custom combo),
  `provider_nodes`, `provider_connections`, `key_value` (namespace `settings`, has `blockedProviders`).
- **Call logs**: `~/.omniroute/call_logs/YYYY-MM-DD/*.json` → `summary.comboName/model/
  requestedModel/provider/account`, top-level `error`. Fastest truth for "what model am I on".

## Key mental model — `auto/*` is NOT a fixed list

`auto/best-reasoning`, `auto/best-coding`, `auto/best-fast`, etc. are **smart-router
aliases**, materialized on demand. They resolve per-request, not from a static model
list. Pipeline (from `open-sse/services/autoCombo/` source):

1. Classify prompt intent (code / math / reasoning / creative / medium / simple).
2. Score every model in the **active-provider pool** for task fitness.
3. Pick best-fit model against a fitness tier (`best-reasoning` ⇒ `minFitness 0.85`).

So the "stack" = union of models from providers with `is_active=1`. If a provider
dies / runs out of balance, routing silently shifts to the next-best active model.
`auto/best-reasoning` maps to variant `"smart"` (see `builtinCatalog.ts` →
`AUTO_TEMPLATE_VARIANTS`). Built-in `auto/*` names are hardcoded in
`src/domain/assessment/types.ts` (`AUTO_COMBO_TEMPLATES`): categories + tiers +
strategy per alias.

## Combo naming & the Hermes config contract (gotcha)

Custom combos match by **exact name**; `auto/` prefix = built-in virtual combos only.
Custom combos do NOT appear in `/v1/models` (so no Hermes dropdown entry) but work
by-name. A `model.default` that isn't an exact combo name AND isn't a known `auto/*`
template throws `HTTP 400 ... not a valid combo or provider` — this is the #1 cause
of group-chat outages. Fix config with `hermes config set model.default <name>` (not
a file patch — config.yaml is protected). Full rules, `model_combo_mappings` remap,
gateway-restart caveat, and free-model leak: see
`references/combo-config-and-troubleshooting.md`.

## Custom combos — create, use, and the `/v1/models` gotcha

Custom combos live in the `combos` table (SQLite). The CLI has **no `combo` command**
(verified v16.2.10) and `omniroute simulate` talks to the management API (needs a
machine token, not the chat `sk-...` key), so the reliable creation path is the
dashboard or a **direct SQLite insert** — full verified recipe:
`references/creating-combos.md`. Each row's `data` JSON holds `{name, description,
models[], strategy, config, isHidden, ...}` where each model entry is
`{kind, model, providerId, connectionId, weight, label}`.

**Gotcha:** custom combos do NOT appear in `/v1/models` (only built-in `auto/*`
plus raw provider models do). So they won't show in Hermes' model dropdown — but
they still work: `getComboForModel()` resolves an exact combo name at request time.
Point Hermes at one by setting `model: <combo-name>` directly in config.yaml; it
routes fine even though the dropdown never lists it.

## Remapping `auto/X` → a custom combo (no Hermes config churn)

`model_combo_mappings` table maps a model-name glob (`pattern`) to a `combo_id`
(priority + enabled columns), usually empty. `getComboForModel()` (in
`src/sse/services/model.ts`) checks it after the exact-name lookup. Use it to make
`auto/best-reasoning` (and/or `auto/cheap`) resolve to a paid-only combo WITHOUT
editing Hermes config — every request keeps the same model string but routes to
your stack. Resolution order: 1) exact combo-name match in `combos`,
2) `model_combo_mappings` glob match, 3) built-in virtual catalog fallback.

## Why free models leak (and the blockedProviders caveat)

Free models come from the built-in NOAUTH provider alias `opencode` (account
`noauth`: big-pickle, `*-free` minimax/nemotron/qwen/ling/trinity). They enter as
**fallback** when the primary paid model fails — most often because the OpenCode
Pro balance is exhausted, NOT because of tier config. `blockedProviders` (settings
namespace) may already contain `"opencode"`, yet noauth fallback can still slip
through. The reliable way to exclude free models is a custom paid-only combo
(explicit list) + the mapping above — explicit lists can't leak.

## Provider architecture (paid vs free)

- `opencode-go/*` = OpenCode Go PAID (key `OPENCODE_GO_API_KEY` in
  `/home/satyaaditech/.omniroute/.env`); served through the `OpenCodePro`
  openai-compatible connection. Includes deepseek-v4-pro, glm-5.x, kimi-k3,
  qwen3.x, mimo-v2-pro, minimax-m3, gpt-5.6-luna, grok-4.5, hy3.
- `antigravity/*` = Google Antigravity OAuth (claude-opus-4-6-thinking,
  claude-sonnet-4-6, gemini-3.1-pro-high, gemini-pro-agent, ...).
- `opencode` (noauth) = FREE fallback provider (block/avoid if unwanted).

## DB & call-log introspection

Full SQLite schema, settings keys, the call-log distribution script, and CLI notes:
see `references/db-and-call-logs.md`.

## Resolve the model currently in use (fast)

```bash
curl -s -m 40 http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer sk-..." -H "Content-Type: application/json" \
  -d '{"model":"auto/best-reasoning","messages":[{"role":"user","content":"Reply with one word: your model name"}],"max_tokens":10}' \
  | grep -o '"model":"[^"]*"' | tail -1
```

**Pitfall:** responses are **SSE streaming** (`data: {...}` chunks), NOT a single JSON
doc. `curl | python3 -c "json.load(sys.stdin)"` throws `JSONDecodeError` on the first
chunk. Never pipe straight to json.load. Extract chunks or use python3 tool / streaming client.

## Support Files

- `references/db-and-call-logs.md` — SQLite schema descriptions and diagnostic queries.
- `references/combo-config-and-troubleshooting.md` — exact-name contract, name validation rules and remapping.
- `references/task-based-routing.md` — configuring different combos for user chat (`model.default`) and background delegation (`delegation.model`), detailing priority fallback setups.
parse the stream. Also `curl | python3` triggers the Hermes security approval prompt;
prefer `grep -o` / write-to-file.

## Introspecting config (where it actually lives)

There is **no plain config file** for routing — it's all in SQLite:
`~/.omniroute/storage.sqlite`. The n8nserver has **no `sqlite3` CLI**, so use Python:

```bash
ssh n8nserver "python3 -c \"import sqlite3; c=sqlite3.connect('/home/satyaaditech/.omniroute/storage.sqlite'); ...\""
```

Key tables:
- `provider_connections` — one row per provider; **`is_active`** is the flag that
  determines pool membership. Columns of note: `provider`, `name`, `default_model`,
  `is_active`, `priority`, `provider_specific_data`.
- `combos` — persisted custom combos (`data` is JSON with a `models` array).
- `model_combo_mappings` — pattern → combo routing (often empty; smart aliases aren't stored here).
- `provider_nodes` — upstream node definitions (e.g. `opencode-go` → `https://opencode.ai/zen/go/v1`).
- `routing_decisions` — audit trail of past routing choices.

Source of truth for alias behavior (read these on the server when the mapping is unclear):
- `~/.nvm/versions/node/v22.22.2/lib/node_modules/omniroute/open-sse/services/autoCombo/builtinCatalog.ts` — `auto/X` → variant table.
- `.../autoCombo/autoPrefix.ts` — valid variants (`coding|fast|cheap|offline|smart|lkgp`).
- `.../autoCombo/pipelineRouter.ts` — `FITNESS_TIERS` (`best-reasoning`: minFitness 0.85).
- `.../src/domain/pipeline.ts` — intent → task pipeline.

## Known quirks / pitfalls

- **Image models don't return pixels via the chat API.** `antigravity/gemini-3.1-flash-image`
  responds with `reasoning_content` text only; no `data:image` / `image_url` comes back
  through OmniRoute's OpenAI-compatible endpoint. Don't expect inline images from it —
  it's for the model to "see" images, not emit them back.
- **`/v1/models` lists many `auto/*` aliases** but those are virtual — the real,
  selectable models are the provider-prefixed ones (`opencode-go/*`, `antigravity/*`,
  `mimocode/*`, etc.).
- Active-provider set changes over time (account balance, health checks) — always
  re-read `provider_connections.is_active` instead of trusting memory of "what's active".

## References

- `references/introspection-recipes.md` — copy-paste SQLite queries + the exact
  `auto/*` → variant mapping table captured during a live inspection.
