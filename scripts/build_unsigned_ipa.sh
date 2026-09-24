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
PRIVACY_MANIFEST="$APP_PATH/PrivacyInfo.xcprivacy"
ADHAN_STANDARD_SOUND="$APP_PATH/adhan-standard.caf"
ADHAN_FAJR_SOUND="$APP_PATH/adhan-fajr.caf"
QURAN_CORPUS="$APP_PATH/quran-uthmani.json"

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

if [ ! -s "$QURAN_CORPUS" ]; then
  echo "Der gebündelte Quran-Text quran-uthmani.json fehlt im App-Bundle." >&2
  exit 1
fi

QURAN_SHA256="$(/usr/bin/shasum -a 256 "$QURAN_CORPUS" | awk '{print $1}')"
if [ "$QURAN_SHA256" != "0df03e1d6da4fc8138208fec1688f2b416f0dd4ebbd514179f3e5e0fbaf4195f" ]; then
  echo "Unerwarteter Inhalt für quran-uthmani.json." >&2
  exit 1
fi

for sound in "$ADHAN_STANDARD_SOUND" "$ADHAN_FAJR_SOUND"; do
  if [ ! -s "$sound" ]; then
    echo "Gebetsruf-Datei fehlt oder ist leer: $sound" >&2
    exit 1
  fi
done

FAJR_SHA256="$(/usr/bin/shasum -a 256 "$ADHAN_FAJR_SOUND" | awk '{print $1}')"
STANDARD_SHA256="$(/usr/bin/shasum -a 256 "$ADHAN_STANDARD_SOUND" | awk '{print $1}')"
if [ "$FAJR_SHA256" != "e0641b2e4a04f38f38c7cc8479a0a3e4d8c5d9a577d04e9acd32c135fb2df47f" ]; then
  echo "Unerwarteter Inhalt für adhan-fajr.caf." >&2
  exit 1
fi
if [ "$STANDARD_SHA256" != "8752346b8fab95baa41b991790233ef99e85e86728fb8d296113aba274eeef43" ]; then
  echo "Unerwarteter Inhalt für adhan-standard.caf." >&2
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
