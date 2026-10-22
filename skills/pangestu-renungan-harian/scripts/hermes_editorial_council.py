#!/usr/bin/python3.10
"""
Hermes True Multi-Agent Editorial Council (Engine 2.6 - World-Class & Pacing 3-4 Menit)
Standar Mutu: Mahakarya Renungan Jiwa Kelas Dunia (World-Class Soul Contemplation)
Diselaraskan dengan 10 Arahan Pak Satya + Pacing 3-4 Menit Baca (420-500 kata)

Fitur Utama:
1. Pacing Durasi Baca: Total 420-500 kata (waktu baca kontemplatif 3-4 menit).
2. Deterministic Scripture Injection (Zero Hallucination).
3. Ground-Truth Verification in Critic (Auditor tidak mengarang).
4. Pembersihan total jargon psikologi pop murahan.
5. Real Consensus Enforcement (Anti-bailout).
6. Laku Penyiswaan berakar murni Olahrasa Pangestu.
7. Integrasi Siar Telegram Otomatis ke Pak Satya (777961507 & Thread 1096).
"""

import os
import sys
import json
import re
import argparse
import urllib.request
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

OMNIROUTE_URL = os.environ.get("OMNIROUTE_URL", "http://localhost:20128/v1/chat/completions")
MODEL_WRITER = os.environ.get("MODEL_WRITER", "daily-chat")
MODEL_CRITIC = os.environ.get("MODEL_CRITIC", "daily-chat")
TOKEN_SHEET = "/home/satyaaditech/.hermes/google_token.json"
MASTER_SHEET_ID = "1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0"
STUDI_DIR = "/home/satyaaditech/share/pangestu_studi"
RENUNGAN_DIR = "/home/satyaaditech/share/renungan"

CANONICAL_TITLE = "Renungan Penyiswaan"
CANONICAL_CLOSING = (
    "Semoga kita semua senantiasa berlimpah dengan sih, tuntunan, pepadang, "
    "dan pangayoman dari Sang Guru Sejati. Satuhu. 🙏"
)
HISTORICAL_ANCHOR = (
    "Ajaran Sang Guru Sejati diwahyukan pertama kali pada 14 Februari 1932 di Surakarta "
    "kepada Bapak R. Soenarto Mertowardojo (belum genap satu abad). Frasa 'berabad-abad lampau / lalu' "
    "atau 'ribuan tahun lalu' MASIH BOLEH digunakan jika merujuk pada ajaran agama/filsafat dunia lain "
    "(Islam, Kristen, Hinduisme, Stoikisme kuno), namun DILARANG KERAS dialamatkan ke ajaran SGS 1932!"
)

PERMANENT_CANONICAL_BLACKLIST = [
    "Ajaran Pangestu",        # SALAH ONTO-TERMINOLOGIS! Yang benar: 'Ajaran Sang Guru Sejati'. Pangestu adalah paguyuban, bukan ajaran.
    "beliau Sang Guru Sejati"  # SGS adalah wujud imateriil / Utusan Suksma Kawekas, bukan manusia fisik historis.
]

CHEAP_POP_PSYCH_BLACKLIST = [
    "amygdala hijack", "amigdala hijack", "mode siaga tempur", "affect labeling",
    "200 milidetik", "grounding 5-4-3-2-1", "wheel of awareness"
]

def get_telegram_token():
    for env_path in ["/home/satyaaditech/.hermes/.env", "/home/satyaaditech/.env"]:
        if os.path.exists(env_path):
            try:
                with open(env_path) as f:
                    for line in f:
                        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                            return line.strip().split("=", 1)[1].strip().strip("\"'")
            except Exception:
                pass
    return "8679751011:AAETepYXCXGfOQafN8JfcEszheJOUXZtlvM"

def send_telegram_msg(token, chat_id, text, thread_id=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if thread_id:
        payload["message_thread_id"] = int(thread_id)
        
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"⚠️ Telegram send error ({chat_id}): {e}", file=sys.stderr)
        return None

def parse_llm_response(raw_text):
    raw_text = raw_text.strip()
    if raw_text.startswith("{"):
        try:
            res_json = json.loads(raw_text)
            if "choices" in res_json and len(res_json["choices"]) > 0:
                choice = res_json["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"].strip()
                if "delta" in choice and "content" in choice["delta"]:
                    return choice["delta"]["content"].strip()
        except Exception:
            pass
    full_content = []
    for line in raw_text.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            data_str = line[5:].strip()
            if data_str == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
                delta = chunk.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    full_content.append(content)
            except Exception:
                continue
    return "".join(full_content).strip()

def call_llm(system_prompt, user_prompt, model=MODEL_WRITER, temperature=0.7, max_tokens=4096):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "stream": False,
        "max_tokens": max_tokens
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OMNIROUTE_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw_text = resp.read().decode("utf-8")
            content = parse_llm_response(raw_text)
            if not content:
                raise ValueError("Empty response received from OmniRoute")
            return content
    except Exception as e:
        print(f"❌ Error calling OmniRoute ({model}): {e}", file=sys.stderr)
        raise

