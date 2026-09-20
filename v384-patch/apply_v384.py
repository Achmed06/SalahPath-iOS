from pathlib import Path

root = Path.cwd()
build_script = root / "scripts" / "build_unsigned_ipa.sh"
s = build_script.read_text(encoding="utf-8")

if 'MARKETING_VERSION="3.62"' not in s:
    raise SystemExit("v3.84: expected MARKETING_VERSION 3.62 not found")
if 'CURRENT_PROJECT_VERSION="71"' not in s:
    raise SystemExit("v3.84: expected build number 71 not found")

s = s.replace('CURRENT_PROJECT_VERSION="71"', 'CURRENT_PROJECT_VERSION="72"', 1)
build_script.write_text(s, encoding="utf-8")

print("SalahPath release checkpoint prepared: v3.62 / build 72")
