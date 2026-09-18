from pathlib import Path
import re

# ---------------- GuideView ----------------
p=Path('SalahZeit/Views/GuideView.swift')
s=p.read_text(encoding='utf-8')

s=s.replace('''                NavigationLink { DuaAudioLibraryView() } label: {
                    Label(settings.t("Duas, Suren & Audio", "Dualar, sureler ve ses"), systemImage: "speaker.wave.2")
                }
''','''                NavigationLink { PrayerDuaAudioView() } label: {
                    Label(settings.t("Gebetsduas", "Namaz duaları"), systemImage: "hands.sparkles")
                }
                NavigationLink { ShortSurahLearningView() } label: {
                    Label(settings.t("Kurze Suren lernen", "Kısa sureleri öğren"), systemImage: "text.book.closed.fill")
                }
                NavigationLink { QuranicDuaLibraryView() } label: {
                    Label(settings.t("Dua-Sammlung", "Dua koleksiyonu"), systemImage: "heart.text.square")
                }
''')

# Add real CC0 prayer profile photo to info card
old='''        VStack(alignment: .leading, spacing: 8) {
            Label(settings.t("Kindgerechte Ansicht", "Çocuklara uygun anlatım"), systemImage: "figure.and.child.holdinghands")
                .font(.headline)
            Text(genderNote)
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
'''
new='''        VStack(alignment: .leading, spacing: 10) {
            PrayerProfilePhoto(audience: settings.prayerAudience)
            Label(settings.t("Gebet lernen", "Namazı öğren"), systemImage: "figure.and.child.holdinghands")
                .font(.headline)
            Text(genderNote)
                .font(.subheadline)
                .foregroundStyle(.secondary)
            Text(settings.t(
                "Das Foto dient nur als freundliche Orientierung. Die Schritttexte erklären die Haltung; Unterschiede zwischen Rechtsschulen werden nicht als Fehler dargestellt.",
                "Foto yalnızca sıcak bir görsel yönlendirmedir. Duruşlar adım metinlerinde açıklanır; mezhep farklılıkları hata olarak gösterilmez."
            ))
            .font(.caption)
            .foregroundStyle(.tertiary)
        }
        .cardStyle(material: true)
'''
if old not in s: raise SystemExit('infoCard block not found')
s=s.replace(old,new,1)

# Replace generated figure in each step with simple pose symbol, removing disliked custom figure
s=s.replace('''                PrayerKidIllustration(pose: step.pose, audience: audience)
                    .frame(width: 118, height: 122)
''','''                ZStack {
                    RoundedRectangle(cornerRadius: 18)
                        .fill(Color.accentColor.opacity(0.10))
                    Image(systemName: poseSymbol)
                        .font(.system(size: 35, weight: .medium))
                        .foregroundStyle(Color.accentColor)
                }
                .frame(width: 76, height: 76)
''')

# Add poseSymbol in PrayerStepCard
needle='''    private var postureNote: String? {
'''
pose='''    private var poseSymbol: String {
        switch step.pose {
        case .intention, .standing, .upright: return "figure.stand"
        case .takbir: return "hand.raised.fill"
        case .bowing: return "arrow.down.forward"
        case .prostration: return "arrow.down.to.line.compact"
        case .sitting: return "chair.fill"
        case .salam: return "arrow.left.and.right"
        }
    }

    private var postureNote: String? {
'''
if needle not in s: raise SystemExit('posture needle not found')
s=s.replace(needle,pose,1)

