---
name: weton-jawa
description: Use when user asks weton/tanggal pasaran Jawa.
---

# Weton Jawa (hari pasaran)

Hitung weton (Saptawara + Pancawara) dengan anchor yang SUDAH TERVERIFIKASI dari Wikipedia "Hari pasaran".

## Anchor (WAJIB — jangan pakai hafalan lain)

```
28 Agustus 2025 = Kamis Pahing   (Kamis=3, Pahing=1)
```

Wikipedia menyebut contoh: 4 Des 2014, 28 Agu 2025, 2 Okt 2025, 6 Nov 2025 semua Kamis Pahing (siklus 35 hari / selapan).

## Urutan pasaran (pancawara)

```
Legi(0), Pahing(1), Pon(2), Wage(3), Kliwon(4)
```

## Hitung

```python
from datetime import date
PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
WEEKDAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
ANCHOR = (date(2025, 8, 28), 3, 1)  # Kamis Pahing

def weton(d):
    ad, aw, ap = ANCHOR
    days = (d - ad).days
    return WEEKDAYS[(aw + days) % 7], PASARAN[(ap + days) % 5]
```

## Langkah

1. Jalankan kode di atas (execute_code), echo `date.today()` dulu (aturan ZERO TOLERANCE).
2. Iterasi semua tanggal bulan yang diminta, cocokkan weekday + pasaran.
3. Laporkan tanggal + hari lengkap (contoh: "Jumat, 28 Agustus 2026").

## Pitfalls

- JANGAN pakai anchor hafalan (mis. 17-08-1945 Jumat Legi atau 01-01-2024 Senin Legi) — dua anchor itu terbukti TIDAK konsisten satu sama lain.
- Jumat Pahing Agustus 2026 = 28-08-2026; Senin Pon = 24-08-2026; Minggu Pon = 09-08-2026. Jadikan sanity check.
- Siklus weton = 35 hari (karena 7×5, lcm). Setiap tanggal tertentu naik 35 hari → weton sama.
