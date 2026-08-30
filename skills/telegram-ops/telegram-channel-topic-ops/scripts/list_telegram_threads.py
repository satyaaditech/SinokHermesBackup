#!/usr/bin/env python3
"""List all Telegram group threads known to Hermes (chat_id, thread_id, display_name).

Authoritative source: ~/.hermes/state.db sessions table.
Usage: python3 list_telegram_threads.py [path-to-state.db]
"""
import sqlite3
import sys
import os

db_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.hermes/state.db")
if not os.path.exists(db_path):
    print(f"state.db not found: {db_path}")
    sys.exit(1)

db = sqlite3.connect(db_path)
rows = db.execute("""
    SELECT DISTINCT chat_id, thread_id, display_name
    FROM sessions
    WHERE source = 'telegram' AND chat_type = 'group'
    ORDER BY chat_id, thread_id
""").fetchall()
db.close()

print(f"{'chat_id':<20} {'thread':<8} group/topic name")
print("-" * 55)
for chat_id, thread_id, display_name in rows:
    print(f"{chat_id:<20} {str(thread_id or '-'):<8} {display_name}")

if not rows:
    print("(no telegram group threads found)")
