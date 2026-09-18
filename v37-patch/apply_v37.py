from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f'Expected block not found for {label}: {old[:120]!r}')
    return text.replace(old, new, 1)

# -----------------------------------------------------------------------------
# App settings: fix live Sudais identifier + richer Quran reading controls.
# -----------------------------------------------------------------------------
p = Path('SalahZeit/Models/AppSettings.swift')
s = p.read_text(encoding='utf-8')
old = '''enum QuranReciter: String, CaseIterable, Identifiable {
    case alafasy
    case husary
    case minshawi
    case sudais

    var id: String { rawValue }

    var edition: String {
        switch self {
        case .alafasy: return "ar.alafasy"
        case .husary: return "ar.husary"
        case .minshawi: return "ar.minshawi"
        case .sudais: return "ar.sudais"
        }
    }

    var bitrate: Int { self == .sudais ? 192 : 128 }

    var title: String {
        switch self {
        case .alafasy: return "Mishary Rashid Alafasy"
        case .husary: return "Mahmoud Khalil Al-Husary"
        case .minshawi: return "Mohamed Siddiq al-Minshawi"
        case .sudais: return "Abdul Rahman Al-Sudais"
        }
    }
}
'''
new = '''enum QuranReciter: String, CaseIterable, Identifiable {
    case alafasy
    case husary
    case minshawi
    case sudais
    case shuraim

    var id: String { rawValue }

    var edition: String {
        switch self {
        case .alafasy: return "ar.alafasy"
        case .husary: return "ar.husary"
        case .minshawi: return "ar.minshawi"
        // Live AlQuran.cloud audio-edition identifier. The older ar.sudais alias
        // appears in some CDN documentation but does not currently return ayah audio.
        case .sudais: return "ar.abdurrahmaansudais"
        case .shuraim: return "ar.saoodshuraym"
        }
    }

    var bitrate: Int {
        switch self {
        case .sudais: return 192
        default: return 128
        }
    }

    var title: String {
        switch self {
        case .alafasy: return "Mishary Rashid Alafasy"
        case .husary: return "Mahmoud Khalil Al-Husary"
        case .minshawi: return "Mohamed Siddiq al-Minshawi"
        case .sudais: return "Abdul Rahman Al-Sudais"
        case .shuraim: return "Saud Al-Shuraim"
        }
    }
}
'''
s = replace_once(s, old, new, 'QuranReciter')
s = s.replace('''        static let quranReciter = "quranReciter"''','''        static let quranReciter = "quranReciter"
        static let quranFontSize = "quranFontSize"
        static let quranShowTranslation = "quranShowTranslation"
        static let quranShowTransliteration = "quranShowTransliteration"''',1)
s = s.replace('''    @Published var quranReciter: QuranReciter { didSet { defaults.set(quranReciter.rawValue, forKey: Keys.quranReciter) } }''','''    @Published var quranReciter: QuranReciter { didSet { defaults.set(quranReciter.rawValue, forKey: Keys.quranReciter) } }
    @Published var quranFontSize: Double { didSet { defaults.set(quranFontSize, forKey: Keys.quranFontSize) } }
    @Published var quranShowTranslation: Bool { didSet { defaults.set(quranShowTranslation, forKey: Keys.quranShowTranslation) } }
    @Published var quranShowTransliteration: Bool { didSet { defaults.set(quranShowTransliteration, forKey: Keys.quranShowTransliteration) } }''',1)
s = s.replace('''        self.quranReciter = QuranReciter(rawValue: defaults.string(forKey: Keys.quranReciter) ?? "") ?? .alafasy''','''        self.quranReciter = QuranReciter(rawValue: defaults.string(forKey: Keys.quranReciter) ?? "") ?? .alafasy
        self.quranFontSize = defaults.object(forKey: Keys.quranFontSize) as? Double ?? 28
        self.quranShowTranslation = defaults.object(forKey: Keys.quranShowTranslation) as? Bool ?? true
        self.quranShowTransliteration = defaults.object(forKey: Keys.quranShowTransliteration) as? Bool ?? false''',1)
