from pathlib import Path

# SalahPath v3.59 FAST — functional wiring audit fixes.
# Turn visible affordances into real actions without changing the approved
# poster proportions unless interaction requires it.

guide = Path("SalahZeit/Views/GuideView.swift")
s = guide.read_text(encoding="utf-8")

# --- Namaz: Deutsch pill must be tappable.
old = '''                Text("Deutsch")
                    .font(.system(size: 10.4, weight: .bold))
                    .foregroundStyle(SalahTheme.deepTeal)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 6)
                    .background(
                        SalahTheme.gold.opacity(settings.language == .german ? 0.24 : 0.12),
                        in: RoundedRectangle(cornerRadius: 8, style: .continuous)
                    )
'''
new = '''                Button {
                    settings.language = .german
                } label: {
                    Text("Deutsch")
                        .font(.system(size: 10.4, weight: .bold))
                        .foregroundStyle(SalahTheme.deepTeal)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 6)
                        .background(
                            SalahTheme.gold.opacity(settings.language == .german ? 0.24 : 0.12),
                            in: RoundedRectangle(cornerRadius: 8, style: .continuous)
                        )
                }
                .buttonStyle(.plain)
'''
if old not in s:
    raise SystemExit("v3.59: Deutsch pill anchor missing")
s = s.replace(old, new, 1)

# --- Namaz: hero arrow must open the actual step-by-step guide.
old = '''                Button {
                    settings.prayerAudience = settings.prayerAudience == .male ? .female : .male
                } label: {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: 32, height: 32)
                        Image(systemName: "chevron.right")
                            .font(.system(size: 12, weight: .black))
                            .foregroundStyle(.white)
                    }
                }
                .buttonStyle(.plain)
                .padding(.trailing, 4)
'''
new = '''                NavigationLink {
                    PrayerHowToView()
                } label: {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: 32, height: 32)
                        Image(systemName: "chevron.right")
                            .font(.system(size: 12, weight: .black))
                            .foregroundStyle(.white)
                    }
                }
                .buttonStyle(.plain)
                .padding(.trailing, 4)
'''
if old not in s:
    raise SystemExit("v3.59: Namaz hero arrow anchor missing")
s = s.replace(old, new, 1)

# --- Dhikr: tabs must visibly change the displayed dhikr, not only tint the pill.
old = '''    @State private var counter = 33
    @State private var section = 0

    private var tabs: [String] { ["Sabah", "Akşam", "Günlük", "Özel"] }
'''
new = '''    @State private var counter = 33
    @State private var section = 0

    private var tabs: [String] { ["Sabah", "Akşam", "Günlük", "Özel"] }

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
if old not in s:
    raise SystemExit("v3.59: Dhikr tab state anchor missing")
s = s.replace(old, new, 1)

old = '''                            withAnimation(.easeOut(duration: 0.15)) {
                                section = index
                            }
'''
new = '''                            withAnimation(.easeOut(duration: 0.15)) {
                                section = index
                                counter = 33
                            }
'''
if old not in s:
    raise SystemExit("v3.59: Dhikr tab action anchor missing")
s = s.replace(old, new, 1)

for old, new in [
    ('Text("أَسْتَغْفِرُ اللّٰهَ")', 'Text(activeDhikr.arabic)'),
    ('Text("Estağfirullâh")', 'Text(activeDhikr.latin)'),
    ('Text("Ich bitte Allah um Vergebung.")', 'Text(activeDhikr.german)'),
]:
    if old not in s:
        raise SystemExit("v3.59: Dhikr visible content anchor missing")
    s = s.replace(old, new, 1)

# --- Dhikr: rows with chevrons must actually navigate.
repls = [
('''                    dhikrStaticRow(
                        icon: "circle.grid.cross.fill",
                        title: "Tesbih Sayacı",
                        subtitle: settings.t("Tasbih-Zähler", "Tesbih sayacı")
                    )
''',
'''                    dhikrReferenceRow(
                        icon: "circle.grid.cross.fill",
                        title: "Tesbih Sayacı",
                        subtitle: settings.t("Tasbih-Zähler", "Tesbih sayacı")
                    ) {
                        TasbihCounterView()
                    }
'''),
('''                    dhikrStaticRow(
                        icon: "character.book.closed.fill",
                        title: "Arapça, Türkçe, Deutsch",
                        subtitle: settings.t("Dreisprachige Begleitung", "Üç dilde kullanım")
                    )
