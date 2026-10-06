#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "PRECHECK ERROR: $*" >&2
  exit 1
}

echo "== SalahPath preflight =="

if command -v xcodebuild >/dev/null 2>&1; then
  XCODE_VERSION="$(xcodebuild -version | awk 'NR==1 {print $2}')"
  XCODE_MAJOR="${XCODE_VERSION%%.*}"
  [[ "$XCODE_MAJOR" =~ ^[0-9]+$ ]] || fail "unable to parse Xcode version: $XCODE_VERSION"
  (( XCODE_MAJOR >= 26 )) || fail "App Store build requires Xcode 26 or newer; found Xcode $XCODE_VERSION"
  echo "App Store Xcode requirement: OK ($XCODE_VERSION)"
fi

require_file() {
  if [ ! -f "$1" ]; then
    echo "Missing required file: $1" >&2
    exit 1
  fi
}

require_dir() {
  if [ ! -d "$1" ]; then
    echo "Missing required directory: $1" >&2
    exit 1
  fi
}

require_file "SalahZeit.xcodeproj/project.pbxproj"
require_file "scripts/build_unsigned_ipa.sh"
require_file "SalahZeit/Views/RootTabView.swift"
require_file "SalahZeit/Views/GuideView.swift"
require_file "SalahZeit/PrivacyInfo.xcprivacy"
require_file "SalahZeit/SalahZeit.entitlements"
require_file "PRIVACY.md"
require_file "SUPPORT.md"
require_file "CONTENT_RIGHTS_AUDIT.md"
require_file "RELIGIOUS_CONTENT_AUDIT.md"
require_file "AUDIO_LICENSES.md"
require_file "SalahZeit/Resources/adhan-standard.caf"
require_file "SalahZeit/Resources/adhan-fajr.caf"
require_file "qa/adhan-audio-hashes.txt"
require_file "SalahZeit/Resources/quran-uthmani.json"
require_file "qa/quran-text-hash.txt"
require_file "qa/approved-prayer-wudu-assets.tsv"
require_file "qa/APPROVED_ASSET_POLICY.md"
require_file "scripts/verify_approved_prayer_wudu_assets.sh"

# Patch/merge integrity.
if grep -RInE '^(<<<<<<<|=======|>>>>>>>)' SalahZeit scripts 2>/dev/null; then
  fail "merge-conflict markers found"
fi

# Release checkpoint: SalahPath v3.62 build 78
grep -q 'MARKETING_VERSION = 3.62;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'CURRENT_PROJECT_VERSION = 78;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'SWIFT_STRICT_CONCURRENCY = complete;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'SWIFT_TREAT_WARNINGS_AS_ERRORS = YES;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'MARKETING_VERSION="3.62"' "scripts/build_unsigned_ipa.sh"
grep -q 'CURRENT_PROJECT_VERSION="78"' "scripts/build_unsigned_ipa.sh"
grep -q 'PRODUCT_BUNDLE_IDENTIFIER = com.achmed06.salahpath;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'repositoryURL = "https://github.com/batoulapps/adhan-swift.git";' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'kind = exactVersion;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'version = 1.5.0;' "SalahZeit.xcodeproj/project.pbxproj"
if grep -A5 'XCRemoteSwiftPackageReference "adhan-swift"' "SalahZeit.xcodeproj/project.pbxproj" | grep -q 'upToNextMajorVersion'; then
  fail "Adhan dependency must stay pinned to exact 1.5.0 for reproducible release builds"
