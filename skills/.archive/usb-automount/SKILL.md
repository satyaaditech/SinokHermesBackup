---
name: usb-automount
description: Use when auto-mounting USB drives on a Linux server.
---

# USB Drive Auto-Mount (Linux server)

Headless Ubuntu/Debian server: make USB flash drives auto-mount when plugged, safe to unplug, no boot errors. Follows the "password never in chat" rule — privileged commands run by the USER in their own terminal (SSH console), the agent prepares scripts and verifies after.

## Detect drives

```bash
lsblk -o NAME,SIZE,TYPE,TRAN,MODEL   # TRAN=usb => removable
lsblk -f /dev/sdX                     # FSTYPE + UUID (vfat/exfat/ext4)
```

exfat mounts natively on kernel 5.15+ (no exfat-fuse needed).

## Scoped sudoers rule (mount ops only, no password)

User runs ONCE in their own terminal:

```bash
echo 'user ALL=(ALL) NOPASSWD: /usr/bin/mount, /usr/bin/umount, /usr/bin/mkdir' | sudo tee /etc/sudoers.d/hermes-mount && sudo chmod 440 /etc/sudoers.d/hermes-mount
```

Verify: `sudo -n mount -l` works; `sudo -n rm /tmp/x` is REFUSED ("a password is required"). Only mount/umount/mkdir freed — everything else still needs a password.

**NOTE:** this rule does NOT cover editing /etc/fstab, `systemctl start`, or sed on /etc. For those, prepare a script in the user's home and have them run `sudo bash script.sh` (password typed once, in their terminal, never in chat).

## Runtime activation (fstab edited while server is running)

fstab edits only REGISTER units — they stay `inactive dead` until started once:

```bash
sudo systemctl start 'mnt-usb\x2dnvme.automount' 'mnt-usb\x2dubuntu.automount'
```

Then `ls /mnt/usb-nvme` triggers the mount. After a reboot, generator units auto-start (no manual step needed).

## Re-plugging (Cabut-Pasang Drive)

Jika drive dicabut secara fisik dan dipasang kembali, systemd.automount terkadang tidak langsung me-mount ketika dideteksi. Lakukan pengecekan dan mounting manual:

1. **Cek koneksi dan UUID:**
   ```bash
   lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,UUID
   ```
2. **Mount manual ke path fstab:**
   Jika entri sudah ada di `/etc/fstab` (seperti `/mnt/usb-nvme`), jalankan:
   ```bash
   sudo mount <mountpoint>   # Contoh: sudo mount /mnt/usb-nvme
   ```

## Pitfall: systemd escapes hyphens in unit names

`/mnt/usb-nvme` → unit `mnt-usb\x2dnvme.automount`. Plain `mnt-usb-nvme.automount` fails with "Unit not found". `systemctl start 'mnt-usb-*.automount'` (glob) expands to loaded units and has NO effect on un-started ones. Path-based `systemctl start /mnt/usb-nvme` also resolves. Watch for `\x2d` in `systemctl list-units` output — that IS the unit, not a typo.

## Pitfall: junk lines in /etc/fstab

A stray line containing only digits/whitespace (e.g. `24`) makes `findmnt --verify` report "parse error at line N" and silently drops the new USB entries. Fix: `sed -i -E '/^[0-9[:space:]]+$/d' /etc/fstab`, then `systemctl daemon-reload`. Validate before touching /etc with `cat /etc/fstab <(echo new lines) > /tmp/t && findmnt --verify --tab-file /tmp/t` → expect `0 parse errors`.

## fstab entry (per drive, by UUID)

```
UUID=<UUID> /mnt/<name> <fstype> nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0
```

- `nofail` — boot OK even when drive absent
- `x-systemd.automount` — mount on first access when plugged
- `idle-timeout=600` — auto-unmount after 10 min idle → safe to pull
- `umask=000` — any user can read/write (single-user personal box)
- `device-timeout=5` — no long hang when drive is missing

## Setup procedure (server already up — runtime change)

1. Validate fstab additions WITHOUT touching /etc:
   `cat /etc/fstab fstab.append > /tmp/fstab.test && findmnt --verify --tab-file /tmp/fstab.test` → expect "0 parse errors"
2. Append via user-run script: backup first, grep-check idempotency, `systemctl daemon-reload`.
3. **PITFALL: daemon-reload only REGISTERS units — automount units stay inactive.** Must start once (runtime):
   `sudo systemctl start mnt-usb\x2dnvme.automount mnt-usb\x2dubuntu.automount`
   - Unit names ESCAPE the mount path: `/mnt/usb-nvme` → `mnt-usb\x2dnvme.automount` (hyphen = `\x2d`). Copy the exact name from `systemctl list-units --all 'mnt-*'`.
   - One-time only; after a real reboot fstab automount units auto-start.
4. Test: `ls /mnt/<name>` triggers mount; verify with `df -h /mnt/<name>` (must show the USB device, not the root filesystem).

## Pitfalls

- **udisksctl mount fails on headless server** — polkit "NotAuthorizedCanObtain" / "Error creating textual authentication agent". Don't fight it; use fstab + systemd instead.
- **Junk lines in fstab → parse error**: a stray numeric line (e.g. `24`) breaks findmnt at that line number. Fix (user-run): `sed -i -E '/^[0-9[:space:]]+$/d' /etc/fstab` + `systemctl daemon-reload`.
- **`findmnt --verify --fstab` warnings** about `/swap.img` ("regular file") are pre-existing and harmless.
- **Never put the user's sudo password in chat or files.** Prepare scripts in the user's home; user runs with `sudo bash` and types the password once.
- **`ls` on a not-mounted empty mount point returns empty silently** — check `df -h` or `mount | grep <name>` to confirm real mount, don't trust empty ls output.

## Support files

- `templates/fstab-setup.sh` — idempotent append + daemon-reload + verify. Copy, edit UUIDs/mount points, have the user run it.
