from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

replacements = {
    '.navigationTitle(settings.t("Namaz lernen", "Namaz Öğren"))':
    '.navigationTitle(settings.t("Gebet lernen", "Namaz Öğren"))',

    '.navigationTitle(settings.t("Namaz lernen", "Namaz öğren"))':
    '.navigationTitle(settings.t("Gebet lernen", "Namaz öğren"))',

    '.navigationTitle(settings.t("Hicri-Kalender", "Hicrî takvim"))':
    '.navigationTitle(settings.t("Hijri-Kalender", "Hicrî takvim"))',
}

for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f"v3.92: prayer-learning title anchor missing: {old}")
    s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")

root_tab = root / "SalahZeit" / "Views" / "RootTabView.swift"
s = root_tab.read_text(encoding="utf-8")

root_replacements = {
    'discoverTile(icon: "figure.mind.and.body", title: settings.t("Namaz lernen", "Namaz Öğren"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))':
    'discoverTile(icon: "figure.mind.and.body", title: settings.t("Gebet lernen", "Namaz Öğren"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))',

    'discoverTile(icon: "drop.fill", title: settings.t("Wudu / Abdest", "Abdest Rehberi"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))':
    'discoverTile(icon: "drop.fill", title: settings.t("Wudu", "Abdest Rehberi"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))',

    'discoverRow(icon: "location.north.circle.fill", title: settings.t("Qibla / Kıble", "Qibla / Kıble"), subtitle: settings.t("Richtung zur Kaaba", "Kâbe yönü"))':
    'discoverRow(icon: "location.north.circle.fill", title: settings.t("Qibla", "Kıble"), subtitle: settings.t("Richtung zur Kaaba", "Kâbe yönü"))',

    'discoverRow(icon: "calendar", title: settings.t("Hicri-Kalender", "Hicrî Takvim"), subtitle: settings.t("Islamischer Kalender", "İslami takvim"))':
    'discoverRow(icon: "calendar", title: settings.t("Hijri-Kalender", "Hicrî Takvim"), subtitle: settings.t("Islamischer Kalender", "İslami takvim"))',
}

for old, new in root_replacements.items():
    if old not in s:
        raise SystemExit(f"v3.92: discover localization anchor missing: {old[:90]}")
    s = s.replace(old, new, 1)

root_tab.write_text(s, encoding="utf-8")

qibla = root / "SalahZeit" / "Views" / "QiblaView.swift"
s = qibla.read_text(encoding="utf-8")
old = 'Text(settings.t("Qibla / Kıble", "Qibla / Kıble"))'
new = 'Text(settings.t("Qibla", "Kıble"))'
if old not in s:
    raise SystemExit("v3.92: Qibla heading localization anchor missing")
s = s.replace(old, new, 1)
qibla.write_text(s, encoding="utf-8")

print("SalahPath v3.92 German prayer/discover/Qibla localization cleanup applied")
