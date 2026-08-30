---
name: youtube-operations
description: Complete YouTube toolkit — extract transcripts, discover trending videos, automate content pipelines, and write viral scripts. Covers both content extraction from YouTube and content creation for YouTube.
trigger: When working with YouTube videos, transcripts, trending discovery, content automation, or script writing for YouTube.
---

# YouTube Operations

Class-level skill for all YouTube-related workflows: extracting content from videos, discovering trending topics, automating content pipelines, and creating engaging scripts.

---

## 1. Transcript Extraction (from youtube-content)

Extract transcripts from YouTube videos and convert them into structured formats.

### Setup
```bash
pip install youtube-transcript-api
```

### Helper Script
Use the provided `scripts/fetch_transcript.py`. It accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

### Output Formats
After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Workflow
1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.
2. **Validate**: confirm the output is non-empty and in the expected language.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

### Environment Notes (IMPORTANT)
The Hermes venv Python at `~/.hermes/hermes-agent/venv/bin/python3` does NOT have `pip`. For script execution, use `/usr/bin/python3` (system Python) which has `youtube-transcript-api` pre-installed.

```bash
# WRONG - will fail
python3 /path/to/script.py  # uses venv python, no pip

# CORRECT - uses system python
/usr/bin/python3 /path/to/script.py
```

### Error Handling
- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript.
- **Dependency missing**: run `pip install youtube-transcript-api` and retry.

---

## 2. Trending Discovery (from youtube-trending-fetcher)

Fetch trending videos from YouTube by region and category.

### Methods Overview

| Method | Reliability | Setup Required | Rate Limits |
|--------|-------------|----------------|-------------|
| **YouTube Data API v3** | ⭐⭐⭐⭐⭐ | API Key | 10,000 units/day |
| **yt-dlp** | ⭐⭐⭐ | Installation | None (respectful use) |
| **Web Scraping** | ⭐⭐ | None | Blocks easily |

### YouTube Data API (RECOMMENDED)

Setup:
1. Go to https://console.cloud.google.com
2. Create new project → Enable **YouTube Data API v3**
3. Create API Key (Credentials → Create Credentials → API Key)

Fetch trending videos:
```python
import requests

API_KEY = "YOUR_API_KEY"
REGION = "ID"
MAX_RESULTS = 10

def fetch_trending(api_key, region_code="ID", category_id=None, max_results=10):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": api_key
    }
    if category_id:
        params["videoCategoryId"] = category_id
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None
```

### Video Category IDs
| ID | Category |
|----|----------|
| 1 | Film & Animation |
| 10 | Music |
| 20 | Gaming |
| 25 | News & Politics |
| 27 | Education |
| 28 | Science & Technology |

### Filtering by Keywords
```python
def format_trending(data, filter_keywords=None):
    videos = []
    for item in data.get('items', []):
        snippet = item['snippet']
        video = {
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'views': item.get('statistics', {}).get('viewCount', 'N/A'),
            'published': snippet['publishedAt'][:10],
        }
        if filter_keywords:
            if any(kw.lower() in video['title'].lower() for kw in filter_keywords):
                videos.append(video)
        else:
            videos.append(video)
    return videos
```

### Rate Limiting
- **10,000 units per day** per API key
- `videos.list` with `snippet` + `statistics` = ~3 units per call
- Max 100 calls per 100 seconds per user

---

## 3. Content Creation Pipeline (from youtube-tech-content-pipeline + yt-content-pipeline)

Automated pipeline: research → extract transcript → generate sourced script → deliver.

### Pipeline Steps

**Step 1: Research Topic**
```bash
ddgs text -q "GPT-5.5 OpenAI Spud April 2026" -m 10 -t w
```

**Step 2: Extract YouTube Transcript**
```bash
/usr/bin/python3 SKILL_DIR/scripts/fetch_transcript.py "VIDEO_URL" --text-only
```

**Step 3: Verify Sources**
```bash
curl -sL "SOURCE_URL" -o /tmp/page.html
python3 -c "
import re
with open('/tmp/page.html') as f:
    text = re.sub(r'<[^>]+>', ' ', f.read())
    print(text[:2000])
"
```

**Step 4: Generate Script**
Write fresh content using sources as reference. DO NOT auto-translate word-by-word.

### Script Requirements
1. **Full teleprompter style** — ~7-8 min reading, NOT bullet points
2. **Indonesian language** — casual mix with English (use "lo" not "kamu")
3. **Specific verifiable data** — real numbers, dates, benchmarks with sources
4. **Distinguish confirmed vs rumored** — be clear what's verified vs speculation
5. **Tone** — expert but grounded, not salesy
6. **Always include sources** — user wants to be able to verify

### Anti-Hallucination Framework
**CRITICAL:** Every claim must be verifiable.

