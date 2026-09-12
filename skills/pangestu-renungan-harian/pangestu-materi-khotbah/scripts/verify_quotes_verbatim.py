import re, os, sys

CORPUS_DIR = "/home/satyaaditech/share/pangestu_studi"

def load_corpus():
    files = {
        "SSJ": "buku_ssj_jawa.txt",
        "BRSR": "buku_brsr.txt",
        "SKH": "buku_skh.txt",
        "TKL": "buku_tkl.txt",
        "UUJM": "buku_uujm.txt"
    }
    corpus = {}
    for k, fname in files.items():
        p = os.path.join(CORPUS_DIR, fname)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                corpus[k] = f.read()
    return corpus

def verify_quote(quote_text, corpus_dict, source_hint=""):
    clean_q = re.sub(r'[*_`]', '', quote_text).strip()
    words = re.findall(r'\w+', clean_q)
    if len(words) < 3:
        return False, "Quote too short"
    
    # Try exact match in hints or all corpus
    targets = [source_hint] if source_hint in corpus_dict else list(corpus_dict.keys())
    for t in targets:
        text = corpus_dict[t]
        if clean_q in text:
            return True, f"Exact match in {t}"
        # Try finding key anchor phrases
        sub1 = " ".join(words[:5])
        sub2 = " ".join(words[-5:])
        if sub1 in text or sub2 in text:
            return True, f"Anchor matched in {t}"
            
    return False, "Not found in canonical corpus"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        q = sys.argv[1]
        c = load_corpus()
        ok, msg = verify_quote(q, c)
        print(f"Verification: {ok} -> {msg}")
