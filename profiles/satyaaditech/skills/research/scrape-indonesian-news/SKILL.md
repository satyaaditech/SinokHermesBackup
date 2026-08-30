---
name: scrape-indonesian-news
description: Scrape headlines and articles from Indonesian news portals (Kompas, Detik, dll)
triggers: [scrape news, headline kompas, berita hari ini]
---

# Scrape Indonesian News Sites

## Key Learnings

### Kompas.com
- **Homepage** (`kompas.com`) is JS-rendered — `curl` returns empty article list
- **News section** (`kompas.com/news`) returns static HTML with `<h3 class="article__title">` structure
- Use: `curl -s "https://www.kompas.com/news" -L -A "Mozilla/5.0"`
- Article title selector: `<h3 class="article__title">` → `<a class="article__link" href="...">`
- Trending topics: `<div class="trendTitle">` inside `<div class="trendName swiper-slide">Trending:</div>`

### Most Popular / Terpopuler (Kompas.com)
- Not on a separate URL — embedded in homepage
- Section title: `<h2 class="mostTitle">` contains article titles
- Extract with: `curl -s "https://www.kompas.com/" -L -A "Mozilla/5.0" | grep -A2 "mostTitle"`
- Anchor tags have `source=terpopuler` query param

### Article Content Scrape
```bash
curl -s "<article_url>" -L -A "Mozilla/5.0" | grep -oP '(?<=<p>)[^<]+' | head -30
```
- Works on article read pages (e.g., `kompas.com/read/...`)
- Strips HTML entities (`&ldquo;`, `&rdquo;`, etc.) naturally via plain text output

### Google News RSS (trending backup)
When direct Google Trends API is blocked (returns 404), use:
```bash
curl -s "https://news.google.com/rss/search?q=trending+Indonesia&hl=id-ID&gl=ID&ceid=ID:id" -L --max-time 15
```
Returns Google News results for "trending Indonesia" query — good proxy for what's trending.

### Detik.com
- Usually returns static HTML on main pages
- Article class: `.media__title` or `.desc__item`

### General Approach
1. Try `curl -L` first on target URL with `Mozilla/5.0` User-Agent
2. If empty, try `/news` subdirectory
3. If still empty, content is JS-rendered → use `ddgs news "site:domain.com"` as fallback
4. Regex lookbehind (`(?<=...)`) in `grep -P` fails for variable-length patterns — use simpler selectors

### Pitfalls
- `grep -oP` with variable-length lookbehind throws "lookbehind assertion is not fixed length" — avoid or use `sed` instead
- Always use `-L` (follow redirects) and `-A "Mozilla/5.0"` to avoid bot blocking