# Insert profile photo component before PrayerKidIllustration struct (old custom illustration left unused but harmless)
marker='''private struct PrayerKidIllustration: View {
'''
profile='''private struct PrayerProfilePhoto: View {
    let audience: PrayerAudience

    private var imageURL: URL? {
        let raw = audience == .male
            ? "https://commons.wikimedia.org/wiki/Special:Redirect/file/Muslim_Kid_Praying.jpg?width=1000"
            : "https://commons.wikimedia.org/wiki/Special:Redirect/file/Women_performing_prayer.jpg?width=1000"
        return URL(string: raw)
    }

    private var sourceURL: URL? {
        let raw = audience == .male
            ? "https://commons.wikimedia.org/wiki/File:Muslim_Kid_Praying.jpg"
            : "https://commons.wikimedia.org/wiki/File:Women_performing_prayer.jpg"
        return URL(string: raw)
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            AsyncImage(url: imageURL) { phase in
                switch phase {
                case .success(let image):
                    image.resizable().scaledToFill()
                case .failure:
                    ZStack { Color.secondary.opacity(0.08); Image(systemName: "photo").font(.largeTitle).foregroundStyle(.secondary) }
                default:
                    ZStack { Color.secondary.opacity(0.08); ProgressView() }
                }
            }
            .frame(height: 175)
            .frame(maxWidth: .infinity)
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .clipped()

            if let sourceURL {
                Link("Wikimedia Commons · CC0", destination: sourceURL)
                    .font(.caption2)
            }
        }
    }
}

'''
if marker not in s: raise SystemExit('prayer illustration marker missing')
s=s.replace(marker,profile+marker,1)