''',
'''                    dhikrReferenceRow(
                        icon: "character.book.closed.fill",
                        title: "Arapça, Türkçe, Deutsch",
                        subtitle: settings.t("Dreisprachige Begleitung", "Üç dilde kullanım")
                    ) {
                        SettingsView()
                    }
'''),
('''                    dhikrStaticRow(
                        icon: "speaker.wave.2.fill",
                        title: "Sesli dinleme",
                        subtitle: settings.t("Mit Audio anhören", "Sesli dinleme")
                    )
''',
'''                    dhikrReferenceRow(
                        icon: "speaker.wave.2.fill",
                        title: "Sesli dinleme",
                        subtitle: settings.t("Mit Audio anhören", "Sesli dinleme")
                    ) {
                        PrayerDuaAudioView()
                    }
''')
]
for old, new in repls:
    if old not in s:
        raise SystemExit("v3.59: Dhikr static row anchor missing")
    s = s.replace(old, new, 1)

# --- Quran: state required by functional preview player.
old = '''    @StateObject private var store = QuranStore()
    @State private var languageTab = 0
    @State private var search = ""
'''
new = '''    @StateObject private var store = QuranStore()
    @StateObject private var previewAudio = RemoteAudioPlayer()
    @State private var languageTab = 0
    @State private var search = ""
    @State private var previewAudioURLs: [URL] = []
    @State private var isResolvingPreviewAudio = false
'''
if old not in s:
    raise SystemExit("v3.59: Quran state anchor missing")
s = s.replace(old, new, 1)

# Functionalize the top player controls inside the v3.57 combined card.
old = '''                                HStack(spacing: 24) {
                                    Image(systemName: "backward.end.fill")
                                        .font(.system(size: 17, weight: .semibold))

                                    ZStack {
                                        Circle()
                                            .fill(SalahTheme.deepTeal)
                                            .frame(width: 54, height: 54)
                                        Image(systemName: "play.fill")
                                            .font(.system(size: 18, weight: .semibold))
                                            .foregroundStyle(.white)
                                    }

                                    Image(systemName: "forward.end.fill")
                                        .font(.system(size: 17, weight: .semibold))

                                    Spacer()

                                    Text("1.0x")
                                        .font(.system(size: 11.5, weight: .bold))
                                        .padding(.horizontal, 9)
                                        .padding(.vertical, 6)
                                        .background(SalahTheme.softTeal, in: Capsule())
                                }
                                .foregroundStyle(SalahTheme.teal)
'''
new = '''                                HStack(spacing: 24) {
                                    Button { previewAudio.previous() } label: {
                                        Image(systemName: "backward.end.fill")
                                            .font(.system(size: 17, weight: .semibold))
                                    }
                                    .buttonStyle(.plain)
                                    .disabled(!previewAudio.hasPrevious)

                                    Button {
                                        Task { await togglePreviewAudio() }
                                    } label: {
                                        ZStack {
                                            Circle()
                                                .fill(SalahTheme.deepTeal)
                                                .frame(width: 54, height: 54)
                                            if isResolvingPreviewAudio || previewAudio.isLoading {
                                                ProgressView()
                                                    .tint(.white)
                                            } else {
                                                Image(systemName: previewAudio.isPlaying ? "pause.fill" : "play.fill")
                                                    .font(.system(size: 18, weight: .semibold))
                                                    .foregroundStyle(.white)
                                            }
                                        }
                                    }
                                    .buttonStyle(.plain)

                                    Button { previewAudio.next() } label: {
                                        Image(systemName: "forward.end.fill")
                                            .font(.system(size: 17, weight: .semibold))
                                    }
                                    .buttonStyle(.plain)
                                    .disabled(!previewAudio.hasNext)

                                    Spacer()

                                    Text("1.0x")
                                        .font(.system(size: 11.5, weight: .bold))
                                        .padding(.horizontal, 9)
                                        .padding(.vertical, 6)
                                        .background(SalahTheme.softTeal, in: Capsule())
                                }
                                .foregroundStyle(SalahTheme.teal)
'''
if old not in s:
    raise SystemExit("v3.59: Quran player anchor missing")
s = s.replace(old, new, 1)

old = '''                            HStack(spacing: 0) {
                                quranAction(icon: "square.and.pencil", title: settings.t("Verse", "Ayetler"))
                                quranAction(icon: "play.circle", title: settings.t("Hören", "Dinle"))
                                NavigationLink {
                                    QuranFavoritesView(chapters: store.chapters)
                                } label: {
                                    quranAction(icon: "heart", title: settings.t("Favorit", "Favori"))
                                }
                                .buttonStyle(.plain)
                                quranAction(icon: "star", title: settings.t("Teilen", "Paylaş"))
                            }