fi
grep -q 'INFOPLIST_KEY_ITSAppUsesNonExemptEncryption = NO;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'PrivacyInfo.xcprivacy in Resources' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'adhan-standard.caf in Resources' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'adhan-fajr.caf in Resources' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'quran-uthmani.json in Resources' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'adhanSoundEnabled' "SalahZeit/Models/AppSettings.swift"
grep -q 'UNNotificationSound(named:' "SalahZeit/Services/NotificationManager.swift"
grep -q 'interruptionLevel = .timeSensitive' "SalahZeit/Services/NotificationManager.swift"
grep -q 'maximumPrayerRequests = 60' "SalahZeit/Services/NotificationManager.swift"
grep -q 'CODE_SIGN_ENTITLEMENTS = SalahZeit/SalahZeit.entitlements;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'com.apple.developer.usernotifications.time-sensitive' "SalahZeit/SalahZeit.entitlements"
[[ "$(git hash-object SalahZeit/Resources/adhan-fajr.caf)" == "546fee5cde9e0e4e9041ed02c44bc0dc5290eb19" ]] || fail "adhan-fajr.caf does not match the audited Doha derivative"
[[ "$(git hash-object SalahZeit/Resources/adhan-standard.caf)" == "5af226c758c556e318f0fe667b415a02807a8c2c" ]] || fail "adhan-standard.caf does not match the audited Doha derivative"
[[ "$(git hash-object SalahZeit/Resources/quran-uthmani.json)" == "a1312281de070617f8062f9718a3bf0e69e44f16" ]] || fail "quran-uthmani.json does not match the validated corpus"

# iOS custom notification sounds must stay below the platform's 30-second limit.
# Validate the actual CAF duration on macOS CI so a future audited-file replacement
# cannot silently fall back to the default notification sound.
if command -v afinfo >/dev/null 2>&1; then
  validate_notification_sound_duration() {
    local file="$1"
    local duration
    duration="$(afinfo "$file" | awk '/estimated duration:/ {print $(NF-1); exit}')"
    [[ "$duration" =~ ^[0-9]+([.][0-9]+)?$ ]] || fail "unable to read notification sound duration: $file"

    python3 - "$file" "$duration" <<'PY_AUDIO'
import sys

path, raw_duration = sys.argv[1], sys.argv[2]
duration = float(raw_duration)
if not (0.0 < duration < 30.0):
    raise SystemExit(
        f"PRECHECK ERROR: iOS notification sound must be shorter than 30 seconds: "
        f"{path} = {duration:.3f}s"
    )
print(f"Notification sound duration: OK ({path}: {duration:.3f}s)")
PY_AUDIO
  }

  validate_notification_sound_duration "SalahZeit/Resources/adhan-standard.caf"
  validate_notification_sound_duration "SalahZeit/Resources/adhan-fajr.caf"
fi

python3 - <<'PY'
import json
from pathlib import Path

path = Path("SalahZeit/Resources/quran-uthmani.json")
payload = json.loads(path.read_text(encoding="utf-8"))
if payload.get("code") != 200:
    raise SystemExit("PRECHECK ERROR: bundled Quran response code is not 200")

surahs = payload.get("data", {}).get("surahs", [])
if len(surahs) != 114:
    raise SystemExit(f"PRECHECK ERROR: bundled Quran has {len(surahs)} surahs instead of 114")

ayahs = [ayah for surah in surahs for ayah in surah.get("ayahs", [])]
if len(ayahs) != 6236:
    raise SystemExit(f"PRECHECK ERROR: bundled Quran has {len(ayahs)} ayahs instead of 6236")

page_counts = {page: 0 for page in range(1, 605)}
for surah in surahs:
    number = int(surah.get("number", 0))
    if not 1 <= number <= 114:
        raise SystemExit(f"PRECHECK ERROR: invalid surah number {number}")
    if not str(surah.get("name", "")).strip():
        raise SystemExit(f"PRECHECK ERROR: surah {number} has no Arabic name")
    if not str(surah.get("englishName", "")).strip():
        raise SystemExit(f"PRECHECK ERROR: surah {number} has no English name")

    for ayah in surah.get("ayahs", []):
        text = str(ayah.get("text", "")).strip()
        page = ayah.get("page")
        if not text:
            raise SystemExit(f"PRECHECK ERROR: empty ayah text in surah {number}")
        if not isinstance(page, int) or page not in page_counts:
            raise SystemExit(f"PRECHECK ERROR: invalid Quran page {page}")
        page_counts[page] += 1

