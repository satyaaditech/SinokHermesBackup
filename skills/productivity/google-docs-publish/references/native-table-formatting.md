# Native Table Formatting in Google Docs API

When publishing executive reports, comparative studies, or structured data (such as paradigm shift tables or run-sheets) to Google Docs, plain ASCII box-drawing tables (`┌─ │ └─`) or markdown tables converted into bullet points look cluttered and unpolished. Converting them to **Native Google Docs Tables** (`insertTable`) produces executive-quality, publication-grade results.

---

## 1. Table Architecture & Insertion Pipeline

Inserting tables in Google Docs API requires a 3-step sequence:

### Step 1: Insert Empty Table Structure
```python
insert_table_req = {
    "insertTable": {
        "rows": num_rows,
        "columns": num_cols,
        "location": {"index": insert_pos}
    }
}
docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [insert_table_req]}).execute()
```

### Step 2: Query Cell Indices & Populate Descending
When Google Docs creates a table, each cell is initialized with an empty paragraph. To prevent index shifting when inserting text into multiple cells:
1. Re-fetch the document via `docs.documents().get(documentId=DOC_ID).execute()`.
2. Locate the table element at or near `insert_pos`.
3. Collect each cell's start index: `cell["content"][0]["paragraph"]["elements"][0]["startIndex"]`.
4. **Sort cell insertions DESCENDING by `startIndex`** so earlier cells' indices remain completely stable while filling text.

```python
cell_insertions = []
for r_idx, row in enumerate(target_table["tableRows"]):
    for c_idx, cell in enumerate(row["tableCells"]):
        cell_text = table_data[r_idx][c_idx]
        cell_start = cell["content"][0]["paragraph"]["elements"][0]["startIndex"]
        cell_insertions.append((cell_start, r_idx, c_idx, cell_text))

# Sort descending to protect earlier indices
cell_insertions.sort(key=lambda x: x[0], reverse=True)

cell_reqs = [{"insertText": {"location": {"index": pos}, "text": text}} for pos, _, _, text in cell_insertions]
docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": cell_reqs}).execute()
```

### Step 3: Apply Executive Cell & Typography Styling
Apply professional typography and colors (`updateTableCellStyle` & `updateTextStyle`):

### A. Header Row (Row 0)
* **Background**: Deep Navy (`#0D3B66`) or Light Soft Tint (`#E8F0FE`).
* **Typography**: Georgia 10pt/10.5pt, Bold, Deep Navy (`#0D3B66`), Center/Left aligned.
* **Padding**: 8pt top/bottom, 8pt left/right.

### B. Data Rows (Rows 1..N)
* **Background**: Clean White (`#FFFFFF`) or Subtle Zebra (`#F8FAFC`).
* **Typography**: Georgia 9.5pt/10pt Regular, Charcoal Body (`#2D3748`).
* **Kutipan Verbatim**: Georgia 9.5pt Bold Italic, Deep Indigo (`#1B365D`).
* **Sumber Referensi**: Georgia 9.5pt Bold Only, Deep Teal (`#0E4A6F`).

---

## 2. Text Sanitization & Visual Hygiene in Table Cells
* **Avoid Math-Mode LaTeX**: Never use LaTeX math symbols like `$\\rightarrow$` inside table cell text. In Docs API or regex markdown converters, the backslash or dollar sign can be misparsed or broken (e.g. into `ightarrow$`), causing row breaks or unrendered artifacts. Always replace with native Unicode arrows (`→`).
* **Replace HTML `<br>` with Native Newlines**: Clean any `<br>` or `<br/>` into actual `\n` or `\n\n` before injecting into table cells.
* **Sanitize Markdown Symbols & Trailing Pipes**: Strip raw markdown decorators (`*`, `**`, `_`) before inserting text runs and apply styling directly via `updateTextStyle`, and ensure no trailing table pipes `|` remain inside cell string buffers.

---

## 3. Google Docs API Error Resilience (Transient 500 / 429 / 503)
When batching hundreds of style operations or multiple table insertions, Google Docs API can occasionally return transient `500 Internal error encountered` or `429 Resource exhausted`.
Always wrap batch updates in an exponential backoff retry loop:

```python
def execute_with_retry(requests_list, max_retries=6):
    if not requests_list:
        return
    for attempt in range(max_retries):
        try:
            return service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests_list}).execute()
        except Exception as e:
            err = str(e)
            if any(code in err for code in ["429", "500", "503", "Internal error", "Quota exceeded"]):
                wait_time = (attempt + 1) * 5
                time.sleep(wait_time)
            else:
                raise e
    raise RuntimeError("Max retries exceeded for Docs API batchUpdate.")
```
