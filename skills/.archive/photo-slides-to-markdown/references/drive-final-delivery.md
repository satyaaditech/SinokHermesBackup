# Final Delivery: Upload .md to Google Drive + Share Link (backup pattern)

Established 2026-08-09 (Bussines_plan_coaching session). User asked: "setelah selesai proses kirim aku link download file terbaru" — same as the FGD_Sekolah_Herbal.md workflow. Deliver the finished .md as a download link, NOT just "file saved on server".

> UPDATE 2026-08-09 (later same session): user prefers the Hermes-server HTTP link (`references/server-link-delivery.md`) — use that as PRIMARY. This Drive path is the FALLBACK/backup.
> TIP: when re-uploading later versions, first list for an existing file with the same name in the parent folder (`files().list(q="name='X' and trashed=false and '<FOLDER>' in parents")`) and `files().update(fileId=...)` it instead of creating a duplicate — keeps the SAME URL so the user's saved link never breaks.

## Preconditions (check BEFORE promising a link)
- `~/.hermes/google_token.json` and `~/.hermes/google_client_secret.json` exist
- `python3 -c "import googleapiclient"` works
If missing, tell the user the Drive link can't be built yet and fix/setup first.

## Script: upload local file → Drive root → anyone-with-link → print share URL

Save as a temp file and run with `python3` (pattern adapted from google-workspace skill's docs-api-workaround; that ref only covers SHARING an existing FILE_ID — this one does UPLOAD + SHARE in one pass).

```python
import json, os, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")
LOCAL_FILE = sys.argv[1] if len(sys.argv) > 1 else "/home/satyaaditech/Bussines_plan_coaching.md"
FOLDER_ID  = sys.argv[2] if len(sys.argv) > 2 else "1Rnsy7DuxI_2jHv2aGeDD-leNmOCBoggK"  # Drive root

with open(TOKEN_PATH) as f:
    t = json.load(f)
creds = Credentials(
    token=t["token"], refresh_token=t.get("refresh_token"),
    token_uri=t["token_uri"], client_id=t["client_id"],
    client_secret=t["client_secret"], scopes=t["scopes"],
)

drive = build("drive", "v3", credentials=creds)
fname = os.path.basename(LOCAL_FILE)
md = drive.files().create(
    body={"name": fname, "parents": [FOLDER_ID], "mimeType": "text/markdown"},
    media_body=LOCAL_FILE, fields="id,webViewLink",
).execute()

drive.permissions().create(
    fileId=md["id"], body={"role": "reader", "type": "anyone"},
).execute()

print("FILE_ID:", md["id"])
print("DOWNLOAD:", f"https://drive.google.com/uc?export=download&id={md['id']}")
print("VIEW:", md.get("webViewLink"))
```

## Message pattern to user
Short confirm + one line per item + the DOWNLOAD link. Example:
"✅ Selesai! File terbaru sudah di-upload. 📥 Download: <link>"

## Pitfalls
- Re-uploading the same filename to the same folder creates a SECOND file (Drive allows duplicates). Either delete the old one first or overwrite by fileId. User wants "file terbaru" → prefer finding existing file by name (drive.files().list q=f"name='{fname}'") and files().update(media_body=...) to avoid duplicate links.
- Use the `uc?export=download` URL for a real download; `webViewLink` opens the Drive viewer (still fine, but user asked "link download").
- Verify the share actually worked by printing the permission result before telling the user it succeeded.
