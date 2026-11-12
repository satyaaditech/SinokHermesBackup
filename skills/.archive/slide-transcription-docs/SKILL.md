---
name: slide-transcription-docs
description: Use when transcribing slide photos to Google Docs.
---

# Slide Transcription to Google Docs

Use this workflow when the user sends photos of presentation slides, conference displays, or sermon screens and requests verbatim transcription into Google Docs with original visual evidence.

## Standing Rules & User Constraints
1. **Strict Verbatim Accuracy (100% Apa Adanya):** Never summarize, rephrase, omit, or embellish text from the slides. Legal terms, regulation numbers (Permenkum, UU, PP), and scriptural citations must match the physical screen exactly.
2. **Public Reader Access:** Always set document and image permissions to `type: 'anyone', role: 'reader'` so the document is shareable and images render properly.
3. **Inline Image Attachment:** Embed each photo directly into the document (`insertInlineImage`) immediately before or after its transcription for instant visual verification.
4. **Native Table Formatting:** Format all tabular, sequential, comparative, or matrix data using Google Docs Native Tables (`insertTable`), never raw markdown tables or bulleted approximations.
5. **Topic Separation:** When the user indicates a new presentation or sermon ("judul baru", "materi baru"), create a fresh Google Doc rather than appending to the previous presentation.

## Prerequisites & Authentication
- Google OAuth token: `~/.hermes/google_token.json`
- Python client libraries: `google-api-python-client`, `google-auth`

## Step-by-Step Procedure

### 1. Document Initialization (On New Topic)
When a new topic starts, create a clean Google Doc and set public permissions:
```python
import json, os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open(os.path.expanduser("~/.hermes/google_token.json")) as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data["token"],
    refresh_token=token_data.get("refresh_token"),
    token_uri=token_data["token_uri"],
    client_id=token_data["client_id"],
    client_secret=token_data["client_secret"],
    scopes=token_data["scopes"]
)

docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

doc = docs_service.documents().create(body={'title': doc_title}).execute()
doc_id = doc['documentId']
drive_service.permissions().create(fileId=doc_id, body={'type': 'anyone', 'role': 'reader'}).execute()
```

### 2. Uploading & Embedding Slide Images
Upload the cached local image to Drive, make it public, and insert as an inline image:
```python
from googleapiclient.http import MediaFileUpload

# Upload to Drive
media = MediaFileUpload(img_path, mimetype='image/jpeg')
file = drive_service.files().create(
    body={'name': f"Slide_{os.path.basename(img_path)}", 'mimeType': 'image/jpeg'},
    media_body=media,
    fields='id'
).execute()
file_id = file['id']

# Grant public read access to the image file
drive_service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
img_uri = f"https://drive.google.com/uc?export=download&id={file_id}"

# Insert inline image into Doc at current end index
d = docs_service.documents().get(documentId=doc_id).execute()
pos = d['body']['content'][-1]['endIndex'] - 1

docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': [{
    'insertInlineImage': {
        'location': {'index': pos},
        'uri': img_uri,
        'objectSize': {
            'width': {'magnitude': 450, 'unit': 'PT'},
            'height': {'magnitude': 250, 'unit': 'PT'}
        }
    }
}]}).execute()
```

### 3. Native Table Insertion
To prevent index drift when inserting text into table cells:
1. Insert empty table structure at `pos`.
2. Re-fetch document and locate the newly created table.
3. Collect all cell start indices and sort them **DESCENDING**.
4. Apply text insertions in descending order.

```python
# 1. Insert empty table
docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': [{
    'insertTable': {'rows': len(rows_data), 'columns': len(rows_data[0]), 'location': {'index': pos}}
}]}).execute()

# 2. Re-fetch table and extract cell indices
d = docs_service.documents().get(documentId=doc_id).execute()
target_table = [el['table'] for el in d['body']['content'] if 'table' in el][-1]

cell_insertions = []
for r_idx, row in enumerate(target_table["tableRows"]):
    for c_idx, cell in enumerate(row["tableCells"]):
        text = str(rows_data[r_idx][c_idx])
        start = cell["content"][0]["paragraph"]["elements"][0]["startIndex"]
        cell_insertions.append((start, text))

# 3. Sort descending to preserve indices
cell_insertions.sort(key=lambda x: x[0], reverse=True)
reqs = [{'insertText': {'location': {'index': s}, 'text': t}} for s, t in cell_insertions]
docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': reqs}).execute()
```

## Pitfalls & Defensive Practices
- **Dynamic End Index:** Always recalculate `d['body']['content'][-1]['endIndex'] - 1` right before each batchUpdate — hardcoded or stale offsets cause `IndexOutOfBounds` errors after prior insertions.
- **Drive Permission Propagation:** Wrap the Drive permission call on newly uploaded images in a 3-attempt retry loop with exponential backoff — Docs API refuses `insertInlineImage` if Drive has not yet registered public readability.
- **Granular Execution over Mega-Batches:** Execute insertions slide-by-slide rather than queuing dozens of slides into a single mega-script — network timeouts or quota spikes during large multi-slide calls will leave the document in an unknown half-applied state.
- **Table Cell Paragraph Retention:** When inserting text into table cells, target `cell["content"][0]["paragraph"]["elements"][0]["startIndex"]` directly — creating new paragraphs inside unpopulated cells breaks cell padding and alignment.
