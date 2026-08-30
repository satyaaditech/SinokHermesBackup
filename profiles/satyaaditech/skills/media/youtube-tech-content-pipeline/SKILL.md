---
name: youtube-tech-content-pipeline
description: >
  Automated pipeline for generating YouTube video scripts from research to delivery.
  Extracts transcripts from YouTube videos, generates content outlines, and produces
  ready-to-read Indonesian scripts with verified sources and specific benchmark data.
  Use for: tech YouTube channel automation, content pipeline, research-to-script workflow.
triggers:
  - "YouTube automation"
  - "generate script from YouTube video"
  - "content pipeline YouTube"
  - "research to script YouTube"
  - "build YouTube automation pipeline"
---

# YouTube Tech Content Pipeline

Automated pipeline: research → extract transcript → generate sourced Indonesian script.

## Pipeline Steps

### Step 1: Research Topic (ddgs)
```bash
ddgs text -q "GPT-5.5 OpenAI Spud April 2026" -m 10 -t w
```

### Step 2: Extract YouTube Transcript
```bash
/usr/bin/python3 ~/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py "VIDEO_URL" --text-only
```
Requires: `youtube-transcript-api` installed at system Python (`/usr/bin/python3`).

### Step 3: Verify Sources
```bash
# Save HTML, then parse (safe - no pipe to interpreter)
curl -sL "SOURCE_URL" -o /tmp/page.html
python3 -c "
import re
with open('/tmp/page.html') as f:
    text = re.sub(r'<[^>]+>', ' ', f.read())
    print(text[:2000])
"
```

### Step 4: Generate Script (manual compose)
Write fresh Indonesian content using English sources as reference. DO NOT auto-translate word-by-word — it produces garbage output.

## Critical Lessons Learned

### Lesson 1: Auto-translation FAIL
- **What happened**: Tried regex word-replace to translate English→Indonesian
- **Result**: Garbled output like "Adalah able to sayanghassayalkan semua tdia components"
- **Why**: Word-by-word replacement ignores grammar, context, sentence structure
- **Correct approach**: Use English sources as REFERENCE material, write Indonesian fresh

### Lesson 2: Tech audiences expect SPECIFIC DATA
- Generic: "Model ini lebih cepat dan lebih baik"
- Good: "83% pada GDPval benchmark, 75% pada OSWorld-Verified, context window 1.05 juta token"

### Lesson 3: Always cite VERIFIABLE SOURCES
- Include actual URLs in the script
- Distinguish CONFIRMED vs RUMOR/UNCONFIRMED data
- Use official sources when possible (OpenAI blog, Wikipedia)

---

## 🛡️ 7-LAYER ANTI-HALLUCINATION FRAMEWORK

**CRITICAL:** User Satya requires ZERO hallucinations. Every claim must be verifiable.

### Layer 1: Source Verification (Wajib!)
```bash
# SEBELUM pakai data, CURL dulu source-nya
curl -sL "https://openai.com/index/..." -o /tmp/verify.html
# Cek manual apakah data benar-benar ada di halaman
```
**Rule:** Kalau tidak bisa di-CURL dan verifikasi → JANGAN pakai!

### Layer 2: Trusted Sources Only

**✅ ALLOWED (Verified):**
- Official company blogs (openai.com, google.com/ai, anthropic.com)
- Reputable tech news (techcrunch.com, theverge.com, arstechnica.com)
- Wikipedia (dengan citation)
- Official YouTube channels
- GitHub repositories (official)

**❌ BLOCKED:**
- Random blogs tanpa author
- Forum posts (Reddit, Quora) tanpa verification
- Social media tanpa official source
- AI-generated content sites

### Layer 3: Data Citation Format
```
✓ GOOD (Verifiable):
"GPT-5.4 scored 83% on GDPval benchmark"
Source: https://openai.com/index/introducing-gpt-5-4/ (April 2026)

✗ BAD (Hallucination risk):
"Model ini sangat cepat dan akurat"
(Tidak ada angka, tidak ada source)
```

### Layer 4: Confirmed vs Rumor Labeling
```python
# Template wajib di script
if data_type == "confirmed":
    script += f"✅ CONFIRMED: {data} (Source: {url})"
elif data_type == "rumor":
    script += f"⚠️ RUMOR/UNCONFIRMED: {data} (Source: {url})"
    script += "   → Masih perlu verifikasi official"
```

