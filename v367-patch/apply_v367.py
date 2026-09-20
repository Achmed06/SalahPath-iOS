from pathlib import Path

root = Path.cwd()
tab = root / "SalahZeit" / "Views" / "RootTabView.swift"
s = tab.read_text(encoding="utf-8")

old = '''    private var items: [(String, String)] {
        [
            ("house.fill", "Ana Sayfa"),
            ("book.fill", "Kur'an"),
            ("figure.mind.and.body", "Namaz"),
            ("location.north.circle", "Keşfet"),
            ("person.crop.circle", "Profil")
        ]
    }
'''
new = '''    private var items: [(String, String)] {
        [
            ("house.fill", settings.t("Start", "Ana Sayfa")),
            ("book.fill", settings.t("Koran", "Kur'an")),
            ("figure.mind.and.body", settings.t("Gebet", "Namaz")),
            ("location.north.circle", settings.t("Entdecken", "Keşfet")),
            ("person.crop.circle", settings.t("Profil", "Profil"))
        ]
    }
'''
if old not in s:
    raise SystemExit("v3.67: bottom-tab localization anchor missing")
s = s.replace(old, new, 1)

tab.write_text(s, encoding="utf-8")
print("SalahPath v3.67 bottom navigation localization applied")
