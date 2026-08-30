import os
sys = __import__("sys")
import re
import markdown
from dotenv import load_dotenv

sys.path.insert(0, "/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts")
from google_api import get_credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Target Folder ID for "Renungan Harian"
PARENT_FOLDER_ID = "1Ei8R28btJH6rjCC1lKrfkaCC-KxmKeNW"

def convert_md_to_html(md_text):
    # Strip YAML frontmatter at the very beginning
    md_text = re.sub(r'^---\s*\n.*?\n---\s*(\n|$)', '', md_text, flags=re.DOTALL)

    # Strip Obsidian wikilinks: [[Concept|alias]] -> alias, then [[Concept]] -> Concept
    clean_text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', md_text)
    clean_text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', clean_text)
    
    processed_text = re.sub(r'(?<!\*)\*(?!\s)([^*]+)(?<!\s)\*(?!\*)', r'**\1**', clean_text)
    html_content = markdown.markdown(processed_text)
    
    html_body = f"""<!DOCTYPE html>
<html>
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

def publish_simple(ind_template, date_str, date_iso, ind_out_path):
    load_dotenv("/home/satyaaditech/.env")
    load_dotenv("/home/satyaaditech/.hermes/.env")
    
    creds = get_credentials()
    drive_service = build("drive", "v3", credentials=creds)
    
    # 1. Create Google Docs draft (Indonesia only)
    print("Creating Indonesian Google Doc...")
    meta_ind = {
        "name": f"Renungan Penyiswaan (Id) - {date_str}",
        "mimeType": "application/vnd.google-apps.document",
        "parents": [PARENT_FOLDER_ID]
    }
    file_ind = drive_service.files().create(body=meta_ind, fields="id").execute()
    id_ind = file_ind.get("id")
    url_ind = f"https://docs.google.com/document/d/{id_ind}/edit"
    drive_service.permissions().create(fileId=id_ind, body={"role": "reader", "type": "anyone"}).execute()
    
    # 2. Insert link to markdown
    ind_md = ind_template.replace("[DOC_URL]", url_ind)
    
    with open(ind_out_path, "w", encoding="utf-8") as f:
        f.write(ind_md)
        
    # 3. Populate Google Docs content
    print("Populating Google Doc...")
    html_ind = convert_md_to_html(ind_md)
    
    tmp_ind = "/tmp/temp_ind.html"
    with open(tmp_ind, "w", encoding="utf-8") as f:
        f.write(html_ind)
        
    media_ind = MediaFileUpload(tmp_ind, mimetype="text/html", resumable=True)
    drive_service.files().update(fileId=id_ind, media_body=media_ind).execute()
    
    os.remove(tmp_ind)
    print(f"Publishing complete! Google Doc URL: {url_ind}")
    return url_ind
