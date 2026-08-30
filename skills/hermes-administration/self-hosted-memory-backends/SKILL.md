---
name: self-hosted-memory-backends
description: Use when self-hosting Honcho on n8nserver via OmniRoute.
version: 1.0.0
author: Sinox
platforms: [linux, macos]
---

# Self-Hosted Memory Backends (Honcho on n8nserver)

How to stand up a self-hosted memory provider on `n8nserver` and point Hermes at it, with LLM reasoning routed through the **local OmniRoute gateway** instead of paying an external memory SaaS. Primary use-case: Honcho.

## When to Use
- User says "self-host Honcho" / "biar murah" / "setup memory via OmniRoute"
- Choosing a self-hosted memory backend over cloud pricing
- Troubleshooting Honcho↔Hermes connection on the n8nserver

## Setup — Honcho (proven path)

### 1. Clone + configure on n8nserver (SSH via Tailscale)
```bash
ssh satyaaditech@100.92.237.45     # TS IP, NOT LAN, NOT Cloudflare
cd ~ && git clone https://github.com/plastic-labs/honcho.git
cd honcho
cp docker-compose.yml.example docker-compose.yml
```

### 2. CRITICAL pitfall — port 8000 is taken
n8nserver port **8000** hosts the user's file-share server (python3, "Share :8000", from memory). **Never** bind Honcho to 8000 — the share breaks / Honcho fails with "address already in use". Move to **8100**:
```bash
sed -i 's/127.0.0.1:8000:8000/0.0.0.0:8100:8000/' docker-compose.yml
```
`0.0.0.0` binding is required so Hermes (other host) can reach it via Tailscale.

### 3. Write `.env` routing LLM to local OmniRoute
OmniRoute runs on n8nserver at `http://100.92.237.45:20128/v1` (OpenRouter-compatible, `/v1/models`). Cheap model = `auto/cheap`. Each text module needs its own `MODEL_CONFIG__MODEL` + `MODEL_CONFIG__OVERRIDES__BASE_URL` (no global default override). Full example in `references/honcho-omniroute-env.md`.

### 4. Start
```bash
docker compose up -d --build   # first run builds; background + notify
```

### 5. Point Hermes at it
- Locate the real Hermes config: `~/.hermes/honcho.json` (set `"baseUrl": "http://100.92.237.45:8100"`, `"environment": "local"`, auth-less).
- **Kill the leftover cloud key**: Hermes writes `HONCHO_API_KEY=hch-v3-...` (cloud) into `~/.hermes/.env`. If not removed, `hermes honcho status` still shows `Auth: API key (...)` and sends the cloud key. Comment it out:
  `sed -i 's|^HONCHO_API_KEY=hch|# HONCHO_API_KEY=hch|' ~/.hermes/.env`
- Verify:
  - `hermes honcho status` → `Auth: API key (not set)` + `OK` (no peer data yet on cold start).
  - On n8nserver: `docker logs honcho-api-1 --since 2m | grep /v3 | grep -v health` → real `/v3/workspaces/hermes/peers/...` requests from Hermes (source IP = Tailscale `100.92.237.45`), proving REAL traffic, not just internal healthchecks.

## Verification signs (green = done)
- `curl -s http://100.92.237.45:8100/health` → `{"status":"ok"}`
- 4 honcho containers up+healthy: `api`, `deriver`, `redis`, `database`
- `hermes honcho status`: Auth "not set", connection OK
- Honcho API logs show non-health `/v3/...` requests from `100.92.237.45`

## Cost reality (be honest with user)
Self-hosted Honcho is free (AGPL-3.0) **BUT** still pays LLM tokens for deriver/dialectic/summary/dream. Routing through the local OmniRoute gateway with `auto/cheap` is the cost lever. There is no full-free option.

## Pitfalls
- Port collision on 8000 (file share) → use 8100.
- Leftover `HONCHO_API_KEY` cloud key in `~/.hermes/.env` silently re-arms cloud → comment out before `honcho status` looks right.
- `MODEL_CONFIG__OVERRIDES__BASE_URL` must be set per module — there is no single global LLM base URL override.
- React/JS sites (honcho.dev, app.honcho.dev) don't scrape cleanly; use the GitHub README (raw.githubusercontent.com) which has the real self-hosting commands.
- SSH from Hermes host can lose its keypair after a daily reset → regenerate `~/.ssh/id_ed25519` and re-add `.pub` to n8nserver `~/.ssh/authorized_keys`. SSH only via Tailscale.