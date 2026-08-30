---
name: server-administration
description: Configure Linux servers. USB auto-mount, firewall.
---

# Server Administration

Linux server administration patterns used in Hermes-managed infrastructure.

## USB Flash Drive Auto-Mount (fstab + systemd)

Goal: USB drive auto-mounts when plugged in, safe to unplug anytime, no boot errors when absent.

### fstab Entry Template

```
UUID=<uuid> <mount-point> <fs-type> nofail,noatime,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0
```

Key options:
- `nofail` — boot proceeds even if drive is absent (CRITICAL)
- `noatime` — reduce writes
- `umask=000` — world-read-write (no permission drama for Hermes)
- `x-systemd.automount` — mount on first access, not at boot
- `x-systemd.idle-timeout=600` — auto-unmount after 10 min idle (safe to pull)
- `x-systemd.device-timeout=5` — fast fail if device not present

### Idempotent Setup Script Pattern

```bash
cp /etc/fstab /etc/fstab.bak-$(date +%Y%m%d-%H%M%S)
if ! grep -q "<mount-point>" /etc/fstab; then
  printf '%s\n' "${LINES[@]}" | tee -a /etc/fstab >/dev/null
fi
mkdir -p <mount-point>
systemctl daemon-reload
findmnt --verify --fstab  # validate
```

### Starting Automount Units

After editing fstab, systemd-fstab-generator creates units at `/run/systemd/generator/`. Start with **escaped names** (hyphens become `\x2d`):

```bash
sudo systemctl start 'mnt-usb\x2dnvme.automount'
```

PITFALL: `systemctl start 'mnt-usb-*.automount'` does NOT work with glob — the escape character prevents matching. Use exact escaped name in single quotes, or path-based: `sudo systemctl start /mnt/usb-nvme`.

Verify: `systemctl list-units --all 'mnt-usb*' --no-pager` → automount units should show `active (waiting)`.

### Sudo Rule (Hermes Needs Passwordless Mount)

```bash
echo '<user> ALL=(ALL) NOPASSWD: /usr/bin/mount, /usr/bin/umount, /usr/bin/mkdir' | sudo tee /etc/sudoers.d/hermes-mount && sudo chmod 440 /etc/sudoers.d/hermes-mount
```

`mkdir` is needed because mount points may not exist yet. Without it, `sudo -n mount ...` fails with "mount point does not exist."

## Tailscale Remote Access (UFW Firewall)

Goal: dashboard/OmniRoute/n8n accessible from Tailscale-connected devices, NOT from public internet.

### Enable All Traffic on Tailscale Interface

```bash
sudo ufw allow in on tailscale0
```

This allows all ports (9119 dashboard, 20128 omniroute, 5678 n8n, 8000 file share) but ONLY from devices on your tailnet. No public exposure.

PITFALL: Without this rule, UFW active with default-deny blocks all traffic from Tailscale devices even though the server itself can reach out. Test with `curl` from server localhost vs from remote Tailscale device.

### Access URLs (prefer IP for reliability)

```
http://<tailscale-ip>:9119   # Hermes Web Dashboard
http://<tailscale-ip>:20128  # OmniRoute
http://<tailscale-ip>:5678   # n8n
```

MagicDNS (`n8nserver.tailf595e8.ts.net`) needs per-device DNS resolution — IP is more reliable across all devices.

## Pin Message to Telegram General Topic via Bot API

General topic does NOT use `message_thread_id`. Send without it:

```bash
# 1. Send to General (no message_thread_id)
RESP=$(curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
  -d "chat_id=<chat_id>" -d "text=<message>")
MSG_ID=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['message_id'])")

# 2. Pin
curl -s -X POST "https://api.telegram.org/bot$TOKEN/pinChatMessage" \
  -d "chat_id=<chat_id>" -d "message_id=$MSG_ID"

# 3. Verify
curl -s "https://api.telegram.org/bot$TOKEN/getChat?chat_id=<chat_id>" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['result']; print(d.get('pinned_message',{}).get('message_id','NO PIN'))"
```

PITFALL: `message_thread_id=1` returns "Bad Request: message thread not found" in forum groups. Thread 1 is NOT General.

## Storage Policy

Default: SSD server (`/`). External NVMe only when user explicitly asks ("simpan ke nvme"). This is set per-user in memory.

## Pitfalls Summary

- Sudo rule too strict → `mkdir` needed alongside `mount`/`umount`
- fstab edited while running → units registered but NOT started; must `systemctl start` manually
- systemd unit names escape hyphens as `\x2d` — glob patterns in shell won't match
- UFW commands NOT in typical sudo rule → have user run them manually
- Telegram General topic ≠ thread 1 → omit `message_thread_id` entirely
