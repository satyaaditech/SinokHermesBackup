import math
import subprocess
import os
from PIL import Image, ImageDraw

WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 5  # seconds
TOTAL_FRAMES = FPS * DURATION
FFMPEG_BIN = "/home/satyaaditech/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
OUTPUT_PATH = "/home/satyaaditech/share/motion_output.mp4"

# Math Easing Curves
def ease_out_cubic(x):
    return 1 - pow(1 - x, 3)

def spring(x):
    return 1 - math.exp(-6 * x) * math.cos(10 * x)

BG_COLOR = (11, 15, 25)
GOLD = (212, 175, 55)
CYAN = (56, 189, 248)
WHITE = (248, 250, 252)

cmd = [
    FFMPEG_BIN, '-y',
    '-f', 'rawvideo', '-vcodec', 'rawvideo',
    '-s', f'{WIDTH}x{HEIGHT}', '-pix_fmt', 'rgb24', '-r', str(FPS),
    '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-preset', 'fast', '-crf', '17',
    OUTPUT_PATH
]

process = subprocess.Popen(cmd, stdin=subprocess.PIPE)

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / FPS
    im = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(im)

    # Example: Pulsing spring badge
    scale = spring(min(1.0, max(0.0, t / 1.0)))
    r = int(120 * scale)
    cx, cy = WIDTH // 2, HEIGHT // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    draw.text((cx, cy), "MOTION GRAPHICS", fill=WHITE, anchor="mm", font_size=28)

    process.stdin.write(im.tobytes())

process.stdin.close()
process.wait()
print(f"Rendered to {OUTPUT_PATH}")