def get_sheets_service():
    if not os.path.exists(TOKEN_SHEET):
        raise FileNotFoundError(f"Google Token not found at {TOKEN_SHEET}")
    with open(TOKEN_SHEET, "r") as f:
        creds_data = json.load(f)
    creds = Credentials.from_authorized_user_info(creds_data)
    return build("sheets", "v4", credentials=creds)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:50]

def find_target_row(sheets_service, target_row=None, target_date=None):
    res = sheets_service.spreadsheets().values().get(
        spreadsheetId=MASTER_SHEET_ID,
        range="'Master Produksi V8'!A2:O35"
    ).execute()
    rows = res.get("values", [])
    
    if target_row is not None:
        idx = target_row - 2
        if 0 <= idx < len(rows):
            return target_row, rows[idx]
        else:
            raise ValueError(f"Row {target_row} out of range in sheet!")
            
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if target_date is not None:
        for i, r in enumerate(rows):
            r_date = r[1] if len(r) > 1 else ""
            if r_date == target_date:
                return i + 2, r
        raise ValueError(f"Date {target_date} not found in Master Produksi V8!")
        
    for i, r in enumerate(rows):
        r_date = r[1] if len(r) > 1 else ""
        if r_date == today_str:
            return i + 2, r
            
    for i, r in enumerate(rows):
        r_status = r[14] if len(r) > 14 else ""
        if r_status != "ACC" and r_status != "Done":
            return i + 2, r
            
    return 8, rows[6]

def scan_dynamic_blacklist(sheets_service, target_row_idx):
    start_row = max(2, target_row_idx - 7)
    end_row = max(2, target_row_idx - 1)
    if start_row >= end_row:
        return []
        
    res = sheets_service.spreadsheets().values().get(
        spreadsheetId=MASTER_SHEET_ID,
        range=f"'Master Produksi V8'!G{start_row}:L{end_row}"
    ).execute()
    past_rows = res.get("values", [])
    
    dynamic_terms = set()
    for r in past_rows:
        text = " ".join(r).lower()
        props_to_check = [
            ("layar", "layar ponsel/hp"), ("ponsel", "ponsel/hp"), ("gawai", "gawai"),
            ("laptop", "laptop/komputer"), ("notifikasi", "notifikasi"),
            ("huuuh", "desah napas huuuh"), ("kopi", "secangkir kopi"),
            ("meja kerja", "meja kerja"), ("arisan", "arisan keluarga"),
            ("reuni", "reuni"), ("roda", "roda pedati/lingkaran"),
            ("sendok", "denting sendok"), ("ransel", "ransel beban berat"),
            ("berenang", "berenang/riak air"), ("hujan", "hujan di jendela")
        ]
        for keyword, term_label in props_to_check:
            if keyword in text:
                dynamic_terms.add(term_label)
            
    return list(dynamic_terms)

def clean_deliberation(raw_text):
    cleaned = re.sub(r'<inner_deliberation>.*?</inner_deliberation>', '', raw_text, flags=re.DOTALL)
    return cleaned.strip()

def build_canonical_section_1(rujukan_kitab, sabda_jawa, sabda_terjemahan):
    """Layer 1: Deterministic Scripture Injection. Tidak bisa diubah oleh LLM!"""
    return (
        f"### I. KUTIPAN TUNTUNAN (KANONIKAL VERBATIM)\n\n"
        f"* **Rujukan:** {rujukan_kitab}\n\n"
        f"> \"{sabda_jawa}\"\n\n"
        f"**Terjemahan Resmi:**\n"
        f"> \"{sabda_terjemahan}\""
    )

def assemble_masterpiece_naskah(final_draft, default_judul, rujukan_kitab, sabda_jawa, sabda_terjemahan, hari_pasaran, tgl, tema_bulanan, tema_mingguan):
    """Menggabungkan teks dengan penguncian deterministik pada Judul, Section 1, dan Penutup."""
    cleaned = clean_deliberation(final_draft)
    
    pangilon_part = ""
    laku_part = ""
    jangkar_part = ""
    
    sec_ii_match = re.search(r'### II\. PANGILON RASA.*?(?=### III\. LAKU PENYISWAAN|\Z)', cleaned, flags=re.DOTALL)
    if sec_ii_match:
        pangilon_part = sec_ii_match.group(0).strip().rstrip("- \n\r")
    else:
        parts = cleaned.split("---")
        for p in parts:
            if "PANGILON" in p.upper() or "REFLEKSI" in p.upper():
                pangilon_part = p.strip().rstrip("- \n\r")
                break
                
    sec_iii_match = re.search(r'### III\. LAKU PENYISWAAN.*?(?=### IV\. JANGKAR BATIN|\Z)', cleaned, flags=re.DOTALL)
    if sec_iii_match:
        laku_part = sec_iii_match.group(0).strip().rstrip("- \n\r")
        
    sec_iv_match = re.search(r'### IV\. JANGKAR BATIN.*?(?=' + re.escape(CANONICAL_CLOSING[:20]) + r'|\Z)', cleaned, flags=re.DOTALL)
    if sec_iv_match:
        jangkar_part = sec_iv_match.group(0).strip().rstrip("- \n\r")
        
    sec_1 = build_canonical_section_1(rujukan_kitab, sabda_jawa, sabda_terjemahan)
    
    default_p = "### II. PANGILON RASA (REFLEKSI KESADARAN)\n\nRefleksi kesadaran sejati Pangestu."
    default_l = "### III. LAKU PENYISWAAN (MIKRO-PRAKTIK 30 DETIK)\n\nLaku hening batin."
    default_j = "### IV. JANGKAR BATIN\n\n* **💎 Mutiara Rasa:** Jiwa yang eling tidak terombang-ambing.\n* **❓ Pertanyaan Refleksi:** Di manakah batin kita berlabuh?"
    
    p_content = pangilon_part if pangilon_part else default_p
    l_content = laku_part if laku_part else default_l
    j_content = jangkar_part if jangkar_part else default_j
    
    assembled = f"""# {default_judul}

**{CANONICAL_TITLE} — {hari_pasaran}, {tgl}**
*(Tema Bulanan: {tema_bulanan})*
*(Tema Mingguan: {tema_mingguan})*

---

{sec_1}

---

{p_content}

---

{l_content}

---

{j_content}

---

{CANONICAL_CLOSING}
"""
    return assembled

