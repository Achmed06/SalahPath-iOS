#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

RULES = {
    "male_intention.png":   (370, 445, 245, 455, 214),
    "male_takbir.png":      (392, 445, 245, 455, 214),
    "female_intention.png": (365, 445, 245, 455, 220),
    "female_takbir.png":    (382, 445, 245, 455, 220),
}

PATHS = [
    Path("SalahZeit/Assets.xcassets/male_intention.imageset/male_intention.png"),
    Path("SalahZeit/Assets.xcassets/male_takbir.imageset/male_takbir.png"),
    Path("SalahZeit/Assets.xcassets/female_intention.imageset/female_intention.png"),
    Path("SalahZeit/Assets.xcassets/female_takbir.imageset/female_takbir.png"),
]

for path in PATHS:
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    x0, x1, y0, y1, light = RULES[path.name]
    x1, y1 = min(x1, w), min(y1, h)
    removed = 0
    for y in range(max(0, y0), y1):
        for x in range(max(0, x0), x1):
            r, g, b, a = px[x, y]
            if a > 0 and r >= light and g >= light and b >= light:
                px[x, y] = (r, g, b, 0)
                removed += 1
    im.save(path, optimize=True)
    print(f"{path}: removed {removed} bright legacy-strip pixels")
