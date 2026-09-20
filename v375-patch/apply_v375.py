from pathlib import Path

root = Path.cwd()

# ---------- Prayer-times overview: honor the selected app language ----------
home = root / "SalahZeit" / "Views" / "HomeView.swift"
s = home.read_text(encoding="utf-8")

old = '''                HStack(spacing: 3) {
                    ForEach(Array(["Bugün", "Haftalık", "Aylık"].enumerated()), id: \.offset) { index, title in
'''
new = '''                HStack(spacing: 3) {
                    let periodTitles = [
                        settings.t("Heute", "Bugün"),
                        settings.t("Wöchentlich", "Haftalık"),
                        settings.t("Monatlich", "Aylık")
                    ]
                    ForEach(Array(periodTitles.enumerated()), id: \.offset) { index, title in
'''
if old not in s:
    raise SystemExit("v3.75: prayer period tabs anchor missing")
s = s.replace(old, new, 1)

old = '''        .navigationTitle(settings.t("Gebetszeiten", "Gebetszeiten"))
'''
new = '''        .navigationTitle(settings.t("Gebetszeiten", "Namaz Vakitleri"))
'''
if old not in s:
    raise SystemExit("v3.75: prayer-times navigation title anchor missing")
s = s.replace(old, new, 1)

old = '''            Text("Kıble Yönü")
                .font(.custom("AvenirNext-DemiBold", size: 10.6))
                .foregroundStyle(SalahTheme.ink)
            Text("Qibla")
'''
new = '''            Text(settings.t("Qibla-Richtung", "Kıble Yönü"))
                .font(.custom("AvenirNext-DemiBold", size: 10.6))
                .foregroundStyle(SalahTheme.ink)
            Text("Qibla")
'''
if old not in s:
    raise SystemExit("v3.75: Qibla tile title anchor missing")
s = s.replace(old, new, 1)

old = '''                            Link(destination: URL(string: "https://maps.apple.com/?q=Kaaba&ll=21.4225,39.8262")!) {
                                referenceMapTile
                            }
                            .buttonStyle(.plain)
'''
new = '''                            Link(destination: URL(string: "https://maps.apple.com/?q=Kaaba&ll=21.4225,39.8262")!) {
                                referenceMapTile
                            }
                            .buttonStyle(.plain)
                            .accessibilityLabel(settings.t(
                                "Kaaba in Apple Maps öffnen",
                                "Kâbe'yi Apple Maps'te aç"
                            ))
'''
if old not in s:
    raise SystemExit("v3.75: Kaaba map link anchor missing")
s = s.replace(old, new, 1)

home.write_text(s, encoding="utf-8")

# ---------- Dhikr screen: localize tabs, translations and navigation rows ----------
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''    private var tabs: [String] { ["Sabah", "Akşam", "Günlük", "Özel"] }

    private var activeDhikr: (arabic: String, latin: String, german: String) {
        switch section {
        case 1:
            return ("سُبْحَانَ اللّٰهِ وَبِحَمْدِهِ", "Sübhânallâhi ve bihamdihî", "Gepriesen sei Allah und Ihm gebührt Lob.")
        case 2:
            return ("لَا إِلٰهَ إِلَّا اللّٰهُ", "Lâ ilâhe illallâh", "Es gibt keinen Gott außer Allah.")
        case 3:
            return ("اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ", "Allâhümme salli alâ Muhammed", "Allah, segne Muhammad.")
        default:
            return ("أَسْتَغْفِرُ اللّٰهَ", "Estağfirullâh", "Ich bitte Allah um Vergebung.")
        }
    }
'''
new = '''    private var tabs: [String] {
        [
            settings.t("Morgen", "Sabah"),
            settings.t("Abend", "Akşam"),
            settings.t("Täglich", "Günlük"),
            settings.t("Spezial", "Özel")
        ]
    }

    private var activeDhikr: (arabic: String, latin: String, translation: String) {
        switch section {
        case 1:
            return (
                "سُبْحَانَ اللّٰهِ وَبِحَمْدِهِ",
                "Sübhânallâhi ve bihamdihî",
                settings.t("Gepriesen sei Allah und Ihm gebührt Lob.", "Allah'ı hamdiyle tesbih ederim.")
            )
        case 2:
            return (
                "لَا إِلٰهَ إِلَّا اللّٰهُ",
                "Lâ ilâhe illallâh",
                settings.t("Es gibt keinen Gott außer Allah.", "Allah'tan başka ilah yoktur.")
            )
        case 3:
            return (
                "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ",
                "Allâhümme salli alâ Muhammed",
                settings.t("Allah, segne Muhammad.", "Allah'ım, Muhammed'e salât eyle.")
            )
        default:
            return (
                "أَسْتَغْفِرُ اللّٰهَ",
                "Estağfirullâh",
                settings.t("Ich bitte Allah um Vergebung.", "Allah'tan bağışlanma dilerim.")
            )
        }
    }
'''
if old not in s:
    raise SystemExit("v3.75: Dhikr tabs/translation anchor missing")
s = s.replace(old, new, 1)

old = '''                    Text(activeDhikr.german)
'''
new = '''                    Text(activeDhikr.translation)
'''
if old not in s:
    raise SystemExit("v3.75: Dhikr visible translation anchor missing")
s = s.replace(old, new, 1)

replacements = [
    ('title: "Sabah & Akşam Zikirleri",', 'title: settings.t("Morgen- & Abend-Adhkar", "Sabah & Akşam Zikirleri"),'),
    ('title: "Günlük Dualar",', 'title: settings.t("Tägliche Duas", "Günlük Dualar"),'),
    ('title: "Tesbih Sayacı",', 'title: settings.t("Tasbih-Zähler", "Tesbih Sayacı"),'),
    ('title: "Arapça, Türkçe, Deutsch",', 'title: settings.t("Arabisch, Türkisch, Deutsch", "Arapça, Türkçe, Deutsch"),'),
    ('title: "Sesli dinleme",', 'title: settings.t("Audio anhören", "Sesli dinleme"),'),
]
for old, new in replacements:
    if old not in s:
        raise SystemExit(f"v3.75: Dhikr row anchor missing: {old}")
    s = s.replace(old, new, 1)

# Quran language tabs should also follow German/Turkish UI language.
old = '''                            ForEach(Array(["Arapça", "Türkçe", "Deutsch"].enumerated()), id: \.offset) { index, title in
'''
new = '''                            let quranLanguageTabs = [
                                settings.t("Arabisch", "Arapça"),
                                settings.t("Türkisch", "Türkçe"),
                                "Deutsch"
                            ]
                            ForEach(Array(quranLanguageTabs.enumerated()), id: \.offset) { index, title in
'''
if old not in s:
    raise SystemExit("v3.75: Quran language-tabs anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.75 localization consistency patch applied")
