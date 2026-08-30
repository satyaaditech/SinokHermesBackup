#!/usr/bin/env bash
# telegram-send.sh — Reliable Telegram message sender using direct Bot API.
# Use when Hermes cron delivery pipeline fails to deliver to Telegram.
#
# Usage:
#   telegram-send.sh "Your message here"
#   telegram-send.sh -f /path/to/message.txt
#   telegram-send.sh -s "[CRON]" "Your message"
#
# The script auto-extracts TELEGRAM_BOT_TOKEN from ~/.hermes/.env (handles
# masked display by reading raw bytes) and CHAT_ID from TELEGRAM_HOME_CHANNEL.

set -euo pipefail

ENV_FILE="${ENV_FILE:-$HOME/.hermes/.env}"
TOKEN=""
CHAT_ID=""
SUBJECT=""
MESSAGE=""

# ── Parse args ─────────────────────────────────────────────────────
while getopts "f:s:hv" opt; do
  case $opt in
    f) MESSAGE=$(cat "$OPTARG") ;;
    s) SUBJECT="$OPTARG" ;;
    h)
      echo "Usage: $(basename "$0") [-s subject] [-f file] [message]"
      echo "  -s SUBJECT   prepend subject line"
      echo "  -f FILE      read message body from file"
      echo "  -h           show this help"
      exit 0
      ;;
    v) set -x ;;
    *) exit 1 ;;
  esac
done
shift $((OPTIND - 1))

if [[ -z "${MESSAGE:-}" && $# -gt 0 ]]; then
  MESSAGE="$*"
fi

if [[ -z "${MESSAGE:-}" ]]; then
  echo "Error: no message provided." >&2
  exit 1
fi

if [[ -n "$SUBJECT" ]]; then
  MESSAGE="${SUBJECT}

${MESSAGE}"
fi

# ── Extract credentials ────────────────────────────────────────────
if [[ -f "$ENV_FILE" ]]; then
  # Read raw bytes to bypass any terminal masking
  TOKEN=$(sed -n '/^TELEGRAM_BOT_TOKEN=/{s/^TELEGRAM_BOT_TOKEN=//p;q}' "$ENV_FILE")
  CHAT_ID=$(sed -n '/^TELEGRAM_HOME_CHANNEL=/{s/^TELEGRAM_HOME_CHANNEL=//p;q}' "$ENV_FILE")
fi

if [[ -z "$TOKEN" ]]; then
  echo "Error: TELEGRAM_BOT_TOKEN not found in $ENV_FILE" >&2
  exit 1
fi

if [[ -z "$CHAT_ID" ]]; then
  CHAT_ID="777961507"  # fallback for Satya's chat
fi

# ── Send ───────────────────────────────────────────────────────────
RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  -d "text=${MESSAGE}")

if echo "$RESPONSE" | grep -q '"ok":true'; then
  echo "✅ Message delivered to Telegram (chat_id=$CHAT_ID)"
else
  echo "❌ Delivery failed: $RESPONSE" >&2
  exit 1
fi
