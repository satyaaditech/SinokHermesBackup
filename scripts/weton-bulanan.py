#!/usr/bin/env python3
"""Weton bulanan — dipanggil cron tiap tanggal 1. Output selalu non-empty."""
from datetime import date
import calendar

PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
WEEKDAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
# Anchor terverifikasi (Wikipedia): 28-08-2025 = Kamis Pahing
ANCHOR = (date(2025, 8, 28), 3, 1)

def weton(d):
    ad, aw, ap = ANCHOR
    days = (d - ad).days
    return WEEKDAYS[(aw + days) % 7], PASARAN[(ap + days) % 5]

today = date.today()
y, m = today.year, today.month
last = calendar.monthrange(y, m)[1]

month_names = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
               "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

lines = [f"📅 WETON {month_names[m-1].upper()} {y}", ""]
for d in range(1, last + 1):
    dd = date(y, m, d)
    w, p = weton(dd)
    lines.append(f"{d:>2} {w} {p}")

print("\n".join(lines))
