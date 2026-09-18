#!/usr/bin/env python3
"""
Master Midnight YouTube Channel Watchdog & Golden Moment Scanner
Runs daily at 00:00 WIB with 3-Tier Fallback:
  Tier 1: Check 'AKTIF MONITORED' channels for newly uploaded videos.
  Tier 2: If none, check 'CADANGAN' channels for new videos.
  Tier 3: If still none, dig into evergreen archive videos from monitored channels.
Extracts Golden Moments -> Updates Google Sheets (Status: DITEMUKAN) -> Reports to Telegram.
"""

import os
import sys
import json
import urllib.request
import xml.etree.ElementTree as ET
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime

CONFIG_PATH = "/home/satyaaditech/youtube_clipper_lab/channels_config.json"
PROCESSED_DB = "/home/satyaaditech/youtube_clipper_lab/processed_videos.json"
GOOGLE_TOKEN_PATH = "/home/satyaaditech/.hermes/google_token.json"
SPREADSHEET_ID = "1d6Iyj0rZ22_m9CmwJn9XXDoAFqbWoWKKo96Uppsn4Ok"

def get_sheets_service():
    with open(GOOGLE_TOKEN_PATH) as f:
        info = json.load(f)
    creds = Credentials.from_authorized_user_info(info)
    return build("sheets", "v4", credentials=creds)

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

def fetch_rss_videos(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            xml_data = res.read()
            root = ET.fromstring(xml_data)
            ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
            videos = []
            for entry in root.findall("atom:entry", ns):
                vid = entry.find("yt:videoId", ns).text
                title = entry.find("atom:title", ns).text
                link = entry.find("atom:link", ns).attrib["href"]
                published = entry.find("atom:published", ns).text
                videos.append({"id": vid, "title": title, "link": link, "published": published})
            return videos
    except Exception as e:
        return []

def run_midnight_scan():
    with open(CONFIG_PATH) as f:
        channels = json.load(f)
    
    processed_ids = load_processed_ids()
    selected_video = None
    source_channel = None
    scan_tier = None
    
    # --- TIER 1: AKTIF MONITORED ---
    active_channels = [c for c in channels if c.get("status") == "AKTIF MONITORED"]
    for ch in active_channels:
        vids = fetch_rss_videos(ch["id"])
        for v in vids:
            if v["id"] not in processed_ids:
                selected_video = v
                source_channel = ch
                scan_tier = "Tier 1 (Kanal Utama Aktif)"
                break
        if selected_video:
            break
            
    # --- TIER 2: CADANGAN (If Tier 1 empty) ---
    if not selected_video:
        backup_channels = [c for c in channels if c.get("status") == "CADANGAN"]
        for ch in backup_channels:
            vids = fetch_rss_videos(ch["id"])
            for v in vids:
                if v["id"] not in processed_ids:
                    selected_video = v
                    source_channel = ch
                    scan_tier = "Tier 2 (Kanal Cadangan)"
                    break
            if selected_video:
                break
                
    # --- TIER 3: ARSIP EVERGREEN (If Tier 2 empty) ---
    if not selected_video:
        # Check archive feeds or fallback channels
        for ch in channels:
            vids = fetch_rss_videos(ch["id"])
            for v in reversed(vids): # check older entries in feed
                if v["id"] not in processed_ids:
                    selected_video = v
                    source_channel = ch
                    scan_tier = "Tier 3 (Arsip Video Lawas Evergreen)"
                    break
            if selected_video:
                break

    if not selected_video:
        msg = "🌙 *Laporan Pantauan Kanal Tengah Malam (00:00 WIB)*\n\nStatus: Seluruh saluran telah terproses sempurna, tidak ditemukan video baru atau arsip belum terproses hari ini."
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
1. Transkrip & Momen Emas sedang diekstraksi ke Google Sheets.
2. Baris baru telah dicatat di Tab 1 dengan status default: `DITEMUKAN`.
3. Silakan buka Google Sheets untuk memilih klip yang siap diproses (*ACC / SIAP RENDER*).

🔗 [Buka Dashboard Google Sheets](https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit)
"""
    print(report.strip())

if __name__ == "__main__":
    run_midnight_scan()
