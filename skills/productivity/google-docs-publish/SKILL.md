---
name: google-docs-publish
description: Use when converting markdown to formatted Google Docs.
---

# Google Docs Publish (Markdown → Formatted Doc)

## References
- Direct Python API publishing and link sharing pattern: [references/direct-api-publishing.md](references/direct-api-publishing.md)
- Native paragraph formatting, images, and page breaks: [references/native-batch-formatting.md](references/native-batch-formatting.md)
- Native table formatting & zebra striping: [references/native-table-formatting.md](references/native-table-formatting.md)
- Targeted in-place document editing & API rate limiting: [references/targeted-in-place-editing.md](references/targeted-in-place-editing.md)
- Google Slides API disabled workaround (pptx upload conversion): [references/slides-api-disabled-workaround.md](references/slides-api-disabled-workaround.md)

User (Pak Satya) requires Google Doc output as **native docs formatting** — real headings, bold, italic — with **ZERO markdown symbols** (`*`, `**`, `###`) visible. Docs go into a specific Drive folder (e.g. 'Materi Olahrasa' `1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U`, 'Pendapatan Sampingan' `1SQaBdLVan5SuLfyHgV9Nr1CGbFFIPd3P`) and are shared "anyone with link (writer)" so he can edit from mobile.

## When to use
- "Buat yang di Google Doc juga ya, supaya mudah aku edit" — any content (renungan, khotbah, ulasan, manuskrip) that must land in Google Docs.
- Any markdown → Google Doc conversion with clean formatting.

## Credentials
- Token: `~/.hermes/google_token.json` (OAuth, already set up; scopes include drive + documents).
- `googleapiclient` available in the Hermes venv (`python -c "import googleapiclient"`).

## Steps
1. Keep the canonical content as a markdown file under `~/share/...` first.
2. Run the reusable converter:
   ```bash
   python ~/.hermes/skills/productivity/google-docs-publish/scripts/md_to_doc.py \
     --source /path/to/file.md \
     --title "Judul Dokumen" \
     --folder <DRIVE_FOLDER_ID> \
     [--doc-id <ID>]   # reuse/overwrite an existing doc (empties content before writing)
   ```
3. Script maps: `#`→Heading 1, `##`→Heading 2, `###`→Heading 3, `>`→indented italic paragraph, markdown tables→plain lines joined with ` · `, `- ` bullets→`• ` lines, inline `**bold**`/`*italic*`→textStyle runs. All markdown symbols stripped.
4. **Verify after upload**: re-fetch the doc, assert zero occurrences of `**`, `##`, `> `, `---` in the final text, and check heading styles landed. A doc that "uploaded successfully" but contains literal `**` fails the user's requirement.

## Pitfalls (hard-won, Docs API)
- **Drive-created docs have NO paragraph at index 0.** `drive.files().create` with `mimeType=application/vnd.google-apps.document` yields body = `[sectionBreak(endIndex 1), paragraph(1–2, "\n")]`. `insertText` at index 0 FAILS: "The insertion index must be inside the bounds of an existing paragraph." FIX: `documents().get()` first, find the first `paragraph` element's `startIndex` (=1), insert there, and offset **every** style/text range by that base.
- **`updateParagraphStyle` / `updateTextStyle` require explicit `fields`** (e.g. `"namedStyleType,indentStart"`, `"bold,italic"`) or the batch fails: "At least one field must be listed in 'fields'."
- A failed `batchUpdate` is validated first and applies nothing — the doc stays empty, so re-running is safe. A successful run is all-or-nothing per batch call.
- Chunk long request arrays (~120 requests per `batchUpdate` call) to stay under size limits.
- Do NOT use `gws docs append --text` for multi-line content — it breaks on newlines/quotes (see bundled google-workspace skill workaround docs).

## Sharing
- After writing: `drive.permissions().create(fileId, body={"type":"anyone","role":"writer"})` → "anyone with link (writer)" so user + peers can edit without asking.

## Related
- Bundled `google-workspace` skill covers the wider GWS CLI surface; this skill carries the session-hardened markdown→doc pipeline and its API pitfalls.
