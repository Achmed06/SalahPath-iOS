#!/usr/bin/env python3
from collections import deque
from pathlib import Path
from PIL import Image

TARGETS = [
    Path("SalahZeit/Assets.xcassets/male_intention.imageset/male_intention.png"),
    Path("SalahZeit/Assets.xcassets/male_takbir.imageset/male_takbir.png"),
    Path("SalahZeit/Assets.xcassets/female_intention.imageset/female_intention.png"),
    Path("SalahZeit/Assets.xcassets/female_takbir.imageset/female_takbir.png"),
]

def clean(path: Path):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    alpha = im.getchannel("A")
    pix = alpha.load()
    seen = set()
    comps = []

    for y in range(h):
        for x in range(w):
            if pix[x, y] < 8 or (x, y) in seen:
                continue
            q = deque([(x, y)])
            seen.add((x, y))
            pts = []
            while q:
                cx, cy = q.popleft()
                pts.append((cx, cy))
                for nx in (cx-1, cx, cx+1):
                    for ny in (cy-1, cy, cy+1):
                        if nx == cx and ny == cy:
                            continue
                        if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and pix[nx, ny] >= 8:
                            seen.add((nx, ny))
                            q.append((nx, ny))
            comps.append(pts)

    if not comps:
        raise SystemExit(f"No foreground in {path}")

    comps.sort(key=len, reverse=True)
    largest = len(comps[0])
    rgba = im.load()
    removed = 0
    for comp in comps[1:]:
        xs = [p[0] for p in comp]
        ys = [p[1] for p in comp]
        cw = max(xs) - min(xs) + 1
        ch = max(ys) - min(ys) + 1
        # Remove only clearly detached slivers/noise. Keep any meaningful
        # secondary component, such as fingers, carpet detail or garment folds.
        if len(comp) < max(300, int(largest * 0.012)) and (cw < 40 or ch < 40):
            for x, y in comp:
                r, g, b, _ = rgba[x, y]
                rgba[x, y] = (r, g, b, 0)
            removed += len(comp)

    im.save(path, optimize=True)
    print(f"{path}: removed {removed} detached pixels")

for p in TARGETS:
    clean(p)
