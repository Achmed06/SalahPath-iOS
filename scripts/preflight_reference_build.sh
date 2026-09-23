#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

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

# Release checkpoint: SalahPath v3.62 build 76
grep -q 'MARKETING_VERSION = 3.62;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'CURRENT_PROJECT_VERSION = 76;' "SalahZeit.xcodeproj/project.pbxproj"
grep -q 'MARKETING_VERSION="3.62"' "scripts/build_unsigned_ipa.sh"
grep -q 'CURRENT_PROJECT_VERSION="76"' "scripts/build_unsigned_ipa.sh"

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

printf 'Reference build checks passed for SalahPath v3.62 build 76\n'
