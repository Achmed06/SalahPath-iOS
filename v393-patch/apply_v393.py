from pathlib import Path

root = Path.cwd()
build_script = root / "scripts" / "build_unsigned_ipa.sh"
s = build_script.read_text(encoding="utf-8")

old = 'CURRENT_PROJECT_VERSION="72"'
new = 'CURRENT_PROJECT_VERSION="73"'

if old not in s:
    raise SystemExit("v3.93: build-number 72 anchor missing")

s = s.replace(old, new, 1)
build_script.write_text(s, encoding="utf-8")
print("SalahPath v3.93 release checkpoint: CURRENT_PROJECT_VERSION 73")
