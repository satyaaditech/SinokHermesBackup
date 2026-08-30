# Membaca Output Delegasi yang Terpotong (Orchestrator)

Saat mengorkestrasi alur 3-role (Researcher→Writer→Editor) via `delegate_task`, hasil
subagent sering masuk TERPOTONG ke conversation (baris `[SUMMARY TRUNCATED]`). Jangan
panic — path penuh selalu dicetak di footer pesan:

```
Full subagent output saved to: /home/satyaaditech/.hermes/cache/delegation/subagent-summary-0-<timestamp>.txt
```

Baca dengan `read_file` + pindai offset untuk dapat teks lengkap. Nama file memuat
timestamp mulai, bukan ID delegasi.

## Jalur lain yang berguna

- **Live transcript** (streaming tool/think/final per langkah):
  `/home/satyaaditech/.hermes/cache/delegation/live/<delegation_id>/task-0.log`
  — untuk memantau progres & melihat status selesai. Status `final status=completed`.
- **Manifest** (ID, status tiap task):
  `/home/satyaaditech/.hermes/cache/delegation/live/<delegation_id>/manifest.json`

## Workflow praktis

1. Dispatch delegasi pertama (Researcher). Jangan polling — hasil masuk sebagai pesan.
2. Kalau perlu progres: baca `live/<id>/task-0.log` (line terakhir = status).
3. Saat hasil masuk: kalau terpotong, `read_file` file `subagent-summary-0-*.txt` dari
   footer untuk konten penuh.
4. Meneruskan hasil (mis. Sabda ke Writer, draft ke Editor): SALIN teks lengkap dari
   file summary ke `context` delegasi berikutnya — subagent baru TIDAK mewarisi konteks.

## Catatan trigger

- Delegasi child model = config `delegation.*` (base_url/api_key/model). Ganti ke
  OpenCode sebelum dispatch Writer/Editor & RESTORE ke OmniRoute seusai — lihat
  `references/provider-opencode-deepseek.md`.
- Leader subagent tidak bisa baca `/tmp/*.txt`? Bukan — semua subagent pakai filesystem
  host yang sama; pastikan path benar.