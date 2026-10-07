#!/usr/bin/env bash
# Setup auto-mount USB drives via fstab + systemd automount.
# Run ONCE from user's own terminal: sudo bash setup-usb-automount.sh
# Idempotent — safe to re-run.
# EDIT: adjust LINES[] entries (UUID, mountpoint, fstype) per drive.
set -euo pipefail

FSTAB=/etc/fstab
LINES=(
  "# ===== USB flash drive auto-mount ====="
  "UUID=<UUID1> /mnt/<name1> <fstype1> nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0"
  "UUID=<UUID2> /mnt/<name2> <fstype2> nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0"
)

if grep -q "/mnt/<name1>" "$FSTAB"; then
  echo "OK: fstab already has auto-mount. Skipping."
else
  cp "$FSTAB" "${FSTAB}.bak-$(date +%Y%m%d-%H%M%S)"
  printf '%s\n' "${LINES[@]}" | tee -a "$FSTAB" >/dev/null
  echo "OK: fstab updated (backup made)."
fi

mkdir -p /mnt/<name1> /mnt/<name2>
systemctl daemon-reload
echo "OK: daemon-reload done."

findmnt --verify --fstab 2>&1 | grep -E 'error|OK' | head -10 || true
echo "DONE. Now start units (hyphen-escape names!):"
echo "  sudo systemctl start 'mnt-<name1-escaped>.automount' 'mnt-<name2-escaped>.automount'"
echo "  # or path-based: sudo systemctl start /mnt/<name1> /mnt/<name2>"
