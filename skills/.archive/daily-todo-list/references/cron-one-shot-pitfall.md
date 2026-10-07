# Pitfall — cron one-shot hilang setelah fire

Cron one-shot (`repeat: 1`) menghapus dirinya sendiri setelah jam-nya lewat.

Gejala: user menambah/mengubah tugas setelah reminder 13:00 sudah fire, lalu
`cronjob(action='update', job_id='<13:00 job>')` return error:

```
"Job with ID or name '<id>' not found. Use cronjob(action='list') to inspect jobs."
```

Itu NORMAL, bukan error sistem. Solusi:

1. Jangan panic, jangan retry job yang sudah lewat (gagal terus).
2. Update saja job yang masih aktif (biasanya reminder sore 17:00).
3. Kalau perlu reminder tambahan untuk sisa hari, buat cron baru dengan
   `cronjob(action='create')` untuk jam berikutnya.

## Catatan format checklist (dikonfirmasi ulang 2026-08-12)

- Tugas baru = kotak kosong `- [ ]` / emoji ☐. JANGAN centang dulu.
- Tugas selesai (hanya setelah user bilang) = `- [x] ~~teks~~` / ☑ + strikethrough.
