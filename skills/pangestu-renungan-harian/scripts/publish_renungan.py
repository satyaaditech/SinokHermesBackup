import os
import sys
import re
import markdown
import requests
import subprocess
from dotenv import load_dotenv

sys.path.insert(0, "/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts")
from google_api import get_credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Target Folder ID for "Renungan Harian"
PARENT_FOLDER_ID = "1Ei8R28btJH6rjCC1lKrfkaCC-KxmKeNW"
CHAT_ID = "-1003256146835"
THREAD_ID = "1096"

def convert_md_to_html(md_text):
    processed_text = re.sub(r'(?<!\*)\*(?!\s)([^*]+)(?<!\s)\*(?!\*)', r'**\1**', md_text)
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

def clean_for_tts(text):
    # Remove emojis
    text = re.sub(r'[\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF]', '', text)
    # Remove markdown formatting
    text = text.replace("**", "").replace("*", "").replace("_", "").replace("##", "").replace("#", "")
    # Remove Google Doc URL line
    text = re.sub(r'(?i)Google Doc:.*', '', text)
    text = text.replace("Terjemahan:", "")
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)

def publish(jawa_template, ind_template, date_str, date_iso, jawa_out_path, ind_out_path, ogg_jawa_path, ogg_ind_path):
    load_dotenv("/home/satyaaditech/.env")
    load_dotenv("/home/satyaaditech/.hermes/.env")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    creds = get_credentials()
    drive_service = build("drive", "v3", credentials=creds)
    
    # 1. Create Google Docs drafts
    print("Creating Google Docs...")
    meta_jawa = {
        "name": f"Renungan Penyiswaan - {date_str}",
        "mimeType": "application/vnd.google-apps.document",
        "parents": [PARENT_FOLDER_ID]
    }
    file_jawa = drive_service.files().create(body=meta_jawa, fields="id").execute()
    id_jawa = file_jawa.get("id")
    url_jawa = f"https://docs.google.com/document/d/{id_jawa}/edit"
    drive_service.permissions().create(fileId=id_jawa, body={"role": "reader", "type": "anyone"}).execute()
    
    meta_ind = {
        "name": f"Renungan Penyiswaan (Id) - {date_str}",
        "mimeType": "application/vnd.google-apps.document",
        "parents": [PARENT_FOLDER_ID]
    }
    file_ind = drive_service.files().create(body=meta_ind, fields="id").execute()
    id_ind = file_ind.get("id")
    url_ind = f"https://docs.google.com/document/d/{id_ind}/edit"
    drive_service.permissions().create(fileId=id_ind, body={"role": "reader", "type": "anyone"}).execute()
    
    # 2. Insert links to markdown
    jawa_md = jawa_template.replace("[DOC_URL]", url_jawa)
    ind_md = ind_template.replace("[DOC_URL]", url_ind)
    
    with open(jawa_out_path, "w", encoding="utf-8") as f:
        f.write(jawa_md)
    with open(ind_out_path, "w", encoding="utf-8") as f:
        f.write(ind_md)
        
    # 3. Populate Google Docs content
    print("Populating Google Docs...")
    html_jawa = convert_md_to_html(jawa_md)
    html_ind = convert_md_to_html(ind_md)
    
    tmp_jawa = "/tmp/temp_jawa.html"
    tmp_ind = "/tmp/temp_ind.html"
    
    with open(tmp_jawa, "w", encoding="utf-8") as f:
        f.write(html_jawa)
    with open(tmp_ind, "w", encoding="utf-8") as f:
        f.write(html_ind)
        
    media_jawa = MediaFileUpload(tmp_jawa, mimetype="text/html", resumable=True)
    drive_service.files().update(fileId=id_jawa, media_body=media_jawa).execute()
    
    media_ind = MediaFileUpload(tmp_ind, mimetype="text/html", resumable=True)
    drive_service.files().update(fileId=id_ind, media_body=media_ind).execute()
    
    os.remove(tmp_jawa)
    os.remove(tmp_ind)
    
    # 4. Generate TTS & convert to Opus ogg
    print("Generating TTS and converting to Ogg...")
    jawa_clean = clean_for_tts(jawa_md)
    ind_clean = clean_for_tts(ind_md)
    
    with open("/tmp/jawa_tts.txt", "w", encoding="utf-8") as f:
        f.write(jawa_clean)
    with open("/tmp/ind_tts.txt", "w", encoding="utf-8") as f:
        f.write(ind_clean)
        
    subprocess.run(["edge-tts", "--voice", "jv-ID-DimasNeural", "--file", "/tmp/jawa_tts.txt", "--write-media", "/tmp/jawa_temp.mp3"], check=True)
    subprocess.run(["edge-tts", "--voice", "id-ID-GadisNeural", "--file", "/tmp/ind_tts.txt", "--write-media", "/tmp/ind_temp.mp3"], check=True)
    
    subprocess.run(["ffmpeg", "-y", "-i", "/tmp/jawa_temp.mp3", "-c:a", "libopus", ogg_jawa_path], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", "/tmp/ind_temp.mp3", "-c:a", "libopus", ogg_ind_path], check=True)
    
    os.remove("/tmp/jawa_tts.txt")
    os.remove("/tmp/ind_tts.txt")
    os.remove("/tmp/jawa_temp.mp3")
    os.remove("/tmp/ind_temp.mp3")
    
    # 5. Send voices to Telegram
    print("Sending voice messages to Telegram...")
    url = f"https://api.telegram.org/bot{telegram_token}/sendVoice"
    
    # Jawa voice
    with open(ogg_jawa_path, "rb") as f:
        requests.post(url, files={'voice': f}, data={
            'chat_id': CHAT_ID,
            'message_thread_id': THREAD_ID,
            'caption': f"Renungan Penyiswaan (Jawi Krama) - {date_str}"
        })
        
    # Ind voice
    with open(ogg_ind_path, "rb") as f:
        requests.post(url, files={'voice': f}, data={
            'chat_id': CHAT_ID,
            'message_thread_id': THREAD_ID,
            'caption': f"Renungan Penyiswaan (Indonesia) - {date_str}"
        })
        
    print("Publishing complete!")