# Replace whole audio section with reliable API-resolved Quran audio + official Diyanet links
start=s.index('// MARK: - Human-recorded dua audio')
end=s.index('// MARK: - Dhikr')
audio_section=r'''// MARK: - Human-recorded prayer/Quran audio

@MainActor
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

    func playQueue(_ urls: [URL]) {
        guard let first = urls.first else {
            lastError = "Keine Audiodatei verfügbar."
            return
        }
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default, options: [.allowAirPlay, .allowBluetooth])
            try AVAudioSession.sharedInstance().setActive(true)
            lastError = nil
            player?.pause()
            if let endObserver { NotificationCenter.default.removeObserver(endObserver) }
            let items = urls.map { AVPlayerItem(url: $0) }
            let queue = AVQueuePlayer(items: items)
            if let last = items.last {
                endObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: last, queue: .main) { [weak self] _ in
                    self?.isPlaying = false
                }
            }
            player = queue
            activeURL = first
            queue.play()
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

private struct AudioEditionResponse: Decodable { let data: AudioSurahData }
private struct AudioSurahData: Decodable { let ayahs: [AudioAyahData] }
private struct AudioAyahData: Decodable { let audio: String? }

private enum QuranAudioResolver {
    static func urls(surah: Int, edition: String) async throws -> [URL] {
        let url = URL(string: "https://api.alquran.cloud/v1/surah/\(surah)/\(edition)")!
        let (data, response) = try await URLSession.shared.data(from: url)
        guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw URLError(.badServerResponse) }
        let decoded = try JSONDecoder().decode(AudioEditionResponse.self, from: data)
        return decoded.data.ayahs.compactMap { item in
            guard let raw = item.audio else { return nil }
            return URL(string: raw.replacingOccurrences(of: "http://", with: "https://"))
        }
    }
}

private struct PrayerDuaLink: Identifiable {
    let id = UUID()
    let deTitle: String
    let trTitle: String
    let deDetail: String
    let trDetail: String
    let sourceURL: URL
}

struct PrayerDuaAudioView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let duas: [PrayerDuaLink] = [
        .init(deTitle: "Sübhaneke", trTitle: "Sübhâneke", deDetail: "Einstiegsdua im Gebet. Offizielle Diyanet-Aufnahme öffnen.", trDetail: "Namaza giriş duası. Resmî Diyanet kaydını aç.", sourceURL: URL(string: "https://dijital.diyanet.gov.tr/Izle/dua/subhaneke-duasi?id=7524")!),
        .init(deTitle: "Ettehiyyatü / Tahiyyat", trTitle: "Ettehiyyâtü / Tahiyyat", deDetail: "Tashahhud im Sitzen. Text und Lernquelle.", trDetail: "Tahiyyat oturuşunda okunur. Metin ve öğrenme kaynağı.", sourceURL: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/namazda-tahiyyat-ve-salli-barik-dualarinin-okunmasi-sirk/019cbdf4-c92f-71ab-b431-11eac874f25f")!),
        .init(deTitle: "Allahümme Salli & Barik", trTitle: "Allâhümme Salli ve Bârik", deDetail: "Salawat im letzten Sitzen. Diyanet-Lernquelle.", trDetail: "Son oturuştaki salavat. Diyanet öğrenme kaynağı.", sourceURL: URL(string: "https://yayin.diyanet.gov.tr/File/Download?id=436&path=dinim_islam.pdf")!),
        .init(deTitle: "Rabbena-Duas", trTitle: "Rabbenâ duaları", deDetail: "Abschlussduas nach den Salawat.", trDetail: "Salavatlardan sonra okunan kapanış duaları.", sourceURL: URL(string: "https://yayin.diyanet.gov.tr/File/Download?id=436&path=dinim_islam.pdf")!)
    ]

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Gebetsduas und kurze Suren sind getrennt: Duas sind Bittgebete; Suren sind Quran-Kapitel. Für Gebetsduas verlinkt SalahPath derzeit auf offizielle Diyanet-Lernquellen, statt instabile MP3-Links vorzutäuschen.",
                    "Namaz duaları ve kısa sureler ayrıdır: Dualar yakarışlardır; sureler Kur'an bölümleridir. SalahPath, bozuk MP3 bağlantıları yerine namaz dualarında şimdilik resmî Diyanet öğrenme kaynaklarını açar."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
            Section(settings.t("Gebetsduas", "Namaz duaları")) {
                ForEach(duas) { item in
                    Link(destination: item.sourceURL) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text(settings.language == .german ? item.deTitle : item.trTitle).font(.headline)
                                Text(settings.language == .german ? item.deDetail : item.trDetail)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                            Image(systemName: "play.rectangle.fill")
                        }
                    }
                }
            }
        }
        .navigationTitle(settings.t("Gebetsduas", "Namaz duaları"))
    }
}

private struct ShortSurahAudio: Identifiable {
    let id = UUID()
    let surahNumber: Int
    let arabicName: String
    let latinName: String
    let deDetail: String
    let trDetail: String
}

struct ShortSurahLearningView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var audio = RemoteAudioPlayer()
    @State private var loadingSurah: Int?

    private let surahs: [ShortSurahAudio] = [
        .init(surahNumber: 1, arabicName: "الفاتحة", latinName: "Al-Fatiha", deDetail: "Grundlage jeder Rakʿah.", trDetail: "Her rekâtın temel kıraatidir."),
        .init(surahNumber: 103, arabicName: "العصر", latinName: "Al-Asr", deDetail: "Sehr kurze Sura.", trDetail: "Çok kısa bir sûre."),
        .init(surahNumber: 108, arabicName: "الكوثر", latinName: "Al-Kawthar", deDetail: "Sehr kurze Sura für Lernende.", trDetail: "Öğrenenler için çok kısa sûre."),
        .init(surahNumber: 109, arabicName: "الكافرون", latinName: "Al-Kafirun", deDetail: "Bekannte kurze Sura.", trDetail: "Bilinen kısa sûre."),
        .init(surahNumber: 112, arabicName: "الإخلاص", latinName: "Al-Ikhlas", deDetail: "Kurze und sehr bekannte Sura.", trDetail: "Kısa ve çok bilinen sûre."),
        .init(surahNumber: 113, arabicName: "الفلق", latinName: "Al-Falaq", deDetail: "Schutzsura.", trDetail: "Koruyucu sûre."),
        .init(surahNumber: 114, arabicName: "الناس", latinName: "An-Nas", deDetail: "Schutzsura.", trDetail: "Koruyucu sûre.")
    ]

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Tippe auf Play: SalahPath fragt die aktuelle Audio-URL über die AlQuran.cloud-API ab und spielt danach die Ayat nacheinander. Dadurch sind wir nicht mehr von einem fest eingebauten CDN-Link abhängig.",
                    "Oynat'a dokun: SalahPath güncel ses bağlantılarını AlQuran.cloud API üzerinden alır ve ayetleri sırayla çalar. Böylece sabit bir CDN bağlantısına bağlı kalmaz."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
                if let error = audio.lastError {
                    Label(error, systemImage: "exclamationmark.triangle.fill")
                        .font(.caption)
                        .foregroundStyle(.orange)
                }
            }
            Section(settings.t("Kurze Suren", "Kısa sureler")) {
                ForEach(surahs) { item in
                    HStack(spacing: 12) {
                        VStack(alignment: .leading, spacing: 3) {
                            Text(item.latinName).font(.headline)
                            Text(item.arabicName).font(.subheadline)
                            Text(settings.language == .german ? item.deDetail : item.trDetail)
                                .font(.caption).foregroundStyle(.secondary)
                        }
                        Spacer()
                        Button {
                            Task { await play(item) }
                        } label: {
                            if loadingSurah == item.surahNumber { ProgressView() }
                            else { Image(systemName: "play.circle.fill").font(.title2) }
                        }
                        .buttonStyle(.plain)
                    }
                    .padding(.vertical, 4)
                }
            }
            Section {
                Text("\(settings.t("Rezitator", "Kâri")): \(settings.quranReciter.title)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Suren lernen", "Sureleri öğren"))
        .onDisappear { audio.stop() }
    }

    @MainActor
    private func play(_ item: ShortSurahAudio) async {
        loadingSurah = item.surahNumber
        defer { loadingSurah = nil }
        do {
            let urls = try await QuranAudioResolver.urls(surah: item.surahNumber, edition: settings.quranReciter.edition)
            audio.playQueue(urls)
        } catch {
            audio.lastError = error.localizedDescription
        }
    }
}

private struct QuranicDua: Identifiable {
    let id = UUID()
    let reference: String
    let arabic: String
    let transliteration: String
    let de: String
    let tr: String
}

struct QuranicDuaLibraryView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let items: [QuranicDua] = [
        .init(reference: "Quran 2:201", arabic: "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", transliteration: "Rabbanā ātinā fi-d-dunyā ḥasanah wa fi-l-ākhirati ḥasanah wa qinā ʿadhāba-n-nār", de: "Unser Herr, gib uns Gutes im Diesseits und Gutes im Jenseits und bewahre uns vor der Strafe des Feuers.", tr: "Rabbimiz, bize dünyada da iyilik ver, ahirette de iyilik ver ve bizi ateş azabından koru."),
        .init(reference: "Quran 20:114", arabic: "رَبِّ زِدْنِي عِلْمًا", transliteration: "Rabbi zidnī ʿilmā", de: "Mein Herr, mehre mein Wissen.", tr: "Rabbim, ilmimi artır."),
        .init(reference: "Quran 25:74", arabic: "رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا", transliteration: "Rabbanā hab lanā min azwājinā wa dhurriyyātinā qurrata aʿyun...", de: "Unser Herr, schenke uns an unseren Ehepartnern und Nachkommen Freude und mache uns zu Vorbildern für Gottesbewusste.", tr: "Rabbimiz, eşlerimizi ve çocuklarımızı bize göz aydınlığı kıl ve bizi takvâ sahiplerine önder eyle."),
        .init(reference: "Quran 3:8", arabic: "رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِنْ لَدُنْكَ رَحْمَةً", transliteration: "Rabbanā lā tuzigh qulūbanā baʿda idh hadaytanā wa hab lanā min ladunka raḥmah", de: "Unser Herr, lass unsere Herzen nicht abweichen, nachdem Du uns rechtgeleitet hast, und schenke uns Barmherzigkeit von Dir.", tr: "Rabbimiz, bize hidayet verdikten sonra kalplerimizi eğriltme; bize katından rahmet bağışla.")
    ]

    var body: some View {
        List(items) { item in
            VStack(alignment: .leading, spacing: 8) {
                Text(item.reference).font(.caption.bold()).foregroundStyle(.secondary)
                Text(item.arabic).font(.title3).frame(maxWidth: .infinity, alignment: .trailing).multilineTextAlignment(.trailing)
                Text(item.transliteration).font(.subheadline.weight(.semibold))
                Text(settings.language == .german ? item.de : item.tr).font(.footnote).foregroundStyle(.secondary)
            }
            .padding(.vertical, 5)
        }
        .navigationTitle(settings.t("Dua-Sammlung", "Dua koleksiyonu"))
    }
}

'''
s=s[:start]+audio_section+s[end:]

