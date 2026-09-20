from pathlib import Path

root = Path("SalahZeit/Views/RootTabView.swift")
text = root.read_text(encoding="utf-8")
old = 'settings.t("Deutsch + Türkisch", "Deutsch + Türkçe")'
new = 'settings.t("Deutsch + Türkisch", "Almanca + Türkçe")'
if old not in text:
    raise SystemExit("v421: RootTab mixed-language anchor missing")
root.write_text(text.replace(old, new, 1), encoding="utf-8")

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")
old = 'settings.t("Arabisch, Türkisch, Deutsch", "Arapça, Türkçe, Deutsch")'
new = 'settings.t("Arabisch, Türkisch, Deutsch", "Arapça, Türkçe, Almanca")'
if old not in text:
    raise SystemExit("v421: Guide mixed-language anchor missing")
guide.write_text(text.replace(old, new, 1), encoding="utf-8")

print("v421 applied: remaining Turkish language labels corrected to Almanca")
