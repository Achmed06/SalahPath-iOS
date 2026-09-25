#!/usr/bin/env python3
"""
One-time, user-approved cleanup for the B78 Prayer/Wudu artwork.

The approved legacy illustrations are intentionally preserved. This script only:
- crops embedded instructional text / counters away from the existing raster art;
- places the untouched crop on a neutral SalahPath cream canvas;
- never redraws, mirrors, swaps or invents a prayer/Wudu pose.

Do not run this script for unrelated changes.
"""

from pathlib import Path
from PIL import Image

ASSET_ROOT = Path("SalahZeit/Assets.xcassets")
CREAM = (250, 248, 240)

# Source-pixel crop boxes (left, top, right, bottom).
# Right/left semantics are unchanged because no image is mirrored.
CROPS = {
    "female_bowing": (0, 65, 96, 260),
    "female_final_sitting": (28, 8, 122, 175),
    "female_intention": (0, 12, 195, 275),
    "female_salam_left": (22, 0, 80, 165),
    "female_salam_right": (22, 0, 80, 165),
    "female_second_sujud": (0, 104, 180, 225),
    "female_sitting": (0, 42, 210, 220),
    "female_standing": (0, 0, 108, 255),
    "female_sujud": (0, 104, 180, 225),
    "female_takbir": (0, 30, 215, 185),
    "female_upright": (0, 36, 195, 220),

    "male_bowing": (20, 40, 132, 235),
    "male_final_sitting": (18, 18, 110, 175),
    "male_intention": (0, 0, 98, 275),
    "male_salam_left": (22, 0, 80, 165),
    "male_salam_right": (22, 0, 80, 165),
    "male_second_sujud": (0, 45, 215, 225),
    "male_sitting": (0, 42, 210, 220),
    "male_standing": (0, 0, 102, 185),
    "male_sujud": (0, 45, 215, 225),
    "male_takbir": (0, 0, 215, 138),
    "male_upright": (0, 26, 195, 155),

    "wudu_basmala": (0, 0, 132, 180),
    "wudu_ears": (0, 0, 270, 150),
    "wudu_face": (0, 0, 145, 175),
    "wudu_hands": (0, 0, 142, 180),
    "wudu_head": (0, 0, 142, 175),
    "wudu_intention": (0, 0, 132, 180),
    "wudu_leftarm": (0, 0, 134, 175),
    "wudu_leftfoot": (0, 0, 180, 150),
    "wudu_mouth": (0, 0, 135, 180),
    "wudu_neck": (0, 0, 900, 650),
    "wudu_nose": (0, 0, 138, 180),
    "wudu_rightarm": (0, 0, 138, 175),
    "wudu_rightfoot": (0, 0, 180, 150),
}


def find_jpg(name: str) -> Path:
    path = ASSET_ROOT / f"{name}.imageset" / f"{name}.jpg"
    if not path.is_file():
        raise SystemExit(f"Missing approved raster asset: {path}")
    return path


def clean(name: str, box: tuple[int, int, int, int]) -> None:
    path = find_jpg(name)
    with Image.open(path) as source:
        rgb = source.convert("RGB")
        if box[2] > rgb.width or box[3] > rgb.height:
            raise SystemExit(
                f"Crop box {box} exceeds {name} source size {rgb.size}; refusing to alter asset."
            )
        cropped = rgb.crop(box)

    if name.startswith("wudu_"):
        target = (360, 260)
        max_box = (330, 230)
    else:
        target = (320, 320)
        max_box = (290, 290)

    cropped.thumbnail(max_box, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", target, CREAM)
    xy = ((target[0] - cropped.width) // 2, (target[1] - cropped.height) // 2)
    canvas.paste(cropped, xy)
    canvas.save(path, "JPEG", quality=94, subsampling=0, optimize=True)
    print(f"cleaned {name}: {source_size(path)}")


def source_size(path: Path) -> str:
    with Image.open(path) as image:
        return f"{image.width}x{image.height}"


def main() -> None:
    for name, box in CROPS.items():
        clean(name, box)
    print(f"Cleaned {len(CROPS)} approved Prayer/Wudu raster assets without redrawing or mirroring.")


if __name__ == "__main__":
    main()
