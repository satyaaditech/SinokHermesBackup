# Native Formatting, Images, and Page Breaks in Google Docs

When converting Markdown or HTML to a Google Doc, standard HTML-to-Doc conversion via the Drive API often yields poor aesthetics (margins, line-heights, background shading, and page breaks are poorly translated). To construct a professional, magazine-quality Google Doc layout, write text and styles natively using the Google Docs batchUpdate API.

### Layout and Legibility Guidelines
When formatting Google Docs, prioritize high readability by using:
1. **Typography**: Center titles in Georgia (~22pt bold), category headers in Georgia (~12-14pt bold), and paragraph text in Calibri or Arial (~10.5pt normal).
2. **Color Accents**: Use professional muted colors (e.g. Teal rgbColor: `0.0, 0.45, 0.45` or Dark Muted Grey) for headers to break monotony.
3. **Spacing**: Set paragraph spacing (`spaceAbove`, `spaceBelow` in `paragraphStyle` request body) and a line spacing of 1.15 to prevent wall-of-text layouts.
4. **Bold Prefixes**: Bold the number or bullet prefixes (e.g., `1.`, `2.`, etc.) to enhance directory readability.

## Common Pitfalls & Google Docs API Traps
- **Zero Markdown Syntax Artifacts**: Pak Satya strictly expects ZERO raw markdown markers (`#`, `##`, `###`, `---`, `>`, `**`, `*`, `|---|`) visible in the final Google Doc. Stripping markers and applying native formatting is mandatory:
  1. Parse `# / ## / ###` into clean heading strings and apply `namedStyleType: 'HEADING_1' / 'HEADING_2' / 'HEADING_3'` with Navy `#0D3B66` bold typography.
  2. Parse `>` into clean quote strings and apply paragraph style `indentStart: {magnitude: 36, unit: 'PT'}`, `indentEnd: {magnitude: 18, unit: 'PT'}`, italic body text, and bold source attribution.
  3. Parse inline tokens `re.split(r'(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*)')` to strip asterisks while recording `(startIndex, endIndex)` for `bold: True` / `italic: True` text runs.
- **Heading Styles**: In `updateParagraphStyle`, use `namedStyleType: 'HEADING_1'` (or `HEADING_2`, `TITLE`, `SUBTITLE`, `NORMAL_TEXT`), with `fields: 'namedStyleType,spaceAbove,spaceBelow'`. NEVER use `headingId` — it throws `HttpError 400: Unallowed field: headingId`.
- **Large Document Chunking**: When inserting documents > 20,000 characters, break raw text into chunks of ~20,000 chars, inserting sequentially at the current document end (`cur_end = content[-1]['endIndex'] - 1`), then do a single pass across `doc.get('body').get('content')` to extract ranges for formatting.
- **Batching Style Updates**: Execute style updates in batches of 50 requests with a small sleep (`time.sleep(0.3)`) to prevent transient `429 Rate Limit Exceeded` errors.


A major hurdle with the Google Docs API is that inserting text or structural elements shifts the absolute indices of all elements located after the insertion point. Keeping track of these shifts when updating styles is error-prone.

**The Solution:** Insert blocks (paragraphs, page breaks, images) in **reverse order** (from last to first) at the document's first paragraph index (`base_idx`, usually `1`).
- When a block is inserted at `base_idx`, it pushes all previously inserted blocks down.
- Because it is placed at `base_idx`, the text of the block always occupies the range `[base_idx, base_idx + len(inserted_text)]`.
- Style requests (paragraph and text formatting) for the block can be applied immediately to the range `[base_idx, base_idx + len(inserted_text)]`.
- All blocks inserted in previous steps are shifted to the right, and the Docs API automatically shifts their styling ranges accordingly.

### Order of Requests in reversing loop:
For each block `(type, text, styles)` in `reversed(blocks)`:
1. **Insert Text/Element** at `base_idx`.
2. **Apply styles** on `[base_idx, base_idx + len(text)]`.
3. If inline styles (bold/italic) exist, apply them relative to `base_idx + offset`.

---

