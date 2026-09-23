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
  CURRENT_PROJECT_VERSION="77" \
  INFOPLIST_KEY_CFBundleDisplayName="SalahPath" \
  build

APP_PATH="$ROOT/build/DerivedData/Build/Products/Release-iphoneos/SalahPath.app"
if [ ! -d "$APP_PATH" ]; then
  echo "SalahPath.app wurde nicht gefunden: $APP_PATH" >&2
  exit 1
fi

APP_BINARY="$APP_PATH/SalahPath"
INFO_PLIST="$APP_PATH/Info.plist"
PRIVACY_MANIFEST="$APP_PATH/PrivacyInfo.xcprivacy"\nADHAN_SOUND="$APP_PATH/adhan-short.caf"

if [ ! -f "$APP_BINARY" ]; then
  echo "SalahPath-Binary wurde nicht gefunden: $APP_BINARY" >&2
  exit 1
fi

if [ ! -f "$INFO_PLIST" ]; then
  echo "Info.plist wurde nicht gefunden: $INFO_PLIST" >&2
  exit 1
fi

if [ ! -f "$PRIVACY_MANIFEST" ]; then
  echo "PrivacyInfo.xcprivacy fehlt im gebauten App-Bundle." >&2
  exit 1
fi

/usr/bin/plutil -lint "$PRIVACY_MANIFEST" >/dev/null

BUNDLE_ID="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$INFO_PLIST")"
VERSION="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$INFO_PLIST")"
BUILD="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' "$INFO_PLIST")"
USES_NONEXEMPT_ENCRYPTION="$(/usr/libexec/PlistBuddy -c 'Print :ITSAppUsesNonExemptEncryption' "$INFO_PLIST")"

if [ "$BUNDLE_ID" != "com.achmed06.salahpath" ] || [ "$VERSION" != "3.62" ] || [ "$BUILD" != "77" ]; then
  echo "Unerwartete App-Metadaten: $BUNDLE_ID · $VERSION ($BUILD)" >&2
  exit 1
fi

if [ "$USES_NONEXEMPT_ENCRYPTION" != "false" ] && [ "$USES_NONEXEMPT_ENCRYPTION" != "NO" ]; then
  echo "ITSAppUsesNonExemptEncryption ist nicht auf false gesetzt: $USES_NONEXEMPT_ENCRYPTION" >&2
  exit 1
fi

mkdir -p Payload
cp -R "$APP_PATH" Payload/
/usr/bin/zip -qry SalahPath-unsigned.ipa Payload
rm -rf Payload

if [ ! -s SalahPath-unsigned.ipa ]; then
  echo "IPA wurde nicht erstellt oder ist leer." >&2
  exit 1
fi

/usr/bin/unzip -tq SalahPath-unsigned.ipa >/dev/null

echo "Fertig geprüft: $ROOT/SalahPath-unsigned.ipa · $BUNDLE_ID · v$VERSION build $BUILD"
