from pathlib import Path
import textwrap


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Expected block not found for {label}: {old[:80]!r}")
    return text.replace(old, new, 1)

# ---------- GuideView: better audio + richer dua/surah audio library ----------
p = Path('SalahZeit/Views/GuideView.swift')
s = p.read_text(encoding='utf-8')

s = s.replace('Label(settings.t("Gebetsduas anhören", "Namaz dualarını dinle"), systemImage: "speaker.wave.2")',
              'Label(settings.t("Duas, Suren & Audio", "Dualar, sureler ve ses"), systemImage: "speaker.wave.2")')

s = s.replace('Label(settings.t("Duas & Audio", "Dualar ve Ses"), systemImage: "speaker.wave.2")',
              'Label(settings.t("Duas, Sureler & Ses", "Dualar, sureler ve ses"), systemImage: "speaker.wave.2")')

old_audio_block = '''@MainActor
final class RemoteAudioPlayer: ObservableObject {
    @Published var activeURL: URL?
    @Published var isPlaying = false
    private var player: AVPlayer?

    func toggle(_ url: URL) {
        if activeURL == url, isPlaying {
            player?.pause(); isPlaying = false; return
        }
        player?.pause()
        activeURL = url
        player = AVPlayer(url: url)
        player?.play()
        isPlaying = true
    }

    func stop() { player?.pause(); isPlaying = false }
}

private struct AudioDua: Identifiable {
    let id = UUID(); let deTitle: String; let trTitle: String; let url: URL; let sourceURL: URL
}

struct DuaAudioLibraryView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var audio = RemoteAudioPlayer()

    private let items: [AudioDua] = [
        .init(deTitle:"Sübhaneke", trTitle:"Sübhâneke", url: URL(string:"https://elifbe.com.tr/wp-content/uploads/sayfa24-1.mp3")!, sourceURL: URL(string:"https://elifbe.com.tr/subhaneke/")!),
        .init(deTitle:"Ettehiyyatü", trTitle:"Ettehiyyâtü", url: URL(string:"https://elifbe.com.tr/wp-content/uploads/sayfa24-2.mp3")!, sourceURL: URL(string:"https://elifbe.com.tr/ettehiyyatu/")!),
        .init(deTitle:"Allahümme Salli & Barik", trTitle:"Allâhümme Salli ve Bârik", url: URL(string:"https://elifbe.com.tr/wp-content/uploads/sayfa24-3.mp3")!, sourceURL: URL(string:"https://elifbe.com.tr/allahumme-salli-ve-barik/")!),
        .init(deTitle:"Rabbena-Duas", trTitle:"Rabbenâ duaları", url: URL(string:"https://elifbe.com.tr/wp-content/uploads/sayfa25-1.mp3")!, sourceURL: URL(string:"https://elifbe.com.tr/rabbena-atina-ve-rabbenagfirli/")!)
    ]

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Hier werden echte menschliche Aufnahmen gestreamt, keine KI-Stimmen. Für eine öffentliche App-Store-Veröffentlichung müssen die Nutzungsrechte der externen Aufnahmen vorab endgültig geklärt werden.",
                    "Burada yapay zekâ sesi değil, gerçek insan kayıtları yayınlanır. App Store'da herkese açık yayınlamadan önce dış kayıtların kullanım hakları kesin olarak doğrulanmalıdır."
                ))
                .font(.footnote).foregroundStyle(.secondary)
            }

            Section(settings.t("Gebetsduas", "Namaz duaları")) {
                ForEach(items) { item in
                    VStack(alignment:.leading,spacing:8) {
                        HStack {
                            Text(settings.language == .german ? item.deTitle : item.trTitle).font(.headline)
                            Spacer()
                            Button {
                                audio.toggle(item.url)
                            } label: {
                                Image(systemName: audio.activeURL == item.url && audio.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                                    .font(.title2)
                            }
                            .buttonStyle(.plain)
                        }
                        Link(settings.t("Quelle öffnen", "Kaynağı aç"), destination: item.sourceURL)
                            .font(.caption)
                    }.padding(.vertical,4)
                }
            }
        }
        .navigationTitle(settings.t("Dua Audio", "Dua Sesleri"))
        .onDisappear { audio.stop() }
    }
}
'''

