#!/bin/bash
set -e

# Ngunggah owah-owahan wonten Obsidian ngginakaken git-dir khusus
git -C /home/satyaaditech/.obsidian_git add .

# Lakukan commit menawi wonten owah-owahan enggal
if ! git -C /home/satyaaditech/.obsidian_git diff-index --quiet HEAD --; then
    git -C /home/satyaaditech/.obsidian_git commit -m "Auto backup Obsidian: $(date '+%Y-%m-%d %H:%M:%S')"
    # Kirim dhateng GitHub
    git -C /home/satyaaditech/.obsidian_git push origin main >/dev/null 2>&1
    echo "Backup Obsidian kasil dipun-unggah dhateng GitHub."
fi
