from pathlib import Path
import re


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Expected block missing: {label}')
    return text.replace(old, new, 1)

# ---------------- HomeView ----------------
p = Path('SalahZeit/Views/HomeView.swift')
h = p.read_text(encoding='utf-8')

h = h.replace('private enum PrayerTrackerStore {', 'enum PrayerTrackerStore {', 1)

# Add pause storage / helpers before completedCount
needle = '''    static func completedCount(on date: Date) -> Int {
        requiredKinds.filter { isCompleted($0, on: date) }.count
    }
'''
insert = '''    private static let pausePrefix = "prayerTrackerPause-"

    private static func pauseKey(for date: Date) -> String {
        pausePrefix + formatter.string(from: date)
    }

    static func isPaused(_ date: Date) -> Bool {
        UserDefaults.standard.bool(forKey: pauseKey(for: date))
    }

    static func togglePause(_ date: Date) {
        UserDefaults.standard.set(!isPaused(date), forKey: pauseKey(for: date))
    }

    static func completedCount(on date: Date) -> Int {
        requiredKinds.filter { isCompleted($0, on: date) }.count
    }
'''
if needle in h and 'pausePrefix' not in h:
    h = h.replace(needle, insert, 1)

# Replace streak function with pause-aware version
pattern = re.compile(r'''    static func streak\(upTo date: Date\) -> Int \{.*?\n    \}\n\}''', re.S)
m = pattern.search(h)
if not m:
    raise SystemExit('streak function not found')
new_streak = '''    static func streak(upTo date: Date) -> Int {
        let calendar = Calendar.current
        var day = calendar.startOfDay(for: date)

        if !isPaused(day) && completedCount(on: day) < requiredKinds.count,
           let yesterday = calendar.date(byAdding: .day, value: -1, to: day) {
            day = yesterday
        }

        var total = 0
        var safety = 0
        while safety < 730 {
            safety += 1
            if isPaused(day) {
                guard let previous = calendar.date(byAdding: .day, value: -1, to: day) else { break }
                day = previous
                continue
            }
            guard completedCount(on: day) == requiredKinds.count else { break }
            total += 1
            guard let previous = calendar.date(byAdding: .day, value: -1, to: day) else { break }
            day = previous
        }
        return total
    }
}

struct TrackerPauseView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var refresh = 0

    var body: some View {
        let today = Date()
        let paused = PrayerTrackerStore.isPaused(today)
        List {
            Section {
                Toggle(isOn: Binding(
                    get: { PrayerTrackerStore.isPaused(today) },
                    set: { _ in PrayerTrackerStore.togglePause(today); refresh += 1 }
                )) {
                    Label(settings.t("Tracker heute pausieren", "Bugün takibi duraklat"), systemImage: "pause.circle")
                }
                Text(settings.t(
                    "Die Pause verändert nur Statistik und Streak. Sie ist keine Aussage darüber, ob ein Gebet religiös verpflichtend ist.",
                    "Duraklatma yalnızca istatistik ve seriyi etkiler. Bir namazın dinî hükmünü değiştirmez."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Für Muslimas", "Müslimeler için")) {
                Text(settings.t(
                    "Während der Menstruation werden die in dieser Zeit nicht verrichteten Pflichtgebete nach der von Diyanet zitierten Überlieferung nicht nachgeholt. Du kannst den Tracker deshalb pausieren, ohne einen Grund in der App zu speichern.",
                    "Diyanet'in aktardığı rivayete göre âdet döneminde kılınmayan farz namazlar daha sonra kaza edilmez. Uygulamada sebep kaydetmeden takibi duraklatabilirsin."
                ))
                .font(.footnote)
                Link(settings.t("Diyanet-Quelle öffnen", "Diyanet kaynağını aç"), destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/kadinlarin-adet-veya-lohusalik-hallerinde-yapamayacaklari/0193c42d-4b21-7774-1a09-738831304296")!)
                    .font(.caption)
            }

            if paused {
                Section {
                    Label(settings.t("Heute wird beim Streak neutral behandelt.", "Bugün seri hesabında nötr sayılır."), systemImage: "checkmark.shield.fill")
                        .foregroundStyle(.green)
                }
            }
        }
        .navigationTitle(settings.t("Tracker-Pause", "Takip duraklatma"))
    }
}
'''
h = h[:m.start()] + new_streak + h[m.end():]