p.write_text(s, encoding='utf-8')

# -----------------------------------------------------------------------------
# Settings: expose Quran reader controls and clarify source.
# -----------------------------------------------------------------------------
p = Path('SalahZeit/Views/SettingsView.swift')
s = p.read_text(encoding='utf-8')
old = '''            Section(settings.t("Quran & Audio", "Kur'an ve Ses")) {
                Picker(settings.t("Rezitation", "Kâri"), selection: $settings.quranReciter) {
                    ForEach(QuranReciter.allCases) { reciter in
                        Text(reciter.title).tag(reciter)
                    }
                }
                Text(settings.t(
                    "Die Quran-Rezitation ist eine menschliche Aufnahme. Die Audio-URLs werden über die AlQuran.cloud/Islamic-Network-API aufgelöst.",
                    "Kur'an tilaveti gerçek insan kaydıdır. Ses bağlantıları AlQuran.cloud/Islamic Network API üzerinden çözülür."
                ))
                .font(.caption)
                .foregroundStyle(.secondary)
            }
'''
new = '''            Section(settings.t("Quran & Audio", "Kur'an ve Ses")) {
                Picker(settings.t("Rezitation", "Kâri"), selection: $settings.quranReciter) {
                    ForEach(QuranReciter.allCases) { reciter in
                        Text(reciter.title).tag(reciter)
                    }
                }
                Stepper(value: $settings.quranFontSize, in: 20...40, step: 2) {
                    LabeledContent(settings.t("Arabische Schriftgröße", "Arapça yazı boyutu"), value: "\(Int(settings.quranFontSize))")
                }
                Toggle(settings.t("Übersetzung anzeigen", "Meali göster"), isOn: $settings.quranShowTranslation)
                Toggle(settings.t("Transliteration anzeigen", "Latin harfli okunuşu göster"), isOn: $settings.quranShowTransliteration)
                Text(settings.t(
                    "Die Quran-Rezitation ist eine menschliche Aufnahme. Audio wird über die aktuell dokumentierten AlQuran.cloud/Islamic-Network-Audioeditionen geladen. Bei einem Netz- oder Anbieterfehler zeigt SalahPath keinen falschen Erfolg an.",
                    "Kur'an tilaveti gerçek insan kaydıdır. Ses, güncel AlQuran.cloud/Islamic Network ses edisyonları üzerinden yüklenir. Ağ veya sağlayıcı hatasında SalahPath sahte bir başarı göstermez."
                ))
                .font(.caption)
                .foregroundStyle(.secondary)
            }
'''
s = replace_once(s, old, new, 'Settings Quran section')
s = s.replace('LabeledContent(settings.t("Version", "Sürüm"), value: "3.6")','LabeledContent(settings.t("Version", "Sürüm"), value: "3.7")')
p.write_text(s, encoding='utf-8')

# -----------------------------------------------------------------------------
# Quran: independent text/audio loading, reader controls, continue, favorites,
# share, optional transliteration and honest audio states.
# -----------------------------------------------------------------------------
p = Path('SalahZeit/Views/GuideView.swift')
s = p.read_text(encoding='utf-8')

old_store = '''    func loadSurah(_ number:Int, language:AppLanguage, reciter:QuranReciter) async throws -> (SurahData,SurahData,SurahData) {
        let translation = language == .german ? "de.bubenheim" : "tr.diyanet"
        async let arabic = fetch(number:number, edition:"quran-uthmani")
        async let translated = fetch(number:number, edition:translation)
        async let audio = fetch(number:number, edition:reciter.edition)
        return try await (arabic,translated,audio)
    }
'''
new_store = '''    func loadSurah(_ number:Int, language:AppLanguage) async throws -> (SurahData,SurahData,SurahData) {
        let translationEdition = language == .german ? "de.bubenheim" : "tr.diyanet"
        async let arabic = fetch(number:number, edition:"quran-uthmani")
        async let translated = fetch(number:number, edition:translationEdition)
        async let transliterated = fetch(number:number, edition:"en.transliteration")
        return try await (arabic, translated, transliterated)
    }
'''
s = replace_once(s, old_store, new_store, 'QuranStore loadSurah')

