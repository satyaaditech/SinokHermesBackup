---
name: walking-vlog-storytelling
description: "Walking vlog scripts: location stories + retention review."
trigger: When the user asks for a walking vlog, location storytelling script, "Jalan Pagi Sejarah" series content, or an audience-retention review of a video script.
---

# Walking Vlog Storytelling (Long-Form Location Vlogs)

Class-level workflow for the user's "Jalan Pagi Sejarah" vlog series: 10-15 min
walking vlogs where the host strolls a location and casually tells interesting
stories about it (history, notable events, insights), with 5W+1H covered.
User: Satya, Solo (Surakarta), Jawa Tengah. Output in Indonesian.

## Workflow

1. **Pick location + walk route** — a loop of ±1 km supports 3-4 content segments.
2. **Verify facts BEFORE scripting** — never write history from memory.
   - Web tools (`web_search`/`web_extract`) may be unconfigured (Firecrawl) —
     the curl fallback below works reliably and is the FIX, not a dead end.
   - Wikipedia via curl:
     - Summary: `curl -sL "https://id.wikipedia.org/api/rest_v1/page/summary/<Title_With_Underscores>"`
     - Full plain text:
       `curl -sL "https://id.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&titles=<Title>" | python3 -c "import json,sys; d=json.load(sys.stdin); p=list(d['query']['pages'].values())[0]; print(p.get('extract',''))"`
   - Mine for: origin of place names (folklore/etymology), heritage remnants
     (petilasan, sendhang/springs), buildings & events, local clubs, day-vs-night
     contrast of the spot.
   - Record source (Wikipedia page + retrieval date) in the script file.
   - Berita/artikel Indonesia (tribun, solopos, dll): fallback chain Google News
     RSS + Wayback CDX + direct curl arsip — chain lengkap di
     `references/riset-news-fallback-id.md` (r.jina.ai hanya jalan utk tribunnews/hutamakarya).
   - PITFALL: vision model sering salah identifikasi lokasi dari foto user (kasus:
     rel layang Simpang Joglo dikira "LRT Jabodebek Cikunir"). Lokasi dari foto =
     hipotesis sampai user konfirmasi; kalau dikoreksi user, riset ULANG dari nol.
   - For spots to visit on camera, tell the user to check physical access with
     locals before filming; hedge anything unverified in the narration.
3. **Build storyboard** — timeline table, full narration in spoken Indonesian,
   5W+1H checklist per segment, production tips, sources. Template pattern:
   see `references/manahan-episode-1.md` for a complete worked example.
4. **Run the audience-retention review (below) before delivering** — the user
   explicitly asks for honest audience-side critique. Give score /10, the exact
   timestamps where viewers quit, and concrete fixes.
5. **Save script** to `/home/satyaaditech/yt-automation/output/vlog_<lokasi>_episode<N>.md`.

## Storyboard structure (10-15 min)

- Hook (0:00) — see retention fix: spoken hook ≤10-15 s
- Intro (1:00-2:30) — who you are, promise, route preview
- 3-4 content segments (~2.5-3.5 min each) — one story beat per segment, each
  covering 5W+1H (What/Who/When/Where/Why/How)
- Insight segment — personal reflection (SHOW, don't lecture)
- Closing — recap, specific CTA, teaser for next episode

## Audience-retention review framework

Deliver: score /10 + the specific points where viewers quit + fixes.

1. **Hook**: viewers give 5-10 s. Open with the most surprising fact, don't
   explain everything, and give a *mission* (breadcrumb): "ada jejak nyatanya di
   ujung rute — kita buktikan bareng."
2. **Breadcrumb**: promise the payoff early (e.g. heritage site), remind mid-video.
3. **Pattern interrupt every 30-45 s**: B-roll, cut, zoom, text overlay —
   walking footage is visually monotonous; edits carry the rhythm.
4. **Cliffhanger between segments**: close the loop every 2-3 min
   ("...tapi cerita paling gilanya bukan di stadion. Bentar lagi.")
5. **Insight = show-don't-tell**: describe a real scene observed that morning
   (e.g. an elderly man still doing morning exercise) instead of a generic
   motivation quote — viewers hate being lectured.
6. **CTA specific + comment bait**: "Kamu olahraga di mana? Tulis di kolom
   komentar" — not "follow channel ini".

Extra insights well received:
- Keep ambient audio (birds, steps, morning sounds) — don't bury it in music.
- 10-11 min is safer than 13-14 for a new channel.
- Chapter markers in the description (visible progress for viewers).
- Numbered titles ("3 Rahasia...") boost CTR — content must match the promise.
- Consistent morning upload time builds a viewing habit.
- Series arc across locations = a reason to subscribe.

## Pitfalls

- Never read 5W+1H labels aloud (APA/SIAPA/KAPAN...) — turns the vlog into a
  school lecture. Use them as structure; write natural spoken prose.
- Don't open with a full 60 s of narration — hook first, details later.
- Verify history before writing; keep sources in the file (anti-hallucination
  standard, consistent with the yt-automation pipeline).

## Support files

- `references/manahan-episode-1.md` — complete worked example: full narration +
  storyboard + 5W+1H checklist + verified fact bank for episode 1 (Manahan).
