from pathlib import Path

# SalahPath v3.60 — release checkpoint after verified v3.57-v3.59
# visual and functional QA passes.

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")

if 'MARKETING_VERSION="3.56"' not in t or 'CURRENT_PROJECT_VERSION="61"' not in t:
    raise SystemExit("v3.60: expected v3.56/61 base version not found")

t = t.replace('MARKETING_VERSION="3.56"', 'MARKETING_VERSION="3.60"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="61"', 'CURRENT_PROJECT_VERSION="65"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.60 / build 65 release checkpoint applied")
