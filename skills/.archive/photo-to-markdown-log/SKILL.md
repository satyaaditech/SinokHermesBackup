---
name: photo-to-markdown-log
description: "Use when user sends photos to append into a markdown doc."
version: 1.0.0
---

# Photo → Markdown Log

Extract content from photos (presentation slides, screenshots, scans, notes) and append each photo as a structured entry into ONE continuously-updated markdown file.

## Trigger

- "buat file .md, tiap foto yang kukirim tambahkan/append"
- "dokumen yang terus diupdate dari foto"
- User sends a series of photos one-by-one to be documented.

## Workflow

1. **Confirm format BEFORE creating anything.** User pattern: satu file .md, append per foto. If the request says "dokumen" ambiguously, ask explicitly: "file markdown (.md) atau Google Sheet?" Do NOT default to a spreadsheet — confirmed correction (FGD Sekolah Herbal, 2026-08): "satu file saja, setiap foto ditambahkan" meant a single .md, not a sheet.
2. Create the file with title + marker comment at the END:
   `<!-- ENTRI FOTO DI-TAMBAHKAN DI BAWAH GARIS INI -->`
   Save file path in memory so the next session continues the same file.
3. Per photo:
   - Timestamp: run `date +"%Y-%m-%d %H:%M"` — NEVER compute dates mentally (zero-tolerance date rule).
   - Extract ALL text: slide number, title, subtitle, bullets, quotes, footer.
   - `patch` (mode=replace): old_string = marker comment, new_string = new entry + marker comment again. Keeps entries ordered, never overwrites.
4. Entry format:
   ```
   ---

   ## Entri N — 2026-08-07 10:02

   **Slide 02 — "<Judul>"**

   **Subtitle:** ...

   > intro/quote

   ### Section Title

   1. **Item** — detail
   2. **Item** — detail

   ### Pesan Penutup

   > footer text

   ---
   ```
   Keep legal references verbatim: UU No., PP No., Pasal, putusan MK, quotes in original wording — these are the substance users rely on.
5. Deliver: short chat summary + `MEDIA:/abs/path/file.md` (user mobile — full file content, not just summary).
6. Close reply with invitation: "Foto berikutnya! 📸" — keeps the photo stream flowing.

## Pitfalls

- Building a Google Sheet when the user wants a markdown file → wrong tool. Ask md vs sheet first.
- Never overwrite/regenerate the file — always append before the marker comment.
- Dense slides with small text: if the auto image description is unclear, run `vision_analyze` on the cached image path (e.g. ~/.hermes/cache/images/img_*.jpg) before writing the entry.
- Timestamps must come from real `date` output, never estimated.
