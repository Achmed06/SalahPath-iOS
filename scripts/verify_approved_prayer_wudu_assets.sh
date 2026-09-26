#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MANIFEST="qa/approved-prayer-wudu-assets.tsv"

if [[ ! -f "$MANIFEST" ]]; then
  echo "ERROR: missing $MANIFEST" >&2
  exit 1
fi

tmp_expected="$(mktemp)"
tmp_actual="$(mktemp)"
trap 'rm -f "$tmp_expected" "$tmp_actual"' EXIT

awk -F '\t' '!/^#/ && NF >= 3 { print $3 }' "$MANIFEST" | LC_ALL=C sort > "$tmp_expected"

find SalahZeit/Assets.xcassets -type f \
  \( -path '*/male_*.imageset/*' -o -path '*/female_*.imageset/*' -o -path '*/wudu_*.imageset/*' \) \
  | LC_ALL=C sort > "$tmp_actual"

if ! diff -u "$tmp_expected" "$tmp_actual"; then
  echo "ERROR: approved Prayer/Wudu asset set changed." >&2
  echo "Do not add/remove/rename these assets without explicit user approval." >&2
  exit 1
fi

fail=0
while IFS=$'\t' read -r expected_sha expected_size path; do
  [[ "$expected_sha" == \#* || -z "$expected_sha" ]] && continue

  if [[ ! -f "$path" ]]; then
    echo "ERROR: missing approved asset: $path" >&2
    fail=1
    continue
  fi

  actual_sha="$(git hash-object "$path")"
  actual_size="$(wc -c < "$path" | tr -d '[:space:]')"

  if [[ "$actual_sha" != "$expected_sha" ]]; then
    echo "ERROR: approved asset changed: $path" >&2
    echo "  expected blob: $expected_sha" >&2
    echo "  actual blob:   $actual_sha" >&2
    fail=1
  fi

  if [[ "$actual_size" != "$expected_size" ]]; then
    echo "ERROR: approved asset size changed: $path ($expected_size -> $actual_size)" >&2
    fail=1
  fi
done < "$MANIFEST"

if [[ "$fail" -ne 0 ]]; then
  echo "Approved Prayer/Wudu asset verification FAILED." >&2
  exit 1
fi

echo "Approved Prayer/Wudu assets: LOCKED and unchanged (74 files)."