new_audio_block = '''@MainActor
final class RemoteAudioPlayer: ObservableObject {
    @Published var activeURL: URL?
    @Published var isPlaying = false
    @Published var lastError: String?
    private var player: AVPlayer?
    private var endObserver: NSObjectProtocol?

    func toggle(_ url: URL) {
        if activeURL == url, isPlaying {
            player?.pause()
            isPlaying = false
            return
        }
        play(url)
    }

    func play(_ url: URL) {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default, options: [.allowAirPlay, .allowBluetooth])
            try AVAudioSession.sharedInstance().setActive(true)
            lastError = nil
            player?.pause()
            if let endObserver { NotificationCenter.default.removeObserver(endObserver) }
            let item = AVPlayerItem(url: url)
            endObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: item, queue: .main) { [weak self] _ in
                self?.isPlaying = false
            }
            player = AVPlayer(playerItem: item)
            activeURL = url
            player?.play()
            isPlaying = true
        } catch {
            lastError = error.localizedDescription
            isPlaying = false
        }
    }

    func stop() {
        player?.pause()
        isPlaying = false
    }
}

private struct AudioDua: Identifiable {
    let id = UUID()
    let deTitle: String
    let trTitle: String
    let deDetail: String
    let trDetail: String
    let url: URL
    let sourceLabel: String
    let sourceURL: URL
}

private struct ShortSurahAudio: Identifiable {
    let id = UUID()
    let surahNumber: Int
    let arabicName: String
    let latinName: String
    let deDetail: String
    let trDetail: String
}

struct DuaAudioLibraryView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var audio = RemoteAudioPlayer()

    private let duas: [AudioDua] = [
        .init(deTitle:"Sübhaneke", trTitle:"Sübhâneke", deDetail:"Einstiegsdua im Gebet.", trDetail:"Namaza giriş duası.", url: URL(string:"https://elifbe.com.tr/wp-content/uploads/sayfa24-1.mp3")!, sourceLabel: "elifbe.com.tr", sourceURL: URL(string:"https://elifbe.com.tr/subhaneke/")!),
        .init(deTitle:"Ettehiyyatü", trTitle:"Ettehiyyâtü", deDetail:"Tashahhud im Sitzen nach zwei Rakʿat.", trDetail:"İki rekâttan sonraki tahiyyat duası.", url: URL(string:"https://elifbe.com.tr/wp-content/uploads/sayfa24-2.mp3")!, sourceLabel: "elifbe.com.tr", sourceURL: URL(string:"https://elifbe.com.tr/ettehiyyatu/")!),
        .init(deTitle:"Allahümme Salli & Barik", trTitle:"Allâhümme Salli ve Bârik", deDetail:"Salawat im letzten Sitzen.", trDetail:"Son oturuştaki salavat duası.", url: URL(string:"https://elifbe.com.tr/wp-content/uploads/sayfa24-3.mp3")!, sourceLabel: "elifbe.com.tr", sourceURL: URL(string:"https://elifbe.com.tr/allahumme-salli-ve-barik/")!),
        .init(deTitle:"Rabbena-Duas", trTitle:"Rabbenâ duaları", deDetail:"Häufig gelesene Abschlussduas.", trDetail:"Sık okunan kapanış duaları.", url: URL(string:"https://elifbe.com.tr/wp-content/uploads/sayfa25-1.mp3")!, sourceLabel: "elifbe.com.tr", sourceURL: URL(string:"https://elifbe.com.tr/rabbena-atina-ve-rabbenagfirli/")!)
    ]

    private let surahs: [ShortSurahAudio] = [
        .init(surahNumber: 1, arabicName: "الفاتحة", latinName: "Al-Fatiha", deDetail: "Im Gebet unverzichtbar – jede Rakʿah.", trDetail: "Namazın her rekâtında okunur."),
        .init(surahNumber: 108, arabicName: "الكوثر", latinName: "Al-Kawthar", deDetail: "Sehr kurze Sura für Lernende.", trDetail: "Öğrenenler için çok kısa sûre."),
        .init(surahNumber: 109, arabicName: "الكافرون", latinName: "Al-Kafirun", deDetail: "Häufig als Zusatzsura im Gebet gelesen.", trDetail: "Namazda sık okunan ek sûre."),
        .init(surahNumber: 112, arabicName: "الإخلاص", latinName: "Al-Ikhlas", deDetail: "Kurze und sehr bekannte Sura.", trDetail: "Kısa ve çok bilinen sûre."),
        .init(surahNumber: 113, arabicName: "الفلق", latinName: "Al-Falaq", deDetail: "Schutzsura.", trDetail: "Koruyucu sûre."),
        .init(surahNumber: 114, arabicName: "الناس", latinName: "An-Nas", deDetail: "Schutzsura.", trDetail: "Koruyucu sûre.")
    ]

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Hier werden echte menschliche Aufnahmen gestreamt, keine KI-Stimmen. Quran-Audio kommt vom Islamic Network CDN, Gebetsduas aktuell aus externen Lernquellen.",
                    "Burada yapay zekâ sesi değil, gerçek insan kayıtları yayınlanır. Kur'an sesleri Islamic Network CDN'den, namaz duaları ise şu anda harici eğitim kaynaklarından gelir."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)

                if let lastError = audio.lastError {
                    Label(lastError, systemImage: "exclamationmark.triangle.fill")
                        .font(.caption)
                        .foregroundStyle(.orange)
                }
            }

            Section(settings.t("Gebetsduas", "Namaz duaları")) {
                ForEach(duas) { item in
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            VStack(alignment: .leading, spacing: 3) {
                                Text(settings.language == .german ? item.deTitle : item.trTitle).font(.headline)
                                Text(settings.language == .german ? item.deDetail : item.trDetail)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                            Button { audio.toggle(item.url) } label: {
                                Image(systemName: audio.activeURL == item.url && audio.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                                    .font(.title2)
                            }
                            .buttonStyle(.plain)
                        }
                        Link("\(settings.t("Quelle", "Kaynak")): \(item.sourceLabel)", destination: item.sourceURL)
                            .font(.caption)
                    }
                    .padding(.vertical, 4)
                }
            }

            Section(settings.t("Kurze Suren mit Audio", "Sesli kısa sureler")) {
                ForEach(surahs) { item in
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            VStack(alignment: .leading, spacing: 3) {
                                Text(item.latinName).font(.headline)
                                Text(item.arabicName).font(.subheadline)
                                Text(settings.language == .german ? item.deDetail : item.trDetail)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                            Button { audio.toggle(surahURL(item.surahNumber)) } label: {
                                Image(systemName: audio.activeURL == surahURL(item.surahNumber) && audio.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                                    .font(.title2)
                            }
                            .buttonStyle(.plain)
                        }
                        Text(settings.t("Rezitator", "Kâri") + ": \(settings.quranReciter.title)")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 4)
                }
            }
        }
        .navigationTitle(settings.t("Dua, Suren & Audio", "Dualar, sureler ve ses"))
        .onDisappear { audio.stop() }
    }

    private func surahURL(_ number: Int) -> URL {
        URL(string: "https://cdn.islamic.network/quran/audio-surah/\(settings.quranReciter.bitrate)/\(settings.quranReciter.edition)/\(number).mp3")!
    }
}
'''

