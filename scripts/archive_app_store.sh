#!/bin/bash
# Requires an enrolled Apple Developer team and a configured signing keychain.
# Produces a signed export locally. Does not upload or submit to App Review.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
: "${SALAH_DEVELOPMENT_TEAM:?Set SALAH_DEVELOPMENT_TEAM to your Apple Developer Team ID}"
[[ "$SALAH_DEVELOPMENT_TEAM" =~ ^[A-Z0-9]{10}$ ]] || { echo "Invalid Apple Team ID" >&2; exit 1; }
[[ "$(uname -s)" = Darwin ]] || { echo "Signed export requires macOS and Xcode" >&2; exit 1; }
test -z "$(git status --porcelain)" || { echo "Commit or preserve local changes before signing" >&2; exit 1; }
export SALAH_SIGNING_STYLE="${SALAH_SIGNING_STYLE:-automatic}"
SIGNING_ARGS=(DEVELOPMENT_TEAM="$SALAH_DEVELOPMENT_TEAM")
PROVISIONING_ARGS=()
case "$SALAH_SIGNING_STYLE" in
  automatic)
    SIGNING_ARGS+=(CODE_SIGN_STYLE=Automatic)
    PROVISIONING_ARGS+=(-allowProvisioningUpdates)
    ;;
  manual)
    : "${SALAH_PROFILE_UUID:?Set the installed App Store profile UUID}"
    : "${SALAH_SIGNING_CERT_SHA1:?Set the matching distribution identity SHA-1}"
    [[ "$SALAH_PROFILE_UUID" =~ ^[A-Fa-f0-9-]{36}$ ]] || exit 1
    [[ "$SALAH_SIGNING_CERT_SHA1" =~ ^[A-Fa-f0-9]{40}$ ]] || exit 1
    SIGNING_ARGS+=(CODE_SIGN_STYLE=Manual CODE_SIGN_IDENTITY="$SALAH_SIGNING_CERT_SHA1"
                   PROVISIONING_PROFILE_SPECIFIER="$SALAH_PROFILE_UUID")
    ;;
  *) echo "Unknown signing style" >&2; exit 1 ;;
esac
./scripts/preflight_reference_build.sh
ARCHIVE_PATH="$ROOT/build/app-store/SalahPath.xcarchive"
EXPORT_PATH="$ROOT/build/app-store/export"
test ! -e "$ROOT/build/app-store" || { echo "Preserve the existing build/app-store directory before continuing." >&2; exit 1; }
mkdir -p build/app-store
xcodebuild -project SalahZeit.xcodeproj -scheme SalahZeit -configuration Release \
  -destination 'generic/platform=iOS' -archivePath "$ARCHIVE_PATH" \
  -derivedDataPath build/app-store/DerivedData \
  "${SIGNING_ARGS[@]}" ${PROVISIONING_ARGS[@]+"${PROVISIONING_ARGS[@]}"} archive
python3 scripts/verify_release_bundle.py "$ARCHIVE_PATH/Products/Applications/SalahPath.app" \
  --report build/app-store/archive-verification.json
python3 - <<'PY'
import os, plistlib
options = {'method': 'app-store-connect', 'destination': 'export',
           'teamID': os.environ['SALAH_DEVELOPMENT_TEAM'],
           'signingStyle': os.environ['SALAH_SIGNING_STYLE'],
           'manageAppVersionAndBuildNumber': False, 'uploadSymbols': True}
if os.environ['SALAH_SIGNING_STYLE'] == 'manual':
    options['provisioningProfiles'] = {'com.achmed06.salahpath': os.environ['SALAH_PROFILE_UUID']}
    options['signingCertificate'] = os.environ['SALAH_SIGNING_CERT_SHA1']
with open('build/app-store/ExportOptions.plist', 'wb') as file:
    plistlib.dump(options, file)
PY
xcodebuild -exportArchive -archivePath "$ARCHIVE_PATH" \
  -exportPath "$EXPORT_PATH" -exportOptionsPlist build/app-store/ExportOptions.plist \
  ${PROVISIONING_ARGS[@]+"${PROVISIONING_ARGS[@]}"}
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
/usr/bin/codesign -d --extract-certificates "$VERIFY_PATH/cert-" "$APP_PATH"
python3 scripts/verify_store_signing.py "$VERIFY_PATH/profile.plist" --team "$SALAH_DEVELOPMENT_TEAM" \
  --entitlements "$VERIFY_PATH/entitlements.plist" --certificate "$VERIFY_PATH/cert-0" \
  --report build/app-store/signing-verification.json
python3 - "$IPA_PATH" <<'PY'
import hashlib, json, subprocess, sys
from pathlib import Path
ipa = Path(sys.argv[1])
report = json.loads(Path('build/app-store/export-verification.json').read_text())
report.update(source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
              ipa_sha256=hashlib.sha256(ipa.read_bytes()).hexdigest(),
              artifact_kind='signed-app-store-export', apple_processing='not_checked',
              device_testing='not_checked', app_review='not_submitted')
Path('build/app-store/SalahPath-signed.provenance.json').write_text(json.dumps(report, indent=2) + '\n')
PY
echo "Signed export verified: $IPA_PATH (not uploaded)"
