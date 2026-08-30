# Panduan Pembuatan Audio & Integrasi Telegram

Panduan ini berisi cara otomatisasi pembuatan versi audio (TTS) renungan harian dan pengirimannya secara langsung sebagai pesan suara (Voice Note) kesiswaan ke Telegram chat menggunakan python API.

## 1. Konversi Audio MP3 ke OGG Opus (Kompatibel Telegram Voice Note)

Layanan `edge-tts` secara bawaan menghasilkan berkas berformat MP3. Telegram memerlukan berkas berkode Opus didalam wadah OGG (`Ogg data, Opus audio`) agar dapat dibagikan aslinya sebagai **Voice Note** (bukan file lampiran regular).

Gunakan `ffmpeg` untuk konversi:
```bash
ffmpeg -y -i input.mp3 -c:a libopus output.ogg
```

## 2. Pengunggahan Otomatis & Alur URL Mandiri (Chicken-and-Egg)

Apabila naskah tertulis di chat memerlukan tautan Google Doc-nya sendiri, buat rancangan draf kosong terlebih dahulu di Google Drive untuk mendapatkan file ID dan pranala:

```python
# 1. Inisialisasi Drive API
sys.path.insert(0, "/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts")
from google_api import get_credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = get_credentials()
drive_service = build("drive", "v3", credentials=creds)

# 2. Buat Draft Dokumen Kosong
metadata = {
    "name": "Renungan Penyiswaan - Jumat, 21 Agustus 2026",
    "mimeType": "application/vnd.google-apps.document",
    "parents": ["1Ei8R28btJH6rjCC1lKrfkaCC-KxmKeNW"]
}
file_obj = drive_service.files().create(body=metadata, fields="id").execute()
file_id = file_obj.get("id")
doc_url = f"https://docs.google.com/document/d/{file_id}/edit"

# 3. Beri Izin Reader Publik
drive_service.permissions().create(fileId=file_id, body={"role": "reader", "type": "anyone"}).execute()

# 4. Sisipkan doc_url ke naskah Markdown lokal
markdown_content = markdown_content.replace("[DOC_URL]", doc_url)

# 5. Konversi Markdown ke HTML & Perbarui Google Doc
# ... (konversi html) ...
media = MediaFileUpload(temp_html_path, mimetype="text/html", resumable=True)
drive_service.files().update(fileId=file_id, media_body=media).execute()
```

## 3. Pengiriman Voice Note Lewat Telegram Bot API

Gunakan metode `sendVoice` untuk mengirimkan berkas OGG Opus secara langsung, sehingga dapat diputar langsung di aplikasi Telegram seluler tanpa di-download terlebih dahulu.

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv("/home/satyaaditech/.hermes/.env")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = "-1003256146835"
thread_id = "1096"

def send_telegram_voice(file_path, caption):
    url = f"https://api.telegram.org/bot{telegram_token}/sendVoice"
    with open(file_path, "rb") as f:
        files = {'voice': f}
        payload = {
            'chat_id': chat_id,
            'message_thread_id': thread_id,
            'caption': caption
        }
        res = requests.post(url, files=files, data=payload)
        return res.json()
```

## 4. Pembersihan Teks Sebelum Diberikan ke TTS

Sebelum mengirimkan teks naskah ke mesin `edge-tts`, hilangkan tag format, emoji, dan tautan luar agar suara lafal terdengar wajar dan tidak terganggu pembacaan simbol:

```python
import re

def clean_for_tts(text):
    # Hilangkan Emojis
    text = re.sub(r'[\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF]', '', text)
    # Hilangkan simbol Markdown (*, _, #)
    text = text.replace("**", "").replace("*", "").replace("_", "").replace("##", "").replace("#", "")
    # Hilangkan baris Google Doc URL
    text = re.sub(r'Google Doc:.*', '', text)
    # Filter baris kosong berlebih
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)
```