# Add quick actions card after Daily Deen
h = h.replace('''                dailyDeenCard
                streakCard
''','''                dailyDeenCard
                quickActionsCard
                streakCard
''',1)

needle = '''    private var streakCard: some View {
'''
quick = '''    private var quickActionsCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(settings.t("Für heute", "Bugün için"))
                .font(.headline)
            HStack(spacing: 10) {
                NavigationLink { MorningEveningAdhkarView() } label: {
                    quickAction(settings.t("Adhkar", "Ezkâr"), icon: "sun.and.horizon.fill")
                }
                .buttonStyle(.plain)
                NavigationLink { ShortSurahLearningView() } label: {
                    quickAction(settings.t("Sura lernen", "Sure öğren"), icon: "text.book.closed.fill")
                }
                .buttonStyle(.plain)
                NavigationLink { QuranicDuaLibraryView() } label: {
                    quickAction(settings.t("Dua", "Dua"), icon: "hands.sparkles.fill")
                }
                .buttonStyle(.plain)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 20))
    }

    private func quickAction(_ title: String, icon: String) -> some View {
        VStack(spacing: 7) {
            Image(systemName: icon).font(.title3)
            Text(title).font(.caption.bold()).multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 12)
        .background(Color.accentColor.opacity(0.10), in: RoundedRectangle(cornerRadius: 14))
    }

'''
if needle not in h:
    raise SystemExit('streakCard marker missing')
h = h.replace(needle, quick + needle, 1)

# Make streak card pause-aware
old = '''        let completed = PrayerTrackerStore.completedCount(on: now)
        let streak = PrayerTrackerStore.streak(upTo: now)
        return VStack(alignment: .leading, spacing: 12) {'''
new = '''        let completed = PrayerTrackerStore.completedCount(on: now)
        let streak = PrayerTrackerStore.streak(upTo: now)
        let paused = PrayerTrackerStore.isPaused(now)
        return VStack(alignment: .leading, spacing: 12) {'''
h = replace_once(h, old, new, 'streak locals')

old = '''            ProgressView(value: Double(completed), total: 5)

            HStack(spacing: 10) {'''
new = '''            if paused {
                Label(settings.t("Tracker heute pausiert", "Takip bugün duraklatıldı"), systemImage: "pause.circle.fill")
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(.secondary)
            } else {
                ProgressView(value: Double(completed), total: 5)
            }

            HStack(spacing: 10) {'''
h = replace_once(h, old, new, 'streak progress')

# disable prayer toggle if paused and visually reflect
old = '''                    Button {
                        _ = PrayerTrackerStore.toggle(kind, on: now)
                        trackerRefresh += 1
                    } label: {'''
new = '''                    Button {
                        guard !paused else { return }
                        _ = PrayerTrackerStore.toggle(kind, on: now)
                        trackerRefresh += 1
                    } label: {'''
h = replace_once(h, old, new, 'streak button')

# Hide exact coordinates from UI; privacy polish
coord = '''            if let coordinate = locationManager.location?.coordinate {
                Text(String(format: "%.5f, %.5f", coordinate.latitude, coordinate.longitude))
                    .font(.subheadline.monospacedDigit())
                    .foregroundStyle(.secondary)
            }
'''
if coord in h:
    h = h.replace(coord, '''            if locationManager.location != nil {
                Text(settings.t("GPS-Standort erkannt", "GPS konumu algılandı"))
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
''', 1)

p.write_text(h, encoding='utf-8')

# ---------------- GuideView ----------------
p = Path('SalahZeit/Views/GuideView.swift')
s = p.read_text(encoding='utf-8')

# Fix optional bug if present
s = s.replace('audioSurah?.ayahs[safe: index].audio', 'audioSurah?.ayahs[safe: index]?.audio')

# Add prayer sequence reference link in guide menu after Wudu
menu_needle = '''                NavigationLink { WuduGuideView() } label: {
                    Label(settings.t("Wudu / Gebetswaschung", "Abdest"), systemImage: "drop.fill")
                }
'''
menu_insert = menu_needle + '''                NavigationLink { PrayerSequenceReferenceView() } label: {
                    Label(settings.t("Gebetspositionen · Übersicht", "Namaz duruşları · genel bakış"), systemImage: "figure.stand.line.dotted.figure.stand")
                }
'''
if menu_needle in s and 'PrayerSequenceReferenceView()' not in s:
    s = s.replace(menu_needle, menu_insert, 1)