s = replace_once(s, old_audio_block, new_audio_block, label='audio block')
p.write_text(s, encoding='utf-8')

# ---------- HomeView: show full sequence + streak + daily dua ----------
p = Path('SalahZeit/Views/HomeView.swift')
h = p.read_text(encoding='utf-8')

insert_after_imports = '''
private enum PrayerTrackerStore {
    private static let prefix = "prayerTracker-"
    private static let formatter: DateFormatter = {
        let f = DateFormatter()
        f.calendar = .current
        f.locale = Locale(identifier: "en_US_POSIX")
        f.dateFormat = "yyyy-MM-dd"
        return f
    }()

    static let requiredKinds: [PrayerKind] = [.fajr, .dhuhr, .asr, .maghrib, .isha]

    private static func key(for date: Date) -> String {
        prefix + formatter.string(from: date)
    }

    static func completedKinds(for date: Date) -> Set<String> {
        Set(UserDefaults.standard.stringArray(forKey: key(for: date)) ?? [])
    }

    static func isCompleted(_ kind: PrayerKind, on date: Date) -> Bool {
        completedKinds(for: date).contains(kind.rawValue)
    }

    @discardableResult
    static func toggle(_ kind: PrayerKind, on date: Date) -> Bool {
        var current = completedKinds(for: date)
        let inserted: Bool
        if current.contains(kind.rawValue) {
            current.remove(kind.rawValue)
            inserted = false
        } else {
            current.insert(kind.rawValue)
            inserted = true
        }
        UserDefaults.standard.set(Array(current).sorted(), forKey: key(for: date))
        return inserted
    }

    static func completedCount(on date: Date) -> Int {
        requiredKinds.filter { isCompleted($0, on: date) }.count
    }

    static func streak(upTo date: Date) -> Int {
        let calendar = Calendar.current
        var day = calendar.startOfDay(for: date)
        var total = 0
        while completedCount(on: day) == requiredKinds.count {
            total += 1
            guard let previous = calendar.date(byAdding: .day, value: -1, to: day) else { break }
            day = previous
        }
        return total
    }
}

private struct DailyDuaEntry {
    let deTitle: String
    let trTitle: String
    let arabic: String
    let transliteration: String
    let deMeaning: String
    let trMeaning: String
    let repetition: String?
}

private enum DailyDuaStore {
    static let items: [DailyDuaEntry] = [
        .init(deTitle: "Rabbana atina", trTitle: "Rabbenâ âtinâ", arabic: "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", transliteration: "Rabbanā ātinā fi-d-dunyā ḥasanah wa fi-l-ākhirati ḥasanah wa qinā ʿadhāba-n-nār", deMeaning: "Unser Herr, gib uns Gutes im Diesseits und Gutes im Jenseits und bewahre uns vor der Strafe des Feuers.", trMeaning: "Rabbimiz, bize dünyada da iyilik ver, ahirette de iyilik ver ve bizi ateş azabından koru.", repetition: nil),
        .init(deTitle: "Rabbi zidni ilma", trTitle: "Rabbî zidnî ilmâ", arabic: "رَبِّ زِدْنِي عِلْمًا", transliteration: "Rabbi zidnī ʿilmā", deMeaning: "Mein Herr, mehre mein Wissen.", trMeaning: "Rabbim, ilmimi artır.", repetition: nil),
        .init(deTitle: "Hasbunallahu", trTitle: "Hasbünallahu", arabic: "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ", transliteration: "Ḥasbunallāhu wa niʿma-l-wakīl", deMeaning: "Allah genügt uns, und Er ist der beste Sachwalter.", trMeaning: "Allah bize yeter, O ne güzel vekildir.", repetition: nil),
        .init(deTitle: "Sayyidul Istighfar", trTitle: "Seyyidü'l-istiğfar", arabic: "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلٰهَ إِلَّا أَنْتَ...", transliteration: "Allāhumma anta rabbī lā ilāha illā anta...", deMeaning: "Große Bittformel um Vergebung.", trMeaning: "Bağışlanma için çok faziletli dua.", repetition: settings_placeholder)
    ]

    static func item(for date: Date) -> DailyDuaEntry {
        let day = Calendar.current.ordinality(of: .day, in: .era, for: date) ?? 1
        return items[(day - 1) % items.count]
    }
}
'''
insert_after_imports = insert_after_imports.replace('settings_placeholder', '"Morgens / akşam"')
if 'private enum PrayerTrackerStore {' not in h:
    h = h.replace('import CoreLocation\n', 'import CoreLocation\n\n' + insert_after_imports + '\n')

