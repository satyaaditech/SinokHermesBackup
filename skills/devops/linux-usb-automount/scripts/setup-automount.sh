#!/usr/bin/env bash
# Setup auto-mount USB flash drive via fstab + systemd automount.
# Dijalankan SEKALI oleh user: sudo bash setup-automount.sh
# Idempotent: aman dijalankan ulang.
set -euo pipefail

FSTAB=/etc/fstab
LINES=(
  "# ===== USB flash drive auto-mount (ditambahkan) ====="
  "UUID=<UUID1> /mnt/usb-1 exfat nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0"
  "UUID=<UUID2> /mnt/usb-2 vfat nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0"
)

if grep -q "/mnt/usb-1" "$FSTAB"; then
  echo "OK: fstab sudah berisi auto-mount. Lewat."
else
  cp "$FSTAB" "${FSTAB}.bak-$(date +%Y%m%d-%H%M%S)"
  printf '%s\n' "${LINES[@]}" | tee -a "$FSTAB" >/dev/null
  echo "OK: fstab diupdate (backup dibuat)."
fi

mkdir -p /mnt/usb-1 /mnt/usb-2
systemctl daemon-reload
echo "OK: daemon-reload selesai."
findmnt --verify --fstab 2>&1 | grep -E 'error|OK' | head -10 || true
echo "SELESAI."