# Add repeat preference in short surah view
s = s.replace('''    @StateObject private var audio = RemoteAudioPlayer()
    @State private var loadingSurah: Int?
''','''    @StateObject private var audio = RemoteAudioPlayer()
    @State private var loadingSurah: Int?
    @AppStorage("surahRepeatCount") private var repeatCount = 1
''',1)

short_section = '''            Section(settings.t("Kurze Suren", "Kısa sureler")) {
'''
controls = '''            Section(settings.t("Lernmodus", "Öğrenme modu")) {
                Picker(settings.t("Wiederholen", "Tekrar"), selection: $repeatCount) {
                    Text("1×").tag(1)
                    Text("3×").tag(3)
                    Text("5×").tag(5)
                }
                .pickerStyle(.segmented)
                Text(settings.t(
                    "Fürs Auswendiglernen kann die komplette Sura automatisch mehrfach abgespielt werden.",
                    "Ezber için tüm sûre otomatik olarak birkaç kez tekrar çalınabilir."
                ))
                .font(.caption)
                .foregroundStyle(.secondary)
            }

'''
if short_section in s and 'surahRepeatCount' in s and 'Section(settings.t("Lernmodus"' not in s:
    s = s.replace(short_section, controls + short_section, 1)

s = s.replace('audio.playQueue(urls)', 'audio.playQueue(Array(repeating: urls, count: max(1, repeatCount)).flatMap { $0 })', 1)

# Add Morning/Evening Adhkar, fasting and Hijri calendar + prayer sequence before Dhikr marker
marker = '// MARK: - Dhikr\n'
if marker not in s:
    raise SystemExit('Dhikr marker missing')

