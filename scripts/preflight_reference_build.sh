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
require_file "PRIVACY.md"
require_file "SUPPORT.md"
require_file "CONTENT_RIGHTS_AUDIT.md"
require_file "RELIGIOUS_CONTENT_AUDIT.md"
require_file "AUDIO_LICENSES.md"
require_file "SalahZeit/Resources/adhan-standard.caf"
require_file "SalahZeit/Resources/adhan-fajr.caf"
require_file "qa/adhan-audio-hashes.txt"

# Patch/merge integrity.
if grep -RInE '^(<<<<<<<|=======|>>>>>>>)' SalahZeit scripts 2>/dev/null; then
  fail "merge-conflict markers found"
fi

# Release checkpoint: SalahPath v3.62 build 77
grep -q 'MARKETING_VERSION = 3.62;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'CURRENT_PROJECT_VERSION = 77;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'SWIFT_STRICT_CONCURRENCY = complete;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'SWIFT_TREAT_WARNINGS_AS_ERRORS = YES;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'MARKETING_VERSION="3.62"' "scripts/build_unsigned_ipa.sh"
grep -q 'CURRENT_PROJECT_VERSION="77"' "scripts/build_unsigned_ipa.sh"
grep -q 'PRODUCT_BUNDLE_IDENTIFIER = com.achmed06.salahpath;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'INFOPLIST_KEY_ITSAppUsesNonExemptEncryption = NO;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'PrivacyInfo.xcprivacy in Resources' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'adhan-standard.caf in Resources' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'adhan-fajr.caf in Resources' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'adhanSoundEnabled' "SalahZeit/Models/AppSettings.swift"
grep -q 'UNNotificationSound(named:' "SalahZeit/Services/NotificationManager.swift"
[[ "$(git hash-object SalahZeit/Resources/adhan-fajr.caf)" == "546fee5cde9e0e4e9041ed02c44bc0dc5290eb19" ]] || fail "adhan-fajr.caf does not match the audited Doha derivative"
[[ "$(git hash-object SalahZeit/Resources/adhan-standard.caf)" == "5af226c758c556e318f0fe667b415a02807a8c2c" ]] || fail "adhan-standard.caf does not match the audited Doha derivative"
grep -q 'NSPrivacyAccessedAPICategoryUserDefaults' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'CA92.1' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'NSPrivacyAccessedAPICategoryFileTimestamp' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'C617.1' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'NSPrivacyCollectedDataTypeDeviceID' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'NSPrivacyCollectedDataTypePurposeAppFunctionality' "SalahZeit/PrivacyInfo.xcprivacy"
grep -q 'PRIVACY.md' "SalahZeit/Views/SettingsView.swift"
grep -q 'SalahPath-iOS/issues' "SalahZeit/Views/SettingsView.swift"

if command -v plutil >/dev/null 2>&1; then
  plutil -lint "SalahZeit/PrivacyInfo.xcprivacy" >/dev/null || fail "PrivacyInfo.xcprivacy is not a valid plist"
fi

grep -q 'struct MoreView: View' "SalahZeit/Views/RootTabView.swift"
grep -q 'NavigationStack { MoreView() }' "SalahZeit/Views/RootTabView.swift"

grep -Eq 'IslamicCalendarEventDetailView|CalendarEventEditor' "SalahZeit/Views/GuideView.swift"

# Crash-hardening regression gates.
if grep -R -nE 'fatalError\(|try!|as!' SalahZeit --include='*.swift'; then
  echo "Unsafe Swift crash primitive found." >&2
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
grep -q 'Quran 20:114 · excerpt' "SalahZeit/Views/HomeView.swift"
grep -q 'Quran 3:173 · excerpt' "SalahZeit/Views/HomeView.swift"
grep -q 'Quran 20:114 · excerpt' "SalahZeit/Views/GuideView.swift"
grep -q 'إِنَّكَ أَنْتَ الْوَهَّابُ' "SalahZeit/Views/GuideView.swift"
grep -q 'Wer einem Imam folgt, rezitiert Fātiha und Zusatzsura nicht selbst' "SalahZeit/Views/GuideView.swift"
grep -q 'Angezeigt sind nur die Anfangszeilen' "SalahZeit/Views/GuideView.swift"
grep -q 'وَإِلَيْكَ الْمَصِيرُ' "SalahZeit/Views/GuideView.swift"
grep -q 'Hier wird keine bestimmte überlieferte Anzahl behauptet' "SalahZeit/Views/GuideView.swift"

if grep -q 'count: 33, source: "Dhikr / İstiğfar"' "SalahZeit/Views/GuideView.swift"; then
  echo "Unsupported fixed Istighfar count regression found." >&2
  exit 1
fi

# Required reference assets (Salam / Wudu / prayer-art parity)
for asset in \
  "SalahZeit/Assets.xcassets/male_salam_right.imageset" \
  "SalahZeit/Assets.xcassets/male_salam_left.imageset" \
  "SalahZeit/Assets.xcassets/female_salam_right.imageset" \
  "SalahZeit/Assets.xcassets/female_salam_left.imageset" \
  "SalahZeit/Assets.xcassets/wudu_head.imageset" \
  "SalahZeit/Assets.xcassets/wudu_face.imageset" \
  "SalahZeit/Assets.xcassets/male_standing.imageset"; do
  require_dir "$asset"
done

# Validate all asset-catalog JSON and PNG structure.
python3 - <<'PY'
from pathlib import Path
import json
import struct
import sys
import zlib

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

print("Asset JSON + PNG structural integrity: OK")
PY

printf 'Reference build checks passed for SalahPath v3.62 build 77\n'
