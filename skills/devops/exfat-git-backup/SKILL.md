---
name: exfat-git-backup
description: Use when backing up files from exfat/non-POSIX drives.
category: devops
---

# Git on exfat (non-POSIX) Backups

This skill provides the workflow and setup instructions to initialize, track, and back up files stored on non-POSIX filesystems (like exfat, FAT32) to remote Git platforms (like GitHub) under Linux.

## Trigger Conditions

Use this skill when:
- Setting up a backup for a folder located on an external/USB drive formatted as exfat or FAT32.
- Encountering permission errors (`Operation not permitted` / `chmod` fail) while running `git init` or config/branch updates on a mounted USB storage.
- Administering automated backups (via cron job) of local data on external drives.

## Pitfall: The exfat chmod Error
By default, Git attempts to change file permissions (using `chmod`) for its lock and configuration files inside the `.git` directory. When the filesystem is exfat, FAT, or NTFS mounted on Linux without specific permission-mapping options (like `quiet`), `chmod` fails with `Operation not permitted`:
```text
error: chmod on /path/to/repo/.git/config.lock failed: Operation not permitted
fatal: could not set 'core.repositoryformatversion' to '0'
```

## Setup Workflow: Hybrid Git Directory

To bypass filesystem limitations, decouple the Git configuration repository (metadata) from the actual directory containing the files (working tree).

1. **Delete failed repository attempts**:
   ```bash
   rm -rf /mnt/usb/my-vault/.git
   ```

2. **Initialize Git in a local ext4 directory** (e.g., home directory):
   ```bash
   git init /home/user/.my_vault_git
   ```
   *Note: Since this directory is on a POSIX filesystem (ext4), Git will create locks and files without errors.*

3. **Rename the default branch** (since renaming config metadata works fine on ext4):
   ```bash
   git -C /home/user/.my_vault_git branch -M main
   ```

4. **Point the Git Instance to the exfat Working Tree**:
   ```bash
   git -C /home/user/.my_vault_git config core.worktree /mnt/usb-vault-path
   ```

5. **Register Safe Directory** (if git complains about dubious ownership due to exfat root/user mapping):
   ```bash
   git config --global --add safe.directory /mnt/usb-vault-path
   ```

## Backups & Cron Automation

Create a dedicated shell backup script using the `-C` argument to target the ext4 Git directory:

```bash
#!/bin/bash
set -e

# Stage edits from the work tree
git -C /home/user/.my_vault_git add .

# Check if there are changes to commit
if ! git -C /home/user/.my_vault_git diff-index --quiet HEAD --; then
    git -C /home/user/.my_vault_git commit -m "Auto backup: \$(date '+%Y-%m-%d %H:%M:%S')"
    # Push back changes to GitHub
    git -C /home/user/.my_vault_git push origin main
fi
```
