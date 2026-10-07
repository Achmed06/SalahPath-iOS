#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Exercise Archive without modifying the resulting bundle after compilation.
ARCHIVE_PATH="$ROOT/build/unsigned/SalahPath.xcarchive"
rm -rf "$ROOT/build/unsigned" SalahPath-unsigned.ipa
xcodebuild \
  -project SalahZeit.xcodeproj \
  -scheme SalahZeit \
  -configuration Release \
  -sdk iphoneos \
  -destination 'generic/platform=iOS' \
  -derivedDataPath build/unsigned/DerivedData \
  -archivePath "$ARCHIVE_PATH" \
  CODE_SIGNING_ALLOWED=NO \
  CODE_SIGNING_REQUIRED=NO \
  CODE_SIGN_IDENTITY="" \
  archive

APP_PATH="$ARCHIVE_PATH/Products/Applications/SalahPath.app"
python3 scripts/verify_release_bundle.py "$APP_PATH" \
  --report build/unsigned/release-verification.json
mkdir -p build/unsigned/package/Payload
cp -R "$APP_PATH" build/unsigned/package/Payload/
(cd build/unsigned/package && /usr/bin/zip -qry "$ROOT/SalahPath-unsigned.ipa" Payload)
/usr/bin/unzip -tq SalahPath-unsigned.ipa >/dev/null
echo "Geprüftes unsigniertes Testpaket: $ROOT/SalahPath-unsigned.ipa"