start = s.index('struct QuranView: View {')
end = s.index('\nprivate extension Collection {', start)
new_quran = r'''struct QuranView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()
    @State private var search = ""
    @State private var lastRead = UserDefaults.standard.string(forKey: QuranBookmarkStore.lastReadKey)

    var body: some View {
        Group {
            if store.isLoading && store.chapters.isEmpty {
                ProgressView(settings.t("Quran wird geladen…", "Kur'an yükleniyor…"))
            } else if let error = store.error, store.chapters.isEmpty {
                ContentUnavailableView(
                    settings.t("Quran konnte nicht geladen werden", "Kur'an yüklenemedi"),
                    systemImage: "wifi.exclamationmark",
                    description: Text(error)
                )
            } else {
                List {
                    if let continueTarget {
                        Section(settings.t("Fortsetzen", "Devam et")) {
                            NavigationLink {
                                QuranSurahView(surah: continueTarget.surah, initialAyah: continueTarget.ayah)
                            } label: {
                                Label(
                                    "\(continueTarget.surah.englishName) · \(settings.t("Ayah", "Ayet")) \(continueTarget.ayah)",
                                    systemImage: "book.pages.fill"
                                )
                            }
                        }
                    }

                    Section(settings.t("Gespeichert", "Kaydedilenler")) {
                        NavigationLink {
                            QuranFavoritesView(chapters: store.chapters)
                        } label: {
                            HStack {
                                Label(settings.t("Favoriten & Lesezeichen", "Favoriler ve işaretler"), systemImage: "heart.fill")
                                Spacer()
                                Text("\(QuranBookmarkStore.tokens().count)").foregroundStyle(.secondary)
                            }
                        }
                    }

                    Section(settings.t("114 Suren", "114 sûre")) {
                        ForEach(filtered) { surah in
                            NavigationLink {
                                QuranSurahView(surah: surah, initialAyah: nil)
                            } label: {
                                HStack(spacing: 12) {
                                    Text("\(surah.number)")
                                        .font(.caption.bold())
                                        .frame(width: 34, height: 34)
                                        .background(SalahTheme.gold.opacity(0.16), in: Circle())
                                    VStack(alignment: .leading, spacing: 3) {
                                        Text(surah.englishName).font(.headline)
                                        Text("\(surah.numberOfAyahs) \(settings.t("Verse", "ayet"))")
                                            .font(.caption).foregroundStyle(.secondary)
                                    }
                                    Spacer()
                                    Text(surah.name).font(.title3)
                                }
                                .padding(.vertical, 3)
                            }
                        }
                    }
                }
                .searchable(text: $search, prompt: settings.t("Sura suchen", "Sure ara"))
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Quran", "Kur'an"))
        .task { await store.loadChapters() }
        .onAppear { lastRead = UserDefaults.standard.string(forKey: QuranBookmarkStore.lastReadKey) }
    }

    private var filtered: [SurahMeta] {
        guard !search.isEmpty else { return store.chapters }
        return store.chapters.filter {
            $0.englishName.localizedCaseInsensitiveContains(search) ||
            $0.englishNameTranslation.localizedCaseInsensitiveContains(search) ||
            $0.name.contains(search) ||
            String($0.number) == search
        }
    }

    private var continueTarget: (surah: SurahMeta, ayah: Int)? {
        guard let lastRead else { return nil }
        let parts = lastRead.split(separator: ":")
        guard parts.count == 2,
              let surahNumber = Int(parts[0]),
              let ayah = Int(parts[1]),
              let surah = store.chapters.first(where: { $0.number == surahNumber }) else { return nil }
        return (surah, ayah)
    }
}

private struct QuranFavoritesView: View {
    @EnvironmentObject private var settings: SettingsStore
    let chapters: [SurahMeta]
    @State private var refresh = 0

    var body: some View {
        List {
            if favorites.isEmpty {
                ContentUnavailableView(
                    settings.t("Noch keine Favoriten", "Henüz favori yok"),
                    systemImage: "bookmark",
                    description: Text(settings.t("Tippe bei einer Ayah auf das Lesezeichen.", "Bir ayette yer imi simgesine dokun."))
                )
            } else {
                ForEach(favorites, id: \.token) { favorite in
                    if let surah = chapters.first(where: { $0.number == favorite.surah }) {
                        NavigationLink {
                            QuranSurahView(surah: surah, initialAyah: favorite.ayah)
                        } label: {
                            VStack(alignment: .leading, spacing: 3) {
                                Text(surah.englishName).font(.headline)
                                Text("\(settings.t("Ayah", "Ayet")) \(favorite.ayah)")
                                    .font(.caption).foregroundStyle(.secondary)
                            }
                        }
                        .swipeActions {
                            Button(role: .destructive) {
                                _ = QuranBookmarkStore.toggle(QuranBookmark(surah: favorite.surah, ayah: favorite.ayah))
                                refresh += 1
                            } label: { Label(settings.t("Entfernen", "Kaldır"), systemImage: "trash") }
                        }
                    }
                }
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Favoriten", "Favoriler"))
    }

    private var favorites: [(token: String, surah: Int, ayah: Int)] {
        QuranBookmarkStore.tokens().compactMap { token in
            let parts = token.split(separator: ":")
            guard parts.count == 2, let surah = Int(parts[0]), let ayah = Int(parts[1]) else { return nil }
            return (token, surah, ayah)
        }.sorted { lhs, rhs in lhs.surah == rhs.surah ? lhs.ayah < rhs.ayah : lhs.surah < rhs.surah }
    }
}

private struct QuranSurahView: View {
    @EnvironmentObject private var settings: SettingsStore
    let surah: SurahMeta
    let initialAyah: Int?

    @StateObject private var store = QuranStore()
    @StateObject private var audio = RemoteAudioPlayer()
    @State private var arabic: SurahData?
    @State private var translation: SurahData?
    @State private var transliteration: SurahData?
    @State private var resolvedAudioURLs: [URL] = []
    @State private var isResolvingAudio = false
    @State private var error: String?
    @State private var bookmarkedTokens = QuranBookmarkStore.tokens()
    @State private var hasScrolledToInitial = false

    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(spacing: 14) {
                    headerSection
                    versesSection
                    sourceFooter
                }
                .padding()
            }
            .background(SalahTheme.page)
            .navigationTitle(surah.englishName)
            .navigationBarTitleDisplayMode(.inline)
            .task(id: "\(settings.language.rawValue)-\(settings.quranReciter.rawValue)") {
                await loadContent()
                scrollToInitialIfNeeded(proxy)
            }
            .onChange(of: arabic?.ayahs.count ?? 0) { _, _ in scrollToInitialIfNeeded(proxy) }
            .onDisappear { audio.stop() }
        }
    }

    private var headerSection: some View {
        VStack(spacing: 12) {
            Text(surah.name).font(.largeTitle)
            Text(surah.englishName).font(.title3.bold())

            HStack(spacing: 18) {
                Button { audio.previous() } label: { Image(systemName: "backward.fill") }
                    .disabled(!audio.hasPrevious)

                Button(action: toggleFullSurah) {
                    ZStack {
                        Circle().fill(audioReady ? SalahTheme.teal : Color.secondary.opacity(0.35)).frame(width: 54, height: 54)
                        if isResolvingAudio || audio.isLoading {
                            ProgressView().tint(.white)
                        } else {
                            Image(systemName: audio.isPlaying ? "pause.fill" : (audioReady ? "play.fill" : "speaker.slash.fill"))
                                .foregroundStyle(.white).font(.title3)
                        }
                    }
                }
                .buttonStyle(.plain)
                .disabled(!audioReady || isResolvingAudio)
                .accessibilityLabel(audioReady ? settings.t("Sura abspielen", "Sureyi oynat") : settings.t("Audio nicht verfügbar", "Ses mevcut değil"))

                Button { audio.next() } label: { Image(systemName: "forward.fill") }
                    .disabled(!audio.hasNext)
            }
            .font(.title3)
            .foregroundStyle(SalahTheme.teal)

            if audio.queueCount > 1 {
                Text("\(settings.t("Ayah", "Ayet")) \(audio.queueIndex + 1)/\(audio.queueCount)")
                    .font(.caption.bold()).monospacedDigit()
            }

            HStack(spacing: 8) {
                Image(systemName: "person.wave.2.fill")
                Text(settings.quranReciter.title)
            }
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
        if let arabic, let translation, let transliteration {
            let translated = translation.ayahs
            let latin = transliteration.ayahs
            ForEach(Array(arabic.ayahs.enumerated()), id: \.element.number) { index, ar in
                if let tr = translated[safe: index], let latinAyah = latin[safe: index] {
                    ayahCard(ar: ar, translated: tr, transliterated: latinAyah, index: index)
                        .id(ar.numberInSurah)
                }
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

    private func ayahCard(ar: AyahData, translated: AyahData, transliterated: AyahData, index: Int) -> some View {
        let token = "\(surah.number):\(ar.numberInSurah)"
        let audioURL = resolvedAudioURLs[safe: index]
        let shareText = shareTextFor(ar: ar, translated: translated)

        return VStack(alignment: .leading, spacing: 12) {
            HStack(spacing: 14) {
                Text("\(ar.numberInSurah)")
                    .font(.caption.bold())
                    .frame(minWidth: 28, minHeight: 28)
                    .background(SalahTheme.gold.opacity(0.16), in: Circle())
                Spacer()

                if let audioURL {
                    Button {
                        QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)
                        audio.toggle(audioURL)
                    } label: {
                        Image(systemName: audio.activeURL == audioURL && audio.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(settings.t("Ayah anhören", "Ayeti dinle"))
                } else {
                    Image(systemName: "speaker.slash")
                        .foregroundStyle(.secondary)
                        .accessibilityLabel(settings.t("Audio nicht verfügbar", "Ses mevcut değil"))
                }

                ShareLink(item: shareText) {
                    Image(systemName: "square.and.arrow.up")
                }
                .buttonStyle(.plain)
                .accessibilityLabel(settings.t("Ayah teilen", "Ayeti paylaş"))

                Button {
                    let bookmark = QuranBookmark(surah: surah.number, ayah: ar.numberInSurah)
                    _ = QuranBookmarkStore.toggle(bookmark)
                    bookmarkedTokens = QuranBookmarkStore.tokens()
                } label: {
                    Image(systemName: bookmarkedTokens.contains(token) ? "bookmark.fill" : "bookmark")
                }
                .buttonStyle(.plain)
                .accessibilityLabel(settings.t("Lesezeichen", "Yer imi"))
            }
            .foregroundStyle(SalahTheme.teal)

            Text(ar.text)
                .font(.system(size: settings.quranFontSize, weight: .regular))
                .multilineTextAlignment(.trailing)
                .frame(maxWidth: .infinity, alignment: .trailing)
                .textSelection(.enabled)
                .accessibilityLabel(ar.text)

            if settings.quranShowTransliteration {
                Divider()
                Text(transliterated.text)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .textSelection(.enabled)
            }

            if settings.quranShowTranslation {
                Divider()
                Text(translated.text)
                    .font(.body)
                    .textSelection(.enabled)
            }
        }
        .cardStyle()
        .overlay {
            if audio.queueCount == resolvedAudioURLs.count,
               audio.queueCount > 1,
               audio.queueIndex == index,
               audio.isPlaying {
                RoundedRectangle(cornerRadius: 20).stroke(SalahTheme.gold, lineWidth: 2)
            }
        }
        .onAppear { QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah) }
    }

    private var sourceFooter: some View {
        Text(settings.t(
            "Quran: Uthmani-Text über AlQuran.cloud. Deutsch: Bubenheim & Elyas. Türkisch: Diyanet. Transliteration: AlQuran.cloud. Rezitation: menschliche Audioedition des Islamic Network. Quran-Text wird nicht von SalahPath umgeschrieben.",
            "Kur'an: AlQuran.cloud Uthmani metni. Almanca: Bubenheim & Elyas. Türkçe: Diyanet. Latin harfli okunuş: AlQuran.cloud. Tilavet: Islamic Network insan ses kaydı. Kur'an metni SalahPath tarafından yeniden yazılmaz."
        ))
        .font(.caption)
        .foregroundStyle(.secondary)
        .padding()
    }

    @MainActor
    private func loadContent() async {
        error = nil
        do {
            let result = try await store.loadSurah(surah.number, language: settings.language)
            arabic = result.0
            translation = result.1
            transliteration = result.2
        } catch {
            self.error = error.localizedDescription
            return
        }

        isResolvingAudio = true
        defer { isResolvingAudio = false }
        do {
            resolvedAudioURLs = try await QuranAudioResolver.urls(surah: surah.number, reciter: settings.quranReciter)
            if resolvedAudioURLs.isEmpty {
                audio.lastError = settings.t("Audio derzeit nicht verfügbar.", "Ses şu anda mevcut değil.")
            } else {
                audio.lastError = nil
            }
        } catch {
            resolvedAudioURLs = []
            audio.lastError = settings.t("Audio derzeit nicht verfügbar. Bitte Verbindung oder Rezitator prüfen.", "Ses şu anda mevcut değil. Bağlantıyı veya kâriyi kontrol et.")
        }
    }

    private var audioReady: Bool { !resolvedAudioURLs.isEmpty }

    private func toggleFullSurah() {
        guard audioReady else {
            audio.lastError = settings.t("Audio derzeit nicht verfügbar.", "Ses şu anda mevcut değil.")
            return
        }
        if audio.isPlaying { audio.stop() }
        else { audio.playQueue(resolvedAudioURLs) }
    }

    private func shareTextFor(ar: AyahData, translated: AyahData) -> String {
        var parts = [ar.text]
        if settings.quranShowTranslation { parts.append(translated.text) }
        parts.append("Quran \(surah.number):\(ar.numberInSurah)")
        return parts.joined(separator: "\n\n")
    }

    private func scrollToInitialIfNeeded(_ proxy: ScrollViewProxy) {
        guard !hasScrolledToInitial, let initialAyah else { return }
        guard arabic?.ayahs.contains(where: { $0.numberInSurah == initialAyah }) == true else { return }
        hasScrolledToInitial = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
            withAnimation { proxy.scrollTo(initialAyah, anchor: .top) }
        }
    }
}
'''
s = s[:start] + new_quran + s[end:]
p.write_text(s, encoding='utf-8')

