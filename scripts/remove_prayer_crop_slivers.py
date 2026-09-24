#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

TARGETS = [
    Path("SalahZeit/Assets.xcassets/male_intention.imageset/male_intention.png"),
    Path("SalahZeit/Assets.xcassets/male_takbir.imageset/male_takbir.png"),
    Path("SalahZeit/Assets.xcassets/female_intention.imageset/female_intention.png"),
    Path("SalahZeit/Assets.xcassets/female_takbir.imageset/female_takbir.png"),
]

def intervals_for_row(alpha, y, w):
    intervals = []
    x = 0
    while x < w:
        while x < w and alpha[x, y] < 8:
            x += 1
        if x >= w:
            break
        start = x
        while x < w and alpha[x, y] >= 8:
            x += 1
        intervals.append((start, x - 1))
    return intervals

def clean(path: Path):
    im = Image.open(path).convert("RGBA")
    alpha = im.getchannel("A")
    a = alpha.load()
    px = im.load()
    w, h = im.size
    removed = 0

    for y in range(h):
        ints = intervals_for_row(a, y, w)
        if len(ints) < 2:
            continue

        largest = max(ints, key=lambda p: p[1] - p[0] + 1)
        l0, l1 = largest

        for start, end in ints:
            if (start, end) == largest:
                continue
            width = end - start + 1
            gap = min(abs(start - l1), abs(l0 - end))

            # Legacy crop artifact: narrow isolated sliver. Preserve genuine
            # detached anatomy/detail by only removing very narrow segments
            # with a clear transparent gap from the main row silhouette.
            if width <= 34 and gap >= 12:
                for x in range(start, end + 1):
                    r, g, b, aa = px[x, y]
                    if aa >= 8:
                        px[x, y] = (r, g, b, 0)
                        removed += 1

    im.save(path, optimize=True)
    print(f"{path}: removed {removed} sliver pixels")

for target in TARGETS:
    clean(target)
