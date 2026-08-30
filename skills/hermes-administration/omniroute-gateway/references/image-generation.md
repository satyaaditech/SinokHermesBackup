# OmniRoute Image Generation (/v1/images/generations)

This reference outlines how to query and troubleshoot image generation via the local OmniRoute proxy endpoint on `http://localhost:20128/v1/images/generations`.

---

## 1. Request Format

OmniRoute supports normal OpenAI-compatible parameters:
```json
{
  "model": "antigravity/gemini-3.1-flash-image",
  "prompt": "prompt details here",
  "n": 1,
  "size": "1024x1024"
}
```

---

## 2. Supported Providers & Models

Built-in image providers are registered in `open-sse/config/imageRegistry.ts`. Active local providers:

### Antigravity (Google Gemini API via OAuth)
* **Model ID**: `antigravity/gemini-3.1-flash-image`
* **Format**: `gemini-image` (Internal translation to Google's internal internal:generateContent endpoint)
* **Sizes**: `1024x1024`

---

## 3. Troubleshooting & Common Errors

### "Invalid image model: X. Use format: provider/model"
* **Cause**: This error occurs when the provider prefix in the `model` string (e.g. `veo-free` in `veo-free/veo`) is not recognized in `IMAGE_PROVIDERS` inside `open-sse/config/imageRegistry.ts`.
* **Fix**: Ensure the model string maps to a registered provider key (like `antigravity` or `openai`).
