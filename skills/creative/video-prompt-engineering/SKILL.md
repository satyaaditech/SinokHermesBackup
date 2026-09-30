---
name: video-prompt-engineering
description: "Use when authoring video motion prompts for Google Flow."
version: 1.0.0
author: Sinox Agent
license: MIT
metadata:
  hermes:
    tags: [video-generation, google-flow, veo, prompt-engineering, motion-vectors, cinematography]
    category: creative
---

# Video Prompt Engineering & Model Routing

Standard operating procedure for authoring video generation prompts for Google Flow, Veo, Kling, and Runway Gen-3 without wasting generation credits or distorting facial morphology.

## When to Use
- Authoring motion prompts for Google Flow (Veo / VideoFX) and image-to-video engines.
- Deciding model delegation between Hermes (Gemini), ChatGPT (GPT-4o), and Claude for creative video pipelines.
- Converting narrative video concepts into physical camera kinematics and motion vectors.
- Structuring 10-second sequential scenes for domestic comedy and UGC commercials.

## Core Principles & Workflow

### 1. Model Role Specialization
- **Hermes / Gemini (Research & Coordination)**: Use for idea brainstorming, domain research, script logic, and workflow automation.
- **Prompt Synthesis (ChatGPT / Claude)**: Video motion prompts MUST be authored using either ChatGPT (GPT-4o) or Hermes delegated to `best-reasoning-v2` (Claude Opus 4.6 Thinking / Sonnet 4.6). Do not use conversational/Flash models for prompt generation.

### 2. Motion Prompt Anatomy (English Only)
Never include conversational fillers, plot explanations, Indonesian narration, or dialogue in video prompt fields. Video models require physical and optical instructions:
- **Subject & Anatomy**: Subject position, clothing, facial expression (e.g. `Medium close-up of a 35-year-old Indonesian man, seated on fabric sofa, sweat bead forming on temple`).
- **Camera Vector & Optics**: Focal length, aperture, motion trajectory (e.g. `35mm lens, f/2.8, slow push-in dolly zoom, eye-level framing`).
- **Lighting & Texture**: Light direction and color temperature (e.g. `Warm 3200K interior ambient light, volumetric rim lighting from side window`).
- **Motion Dynamics & Physics**: Speed, micro-movements, secondary physics (e.g. `Subtle nervous eye darts, quick defensive flinch pulling sofa cushion over lower face, smooth 24fps`).

## Common Pitfalls

### 1. Conversational / Narrative Prompting Wastes Credits
Gemini Flash / conversational LLMs default to abstract narrative text (e.g. *"A man feels nervous because his wife is angry"*). Generative video models fail on abstract emotions, resulting in warped faces, glitching limbs, and lost credits. Always translate emotions into physical anatomy and micro-expressions.

### 2. Mixing Dialogue in Motion Prompts
Do not paste script dialogue into the video generator prompt box. Dialogue and voiceovers must be added in post-production (CapCut / Google Flow Native Audio). The prompt box is strictly for visual physics and camera mechanics.
