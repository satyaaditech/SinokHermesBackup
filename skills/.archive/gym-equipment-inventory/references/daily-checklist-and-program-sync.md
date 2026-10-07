# Daily Gym Checklist, 1-Month Periodization & Program Synchronization

## 1. Core Principles

1. **Google Sheets as Single Source of Truth**:
   - The training program defined in Google Sheets is the authoritative source.
   - Any checklist or reminder sent to the user (e.g., via Telegram morning reminder at 05:00 WIB) MUST strictly mirror the Google Sheet.
   - When the user asks for a monthly cycle, generate the concrete 12-session calendar directly in Google Sheets (`Program Bulan 1 (12 Sesi)`) rather than relying on ad-hoc memory.

2. **Mandatory Drive Image URLs for Every Station**:
   - When communicating workout checklists in chat/Telegram, every single exercise MUST include a direct, clickable URL to that machine's photo in Google Drive (`Link Foto Drive`).
   - Why: Users working out on mobile need immediate visual confirmation of the machine number, appearance, and setting levers to locate the correct station without confusion.

3. **Mandatory Complete Format with Machine Usage Instructions (`Cara Pakai & Pandom`)**:
   - The user explicitly requested: *"Aku suka yang ini versi lengkap dengan cara pakainya, pada bagian akhir tambahkan url utk report hasil"*.
   - Never send abbreviated/minimalist exercise lines that omit how to use the machine.
   - Every single exercise item MUST explicitly show:
     * Exercise Name & Machine No.
     * Drive Photo Link
     * Target Sets & Reps + Rest Interval (`Ngaso`)
     * Target Muscle Group (`Fokus Otot`)
     * Biomechanics & Setup Instructions (`💡 Cara Pakai & Pandom`)
   - For cardio stations: specify Incline (8-10%), Speed (4.2-4.8 km/h) or RPM (70-80), and non-grip posture cues.

4. **Footer Report Section: URL Only (No WhatsApp / Copy-Paste Text Template)**:
   - The user explicitly corrected: *"utk report cukup url saja, tidak perlu versi WhatsApp"*.
   - DO NOT include copy-paste text code blocks or manual message reply templates.
   - At the bottom of the checklist, provide ONLY the direct URL link to the Dynamic Web Form:
     * `👉 [Formulir Rekap Online Coach Sinok](http://100.92.237.45:8085)` (Tailscale / Cellular)
     * `(WiFi Griya: http://192.168.0.112:8085)`

