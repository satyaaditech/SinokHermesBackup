# Known-good setup commands (verified 2026-08-10, Ubuntu 22.04, kernel 5.15)

Full sequence that worked for two USB drives (256G exFAT "Nvme", 16G FAT32 Ubuntu installer) on Hermes server n8nserver.

## 1. Detect
```
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL,TRAN | grep -v loop
lsblk -f /dev/sdc /dev/sdd     # FSTYPE LABEL UUID
```
Sample: sdc2 exfat label Nvme UUID=6960-FA27; sdd1 vfat label UBUNTU-SERV UUID=FCF7-CC69.

## 2. Limited sudoers (user runs in own terminal, once)
```
echo 'satyaaditech ALL=(ALL) NOPASSWD: /usr/bin/mount, /usr/bin/umount, /usr/bin/mkdir' | sudo tee /etc/sudoers.d/hermes-mount && sudo chmod 440 /etc/sudoers.d/hermes-mount
```
Check: `sudo -n mount -l | head -1` → runs; `sudo -n rm /tmp/x` → "a password is required".

## 3. fstab entries (validated syntax first via `findmnt --verify --tab-file /tmp/fstab.test`)
```
UUID=6960-FA27 /mnt/usb-nvme exfat nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0
UUID=FCF7-CC69 /mnt/usb-ubuntu vfat nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0
```
Append + `systemctl daemon-reload` (needs user's sudo — package in a script they run).

## 4. Runtime activation (the step everyone forgets)
After daemon-reload, units exist but are inactive. Start once:
```
sudo systemctl start 'mnt-usb\x2dnvme.automount' 'mnt-usb\x2dubuntu.automount'
```
(path-based `systemctl start /mnt/usb-nvme /mnt/usb-ubuntu` also works)

## 5. Verify
```
systemctl list-units --all 'mnt-usb*'   # automount units: active (waiting)
ls /mnt/usb-nvme                        # triggers mount on access
df -h | grep usb                        # /dev/sdc2 ... /mnt/usb-nvme
```

## Errors hit this session (transcripts)
- `udisksctl mount` → `NotAuthorizedCanObtain: Not authorized to perform operation` (polkit, headless) — abandoned
- `sudo -n` anything outside the 3 allowed cmds → `sudo: a password is required`
- `systemctl start mnt-usb-nvme.automount` → `Unit mnt-usb-nvme.automount not found` (hyphen NOT escaped in command; unit name has \x2d)
- `systemctl start 'mnt-usb-*.automount'` → warning, no effect (glob doesn't expand escaped names)
- stray line `24` in fstab → `findmnt: /etc/fstab: parse error at line 15 -- ignored`; fixed with `sed -i -E '/^[0-9[:space:]]+$/d' /etc/fstab` + daemon-reload