'''
new = '''                            HStack(spacing: 0) {
                                if let first = store.chapters.first {
                                    NavigationLink {
                                        QuranSurahView(surah: first, initialAyah: 1)
                                    } label: {
                                        quranAction(icon: "square.and.pencil", title: settings.t("Verse", "Ayetler"))
                                    }
                                    .buttonStyle(.plain)
                                } else {
                                    quranAction(icon: "square.and.pencil", title: settings.t("Verse", "Ayetler"))
                                }

                                Button {
                                    Task { await togglePreviewAudio() }
                                } label: {
                                    quranAction(
                                        icon: previewAudio.isPlaying ? "pause.circle" : "play.circle",
                                        title: settings.t("Hören", "Dinle")
                                    )
                                }
                                .buttonStyle(.plain)

                                NavigationLink {
                                    QuranFavoritesView(chapters: store.chapters)
                                } label: {
                                    quranAction(icon: "heart", title: settings.t("Favorit", "Favori"))
                                }
                                .buttonStyle(.plain)

                                ShareLink(item: quranShareText) {
                                    quranAction(icon: "square.and.arrow.up", title: settings.t("Teilen", "Paylaş"))
                                }
                                .buttonStyle(.plain)
                            }
'''
if old not in s:
    raise SystemExit("v3.59: Quran action strip anchor missing")
s = s.replace(old, new, 1)

# Stop preview audio when leaving and add helpers before filtered.
old = '''        .task { await store.loadChapters() }
        .tint(SalahTheme.teal)
    }

    private func quranAction(icon: String, title: String) -> some View {
'''
new = '''        .task { await store.loadChapters() }
        .onDisappear { previewAudio.stop() }
        .tint(SalahTheme.teal)
    }

    private var quranShareText: String {
        "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ\nBismillâhirrahmânirrahîm"
    }

    @MainActor
    private func togglePreviewAudio() async {
        if previewAudio.isPlaying {
            previewAudio.stop()
            return
        }

        if !previewAudioURLs.isEmpty {
            previewAudio.playQueue(previewAudioURLs)
            return
        }

        isResolvingPreviewAudio = true
        defer { isResolvingPreviewAudio = false }
        do {
            let urls = try await QuranAudioResolver.urls(surah: 1, reciter: settings.quranReciter)
            previewAudioURLs = urls
            previewAudio.playQueue(urls)
        } catch {
            previewAudio.lastError = settings.t(
                "Audio konnte nicht geladen werden. Erneut versuchen.",
                "Ses yüklenemedi. Tekrar dene."
            )
        }
    }

    private func quranAction(icon: String, title: String) -> some View {
'''
if old not in s:
    raise SystemExit("v3.59: Quran helper insertion anchor missing")
s = s.replace(old, new, 1)

# Add a standalone favorites landing view usable from Home.
marker = "\nprivate struct QuranFavoritesView: View {"
if marker not in s:
    raise SystemExit("v3.59: QuranFavoritesView marker missing")
wrapper = '''
struct QuranFavoritesLandingView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()

    var body: some View {
        Group {
            if store.isLoading && store.chapters.isEmpty {
                ProgressView(settings.t("Quran wird geladen…", "Kur'an yükleniyor…"))
            } else if let error = store.error, store.chapters.isEmpty {
                ContentUnavailableView(
                    settings.t("Favoriten konnten nicht geladen werden", "Favoriler yüklenemedi"),
                    systemImage: "wifi.exclamationmark",
                    description: Text(error)
                )
            } else {
                QuranFavoritesView(chapters: store.chapters)
            }
        }
        .task { await store.loadChapters() }
    }
}

