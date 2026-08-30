# Task-Based Routing: Chat vs. Delegation

Details on configuring splitting workloads between lightweight conversational models and heavy reasoning tools in the OmniRoute + Hermes setup.

## 1. Workload Split Strategy

For resource and quality optimization, workloads are split:
- **Daily Conversation & Light Tasks (`model.default`)**: Map to a fast, cost-effective multimodal or natural chat model with fallbacks (e.g., `daily-chat` combo).
- **Subagent Delegation & Deep Work (`delegation.model`)**: Map to a heavyweight reasoning/logic model (e.g., `best-reasoning-v2` combo).

## 2. Actual Model ID vs. Benchmark ELO Metadata

When configuring OmniRoute combos, ensure you use the actual upstream model IDs returned by `/v1/models` rather than global ELO benchmark metadata models.
* *Example Pitfall*: `deepseek-v4-flash-high` is listed in `model_intelligence` for ELO tracking, but the actual callable identifier from the provider is `opencode-go/deepseek-v4-flash`. Always verify names against `/v1/models` first.

## 3. Database Insertion & Priority Fallback

To inject a custom combo directly into `storage.sqlite` without using the dashboard (useful when dashboard access is password-inaccessible or constrained):

```python
import sqlite3, json, uuid
from datetime import datetime, timezone

db = '/home/satyaaditech/.omniroute/storage.sqlite'
con = sqlite3.connect(db)

combo_id = str(uuid.uuid4())
now_str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

# Define fallback order (1 = primary, 2 = fallback, 3 = secondary fallback)
models = [
    {"id": "daily-chat-1", "kind": "model", "model": "antigravity/gemini-3.5-flash-high", "providerId": "antigravity", "connectionId": "5038649b-5021-49f1-80ad-ac8b236f3a2c", "weight": 0, "label": "thefullstackprogrammer@gmail.com"},
    {"id": "daily-chat-2", "kind": "model", "model": "opencode-go/deepseek-v4-flash", "providerId": "opencode-go", "connectionId": "7a3868a9-3cc2-49b3-b04f-7062fb1f6823", "weight": 0, "label": "Account 1"},
    {"id": "daily-chat-3", "kind": "model", "model": "opencode-go/qwen3.7-plus", "providerId": "opencode-go", "connectionId": "7a3868a9-3cc2-49b3-b04f-7062fb1f6823", "weight": 0, "label": "Account 1"}
]

data = {
    "name": "daily-chat",
    "description": "Daily chat & light tasks (priority fallback)",
    "models": models,
    "strategy": "priority",
    "config": {"maxRetries": 2, "retryDelayMs": 1500, "handoffThreshold": 0.85, "handoffModel": "", "maxMessagesForSummary": 30, "trackMetrics": True, "reasoningTokenBufferEnabled": True, "zeroLatencyOptimizationsEnabled": False},
    "id": combo_id,
    "isHidden": False,
    "sortOrder": 3,
    "createdAt": now_str,
    "updatedAt": now_str,
    "version": 2
}

with con:
    con.execute(
        "INSERT INTO combos (id, name, data, sort_order, created_at, updated_at, system_message, tool_filter_regex, context_cache_protection) VALUES (?,?,?,?,?,?,?,?,?)",
        (combo_id, 'daily-chat', json.dumps(data), 3, now_str, now_str, None, None, 0)
    )
```

## 4. Hermes Configuration Contract

Update the corresponding settings inside `~/.hermes/config.yaml`:
```yaml
model:
  default: daily-chat
delegation:
  model: best-reasoning-v2
```
*Note*: No reboot is required for OmniRoute to pick up the new database combo row, and the running Hermes gateway re-reads its config on the next call.
