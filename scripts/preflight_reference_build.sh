#!/usr/bin/env bash
# Release checkpoint: SalahPath v3.62 build 73; final cleanup chain validated through v393.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "PRECHECK ERROR: $*" >&2
  exit 1
}

echo "== SalahPath preflight =="

test -d SalahZeit || fail "SalahZeit source directory missing"
test -f SalahZeit/SalahZeitApp.swift || fail "SalahZeitApp.swift missing"
test -f SalahZeit/Views/HomeView.swift || fail "HomeView.swift missing"
test -f SalahZeit/Views/RootTabView.swift || fail "RootTabView.swift missing"
test -f SalahZeit/Views/GuideView.swift || fail "GuideView.swift missing"
test -f scripts/build_unsigned_ipa.sh || fail "build script missing"

# Patch/merge integrity.
if grep -RInE '^(<<<<<<<|=======|>>>>>>>)' SalahZeit scripts 2>/dev/null; then
  fail "merge-conflict markers found"
fi

# Current expected app version after the v3.62 build 72 release checkpoint.
grep -q 'MARKETING_VERSION="3.62"' scripts/build_unsigned_ipa.sh   || fail "expected MARKETING_VERSION 3.62 not present"
grep -q 'CURRENT_PROJECT_VERSION="73"' scripts/build_unsigned_ipa.sh   || fail "expected build number 73 not present"

# Reference assets introduced by the visual parity passes.
required_assets=(
  home_mosque
  ref_dash_quran ref_dash_dhikr ref_dash_prayer ref_dash_wudu
  ref_dash_times ref_dash_qibla ref_dash_info ref_dash_fav
)

for asset in "${required_assets[@]}"; do
  dir="SalahZeit/Assets.xcassets/${asset}.imageset"
  test -d "$dir" || fail "asset imageset missing: $asset"
  test -f "$dir/Contents.json" || fail "Contents.json missing: $asset"
done

# Validate every asset-catalog JSON file and all PNG signatures.
python3 - <<'PY'
from pathlib import Path
import json, sys

