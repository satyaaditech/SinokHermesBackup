---
name: hermes-model-routing
description: Configure Hermes auxiliary vision & image routing.
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos]
---

# Hermes Model Routing & Auxiliary Vision

How to make Hermes auto-analyze user-uploaded images even when the main model
has no native vision (e.g. text-only model behind a custom endpoint), plus the
general mechanics of `auxiliary.*` model config and custom-endpoint probing.

## When to Use

- User asks why photos/screenshots aren't understood, or wants "auto switch to
  a vision model when I upload an image"
- Main model is non-vision and you must wire a vision-capable auxiliary model
- Any task probing which models a custom OpenAI-compatible endpoint (e.g.
  OmniRouter, llama.cpp, vLLM) can actually serve for a given capability
- `vision_analyze` silently returns "No image provided" / "Tidak ada gambar
  terlihat" / "Cannot see image" while the file is a valid image — the
  `auxiliary.vision.model` has drifted to a text-only model (e.g.
  `auto/best-reasoning`, a reasoning alias with no multimodal models). Text-only
  models don't error; they just report they can't see pixels. Confirm with
  `hermes config get auxiliary.vision`, fix with
  `hermes config set auxiliary.vision.model antigravity/antigravity/antigravity/gemini-3.7-flash-low`.
  Never point vision at an `auto/*` reasoning alias — those also leak
  free/noauth fallback models. (`auto/best-reasoning` ≠ `best-reasoning-v2`,
  which is a paid-only custom combo.)
- **Error code: 400 - Ambiguous Model**: If the custom provider/gateway complains that the model is ambiguous (e.g., `Ambiguous model 'gemini-3.7-flash-low'. Use provider/model prefix`), make sure you prepend the correct provider prefix (e.g., `antigravity/antigravity/antigravity/gemini-3.7-flash-low` or `agy/gemini-3.7-flash-low`) in the configuration:
  `hermes config set auxiliary.vision.model antigravity/antigravity/antigravity/gemini-3.7-flash-low`

## 1. How Image Routing Works

`agent.image_input_mode` in `~/.hermes/config.yaml` (`auto` | `native` | `text`,
default `auto`). Decision is made per message turn:

- `native` — attach images as OpenAI-style `image_url` parts. Only correct when
  the main model supports vision (config override `model.supports_vision: true`
  or models.dev metadata).
- `text` — run `vision_analyze` on each image up-front, prepend the description
  to the user's text. The main model never sees pixels.
- `auto` — native if main model supports vision; else, if `auxiliary.vision` is
  **explicitly configured** (provider/model/base_url not auto/empty), route
  through the text pipeline with that backend; else default `vision_analyze`
  flow.

Inbound platform photos (Telegram, etc.) take this exact path, so one config
fixes image uploads across all channels. `vision_analyze` stays available as a
tool in every session regardless.

## 2. Configuring a Vision-Capable Auxiliary Model

Edit with `hermes config set auxiliary.vision.<key> ...` — the patch tool
REFUSES to write `~/.hermes/config.yaml` (security guard on agent config).

```yaml
auxiliary:
  vision:
    provider: custom        # custom | main | openrouter | nous | gemini | codex | auto
    model: <vision-model>
    base_url: http://localhost:20128/v1
    api_key: ${OMNIROUTER_API_KEY}
```

- `provider: main` resolves to the user's actual main provider (handles named
  custom providers correctly). Explicit `base_url`/`api_key` take precedence
  over provider selection.
- `provider: auto` for vision resolves conservatively to known-good vision
  backends (OpenRouter → Nous → main endpoint, etc.) — only works when those
  credentials exist.

## 3. Pitfalls

- **Probe before wiring.** Advertised vision routes can fail at runtime (401
  auth on a combo route, wrong backend, invalid combo name). Test the exact
  model id with a real image via the endpoint's chat API before configuring.
  See `references/vision-image-input.md` for the tiny-PNG probe recipe.
- **No restart needed for config changes.** `load_config()` caches on the
  config file's `(mtime_ns, size)`; once `hermes config set` rewrites the file,
  the running gateway re-reads it on the next call. Do not restart for config
  edits.
- **Gateway restart is blocked from inside the gateway.** `hermes gateway
  restart` (and systemd-run attempts) are refused when invoked from a terminal
  spawned by the gateway — the guard checks `_HERMES_GATEWAY` env + process
  ancestry, and SIGTERM would propagate to child processes. If a restart is
  truly needed, run it from a separate shell outside the gateway.
- **Verify end-to-end in the live gateway** after configuring: call
  `vision_analyze` on a local test image. It exercises the same auxiliary path
  inbound photos use, and proves the config was picked up.
- Env-var references like `${OMNIROUTER_API_KEY}` work in config values.
- **Regression signature → diagnosis.** `vision_analyze` returning "No image
  provided" / "Cannot see image" / "Cannot describe" on a *valid* JPEG means
  `auxiliary.vision.model` drifted to a text-only combo (seen:
  `auto/best-reasoning` after model-override experiments). Fix:
  `hermes config set auxiliary.vision.model antigravity/antigravity/antigravity/gemini-3.7-flash-low`,
  then re-run `vision_analyze` to confirm live pickup (no restart needed).

## Support Files

- `references/vision-image-input.md` — probe recipe, OmniRouter-specific
  findings (which vision model ids actually work), full worked example.
