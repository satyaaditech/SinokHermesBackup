# Panduan Unggah Google Drive & Konversi Google Doc

Panduan ini berisi cara otomatisasi pengunggahan renungan harian dan berkas kesiswaan dari format Markdown lokal ke format Google Doc terformat di Google Drive menggunakan python API.

## Masalah dengan CLI `gws` / `google_api.py` bawaan
Fungsi `google_api.py drive upload` menyamakan tipe biner lokal dengan target di Drive.
Apabila kita menyuplai `--mime-type application/vnd.google-apps.document` saat mengunggah file HTML lokal, Drive API akan menolak karena mengira file biner lokal tersebut bernilai Google Doc.

## Solusi (Konversi Markdown -> HTML -> Google Doc)
Konversi dilakukan dengan cara mengubah asterisks obrolan WhatsApp menjadi standard Markdown bold (`**`), mengekstraksinya menjadi kode HTML terstruktur, menyimpan ke berkas temporary HTML, lalu mengunggahnya ke Drive dengan menyetel:
- **MediaFileUpload `mimetype`**: `'text/html'` (tipe berkas lokal kita)
- **Metadata `mimeType`**: `'application/vnd.google-apps.document'` (tipe berkas konversi target di Drive)

### Implementasi Python Custom Script
Gunakan script pembantu berikut (`/tmp/upload_reflections.py`):
```python
import sys
import os
import re
import markdown
import json

sys.path.insert(0, "/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts")
from google_api import get_credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = get_credentials()
drive_service = build("drive", "v3", credentials=creds)

def convert_md_to_html(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    # Ubah format bold obrolan WhatsApp (*) ke standard markdown (**)
    processed_text = re.sub(r'(?<!\*)\*(?!\s)([^*]+)(?<!\s)\*(?!\*)', r'**\1**', md_text)
    html_content = markdown.markdown(processed_text)
    
    html_body = f"""<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: 'Arial', sans-serif; font-size: 11pt; line-height: 1.6; color: #333333; }}
  h1 {{ font-size: 16pt; color: #1155cc; margin-top: 18px; margin-bottom: 6px; }}
  h2 {{ font-size: 13pt; color: #434343; margin-top: 13px; margin-bottom: 4px; }}
  p {{ margin-top: 0; margin-bottom: 12px; }}
  ul, ol {{ margin-top: 0; margin-bottom: 12px; padding-left: 20px; }}
  li {{ margin-bottom: 4px; }}
  blockquote {{ margin: 0 0 12px 0; padding-left: 10px; border-left: 3px solid #ccc; font-style: italic; color: #666; }}
</style>
</head>
<body>
  {html_content}
</body>
</html>"""
    return html_body

def upload_and_convert(html_content, name, parent_id):
    temp_html_path = "/tmp/temp_output.html"
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [parent_id]
    }
    
    media = MediaFileUpload(temp_html_path, mimetype="text/html", resumable=True)
    file = drive_service.files().create(body=metadata, media_body=media, fields="id, name, mimeType, webViewLink").execute()
    file_id = file.get("id")
    
    # Atur permission agar bisa dibaca siapa saja
    drive_service.permissions().create(fileId=file_id, body={"role": "reader", "type": "anyone"}).execute()
    
    # Ambil link webViewLink terbaru
    updated_file = drive_service.files().get(fileId=file_id, fields="webViewLink").execute()
    file["webViewLink"] = updated_file.get("webViewLink")
    
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)
    return file
```

## Metode Chicken-and-Egg (Tautan Mandiri Google Doc)

Apabila dokumen yang diunggah harus menyertakan tautan Google Doc-nya sendiri di bagian bawah teks (misal ketika menyematkan `Google Doc: [DOC_URL]`):
1. **Buat draft kosong terlebih dahulu di Drive** untuk mendapatkan `fileId` dan menghasilkan pranala `webViewLink`.
2. **Masukkan pranala tersebut ke dalam teks Markdown** sebelum dikonversi.
3. **Konversi dan unggah (update) konten** ke `fileId` yang sudah ada menggunakan `drive_service.files().update()`.

### Contoh Implementasi Python:
```python
# 1. Buat berkas kosong untuk dapatkan ID
metadata = {
    "name": "Renungan Narima - Sabtu, 15 Agustus 2026",
    "mimeType": "application/vnd.google-apps.document",
    "parents": [PARENT_FOLDER_ID]
}
file_obj = drive_service.files().create(body=metadata, fields="id").execute()
file_id = file_obj.get("id")
doc_url = f"https://docs.google.com/document/d/{file_id}/edit"

# 2. Atur izin publik (anyone with link can view)
drive_service.permissions().create(fileId=file_id, body={"role": "reader", "type": "anyone"}).execute()

# 3. Sisipkan doc_url ke teks Markdown lokal
markdown_template = markdown_template.replace("[DOC_URL]", doc_url)

# 4. Simpan ke berkas Markdown lokal & konversi ke HTML
# ... (proses konversi MD ke HTML) ...

# 5. Update isi Google Doc dengan berkas HTML
media = MediaFileUpload(temp_html_path, mimetype="text/html", resumable=True)
drive_service.files().update(fileId=file_id, media_body=media).execute()
```
