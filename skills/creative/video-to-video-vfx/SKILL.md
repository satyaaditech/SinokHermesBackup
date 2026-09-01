---
name: video-to-video-vfx
description: Use when prompting V2V models for VFX and video editing.
---

# Video-to-Video (V2V) VFX Prompt Engineering

Workflow and prompt structures for video-to-video (V2V) generative AI models (Gemini Omni Flash, Google Veo, Higgsfield, Runway Gen-3) to perform precise visual effects without breaking source video consistency.

## Core Principle: The "Source Lock" Pattern

V2V models tend to re-generate the entire frame if not strictly constrained. To perform clean object swaps, material edits, character additions, or relighting, the prompt MUST explicitly declare what is locked and what changes.

### Prompt Structure Anatomy

```text
=== [EVENT SUMMARY] — V2V on <<<video_1>>> (~[DURATION]s) ===
⚠️ SOURCE LOCK: this is an [EDIT TYPE] layered onto <<<video_1>>>, NOT a new generation.
KEEP 1:1:
- Subject identity, face, body, performance, and timing.
- Camera focal length, framing, pan/tilt/zoom, and cuts (do NOT re-frame/re-cut).
- Background environment, room layout, props, and practical lighting.

LOCATION & GEOMETRY: [Describe locked geometry of the plate].
THE EVENT / CHANGE: [Describe exact moment and visual effect in detail].
LOOK & FEEL: Photoreal cinema, practical lighting, real shadows and grain, anti-slop (no cartoon/plastic/oversaturated look).
```

## Common V2V Effect Types

1. **Object Swap:**
   - Lock hands, posture, and timing.
   - Specify trigger action (e.g. "at the exact moment the hand stops raising the vase, replace the vase with a kitten").
2. **Material / Texture Swap:**
   - Declare single-object lock: "MATERIAL SWAP on ONE existing object, NOT an added duplicate".
   - Maintain original shape and reflection geometry while altering surface texture (e.g. concrete pillar -> transparent glass).
3. **Props Alive / Added Creatures:**
   - Lock all real humans and static props.
   - Design creature with precise scale relative to scene references (e.g. "lovebird roughly 13cm, size of thumb-to-palm width").
4. **Relighting / Atmosphere:**
   - Keep 1:1 motion and plates.
   - Synchronize light change with in-scene trigger (e.g. finger snap, switch flick).
5. **Environment Destruction / Surface Replacement:**
   - Define exact rectangular boundary or plane being replaced (e.g. "change ONLY the tabletop surface into a mini city").

## Pitfalls & Best Practices

- **Never leave camera motion unconstrained:** Always explicitly state `camera never cuts, matches <<<video_1>>>'s move exactly`.
- **Avoid vague edits:** Specify timing down to the second (e.g. `at 3.2s-4.0s`).
- **Anti-slop constraint:** Include keywords like `real photographed film frame, real depth and grain, grounded and believable`.
