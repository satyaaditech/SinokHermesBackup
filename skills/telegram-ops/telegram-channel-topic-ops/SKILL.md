---
name: telegram-channel-topic-ops
description: Verify Telegram forum topic membership for routing.
version: 1.0.0
platforms: [linux]
---

# Telegram Channel & Forum Topic Ops

Class-level skill for inspecting Telegram group/forum-topics and mapping them for Hermes delivery routing.

## When to Use

- User asks "which groups/topics is the bot in?" or "can you see this topic?"
- User wants to verify membership, enumerate active topics, or route messages to a specific topic (`telegram:<chat_id>:<thread_id>`)
- User reports a topic exists but Hermes doesn't seem to know it

## Key Facts (verified 2026-08)

1. **Bot API has NO forum-topic listing endpoint.** `getForumTopics?chat_id=X` returns HTTP 404. Topic NAMES are never exposed by the API.
2. Topic membership is not per-topic — a bot that is a group member can receive from any topic where it's mentioned. Only *which topics have been used* is observable, via Hermes state.
3. Hermes registers channels in `~/.hermes/channel_directory.json`, entries keyed `chat_id:thread_id` (e.g. `-1003256146835:44`). The directory can lag — the currently-active topic may not appear until a message round-trips.
4. Session titles are auto-generated summaries, NOT topic names. Always ask the user to confirm the real topic name, then save to memory.
5. **General topic ≠ thread 1.** `sendMessage` dengan `message_thread_id=1` bisa gagal dengan "message thread not found" padahal itu #General. Kirim ke General dengan **tanpa** `message_thread_id` sama sekali. (Verified 2026-08-10: thread 1 ditolak, tanpa thread id sukses.)
6. **Pin message workflow:** `sendMessage` → ambil `result.message_id` → `pinChatMessage` (chat_id + message_id). Ganti pin lama: `unpinChatMessage` dulu. Verifikasi via `getChat` → `result.pinned_message.message_id`.

## Confirmed Topic Map (updated 2026-09-06)

- **HERMES GROUP CHAT** (`-1003256146835`):
  - thread `1` = **General / Obrolan Utama**
  - thread `10` = **🌱 Urban Farming & Tanaman Herbal**
  - thread `12` = **🤖 Mastering AI & Tools**
  - thread `14` = **💡 Brainstorming**
  - thread `44` = **🚶♂️ Walking Vlog & Content Creator Storytelling**
  - thread `433` = **🩺 Rekap Tensi Darah & Kesehatan** (Omron HEM-7120 → Sheets)
  - thread `1014` = **💰 Rekap Pengeluaran & Finansial** (Nota/struk → Sheets)
  - thread `1096` = **🕊️ Pangestu & Renungan Harian** (Piwulang SGS, Daily Bread)
  - thread `3443` = **🏋️♂️ Gym & Workout Tracking** (Sel/Kam/Sab 05:00)
  - thread `4038` = **🖥️ Server, Domain & Infrastruktur** (n8n, satyaaditech.web.id)
  - thread `4305` = **💵 Bisnis & Monetisasi Digital** (Google AI / Blue Ocean dollar market)
- **My Sinox Agents** (`-1003980421737`): thread `1`, `3`
- **Satya AI Labs** (`-1003981550688`): thread `1`, `2`, `182`

Update section ini setiap kali user mengonfirmasi nama topic baru, lalu sinkronkan juga ke memory.

## Steps to Verify Membership / Enumerate Topics

1. `getChat?chat_id=<id>` → ok:true means bot has access; `getChatMemberCount?chat_id=<id>` confirms member count.
2. Read `~/.hermes/channel_directory.json` for registered channels.
3. Query `~/.hermes/state.db` sessions table for all telegram group threads (see script below) — authoritative list of every thread ever used.
4. Report thread ids + last session titles; ask user to confirm topic names.

## Routing

- Deliver to a specific topic: `telegram:<chat_id>:<thread_id>` (e.g. `telegram:-1003256146835:44`). Without `:<thread_id>` you lose topic targeting.
- Bot API note: group id is negative, e.g. `-1003256146835`.

## Pitfalls

- `sqlite3` CLI is often NOT installed on this server — use the Python module (`python3 -c` or scripts/).
- `state.db` session titles ≠ topic names (auto-generated from conversation, can be stale/wrong — e.g. a "Mastering AI" topic showed a title about storytelling).
- Channel directory entries use format `chat_id:thread_id` as the id field — parse on the LAST colon, not the first.

## Support Files

- `scripts/list_telegram_threads.py` — re-runnable: dumps all telegram group chat_id/thread_id/display_name from state.db
- `references/telegram-channel-inspection.md` — exact curl commands + state.db schema notes
