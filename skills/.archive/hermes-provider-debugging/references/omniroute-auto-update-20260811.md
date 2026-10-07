# OmniRoute Auto-Update Incident — 11 Aug 2026

## Timeline

| Time | Event |
|------|-------|
| ~12:38 | OmniRoute npm auto-update → v16.2.10 starts (PID 164668) |
| 12:38:25 | New process takes over port 20128 |
| ~12:38-12:42 | Brief outage during port transition; Hermes session mid-request |
| 12:42:33 | Gateway receives user message: "Kenapa begini lagi ya : ⚠️ The model provider failed..." |
| 12:42 | Session auto-reset by daily schedule; new session starts |
| Current | OmniRoute healthy, port 20128 responds HTTP 200 |

## Root Cause

OmniRoute auto-updated to v16.2.10. During the restart, port 20128 was briefly unavailable. Hermes retried 3x (`api_max_retries: 3` in config.yaml), then showed the "model provider failed after retries" error to the user.

**Contributing factor**: `fallback_providers: []` is empty — no backup provider configured.

## Zombie Process

After the update, old OmniRoute process (PID 871, started Aug 4, elapsed 6 days) remained alive but held NO ports:

```
PID     STAT   ELAPSED     CMD
871     Ssl    6-18:26:23  node .../omniroute serve --port 20128
```

`ss -tlnp | grep 871` returned nothing — confirmed zombie. Safe to kill but was left running during investigation.

## Diagnostic Commands Used

```bash
# Check port ownership
ss -tlnp | grep -E "20128|omniroute"

# Find all OmniRoute processes
ps -eo pid,lstart,etime,cmd | grep omniroute | grep -v grep

# Test inference
curl -s http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OMNIROUTER_API_KEY" \
  -d '{"model":"auto/best-reasoning","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'

# Gateway log search
grep -n -i "provider.fail\|api.error\|retry\|non.200" ~/.hermes/logs/gateway.log | tail -20
grep -c "ended in state.db but still live" ~/.hermes/logs/gateway.log  # result: 19
```

## Key Config (relevant snippet)

```yaml
model:
  default: auto/best-reasoning
  provider: custom
  base_url: http://localhost:20128/v1
  api_key: ${OMNIROUTER_API_KEY}
fallback_providers: []
agent:
  api_max_retries: 3
  gateway_timeout: 1800
```

## Recurring Pattern

Previous session (Aug 10) identified: OmniRoute sometimes routes `auto/best-reasoning` to free/inactive OpenCode models → "Provider auth failed". This has happened multiple times. The auto-update outage is a separate but complementary trigger.
