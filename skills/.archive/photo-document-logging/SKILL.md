---
name: photo-document-logging
description: "Use when photos build a persistent, appended .md document."
version: 1.0.0
author: curator
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [photos, markdown, logging, document, append, extraction]
---

# Photo → Appended Markdown Document

Class of work: the user sends a series of photos and wants each photo's extracted
content **appended as a new entry** to ONE persistent file (usually `.md`), which
grows over time and across sessions. Example: FGD Sekolah Herbal slide capture
(`/home/satyaaditech/FGD_Sekolah_Herbal.md`).

## Critical first step — confirm target format

When the user says "buat dokumen yang terus diupdate" + "saya kirim foto", DO NOT
assume a Google Sheet. In this user's workflow, a continuously-updated photo log is
frequently either a **single markdown file** ("satu file saja, tiap foto ditambah di dokumen")
or a **Google Document** (shared as "anyone with link can edit").
Ask once if ambiguous (markdown doc vs Google Doc vs spreadsheet vs per-date file), or wait for the first
photo and infer. A wrongly-created file/spreadsheet must be deleted — wasted work.

If the target is a **Google Doc**, follow the formatting and API guidelines in the
reference file `references/google-docs-append.md`. DO NOT write raw markdown symbols
(like `**`, `*`, `###`, etc.) inside a Google Doc; use native API paragraph and text styles
instead to maintain professional document legibility.

## Workflow

1. **Create the file** once: `# <Judul>` header + a short intro blockquote +
   an append anchor comment at the bottom:
   `<!-- ENTRI FOTO DI-TAMBAHKAN DI BAWAH GARIS INI -->`
   (anchor stays last; every new entry is inserted directly above it).
2. **Per photo received:**
   a. Get the real timestamp: `date +"%Y-%m-%d %H:%M"` — NEVER compute dates
      mentally (zero-tolerance date rule; a manual +1 error caused a missed
      appointment before).
   b. Extract content from the photo description / vision_analyze result.
   c. `patch` (replace mode): old_string = the anchor comment, new_string =
      entry + anchor again. This keeps the anchor at the bottom and appends
      in file order.
3. **Entry structure** (kept consistent for every entry):
   ```
   ---

   ## Entri N — YYYY-MM-DD HH:MM

   **Slide XX — "<Judul Slide>"** (+ subtitle / legal reference if any)

   ### Subsection
   1. item
   2. item

   > Key quote / banner text verbatim.

   ### Pesan Penutup

   > Bottom banner message verbatim.

   ---

   <!-- ENTRI FOTO DI-TAMBAHKAN DI BAWAH GARIS INI -->
   ```
   - Keep slide numbering from the deck (e.g. "Slide 05"); note slide number if
     visible only in a corner.
   - Preserve quoted text exactly; keep official names/numbers (UU No., PP No.,
     Pasal) verbatim — do not paraphrase legal references.
   - Use emoji bullets sparingly for short list slides; full structured headings
     for dense slides.
4. **Reply**: short summary (slide + key points) + deliver the full file:
   `MEDIA:/absolute/path/file.md` (user reads the complete file on mobile).
5. **Remember** the file path + convention in memory so the next session
   continues the same file (append, never create a second file for the same doc).

## Pitfalls

- Never overwrite the file — only append via the anchor marker. `write_file`
  replaces everything; use `patch` for appends.
- Keep entry numbers sequential (Entri 1, 2, 3, ...) even across sessions.
- If a photo shows TWO columns/sections (e.g. "C. X" + "D. Y"), record both as
  separate `###` subsections in one entry — don't split into two entries.
- Slides from a presentation are often sent out of numeric order; that's fine,
  entries follow arrival order, slide numbers stay as printed.
- If the user later says "jadikan satu file" they mean one document for this
  topic, not one file per photo or per date.
