from pathlib import Path
import json

assets_root = Path("SalahZeit/Assets.xcassets")

# Restore the original v3.5 prayer artwork the user preferred.
# These JPGs are created earlier by apply_v35.py from the original prayer sheets.
legacy_assets = [
    "male_intention", "male_takbir", "male_standing", "male_upright",
    "male_bowing", "male_sujud", "male_sitting", "male_final_sitting",
    "female_intention", "female_takbir", "female_standing", "female_upright",
    "female_bowing", "female_sujud", "female_sitting", "female_final_sitting",
]

for name in legacy_assets:
    imageset = assets_root / f"{name}.imageset"
    jpg = imageset / f"{name}.jpg"
    if not jpg.is_file():
        raise SystemExit(f"v436: original v3.5 prayer JPG missing: {jpg}")

    # v434 generated replacement SVGs. Remove them so there is only one visual truth.
    svg = imageset / f"{name}.svg"
    if svg.exists():
        svg.unlink()

    contents = {
        "images": [
            {
                "filename": jpg.name,
                "idiom": "universal",
                "scale": "1x",
            }
        ],
        "info": {
            "author": "xcode",
            "version": 1,
        },
    }
    (imageset / "Contents.json").write_text(
        json.dumps(contents, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

print("v436 applied: restored original v3.5 male/female prayer artwork")
