# Telegram Channel Inspection — Exact Commands (verified 2026-08)

## 1. Verify group access & membership (Bot API)

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getChat?chat_id=-1003256146835"
# -> {"ok":true,"result":{"id":-1003256146835,"title":"HERMES GROUP CHAT","is_forum":true,"type":"supergroup",...}}

curl -s "https://api.telegram.org/bot<TOKEN>/getChatMemberCount?chat_id=-1003256146835"
# -> {"ok":true,"result":3}
```

## 2. Listing forum topics — NOT possible

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getForumTopics?chat_id=-1003256146835"
# -> {"ok":false,"error_code":404,"description":"Not Found"}
```

The public Bot API has NO endpoint to list a group's forum topics. Topic names are
never exposed. Workaround: enumerate threads from Hermes state (below), then ask the
user to confirm topic names.

## 3. Registered channels (Hermes)

`~/.hermes/channel_directory.json` — entries keyed `chat_id:thread_id`:

```json
{"id": "-1003256146835:44", "name": "HERMES GROUP CHAT / topic 44", "type": "group", "thread_id": "44"}
```

Note: directory can lag; an active topic may be missing until a message round-trips.

## 4. Authoritative thread list (Hermes state.db)

`sqlite3` CLI is often absent — use Python module:

```python
import sqlite3
db = sqlite3.connect('/home/<user>/.hermes/state.db')
for r in db.execute("""
    SELECT DISTINCT chat_id, thread_id, display_name FROM sessions
    WHERE source='telegram' AND chat_type='group'
    ORDER BY chat_id, thread_id"""):
    print(r)
```

Also useful: latest activity per thread:

```sql
SELECT id, chat_id, thread_id, display_name, title, started_at
FROM sessions
WHERE chat_id = '<group_id>'
ORDER BY started_at DESC;
```

## 5. Key schema facts

- `sessions` table columns: `id, source, user_id, chat_id, chat_type, thread_id, display_name, title, started_at, message_count, ...`
- `chat_id` = negative group id (e.g. `-1003256146835`); `thread_id` = topic number (e.g. `12`, `44`)
- `title` = auto-generated session title, NOT the Telegram topic name (can be stale/misleading)
- `gateway_routing` table holds live routing index; `sessions.json` in ~/.hermes/sessions is a LEGACY mirror

## 6. Example mapping (HERMES GROUP CHAT, 2026-08-06)

| thread | confirmed topic name |
|--------|----------------------|
| 12     | Mastering AI         |
| 1      | (ask user)           |
| 44     | (ask user)           |
