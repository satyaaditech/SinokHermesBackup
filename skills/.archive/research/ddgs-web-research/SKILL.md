---
name: ddgs-web-research
description: Web research using ddgs (duckduckgo-search) CLI — news, text, and trends search for content research and trend monitoring.
triggers:
  - "trending topics"
  - "AI news"
  - "research"
  - "trending"
  - "web search"
---

# DDGS Web Research Skill

Use `ddgs` (duckduckgo-search Python CLI) for web research, news monitoring, and trend discovery.

## Installation

```bash
pip install duckduckgo-search
```

## Core Commands

### News Search
```bash
ddgs news -q "QUERY" -m 10 -t w
```
Flags: `-m N` = max results, `-t w` = this week, `-t d` = today, `-t m` = this month

### Text/Web Search
```bash
ddgs text -q "QUERY" -m 8 -t w
```

### Combined Research Pattern (AI Trends Example)
```bash
# Parallel searches for comprehensive coverage
ddgs news -q "artificial intelligence trending $(date +'%B %Y')" -m 10 -t w
ddgs news -q "AI ChatGPT OpenAI news this week" -m 8 -t w
ddgs text -q "AI tools trending $(date +'%B %Y')" -m 8 -t w
```

## Telegram Output Format

CRITICAL: User wants plain text, NO markdown tables.

GOOD:
```
▸ Topic 1 — description
▸ Topic 2 — description
• Bullet point
```

BAD:
```
| Topic | Description |
|-------|-------------|
```

Use `▸` for main points, `•` for sub-items, `1️⃣ 2️⃣ 3️⃣` for numbered lists.

## Content Creator Workflow

When asked for trending topics or content research:
1. Run 2-3 parallel ddgs searches (news + text, different angles)
2. Combine and deduplicate results
3. Extract 5-7 most relevant items
4. Format as Telegram plain-text bullet list
5. End with 2-3 content angle suggestions

## Python API (Alternative)

```python
from duckduckgo_search import DDGS
with DDGS() as ddgs:
    results = list(ddgs.news("QUERY", max_results=10, timelimit="w"))
    results = list(ddgs.text("QUERY", max_results=8, timelimit="w"))
```
