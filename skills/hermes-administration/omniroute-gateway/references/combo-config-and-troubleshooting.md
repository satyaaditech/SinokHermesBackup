# Combo name resolution & the Hermes↔OmniRoute config contract

Live-learned from a real outage (2026-08-13): Hermes group chat threw
`HTTP 400: Model 'X' is not a valid combo or provider. Unknown built-in auto combo.`
Root cause = name mismatch between Hermes `model.default` and the combo stored in
OmniRoute. This reference captures the resolution rules + the fix path.

## Name resolution rules (exact-match is the contract)

- A custom combo (in the `combos` table) is matched by its **exact `name`**.
  `getComboForModel(modelStr)` → `getCombo(modelStr)` does a literal lookup; no fuzzy
  for custom combos.
- The `auto/` prefix is reserved for **built-in virtual combos** (hardcoded in
  `AUTO_COMBO_TEMPLATES`). `auto/best-reasoning`, `auto/cheap`, etc. are NOT in the
  `combos` table — they materialize on demand.
- **Custom combos use plain names** (no `auto/`). e.g. `best-reasoning-v2`,
  `auto/antigravity` (note: this one happens to carry `auto/` but IS a custom row —
  do not rely on the prefix to infer type; check the `combos` table).
- Consequence: `auto/best-reasoning2` ≠ `best-reasoning-v2`. A config pointing at a
  name that isn't an exact combo name AND isn't a known `auto/*` template → HTTP 400.

## Custom combos do NOT appear in `/v1/models`

`/v1/models` only lists (a) built-in `auto/*` combos and (b) raw provider models
(`antigravity/claude-...`, etc.). Custom combos from the `combos` table are resolved
by name at request time but are **not injected into the catalog** — so they won't
show in Hermes' model dropdown. They still work if you set `model:` to their exact
name in config.

## Remapping without touching Hermes config: `model_combo_mappings`

Table `model_combo_mappings` (id, pattern, combo_id, priority, enabled, description)
maps a **glob pattern** → combo. Empty by default. Resolution order in
`getComboForModel`: exact combo name first, then pattern match via
`resolveComboForModel`. Use this to point `auto/best-reasoning` at a paid-only combo
without editing Hermes' 10+ auxiliary model entries. Patterns support `*`/`?`,
case-insensitive.

## Fixing a wrong Hermes model config

- **Do NOT** `patch`/`write_file` into `~/.hermes/config.yaml` — Hermes blocks agent
  edits to security-sensitive config ("Refusing to write to Hermes config file").
- Use the CLI instead: `hermes config set model.default <exact-combo-name>`.
  Confirms with `✓ Set model.default = ...`.
- Verify with `grep -A2 '^model:' ~/.hermes/config.yaml`.

## Gateway restart caveat

- `systemctl --user restart hermes-gateway` run from INSIDE the gateway is blocked
  ("cannot restart or stop the gateway from inside the gateway process" — SIGTERM
  would kill the command itself). Tell the user to run it from a separate SSH shell,
  or use `hermes gateway restart`.
- Auxiliary models (vision/compression/skills_hub/approval/mcp/delegation) each have
  their own `model:` line in config.yaml — check them too, not just `model.default`.

## Free-model leak (why "gratisan" appears)

- Free models come from a built-in **noauth** provider (`opencode` account `noauth`:
  big-pickle, `*-free` variants, nemotron, qwen-free, ling, trinity).
- `blockedProviders` in `key_value` (namespace `settings`) may already list
  `"opencode"`, but the smart-router **fallback path still uses noauth models** when
  paid targets fail/exhaust. Setting `blockedProviders` alone does NOT stop the leak.
- Reliable fix = a **custom paid-only combo** (priority strategy) so fallback can only
  land on another paid model, not a noauth free one.

## Call-log error signatures

- `[524] Combo "auto/cheap" failed — all targets exhausted` → every target in the
  combo failed (rate-limit / balance / provider down).
- `error_type=BadRequestError ... summary=HTTP 400: Model 'X' is not a valid combo or
  provider` → name mismatch (see above); check config vs `combos` table name.

## Distribution one-liner (what am I actually on right now)

```python
import json, glob
from collections import Counter
files = sorted(glob.glob('/home/satyaaditech/.omniroute/call_logs/2026-08-13/*.json'))[-40:]
combo, model, acc = Counter(), Counter(), Counter()
for f in files:
    try: s = json.load(open(f))['summary']
    except: continue
    combo[s.get('comboName','?')] += 1
    model[s.get('model','?')] += 1
    acc[(s.get('provider','?'), s.get('account','?'))] += 1
print('COMBO', combo.most_common())
print('MODEL', model.most_common())
print('PROV/ACC', acc.most_common())
```
Account `main` = paid OpenCode Go key active. Account `noauth` = free leak.
