# Gemini Context Caching & Quota in OmniRoute

This reference document explains how Google's Gemini-specific features (such as Context Caching) and unified quotas are managed and optimized through the OmniRoute gateway on `n8nserver`.

## 1. Gemini Context Caching

Gemini Developer Console (Google AI Studio) supports **Context Caching**, which caches large inputs (such as books, directories, or kandel codebases) in memory to reduce token costs by up to 90% and speed up response times.

### How it Works in OmniRoute
- OmniRoute's translation layer (`openai-to-gemini.ts`) is designed to look for the `cachedContent` parameter in the client payload.
- If the OpenAI-compatible request includes `"cachedContent": "cachedContents/xxxxxxxxxxxx"`, OmniRoute preserves and forwards this to the Google Gemini API.
- Subscriptions using Google AI Studio / Gemini API keys can leverage this directly when working on large-context tasks.

### Requirements:
- The resource must meet the minimum content limit of **32,768 tokens** (around 24,000 words or 100 pages of text) to trigger caching.
- Caches have a default Time-To-Live (TTL) of 1 hour, which is refreshed automatically with each query using the cache, or can be set manually.

---

## 2. Unified Quotas for Gemini Models

Google AI Studio projects share a unified rate limit across all Gemini model versions (RPM, RPD, or daily token caps). 

### Behavior in OmniRoute
- Quota snapshots tracked by OmniRoute (`quota_snapshots` table) will show identical remaining percentages (e.g. `70.0%`) and the same reset time across all Gemini models (e.g., `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-3.1-pro-high`) for a single connection.
- Pangginaan (usage) of any single Gemini model counts against the account/project limit as a whole. This is normal and reflects Google's project-wide rate limits rather than individual model limits.

---

## 3. Vertex AI Speech & Audio (Google Audio Flash)

OmniRoute supports native audio modality output via Vertex AI (`vertex-gemini-tts` format and `vertexGenerateSpeech` executor).

### Under the Hood:
- It requests the Vertex model with `responseModalities: ["AUDIO"]` and prebuilt voice configuration (e.g., `Aoede`, `Kore`, `Puck`).
- Returns raw PCM L16 audio and converts it to a standard WAV container.

### GCP Project Setup:
- Connections authenticated via desktop/native OAuth (`antigravity` provider) carry the `https://www.googleapis.com/auth/cloud-platform` scope, which allows them to hit Vertex regional API endpoints.
- However, the **Agent Platform API** (`aiplatform.googleapis.com`) must be enabled on the respective GCP projects (e.g., `gleaming-tune-7hnws`, `silken-arcanum-530wt`, or `enhanced-audio-tz266`) in the Google Cloud Console for the request to succeed.
