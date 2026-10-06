#!/usr/bin/env python3
"""Verify the actual archive/export, never silently repair its contents."""
from __future__ import annotations

import argparse
import hashlib
import json
import plistlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_HASHES = {
    "quran-uthmani.json": "0df03e1d6da4fc8138208fec1688f2b416f0dd4ebbd514179f3e5e0fbaf4195f",
    "adhan-fajr.caf": "e0641b2e4a04f38f38c7cc8479a0a3e4d8c5d9a577d04e9acd32c135fb2df47f",
    "adhan-standard.caf": "8752346b8fab95baa41b991790233ef99e85e86728fb8d296113aba274eeef43",
}
FORBIDDEN_MARKERS = (
    b"LiveContainer", b"LC_HOME_PATH", b"fixLocalNotification",
    b"SALAH_QA_SCREEN", b"SALAH_QA_SCREENSHOT", b"SALAH_QA_NOW",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify_bundle(app: Path) -> dict:
    with (app / "Info.plist").open("rb") as file:
        info = plistlib.load(file)
    project = (ROOT / "SalahZeit.xcodeproj/project.pbxproj").read_text()
    for setting, key in (("MARKETING_VERSION", "CFBundleShortVersionString"),
                         ("CURRENT_PROJECT_VERSION", "CFBundleVersion")):
        values = set(re.findall(rf"\b{setting}\s*=\s*([\d.]+);", project))
        require(len(values) == 1 and str(info.get(key)) in values,
                f"{key} differs from the project's release identity")

    require(info.get("CFBundleIdentifier") == "com.achmed06.salahpath", "Wrong bundle identifier")
    require(info.get("CFBundleDisplayName") == "SalahPath", "Wrong display name")
    require(info.get("CFBundleExecutable") == "SalahPath", "Wrong executable name")
    require(info.get("CFBundlePackageType") == "APPL", "Not an application bundle")
    require(info.get("CFBundleSupportedPlatforms") == ["iPhoneOS"], "Not an iOS device build")
    require(info.get("UIBackgroundModes") == ["audio"], "Archive must contain the audio background mode")
    require(info.get("ITSAppUsesNonExemptEncryption") is False, "Missing encryption declaration")
    require(set(info.get("CFBundleLocalizations", [])) == {"de", "tr"}, "Missing supported languages")
    require(bool(info.get("NSLocationWhenInUseUsageDescription")), "Missing location purpose")
    require(not info.get("NSAppTransportSecurity", {}).get("NSAllowsArbitraryLoads"), "Insecure ATS override")
    for key in ("NSCameraUsageDescription", "NSMicrophoneUsageDescription",
                "NSCalendarsFullAccessUsageDescription", "NSCalendarsWriteOnlyAccessUsageDescription",
                "NSLocationAlwaysAndWhenInUseUsageDescription", "NSUserTrackingUsageDescription"):
        require(key not in info, f"Unexpected permission: {key}")

    sdk = re.fullmatch(r"iphoneos(\d+)(?:\.\d+)*", str(info.get("DTSDKName", "")))
    require(sdk is not None and int(sdk.group(1)) >= 26, "App Store requires iOS SDK 26 or newer")
    require(int(info.get("DTXcode", "0")) >= 2600, "App Store requires Xcode 26 or newer")
    minimum = str(info.get("MinimumOSVersion", "0"))
    require(int(minimum.split(".")[0]) >= 17, "Deployment target regressed below iOS 17")
    require(bool(info.get("CFBundleIcons", {}).get("CFBundlePrimaryIcon", {}).get("CFBundleIconName")),
            "Missing compiled app icon")

    with (app / "PrivacyInfo.xcprivacy").open("rb") as file:
        privacy = plistlib.load(file)
    require(privacy.get("NSPrivacyTracking") is False, "Unexpected tracking declaration")
    require(privacy.get("NSPrivacyTrackingDomains") == [], "Unexpected tracking domains")
    reasons = {item["NSPrivacyAccessedAPIType"]: item["NSPrivacyAccessedAPITypeReasons"]
               for item in privacy.get("NSPrivacyAccessedAPITypes", [])}
    require(reasons.get("NSPrivacyAccessedAPICategoryUserDefaults") == ["CA92.1"], "Missing UserDefaults reason")
    require(reasons.get("NSPrivacyAccessedAPICategoryFileTimestamp") == ["C617.1"], "Missing file timestamp reason")

    for filename, expected in RESOURCE_HASHES.items():
        require(hashlib.sha256((app / filename).read_bytes()).hexdigest() == expected,
                f"Missing or altered audited resource: {filename}")
    notices = (app / "ThirdPartyNotices.txt").read_text()
    require(notices == (ROOT / "SalahZeit/Resources/ThirdPartyNotices.txt").read_text(),
            "Incomplete third-party notices")
    require("Copyright (c) 2016 Batoul Apps" in notices, "Missing Adhan license notice")
    for language in ("de", "tr"):
        path = app / f"{language}.lproj/InfoPlist.strings"
        require(path.is_file() and path.stat().st_size > 0, f"Missing {language} permission localization")

    binary = (app / "SalahPath").read_bytes()
    require(len(binary) > 0, "Empty executable")
    for marker in FORBIDDEN_MARKERS:
        require(marker not in binary, f"Internal test marker in Release binary: {marker.decode()}")
    return {
        "bundle_id": info["CFBundleIdentifier"],
        "version": info["CFBundleShortVersionString"],
        "build": info["CFBundleVersion"],
        "sdk": info["DTSDKName"],
        "xcode": info["DTXcode"],
        "background_modes": info["UIBackgroundModes"],
        "languages": info["CFBundleLocalizations"],
        "verification": "passed",
        "scope": "bundle contents; signing, device behavior and App Review are separate checks",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = verify_bundle(args.app)
    except (OSError, ValueError, KeyError, plistlib.InvalidFileException) as error:
        raise SystemExit(f"RELEASE VERIFICATION FAILED: {error}") from error
    output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
