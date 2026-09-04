---
name: gym-equipment-inventory
description: "Use when cataloging gym equipment photos to Drive & Sheets."
version: 1.0.0
author: Sinok (Hermes Agent)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [fitness, gym, equipment, google-drive, google-sheets, biomechanics]
    related_skills: [google-workspace, health-metrics-logging]
---

# Gym Equipment Inventory & Program Planning

> **🔒 STATUS: LOCKED & FINALIZED (Approved by Pak Satya Adi Dharma on 04/09/2026)**
> **STRICT RULE: Do NOT change, abridge, or alter the program structure, reminder format, or reporting workflow without explicit user instruction from Pak Satya.**
> - Telegram Morning Reminder (05:00 WIB Tue/Thu/Sat): Full complete version with `Cara Pakai & Pandom`, `Fokus Otot`, `Ngaso`, and direct Drive photo URLs.
> - Report Section at footer: Web Form URL ONLY (`http://100.92.237.45:8085`), NO WhatsApp / text template.
> - Web Tracker: Running on port 8085 via `gym-tracker.service`, dynamic 2-way sync with Google Sheets master (`Program Bulan 1 (12 Sesi)` & `Log Progres Harian`), includes post-submit confirmation review & history progress tabs. Default UI MUST be Light Theme (high-contrast text, clear cards for eye comfort) with an optional dark mode toggle.

Catalog and inventory gym equipment and exercise machines from photos into Google Drive and Google Sheets. The resulting catalog serves as the single source of truth for designing customized, realistic fitness training programs based on actual available gym equipment.

## Triggers

- User sends photos of gym machines / equipment.
- User mentions "rekap alat gym", "inventaris mesin fitness", "foto alat gym".
- Follow-up planning: "buat program latihan dari daftar alat gym ini".
- User reports unphotographed / missing equipment (e.g., dumbbells, treadmills, stationary bikes, barbells) or asks to complement machine inventory.
- Daily workout checklist & reminder delivery ("jadwal gym", "ceklist latihan", "reminder gym").
- User requests full-month periodization or online progress reporting forms ("program sebulan", "rekap progres form online", "buat form isian").

## Daily Workout Checklist & Sheet Synchronization Rules

See complete specification in `references/daily-checklist-and-program-sync.md`, `references/dynamic-web-tracker-and-sheets-sync.md`, and `references/bodyweight-and-home-workouts.md`.

### Format Rules for Daily Telegram Reminders (Mandatory User Preferences)
1. **Always Use the Complete Version with Usage Instructions (`Cara Pakai & Pandom`)**:
   - The user explicitly requested the complete format with biomechanical setup and execution cues.
   - Every exercise item MUST include all 5 components:
     * `**<No>. <Nama Alat & Gerakan>** (Mesin No. <ID>)`
     * `📸 [Pirsani Foto Alat ing Drive](<URL>)`
     * `🎯 **Target**: <Set> x <Reps> | Ngaso: <Rest in sec>`
     * `💪 **Fokus Otot**: <Target muscles in Javanese/Indonesian>`
     * `💡 **Cara Pakai & Pandom**: <Setup lever, seat height, core brace, and execution cues>`
2. **Footer Report Section: URL Only (No WhatsApp Text Template)**:
   - User correction: *"utk report cukup url saja, tidak perlu versi WhatsApp"*.
   - Do NOT include text codeblocks or copy-paste templates for WhatsApp/Telegram.
   - Conclude strictly with the direct URL to the web reporting app (`http://100.92.237.45:8085` for mobile/Tailscale, `http://192.168.0.112:8085` for home LAN).

1. **Google Sheets as Single Source of Truth**:
   - The workout program in Google Sheets (`Program Latihan Master` and `Program Bulan 1 (12 Sesi)`) MUST be 100% identical to any daily workout checklist sent to the user. Never propose or deliver exercises out-of-sync with the sheet.
   - For monthly periodization, write the complete concrete calendar (12 sessions across 4 weeks) into `Program Bulan 1 (12 Sesi)`.

2. **Mandatory Drive Image URLs**:
   - Every single exercise listed in Telegram messages and Web Form cards MUST include a direct, clickable URL to that machine's photo in Google Drive (`Link Foto Drive`).

3. **Dynamic Web Workout Tracker & Two-Way Sync**:
   - Host a FastAPI mobile web application (`gym_web_app.py` & `gym_backend.py`) managed via systemd user service `gym-tracker.service` on port 8085.
   - Dynamic session rendering: automatically queries today's date from `Program Bulan 1 (12 Sesi)` so users only see today's exercises.
   - Post-submission review: immediately renders a confirmation modal with all entered metrics.
   - History & analytics tab: reads from `Log Progres Harian` to display workout history and overload progress.
   - Dual reporting options: provide both the web app URL and a one-tap copyable Telegram code-block template in the 05:00 WIB morning reminder.
4. **Post-Workout Recap via Online Forms & One-Tap Templates**:
   - To prevent users forgetting what to report post-workout, provide a Google Form linked directly to Sheets (`Tools -> Create a new form`) and append a one-tap copyable code block template (` ```text ... ``` `) to every morning reminder so mobile users can tap, fill numbers, and reply in seconds.
