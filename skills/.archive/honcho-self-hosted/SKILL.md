---
name: honcho-self-hosted
description: Self-host Honcho memory via Docker. Use OpenRouter for LLM.
version: 1.0.0
category: devops
platforms: [linux]
---

# Honcho Self-Hosted

Deploy Honcho memory server on your own Linux server via Docker and connect it to Hermes.

## When to Use

- User wants free/self-hosted Honcho instead of cloud (app.honcho.dev)
- Setting up Honcho on n8nserver or any Linux server
- Configuring OpenRouter/OmniRoute as the LLM backend for Honcho
- Hermes needs to reach a self-hosted Honcho instance

## Prerequisites

- Server with Docker + Docker Compose, ≥ 2 GB RAM, ≥ 3 GB free disk
- LLM API key (Honcho needs LLM for dialectic reasoning — it calls an LLM to analyze conversations)
- Hermes host can reach the server (Tailscale, LAN, etc.)

## Step 1: Clone & Prepare

```bash
git clone https://github.com/plastic-labs/honcho.git
cd honcho
cp docker-compose.yml.example docker-compose.yml
```

**Pitfall:** The default `docker-compose.yml` binds to `127.0.0.1:8000`. Change to `0.0.0.0:8000` so Hermes can reach it from other machines.

## Step 2: Configure LLM Backend

Honcho uses LLMs for deriver, dialectic, summary, and dream modules. Each module needs its own `MODEL_CONFIG__OVERRIDES__BASE_URL` when not using native OpenAI.

### For OpenRouter / OmniRoute (OpenAI-compatible)

Create `.env` — see `references/honcho-env-template.env` for the full ready-to-copy template.

Key points:
- `LLM_OPENAI_API_KEY` = your OpenRouter API key
- All modules override base URL to `https://openrouter.ai/api/v1`
- Recommended cheap model: `google/gemini-2.0-flash-001` (supports function calling)
- **Pitfall:** ALL five dialectic levels (minimal→max) must be overridden. Missing one causes fallback to native OpenAI and failure.

## Step 3: Start

```bash
docker compose up -d
```

**Pitfall on `.env` updates:** `docker restart` does NOT reload `.env` file changes into existing containers. Always run `docker compose up -d --force-recreate api deriver` after editing `.env`.
```

Wait for `api` and `deriver` services to show healthy.

## Step 4: Connect Hermes

In Hermes dashboard → Runtime Provider Plugins:
- **Memory Provider**: `honcho`
- **API Key**: kosongkan (self-hosted tanpa auth by default)
- **Base URL**: `http://<server-ip>:8000` (e.g. `http://192.168.0.112:8000`)
- Click **SAVE MEMORY PROVIDER**

Verify:
```bash
hermes memory status
# should show: Provider: honcho ✓
```

## Pitfalls

1. **Port binding**: Default docker-compose binds `127.0.0.1` — unreachable from LAN. Must change to `0.0.0.0`.
2. **API key masking**: Hermes masks API keys. Cannot extract full key programmatically for use in other configs. User must manually enter in `.env`.
3. **SSH key loss after daily reset**: Hermes host SSH keys may disappear on session reset. Regenerate with `ssh-keygen -t ed25519` and re-add to target `~/.ssh/authorized_keys`.
4. **Model must support function calling**: Honcho requires tool-calling capable models. Cheapest OpenRouter option: Gemini Flash.
5. **All modules need override**: Every Honcho module (deriver, dialectic×5, summary, dream×2, embedding) needs its own `_MODEL_CONFIG__OVERRIDES__BASE_URL`. No global fallback.

## See Also

- `hermes-memory-providers` skill — Hermes-side memory provider config
- `references/honcho-env-template.env` — full `.env` template ready to copy
