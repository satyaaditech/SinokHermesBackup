---
name: ascii-media
description: "ASCII media toolkit: static text art (banners, cowsay, boxes, image-to-ascii) and animated ASCII video production (MP4/GIF with colored characters)."
trigger: When the user requests ASCII art, text banners, character art, image-to-ASCII conversion, ASCII video, text art animation, terminal-style video, or retro text visualization.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ASCII, Art, Banners, Creative, Unicode, Text-Art, Video, Animation, ASCII-Video, pyfiglet, cowsay, boxes]
---

# ASCII Media Toolkit

Everything ASCII: static text art, banners, decorative borders, image conversion, and animated ASCII video production.

---

## 1. Static ASCII Art (absorbed from ascii-art)

Multiple tools for different ASCII art needs. All are local CLI programs or free REST APIs — no API keys required.

### Text Banners (pyfiglet — local)

Render text as large ASCII art banners. 571 built-in fonts.

```bash
pip install pyfiglet --break-system-packages -q
python3 -m pyfiglet "YOUR TEXT" -f slant
python3 -m pyfiglet --list_fonts
```

Recommended fonts: `slant` (clean), `doom` (bold), `big` (readable), `banner3` (classic), `small` (compact), `cyberlarge` (cyberpunk), `3-d` (3D), `gothic` (dramatic).

### Text Banners (asciified API — remote, no install)

Free REST API returning plain text ASCII art directly.

```bash
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello+World"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Slant"
curl -s "https://asciified.thelicato.io/api/v2/fonts"
```

### Cowsay (Message Art)

Classic tool that wraps text in a speech bubble with an ASCII character.

```bash
sudo apt install cowsay -y
cowsay "Hello World"
cowsay -f tux "Linux rules"
cowsay -f dragon "Rawr!"
cowthink "Hmm..."
cowsay -l
```

50+ characters available. Eye/tongue modifiers: `-b` (Borg), `-d` (dead), `-g` (greedy), `-p` (paranoid), `-s` (stoned), `-w` (wired).

### Boxes (Decorative Borders)

Draw decorative ASCII art borders/frames around any text. 70+ built-in designs.

```bash
sudo apt install boxes -y
echo "Hello World" | boxes
echo "Hello" | boxes -d stone
echo "Hello" | boxes -d cat
echo "Hello" | boxes -d dog
boxes -l
```

Combine with pyfiglet: `python3 -m pyfiglet "HERMES" -f slant | boxes -d stone`

### TOIlet (Colored Text Art)

Like pyfiglet but with ANSI color effects and visual filters.

```bash
sudo apt install toilet toilet-fonts -y
toilet "Hello World"
toilet --gay "Rainbow!"
toilet --metal "Metal!"
toilet -F border --gay "Fancy!"
```

### Image to ASCII Art

Convert images (PNG, JPEG, GIF, WEBP) to ASCII art.

**Option A: ascii-image-converter (recommended)**
```bash
sudo snap install ascii-image-converter
ascii-image-converter image.png
ascii-image-converter image.png -C        # Color
ascii-image-converter image.png -d 60,30  # Dimensions
ascii-image-converter image.png -b        # Braille
```

**Option B: jp2a (lightweight, JPEG only)**
```bash
sudo apt install jp2a -y
jp2a --width=80 image.jpg
jp2a --colors image.jpg
```

### Search Pre-Made ASCII Art

Search curated ASCII art from ascii.co.uk via curl.

```bash
curl -s 'https://ascii.co.uk/art/cat' -o /tmp/ascii_art.html
```

Then extract from `<pre>` tags. Available subjects: cat, dog, horse, bird, fish, dragon, car, ship, airplane, rocket, guitar, computer, coffee, tree, flower, sun, moon, star, robot, skull, christmas, halloween, etc.

### Fun ASCII Utilities

**QR Codes:**
```bash
curl -s "qrenco.de/Hello+World"
```

**Weather as ASCII Art:**
```bash
curl -s "wttr.in/London"
curl -s "wttr.in/Moon"
```

### Decision Flow

1. **Text banner** → pyfiglet if installed, otherwise asciified API
2. **Wrap a message in fun character art** → cowsay
3. **Add decorative border/frame** → boxes
4. **Art of a specific thing** (cat, rocket) → ascii.co.uk via curl
5. **Convert an image to ASCII** → ascii-image-converter or jp2a
6. **QR code** → qrenco.de
7. **Weather/moon art** → wttr.in
8. **Something custom/creative** → LLM generation with Unicode palette

---

## 2. ASCII Video Production (absorbed from ascii-video)

Convert video/audio/images/generative input into colored ASCII character video output (MP4, GIF, image sequence).

### Modes

| Mode | Input | Output |
|------|-------|--------|
| **Video-to-ASCII** | Video file | ASCII recreation of source footage |
| **Audio-reactive** | Audio file | Generative visuals driven by audio features |
| **Generative** | None (or seed params) | Procedural ASCII animation |
| **Hybrid** | Video + audio | ASCII video with audio-reactive overlays |
| **Lyrics/text** | Audio + text/SRT | Timed text with visual effects |
| **TTS narration** | Text quotes + TTS API | Narrated testimonial/quote video |

### Stack

Single self-contained Python script per project. No GPU required.

| Layer | Tool | Purpose |
|-------|------|---------|
| Core | Python 3.10+, NumPy | Math, array ops |
| Signal | SciPy | FFT, peak detection |
| Imaging | Pillow (PIL) | Font rasterization, frame decoding |
| Video I/O | ffmpeg (CLI) | Decode input, encode output |
| Parallel | concurrent.futures | N workers for batch rendering |

### Pipeline Architecture

```
INPUT → ANALYZE → SCENE_FN → TONEMAP → SHADE → ENCODE
```

1. **INPUT** — Load/decode source material
2. **ANALYZE** — Extract per-frame features (audio bands, video luminance)
3. **SCENE_FN** — Scene function renders to pixel canvas. See `references/scenes.md`
4. **TONEMAP** — Percentile-based adaptive brightness. See `references/composition.md`
5. **SHADE** — Post-processing via `ShaderChain` + `FeedbackBuffer`. See `references/shaders.md`
6. **ENCODE** — Pipe raw RGB frames to ffmpeg

### Critical Implementation Notes

**Brightness — Use `tonemap()`, Not Linear Multipliers:**
```python
def tonemap(canvas, gamma=0.75):
    f = canvas.astype(np.float32)
    lo, hi = np.percentile(f[::4, ::4], [1, 99.5])
    if hi - lo < 10: hi = lo + 10
    f = np.clip((f - lo) / (hi - lo), 0, 1) ** gamma
    return (f * 255).astype(np.uint8)
```

**ffmpeg Pipe Deadlock:** Never `stderr=subprocess.PIPE` with long-running ffmpeg — buffer fills at 64KB and deadlocks. Redirect to file.

### References

| File | Contents |
|------|----------|
| `references/architecture.md` | Grid system, resolution presets, font selection, character palettes, color system |
| `references/composition.md` | Pixel blend modes, `tonemap()`, `FeedbackBuffer`, masking |
| `references/effects.md` | Effect building blocks: noise, SDFs, particles, transforms |
| `references/inputs.md` | Audio analysis, video sampling, image conversion, TTS |
| `references/optimization.md` | Hardware detection, quality profiles, parallel rendering |
| `references/scenes.md` | Scene protocol, `Renderer` class, beat-synced cutting |
| `references/shaders.md` | `ShaderChain`, 38 shader catalog, transitions |
| `references/troubleshooting.md` | Common mistakes, ffmpeg issues, font problems |
