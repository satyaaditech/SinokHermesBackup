# Memory Provider Discovery — Raw Output

Captured from `hermes memory status` on 2026-07-29:

```
Memory status
────────────────────────────────────────
  Built-in (MEMORY.md / USER.md):
    Memory injection:   enabled ✓
    User profile:       enabled ✓
    Memory tool:        enabled ✓
  Provider:  (none — built-in only)

  Installed plugins:
    • byterover  (API key / local)
    • hindsight  (API key / local)
    • holographic  (local)
    • honcho  (API key / local)
    • mem0  (API key / local)
    • openviking  (API key / local)
    • retaindb  (API key / local)
    • supermemory  (requires API key)
```

Provider discovery via `discover_memory_providers()`:

```
byterover: ByteRover — persistent knowledge tree with tiered retrieval via the brv CLI. (available=False)
hindsight: Hindsight — long-term memory with knowledge graph, entity resolution, and multi-strategy retrieval. (available=False)
holographic: Holographic memory — local SQLite fact store with FTS5 search, trust scoring, and HRR-based compositional retrieval. (available=True)
honcho: Honcho AI-native memory — cross-session user modeling with dialectic Q&A, semantic search, and persistent conclusions. (available=False)
mem0: Mem0 — server-side LLM fact extraction with semantic search, automatic deduplication, and opt-in reranking (platform mode). (available=False)
openviking: OpenViking context database — session-managed memory with automatic extraction, tiered retrieval, and filesystem-style knowledge browsing. (available=False)
retaindb: RetainDB — cloud memory API with hybrid search and 7 memory types. (available=False)
supermemory: Supermemory semantic long-term memory with profile recall, semantic search, explicit memory tools, and session ingest. (available=False)
```

## Config Locations

- Hermes config: `~/.hermes/config.yaml` → `memory.provider`
- Honcho config (instance-local): `$HERMES_HOME/honcho.json`
- Honcho config (global): `~/.honcho/config.json`

## Dashboard Config Merging

From `web_server.py`:
- `memory.provider` is a select field populated by `_memory_provider_options()`
- Provider-specific schemas merged via `_memory_provider_schema_options()`
- `_declared_provider_payload()` renders per-provider fields
- Honcho uses `STORAGE_HONCHO_HOST_BLOCK` for host-block config pattern

## Web Dashboard Endpoint

- Default: `http://localhost:9119`
- Config page shows `memory.provider` as dropdown with all discovered providers
