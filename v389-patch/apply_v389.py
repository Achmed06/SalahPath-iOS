from pathlib import Path

root = Path.cwd()
home = root / "SalahZeit" / "Views" / "HomeView.swift"
s = home.read_text(encoding="utf-8")

replacements = {
    'Text("İbadetle Daha Güzel Bir Hayat")':
    'Text(settings.t("Ein schöneres Leben durch Anbetung", "İbadetle Daha Güzel Bir Hayat"))',

    'Text("„Şüphesiz namaz, müminlere vakitleri belli bir farzdır.“")':
    'Text(settings.t("„Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.“", "„Şüphesiz namaz, müminlere vakitleri belli bir farzdır.“"))',

    'Text("„Namaz, müminlere vakitleri belirlenmiş bir farzdır.“ (Nisâ, 103)")':
    'Text(settings.t("„Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.“ (An-Nisāʾ 4:103)", "„Namaz, müminlere vakitleri belirlenmiş bir farzdır.“ (Nisâ, 103)"))',

    '''                Text("“Küçük adımlar, büyük değişimler getirir.”")
                    .font(.custom("Georgia-Italic", size: 9.1))
                    .italic()
                    .foregroundStyle(SalahTheme.ink)
                Text("Kleine Schritte bringen große Veränderungen.")
                    .font(.custom("AvenirNext-Medium", size: 7.6))
                    .foregroundStyle(SalahTheme.mutedInk)''':
    '''                Text(settings.t("„Kleine Schritte bringen große Veränderungen.“", "“Küçük adımlar, büyük değişimler getirir.”"))
                    .font(.custom("Georgia-Italic", size: 9.1))
                    .italic()
                    .foregroundStyle(SalahTheme.ink)''',

    'Text("Sıradaki Namaz / Nächstes Gebet")':
    'Text(settings.t("Nächstes Gebet", "Sıradaki Namaz"))',

    'Text(isScreenshotQA ? "14 Mart 2025" : gregorianDateShort(effectiveNow))':
    'Text(gregorianDateShort(effectiveNow))',

    'Text(isScreenshotQA ? "Cuma" : shortWeekday(effectiveNow))':
    'Text(shortWeekday(effectiveNow))',

    'Text(isScreenshotQA ? "İkindi" : prayer.kind.localizedName(settings.language))':
    'Text(prayer.kind.localizedName(settings.language))',

    '''                    let segments = isScreenshotQA
                        ? [("4", "Sünnet"), ("4", "Farz"), ("2", "Sünnet")]
                        : referenceSequence(for: prayer.kind)''':
    '''                    let segments = referenceSequence(for: prayer.kind)''',

    '''        let meaning = isScreenshotQA
            ? "Rabbim, ilmimi artır."
            : (settings.language == .german ? dua.deMeaning : dua.trMeaning)''':
    '''        let meaning = isScreenshotQA
            ? settings.t("Mein Herr, mehre mein Wissen.", "Rabbim, ilmimi artır.")
            : (settings.language == .german ? dua.deMeaning : dua.trMeaning)''',

    'Text("Günün Duası / Dua des Tages")':
    'Text(settings.t("Dua des Tages", "Günün Duası"))',

    'Text("Namaz Takibi / Gebets-Tracking")':
    'Text(settings.t("Gebets-Tracking", "Namaz Takibi"))',

    '''        let qaLabels = ["Pzt", "Sal", "Çar", "Prş", "Cum", "Cts", "Paz"]
        let done: Bool''':
    '''        let done: Bool''',

    'let label = isScreenshotQA ? qaLabels[index] : shortWeekdayLetter(date)':
    'let label = shortWeekdayLetter(date)',

    'DashboardTile(title: "Kur\'an", subtitle: "Oku & Dinle", icon: "quran")':
    'DashboardTile(title: settings.t("Quran", "Kur\'an"), subtitle: settings.t("Lesen & hören", "Oku & Dinle"), icon: "quran")',

    'DashboardTile(title: "Dua &\\nZikir", subtitle: "", icon: "dhikr")':
    'DashboardTile(title: settings.t("Dua &\\nDhikr", "Dua &\\nZikir"), subtitle: "", icon: "dhikr")',

    'DashboardTile(title: "Namaz\\nÖğren", subtitle: "", icon: "prayer")':
    'DashboardTile(title: settings.t("Gebet\\nlernen", "Namaz\\nÖğren"), subtitle: "", icon: "prayer")',

    'DashboardTile(title: "Abdest\\nRehberi", subtitle: "", icon: "wudu")':
    'DashboardTile(title: settings.t("Wudu\\nAnleitung", "Abdest\\nRehberi"), subtitle: "", icon: "wudu")',

    'DashboardTile(title: "Gebetszeiten", subtitle: "Namaz Vakitleri", icon: "times")':
    'DashboardTile(title: settings.t("Gebetszeiten", "Namaz Vakitleri"), subtitle: "", icon: "times")',

    'DashboardTile(title: "Kıble Yönü", subtitle: "Qibla", icon: "qibla")':
    'DashboardTile(title: settings.t("Qibla", "Kıble Yönü"), subtitle: settings.t("Richtung", "Qibla"), icon: "qibla")',

    'DashboardTile(title: "İslami Bilgiler", subtitle: "Bilgi", icon: "info")':
    'DashboardTile(title: settings.t("Islamisches Wissen", "İslami Bilgiler"), subtitle: settings.t("Wissen", "Bilgi"), icon: "info")',

    'DashboardTile(title: "Favorilerim", subtitle: "Favorilerim", icon: "fav")':
    'DashboardTile(title: settings.t("Favoriten", "Favoriler"), subtitle: "", icon: "fav")',
}

for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f"v3.89: home localization anchor missing: {old[:80]}")
    s = s.replace(old, new, 1)

home.write_text(s, encoding="utf-8")
print("SalahPath v3.89 home language + language-aware QA cleanup applied")
