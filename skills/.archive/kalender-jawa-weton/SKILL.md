---
name: kalender-jawa-weton
description: Use when computing Javanese weton/pasaran dates.
---

# Kalender Jawa / Weton (hari pasaran)

Hitung weton untuk tanggal Masehi, atau cari tanggal dengan weton tertentu (mis. "Jumat Pahing bulan ini tanggal berapa?"). JANGAN pernah menghitung mental — selalu jalankan script (aturan ZERO TOLERANCE tanggal: `datetime.now()` dulu, echo tanggal hari ini, baru jawab).

## Anchor TERVERIFIKASI
Sumber: Wikipedia id "Hari pasaran" (siklus selapan 35 hari, contoh eksplisit di halaman):
- **28-08-2025 = Kamis Pahing**, dan 02-10-2025 & 06-11-2025 juga Kamis Pahing (+35 hari tiap) — konsisten, bisa dipakai cross-check.
- Urutan pasaran: Legi (0) → Pahing (1) → Pon (2) → Wage (3) → Kliwon (4)
- Hari: Senin (0) … Minggu (6)
- Weton = (index hari + selisih hari) mod 7, (index pasaran + selisih hari) mod 5

## Cara pakai
```bash
python3 scripts/weton.py                          # weton hari ini
python3 scripts/weton.py 2026-08-28               # weton tanggal tertentu
python3 scripts/weton.py Jumat Pahing 2026-08     # semua tanggal dgn weton itu di bulan itu
```

## Pitfalls (penting!)
1. **Anchor dari ingatan TIDAK cukup.** Di sesi 2026-08, dua anchor populer — "17-08-1945 = Jumat Legi" dan "01-01-2024 = Senin Legi" — menghasilkan mismatch (satu pasti salah). Selalu verifikasi anchor terhadap tanggal TERDOKUMENTASI dari sumber (Wikipedia "Hari pasaran" punya contoh eksplisit + siklus 35 hari), lalu cross-check minimal 2-3 tanggal sebelum menjawab.
2. **Bulan tidak selalu punya weton tsb.** Interval weton = 35 hari. Contoh: Jumat Pahing Agustus 2026 hanya 28-08; berikutnya 02-10-2026. Cek bulan target + bulan setelahnya agar jawaban tidak menyesatkan.
3. **Verifikasi web saat ragu** pakai pola curl + r.jina.ai (Google diblok 403, Bing jalan; detail di skill `web-research-fallback`). `web_extract`/Firecrawl bisa error → jangan bergantung.
4. Kalau user hanya tanya "Jumat Pahing bulan ini", jawab tanggal + konteks hari ini (mis. "hari ini Senin Wage") — membantu user memastikan.

## Support files
- `scripts/weton.py` — kalkulator weton (deterministik, re-runnable)
