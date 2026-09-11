# n8n AI Assistant & OmniRoute Compatibility Adapter

## Architecture Overview
n8n's built-in **AI Assistant** (powered by Vercel AI SDK `@ai-sdk/openai-compatible`) verifies and connects to OpenAI-compatible endpoints by issuing non-streaming `POST /v1/chat/completions` requests.

### The Root Cause
1. When validating models during setup, n8n sends JSON payloads without an explicit `"stream": false` field (relying on the OpenAI default behavior where `stream` is false).
2. OmniRoute by default handles any request missing `stream: false` as a Server-Sent Events (`text/event-stream`) stream.
3. n8n's SDK expects standard `application/json` and immediately fails with `JSONParseError: Unexpected token 'd' ("data: ...")` / `The service returned an unexpected response`.
4. In addition, frontier reasoning models with long initial `reasoning_content` can exhaust n8n's verification token budget (`maxOutputTokens: 16`) before producing visible content.

## Solution: Port 20129 Adapter
The script `/home/satyaaditech/scripts/omniroute_n8n_adapter.py` acts as a lightweight proxy:
- **Port**: `20129` (accessible from Docker container `n8n_app` as `http://172.17.0.1:20129/v1`)
- **Forward Target**: `http://127.0.0.1:20128` (OmniRoute Gateway)
- **Logic**: Inspects incoming POST requests to `/v1/chat/completions`. If `stream` is not present in the body, it automatically injects `"stream": false` before forwarding, guaranteeing clean JSON responses for non-streaming callers while preserving native SSE streaming when `stream: true` is requested.

## Setup Values for n8n Modal ("Connect a model")
- **Provider**: `Self-hosted or OpenAI-compatible endpoint`
- **Base URL**: `http://172.17.0.1:20129/v1`
- **API Key**: `sk-omniroute` (or any string)
- **Model**: `antigravity/gemini-2.5-flash` (fast, non-thinking), `daily-chat`, or `antigravity/gemini-3.1-pro-low`.