h = h.replace('@State private var selectedPrayer: PrayerOccurrence?\n    private let engine = PrayerEngine()', '@State private var selectedPrayer: PrayerOccurrence?\n    @State private var trackerRefresh = 0\n    private let engine = PrayerEngine()')

old_stack = '''            VStack(spacing: 16) {
                headerCard

                if let next = engine.nextPrayer(now: now, location: location, settings: settings) {
                    nextPrayerCard(next)
                }

                VStack(spacing: 0) {'''
new_stack = '''            VStack(spacing: 16) {
                headerCard

                if let next = engine.nextPrayer(now: now, location: location, settings: settings) {
                    nextPrayerCard(next)
                }

                streakCard
                dailyDuaCard

                VStack(spacing: 0) {'''
h = replace_once(h, old_stack, new_stack, label='home stack')

old_next = '''                    if let rakats = prayer.kind.fardRakats {
                        Text("\(rakats) \(settings.t("Rakʿat Fard", "rekât farz"))")
                            .font(.subheadline)
                    }'''
new_next = '''                    Text(prayer.kind.fullSequence(settings.language))
                        .font(.subheadline)
                        .foregroundStyle(.secondary)'''
h = replace_once(h, old_next, new_next, label='next prayer text')

insert_before_location_state = '''
    private var streakCard: some View {
        let completed = PrayerTrackerStore.completedCount(on: now)
        let streak = PrayerTrackerStore.streak(upTo: now)
        return VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(settings.t("Täglicher Gebets-Tracker", "Günlük namaz takibi"))
                        .font(.headline)
                    Text(settings.t("Motivation statt Druck: markiere, was du heute geschafft hast.", "Baskı değil motivasyon: bugün kıldıklarını işaretle."))
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
                Spacer()
                VStack(alignment: .trailing, spacing: 4) {
                    Text("\(completed)/5")
                        .font(.title3.bold().monospacedDigit())
                    Text(settings.t("Streak: \(streak) Tage", "Seri: \(streak) gün"))
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }

            ProgressView(value: Double(completed), total: 5)

            HStack(spacing: 10) {
                ForEach(PrayerTrackerStore.requiredKinds) { kind in
                    let done = PrayerTrackerStore.isCompleted(kind, on: now)
                    Button {
                        _ = PrayerTrackerStore.toggle(kind, on: now)
                        trackerRefresh += 1
                    } label: {
                        VStack(spacing: 6) {
                            Image(systemName: done ? "checkmark.circle.fill" : "circle")
                                .font(.title3)
                            Text(kind.localizedName(settings.language))
                                .font(.caption2)
                                .lineLimit(1)
                                .minimumScaleFactor(0.65)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 8)
                        .background(done ? Color.green.opacity(0.14) : Color.secondary.opacity(0.08), in: RoundedRectangle(cornerRadius: 12))
                    }
                    .buttonStyle(.plain)
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 20))
    }

    private var dailyDuaCard: some View {
        let dua = DailyDuaStore.item(for: now)
        return VStack(alignment: .leading, spacing: 8) {
            HStack {
                Label(settings.t("Tagesdua", "Günün duası"), systemImage: "sparkles")
                    .font(.headline)
                Spacer()
                if let repetition = dua.repetition {
                    Text(repetition)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
            Text(settings.language == .german ? dua.deTitle : dua.trTitle)
                .font(.subheadline.weight(.semibold))
            Text(dua.arabic)
                .font(.title3)
                .multilineTextAlignment(.trailing)
                .frame(maxWidth: .infinity, alignment: .trailing)
            Text(dua.transliteration)
                .font(.subheadline)
            Text(settings.language == .german ? dua.deMeaning : dua.trMeaning)
                .font(.footnote)
                .foregroundStyle(.secondary)
            Text(settings.t("Kleine Schritte zählen: das nächste Gebet pünktlich, eine kurze Sura und etwas Dhikr.", "Küçük adımlar önemlidir: sıradaki namazı vaktinde kıl, kısa bir sûre oku ve biraz zikir yap."))
                .font(.caption)
                .foregroundStyle(.tertiary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 20))
    }

'''
h = h.replace('    private var locationState: some View {', insert_before_location_state + '    private var locationState: some View {', 1)