# Quran audio: allow audio field, fetch audio edition, queue full surah
s=s.replace('private struct AyahData: Decodable, Identifiable { let number:Int; let numberInSurah:Int; let text:String; var id:Int { number } }',
'''private struct AyahData: Decodable, Identifiable {
    let number:Int
    let numberInSurah:Int
    let text:String
    let audio:String?
    var id:Int { number }
}''')

s=s.replace('''    func loadSurah(_ number:Int, language:AppLanguage) async throws -> (SurahData,SurahData) {
        let translation = language == .german ? "de.bubenheim" : "tr.diyanet"
        async let arabic = fetch(number:number, edition:"quran-uthmani")
        async let translated = fetch(number:number, edition:translation)
        return try await (arabic,translated)
    }
''','''    func loadSurah(_ number:Int, language:AppLanguage, reciter:QuranReciter) async throws -> (SurahData,SurahData,SurahData) {
        let translation = language == .german ? "de.bubenheim" : "tr.diyanet"
        async let arabic = fetch(number:number, edition:"quran-uthmani")
        async let translated = fetch(number:number, edition:translation)
        async let audio = fetch(number:number, edition:reciter.edition)
        return try await (arabic,translated,audio)
    }
''')

s=s.replace('@State private var translation:SurahData?\n    @State private var error:String?', '@State private var translation:SurahData?\n    @State private var audioSurah:SurahData?\n    @State private var error:String?')