### Layer 5: No Auto-Translation
**PELAJARAN PENTING:** Auto-translate word-by-word menghasilkan output rusak.
```
✗ BAD: "Adalah able to sayanghassayalkan semua tdia components"
✓ GOOD: "Model ini bisa handle semua components dengan efisien"
```
Write fresh Indonesian using English as REFERENCE only.

### Layer 6: Fact-Checking Step (verify_sources.py)
Add verification module to pipeline:
```
/home/satyaaditech/yt-automation/verify_sources.py
```
This module will:
1. Parse all URLs from research results
2. CURL each URL and save HTML
3. Extract claims from transcript
4. Match claims with source content
5. Flag/remove unverifiable claims
6. Output: Verified data points only

### Layer 7: Timestamp & Expiry
```python
# Setiap script WAJIB punya timestamp
script_header = f"""
================================================================
📝 SCRIPT: {topic}
📅 GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}
⏰ DATA VALID UNTIL: {datetime.now() + timedelta(days=7)}
================================================================
"""
```

---

## ✅ PRE-DELIVERY CHECKLIST

```
ANTI-HALLUCINATION CHECKLIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
□ Setiap data punya URL source?
□ URL bisa di-CURL dan diakses?
□ Confirmed vs Rumor sudah labeled?
□ Tidak ada auto-translation?
□ Timestamp sudah ditambahkan?
□ Data masih valid (tidak expired)?
□ Bahasa Indonesia natural (bukan translate)?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
**DO NOT DELIVER** jika ada yang belum dicheck!

## Script Template (Indonesian Tech)

```python
# Template for Indonesian tech script with sources
script = f"""
================================================================
📝 SCRIPT VIDEO - {topic}
📌 Baca Langsung / Teleprompter
================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 BAGIAN 1 - HOOK & INTRO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Engaging opener with topic introduction]
[Duration estimate]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 BAGIAN 2 - DATA SPESIFIK (VERIFIED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Sourced data points with specific numbers]

Benchmark data:
— GPT-5.4: 83% GDPval, 75% OSWorld, 57.7% SWE-bench
— Source: https://openai.com/index/introducing-gpt-5-4/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 BAGIAN 3 - RUMOR/UNCONFIRMED (if applicable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Clearly labeled as "unconfirmed" with source attribution]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 KESIMPULAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Rapid summary of key points]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 OUTRO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Call to action + engagement prompt]

================================================================
📚 SOURCES:
1. https://source-url-1.com (Date)
2. https://source-url-2.com (Date)
================================================================
"""
```

## File Structure
```
/home/satyaaditech/yt-automation/
├── pipeline.py           # Main automation controller
├── script_gen.py        # Script generator (Indonesian, sourced)
├── research_topic.py    # Topic research tool
├── fetch_transcript.py  # Extract YouTube transcripts
├── verify_sources.py    # ⭐ NEW: Fact-checking & verification
├── rewrite_content.py   # Content rewriter (4 formats)
└── n8n-workflow.json   # N8N workflow template
```

## Cron Job Setup
```bash
hermes cron create \
  --name "YouTube Content Automation" \
  --prompt "python3 /home/satyaaditech/yt-automation/pipeline.py full 'AI technology trending'" \
  --schedule "0 8,20 * * *" \
  --deliver origin
```

## Key Verification Commands
```bash
# Verify YouTube transcript works
/usr/bin/python3 ~/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py "URL" --text-only

# Verify ddgs works
ddgs text -q "search query" -m 5

# Verify source content (anti-hallucination)
curl -sL "SOURCE_URL" -o /tmp/verify.html && cat /tmp/verify.html | head -50

# Check cron jobs
hermes cron list

# Run verification module (NEW)
python3 /home/satyaaditech/yt-automation/verify_sources.py --input transcript.txt --sources sources.json
```

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `youtube-transcript-api not installed` | Using wrong Python | Use `/usr/bin/python3` not venv python |
| Script too generic | Auto-translation failed | Write fresh Indonesian, use sources as reference |
| No sources cited | Lazy approach | Always include verifiable URLs in script |
| Data feels "hallucinated" | No source verification | curl the article first to verify data exists |