# -----------------------------------------------------------------------------
# Home: dedicated prayer-times screen instead of accidentally opening Rak'ah.
# -----------------------------------------------------------------------------
p = Path('SalahZeit/Views/HomeView.swift')
s = p.read_text(encoding='utf-8')
s = s.replace('NavigationLink { RakatOverviewView() } label: { DashboardTile(title: settings.t("Gebetszeiten", "Namaz vakitleri"), subtitle: settings.t("Fard · Sunnah · Witr", "Farz · sünnet · vitir"), icon: "clock.fill") }',
              'NavigationLink { PrayerTimesOverviewView() } label: { DashboardTile(title: settings.t("Gebetszeiten", "Namaz vakitleri"), subtitle: settings.t("Heute · Woche · Monat", "Bugün · hafta · ay"), icon: "clock.fill") }',1)
s = s.replace('NavigationLink { QuranView() } label: { DashboardTile(title: settings.t("Favoriten", "Favoriler"), subtitle: settings.t("Quran-Lesezeichen", "Kur\'an işaretleri"), icon: "heart.fill") }',
              'NavigationLink { QuranView() } label: { DashboardTile(title: settings.t("Favoriten", "Favoriler"), subtitle: settings.t("Quran-Lesezeichen", "Kur\'an işaretleri"), icon: "heart.fill") }',1)

