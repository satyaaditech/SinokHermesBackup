---
name: pillow-infographics
description: Draw custom skeletal diagrams/infographics using Pillow.
category: creative
---
# Closed-Loop Infographic Creation using Pillow and Vision Verification

Use this skill when you need to draw custom multi-step diagrams, posture sketches (e.g., stick figures for physical movements), or structural annotations, and standard text art or general generative models are not suitable or available.

## Workflow

1. **Grid & Palette Planning**:
   - Use a clean canvas of standard size (e.g., `1200 x 650` for 3 horizontal panels).
   - Use a light-mode layout: off-white background (`#F8FAFC`), dark lines for primary elements (`#0F172A`), and bold accent colors (e.g., Red `#DC2626` or Blue `#2563EB`) to highlight active components, weights, or vector paths.
   - Keep panel widths consistent and leave empty paddings/gutters (e.g., 30px) between card panels.

2. **Anatomical Stick Figures & Proportions**:
   - **8-Heads Proportion Rule (Standard H-unit)**: Use the head height `H` as the base unit to calculate correct, natural body proportions in Pillow:
     - Head: Radius = `12px` (diameter `H = 24px`).
     - Gulu (Neck): Length = `0.25H` to `0.5H`.
     - Torso / Spine: Length = `3H`. Shoulders horizontal bar = `2H` wide.
     - Lengen (Arms): Upper arm = `1.5H`, Forearm = `1.5H`.
     - Sikil (Legs): Thigh (hip-knee) = `2H`, Calf (knee-ankle) = `2H`.
   - **Bent Limbs (Squats, Pull-ups, Presses)**: Compute joints (elbows/knees) as distinct coordinates shifted outwards/downwards from a direct shoulder-to-hand or hip-to-foot path. This creates a realistic bend/V-shape.
   - **Interface Points**: Draw small filled circles (radius ~5px) for hands at contact surfaces (barbells/bars) so they look attached and do not blend into the background lines.
   - **Equipment Accuracy**: Always verify the actual machine design (e.g. Smith Machine vs. Free Weights). For a Smith Machine, draw vertical gray guide rails (`metal_color` with width=4) flanking the figure with small horizontal safety pegs at regular intervals (e.g., every 40px), showing the barbell sliding along these rails rather than floating freely.
   - **Smith Machine Hook Detail**: When illustrating Smith lock/unlock mechanics, draw a close-up circle of the bar with a flat peg and a curved hook line showing the locked hook catching the peg (Ngancing/Lock) versus hook rotated off the peg (Mbukak/Unlock).

3. **Text & Alignment Rules**:
   - Never hardcode text Y-positions close to maximum limb extension points.
   - Align footer step labels (e.g., "1. Mapan", "2. Nyurung" in Javanese) to a single fixed bottom Y-line (e.g., `panel_y_start + panel_h - 45`).
   - Draw horizontal rule dividers at the top of panels to clearly separate structural headers from drawing spaces.

4. **Closed-Loop Verification**:
   - Write the script, execute it to output the image (e.g., versioned file suffix `_v1.png`).
   - Call `vision_analyze_ide` immediately on the image path with targeted check questions (overlapping lines, legibility, correct joint/limb attachment).
   - Iterate and patch coordinate calculations until the vision feedback is fully positive.

## Minimal Pillow Boilerplate

```python
from PIL import Image, ImageDraw, ImageFont

# Set up canvas
width, height = 1200, 650
img = Image.new("RGB", (width, height), (248, 250, 252)) # Slate-50
draw = ImageDraw.Draw(img)

# Text and Font setup
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
except IOError:
    font = ImageFont.load_default()

# Drawing stick figures with custom bent limbs
# Example: Left Shoulder to Hand with bent Elbow
# Shoulder (x, y) = (100, 200), Hand/Bar (x, y) = (100, 240)
# Bent Elbow (x, y) = (80, 220)
draw.line([100, 200, 80, 220], fill=(15, 23, 42), width=4) # Upper arm
draw.line([80, 220, 100, 240], fill=(15, 23, 42), width=4) # Forearm
draw.ellipse([100-5, 240-5, 100+5, 240+5], fill=(15, 23, 42)) # Hand grip

img.save("diagram_v1.png")
```
