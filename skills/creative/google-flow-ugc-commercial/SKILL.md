---
name: google-flow-ugc-commercial
description: "Use when creating commercial UGC video via Google Flow."
version: 1.0.0
author: Sinox Agent
license: MIT
metadata:
  hermes:
    tags: [ugc, commercial, google-flow, veo, storyboard, character-sheet, product-sheet, master-prompt]
    category: creative
---

# Google Flow AI Commercial & UGC Creative Director Workflow

Standard Operating Procedure (SOP) for producing commercial packages and UGC video ads for modern audiences using the 11-Stage Strict Sequential Production Pipeline for Google Flow Agent Mode.

## When to Use
- Producing commercial ads, UGC videos, and product showcase packages for modern audiences.
- Executing the strict 11-stage sequential AI video production pipeline for Google Flow Agent Mode.
- Ensuring asset separation across Character, Product, Location reference sheets, and Storyboards.

## Core Production Principles
1. **Strict Sequential Workflow**: Each stage is executed strictly one by one. Never skip, never merge stages, never predict future stages early.
2. **Narrative Summary First**: ALWAYS present a clear 3-act story summary / problem-solving narrative flow before generating the detailed prompt.
3. **Strict Scene Cohesion & Continuity**:
   - Scenes must flow logically in space, time, and theme (no random environment jumping, e.g. city traffic to mountain).
   - The product MUST act as a clear problem solver with emotional/practical payoff.
   - Avoid "AI-generated look" by ensuring continuous grounded reality.
4. **Absolute Asset Separation**: Exactly 4 standalone visual reference assets (NEVER combined into one image):
   - Asset 1: Character Reference Sheet Image
   - Asset 2: Product Reference Sheet Image
   - Asset 3: Location Reference Sheet Image
   - Asset 4: Complete Storyboard Image
3. **Current Stage Only**: Never generate storyboard or script in reference sheet stages.

## The 11 Production Stages

### Stage 1: Character Reference Intake + Character Sheet + Lock
- Ask ONLY: "Do you already have a character image you want to use?" (YES / NO)
- Never invent a character if user chooses NO; wait or proceed without inventing.
- Analyze user image: face structure, features, skin tone, eye color, jawline, hair, body type, proportions.
- Produce detailed Character Sheet (text) + 1 separate High-Quality Character Reference Sheet Image (multi-angle/expression).
- LOCK Character Identity (face, hair, age, body, clothing).

### Stage 2: Product Reference Intake + Product Sheet + Lock
- Ask ONLY: "Do you already have a product image you want to use?" (YES / NO)
- Preserve 100% exact: shape, dimensions, materials, colors, finish, buttons, displays, logos, branding text.
- Produce detailed Product Sheet (text) + 1 separate High-Quality Product Reference Sheet Image.
- LOCK Product Design.

### Stage 3: Location Reference Intake + Location Sheet + Lock
- Ask ONLY: "Do you already have a location image you want to use?" (YES / NO — Create location yourself)
- If user provides: preserve architecture, layout, lighting, materials.
- If user selects NO: AI designs modern, premium commercial location.
- Produce detailed Location Sheet (text) + 1 separate High-Quality Location Reference Sheet Image.
- LOCK Location.

### Stage 4: Generate 10 Commercial Concepts
- ONLY after Stage 1, 2, 3 are locked.
- Generate exactly 10 original commercial concepts tailored for US audience (Text only).
- Fields per concept: Product, Campaign Title, Strong Hook, Problem/Desire, Solution, Payoff, Brand Message, Visual Style.
- Ask ONLY: "Which commercial do you want to create?" -> STOP.

### Stage 5: User Selects Concept
- User picks 1 concept -> LOCK Concept.

### Stage 6: Duration Selection
- Ask ONLY: "What duration do you want?" (15s / 30s / 45s / 50s / 60s) -> STOP.

### Stage 7: Write Commercial Script
- Text only. Structure: Hook -> Problem/Desire -> Product -> Experience -> Benefit -> Payoff -> Brand Message.
- Natural contemporary English, concise dialogue, voiceover only when helpful. Animals never speak.

### Stage 8: Create Storyboard Plan (Text/Table)
- Verify 6 prerequisites exist (Character, Product, Location, Concept, Duration, Script).
- Table columns: Shot #, Duration, Main Action, Character Present, Product Present, Location, Dialogue/VO, Camera, Continuity Notes.
- For 50-60s: ~8-12 shots.

### Stage 9: Create Complete Storyboard Image
- ONE single separate storyboard image displaying all panels in sequential order (Shot 1 -> Shot N).

### Stage 10: Final Consistency Check
- Audit Character, Product, Location, Story, and Visual Style across all 4 separate visual assets.
- If any asset contains another, regenerate ONLY that incorrect asset.

### Stage 11: Final Flow AI Agent Master Prompt
- Unified master prompt instructing Google Flow Agent Mode to treat the 4 images + script + storyboard as the authoritative ground truth.
- Multi-part video continuity rules (Part 1 -> Part 2 -> Part N) preserving seamless visual & temporal flow.
- Animal rules: natural sounds/actions only, never speak human language.
- Visual style: default to premium cinematic live-action.

---

## Direct Master Agent Pipeline (UGC & Commercial Ads SOP)

Optimized high-speed workflow for commercial product ads and UGC videos without manual image-by-image assembly.

### 1. Pre-Production Protocol (Strict Order)
1. **Story Summary First**: Sinox provides a concise 3-act story outline demonstrating the product as a clear problem solver (Setup -> Fluid Bypass/Experience -> Payoff/Brand Message).
2. **User Approval (ACC)**: Wait for user confirmation before authoring full technical prompts.
3. **Master Agent Prompt Generation**: Full prompt generated using dual-language standard or English commercial standard.

### 2. Storyboard Studio Zero-Friction Workflow
1. Paste prompt into **Storyboard Studio** to generate visual panels (Hero Character, Hero Product, Commercial Location, Storyboard).
2. Use **"Select All" -> "Add as Reference"** globally (bypasses tedious manual `@` tagging per scene).
3. Set Google Flow: `Confirm before generating: Never`.
4. Render 3 sequential clips (10s each = 30s total) automatically in continuous pass.

### 3. Surgical Revisions Rule
- Modify ONLY the specific broken elements (e.g. motion stability, specific clothing/product keywords repeated inside scene visual blocks to prevent AI amnesia). Keep working sections untouched.
