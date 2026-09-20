from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''        .navigationTitle("Dua & Zikir")
'''
new = '''        .navigationTitle(settings.t("Dua & Dhikr", "Dua & Zikir"))
'''
if old not in s:
    raise SystemExit("v3.68: Dhikr navigation title anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.68 Dhikr title localization applied")
