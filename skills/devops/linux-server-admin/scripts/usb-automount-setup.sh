#!/usr/bin/env bash
# Setup USB auto-mount via fstab + systemd automount
# Usage: sudo bash usb-automount-setup.sh
# Idempotent — safe to re-run.
set -euo pipefail

FSTAB=/etc/fstab
DRIVES=(
  "UUID=6960-FA27|/mnt/usb-nvme|exfat"
  "UUID=FCF7-CC69|/mnt/usb-ubuntu|vfat"
)

# Common options for removable media
# nofail: boot continues if drive missing
# noatime: reduce writes on flash
# nosuid,nodev: security hardening
# umask=000: world read/write (exFAT/vFAT)
# x-systemd.automount: mount on first access
# x-systemd.idle-timeout=600: auto-unmount after 10 min idle
# x-systemd.device-timeout=5: fast failure if missing
OPTS="nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5"

HEADER="# ===== USB flash drive auto-mount ($(date +%Y-%m-%d)) ====="

if grep -q "usb-nvme" "$FSTAB"; then
  echo "OK: fstab already contains USB auto-mount entries. Skipping."
  exit 0
fi

cp "$FSTAB" "${FSTAB}.bak-$(date +%Y%m%d-%H%M%S)"
{
  echo "$HEADER"
  for drive in "${DRIVES[@]}"; do
    IFS='|' read -r uuid mountpoint fstype <<< "$drive"
    echo "$uuid $mountpoint $fstype $OPTS 0 0"
    mkdir -p "$mountpoint"
  done
} | tee -a "$FSTAB" >/dev/null

systemctl daemon-reload

# Start automount units (path-based — more reliable than escaped names)
for mountpoint in /mnt/usb-nvme /mnt/usb-ubuntu; do
  # Try path-based start first
  systemctl start "$mountpoint" 2>/dev/null && echo "  started $mountpoint" || \
  # Fallback: escaped unit name
  unit="mnt-${mountpoint#/mnt/}"
  unit="${unit//-/\\\\x2d}"
  systemctl start "${unit}.automount" 2>/dev/null || \
    echo "  warning: could not start $mountpoint (may need manual start or reboot)"
done

echo "DONE. Drives will auto-mount on access. Safe to unplug after 10 min idle."