root = Path("SalahZeit/Assets.xcassets")
for path in root.rglob("Contents.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"PRECHECK ERROR: invalid asset JSON {path}: {exc}", file=sys.stderr)
        raise SystemExit(1)

import struct, zlib

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

# Ensure QA routing added for the five visual-reference screens exists.
grep -Rqs 'SALAH_QA_SCREEN' SalahZeit   || fail "multi-screen screenshot QA routing missing"

# Ensure required reference copy/data survived the patch chain.
grep -q '2:38:15' SalahZeit/Views/HomeView.swift   || fail "reference countdown missing"
grep -q 'Rabbim, ilmimi artır.' SalahZeit/Views/HomeView.swift   || fail "reference daily dua missing"
grep -q 'Text(settings.t("Dua des Tages", "Günün Duası"))' SalahZeit/Views/HomeView.swift \
  || fail "localized daily-dua heading missing"
grep -q 'Text(settings.t("Gebets-Tracking", "Namaz Takibi"))' SalahZeit/Views/HomeView.swift \
  || fail "localized prayer-tracking heading missing"
grep -q 'Text(settings.t("Nächstes Gebet", "Sıradaki Namaz"))' SalahZeit/Views/HomeView.swift \
  || fail "localized next-prayer heading missing"
grep -q 'Text(settings.t("(An-Nisāʾ 4:103)", "(Nisâ, 103)"))' SalahZeit/Views/HomeView.swift \
  || fail "localized Home Quran citation missing"

# Language-consistency regressions fixed after v3.62.
grep -q 'settings.t("Gebetszeiten", "Namaz Vakitleri")' SalahZeit/Views/HomeView.swift \
  || fail "localized prayer-times title missing"
grep -q 'settings.t("Morgen", "Sabah")' SalahZeit/Views/GuideView.swift \
  || fail "localized Dhikr tabs missing"
grep -q 'Text(activeDhikr.translation)' SalahZeit/Views/GuideView.swift \
  || fail "localized Dhikr translation output missing"
grep -q 'settings.t("Arabisch", "Arapça")' SalahZeit/Views/GuideView.swift \
  || fail "localized Quran language tabs missing"
grep -q 'audiencePill(.male, title: settings.t("Mann", "Erkek"))' SalahZeit/Views/GuideView.swift \
  || fail "localized prayer audience selector missing"
grep -q 'settings.language = settings.language == .german ? .turkish : .german' SalahZeit/Views/GuideView.swift \
  || fail "bidirectional prayer language toggle missing"
grep -q 'settings.language == .german ? german : turkish' SalahZeit/Views/GuideView.swift \
  || fail "language-specific prayer feature copy missing"
grep -q 'settings.t("Arabisch", "Arapça")' SalahZeit/Views/GuideView.swift \
  || fail "localized Quran reader language copy missing"
grep -q 'settings.t("Tägliche Serie", "Günlük Seri")' SalahZeit/Views/HomeView.swift \
  || fail "localized Home streak copy missing"
grep -q '.navigationBarTitleDisplayMode(.inline)' SalahZeit/Views/GuideView.swift \
  || fail "compact navigation headers missing"
grep -q 'settings.t("Gebet lernen", "Namaz Öğren")' SalahZeit/Views/GuideView.swift \
  || fail "localized German prayer-learning title missing"
grep -q 'settings.t("Gebet lernen", "Namaz öğren")' SalahZeit/Views/GuideView.swift \
  || fail "localized German prayer-howto title missing"
grep -q 'settings.t("Hijri-Kalender", "Hicrî takvim")' SalahZeit/Views/GuideView.swift \
  || fail "localized German Hijri title missing"
grep -q 'settings.t("Gebet lernen", "Namaz Öğren")' SalahZeit/Views/RootTabView.swift \
  || fail "localized Discover prayer title missing"
grep -q 'settings.t("Wudu", "Abdest Rehberi")' SalahZeit/Views/RootTabView.swift \
  || fail "localized Discover Wudu title missing"
grep -q 'settings.t("Qibla", "Kıble")' SalahZeit/Views/RootTabView.swift \
  || fail "localized Discover Qibla title missing"
grep -q 'settings.t("Qibla", "Kıble")' SalahZeit/Views/QiblaView.swift \
  || fail "localized Qibla screen heading missing"
grep -q 'settings.t("Hijri-Kalender", "Hicrî Takvim")' SalahZeit/Views/RootTabView.swift \
  || fail "localized Discover Hijri title missing"
grep -q 'Text(settings.t("FARD", "FARZ"))' SalahZeit/Views/GuideView.swift \
  || fail "localized Wudu obligation badge missing"
grep -q 'case "wudu_rightfoot": footVisual(mirrored: false)' SalahZeit/Views/GuideView.swift \
  || fail "right-foot Wudu artwork mapping missing"
grep -q 'case "wudu_leftfoot": footVisual(mirrored: true)' SalahZeit/Views/GuideView.swift \
  || fail "left-foot Wudu artwork mapping missing"
grep -q '.navigationTitle(settings.t("Wudu", "Abdest"))' SalahZeit/Views/GuideView.swift \
  || fail "localized Wudu navigation title missing"

# Parse every Swift file before Xcode build. This catches syntax damage from a patch
# before package resolution/build spends several minutes.
if command -v xcrun >/dev/null 2>&1; then
  echo "Parsing Swift sources..."
  while IFS= read -r -d '' file; do
    xcrun swiftc -frontend -parse "$file" >/dev/null
  done < <(find SalahZeit -name '*.swift' -type f -print0)
  echo "Swift parse: OK"
else
  echo "xcrun unavailable: skipping Swift parse on this host"
fi

echo "SalahPath preflight: PASS"
