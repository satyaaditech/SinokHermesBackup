#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert a markdown file into a natively-formatted Google Doc
(no markdown symbols visible). Hardened against Docs API pitfalls:
- Drive-created docs have no paragraph at index 0 -> detect base index.
- updateParagraphStyle/updateTextStyle need explicit 'fields'.

Usage:
  python md_to_doc.py --source file.md --title "Title" --folder <FOLDER_ID> [--doc-id <ID>]
"""
import argparse, json, os, re, sys

TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")

# Matches: **bold**, *italic*, `code`
INLINE = re.compile(r"(\*\*.*?\*\*|\*.*?\*|`.*?`)")

def segs(text):
    """Split text into (content, bold, italic, code) segments."""
    out = []
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            out.append((part[2:-2], True, False, False))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append((part[1:-1], False, True, False))
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            out.append((part[1:-1], False, False, True))
        else:
            out.append((part, False, False, False))
    return out

def parse_blocks(src):
    blocks = []  # (kind, segments, indent)
    in_code = False
    code_lines = []
    
    with open(src, encoding="utf-8") as f:
        for raw in f.read().splitlines():
            line = raw.rstrip()
            
            # Handle start/end of code blocks
            if line.strip().startswith("```"):
                if in_code:
                    # End of code block
                    for cl in code_lines:
                        blocks.append(("code", [(cl, False, False, True)], 0))
                    in_code = False
                    code_lines = []
                else:
                    in_code = True
                continue
                
            if in_code:
                code_lines.append(line)
                continue
                
            if not line.strip():
                blocks.append(("normal", [("", False, False, False)], 0))
                continue
                
            if re.match(r"^---+$", line.strip()):
                blocks.append(("normal", [("―" * 40, False, False, False)], 0))
                continue
                
            if line.startswith("### "):
                blocks.append(("h3", segs(line[4:]), 0))
            elif line.startswith("## "):
                blocks.append(("h2", segs(line[3:]), 0))
            elif line.startswith("# "):
                blocks.append(("h1", segs(line[2:]), 0))
            elif line.startswith(">"):
                blocks.append(("quote", segs(line.lstrip("> ").strip()), 0))
            elif line.strip().startswith("|"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if all(re.match(r"^:?-{2,}:?$", c) for c in cells):
                    continue
                blocks.append(("normal", segs("  ·  ".join(cells)), 0))
            elif line.lstrip().startswith("* "):
                indent = len(line) - len(line.lstrip())
                blocks.append(("bullet", segs(line.strip()[2:].strip()), indent))
            elif line.lstrip().startswith("- "):
                indent = len(line) - len(line.lstrip())
                blocks.append(("bullet", segs(line.strip()[2:].strip()), indent))
            else:
                blocks.append(("normal", segs(line), 0))
                
        if in_code and code_lines:
            for cl in code_lines:
                blocks.append(("code", [(cl, False, False, True)], 0))
                
    return blocks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--folder", required=True)
    ap.add_argument("--doc-id", default=None)
    args = ap.parse_args()

    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    with open(TOKEN_PATH) as f:
        td = json.load(f)
    creds = Credentials(
        token=td["token"],
        refresh_token=td.get("refresh_token"),
        token_uri=td["token_uri"],
        client_id=td["client_id"],
        client_secret=td["client_secret"],
        scopes=td["scopes"],
    )
    drive = build("drive", "v3", credentials=creds)
    docs = build("docs", "v1", credentials=creds)

    blocks = parse_blocks(args.source)

    if args.doc_id:
        doc_id = args.doc_id
        meta = drive.files().get(fileId=doc_id, fields="id,name").execute()
        print("using existing:", doc_id, meta["name"])
        
        # Clear existing document content
        d = docs.documents().get(documentId=doc_id).execute()
        end_index = d["body"]["content"][-1]["endIndex"]
        if end_index > 2:
            docs.documents().batchUpdate(documentId=doc_id, body={
                "requests": [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index - 1}}}]
            }).execute()
    else:
        meta = (drive.files().create(
            body={
                "name": args.title,
                "mimeType": "application/vnd.google-apps.document",
                "parents": [args.folder],
            },
            fields="id,name").execute())
        doc_id = meta["id"]
        print("created:", doc_id, meta["name"])

    # base index: first paragraph startIndex (NOT 0 for Drive-created docs)
    d = docs.documents().get(documentId=doc_id).execute()
    base = None
    for el in d["body"]["content"]:
        if "paragraph" in el:
            base = el["startIndex"]
            break
    if base is None:
        raise RuntimeError("no paragraph found in doc body")
    print("base insert index:", base)

    texts = []
    for kind, seg_list, indent in blocks:
        parts = ["• " if kind == "bullet" else ""]
        for content, b, i, code in seg_list:
            parts.append(content)
        texts.append("".join(parts) + "\n")
    full = "".join(texts)

    reqs = [{"insertText": {"location": {"index": base}, "text": full}}]

    style_map = {
        "h1": "HEADING_1", 
        "h2": "HEADING_2", 
        "h3": "HEADING_3",
        "normal": "NORMAL_TEXT", 
        "quote": "NORMAL_TEXT", 
        "bullet": "NORMAL_TEXT",
        "code": "NORMAL_TEXT"
    }

    pos = 0
    for (kind, seg_list, indent), text in zip(blocks, texts):
        start, end = base + pos, base + pos + len(text)
        
        ps = {"paragraphStyle": {"namedStyleType": style_map[kind]}}
        pfields = "namedStyleType"
        
        if kind == "h1":
            ps["paragraphStyle"]["spaceAbove"] = {"magnitude": 18, "unit": "PT"}
            ps["paragraphStyle"]["spaceBelow"] = {"magnitude": 8, "unit": "PT"}
            ps["paragraphStyle"]["keepWithNext"] = True
            pfields += ",spaceAbove,spaceBelow,keepWithNext"
        elif kind == "h2":
            ps["paragraphStyle"]["spaceAbove"] = {"magnitude": 14, "unit": "PT"}
            ps["paragraphStyle"]["spaceBelow"] = {"magnitude": 6, "unit": "PT"}
            ps["paragraphStyle"]["keepWithNext"] = True
            pfields += ",spaceAbove,spaceBelow,keepWithNext"
        elif kind == "h3":
            ps["paragraphStyle"]["spaceAbove"] = {"magnitude": 10, "unit": "PT"}
            ps["paragraphStyle"]["spaceBelow"] = {"magnitude": 4, "unit": "PT"}
            ps["paragraphStyle"]["keepWithNext"] = True
            pfields += ",spaceAbove,spaceBelow,keepWithNext"
        elif kind == "quote":
            ps["paragraphStyle"]["indentStart"] = {"magnitude": 36, "unit": "PT"}
            ps["paragraphStyle"]["spaceBelow"] = {"magnitude": 6, "unit": "PT"}
            pfields += ",indentStart,spaceBelow"
        elif kind == "bullet":
            indent_pt = 18 + (indent * 9)
            ps["paragraphStyle"]["indentStart"] = {"magnitude": indent_pt, "unit": "PT"}
            ps["paragraphStyle"]["spaceBelow"] = {"magnitude": 3, "unit": "PT"}
            pfields += ",indentStart,spaceBelow"
        elif kind == "code":
            ps["paragraphStyle"]["indentStart"] = {"magnitude": 24, "unit": "PT"}
            ps["paragraphStyle"]["spaceBelow"] = {"magnitude": 0, "unit": "PT"}
            ps["paragraphStyle"]["spaceAbove"] = {"magnitude": 0, "unit": "PT"}
            pfields += ",indentStart,spaceBelow,spaceAbove"
        else:
            if len(seg_list) == 1 and seg_list[0][0] == "":
                ps["paragraphStyle"]["spaceBelow"] = {"magnitude": 3, "unit": "PT"}
            else:
                ps["paragraphStyle"]["spaceBelow"] = {"magnitude": 6, "unit": "PT"}
            pfields += ",spaceBelow"
            
        ps["fields"] = pfields
        reqs.append({"updateParagraphStyle": {"range": {"startIndex": start, "endIndex": end}, **ps}})
        
        off = 2 if kind == "bullet" else 0
        cur = start + off
        for content, b, i, is_code in seg_list:
            if len(content) > 0:
                ts = {"textStyle": {}}
                f = []
                
                if b:
                    ts["textStyle"]["bold"] = True
                    f.append("bold")
                if i or kind == "quote":
                    ts["textStyle"]["italic"] = True
                    f.append("italic")
                if is_code or kind == "code":
                    ts["textStyle"]["weightedFontFamily"] = {"fontFamily": "Consolas"}
                    ts["textStyle"]["fontSize"] = {"magnitude": 9.5, "unit": "PT"}
                    ts["textStyle"]["foregroundColor"] = {
                        "color": {
                            "rgbColor": {
                                "red": 0.2,
                                "green": 0.2,
                                "blue": 0.2
                            }
                        }
                    }
                    f.extend(["weightedFontFamily", "fontSize", "foregroundColor"])
                    
                if f:
                    ts["fields"] = ",".join(f)
                    reqs.append({"updateTextStyle": {"range": {"startIndex": cur, "endIndex": cur + len(content)}, **ts}})
            cur += len(content)
        pos = end - base

    CH = 120
    for i in range(0, len(reqs), CH):
        chunk = reqs[i:i + CH]
        docs.documents().batchUpdate(documentId=doc_id, body={"requests": chunk}).execute()

    try:
        drive.permissions().create(fileId=doc_id, body={"type": "anyone", "role": "writer"}).execute()
        print("shared: anyone with link (writer)")
    except Exception as e:
        print("share skipped:", e)

    print("URL: https://docs.google.com/document/d/%s/edit" % doc_id)

if __name__ == "__main__":
    main()
