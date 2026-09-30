---
name: hybrid-ai-video-pipeline
description: "Use when producing AI commercial and sitcom video."
version: 1.1.0
author: Sinox Agent
license: MIT
metadata:
  hermes:
    tags: [ai-video, google-flow, veo, master-lock, commercial, sitcom, ugc, storyboard-studio]
    category: creative
---

# Hybrid AI Video Production Pipeline (Commercial & Sitcom)

Unified, authoritative Google Flow / Veo 3.1 production pipeline synthesizing:
1. **Google Flow Master Workflow (36-Point Framework & 10 Golden Rules)**: Full film production discipline (Shot-by-Shot generation, Visual Bible Assets, Camera Grammar, Physics & Biomechanics, End/Start Keyframe Chaining, Scenebuilder Assembly, QC Checklist).
2. **Modul Level 1**: Modular Master Lock blocks (Product, Model, Location, Lighting) + standardized scene parameter blocks.
3. **Master Prompt / UGC SOP**: 3-Act Narrative Flow, Problem-Solving Hook, Multi-Part Continuity, Native Audio/SFX directives.
4. **Storyboard Studio Zero-Friction**: Global "Select All -> Add as Reference" with textual keyword anchors in every scene.
5. **Dual-Language Standard**: English directorial directives (camera, motion, lighting) + Indonesian spoken dialogue.

*Comprehensive Reference Document*: `references/google-flow-master-workflow.md`

## When to Use
- Producing professional 15s–60s commercial ads, UGC videos, and episodic sitcom shorts in Google Flow / Veo.
- Demanding high consistency across characters, products, and interconnected environments without tedious manual tagging.

## The 4-Phase Hybrid Pipeline

### Phase 1: Pre-Production & Narrative Alignment
1. **Intake**: User supplies product/topic/character idea (optional: 1 product photo or 1 model photo).
2. **Story Summary First**: Sinox drafts a tight 3-Act Story Summary (Setup -> Escalation/Fluid Solution -> Payoff).
3. **User Approval (ACC)**: Wait for user confirmation before generating full technical prompts.

### Phase 2: Master Lock & Visual Asset Generation
1. **Master Lock Assembly**:
   - `MASTER PRODUCT / PROP LOCK` (Name, Color, Texture, Packaging, Logo, Never Change).
   - If comparing old/failed vs new hero product (e.g. worn shoe vs cloud shoe), create TWO separate locks: `MASTER OLD PRODUCT LOCK (SCENE 1 ONLY)` and `MASTER NEW HERO PRODUCT LOCK (SCENE 2+ ONLY)`.
   - `MASTER MODEL / CAST LOCK` (Identity, Age, Hair, Skin, Fixed Wardrobe).
   - `MASTER SPATIAL & LOCATION LOCK` (Layout, Fixed Architecture, Cabinet/Table Colors, Flooring, Lighting).
2. **Storyboard Studio Execution**:
   - Generate key visual panels (Character, Prop, Spatial Location).
   - Click **"Select All" -> "Add as Reference"** to establish the global visual memory bank.

### Phase 3: Master Agent Prompt Execution (Primary 1-Click Mode)
- **Primary Delivery Mode**: Single cohesive prompt pasted into Google Flow Agent Mode (`Confirm before generating: Never`). Generates 3 sequential 10s clips (30s total) in one click without manual multi-shot assembly friction.
- **Secondary Mode**: Detailed Modular Shot-by-Shot (6-9 shots @ 2-4s) documented in `references/google-flow-master-workflow.md` for high-precision manual Scenebuilder trimming.
- Structure per scene (10s blocks):
  ```text
  SCENE [N] (Duration: 00:00 - 00:10) — "[SCENE TITLE]"
  - Visual & Framing: [Action narrative + explicit repetition of Master Lock wardrobe/product/location keywords + camera framing]
  - Camera: [ONE primary stabilized movement: Dolly In, Tracking, Low-Angle Macro]
  - Lighting: [Consistent lighting setup: 6:00 AM Golden Hour, Warm Rim Light]
  - [NATIVE AUDIO DIRECTIVES]:
    * Spoken Dialogue ([Character], [tone]): "[Verbatim Dialogue in Indonesian or English]"
    * Ambient & SFX: [Layered sound effects matching physical action]
  ```

### Phase 4: Surgical Revision Protocol
- If any element drifts (e.g. background color shift, unnatural motion start), revise ONLY the specific broken parameters.
- Re-inject explicit negative constraints (e.g. `strictly NO white cabinets, identical matte petrol-teal only`) into the scene visual block.

