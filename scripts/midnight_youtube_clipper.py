#!/usr/bin/env python3
"""
Master Midnight YouTube Channel Watchdog & Autonomous Golden Moment Scanner
Runs daily at 00:00 WIB:
  1. Scans Target Channels (Tier 1: Aktif, Tier 2: Cadangan, Tier 3: Viral Classics).
  2. Filters long-form videos (>= 180s, ignores Shorts).
  3. Extracts full transcript via YouTubeTranscriptApi.
  4. Analyzes & discovers 2-4 Golden Moments (60-150s, 3-Act Story Arc) via LLM.
  5. Automatically writes new rows to Master Google Sheets with status 'DITEMUKAN'.
  6. Saves processed video ID to prevent duplicate processing.
  7. Formats & delivers a complete Telegram executive brief.
"""

import os
import sys
import json
import re
import requests
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from youtube_transcript_api import YouTubeTranscriptApi

CONFIG_PATH = "/home/satyaaditech/youtube_clipper_lab/channels_config.json"
PROCESSED_DB = "/home/satyaaditech/youtube_clipper_lab/processed_videos.json"
GOOGLE_TOKEN_PATH = "/home/satyaaditech/.hermes/google_token.json"
YOUTUBE_TOKEN_PATH = "/home/satyaaditech/.config/youtube/token.json"
SPREADSHEET_ID = "1d6Iyj0rZ22_m9CmwJn9XXDoAFqbWoWKKo96Uppsn4Ok"
OMNIROUTE_URL = "http://127.0.0.1:20128/v1/chat/completions"

def get_sheets_service():
    if not os.path.exists(GOOGLE_TOKEN_PATH):
        return None
    with open(GOOGLE_TOKEN_PATH) as f:
        info = json.load(f)
    creds = Credentials.from_authorized_user_info(info)
    return build("sheets", "v4", credentials=creds)

