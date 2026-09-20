from pathlib import Path

build = Path("scripts/build_unsigned_ipa.sh")
text = build.read_text(encoding="utf-8")

old = 'CURRENT_PROJECT_VERSION="74"'
new = 'CURRENT_PROJECT_VERSION="75"'
if old not in text:
    raise SystemExit("v420: build 74 version anchor missing")

build.write_text(text.replace(old, new, 1), encoding="utf-8")
print("v420 applied: SalahPath v3.62 build 75 checkpoint")
