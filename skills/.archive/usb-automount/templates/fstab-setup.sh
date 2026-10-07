#!/usr/bin/env bash
# Idempotent USB auto-mount setup via fstab + systemd automount.
# Usage: sudo bash fstab-setup.sh   (user types password once in their terminal)
# Copy, edit UUIDs / mount points / fs types for the actual drives.
set -euo pipefail

FSTAB=/etc/fstab
LINES=(
  "# ===== USB flash drive auto-mount ====="
  "UUID=<UUID1> /mnt/usb-nvme exfat nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0"
  "UUID=<UUID2> /mnt/usb-ubuntu vfat nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0"
)

# Idempotent: skip if marker already present
if grep -q "usb-nvme" "$FSTAB"; then
  echo "OK: fstab already has auto-mount. Skipping append."
else
  cp "$FSTAB" "${FSTAB}.bak-$(date +%Y%m%d-%H%M%S)"
  printf '%s\n' "${LINES[@]}" | tee -a "$FSTAB" >/dev/null
  echo "OK: fstab updated (backup created)."
fi

mkdir -p /mnt/usb-nvme /mnt/usb-ubuntu
systemctl daemon-reload
echo "OK: daemon-reload done."

findmnt --verify --fstab 2>&1 | grep -E 'error' | head -10 || true
echo "SELESAI. Next: sudo systemctl start mnt-usb\\x2dnvme.automount mnt-usb\\x2dubuntu.automount (runtime one-time start)."
