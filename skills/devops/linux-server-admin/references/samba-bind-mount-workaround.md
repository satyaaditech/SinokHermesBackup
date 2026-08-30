# Samba Bind Mount Workaround (Restricted Sudo / No Samba Config Access)

Use this pattern when you want to share a directory via Samba (SMB), but you do not have permission to edit `/etc/samba/smb.conf` (e.g., missing sudo password to edit the config or restart `smbd`) but you DO have restricted sudo permissions to run `mount`, `umount`, and `mkdir`.

## Context & Constraints
- You need to expose a directory (e.g. `/mnt/usb-nvme/obsidian/`) via SMB so a client (like macOS Finder) can open it.
- `/etc/samba/smb.conf` is read-only and `systemctl restart smbd` is blocked behind a password prompt.
- An existing Samba share is already active and writeable (e.g. `[ShortsFactory]` sharing `/home/satyaaditech/shorts_factory`).

## Solution: Bind Mount into an Active Share
A Linux bind mount mirrors a directory tree to another point. Samba treats the mounted files as if they were natively inside the shared folder.

### Step 1: Create the mount point inside the active share
Create a subdirectory under the existing shared path:
```bash
mkdir -p /home/satyaaditech/shorts_factory/obsidian
```

### Step 2: Perform the Bind Mount
Mount the source directory containing the files to the newly created subdirectory:
```bash
sudo mount --bind /mnt/usb-nvme/obsidian /home/satyaaditech/shorts_factory/obsidian
```
*(Requires `mount` to be permitted in sudoers via `NOPASSWD`)*

### Step 3: Ensure Persistence (User Crontab @reboot)
Since `/etc/fstab` cannot be edited without root write permissions and systemd daemon reload:
1. Append a `@reboot` rule to the user's crontab:
   ```bash
   (crontab -l 2>/dev/null; echo "@reboot sudo mount --bind /mnt/usb-nvme/obsidian /home/satyaaditech/shorts_factory/obsidian") | crontab -
   ```
2. Verify:
   ```bash
   crontab -l
   ```
