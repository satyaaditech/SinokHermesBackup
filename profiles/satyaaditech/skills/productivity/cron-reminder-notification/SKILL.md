---
name: cron-reminder-notification
description: Create reliable reminder/notification cron jobs that always deliver. Solves the [SILENT] suppression issue where default cron prompts cause delivery to be blocked.
version: 1.0.0
author: Hermes Agent
tags: [cron, reminder, notification, telegram]
---

# Cron Reminder & Notification Skill

Use this skill whenever creating a reminder, alarm, or notification-style cron job to ensure it actually delivers.

## The Problem

Cron jobs run in isolated sub-agents with default prompts that may cause `[SILENT]` responses for monitoring-style tasks. When a cron agent responds with `[SILENT]`, Hermes **suppresses delivery entirely** — the user never gets the notification.

**CRITICAL LIMITATION:** Cron sub-agents do NOT have access to the `send_message` tool (or most other tools). They can only produce output as their final response, which Hermes auto-delivers.

## The Solution

When creating reminder/notification cron jobs, ALWAYS use explicit language in the prompt:

### ✅ Good Prompt Patterns

**Pattern: Write output as final response (Hermes auto-delivers)**

```
Ini adalah test cron job reminder untuk Satya.

TUGAS KAMU:
Produksikan pesan berikut SEBAGAI FINAL RESPONSE kamu (jangan pakai send_message, jangan pakai tool apapun):

================================================================
🧪 [DUMMY TEST REMINDER]
Halo Satya! Ini adalah test cron job reminder.
Waktu sekarang: (sebutkan hari, tanggal, jam dan menit)
Jika kamu menerima pesan ini, berarti cron job BERHASIL! ✅
================================================================

CATATAN PENTING:
- Jangan gunakan tool send_message (tidak tersedia di cron job)
- Jangan gunakan [SILENT]
- Tulis output di atas SEBAGAI FINAL RESPONSE kamu
- Hermes akan otomatis deliver final response kamu ke Telegram user
```

**Key points:**
- Tell agent to write output as **FINAL RESPONSE**
- Explicitly say **JANGAN pakai send_message** (not available)
- Hermes auto-delivers final response to `--deliver` target
- No tools needed — just produce text output

### ❌ Bad Prompt Patterns

**Pattern: Trying to use send_message tool (WILL FAIL)**

```
Kirim pesan ke Telegram user dengan send_message:
send_message action='send' target='telegram:777961507' message='Reminder!'
```

**Why this fails:**
- Cron sub-agents do NOT have `send_message` tool available
- Agent will search for alternative methods and fail
- Job appears to run (`last_status: ok`) but no delivery
- Session logs show agent confused about missing tool

**Pattern: Too vague, can trigger [SILENT]**

```
"Remind user to brush teeth"  ← Too vague, can trigger [SILENT]
```

## Why This Happens (Root Causes)

**1. Default LLM Prompt Designed for Monitoring**
> "If the agent's final response starts with [SILENT], delivery is suppressed entirely."

Default cron behavior: **lapor HANYA kalau ada masalah** (monitoring).
Reminder behavior: **lapor SETIAP KALI** (notification).

Konflik ini yang menyebabkan [SILENT].

**2. Origin NULL**
Job tidak punya info destination chat → pesan tidak tahu dikirim kemana.
Fix: Selalu gunakan `--deliver origin` saat create.

**3. Lock File Stuck**
Cron engine tidak trigger job.
Fix: `rm -f /root/hermes_cli/hermes/data/hold.lock`

## Debugging Workflow (Lessons Learned)

**Case Study: Test reminder tidak terkirim (April 2026)**

**Symptoms:**
- Job created successfully, status `scheduled`
- Job never executed (`last_run_at: null`)
- Manual `hermes cron tick` ran but no delivery

**Investigation Steps:**

```bash
# 1. Check job status
hermes cron list

# 2. Check cron engine status
hermes cron status

# 3. Check logs for job execution
hermes logs --lines 100 | grep -i cron

# 4. Check session output
ls ~/.hermes/sessions/session_cron_<job_id>*.json

# 5. Read session to see what agent tried
cat ~/.hermes/sessions/session_cron_<job_id>*.json | grep -i "send_message\|SILENT"
```

**Root Cause Found:**
- Job DID run (logs showed `Running job 'Test Reminder'`)
- But sub-agent had NO `send_message` tool available
- Agent spent 50+ turns searching for Telegram delivery method
- Session ended without producing final response

**Fix Applied:**
- Changed prompt to explicitly say "JANGAN pakai send_message"
- Tell agent to "write output as FINAL RESPONSE"
- Hermes auto-delivers final response to `--deliver` target

**Key Lesson:** Cron sub-agents are ISOLATED with limited tools. Never assume tools available in main agent are available in cron jobs.

