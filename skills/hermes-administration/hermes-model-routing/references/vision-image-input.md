# Vision Model Probing & Worked Example

Session-specific detail behind `hermes-model-routing`. Verified on
Satya's setup (OmniRouter at localhost:20128, ~2026-08).

## 1. Tiny-PNG Probe Recipe

Probe a candidate vision model BEFORE wiring it into `auxiliary.vision`.
Generate a solid-color PNG, base64 it, and POST one chat completion with an
`image_url` data part. If it answers the color, vision works end-to-end.

```bash
# 1) create 4x4 solid red PNG, base64 to /tmp/test_red.png.b64
python3 -c "
import base64, struct, zlib
def chunk(t, d):
    c = t + d
    return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
ihdr = struct.pack('>IIBBBBB', 4, 4, 8, 2, 0, 0, 0)
raw = b''.join(b'\x00' + b'\xff\x00\x00' * 4 for _ in range(4))
png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')
print(base64.b64encode(png).decode())
" > /tmp/test_red.png.b64

# 2) probe each candidate model id
B64=$(cat /tmp/test_red.png.b64)
for M in "auto/vision" "antigravity/gemini-3.5-flash-low"; do
  echo "=== $M ==="
  curl -s --max-time 45 http://localhost:20128/v1/chat/completions \
    -H "Authorization: Bearer $OMNIROUTER_API_KEY" -H "Content-Type: application/json" \
    -d "{\"model\":\"$M\",\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"What color is this image? Answer in one word.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,$B64\"}}]}],\"max_tokens\":100}" \
    | head -c 600; echo
done
```

Use `jq -r .choices[0].message.content` (or the streaming `data:` lines) to
read the answer.

### Probing pitfalls (hit 2026-08-13, real tensi photo)

- **Shell arg limit.** A full-size photo (~100 KB JPEG → ~136 KB base64)
  breaks the `$B64`-in-`curl -d` pattern above with
  `curl: Argument list too long`. Use a `python3 -c` one-liner instead: read
  the file in-process, base64 it, and POST via `urllib.request` — no giant
  shell variable.
- **Probe from `terminal`, not `execute_code`.** The `execute_code` sandbox
  does NOT inherit `OMNIROUTER_API_KEY` (raises `KeyError`); the terminal
  shell does. Read the key from `os.environ` inside a terminal-run python.
- **OmniRoute streams by default.** The chat/completions reply arrives as SSE
  (`data: {...}` lines) even when `stream` is not requested — a plain
  `json.loads(raw)` on the body raises `JSONDecodeError`. Parse `data:` lines
  (skip `[DONE]`), concatenate `delta.content`, or set `"stream": true` and
  iterate the same way.

## 2. OmniRouter-Specific Findings (verified 2026-08)

OmniRouter advertises many `auto/*-vision` combos, but the auto combos route to
the OpenCode free-tier pool and returned `[401]: Model ...-free is not
supported` — e.g. `auto/best-vision`, `auto/vision`, `auto/multimodal`
(attempt order showed `oc/qwen3.6-plus-free`, `oc/minimax-m3-free`).
`auto/gemini` was an invalid combo (`bad_request`).

Working, verified vision route on this endpoint:

```
antigravity/gemini-3.5-flash-low   → answered "Red." for the red PNG
```

Also listed with vision capability (`/v1/models` capabilities.vision=true):
`antigravity/gemini-3.1-pro-low/high`, `antigravity/gemini-2.5-flash*`,
`antigravity/gemini-3.1-flash-lite`, `openrouter/nvidia/*:free`,
`openrouter/google/gemma-4-26b-a4b-it:free`, etc.

Rule: model lists lie less than endpoints — always re-probe before relying on
a route; free-tier pools change auth/availability frequently.

## 3. Final Working Config (this setup)

```yaml
agent:
  image_input_mode: auto
auxiliary:
  vision:
    provider: custom
    model: antigravity/gemini-3.5-flash-low
    base_url: http://localhost:20128/v1
    api_key: ${OMNIROUTER_API_KEY}
```

Applied via:

```bash
hermes config set auxiliary.vision.provider custom
hermes config set auxiliary.vision.model antigravity/gemini-3.5-flash-low
hermes config set auxiliary.vision.base_url http://localhost:20128/v1
hermes config set auxiliary.vision.api_key '${OMNIROUTER_API_KEY}'
```

## 4. Verification Steps (in order)

1. **Resolver check** (fresh process reads fresh config):
   ```bash
   cd ~/.hermes/hermes-agent && venv/bin/python -c "
   import sys; sys.path.insert(0, '.')
   from agent.auxiliary_client import resolve_vision_provider_client
   prov, client, model = resolve_vision_provider_client()
   print('provider:', prov); print('model   :', model)
   print('client  :', type(client).__name__ if client else None)"
   ```
   Expect `provider: custom`, `model: antigravity/gemini-3.5-flash-low`,
   `client: OpenAI`.
2. **Live-gateway test**: call `vision_analyze` tool with a local image path
   (`/tmp/test_red.png`). Success proves the running gateway re-read config
   (mtime cache) and the auxiliary path works — same path inbound photos use.

## 5. Internal Details Worth Knowing

- `agent/image_routing.py` — `decide_image_input_mode()`,
  `_lookup_supports_vision()`, `extract_image_refs()` (regexes for local paths
  and image URLs).
- `agent/auxiliary_client.py` — `resolve_vision_provider_client()`; explicit
  `base_url`/`api_key` overrides take precedence; `provider: main` resolves via
  `_read_main_provider()`; `_resolve_task_provider_model()` reads the
  `auxiliary.<task>` section from `load_config()`.
- `hermes_cli/config.py` — `load_config()` caches on `(mtime_ns, size)` of
  `config.yaml`, so file changes are live without gateway restart. Edit with
  `hermes config set` (the patch tool refuses to write the config file).
- Gateway restart guard lives in the CLI; it refuses restart/stop from inside
  the gateway process (`_HERMES_GATEWAY` env marker + ancestry check; a
  `systemd-run --user` bypass is also blocked because the terminal tool spawns
  under the gateway). Restart from a separate shell when required.
