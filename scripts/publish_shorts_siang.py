#!/usr/bin/env python3
import subprocess
import sys

if __name__ == "__main__":
    res = subprocess.run(
        ["/usr/bin/python3", "/home/satyaaditech/.hermes/scripts/publish_shorts_slot.py", "Slot 1 — Siang (12:00 WIB)"],
        capture_output=True,
        text=True
    )
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"Error: {res.stderr.strip()}", file=sys.stderr)
        sys.exit(res.returncode)
