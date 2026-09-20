from pathlib import Path

root = Path.cwd()

guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

anchor = '''private struct QuranBookmark: Hashable {
'''
wrapper = '''struct QuranReaderQAView: View {
    var body: some View {
        QuranSurahView(
            surah: SurahMeta(
                number: 1,
                name: "سُورَةُ ٱلْفَاتِحَةِ",
                englishName: "Al-Faatiha",
                englishNameTranslation: "The Opening",
                numberOfAyahs: 7,
                revelationType: "Meccan"
            ),
            initialAyah: 1
        )
    }
}

'''
if anchor not in s:
    raise SystemExit("v3.80: Quran bookmark anchor missing")
if "struct QuranReaderQAView" not in s:
    s = s.replace(anchor, wrapper + anchor, 1)
guide.write_text(s, encoding="utf-8")

app = root / "SalahZeit" / "SalahZeitApp.swift"
s = app.read_text(encoding="utf-8")
old = '''        case "quran-favorites":
            NavigationStack { QuranFavoritesLandingView() }
'''
new = '''        case "quran-favorites":
            NavigationStack { QuranFavoritesLandingView() }
        case "quran-reader":
            NavigationStack { QuranReaderQAView() }
'''
if old not in s:
    raise SystemExit("v3.80: QA Quran favorites route anchor missing")
s = s.replace(old, new, 1)
app.write_text(s, encoding="utf-8")

print("SalahPath v3.80 Quran reader QA route applied")
