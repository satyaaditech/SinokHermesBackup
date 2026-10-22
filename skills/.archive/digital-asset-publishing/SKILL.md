---
name: digital-asset-publishing
description: Use when publishing digital assets to itch.io/Gumroad.
---

# Digital Asset Packaging & Marketplace Publishing

A complete guide and workflow for transforming AI-generated assets (video VFX loops, HUD elements, 3D textures, sound effects, UI kits, prompt vaults) into commercially packaged digital products on global marketplaces like **itch.io**, **Gumroad**, **Unity Asset Store**, **Fab (Unreal Engine)**, and **Wirestock**.

---

## 🎯 When to Use
- User wants to monetize AI video/image/audio capabilities into passive digital income streams.
- Packaging raw files (MP4, PNG, WAV, JSON, PDF) into structured digital asset packs.
- Guiding users through marketplace onboarding, listing configuration, cover artwork creation, and pricing.

## 📚 Supporting References
- `references/itch-gumroad-zero-client-guide.md`: Detailed onboarding pacing, Imagen 3 in-image typography cover art prompts, asset resolution/count fidelity rules, and Agent System Instructions.
- `references/wirestock-microstock-syndication.md`: Wirestock 2026 UI navigation (Projects -> Original Raw Video & VFX Video), AI declaration compliance, and Gumroad REST API/webhook automation.
- `references/apify-actors-and-micro-saas.md`: Monetizing cloud bots on Apify Store (Google Maps leads, scraper AI enrichers) & RapidAPI headless micro-SaaS with zero local server risks.

---

## 🧩 The 5-Stage Publishing Lifecycle

```
[1. Asset Production] ──► [2. Quality & Looping Check] ──► [3. Packaging & License] ──► [4. Storefront Listing] ──► [5. Multi-Marketplace Syndication]
```

---

### Stage 1: Batch Asset Production
1. **Targeting High-Demand / Low-Supply Niches:**
   - Seamless Sci-Fi/Cyberpunk HUD terminal loops (for game engine emissive screens & VTuber streams).
   - Magic spell particles & portal VFX loops.
   - Dynamic skybox atmospheres (timelapse nebulas, stormy alien skies).
   - Specialized prompt engineering vaults & structured JSON datasets.
2. **AI Video Prompting Standards:**
   - Always enforce: `static camera`, `seamless loop`, `dark background / high contrast` (for clean Additive/Screen blending), `8k resolution / photorealistic cinematic lighting`.

---

### Stage 2: Quality & Loop Verification
1. Ensure all video clips loop seamlessly without sudden jump-cuts.
2. Formats: Standard H.264 `.mp4` (Full HD 1080p or 4K UHD) for universal compatibility across Unity, Unreal Engine, Godot, Blender, Premiere Pro, and OBS Studio.

---

### Stage 3: Packaging & Automated Bundling
Structure the release folder consistently:
```
<product_slug>/
├── raw_clips/              # Individual generated MP4 files
├── dist/                   # Final output ZIP for buyers
│   └── <Product_Name_Vol1>.zip
├── cover_banner.png        # 1200x630 OpenGraph / Gumroad banner
├── itch_cover_630x500.png  # 630x500 (or 1260x1000) itch.io cover art
├── PROMPTS_MASTER.md       # Generation archive & reproducibility
├── LISTING_COPY.md         # Sales copy, tags, technical specs
├── README_AND_LICENSE.txt  # Commercial royalty-free license
├── generate_cover.py       # Pillow script for banner generation
└── package_builder.py      # Python script to build the release zip
```

---

### Stage 4: Storefront Listing & User Guidance Rules

#### ⚠️ Critical UX & Pacing Rule for First-Time Publishers:
When guiding users who are new to digital marketplaces (e.g. itch.io or Gumroad):
1. **Pace Strictly One Step at a Time:** Do not dump the entire multi-step form at once. Address the active field the user is looking at.
2. **Provide Verbatim Copy-Paste Blocks:** Give exact text strings in code blocks for Title, Tagline, Description, and Tags.
3. **Deliver Exact-Dimension Artwork Natively:** Generate the cover image using code and send it immediately via `MEDIA:<path>` so the user can download and upload it with zero friction.
4. **Key Form Configurations (itch.io Specific):**
   - **Classification:** Select `Game assets` (NOT `Games`).
   - **Kind of project:** Select `Downloadable`.
   - **Release status:** Select `Released`.
   - **Cover Image:** Strictly upload 630x500 (1.26 aspect ratio).
   - **Payment Warning:** Yellow warning banner *"You don't have payment configured..."* is normal during draft stage; connect PayPal/Stripe before public release.

---

### Stage 5: Multi-Marketplace Syndication
* **Instant Direct Stores (Zero Review Wait):**
  - **itch.io:** Ideal for game assets, indie dev tools, VFX.
  - **Gumroad:** Ideal for prompt packs, video bundles, creator overlays.
* **Curated Asset Stores (1–2 Week Review Queue):**
  - **Unity Asset Store & Epic Games Fab:** High-ticket bundles ($29 - $99).
* **Microstock Syndication:**
  - **Wirestock:** Single upload distributes automatically to Adobe Stock, Shutterstock, Pond5, Getty Images, earning USD royalties passively.

---

## 🚫 Common Pitfalls & Solutions

| Pitfall | Impact | Prevention / Fix |
|---|---|---|
| Selecting `Games` instead of `Game assets` on itch.io | Product gets buried in indie video games section | Always set Classification dropdown to `Game assets`. |
| Uploading 16:9 banner into 630x500 itch cover slot | Image gets cropped or letterboxed awkwardly | Generate dedicated 630x500 (or 1260x1000) image. |
| Non-looping video clips sold as "loops" | Negative buyer reviews and refund requests | Enforce cyclic animation prompts + test loop in video player. |
| Complex multi-field guidance overload | User gets overwhelmed | Step-by-step guidance: handle Cover $\rightarrow$ Title $\rightarrow$ Desc $\rightarrow$ Pricing. |
