---
name: linux-usb-automount
description: Use when auto-mounting USB drives on a Linux server.
---

# USB Auto-Mount (Linux server)

Auto-mount USB flash drives via fstab + systemd automount: colok = siap pakai, cabut = aman, boot tetap jalan tanpa drive.

## Prasyarat akses root terbatas (pola aman)

Hermes biasanya tidak punya sudo. Jangan minta password lewat chat. User menjalankan sendiri di terminal server:

```bash
echo 'satyaaditech ALL=(ALL) NOPASSWD: /usr/bin/mount, /usr/bin/umount, /usr/bin/mkdir' | sudo tee /etc/sudoers.d/hermes-mount && sudo chmod 440 /etc/sudoers.d/hermes-mount
```

Verifikasi: `sudo -n mount -l` jalan tanpa password; `sudo -n rm /tmp/x` DITOLAK (rule hanya mount/umount/mkdir). Edit `/etc/fstab` TIDAK tercakup — user harus jalankan script setup dengan password-nya sendiri (sekali).

## Setup (fstab entry)

```
UUID=<UUID> /mnt/<name> <fstype> nofail,noatime,nosuid,nodev,umask=000,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.device-timeout=5 0 0
```

- `nofail` → boot aman tanpa drive
- `x-systemd.automount` → lazy mount saat path diakses
- `x-systemd.idle-timeout=600` → auto-unmount setelah 10 menit idle (aman dicabut)
- `umask=000` → semua user bisa baca/tulis (exFAT/FAT32 root-owned)
- exFAT: `exfat`; FAT32: `vfat`; pastikan kernel punya exfat (5.15+ sudah)

Jalankan dalam script idempotent (grep dulu sebelum append), user eksekusi `sudo bash setup.sh` di terminal sendiri. Validasi sintaks SEBELUM daemon-reload: `findmnt --verify --tab-file <file-gabungan>` (harus 0 parse errors).

## Re-plugging / Pasca Cabut-Pasang Drive

Jika drive dicabut secara fisik dan dipasang kembali, systemd.automount terkadang tidak langsung melakukan mount secara otomatis ketika diakses. Hubungkan/mount ulang dengan langkah:

1. **Cek ketersediaan partisi dan UUID:**
   ```bash
   lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,UUID
   ```
2. **Mount manual sesuai target fstab:**
   ```bash
   sudo mount <mountpoint>   # Contoh: sudo mount /mnt/usb-nvme
   ```

## Pitfalls

1. **Nama unit systemd dengan hyphen di-escape `\x2d`.** Mount point `/mnt/usb-nvme` → unit `mnt-usb\x2dnvme.automount`, BUKAN `mnt-usb-nvme.automount`. `systemctl start mnt-usb-nvme.automount` gagal "Unit not found"; glob `mnt-usb-*.automount` juga tidak match. Start manual pakai path: `sudo systemctl start /mnt/usb-nvme /mnt/usb-ubuntu` ATAU nama literal escape: `sudo systemctl start 'mnt-usb\x2dnvme.automount'`.
2. **fstab diubah saat runtime → unit belum start.** Setelah `daemon-reload`, unit terdaftar (generator `/run/systemd/generator/`) tapi `inactive dead`. Perlu start manual SATU KALI (`systemctl start` unit/automount). Setelah reboot, fstab-generator auto-start unit (local-fs.target). Cek status: `systemctl list-units --all 'mnt-usb*'` → `active (waiting)` = sehat.
3. **Baris sampah di /etc/fstab.** Bisa ada baris angka nyasar (mis. "24") yang bikin `parse error at line N`. Fix: `sed -i -E '/^[0-9[:space:]]+$/d' /etc/fstab` + `systemctl daemon-reload` + `findmnt --verify --fstab`.
4. **ufw aktif default deny** memblokir akses service dari luar — bukan masalah mount, tapi akses remote (lihat skill terkait Tailscale).

## Verifikasi selesai

```bash
systemctl list-units --all 'mnt-usb*' --no-pager   # automount active (waiting)
ls /mnt/<name>                                      # memicu automount, isi tampil
df -h /mnt/<name>                                   # filesystem ter-mount
```

## Notes

- Data yang sedang ditulis saat dicabut = risiko korup (wajar semua USB, exFAT tanpa journaling).
- File `._*` dan `.fseventsd` di exFAT = artefak macOS, bisa dibersihkan.
- Setup aktif di n8nserver: `/mnt/usb-nvme` (exFAT 256G, UUID 6960-FA27), `/mnt/usb-ubuntu` (vfat installer, UUID FCF7-CC69). Script ada di `~/usb-automount/`.
