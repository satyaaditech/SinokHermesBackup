---
name: run-skill-scripts-without-cli
description: Use when a skill script has no CLI and needs a temp wrapper.
---

# Running Hermes skill scripts that lack a CLI entry point

Some packaged skill scripts (e.g. `scripts/publish_renungan.py`, `scripts/render_cover.py` under a Pangestu/Youtube/medal skill) define pure Python functions but have **no `if __name__ == "__main__"` guard**, so `python3 scripts/x.py` does nothing. This skill documents the wrapper pattern and the pitfalls hit while executing them end-to-end.

## Trigger
- A skill's `references/` doc says a script exists, but `python3 path.py` produces no output.
- You need to call a library-style function (upload, render, publish) from a skill script and it won't run standalone.

## How to run (the wrapper pattern)

1. Inspect the script to read the exact function signatures (params + order).
2. Write a temp wrapper at `/tmp/run_*.py` that:
   - `sys.path.insert(0, "<skill>/scripts")` (so the plain module name imports),
   - `from <module> import <function>` (NOT `import whole_script` — that only binds the module),
   - calls the functions/templates you need.
3. Run `python3 /tmp/run_*.py`.

## Pitfalls discovered (hard-won)

1. **`[DOC_URL]` placeholder**: the publish flow (e.g. `publish_renungan.publish`) replaces a literal `[DOC_URL]` token in your template string with the real Google Doc URL, then writes it into the output `.md`. If your template does NOT contain `[DOC_URL]`, the `.md` is silently written fine but the published Doc link is missing from the local file after upload. **Always include `[DOC_URL]` on the closing line of each template** so the local copy carries the final link.
2. **Long-running subprocesses** (TTS `edge-tts` → `ffmpeg` conversion to Opus) can exceed the default 60s foreground terminal timeout when the full text is long (~5+ min of audio). Run the wrapper with a generous `timeout` (e.g. 300), or in the background with `notify_on_complete=true`. A 60s timeout mid-run does NOT necessarily mean failure — check `/tmp/*_temp.mp3` / `.ogg` artifacts and the Drat output before concluding it failed.
3. **Stderr dump on ffmpeg**: ffmpeg prints its banner/config to stdout/stderr — that's normal, not an error. Look at the tail of output/log for the final status line.
4. **Verify by reading the written artifact** (the `.md` and generated images), not just the script exit code — the upload/`sendVoice` HTTP calls are fire-and-forget `requests.post` with no status check.
5. When the same script publishes to both Telegram and Google Drive in one call, a timeout at 60s usually means it reached the slow TTS/ffmpeg stage — the earlier stages (docs created, local `.md` written) already succeeded. Rerun with more time to finish cleanly.

## Environment notes
- `publish_renungan.py` loads creds via `/home/satyaaditech/.env` + `.hermes/.env` (TELEGRAM_BOT_TOKEN) and `google-workspace/scripts/google_api` for Drive. No manual env setup needed at call time.