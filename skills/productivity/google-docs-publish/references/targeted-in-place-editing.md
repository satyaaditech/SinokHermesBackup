# Targeted In-Place Document Refinement & Google Docs API Quota Safety

## 1. Targeted In-Place Editing (Preserving User Edits)
When the user asks to refine, format, or replace specific sections in an existing Google Doc that they have already manually modified (e.g. added manual page breaks, adjusted margins, rearranged sections):
- **NEVER wipe or overwrite the whole document** using a full delete range (`deleteContentRange(1, total_len)`).
- Query the live document structure first via `docs.documents().get(documentId=DOC_ID).execute()`.
- Scan structural elements to locate the exact `startIndex` and `endIndex` of the targeted section (e.g., between the section heading and the next chapter heading).
- Execute `deleteContentRange` only on that specific range.
- Insert and style the new elements (tables, headings, paragraphs) in-place at the exact start position.
- This guarantees all user page breaks, custom formatting, and surrounding chapters remain 100% untouched.

---

## 2. Google Docs API Write Quota & Rate Limit Pacing (HTTP 429)
- Google Docs API enforces a hard quota of **60 write operations per minute per user**.
- Multi-table documents (e.g., 12 detailed comparison tables) will easily exceed this limit if every table insertion, cell population, and text styling is executed in separate round-trip API calls (70+ calls in < 15 seconds).
- **Required Patterns**:
  1. **Batching**: Group related requests (e.g. title insertion + text style + paragraph style) into a single `batchUpdate` payload.
  2. **Pacing**: Insert `time.sleep(1.5)` to `time.sleep(2.0)` between consecutive `batchUpdate` requests during large multi-element generation tasks.
  3. **Table Cell Insertion Stability**: When populating a multi-cell table, insert text into cells in descending order of cell start index, or re-fetch table cell bounds after each table insertion to prevent index drift.
