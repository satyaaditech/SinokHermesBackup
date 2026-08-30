# Direct Google Docs & Drive API Publishing in Python

When you need to publish content directly to Google Docs and make it accessible immediately via a shareable link, use this Python pattern.

## Prerequisites
- Library: `google-api-python-client` (imported in Python).
- Credentials: Token at `~/.hermes/google_token.json`.

## Code Example: Create Doc, Insert Content, and Share with Anyone

```python
import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials
token_path = os.path.expanduser("~/.hermes/google_token.json")
with open(token_path) as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data["token"],
    refresh_token=token_data.get("refresh_token"),
    token_uri=token_data["token_uri"],
    client_id=token_data["client_id"],
    client_secret=token_data["client_secret"],
    scopes=token_data["scopes"]
)

# Build services
docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# 1. Create document
doc_title = "Document Title"
doc = docs_service.documents().create(body={"title": doc_title}).execute()
doc_id = doc.get("documentId")

# 2. Insert clean text (Replace all markdown elements)
content = "Your clean text here..."
requests = [
    {
        'insertText': {
            'location': {'index': 1},
            'text': content
        }
    }
]
docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

# 3. Share: Anyone with link can view (or 'writer' to write)
body = {
    'role': 'reader', # or 'writer'
    'type': 'anyone'
}
drive_service.permissions().create(
    fileId=doc_id,
    body=body
).execute()

print(f"https://docs.google.com/document/d/{doc_id}/edit")
```
