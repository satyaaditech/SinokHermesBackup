---
name: hybrid-ai-video-pipeline
description: "Use when producing AI commercial and sitcom video."
version: 1.2.0
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
2. **Story Summary First**: Sinox drafts a tight 3-Act Story Summary (Setup -> Escalation/Bridge -> Payoff).
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

### Phase 3: Prompt Execution Modes

#### Mode A: 1-Click Master Agent Mode (Fast Turnaround / Daily Production)
- Single cohesive prompt pasted into Google Flow Agent Mode (`Confirm before generating: Never`).
- Generates 3 sequential 10-second scenes (30s total) automatically.
- Structure per scene (10s blocks):
  ```text
  SCENE [N] (Duration: 00:00 - 00:10) — "[SCENE TITLE]"
  - Setup & Visual: [Action narrative + explicit repetition of Master Lock wardrobe/product/location keywords]
  - Camera: [ONE primary stabilized cinematic movement: Low Tracking, Dolly In, Macro]
  - Lighting: [Consistent motivated lighting setup]
  - [NATIVE AUDIO DIRECTIVES]:
    * Spoken Dialogue ([Character], [tone]): "[Verbatim Dialogue in Indonesian, Sentence Case]"
    * Ambient & SFX: [Layered sound effects matching physical action]
  ```

#### Mode B: Precision Shot-by-Shot Mode (Brand / TV Quality)
- Break the 30s ad into 6–9 modular shots (2s–4s each) following the 36-point format.
- Generate shots individually, select best takes, and assemble in Scenebuilder timeline.

### Phase 4: Surgical Revision Protocol
- If any element drifts (e.g. background color shift, unnatural motion start), revise ONLY the specific broken parameters.
- Re-inject explicit negative constraints (e.g. `strictly NO white cabinets, identical matte petrol-teal only`) into the scene visual block.

## Critical Production Pitfalls & Anti-Glitch Rules

### 1. Product Dominance & Screen Occupancy (50%–70% Macro Priority)
- **Root Cause**: AI defaults to full-body wide shots where the product appears tiny and insignificant.
- **Rule**: In product commercials, the hero product MUST occupy at least 50% to 70% of the frame in macro/low-angle close-ups. Keep human figures in soft focus or secondary framing.

### 2. Narrative Bridge vs Instant Teleportation
- **Root Cause**: Jumping directly from suffering/struggle (Scene 1) to effortlessly using/wearing the new product (Scene 2) feels disjointed and unnatural.
- **Rule**: Include a physical discovery/bridging action: unboxing, holding the hero item, examining the packaging, or tying laces before launching into full performance.

### 3. Hard Cut Editorial Transformation vs Generative Morphing
- **Root Cause**: Requesting literal dynamic visual transformation/morphing within a single clip causes generative models to hallucinate melting geometries, rubbery deformations, and hybrid half-old/half-new artifacts.
- **Rule**: NEVER ask the AI to morph products or characters. Clip 1 strictly ends on the old asset; Clip 2 strictly begins with the new hero asset already fully worn/formed. Let the video cut do the transformation, not diffusion physics.

### 4. Single Primary Camera Movement per Clip
- **Root Cause**: Compounding multiple camera moves in a single short clip (e.g. tracking -> dolly-in -> crane -> 360-orbit) destabilizes frame generation and introduces severe warping or extra limbs.
- **Rule**: Limit each clip to ONE primary stabilized camera movement (e.g. stabilized low-angle side tracking shot) with at most one smooth, subtle secondary adjustment (e.g. gentle tilt-up).

### 5. Phantom Limbs & Extra Object Glitches (3rd Shoe / Floating Foot)
- **Root Cause**: Forcing contradictory or compound physical actions (e.g. holding a shoe while wearing shoes, or sitting while running).
- **Rule**: Start characters in stable physical choreography (e.g. `ALREADY SEATED on the bench, BOTH feet firmly planted on the ground`). Add explicit negative guards: `strictly two feet, strictly two shoes total, no floating limbs, no morphing`.

### 6. Accidental Hardsub / Subtitle Bleed
- **Root Cause**: Writing dialogue or VO in ALL-CAPS causes the generative model to treat the text as an on-screen graphic/poster overlay.
- **Rule**: ALWAYS write dialogue and voiceover lines in standard **Sentence case** inside quotation marks (e.g. `"Lari pagi harusnya bikin segar, bukan bikin tersiksa."`).

### 8. Disembodied / Ghost Product Placements
- **Root Cause**: Prompts describing products and humans in separate layers (e.g. "shoes planted in foreground while runner stands in background") cause generative models to render empty, unattached products (empty shoes without feet inside).
- **Rule**: When subjects and wearable products co-exist, explicitly dictate that the subject is `ACTIVELY WEARING the [Product] on BOTH feet` (or body) with `strictly two feet inside the shoes`, or `firmly holding [Product] with hands`. Add negative constraint: `no empty shoes, no disembodied products, no ghost accessories`.

### 9. Telegram Markdown Formatting (Strictly NO LaTeX)
- **Root Cause**: Mathematical/LaTeX notation (`\rightarrow`, `$$`) renders as broken escape sequences in Telegram.
- **Rule**: Strictly use plain text characters (`->`, `-`). Never emit LaTeX formatting in scripts, prompt sheets, or summaries.
