# Google Flow Domestic Sitcom Production Workflow (Full-Stack Video + Native Audio)

Standard operating procedures for domestic/family comedy sketches and sitcom production using Google Imagen 3 / ChatGPT (GPT-4o), Google Flow / Veo (Full-Stack Video + Audio), Storyboard Maker, and minimal CapCut assembly.

---

## 🚦 Strict Sequential Production Pipeline (Anti-Skipping Rule)

**CRITICAL RULE**: NEVER jump directly from a concept into scene-by-scene prompts. Generative AI models hallucinate faces, props, and room layouts if assets are not locked in advance. Always follow the 3-Phase, 7-Stage pipeline:

```
[Phase 1: Pre-Production & Visual Asset Locking]
  ├── Path A (ChatGPT / Imagen 3):
  │     ├── Stage 1: Character Reference Sheet (8-Module Continuity Sheet & Digital Twin Lock)
  │     ├── Stage 2: Prop Reference Sheet (Key Storytelling Objects Multi-Angle & Swatches)
  │     ├── Stage 3: Location Reference Sheet (Living Room, Porch, Floor Plan Axis, 5500K Light)
  │     ├── Stage 4: Storyboard Plan (Technical Matrix: Shot, Camera, Visual, Native Audio/SFX)
  │     └── Stage 5: Single Keyframe Images per Scene (9:16 Full-Frame Start Images)
  │
  └── Path B (Google Flow Native Tools):
        └── Google Flow > Tools > Storyboard Maker (Auto-binds Character, Prop, & Keyframes)
         ↓
[Phase 2: Full-Stack Generation in Google Flow (Video + Native Audio)]
  ├── Use Single-Frame Keyframe / Storyboard Maker slot as Start Image (I2V)
  └── Execute Scene Prompts (Visual Motion + Native Dialogue/VO/SFX Directives @10s)
         ↓
[Phase 3: Minimal Post-Production (CapCut)]
  └── Stitch 3x 10s clips (30s total), seam trim, and yellow hardsub subtitles
```

---

## 🛑 Critical Rules & User Preferences

### 1. 100% VERBATIM User Script Rule
- If the user provides an existing script, dialogue lines, or character jokes: **DO NOT alter, paraphrase, censor, summarize, or rewrite even a single word**.
- Spoken dialogue in `[NATIVE AUDIO]` directives must match the user's script with 100% verbatim fidelity.

### 2. Google Flow Safety Policy & Filter Evasion
Google Cloud / Flow safety filters frequently block comedy scenes due to false-positive classification:
- ❌ **DO NOT use ALL-CAPS in dialogue** (e.g. `"PAKET! COD TIGA RATUS..."` is flagged as verbal aggression/harassment).
- ❌ **DO NOT use violent/medical shock words**: `"The Ambush"`, `"violently choking"`, `"slamming the mug"`, `"screaming"`.
- ❌ **DO NOT combine personal names, cash amounts, and debt terms** (can trigger debt collection/PII safety flags).
- ✅ **DO USE clean directorial phrasing**: `"The Surprise Arrival"`, `"pauses mid-sip, eyes widening in comedic shock"`, `"gently places mug down"`, `"friendly courier arrival"`.

### 3. Face-Locking & Multi-Panel Sheet Limitation
- **Google Flow / Veo does NOT parse multi-image collage sheets (8-module grids) for facial landmarks**. Uploading an 8-panel collage as an attachment leads to generic AI faces or role-swapping (e.g., wife turning into the delivery courier).
- **The True Fix**:
  1. Generate **Single Full-Frame 9:16 Keyframe Images** per scene in ChatGPT (GPT-4o) and feed each as a **Start Image (I2V)**.
  2. OR use **Google Flow > Tools > Storyboard Maker** where keyframe panels are natively bound to timeline scene slots.

---

## 📺 Genre Styles & Aesthetic Packs

### 1. 1990s Indonesian Retro Sitcom (Si Doel / Lenong Style)
- **Visual Texture**: 1990s analog videotape (VHS) look, warm CRT tube-television color saturation, subtle scanlines, multi-camera sitcom set lighting.
- **Wardrobe & Props**: Sarung kotak-kotak, kaos kutang singlet putih, daster retro motif cerah, rol rambut plastik warna-warni, sandal jepit swallow, kursi rotan antik, cangkir enamel seng lurik.
- **Audio Directives**: Canned studio audience laughter / laugh tracks (`"Hahaha! Woohoo!"`), audience gasps (`"Oooooh!"`), comedic cartoon slides (`"Boing!"`, `"Wah-wah-waaah!"`).

### 2. Modern Everyday Domestic Sitcom
- **Visual Texture**: Clean 1080p live-action cinematic sitcom, warm 5500K morning sunlight, modern Indonesian living room, teak wood furniture, monstera indoor plants.
- **Wardrobe & Props**: Heather grey crew-neck t-shirt, batik floral daster (#F4D03F), geometric wire glasses, leather bifold wallet.
- **Audio Directives**: Natural room tone, ambient street/scooter sounds, clean Indonesian dialogue, internal comical voiceovers.

---

## 🎬 Prompt Template: Google Flow I2V (Scene-by-Scene)

```text
[Genre / Aesthetic Definition, e.g., 1990s Indonesian retro TV sitcom, authentic VHS tape aesthetic, 24fps, 9:16 vertical.]

[MOTION DIRECTIVE]:
[Single dominant camera trajectory: pan, push-in, or tracking]
[Character action: subtle organic breathing, authentic micro-expressions, 180-degree shutter angle motion blur, relaxed kinematic weight. No morphing, no rubbery limbs.]

[NATIVE AUDIO & VOICE]:
- Sound Effects: [Specific realistic SFX + canned laughter if sitcom]
- Ambient Sound: [Room tone / environmental ambience]
- Spoken Dialogue ([Character], [tone/cadence]): "[Exact 100% Verbatim Script Dialogue in Indonesian]"
- Voiceover / Internal Thought: "[Internal comedic monologue if applicable]"
```
