---
name: yt-content-pipeline
description: End-to-end YouTube content automation — research, extract, generate teleprompter scripts, deliver to Telegram
---

# YouTube Content Automation Pipeline

## What It Does
End-to-end YouTube content automation: research trending topics → extract video transcripts → generate full teleprompter scripts → deliver to Telegram.

## Workflow
```
ddgs search (research) → youtube-transcript-api (extract) → rewrite_content.py (generate) → send_message Telegram
```

## Pipeline Location
`/home/satyaaditech/yt-automation/`

## Cron Job Active
- Name: "YouTube Content Automation - Daily"
- Schedule: 08:00 & 20:00 every day
- Deliver: Telegram (chat_id: 777961507)

## Script Requirements (IMPORTANT)
1. **Full teleprompter style** — ~7-8 min reading, NOT bullet points
2. **Indonesian language** — casual mix with English (use "lo" not "kamu")
3. **Specific verifiable data** — include real numbers, dates, benchmarks with sources
4. **Distinguish confirmed vs rumored** — be clear what's verified vs speculation
5. **Tone** — expert but grounded, not salesy
6. **Always include sources** — user wants to be able to verify

## Script Format Options

### Option A: Standard Informative (Default)
- Balanced, educational tone
- Good for: Tutorials, explainers, how-to content

### Option B: Viral/Engaging (NEW!)
- Use `viral-tech-script` skill formula
- Shock hook, conflict framing, emotional triggers
- Good for: Breaking news, controversies, competitive analysis
- See: `skill_view(name='viral-tech-script')`

## Sources Used
- OpenAI official blog (openai.com/index/introducing-gpt-5-4/)
- YouTube: UfUBW9QcTjU, 4lkDILIFSjw
- primeaicenter.com, nxcode.io, wikipedia.org

## Telegram Format Rules
- Plain text ONLY — NO markdown tables
- Use bullet points (▸ or •)
- NO [SILENT] responses ever
