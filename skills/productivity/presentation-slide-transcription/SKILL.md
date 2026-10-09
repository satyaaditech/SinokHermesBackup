---
name: presentation-slide-transcription
description: Use when transcribing presentation slides to Google Docs.
---

# Presentation Slide Transcription to Google Docs

Use this skill when the user sends sequential photographs or screenshots of presentation slides (seminars, conferences, webinars, training materials) and requests verbatim transcription into Google Docs with embedded images and native tables.

## Core Directives & Quality Gates

1. **Strict Verbatim (Apa Adanya 100%)**:
   - Transcribe every word, title, subtitle, bullet point, regulation number, article reference, and note exactly as shown.
   - Do NOT summarize, paraphrase, add external commentary, or omit details.
   - If text is cut off or partially obscured, transcribe what is visible verbatim and indicate `[terpotong]` without inventing words.

2. **Native Google Docs Tables**:
   - Never use ASCII box-drawing or raw markdown tables in Google Docs.
   - Convert comparison columns, multi-step workflows, matrices, and checklists into real Google Docs tables (`insertTable`).

3. **Inline Image Attachment**:
   - Upload each original slide image to Google Drive, set sharing to public reader (`anyone: reader`), and embed it inline immediately before or after the transcript using `insertInlineImage`.
   - Maintain visual context directly in the document so the user can verify text against the source image.

4. **Multi-Topic / New Presentation Handling**:
   - When the user sends a signal like *"judul baru lagi ya nox"* or *"materi baru, judul yang baru"*, do NOT append to the previous document.
   - Immediately create a brand new Google Doc with a fitting title, set public reader permissions, and notify the user with the new link.

5. **Document Access**:
   - Always ensure documents are set to Public View (`type: 'anyone', role: 'reader'`) so the user can view and share them from mobile without login walls.

---

## Step-by-Step Procedure

### Step 1: Multimodal Extraction (`vision_analyze`)
For each slide image:
1. Examine the full slide layout, headers, body columns, badges, slide numbering (e.g. `Slide X of Y`), and footers.
2. Extract all textual content verbatim.
3. Identify logical table structures (e.g. Stage vs Description vs Legal Basis, or Step vs Component vs Action).

### Step 2: Google Drive Image Upload & Public Link Generation
Before inserting into Google Docs, upload the image file to Google Drive and set permission:
```python
file_metadata = {
    'name': f"Slide_{os.path.basename(img_path)}",
    'mimeType': 'image/jpeg'
}
media = MediaFileUpload(img_path, mimetype='image/jpeg')
file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
file_id = file.get('id')
drive_service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
img_direct_link = f"https://drive.google.com/uc?export=download&id={file_id}"
```

### Step 3: Append Content at Document Tail (`endIndex - 1`)
Always query the latest document state to determine insertion position:
```python
def append_text(docs_service, doc_id, text):
    d = docs_service.documents().get(documentId=doc_id).execute()
    pos = d.get('body').get('content')[-1].get('endIndex') - 1
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': [{
        'insertText': {'location': {'index': pos}, 'text': text}
    }]}).execute()
```

### Step 4: Insert Inline Image
```python
def append_image(docs_service, doc_id, image_uri, width_pt=450, height_pt=250):
    d = docs_service.documents().get(documentId=doc_id).execute()
    pos = d.get('body').get('content')[-1].get('endIndex') - 1
    req = {
        'insertInlineImage': {
            'location': {'index': pos},
            'uri': image_uri,
            'objectSize': {
                'width': {'magnitude': width_pt, 'unit': 'PT'},
                'height': {'magnitude': height_pt, 'unit': 'PT'}
            }
        }
    }
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': [req]}).execute()
    append_text(docs_service, doc_id, "\n\n")
```

### Step 5: Insert Native Table (Descending StartIndex Sorting)
**Crucial Rule**: When populating cells of a freshly created table, sort all cell insertions in **descending order by `startIndex`**. Inserting from the bottom-up prevents earlier cell indices from shifting.

```python
def append_table(docs_service, doc_id, rows_data):
    num_rows = len(rows_data)
    num_cols = len(rows_data[0])
    
    d = docs_service.documents().get(documentId=doc_id).execute()
    pos = d.get('body').get('content')[-1].get('endIndex') - 1
    
    # 1. Insert empty table
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': [{
        'insertTable': {'rows': num_rows, 'columns': num_cols, 'location': {'index': pos}}
    }]}).execute()
    
    # 2. Re-fetch table cells
    d = docs_service.documents().get(documentId=doc_id).execute()
    target_table = [el['table'] for el in d.get('body').get('content') if 'table' in el][-1]
    
    # 3. Collect cell start indices
    cell_insertions = []
    for r_idx, row in enumerate(target_table["tableRows"]):
        for c_idx, cell in enumerate(row["tableCells"]):
            cell_text = str(rows_data[r_idx][c_idx])
            cell_start = cell["content"][0]["paragraph"]["elements"][0]["startIndex"]
            cell_insertions.append((cell_start, cell_text))
            
    # 4. Sort descending to prevent index drift
    cell_insertions.sort(key=lambda x: x[0], reverse=True)
    cell_reqs = [{"insertText": {"location": {"index": cs}, "text": ct}} for cs, ct in cell_insertions]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': cell_reqs}).execute()
```

---

## Pitfalls & Recovery Rules

- **Orphan Recovery / Timeout Interruption**:
  - Long batch updates or large file uploads may occasionally experience network interruption or script timeout (`Orphan recovery`).
  - **Rule**: NEVER blindly re-run the entire append script upon recovery. Run a lightweight check script first to read existing headers (`if 'FOTO' in line: print(line)`).
  - Only resume appending from the first missing slide to avoid duplicate entries in the document.

- **Index Drift during Table Cell Population**:
  - Inserting text into table cells in forward order alters the indices of subsequent cells, causing text to land in wrong cells or throw out-of-bounds index errors.
  - **Rule**: Always sort cell insertion requests in descending order by `startIndex`.

- **Drive Permission Propagation**:
  - When uploading an image to Google Drive, permission propagation to public reader (`anyone: reader`) can occasionally take 1–2 seconds.
  - **Rule**: Wrap `drive_service.permissions().create()` in a simple retry block (up to 3 attempts with 1s sleep) before constructing the `insertInlineImage` request.
