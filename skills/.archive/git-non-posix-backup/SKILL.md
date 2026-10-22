---
name: git-non-posix-backup
description: Use when git on exfat/FAT filesystems fails with EPERM.
version: 1.0.0
author: Sinox
category: devops
---

# Git Backup on non-POSIX Filesystems (exfat, vfat, NTFS)

Use this skill when attempting to initialize parent Git repositories or make commits on external, non-POSIX partitions (exfat/vfat/NTFS mount points) where standard Linux file permission modifications (`chmod`, `chown`) fail and yield `EPERM (Operation not permitted)` errors.

## Trigger Conditions
- Running `git init` on an exfat/vfat/NTFS mount yields: `error: chmod on ... failed: Operation not permitted`
- Git commands fail with: `fatal: could not set 'core.repositoryformatversion' to '0'` or errors relating to lock files.

## The Dual-Directory Strategy

Since FAT/exfat filesystems do not support POSIX permission rules, Git cannot write lock configuration files directly onto the partition without failing on permission checks. 

To overcome this, **store the Git database (`.git` directory) on a POSIX-compliant local filesystem (like ext4)** and target the external drive folder as the **Working Tree** (`--work-tree`).

### Step-by-Step Implementation

1. **Clean up any failed attempts**:
   Ensure no broken `.git` directory is left in the target directory:
   ```bash
   rm -rf /mnt/usb-drive/my-folder/.git
   ```

2. **Initialize Git outside the non-POSIX volume**:
   Create a dedicated Git directory folder on a native Linux disk partition (e.g., your home directory):
   ```bash
   git init ~/.my-folder_git
   ```

3. **Link the work tree to your non-POSIX partition**:
   Configure the repository to use the exfat/NTFS path as its working directory:
   ```bash
   git -C ~/.my-folder_git config core.worktree /mnt/usb-drive/my-folder
   ```

4. **Change the default branch (optional but standard)**:
   ```bash
   git -C ~/.my-folder_git branch -M main
   ```

5. **Run Git commands pointing to the git-dir**:
   All git commands must be run referencing the local directory:
   ```bash
   # Check status
   git -C ~/.my-folder_git status

   # Stage updates
   git -C ~/.my-folder_git add .

   # Commit changes
   git -C ~/.my-folder_git commit -m "my commit message"
   ```

## Chronological Auto-backup Script Example

If setting up automated backups via CRON, include the `-C` argument targeting the local git-dir path:

```bash
#!/bin/bash
set -e

# Add changes
git -C /home/username/.my-folder_git add .

# Commit only if there are modifications
if ! git -C /home/username/.my-folder_git diff-index --quiet HEAD --; then
    git -C /home/username/.my-folder_git commit -m "Auto backup: $(date '+%Y-%m-%d %H:%M:%S')"
    # Push to origin
    git -C /home/username/.my-folder_git push origin main >/dev/null 2>&1
fi
```

## Troubleshooting & Dubious Ownership

If you hit `fatal: detected dubious ownership in repository` because the external USB is mounted under a different user or `root`, whitelist the path:

```bash
git config --global --add safe.directory /mnt/usb-drive/my-folder
```
