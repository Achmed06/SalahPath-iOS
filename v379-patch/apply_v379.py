from pathlib import Path

root = Path.cwd()

guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''            Picker(settings.t("Ansicht", "Görünüm"), selection: $displayMode) {
                Text("Arapça").tag(0)
                Text("Türkçe").tag(1)
                Text("Deutsch").tag(2)
            }
'''
new = '''            Picker(settings.t("Ansicht", "Görünüm"), selection: $displayMode) {
                Text(settings.t("Arabisch", "Arapça")).tag(0)
                Text(settings.t("Türkisch", "Türkçe")).tag(1)
                Text("Deutsch").tag(2)
            }
'''
if old not in s:
    raise SystemExit("v3.79: Quran reader display picker anchor missing")
s = s.replace(old, new, 1)

old = '''                    Text("Türkçe")
                        .font(.system(size: 8.5, weight: .bold))
'''
new = '''                    Text(settings.t("Türkisch", "Türkçe"))
                        .font(.system(size: 8.5, weight: .bold))
'''
if old not in s:
    raise SystemExit("v3.79: Quran reader Turkish translation label anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")

home = root / "SalahZeit" / "Views" / "HomeView.swift"
s = home.read_text(encoding="utf-8")

old = '''            Text("Günlük Seri")
                .font(.system(size: 7.0, weight: .bold))
                .foregroundStyle(SalahTheme.ink)

            Text("Tage in Folge")
                .font(.system(size: 6.3, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)

            Text("İstikrar\nbaşarının anahtarıdır.")
                .font(.system(size: 5.7, weight: .medium, design: .serif))
'''
new = '''            Text(settings.t("Tägliche Serie", "Günlük Seri"))
                .font(.system(size: 7.0, weight: .bold))
                .foregroundStyle(SalahTheme.ink)

            Text(settings.t("Tage in Folge", "Gün üst üste"))
                .font(.system(size: 6.3, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)

            Text(settings.t(
                "Beständigkeit ist der\nSchlüssel zum Erfolg.",
                "İstikrar\nbaşarının anahtarıdır."
            ))
                .font(.system(size: 5.7, weight: .medium, design: .serif))
'''
if old not in s:
    raise SystemExit("v3.79: home streak localization anchor missing")
s = s.replace(old, new, 1)

home.write_text(s, encoding="utf-8")
print("SalahPath v3.79 Quran reader and home streak localization applied")
