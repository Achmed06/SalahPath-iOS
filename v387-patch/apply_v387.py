from pathlib import Path

root = Path.cwd()

# ---------- Prayer guide wording + stable official Diyanet links ----------
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = 'german: "Mit Bildern und gesprochenem Text"'
new = 'german: "Mit Bildern und Rezitationstexten"'
if old not in s:
    raise SystemExit("v3.87: main prayer feature wording anchor missing")
s = s.replace(old, new, 1)

old = '"Hanafi-Lernmodus: Handlung und gesprochener Text werden getrennt gezeigt."'
new = '"Hanafi-Lernmodus: Handlung und Rezitationstext werden getrennt gezeigt."'
if old not in s:
    raise SystemExit("v3.87: prayer learning note anchor missing")
s = s.replace(old, new, 1)

old_url = 'https://yayin.diyanet.gov.tr/File/Download?id=436&path=dinim_islam.pdf'
new_url = 'https://namaz.diyanet.gov.tr/namaz/assets/dosya/Namaz_ilmihali_2011%28SON%29.pdf'
count = s.count(old_url)
if count != 2:
    raise SystemExit(f"v3.87: expected 2 legacy Diyanet prayer-dua URLs, found {count}")
s = s.replace(old_url, new_url)

guide.write_text(s, encoding="utf-8")

# ---------- Calculation-method names must follow app language ----------
model = root / "SalahZeit" / "Models" / "AppSettings.swift"
s = model.read_text(encoding="utf-8")

old = '''    var title: String {
        switch self {
        case .muslimWorldLeague: return "Muslim World League"
        case .moonsightingCommittee: return "Moonsighting Committee"
        case .turkey: return "Diyanet / Türkiye (yaklaşım)"
        case .egyptian: return "Egyptian General Authority"
        case .karachi: return "Karachi"
        case .ummAlQura: return "Umm al-Qura"
        case .northAmerica: return "ISNA / Nordamerika"
        case .dubai: return "Dubai"
        case .qatar: return "Qatar"
        case .kuwait: return "Kuwait"
        case .singapore: return "Singapur"
        case .tehran: return "Teheran"
        }
    }
'''
new = '''    func title(_ language: AppLanguage) -> String {
        switch self {
        case .muslimWorldLeague: return "Muslim World League"
        case .moonsightingCommittee: return "Moonsighting Committee"
        case .turkey:
            return language == .german ? "Diyanet / Türkei (Annäherung)" : "Diyanet / Türkiye (yaklaşım)"
        case .egyptian: return "Egyptian General Authority"
        case .karachi: return "Karachi"
        case .ummAlQura: return "Umm al-Qura"
        case .northAmerica:
            return language == .german ? "ISNA / Nordamerika" : "ISNA / Kuzey Amerika"
        case .dubai: return "Dubai"
        case .qatar: return "Qatar"
        case .kuwait: return "Kuwait"
        case .singapore: return "Singapur"
        case .tehran:
            return language == .german ? "Teheran" : "Tahran"
        }
    }
'''
if old not in s:
    raise SystemExit("v3.87: CalculationPreset title block anchor missing")
s = s.replace(old, new, 1)
model.write_text(s, encoding="utf-8")

settings = root / "SalahZeit" / "Views" / "SettingsView.swift"
s = settings.read_text(encoding="utf-8")
old = 'Button(method.title) { settings.calculationPreset = method }'
new = 'Button(method.title(settings.language)) { settings.calculationPreset = method }'
if old not in s:
    raise SystemExit("v3.87: calculation method menu anchor missing")
s = s.replace(old, new, 1)

old = 'value: settings.calculationPreset.title)'
new = 'value: settings.calculationPreset.title(settings.language))'
if old not in s:
    raise SystemExit("v3.87: selected calculation title anchor missing")
s = s.replace(old, new, 1)
settings.write_text(s, encoding="utf-8")

print("SalahPath v3.87 final copy/link/localization cleanup applied")
