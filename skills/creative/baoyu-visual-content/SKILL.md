---
name: baoyu-visual-content
description: "宝玉 (JimLiu) visual content suite: article illustrations, knowledge comics, and infographics. All three use the same Type × Style × Palette framework via Hermes' image_generate tool."
trigger: When the user asks to create an article illustration, knowledge comic, or infographic using the baoyu visual style system.
version: 2.0.0
author: 宝玉 (JimLiu)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, image-generation, article-illustration, comic, infographic, baoyu]
    homepage: https://github.com/JimLiu/baoyu-skills
---

# Baoyu Visual Content Suite

Unified skill for three visual content types built on the same Type × Style × Palette framework. All use Hermes' `image_generate` tool (prompt-only, returns a URL). The user provides content (text, file path, URL, or topic) and optionally specifies visual dimensions.

## Three Workflows

| Workflow | Output | When to Use |
|----------|--------|-------------|
| **Article Illustration** | Single image for an article/blog post | User asks for article illustration, blog image, or editorial graphic |
| **Knowledge Comic** | Multi-page comic (cover + pages) | User asks for knowledge comic, educational comic, tutorial comic, biography comic |
| **Infographic** | Single high-density visual summary | User asks for infographic, visual summary, 信息图, or 可视化 |

All workflows share these principles:
- **Prompt-only generation**: `image_generate` accepts only `prompt` and `aspect_ratio`; all visual consistency is enforced via text descriptions in prompts.
- **Language handling**: Use the user's input language for all interactions (storyboards, prompts, confirmations, summaries). Technical terms remain in English.
- **Absolute paths for downloads**: Always use fully-qualified paths with `curl -o`; never rely on persistent-shell CWD.
- **Backup rule**: If a file exists before regeneration, rename it with `-backup-YYYYMMDD-HHMMSS`.
- **Strip secrets**: Scan source content for API keys, tokens, or credentials before writing any output.

---

## 1. Article Illustration (absorbed from baoyu-article-illustrator)

Create a single illustration for an article/blog post using Type × Style × Palette.

### Dimensions

| Dimension | Options |
|-----------|---------|
| **Type** | decorative, explanatory, emotional, narrative, diagrammatic |
| **Style** | 15+ options including flat, watercolor, chalkboard, pixel-art, retro, etc. |
| **Palette** | macaron, mono-ink, warm, neon, cool, pastel |

Full style definitions: `references/article-illustrator/styles/<style>.md`  
Full palette definitions: `references/article-illustrator/palettes/<palette>.md`  
Prompt construction guide: `references/article-illustrator/prompt-construction.md`

### Output
```
illustration/{topic-slug}/
├── source-{slug}.md
├── analysis.md
├── prompts/illustration.md
└── illustration.png
```

### Workflow
1. Analyze content → `analysis.md`
2. Confirm type, style, and palette with user via `clarify`
3. Generate prompt → `prompts/illustration.md`
4. Generate image via `image_generate`
5. Download to `illustration.png`

---

## 2. Knowledge Comic (absorbed from baoyu-comic)

Create original knowledge/educational comics with flexible Art × Tone × Layout combinations.

### Dimensions

| Dimension | Options | Default |
|-----------|---------|---------|
| Art | ligne-claire, manga, realistic, ink-brush, chalk, minimalist | ligne-claire |
| Tone | neutral, warm, dramatic, romantic, energetic, vintage, action | neutral |
| Layout | standard, cinematic, dense, splash, mixed, webtoon, four-panel | standard |
| Aspect | 3:4 (portrait), 4:3 (landscape), 16:9 (widescreen) | 3:4 |

Full art style definitions: `references/comic/art-styles/<style>.md`  
Full tone definitions: `references/comic/tones/<tone>.md`  
Full layout definitions: `references/comic/layouts/<layout>.md`  
Preset guides: `references/comic/presets/<preset>.md`  
Workflow details: `references/comic/workflow.md`

### Output
```
comic/{topic-slug}/
├── source-{slug}.md
├── analysis.md
├── storyboard.md
├── characters/
│   ├── characters.md
│   └── characters.png   # review artifact
├── prompts/
│   └── NN-{cover|page}-{slug}.md
└── NN-{cover|page}-{slug}.png
```

### Workflow
1. Analyze content → `analysis.md`
2. Confirm art, tone, layout, aspect, and review gates via `clarify`
3. Generate storyboard + character definitions
4. Generate prompts → `prompts/*.md`
5. Generate character sheet (if multi-page)
6. Generate pages via `image_generate`
7. Download each page to the output directory

**Critical**: Character consistency is enforced by embedding character text descriptions inline in every page prompt during Step 4. The PNG character sheet is a human-facing review artifact only.

---

## 3. Infographic (absorbed from baoyu-infographic)

Create information graphics with Layout × Style combinations.

### Dimensions

| Dimension | Options | Default |
|-----------|---------|---------|
| Layout | 21 options (linear-progression, bento-grid, hub-spoke, venn-diagram, etc.) | bento-grid |
| Style | 21 options (craft-handmade, cyberpunk-neon, chalkboard, pixel-art, etc.) | craft-handmade |
| Aspect | landscape (16:9), portrait (9:16), square (1:1), or custom W:H | landscape |

Full layout definitions: `references/infographic/layouts/<layout>.md`  
Full style definitions: `references/infographic/styles/<style>.md`  
Content template: `references/infographic/structured-content-template.md`

### Output
```
infographic/{topic-slug}/
├── source-{slug}.{ext}
├── analysis.md
├── structured-content.md
├── prompts/infographic.md
└── infographic.png
```

### Workflow
1. Analyze content → `analysis.md`
2. Generate structured content → `structured-content.md`
3. Recommend 3-5 layout×style combinations
4. Confirm selection via `clarify`
5. Generate prompt → `prompts/infographic.md`
6. Generate image via `image_generate`
7. Download to `infographic.png`

**Critical**: Preserve source data faithfully — never summarize, paraphrase, or alter statistics.

---

## Common Pitfalls

1. **image_generate is prompt-only** — it does not accept reference images. Visual consistency is text-driven.
2. **Always download results** — `image_generate` returns a URL; save to local files with absolute paths.
3. **Use absolute paths for curl** — never rely on persistent-shell CWD across batches.
4. **Backup before regeneration** — rename existing files with `-backup-YYYYMMDD-HHMMSS`.
5. **Strip secrets from source** — scan for API keys, tokens, credentials before outputting.
6. **Timeout handling in clarify** — if `clarify` times out, treat as default for that one question only, surface the default visibly, and continue asking remaining questions.