'''
s = s.replace(marker, "\n" + wrapper + "private struct QuranFavoritesView: View {", 1)

# Add a real tasbih counter destination.
marker = "\nprivate struct DhikrTextCard: View {"
if marker not in s:
    raise SystemExit("v3.59: DhikrTextCard marker missing")
tasbih = '''
struct TasbihCounterView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var count = 0

    var body: some View {
        VStack(spacing: 24) {
            Spacer()
            Text(settings.t("Tasbih-Zähler", "Tesbih Sayacı"))
                .font(.title2.bold())
                .foregroundStyle(SalahTheme.ink)

            Text("\\(count)")
                .font(.system(size: 72, weight: .bold, design: .rounded).monospacedDigit())
                .foregroundStyle(SalahTheme.deepTeal)

            HStack(spacing: 28) {
                Button {
                    if count > 0 { count -= 1 }
                } label: {
                    Image(systemName: "minus")
                        .font(.title2.bold())
                        .frame(width: 58, height: 58)
                        .background(SalahTheme.softTeal, in: Circle())
                }

                Button {
                    count += 1
                } label: {
                    Image(systemName: "plus")
                        .font(.title2.bold())
                        .frame(width: 58, height: 58)
                        .background(SalahTheme.teal, in: Circle())
                        .foregroundStyle(.white)
                }
            }
            .buttonStyle(.plain)

            Button(settings.t("Zurücksetzen", "Sıfırla")) {
                count = 0
            }
            .buttonStyle(.bordered)

            Spacer()
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Tasbih-Zähler", "Tesbih Sayacı"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }
}

'''
s = s.replace(marker, "\n" + tasbih + "private struct DhikrTextCard: View {", 1)

guide.write_text(s, encoding="utf-8")

# --- Home wiring.
home = Path("SalahZeit/Views/HomeView.swift")
h = home.read_text(encoding="utf-8")

for old, new in [
    (
'''            NavigationLink { MorningEveningAdhkarView() } label: {
                DashboardTile(title: "Dua &\\nZikir", subtitle: "", icon: "dhikr")
            }
''',
'''            NavigationLink { DhikrView() } label: {
                DashboardTile(title: "Dua &\\nZikir", subtitle: "", icon: "dhikr")
            }
'''
    ),
    (
'''            NavigationLink { PrayerHowToView() } label: {
                DashboardTile(title: "Namaz\\nÖğren", subtitle: "", icon: "prayer")
            }
''',
'''            NavigationLink { GuideView() } label: {
                DashboardTile(title: "Namaz\\nÖğren", subtitle: "", icon: "prayer")
            }
'''
    ),
]:
    if old not in h:
        raise SystemExit("v3.59: Home reference destination anchor missing")
    h = h.replace(old, new, 1)

old = '''            NavigationLink { QuranView() } label: {
                DashboardTile(title: "Favorilerim", subtitle: "Favorilerim", icon: "fav")
            }
'''
new = '''            NavigationLink { QuranFavoritesLandingView() } label: {
                DashboardTile(title: "Favorilerim", subtitle: "Favorilerim", icon: "fav")
            }
'''
if old not in h:
    raise SystemExit("v3.59: Home favorites anchor missing")
h = h.replace(old, new, 1)

old = '''                            referenceMapTile
'''
new = '''                            Link(destination: URL(string: "https://maps.apple.com/?q=Kaaba&ll=21.4225,39.8262")!) {
                                referenceMapTile
                            }
                            .buttonStyle(.plain)
'''
if old not in h:
    raise SystemExit("v3.59: Prayer map tile anchor missing")
h = h.replace(old, new, 1)
home.write_text(h, encoding="utf-8")

# --- QA direct routes for destination smoke rendering.
app = Path("SalahZeit/SalahZeitApp.swift")
a = app.read_text(encoding="utf-8")
old = '''        case "times":
            NavigationStack {
                PrayerTimesOverviewView()
                    .toolbar { referenceQAToolbar }
            }
        default:
'''
new = '''        case "times":
            NavigationStack {
                PrayerTimesOverviewView()
                    .toolbar { referenceQAToolbar }
            }
        case "quran-favorites":
            NavigationStack { QuranFavoritesLandingView() }
        case "namaz-howto":
            NavigationStack { PrayerHowToView() }
        case "tasbih":
            NavigationStack { TasbihCounterView() }
        case "dhikr-morning":
            NavigationStack { MorningEveningAdhkarView() }
        case "dhikr-duas":
            NavigationStack { QuranicDuaLibraryView() }
        case "dhikr-audio":
            NavigationStack { PrayerDuaAudioView() }
        case "qibla":
            NavigationStack { QiblaView() }
        case "settings":
            NavigationStack { SettingsView() }
        default:
'''
if old not in a:
    raise SystemExit("v3.59: QA route anchor missing")
a = a.replace(old, new, 1)
app.write_text(a, encoding="utf-8")

print("SalahPath v3.59 functional wiring fixes applied")
