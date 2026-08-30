---
name: vlog-script-storytelling
description: Use when writing long-form vlog scripts (walk-and-talk).
trigger: When creating long-form (10-15 min) vlog scripts — walk-and-talk storytelling, local history/heritage content, location-based narrative videos, or script revisions for Satya's YouTube series.
---

# Vlog Script Storytelling

Class-level workflow for long-form narrative vlog scripts in Indonesian: presenter
walks a real location and tells its story (history, events, insight), covering
5W+1H, with verified fun facts. Built from Satya's "Jalan Pagi Sejarah" Solo series.

## User's format preferences (explicitly corrected during session — follow these)

1. **Structured point-per-point narration with 5W+1H labels** (APA/SIAPA/KAPAN/DIMANA/
   MENGAPA/BAGAIMANA) per segment. User REJECTED flowy audience-optimized prose as the
   main format — the labeled structure is easier to memorize while filming. Default to v1-style.
2. **NEVER reduce content when revising.** Standing rule: "harus komplit jangan dikurangi".
   Preserve 100% of existing facts; add features on top.
3. **Fun facts welcome** — dedicated FUN FACT block per segment (2-5 each) + compiled
   "Bank Fun Fact" table. Only verified facts; mark unverified as (±).
4. **Deliver as downloadable .md** via `MEDIA:/abs/path` in
   `/home/satyaaditech/yt-automation/output/`. Keep older versions; offer cleanup.
5. User accepted exactly 3 retention add-ons ("refined" version): 10-second hook with a
   mission, 1-sentence cliffhanger at end of each segment, comment CTA in closing.
   Do NOT push the full audience-optimized rewrite again.

## Workflow

1. Clarify format (long vs Shorts), location, angle, core message — offer choices via clarify.
2. **Verify every fact BEFORE writing** (dates, names, capacities, ownership, heritage spots).
   Use `references/wikipedia-api-curl.md` fallback when web tools are unconfigured.
   Never write history from memory.
3. Build a fact bank per segment with source attribution, then write narration.
4. Script structure:
   - HOOK 10 detik: most surprising fact + mission ("kita buktikan bareng")
   - INTRO: kenalan, konteks, janji konten, route
   - 3-4 SEGMEN: 5W+1H point-per-point + FUN FACT block, each ending with cliffhanger
   - INSIGHT: show-don't-tell (real observed scene), not moralizing lecture
   - CLOSING: recap singkat + CTA komentar + teaser episode berikutnya
5. Timeline companion doc when asked for chronology: stages with modern-day locations,
   ASCII map, relative positions, (±) on unverified locations, "bahan cerita untuk vlog".
6. Checklist section: 5W+1H per segment + production tips + sources.

## Retention elements (full list, apply as add-ons)

- Hook 10 detik + breadcrumb mission (promise a payoff at route end)
- Cliffhanger 1 kalimat per segment transition (open loop → close next segment)
- Pattern interrupt: [CUT]/[B-ROLL] cues in narration, cut every 30-45 detik
- Insight via real observed scene (e.g. bapak senam), not lecture
- CTA komentar spesifik: "kamu olahraga di mana? tulis di komentar"
- Chapter markers, thumbnail (bold text + face), angka judul option

## Production tips to embed in scripts

Lapel mic priority (morning wind); take per segment 2-3x; memorize points not prose;
B-roll list per segment; ambient sound kept under vocals; new channels safer at 10-11 min,
cut from middle; check physical access of heritage spots before filming.

## Pitfalls

- History claims MUST be sourced; unverified location = say so in the script (e.g.
  Bengawan Sore in the Pamanahan story — name only, no location claim).
- Physical heritage spots (petilasan/sendhang) = strongest hook + natural episode-2 teaser.
- When user prefers v1 structure, apply the 3 accepted elements on top — never rewrite wholesale.
- Source list at end of every script; keep honest (±) marks.

## Project state (Solo "Jalan Pagi Sejarah" series)

- Episode 1: Manahan — 4 versions in yt-automation/output/
  `vlog_manahan_episode1_{v1,v2,refined,funfacts}.md` (final = funfacts, 14-15 min)
- Timeline: `timeline_ki_ageng_pamanahan.md` — Sela/Grobogan → Pengging/Boyolali →
  Manahan/Solo → Mentaok/Kotagede → Mataram → 1755 pecah Surakarta & Yogyakarta
- Episode 2 planned: petilasan sendhang Ki Ageng Pamanahan, Kampung Ngumbul, Kel. Manahan
- Queued locations: Sriwedari, Balekambang, Pasar Gede

## Support files

- `references/wikipedia-api-curl.md` — curl fallback for fact verification when web tools unconfigured
