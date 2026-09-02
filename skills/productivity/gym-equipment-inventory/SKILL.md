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

Catalog and inventory gym equipment and exercise machines from photos into Google Drive and Google Sheets. The resulting catalog serves as the single source of truth for designing customized, realistic fitness training programs based on actual available gym equipment.

## Triggers

- User sends photos of gym machines / equipment.
- User mentions "rekap alat gym", "inventaris mesin fitness", "foto alat gym".
- Follow-up planning: "buat program latihan dari daftar alat gym ini".

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