1. **Source Verification**: curl the source and verify data exists before using it.
2. **Trusted Sources Only**: Official blogs, reputable tech news, Wikipedia, GitHub.
3. **Data Citation Format**: Include actual URLs in the script.
4. **Confirmed vs Rumor Labeling**:
   - `✅ CONFIRMED: {data} (Source: {url})`
   - `⚠️ RUMOR/UNCONFIRMED: {data} (Source: {url})`
5. **No Auto-Translation**: Write fresh in target language using sources as reference only.
6. **Timestamp & Expiry**: Every script must have a generation date and data validity window.

### Pre-Delivery Checklist
```
□ Setiap data punya URL source?
□ URL bisa di-CURL dan diakses?
□ Confirmed vs Rumor sudah labeled?
□ Tidak ada auto-translation?
□ Timestamp sudah ditambahkan?
□ Data masih valid (tidak expired)?
□ Bahasa Indonesia natural (bukan translate)?
```

### Cron Job Setup
```bash
hermes cron create \
  --name "YouTube Content Automation" \
  --prompt "python3 /path/to/pipeline.py full 'AI technology trending'" \
  --schedule "0 8,20 * * *" \
  --deliver origin
```

---

## 4. Viral Script Writing (from viral-tech-script)

Create engaging, viral-worthy tech news scripts using proven emotional triggers and storytelling structure.

### The Viral Formula (9-Part Structure)

| Time | Section | Purpose |
|------|---------|---------|
| 0:00-0:05 | **SHOCK HOOK** | Controversial statement / Unexpected reveal |
| 0:05-0:15 | **CONFLICT SETUP** | Two sides fighting / David vs Goliath |
| 0:15-0:30 | **STAKES** | Why should viewer care? |
| 0:30-2:00 | **STORYTELLING** | Chronological narrative dengan tension |
| 2:00-3:30 | **EVIDENCE DROP** | Specific data, screenshots, quotes |
| 3:30-4:30 | **TWIST / REVELATION** | Unexpected angle / Hidden truth |
| 4:30-5:30 | **IMPLICATIONS** | What this means for viewers |
| 5:30-6:30 | **CALL TO ACTION** | Engagement + Opinion prompt |
| 6:30-7:00 | **OUTRO** | Subscribe + Tease next video |

### Emotional Hooks (Pick 2-3 per script)

| Emotion | Example | When to Use |
|---------|---------|-------------|
| **Shock** | "Mereka bohongin kita selama ini." | Breaking news, scandals |
| **Anger** | "Ini nggak adil dan kita harus marah." | Injustice, betrayal |
| **Fear** | "Kalau ini lolos, privacy kamu habis." | Policy changes, risks |
| **Hope** | "Tapi ada satu company yang berani lawan." | Underdog stories |
| **Curiosity** | "Dan ini yang tidak diberitakan media." | Hidden facts, twists |

### Conflict Framing Examples
```
❌ Boring: "Google signs AI deal with Pentagon."
✅ Viral: "Google jual AI ke militer, Anthropic REFUSE karena etika. Siapa yang benar?"

❌ Boring: "OpenAI releases new model."
✅ Viral: "OpenAI miss revenue targets. Anthropic dan Google close in. Apakah era dominasi mereka selesai?"
```

### Fresh News Detection (Critical!)
**OLD NEWS = DEAD CONTENT.** Always verify news is fresh:

```bash
# Search for recent news (last 7 days)
ddgs text -q "AI news $(date +'%B %Y')" -m 15 -t w
```

**Viral News Indicators:**
- 🔥 Breaking/controversial headline
- 💰 Money involved ($200M+)
- ⚔️ Conflict (Company A vs Company B)
- 🏛️ Government/military angle
- 🚨 Scandal or ethical dilemma

### Complete YouTube Package Workflow
Don't just create script—create **complete package**:

1. **Script** (7-8 minutes) — teleprompter-ready with source citations
2. **YouTube Metadata** — Title, description, tags, timestamps
3. **Thumbnail Design** — 1280x720 specs with text and color palette
4. **TTS for Pacing Reference** — Check speaking speed and pause placement

### 5-Second Viral Check
```
□ Shock value in first 5 seconds?
□ Conflict (A vs B) clear?
□ Specific numbers ($X million)?
□ Sources verified with URLs?
□ News < 1 week old?
□ Stakes personal for viewer?
```
**If 4+ ✓ = Ready to script**
**If < 4 ✓ = Find better angle/topic**

---

## General Rules

1. Never use markdown tables (`|`) in Telegram output
2. Prefer bullet points (`▸` or `•`) for lists
3. Use code blocks only when data density is high
4. Test readability on mobile (narrow screens)
5. Every claim MUST have a verifiable URL
6. Distinguish confirmed vs unconfirmed data clearly
