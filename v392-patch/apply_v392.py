from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

replacements = {
    '.navigationTitle(settings.t("Namaz lernen", "Namaz Öğren"))':
    '.navigationTitle(settings.t("Gebet lernen", "Namaz Öğren"))',

    '.navigationTitle(settings.t("Namaz lernen", "Namaz öğren"))':
    '.navigationTitle(settings.t("Gebet lernen", "Namaz öğren"))',
}

for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f"v3.92: prayer-learning title anchor missing: {old}")
    s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.92 localized German prayer-learning navigation titles applied")