5. **Multi-Tab Spreadsheet Architecture**:
   - **Tab 1: `Daftar Alat Gym`**: Master hardware inventory (ID, Name, Image preview, Primary/Secondary muscles, Movement type, Biomechanics/settings, Drive photo URL).
   - **Tab 2: `Program Latihan Master`**: Base periodized split templates (Day/Session, Movement Order, Tool ID, Movement Name, Muscle Group, Target Sets, Target Reps, Rest Interval, Biomechanics Setup Cues, Drive Link).
   - **Tab 3: `Program Bulan 1 (12 Sesi)`**: Concrete 4-week calendar (Date, Session ID, Week ID, Focus, Exercise Order, Tool ID, Movement Name, Target Sets, Target Reps, Coach Notes/Phase, Realized Weight, Realized Reps, RPE, Drive Photo Link).
   - **Tab 4: `Log Progres Harian`**: Historical tracking of real workouts (Date & Time, Session, Tool ID, Exercise, Target Sets x Reps, Realized Weight in kg, Realized Reps, RPE 1-10, Cardio Duration, Daily Bodyweight, Fatigue/Injury Notes).
   - **Tab 5: `Monitoring Transformasi`**: Weekly progress rollups (Week #, Date Range, Avg Bodyweight, +/- Change kg, Waist/Abdominal Girth cm, Drive Photo Folder Link, Coach Assessment).

---

## 2. 4-Week Periodization Pathway (Mesocycle Structure)

When structuring a 1-month program (12 sessions for 3x/week training):
- **Week 1 (Sesi 01–03) — Calibration & Foundation**: Establish baseline working weights, perfect movement trajectory/tempo, ensure joint comfort (RPE 6–7).
- **Week 2 (Sesi 04–06) — Volume Accumulation**: Keep working weights steady while cementing contraction quality, peak squeezes, and consistent rep completion (RPE 7–8).
- **Week 3 (Sesi 07–09) — Progressive Overload & Intensification**: Increase resistance (+2.5 kg to 5 kg depending on compound vs isolation), target lower rep bounds with maximum focus (RPE 8–9).
- **Week 4 (Sesi 10–12) — Peak Realization & Mesocycle Review**: Test maximum strength on target stations, measure abdominal/waist circumference, assess total weight change, and prepare the next mesocycle.

---

## 3. Morning Reminder Checklist Format (Telegram 05:00 WIB)

The morning cronjob executes at 05:00 WIB on scheduled days (Tuesday, Thursday, Saturday via `0 5 * * 2,4,6`).
The script queries Google Sheets by today's date (`DD/MM/YYYY`) from `Program Bulan 1 (12 Sesi)` and formats:

1. **Greeting & Context**: Polite, encouraging (e.g., in Javanese Krama Alus).
2. **Session Header**: Session ID, Week ID, Day focus, Coach intent/phase.
3. **Numbered Exercise Checklist**:
   - Exercise name & Machine number
   - Direct Drive image link: `📸 [Pirsani Foto Alat ing Drive](<URL>)`
   - Target sets x reps
   - Biomechanics cues & seat/pulley settings
4. **Safety & Progressive Overload Guidance**: Emphasize core bracing, joint protection, and recording exact numbers.
5. **One-Tap Post-Workout Reporting Template**: Formatted inside a code block (` ```text ... ``` `) so mobile users can tap to copy, replace placeholders with actual numbers, and send in under 20 seconds.

---

## 4. Post-Workout Recap Framework (Solving User Forgetfulness)

Users frequently forget what metrics to report after an exhausting gym session. Address this with two complementary mechanisms:

### A. Online Form (Google Forms Linked to Sheets)
- Instruct user to create a linked Google Form via: **Google Sheets menu ➡️ Tools (Alat) ➡️ Create a new form (Buat formulir baru)**.
- Fields to configure in the form:
  1. **Tanggal & Sesi Gladhen**: Dropdown (Sesi 01 - Legs, Sesi 02 - Push, Sesi 03 - Pull).
  2. **Bobot Badan Enjang Punika (kg)**: Short answer (number).
  3. **Cathetan Beban & Repetisi**: Paragraph text for machine loads and reps completed.
  4. **Durasi Kardio (Menit)**: Short answer (number).
  5. **Tingkat Sayah / RPE (1 - 10)**: Linear scale 1 to 10.
  6. **Cathetan Rasa Fisik / Sayah**: Short answer for joint comfort, fatigue, or muscle soreness.
  7. **Foto Salira / Timbangan (Opsional)**: File upload.
- Submissions populate a new responses tab automatically, which the agent summarizes into `Log Progres Harian` and `Monitoring Transformasi`.

### B. One-Tap Copyable Code Block Template (In Telegram)
Every morning checklist message MUST conclude with a pre-filled text template inside a monospaced code block:

```text
Lapuran Sesi 01 (05/09/2026):
1. Plate-Loaded 45-Degree Leg Press Machine: ... kg (... reps)
2. PLAMAX Seated Hip Adductor & Abductor: ... kg (... reps)
3. Plate-Loaded Seated Calf Raise Machine: ... kg (... reps)
4. Plate-Loaded Standing Viking Press: ... kg (... reps)
5. Ab Coaster Machine: ... reps
6. Kardio: Treadmill Incline / Sepeda Statis: ... menit
- Bobot Badan Enjang Punika: ... kg
- Tingkat Sayah (RPE 1-10): ...
- Cathetan Fisik / Sayah: ...
```
Mobile Telegram users can tap once to copy the entire block, replace the ellipses with their numbers, and send.
