from pathlib import Path

root = Path.cwd()

# ---------- Guide copy: do not promise audio where only learning links exist ----------
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''                    dhikrReferenceRow(
                        icon: "speaker.wave.2.fill",
                        title: settings.t("Audio anhören", "Sesli dinleme"),
                        subtitle: settings.t("Mit Audio anhören", "Sesli dinleme")
                    ) {
                        PrayerDuaAudioView()
                    }
'''
new = '''                    dhikrReferenceRow(
                        icon: "text.book.closed.fill",
                        title: settings.t("Gebetsduas", "Namaz duaları"),
                        subtitle: settings.t("Offizielle Lernquellen", "Resmî öğrenme kaynakları")
                    ) {
                        PrayerDuaAudioView()
                    }
'''
if old not in s:
    raise SystemExit("v3.85: Dhikr prayer-dua row anchor missing")
s = s.replace(old, new, 1)

old = '''                    "Gebetsduas und kurze Suren sind getrennt: Duas sind Bittgebete; Suren sind Quran-Kapitel. Für Gebetsduas verlinkt SalahPath derzeit auf offizielle Diyanet-Lernquellen, statt instabile MP3-Links vorzutäuschen.",
                    "Namaz duaları ve kısa sureler ayrıdır: Dualar yakarışlardır; sureler Kur'an bölümleridir. SalahPath, bozuk MP3 bağlantıları yerine namaz dualarında şimdilik resmî Diyanet öğrenme kaynaklarını açar."
'''
new = '''                    "Gebetsduas und kurze Suren sind getrennt: Duas sind Bittgebete; Suren sind Quran-Kapitel. Für Gebetsduas öffnet SalahPath derzeit offizielle Diyanet-Lernquellen.",
                    "Namaz duaları ve kısa sureler ayrıdır: Dualar yakarışlardır; sureler Kur'an bölümleridir. SalahPath namaz duaları için şu anda resmî Diyanet öğrenme kaynaklarını açar."
'''
if old not in s:
    raise SystemExit("v3.85: Prayer dua explanatory copy anchor missing")
s = s.replace(old, new, 1)

old = 'learningFeature(settings.t("Mit Bildern und gesprochenem Text", "Görsel ve okunan metinlerle"), icon: "checkmark.circle.fill")'
new = 'learningFeature(settings.t("Mit Bildern und Rezitationstexten", "Görsel ve okunan metinlerle"), icon: "checkmark.circle.fill")'
if old not in s:
    raise SystemExit("v3.85: prayer learning feature copy anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")

# ---------- Discover tile: truthful destination ----------
root_tab = root / "SalahZeit" / "Views" / "RootTabView.swift"
s = root_tab.read_text(encoding="utf-8")
old = '''                    NavigationLink { PrayerDuaAudioView() } label: {
                        discoverTile(icon: "speaker.wave.2.fill", title: settings.t("Gebetsduas", "Namaz Duaları"), subtitle: settings.t("Lesen & hören", "Oku & dinle"))
                    }
'''
new = '''                    NavigationLink { PrayerDuaAudioView() } label: {
                        discoverTile(icon: "text.book.closed.fill", title: settings.t("Gebetsduas", "Namaz Duaları"), subtitle: settings.t("Lesen & lernen", "Oku & öğren"))
                    }
'''
if old not in s:
    raise SystemExit("v3.85: Discover prayer-dua tile anchor missing")
s = s.replace(old, new, 1)
root_tab.write_text(s, encoding="utf-8")

# ---------- Settings footer localization ----------
settings = root / "SalahZeit" / "Views" / "SettingsView.swift"
s = settings.read_text(encoding="utf-8")
old = 'Text(settings.t("İbadetle Daha Güzel Bir Hayat", "İbadetle Daha Güzel Bir Hayat"))'
new = 'Text(settings.t("Ein schöneres Leben durch Anbetung", "İbadetle Daha Güzel Bir Hayat"))'
if old not in s:
    raise SystemExit("v3.85: Settings footer tagline anchor missing")
s = s.replace(old, new, 1)
settings.write_text(s, encoding="utf-8")

# ---------- Expand QA routing for screens not yet captured ----------
app = root / "SalahZeit" / "SalahZeitApp.swift"
s = app.read_text(encoding="utf-8")
anchor = '''        case "settings":
            NavigationStack { SettingsView() }
        default:
            RootTabView()
'''
replacement = '''        case "settings":
            NavigationStack { SettingsView() }
        case "more":
            NavigationStack { MoreView() }
        case "fasting":
            NavigationStack { FastingTrackerView() }
        case "hijri":
            NavigationStack { HijriCalendarView() }
        case "terms":
            NavigationStack { PrayerTermsView() }
        case "surahs":
            NavigationStack { ShortSurahLearningView() }
        case "positions":
            NavigationStack { PrayerSequenceReferenceView() }
        case "rakats":
            NavigationStack { RakatOverviewView() }
        case "hanafi-plan":
            NavigationStack { HanafiPrayerPlanView() }
        case "tracker-pause":
            NavigationStack { TrackerPauseView() }
        default:
            RootTabView()
'''
if anchor not in s:
    raise SystemExit("v3.85: QA route insertion anchor missing")
s = s.replace(anchor, replacement, 1)
app.write_text(s, encoding="utf-8")

print("SalahPath v3.85 truthful prayer-dua copy + expanded QA routes applied")
