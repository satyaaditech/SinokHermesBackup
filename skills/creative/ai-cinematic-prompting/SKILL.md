---
name: ai-cinematic-prompting
description: "Use when prompting AI image, video, or character sheets."
version: 1.0.0
author: Sinox Agent
license: MIT
metadata:
  hermes:
    tags: [cinematography, image-to-video, prompts, character-sheets, gemini, imagen-3, flow, veo, midjourney]
    category: creative
---

# AI Cinematic & Video Prompting

Standard operating procedures for authoring high-fidelity, production-grade prompts across text-to-image (Gemini Imagen 3, Midjourney v6, Flux.1) and image-to-video pipelines (Google Flow, Veo, Kling, Runway Gen-3).

## When to Use
- Constructing prompts for cinematic stills, b-roll, YouTube visual assets, or portrait photography.
- Creating 2-stage image-to-video animations (First Frame Keyframe + Motion Prompt via Google Flow / Veo).
- Structuring single-prompt multi-scene workflows for Google Flow Agent mode (auto batch 10s scenes).
- Generating character consistency turnarounds & 8-module production continuity sheets (identity-locked).
- Directing Google Flow / Veo video motion with viral hooks, UGC styles, and impossible VFX transitions.
- Ingesting visual prompting frameworks into Obsidian LLM Wikis (`MasteringAI`).

## References & Detailed Frameworks
- `references/character-continuity-8module.md` : 8-Module Video Production Continuity & Character Sheet (Identity-Locked) prompt deck.
- `references/google-flow-motion-directives.md` : 99 Google Flow & Veo motion directives (hooks, UGC, VFX transitions, commercials).
- `references/chatgpt-image-quick-commands.md` : 99 Viral AI image quick commands & modifiers for ChatGPT, Gemini, and Midjourney.
- `references/google-flow-multi-scene-agent.md` : Single-prompt multi-scene generation template using Google Flow Agent mode.

## The 2-Stage Image-to-Video Workflow

Direct text-to-video (T2V) often yields morphed limbs, distorted anatomy, and flickering lights. Always separate static visual composition from dynamic motion:

```text
┌────────────────────────────────┐       ┌────────────────────────────────┐
│  Stage 1: Keyframe Prompt      │  ───► │  Stage 2: Motion Prompt        │
│  (Gemini Pro / Imagen 3)       │       │  (Google Flow / Veo / Kling)   │
│  Subject + Environment + Lens  │       │  Camera Vector + Particle Move │
└────────────────────────────────┘       └────────────────────────────────┘
```

### 1. Stage 1: Keyframe Image Formula (5 Blocks)
```text
[Shot Type & Camera Angle] + [Subject & Action/Pose] + [Environment & Time] + [Lighting & Color Palette] + [Lens Optics & Render Fidelity]
```
* **Camera Angle Keywords**: `low-angle heroic perspective`, `dutch angle shot`, `bird's-eye top-down view`, `eye-level medium close-up`.
* **Lighting Keywords**: `Rembrandt lighting`, `dramatic chiaroscuro`, `golden hour warm honey glow`, `volumetric rim lighting`, `soft diffused overcast`.
* **Lens & Texture**: `shot on 35mm anamorphic prime lens`, `creamy bokeh f/1.4`, `photorealistic 8K`, `subtle organic film grain`.

### 2. Stage 2: Motion Prompt Formula (Active Verbs & Vectors)
* Focus purely on camera movement and environmental dynamics — do NOT restate static subject traits.
* **Camera Path**: `camera pushes in slowly`, `smooth tracking shot following subject forward`, `slow 360-degree orbital arc`.
* **Physics & Particles**: `subtle floating dust motes drifting in light beams`, `gentle rising smoke`, `rippling water surface`.
* **Lock Anchor**: `subject remains locked in central focus, steady 24fps cinematic motion`.

---

## Character Consistency & Turnaround Sheets

To preserve facial identity across scenes:
1. **Master Consistency Anchor**:
   ```text
   Maintain the exact facial identity, bone structure, eye shape, skin tone, and hair texture of the person in the uploaded reference photo across every panel of the character sheet. Do not alter their face. Render a comprehensive high-resolution character design sheet with the following layout:
   ```
2. **6-Panel Modular Grid Layout**:
   - Top: 3-way full-body turnaround (Front, 90° Side Profile, Back).
   - Middle: Horizontal expression strip (Neutral, Happy, Pensive, Determined, Surprised).
   - Bottom: 3-4 dynamic action poses + fabric zoom-in callouts + color palette chips.
3. **Midjourney / Flux Parameters**:
   `--cref [IMAGE_URL] --cw 20 --ar 4:5 --style raw`

---

## Pitfalls & Edge Cases

1. **Adjective Stacking vs Scene Narrative**: Modern LLM-backed image generators (Imagen 3, DALL-E 3) respond better to coherent descriptive sentences than raw comma-separated keyword soup.
2. **Negative Prompting**: If hands or eyes distort in video generation, explicitly exclude: `morphing face, extra limbs, frame jitter, flickering lighting, sudden jump cuts`.
3. **Aspect Ratio Preservation**: Always generate the Stage 1 Keyframe in the identical aspect ratio required for the Stage 2 Video (16:9 for YouTube Long-form, 9:16 for Shorts/Reels).
