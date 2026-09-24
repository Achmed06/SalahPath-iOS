#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

RULES = {
    Path("SalahZeit/Assets.xcassets/male_intention.imageset/male_intention.png"):   (365, 512, 250, 455),
    Path("SalahZeit/Assets.xcassets/female_intention.imageset/female_intention.png"): (365, 512, 250, 455),
    Path("SalahZeit/Assets.xcassets/male_takbir.imageset/male_takbir.png"):         (395, 512, 275, 455),
    Path("SalahZeit/Assets.xcassets/female_takbir.imageset/female_takbir.png"):     (390, 512, 275, 455),
}

for path, (x0, x1, y0, y1) in RULES.items():
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    x1, y1 = min(x1, w), min(y1, h)
    removed = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r,g,b,a = px[x,y]
            if a:
                px[x,y] = (r,g,b,0)
                removed += 1
    im.save(path, optimize=True)
    print(f"{path}: masked {removed} residual crop pixels")
