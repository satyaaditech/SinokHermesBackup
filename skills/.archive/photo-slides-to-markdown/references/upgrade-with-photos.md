# Upgrade .md: embed original photos + Indonesian extraction + explanation

Established 2026-08-09 (Bussines_plan_coaching session). After the raw transcription was done, user asked: "bikin file .md yang baru, versi upgrade, content tersusun selang seling: photo asli -> hasil extract dalam bahasa Indonesia + penjelasan."

## Feasibility check FIRST (before promising embedded photos)
- Sum the source image sizes (`ls -la ~/.hermes/cache/images/img_*.jpg`). Base64 adds ~33%: 23 photos ≈ 1.9 MB → ~2.5 MB self-contained .md, acceptable. Over ~3–5 MB the file gets unwieldy → fall back to a relative `images/` folder + zip bundle, or an HTML version.
- Source photos are the cached chat images at `~/.hermes/cache/images/img_*.jpg` (paths appear in the message payloads / vision_analyze hints).

## Structure per slide (the alternating pattern the user wants)
```
## Slide NN — Judul
![Foto asli — Slide NN](data:image/jpeg;base64,<...>)

### 📝 Hasil Ekstrak (Bahasa Indonesia)
<translated/paraphrased content of the slide — NOT the raw English verbatim>

### 💡 Penjelasan
<why this slide matters + how to use it — added coaching value, not just transcription>
```
Plus `## 📑 Daftar Isi` at the top: numbered list `1. **Slide NN** — Judul`.

## Generate with a script, never hand-write
Python generator pattern (worked well, ~2.5 MB output):
- Data list of tuples `(slide_no, title, img_filename, extract_id, explanation)`.
- `base64.b64encode(open(img,'rb').read()).decode()` per image.
- Assemble: header + TOC + per-slide blocks joined with `---`.
- Verify after writing: `grep -c "data:image/jpeg;base64" file.md` == number of slides; `ls -la` shows the expected MB.

## Delivery
`ln -sf <file>.md ~/share/<file>.md` → the already-running `http.server` on ~/share serves it automatically → same LAN/Tailscale link pattern as `server-link-delivery.md`. No new server needed.

## Batch: several photos in ONE message
When multiple photos arrive at once, run vision_analyze for EACH photo in parallel + a single `date +"%Y-%m-%d %H:%M"` call, then ONE patch that appends all entries before the marker. This session did 4-at-once cleanly.

## Notes from the session
- Duplicate photos (same slide number/content re-sent) should be detected via vision_analyze comparison and SKIPPED — no new entry, tell the user it's a duplicate.
- If two vision passes disagree on a value (e.g. product name "Choc-O-Koko" vs "Choc-O-Katsu"), record the discrepancy as a note in the entry rather than guessing silently.
- Keep the raw transcription file and the upgrade file as two separate deliverables; the user referenced both.
