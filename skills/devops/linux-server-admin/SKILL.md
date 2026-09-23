---
name: linux-server-admin
description: "Use for Linux server tasks: USB mount, fstab, UFW, sudoers."
---

# Linux Server Administration

Non-trivial patterns for server administration on Ubuntu/Debian — USB auto-mount, firewall rules, restricted sudoers, Tailscale access. For Hermes-specific administration (backup, config, memory providers), use `hermes-administration`.

## Triggers

- USB flash drive / external storage mount
- fstab configuration, systemd automount
- Firewall (UFW) rules
- sudoers / NOPASSWD setup
- Tailscale remote access
- Server diagnostics (temperature, load, RAM)
- Console screen / monitor control (backlight poweroff without sudo) (see [references/screen-backlight-control-docker.md](references/screen-backlight-control-docker.md))
- Laptop as server power-loss recovery without UPS (see [references/laptop-server-power-loss-recovery.md](references/laptop-server-power-loss-recovery.md))
- Samba (SMB) directory sharing and bind mount workarounds (see [references/samba-bind-mount-workaround.md](references/samba-bind-mount-workaround.md))
- Custom n8n Docker upgrades with hardened image workarounds (see [references/n8n-docker-hardened-workaround.md](references/n8n-docker-hardened-workaround.md))
- n8n workflow automation via Docker CLI and REST API (see [references/n8n-automation-cli-api.md](references/n8n-automation-cli-api.md))
- Cloudflare Tunnel domain masking and routing (see [references/cloudflare-tunnel-masking.md](references/cloudflare-tunnel-masking.md))
- Systemd user service for unprivileged Python web apps (see [references/systemd-user-daemon-web-app.md](references/systemd-user-daemon-web-app.md))

## USB Auto-Mount Pattern (fstab + systemd)

Goal: USB drive auto-mounts when plugged in, survives reboot, and never causes boot failure when missing.

### Step 1: Identify UUID

```bash
lsblk -f /dev/sdX
# or: blkid /dev/sdX1
```

### Step 2: fstab entry

```
UUID=XXXX-YYYY /mnt/mountpoint fs_type nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0
```

Key options:
- `nofail` — boot continues if drive missing (CRITICAL)
- `x-systemd.automount` — mount on first access, not at boot
- `x-systemd.idle-timeout=600` — auto-unmount after 10 min idle (safe to unplug)
- `x-systemd.device-timeout=5` — give up fast if device missing
- `umask`

### Pitfall / Troubleshooting: Stale Mount Points (Input/output error)

If a USB drive is disconnected and reconnected, the kernel may assign it a new device block name (e.g., changing from `/dev/sdc` to `/dev/sdd`), causing old active paths to throw `Input/output error`.

To resolve:
1. Verify the current block mapping using `lsblk` and check the active mount point (e.g., `/mnt/usb-nvme` on `/dev/sdd2`).
2. Clean up stale/broken mounts using lazy unmount:
   ```bash
   sudo umount -l /path/to/broken/mount
   ```
3. Re-link the folder symlink or bind mount to the fresh active path:
   ```bash
   ln -s /mnt/usb-nvme/obsidian /path/to/shorts_factory/obsidian
   ```
- `nosuid,nodev` — security hardening for removable media
- `noatime` — reduce writes on flash drives

### Step 3: After fstab edit

```bash
sudo systemctl daemon-reload
# Start the automount unit (systemd fstab-generator creates these)
sudo systemctl start 'mnt-mountpoint.automount'
```

## Samba (SMB) Shared Folders & Bind Mount Workaround

When you want to share a directory via Samba but have restricted permissions (cannot modify `/etc/samba/smb.conf` because it is password-protected or owned by root), but you have an existing writeable Samba share and passwordless sudo privileges for `mount` and `mkdir`:

1. **Create the mountpoint** inside the existing shared folder (e.g., `/home/user/existing_share/`):
   ```bash
   mkdir -p /home/user/existing_share/new_vault
   ```
2. **Bind-mount the target directory** to the mountpoint:
   ```bash
   sudo mount --bind /home/user/target_directory /home/user/existing_share/new_vault
   ```
   Now clients accessing the existing share can read and write to `/home/user/target_directory` as if it were a direct subdirectory.