empty_pages = [page for page, count in page_counts.items() if count == 0]
if empty_pages:
    raise SystemExit(f"PRECHECK ERROR: bundled Quran has empty pages: {empty_pages}")

print("Bundled Quran integrity: 114 surahs, 6236 ayahs, all 604 pages populated")
PY
grep -q 'NSPrivacyAccessedAPICategoryUserDefaults' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'CA92.1' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'NSPrivacyAccessedAPICategoryFileTimestamp' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'C617.1' "SalahZeit/PrivacyInfo.xcprivacy"
if grep -q 'NSPrivacyCollectedDataTypeDeviceID' "SalahZeit/PrivacyInfo.xcprivacy"; then
  fail "Privacy manifest must not claim Device ID collection without matching app behavior"
fi
grep -q 'PRIVACY.md' "SalahZeit/Views/SettingsView.swift"
grep -q 'SalahPath-iOS/issues' "SalahZeit/Views/SettingsView.swift"
grep -q 'SalahPath build 78 bundles two short iOS notification sounds' "AUDIO_LICENSES.md"
grep -q 'validated Arabic Uthmani Quran corpus is bundled with SalahPath' "PRIVACY.md"
if grep -q 'Quran text, translations, and recitation audio are requested directly' "PRIVACY.md"; then
  fail "privacy policy regressed to claiming bundled Arabic Quran text is remotely requested"
fi

if command -v plutil >/dev/null 2>&1; then
  plutil -lint "SalahZeit/PrivacyInfo.xcprivacy" >/dev/null || fail "PrivacyInfo.xcprivacy is not a valid plist"
  plutil -lint "SalahZeit/SalahZeit.entitlements" >/dev/null || fail "SalahZeit.entitlements is not a valid plist"
fi

grep -q 'struct MoreView: View' "SalahZeit/Views/RootTabView.swift"
grep -q 'NavigationStack { MoreView() }' "SalahZeit/Views/RootTabView.swift"

grep -Eq 'IslamicCalendarEventDetailView|CalendarEventEditor' "SalahZeit/Views/GuideView.swift"
grep -q 'EKEventEditViewController' "SalahZeit/Views/GuideView.swift"
if grep -qE 'INFOPLIST_KEY_NSCalendars(WriteOnly|Full)AccessUsageDescription' "SalahZeit.xcodeproj/project.pbxproj"; then
  fail "calendar permission string returned even though release only uses EKEventEditViewController"
fi

# Crash-hardening regression gates.
if grep -R -nE 'fatalError\(|try!|as!' SalahZeit --include='*.swift'; then
  echo "Unsafe Swift crash primitive found." >&2
  exit 1
fi

# Release-hygiene regression gate: sideload/debug-container branding must never
# leak into shipped app source.
if grep -R -nEi 'LiveContainer|SideStore|AltStore|TrollStore' SalahZeit --include='*.swift'; then
  echo "Sideload/debug-container branding found in app Swift source." >&2
  exit 1
fi

grep -q 'safeQuranFontSize' "SalahZeit/Models/AppSettings.swift"
grep -q 'CLLocationCoordinate2DIsValid' "SalahZeit/Services/LocationManager.swift"
grep -q 'addingReportingOverflow' "SalahZeit/Views/GuideView.swift"
grep -q 'numberInSurah' "SalahZeit/Views/GuideView.swift"
grep -q 'sanitizedChapters' "SalahZeit/Views/GuideView.swift"
grep -q 'sanitizedPage' "SalahZeit/Views/GuideView.swift"

if grep -q 'Array(repeating: urls, count: max(1, repeatCount))' "SalahZeit/Views/GuideView.swift"; then
  echo "Unsafe persisted Quran repeat count regression found." >&2
  exit 1
fi

