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
    git push origin main
    echo "Backup kasil dipun-unggah."
else
    echo "Mboten wonten owah-owahan ingkang kedah dipun-backup."
fi