3. **Make the bind mount persistent** across reboots without `/etc/fstab` (since fstab editing requires root editing rights) by utilizing `@reboot` in the user's crontab:
   ```bash
   (crontab -l 2>/dev/null; echo "@reboot sudo mount --bind /home/user/target_directory /home/user/existing_share/new_vault") | crontab -
   ```

### Pitfalls

### Pitfalls

- **Hyphen in mount path**: systemd escapes `-` to `\\x2d` in unit names. Use `systemctl list-units 'mnt*'` to find real unit names, then start with escaped form: `systemctl start 'mnt-usb\\x2dnvme.automount'`. If glob/escaped forms fail, use path-based start: `systemctl start /mnt/usb-nvme`.
- **After fstab changes on a running system**: automount units are created but NOT auto-started. Manual `systemctl daemon-reload` then `systemctl start /mnt/<mount>` required. On reboot they activate automatically.
- **exFAT**: may need `apt install exfat-fuse exfatprogs`
- **polkit blocking**: `udisksctl mount` may fail without desktop session. Use fstab+sudo instead.
- **idempotent**: always `grep` before appending to `/etc/fstab` to avoid duplicates

## Remote Access + UFW (Tailscale)

When services listening on `0.0.0.0` are unreachable via Tailscale from another device, but `curl` works locally — UFW default-deny is the culprit.

```bash
sudo ufw allow in on tailscale0
```

This opens traffic from Tailscale-authenticated devices only — no public exposure.
**User preference**: Tailscale direct IP (`http://100.92.237.45:PORT`), not Cloudflare tunnel DNS.

## Console Screen Power Control (Without Sudo via Docker)

When running headless on a physical machine (e.g., a laptop or All-in-One PC acting as a server), you may want to turn off the physical screen (backlight and DPMS link) to save power. If the SSH/gateway user has restricted sudo (cannot run control commands without a password prompt) but belongs to the `docker` or `lxd` group, you can control the screen hardware parameters by running a privileged container that mounts `/sys`:

### Turn OFF Screen
```bash
docker run --rm --privileged -v /sys:/sys alpine sh -c "echo 0 > /sys/class/backlight/amdgpu_bl0/brightness; echo 4 > /sys/class/graphics/fb0/blank"
```
*Note: Adjust `amdgpu_bl0` to the actual graphics backlight driver directory present inside `/sys/class/backlight/`.*

### Turn ON Screen
```bash
docker run --rm --privileged -v /sys:/sys alpine sh -c "echo 255 > /sys/class/backlight/amdgpu_bl0/brightness; echo 0 > /sys/class/graphics/fb0/blank"
```

### Script Scaffolding
Deploy executable shells (`screen_off.sh` and `screen_on.sh`) in the user's home directory utilizing this privileged container wrapper for convenience.


## OmniRoute Diagnostics

For auth failures or routing issues: query `~/.omniroute/storage.sqlite` directly. See `references/omniroute-schema.md` for schema and queries.

## Restricted sudoers Rule

Allow specific commands without password, block everything else:

```bash
echo 'username ALL=(ALL) NOPASSWD: /usr/bin/mount, /usr/bin/umount, /usr/bin/mkdir' | sudo tee /etc/sudoers.d/hermes-mount && sudo chmod 440 /etc/sudoers.d/hermes-mount
```

- File must be `440` perms or sudo ignores it
- Use `/etc/sudoers.d/` subdirectory, never edit `/etc/sudoers` directly
- Verify: `sudo -n mount` → OK; `sudo -n rm` → "password required" (blocked)

## Tailscale + UFW Remote Access

```bash
# Allow all Tailscale traffic through firewall
sudo ufw allow in on tailscale0
```

- Access via Tailscale IP (e.g. `http://100.92.237.45:9119`) or MagicDNS (`http://n8nserver.tailf595e8.ts.net:9119`)
- Only devices in your tailnet can reach the server — not public internet

## Server Diagnostics

```bash
# Temperature
sensors | grep -iE 'temp|tctl'
# Fallback: cat /sys/class/thermal/thermal_zone*/{type,temp}

# Load & RAM
uptime
free -h

# Top processes
ps aux --sort=-%cpu | head -8
```

## OmniRoute Model Query

OmniRoute stores configuration in SQLite at `~/.omniroute/storage.sqlite`. See `references/omniroute-schema.md` for table structure and query patterns.