s=s.replace('''                    Button {
                        audio.toggle(audioURL)
                    } label: {
                        Label(audio.activeURL == audioURL && audio.isPlaying ? settings.t("Pause", "Duraklat") : settings.t("Rezitation anhören", "Tilaveti dinle"), systemImage:audio.activeURL == audioURL && audio.isPlaying ? "pause.fill" : "play.fill")
                    }.buttonStyle(.borderedProminent)
''','''                    Button {
                        let urls = audioSurah?.ayahs.compactMap { ayah -> URL? in
                            guard let raw = ayah.audio else { return nil }
                            return URL(string: raw.replacingOccurrences(of: "http://", with: "https://"))
                        } ?? []
                        if audio.isPlaying { audio.stop() } else { audio.playQueue(urls) }
                    } label: {
                        Label(audio.isPlaying ? settings.t("Pause", "Duraklat") : settings.t("Sura anhören", "Sureyi dinle"), systemImage:audio.isPlaying ? "pause.fill" : "play.fill")
                    }.buttonStyle(.borderedProminent)
''')

# replace per ayah button block using audio data by index
s=s.replace('''                                    QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)
                                    audio.toggle(ayahAudioURL(globalAyah: ar.number))
                                } label: {
                                    Image(systemName: audio.activeURL == ayahAudioURL(globalAyah: ar.number) && audio.isPlaying ? "pause.circle.fill" : "play.circle")
''','''                                    QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)
                                    if let raw = audioSurah?.ayahs[safe: entry.offset].audio,
                                       let url = URL(string: raw.replacingOccurrences(of: "http://", with: "https://")) {
                                        audio.toggle(url)
                                    }
                                } label: {
                                    Image(systemName: "play.circle")
''')

s=s.replace('''        .task(id:settings.language) {
            do { let result=try await store.loadSurah(surah.number,language:settings.language); arabic=result.0; translation=result.1; error=nil }
            catch { self.error=error.localizedDescription }
        }
''','''        .task(id:"\(settings.language.rawValue)-\(settings.quranReciter.rawValue)") {
            do {
                let result = try await store.loadSurah(surah.number, language: settings.language, reciter: settings.quranReciter)
                arabic = result.0
                translation = result.1
                audioSurah = result.2
                error = nil
            } catch { self.error=error.localizedDescription }
        }
''')

# Remove stale direct URL helpers
s=re.sub(r'\n    private var audioURL:URL \{.*?\n    \}\n\n    private func ayahAudioURL\(globalAyah: Int\) -> URL \{.*?\n    \}\n', '\n', s, flags=re.S)

