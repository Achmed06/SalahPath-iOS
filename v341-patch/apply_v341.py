from pathlib import Path

# SalahPath v3.41 compatibility pass.
# The original extracted-icon archive became corrupted in-repo.
# Keep the verified v3.40 visual assets and advance the build version safely.

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.40"' not in t or 'CURRENT_PROJECT_VERSION="45"' not in t:
    raise SystemExit("v3.41: expected v3.40/45 build version not found")
t = t.replace('MARKETING_VERSION="3.40"', 'MARKETING_VERSION="3.41"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="45"', 'CURRENT_PROJECT_VERSION="46"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.41 compatibility pass applied")
