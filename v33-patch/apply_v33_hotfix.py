from pathlib import Path
import re

p=Path('SalahZeit/Views/GuideView.swift')
s=p.read_text(encoding='utf-8')

s=s.replace('''endObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: item, queue: .main) { [weak self] _ in
                self?.isPlaying = false
            }''','''endObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: item, queue: .main) { [weak self] _ in
                Task { @MainActor in self?.isPlaying = false }
            }''')
s=s.replace('''endObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: last, queue: .main) { [weak self] _ in
                    self?.isPlaying = false
                }''','''endObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: last, queue: .main) { [weak self] _ in
                    Task { @MainActor in self?.isPlaying = false }
                }''')

start=s.index('private struct QuranSurahView: View {')
end=s.index('private extension Collection {', start)
replacement=r'''private struct QuranSurahView: View {
    @EnvironmentObject private var settings: SettingsStore
    let surah: SurahMeta
    @StateObject private var store = QuranStore()
    @StateObject private var audio = RemoteAudioPlayer()
    @State private var arabic: SurahData?
    @State private var translation: SurahData?
    @State private var audioSurah: SurahData?
    @State private var error: String?
    @State private var bookmarkedTokens = QuranBookmarkStore.tokens()

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                headerSection
                versesSection
                sourceFooter
            }
            .padding()
        }
        .navigationTitle(surah.englishName)
        .navigationBarTitleDisplayMode(.inline)
        .task(id: "\(settings.language.rawValue)-\(settings.quranReciter.rawValue)") {
            await loadContent()
        }
        .onDisappear { audio.stop() }
    }

    private var headerSection: some View {
        VStack(spacing: 8) {
            Text(surah.name).font(.largeTitle)
            Text(surah.englishName).font(.title3.bold())
            Button(action: toggleFullSurah) {
                Label(
                    audio.isPlaying ? settings.t("Pause", "Duraklat") : settings.t("Sura anhören", "Sureyi dinle"),
                    systemImage: audio.isPlaying ? "pause.fill" : "play.fill"
                )
            }
            .buttonStyle(.borderedProminent)
            Text("\(settings.quranReciter.title) · AlQuran.cloud / Islamic Network")
                .font(.caption)
                .foregroundStyle(.secondary)
            if let audioError = audio.lastError {
                Label(audioError, systemImage: "exclamationmark.triangle.fill")
                    .font(.caption)
                    .foregroundStyle(.orange)
            }
        }
        .cardStyle(material: true)
    }

    @ViewBuilder
    private var versesSection: some View {
        if let arabic, let translation {
            let pairs = Array(zip(arabic.ayahs, translation.ayahs))
            ForEach(Array(pairs.enumerated()), id: \.offset) { index, pair in
                ayahCard(ar: pair.0, translated: pair.1, index: index)
            }
        } else if let error {
            ContentUnavailableView(
                settings.t("Inhalt nicht geladen", "İçerik yüklenemedi"),
                systemImage: "wifi.exclamationmark",
                description: Text(error)
            )
        } else {
            ProgressView().padding(.top, 40)
        }
    }

    private func ayahCard(ar: AyahData, translated: AyahData, index: Int) -> some View {
        let token = "\(surah.number):\(ar.numberInSurah)"
        return VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("\(ar.numberInSurah)")
                    .font(.caption.bold())
                    .foregroundStyle(.secondary)
                Spacer()
                Button {
                    QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)
                    playAyah(at: index)
                } label: {
                    Image(systemName: "play.circle")
                }
                .buttonStyle(.plain)

                Button {
                    let bookmark = QuranBookmark(surah: surah.number, ayah: ar.numberInSurah)
                    _ = QuranBookmarkStore.toggle(bookmark)
                    bookmarkedTokens = QuranBookmarkStore.tokens()
                } label: {
                    Image(systemName: bookmarkedTokens.contains(token) ? "bookmark.fill" : "bookmark")
                }
                .buttonStyle(.plain)
            }

            Text(ar.text)
                .font(.title2)
                .multilineTextAlignment(.trailing)
                .frame(maxWidth: .infinity, alignment: .trailing)
                .textSelection(.enabled)
            Divider()
            Text(translated.text)
                .font(.body)
                .textSelection(.enabled)
        }
        .cardStyle()
        .onAppear {
            QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)
        }
    }

    private var sourceFooter: some View {
        Text(settings.t(
            "Quran-Text/Übersetzung: AlQuran.cloud. Deutsch: Bubenheim & Elyas. Türkisch: Diyanet. Audio-URLs werden über die gewählte Audio-Edition der API geladen.",
            "Kur'an metni/meali: AlQuran.cloud. Almanca: Bubenheim & Elyas. Türkçe: Diyanet. Ses bağlantıları seçilen ses edisyonundan API üzerinden alınır."
        ))
        .font(.caption)
        .foregroundStyle(.secondary)
        .padding()
    }

    @MainActor
    private func loadContent() async {
        do {
            let result = try await store.loadSurah(surah.number, language: settings.language, reciter: settings.quranReciter)
            arabic = result.0
            translation = result.1
            audioSurah = result.2
            error = nil
        } catch {
            self.error = error.localizedDescription
        }
    }

    private func toggleFullSurah() {
        if audio.isPlaying {
            audio.stop()
            return
        }
        let urls = audioURLs
        if urls.isEmpty {
            audio.lastError = settings.t("Für diese Rezitation wurde kein Audio geliefert.", "Bu kıraat için ses bulunamadı.")
        } else {
            audio.playQueue(urls)
        }
    }

    private func playAyah(at index: Int) {
        guard let raw = audioSurah?.ayahs[safe: index].audio,
              let url = secureURL(raw) else {
            audio.lastError = settings.t("Audio für diese Ayah nicht verfügbar.", "Bu ayet için ses mevcut değil.")
            return
        }
        audio.toggle(url)
    }

    private var audioURLs: [URL] {
        (audioSurah?.ayahs ?? []).compactMap { ayah in
            guard let raw = ayah.audio else { return nil }
            return secureURL(raw)
        }
    }

    private func secureURL(_ raw: String) -> URL? {
        URL(string: raw.replacingOccurrences(of: "http://", with: "https://"))
    }
}

'''
s=s[:start]+replacement+s[end:]
p.write_text(s,encoding='utf-8')
print('v3.3 hotfix applied')