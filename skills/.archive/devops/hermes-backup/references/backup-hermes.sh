#!/bin/bash
# Hermes Backup Script
# Backs up config, memory, skills, and cron data to a git repository.
# Excludes secrets: .env, auth.json, tokens.
# Usage: copy to ~/scripts/backup-hermes.sh, chmod +x, then run or cron it.

set -e

SOURCE="$HOME/.hermes"
BACKUP="$HOME/hermes-backup"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$BACKUP"

echo "[*] Syncing Hermes data..."

# Config & personality
cp -f "$SOURCE/config.yaml" "$BACKUP/" 2>/dev/null || true
cp -f "$SOURCE/SOUL.md" "$BACKUP/" 2>/dev/null || true

# Memory
mkdir -p "$BACKUP/memories"
rsync -a --delete "$SOURCE/memories/" "$BACKUP/memories/"

# Skills
mkdir -p "$BACKUP/skills"
rsync -a --delete "$SOURCE/skills/" "$BACKUP/skills/"

# Cron jobs
mkdir -p "$BACKUP/cron"
rsync -a --delete "$SOURCE/cron/" "$BACKUP/cron/"

cd "$BACKUP"

# Ensure git uses .netrc for HTTPS auth if present (disable helper cache)
git config --local credential.helper "" 2>/dev/null || true

if [ ! -d ".git" ]; then
    git init
    git checkout -b main 2>/dev/null || true
fi

git add -A
if git diff --cached --quiet; then
    echo "[*] No changes to commit."
else
    git commit -m "Hermes backup: $DATE"
    if git remote get-url origin >/dev/null 2>&1; then
        git push origin main
        echo "[*] Pushed to GitHub."
    else
        echo "[!] No remote configured. Skipping push."
    fi
fi

echo "[*] Backup complete: $DATE"
