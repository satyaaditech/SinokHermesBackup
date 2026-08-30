#!/bin/bash
set -e

# Navigasi dhateng direktori .hermes
cd /home/satyaaditech/.hermes

# Tambahaken owah-owahan
git add .

# Lakukan commit menawi wonten owah-owahan
if ! git diff-index --quiet HEAD --; then
    git commit -m "Auto backup: $(date '+%Y-%m-%d %H:%M:%S')"
    # Kirim dhateng GitHub
    git push origin main >/dev/null 2>&1
    echo "Backup Hermes kasil dipun-unggah dhateng GitHub."
fi
