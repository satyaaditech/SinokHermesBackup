---
name: ai-ugc-video-production
description: Use when creating viral realistic AI UGC videos or ads.
category: creative
---

# AI UGC Video Production & Delivery Pipeline

A complete production standard for creating high-converting, realistic AI User-Generated Content (UGC) videos and ads across TikTok, Instagram Reels, and YouTube Shorts.

---

## 🎯 1. Core Production Philosophy (The 2025/2026 Viral Playbook)

1. **The "Zero-Polish" Imperfection (Anti-Uncanny Valley)**:
   - Audiences immediately swipe away overtly polished, studio-lit commercial videos within the first 2 seconds.
   - Viral AI UGC must simulate **raw handheld smartphone capture (iPhone 15 Pro)**: subtle natural camera shake, realistic skin texture and micro-blemishes, authentic bedroom/office window lighting, and casual everyday attire.
2. **Conversational Audio Layering**:
   - Never use monotonous robotic voiceovers. Incorporate natural micro-breaths, slight pauses (`...`), sigh markers, and relatable colloquial phrasing.
   - Always mix subtle background ambient room tone or lo-fi sound effects (foley: mouse clicks, keyboard taps, coffee cup clinks, desk thuds).
3. **Pacing & Pattern Interrupts (3–5 Second Rule)**:
   - Shift the visual frame every 3 to 5 seconds: punch-in zooms (5–10%), cuts between A-Roll (talking head) and B-Roll (first-person POV hands/screen), or dynamic kinetic text highlights.

---

## 🎬 2. The 7-Act High-Retention UGC Storytelling Structure (60s – 180s)

For long-form UGC videos (up to 3 minutes / 180s) that maintain high watch time:

* **Act 1: The Anti-Ad Whistleblower Hook (00:00 – 00:15)**
  - Direct confessional or contrarian statement breaking scrolling habits ("Jujur gue bikin video ini rada takut...", "Masalah lo bukan males, otak lo lagi overload").
* **Act 2: The Raw Vulnerability / Shared Struggle (00:15 – 00:45)**
  - Relatable pain point illustrated with concrete artifacts (e.g., hundreds of forgotten voice memos, cluttered desktop with 40 tabs).
* **Act 3: The Skeptical Discovery (00:45 – 01:15)**
  - Creator expresses genuine prior skepticism to disarm audience defense ("Gue kira cuma AI gimmick receh...").
* **Act 4: Live Demo & The "Aha!" Moment (01:15 – 01:50)**
  - Concrete visual proof: showing input transformed into clean actionable output within seconds.
* **Act 5: Objection Handling (01:50 – 02:25)**
  - Why existing alternatives fail (e.g., why complex Notion setups or paper journals get abandoned during busy sprints).
* **Act 6: Emotional Identity Payoff (02:25 – 02:45)**
  - Focus on life transformation, not software features (e.g., closing laptop at 6 PM without dread, guilt-free evenings).
* **Act 7: Low-Pressure CTA & Seamless Loop (02:45 – 03:00)**
  - Casual call-to-action ("coba mumpung versi beta gratis...") and a verbal transition looping back into the opening hook.

---

## ⚙️ 3. Execution & Delivery Architecture (Dual-Tier Pipeline)

When a user requests a **ready-to-upload video ("video siap upload")**, never stop at text prompts or storyboard outlines. Execute or clarify according to host capability:

### Tier 1: Motion-Cinematic MP4 (Self-Hosted CPU / Server Render)
Use this tier when rendering locally on CPU-only machines (e.g. Ubuntu server without dedicated GPU):
1. **Photorealistic Visuals**: Generate 9:16 vertical frames (1024x1792) via OmniRoute (`antigravity/gemini-3.1-flash-image`) with fixed character and scene prompts.
2. **Conversational Voiceover**: Generate audio via Edge-TTS (e.g. `id-ID-ArdiNeural` or equivalent) with balanced pitch and conversational tempo.
3. **Dynamic Centered Captions**: Generate frame-accurate ASS subtitles rendered inside a translucent dark contrast overlay card (Alignment=5 / Montserrat font with dual-tone highlights).
4. **FFmpeg Motion Synthesis**: Assemble clips using subpixel bicubic perspective motion (Ken Burns zoom in/out, handheld sway) and 1.0s cross-dissolves (`xfade=transition=fade`).
5. **Output**: Deliver the compiled `.mp4` file via Telegram markdown `MEDIA:/path/to/video.mp4`.

### Tier 2: Full-Motion Talking-Head Avatar (GPU / Cloud API Delegation)
Use this tier when the user explicitly requires full-motion facial lip-sync and dynamic body gestures:
1. **Master Anchor Frame**: Generate character anchor portraits via Flux.1 or Midjourney v6.1 (`--cref`).
2. **Motion Generation**: Animate using Kling AI 1.5, Hailuo (Minimax), or Runway Gen-3 Image-to-Video with low-to-medium motion amplitude (3–4/10).
3. **Lip-Sync**: Sync facial phonemes with Hedra Character-2 or LivePortrait.
4. **Compute Delegation**: Delegate heavy video rendering to dedicated GPU nodes (e.g. ASUS ROG / Sinox) or cloud API endpoints.

---

## ⚠️ 4. Critical Pitfalls & Rules

* **Action over Narration for "Siap Upload"**: When the user asks for a ready-to-upload video, deliver a concrete executable `.mp4` file or explicitly present the Tier 1 vs Tier 2 execution choice. Never reply with just prompt instructions.
* **Avoid High Motion Amplitude in Video Diffusion**: Excessive motion prompts cause character facial warping and limb melting. Restrict camera movement to subtle handheld sway, slow zoom, or static framing.
* **Never Skip Audio Layering**: Clean studio-grade dry voiceovers sound synthetic. Always include room tone, subtle foley SFX, or gentle background music.
* **Keep Scripts Conversational**: Avoid marketing jargon and textbook prose in UGC dialog. Mirror natural speech patterns with colloquial vocabulary, rhetorical questions, and pause markers.
