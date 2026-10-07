---
name: usb-automount-linux
description: Use when mounting USB/flash drives on a Linux server.
---

# USB / Flash Drive Auto-Mount (Linux server)

Setup hotplug USB storage so drives mount automatically on plug, unmount safely when idle, and never break boot when absent. Also covers the limited-sudo pattern so the agent can mount without the user's password ever entering chat.

## Triggers
- User plugs flash drive / USB storage, asks to access or mount it
- User wants auto-mount on plug + safe unplug ("kapan saja bisa lepas")
- Agent needs sudo for mount/umount but user refuses to type password in chat history

## Detect drives (no sudo needed)
- `lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL,TRAN | grep -v loop`
- `lsblk -f /dev/sdX` → FSTYPE, LABEL, UUID (blkid needs sudo; lsblk -f does not)
- `df -h` → what is currently mounted

## Limited sudo — password never enters chat
User runs ONCE in their own SSH/console terminal:
```
echo 'USER ALL=(ALL) NOPASSWD: /usr/bin/mount, /usr/bin/umount, /usr/bin/mkdir' | sudo tee /etc/sudoers.d/hermes-mount && sudo chmod 440 /etc/sudoers.d/hermes-mount
```
- Only mount/umount/mkdir freed; everything else still prompts for password
- Verify: `sudo -n mount -l` runs silently; `sudo -n rm /tmp/x` → "a password is required"
- NOT covered: systemctl, sed/tee/cp into /etc — those edits must be packaged into scripts the USER runs with sudo themselves

## Auto-mount via fstab (systemd automount)
Entry per drive, UUID from `lsblk -f`:
```
UUID=XXXX-XXXX /mnt/usb-nvme exfat nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0
```
- `nofail`: boot OK when drive absent (the "cabut tidak bikin error" guarantee)
- `x-systemd.automount`: lazy mount on first access — plug then access = mounted
- `x-systemd.idle-timeout=600`: auto-unmount after 10 min idle → safe to unplug
- `x-systemd.device-timeout=5`: no long hang if device missing
- `umask=000`: all users can read/write (single-user server)
- fs type: `exfat` for exFAT (kernel 5.15+ has it built-in), `vfat` for FAT32

Validate syntax BEFORE committing:
`findmnt --verify --tab-file <concat-of-old-fstab-plus-new-lines>` → must show "0 parse errors".

## Critical pitfalls

### 1. systemd unit-name escaping (the big one)
Mount point with a hyphen → systemd escapes the hyphen as `\x2d`:
- `/mnt/usb-nvme` → unit is `mnt-usb\x2dnvme.automount`
- `systemctl start mnt-usb-nvme.automount` FAILS: "Unit not found"
- Glob `systemctl start 'mnt-usb-*.automount'` does NOT match escaped names (expands to nothing)
- WORKING forms:
  - path-based: `systemctl start /mnt/usb-nvme /mnt/usb-ubuntu` (systemd resolves)
  - literal escaped, single-quoted: `systemctl start 'mnt-usb\x2dnvme.automount' 'mnt-usb\x2dubuntu.automount'`

### 2. Runtime fstab edit ≠ auto-start
Editing fstab while server is up + `systemctl daemon-reload` only REGISTERS the units (loaded/inactive/dead). The .automount units must be started manually once (see #1). After a reboot the generator auto-enables them — so the manual start is a one-time runtime-only step.

### 3. fstab parse errors from stray lines
A stray line (e.g. a lone "24" that leaked in from some earlier command) breaks every entry AFTER it; `findmnt --verify` reports "parse error at line N -- ignored". Fix: `sed -i -E '/^[0-9[:space:]]+$/d' /etc/fstab` (fstab never has a valid line that is only digits), then daemon-reload + verify.

### 4. udisksctl is not a path on headless servers
`udisksctl mount` fails: "NotAuthorizedCanObtain" / polkit wants an auth agent + controlling tty. Do not waste time there; go straight to the limited-sudoers + fstab route.

## Pattern: setup scripts run by the USER
Agent prepares scripts in the home dir; user runs `sudo bash ~/path/setup.sh` once (password stays on their terminal, never in chat):
- idempotent: grep for an existing marker (e.g. `grep -q "usb-nvme" /etc/fstab`) before appending
- backup fstab first: `cp /etc/fstab /etc/fstab.bak-$(date +%Y%m%d-%H%M%S)`
- end with verification: `findmnt --verify --fstab`

## Verify for the user (commands they run themselves)
- `df -h | grep usb` → drive listed = mounted & ready; line absent = unplugged/idle (normal, not error)
- `systemctl status mnt-usb\x2dnvme.automount` → `active (running)` = mechanism healthy
- `ls /mnt/usb-nvme` → content visible = usable

## Unplug safety
- Data mid-write when unplugged can corrupt (physical risk, not system error) — tell the user to wait for idle-timeout or for the copy to finish
- `nofail` guarantees boot never fails on a missing drive

See `references/known-good-setup-commands.md` for the exact command sequence that worked end-to-end.
