# Google Docs & Drive API Workarounds

This reference documents Hermes-specific workarounds when the bundled `google_api.py` CLI wrapper fails on complex content or sharing operations.

## Workaround 1: Append Multi-Line Text to a Google Doc

**Problem**: `google_api.py docs append DOC_ID --text "..."` fails when the text contains newlines, double quotes, or single quotes. The `--text` value is passed through shell quoting and breaks on special characters.

**Solution**: Use `execute_code` with the Python Google API client directly.

```python
from hermes_tools import terminal
import json, os

TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")
DOC_ID = "YOUR_DOC_ID"
CONTENT = """Your multi-line
text content here..."""

script = f'''
import json, os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open("{TOKEN_PATH}") as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data["token"],
    refresh_token=token_data.get("refresh_token"),
    token_uri=token_data["token_uri"],
    client_id=token_data["client_id"],
    client_secret=token_data["client_secret"],
    scopes=token_data["scopes"]
)

service = build('docs', 'v1', credentials=creds)

# Get current end index
doc = service.documents().get(documentId="{DOC_ID}").execute()
end_index = doc['body']['content'][-1]['endIndex'] - 1

requests = [{{
    'insertText': {{
        'location': {{'index': end_index}},
        'text': """{CONTENT}"""
    }}
}}]

result = service.documents().batchUpdate(
    documentId="{DOC_ID}",
    body={{'requests': requests}}
).execute()

print(json.dumps({{"status": "success"}}, indent=2))
'''

with open('/tmp/update_doc.py', 'w') as f:
    f.write(script)

result = terminal("python /tmp/update_doc.py")
print(result['output'])
```

**Notes**:
- The `endIndex` from `doc['body']['content'][-1]` is the insertion point at the end of the document.
- Escape triple-quotes in `CONTENT` if the text itself contains `"""`.
- For very long content, write to a temp file first and read it in the script.

## Workaround 2: Share File as "Anyone with Link"

**Problem**: `google_api.py drive share --type anyone` may be blocked by Drive configuration or not support all permission scenarios.

**Solution**: Use `execute_code` with the Drive API directly.

```python
from hermes_tools import terminal
import json, os

TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")
FILE_ID = "YOUR_FILE_ID"

script = f'''
import json, os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open("{TOKEN_PATH}") as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data["token"],
    refresh_token=token_data.get("refresh_token"),
    token_uri=token_data["token_uri"],
    client_id=token_data["client_id"],
    client_secret=token_data["client_secret"],
    scopes=token_data["scopes"]
)

service = build('drive', 'v3', credentials=creds)

body = {{
    'role': 'reader',
    'type': 'anyone'
}}

result = service.permissions().create(
    fileId="{FILE_ID}",
    body=body
).execute()

print(json.dumps({{
    "status": "success",
    "permission_id": result["id"],
    "role": result["role"],
    "type": result["type"]
}}, indent=2))
'''

with open('/tmp/share_file.py', 'w') as f:
    f.write(script)

result = terminal("python /tmp/share_file.py")
print(result['output'])
```

**Notes**:
- `role`: `reader` (view only), `commenter`, or `writer`
- `type`: `anyone` (link-based), `user` (specific email), `domain`
- The file will be accessible to anyone with the link after this call.

## Workaround 3: Date Verification Before Calendar Queries

**Critical Rule**: NEVER calculate target dates mentally. A manual `+1 day` error caused querying the wrong date and missing an appointment.

**Required verification pattern**:

```python
from datetime import datetime, timedelta

today = datetime.now()
tomorrow = today + timedelta(days=1)
next_week_start = today + timedelta(days=7)

print(f"Today: {today.strftime('%A, %d %B %Y')} ({today.strftime('%Y-%m-%d')})")
print(f"Tomorrow: {tomorrow.strftime('%A, %d %B %Y')} ({tomorrow.strftime('%Y-%m-%d')})")
```

**Before EVERY calendar query**:
1. Run the verification script above
2. Echo the computed date to the user
3. Only then pass the ISO date string to `$GAPI calendar list --start ... --end ...`

**Anti-pattern** (DO NOT do this):
```
# WRONG — mental arithmetic, error-prone
$GAPI calendar list --start "2026-05-29T00:00:00+07:00"  # guessed wrong
```

**Pattern** (DO this):
```bash
# Verify first
python -c "from datetime import datetime, timedelta; t = datetime.now() + timedelta(days=1); print(t.strftime('%Y-%m-%d'))"
# Then query with the verified date
$GAPI calendar list --start "2026-05-28T00:00:00+07:00" --end "2026-05-28T23:59:59+07:00"
```
