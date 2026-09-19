#!/usr/bin/env bash
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

# Current expected app version after the v3.53 patch chain.
grep -q 'MARKETING_VERSION="3.53"' scripts/build_unsigned_ipa.sh   || fail "expected MARKETING_VERSION 3.53 not present"
grep -q 'CURRENT_PROJECT_VERSION="58"' scripts/build_unsigned_ipa.sh   || fail "expected build number 58 not present"

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
grep -q 'Günün Duası / Dua des Tages' SalahZeit/Views/HomeView.swift   || fail "reference dua heading missing"
grep -q 'Namaz Takibi / Gebets-Tracking' SalahZeit/Views/HomeView.swift   || fail "reference tracking heading missing"

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
