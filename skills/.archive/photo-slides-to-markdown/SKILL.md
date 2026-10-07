---
name: photo-slides-to-markdown
description: "Use when user sends slide/doc photos to transcribe into .md or Google Doc."
version: 1.0.0
metadata:
  hermes:
    tags: [photos, markdown, transcription, notes, slides]
---

# Photo → Markdown Transcription Log

Workflow when user sends photos (presentation slides, documents, screens) and wants each photo's info appended to ONE persistent markdown file that keeps growing.

## Trigger
- User: "aku kirim beberapa foto, baca, buat file .md, tiap foto append" or similar.
- User requests transcribing slide/doc photos into a Google Doc progressively.
- Photos of slides/docs arrive in chat with instruction to record them into a named document or Google Doc.

## Google Docs Workflow
We can log/append to a Google Doc progressively instead of a local Markdown file.
See `references/google-docs-append.md` for specific creation, sharing, and batchUpdate append API scripts.

**Important Formatting Constraint**:
- **NEVER** write raw markdown symbols (like `**`, `*`, `###`, `---`, `_`) directly as text in Google Docs. Always strip them out and use clean spacing, or apply native styles programmatically via Google Docs API `batchUpdate` formatting requests.

## Final delivery (user-requested pattern)
When the user asks for the file link (or says processing is done), deliver a **download link**, NOT just "file saved on server". User's words: "setelah selesai proses kirim aku link download file terbaru".
1. **Preferred: Hermes-server HTTP link** — user corrected away from Drive ("linknya ke dokumen yang ada di server hermes aja gpp"). Recipe + pitfalls: `references/server-link-delivery.md`. Serve via a `~/share` symlink so the link auto-updates after every photo; the link can also be sent mid-processing.
2. **Fallback/backup: Google Drive link** — create-or-update the SAME filename so the URL stays stable across updates. Script + pitfalls: `references/drive-final-delivery.md`.

## Duplicate-photo handling (learned 2026-08-09)
Users often re-send the same slide/photo (galeri dobel or a retake). Before appending, run
`vision_analyze` asking: "apakah foto ini identik dengan entri sebelumnya? sebutkan nomor
slide" — if identical, SKIP the append and tell the user ("duplikat slide N, tidak di-append"),
keeping entry numbering intact. Exception: if a photo is a HIGHER-QUALITY retake of a partially
cut-off slide (e.g. first shot truncated Customer Segments), append it as a NEW entry with the
fuller text and note it completes the earlier entry.

## Key rule (learned from user correction)
User's "dokumen foto" / "satu file saja" = **satu file .md, append per foto**. NOT Google Sheets/spreadsheet, NOT a new file per photo. Building a Sheet first wasted work (had to delete it). When the format is ambiguous, ask ONE clarifying question before building.

## Upgrade version: foto asli + ekstrak Bahasa Indonesia + penjelasan
When the user wants an ONLINE Google Doc version of the upgrade (same title + content), use
`references/gdoc-from-markdown.md` — upload photos → build HTML → Drive-import to Google Doc.
User may ask for a "versi upgrade" of the transcription: each slide rendered as **📷 foto asli → 📝 hasil ekstrak (Bahasa Indonesia) → 💡 penjelasan**, alternating (their words: "content tersusun selang seling, photo asli -> hasil extract dalam bahasa Indonesia + penjelasan"). Recipe, feasibility check, and generator pattern: `references/upgrade-with-photos.md`. Key rules:
- Check total image size BEFORE embedding (base64 ≈ +33%); ~1.9 MB of photos → ~2.5 MB self-contained .md is fine.
- Generate via a Python script (data tuples + base64 + assemble), never hand-write 20+ entries.
- Symlink the upgraded file into ~/share too so the same server link serves it.

## Batch: several photos in ONE message
Fire vision_analyze in parallel (one per photo) + ONE `date` call, then a single patch appending all entries before the marker. Do not serialize.

## Pitfall: duplicate photos / repeated slides
If a photo looks like an earlier slide (same title + same page number), verify with vision_analyze ("apakah identik dengan slide N?") BEFORE appending. If identical → skip, do NOT add an empty entry; tell the user it's a duplicate and the file is unchanged. (2026-08-09: user re-sent slide 18 "Segmenting" — vision confirmed identical, entry skipped.)

## Convention: preserve typos from the source slide
Transcribe typos VERBATIM and annotate: *(typo "transportatio" sesuai teks asli slide)*. Seen on teaching decks: "transportatio apps", "Questions that need to be answer", "Cari produk yang diingkan". Faithful transcription beats silent correction for business/teaching material. If the typo makes meaning ambiguous (e.g. diingkan vs diinginkan), flag it in the Telegram summary.

## Batching: several photos in one message
When N photos arrive together: fire N vision_analyze calls + ONE `date` call in parallel, then append ALL entries in a single patch (one marker replacement). Do not serialize photo-by-photo.

## Pitfall: vision_analyze truncates on dense slides
**Combine sources**: when vision_analyze output gets cut off on dense slides, merge the platform-provided initial image description (often complete, e.g. all 20 chart bars or full card text) with the vision output — both were needed for SCQA cards & USP slide (entri 7 & 8).
On text-heavy slides (long example paragraphs, multi-card layouts like SCQA), vision_analyze output can be cut off mid-card. The platform's initial image description (the "Here's what I can see: ..." text attached to the incoming photo) often carries the FULL text — merge both sources before writing the entry. Verify each card/example is complete; if a section is still missing/truncated, add a note in the entry (`*terpotong di foto*`) instead of silently dropping content.

## Steps
1. Confirm/create the single .md target file (check memory for the active file path; else ask where to put it).
2. On create, write: title (`# ...`), short intro, and bottom marker comment:
   `<!-- ENTRI FOTO DI-TAMBAHKAN DI BAWAH GARIS INI -->`
3. Per photo:
   - Read image (vision) and extract ALL slide content: slide number, title, subtitle, section headers, bullets, exact quotes, closing banner.
   - Real timestamp: `date +"%Y-%m-%d %H:%M"` — NEVER compute dates mentally.
   - Insert entry BEFORE the marker via patch: replace marker line with `entry + marker`. Entry header: `## Entri N — YYYY-MM-DD HH:MM`.
   - Structure: Slide number + title, Subtitle, key quotes as blockquote, numbered/bulleted lists per section, closing quote as "Pesan Penutup".
4. After each append, reply: short summary + FULL file via `MEDIA:/abs/path/to/file.md` (user reads the complete .md on mobile — full content, not summary).
5. Keep appending; never overwrite previous entries.

## Entry template
`templates/entry_template.md` — copy and fill per slide.

## Pitfalls
- Don't auto-create spreadsheets for photo→doc requests (did this once; user corrected: "kamu salah pengertian").
- Don't drop the bottom marker comment — it anchors insertion so entries stay in order.
- Timestamps from `date` command only, never mental math.
- Preserve exact numbers/quotes from slides (regulation/article numbers, legal citations) — these are the substance of the doc.