## Common Pitfalls & Anti-Glitch Rules

### 1. Hard Cut Editorial Transformation vs Generative Morphing
- **Root Cause**: Requesting literal dynamic visual transformation/morphing within a single clip (e.g. worn shoe turning into new shoe, or clothes transforming) causes generative models to hallucinate melting geometries, rubbery deformations, and hybrid half-old/half-new artifacts.
- **Rule**: NEVER ask the AI to morph products or characters. Clip 1 strictly ends on the old asset; Clip 2 strictly begins with the new hero asset already fully worn and formed. Let the video editor cut do the transformation, not diffusion physics.

### 2. Single Primary Camera Movement per Clip
- **Root Cause**: Compounding multiple camera moves in a single short clip (e.g. tracking -> dolly-in -> crane -> 360-orbit) destabilizes frame generation and introduces severe warping or extra limbs.
- **Rule**: Limit each clip to ONE primary stabilized camera movement (e.g. stabilized low-angle side tracking shot) with at most one smooth, subtle secondary adjustment (e.g. gentle tilt-up).

### 3. Keyframe Continuity Chaining (End Frame -> Start Frame)
- **Rule**: In multi-clip workflows, use the final frame (End Frame) of Clip N as the image reference / Start Frame of Clip N+1 whenever possible to maintain 100% spatial and subject continuity.

### 4. Separate UI Settings from Prompt Payload
- **Rule**: Keep aspect ratio (9:16) and duration (e.g. 4s, 6s, 8s, 10s) configured in Google Flow's UI controls, not overloading the text prompt.

### 5. Phantom Limbs & Extra Object Glitches (3rd Shoe / Floating Foot)
- **Root Cause**: Forcing contradictory or compound physical actions (e.g. running while limping, or holding a shoe while wearing shoes).
- **Rule**: Start characters in stable physical choreography (e.g. `BOTH feet firmly planted on the ground`). Add explicit negative guards: `strictly two feet, strictly two shoes total, no floating limbs, no morphing`.

### 6. Accidental Hardsub / Subtitle Bleed
- **Root Cause**: Writing dialogue or VO in ALL-CAPS causes the generative model to treat the text as an on-screen graphic/poster overlay.
- **Rule**: ALWAYS write dialogue and voiceover lines in standard **Sentence case** inside quotation marks (e.g. `"Lari pagi harusnya bikin segar, bukan bikin tersiksa."`).

### 7. Audio Looping & Voice Stutter
- **Root Cause**: Bare `[AUDIO]:` tags without explicit structured section headers cause duration timing miscalculations in Veo audio engines.
- **Rule**: Use the structured `[NATIVE AUDIO DIRECTIVES]` block with explicit `Spoken Dialogue` and `Ambient & SFX` sub-fields. Provide a single Voice Reference ingredient in Flow UI if voice consistency across clips is required.

### 8. Product Commercial Macro Dominance (50%–70% Screen Occupancy)
- **Root Cause**: AI video models default to wide full-body human compositions if framing is not strictly enforced, making the advertised product appear tiny and lost in the background.
- **Rule**: In commercial product ads, explicitly specify framing such that the hero product occupies 50% to 70% of the frame (e.g. `EXTREME MACRO CLOSE-UP`, `GROUND-LEVEL LOW-ANGLE TRACKING`). The product must be the visual hero.

### 9. Narrative Bridge in Transformation Ads (No Sudden Gear Teleportation)
- **Root Cause**: Jumping directly from the problem state (struggling in worn gear) to running in new gear feels jarring and unmotivated.
- **Rule**: Always include a narrative bridge shot or action (e.g. unboxing the sleek shoe box, holding the product, tying clean laces, stepping onto ground) to establish how the character acquired and fitted the solution.

### 10. Anti-Ghost Product Glitch (No Disembodied Detached Objects)
- **Root Cause**: Describing a hero product in the foreground and a human in the background without explicitly connecting them causes diffusion models to generate empty "ghost" products (e.g. empty laced shoes sitting alone on pavement while character stands barefoot/separated behind).
- **Rule**: Always explicitly anchor physical connection: `ACTIVELY WEARING on BOTH feet (strictly two feet inside shoes)` or `ACTIVELY HOLDING firmly with both hands`.

### 11. Formatting Constraint: No LaTeX / Math Delimiters
- **Rule**: Never use LaTeX math symbols (`\rightarrow`, `$$`, `\text{}`). Always use plain text arrows (`->`) and standard formatting to prevent broken rendering on chat platforms.