def get_youtube_service():
    if not os.path.exists(YOUTUBE_TOKEN_PATH):
        return None
    with open(YOUTUBE_TOKEN_PATH) as f:
        info = json.load(f)
    creds = Credentials.from_authorized_user_info(info)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(YOUTUBE_TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def load_processed_ids():
    if os.path.exists(PROCESSED_DB):
        try:
            with open(PROCESSED_DB) as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_processed_id(video_id):
    ids = load_processed_ids()
    if video_id not in ids:
        ids.append(video_id)
        with open(PROCESSED_DB, "w") as f:
            json.dump(ids, f, indent=2)

def parse_iso_duration(duration_str):
    match = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    d = int(match.group(1) or 0)
    h = int(match.group(2) or 0)
    m = int(match.group(3) or 0)
    s = int(match.group(4) or 0)
    return d * 86400 + h * 3600 + m * 60 + s

def get_video_details(youtube, video_ids):
    if not video_ids:
        return {}
    res = youtube.videos().list(
        id=",".join(video_ids),
        part="snippet,contentDetails"
    ).execute()
    details = {}
    for item in res.get("items", []):
        vid = item["id"]
        snip = item["snippet"]
        cd = item["contentDetails"]
        dur_sec = parse_iso_duration(cd.get("duration", "PT0S"))
        details[vid] = {
            "id": vid,
            "title": snip.get("title", ""),
            "channel_title": snip.get("channelTitle", ""),
            "published": snip.get("publishedAt", ""),
            "duration_sec": dur_sec,
            "link": f"https://youtu.be/{vid}"
        }
    return details

def fetch_channel_videos(youtube, uploads_id, max_results=10):
    try:
        res = youtube.playlistItems().list(
            playlistId=uploads_id,
            part="snippet",
            maxResults=max_results
        ).execute()
        raw_ids = [item["snippet"]["resourceId"]["videoId"] for item in res.get("items", [])]
        details = get_video_details(youtube, raw_ids)
        return list(details.values())
    except Exception as e:
        print(f"Error fetching playlist {uploads_id}: {e}", file=sys.stderr)
        return []

def fetch_viral_videos(youtube, channel_id, max_results=5):
    try:
        res = youtube.search().list(
            channelId=channel_id,
            order="viewCount",
            type="video",
            videoDuration="medium",
            part="snippet",
            maxResults=max_results
        ).execute()
        raw_ids = [item["id"]["videoId"] for item in res.get("items", [])]
        details = get_video_details(youtube, raw_ids)
        return list(details.values())
    except Exception as e:
        print(f"Error searching viral videos for {channel_id}: {e}", file=sys.stderr)
        return []

def extract_transcript(video_id):
    ytt = YouTubeTranscriptApi()
    try:
        t = ytt.fetch(video_id)
        return t
    except Exception as e:
        print(f"Transcript fetch error for {video_id}: {e}", file=sys.stderr)
        return None

def analyze_golden_moments(video_title, channel_name, transcript_items):
    formatted_lines = []
    for item in transcript_items:
        mm = int(item.start // 60)
        ss = int(item.start % 60)
        text_clean = item.text.replace("\n", " ").strip()
        formatted_lines.append(f"[{mm:02d}:{ss:02d}] {text_clean}")
    
    transcript_text = "\n".join(formatted_lines)
    
    prompt = f"""Kamu adalah analis kurasi konten YouTube Shorts & video editor profesional.
Tugasmu adalah menganalisis transkrip video berikut dan memilih 2 sampai 4 'Momen Emas' (Golden Moments) yang berdiri sendiri (self-contained) dan sangat potensial viral untuk YouTube Shorts (format vertikal 9:16).

Kriteria Mutlak Momen Emas:
1. Durasi tiap klip antara 60 detik hingga 150 detik (1 - 2,5 menit).
2. Memiliki alur cerita 3-Babak TUNTAS:
   - Hook / Percikan Penasaran (menarik penonton dalam 5 detik pertama).
   - Eksplorasi / Alur Pemikiran (pembahasan inti secara jelas dan memikat).
   - Dudutan / Poin Kunci / Kesimpulan Penting (jawaban atau insight di akhir klip).
3. Draft Judul Shorts wajib dalam Bahasa Indonesia baku yang memancing rasa penasaran, dilengkapi 1-2 emoji dan tag #Shorts.
4. Timestamp harus presisi (format MM:SS - MM:SS) berdasarkan transkrip.

Detail Video:
- Saluran Sumber: {channel_name}
- Judul Video: {video_title}

Transkrip Video:
{transcript_text[:12000]}

Keluarkan HANYA JSON murni dengan format persis seperti ini:
{{
  "clips": [
    {{
      "topic": "Uraian singkat topik klip dalam bahasa Indonesia",
      "start_time": "MM:SS",
      "end_time": "MM:SS",
      "duration_sec": 105,
      "draft_title": "Judul Shorts Bahasa Indonesia 🧠💥 #Shorts"
    }}
  ]
}}"""

    payload = {
        "model": "daily-chat",
        "stream": False,
        "messages": [
            {"role": "system", "content": "You are a professional video curator. Output strictly valid JSON only."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        r = requests.post(OMNIROUTE_URL, json=payload, timeout=60)
        content = r.json()["choices"][0]["message"]["content"].strip()
        
        # Strip markdown json block if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        data = json.loads(content)
        return data.get("clips", [])
    except Exception as e:
        print(f"LLM analysis error: {e}", file=sys.stderr)
        return []

def get_next_clip_id(sheets):
    try:
        res = sheets.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A2:A100"
        ).execute()
        rows = res.get("values", [])
        max_id = 0
        for r in rows:
            if r and r[0].startswith("CLIP-"):
                try:
                    num = int(r[0].replace("CLIP-", ""))
                    if num > max_id:
                        max_id = num
                except ValueError:
                    pass
        return max_id + 1
    except Exception as e:
        print(f"Error finding next clip id: {e}", file=sys.stderr)
        return 1

def append_clips_to_sheets(sheets, channel_name, video_title, clips):
    if not clips:
        return []
    
    start_num = get_next_clip_id(sheets)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    rows_to_append = []
    created_clips = []
    
    for idx, clip in enumerate(clips):
        clip_num = start_num + idx
        clip_id = f"CLIP-{clip_num:03d}"
        
        start_ts = clip.get("start_time", "00:00")
        end_ts = clip.get("end_time", "01:30")
        dur_s = clip.get("duration_sec", 90)
        dur_str = f"{dur_s}s ({dur_s//60}m {dur_s%60:02d}s)"
        topic = clip.get("topic", "")
        draft_title = clip.get("draft_title", "")
        
        row = [
            clip_id,
            channel_name,
            video_title,
            topic,
            f"{start_ts} - {end_ts}",
            dur_str,
            draft_title,
            "DITEMUKAN",
            "-",
            today_str,
            f"Credit: {channel_name}"
        ]
        rows_to_append.append(row)
        created_clips.append({
            "id": clip_id,
            "topic": topic,
            "timestamp": f"{start_ts} - {end_ts}",
            "duration": dur_str,
            "title": draft_title
        })
        
    sheets.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A12:K",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": rows_to_append}
    ).execute()
    
    return created_clips

def run_midnight_scan():
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Configuration not found: {CONFIG_PATH}")
        return

    with open(CONFIG_PATH) as f:
        channels = json.load(f)
    
    youtube = get_youtube_service()
    if not youtube:
        print("❌ YouTube API credentials not found.")
        return
        
    sheets = get_sheets_service()
    if not sheets:
        print("❌ Google Sheets API credentials not found.")
        return

    processed_ids = load_processed_ids()
    selected_video = None
    source_channel = None
    scan_tier = None
    transcript_items = None
    
    # --- TIER 1: AKTIF MONITORED (New Uploads >= 180s) ---
    active_channels = [c for c in channels if c.get("status") == "AKTIF MONITORED"]
    for ch in active_channels:
        vids = fetch_channel_videos(youtube, ch["uploads_id"], max_results=10)
        for v in vids:
            if v["id"] not in processed_ids and v["duration_sec"] >= 180:
                t = extract_transcript(v["id"])
                if t:
                    selected_video = v
                    source_channel = ch
                    scan_tier = "Tier 1 (Kanal Utama Aktif - Video Baru)"
                    transcript_items = t
                    break
        if selected_video:
            break
            
    # --- TIER 2: CADANGAN (New Uploads from Backup Channels) ---
    if not selected_video:
        backup_channels = [c for c in channels if c.get("status") == "CADANGAN"]
        for ch in backup_channels:
            vids = fetch_channel_videos(youtube, ch["uploads_id"], max_results=10)
            for v in vids:
                if v["id"] not in processed_ids and v["duration_sec"] >= 180:
                    t = extract_transcript(v["id"])
                    if t:
                        selected_video = v
                        source_channel = ch
                        scan_tier = "Tier 2 (Kanal Cadangan - Video Baru)"
                        transcript_items = t
                        break
            if selected_video:
                break
                
    # --- TIER 3: VIRAL & EVERGREEN CLASSICS ---
    if not selected_video:
        for ch in channels:
            vids = fetch_viral_videos(youtube, ch["id"], max_results=5)
            for v in vids:
                if v["id"] not in processed_ids and v["duration_sec"] >= 180:
                    t = extract_transcript(v["id"])
                    if t:
                        selected_video = v
                        source_channel = ch
                        scan_tier = "Tier 3 (Arsip Video Lawas / Viral Evergreen)"
                        transcript_items = t
                        break
            if selected_video:
                break

    if not selected_video or not source_channel or not transcript_items:
        msg = "🌙 *Laporan Pantauan Kanal Tengah Malam (00:00 WIB)*\n\nStatus: Seluruh video panjang dari saluran target telah terproses. Tidak ada video baru atau arsip belum terproses hari ini. Tidak boleh [SILENT], laporan terkirim."
        print(msg)
        return

    # Extract Golden Moments via LLM
    golden_clips = analyze_golden_moments(
        video_title=selected_video["title"],
        channel_name=source_channel["name"],
        transcript_items=transcript_items
    )
    
    if not golden_clips:
        print(f"⚠️ Gagal mengekstrak momen emas untuk {selected_video['title']}.")
        return
        
    # Append to Google Sheets with status DITEMUKAN
    created = append_clips_to_sheets(
        sheets=sheets,
        channel_name=source_channel["name"],
        video_title=selected_video["title"],
        clips=golden_clips
    )
    
    # Save video ID to prevent duplicate scan
    save_processed_id(selected_video["id"])

    # Output detailed report for Telegram
    clips_table = ""
    for c in created:
        clips_table += f"• **{c['id']}** (`{c['timestamp']}` - {c['duration']})\n  _{c['title']}_\n"

    report = f"""🌙 *Laporan Pantauan Saluran YouTube (00:00 WIB)*

📡 *Tingkat Pemindaian:* `{scan_tier}`
📺 *Saluran Sumber:* **{source_channel['name']}** (`{source_channel['handle']}`)
📌 *Judul Video Sumber:* _{selected_video['title']}_
🔗 *Link YouTube:* {selected_video['link']}
📅 *Waktu Rilis:* `{selected_video['published']}`

✨ *Momen Emas Berhasil Ditambahkan ke Google Sheets (Status: `DITEMUKAN`):*
{clips_table}
Pusat Kontrol: [Buka Google Sheets Master Pipeline](https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit)"""

    print(report)

if __name__ == "__main__":
    run_midnight_scan()
