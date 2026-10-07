# Dynamic Web Workout Tracker & Google Sheets Integration

This reference documents the architecture and implementation of the self-hosted Dynamic Web Workout Tracker (`gym_web_app.py` & `gym_backend.py`), running as a systemd user service on n8nserver (`gym-tracker.service` on port 8085).

## 1. Problem & User Requirements

Users working out at the gym need an effortless, zero-friction reporting mechanism right from their mobile phone:
1. **Dynamic Session Loading**: The form must automatically present *only* the exercises scheduled for today (e.g. Legs on Saturday vs Push on Tuesday), rather than forcing the user to pick exercises from a huge static form.
2. **Visual Station Confirmation**: Each exercise card must link directly to the Google Drive photo of that machine.
3. **Touch-Friendly Numeric Inputs**: Stepper buttons (`+` / `-` 2.5 kg for weights, `+` / `-` 1 for reps) to minimize manual typing on mobile.
4. **Post-Submission Verification**: After hitting Submit, the UI must immediately display a full confirmation review modal showing all recorded metrics (load, reps, body weight, cardio, RPE, notes) so the user can verify accuracy.
5. **History & Progression Tracking**: A dedicated History tab that queries Google Sheets in real-time to show past workouts, progressive overload across sessions, and fatigue trends.
6. **Real-Time Two-Way Google Sheets Sync**:
   - Updates `Realisasi Beban (kg)`, `Realisasi Reps`, and `RPE` in `Program Bulan 1 (12 Sesi)` for the matching session date.
   - Appends a new timestamped row to `Log Progres Harian`.
7. **UI Contrast & Default Theme Preference**:
   - User preference: Light Theme by default (`#f8fafc` background, `#ffffff` cards, `#0f172a` deep slate text, clear borders). Reason: user experiences eye strain / lack of visual clarity with dark mode.
   - Dark mode toggle button (`🌙 Mode Gelap` / `☀️ Mode Terang`) is provided in the header for optional switching, persisted via `localStorage`, but initial load MUST always default to Light Mode.

## 2. Architecture Overview

```
[Mobile Phone (Gym / Home)]
        │
        ▼ (HTTP :8085 via Tailscale 100.92.237.45 or LAN 192.168.0.112)
[FastAPI Web Server (gym_web_app.py)]
        │
        ▼
[Backend Engine (gym_backend.py)]
        │
        ▼ (Google OAuth2 google_token.json)
[Google Sheets Master: 'Inventaris Alat & Program Fitness']
        ├── Program Bulan 1 (12 Sesi)  <-- Dynamic session source + Realisasi update
        ├── Log Progres Harian         <-- Append full workout log row
        └── Monitoring Transformasi    <-- Weekly meso review
```

## 3. Systemd Service Deployment

The service runs under systemd user control to ensure 24/7 uptime and auto-restart on reboot:
File: `~/.config/systemd/user/gym-tracker.service`

```ini
[Unit]
Description=Coach Sinok Gym Tracker Web App on Port 8085
After=network.target

[Service]
Type=simple
ExecStart=/home/satyaaditech/.hermes/hermes-agent/venv/bin/python3 /home/satyaaditech/gym_web_app.py
WorkingDirectory=/home/satyaaditech
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

Commands:
```bash
systemctl --user daemon-reload
systemctl --user enable gym-tracker.service
systemctl --user restart gym-tracker.service
systemctl --user status gym-tracker.service
```

*Pitfall Note*: Ensure `ExecStart` points to the active virtualenv's python binary where `fastapi`, `uvicorn`, and `google-api-python-client` are installed, NOT the bare system `/usr/bin/python3`.

## 4. API Specification

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Responsive SPA (Mobile-first, dark fitness UI, 3 tabs: Form, History, Master Program) |
| `GET` | `/api/session?date=DD/MM/YYYY` | Returns today's active session metadata, exercises, target sets/reps, and Drive image links |
| `GET` | `/api/program` | Returns full 12-session mesocycle program |
| `GET` | `/api/history` | Fetches chronological workout logs from `Log Progres Harian` |
| `POST` | `/api/submit` | Updates real-time load/reps in `Program Bulan 1` and appends to `Log Progres Harian` |

## 5. Pitfalls & Debugging Lessons

1. **FastAPI Route Parity with Backend Engine**:
   - Ensure backend function signatures match route handler calls exactly (e.g. `gym_backend.get_month_program()` vs `get_all_sessions()`, `gym_backend.save_workout_submission(payload.dict())` vs `submit_workout_log`).
   - Mismatches lead to unhandled `AttributeError` returning HTTP 500 when client tabs fetch API endpoints (e.g., Tab 3 Master Schedule).
2. **Head Request Handling in FastAPI**:
   - Browser pre-checks and uptime monitors may issue `HEAD /` requests. Include `@app.head("/")` alongside `@app.get("/")` to prevent `405 Method Not Allowed`.
3. **High Contrast for Eye Comfort**:
   - Always maintain pure white cards (`#ffffff`) on soft background (`#f8fafc`) with deep slate text (`#0f172a`) and bold borders (`#cbd5e1`). Never use washed-out low-contrast gray text on mobile interfaces.

## 6. Mobile Workflow Integration

In the 05:00 WIB morning Telegram reminder (`gym_reminder.py`):
1. Include direct clickable link: `👉 [Formulir Rekap Online Coach Sinok](http://100.92.237.45:8085)`.
2. **URL Only (No WhatsApp Template)**: Do NOT include WhatsApp / text copy-paste code block template. The user explicitly directed: *"utk report cukup url saja, tidak perlu versi WhatsApp"*.

## 6. Troubleshooting & Common Pitfalls

1. **Python Environment Mismatch**:
   - The user systemd unit (`~/.config/systemd/user/gym-tracker.service`) must point to the virtual environment binary (`/home/satyaaditech/.hermes/hermes-agent/venv/bin/python3`) where `fastapi` and `uvicorn` are installed, NOT system `/usr/bin/python3`.

2. **Function Signature Mismatch between API & Backend**:
   - In `gym_web_app.py`, the endpoint `GET /api/program` MUST call `gym_backend.get_month_program()`. Calling nonexistent `get_all_sessions()` raises `AttributeError` resulting in HTTP 500 (`Gagal mundhut data jadwal master`).
   - The endpoint `POST /api/submit` MUST call `gym_backend.save_workout_submission(payload.dict())`.

3. **Light Mode High-Contrast CSS Requirements**:
   - User preference: Light Theme by default (`#f8fafc` background, `#ffffff` cards, `#0f172a` deep slate text, clear borders). Reason: user experiences eye strain / lack of visual clarity with dark mode.
   - Any theme toggle MUST persist via `localStorage` with light theme as default fallback.
