#!/bin/bash
# Only for ephemeral GitHub-hosted macOS runners. No credentials enter artifacts.
set -euo pipefail
set +x
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
[[ "$(uname -s)" = Darwin && "${GITHUB_ACTIONS:-}" = true && "${RUNNER_ENVIRONMENT:-}" = github-hosted ]] || {
  echo 'Use the manually started App Store signed export workflow on a GitHub-hosted Mac.' >&2; exit 1;
}
for name in SALAH_DEVELOPMENT_TEAM SALAH_CERTIFICATE_BASE64 SALAH_CERTIFICATE_PASSWORD SALAH_PROFILE_BASE64; do
  test -n "${!name:-}" || { echo "Missing setting: $name" >&2; exit 1; }
done
[[ "${SALAH_UPLOAD_TO_TESTFLIGHT:-false}" =~ ^(true|false)$ ]] || exit 1
if [[ "${SALAH_UPLOAD_TO_TESTFLIGHT:-false}" = true ]]; then
  for name in SALAH_ASC_KEY_BASE64 SALAH_ASC_KEY_ID SALAH_ASC_ISSUER_ID; do
    test -n "${!name:-}" || { echo "Missing upload setting: $name" >&2; exit 1; }
  done
  [[ "$SALAH_ASC_KEY_ID" =~ ^[A-Z0-9]{10}$ ]] || { echo 'Invalid API key ID' >&2; exit 1; }
  [[ "$SALAH_ASC_ISSUER_ID" =~ ^[A-Fa-f0-9-]{36}$ ]] || { echo 'Invalid API issuer ID' >&2; exit 1; }
fi
umask 077
SIGNING_DIR="$(mktemp -d "$RUNNER_TEMP/salahpath-signing.XXXXXX")"
KEYCHAIN_PATH="$SIGNING_DIR/signing.keychain-db"
PROFILE_DESTINATION=""
cleanup() {
  result=$?
  trap - EXIT
  if test -f "$KEYCHAIN_PATH"; then security delete-keychain "$KEYCHAIN_PATH" >/dev/null 2>&1 || true; fi
  if test -n "$PROFILE_DESTINATION"; then rm -f "$PROFILE_DESTINATION"; fi
  rm -rf "$SIGNING_DIR"
  exit "$result"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
export SALAH_SIGNING_TEMP="$SIGNING_DIR"
python3 - <<'PY'
import base64, os
from pathlib import Path
root = Path(os.environ['SALAH_SIGNING_TEMP'])
files = {'SALAH_CERTIFICATE_BASE64': 'certificate.p12', 'SALAH_PROFILE_BASE64': 'profile.mobileprovision'}
if os.environ.get('SALAH_UPLOAD_TO_TESTFLIGHT') == 'true':
    (root / 'private_keys').mkdir()
    files['SALAH_ASC_KEY_BASE64'] = f"private_keys/AuthKey_{os.environ['SALAH_ASC_KEY_ID']}.p8"
for variable, name in files.items():
    try:
        data = base64.b64decode(''.join(os.environ[variable].split()), validate=True)
        if not data:
            raise ValueError('empty data')
        (root / name).write_bytes(data)
    except ValueError:
        raise SystemExit(f'Invalid Base64 secret: {variable}') from None
PY
security cms -D -i "$SIGNING_DIR/profile.mobileprovision" > "$SIGNING_DIR/profile.plist"
python3 scripts/verify_store_signing.py "$SIGNING_DIR/profile.plist" --team "$SALAH_DEVELOPMENT_TEAM" > "$SIGNING_DIR/profile-check.json"
KEYCHAIN_PASSWORD="$(openssl rand -hex 32)"
security create-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
security set-keychain-settings -lut 3600 "$KEYCHAIN_PATH"
security unlock-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
security import "$SIGNING_DIR/certificate.p12" -P "$SALAH_CERTIFICATE_PASSWORD" -t cert -f pkcs12 \
  -k "$KEYCHAIN_PATH" -T /usr/bin/codesign -T /usr/bin/security >/dev/null
security set-key-partition-list -S apple-tool:,apple:,codesign: -k "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH" >/dev/null
security list-keychains -d user -s "$KEYCHAIN_PATH" "$HOME/Library/Keychains/login.keychain-db"
security find-identity -v -p codesigning "$KEYCHAIN_PATH" > "$SIGNING_DIR/identities.txt"
python3 scripts/verify_store_signing.py "$SIGNING_DIR/profile.plist" --team "$SALAH_DEVELOPMENT_TEAM" \
  --identities "$SIGNING_DIR/identities.txt" > "$SIGNING_DIR/profile-check.json"
SALAH_PROFILE_UUID="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["profile_uuid"])' "$SIGNING_DIR/profile-check.json")"
SALAH_SIGNING_CERT_SHA1="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["certificate_sha1"])' "$SIGNING_DIR/profile-check.json")"
export SALAH_PROFILE_UUID SALAH_SIGNING_CERT_SHA1 SALAH_SIGNING_STYLE=manual
PROFILE_DIRECTORY="$HOME/Library/Developer/Xcode/UserData/Provisioning Profiles"
mkdir -p "$PROFILE_DIRECTORY"
test ! -e "$PROFILE_DIRECTORY/$SALAH_PROFILE_UUID.mobileprovision" || { echo 'Profile already present; refusing to overwrite' >&2; exit 1; }
PROFILE_DESTINATION="$PROFILE_DIRECTORY/$SALAH_PROFILE_UUID.mobileprovision"
cp "$SIGNING_DIR/profile.mobileprovision" "$PROFILE_DESTINATION"
bash scripts/archive_app_store.sh
if [[ "${SALAH_UPLOAD_TO_TESTFLIGHT:-false}" = true ]]; then
  # altool searches ./private_keys. Run from this private temporary directory.
  (
    cd "$SIGNING_DIR"
    xcrun altool --validate-app -f "$ROOT/build/app-store/export/SalahPath.ipa" -t ios \
      --apiKey "$SALAH_ASC_KEY_ID" --apiIssuer "$SALAH_ASC_ISSUER_ID" --output-format json
    xcrun altool --upload-app -f "$ROOT/build/app-store/export/SalahPath.ipa" -t ios \
      --apiKey "$SALAH_ASC_KEY_ID" --apiIssuer "$SALAH_ASC_ISSUER_ID" --output-format json
  )
fi
python3 - <<'PY'
import json, os
from pathlib import Path
uploaded = os.environ.get('SALAH_UPLOAD_TO_TESTFLIGHT') == 'true'
Path('build/app-store/apple-upload-status.json').write_text(json.dumps({
    'upload_command_succeeded': uploaded,
    'apple_processing': 'must_check_in_app_store_connect' if uploaded else 'not_uploaded',
    'testflight_device_tests': 'not_run', 'app_review': 'not_submitted'
}, indent=2) + '\n')
PY