# add safe collection extension before shared card style
marker='// MARK: - Shared card style\n'
safe='''private extension Collection {
    subscript(safe index: Index) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}

'''
if safe not in s: s=s.replace(marker,safe+marker,1)

p.write_text(s,encoding='utf-8')

# ---------------- HomeView: Daily Deen + legend + source refs ----------------
p=Path('SalahZeit/Views/HomeView.swift')
h=p.read_text(encoding='utf-8')

# source labels in daily duas
h=h.replace('''    let repetition: String?
}''','''    let repetition: String?
    let source: String
}''',1)
# replace four initializers linewise
h=h.replace('repetition: nil),', 'repetition: nil, source: "Quran 2:201"),',1)
h=h.replace('repetition: nil),', 'repetition: nil, source: "Quran 20:114"),',1)
h=h.replace('repetition: nil),', 'repetition: nil, source: "Quran 3:173"),',1)
h=h.replace('repetition: "Morgens / akşam")', 'repetition: "Morgens / akşam", source: "Bukhari 6306")',1)

# improve streak logic to retain prior complete-day streak while today is ongoing
old='''    static func streak(upTo date: Date) -> Int {
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
}'''
new='''    static func streak(upTo date: Date) -> Int {
        let calendar = Calendar.current
        var day = calendar.startOfDay(for: date)
        if completedCount(on: day) < requiredKinds.count,
           let yesterday = calendar.date(byAdding: .day, value: -1, to: day) {
            day = yesterday
        }
        var total = 0
        while completedCount(on: day) == requiredKinds.count {
            total += 1
            guard let previous = calendar.date(byAdding: .day, value: -1, to: day) else { break }
            day = previous
        }
        return total
    }
}

private enum DailyDeenStore {
    static func dayKey(_ date: Date) -> String {
        let f = DateFormatter(); f.calendar = .current; f.locale = Locale(identifier: "en_US_POSIX"); f.dateFormat = "yyyy-MM-dd"
        return "dailyDeen-" + f.string(from: date)
    }
    static func values(_ date: Date) -> Set<String> { Set(UserDefaults.standard.stringArray(forKey: dayKey(date)) ?? []) }
    static func isDone(_ id: String, _ date: Date) -> Bool { values(date).contains(id) }
    static func toggle(_ id: String, _ date: Date) {
        var set = values(date)
        if set.contains(id) { set.remove(id) } else { set.insert(id) }
        UserDefaults.standard.set(Array(set), forKey: dayKey(date))
    }
}'''
if old not in h: raise SystemExit('streak block missing')
h=h.replace(old,new,1)

# add state refresh
h=h.replace('@State private var trackerRefresh = 0', '@State private var trackerRefresh = 0\n    @State private var dailyDeenRefresh = 0')

# add cards after nextPrayer
h=h.replace('''                streakCard
                dailyDuaCard
''','''                prayerLegendCard
                dailyDeenCard
                streakCard
                dailyDuaCard
''',1)

# insert card vars before streakCard
needle='''    private var streakCard: some View {
'''
insert='''    private var prayerLegendCard: some View {
        HStack(spacing: 10) {
            legendPill(settings.t("Fard · Pflicht", "Farz · zorunlu"), system: "exclamationmark.circle.fill")
            legendPill(settings.t("Sunnah · Vorbild", "Sünnet · örneklik"), system: "star.circle.fill")
            legendPill(settings.t("Witr", "Vitir"), system: "moon.stars.fill")
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 20))
    }

    private func legendPill(_ title: String, system: String) -> some View {
        VStack(spacing: 5) {
            Image(systemName: system)
            Text(title).font(.caption2).multilineTextAlignment(.center).lineLimit(2)
        }
        .frame(maxWidth: .infinity)
    }

    private var dailyDeenCard: some View {
        let tasks = [
            ("quran", settings.t("5 Min. Quran", "5 dk Kur'an"), "book.fill"),
            ("dhikr", settings.t("Kurzer Dhikr", "Kısa zikir"), "circle.grid.cross.fill"),
            ("learn", settings.t("1 Dua/Sura lernen", "1 dua/sure öğren"), "graduationcap.fill")
        ]
        let done = tasks.filter { DailyDeenStore.isDone($0.0, now) }.count
        return VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 3) {
                    Text(settings.t("Daily Deen", "Günlük Deen")).font(.headline)
                    Text(settings.t("Kleine, regelmäßige Schritte statt alles auf einmal.", "Her şeyi bir anda değil, küçük ve düzenli adımlar."))
                        .font(.caption).foregroundStyle(.secondary)
                }
                Spacer()
                Text("\(done)/\(tasks.count)").font(.headline.monospacedDigit())
            }
            ForEach(Array(tasks.enumerated()), id: \.offset) { _, task in
                let checked = DailyDeenStore.isDone(task.0, now)
                Button {
                    DailyDeenStore.toggle(task.0, now)
                    dailyDeenRefresh += 1
                } label: {
                    HStack {
                        Image(systemName: task.2).frame(width: 24)
                        Text(task.1)
                        Spacer()
                        Image(systemName: checked ? "checkmark.circle.fill" : "circle")
                            .foregroundStyle(checked ? .green : .secondary)
                    }
                    .contentShape(Rectangle())
                }
                .buttonStyle(.plain)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 20))
    }

'''
if needle not in h: raise SystemExit('streak needle missing')
h=h.replace(needle,insert+needle,1)

