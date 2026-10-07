#!/usr/bin/env python3
"""Export reviewed Store material; never upload or infer owner/privacy answers."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "release/store"
TEXT_LIMITS = {"name": 30, "subtitle": 30, "promotional_text": 170,
               "keywords": 100, "description": 4000}
DOCUMENTS = ("README.md", "review-notes.txt", "device-test-checklist.md",
             "owner-details.template.json", "provider-privacy-request.txt", "provider-evidence.md",
             "START-HIER.md", "app-store-connect-fields.md", "signing-setup.md",
             "testflight-de.txt", "testflight-tr.txt")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".partial")
    with temporary.open("xb") as file:
        require(file.write(data) == len(data), f"Incomplete write: {path.name}")
        file.flush()
        os.fsync(file.fileno())
    temporary.replace(path)
    require(path.read_bytes() == data, f"Stored file differs from validated bytes: {path.name}")


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
    staging_archive = archive.with_name(archive.name + ".partial")
    require(not output.exists() and not archive.exists() and not staging_archive.exists(),
            "Output already exists; choose a new directory")
    entries = manifest["screenshots"]
    require({entry["locale"] for entry in entries} == set(metadata), "Screenshot languages do not match")
    destinations = set()
    source_bytes = {}
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
        data = source.read_bytes()
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"Unreviewed screenshot: {source.name}")
        source_bytes[entry["source_file"]] = data
        with Image.open(io.BytesIO(data)) as image:
            require(image.format == "PNG" and image.size == (1206, 2622), "Unexpected native screenshot size")
            require(image.mode in {"RGB", "RGBA"}, "Unexpected screenshot color mode")
            require("transparency" not in image.info, "Unexpected PNG transparency")
            if image.mode == "RGBA":
                require(image.getchannel("A").getextrema() == (255, 255), "Non-opaque screenshot; do not flatten")

    payloads = {document: (SOURCE / document).read_bytes() for document in DOCUMENTS}
    for document in ("SUPPORT.md", "PRIVACY.md"):
        payloads[document] = (ROOT / document).read_bytes()
    payloads["metadata-validation.json"] = json_bytes(lengths)
    for locale, fields in metadata.items():
        for name, value in fields.items():
            payloads[f"metadata/{locale}/{name}.txt"] = (value + "\n").encode("utf-8")
    for entry in entries:
        relative_path = f"screenshots/{entry['locale']}/{entry['output_file']}"
        with Image.open(io.BytesIO(source_bytes[entry["source_file"]])) as image:
            rgb = image.convert("RGB")
            color_metadata = PngImagePlugin.PngInfo()
            if "srgb" in image.info:
                color_metadata.add(b"sRGB", bytes([image.info["srgb"]]))
            buffer = io.BytesIO()
            rgb.save(buffer, format="PNG", optimize=True, pnginfo=color_metadata,
                     icc_profile=image.info.get("icc_profile"))
            data = buffer.getvalue()
            with Image.open(io.BytesIO(data)) as exported:
                require(exported.mode == "RGB" and exported.size == image.size,
                        "Exported screenshot format changed")
                require(exported.tobytes() == rgb.tobytes(), "Visible screenshot pixels changed")
                require("transparency" not in exported.info, "Export introduced transparency")
                for key in ("srgb", "icc_profile"):
                    require(exported.info.get(key) == image.info.get(key), "Screenshot color profile changed")
        payloads[relative_path] = data
        entry["output_sha256"] = hashlib.sha256(data).hexdigest()
        entry["output_relative_path"] = relative_path
        entry["rgb_pixels_unchanged"] = True
    manifest["status"] = "prepared_materials_not_uploaded_or_approved"
    manifest["text_validation"] = "passed"
    manifest["screenshot_export"] = "opaque RGB PNG; original dimensions and RGB pixels preserved"
    payloads["provenance.json"] = json_bytes(manifest)
    payloads["checksums.sha256"] = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(payloads.items())
    ).encode("utf-8")
    output.mkdir(parents=True)
    for name, data in payloads.items():
        write_atomic(output / name, data)
    # Package the exact validated bytes, without re-reading mutable intermediate images.
    with zipfile.ZipFile(staging_archive, "x", zipfile.ZIP_DEFLATED) as bundle:
        for name, data in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 7, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)
    with zipfile.ZipFile(staging_archive) as bundle:
        require(bundle.testzip() is None, "ZIP integrity check failed")
        require(set(bundle.namelist()) == set(payloads), "Unexpected ZIP entries")
        for name, data in payloads.items():
            require(bundle.read(name) == data, f"File changed during packaging: {name}")
    staging_archive.replace(archive)
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