insert_point = s.index('\nprivate struct DashboardTile: View')
prayer_times_view = r'''

struct PrayerTimesOverviewView: View {
    @EnvironmentObject private var locationManager: LocationManager
    @EnvironmentObject private var settings: SettingsStore
    @State private var period = 0
    private let engine = PrayerEngine()

    var body: some View {
        ScrollView {
            VStack(spacing: 14) {
                Picker(settings.t("Zeitraum", "Dönem"), selection: $period) {
                    Text(settings.t("Heute", "Bugün")).tag(0)
                    Text(settings.t("7 Tage", "7 gün")).tag(1)
                    Text(settings.t("30 Tage", "30 gün")).tag(2)
                }
                .pickerStyle(.segmented)

                if let location = locationManager.location {
                    ForEach(days, id: \.self) { date in
                        if let day = engine.calculateDay(for: date, location: location, settings: settings) {
                            VStack(alignment: .leading, spacing: 10) {
                                HStack {
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(shortDate(date)).font(.headline)
                                        Text(hijriDateString(date, language: settings.language))
                                            .font(.caption).foregroundStyle(.secondary)
                                    }
                                    Spacer()
                                    if Calendar.current.isDateInToday(date) {
                                        Text(settings.t("HEUTE", "BUGÜN"))
                                            .font(.caption2.bold())
                                            .foregroundStyle(SalahTheme.teal)
                                    }
                                }
                                ForEach(day.prayers) { prayer in
                                    HStack {
                                        Label(prayer.kind.localizedName(settings.language), systemImage: prayer.kind.systemImage)
                                        Spacer()
                                        Text(timeString(prayer.date, use24Hour: settings.use24Hour))
                                            .font(.body.monospacedDigit().weight(.semibold))
                                    }
                                    .font(.subheadline)
                                    if prayer.kind != day.prayers.last?.kind { Divider().opacity(0.5) }
                                }
                            }
                            .salahCard()
                        }
                    }
                } else {
                    ContentUnavailableView(
                        settings.t("Standort benötigt", "Konum gerekli"),
                        systemImage: "location.slash",
                        description: Text(settings.t("Für Gebetszeiten wird dein aktueller Standort benötigt.", "Namaz vakitleri için mevcut konumun gerekir."))
                    )
                }
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetszeiten", "Namaz vakitleri"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear { locationManager.requestAccessAndStart() }
    }

    private var days: [Date] {
        let count = period == 0 ? 1 : (period == 1 ? 7 : 30)
        let start = Calendar.current.startOfDay(for: Date())
        return (0..<count).compactMap { Calendar.current.date(byAdding: .day, value: $0, to: start) }
    }

    private func shortDate(_ date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        f.dateFormat = "EEE, d. MMM"
        return f.string(from: date)
    }
}
'''
s = s[:insert_point] + prayer_times_view + s[insert_point:]
p.write_text(s, encoding='utf-8')

# -----------------------------------------------------------------------------
# Version/build.
# -----------------------------------------------------------------------------
p = Path('scripts/build_unsigned_ipa.sh')
s = p.read_text(encoding='utf-8')
s = s.replace('MARKETING_VERSION="3.6"', 'MARKETING_VERSION="3.7"')
s = s.replace('CURRENT_PROJECT_VERSION="11"', 'CURRENT_PROJECT_VERSION="12"')
p.write_text(s, encoding='utf-8')

print('SalahPath v3.7 patch applied')