import os
import glob
import re
import json

def generate_library():
    renungan_dir = "/home/satyaaditech/share/renungan"
    pustaka_dir = "/home/satyaaditech/share/pustaka"
    os.makedirs(pustaka_dir, exist_ok=True)

    md_files = sorted(glob.glob(os.path.join(renungan_dir, "*.md")), reverse=True)
    articles = []

    def clean_stars(text):
        if not text:
            return ""
        return re.sub(r'^\*+|\*+$', '', text.strip()).strip()

    for fpath in md_files:
        fname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Language detection
        lang = "jv"
        if "-ind-" in fname or "-ind." in fname or ("ind" in fname.lower() and "pindha" not in fname):
            lang = "id"
        elif "-eng-" in fname or "-eng." in fname:
            lang = "en"
        elif "kamardikan-ind" in fname or "mengampuni-ind" in fname:
            lang = "id"
        elif "mengampuni-eng" in fname:
            lang = "en"
        
        if "*SABDA HARI INI" in raw_text or "Salam Bahagia" in raw_text or "*URAIAN" in raw_text:
            lang = "id"
        elif "*DAILY SCRIPTURE" in raw_text or "Greetings of Peace" in raw_text or "*EXPOSITION" in raw_text:
            lang = "en"
        elif "*PETHIKAN DINTEN" in raw_text or "Sugeng Enjang" in raw_text or "*ANDHARAN" in raw_text:
            lang = "jv"

        # Date
        date_match = re.search(r'^\*([A-Z\s,0-9]+)\*', raw_text, re.MULTILINE)
        date_str = date_match.group(1).strip() if date_match else ""
        date_iso = ""
        d_match = re.search(r'(\d{4}-\d{2}-\d{2})', fname)
        if d_match:
            date_iso = d_match.group(1)
        if not date_str:
            date_str = date_iso

        # Title
        title = ""
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        for l in lines[1:5]:
            if "RENUNGAN" not in l and not l.startswith("_Salam") and not l.startswith("_Sugeng") and not l.startswith("_Greetings"):
                title = clean_stars(l)
                break
        if not title:
            title = fname.replace(".md", "").replace("renungan-", "").replace("-", " ").title()

        # Google Doc URL
        gdoc_match = re.search(r'https://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)(?:/edit)?', raw_text)
        gdoc_url = gdoc_match.group(0) if gdoc_match else ""

        # Audio file
        base_no_ext = os.path.splitext(fname)[0]
        audio_file = ""
        for ext in [".ogg", ".mp3"]:
            cand = os.path.join(renungan_dir, base_no_ext + ext)
            if os.path.exists(cand):
                audio_file = f"/renungan/{base_no_ext}{ext}"
                break

        # Poster / Infographic / Cover Image Detection
        poster_file = ""
        stem = fname.replace("renungan-", "").replace(".md", "")
        core_stem = re.sub(r'-(?:ind|eng)$', '', stem)
        
        candidates = [
            f"poster-{core_stem}.jpg", f"poster-{core_stem}.png",
            f"infografis-{core_stem}.png", f"infografis_{core_stem}.png",
            f"cover-{core_stem}.png", f"cover-{stem}.png",
            f"poster-{stem}.jpg", f"poster-{stem}.png",
            f"newsletter-{core_stem}-A4-2026-08-25.png"
        ]
        if date_iso:
            candidates.extend([
                f"poster-teladan-{date_iso}.jpg",
                f"infografis-budi-darma-{date_iso}.png",
                f"cover-sabar-momot-{date_iso}.png",
                f"cover-ngunjara-hawa-napsu-{date_iso}.png",
                f"cover-kamardikan-{date_iso}.png",
                f"cover-sokur-{date_iso}.png",
                f"cover-sumelang-{date_iso}.png"
            ])

        for cand in candidates:
            if os.path.exists(os.path.join(renungan_dir, cand)):
                poster_file = f"/renungan/{cand}"
                break

        # Book source
        book_source = "Sasangka Jati"
        if "BRSR" in raw_text or "Bawa Raos" in raw_text:
            book_source = "Bawa Raos (BRSR)"
        elif "Sabda Khusus" in raw_text or "SKH" in raw_text:
            book_source = "Sabda Khusus (SKH)"
        elif "TKL" in raw_text or "Taman Kamulyan" in raw_text:
            book_source = "Taman Kamulyan (TKL)"
        elif "UUJM" in raw_text or "Ular-Ular" in raw_text:
            book_source = "Ular-Ular (UUJM)"
        elif "Hasta Sila" in raw_text:
            book_source = "Sasangka Jati (Hasta Sila)"
        elif "Tunggal Sabda" in raw_text:
            book_source = "Sasangka Jati (Tunggal Sabda)"
        elif "Panembah" in raw_text:
            book_source = "Sasangka Jati (Panembah)"

        # Excerpt
        sabda_excerpt = ""
        sabda_match = re.search(r'(?:PETHIKAN DINTEN PUNIKA|SABDA HARI INI|DAILY SCRIPTURE)\s*:\s*\n*(.*?)(?=\n\s*(?:Terjemahan|Translation|💭|\*ANDHARAN|\*URAIAN|\*EXPOSITION|$))', raw_text, re.DOTALL | re.IGNORECASE)
        if sabda_match:
            sabda_excerpt = sabda_match.group(1).strip()
            sabda_excerpt = re.sub(r'[*_"]', '', sabda_excerpt)
            sabda_excerpt = (sabda_excerpt[:150] + "...") if len(sabda_excerpt) > 150 else sabda_excerpt

        # Tags
        tags = [book_source.split("(")[0].strip()]
        for kw, tag in [
            ("sabar", "Sabar"), ("rila", "Rila"), ("narima", "Narima"),
            ("pangapura", "Pengampunan"), ("mengampuni", "Pengampunan"), ("pangaksama", "Pengampunan"),
            ("lisan", "Lisan"), ("eling", "Eling"), ("hawa napsu", "Hawa Nafsu"), ("nafsu", "Hawa Nafsu"),
            ("panembah", "Panembah"), ("sukma", "Kasukman"), ("kamardikan", "Kamardikan"),
            ("merdeka", "Kamardikan"), ("beban", "Katentreman"), ("sumelang", "Piandel"),
            ("teladan", "Keteladanan")
        ]:
            if kw in raw_text.lower() and tag not in tags:
                tags.append(tag)

        articles.append({
            "id": fname,
            "filename": fname,
            "title": title,
            "date": date_str,
            "lang": lang,
            "book": book_source,
            "tags": tags[:4],
            "gdoc": gdoc_url,
            "audio": audio_file,
            "poster": poster_file,
            "excerpt": sabda_excerpt,
            "raw": raw_text
        })

    articles_json_str = json.dumps(articles, ensure_ascii=False)
    # Output file write
    print("Catalog parsed", len(articles), "articles.")

if __name__ == "__main__":
    generate_library()
