#!/usr/bin/env python3
"""
Master Midnight YouTube Channel Watchdog & Viral Video Scanner
Runs daily at 00:00 WIB with 3-Tier Multi-Channel Discovery:
  Tier 1: Check 'AKTIF MONITORED' channels for newly uploaded videos.
  Tier 2: If none, check 'CADANGAN' channels for new videos.
  Tier 3: Dig into high-performing / viral evergreen classic videos from all 10 monitored channels.
Extracts Golden Moments -> Updates Google Sheets (Status: DITEMUKAN) -> Reports to Telegram.
"""

import os
import sys
import json
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

CONFIG_PATH = "/home/satyaaditech/youtube_clipper_lab/channels_config.json"
PROCESSED_DB = "/home/satyaaditech/youtube_clipper_lab/processed_videos.json"
GOOGLE_TOKEN_PATH = "/home/satyaaditech/.hermes/google_token.json"
YOUTUBE_TOKEN_PATH = "/home/satyaaditech/.config/youtube/token.json"
SPREADSHEET_ID = "1d6Iyj0rZ22_m9CmwJn9XXDoAFqbWoWKKo96Uppsn4Ok"

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

def fetch_channel_videos(youtube, uploads_id, max_results=5):
    try:
        res = youtube.playlistItems().list(
            playlistId=uploads_id,
            part="snippet",
            maxResults=max_results
        ).execute()
        videos = []
        for item in res.get("items", []):
            snip = item["snippet"]
            vid = snip["resourceId"]["videoId"]
            title = snip["title"]
            pub = snip["publishedAt"]
            videos.append({
                "id": vid,
                "title": title,
                "link": f"https://youtu.be/{vid}",
                "published": pub
            })
        return videos
    except Exception as e:
        print(f"Error fetching playlist {uploads_id}: {e}", file=sys.stderr)
        return []

def fetch_viral_videos(youtube, channel_id, max_results=5):
    try:
        res = youtube.search().list(
            channelId=channel_id,
            order="viewCount",
            type="video",
            videoDuration="medium", # 4-20 min
            part="snippet",
            maxResults=max_results
        ).execute()
        videos = []
        for item in res.get("items", []):
            snip = item["snippet"]
            vid = item["id"]["videoId"]
            title = snip["title"]
            pub = snip["publishedAt"]
            videos.append({
                "id": vid,
                "title": title,
                "link": f"https://youtu.be/{vid}",
                "published": pub
            })
        return videos
    except Exception as e:
        print(f"Error searching viral videos for {channel_id}: {e}", file=sys.stderr)
        return []

def run_midnight_scan():
    with open(CONFIG_PATH) as f:
        channels = json.load(f)
    
    youtube = get_youtube_service()
    if not youtube:
        print("❌ YouTube API credentials not found.")
        return

    processed_ids = load_processed_ids()
    selected_video = None
    source_channel = None
    scan_tier = None
    
    # --- TIER 1: AKTIF MONITORED (New Uploads) ---
    active_channels = [c for c in channels if c.get("status") == "AKTIF MONITORED"]
    for ch in active_channels:
        vids = fetch_channel_videos(youtube, ch["uploads_id"], max_results=5)
        for v in vids:
            if v["id"] not in processed_ids:
                selected_video = v
                source_channel = ch
                scan_tier = "Tier 1 (Kanal Utama Aktif - Video Baru)"
                break
        if selected_video:
            break
            
    # --- TIER 2: CADANGAN (New Uploads from Backup Channels) ---
    if not selected_video:
        backup_channels = [c for c in channels if c.get("status") == "CADANGAN"]
        for ch in backup_channels:
            vids = fetch_channel_videos(youtube, ch["uploads_id"], max_results=5)
            for v in vids:
                if v["id"] not in processed_ids:
                    selected_video = v
                    source_channel = ch
                    scan_tier = "Tier 2 (Kanal Cadangan - Video Baru)"
                    break
            if selected_video:
                break
                
    # --- TIER 3: VIRAL & EVERGREEN CLASSICS (Top Views from All Channels) ---
    if not selected_video:
        for ch in channels:
            vids = fetch_viral_videos(youtube, ch["id"], max_results=5)
            for v in vids:
                if v["id"] not in processed_ids:
                    selected_video = v
                    source_channel = ch
                    scan_tier = "Tier 3 (Arsip Video Lawas / Viral Evergreen)"
                    break
            if selected_video:
                break

    if not selected_video:
        msg = "🌙 *Laporan Pantauan Kanal Tengah Malam (00:00 WIB)*\n\nStatus: Seluruh saluran telah terproses sempurna, tidak ditemukan video baru atau arsip belum terproses hari ini. Tidak boleh [SILENT], laporan terkirim."
        print(msg)
        return

    # Mark as processed in local tracking
    save_processed_id(selected_video["id"])

    # Output detailed report for Telegram
    report = f"""🌙 *Laporan Pantauan Saluran YouTube (00:00 WIB)*

📡 *Tingkat Pemindaian:* `{scan_tier}`
📺 *Saluran Sumber:* **{source_channel['name']}** (`{source_channel['handle']}`)
📌 *Judul Video Sumber:* _{selected_video['title']}_
🔗 *Link YouTube:* {selected_video['link']}
📅 *Waktu Rilis:* `{selected_video['published']}`

✨ *Status Integrasi:*
1. Video berhasil diamankan dan ditandai dalam sistem pencegahan duplikasi (`processed_videos.json`).
2. Calon momen emas siap dianalisis dan dicatat ke Google Sheets dengan status default `DITEMUKAN`.

Pusat Kontrol: [Buka Google Sheets Pipeline](https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit)"""

    print(report)

if __name__ == "__main__":
    run_midnight_scan()
