#!/usr/bin/env python3
"""Kalkulator weton (hari pasaran Jawa) — deterministik, re-runnable.

Anchor terverifikasi dari Wikipedia id "Hari pasaran" (siklus selapan 35 hari):
    28-08-2025 = Kamis Pahing, 02-10-2025 = Kamis Pahing, 06-11-2025 = Kamis Pahing

Pemakaian:
    python3 weton.py                              # weton hari ini
    python3 weton.py 2026-08-28                   # weton tanggal tertentu
    python3 weton.py Jumat Pahing 2026-08         # semua tanggal weton itu di bulan itu
"""
import sys
from datetime import date

PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
WEEKDAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# (tanggal anchor, index weekday Senin=0, index pasaran Legi=0)
ANCHOR = (date(2025, 8, 28), 3, 1)  # Kamis Pahing


def weton(d):
    ad, aw, ap = ANCHOR
    days = (d - ad).days
    return WEEKDAYS[(aw + days) % 7], PASARAN[(ap + days) % 5]


def parse_date(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        sys.exit(f"Format tanggal salah: {s} (pakai YYYY-MM-DD)")


def main():
    args = sys.argv[1:]
    if not args:
        d = date.today()
        w, p = weton(d)
        print(f"Hari ini {d} = {w} {p}")
        return

    # Mode pencarian: weton.py <Hari> <Pasaran> <YYYY-MM>
    if len(args) == 3 and "-" in args[2] and len(args[2]) == 7:
        hari, pasaran, bulan = args[0].capitalize(), args[1].capitalize(), args[2]
        y, m = int(bulan[:4]), int(bulan[5:7])
        hits = []
        for day in range(1, 32):
            try:
                dd = date(y, m, day)
            except ValueError:
                break
            w, p = weton(dd)
            if w == hari and p == pasaran:
                hits.append(dd)
        if hits:
            for h in hits:
                print(h, "=", hari, pasaran)
        else:
            print(f"Tidak ada {hari} {pasaran} di {bulan}")
        return

    # Mode tanggal tunggal
    for a in args:
        d = parse_date(a)
        w, p = weton(d)
        print(f"{d} = {w} {p}")


if __name__ == "__main__":
    main()
