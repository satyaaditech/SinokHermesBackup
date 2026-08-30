---
name: telegram-bot-api
description: "Use when managing Telegram groups/topics via Bot API."
---

# Telegram Bot API

Direct Bot API calls (curl) for group/topic/platform management — used when the Hermes gateway handles normal chat but you need admin/platform operations: create forum topics, verify bot rights, send into specific threads, manage groups.

## Triggers

- create/make/add a topic (topik) in a Telegram group
- bot needs admin rights, verify bot status in a group
- send message to a specific topic/thread (not General)
- manage group chat: pin, delete, restrict, promote
- any "how do I do X in Telegram Bot API" task

## Prerequisites

- Bot token: read from `~/.hermes/.env` → line `TELEGRAM_BOT_TOKEN=<id>:<secret>` (NOT config.yaml — config.yaml holds no plaintext token). Source it in-shell without echoing the secret: `TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env | cut -d= -f2)`
- `curl` + `python3 -m json.tool` for readable JSON. NOTE: `curl | python3` pipes trigger Hermes security approval — acceptable, just expect the prompt.

## Pitfalls: General topic & pinning (verified 2026-08-10)

- **The General topic is NOT thread 1.** `message_thread_id=1` fails with `Bad Request: message thread not found` even though thread `1` appears in channel_directory. To post to #General, OMIT `message_thread_id` entirely — a bare sendMessage to the group lands in General.
- **Pin a message:** capture `result.message_id` from the sendMessage response, then `curl -s -X POST "https://api.telegram.org/bot$TOKEN/pinChatMessage" -d "chat_id=-100XXX" -d "message_id=<ID>"` (bot must be admin).
- New topic creation returns `result.message_thread_id` — save it to memory + channel_directory + the `telegram-channel-topic-ops` skill topic map so routing recognizes it.
- **Verify a topic/thread exists (verified 2026-08-13):** there is NO listing endpoint — `getForumTopics` returns 404 even on a valid forum. To confirm: `getChat` → `result.is_forum == true` (group supports topics), and read `~/.hermes/channel_directory.json` for thread_ids already in use (entries `-100…:<thread_id>`). Topic NAMES are never exposed by the API — ask the user for the real name.

## Workflow: create a forum topic in a group

1. **Find the group chat ID.** `getUpdates` is usually EMPTY because the Hermes gateway consumes updates. Instead read `~/.hermes/channel_directory.json` — entries like `"-1003256146835:433"` = `chat_id:thread_id`, with human-readable names ("HERMES GROUP CHAT / topic 10").
2. **Verify forum mode + bot rights:**
   ```
   curl -s "https://api.telegram.org/bot$TOKEN/getChat?chat_id=-100XXX" | python3 -m json.tool
   # result.is_forum == true  → topics enabled
   curl -s "https://api.telegram.org/bot$TOKEN/getChatMember?chat_id=-100XXX&user_id=<BOT_ID>" | python3 -m json.tool
   # result.status == "administrator" AND result.can_manage_topics == true
   ```
3. **Create the topic:**
   ```
   curl -s -X POST "https://api.telegram.org/bot$TOKEN/createForumTopic" \
     -d "chat_id=-100XXX" \
     -d "name=🩺 Rekap Tekanan Darah" \
     -d "icon_color=16729490"
   ```
   Response carries `message_thread_id` — that is the topic's ID, used for every message in that topic.
4. **Post into the topic** (REQUIRES `message_thread_id` or the message lands in General):
   ```
   curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
     -d "chat_id=-100XXX" \
     -d "message_thread_id=<thread_id>" \
     -d "parse_mode=HTML" \
     -d "text=..."
   ```

## Pitfalls

- **400 "not enough rights to create a topic"** — bot is not admin, or admin without Manage Topics. Fix: ask user to promote the bot in group settings (Edit → Administrators → Add Admin → check **Manage Topics**). Re-verify with getChatMember before retrying.
- **Invalid `icon_color` is silently replaced** with default blue (0x6FB9F0) — no error. Valid values: 0x6FB9F0 blue, 0x7DCFB6 green, 0xFFC67D orange, 0xFF8595 red, 0x8A95F1 purple, 0xFF94A2 pink, 0x87CDFB, 0xCFE784, 0xFFD8E1.
- **`getUpdates` returns empty** when the Hermes gateway is polling — never rely on it for chat IDs; use `channel_directory.json`.
- **`getMe().has_topics_enabled`** describes the bot client config, NOT whether a chat has topics — check the chat via getChat.
- Topic messages need `message_thread_id`; omitting it posts to General, which is usually not what the user wants.

## Verified example

2026-08-06: created topic "🩺 Rekap Tekanan Darah" in HERMES GROUP CHAT (-1003256146835). First attempt → 400 "not enough rights" (bot wasn't admin); user promoted bot with Manage Topics; retry → thread 433. Protocol message posted with parse_mode=HTML, then a Google Sheet was linked for data capture.
