#!/bin/bash
# Requires an enrolled Apple Developer team and a configured signing keychain.
# Produces a signed export locally. Does not upload or submit to App Review.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
: "${SALAH_DEVELOPMENT_TEAM:?Set SALAH_DEVELOPMENT_TEAM to your Apple Developer Team ID}"
[[ "$SALAH_DEVELOPMENT_TEAM" =~ ^[A-Z0-9]{10}$ ]] || { echo "Invalid Apple Team ID" >&2; exit 1; }
./scripts/preflight_reference_build.sh
ARCHIVE_PATH="$ROOT/build/app-store/SalahPath.xcarchive"
EXPORT_PATH="$ROOT/build/app-store/export"
test ! -e "$ARCHIVE_PATH" || { echo "Archive already exists: $ARCHIVE_PATH. Preserve or remove it before continuing." >&2; exit 1; }
mkdir -p build/app-store
xcodebuild -project SalahZeit.xcodeproj -scheme SalahZeit -configuration Release \
  -destination 'generic/platform=iOS' -archivePath "$ARCHIVE_PATH" \
  -derivedDataPath build/app-store/DerivedData \
  DEVELOPMENT_TEAM="$SALAH_DEVELOPMENT_TEAM" CODE_SIGN_STYLE=Automatic \
  -allowProvisioningUpdates archive
python3 scripts/verify_release_bundle.py "$ARCHIVE_PATH/Products/Applications/SalahPath.app" \
  --report build/app-store/archive-verification.json
python3 - <<'PY'
import os, plistlib
with open('build/app-store/ExportOptions.plist', 'wb') as file:
    plistlib.dump({'method': 'app-store-connect', 'destination': 'export',
                  'teamID': os.environ['SALAH_DEVELOPMENT_TEAM'], 'signingStyle': 'automatic',
                  'manageAppVersionAndBuildNumber': False, 'uploadSymbols': True}, file)
PY
xcodebuild -exportArchive -archivePath "$ARCHIVE_PATH" \
  -exportPath "$EXPORT_PATH" -exportOptionsPlist build/app-store/ExportOptions.plist \
  -allowProvisioningUpdates
IPA_PATH="$EXPORT_PATH/SalahPath.ipa"
test -s "$IPA_PATH"
VERIFY_PATH="$(mktemp -d "$ROOT/build/app-store/verify.XXXXXX")"
trap 'rm -rf "$VERIFY_PATH"' EXIT
/usr/bin/unzip -q "$IPA_PATH" -d "$VERIFY_PATH"
APP_PATH="$VERIFY_PATH/Payload/SalahPath.app"
python3 scripts/verify_release_bundle.py "$APP_PATH" --report build/app-store/export-verification.json
/usr/bin/codesign --verify --deep --strict "$APP_PATH"
/usr/bin/codesign -d --entitlements :- "$APP_PATH" > "$VERIFY_PATH/entitlements.plist"
/usr/bin/security cms -D -i "$APP_PATH/embedded.mobileprovision" > "$VERIFY_PATH/profile.plist"
python3 - "$VERIFY_PATH" <<'PY'
import os, plistlib, sys
from pathlib import Path
root = Path(sys.argv[1])
with (root / 'entitlements.plist').open('rb') as file: entitlements = plistlib.load(file)
with (root / 'profile.plist').open('rb') as file: profile = plistlib.load(file)
team = os.environ['SALAH_DEVELOPMENT_TEAM']
assert entitlements.get('com.apple.developer.team-identifier') == team, 'Wrong signing team'
assert not entitlements.get('get-task-allow', False), 'Development signing is not an App Store export'
assert entitlements.get('application-identifier', '').endswith('.com.achmed06.salahpath'), 'Wrong signed app ID'
assert entitlements.get('com.apple.developer.usernotifications.time-sensitive') is True, 'Missing Time Sensitive entitlement'
assert 'ProvisionedDevices' not in profile and not profile.get('ProvisionsAllDevices'), 'Not App Store distribution'
assert profile.get('Entitlements', {}).get('beta-reports-active') is True, 'Missing App Store distribution entitlement'
PY
echo "Signed export verified: $IPA_PATH (not uploaded)"
