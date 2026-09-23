#!/usr/bin/env python3
from collections import deque
from pathlib import Path
from PIL import Image

ROOT = Path("SalahZeit/Assets.xcassets")
TARGETS = sorted(
    list(ROOT.glob("male_*.imageset/*.png")) +
    list(ROOT.glob("female_*.imageset/*.png"))
)

CANVAS = (512, 768)
MAX_ART = (430, 700)
THRESHOLD = 44

def distance(a, b):
    return sum((int(a[i]) - int(b[i])) ** 2 for i in range(3)) ** 0.5

def clear_connected_background(image):
    im = image.convert("RGBA")
    px = im.load()
    w, h = im.size
    corners = [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]
    samples = [px[x,y][:3] for x,y in corners]
    # The legacy pose art uses a pale warm background. Use the brightest
    # corner sample as the background reference, then flood only connected pixels.
    bg = max(samples, key=lambda c: sum(c))
    seen = set()
    q = deque(corners)
    while q:
        x,y = q.popleft()
        if (x,y) in seen:
            continue
        seen.add((x,y))
        r,g,b,a = px[x,y]
        if a == 0 or distance((r,g,b), bg) <= THRESHOLD:
            px[x,y] = (r,g,b,0)
            if x > 0: q.append((x-1,y))
            if x+1 < w: q.append((x+1,y))
            if y > 0: q.append((x,y-1))
            if y+1 < h: q.append((x,y+1))
    return im

def normalize(path):
    im = Image.open(path)
    im = clear_connected_background(im)
    alpha = im.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError(f"No foreground remained in {path}")
    im = im.crop(bbox)

    scale = min(MAX_ART[0] / im.width, MAX_ART[1] / im.height)
    new_size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    im = im.resize(new_size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", CANVAS, (0,0,0,0))
    x = (CANVAS[0] - im.width) // 2
    y = CANVAS[1] - im.height - 24
    canvas.alpha_composite(im, (x, y))
    canvas.save(path, optimize=True)

for path in TARGETS:
    normalize(path)
    print(path)
