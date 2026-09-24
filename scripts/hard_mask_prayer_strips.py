#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

RULES = {
    Path("SalahZeit/Assets.xcassets/male_intention.imageset/male_intention.png"): (346, 250, 455, 220, 18),
    Path("SalahZeit/Assets.xcassets/male_takbir.imageset/male_takbir.png"): (340, 270, 455, 228, 20),
    Path("SalahZeit/Assets.xcassets/female_intention.imageset/female_intention.png"): (360, 250, 455, 225, 20),
    Path("SalahZeit/Assets.xcassets/female_takbir.imageset/female_takbir.png"): (342, 295, 455, 225, 26),
}

for path, (x0, y0, y1, light, chroma) in RULES.items():
    im=Image.open(path).convert("RGBA")
    px=im.load()
    w,h=im.size
    removed=0
    for y in range(max(0,y0), min(h,y1)):
        for x in range(max(0,x0), w):
            r,g,b,a=px[x,y]
            if not a:
                continue
            if min(r,g,b) >= light and max(r,g,b)-min(r,g,b) <= chroma:
                px[x,y]=(r,g,b,0)
                removed += 1
    im.save(path,optimize=True)
    print(f"{path}: removed {removed} neutral-bright crop pixels")
