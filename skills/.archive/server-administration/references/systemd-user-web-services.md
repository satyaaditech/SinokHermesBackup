# Systemd User Services for Internal Web Apps & Tailscale

When deploying internal web apps, dashboards, or product landing pages on `n8nserver` accessible over Tailscale without requiring root/sudo privileges:

## 1. Systemd User Service Architecture
User services run under `systemd --user` for the active user (`satyaaditech`), managed independently of root systemd:
- Directory: `~/.config/systemd/user/<service-name>.service`
- Enabled symlinks: `~/.config/systemd/user/default.target.wants/<service-name>.service`
- Daemon reload: `systemctl --user daemon-reload`
- Management: `systemctl --user [start|stop|restart|status|enable|disable] <service-name>.service`

## 2. Standard Service Unit Template
```ini
[Unit]
Description=<App Name> Web App on Port <Port>
After=network.target

[Service]
Type=simple
ExecStart=/home/satyaaditech/.hermes/hermes-agent/venv/bin/python3 /path/to/project/server.py
WorkingDirectory=/path/to/project
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

## 3. Fast & Reliable FastAPI / HTTP Server Pattern
```python
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="App Name")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Always include HEAD method to avoid 405 on curl -I and health monitors
@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
async def health():
    return {"status": "online", "port": PORT}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=False)
```

## 4. Port Allocations on n8nserver
- 5678: n8n automation
- 8000: Share HTTP Server (media / static)
- 8085: Gym Tracker
- 8086: AeroBlade Badminton Landing Page
- 8090: Obsidian & LLM Wiki Reader
- Always check port availability first: `ss -tuln | grep -E ':<port>'`
