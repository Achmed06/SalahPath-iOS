from pathlib import Path

root = Path.cwd()
build_script = root / "scripts" / "build_unsigned_ipa.sh"
s = build_script.read_text(encoding="utf-8")

if 'MARKETING_VERSION="3.61"' not in s:
    raise SystemExit("v3.72: expected MARKETING_VERSION 3.61 not found")
if 'CURRENT_PROJECT_VERSION="67"' not in s:
    raise SystemExit("v3.72: expected build number 67 not found")

s = s.replace('MARKETING_VERSION="3.61"', 'MARKETING_VERSION="3.62"', 1)
s = s.replace('CURRENT_PROJECT_VERSION="67"', 'CURRENT_PROJECT_VERSION="68"', 1)
build_script.write_text(s, encoding="utf-8")

print("SalahPath release checkpoint prepared: v3.62 / build 68")
