# OmniRoute Introspection Recipes

Live-captured query snippets + the `auto/*` → variant mapping. SSH host = `n8nserver`
(Tailscale `100.92.237.45`). DB path = `/home/satyaaditech/.omniroute/storage.sqlite`.
No `sqlite3` CLI on the box — use `python3`.

## List active vs inactive providers (the routing pool)

```python
import sqlite3
c = sqlite3.connect('/home/satyaaditech/.omniroute/storage.sqlite')
cur = c.cursor()
cur.execute("SELECT provider, name, is_active, default_model, priority "
            "FROM provider_connections")
for r in cur.fetchall():
    print(r)
```

Live snapshot (2026-08-12):
- `antigravity` — thefullstackprogrammer@gmail.com — **active** (Gemini + Claude family)
- `openai-compatible-chat-...` — OpenCodePro → `opencode-go/deepseek-v4-pro` — **active**
- `mimocode` — MiMoCode Account 1 — inactive
- `nvidia` — inactive
- `openrouter` — MyOpenRouter — inactive

## List persisted combos + their models

```python
import sqlite3, json
c = sqlite3.connect('/home/satyaaditech/.omniroute/storage.sqlite')
cur = c.cursor()
cur.execute("SELECT name, data FROM combos")
for name, data in cur.fetchall():
    print(name)
    d = json.loads(data)
    for m in d.get('models', []):
        print('  -', m.get('model'), '| provider:', m.get('providerId'))
```

## List upstream provider nodes

```python
cur.execute("SELECT id, type, name, prefix, base_url FROM provider_nodes")
```

## `auto/*` → AutoVariant mapping (builtinCatalog.ts)

| alias | variant |
|---|---|
| auto/best-coding | coding |
| auto/best-reasoning | smart |
| auto/best-fast | fast |
| auto/best-vision | smart |
| auto/best-chat | (default) |
| auto/best-coding-fast | fast |
| auto/pro-coding / pro-reasoning / pro-vision | coding / smart / smart |
| auto/pro-fast | fast |
| auto/coding / fast / chat | coding / fast / (default) |
| auto/cheap | cheap |
| auto/offline | offline |
| auto/smart | smart |
| auto/claude-opus | smart |
| auto/claude-sonnet | coding |
| auto/best-free | cheap |

Valid variants (`autoPrefix.ts`): `coding | fast | cheap | offline | smart | lkgp`.

Fitness tiers (`pipelineRouter.ts` `FITNESS_TIERS`):
- `best-reasoning` → minFitness 0.85
- `cheapest` → maxFitness 0.75
- `moderate` → min 0.6, max 0.9

Intent → task map: `code→code, math→math, reasoning→reasoning, creative→creative,
medium→medium, simple→simple`.

## Resolve current model from a streaming response

Responses stream as SSE `data:` chunks. Extract the resolved model with grep (NOT
`json.loads` — the whole body is not a single JSON doc):

```bash
curl -s http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer sk-..." -H "Content-Type: application/json" \
  -d '{"model":"auto/best-reasoning","messages":[{"role":"user","content":"hi"}],"max_tokens":5}' \
  | grep -o '"model":"[^"]*"' | tail -1
```

The `model` field on the chunk is the *resolved* concrete model (e.g. `deepseek-v4-pro`),
and the last chunk carries `usage` + `finish_reason: stop` with an `omniroute-keepalive`
interstitial chunk that should be ignored.
