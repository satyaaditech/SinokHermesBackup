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

insert_requests = []
for cell_start, r_idx, c_idx, cell_text in cell_insertions:
    insert_requests.append({
        "insertText": {
            "location": {"index": cell_start},
            "text": cell_text
        }
    })
docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": insert_requests}).execute()
```

---

## 2. Critical Pitfalls & Solutions

### Pitfall 1: Raw HTML `<br>` and Markdown Syntax in Table Cells
**Symptom:** Markdown tables frequently use `<br>` or `<br><br>` for line breaks inside cells. Direct insertion leaves raw `<br><br>` and `:---` strings rendered as ugly plain text in Google Docs.
**Rule:** Always sanitize and tokenize cell text before insertion:
```python
# Convert HTML breaks to real newlines
clean_cell = re.sub(r'<br\s*/?>\s*<br\s*/?>', '\n\n', raw_cell, flags=re.IGNORECASE)
clean_cell = re.sub(r'<br\s*/?>', '\n', clean_cell, flags=re.IGNORECASE)

# Parse inline bold and italic tokens
tokens = re.split(r'(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*)', clean_cell)
clean_parts, spans = [], []
cursor = 0
for tok in tokens:
    if tok.startswith('***') and tok.endswith('***'):
        txt = tok[3:-3]
        clean_parts.append(txt)
        spans.append((cursor, cursor + len(txt), True, True)) # bold, italic
        cursor += len(txt)
    elif tok.startswith('**') and tok.endswith('**'):
        txt = tok[2:-2]
        clean_parts.append(txt)
        spans.append((cursor, cursor + len(txt), True, False)) # bold
        cursor += len(txt)
    elif tok.startswith('*') and tok.endswith('*'):
        txt = tok[1:-1]
        clean_parts.append(txt)
        spans.append((cursor, cursor + len(txt), False, True)) # italic
        cursor += len(txt)
    else:
        clean_parts.append(tok)
        spans.append((cursor, cursor + len(tok), False, False))
        cursor += len(tok)
```

---

## 3. High-Performance Cluster-Batch Architecture

When publishing comprehensive 20+ page documents with 15–25 mixed tables and paragraphs, running single API calls per paragraph will hit HTTP 429 quota limits or timeouts.

**Pattern:**
1. Group consecutive paragraphs, headings, and quotes between tables into `text_cluster` blocks.
2. Insert each `text_cluster` in a single `insertText` call, and batch paragraph/character styling in sub-batches of 50 requests.
3. On table boundaries, perform the dedicated `insertTable` + cell styling pipeline.
4. This reduces API round-trips from >200 down to ~35, accelerating rendering by 10x and eliminating timeouts.

---

## 4. Executive Table Styling Specs

| Element | Background Color | Text Color | Font & Size | Padding |
| :--- | :--- | :--- | :--- | :--- |
| **Header Row** | Royal Navy `#0D3B66` | Pure White `#FFFFFF` | Georgia 10pt Bold | Top/Bottom 6pt, L/R 8pt |
| **Left Column (Context / Lama)** | Soft Gray `#F8FAFC` | Dark Slate `#2D3748` | Georgia 9.5pt Regular | Top/Bottom 6pt, L/R 8pt |
| **Right Column (Pembaruan / SGS)** | Pure White `#FFFFFF` | Dark Slate `#2D3748` | Georgia 9.5pt (Navy Bold subheadings) | Top/Bottom 6pt, L/R 8pt |