if grep -R -nE 'URL\(string:[[:space:]]*"http://' SalahZeit --include='*.swift'; then
  echo "Unencrypted HTTP URL construction found." >&2
  exit 1
fi

# Religious-content regression gates for previously corrected release issues.
grep -q 'Quran 20:114 · Auszug / alıntı' "SalahZeit/Views/HomeView.swift"
grep -q 'Quran 3:173 · Auszug / alıntı' "SalahZeit/Views/HomeView.swift"
grep -q 'Quran 20:114 · Auszug / alıntı' "SalahZeit/Views/GuideView.swift"
grep -q 'إِنَّكَ أَنْتَ الْوَهَّابُ' "SalahZeit/Views/GuideView.swift"
grep -q 'Hinter einem Imam werden Fātiha und Zusatzsura nicht selbst rezitiert' "SalahZeit/Views/GuideView.swift"
grep -q 'Angezeigt sind nur die Anfangszeilen' "SalahZeit/Views/GuideView.swift"
grep -q 'وَإِلَيْكَ الْمَصِيرُ' "SalahZeit/Views/GuideView.swift"
grep -q 'Hier wird keine bestimmte überlieferte Anzahl behauptet' "SalahZeit/Views/GuideView.swift"

if grep -q 'count: 33, source: "Dhikr / İstiğfar"' "SalahZeit/Views/GuideView.swift"; then
  echo "Unsupported fixed Istighfar count regression found." >&2
  exit 1
fi

# Hard lock: approved Prayer/Wudu assets must never drift during unrelated work.
bash scripts/verify_approved_prayer_wudu_assets.sh

# Standalone visual regression gates.
# The generated premium feature/navigation set intentionally uses transparent
# PNG artwork. Remaining legacy feature icons stay vector until they are
# individually replaced. Prayer and Wudu may intentionally use the older
# approved raster artwork; every imageset must still point to exactly one real
# standalone file.
python3 - <<'PY'
from pathlib import Path
import json

root = Path("SalahZeit/Assets.xcassets")
required_wudu = {
    "wudu_intention", "wudu_basmala", "wudu_hands", "wudu_mouth",
    "wudu_nose", "wudu_face", "wudu_rightarm", "wudu_leftarm",
    "wudu_head", "wudu_ears", "wudu_neck", "wudu_rightfoot",
    "wudu_leftfoot",
}
poses = {
    "intention", "takbir", "standing", "bowing", "upright", "sujud",
    "sitting", "second_sujud", "final_sitting", "salam_right",
    "salam_left", "finger",
}
required_prayer = {
    f"{audience}_{pose}"
    for audience in ("male", "female")
    for pose in poses
}
required_features = {
    "feature_quran", "feature_quran_audio", "feature_bookmarks",
    "feature_times", "feature_prayer", "feature_wudu", "feature_calendar",
    "feature_dhikr", "feature_qibla", "feature_info", "feature_checkmark",
    "feature_settings", "feature_community", "feature_moon",
    "feature_sparkles", "feature_language", "feature_more", "feature_list",
    "feature_home", "feature_discover", "feature_profile",
    "feature_fajr", "feature_sunrise", "feature_dhuhr", "feature_asr",
    "feature_maghrib", "feature_isha", "feature_reminder", "feature_mute",
}
premium_png_features = {
    "feature_home", "feature_prayer", "feature_wudu", "feature_quran",
    "feature_discover", "feature_profile", "feature_qibla", "feature_times",
    "feature_dhikr", "feature_reminder", "feature_settings",
    "feature_quran_audio", "feature_bookmarks", "feature_calendar",
    "feature_checkmark", "feature_language", "feature_info", "feature_more",
    "feature_moon", "feature_list",
}
required = required_wudu | required_prayer | required_features | {
    "salahpath_logo", "home_mosque"
}

