# itch.io & Gumroad Zero-Client Asset Publishing Reference

## 1. Step-by-Step Onboarding & Pacing Rules
- **Beginner Pacing ("15-Year Old Rule"):** Break down marketplace onboarding into bite-sized turns ("satu per satu"). Do not dump the entire form in one message.
- **Form Columns Breakdown:**
  - **Left Column:** Title -> Short Tagline -> Classification (Default is often `Games` -> change to `Game assets`) -> Project Kind (`Downloadable`) -> Release Status (`Released`).
  - **Right Column:** Cover Image upload (Aspect Ratio 1.26:1 or 630x500 / 1260x1000) -> Screenshots / Preview GIFs.
  - **Pricing & Files:** Pricing tier (`$0 or donate` with suggested price during setup, or `Paid`), Uploads (distributable `.zip`), Description (HTML/Markdown specs + Game engine setup guide).

## 2. Store Cover Art Generation (Imagen 3 / Gemini Prompting)
Do not use crude programmatic Pillow banners for final storefront listings. Always generate 3D cinematic Octane render cover art with in-image typography via Imagen 3 / Gemini:
- **Environment Prompting:** Dark cyberpunk laboratory / starship cockpit, floating neon cyan & magenta holographic HUD panels, reflective glass surfaces, volumetric blue lighting, shallow depth of field, 8k resolution.
- **Integrated Typography:** Put exact titles and badges in double quotes:
  - `"SCI-FI HUD PACK"`
  - `"10 SEAMLESS FULL HD VIDEO LOOPS"`
  - `"100% SEAMLESS LOOPS"` • `"FULL HD 1080P"` • `"UNITY • UNREAL • GODOT"` • `"COMMERCIAL LICENSE"`

## 3. Strict Truth in Advertising & Asset Matching
- **Resolution Fidelity:** If raw assets are 1080p, explicitly label them as `Full HD 1080p` across copy and cover art (do not claim 4K if files are 1080p).
- **File Count Fidelity:** If the pack promises 10 loops, generate and verify all 10 clips before assembling the final distributable ZIP and publishing.

## 4. Gumroad Editor Specifics & Automation (API / CLI)
- **Slug & URL Optimization:** Always replace the randomly generated slug (e.g. `atoiq`) with a clean descriptive product slug (e.g. `scifi-hud-vfx-pack`) so the URL becomes `username.gumroad.com/l/scifi-hud-vfx-pack`.
- **Form Layout & Tab Flow:**
  - **Product Tab:** Title, Description (rich text/markdown with engine setup), Cover (16:9 min 1280x720), Thumbnail (1:1 square min 600x600), Call to Action (`"I want this!"`), Summary (1-line punchy benefit string), Price in USD.
  - **Content Tab:** This is where the actual downloadable `.zip` file is attached. Do not look for file upload inside the main Product description tab.
- **Gumroad REST API & Webhook Automation:**
  - Token access under `Settings -> Advanced -> Create an application`.
  - API endpoint: `POST https://api.gumroad.com/v2/products` with `access_token` to programmatically publish new asset packs without manual browser clicks.
  - Webhooks: Forward Gumroad `sale` ping to n8n / Telegram bot for instant real-time sales notifications ("Kring! New purchase: $9.99 from US").

## 5. Agent System Instructions
Set Google AI / Veo system instructions to:
```text
You are an elite 3D VFX technical artist specializing in sci-fi video game UI, cyberpunk holograms, and seamless cyclic loops for game engines.
```