After creating a reminder cron job:
1. Check `~/.hermes/cron/output/{job_id}/` after the job runs
2. If the `.md` file shows `[SILENT]` as the response, the prompt needs to be more explicit
3. Recreate with explicit "must send" instructions

## Automation: Shell Function (Recommended)

Tambahkan ke `~/.bashrc` atau `~/.zshrc` untuk otomatis inject instruksi PERHATIAN:

```bash
reminder() {
  local schedule="$1"
  local name="$2"
  local message="$3"
  
  hermes cron create "$schedule" \
    "${message}

    PERHATIAN:
    - Pesan ini WAJIB dikirim ke user
    - Tidak boleh kosong
    - Tidak boleh [SILENT]
    - Harus sampai ke Telegram user" \
    --name "$name" \
    --deliver origin
}
```

**Cara pakai:**
```bash
reminder "30m" "Meeting" "🔔 Reminder: Waktunya meeting!"
reminder "1h" "Cek Email" "📧 Jangan lupa cek email!"
reminder "0 7 * * *" "Olahraga" "☀️ Waktu olahraga pagi!"
```

## Workaround: Direct Telegram API (Most Reliable)

Jika cron engine bermasalah, kirim langsung via Telegram Bot API:

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=777961507&text=🔔 Reminder!"
```

Atau buat cron Linux tradisional di crontab:
```bash
crontab -e
# Tambahkan:
*/30 * * * * curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=777961507&text=Reminder"
```

### Preferred: `hermes send` (No LLM, No Agent Loop)

The `hermes send` command reuses the gateway's Telegram credentials and bypasses the cron delivery pipeline entirely. It is the most reliable method when Hermes cron jobs fail to deliver.

```bash
# Send a simple message
hermes send --to telegram "🔔 Reminder: Your message here"

# Send to specific chat ID
hermes send --to telegram:777961507 "🔔 Reminder"

# Send with subject line
hermes send --to telegram --subject "[CRON]" --file /path/to/message.md

# Send from stdin
echo "🔔 Reminder" | hermes send --to telegram
```

**Why this is preferred over curl:**
- Reuses credentials from `~/.hermes/.env` (no manual token management)
- No risk of token masking issues (`.env` may display `867975...tlvM` but `hermes send` reads the real value)
- Exit code 0 = delivered, exit code 1 = delivery error
- No LLM call, no agent loop — pure API passthrough

**Note:** When running inside a cron job context, `hermes send` may print:
> "Skipped send_message to telegram:777961507. This cron job will already auto-deliver its final response to that same target."

In that case, put the content in your final response instead, or use direct curl as fallback.

Use the `hermes cron create` CLI command** (the `hermes_tools` module is not a real Python package — its example code below is non-functional):

```bash
hermes cron create "5m" \
  '🦷 Waktunya Gosok Gigi! Sudah 5 menit berlalu.

PERHATIAN:
- Pesan ini WAJIB dikirim ke user
- Tidak boleh kosong
- Tidak boleh [SILENT]
- Pastikan pesan ini sampai ke chat Telegram user' \
  --name "Reminder Gosok Gigi" \
  --deliver origin \
  --skill cron-reminder-notification
```

## User Preference (Satya Adi Dharma)

**Setiap reminder/cron job HARUS:**
- Selalu kirim pesan ke Telegram (chat ID: 777961507)
- Tidak boleh [SILENT]
- Tidak boleh kosong
- Prompt harus eksplisit: "tidak boleh [SILENT], tidak boleh kosong, harus dikirim"

Preference ini sudah disimpan di memory Hermes dan berlaku untuk SEMUA reminder jobs.

**Job berjalan tapi tidak terkirim:**
```bash
# Cek origin null
cat /root/hermes_cli/hermes/data/jobs.json | grep -A5 "<job_id>"

# Cek lock file stuck
ls -la /root/hermes_cli/hermes/data/*.lock
rm -f /root/hermes_cli/hermes/data/hold.lock

# Cek output logs
cat ~/.hermes/cron/output/<job_id>/*.md
```

**Jika masih [SILENT]:**
1. Recreate job dengan prompt lebih eksplisit
2. Attach skill ini: `--skill cron-reminder-notification`
3. Gunakan workaround curl langsung ke Telegram API

**Verification setelah create:**
```bash
hermes cron list
# Cek last_status dan last_delivery_error
```
- ✅ `"5m"` — 5 minutes from now (one-shot)
- ✅ `"every 2h"` — recurring every 2 hours  
- ✅ `"0 9 * * *"` — cron expression (daily at 9 AM)
- ❌ `"now + 5m"` — **invalid** format

If you need to create jobs programmatically (e.g. from within the hermes-agent codebase itself), use the internal API via the hermes CLI's Python environment, not a standalone Python script.
