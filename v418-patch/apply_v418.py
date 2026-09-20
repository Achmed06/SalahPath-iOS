from pathlib import Path

build = Path("scripts/build_unsigned_ipa.sh")
text = build.read_text(encoding="utf-8")

old = 'CURRENT_PROJECT_VERSION="73"'
new = 'CURRENT_PROJECT_VERSION="74"'
if old not in text:
    raise SystemExit("v418: build 73 version anchor missing")

build.write_text(text.replace(old, new, 1), encoding="utf-8")
print("v418 applied: SalahPath v3.62 build 74 checkpoint")
