#!/usr/bin/env python3
"""
Hermes Cron Script: Autonomous YouTube Shorts Publisher
Executed at 12:00 WIB and 18:00 WIB.
Delivers a formatted Telegram executive report directly.
"""

import sys
import os
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add lab path
sys.path.append("/home/satyaaditech/youtube_clipper_lab")
from auto_scheduler_publisher import (
    read_pipeline_sheet,
    select_next_clip,
    build_metadata,
    update_sheet_row_status,
    BASE_DIR
)
import youtube_uploader
from datetime import datetime

def run_publisher_cron(slot_title="Slot Siang 12:00 WIB"):
    try:
        pipeline = read_pipeline_sheet()
        if not pipeline:
            print(f"⚠️ *[YouTube Shorts Publisher — {slot_title}]*\n\nGagal maos data saking Google Sheets pipeline. Nyumanggakaken priksa sambungan API.")
            return

        selected, reason, stock_count, last_live_ch = select_next_clip(pipeline)

        if not selected:
            print(f"⚠️ *[YouTube Shorts Publisher — {slot_title}]*\n\nAntrean video kothong! Boten wonten klip kanthi status `SUDAH DIRENDER` utawi `ACC` wonten ing Google Sheets.")
            return

        # Check video file
        clip_id_lower = selected["clip_id"].lower().replace("-", "")
        possible_paths = [
            os.path.join(BASE_DIR, f"shorts_{clip_id_lower}_1080x1920.mp4"),
            os.path.join(BASE_DIR, f"shorts_{selected['clip_id']}.mp4"),
            os.path.join(BASE_DIR, f"shorts_clip004_1080x1920.mp4") if selected["clip_id"] == "CLIP-004" else "",
        ]
        video_path = next((p for p in possible_paths if p and os.path.exists(p)), None)

        if not video_path:
            print(f"⚠️ *[YouTube Shorts Publisher — {slot_title}]*\n\nKlip `{selected['clip_id']}` kapilih nanging berkas video dereng kasil dipun-render wonten ing server.\n\n*Topik:* {selected['draft_title']}\n*Sumber:* {selected['channel']}\n*Katerangan:* Mbetahaken proses render rumiyin.")
            return

        meta = build_metadata(selected)

        # Upload to YouTube
        try:
            res = youtube_uploader.upload_shorts(
                video_path=video_path,
                title=meta["title"],
                description=meta["description"],
                tags=meta["tags"],
                category_id=meta["category_id"],
                privacy=meta["privacy"],
            )
            if isinstance(res, tuple):
                video_id, live_url = res
            elif isinstance(res, dict):
                video_id = res.get("video_id")
                live_url = res.get("url")
            else:
                video_id = str(res)
                live_url = f"https://youtube.com/shorts/{video_id}"

            update_sheet_row_status(selected["row_num"], "SUDAH TAYANG (LIVE)", live_url)

            # Build Telegram report in polite Krama Alus & clear structure
            msg = f"""🎬 **Laporan Publikasi Otomatis YouTube Shorts**
*Jadwal:* {slot_title} | {datetime.now().strftime('%d %B %Y %H:%M WIB')}

Puji syukur, video Shorts sampun kasil kaunggah kanthi otomatis dhateng saluran YouTube **@siswatalkstv**:

* **ID Klip:** `{selected['clip_id']}`
* **Saluran Sumber:** `{selected['channel']}` *(Rotasi Silang Anti-Beruntun: OK)*
* **Irah-irahan:** {selected['draft_title']}
* **Tautan Video Live:** 🔗 [Nonton ing YouTube Shorts]({live_url})

---
📊 **Status Kontrol Pipeline:**
* **Google Sheet:** Status baris {selected['row_num']} sampun kaanyaraken dados `SUDAH TAYANG (LIVE)`.
* **Sisa Buffer Stok:** `{stock_count - 1}` klip cumawis ing antrean.
* **Tautan Master Sheet:** [Bikak Master Pipeline Sheet](https://docs.google.com/spreadsheets/d/1d6Iyj0rZ22_m9CmwJn9XXDoAFqbWoWKKo96Uppsn4Ok/edit)
"""
            if (stock_count - 1) < 4:
                msg += f"\n⚠️ *Pènget Stok:* Sisa stok video siap tayang kantun {stock_count - 1} klip. Sistem badhe otomatis mindai kanal dalu mengko."

            print(msg)
        except Exception as e:
            print(f"❌ *[YouTube Shorts Publisher — {slot_title}]*\n\nGagal ngunggah video `{selected['clip_id']}` dhateng YouTube.\n*Penyebab:* `{str(e)}`")

    except Exception as e:
        print(f"❌ *[YouTube Shorts Publisher — {slot_title}] Error:*\n`{str(e)}`")

if __name__ == "__main__":
    slot = sys.argv[1] if len(sys.argv) > 1 else "Slot Siang (12:00 WIB)"
    run_publisher_cron(slot)
