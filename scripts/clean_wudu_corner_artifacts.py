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

    # The clipped ornament occupies only the extreme upper-left corner.
    # Clear that tiny source corner directly; this avoids relying on color
    # thresholds and leaves the instructional figure untouched.
    clear_w = min(27, w)
    clear_h = min(15, h)
    for y in range(clear_h):
        for x in range(clear_w):
            r, g, b, _ = px[x, y]
            px[x, y] = (r, g, b, 0)

    # Feather the two inner edges so the cleanup blends into the card.
    for y in range(clear_h, min(clear_h + 3, h)):
        factor = (y - clear_h + 1) / 4.0
        for x in range(clear_w):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, int(a * factor))
    for x in range(clear_w, min(clear_w + 3, w)):
        factor = (x - clear_w + 1) / 4.0
        for y in range(clear_h):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, int(a * factor))

    im.save(path, optimize=True)
    print(path)

for target in TARGETS:
    clean(target)
