# Google Flow Agent Mode — Practical Execution Workflow

End-to-end pipeline for producing cinematic AI commercials using ChatGPT + Google Flow Agent Mode + CapCut, derived from Lyra AI masterclass (Sept 2026).

## 4-Phase Pipeline

```
Phase 1: ChatGPT (Asset Preparation)
  Execute 11-Stage Master Prompt → produce 4 visual assets + Final Prompt
    ↓
Phase 2: Google Flow Agent Mode (Video Generation)
  Paste Final Prompt + Attach 4 images → Run Agent (Veo multi-part clips)
    ↓
Phase 3: Troubleshooting & Regeneration
  Evaluate clips → identify failure variable → targeted fix or re-run
    ↓
Phase 4: CapCut Post-Production
  Assemble timeline → trim → SFX/music layering → on-screen text/CTA → export
```

## Phase 2 Detail: Google Flow Agent Execution

1. Open `flow.google`, create **New Project**.
2. Enable **Agent Mode** in the right-side AI Assistant panel.
3. Paste the *Final Master Prompt* from ChatGPT.
4. **Attach all 4 reference images** via "Add to Prompt":
   - Character Reference Sheet Image
   - Product Reference Sheet Image
   - Location Reference Sheet Image
   - Complete Storyboard Image
5. Click **Run**. Flow Agent reads all references as authoritative and generates multi-part video clips via Veo.

## Phase 3: Troubleshooting AI Video Generations

Key principle: **The goal is NOT a perfect clip on first attempt. Identify the cause, then change the right variable.**

| Problem | Root Cause | Fix |
|---|---|---|
| Dialog cutoff (video ends before character finishes speaking) | Clip duration too short for dialogue length | Increase duration to 10s OR shorten dialogue text in prompt |
| Object/motion glitch (weird movement, shape-shifting) | Complex camera trajectory confuses model | Simplify camera instruction (e.g. dynamic dolly zoom → subtle push-in) OR re-run |
| Word repetition in audio (character repeats 1-2 words at end) | Veo audio synthesis artifact | Do NOT re-generate (wastes credits); trim in CapCut instead |
| Camera not behaving as expected | Ambiguous camera instruction in prompt | Be more explicit with direction (e.g. "static medium shot" vs "cinematic") |
| Insufficient time for action | Too much action packed into short duration | Split into two clips or extend duration |

## Phase 4: CapCut Post-Production Checklist

1. Import all downloaded clips from Flow
2. Arrange on timeline per storyboard sequence
3. Precision trim: cut visual artifacts at clip edges, remove audio word repetitions
4. Audio layering: ambient SFX → transition whoosh → product-reveal silence → music bed swell at climax
5. On-screen text: feature callouts, brand logo, CTA at final shot
6. Export: 1080p or 4K MP4

## Credit Efficiency Tips (from Teacher's Tech + Lyra AI)

- Planning & text prompts = **FREE** in Flow → maximize planning before spending credits
- Image generation << video cost → perfect your keyframes first
- Use 5-second clips to test before committing to 10-second generations
- Failed tiles can be trashed and re-run (agent auto-recovers)
- Nano Banana 2 image editor inside Flow can polish keyframes without leaving the workspace