addition = r'''// MARK: - Morning / evening adhkar

private struct AdhkarEntry: Identifiable {
    let id: String
    let deTitle: String
    let trTitle: String
    let arabic: String
    let transliteration: String
    let deMeaning: String
    let trMeaning: String
    let count: Int
    let source: String
}

private enum AdhkarProgressStore {
    private static func dayToken(_ date: Date) -> String {
        let f = DateFormatter(); f.calendar = .current; f.locale = Locale(identifier: "en_US_POSIX"); f.dateFormat = "yyyy-MM-dd"
        return f.string(from: date)
    }

    static func key(id: String, period: String, date: Date) -> String {
        "adhkar-\(dayToken(date))-\(period)-\(id)"
    }

    static func value(id: String, period: String, date: Date) -> Int {
        UserDefaults.standard.integer(forKey: key(id: id, period: period, date: date))
    }

    static func set(_ value: Int, id: String, period: String, date: Date) {
        UserDefaults.standard.set(value, forKey: key(id: id, period: period, date: date))
    }
}

struct MorningEveningAdhkarView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var period = 0
    @State private var refresh = 0
    private let today = Date()

    private let items: [AdhkarEntry] = [
        .init(id: "ayatkursi", deTitle: "Ayat al-Kursi", trTitle: "Âyetel Kürsî", arabic: "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ …", transliteration: "Allāhu lā ilāha illā huwa-l-Ḥayyul-Qayyūm…", deMeaning: "Quran 2:255. Für den vollständigen Text öffne die Sura al-Baqara im Quran-Bereich.", trMeaning: "Kur'an 2:255. Tam metin için Kur'an bölümünde Bakara sûresini aç.", count: 1, source: "Quran 2:255 · Hisn al-Muslim 75"),
        .init(id: "threequls", deTitle: "Al-Ikhlas, Al-Falaq, An-Nas", trTitle: "İhlâs, Felak, Nâs", arabic: "قُلْ هُوَ اللَّهُ أَحَدٌ · قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ · قُلْ أَعُوذُ بِرَبِّ النَّاسِ", transliteration: "Qul huwa-llāhu aḥad · Qul aʿūdhu bi-rabbi-l-falaq · Qul aʿūdhu bi-rabbi-n-nās", deMeaning: "Die drei kurzen Suren werden in dieser Morgen-/Abend-Überlieferung jeweils dreimal rezitiert.", trMeaning: "Bu sabah-akşam zikrinde üç kısa sûre ayrı ayrı üçer kez okunur.", count: 3, source: "Hisn al-Muslim 76"),
        .init(id: "bika", deTitle: "Allahumma bika asbahna / amsayna", trTitle: "Allahümme bike asbahnâ / emseynâ", arabic: "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ", transliteration: "Allāhumma bika aṣbaḥnā wa bika amsaynā wa bika naḥyā wa bika namūt", deMeaning: "Bitte um Allahs Beistand für Morgen/Abend, Leben und Tod; abends wird die Formulierung entsprechend angepasst.", trMeaning: "Sabah/akşam, hayat ve ölüm için Allah'a yöneliş; akşam ifadesi buna göre değiştirilir.", count: 1, source: "Hisn al-Muslim 78 · Tirmidhi"),
        .init(id: "istighfar", deTitle: "Sayyid al-Istighfar", trTitle: "Seyyidü'l-istiğfar", arabic: "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ خَلَقْتَنِي وَأَنَا عَبْدُكَ …", transliteration: "Allāhumma anta rabbī lā ilāha illā anta, khalaqtanī wa anā ʿabduk…", deMeaning: "Umfassende Bitte um Vergebung. Der vollständige Text sollte bewusst und nicht nur mechanisch gelesen werden.", trMeaning: "Kapsamlı istiğfar duasıdır. Tam metin bilinçli şekilde okunmalıdır.", count: 1, source: "Hisn al-Muslim 79 · Bukhari"),
        .init(id: "protection", deTitle: "Bismillahi alladhi la yadurru", trTitle: "Bismillâhillezî lâ yadurru", arabic: "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ", transliteration: "Bismillāhi-lladhī lā yaḍurru maʿa-smihi shay'un fi-l-arḍi wa lā fi-s-samā' wa huwa-s-Samīʿu-l-ʿAlīm", deMeaning: "Bitte um Schutz, dreimal morgens und dreimal abends überliefert.", trMeaning: "Korunma duası; sabah ve akşam üçer kez rivayet edilmiştir.", count: 3, source: "Hisn al-Muslim 86 · Abu Dawud / Tirmidhi"),
        .init(id: "raditu", deTitle: "Raditu billahi Rabban", trTitle: "Radîtü billâhi Rabben", arabic: "رَضِيتُ بِاللَّهِ رَبًّا وَبِالْإِسْلَامِ دِينًا وَبِمُحَمَّدٍ نَبِيًّا", transliteration: "Raḍītu billāhi Rabban, wa bi-l-Islāmi dīnan, wa bi-Muḥammadin nabiyyan", deMeaning: "Bekenntnis der Zufriedenheit mit Allah als Herrn, Islam als Religion und Muhammad als Propheten.", trMeaning: "Allah'ı Rab, İslâm'ı din ve Muhammed'i peygamber olarak kabul ve hoşnutluk ifadesi.", count: 3, source: "Hisn al-Muslim 87 · Ahmad / Tirmidhi")
    ]

    var body: some View {
        List {
            Section {
                Picker(settings.t("Zeit", "Vakit"), selection: $period) {
                    Text(settings.t("Morgen", "Sabah")).tag(0)
                    Text(settings.t("Abend", "Akşam")).tag(1)
                }
                .pickerStyle(.segmented)
                Text(settings.t(
                    "Die Liste ist bewusst quellenbezogen und nicht als vollständig gemeint. Überlieferte Varianten und unterschiedliche Einstufungen existieren.",
                    "Liste kaynak gösterilerek hazırlanmıştır ve eksiksiz olduğu iddia edilmez. Rivayetlerde farklılıklar ve farklı değerlendirmeler bulunabilir."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            ForEach(items) { item in
                let current = progress(item)
                Section {
                    VStack(alignment: .leading, spacing: 9) {
                        HStack {
                            VStack(alignment: .leading, spacing: 3) {
                                Text(settings.language == .german ? item.deTitle : item.trTitle).font(.headline)
                                Text(item.source).font(.caption2).foregroundStyle(.tertiary)
                            }
                            Spacer()
                            Text("\(current)/\(item.count)").font(.subheadline.bold().monospacedDigit())
                        }
                        Text(item.arabic).font(.title3).frame(maxWidth: .infinity, alignment: .trailing).multilineTextAlignment(.trailing)
                        Text(item.transliteration).font(.subheadline.weight(.semibold))
                        Text(settings.language == .german ? item.deMeaning : item.trMeaning).font(.footnote).foregroundStyle(.secondary)
                        ProgressView(value: Double(current), total: Double(item.count))
                        HStack {
                            Button(settings.t("Reset", "Sıfırla")) { setProgress(0, item) }.buttonStyle(.bordered)
                            Spacer()
                            Button(current >= item.count ? settings.t("Erledigt", "Tamam") : "+1") {
                                if current < item.count { setProgress(current + 1, item) }
                            }
                            .buttonStyle(.borderedProminent)
                            .disabled(current >= item.count)
                        }
                    }
                    .padding(.vertical, 4)
                }
            }
        }
        .navigationTitle(settings.t("Morgen & Abend Adhkar", "Sabah & Akşam Ezkârı"))
    }

    private var periodKey: String { period == 0 ? "morning" : "evening" }
    private func progress(_ item: AdhkarEntry) -> Int { AdhkarProgressStore.value(id: item.id, period: periodKey, date: today) }
    private func setProgress(_ value: Int, _ item: AdhkarEntry) { AdhkarProgressStore.set(value, id: item.id, period: periodKey, date: today); refresh += 1 }
}

// MARK: - Fasting tracker

private enum FastingStore {
    private static let key = "fastingDays"
    static func token(_ date: Date) -> String {
        let f = DateFormatter(); f.calendar = .current; f.locale = Locale(identifier: "en_US_POSIX"); f.dateFormat = "yyyy-MM-dd"
        return f.string(from: date)
    }
    static func tokens() -> Set<String> { Set(UserDefaults.standard.stringArray(forKey: key) ?? []) }
    static func contains(_ date: Date) -> Bool { tokens().contains(token(date)) }
    static func toggle(_ date: Date) {
        var set = tokens(); let t = token(date)
        if set.contains(t) { set.remove(t) } else { set.insert(t) }
        UserDefaults.standard.set(Array(set).sorted(), forKey: key)
    }
}

struct FastingTrackerView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var refresh = 0
    private let calendar = Calendar.current

    var body: some View {
        List {
            Section {
                Toggle(isOn: Binding(get: { FastingStore.contains(Date()) }, set: { _ in FastingStore.toggle(Date()); refresh += 1 })) {
                    Label(settings.t("Heute als Fastentag markieren", "Bugünü oruç günü olarak işaretle"), systemImage: "moon.fill")
                }
                Text(settings.t(
                    "Der Tracker ist nur eine private lokale Liste. Er entscheidet nicht, ob ein Fasten religiös gültig oder verpflichtend ist.",
                    "Bu takip yalnızca cihazdaki özel bir listedir. Orucun dinen geçerli veya zorunlu olup olmadığına karar vermez."
                ))
                .font(.footnote).foregroundStyle(.secondary)
            }

            Section(settings.t("Letzte 14 Tage", "Son 14 gün")) {
                ForEach(lastDays, id: \.self) { day in
                    Button {
                        FastingStore.toggle(day); refresh += 1
                    } label: {
                        HStack {
                            VStack(alignment: .leading) {
                                Text(gregorianDateString(day, language: settings.language))
                                Text(hijriDateString(day, language: settings.language)).font(.caption).foregroundStyle(.secondary)
                            }
                            Spacer()
                            Image(systemName: FastingStore.contains(day) ? "checkmark.circle.fill" : "circle")
                                .foregroundStyle(FastingStore.contains(day) ? .green : .secondary)
                        }
                    }
                    .buttonStyle(.plain)
                }
            }
        }
        .navigationTitle(settings.t("Fasten-Tracker", "Oruç takibi"))
    }

    private var lastDays: [Date] {
        (0..<14).compactMap { calendar.date(byAdding: .day, value: -$0, to: calendar.startOfDay(for: Date())) }
    }
}

// MARK: - Hijri calendar

struct HijriCalendarView: View {
    @EnvironmentObject private var settings: SettingsStore
    private let calendar = Calendar.current
    private let hijri = Calendar(identifier: .islamicUmmAlQura)

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Umm-al-Qura ist ein berechneter Kalender. Tatsächliche Monatsanfänge können je nach regionaler Mondsichtung abweichen.",
                    "Ummü'l-Kurâ hesaplanmış bir takvimdir. Gerçek ay başlangıçları bölgesel hilal gözlemine göre değişebilir."
                ))
                .font(.footnote).foregroundStyle(.secondary)
            }
            Section(settings.t("Nächste Tage", "Yaklaşan günler")) {
                ForEach(days, id: \.self) { date in
                    HStack {
                        VStack(alignment: .leading, spacing: 3) {
                            Text(gregorianDateString(date, language: settings.language)).font(.subheadline)
                            Text(hijriDateString(date, language: settings.language)).font(.headline)
                            if let event = eventName(date) {
                                Label(event, systemImage: "sparkles").font(.caption).foregroundStyle(.secondary)
                            }
                        }
                        Spacer()
                        if calendar.isDateInToday(date) { Text(settings.t("Heute", "Bugün")).font(.caption.bold()).foregroundStyle(.tint) }
                    }
                }
            }
        }
        .navigationTitle(settings.t("Hicri-Kalender", "Hicrî takvim"))
    }

    private var days: [Date] {
        (-7...30).compactMap { calendar.date(byAdding: .day, value: $0, to: calendar.startOfDay(for: Date())) }
    }

    private func eventName(_ date: Date) -> String? {
        let m = hijri.component(.month, from: date)
        let d = hijri.component(.day, from: date)
        if m == 9 && d == 1 { return settings.t("Berechneter Beginn Ramadan", "Hesaplanan Ramazan başlangıcı") }
        if m == 10 && d == 1 { return settings.t("Berechnetes Eid al-Fitr", "Hesaplanan Ramazan Bayramı") }
        if m == 12 && d == 9 { return settings.t("Arafat-Tag (berechnet)", "Arefe günü (hesaplanan)") }
        if m == 12 && d == 10 { return settings.t("Eid al-Adha (berechnet)", "Kurban Bayramı (hesaplanan)") }
        if m == 1 && d == 10 { return settings.t("ʿAshura (berechnet)", "Aşure günü (hesaplanan)") }
        return nil
    }
}

// MARK: - Prayer position reference

struct PrayerSequenceReferenceView: View {
    @EnvironmentObject private var settings: SettingsStore
    private let imageURL = URL(string: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Salat_or_Muslim_Prayers_-_Illustration_showing_the_sequence_and_recitations_made_in_each_posture.jpg?width=1280")!
    private let sourceURL = URL(string: "https://commons.wikimedia.org/wiki/File:Salat_or_Muslim_Prayers_-_Illustration_showing_the_sequence_and_recitations_made_in_each_posture.jpg")!

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text(settings.t(
                    "Diese CC0-Grafik zeigt die Grundabfolge einer Rakʿah. Sie ist eine allgemeine Übersicht, nicht eine vollständige Darstellung aller madhhab-spezifischen Männer-/Frauenunterschiede.",
                    "Bu CC0 görseli bir rekâtın temel akışını gösterir. Tüm mezhep ve kadın/erkek farklılıklarını eksiksiz temsil eden bir şema değildir."
                ))
                .font(.footnote).foregroundStyle(.secondary)

                AsyncImage(url: imageURL) { phase in
                    switch phase {
                    case .success(let image): image.resizable().scaledToFit()
                    case .failure: ContentUnavailableView(settings.t("Bild konnte nicht geladen werden", "Görsel yüklenemedi"), systemImage: "photo")
                    default: ProgressView().frame(maxWidth: .infinity, minHeight: 220)
                    }
                }
                .clipShape(RoundedRectangle(cornerRadius: 18))

                Link("Wikimedia Commons · CC0", destination: sourceURL)
                    .font(.caption)

                Text(settings.t(
                    "Für die praktische Anleitung verwende weiterhin den Männer-/Frauen-Umschalter in 'Gebet lernen'. Dort sind hanafitische Unterschiede ausdrücklich als solche markiert.",
                    "Uygulamalı anlatım için 'Namazı öğren' bölümündeki erkek/kadın seçimini kullan. Hanefî farklılıklar orada açıkça belirtilir."
                ))
                .font(.subheadline)
            }
            .padding()
        }
        .navigationTitle(settings.t("Gebetspositionen", "Namaz duruşları"))
    }
}

'''
if 'struct MorningEveningAdhkarView' not in s:
    s = s.replace(marker, addition + marker, 1)

