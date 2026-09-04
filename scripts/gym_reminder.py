#!/usr/bin/env python3
"""
Gym Reminder & Checklist Script for Satya Adi Dharma.
Complete Version: Includes Biomechanics / Cara Pakai, Muscle Targets, Rest Time, Photo Links,
and at the end provides the Direct Online Report URL (no WhatsApp template).
"""

import sys
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = "1NAkd3IOOx_gNDeKPXOHI3gSQSHleW6q8pyDmBubdHVo"
TOKEN_PATH = "/home/satyaaditech/.hermes/google_token.json"

def main():
    now = datetime.datetime.now()
    
    # Target date logic
    target_date_str = now.strftime("%d/%m/%Y")
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        if "/" in arg and len(arg) == 10:
            target_date_str = arg
        elif "sabtu" in arg.lower() or arg == "05":
            target_date_str = "05/09/2026"
        elif "selasa" in arg.lower() or arg == "08":
            target_date_str = "08/09/2026"
        elif "kamis" in arg.lower() or arg == "10":
            target_date_str = "10/09/2026"

    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH)
        sheets = build('sheets', 'v4', credentials=creds)

        # 1. Fetch Month 1 Program (for date & session meta)
        res_m = sheets.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="'Program Bulan 1 (12 Sesi)'!A2:N100"
        ).execute()
        month_rows = res_m.get('values', [])

        # 2. Fetch Master Program (for rich biomechanics & cues)
        res_master = sheets.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="'Program Latihan Master'!A2:J25"
        ).execute()
        master_rows = res_master.get('values', [])

    except Exception as e:
        print(f"Error mengakses Google Sheets: {e}")
        return

    # Filter session by date
    session_rows = [r for r in month_rows if len(r) > 0 and r[0] == target_date_str]

    if not session_rows:
        weekday_name = ["Senen", "Selasa", "Rebo", "Kamis", "Jemuwah", "Setu", "Minggu"][now.weekday()]
        print(f"Dinten punika ({weekday_name}, {target_date_str}) boten wonten jadwal gladhen gym ing Google Sheets.")
        return

    first_row = session_rows[0]
    date_val = first_row[0]
    sesi_id = first_row[1]
    minggu_id = first_row[2]
    day_focus = first_row[3]
    coach_notes = first_row[9] if len(first_row) > 9 else ""

    # Map master cues by exercise name / no_alat
    master_cues = {}
    for mr in master_rows:
        if len(mr) >= 9:
            # key by tool name or no_alat
            key_name = mr[3].split("(")[0].strip().lower()
            master_cues[key_name] = {
                "nama_lengkap": mr[3],
                "target_otot": mr[4],
                "set": mr[5],
                "reps": mr[6],
                "ngaso": mr[7],
                "pandom": mr[8],
                "img_url": mr[9] if len(mr) > 9 else ""
            }

    msg = []
    msg.append(f"Sugeng enjang, Pak Satya. Dinten punika **{day_focus} ({date_val})**, wancinipun gladhen:")
    msg.append(f"🏋️♂️ **{sesi_id.upper()} — {minggu_id.upper()}**")
    msg.append(f"🎯 **Pandom Coach Sinok**: {coach_notes}")
    msg.append("")
    msg.append("📋 **CEKLIST GERAKAN & CARA PAKAI ALAT GYM:**")
    msg.append("*(Saben piranti dipun-jangkepi link foto Drive sarta pandom biomekanika)*\n")

    for r in session_rows:
        no_u = r[4]
        no_alat = r[5]
        nama_ex = r[6]
        t_set = r[7]
        t_reps = r[8]
        link_img = r[13] if len(r) > 13 else ""

        # Look up cue in master
        key_name = nama_ex.split("(")[0].strip().lower()
        cue = master_cues.get(key_name, {})
        
        if "kardio" in key_name:
            target_otot = "Kardiorespirasi & Pembakaran Gajih (Zone 2 Fat Loss)"
            ngaso = "Kardio Kontinu"
            pandom = "Setel Incline 8 - 10%, kacepetan 4.2 - 4.8 km/jam (utawi sepeda statis RPM 70-80); mlampah ajeg tanpa nyepeng rel supados kalori kaobong maksimal."
        else:
            target_otot = cue.get("target_otot", "Otot Utama")
            ngaso = cue.get("ngaso", "60 dtk")
            pandom = cue.get("pandom", "Jaga postur tegap lan kontrol obahan kanthi alon.")
        if not link_img:
            link_img = cue.get("img_url", "")

        alat_tag = f"(Mesin No. {no_alat})" if str(no_alat) != "-" else "(Kardio Zone)"

        msg.append(f"**{no_u}. {nama_ex}** {alat_tag}")
        if link_img:
            msg.append(f"   📸 [Pirsani Foto Alat ing Drive]({link_img})")
        msg.append(f"   🎯 **Target**: {t_set} x {t_reps} | Ngaso: {ngaso}")
        msg.append(f"   💪 **Fokus Otot**: {target_otot}")
        msg.append(f"   💡 **Cara Pakai & Pandom**: {pandom}")
        msg.append("")

    msg.append("---")
    msg.append("💡 **Pandom Progressive Overload & Kaslametan**:")
    msg.append("• Kunci posisi boyok & sendi kanthi bener sadèrèngipun ngangkat beban.")
    msg.append("• Rekap beban dinten punika supados minggu candhakipun saged dipun-tingkataken bertahap.")
    msg.append("")
    msg.append("📝 **LAPURAN PROGRES BIBAR GLADHEN**:")
    msg.append("Sabibaripun rampung gladhen, sumangga langsung tutul tautan formulir punika kagem nglebetaken asil latihan:")
    msg.append("👉 **[Formulir Rekap Online Coach Sinok](http://100.92.237.45:8085)**")
    msg.append("*(Akses Seluler / Jaba: http://100.92.237.45:8085 | WiFi Griya: http://192.168.0.112:8085)*")
    msg.append("")
    msg.append("Mugi gladhen dinten punika lancar, seger-bagas, lan target salira atletis sansaya celak! 💪🔥")

    print("\n".join(msg))

if __name__ == "__main__":
    main()