for name in sorted(required):
    folder = root / f"{name}.imageset"
    if not folder.is_dir():
        raise SystemExit(f"PRECHECK ERROR: missing standalone visual imageset: {name}")
    contents = folder / "Contents.json"
    if not contents.is_file():
        raise SystemExit(f"PRECHECK ERROR: missing Contents.json for visual: {name}")

    payload = json.loads(contents.read_text(encoding="utf-8"))
    filenames = [
        entry.get("filename")
        for entry in payload.get("images", [])
        if entry.get("filename")
    ]
    if len(filenames) != 1:
        raise SystemExit(
            f"PRECHECK ERROR: visual must reference exactly one standalone file: {name} -> {filenames}"
        )

    visual = folder / filenames[0]
    if not visual.is_file():
        raise SystemExit(f"PRECHECK ERROR: referenced visual file missing: {visual}")
    if visual.suffix.lower() not in {".svg", ".png", ".jpg", ".jpeg"}:
        raise SystemExit(f"PRECHECK ERROR: unsupported standalone visual format: {visual}")

    if name in premium_png_features and visual.suffix.lower() != ".png":
        raise SystemExit(f"PRECHECK ERROR: generated premium visual must remain PNG: {name}")
    if (
        name in required_features
        and name not in premium_png_features
        and visual.suffix.lower() != ".svg"
    ):
        raise SystemExit(f"PRECHECK ERROR: remaining feature/navigation visual must remain SVG: {name}")

print(
    "Standalone SalahPath visual set: "
    f"{len(required_wudu)} Wudu, {len(required_prayer)} prayer, "
    f"{len(required_features)} feature/navigation icons"
)
PY

# Validate all asset-catalog JSON and PNG structure.
python3 - <<'PY'
from pathlib import Path
import json
import struct
import sys
import zlib
import xml.etree.ElementTree as ET

root = Path("SalahZeit/Assets.xcassets")
for path in root.rglob("Contents.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"PRECHECK ERROR: invalid asset JSON {path}: {exc}", file=sys.stderr)
        raise SystemExit(1)

png_sig = b"\x89PNG\r\n\x1a\n"
for path in root.rglob("*.png"):
    data = path.read_bytes()
    if len(data) < 8 or data[:8] != png_sig:
        print(f"PRECHECK ERROR: invalid PNG signature: {path}", file=sys.stderr)
        raise SystemExit(1)

    offset = 8
    saw_iend = False
    while offset < len(data):
        if offset + 12 > len(data):
            print(f"PRECHECK ERROR: truncated PNG chunk header: {path}", file=sys.stderr)
            raise SystemExit(1)
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            print(f"PRECHECK ERROR: truncated PNG chunk payload: {path}", file=sys.stderr)
            raise SystemExit(1)
        payload = data[offset + 8:offset + 8 + length]
        stored_crc = struct.unpack(">I", data[offset + 8 + length:chunk_end])[0]
        actual_crc = zlib.crc32(chunk_type)
        actual_crc = zlib.crc32(payload, actual_crc) & 0xffffffff
        if stored_crc != actual_crc:
            print(f"PRECHECK ERROR: PNG CRC mismatch: {path}", file=sys.stderr)
            raise SystemExit(1)
        offset = chunk_end
        if chunk_type == b"IEND":
            saw_iend = True
            break

    if not saw_iend:
        print(f"PRECHECK ERROR: PNG missing IEND: {path}", file=sys.stderr)
        raise SystemExit(1)

for path in root.rglob("*.svg"):
    try:
        tree = ET.parse(path)
        svg_root = tree.getroot()
    except Exception as exc:
        print(f"PRECHECK ERROR: invalid SVG XML {path}: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if not svg_root.tag.endswith("svg"):
        print(f"PRECHECK ERROR: SVG root element missing: {path}", file=sys.stderr)
        raise SystemExit(1)

print("Asset JSON + PNG + SVG structural integrity: OK")
PY

python3 scripts/build78_regression_guard.py

printf 'Reference build checks passed for SalahPath v3.62 build 78\n'