p.write_text(s, encoding='utf-8')

# ---------------- RootTabView ----------------
p = Path('SalahZeit/Views/RootTabView.swift')
r = p.read_text(encoding='utf-8')

# Add hubs to More
needle = '''                NavigationLink { QiblaView() } label: {
                    Label(settings.t("Qibla-Kompass", "Kıble Pusulası"), systemImage: "location.north.circle")
                }
'''
extra = needle + '''                NavigationLink { MorningEveningAdhkarView() } label: {
                    Label(settings.t("Morgen & Abend Adhkar", "Sabah & Akşam Ezkârı"), systemImage: "sun.and.horizon.fill")
                }
                NavigationLink { FastingTrackerView() } label: {
                    Label(settings.t("Fasten-Tracker", "Oruç takibi"), systemImage: "moon.fill")
                }
                NavigationLink { HijriCalendarView() } label: {
                    Label(settings.t("Hicri-Kalender", "Hicrî takvim"), systemImage: "calendar")
                }
                NavigationLink { TrackerPauseView() } label: {
                    Label(settings.t("Tracker-Pause", "Takip duraklatma"), systemImage: "pause.circle")
                }
'''
if needle in r and 'MorningEveningAdhkarView()' not in r:
    r = r.replace(needle, extra, 1)

# Add positions link after prayer dua or before settings
needle2 = '''                NavigationLink { QuranicDuaLibraryView() } label: {
                    Label(settings.t("Dua-Sammlung", "Dua koleksiyonu"), systemImage: "heart.text.square")
                }
'''
extra2 = needle2 + '''                NavigationLink { PrayerSequenceReferenceView() } label: {
                    Label(settings.t("Gebetspositionen", "Namaz duruşları"), systemImage: "figure.stand")
                }
'''
if needle2 in r and 'PrayerSequenceReferenceView()' not in r:
    r = r.replace(needle2, extra2, 1)