## 2. Code Template for Reverse Batch Insertion

Below is the verified Python pattern to clear a document, parse markdown paragraphs, apply custom typography (Georgia for headings, Calibri for body, justified alignments), and execute chuncked batch updates.

```python
import sys
import re
from googleapiclient.discovery import build

doc_id = "YOUR_DOCUMENT_ID"
docs_service = build("docs", "v1", credentials=creds)

# 1. Clear existing document content
doc = docs_service.documents().get(documentId=doc_id).execute()
end_idx = doc["body"]["content"][-1]["endIndex"]
if end_idx > 2:
    docs_service.documents().batchUpdate(
        documentId=doc_id, 
        body={"requests": [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_idx - 1}}}]}
    ).execute()

# 2. Get base index of empty document
doc = docs_service.documents().get(documentId=doc_id).execute()
base_idx = next((el["startIndex"] for el in doc["body"]["content"] if "startIndex" in el), 1)

requests_list = []

# Iterate backwards
for b_type, content, styles in reversed(blocks):
    if b_type == "page_break":
        requests_list.append({"insertPageBreak": {"location": {"index": base_idx}}})
    elif b_type == "image":
        # Centered inline image with line spacer
        requests_list.append({"insertText": {"text": "\n", "location": {"index": base_idx}}})
        requests_list.append({"insertInlineImage": {"uri": content, "location": {"index": base_idx}}})
        requests_list.append({
            "updateParagraphStyle": {
                "paragraphStyle": {"alignment": "CENTER"},
                "range": {"startIndex": base_idx, "endIndex": base_idx + 1},
                "fields": "alignment"
            }
        })
    else:
        text_to_insert = content + "\n"
        requests_list.append({"insertText": {"text": text_to_insert, "location": {"index": base_idx}}})
        L = len(text_to_insert)
        
        # Style paragraph properties (Named Styles and Spacing)
        ps = {"namedStyleType": "NORMAL_TEXT"}
        ps_fields = ["namedStyleType"]
        
        if b_type == "h1":
            ps.update({"namedStyleType": "HEADING_1", "alignment": "CENTER", "spaceAbove": {"magnitude": 24, "unit": "PT"}})
            ps_fields.extend(["alignment", "spaceAbove"])
        elif b_type == "normal":
            ps.update({"alignment": "JUSTIFIED", "spaceBelow": {"magnitude": 8, "unit": "PT"}})
            ps_fields.extend(["alignment", "spaceBelow"])
            
        requests_list.append({
            "updateParagraphStyle": {
                "paragraphStyle": ps,
                "range": {"startIndex": base_idx, "endIndex": base_idx + L},
                "fields": ",".join(ps_fields)
            }
        })
        
        # Style font properties (Fonts family, size, color)
        ts = {"weightedFontFamily": {"fontFamily": "Georgia" if b_type.startswith("h") else "Calibri"}}
        ts_fields = ["weightedFontFamily"]
        requests_list.append({
            "updateTextStyle": {
                "textStyle": ts,
                "range": {"startIndex": base_idx, "endIndex": base_idx + L},
                "fields": ",".join(ts_fields)
            }
        })

# Execute in chunks to prevent payload bottlenecks (max 120 requests at a time)
CHUNK_SIZE = 120
for idx in range(0, len(requests_list), CHUNK_SIZE):
    docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests_list[idx:idx+CHUNK_SIZE]}).execute()
```

---

## 3. Formatting Images and Page Breaks

*   **Google Drive Direct Image Link**: Google Docs API requires a publicly accessible URI to fetch and embed an image. If the image is hosted on Google Drive:
    1. Share the image file: `anyone with link (reader)`.
    2. Convert the image's `FILE_ID` into the direct raw download path:
       `https://drive.google.com/uc?export=download&id=FILE_ID`
    Do not use base64 URIs as they are often ignored or rejected by the Docs API.
*   **Page Breaks**: An `insertPageBreak` inserts a page break character. In the reverse-injection loop, it shifts all downstream items to the next page cleanly. Avoid double page breaks by strictly filtering separators and layout tags.
