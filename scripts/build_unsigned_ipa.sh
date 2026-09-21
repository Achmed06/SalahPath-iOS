#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

rm -rf build Payload SalahPath-unsigned.ipa

xcodebuild \
  -project SalahZeit.xcodeproj \
  -scheme SalahZeit \
  -configuration Release \
  -sdk iphoneos \
  -destination 'generic/platform=iOS' \
  -derivedDataPath build/DerivedData \
  CODE_SIGNING_ALLOWED=NO \
  CODE_SIGNING_REQUIRED=NO \
  CODE_SIGN_IDENTITY="" \
  PRODUCT_NAME="SalahPath" \
  PRODUCT_BUNDLE_IDENTIFIER="com.achmed06.salahpath" \
  MARKETING_VERSION="3.62" \
  CURRENT_PROJECT_VERSION="76" \
  INFOPLIST_KEY_CFBundleDisplayName="SalahPath" \
  build

APP_PATH="$ROOT/build/DerivedData/Build/Products/Release-iphoneos/SalahPath.app"
if [ ! -d "$APP_PATH" ]; then
  echo "SalahPath.app wurde nicht gefunden: $APP_PATH" >&2
  exit 1
fi

mkdir -p Payload
cp -R "$APP_PATH" Payload/
/usr/bin/zip -qry SalahPath-unsigned.ipa Payload
rm -rf Payload

echo "Fertig: $ROOT/SalahPath-unsigned.ipa"
