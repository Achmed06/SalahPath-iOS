#!/usr/bin/env python3
"""Export reviewed Store material; never upload or infer owner/privacy answers."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "release/store"
TEXT_LIMITS = {"name": 30, "subtitle": 30, "promotional_text": 170,
               "keywords": 100, "description": 4000}
DOCUMENTS = ("README.md", "review-notes.txt", "device-test-checklist.md",
             "owner-details.template.json", "provider-privacy-request.txt", "provider-evidence.md")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_metadata() -> tuple[dict, dict]:
    metadata = json.loads((SOURCE / "metadata.json").read_text(encoding="utf-8"))
    require(set(metadata) == {"de-DE", "tr"}, "Expected German and Turkish metadata")
    report = {}
    for locale, fields in metadata.items():
        require(set(fields) == set(TEXT_LIMITS), f"Unexpected fields in {locale}")
        report[locale] = {}
        for name, limit in TEXT_LIMITS.items():
            value = fields[name]
            require(isinstance(value, str) and value.strip() == value and bool(value),
                    f"Empty or padded text: {locale}/{name}")
            require(len(value) <= limit, f"Text too long: {locale}/{name}")
            require("\x00" not in value and "<" not in value and ">" not in value,
                    f"Expected plain text: {locale}/{name}")
            if name == "keywords":
                require(len(value.encode("utf-8")) <= 100, f"Keywords exceed 100 bytes: {locale}")
                words = value.split(",")
                require(all(len(word) > 2 and word.strip() == word for word in words),
                        f"Invalid keyword: {locale}")
                require(len(set(word.casefold() for word in words)) == len(words),
                        f"Duplicate keywords: {locale}")
            report[locale][name] = {"characters": len(value), "utf8_bytes": len(value.encode("utf-8")),
                                   "character_limit": limit}
    return metadata, report


def export_materials(screenshots: Path, output: Path, metadata: dict, lengths: dict) -> Path:
    from PIL import Image, PngImagePlugin

    manifest = json.loads((SOURCE / "screenshot-sources.json").read_text(encoding="utf-8"))
    result = subprocess.run(["git", "diff", "--quiet", manifest["release_commit"], "--",
                             "SalahZeit", "SalahZeit.xcodeproj", "scripts/build_unsigned_ipa.sh",
                             "scripts/verify_release_bundle.py"], cwd=ROOT, check=False)
    require(result.returncode == 0, "App/build sources differ from the reviewed release; capture new screenshots")
    archive = output.with_name(output.name + ".zip")
    require(not output.exists() and not archive.exists(), "Output already exists; choose a new directory")
    entries = manifest["screenshots"]
    require({entry["locale"] for entry in entries} == set(metadata), "Screenshot languages do not match")
    destinations = set()
    # Validate the complete input before creating any output.
    for locale in metadata:
        require(1 <= sum(entry["locale"] == locale for entry in entries) <= 10,
                f"Expected 1–10 screenshots for {locale}")
    for entry in entries:
        for field in ("source_file", "output_file"):
            name = entry[field]
            require(Path(name).name == name and name.endswith(".png"), "Unsafe screenshot filename")
        destination = (entry["locale"], entry["output_file"])
        require(destination not in destinations, "Duplicate output screenshot")
        destinations.add(destination)
        source = screenshots / entry["source_file"]
        require(digest(source) == entry["sha256"], f"Unreviewed screenshot: {source.name}")
        with Image.open(source) as image:
            require(image.format == "PNG" and image.size == (1206, 2622), "Unexpected native screenshot size")
            require(image.mode in {"RGB", "RGBA"}, "Unexpected screenshot color mode")
            require("transparency" not in image.info, "Unexpected PNG transparency")
            if image.mode == "RGBA":
                require(image.getchannel("A").getextrema() == (255, 255), "Non-opaque screenshot; do not flatten")

    output.mkdir(parents=True)
    for document in DOCUMENTS:
        shutil.copyfile(SOURCE / document, output / document)
    write_json(output / "metadata-validation.json", lengths)
    for locale, fields in metadata.items():
        folder = output / "metadata" / locale
        folder.mkdir(parents=True)
        for name, value in fields.items():
            (folder / f"{name}.txt").write_text(value + "\n", encoding="utf-8")
    for entry in entries:
        source = screenshots / entry["source_file"]
        destination = output / "screenshots" / entry["locale"] / entry["output_file"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            rgb = image.convert("RGB")
            color_metadata = PngImagePlugin.PngInfo()
            if "srgb" in image.info:
                color_metadata.add(b"sRGB", bytes([image.info["srgb"]]))
            rgb.save(destination, format="PNG", optimize=True, pnginfo=color_metadata,
                     icc_profile=image.info.get("icc_profile"))
            with Image.open(destination) as exported:
                require(exported.mode == "RGB" and exported.size == image.size,
                        "Exported screenshot format changed")
                require(exported.tobytes() == rgb.tobytes(), "Visible screenshot pixels changed")
                require("transparency" not in exported.info, "Export introduced transparency")
                for key in ("srgb", "icc_profile"):
                    require(exported.info.get(key) == image.info.get(key), "Screenshot color profile changed")
        entry["output_sha256"] = digest(destination)
        entry["output_relative_path"] = str(destination.relative_to(output))
        entry["rgb_pixels_unchanged"] = True
    manifest["status"] = "prepared_materials_not_uploaded_or_approved"
    manifest["text_validation"] = "passed"
    manifest["screenshot_export"] = "opaque RGB PNG; original dimensions and RGB pixels preserved"
    write_json(output / "provenance.json", manifest)
    files = sorted(path for path in output.rglob("*") if path.is_file())
    (output / "checksums.sha256").write_text("".join(
        f"{digest(path)}  {path.relative_to(output).as_posix()}\n" for path in files), encoding="utf-8")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(output.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(output).as_posix(), date_time=(2026, 10, 7, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, path.read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        require(bundle.testzip() is None, "ZIP integrity check failed")
        for entry in entries:
            data = bundle.read(entry["output_relative_path"])
            require(hashlib.sha256(data).hexdigest() == entry["output_sha256"],
                    f"Screenshot changed during packaging: {entry['output_relative_path']}")
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--screenshots", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        metadata, lengths = validate_metadata()
        if args.metadata_only:
            print(json.dumps(lengths, ensure_ascii=False, indent=2))
            return
        require(args.screenshots is not None and args.output is not None, "Set --screenshots and --output")
        archive = export_materials(args.screenshots.resolve(), args.output.resolve(), metadata, lengths)
        print(json.dumps({"archive": str(archive), "sha256": digest(archive), "bytes": archive.stat().st_size}, indent=2))
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit(f"STORE MATERIAL PREPARATION FAILED: {error}") from error


if __name__ == "__main__":
    main()
