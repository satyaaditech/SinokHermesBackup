---
name: photorealistic-image-generation
description: Use when generating photorealistic images via OmniRoute.
version: 1.0.0
author: Sinox
platforms: [linux]
---

# Photorealistic Image Generation Blueprint

SOP and technical specification for generating cinema-grade photorealistic images without AI artifacts, distortions, or plastic rendering using OmniRoute and Antigravity Gemini Image.

---

## 1. Core Technical Setup & API Call

Images are generated via the local OmniRoute proxy endpoint:
* **Endpoint URL**: `http://localhost:20128/v1/images/generations`
* **Model ID**: `antigravity/gemini-3.1-flash-image`
* **Auth**: `Bearer $OMNIROUTER_API_KEY`

### Native Dimensions (Strict Ratio Enforcement)
Never generate square 1:1 and stretch/squish it in video editing. Always use native output dimensions:
* **YouTube Shorts / Mobile Vertical (9:16)**: `"size": "1024x1792"`
* **Long-Form / Horizontal (16:9)**: `"size": "1792x1024"`
* **Square (1:1)**: `"size": "1024x1024"`

### Python Generation Script
```python
import urllib.request, json, base64, os

def generate_photoreal_image(prompt: str, output_path: str, aspect_ratio="vertical"):
    url = 'http://localhost:20128/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {os.environ.get("OMNIROUTER_API_KEY", "")}',
        'Content-Type': 'application/json'
    }

    size = "1024x1792" if aspect_ratio == "vertical" else "1792x1024"
    payload = {
        "model": "antigravity/gemini-3.1-flash-image",
        "prompt": prompt,
        "n": 1,
        "size": size
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.loads(resp.read().decode())
        b64_data = res['data'][0]['b64_json']
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(b64_data))
    return output_path
```

---

## 2. The 6-Layer Prompt Architecture

Every photorealistic prompt must strictly assemble these 6 layers:

```
[Layer 1: Framing & Shot Type]
+ [Layer 2: Core Subject & Action]
+ [Layer 3: Micro-Materiality & Textures]
+ [Layer 4: Lighting Physics]
+ [Layer 5: Lens & Depth of Field]
+ [Layer 6: Reality Anchor]
```

### Layer Details:
1. **L1 - Framing & Ratio**: Always specify the aspect ratio and shot scale first:
   `"Vertical 9:16 composition, extreme close-up macro editorial photograph of..."` or
   `"Vertical 9:16 composition, low-angle cinematic establishing shot of..."`
2. **L2 - Core Subject**: Precise, concise subject definition. Avoid vague terms.
3. **L3 - Micro-Materiality**: Specify physical material science:
   * *Leather*: `"visible individual leather grain pores"`, `"beeswaxed linen thread"`, `"edge crease"`.
   * *Human*: `"fine skin wrinkles on knuckles"`, `"subsurface scattering"`, `"natural skin pores"`.
   * *Automotive*: `"Rosso Corsa glossy coat"`, `"wet dark asphalt reflecting neon"`, `"star 5-spoke wheels"`.
   * *Horology*: `"brushed stainless steel bezel"`, `"anti-reflective sapphire crystal reflections"`.
4. **L4 - Lighting Physics**: Direction, color temperature, and atmospheric interaction:
   `"soft cinematic afternoon sunbeam cutting through workshop dust"`,
   `"dramatic overhead warm spotlight with volumetric light beam"`,
   `"cyan rim lighting bouncing off cold metallic surfaces"`.
5. **L5 - Camera Optics & DoF**: Optical character of real cinema/photo lenses:
   `"shallow depth of field, razor-sharp foreground subject with soft optical bokeh blur in background, 35mm lens"`.
6. **L6 - Reality Anchor & Negative Buzzwords**:
   * **BANNED BUZZWORDS** (Triggers AI 3D/CGI cartoon look): *hyperrealistic, octane render, unreal engine, 8k trending on artstation, masterpiece*.
   * **REQUIRED ANCHORS**: *editorial documentary photography, candid photojournalism, authentic luxury atelier documentary aesthetic, 35mm film grain*.

---

## 3. Post-Generation Verification SOP

1. **Vision Inspection (`vision_analyze`)**:
   Check for anatomy glitches (extra fingers, face distortion), text gibberish, or anamorphic squeeze.
2. **Video Motion Processing**:
   When using in Ken Burns video pipelines, scale up to 4K (`2160x3780`), apply floating-point zoompan with `Lanczos` downsampling to eliminate jitter.
