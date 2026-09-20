from pathlib import Path

build = Path("scripts/build_unsigned_ipa.sh")
text = build.read_text(encoding="utf-8")

old = 'CURRENT_PROJECT_VERSION="75"'
new = 'CURRENT_PROJECT_VERSION="76"'
if old not in text:
    raise SystemExit("v422: build 75 version anchor missing")

build.write_text(text.replace(old, new, 1), encoding="utf-8")
print("v422 applied: SalahPath v3.62 build 76 checkpoint")