5. **Integrated Spreadsheet Architecture**:
   - Maintain 4 linked tabs: `Daftar Alat Gym` (inventory & photo links), `Program Latihan Master` (periodized splits & cues), `Log Progres Harian` (realized load, reps, RPE, cardio, bodyweight), and `Monitoring Transformasi` (weekly bodyweight delta, waist measurements, photo links, coach notes).
4. **Autonomous Morning Reminder (05:00 WIB)**:
   - Schedule via cronjob (e.g. Tue, Thu, Sat at 05:00 WIB) using `~/.hermes/scripts/gym_reminder.py` (`no_agent=True`) reading dynamically from Google Sheets. Ensure prompt/script is never silent on workout days.

## Handling Incomplete / Unphotographed Equipment (Free Weights & Cardio)

Users frequently photograph selectorized/plate-loaded machines first and overlook staple free-weight and cardio stations (dumbbells, barbells, benches, treadmills, bikes).
1. **Checklist for Commonly Overlooked Equipment**:
   - **Free Weights**: Dumbbell rack & incremental weights, Olympic barbells (20kg), EZ curl bars, weight plates, collars.
   - **Benches**: Adjustable incline/flat/decline benches, preacher curl bench, flat utility bench.
   - **Cardio Area**: Treadmills, stationary bikes (spin / upright / recumbent), elliptical, rowing machine.
   - **Cable Attachments**: Triceps rope, close-grip V-bar, straight bar, stirrup D-handles, ankle straps.
2. **Placeholder Logging Strategy**:
   - Offer to log unphotographed items directly into Google Sheets with a placeholder status (e.g., `[Foto Menyusul]`) so biomechanical program design is not blocked.
   - Keep item numbering sequential. When photos arrive later, update the row with the Drive URL and file thumbnail.

## References & Scripts

- `references/anti-overprocessing-delay.md` — Best practices for anti over-processing jitter, Drive thumbnail permissions, and mobile formatting.
- `scripts/catalog_gym_item.py` — Helper script to upload a gym photo and append a formatted row with randomized delay.

## Google Workspace Setup & IDs

- **Google Drive Folder**: `alat gym`
  - Folder ID: `1Ec3XHJW6k8MYc3dyOvtxL7m1wRgbzyFa`
  - URL: `https://drive.google.com/drive/folders/1Ec3XHJW6k8MYc3dyOvtxL7m1wRgbzyFa`
- **Master Spreadsheet**: `Inventaris Alat & Program Fitness`
  - Spreadsheet ID: `1NAkd3IOOx_gNDeKPXOHI3gSQSHleW6q8pyDmBubdHVo`
  - Tab: `Daftar Alat Gym`
  - URL: `https://docs.google.com/spreadsheets/d/1NAkd3IOOx_gNDeKPXOHI3gSQSHleW6q8pyDmBubdHVo/edit`
- **Credentials**: `/home/satyaaditech/.hermes/google_token.json`

## Column Structure (Daftar Alat Gym)

Row 1 header:
1. `No`
2. `Nama Alat` (e.g. Chest Press Machine, Lat Pulldown, Standing Leg Curl)
3. `Pratilik Gambar` (Formula `=IMAGE("...")` atau direct thumbnail)
4. `Target Otot Utama` (Dada, Punggung, Bahu, Quadriceps, Hamstring, Glutes, dll.)
5. `Target Otot Sekunder` (Triceps, Biceps, Core, dll.)
6. `Tipe Gerakan` (Compound Push, Isolation Pull, Hip Hinge, Knee Flexion, dll.)
7. `Variasi Latihan` (Semua variasi latihan yang dapat dieksekusi dengan mesin tersebut)
8. `Catatan & Setelan` (Posisi pin, setelan jok/kursi, lintasan rel gerak, biomekanika)
9. `Link Foto Drive` (URL webViewLink berkas gambar di Google Drive)

## CRITICAL: Anti-Overprocessing Delay Rule (User Preference)

**ZERO TOLERANCE for rapid burst API requests:**
When multiple photos are sent by the user:
- **NEVER** batch-call Google Drive / Sheets API without delays.
- Apply a **randomized human-like jitter / delay** of 45 to 110 seconds between processing successive items (e.g., `time.sleep(random.randint(45, 110))`).
- This prevents Google from detecting automated burst activity, triggering account safety flags, or throwing `HTTP 429 Too Many Requests`.

## Workflow Steps

1. **Receive & Download Photo**:
   - Save incoming image locally under `/tmp/` or working cache.
2. **Vision Analysis**:
   - Identify machine model/brand (e.g., Impulse Sterling, Matrix, Technogym).
   - Analyze mechanics: cable vs plate-loaded vs pin-selected, pivot point, grip angles, and seat adjustability.
   - Determine primary and secondary muscle recruitment and biomechanical trajectory.
3. **Upload to Google Drive**:
   - Standardize file name: `<XX>_<nama_alat_lowercase>.jpg` (e.g., `01_chest_press_machine.jpg`).
   - Upload to folder ID `1Ec3XHJW6k8MYc3dyOvtxL7m1wRgbzyFa`.
   - Retrieve `webViewLink`.
4. **Rate-Limit Jitter (If multiple photos)**:
   - Wait random delay: `sleep(random.randint(45, 110))` seconds.
5. **Append to Google Sheets**:
   - Append new row under tab `Daftar Alat Gym` with the 9 structured columns.
6. **Telegram Confirmation**:
   - Respond in polite Javanese Krama Alus confirming the machine name, primary muscle, and confirmation of safe recording.
