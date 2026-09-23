# Systemd User Services for Python Web Apps (Tailscale / LAN Access)

Pattern for running persistent background web services (FastAPI, Uvicorn, Flask, HTTP servers) on Linux servers under an unprivileged user without needing `sudo`.

## Why Systemd User Units
- Does not require root / sudo permissions.
- Automatically managed under `systemd --user`.
- Auto-restarts on failure and survives crashes.
- Accessible across local LAN and Tailscale mesh network.

## Setup Steps

### 1. Create Unit File
Create unit file at `~/.config/systemd/user/<service-name>.service`:

```ini
[Unit]
Description=Sinox Obsidian & LLM Wiki Reader Web App on Port 8090
After=network.target

[Service]
Type=simple
ExecStart=/home/satyaaditech/.hermes/hermes-agent/venv/bin/python3 /path/to/app.py
WorkingDirectory=/path/to/working_dir
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

### 2. Enable and Start
```bash
systemctl --user daemon-reload
systemctl --user enable --now <service-name>.service
systemctl --user status <service-name>.service
```

### 3. Verification & Port Audit
```bash
# Check running status
systemctl --user list-units --type=service

# Verify listening port
ss -tulpn | grep 8090
curl -s http://127.0.0.1:8090/
```

### 4. Tailscale Remote Access
Verify listener binds to `0.0.0.0:<port>` so Tailscale IP (`100.x.x.x:<port>`) can reach the web app without firewall issues.
