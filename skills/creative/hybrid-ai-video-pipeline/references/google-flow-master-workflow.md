# Google Flow & Veo Master Workflow Bible

Complete, authoritative 36-Point Production Blueprint & 10 Golden Rules for High-End Commercial Ads & Episodic Video in Google Flow / Veo.

---

## The Core Philosophy: Generate Shots, Not Films
Film -> Sequence -> Scene -> Shot -> Generation

---

## 1. The 5 Visual Bible Master Assets (Pre-Production)
1. **@HeroCharacter**: Single clean reference (face, hair, skin tone, body proportions, exact wardrobe, smartwatch).
2. **@HeroProduct**: Clean segmented reference on plain background (silhouette, mesh texture, sole gradient, lateral logo, sole thickness).
3. **@Location**: Clean environmental reference (path, trees, bridge, skyline, morning mist) with NO random subjects.
4. **@Lighting**: Dedicated lighting anchor (6:00 AM low-angle golden hour, soft backlight, motivated rim light).
5. **@Style**: Cinematic commercial look (photorealistic, natural skin texture, realistic biomechanics, motivative depth of field).

---

## 2. Master Shot Prompt Formula
```text
PROJECT: [PROJECT NAME]
SHOT: [SHOT NUMBER]
SHOT PURPOSE: [What this shot communicates]

REFERENCE ASSETS:
@Character
@Product
@Location
@Style
@Voice

SUBJECT: [Who / what is visible]
IDENTITY LOCK: [Face / appearance / design that must remain constant]
WARDROBE: [Exact clothing and accessories]
PRODUCT: [Exact product details]
LOCATION: [Physical environment]
TIME: [Time of day]
WEATHER / ATMOSPHERE: [Atmospheric conditions]
LIGHTING: [Motivated source, direction, quality, color]
COMPOSITION: [Wide / Medium / Close-up / Macro]
CAMERA: [Camera placement]
CAMERA MOVEMENT: [ONE primary stabilized motion + ONE subtle secondary adjustment]
LENS / OPTICAL FEEL: [DOF motivated by shot purpose]
ACTION: [Specific physical movement]
PHYSICS: [Biomechanics, shoe-ground contact, foam compression & rebound]
FACIAL PERFORMANCE: [Emotion and expression]
MATERIAL BEHAVIOR: [Fabric movement, mesh reflection, rubber grip]
AUDIO: [Layered Foley, Ambience, Music, Impact]
DIALOGUE / VO: "[Exact spoken line in Sentence Case]"
ENDING FRAME: [Exact visual state where clip ends]
CONTINUITY: [What must match adjacent shots]
CONSTRAINTS: [Strict negative guards: no extra limbs, no extra shoes, no morphing, no UI/text]
VISUAL STYLE: [Cinematic sports commercial]
```

### Quick Formula:
`WHO + WHAT + WHERE + WHEN + HOW + CAMERA + LIGHT + SOUND`

---

## 3. The 10 Golden Rules of Google Flow Production
1. **Generate Shot, Not Film**: Break 30s ads into 6–9 modular shots (2s–4s each).
2. **Reference > Description**: Visual ingredients (@Product, @Character) beat text adjectives for geometry and logo consistency.
3. **One Camera Language per Shot**: 1 primary stabilized movement. No compound chaotic moves.
4. **Image-First for Critical Composition**: Text -> Image first to lock framing and assets, then Image/Frame -> Video.
5. **Keyframe Chaining (Start/End Frames)**: Use End Frame of Clip N as Start Frame of Clip N+1 for critical physical transitions.
6. **Hard Cut Editorial over Generative Morphing**: Never ask diffusion models to morph products or anatomy. Cut from old to new.
7. **Describe Physics & Biomechanics**: Foam compression, realistic foot strike, inertia, weight transfer.
8. **Separate Identity, Action, Camera, and Audio**: Keep prompt blocks modular so the model isolates parameters cleanly.
9. **Assemble in Scenebuilder**: Generate multiple takes, save best takes, trim and arrange in timeline.
10. **Upscaling is Finishing**: 1080p/4K upscale polishes good motion; it cannot fix broken anatomy, drift, or bad physics.

---

## 4. Lighting Progression Matrix (Emotional Visual Arc)
- **Shot 01 (Fatigue)**: Cool early-dawn blue/grey ambient light.
- **Shot 02 (Struggle)**: Neutral early morning, muted lighting.
- **Shot 03 (Product Reveal)**: First warm golden light breaking through trees.
- **Shot 04 (Performance/Impact)**: Strong golden-hour side highlights on sole and mesh.
- **Shot 05 (Confidence/Stride)**: Bright energetic morning light, motivated sun flares.
- **Shot 06 (Payoff Hero)**: Dramatic golden sunrise backlight, soft city skyline rim lighting.

---

## 5. Quality Control (QC) Checklist Before Final Cut
- [ ] **Character**: Face identical, hair stable, wardrobe identical, watch on LEFT wrist.
- [ ] **Product**: Mesh, sole gradient, logo placement, and geometry 100% match reference.
- [ ] **Anatomy**: Strictly 2 legs, 2 feet, 2 shoes, realistic 5-finger hands, no phantom mass.
- [ ] **Physics**: Ground contact solid, no floating, no sliding, foam compression realistic.
- [ ] **Camera**: Stable horizon, plausible physical trajectory, no teleporting focal lengths.
- [ ] **Environment**: Consistent architecture, consistent sun angle, no random crowds/vehicles.
