---
name: hermes-memory-providers
description: Configure Hermes memory providers via CLI or dashboard.
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos]
---

# Hermes Memory Providers

Configure external memory providers for Hermes — Honcho, Mem0, Holographic, and others — on top of built-in MEMORY.md/USER.md storage.

## When to Use

- User wants to switch from built-in memory to an external provider
- User asks about Honcho, Mem0, or other memory backends
- User needs to check which providers are available/configured
- Troubleshooting memory provider connection issues

---

## 1. Check Current Status

```bash
hermes memory status
```

Output shows:
- Built-in status (enabled/disabled)
- Current provider (or "none — built-in only")
- Installed plugins with availability flags

**Pitfall:** "Installed" ≠ "Available". A provider shows `available=False` until credentials/config are set.

---

## 2. Discover Available Providers

```python
from plugins.memory import discover_memory_providers
for name, desc, avail in discover_memory_providers():
    print(f"{name}: {desc} (available={avail})")
```

Providers bundled with Hermes:
| Provider | Type | Notes |
|----------|------|-------|
| honcho | API key / local | AI-native memory, cross-session user modeling. **Base URL**: kosongkan untuk cloud (app.honcho.dev), isi hanya jika self-hosted. Open source (Apache 2.0) — cloud pakai API key dari app.honcho.dev, self-hosted gratis 100% via Docker. |
| mem0 | API key / local | Server-side LLM fact extraction |
| holographic | local | SQLite FTS5 + trust scoring |
| supermemory | API key | Semantic long-term memory |
| retaindb | API key | Cloud memory API, hybrid search |
| openviking | API key / local | Session-managed, tiered retrieval |
| byterover | API key / local | Persistent knowledge tree |
| hindsight | API key / local | Knowledge graph + entity resolution |

---

## 3. Configure via CLI

```bash
hermes memory setup
```

Interactive radio picker → select provider → follow prompts. Select empty `""` to revert to built-in only.

---

## 4. Configure via Web Dashboard

Dashboard at `http://localhost:9119` → navigate to **Settings** → search for `memory.provider`:
1. Select provider from dropdown
2. Fill provider-specific fields (API key, base URL, environment, etc.)
3. Save — Hermes switches immediately without restart

The dashboard renders provider-specific config panels dynamically based on each provider's `config_schema.py`.

---

## 5. Honcho Provider Details

Honcho is an AI-native memory provider for Hermes with cross-session user modeling, dialectic Q&A, semantic search, and persistent conclusions.

### Availability Check

Honcho shows `available=True` only when BOTH `enabled=True` AND (`api_key` OR `base_url`) is set:

```python
cfg.enabled and bool(cfg.api_key or cfg.base_url)
```

**Pitfall:** Installing the `honcho` Python SDK makes the plugin visible in `hermes memory status` but it stays `available=False` until credentials/config are configured.

### Config File Resolution Order

1. `$HERMES_HOME/honcho.json` — profile-scoped (most specific, enables isolated Hermes instances)
2. `~/.hermes/honcho.json` — default profile fallback
3. `~/.honcho/config.json` — global, shared across all Honcho-enabled apps
4. Environment variables — `HONCHO_API_KEY`, `HONCHO_ENVIRONMENT`, `HONCHO_BASE_URL`

If none exist, first-time writes go to `~/.honcho/config.json`.

### Cloud vs Self-Hosted

| Mode | Config Needed | RAM Impact | Notes |
|------|--------------|------------|-------|
| **Cloud** | `apiKey` | None (offloaded) | Sign up at https://app.honcho.dev |
| **Self-hosted** | `baseUrl` + `environment: local` | Hosting server RAM | Auto-detects local IPs (localhost, 192.168.x.x, 10.x.x.x, 100.64.x.x/Tailscale) |

### Manual Config (Non-Interactive)

When the TUI `hermes memory setup` isn't viable (headless/cron/pipe), configure directly:

**Step 1 — Create `~/.hermes/honcho.json`:**

For cloud:
```json
{
  "hosts": {
    "hermes": {
      "environment": "production",
      "apiKey": "your-api-key"
    }
  }
}
```

For self-hosted:
```json
{
  "hosts": {
    "hermes": {
      "environment": "local",
      "baseUrl": "http://localhost:8000"
    }
  }
}
```

**Step 2 — Set provider in `~/.hermes/config.yaml`:**
```yaml
memory:
  provider: honcho
```

**Step 3 — Verify:**
```bash
hermes memory status
```

### Dashboard Config Path

Via dashboard (`http://localhost:9119`) → **Settings → Config**:
- `memory.provider` dropdown → select "honcho"
- Honcho-specific credentials (apiKey, baseUrl) go in `honcho.json`, not config.yaml
- If dashboard doesn't expose Honcho fields, create `honcho.json` manually

### Single-User Optimization

Set `pinPeerName: true` in the host block to keep memory unified across platforms:

```json
{
  "hosts": {
    "hermes": {
      "pinPeerName": true
    }
  }
}
```

### Config Fields

- `environment`: `production` (cloud → `https://api.honcho.dev`) or `local` (self-hosted)
- `apiKey`: Cloud API key from [app.honcho.dev](https://app.honcho.dev)
- `baseUrl`: Self-hosted URL (overrides environment-derived URL when set)

### OAuth Browser Flow

- `begin_authorization` opens browser to `app.honcho.dev/authorize`
- Loopback listener on `http://127.0.0.1:8765/callback` receives the code
- `complete_authorization` exchanges code for token, stores in `honcho.json` host block
- No CLI step needed — fully browser-based

### Host Keys (Multi-Profile)

Each Hermes profile gets its own Honcho host key:
- `default` profile → host key `hermes`
- Other profiles → host key `hermes_<profile_name>` (sanitized)

---

## 6. Troubleshooting

**Provider not available despite being installed:**
- Check credentials: most providers need API key or base URL
- For Honcho: run `hermes memory setup`, select honcho, complete OAuth flow

**Dashboard doesn't show provider:**
- Provider may not be bundled; check `hermes plugins list`
- Memory providers are separate from general plugins — scan via `plugins.memory`

**Revert to built-in:**
```bash
# Via CLI
hermes memory setup   # select ""

# Via config edit
# Set memory.provider: "" in ~/.hermes/config.yaml
```

---

## Related

- `references/provider-discovery.md` — raw output from `hermes memory status` and `discover_memory_providers()`
- `hermes-agent` skill: general configuration and CLI
- `hermes-administration` skill: backup, disaster recovery, profile management
- Honcho docs: https://docs.honcho.dev/v3/guides/integrations/hermes
