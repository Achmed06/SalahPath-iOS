#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

TARGETS = [
    Path("SalahZeit/Assets.xcassets/wudu_head.imageset/wudu_head.png"),
    Path("SalahZeit/Assets.xcassets/wudu_ears.imageset/wudu_ears.png"),
]

def clean(path: Path) -> None:
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size

    # The legacy source contains a small clipped gold decorative disk touching
    # the upper-left edge. Remove only gold-toned pixels in that tiny corner,
    # preserving the instructional artwork itself.
    for y in range(min(28, h)):
        for x in range(min(42, w)):
            r, g, b, a = px[x, y]
            is_gold = (
                a > 0 and
                r >= 145 and
                85 <= g <= 190 and
                b <= 120 and
                r > g + 20 and
                g > b + 15
            )
            if is_gold:
                px[x, y] = (r, g, b, 0)

    # Feather semi-gold antialiasing immediately around removed pixels.
    for y in range(min(30, h)):
        for x in range(min(44, w)):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            near_transparent = False
            for yy in range(max(0, y - 1), min(h, y + 2)):
                for xx in range(max(0, x - 1), min(w, x + 2)):
                    if px[xx, yy][3] == 0:
                        near_transparent = True
                        break
                if near_transparent:
                    break
            if near_transparent and r >= 130 and g >= 80 and b <= 140 and r > b + 25:
                px[x, y] = (r, g, b, min(a, 80))

    im.save(path, optimize=True)
    print(path)

for target in TARGETS:
    clean(target)