old_row = '''                if let rakats = prayer.kind.fardRakats {
                    Text("\(rakats) \(settings.t("Rakʿat Fard", "rekât farz"))")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }'''
new_row = '''                Text(prayer.kind.fullSequence(settings.language))
                    .font(.caption)
                    .foregroundStyle(.secondary)'''
h = replace_once(h, old_row, new_row, label='prayer row text')

p.write_text(h, encoding='utf-8')

# ---------- RootTab labels refine ----------
p = Path('SalahZeit/Views/RootTabView.swift')
r = p.read_text(encoding='utf-8')
r = r.replace('Gebetszeiten, Lernhilfe, Quran, Dhikr und Qibla in einer App.', 'Gebetszeiten, Lernhilfe, Quran, Dua, Dhikr und Qibla in einer App.')
r = r.replace('Namaz vakitleri, namaz öğrenimi, Kur\'an, zikir ve kıble tek uygulamada.', 'Namaz vakitleri, namaz öğrenimi, Kur\'an, dua, zikir ve kıble tek uygulamada.')
p.write_text(r, encoding='utf-8')

# ---------- Build version ----------
p = Path('scripts/build_unsigned_ipa.sh')
b = p.read_text(encoding='utf-8')
b = b.replace('MARKETING_VERSION="3.1"', 'MARKETING_VERSION="3.2"')
b = b.replace('CURRENT_PROJECT_VERSION="4"', 'CURRENT_PROJECT_VERSION="5"')
p.write_text(b, encoding='utf-8')

print('SalahPath v3.2 patch applied')