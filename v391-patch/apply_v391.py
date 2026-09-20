from pathlib import Path

root = Path.cwd()
home = root / "SalahZeit" / "Views" / "HomeView.swift"
s = home.read_text(encoding="utf-8")

old = 'Text("(Nisâ, 103)")'
new = 'Text(settings.t("(An-Nisāʾ 4:103)", "(Nisâ, 103)"))'

if old not in s:
    raise SystemExit("v3.91: Home Quran-reference citation anchor missing")

s = s.replace(old, new, 1)
home.write_text(s, encoding="utf-8")
print("SalahPath v3.91 localized Home Quran-reference citation applied")