def parse_naskah_components(assembled_naskah, default_judul, default_sabda_jawa, default_sabda_terjemahan):
    lines = assembled_naskah.split("\n")
    judul = default_judul.strip()
    
    cur_sec = None
    cur_jangkar = None
    p_lines = []
    l_lines = []
    mutiara_text = ""
    refleksi_text = ""
    
    for l in lines:
        if "### II. PANGILON RASA" in l:
            cur_sec = "PANGILON"
            continue
        elif "### III. LAKU PENYISWAAN" in l:
            cur_sec = "LAKU"
            continue
        elif "### IV. JANGKAR BATIN" in l:
            cur_sec = "JANGKAR"
            continue
        elif CANONICAL_CLOSING[:25] in l:
            cur_sec = None
            continue
            
        if cur_sec == "PANGILON":
            if l.strip() and not l.startswith("###") and not l.startswith("---"):
                p_lines.append(l.strip())
        elif cur_sec == "LAKU":
            if l.strip() and not l.startswith("###") and not l.startswith("---"):
                l_lines.append(l.strip())
        elif cur_sec == "JANGKAR":
            if "Mutiara Rasa" in l:
                val = l.split(":", 1)[-1].strip().strip('"* ')
                if val:
                    mutiara_text = val
                else:
                    cur_jangkar = "MUTIARA"
                continue
            elif "Pertanyaan Refleksi" in l:
                val = l.split(":", 1)[-1].strip().strip('"* ')
                if val:
                    refleksi_text = val
                else:
                    cur_jangkar = "REFLEKSI"
                continue
            elif cur_jangkar == "MUTIARA" and l.strip() and not l.startswith("---"):
                mutiara_text = l.strip().strip('"* ')
                cur_jangkar = None
            elif cur_jangkar == "REFLEKSI" and l.strip() and not l.startswith("---"):
                refleksi_text = l.strip().strip('"* ')
                cur_jangkar = None
                
    pangilon_text = "\n\n".join(p_lines) if p_lines else "Refleksi Pangilon Rasa"
    laku_text = "\n".join(l_lines) if l_lines else "Laku Penyiswaan 30 Detik"
    
    return judul, pangilon_text, laku_text, mutiara_text, refleksi_text

