---
name: usb-drive-automount
description: Use when mounting USB/external drives on Linux servers.
---

# USB Drive Automount (headless server)

Set up external USB/NVMe drives on a headless Linux server: detect, grant limited sudo, auto-mount via fstab+systemd, verify. Designed for portable drives the user plugs/unplugs freely.

## Triggers

- User plugs in USB/flash/external drive, asks to access, auto-mount, or use as storage
- "cek flash drive", "auto mount", "drive tidak ke-mount", "tambah storage"
- Works with exfat, vfat/FAT32, ext4

## Workflow

### 1. Detect (no sudo needed)
```bash
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL,TRAN | grep -v loop
lsblk -f /dev/sdX          # FSTYPE + UUID + LABEL
```
Note TRAN=usb. If drive is an installer (casper/, squashfs, autorun.inf) — it's a live-USB, do NOT use as storage.

### 2. Grant limited sudo — user runs this in THEIR terminal (password never in chat)
Hermes cannot mount without root. Best pattern: user types password ONCE in their own SSH session:
```bash
echo 'USER ALL=(ALL) NOPASSWD: /usr/bin/mount, /usr/bin/umount, /usr/bin/mkdir' | sudo tee /etc/sudoers.d/hermes-mount && sudo chmod 440 /etc/sudoers.d/hermes-mount
```
Verify: `sudo -n mount -l | head -1` runs, `sudo -n rm /tmp/x` → "password is required".
Do NOT grant NOPASSWD: ALL — keep the blast radius small.
(Note: `systemctl start` is NOT covered — user must run that manually too, see step 5.)

### 3. fstab entry (auto-mount template)
```
UUID=<UUID> /mnt/<name> <fstype> nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0
```
- `nofail` — boot OK without drive; `x-systemd.automount` — mount lazily on access; `idle-timeout=600` — auto-unmount after 10min idle (safe unplug); `umask=000` — all users read/write; `device-timeout=5` — no long hangs.
- exfat for >4GB files, vfat for FAT32.
- Write via a setup script + `sudo bash script.sh` (user's terminal, once). Script must be idempotent (grep marker before append) and back up fstab first. Template: `templates/setup-usb-automount.sh`.
- Validate syntax WITHOUT touching /etc: `cat /etc/fstab /tmp/newlines > /tmp/fstab.test && findmnt --verify --tab-file /tmp/fstab.test` → want "0 parse errors".

### 4. Pitfall — stray numeric line in /etc/fstab
A lone "24" line appeared in fstab (leftover output from a previous command, source unknown) → "parse error at line 15". Fix (user's terminal):
```bash
sudo bash -c "sed -i -E '/^[0-9[:space:]]+$/d' /etc/fstab && systemctl daemon-reload"
```

### 5. CRITICAL pitfall — systemd unit name escaping
Mount point `/mnt/usb-nvme` contains a hyphen → unit name is `mnt-usb\x2dnvme.automount` (hyphen escaped as \x2d), NOT `mnt-usb-nvme.automount`.
- `sudo systemctl start mnt-usb-nvme.automount` → "Unit not found" ❌
- Glob `systemctl start 'mnt-usb-*.automount'` → "0 loaded units"/no effect ❌
- Works: `sudo systemctl start 'mnt-usb\x2dnvme.automount' 'mnt-usb\x2dubuntu.automount'` ✅ (literal escape, single quotes)
- Or path-based: `sudo systemctl start /mnt/usb-nvme /mnt/usb-ubuntu` ✅
After fstab edited at runtime, units exist but are inactive — need ONE manual start. After reboot, systemd-fstab-generator starts them automatically.

### 6. Verify
```bash
systemctl list-units --all 'mnt-usb*' --no-pager   # automount = active (waiting)
df -h | grep usb                                   # mounted = ready
ls /mnt/<name>                                     # content readable
```
Healthy states: automount `active (waiting)` + mount `active (mounted)`. Drive unplugged → no row in df, system fine. That's by design, not an error.

## Pitfalls

- exFAT/FAT32 have NO journaling — unplugging mid-write can corrupt files. idle-timeout + telling the user to wait after copy mitigates; always warn.
- `udisksctl mount` fails headless ("No such device or address" / polkit NotAuthorized) — don't rely on it, use the sudoers+fstab route.
- Never mount a live-installer USB (casper/, squashfs, [boot]) as storage — persistent partition `casper-rw` is for live sessions.
- Du read-only check: `du -x --max-depth=1 /` as non-root misses /root and some /var — use df for authoritative numbers.

## Verification after reboot
- Units auto-start (fstab generator default enables to local-fs.target).
- Test unplug: `sudo umount /mnt/<name>` then re-access path — automount remounts on next access.
