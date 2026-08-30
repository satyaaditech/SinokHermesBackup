# Google Docs Operations for Photo Transcription Logs

When the user asks to transcribe/recap photos into a **Google Doc** (instead of a local `.md` file) and update it progressively:

## 1. Creation and Sharing Workflow

Always create the Google Doc first and share it as public-writable (or as requested) so the user has immediate access.

```python
import os, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")

with open(TOKEN_PATH) as f:
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

# Create Doc
title = "Rekap Presentasi - YYYY-MM-DD HH:MM"
doc = docs_service.documents().create(body={'title': title}).execute()
doc_id = doc['documentId']

# Share as "Anyone with link can edit"
permission = {
    'role': 'writer',
    'type': 'anyone'
}
drive_service.permissions().create(fileId=doc_id, body=permission).execute()

web_url = f"https://docs.google.com/document/d/{doc_id}/edit"
print(f"Doc URL: {web_url}")
```

## 2. Formatting Guidelines: Avoid Raw Markdown Symbols (Zero Markdown in Google Docs)

**CRITICAL RULE:** Do NOT write raw markdown characters (like `**`, `*`, `###`, `---`, `_`) directly into the text for Google Docs. Google Docs does not automatically render markdown, leaving raw syntax markers visible, which is cluttered and unprofessional.

Instead:
- Format the content using clean plain text spacing, capitalization, and native styles.
- Use Google Docs API `batchUpdate` requests to style the text programmatically:
  * Paragraph named styles (`HEADING_1`, `TITLE`, `SUBTITLE`, `NORMAL_TEXT`).
  * Text styles (`bold`, `fontSize`, `foregroundColor` with RGB colors) targeting precise character ranges.
- When sending a batch of insertions and style updates in the same `batchUpdate` call, track the index shifts precisely. As you append blocks sequentially, calculate the ranges (`start = current_index`, `end = current_index + len(text)`) and increment `current_index = end` for the next block, since the API processes the requests in order and shifts subsequent indices accordingly.and standard indentations.
- Programmatically apply styles (such as bold, italics, or paragraph heading named styles like `HEADING_1`) using the Google Docs `batchUpdate` API.

## 3. Verified Script Pattern to Append and Format Programmatically

When appending multiple slides progressively, retrieve the current document's final index first. To insert text and format it in one batch without index shifting errors, use the following pattern:

```python
import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")
DOC_ID = "YOUR_DOC_ID"

with open(TOKEN_PATH) as f:
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

# Fetch latest document boundaries
doc = docs_service.documents().get(documentId=DOC_ID).execute()
content_list = doc.get('body', {}).get('content', [])
end_index = content_list[-1]['endIndex'] - 1 if content_list else 1

# Define styled blocks to insert
blocks = [
    {"text": "SLIDE X: JUDUL SLIDE\n", "style": "HEADING_1"},
    {"text": "Isi slaid normal penjelasan detail.\n\n", "style": "NORMAL"},
    {"text": "• Poin Pertama: Informasi penting.\n", "style": "BULLET"},
]

requests = []
current_index = end_index

for b in blocks:
    text_len = len(b['text'])
    start = current_index
    end = current_index + text_len
    
    # 1. Insert text block
    requests.append({
        'insertText': {
            'location': {'index': current_index},
            'text': b['text']
        }
    })
    
    # 2. Style Paragraph
    p_style = {'namedStyleType': 'HEADING_1' if b['style'] == 'HEADING_1' else 'NORMAL_TEXT'}
    requests.append({
        'updateParagraphStyle': {
            'range': {'startIndex': start, 'endIndex': end},
            'paragraphStyle': p_style,
            'fields': 'namedStyleType'
        }
    })
    
    # 3. Style Text (Bold, Color, etc.)
    t_style = {}
    if b['style'] == 'HEADING_1':
        t_style = {
            'bold': True, 
            'fontSize': {'magnitude': 13, 'unit': 'PT'}, 
            'foregroundColor': {'color': {'rgbColor': {'blue': 0.2, 'green': 0.1, 'red': 0.6}}}
        }
    elif b['style'] == 'ITALIC':
        t_style = {'italic': True, 'fontSize': {'magnitude': 10, 'unit': 'PT'}}
        
    if t_style:
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'textStyle': t_style,
                'fields': '*'
            }
        })
        
    # Increment current_index to the new end boundary
    current_index = end

docs_service.documents().batchUpdate(
    documentId=DOC_ID,
    body={'requests': requests}
).execute()
```hUpdate` API:

### Programmatic Formatting Example
Use the following Python snippet to insert clean text blocks and apply styling (such as headings and bold text) via API requests:

```python
# Ambil end index dokumen
doc = docs_service.documents().get(documentId=doc_id).execute()
content_list = doc.get('body', {}).get('content', [])
end_index = content_list[-1]['endIndex'] - 1 if content_list else 1

# Definisikan blok teks beserta tipenya
blocks = [
    {"text": "SLIDE N: JUDUL SLIDE\n", "style": "HEADING_1"},
    {"text": "Deskripsi atau gambaran umum mengenai slide ini.\n\n", "style": "NORMAL"},
    {"text": "• Poin Utama 1: Penjelasan rinci.\n", "style": "BULLET"},
    {"text": "• Poin Utama 2: Penjelasan rinci.\n", "style": "BULLET"},
    {"text": "• Kesimpulan Penting/Hasil Bersih: Rp 10.000.000\n\n", "style": "BULLET_BOLD"}
]

requests = []
current_index = end_index

for b in blocks:
    text_len = len(b['text'])
    start = current_index
    end = current_index + text_len
    
    # 1. Masukkan teks ke dalam dokumen
    requests.append({
        'insertText': {
            'location': {'index': current_index},
            'text': b['text']
        }
    })
    
    # 2. Atur gaya paragraf (Heading vs Normal)
    p_style = {}
    if b['style'] == 'HEADING_1':
        p_style = {'namedStyleType': 'HEADING_1'}
    else:
        p_style = {'namedStyleType': 'NORMAL_TEXT'}
        
    requests.append({
        'updateParagraphStyle': {
            'range': {'startIndex': start, 'endIndex': end},
            'paragraphStyle': p_style,
            'fields': 'namedStyleType'
        }
    })
    
    # 3. Atur gaya teks (Tebal, Ukuran Font, dsb)
    t_style = {}
    if b['style'] == 'HEADING_1':
        t_style = {
            'bold': True, 
            'fontSize': {'magnitude': 13, 'unit': 'PT'}, 
            'foregroundColor': {'color': {'rgbColor': {'blue': 0.2, 'green': 0.1, 'red': 0.6}}}
        }
    elif b['style'] == 'BULLET_BOLD':
        t_style = {'bold': True}
        
    if t_style:
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'textStyle': t_style,
                'fields': '*'
            }
        })
        
    current_index = end

# Eksekusi batch update
docs_service.documents().batchUpdate(
    documentId=doc_id,
    body={'requests': requests}
).execute()
```
