from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

marker = "\nstruct QuranProgressQAView: View {"
if marker not in text:
    raise SystemExit("v430: QuranProgressQAView marker missing")

qa_view = r'''
struct QuranAudioCacheQAView: View {
    @State private var status = "Prüfe Offline-Audio …"
    @State private var detail = ""
    @State private var passed = false

    var body: some View {
        VStack(spacing: 18) {
            Image(systemName: passed ? "checkmark.seal.fill" : "arrow.down.circle.fill")
                .font(.system(size: 64))
                .foregroundStyle(passed ? .green : SalahTheme.teal)

            Text("Quran Offline-Audio")
                .font(.title2.bold())

            Text(status)
                .font(.headline)
                .multilineTextAlignment(.center)

            Text(detail)
                .font(.footnote.monospaced())
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding(24)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(SalahTheme.page)
        .task { await runTest() }
    }

    @MainActor
    private func runTest() async {
        UserDefaults.standard.set(false, forKey: "audioCacheQAPassed")
        await QuranAudioCache.shared.clear()

        do {
            let urls = try await QuranAudioResolver.urls(surah: 1, reciter: .alafasy)
            guard let remote = urls.first else {
                throw URLError(.badServerResponse)
            }

            let firstLocal = await QuranAudioCache.shared.playbackURL(for: remote)
            let firstStats = await QuranAudioCache.shared.stats()
            let secondLocal = await QuranAudioCache.shared.playbackURL(for: remote)
            let secondStats = await QuranAudioCache.shared.stats()

            let sameFile = firstLocal == secondLocal
            let localFile = firstLocal.isFileURL
            let hasBytes = firstStats.count >= 1 && firstStats.bytes > 0
            let reusedWithoutDuplicate = secondStats.count == firstStats.count
                && secondStats.bytes == firstStats.bytes

            passed = sameFile && localFile && hasBytes && reusedWithoutDuplicate
            status = passed ? "PASS · lokal gespeichert und wiederverwendet" : "FAIL · Cache-Prüfung fehlgeschlagen"
            detail = "Dateien: \(secondStats.count) · Bytes: \(secondStats.bytes)\nLokal: \(localFile) · Gleiche Datei: \(sameFile)"
            UserDefaults.standard.set(passed, forKey: "audioCacheQAPassed")
            UserDefaults.standard.set(detail, forKey: "audioCacheQADetail")
        } catch {
            passed = false
            status = "FAIL · \(error.localizedDescription)"
            detail = error.localizedDescription
            UserDefaults.standard.set(false, forKey: "audioCacheQAPassed")
            UserDefaults.standard.set(detail, forKey: "audioCacheQADetail")
        }
    }
}
'''
text = text.replace(marker, qa_view + marker, 1)
guide.write_text(text, encoding="utf-8")

app = Path("SalahZeit/SalahZeitApp.swift")
app_text = app.read_text(encoding="utf-8")

anchor = '''        case "quran-progress":
            NavigationStack {
                QuranProgressQAView()
            }
'''
if anchor not in app_text:
    raise SystemExit("v430: quran-progress QA route anchor missing")

replacement = anchor + '''        case "audio-cache":
            NavigationStack {
                QuranAudioCacheQAView()
            }
'''
app.write_text(app_text.replace(anchor, replacement, 1), encoding="utf-8")

print("v430 applied: deterministic Quran audio-cache integration QA route")
