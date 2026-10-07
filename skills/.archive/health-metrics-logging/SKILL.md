---
name: health-metrics-logging
description: "Log blood pressure/vitals from photos to Google Sheets."
version: 1.0.0
author: Sinok (Hermes Agent)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [health, vitals, blood-pressure, tensi, google-sheets, logging]
    related_skills: [google-workspace]
---

# Health Metrics Logging

Log recurring health readings — currently blood pressure (tensi) — to Google Sheets when the user sends a photo of a monitor or types values in the dedicated Telegram topic.

## Triggers

- Photo of blood pressure monitor (Omron HEM-7120 etc.) — topic TG -1003256146835:433 OR DM
- Typed values like "155/86/94" or mentions: tensi, tekanan darah, nadi, denyut, cek tensi

## Current Setup

- Sheet: `1n3BowI-SLk1OP3FcYIVbEpv92olZ7v_VkpTcorkdXGM`
- Tab: `Tensi Harian`
- Input channel: Telegram group -1003256146835, topic 433
- CLI: `SKILL=/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts; python3 $SKILL/google_api.py sheets ...`

## Column Structure (Tensi Harian)

`Tanggal | Waktu | Sistolik | Diastolik | Nadi | Keterangan | Sumber`

## Response Format & Style

When logging blood pressure, always respond in Javanese Krama Alus using this exact template. Adjust the greeting (Sugeng enjang/siang/sore/sonten) based on the current time of day:

```
Sugeng [enjang/siang/sore/sonten], Pak Satya. Data tensi sampun kula serat wonten spreadsheet:

• Sistolik: <systolic> mmHg
• Diastolik: <diastolic> mmHg
• Nadi: <pulse> bpm
• Tanggal: <day> <Month in Indonesian> <year>
• Wanci: <HH:MM> WIB

Matur nuwun, Pak.
```

## Steps

1. **Read the photo** — extract SYS (sistolik), DIA (diastolik), PULSE (nadi). Use vision_analyze with the cached image path if you need a closer look.
2. **Get current date/time via code, never mentally** (ZERO TOLERANCE rule): `python3 -c "from datetime import datetime, timedelta; print(datetime.now().strftime('%Y-%m-%d %H:%M'))"`
3. **Verify column layout** (optional, first time per sheet): `python3 $SKILL/google_api.py sheets get 1n3BowI-SLk1OP3FcYIVbEpv92olZ7v_VkpTcorkdXGM "Tensi Harian!A1:J20"`
4. **Append row**:
   `python3 $SKILL/google_api.py sheets append 1n3BowI-SLk1OP3FcYIVbEpv92olZ7v_VkpTcorkdXGM "Tensi Harian!A:G" --values '[["YYYY-MM-DD","HH:MM","SYS","DIA","PULSE","","Foto"]]'`
   - `Sumber` = "Foto" (from image) or "Ketik" (typed)
   - `Keterangan`: fill whenever user requests ("berikan keterangan X", "tambahkan keterangan X") — use their exact phrase (e.g. "Sebelum olahraga", "Setelah olahraga pagi", "Habis ngegym"). This user routinely requests it, so default to including the context phrase rather than leaving blank.
5. **Reply**: compact table of recorded values + confirmation only. **NO medical commentary** — user requires "NO komentar medis": just log the numbers; no range flags, no "konsultasi dokter" nudges unless the user explicitly asks. Give the sheet link when asked.
6. **Recap on request** — "rekap 2 hari terakhir" etc.: fetch last ~30 rows (`sheets get ... "Tensi Harian!A1:G40"`), group by date, present compact per-day table + trend lines (sistolik membaik / diastolik konsisten tinggi / nadi normal). Flag out-of-range patterns (DIA > 90 berulang, SYS > 140) and suggest konsultasi dokter if pattern persists. Keep it short; markdown tables render fine on Telegram.

## User Preferences (CRITICAL)

- **DO NOT upload photos to Google Drive.** User explicitly decided: catat datanya saja, foto tidak perlu di-upload. Never offer Drive upload for this workflow.
- **Minimal response**: values + confirmation only. One short health note max — no lectures, no full guidance.
- Keep appending to the SAME sheet/tab — never create a new spreadsheet.

## Pitfalls

- "OK" circle icon on Omron = measurement normal; heart icon is just the pulse indicator.
- Read the header row before first append to confirm columns; the tab may be empty (headers only) on a fresh sheet.
- Sheet link format for user: `https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit`
