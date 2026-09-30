---
name: sitkom-short-serial
description: "Use when creating family sitcom short serials in Flow."
version: 1.0.0
author: Sinox Agent
license: MIT
metadata:
  hermes:
    tags: [sitcom, comedy, youtube-shorts, google-flow, family, serial, recurring-cast]
    category: creative
---

# Google Flow Family Sitcom Short Serial Workflow

Standard Operating Procedure (SOP) for creating recurring Indonesian family comedy sitcoms (Ayah, Ibu, Anak) for YouTube Shorts using Google Flow Agent Mode and Storyboard Studio.

## When to Use
- Producing episodic family comedy sketches and recurring sitcom shorts (30s: 3 scenes @ 10s).
- Directing multi-character comedy with English camera/motion directives and Indonesian spoken dialogue.
- Maintaining consistent recurring family digital twins (Ayah, Ibu, Anak) across episodes.

## Core Production Rules

### 1. Pre-Production Protocol (Mandatory)
1. **Story Summary First**: Sinox MUST present a concise 3-act story outline (Setup -> Escalation -> Punchline) before authoring the full prompt.
2. **User Approval (ACC)**: Wait for user confirmation before writing the detailed technical prompt.
3. **Master Agent Prompt**: Detailed technical prompt generated only after user approval.

### 2. Dual-Language Architecture
- **Director Directives (Visuals, Camera, Action, Lighting, SFX)**: Written in **English** for maximum AI compliance and cinematography precision in Veo / Google Flow.
- **Spoken Dialogue**: Written in natural **Indonesian** verbatim inside `[NATIVE AUDIO DIRECTIVES]` with character tags and comedic cadence (e.g. `Spoken Dialogue (Ayah, shocked funny tone): "Lho, Bu... kopinya kok asin?!"`).

### 3. Storyboard Studio Zero-Friction Workflow
1. Paste prompt into **Storyboard Studio** to generate visual panels (Family Characters, House Location, Storyboard).
2. Use **"Select All" -> "Add as Reference"** globally (bypasses tedious manual `@` tagging per scene).
3. Set Google Flow: `Confirm before generating: Never`.
4. Render 3 sequential clips (10s each = 30s total) automatically in continuous pass.

### 4. Recurring Family Cast & Environment Consistency
Lock the recurring family cast and physical house environment once to reuse across all serial episodes:
- **Ayah (Father)**: 35–38 yrs old, relatable, friendly, slightly goofy expression, consistent polo/shirt.
- **Ibu (Mother)**: 32–35 yrs old, sharp, caring, modern house attire/batik dress, neat hair bun.
- **Anak (Child)**: 7–8 yrs old, witty, playful, striped t-shirt.
- **Strict Spatial & Background Consistency (Environmental Lock)**:
  - Explicitly define fixed architectural details and color palette: e.g. *Warm cream walls, matte-teal kitchen cabinets, light-oak wooden dining table, white ceramic tile floor, 5000K warm natural morning window light*.
  - MUST repeat these exact environment color/material keywords inside the visual block of EVERY scene to lock spatial continuity and prevent AI background drifting.
  - Fix camera angle orientations relative to the set (e.g. looking south towards table, panning west towards kitchen counter).

### 5. 30-Second 3-Act Sitcom Formula
- **Scene 1 (0–10s) — Setup**: Normal domestic situation meets a subtle anomaly/problem.
- **Scene 2 (10–20s) — Escalation**: Attempting to fix the problem causes misunderstanding or chaos.
- **Scene 3 (20–30s) — Punchline & Payoff**: Climax, revelation, funny reaction, and comedic payoff SFX.

### 6. Surgical Revisions Rule
- If any scene needs refinement, revise ONLY the specific broken elements (e.g. motion stability, specific clothing keywords repeated inside scene visual blocks to prevent AI amnesia). Keep working sections untouched.
