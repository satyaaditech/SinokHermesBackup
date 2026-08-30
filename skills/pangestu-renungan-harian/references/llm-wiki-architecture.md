# Andrej Karpathy LLM Wiki Architecture for Buku Pangestu

This reference document defines the structural guidelines, file operations, and ingest workflows for the Buku Pangestu LLM Wiki vault located at `/home/satyaaditech/shorts_factory/obsidian/BukuPangestu/`.

---

## 1. Vault Directory Structure

The vault follows a 3-layer architecture (Raw Sources, Wiki Markdown, and System Rules schema):

*   **`books/` (Immutable Source Texts)**:
    *   Holds the unmodified, full-length, and authoritative books of the Paguyuban Ngesti Tunggal (e.g., `ssj.md`, `brsr.md`, `skh.md`, `tkl.md`).
    *   This is the *immutable source of truth*. The AI must NEVER modify files in this directory. They are read-only references for quoting and cross-referencing.
*   **`wiki/` (Managed Knowledge Base)**:
    *   Contains structured, topic-focused concept files (e.g., `Sabar.md`, `Rila.md`, `Candrajiwa.md`, `Dalan Rahayu.md`).
    *   All concept files must be written in structured Indonesian, keeping core Javanese terms and sentences in quotes, and heavily cross-linked using `[[wikilinks]]`.
    *   Contains the catalog `wiki/index.md` and the audit trail `wiki/log.md`.
*   **`wiki/renungan/` (Ingested Reflections Subfolder)**:
    *   Holds past daily reflections (renungans) in Javanese (`jv`), Indonesian (`id`), and English (`en`), clean-formatted with YAML frontmatter.
*   **`raw/` (Staging Ground)**:
    *   Where the user places web clippings, pdfs, transcripts, or new raw text files to be ingested by the AI.
*   **`archive/` (Processed Raw Storage)**:
    *   Once a file from `raw/` is successfully processed and ingested into the wiki, it must be moved here. This prevents the AI from double-processing the same document in future turns while preserving the original raw backup.
*   **`inbox/` (Temporary Scrapbook)**:
    *   Where fast-entry messages, quick notes, and temporary thoughts are kept before being triage-categorized.

---

## 2. The Ingest Workflow (Step-by-Step)

When the user requests an ingest of a raw file:
1.  **Read and Parse**: Read the raw file using appropriate encoding (typically `utf-8` or `latin-1` if `utf-8` fails).
2.  **Concept Extraction & Synthesis**:
    *   Identify spiritual concepts, definitions, prohibitions, or guidelines.
    *   If a concept exists, prepare to append a section titled `### Rujukan saking <Source Name / Book>` with verbatim blockquotes and brief analytical context.
    *   If the concept is new, design a fresh page with metadata frontmatter (title, tags, reference list).
3.  **Cross-linking & Auto-Wiki-linking**:
    *   When writing or updating wiki pages, scan for core concepts (e.g., *sabar, rila/rela, narima, jujur, budi luhur, suksma sejati, eling, pracaya, mituhu, candrajiwa, dalan rahayu, paliwara*) and automatically wrap them with `[[wikilinks]]`.
    *   Ensure any replacement does not break existing formatting or double-wrap existing links.
4.  **Index & Log Bookkeeping**:
    *   Update `wiki/index.md` to classify the new page(s) under its matching category (Tri Sila, Panca Sila, Kejiwaan, lsp.).
    *   Append `wiki/log.md` with: `## [YYYY-MM-DD] Ingest | Description`.
5.  **Clean up**: Move the processed file from `raw/` to `archive/` and delete any temporary macOS metadata (`._*` files).

---

## 3. Daily Renungan Ingest (Special Case)

When ingesting daily reflections from `~/share/renungan/`:
*   Identify language from filename (`-ind-` -> `id`, `-eng-` -> `en`, else -> `jv`).
*   Extract date from filename (e.g. `YYYY-MM-DD`) or parse it from the top lines of the file.
*   Extract clean title by ignoring days of the week, headings like "RENUNGAN PENYISWAAN", etc.
*   Standardize the frontmatter with YAML properties (`title`, `date`, `tags`, `language`).
*   Write output to `wiki/renungan/` under the original basename.
*   Update `wiki/Daftar Renungan.md` as a chronological log, grouping by month and date, with flag icons (🇮🇩 / JV / 🇬🇧).
