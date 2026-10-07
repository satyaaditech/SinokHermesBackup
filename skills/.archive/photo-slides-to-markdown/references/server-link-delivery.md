# Server-Link Delivery: serve the .md from the Hermes server (user-PREFERRED pattern)

Established 2026-08-09 (Bussines_plan_coaching session). After receiving a Google Drive link, user said: "linknya ke dokumen yang ada di server hermes aja gpp" — prefers an HTTP link served from the Hermes server over Drive. Use this as the PRIMARY delivery; Drive (drive-final-delivery.md) is the backup.

## Setup (once per file / after each server reboot)
1. `mkdir -p ~/share && ln -sf /home/satyaaditech/<file>.md ~/share/<file>.md`
   Symlink is the trick: the served content is ALWAYS the latest version — no re-upload after every photo append.
2. Start a long-lived background server (no sudo needed):
   `python3 -m http.server 8000 --directory /home/satyaaditech/share --bind 0.0.0.0`
3. Verify: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/<file>.md` → expect 200.
4. Send BOTH links (user is on LAN at home, Tailscale outside):
   - LAN: `http://192.168.0.112:8000/<file>.md`
   - Tailscale: `http://100.92.237.45:8000/<file>.md`

## Pitfalls
- Background process dies on server reboot → offer to restart on request ("bisa minta kapan saja").
- NEVER serve the whole home dir (~/.hermes holds credentials); only the ~/share folder.
- Send the link mid-processing if the user asks to check progress — it already shows the latest entries.
- Port 8000 can be taken on other setups: check `ss -tlnp` first, else pick another port (e.g. 8010) and tell the user.
- Keep the Drive link as a cadangan/backup in case the server link fails.
