---
name: daily-todo-list
description: "Buat to-do list harian + reminder cron 13:00 & 17:00."
version: 1.0.0
author: Hermes Agent
tags: [todo, reminder, daily, productivity, telegram]
---

# Daily To-Do List

Buat dan kelola to-do list harian untuk Pak Satya. File markdown satu per hari, dengan dua reminder cron (siang & sore) yang otomatis mengingatkan.

## File Lokasi & Penamaan

- Direktori: `/home/satyaaditech/todolist/`
- Nama file: `YYYY-MM-DD.md` (contoh: `2026-08-12.md`)

## Format File

```markdown
# To-Do List Harian — [Hari], [Tanggal Bulan Tahun]

## Tugas Hari Ini

- [ ] 1. [deskripsi tugas]
- [x] ~~2. [tugas selesai]~~

## Catatan

- Dibuat: [hari, tanggal, jam]
```

**Aturan format:**
- Tugas **belum selesai**: `- [ ] nomor. deskripsi` (kotak kosong)
- Tugas **sudah selesai**: `- [x] ~~nomor. deskripsi~~` (centang + strikethrough)
- Response ke user gunakan emoji: ☐ untuk belum, ☑ + ~~strikethrough~~ untuk selesai

## Pitfall — JANGAN centang dulu

**JANGAN PERNAH** kasih centang hijau (✅ / ☑) atau `[x]` untuk tugas yang BELUM dikerjakan. Semua tugas baru harus dalam keadaan kotak kosong (`- [ ]` / ☐). Hanya tandai selesai ketika user secara eksplisit mengatakan sudah dikerjakan.

## Reminder Cron

Setiap pembuatan to-do list baru, buat 2 cron job one-shot:

1. **Siang (13:00 WIB)**
2. **Sore (17:00 WIB)**

**Prompt wajib mengandung:**
- Sebut SEMUA tugas (update prompt setiap tugas bertambah/berkurang)
- Format ☐ untuk belum, ☑ ~~strikethrough~~ untuk selesai
- Akhiri dengan: `Wajib kirim pesan — tidak boleh [SILENT], tidak boleh kosong, harus dikirim.`

Gunakan `schedule: 2026-08-12T13:00:00` / `2026-08-12T17:00:00`, `repeat: 1` (one-shot).

## Workflow

### Membuat Baru
1. `date` untuk hari & tanggal
2. Buat file `.md` di `/home/satyaaditech/todolist/`
3. Buat 2 cron reminder

### Menambah Tugas
1. Patch file — tambahkan `- [ ] nomor. tugas`
2. Update prompt kedua cron reminder

### Menandai Selesai
1. Patch file: `- [ ]` → `- [x] ~~teks~~`
2. Response: tampilkan dengan ☑ ~~strikethrough~~
3. One-shot reminder yang sudah lewat akan hilang — update hanya yang masih aktif