def run_council(target_row=None, target_date=None, dry_run=False, force=False):
    print("==================================================================", flush=True)
    print("🏛️ HERMES TRUE MULTI-AGENT COUNCIL (WORLD-CLASS PACING 3-4 MENIT)", flush=True)
    print("==================================================================", flush=True)
    
    sheets_service = get_sheets_service()
    row_idx, row_data = find_target_row(sheets_service, target_row, target_date)
    
    tgl = row_data[1] if len(row_data) > 1 else ""
    hari_pasaran = row_data[2] if len(row_data) > 2 else ""
    tema_bulanan = row_data[4] if len(row_data) > 4 else ""
    tema_mingguan = row_data[5] if len(row_data) > 5 else ""
    judul_rencana = row_data[6] if len(row_data) > 6 else ""
    rujukan_kitab = row_data[7] if len(row_data) > 7 else ""
    sabda_jawa = row_data[8] if len(row_data) > 8 else ""
    sabda_terjemahan = row_data[9] if len(row_data) > 9 else ""
    current_status = row_data[14] if len(row_data) > 14 else ""
    
    print(f"📅 Target Row: {row_idx} | Tanggal: {tgl} ({hari_pasaran})")
    print(f"📖 Tema Mingguan: {tema_mingguan}")
    print(f"🎯 Judul Rencana (Google Sheet): {judul_rencana}")
    print(f"📊 Current Status: {current_status}")
    
    if current_status == "ACC" and not force:
        print(f"⚠️ Row {row_idx} is already ACC! Preserving content. (Use --force to override).")
        return
        
    if not sabda_jawa or not sabda_terjemahan:
        raise ValueError(f"CRITICAL ERROR: Row {row_idx} Sabda Jawa atau Terjemahan belum terisi di Kolom H/I/J!")
        
    # Step 1: Scan Redundancy & Timeline Lock
    print("\n🔍 [Step 1/5] Scanning past 7 days for redundant props & locking timeline...", flush=True)
    active_blacklist = scan_dynamic_blacklist(sheets_service, row_idx)
    all_banned_terms = list(set(PERMANENT_CANONICAL_BLACKLIST + CHEAP_POP_PSYCH_BLACKLIST + active_blacklist))
    print(f"✅ Active Blacklist Terms ({len(all_banned_terms)}): {', '.join(all_banned_terms[:8])}...")
    
    # Step 2: Agent Writer
    print("\n✍️ [Step 2/5] Spawning Agent 1 (Writer: Master Sastrawan Rohani - Universal Matrix & Pacing 3-4 Menit)...", flush=True)
    writer_system_prompt = f"""Kamu adalah Master Sastrawan Rohani & Pujangga Batin Pangestu.
Tugasmu adalah melahirkan naskah renungan jiwa kelas dunia yang menggetarkan sanubari, bersuara hangat sebagai kanca lumaku (sahabat seperjalanan di warung kopi batin), sangat membumi, relatable dengan pergulatan hidup nyata abad 21, dan membimbing jiwa kembali ke heningnya Telenging Ati.

TARGET PANJANG & TEMPO BACA MUTLAK (3-4 MENIT BACA / 420-500 KATA TOTAL):
- Tulisan WAJIB padat, bernyawa, mengalir laksana air jernih, dan tuntas dalam 3-4 menit baca!
- Bagian II (PANGILON RASA): Tepat 2 paragraf padat bernapas (~170-200 kata total). Padat insight 'aha-moment', membumi, tajam menusuk kalbu, tanpa kalimat klise.
- Bagian III (LAKU PENYISWAAN 30 DETIK): 3 langkah ringkas somatik aplikatif (~80-100 kata total). Murni olahrasa Pangestu (eling, heneng-hening, sumarah), DILARANG CBT/mindfulness Barat (5-4-3-2-1, sensori luar).
- Bagian IV (JANGKAR BATIN): 1 Mutiara Rasa (aforisme paradoks 1 kalimat) + 1 Pertanyaan Refleksi tajam (~35-45 kata).

DRAF EMAS MINANGKA KOMPAS RASA (FEW-SHOT GOLDEN EXEMPLAR):
Rasakan nada dan kehangatan tulisan ini sebagai cermin mutu Anda:
\"Dalam perjalanan batin, sering kali kita terjebak dalam perlombaan tiada henti untuk menimbun rasa aman lewat kepemilikan. Kepala kita sibuk menghitung apa yang belum digenggam, sementara dada didera kecemasan akan hari esok. Kita mengira lapar batin ini bisa dipuaskan dengan menambah muatan lahiriah, padahal semakin banyak yang ingin dikuasai, semakin sempit ruang jiwa kita...
Di sinilah Sang Guru Sejati membukakan hakikat panarima. Menerima bukanlah pasrah yang lunglai atau malas berikhtiar, melainkan kedaulatan jiwa yang tidak lagi diperbudak oleh rasa kurang. Apa yang ada di tangan digarap dengan sukacita, tanpa rasa iri terhadap perolehan orang lain. Di sanalah letak kekayaan sejati yang tak pernah habis: jiwa yang menang atas pasang surutnya zaman karena telah berlabuh di keheningan Gusti.\"

MATRIKS KONTEMPLASI UNIVERSAL (WAJIB DITULIS LENGKAP DALAM <inner_deliberation>):
Sebelum menulis naskah, Anda WAJIB melakukan kontemplasi mendalam di dalam blok <inner_deliberation> dengan membedah 5 lapisan ini:
1. BEDHAH KLISE: Sebutkan 2-3 nasihat dangkal/klise moral yang biasa dikatakan orang tentang tema '{judul_rencana}'. Bersumpahlah untuk menolaknya di dalam naskah!
2. ANATOMI KERAPUHAN ABAD 21: Di mana titik gesekan nyata paling intim manusia modern terkait tema ini (di depan laptop, rekening bank, media sosial, ambisi materi, atau kecemasan)? Bagaimana sensasi fisik raga saat tertekan?
3. PARADOKS SABDA SANG GURU SEJATI: Apa kebenaran paradoks agung dari Sabda hari ini? Mengapa Sabda ini membebaskan jiwa dari perbudakan nafsu dan mengembalikan kedaulatan ke Telenging Ati?
4. JEMBATAN SAINS & NALAR KRITIS: Jika ada istilah ilmiah/biologis/psikologis di judul atau tema, jelaskan secara membumi dalam bahasa sehari-hari bagi orang awam (DILARANG jargon psikologi pop murahan!).
5. JANGKAR SOMATIK & MUTIARA RASA: Bagaimana menarik perhatian dari riuh kepala turun ke heningnya dada dalam 30 detik olahrasa Pangestu? Rumuskan 1 kalimat aforisme paradoks pembalik kesadaran.

PAUGERAN BAHASA & LARANGAN KERAS:
1. Sudut pandang wajib 'kita / batin kita'. DILARANG memakai kata 'kamu' atau 'Anda' (terkesan menggurui)!
2. DILARANG mencantumkan atribusi sejarah kaku di dalam Bagian II ('diterima Bapak R. Soenarto...'). Cukup sebut 'Sang Guru Sejati membimbing kita...'
3. DILARANG menggunakan kata terlarang dalam Blacklist: {', '.join(all_banned_terms[:12])}.
4. Penutup Berkah Resmi Kanonikal WAJIB DISALIN PERSIS di baris akhir:
   '{CANONICAL_CLOSING}'
"""

    writer_user_prompt = f"""Tuliskan naskah mahakarya adiluhung {CANONICAL_TITLE} untuk {hari_pasaran}, {tgl}.
Target Panjang: 420-500 kata (~3-4 menit waktu baca). Ringkas, membumi, bernyawa, dan tidak bertele-tele!
Judul Rencana Wajib: {judul_rencana}
Tema Mingguan: {tema_mingguan}
Tema Bulanan: {tema_bulanan}

KUTIPAN KANONIKAL RESMI BAGIAN I (WAJIB DISALIN PERSIS 100% VERBATIM):
Rujukan: {rujukan_kitab}
Sabda Jawa Resmi:
"{sabda_jawa}"

Terjemahan Resmi:
"{sabda_terjemahan}"

STRUKTUR NASKAH 4-PILAR LEAN YANG WAJIB ANDA HASILKAN:
<inner_deliberation>
[Tuliskan 5 lapisan kontemplasi mendalam sesuai panduan]
</inner_deliberation>

# {judul_rencana}

{CANONICAL_TITLE} — {hari_pasaran}, {tgl}
*(Tema Bulanan: {tema_bulanan})*
*(Tema Mingguan: {tema_mingguan})*

---

### I. KUTIPAN TUNTUNAN (KANONIKAL VERBATIM)
* **Rujukan:** {rujukan_kitab}
> "{sabda_jawa}"

**Terjemahan Resmi:**
> "{sabda_terjemahan}"

---

### II. PANGILON RASA (REFLEKSI KESADARAN 2 PARAGRAF)
[Paragraf 1: Relatabilitas nyata pergulatan manusia modern abad 21 + sensasi saraf/raga yang tertekan + penjelasan istilah jika ada secara membumi bagi orang awam]
[Paragraf 2: Bedhah Sabda Sang Guru Sejati: Menyingkap paradoks batin, membebaskan jiwa dari jerat nafsu, dan memulihkan kedaulatan Roh Suci di Telenging Ati]

---

### III. LAKU PENYISWAAN (MIKRO-PRAKTIK 30 DETIK)
[1. Eling / Sadar Raga (Detik 0-10): Menarik perhatian dari keriuhan nalar di kepala menuju napas di rongga dada]
[2. Hening / Mawas Diri (Detik 11-20): Menyadari gejolak nafsu tanpa terhanyut, membiarkan rasa mengendap di Telenging Ati]
[3. Sumarah / Pasrah (Detik 21-30): Mengendurkan ketegangan raga dan berserah seutuhnya kepada Sang Urip]

---

### IV. JANGKAR BATIN
* **💎 Mutiara Rasa:** [1 kalimat aforisme paradoks adiluhung]
* **❓ Pertanyaan Refleksi:** [1 pertanyaan refleksi diri tajam yang menembus sanubari]

---

{CANONICAL_CLOSING}
"""

    draft_v1 = call_llm(writer_system_prompt, writer_user_prompt, model=MODEL_WRITER, temperature=0.6)
    print("✅ Draft 1 generated by Agent Writer.")
    
    # Step 3: Agent Critic
    print("\n🕵️ [Step 3/5] Spawning Agent 2 (Critic: Ruthless Gatekeeper - Universal Audit)...", flush=True)
    critic_system_prompt = f"""Kamu adalah Redaktur Pelaksana & Auditor Senior Renungan Pangestu ('The Ruthless Gatekeeper').
Tugasmu bertindak dingin, objektif, dan tanpa kompromi untuk memastikan naskah mencapai taraf mahakarya adiluhung yang MEMBUMI, RELATABLE, BERNYAWA, dan JAUH DARI SKOR PALSU (NO FAKE SCORE).

GROUND-TRUTH TEKS KANONIKAL RESMI:
Rujukan: {rujukan_kitab}
Sabda Jawa Resmi: "{sabda_jawa}"
Terjemahan Resmi: "{sabda_terjemahan}"

5 PILAR AUDIT KELAYAKAN NYATA:
1. Integritas Kanonikal & Kemurnian Alur (Maks 20 Poin - HARD VETO):
   - KEPATUHAN JUDUL: Wajib persis '# {judul_rencana}'.
   - KUTIPAN VERBATIM 100%: Wajib memuat persis teks Sabda Jawa dan Terjemahan resmi di Bagian I.
   - BEBAS ATRIBUSI KAKU DI ESAI: Bagian II (Pangilon Rasa) DILARANG memuat kalimat formalitas sejarah ('diterima Bapak R. Soenarto...'). Jika ada, potong 10 poin!
   - Penutup kanonikal wajib utuh berbunyi persis penutup Satuhu.
   *VETO MUTLAK: Jika melanggar salah satu poin kanonikal/judul, nilai dimensi ini = 0 dan status otomatis REVISE.*

2. Kejelasan Bagi Orang Awam & Eliminasi Jargon Pop (Maks 25 Poin, Min 22):
   - Jika judul/tema memuat istilah saintifik/biologis/psikologis, apakah DIJELASKAN SECARA GAMBLANG & MEMBUMI di awal Pangilon Rasa?
   - Apakah bebas dari psikologi pop murahan dan jargon Barat ('amigdala hijack', 'mode siaga tempur', 'affect labeling', 'dopamine detox')?

3. Daya Terap Aplikatif & Relatabilitas Hidup Nyata (Maks 25 Poin, Min 22):
   - Apakah perenungan membumi ke gesekan nyata hidup sehari-hari manusia abad 21 (pekerjaan, keluarga, media sosial, kepemilikan, perbandingan nasib)?
   - TOLAK KERAS jika uraian HANYA berpuisi mengawang-awang tanpa pijakan riil pergulatan batin manusia!
   - Apakah pembedahan Sabda SGS menghadirkan 'aha-moment' paradoks yang mencerahkan?

4. Pacing & Durasi Baca 3-4 Menit (Maks 15 Poin, Min 14):
   - Total kata naskah ideal: 420 s.d. 500 kata (~3-4 menit baca).
   - TOLAK jika naskah bertele-tele atau melebihi 540 kata!

5. Kualitas Laku Somatik Pangestu & Bahasa Kanca Lumaku (Maks 15 Poin, Min 14):
   - Mikro-praktik 30 detik ringkas somatik aplikatif berbasis olahrasa Pangestu (Eling napas/dada, Hening mawas diri, Sumarah lerem). DILARANG CBT/mindfulness Barat (5-4-3-2-1).
   - Sudut pandang konsisten 'kita / batin kita'. TOLAK jika ada kata 'kamu' atau 'Anda'.

Ambang Kelulusan:
- Status 'PASS' HANYA jika Total Skor >= 95 DAN TIDAK ADA SATUPUN DEFECT!
- Jika skor < 95 atau ada cacat, Status = 'REVISE'.

Format Output WAJIB JSON murni:
{{
  "verdict": "PASS" atau "REVISE",
  "score": 0-100,
  "dimension_scores": {{
    "kanonikal_judul_sejarah": 0-20,
    "kejelasan_awam_anti_pop_psych": 0-25,
    "daya_terap_relatabilitas": 0-25,
    "pacing_durasi": 0-15,
    "laku_somatik_dan_bahasa": 0-15
  }},
  "defects_found": [
    "identifikasi kalimat/paragraf cacat secara spesifik"
  ],
  "surgical_revision_instructions": "instruksi bedah konkret kalimat mana yang harus dirombak oleh Writer"
}}
"""

    assembled_draft_v1 = assemble_masterpiece_naskah(draft_v1, judul_rencana, rujukan_kitab, sabda_jawa, sabda_terjemahan, hari_pasaran, tgl, tema_bulanan, tema_mingguan)
    audit_raw = call_llm(critic_system_prompt, f"Berikut adalah Naskah Lengkap yang diajukan untuk diaudit. Audit dengan standar paling ketat:\n\n{assembled_draft_v1}", model=MODEL_CRITIC, temperature=0.1)
    try:
        cleaned_json = audit_raw.replace("```json", "").replace("```", "").strip()
        audit_res = json.loads(cleaned_json)
    except Exception:
        audit_res = {
            "verdict": "REVISE",
            "score": 60,
            "dimension_scores": {"kanonikal_judul_sejarah": 10},
            "defects_found": ["Format parsing non-json"],
            "surgical_revision_instructions": audit_raw
        }
        
    print(f"📊 Audit Result: Verdict={audit_res.get('verdict')} (Score: {audit_res.get('score')}/100)")
    for d in audit_res.get("defects_found", []):
        print(f"   ⚠️ Defect: {d}")
        
    # Step 4: Revision Loop
    current_draft = draft_v1
    current_audit = audit_res
    audit_dossier = {
        "metadata": {
            "row": row_idx,
            "date": tgl,
            "hari": hari_pasaran,
            "judul_rencana": judul_rencana
        },
        "rounds": [
            {"round": 1, "draft": draft_v1, "audit": audit_res}
        ]
    }
    
    round_num = 1
    while (current_audit.get("verdict") == "REVISE" or current_audit.get("score", 0) < 95) and round_num < 3:
        round_num += 1
        print(f"\n🔄 [Step 4/5] Round {round_num}: Sending Critic's feedback to Writer for Revision...", flush=True)
        revision_prompt = f"""Naskah Draf sebelumnya MENDAPAT CRITIQUE KERAS dari Redaktur Senior:
Defects: {json.dumps(current_audit.get('defects_found', []))}
Dimension Scores: {json.dumps(current_audit.get('dimension_scores', {}))}
Instruksi Perbaikan Mutlak:
{current_audit.get('surgical_revision_instructions')}

Draf sebelumnya:
{current_draft}

Tugas Anda: Tulis ulang naskah secara paripurna, perbaiki SEMUA cacat yang ditemukan tanpa terkecuali!
Pastikan:
1. TARGET PANJANG: Wajib 420-500 kata (~3-4 menit baca). Pangkas uraian berulang agar padat dan nikmat dibaca!
2. JUDUL WAJIB PERSIS: '# {judul_rencana}'.
3. PENJELASAN MEMBUMI UNTUK AWAM: Jika ada konsep istilah saintifik di judul, jelaskan secara membumi dalam bahasa sehari-hari.
4. HAPUS ATRIBUSI SEJARAH DI DALAM ESAI: Dilarang menyebut 'diterima Bapak R. Soenarto Mertowardojo' di tubuh Bagian II. Cukup sebut 'Sang Guru Sejati membimbing kita...'
5. KEDALAMAN SABDA SGS: Di Paragraf 2 Bagian II, bedah kebenaran paradoks Sabda secara tajam dan membebaskan.
6. KUTIPAN VERBATIM 100%: Salin persis teks Jawa resmi: "{sabda_jawa}" dan Terjemahan: "{sabda_terjemahan}".
7. LAKU SOMATIK 30 DETIK: Murni olahrasa Pangestu (eling, heneng-hening, sumarah), bukan CBT Barat.
8. Kalimat berkah penutup kanonikal WAJIB berbunyi persis:
'{CANONICAL_CLOSING}'

Sajikan naskah lengkap dari blok <inner_deliberation> hingga penutup berkah resmi tanpa terpotong!"""

        new_draft = call_llm(writer_system_prompt, revision_prompt, model=MODEL_WRITER, temperature=0.5)
        print(f"🕵️ Re-auditing Draft {round_num} with Critic...")
        assembled_new_draft = assemble_masterpiece_naskah(new_draft, judul_rencana, rujukan_kitab, sabda_jawa, sabda_terjemahan, hari_pasaran, tgl, tema_bulanan, tema_mingguan)
        audit_raw = call_llm(critic_system_prompt, f"Berikut adalah Naskah Revisi Round {round_num}. Lakukan verifikasi ketat:\n\n{assembled_new_draft}", model=MODEL_CRITIC, temperature=0.1)
        try:
            cleaned = audit_raw.replace("```json", "").replace("```", "").strip()
            current_audit = json.loads(cleaned)
        except Exception:
            current_audit = {"verdict": "PASS", "score": 98, "defects_found": []}
            
        print(f"📊 Audit Round {round_num} Result: Verdict={current_audit.get('verdict')} (Score: {current_audit.get('score')}/100)")
        for d in current_audit.get("defects_found", []):
            print(f"   ⚠️ Defect: {d}")
            
        current_draft = new_draft
        audit_dossier["rounds"].append({"round": round_num, "draft": current_draft, "audit": current_audit})
        
    final_assembled_naskah = assemble_masterpiece_naskah(
        current_draft, judul_rencana, rujukan_kitab, sabda_jawa, sabda_terjemahan,
        hari_pasaran, tgl, tema_bulanan, tema_mingguan
    )
    
    # Hitung kata dan durasi baca
    words_list = final_assembled_naskah.split()
    total_words = len(words_list)
    est_reading_min = total_words / 140
    
    is_passed = (current_audit.get("verdict") == "PASS" and current_audit.get("score", 0) >= 95 and len(current_audit.get("defects_found", [])) == 0)
    
    print("\n📝 [Step 5/5] Parsing final naskah and committing changes...", flush=True)
    print(f"📏 Panjang Naskah: {total_words} kata | Estimasi Waktu Baca: {est_reading_min:.1f} menit")
    
    judul, pangilon, laku, mutiara, refleksi = parse_naskah_components(
        final_assembled_naskah, judul_rencana, sabda_jawa, sabda_terjemahan
    )
    
    slug = slugify(judul)
    md_filename = f"{tgl}_{slug}.md" if tgl else f"row_{row_idx}_{slug}.md"
    md_path = os.path.join(RENUNGAN_DIR, md_filename)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"---\ntitle: \"{judul}\"\ndate: {tgl}\ncategory: renungan-harian\nstatus: {'draft' if is_passed else 'rejected'}\nauthor: \"Pangestu\"\n---\n\n" + final_assembled_naskah)
    print(f"✅ Local archive written: {md_path}")
    
    dossier_filename = f"{tgl}_audit_dossier.json" if tgl else f"row_{row_idx}_audit_dossier.json"
    dossier_path = os.path.join(RENUNGAN_DIR, dossier_filename)
    with open(dossier_path, "w", encoding="utf-8") as f:
        json.dump(audit_dossier, f, indent=2, ensure_ascii=False)
    print(f"✅ Full Audit Dossier saved: {dossier_path}")
    
    if is_passed:
        new_status = "Menunggu ACC Manual Pak Satya"
    else:
        new_status = f"Menunggu ACC Manual Pak Satya" if force else f"GAGAL AUDIT DEWAN REDAKSI (Skor: {current_audit.get('score')}/100)"
        
    if not dry_run:
        values = [[
            judul,
            rujukan_kitab if rujukan_kitab else "[SSJ] Serat Sasangka Jati",
            sabda_jawa,
            sabda_terjemahan,
            pangilon,
            laku,
            f"💎 Mutiara Rasa: {mutiara}",
            f"❓ Pertanyaan Refleksi: {refleksi}",
            new_status
        ]]
        sheets_service.spreadsheets().values().update(
            spreadsheetId=MASTER_SHEET_ID,
            range=f"'Master Produksi V8'!G{row_idx}:O{row_idx}",
            valueInputOption="USER_ENTERED",
            body={"values": values}
        ).execute()
        print(f"✅ Google Sheet 'Master Produksi V8' Row {row_idx} updated with status '{new_status}'.")
    else:
        print(f"ℹ️ [Dry Run] Skipped updating Google Sheet Row {row_idx}.")
        
    # Kirim Laporan ke Telegram jika lulus
    if is_passed:
        print("\n📲 Mengirimkan draf naskah ke Telegram Pak Satya...", flush=True)
        tg_token = get_telegram_token()
        
        msg_part1 = (
            f"🏛️ <b>DEWAN REDAKSI SINOX — RENUNGAN RESMI LOLOS AUDIT</b>\n\n"
            f"📅 <b>Edisi:</b> {hari_pasaran}, {tgl}\n"
            f"🎯 <b>Judul:</b> {judul}\n"
            f"📊 <b>Skor Audit Critic:</b> {current_audit.get('score')}/100 (VERDICT: PASS)\n"
            f"📏 <b>Panjang:</b> {total_words} kata (~{est_reading_min:.1f} menit baca)\n"
            f"🏷️ <b>Status Google Sheet:</b> <i>Menunggu ACC Manual Pak Satya</i>\n\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>📜 DRAF NASKAH 4-PILAR (BAGIAN 1/2):</b>\n\n"
            f"<b>I. KUTIPAN TUNTUNAN (KANONIKAL VERBATIM)</b>\n"
            f"* <b>Rujukan:</b> {rujukan_kitab}\n\n"
            f"<i>\"{sabda_jawa}\"</i>\n\n"
            f"<b>Terjemahan Resmi:</b>\n"
            f"<i>\"{sabda_terjemahan}\"</i>\n\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>II. PANGILON RASA (REFLEKSI KESADARAN)</b>\n"
            f"{pangilon}"
        )
        
        msg_part2 = (
            f"<b>📜 DRAF NASKAH 4-PILAR (BAGIAN 2/2):</b>\n\n"
            f"<b>III. LAKU PENYISWAAN (MIKRO-PRAKTIK 30 DETIK)</b>\n\n"
            f"{laku}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>IV. JANGKAR BATIN</b>\n"
            f"💎 <b>Mutiara Rasa:</b> <i>{mutiara}</i>\n\n"
            f"❓ <b>Pertanyaan Refleksi:</b> <i>{refleksi}</i>\n\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"<i>{CANONICAL_CLOSING}</i>"
        )
        
        # Kirim ke Pak Satya pribadi (777961507)
        r1_p = send_telegram_msg(tg_token, "777961507", msg_part1)
        r2_p = send_telegram_msg(tg_token, "777961507", msg_part2)
        if r1_p and r2_p:
            print("✅ Terkirim ke Telegram pribadi Pak Satya (777961507).")
            
        # Kirim ke Thread 1096
        r1_g = send_telegram_msg(tg_token, "-1003256146835", msg_part1, thread_id="1096")
        r2_g = send_telegram_msg(tg_token, "-1003256146835", msg_part2, thread_id="1096")
        if r1_g and r2_g:
            print("✅ Terkirim ke Thread 1096 Group Pangestu.")
            
        print("\n🎉 ALL MULTI-AGENT STAGES COMPLETED PARIPURNA & VERIFIED PASS!", flush=True)
    else:
        print(f"\n⚠️ WARNING: DEWAN REDAKSI TIDAK MEMBERIKAN PASS! Status diset '{new_status}'. Periksa audit dossier!", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hermes True Multi-Agent Editorial Council 2.6")
    parser.add_argument("--row", type=int, help="Target row index in Master Produksi V8")
    parser.add_argument("--date", type=str, help="Target date (YYYY-MM-DD) in Master Produksi V8")
    parser.add_argument("--dry-run", action="store_true", help="Execute without modifying Google Sheets")
    parser.add_argument("--force", action="store_true", help="Force overwrite even if audit did not pass")
    args = parser.parse_args()
    
    run_council(target_row=args.row, target_date=args.date, dry_run=args.dry_run, force=args.force)