r = r.replace(
    'Gebetszeiten, kompletter Fard/Sunnah/Witr-Plan, Gebets-Tracker, Daily Deen, Quran, Suren-Audio, Duas, Dhikr, Wudu, Lernen und Qibla in einer App.',
    'Gebetszeiten, Fard/Sunnah/Witr-Plan, Gebets- und Fasten-Tracker, Daily Deen, Morgen-/Abend-Adhkar, Quran, Lern-Audio, Duas, Wudu, Hicri-Kalender und Qibla in einer App.'
)
r = r.replace(
    "Namaz vakitleri, tam farz/sünnet/vitir planı, namaz takibi, Günlük Deen, Kur'an, sure sesleri, dualar, zikir, abdest, öğrenme ve kıble tek uygulamada.",
    "Namaz vakitleri, farz/sünnet/vitir planı, namaz ve oruç takibi, Günlük Deen, sabah-akşam ezkârı, Kur'an, öğrenme sesleri, dualar, abdest, Hicrî takvim ve kıble tek uygulamada."
)

p.write_text(r, encoding='utf-8')

# ---------------- Settings ----------------
p = Path('SalahZeit/Views/SettingsView.swift')
sett = p.read_text(encoding='utf-8')
sett = sett.replace('LabeledContent(settings.t("Version", "Sürüm"), value: "3.1")', 'LabeledContent(settings.t("Version", "Sürüm"), value: "3.4")')
sett = sett.replace('''                    "Die Quran-Rezitation wird als menschliche Aufnahme über den Islamic Network CDN gestreamt.",
                    "Kur'an tilaveti Islamic Network CDN üzerinden gerçek insan kaydı olarak yayınlanır."
''','''                    "Die Quran-Rezitation ist eine menschliche Aufnahme. Die Audio-URLs werden über die AlQuran.cloud/Islamic-Network-API aufgelöst.",
                    "Kur'an tilaveti gerçek insan kaydıdır. Ses bağlantıları AlQuran.cloud/Islamic Network API üzerinden çözülür."
''')
p.write_text(sett, encoding='utf-8')

# ---------------- build version ----------------
p = Path('scripts/build_unsigned_ipa.sh')
b = p.read_text(encoding='utf-8')
b = b.replace('MARKETING_VERSION="3.3"', 'MARKETING_VERSION="3.4"')
b = b.replace('CURRENT_PROJECT_VERSION="6"', 'CURRENT_PROJECT_VERSION="7"')
p.write_text(b, encoding='utf-8')

print('SalahPath v3.4 patch applied')