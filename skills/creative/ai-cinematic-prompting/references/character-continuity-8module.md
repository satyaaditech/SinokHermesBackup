# 8-Module Video Production Continuity & Character Sheet (Identity-Locked)

Based on the STEAL.PROMPTS Production Deck standard for AI video pipelines (GPT Image 2, Midjourney, Flux.1, Gemini Imagen 3).

## Master Production Prompt Template (Ratio 4:5 Portrait)

```text
Upload your reference image and copy the prompt below :

Create a professional AI Video Production — Character Reference Sheet for the provided character image.
Create a polished 4:5 portrait continuity sheet focused exclusively on the character:

1. CHARACTER PROFILE — name, role, approximate age, height, body type, personality, distinctive traits, and signature colors.
2. FULL-BODY TURNAROUND — front, 3/4, side, and back views of the exact same character at matching scale, with identical facial features, hairstyle, body proportions, costume, colors, and accessories.
3. FACE AND IDENTITY DETAILS — front, profile, and 3/4 head-and-shoulder close-ups showing facial structure, eyes, eyebrows, nose, lips, hairstyle, skin tone, makeup, scars, tattoos, and other defining features.
4. EXPRESSION SHEET — neutral, happy, angry, sad, surprised, worried, confident, and determined expressions. Preserve the exact same facial structure and identity in every expression.
5. POSE AND BODY LANGUAGE — neutral standing, walking, sitting, relaxed, tense, and action-ready poses. Maintain consistent anatomy, proportions, posture, and silhouette.
6. COSTUME DETAILS — close-ups of clothing layers, fabrics, seams, fasteners, footwear, jewelry, eyewear, markings, logos, and other character-defining wardrobe elements.
7. COLOR AND MATERIAL PALETTE — include 4-6 key colors with HEX codes, plus references for skin, hair, fabric, leather, metal, plastic, armor, or other visible materials.
8. DO NOT CHANGE — lock the character's face, identity, skin tone, age, hair, eye color, body shape, proportions, costume, accessories, markings, colors, and defining features. Do not redesign, beautify, age, stylize, simplify, or create alternate versions.

Use a clean white or neutral studio background, soft controlled lighting, realistic materials, sharp details, subtle shadows, clean typography, thin dividers, balanced spacing, and a sophisticated editorial production-design grid. Every panel must depict the exact same character with absolute visual consistency. Focus only on the character. Do not include props, additional characters, environments, unrelated objects, or alternate outfits.
```

## Midjourney & Flux Parameters
* `--cref [IMAGE_URL]` : Hard-lock character identity onto canvas.
* `--cw 20` : Locks face while allowing wardrobe/expression flexibility.
* `--ar 4:5` : Optimal vertical ratio for 8-module grid layout.