# add source to daily dua
h=h.replace('''            Text(settings.language == .german ? dua.deMeaning : dua.trMeaning)
                .font(.footnote)
                .foregroundStyle(.secondary)
''','''            Text(settings.language == .german ? dua.deMeaning : dua.trMeaning)
                .font(.footnote)
                .foregroundStyle(.secondary)
            Text(dua.source)
                .font(.caption2.bold())
                .foregroundStyle(.tertiary)
''',1)

p.write_text(h,encoding='utf-8')

# ---------------- RootTab: clearer all-in-one More hub ----------------
p=Path('SalahZeit/Views/RootTabView.swift')
r=p.read_text(encoding='utf-8')
r=r.replace('''                NavigationLink { DuaAudioLibraryView() } label: {
                    Label(settings.t("Duas & Audio", "Dualar ve Ses"), systemImage: "speaker.wave.2")
                }
''','''                NavigationLink { PrayerDuaAudioView() } label: {
                    Label(settings.t("Gebetsduas", "Namaz duaları"), systemImage: "hands.sparkles")
                }
                NavigationLink { ShortSurahLearningView() } label: {
                    Label(settings.t("Kurze Suren + Audio", "Kısa sureler + ses"), systemImage: "play.square.stack")
                }
                NavigationLink { QuranicDuaLibraryView() } label: {
                    Label(settings.t("Dua-Sammlung", "Dua koleksiyonu"), systemImage: "heart.text.square")
                }
''')
r=r.replace('''            Section(settings.t("SalahPath", "SalahPath")) {
                Text(settings.t(
                    "Gebetszeiten, Lernhilfe, Quran, Dua, Dhikr und Qibla in einer App.",
                    "Namaz vakitleri, namaz öğrenimi, Kur'an, dua, zikir ve kıble tek uygulamada."
                ))
''','''            Section(settings.t("SalahPath · All in One", "SalahPath · Hepsi bir arada")) {
                Text(settings.t(
                    "Gebetszeiten, kompletter Fard/Sunnah/Witr-Plan, Gebets-Tracker, Daily Deen, Quran, Suren-Audio, Duas, Dhikr, Wudu, Lernen und Qibla in einer App.",
                    "Namaz vakitleri, tam farz/sünnet/vitir planı, namaz takibi, Günlük Deen, Kur'an, sure sesleri, dualar, zikir, abdest, öğrenme ve kıble tek uygulamada."
                ))
''')
p.write_text(r,encoding='utf-8')

# ---------------- build version ----------------
p=Path('scripts/build_unsigned_ipa.sh')
b=p.read_text(encoding='utf-8').replace('MARKETING_VERSION="3.2"','MARKETING_VERSION="3.3"').replace('CURRENT_PROJECT_VERSION="5"','CURRENT_PROJECT_VERSION="6"')
p.write_text(b,encoding='utf-8')

print('SalahPath v3.3 local patch applied')