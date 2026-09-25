#!/usr/bin/env python3
"""
One-time user-approved cleanup for the B78 Prayer/Wudu artwork.

Rules:
- restore/use the already-approved legacy illustrations;
- remove embedded instructional text/counters only;
- never mirror, swap, redraw or invent a prayer/Wudu pose;
- keep right/left semantics unchanged.
"""

from pathlib import Path
from PIL import Image, ImageDraw

ASSET_ROOT = Path("SalahZeit/Assets.xcassets")
CREAM = (250, 248, 240)

# Crop only where surrounding source text can be removed without changing
# the pose. Coordinates are in the original approved JPG pixel space.
CROPS = {
    "male_bowing": None,
    "male_final_sitting": (0, 18, 158, 175),
    "male_intention": (0, 0, 110, 275),
    "male_salam_left": (30, 25, 80, 145),
    "male_salam_right": (30, 25, 80, 145),
    "male_second_sujud": (0, 24, 215, 225),
    "male_sitting": (0, 18, 210, 220),
    "male_standing": (0, 0, 110, 188),
    "male_sujud": (0, 24, 215, 225),
    "male_takbir": (0, 0, 215, 145),
    "male_upright": (0, 10, 140, 175),

    "female_bowing": (5, 55, 185, 260),
    "female_final_sitting": (22, 0, 165, 175),
    "female_intention": (0, 8, 195, 275),
    "female_salam_left": (30, 25, 80, 145),
    "female_salam_right": (30, 25, 80, 145),
    "female_second_sujud": (0, 98, 215, 225),
    "female_sitting": (0, 18, 210, 220),
    "female_standing": (0, 5, 116, 255),
    "female_sujud": (0, 98, 215, 225),
    "female_takbir": (0, 12, 215, 208),
    "female_upright": (0, 18, 195, 220),

    "wudu_basmala": (0, 0, 132, 180),
    "wudu_ears": (0, 5, 270, 150),
    "wudu_face": None,
    "wudu_hands": None,
    "wudu_head": None,
    "wudu_intention": (0, 0, 132, 180),
    "wudu_leftarm": None,
    "wudu_leftfoot": (0, 5, 260, 150),
    "wudu_mouth": None,
    "wudu_neck": None,
    "wudu_nose": None,
    "wudu_rightarm": None,
    "wudu_rightfoot": (0, 5, 260, 150),
}

# Text/counter-only masks, also in original source coordinates.
# These areas are background in the approved artwork and do not contain the
# instructional body part/pose that the user needs to see.
POLYGON_MASKS = {
    # The old Hanafi note sits above/behind the female ruku silhouette.
    # Cover only the empty note area and follow the shoulder/back contour so
    # the approved pose itself is preserved.
    "female_bowing": [
        (
            [(65, 0), (180, 0), (180, 45), (155, 45), (135, 42),
             (115, 37), (95, 30), (80, 24), (65, 18)],
            (253, 252, 242),
        )
    ],
}

MASKS = {
    "male_bowing": [(118, 0, 215, 55), (0, 224, 138, 260)],

    "wudu_basmala": [(132, 0, 215, 108)],
    "wudu_intention": [(132, 0, 215, 108)],
    "wudu_face": [(154, 0, 215, 76)],
    "wudu_hands": [(146, 0, 210, 78)],
    "wudu_head": [(145, 0, 205, 78)],
    "wudu_leftarm": [(140, 0, 200, 78)],
    "wudu_rightarm": [(148, 0, 210, 78)],
    "wudu_mouth": [(140, 0, 200, 78)],
    "wudu_nose": [(145, 0, 205, 78)],
    "wudu_leftfoot": [(190, 0, 260, 76)],
    "wudu_rightfoot": [(190, 0, 260, 76)],
}


def source_path(name: str) -> Path:
    path = ASSET_ROOT / f"{name}.imageset" / f"{name}.jpg"
    if not path.is_file():
        raise SystemExit(f"Missing approved raster asset: {path}")
    return path


def local_background(image: Image.Image, rect: tuple[int, int, int, int]) -> tuple[int, int, int]:
    x1, _y1, x2, y2 = rect
    candidates = [
        (min(image.width - 2, x2 - 2), min(image.height - 2, y2 + 8)),
        (min(image.width - 2, x2 - 2), min(image.height - 2, y2 + 18)),
        (max(1, x1 - 8), min(image.height - 2, y2 + 12)),
    ]
    pixels = [image.getpixel(point) for point in candidates]
    # Pick the candidate closest to the light neutral artwork background.
    return min(pixels, key=lambda rgb: sum(abs(channel - 248) for channel in rgb))


def clean(name: str) -> None:
    path = source_path(name)
    with Image.open(path) as source:
        image = source.convert("RGB")

    crop = CROPS[name]
    offset_x = offset_y = 0
    if crop is not None:
        offset_x, offset_y, right, bottom = crop
        if right > image.width or bottom > image.height:
            raise SystemExit(f"Crop exceeds source for {name}: {crop} vs {image.size}")
        image = image.crop(crop)

    draw = ImageDraw.Draw(image)
    for points, fill in POLYGON_MASKS.get(name, []):
        draw.polygon(points, fill=fill)

    for original_rect in MASKS.get(name, []):
        x1, y1, x2, y2 = original_rect
        rect = (
            max(0, x1 - offset_x),
            max(0, y1 - offset_y),
            min(image.width, x2 - offset_x),
            min(image.height, y2 - offset_y),
        )
        if rect[2] <= rect[0] or rect[3] <= rect[1]:
            continue
        fill = local_background(image, rect)
        draw.rectangle(rect, fill=fill)

    if name.startswith("wudu_"):
        target = (360, 260)
        max_size = (330, 230)
    else:
        target = (320, 320)
        max_size = (290, 290)

    scale = min(max_size[0] / image.width, max_size[1] / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )

    canvas = Image.new("RGB", target, CREAM)
    position = (
        (target[0] - resized.width) // 2,
        (target[1] - resized.height) // 2,
    )
    canvas.paste(resized, position)
    canvas.save(path, "JPEG", quality=95, subsampling=0, optimize=True)
    print(f"cleaned {name}: {target[0]}x{target[1]}")


def main() -> None:
    for name in CROPS:
        clean(name)
    print(
        f"Cleaned {len(CROPS)} approved Prayer/Wudu assets: "
        "embedded text removed, poses/directions preserved."
    )


if __name__ == "__main__":
    main()
