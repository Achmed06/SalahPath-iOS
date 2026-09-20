from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

marker = "\nstruct QuranJuzQAView: View {"
if marker not in text:
    raise SystemExit("v425: QuranJuzQAView marker missing")

qa_view = r'''
struct QuranProgressQAView: View {
    var body: some View {
        QuranView()
            .onAppear {
                QuranBookmarkStore.setLastRead(surah: 2, ayah: 142)
            }
    }
}
'''
text = text.replace(marker, qa_view + marker, 1)
guide.write_text(text, encoding="utf-8")

app = Path("SalahZeit/SalahZeitApp.swift")
app_text = app.read_text(encoding="utf-8")
anchor = '''        case "quran-juz":
            NavigationStack {
                QuranJuzQAView()
            }
'''
replacement = anchor + '''        case "quran-progress":
            NavigationStack {
                QuranProgressQAView()
            }
'''
if anchor not in app_text:
    raise SystemExit("v425: quran-juz QA route anchor missing")
app.write_text(app_text.replace(anchor, replacement, 1), encoding="utf-8")

print("v425 applied: QA route for visible Quran reading progress")
