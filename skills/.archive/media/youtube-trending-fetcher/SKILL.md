---
name: youtube-trending-fetcher
description: Fetch YouTube trending videos by region with filtering capabilities. Handles API methods and documents scraping limitations due to YouTube's anti-bot protection.
trigger: When user asks about YouTube trending videos, hot/trending content monitoring, or wants to track popular videos by category
---

# YouTube Trending Fetcher

Fetch trending videos from YouTube by region and category.

## Methods Overview

| Method | Reliability | Setup Required | Rate Limits |
|--------|-------------|----------------|-------------|
| **YouTube Data API v3** | ⭐⭐⭐⭐⭐ | API Key | 10,000 units/day |
| **yt-dlp** | ⭐⭐⭐ | Installation | None (respectful use) |
| **Web Scraping** | ⭐⭐ | None | Blocks easily |

## Method 1: YouTube Data API (RECOMMENDED)

### Setup
1. Go to https://console.cloud.google.com
2. Create new project
3. Enable **YouTube Data API v3**
4. Create API Key (Credentials → Create Credentials → API Key)
5. (Optional) Restrict key for security

### Fetch Trending Videos

```python
import requests

API_KEY = "YOUR_API_KEY"
REGION = "ID"  # Indonesia
MAX_RESULTS = 10

def fetch_trending(api_key, region_code="ID", category_id=None, max_results=10):
    """
    Fetch trending videos from YouTube
    
    Args:
        api_key: YouTube Data API v3 key
        region_code: ISO country code (ID, US, etc.)
        category_id: Video category (28=Science & Tech, 1=Film, etc.)
        max_results: Number of results (max 50)
    """
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
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

def format_trending(data, filter_keywords=None):
    """
    Format trending data for display
    
    Args:
        data: API response JSON
        filter_keywords: List of keywords to filter (e.g., ['AI', 'tech'])
    """
    if not data or 'items' not in data:
        return "No data available"
    
    videos = []
    for item in data['items']:
        snippet = item['snippet']
        stats = item.get('statistics', {})
        
        video = {
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'views': stats.get('viewCount', 'N/A'),
            'likes': stats.get('likeCount', 'N/A'),
            'published': snippet['publishedAt'][:10],
            'category_id': snippet.get('categoryId', 'N/A')
        }
        
        # Filter by keywords if provided
        if filter_keywords:
            title_lower = video['title'].lower()
            if any(kw.lower() in title_lower for kw in filter_keywords):
                videos.append(video)
        else:
            videos.append(video)
    
    return videos

# Usage
# data = fetch_trending(API_KEY, region_code="ID")
# ai_videos = format_trending(data, filter_keywords=['AI', 'artificial intelligence', 'ChatGPT'])
```

### Video Category IDs

| ID | Category |
|----|----------|
| 1 | Film & Animation |
| 2 | Autos & Vehicles |
| 10 | Music |
| 15 | Pets & Animals |
| 17 | Sports |
| 19 | Travel & Events |
| 20 | Gaming |
| 22 | People & Blogs |
| 23 | Comedy |
| 24 | Entertainment |
| 25 | News & Politics |
| 26 | Howto & Style |
| 27 | Education |
| 28 | Science & Technology |
| 29 | Nonprofits & Activism |

## Method 2: yt-dlp (Limited)

**Note:** YouTube's `/feed/trending` page now redirects to homepage when accessed via yt-dlp. This method is unreliable as of 2024.

```bash
# This will likely fail due to redirect
yt-dlp --flat-playlist --dump-single-json \
  "https://www.youtube.com/feed/trending?gl=ID&hl=id"
```

## Method 3: Web Scraping (Not Recommended)

**⚠️ YouTube heavily blocks scraping attempts.**

The page structure uses `ytInitialData` with nested JSON:
```
contents
└── twoColumnBrowseResultsRenderer
    └── tabs[0]
        └── tabRenderer
            └── content
                └── richGridRenderer (or sectionListRenderer in old UI)
                    └── contents
                        └── richSectionRenderer
                            └── content
                                └── richShelfRenderer
                                    └── contents
                                        └── richItemRenderer
                                            └── content
                                                └── videoRenderer
```

**Why it fails:**
- YouTube serves different HTML to bots vs browsers
- Heavy rate limiting and IP blocking
- Dynamic content loading
- Requires sophisticated browser automation (Selenium/Playwright)

## Complete Monitoring Solution

```python
import requests
import json
from datetime import datetime

def monitor_trending(api_key, config):
    """
    Complete trending monitoring solution
    
    Args:
        api_key: YouTube API key
        config: Dict with 'regions', 'categories', 'keywords', 'webhook_url'
    """
    all_results = {}
    
    for region in config.get('regions', ['ID']):
        all_results[region] = {}
        
        for category in config.get('categories', [28]):  # Default: Tech
            data = fetch_trending(api_key, region, category)
            
            if data:
                filtered = format_trending(data, config.get('keywords'))
                all_results[region][category] = filtered
    
    # Send to webhook (Telegram, Discord, etc.)
    if config.get('webhook_url'):
        send_to_webhook(all_results, config['webhook_url'])
    
    return all_results

def send_to_webhook(data, webhook_url):
    """Send results to Telegram/Discord webhook"""
    formatted = format_for_telegram(data)
    
    # Telegram Bot API example
    requests.post(webhook_url, json={
        'text': formatted,
        'parse_mode': 'HTML'
    })

def format_for_telegram(data):
    """Format results for Telegram message"""
    lines = [
        "🔥 <b>YouTube Trending Update</b>",
        f"📅 {datetime.now().strftime('%d %B %Y, %H:%M')}\n"
    ]
    
    for region, categories in data.items():
        lines.append(f"\n🇮🇩 <b>Region: {region}</b>")
        
        for cat_id, videos in categories.items():
            lines.append(f"\n📁 Category: {cat_id}")
            
            for i, video in enumerate(videos[:5], 1):
                lines.append(
                    f"{i}. {video['title'][:50]}...\n"
                    f"   👁 {video['views']} | 📺 {video['channel']}\n"
                )
    
    return '\n'.join(lines)

# Example config
CONFIG = {
    'regions': ['ID', 'US'],
    'categories': [28, 27],  # Tech & Education
    'keywords': ['AI', 'artificial intelligence', 'machine learning', 'ChatGPT'],
    'webhook_url': 'https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>'
}
```

## Cron Job Setup

```bash
# Edit crontab
crontab -e

# Run every 6 hours
0 */6 * * * /usr/bin/python3 /path/to/trending_monitor.py >> /path/to/log.txt 2>&1
```

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `403 API_KEY_INVALID` | Wrong/expired key | Regenerate in Google Console |
| `403 quotaExceeded` | Daily limit reached | Wait 24h or request increase |
| `400 invalid_region` | Invalid region code | Use ISO 3166-1 alpha-2 codes |
| Empty results | No trending in category | Try different category or region |

## Rate Limiting

- **10,000 units per day** per API key
- `videos.list` with `snippet` + `statistics` = ~3 units per call
- Max 100 calls per 100 seconds per user

## Tips

1. **Cache results** - Don't call API on every request
2. **Use multiple API keys** - Rotate if hitting limits
3. **Filter client-side** - Fetch all, then filter (more efficient)
4. **Monitor quota** - Track usage in Google Console
5. **Handle pagination** - Use `nextPageToken` for >50 results
