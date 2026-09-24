import SwiftUI
import CoreLocation
import UIKit


extension Notification.Name {
    static let prayerTrackerDidChange = Notification.Name("salahpath.prayerTrackerDidChange")
}

enum PrayerTrackerStore {
    private static let prefix = "prayerTracker-"

    static let requiredKinds: [PrayerKind] = [.fajr, .dhuhr, .asr, .maghrib, .isha]

    private static func localDayToken(for date: Date) -> String {
        LocalDay.token(for: date)
    }

    private static func key(for date: Date) -> String {
        prefix + localDayToken(for: date)
    }

    static func completedKinds(for date: Date) -> Set<String> {
        let allowed = Set(requiredKinds.map(\.rawValue))
        let stored = Set(UserDefaults.standard.stringArray(forKey: key(for: date)) ?? [])
        return stored.intersection(allowed)
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
        NotificationCenter.default.post(name: .prayerTrackerDidChange, object: nil)
        return inserted
    }

    private static let pausePrefix = "prayerTrackerPause-"

    private static func pauseKey(for date: Date) -> String {
        pausePrefix + localDayToken(for: date)
    }

    static func isPaused(_ date: Date) -> Bool {
        UserDefaults.standard.bool(forKey: pauseKey(for: date))
    }

    static func togglePause(_ date: Date) {
        UserDefaults.standard.set(!isPaused(date), forKey: pauseKey(for: date))
        NotificationCenter.default.post(name: .prayerTrackerDidChange, object: nil)
    }

    static func completedCount(on date: Date) -> Int {
        requiredKinds.filter { isCompleted($0, on: date) }.count
    }

    static func streak(upTo date: Date) -> Int {
        let calendar = LocalDay.calendar()
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

struct PrayerTrackerOverviewView: View {
    @EnvironmentObject private var settings: SettingsStore
    @Environment(\.scenePhase) private var scenePhase
    @State private var refresh = 0
    @State private var now = Date()
    @State private var selectedDate = Date()

    private var calendar: Calendar { LocalDay.calendar() }

    private var today: Date {
        calendar.startOfDay(for: now)
    }

    private var selectedDay: Date {
        calendar.startOfDay(for: selectedDate)
    }

    private var isTodaySelected: Bool {
        calendar.isDate(selectedDay, inSameDayAs: today)
    }

    private var displayedWeekDays: [Date] {
        let weekday = calendar.component(.weekday, from: selectedDay)
        let firstWeekday = calendar.firstWeekday
        let delta = (weekday - firstWeekday + 7) % 7
        guard let weekStart = LocalDay.addingDays(-delta, to: selectedDay) else {
            return [selectedDay]
        }
        return (0..<7).compactMap { LocalDay.addingDays($0, to: weekStart) }
    }

    var body: some View {
        let _ = refresh
        let completed = PrayerTrackerStore.completedCount(on: selectedDay)
        let streak = PrayerTrackerStore.streak(upTo: selectedDay)

        List {
            Section {
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Button {
                            moveSelection(by: -1)
                        } label: {
                            Image(systemName: "chevron.left")
                                .frame(width: 30, height: 30)
                        }
                        .buttonStyle(.borderless)
                        .accessibilityLabel(settings.t("Vorheriger Tag", "Önceki gün"))

                        Spacer()

                        VStack(spacing: 2) {
                            Text(dayTitle(selectedDay))
                                .font(.headline)
                                .foregroundStyle(SalahTheme.ink)
                            Text(hijriDateString(selectedDay, language: settings.language))
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        .multilineTextAlignment(.center)

                        Spacer()

                        Button {
                            moveSelection(by: 1)
                        } label: {
                            Image(systemName: "chevron.right")
                                .frame(width: 30, height: 30)
                        }
                        .buttonStyle(.borderless)
                        .disabled(isTodaySelected)
                        .opacity(isTodaySelected ? 0.30 : 1)
                        .accessibilityLabel(settings.t("Nächster Tag", "Sonraki gün"))
                    }

                    HStack(spacing: 6) {
                        ForEach(displayedWeekDays, id: \.self) { date in
                            Button {
                                selectedDate = date
                            } label: {
                                VStack(spacing: 4) {
                                    Text(shortTrackerWeekday(date))
                                        .font(.caption2.bold())

                                    ZStack {
                                        Circle()
                                            .stroke(
                                                calendar.isDate(date, inSameDayAs: selectedDay)
                                                    ? SalahTheme.gold
                                                    : SalahTheme.teal.opacity(0.28),
                                                lineWidth: calendar.isDate(date, inSameDayAs: selectedDay) ? 2.5 : 1
                                            )
                                            .frame(width: 32, height: 32)

                                        let count = PrayerTrackerStore.completedCount(on: date)
                                        let paused = PrayerTrackerStore.isPaused(date)

                                        if count == PrayerTrackerStore.requiredKinds.count {
                                            Circle()
                                                .fill(SalahTheme.teal)
                                                .frame(width: 28, height: 28)
                                            Image(systemName: "checkmark")
                                                .font(.caption2.bold())
                                                .foregroundStyle(.white)
                                        } else if paused {
                                            Image(systemName: "pause.fill")
                                                .font(.caption2.bold())
                                                .foregroundStyle(SalahTheme.mutedInk)
                                        } else {
                                            Text("\(count)")
                                                .font(.caption2.bold().monospacedDigit())
                                                .foregroundStyle(SalahTheme.deepTeal)
                                        }
                                    }
                                }
                                .frame(maxWidth: .infinity)
                                .foregroundStyle(SalahTheme.ink)
                                .contentShape(Rectangle())
                            }
                            .buttonStyle(.plain)
                            .accessibilityLabel(trackerDayAccessibility(date))
                        }
                    }
                }
                .padding(.vertical, 4)
            }

            Section {
                HStack {
                    Label(
                        isTodaySelected
                            ? settings.t("Heute", "Bugün")
                            : settings.t("Ausgewählter Tag", "Seçili gün"),
                        systemImage: "checkmark.circle.fill"
                    )
                    Spacer()
                    Text("\(completed)/\(PrayerTrackerStore.requiredKinds.count)")
                        .font(.headline.monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
                }

                HStack {
                    Label(settings.t("Serie", "Seri"), systemImage: "flame.fill")
                    Spacer()
                    Text("\(streak) \(settings.t("Tage", "gün"))")
                        .font(.headline.monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
                }
            }

            Section(
                isTodaySelected
                    ? settings.t("Heutige Gebete", "Bugünkü namazlar")
                    : settings.t("Gebete an diesem Tag", "Bu gündeki namazlar")
            ) {
                ForEach(PrayerTrackerStore.requiredKinds, id: \.id) { kind in
                    let done = PrayerTrackerStore.isCompleted(kind, on: selectedDay)
                    Button {
                        _ = PrayerTrackerStore.toggle(kind, on: selectedDay)
                        refresh &+= 1
                    } label: {
                        HStack {
                            Text(kind.localizedName(settings.language))
                                .foregroundStyle(SalahTheme.ink)
                            Spacer()
                            Image(systemName: done ? "checkmark.circle.fill" : "circle")
                                .foregroundStyle(done ? SalahTheme.teal : .secondary)
                        }
                        .contentShape(Rectangle())
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(
                        settings.t(
                            "\(kind.localizedName(settings.language)), \(done ? "erledigt" : "offen")",
                            settings.t(
                            "\(kind.localizedName(settings.language)), \(done ? "markiert" : "offen")",
                            "\(kind.localizedName(settings.language)), \(done ? "tamamlandı" : "açık")"
                        )
                        )
                    )
                }
            }

            Section(settings.t("Tracker", "Takip")) {
                Toggle(isOn: Binding(
                    get: { PrayerTrackerStore.isPaused(selectedDay) },
                    set: { newValue in
                        if PrayerTrackerStore.isPaused(selectedDay) != newValue {
                            PrayerTrackerStore.togglePause(selectedDay)
                        }
                        refresh &+= 1
                    }
                )) {
                    Label(
                        isTodaySelected
                            ? settings.t("Tracker heute pausieren", "Bugün takibi duraklat")
                            : settings.t("Diesen Tag pausieren", "Bu günü duraklat"),
                        systemImage: "pause.circle"
                    )
                }

                Text(settings.t(
                    "Die Pause verändert nur Statistik und Streak. Sie ändert keine religiöse Pflicht. Markierungen bleiben lokal auf diesem Gerät gespeichert.",
                    "Duraklatma yalnızca istatistik ve seriyi etkiler; dinî yükümlülüğü değiştirmez. İşaretlemeler yalnızca bu cihazda yerel olarak saklanır."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Gebets-Tracking", "Namaz Takibi"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
        .onAppear {
            now = Date()
            clampSelectionToToday()
        }
        .onChange(of: scenePhase) { _, phase in
            if phase == .active {
                now = Date()
                clampSelectionToToday()
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
            now = Date()
            clampSelectionToToday()
        }
        .onReceive(NotificationCenter.default.publisher(for: .prayerTrackerDidChange)) { _ in
            refresh &+= 1
            now = Date()
            clampSelectionToToday()
        }
    }

    private func moveSelection(by days: Int) {
        guard let candidate = LocalDay.addingDays(days, to: selectedDay) else { return }
        if candidate > today {
            selectedDate = today
        } else {
            selectedDate = candidate
        }
    }

    private func clampSelectionToToday() {
        if selectedDay > today {
            selectedDate = today
        }
    }

    private func dayTitle(_ date: Date) -> String {
        if calendar.isDate(date, inSameDayAs: today) {
            return settings.t("Heute", "Bugün")
        }
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        formatter.timeZone = .autoupdatingCurrent
        formatter.dateFormat = "EEE, d. MMM"
        return formatter.string(from: date)
    }

    private func shortTrackerWeekday(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        formatter.timeZone = .autoupdatingCurrent
        formatter.dateFormat = "EE"
        return formatter.string(from: date)
    }

    private func trackerDayAccessibility(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        formatter.timeZone = .autoupdatingCurrent
        formatter.dateStyle = .medium
        let count = PrayerTrackerStore.completedCount(on: date)
        let paused = PrayerTrackerStore.isPaused(date)
        let state = paused
            ? settings.t("pausiert", "duraklatıldı")
            : settings.t("\(count) von 5 Gebeten markiert", "5 namazdan \(count) tanesi işaretli")
        return "\(formatter.string(from: date)), \(state)"
    }
}

struct TrackerPauseView: View {
    @EnvironmentObject private var settings: SettingsStore
    @Environment(\.scenePhase) private var scenePhase
    @State private var refresh = 0
    @State private var now = Date()

    var body: some View {
        let _ = refresh
        let today = now
        let paused = PrayerTrackerStore.isPaused(today)
        List {
            Section {
                Toggle(isOn: Binding(
                    get: { PrayerTrackerStore.isPaused(today) },
                    set: { _ in PrayerTrackerStore.togglePause(today); refresh &+= 1 }
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

            Section(settings.t("Für Musliminnen", "Müslüman kadınlar için")) {
                Text(settings.t(
                    "Während der Menstruation werden die in dieser Zeit nicht verrichteten Pflichtgebete nach der von Diyanet zitierten Überlieferung nicht nachgeholt. Du kannst den Tracker deshalb pausieren, ohne einen Grund in der App zu speichern.",
                    "Diyanet'in aktardığı rivayete göre âdet döneminde kılınmayan farz namazlar daha sonra kaza edilmez. Uygulamada sebep kaydetmeden takibi duraklatabilirsin."
                ))
                .font(.footnote)
                Text(settings.t("Quelle: Diyanet Din İşleri Yüksek Kurulu.", "Kaynak: Diyanet Din İşleri Yüksek Kurulu."))
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            if paused {
                Section {
                    Label(settings.t("Heute wird beim Streak neutral behandelt.", "Bugün seri hesabında nötr sayılır."), systemImage: "checkmark.shield.fill")
                        .foregroundStyle(.green)
                }
            }
        }
        .navigationTitle(settings.t("Tracker-Pause", "Takip duraklatma"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            now = Date()
        }
        .onChange(of: scenePhase) { _, phase in
            if phase == .active {
                now = Date()
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
            now = Date()
        }
        .onReceive(NotificationCenter.default.publisher(for: .prayerTrackerDidChange)) { _ in
            refresh &+= 1
            now = Date()
        }
    }
}


private enum DailyDeenStore {
    static func dayKey(_ date: Date) -> String {
        "dailyDeen-" + LocalDay.token(for: date)
    }
    static func values(_ date: Date) -> Set<String> { Set(UserDefaults.standard.stringArray(forKey: dayKey(date)) ?? []) }
    static func isDone(_ id: String, _ date: Date) -> Bool { values(date).contains(id) }
    static func toggle(_ id: String, _ date: Date) {
        var set = values(date)
        if set.contains(id) { set.remove(id) } else { set.insert(id) }
        UserDefaults.standard.set(Array(set), forKey: dayKey(date))
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
    let source: String
}

private enum DailyDuaStore {
    static let items: [DailyDuaEntry] = [
        .init(deTitle: "Rabbana atina", trTitle: "Rabbenâ âtinâ", arabic: "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", transliteration: "Rabbanā ātinā fi-d-dunyā ḥasanah wa fi-l-ākhirati ḥasanah wa qinā ʿadhāba-n-nār", deMeaning: "Unser Herr, gib uns Gutes im Diesseits und Gutes im Jenseits und bewahre uns vor der Strafe des Feuers.", trMeaning: "Rabbimiz, bize dünyada da iyilik ver, ahirette de iyilik ver ve bizi ateş azabından koru.", repetition: nil, source: "Quran 2:201"),
        .init(deTitle: "Rabbi zidni ilma", trTitle: "Rabbî zidnî ilmâ", arabic: "رَبِّ زِدْنِي عِلْمًا", transliteration: "Rabbi zidnī ʿilmā", deMeaning: "Mein Herr, mehre mein Wissen.", trMeaning: "Rabbim, ilmimi artır.", repetition: nil, source: "Quran 20:114 · excerpt"),
        .init(deTitle: "Hasbunallahu", trTitle: "Hasbünallahu", arabic: "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ", transliteration: "Ḥasbunallāhu wa niʿma-l-wakīl", deMeaning: "Allah genügt uns, und Er ist der beste Sachwalter.", trMeaning: "Allah bize yeter, O ne güzel vekildir.", repetition: nil, source: "Quran 3:173 · excerpt"),
        .init(
            deTitle: "Sayyidul Istighfar",
            trTitle: "Seyyidü'l-istiğfar",
            arabic: "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلٰهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ لَكَ بِذَنْبِي فَاغْفِرْ لِي، فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ",
            transliteration: "Allāhumma anta rabbī lā ilāha illā anta, khalaqtanī wa anā ʿabduka, wa anā ʿalā ʿahdika wa waʿdika ma-staṭaʿtu, aʿūdhu bika min sharri mā ṣanaʿtu, abūʾu laka biniʿmatika ʿalayya, wa abūʾu laka bidhanbī, faghfir lī, fa-innahu lā yaghfiru-dh-dhunūba illā anta.",
            deMeaning: "O Allah, Du bist mein Herr. Du hast mich erschaffen und ich bin Dein Diener. Soweit ich kann, halte ich an meinem Bund mit Dir fest. Ich suche Schutz bei Dir vor dem Schlechten meiner Taten, erkenne Deine Gaben und meine Fehler an und bitte Dich um Vergebung; nur Du vergibst die Sünden.",
            trMeaning: "Allah'ım, Sen benim Rabbimsin. Beni Sen yarattın, ben Senin kulunum. Gücüm yettiğince ahdine bağlı kalırım. Yaptıklarımın şerrinden Sana sığınır, nimetlerini ve günahımı itiraf ederim. Beni bağışla; günahları ancak Sen bağışlarsın.",
            repetition: "Morgens / Sabah · Abends / Akşam",
            source: "Diyanet · Buhârî 6306"
        )
    ]

    static func item(for date: Date) -> DailyDuaEntry {
        let day = LocalDay.ordinal(for: date)
        return items[(day - 1) % items.count]
    }
}


private struct DailyDuaDetailView: View {
    @EnvironmentObject private var settings: SettingsStore
    let dua: DailyDuaEntry

    var body: some View {
        ScrollView {
            VStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 5) {
                    Text(settings.language == .german ? dua.deTitle : dua.trTitle)
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    if let repetition = dua.repetition {
                        Label(repetition, systemImage: "repeat")
                            .font(.caption.bold())
                            .foregroundStyle(SalahTheme.teal)
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(SalahTheme.cream.opacity(0.94), in: RoundedRectangle(cornerRadius: 20, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .stroke(SalahTheme.cardStroke(), lineWidth: 1)
                }

                VStack(spacing: 12) {
                    Text(dua.arabic)
                        .font(.system(size: 26, weight: .regular))
                        .frame(maxWidth: .infinity, alignment: .trailing)
                        .multilineTextAlignment(.trailing)
                        .textSelection(.enabled)

                    Divider().opacity(0.3)

                    Text(dua.transliteration)
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(SalahTheme.ink)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .textSelection(.enabled)

                    Text(settings.language == .german ? dua.deMeaning : dua.trMeaning)
                        .font(.body)
                        .foregroundStyle(SalahTheme.ink)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 20, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .stroke(SalahTheme.cardStroke(), lineWidth: 1)
                }

                Label(dua.source, systemImage: "checkmark.seal.fill")
                    .font(.footnote)
                    .foregroundStyle(SalahTheme.mutedInk)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.horizontal, 2)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Dua des Tages", "Günün Duası"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

enum SalahTheme {
    // The navigation/header tone remains brand-stable; content colors adapt to iOS appearance.
    static let navigationTeal = Color(red: 36/255, green: 79/255, blue: 77/255)

    static let teal = adaptive(
        light: UIColor(red: 43/255, green: 86/255, blue: 82/255, alpha: 1),
        dark: UIColor(red: 91/255, green: 188/255, blue: 174/255, alpha: 1)
    )
    static let deepTeal = adaptive(
        light: UIColor(red: 36/255, green: 79/255, blue: 77/255, alpha: 1),
        dark: UIColor(red: 116/255, green: 207/255, blue: 192/255, alpha: 1)
    )
    static let gold = adaptive(
        light: UIColor(red: 234/255, green: 185/255, blue: 80/255, alpha: 1),
        dark: UIColor(red: 244/255, green: 200/255, blue: 103/255, alpha: 1)
    )
    static let cream = adaptive(
        light: UIColor(red: 250/255, green: 250/255, blue: 241/255, alpha: 1),
        dark: UIColor(red: 28/255, green: 34/255, blue: 32/255, alpha: 1)
    )
    static let page = adaptive(
        light: UIColor(red: 235/255, green: 232/255, blue: 216/255, alpha: 1),
        dark: UIColor(red: 14/255, green: 20/255, blue: 19/255, alpha: 1)
    )
    static let ink = adaptive(
        light: UIColor(red: 15/255, green: 39/255, blue: 50/255, alpha: 1),
        dark: UIColor(red: 239/255, green: 244/255, blue: 240/255, alpha: 1)
    )
    static let mutedInk = adaptive(
        light: UIColor(red: 82/255, green: 103/255, blue: 101/255, alpha: 1),
        dark: UIColor(red: 170/255, green: 187/255, blue: 183/255, alpha: 1)
    )
    static let softTeal = adaptive(
        light: UIColor(red: 230/255, green: 238/255, blue: 232/255, alpha: 1),
        dark: UIColor(red: 34/255, green: 58/255, blue: 54/255, alpha: 1)
    )

    static func cardStroke(_ opacity: Double = 0.34) -> Color { gold.opacity(opacity) }

    private static func adaptive(light: UIColor, dark: UIColor) -> Color {
        Color(UIColor { traits in
            traits.userInterfaceStyle == .dark ? dark : light
        })
    }
}

struct HomeView: View {
    @EnvironmentObject private var locationManager: LocationManager
    @EnvironmentObject private var settings: SettingsStore
    @Environment(\.scenePhase) private var scenePhase

    @State private var now = Date()
    @State private var clockTask: Task<Void, Never>?
    @State private var selectedPrayer: PrayerOccurrence?
    @State private var trackerRefresh = 0
    @State private var dailyDeenRefresh = 0
    @State private var manualLocationText = ""
    @State private var manualLocationError: String?
    @State private var isResolvingManualLocation = false
    private let engine = PrayerEngine()

    private var isScreenshotQA: Bool {
        ProcessInfo.processInfo.environment["SALAH_QA_SCREENSHOT"] == "1"
    }

    private var effectiveLocation: CLLocation? {
        if let live = locationManager.location { return live }
        if isScreenshotQA {
            return CLLocation(latitude: 41.0082, longitude: 28.9784)
        }
        return nil
    }

    private var effectiveLocality: String {
        if isScreenshotQA { return "İstanbul" }
        return locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum")
    }

    private var effectiveNow: Date {
        now
    }

    var body: some View {
        ZStack(alignment: .top) {
            SalahTheme.navigationTeal.ignoresSafeArea()
            SalahTheme.navigationTeal
                .frame(height: 76)
                .ignoresSafeArea(edges: .top)

            Group {
                if let location = effectiveLocation,
                   let today = engine.calculateDay(for: now, location: location, settings: settings) {
                    prayerContent(location: location, today: today)
                } else {
                    locationState
                }
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar(.hidden, for: .navigationBar)
        .onAppear {
            if !isScreenshotQA {
                if locationManager.authorizationStatus == .authorizedWhenInUse ||
                    locationManager.authorizationStatus == .authorizedAlways {
                    locationManager.requestAccessAndStart()
                }
                startClock()
            }
        }
        .onDisappear {
            stopClock()
        }
        .onChange(of: scenePhase) { _, phase in
            guard !isScreenshotQA else { return }
            if phase == .active {
                startClock()
            } else {
                stopClock()
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
            now = Date()
        }
        .onReceive(NotificationCenter.default.publisher(for: .prayerTrackerDidChange)) { _ in
            trackerRefresh &+= 1
            now = Date()
        }
        .sheet(item: $selectedPrayer) { prayer in
            if let location = effectiveLocation,
               let today = engine.calculateDay(for: prayer.date, location: location, settings: settings),
               let tomorrowDate = Calendar.current.date(byAdding: .day, value: 1, to: prayer.date),
               let tomorrow = engine.calculateDay(for: tomorrowDate, location: location, settings: settings) {
                PrayerDetailView(prayer: prayer, day: today, nextDay: tomorrow)
                    .environmentObject(settings)
            }
        }
    }

    private func startClock() {
        clockTask?.cancel()
        now = Date()

        clockTask = Task { @MainActor in
            while !Task.isCancelled {
                do {
                    try await Task.sleep(for: .seconds(1))
                } catch {
                    break
                }
                guard !Task.isCancelled else { break }
                now = Date()
            }
        }
    }

    private func stopClock() {
        clockTask?.cancel()
        clockTask = nil
    }

    @ViewBuilder
    private func prayerContent(location: CLLocation, today: PrayerDay) -> some View {
        ScrollView {
            LazyVStack(spacing: 5) {
                brandHeader

                if let next = engine.nextPrayer(now: now, location: location, settings: settings) {
                    nextPrayerHero(next)
                }

                todayPrayersCard(today, location: location)

                quickActionStrip

                dailyDuaCard
                NavigationLink { PrayerTrackerOverviewView() } label: { streakCard }
                    .buttonStyle(.plain)
                    .accessibilityHint(settings.t("Gebets-Tracking öffnen", "Namaz takibini aç"))
                dashboardGrid
                referenceQuoteStrip
            }
            .padding(.horizontal, 7)
            .padding(.top, 3)
            .padding(.bottom, 4)
        }
        .scrollIndicators(.hidden)
        .refreshable {
            locationManager.refresh()
            if settings.notificationsEnabled {
                await NotificationManager.shared.scheduleNextSevenDays(location: location, settings: settings)
            }
        }
    }

    private var brandHeader: some View {
        HStack(spacing: 9) {
            Image("salahpath_logo")
                .resizable()
                .scaledToFit()
                .frame(width: 37, height: 44)
                .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: 1) {
                Text("SalahPath")
                    .font(.system(size: 21, weight: .bold, design: .serif))
                    .foregroundStyle(.white)
                    .lineLimit(1)
                Text(settings.t("Ein schöneres Leben mit Gebet", "İbadetle Daha Güzel Bir Hayat"))
                    .font(.system(size: 8.8, weight: .semibold))
                    .foregroundStyle(.white.opacity(0.78))
                    .lineLimit(1)
            }

            Spacer(minLength: 5)

            VStack(alignment: .trailing, spacing: 2) {
                Text(settings.t("„Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.“", "„Şüphesiz namaz, müminlere vakitleri belli bir farzdır.“"))
                    .font(.system(size: 7.7, weight: .medium, design: .serif))
                    .italic()
                    .foregroundStyle(.white.opacity(0.90))
                    .multilineTextAlignment(.trailing)
                    .lineLimit(3)
                    .frame(maxWidth: 108, alignment: .trailing)

                HStack(spacing: 5) {
                    Text(settings.t("(An-Nisāʾ 4:103)", "(Nisâ, 103)"))
                        .font(.custom("AvenirNext-Medium", size: 7.0))
                        .foregroundStyle(SalahTheme.gold)
                    NavigationLink { SettingsView() } label: {
                        Image(systemName: settings.notificationsEnabled ? "bell.fill" : "bell")
                            .font(.system(size: 12, weight: .semibold))
                            .foregroundStyle(.white)
                            .frame(width: 24, height: 24)
                            .contentShape(Rectangle())
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(settings.t("Benachrichtigungseinstellungen", "Bildirim ayarları"))
                }
            }
        }
        .padding(.horizontal, 7)
        .padding(.vertical, 5)
        .frame(maxWidth: .infinity)
        .background(Color.clear)
        .accessibilityElement(children: .contain)
    }

    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {
        ZStack(alignment: .bottomTrailing) {
            LinearGradient(
                colors: [
                    Color.clear,
                    SalahTheme.gold.opacity(0.08),
                    SalahTheme.gold.opacity(0.16)
                ],
                startPoint: .leading,
                endPoint: .trailing
            )
            .frame(width: 205, height: 116)
            .offset(x: 9, y: -40)
            .allowsHitTesting(false)

            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 188, height: 108)
                .opacity(0.96)
                .offset(x: 7, y: -4)
                .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: 4) {
                HStack(alignment: .top) {
                    Text(settings.t("Nächstes Gebet", "Sıradaki Namaz"))
                        .font(.system(size: 11.6, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)

                    Spacer()

                    VStack(alignment: .trailing, spacing: 0) {
                        Text(gregorianDateShort(now))
                            .font(.system(size: 8.8, weight: .bold))
                            .foregroundStyle(SalahTheme.ink)
                        Text(shortWeekday(now))
                            .font(.system(size: 7.8, weight: .semibold))
                            .foregroundStyle(SalahTheme.mutedInk)
                    }
                }

                HStack(alignment: .center, spacing: 7) {
                    Image(systemName: prayer.kind.systemImage)
                        .font(.system(size: 22, weight: .medium))
                        .symbolRenderingMode(.hierarchical)
                        .foregroundStyle(SalahTheme.gold)
                        .frame(width: 31)

                    VStack(alignment: .leading, spacing: 0) {
                        Text(prayer.kind.localizedName(settings.language))
                            .font(.system(size: 18, weight: .bold, design: .rounded))
                            .foregroundStyle(SalahTheme.ink)

                        Text(countdownString(from: now, to: prayer.date))
                            .font(.system(size: 25, weight: .bold, design: .rounded).monospacedDigit())
                            .foregroundStyle(SalahTheme.deepTeal)
                            .lineLimit(1)
                            .minimumScaleFactor(0.72)
                    }

                    Spacer(minLength: 90)
                }

                HStack(spacing: 4) {
                    Image(systemName: "mappin")
                        .font(.system(size: 9.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(effectiveLocality)
                        .font(.custom("AvenirNext-DemiBold", size: 9.2))
                        .foregroundStyle(SalahTheme.teal)
                        .lineLimit(1)
                    Spacer()
                }

                HStack(spacing: 5) {
                    Group {
                        if isScreenshotQA || prayer.kind == .asr {
                            ReferenceSunGlyph()
                                .frame(width: 15, height: 15)
                        } else {
                            Image(systemName: prayer.kind.systemImage)
                                .font(.system(size: 10, weight: .semibold))
                                .foregroundStyle(SalahTheme.gold)
                        }
                    }

                    let segments = referenceSequence(for: prayer.kind)
                    ForEach(Array(segments.enumerated()), id: \.offset) { index, segment in
                        HStack(spacing: 2) {
                            Text(segment.0)
                                .font(.system(size: 9.5, weight: .bold))
                            Text(segment.1)
                                .font(.system(size: 8.0, weight: .bold))
                        }
                        .foregroundStyle(SalahTheme.ink)

                        if index < segments.count - 1 {
                            Image(systemName: "arrow.right")
                                .font(.system(size: 7.5, weight: .black))
                                .foregroundStyle(SalahTheme.teal)
                        }
                    }

                    Spacer(minLength: 0)
                    Image(systemName: "chevron.right")
                        .font(.system(size: 7.5, weight: .bold))
                        .foregroundStyle(SalahTheme.gold)
                }
                .frame(maxWidth: .infinity)
                .padding(.horizontal, 8)
                .padding(.vertical, 5)
                .background(SalahTheme.cream.opacity(0.94), in: RoundedRectangle(cornerRadius: 7, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 7, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.30), lineWidth: 0.7)
                }

                Text(settings.t("„Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.“ (An-Nisāʾ 4:103)", "„Namaz, müminlere vakitleri belirlenmiş bir farzdır.“ (Nisâ, 103)"))
                    .font(.custom("Georgia-Italic", size: 6.9))
                    .italic()
                    .foregroundStyle(SalahTheme.mutedInk)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
            }
            .padding(.horizontal, 8)
            .padding(.vertical, 6)
        }
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.66), lineWidth: 0.8)
        }
        .shadow(color: SalahTheme.deepTeal.opacity(0.025), radius: 2, y: 1)
        .frame(minHeight: 178)
        .clipped()
    }

    private var prayerLegendCard: some View {
        HStack(spacing: 8) {
            legendPill(settings.t("Fard", "Farz"), detail: settings.t("Pflicht", "Zorunlu"), icon: "checkmark.seal.fill")
            legendPill(settings.t("Sunnah", "Sünnet"), detail: settings.t("Prophetische Praxis", "Peygamber uygulaması"), icon: "star.fill")
            legendPill(settings.t("Witr", "Vitir"), detail: settings.t("Hanafi: wajib", "Hanefî: vacip"), icon: "moon.stars.fill")
        }
        .salahCard()
    }

    private func legendPill(_ title: String, detail: String, icon: String) -> some View {
        VStack(spacing: 5) {
            Image(systemName: icon).foregroundStyle(SalahTheme.teal)
            Text(title).font(.caption.bold())
            Text(detail).font(.caption2).foregroundStyle(.secondary).multilineTextAlignment(.center).lineLimit(2)
        }
        .frame(maxWidth: .infinity)
    }

    private func todayPrayersCard(_ day: PrayerDay, location: CLLocation) -> some View {
        let displayedTimes = day.prayers

        return VStack(alignment: .leading, spacing: 7) {
            HStack(alignment: .center) {
                Text(settings.t("Heutige Gebetszeiten", "Bugün Namaz Vakitleri"))
                    .font(.system(size: 11.5, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)

                Spacer()

                NavigationLink {
                    PrayerTimesOverviewView()
                } label: {
                    Text(settings.t("Details", "Detaylar"))
                        .font(.system(size: 9.2, weight: .semibold))
                        .foregroundStyle(SalahTheme.teal)
                }
                .buttonStyle(.plain)
            }

            ForEach(displayedTimes, id: \.id) { prayer in
                let active = isNext(prayer, location: location)
                HStack(alignment: .center, spacing: 8) {
                    Image(systemName: prayer.kind.systemImage)
                        .font(.system(size: 12, weight: .bold))
                        .foregroundStyle(active ? SalahTheme.teal : SalahTheme.mutedInk)
                        .frame(width: 16)

                    Text(prayer.kind.localizedName(settings.language))
                        .font(.system(size: 11, weight: active ? .bold : .semibold))
                        .foregroundStyle(SalahTheme.ink)
                        .lineLimit(1)
                        .minimumScaleFactor(0.76)
                        .frame(width: 78, alignment: .leading)

                    Spacer()

                    Text(timeString(prayer.date, use24Hour: settings.use24Hour, language: settings.language))
                        .font(.system(size: 11, weight: .bold, design: .rounded).monospacedDigit())
                        .foregroundStyle(active ? SalahTheme.deepTeal : SalahTheme.ink)
                }
                .padding(.vertical, 2)
            }

            Divider().opacity(0.35)

            NavigationLink {
                PrayerTrackerOverviewView()
            } label: {
                HStack(spacing: 7) {
                    ZStack {
                        Circle().fill(SalahTheme.softTeal).frame(width: 22, height: 22)
                        Image(systemName: "checkmark.circle.fill")
                            .font(.system(size: 12, weight: .bold))
                            .foregroundStyle(SalahTheme.teal)
                    }

                    VStack(alignment: .leading, spacing: 1) {
                        Text(settings.t("Heutige Gebete markieren", "Bugün namazları işaretle"))
                            .font(.system(size: 10.5, weight: .bold))
                            .foregroundStyle(SalahTheme.ink)
                        Text(settings.t("Fortschritt & Serie", "İlerleme ve seri"))
                            .font(.system(size: 8.4, weight: .medium))
                            .foregroundStyle(SalahTheme.mutedInk)
                    }

                    Spacer()
                    Image(systemName: "chevron.right")
                        .font(.system(size: 11, weight: .bold))
                        .foregroundStyle(SalahTheme.gold)
                }
            }
            .buttonStyle(.plain)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 6)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
    }

    private var quickActionStrip: some View {
        HStack(spacing: 7) {
            NavigationLink {
                PrayerTimesOverviewView()
            } label: {
                quickActionPill(
                    icon: "clock.fill",
                    title: settings.t("Zeiten", "Vakitler"),
                    subtitle: settings.t("Heute", "Bugün")
                )
            }
            .buttonStyle(.plain)

            NavigationLink {
                PrayerTrackerOverviewView()
            } label: {
                quickActionPill(
                    icon: "checkmark.circle.fill",
                    title: settings.t("Tracker", "Takip"),
                    subtitle: settings.t("Fortschritt", "İlerleme")
                )
            }
            .buttonStyle(.plain)

            NavigationLink {
                QuranView()
            } label: {
                quickActionPill(
                    icon: "book.fill",
                    title: settings.t("Koran", "Kur'an"),
                    subtitle: settings.t("Lesen", "Oku")
                )
            }
            .buttonStyle(.plain)
        }
    }

    private func quickActionPill(icon: String, title: String, subtitle: String) -> some View {
        VStack(spacing: 5) {
            ZStack {
                Circle()
                    .fill(SalahTheme.softTeal)
                    .frame(width: 30, height: 30)
                Image(systemName: icon)
                    .font(.system(size: 13, weight: .bold))
                    .foregroundStyle(SalahTheme.teal)
            }

            Text(title)
                .font(.system(size: 9.5, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .lineLimit(1)

            Text(subtitle)
                .font(.system(size: 7.5, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)
                .lineLimit(1)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 6)
        .padding(.horizontal, 4)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.38), lineWidth: 0.8)
        }
    }

    private var dailyDuaCard: some View {
        let dua = DailyDuaStore.item(for: now)

        return NavigationLink {
            DailyDuaDetailView(dua: dua)
        } label: {
            VStack(spacing: 4) {
                HStack(spacing: 6) {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.gold.opacity(0.20))
                            .frame(width: 27, height: 27)
                        ReferenceLeafMark(color: SalahTheme.teal)
                            .frame(width: 14, height: 18)
                    }

                    VStack(alignment: .leading, spacing: 1) {
                        Text(settings.t("Dua des Tages", "Günün Duası"))
                            .font(.system(size: 11.3, weight: .bold))
                            .foregroundStyle(SalahTheme.ink)

                        Text(settings.language == .german ? dua.deTitle : dua.trTitle)
                            .font(.system(size: 8.2, weight: .semibold))
                            .foregroundStyle(SalahTheme.mutedInk)
                            .lineLimit(1)
                    }

                    Spacer()

                    Image(systemName: "chevron.right")
                        .font(.system(size: 10, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                        .frame(width: 28, height: 28)
                        .background(SalahTheme.softTeal.opacity(0.88), in: RoundedRectangle(cornerRadius: 8))
                }

                Text(dua.arabic)
                    .font(.system(size: 17.2, weight: .regular))
                    .frame(maxWidth: .infinity)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
                    .minimumScaleFactor(0.88)

                Text(settings.language == .german ? dua.deMeaning : dua.trMeaning)
                    .font(.system(size: 9.2, weight: .semibold))
                    .foregroundStyle(SalahTheme.ink)
                    .frame(maxWidth: .infinity)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)

                HStack(spacing: 5) {
                    if let repetition = dua.repetition {
                        Text(repetition)
                            .font(.system(size: 7.6, weight: .bold))
                            .foregroundStyle(SalahTheme.teal)
                    }

                    Spacer(minLength: 4)

                    Text(dua.source)
                        .font(.system(size: 7.2, weight: .semibold))
                        .foregroundStyle(SalahTheme.mutedInk)
                        .lineLimit(1)
                }
            }
            .padding(.horizontal, 8)
            .padding(.vertical, 7)
            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
            .overlay {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.38), lineWidth: 0.8)
            }
        }
        .buttonStyle(.plain)
        .accessibilityLabel(settings.t(
            "Dua des Tages öffnen: \(dua.deTitle)",
            "Günün duasını aç: \(dua.trTitle)"
        ))
    }

    private var streakCard: some View {
        let _ = trackerRefresh
        let streakValue = isScreenshotQA ? 12 : PrayerTrackerStore.streak(upTo: effectiveNow)
        let weekDates = currentWeekDates()

        return HStack(spacing: 7) {
            VStack(alignment: .leading, spacing: 6) {
                HStack(spacing: 5) {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: 20, height: 20)
                        Image(systemName: "checkmark")
                            .font(.system(size: 8, weight: .black))
                            .foregroundStyle(.white)
                    }

                    Text(settings.t("Gebets-Tracking", "Namaz Takibi"))
                        .font(.system(size: 10.3, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                }

                HStack(spacing: 3) {
                    ForEach(Array(weekDates.enumerated()), id: \.offset) { item in
                        trackingDay(index: item.offset, date: item.element)
                    }
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            Rectangle()
                .fill(SalahTheme.gold.opacity(0.28))
                .frame(width: 0.7, height: 63)

            streakSummary(streakValue)
                .frame(width: 82)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 7)
        .frame(minHeight: 103)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
    }

    private func trackingDay(index: Int, date: Date) -> some View {
        let qaLabels = settings.language == .german
            ? ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
            : ["Pzt", "Sal", "Çar", "Prş", "Cum", "Cts", "Paz"]
        let done: Bool
        let paused: Bool

        if isScreenshotQA {
            done = index < 4
            paused = false
        } else {
            done = PrayerTrackerStore.completedCount(on: date) == PrayerTrackerStore.requiredKinds.count
            paused = PrayerTrackerStore.isPaused(date)
        }

        let label = isScreenshotQA
            ? (qaLabels.indices.contains(index) ? qaLabels[index] : shortWeekdayLetter(date))
            : shortWeekdayLetter(date)

        return VStack(spacing: 2) {
            ZStack {
                Circle()
                    .stroke(done ? SalahTheme.teal : SalahTheme.teal.opacity(0.30), lineWidth: 1)
                    .frame(width: 21, height: 21)

                if done {
                    Circle()
                        .fill(SalahTheme.teal)
                        .frame(width: 21, height: 21)

                    Image(systemName: "checkmark")
                        .font(.system(size: 7.5, weight: .black))
                        .foregroundStyle(.white)
                } else if paused {
                    Image(systemName: "pause.fill")
                        .font(.custom("AvenirNext-DemiBold", size: 6.2))
                        .foregroundStyle(SalahTheme.mutedInk)
                }
            }

            Text(label)
                .font(.system(size: 6.5, weight: .bold))
                .foregroundStyle(SalahTheme.mutedInk)
        }
        .frame(maxWidth: .infinity)
    }

    private func streakSummary(_ value: Int) -> some View {
        VStack(spacing: 0) {
            HStack(spacing: 4) {
                Image(systemName: "flame.fill")
                    .font(.system(size: 18))
                    .foregroundStyle(SalahTheme.gold)

                Text("\(value)")
                    .font(.system(size: 21, weight: .bold).monospacedDigit())
                    .foregroundStyle(SalahTheme.ink)
            }

            Text(settings.t("Tägliche Serie", "Günlük Seri"))
                .font(.system(size: 7.0, weight: .bold))
                .foregroundStyle(SalahTheme.ink)

            Text(settings.t("Tage in Folge", "Gün üst üste"))
                .font(.system(size: 6.3, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)

            Text(settings.t(
                "Beständigkeit ist der\nSchlüssel zum Erfolg.",
                "İstikrar\nbaşarının anahtarıdır."
            ))
                .font(.system(size: 5.7, weight: .medium, design: .serif))
                .italic()
                .multilineTextAlignment(.center)
                .foregroundStyle(SalahTheme.mutedInk)
                .lineLimit(2)
                .padding(.top, 2)
        }
    }

    private var dailyDeenCard: some View {
        let tasks = [
            ("quran", settings.t("5 Min. Quran", "5 dk Kur'an"), "book.fill"),
            ("dhikr", settings.t("Kurzer Dhikr", "Kısa zikir"), "circle.grid.cross.fill"),
            ("learn", settings.t("1 Dua/Sura wiederholen", "1 dua/sure tekrarla"), "graduationcap.fill")
        ]
        let done = tasks.filter { DailyDeenStore.isDone($0.0, now) }.count
        return VStack(alignment: .leading, spacing: 10) {
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text(settings.t("Daily Deen", "Günlük Deen")).font(.headline)
                    Text(settings.t("Kleine Schritte. Beständig bleiben.", "Küçük adımlar. İstikrarlı ol."))
                        .font(.caption).foregroundStyle(.secondary)
                }
                Spacer()
                Text("\(done)/\(tasks.count)").font(.headline.monospacedDigit()).foregroundStyle(SalahTheme.teal)
            }
            ForEach(tasks, id: \.0) { task in
                let checked = DailyDeenStore.isDone(task.0, now)
                Button {
                    DailyDeenStore.toggle(task.0, now)
                    dailyDeenRefresh &+= 1
                } label: {
                    HStack(spacing: 10) {
                        Image(systemName: task.2).frame(width: 22).foregroundStyle(SalahTheme.teal)
                        Text(task.1).foregroundStyle(SalahTheme.ink)
                        Spacer()
                        Image(systemName: checked ? "checkmark.circle.fill" : "circle")
                            .foregroundStyle(checked ? SalahTheme.teal : .secondary)
                    }
                    .contentShape(Rectangle())
                }
                .buttonStyle(.plain)
            }
        }
        .salahCard()
    }

    private var dashboardGrid: some View {
        let columns = Array(repeating: GridItem(.flexible(), spacing: 7), count: 4)
        return LazyVGrid(columns: columns, spacing: 7) {
            NavigationLink { QuranView() } label: {
                DashboardTile(title: settings.t("Quran", "Kur'an"), subtitle: settings.t("Lesen & hören", "Oku & Dinle"), icon: "quran")
            }
            NavigationLink { QuranView() } label: {
                DashboardTile(title: settings.t("Quran-Audio", "Kur'an Sesi"), subtitle: settings.t("Anhören", "Dinle"), icon: "quran_audio")
            }
            NavigationLink { QuranFavoritesLandingView() } label: {
                DashboardTile(title: settings.t("Juz & Favoriten", "Cüz & Favoriler"), subtitle: settings.t("Lesezeichen", "İşaretler"), icon: "fav")
            }
            NavigationLink { PrayerTimesOverviewView() } label: {
                DashboardTile(title: settings.t("Gebetszeiten", "Namaz Vakitleri"), subtitle: settings.t("Zeiten", "Vakitler"), icon: "times")
            }
            NavigationLink { GuideView() } label: {
                DashboardTile(title: settings.t("Gebet\nlernen", "Namaz\nÖğren"), subtitle: settings.t("Schritt für Schritt", "Adım adım"), icon: "prayer")
            }
            NavigationLink { WuduGuideView() } label: {
                DashboardTile(title: settings.t("Wudu\nAnleitung", "Abdest\nRehberi"), subtitle: settings.t("Grundlagen", "Temel"), icon: "wudu")
            }
            NavigationLink { HijriCalendarView() } label: {
                DashboardTile(title: settings.t("Islamischer\nKalender", "İslami Takvim"), subtitle: settings.t("Ereignisse", "Olaylar"), icon: "calendar")
            }
            NavigationLink { DhikrView() } label: {
                DashboardTile(title: settings.t("Dua & Dhikr", "Dua & Zikir"), subtitle: settings.t("Täglich", "Günlük"), icon: "dhikr")
            }
            NavigationLink { QiblaView() } label: {
                DashboardTile(title: settings.t("Qibla-Richtung", "Kıble Yönü"), subtitle: settings.t("Qibla", "Qibla"), icon: "qibla")
            }
            NavigationLink { PrayerTermsView() } label: {
                DashboardTile(title: settings.t("Islamwissen", "İslami Bilgiler"), subtitle: settings.t("Wissen", "Bilgi"), icon: "info")
            }
            NavigationLink { PrayerTrackerOverviewView() } label: {
                DashboardTile(title: settings.t("Gebets-Tracker", "Namaz Takibi"), subtitle: settings.t("Fortschritt", "İlerleme"), icon: "checkmark")
            }
            NavigationLink { SettingsView() } label: {
                DashboardTile(title: settings.t("Einstellungen", "Ayarlar"), subtitle: settings.t("Einstellungen", "Ayarlar"), icon: "settings")
            }
        }
        .buttonStyle(.plain)
    }

    private var referenceQuoteStrip: some View {
        HStack(spacing: 8) {
            ReferenceLeafMark(color: SalahTheme.teal)
                .frame(width: 18, height: 23)
            VStack(alignment: .leading, spacing: 1) {
                Text(settings.t("„Kleine Schritte führen zu großen Veränderungen.“", "“Küçük adımlar, büyük değişimler getirir.”"))
                    .font(.system(size: 10.5, weight: .semibold, design: .serif))
                    .italic()
                    .foregroundStyle(SalahTheme.ink)
                Text("Kleine Schritte bringen große Veränderungen.")
                    .font(.system(size: 8.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
            }
            Spacer(minLength: 0)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 7)
        .background(
            SalahTheme.cream,
            in: RoundedRectangle(cornerRadius: 8, style: .continuous)
        )
        .frame(minHeight: 48)
        .overlay {
            RoundedRectangle(cornerRadius: 9, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.36), lineWidth: 0.8)
        }
    }

    private func referenceSequence(for kind: PrayerKind) -> [(String, String)] {
        let sunnah = settings.language == .german ? "Sunnah" : "Sünnet"
        let fard = settings.language == .german ? "Fard" : "Farz"
        let witr = settings.language == .german ? "Witr" : "Vitir"

        switch kind {
        case .fajr:
            return [("2", sunnah), ("2", fard)]
        case .sunrise:
            return [("2", settings.language == .german ? "Duha" : "Kuşluk")]
        case .dhuhr:
            return [("4", sunnah), ("4", fard), ("2", sunnah)]
        case .asr:
            return [("4", sunnah), ("4", fard)]
        case .maghrib:
            return [("3", fard), ("2", sunnah)]
        case .isha:
            return [("4", sunnah), ("4", fard), ("2", sunnah), ("3", witr)]
        }
    }

    private func currentWeekDates() -> [Date] {
        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = .autoupdatingCurrent
        let today = calendar.startOfDay(for: effectiveNow)
        let weekday = calendar.component(.weekday, from: today)
        let daysFromMonday: Int = (weekday + 5) % 7
        guard let monday = calendar.date(byAdding: .day, value: -daysFromMonday, to: today) else { return [today] }
        return (0..<7).compactMap { calendar.date(byAdding: .day, value: $0, to: monday) }
    }

    private func shortWeekdayLetter(_ date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        f.timeZone = .autoupdatingCurrent
        f.dateFormat = "EE"
        return f.string(from: date)
            .replacingOccurrences(of: ".", with: "")
            .capitalized
    }

    private func shortWeekday(_ date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        f.timeZone = .autoupdatingCurrent
        f.dateFormat = "EEEE"
        return f.string(from: date).capitalized
    }

    private func prayerTimesCard(today: PrayerDay, location: CLLocation) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Text(settings.t("Heutige Gebetszeiten", "Bugünkü namaz vakitleri")).font(.headline)
                Spacer()
                Button { locationManager.refresh() } label: { Image(systemName: "arrow.clockwise") }
                    .buttonStyle(.plain)
                    .accessibilityLabel(settings.t("Standort aktualisieren", "Konumu güncelle"))
            }
            .padding(.bottom, 8)

            ForEach(today.prayers) { prayer in
                Button { selectedPrayer = prayer } label: {
                    PrayerRow(prayer: prayer, isNext: isNext(prayer, location: location))
                }
                .buttonStyle(.plain)
                if prayer.id != today.prayers.last?.id { Divider().opacity(0.6) }
            }
        }
        .salahCard()
    }

    private var fridayCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Label(settings.t("Freitag / Jumuʿah", "Cuma"), systemImage: "person.3.fill")
                .font(.headline).foregroundStyle(SalahTheme.teal)
            Text(settings.t(
                "Jumuʿah hat 2 Rakʿah Fard in Gemeinschaft. Die tatsächliche Jumuʿah-Uhrzeit legt die jeweilige Moschee fest.",
                "Cuma namazının cemaatle kılınan farzı 2 rekâttır. Gerçek cuma saatini ilgili cami belirler."
            )).font(.subheadline)
        }
        .salahCard()
    }

    @ViewBuilder
    private func qiyamCard(_ day: PrayerDay) -> some View {
        if day.middleOfNight != nil || day.lastThirdOfNight != nil {
            VStack(alignment: .leading, spacing: 8) {
                Label(settings.t("Nacht", "Gece"), systemImage: "moon.stars.fill")
                    .font(.headline).foregroundStyle(SalahTheme.teal)
                if let middle = day.middleOfNight {
                    valueRow(settings.t("Mitte der Nacht", "Gecenin yarısı"), timeString(middle, use24Hour: settings.use24Hour, language: settings.language))
                }
                if let lastThird = day.lastThirdOfNight {
                    valueRow(settings.t("Letztes Drittel beginnt", "Son üçte birlik bölüm başlar"), timeString(lastThird, use24Hour: settings.use24Hour, language: settings.language))
                }
            }
            .salahCard()
        }
    }

    private func valueRow(_ title: String, _ value: String) -> some View {
        HStack { Text(title).font(.subheadline); Spacer(); Text(value).font(.subheadline.bold().monospacedDigit()) }
    }

    private var locationState: some View {
        ScrollView {
            VStack(spacing: 0) {
                brandHeader
                    .padding(.horizontal, 7)
                    .padding(.top, 3)
                    .padding(.bottom, 5)
                    .background(SalahTheme.navigationTeal)

                LazyVStack(spacing: 5) {
                    VStack(alignment: .leading, spacing: 7) {
                        HStack(spacing: 8) {
                            Image(systemName: "location.slash")
                                .font(.system(size: 17, weight: .semibold))
                                .foregroundStyle(SalahTheme.teal)

                            VStack(alignment: .leading, spacing: 1) {
                                Text(settings.t("Standort ist optional", "Konum isteğe bağlı"))
                                    .font(.system(size: 12.5, weight: .bold))
                                    .foregroundStyle(SalahTheme.ink)
                                Text(settings.t(
                                    "Nur Gebetszeiten und Qibla benötigen deinen Standort. Alle anderen Bereiche bleiben nutzbar.",
                                    "Yalnızca namaz vakitleri ve kıble konum gerektirir. Diğer tüm alanları kullanabilirsin."
                                ))
                                .font(.system(size: 9.2, weight: .medium))
                                .foregroundStyle(SalahTheme.mutedInk)
                                .fixedSize(horizontal: false, vertical: true)
                            }

                            Spacer(minLength: 4)
                        }

                        Button {
                            locationManager.useDeviceLocation()
                            manualLocationError = nil
                        } label: {
                            Label(settings.t("Standort aktivieren", "Konumu etkinleştir"), systemImage: "location.fill")
                                .font(.system(size: 10.5, weight: .bold))
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 8)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(.white)
                        .background(SalahTheme.teal, in: RoundedRectangle(cornerRadius: 10, style: .continuous))

                        HStack(spacing: 7) {
                            TextField(settings.t("Stadt oder PLZ manuell", "Şehir veya posta kodu"), text: $manualLocationText)
                                .textInputAutocapitalization(.words)
                                .autocorrectionDisabled()
                                .font(.system(size: 10.5, weight: .medium))
                                .padding(.horizontal, 10)
                                .frame(height: 38)
                                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 9))
                                .overlay {
                                    RoundedRectangle(cornerRadius: 9)
                                        .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
                                }

                            Button {
                                Task {
                                    isResolvingManualLocation = true
                                    manualLocationError = nil
                                    let success = await locationManager.setManualLocation(searchText: manualLocationText)
                                    isResolvingManualLocation = false
                                    if !success { manualLocationError = locationManager.lastError }
                                }
                            } label: {
                                Group {
                                    if isResolvingManualLocation {
                                        ProgressView().tint(.white)
                                    } else {
                                        Image(systemName: "checkmark")
                                            .font(.system(size: 12, weight: .bold))
                                    }
                                }
                                .frame(width: 38, height: 38)
                            }
                            .buttonStyle(.plain)
                            .foregroundStyle(.white)
                            .background(SalahTheme.navigationTeal, in: RoundedRectangle(cornerRadius: 9))
                            .disabled(manualLocationText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || isResolvingManualLocation)
                        }

                        if let manualLocationError {
                            Text(manualLocationError)
                                .font(.system(size: 8.5, weight: .medium))
                                .foregroundStyle(.red)
                        }
                    }
                    .padding(10)
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13, style: .continuous))
                    .overlay {
                        RoundedRectangle(cornerRadius: 13, style: .continuous)
                            .stroke(SalahTheme.gold.opacity(0.40), lineWidth: 0.8)
                    }

                    quickActionStrip
                    dailyDuaCard

                    NavigationLink { PrayerTrackerOverviewView() } label: { streakCard }
                        .buttonStyle(.plain)
                        .accessibilityHint(settings.t("Gebets-Tracking öffnen", "Namaz takibini aç"))

                    dashboardGrid
                    referenceQuoteStrip
                }
                .padding(.horizontal, 7)
                .padding(.top, 5)
                .padding(.bottom, 4)
                .background(SalahTheme.page)
            }
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
    }

    private func isNext(_ prayer: PrayerOccurrence, location: CLLocation) -> Bool {
        guard let next = engine.nextPrayer(now: now, location: location, settings: settings) else { return false }
        return prayer.kind == next.kind && LocalDay.calendar().isDate(prayer.date, inSameDayAs: next.date)
    }

    private func gregorianDateShort(_ date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        f.timeZone = .autoupdatingCurrent
        f.dateFormat = settings.language == .german ? "dd.MM.yyyy" : "d MMMM yyyy"
        return f.string(from: date)
    }
}


struct PrayerTimesOverviewView: View {
    @EnvironmentObject private var locationManager: LocationManager
    @EnvironmentObject private var settings: SettingsStore
    @Environment(\.scenePhase) private var scenePhase
    @State private var period = 0
    @State private var now = Date()
    private let engine = PrayerEngine()

    private var isScreenshotQA: Bool {
        ProcessInfo.processInfo.environment["SALAH_QA_SCREENSHOT"] == "1"
    }

    private var referenceDate: Date {
        guard isScreenshotQA else { return now }
        var c = DateComponents()
        c.calendar = Calendar(identifier: .gregorian)
        c.timeZone = TimeZone(identifier: "Europe/Istanbul")
        c.year = 2025; c.month = 3; c.day = 14; c.hour = 13; c.minute = 0
        return c.date ?? Date()
    }

    private var effectiveLocation: CLLocation? {
        if isScreenshotQA { return CLLocation(latitude: 41.0082, longitude: 28.9784) }
        return locationManager.location
    }

    var body: some View {
        ScrollView {
            VStack(spacing: 10) {
                HStack(spacing: 3) {
                    let periodTitles = [
                        settings.t("Heute", "Bugün"),
                        settings.t("Wöchentlich", "Haftalık"),
                        settings.t("Monatlich", "Aylık")
                    ]
                    ForEach(Array(periodTitles.enumerated()), id: \.offset) { index, title in
                        Button {
                            withAnimation(.easeOut(duration: 0.12)) { period = index }
                        } label: {
                            Text(title)
                                .font(.custom("AvenirNext-DemiBold", size: 8.8))
                                .foregroundStyle(period == index ? SalahTheme.deepTeal : SalahTheme.mutedInk)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 5)
                                .background(period == index ? SalahTheme.gold.opacity(0.18) : Color.clear,
                                            in: RoundedRectangle(cornerRadius: 6, style: .continuous))
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(3)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 8).stroke(SalahTheme.gold.opacity(0.32), lineWidth: 0.7) }

                if let location = effectiveLocation {
                    if period == 0, let day = engine.calculateDay(for: referenceDate, location: location, settings: settings) {
                        referenceTodayCard(day: day, location: location)

                        HStack(spacing: 8) {
                            NavigationLink { QiblaView() } label: {
                                referenceQiblaTile
                            }
                            .buttonStyle(.plain)

                            referenceMapTile
                                .accessibilityElement(children: .ignore)
                                .accessibilityLabel(settings.t(
                                    "Kaaba und Gebetsrichtung",
                                    "Kâbe ve kıble yönü"
                                ))
                        }
                    } else {
                        ForEach(days, id: \.self) { date in
                            if let day = engine.calculateDay(for: date, location: location, settings: settings) {
                                compactDayCard(day: day, date: date)
                            }
                        }
                    }
                } else {
                    VStack(spacing: 12) {
                        ContentUnavailableView(
                            settings.t("Standort benötigt", "Konum gerekli"),
                            systemImage: "location.slash",
                            description: Text(settings.t(
                                "Für Gebetszeiten wird ein Standort benötigt. Verwende GPS oder lege einen Ort im Profil manuell fest.",
                                "Namaz vakitleri için bir konum gerekir. GPS kullan veya profilde manuel bir yer belirle."
                            ))
                        )

                        Button {
                            if locationManager.authorizationStatus == .denied ||
                                locationManager.authorizationStatus == .restricted {
                                guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
                                UIApplication.shared.open(url)
                            } else {
                                locationManager.useDeviceLocation()
                            }
                        } label: {
                            Label(
                                settings.t(
                                    locationManager.authorizationStatus == .denied ||
                                        locationManager.authorizationStatus == .restricted
                                        ? "iPhone-Einstellungen öffnen"
                                        : "Aktuellen Standort verwenden",
                                    locationManager.authorizationStatus == .denied ||
                                        locationManager.authorizationStatus == .restricted
                                        ? "iPhone ayarlarını aç"
                                        : "Mevcut konumu kullan"
                                ),
                                systemImage: locationManager.authorizationStatus == .denied ||
                                    locationManager.authorizationStatus == .restricted
                                    ? "gear"
                                    : "location.fill"
                            )
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.borderedProminent)
                        .tint(SalahTheme.teal)

                        NavigationLink {
                            SettingsView()
                        } label: {
                            Label(
                                settings.t("Ort manuell festlegen", "Konumu manuel belirle"),
                                systemImage: "mappin.and.ellipse"
                            )
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                        .tint(SalahTheme.teal)
                    }
                    .padding(.vertical, 8)
                }
            }
            .padding(.horizontal, 11)
            .padding(.vertical, 10)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetszeiten", "Namaz Vakitleri"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            guard !isScreenshotQA else { return }
            now = Date()
            if locationManager.usesManualLocation ||
                locationManager.authorizationStatus == .authorizedWhenInUse ||
                locationManager.authorizationStatus == .authorizedAlways {
                locationManager.requestAccessAndStart()
            }
        }
        .onChange(of: scenePhase) { _, phase in
            guard !isScreenshotQA, phase == .active else { return }
            now = Date()
        }
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
            guard !isScreenshotQA else { return }
            now = Date()
        }
    }

    private func referenceTodayCard(day: PrayerDay, location: CLLocation) -> some View {
        let next = engine.nextPrayer(now: referenceDate, location: location, settings: settings)

        return VStack(spacing: 0) {
            VStack(spacing: 0) {
                ForEach(Array(day.prayers.enumerated()), id: \.element.id) { index, prayer in
                    let isNext = isScreenshotQA
                        ? prayer.kind == .asr
                        : (next?.kind == prayer.kind &&
                           LocalDay.calendar().isDate(prayer.date, inSameDayAs: next?.date ?? .distantPast))

                    HStack(spacing: 9) {
                        ZStack {
                            Circle()
                                .stroke(isNext ? SalahTheme.teal : SalahTheme.mutedInk.opacity(0.72), lineWidth: 1.1)
                                .frame(width: 7, height: 7)
                            if isNext {
                                Circle()
                                    .fill(SalahTheme.teal)
                                    .frame(width: 3, height: 3)
                            }
                        }
                        .frame(width: 22)

                        Text(referencePrayerName(prayer.kind))
                            .font(.custom(isNext ? "AvenirNext-Bold" : "AvenirNext-DemiBold", size: 10.8))
                            .foregroundStyle(SalahTheme.ink)

                        Spacer()

                        Text(referenceTimeText(for: prayer.kind, actual: prayer.date))
                            .font(.custom("AvenirNext-DemiBold", size: 11.4).monospacedDigit())
                            .foregroundStyle(SalahTheme.ink)
                    }
                    .padding(.horizontal, 13)
                    .padding(.vertical, 5.5)
                    .background(isNext ? SalahTheme.gold.opacity(0.16) : Color.clear)

                    if index < day.prayers.count - 1 {
                        Divider().padding(.leading, 44).opacity(0.38)
                    }
                }
            }
            .background(SalahTheme.cream)
        }
        .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 10).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 0.7) }
    }

    private func referenceTimeText(for kind: PrayerKind, actual: Date) -> String {
        if isScreenshotQA {
            switch kind {
            case .fajr: return "04:52"
            case .sunrise: return "06:18"
            case .dhuhr: return "12:43"
            case .asr: return "15:21"
            case .maghrib: return "18:57"
            case .isha: return "20:19"
            }
        }
        return timeString(actual, use24Hour: settings.use24Hour, language: settings.language)
    }

    private var referenceQiblaTile: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(settings.t("Qibla-Richtung", "Kıble Yönü"))
                .font(.custom("AvenirNext-DemiBold", size: 10.6))
                .foregroundStyle(SalahTheme.ink)
            Text("Qibla")
                .font(.custom("AvenirNext-Medium", size: 8.4))
                .foregroundStyle(SalahTheme.mutedInk)

            Spacer(minLength: 2)

            ReferencePosterQiblaArt()
                .frame(maxWidth: .infinity, minHeight: 73, maxHeight: 73)
                .accessibilityHidden(true)
        }
        .frame(maxWidth: .infinity, minHeight: 126, alignment: .leading)
        .padding(10)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7)
        }
    }

    private var referenceMapTile: some View {
        ReferencePosterMapArt()
            .frame(maxWidth: .infinity, minHeight: 146, maxHeight: 146)
            .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
            .overlay {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7)
            }
            .accessibilityHidden(true)
    }

    private func referenceToolTile(icon: String, title: String, subtitle: String) -> some View {
        VStack(spacing: 5) {
            ZStack {
                Circle()
                    .fill(SalahTheme.softTeal)
                    .frame(width: 51, height: 51)
                Image(systemName: icon)
                    .font(.system(size: 29, weight: .semibold))
                    .foregroundStyle(SalahTheme.teal)
            }
            Text(title)
                .font(.system(size: 10.5, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .multilineTextAlignment(.center)
                .lineLimit(2)
            Text(subtitle)
                .font(.system(size: 8.5, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)
        }
        .frame(maxWidth: .infinity, minHeight: 94)
        .padding(9)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 10).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7) }
    }

    private func referencePrayerName(_ kind: PrayerKind) -> String {
        if settings.language == .turkish {
            switch kind {
            case .fajr: return "İmsak"
            case .sunrise: return "Sabah"
            case .dhuhr: return "Öğle"
            case .asr: return "İkindi"
            case .maghrib: return "Akşam"
            case .isha: return "Yatsı"
            }
        }
        switch kind {
        case .fajr: return "Fajr"
        case .sunrise: return "Sonnenaufgang"
        case .dhuhr: return "Dhuhr"
        case .asr: return "Asr"
        case .maghrib: return "Maghrib"
        case .isha: return "Isha"
        }
    }

    private func compactDayCard(day: PrayerDay, date: Date) -> some View {
        VStack(alignment: .leading, spacing: 7) {
            HStack {
                VStack(alignment: .leading, spacing: 1) {
                    Text(shortDate(date))
                        .font(.system(size: 13, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                    Text(hijriDateString(date, language: settings.language))
                        .font(.system(size: 8.5, weight: .medium))
                        .foregroundStyle(SalahTheme.mutedInk)
                }
                Spacer()
                if LocalDay.calendar().isDateInToday(date) {
                    Text(settings.t("HEUTE", "BUGÜN"))
                        .font(.system(size: 8, weight: .black))
                        .foregroundStyle(SalahTheme.teal)
                        .padding(.horizontal, 7)
                        .padding(.vertical, 4)
                        .background(SalahTheme.softTeal, in: Capsule())
                }
            }

            ForEach(day.prayers) { prayer in
                HStack {
                    Text(referencePrayerName(prayer.kind))
                        .font(.system(size: 10.5, weight: .semibold))
                    Spacer()
                    Text(timeString(prayer.date, use24Hour: settings.use24Hour, language: settings.language))
                        .font(.system(size: 10.5, weight: .bold).monospacedDigit())
                }
                .foregroundStyle(SalahTheme.ink)
            }
        }
        .padding(12)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
    }

    private var days: [Date] {
        let count = period == 1 ? 7 : 30
        let start = LocalDay.startOfDay(for: referenceDate)
        return (0..<count).compactMap { LocalDay.addingDays($0, to: start) }
    }

    private func shortDate(_ date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        f.timeZone = .autoupdatingCurrent
        f.dateFormat = "EEE, d. MMM"
        return f.string(from: date)
    }
}

private struct ReferencePosterQiblaArt: View {
    var body: some View {
        GeometryReader { proxy in
            let size = min(proxy.size.width, proxy.size.height)
            let center = CGPoint(x: proxy.size.width * 0.50, y: proxy.size.height * 0.50)

            ZStack {
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [SalahTheme.softTeal, SalahTheme.cream],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: size * 0.82, height: size * 0.82)

                Circle()
                    .stroke(SalahTheme.gold.opacity(0.78), lineWidth: max(2, size * 0.018))
                    .frame(width: size * 0.66, height: size * 0.66)

                ForEach(0..<8, id: \.self) { index in
                    Capsule()
                        .fill(index == 0 ? SalahTheme.gold : SalahTheme.deepTeal.opacity(0.50))
                        .frame(width: size * 0.018, height: index % 2 == 0 ? size * 0.105 : size * 0.072)
                        .offset(y: -size * 0.285)
                        .rotationEffect(.degrees(Double(index) * 45))
                }

                Path { p in
                    p.move(to: CGPoint(x: center.x, y: center.y - size * 0.24))
                    p.addLine(to: CGPoint(x: center.x - size * 0.07, y: center.y + size * 0.05))
                    p.addLine(to: CGPoint(x: center.x, y: center.y + size * 0.015))
                    p.addLine(to: CGPoint(x: center.x + size * 0.07, y: center.y + size * 0.05))
                    p.closeSubpath()
                }
                .fill(SalahTheme.teal)
                .rotationEffect(.degrees(34))

                ZStack {
                    RoundedRectangle(cornerRadius: size * 0.035, style: .continuous)
                        .fill(SalahTheme.deepTeal)
                        .frame(width: size * 0.25, height: size * 0.20)

                    Rectangle()
                        .fill(SalahTheme.gold)
                        .frame(width: size * 0.25, height: size * 0.035)
                        .offset(y: -size * 0.035)

                    RoundedRectangle(cornerRadius: size * 0.008)
                        .fill(SalahTheme.gold.opacity(0.88))
                        .frame(width: size * 0.045, height: size * 0.070)
                        .offset(y: size * 0.042)
                }
                .offset(y: size * 0.09)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .padding(12)
        .accessibilityHidden(true)
    }
}

private struct ReferencePosterMapArt: View {
    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height

            ZStack {
                Color(red: 0.72, green: 0.88, blue: 0.87)

                // Soft simplified world-map land masses matching the poster tile.
                Path { p in
                    p.move(to: CGPoint(x: w * 0.03, y: h * 0.18))
                    p.addCurve(
                        to: CGPoint(x: w * 0.25, y: h * 0.31),
                        control1: CGPoint(x: w * 0.09, y: h * 0.10),
                        control2: CGPoint(x: w * 0.22, y: h * 0.13)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.19, y: h * 0.50),
                        control1: CGPoint(x: w * 0.27, y: h * 0.39),
                        control2: CGPoint(x: w * 0.23, y: h * 0.46)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.08, y: h * 0.42),
                        control1: CGPoint(x: w * 0.15, y: h * 0.53),
                        control2: CGPoint(x: w * 0.09, y: h * 0.50)
                    )
                    p.closeSubpath()
                }
                .fill(Color.white.opacity(0.58))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.30, y: h * 0.14))
                    p.addCurve(
                        to: CGPoint(x: w * 0.60, y: h * 0.20),
                        control1: CGPoint(x: w * 0.38, y: h * 0.06),
                        control2: CGPoint(x: w * 0.52, y: h * 0.08)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.66, y: h * 0.39),
                        control1: CGPoint(x: w * 0.68, y: h * 0.24),
                        control2: CGPoint(x: w * 0.69, y: h * 0.32)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.49, y: h * 0.45),
                        control1: CGPoint(x: w * 0.59, y: h * 0.44),
                        control2: CGPoint(x: w * 0.54, y: h * 0.42)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.36, y: h * 0.34),
                        control1: CGPoint(x: w * 0.43, y: h * 0.49),
                        control2: CGPoint(x: w * 0.35, y: h * 0.44)
                    )
                    p.closeSubpath()
                }
                .fill(Color.white.opacity(0.64))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.43, y: h * 0.42))
                    p.addCurve(
                        to: CGPoint(x: w * 0.52, y: h * 0.79),
                        control1: CGPoint(x: w * 0.55, y: h * 0.49),
                        control2: CGPoint(x: w * 0.58, y: h * 0.65)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.37, y: h * 0.59),
                        control1: CGPoint(x: w * 0.44, y: h * 0.75),
                        control2: CGPoint(x: w * 0.37, y: h * 0.68)
                    )
                    p.closeSubpath()
                }
                .fill(Color.white.opacity(0.57))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.69, y: h * 0.24))
                    p.addCurve(
                        to: CGPoint(x: w * 0.96, y: h * 0.31),
                        control1: CGPoint(x: w * 0.80, y: h * 0.16),
                        control2: CGPoint(x: w * 0.91, y: h * 0.20)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.78, y: h * 0.49),
                        control1: CGPoint(x: w * 0.95, y: h * 0.42),
                        control2: CGPoint(x: w * 0.87, y: h * 0.48)
                    )
                    p.closeSubpath()
                }
                .fill(Color.white.opacity(0.55))

                Image(systemName: "mappin.circle.fill")
                    .font(.system(size: min(w, h) * 0.25, weight: .bold))
                    .symbolRenderingMode(.palette)
                    .foregroundStyle(SalahTheme.teal, Color.white)
                    .offset(x: w * 0.08, y: h * 0.08)
            }
            .frame(width: w, height: h)
        }
    }
}

private struct ReferencePagePattern: View {
    var body: some View {
        GeometryReader { proxy in
            Canvas { context, size in
                let step: CGFloat = 44
                var path = Path()
                var x: CGFloat = -step
                while x < size.width + step {
                    var y: CGFloat = -step
                    while y < size.height + step {
                        let rect = CGRect(x: x, y: y, width: 15, height: 15)
                        path.addRect(rect)
                        y += step
                    }
                    x += step
                }
                context.stroke(path, with: .color(SalahTheme.gold.opacity(0.055)), lineWidth: 0.65)
            }
        }
    }
}

private struct ReferenceSunGlyph: View {
    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height

            ZStack {
                Circle()
                    .fill(SalahTheme.gold.opacity(0.18))
                    .frame(width: w, height: h)

                ForEach(0..<8, id: \.self) { index in
                    Rectangle()
                        .fill(SalahTheme.gold)
                        .frame(width: max(2, w * 0.08), height: max(3, h * 0.16))
                        .rotationEffect(.degrees(Double(index) * 45))
                        .offset(y: -(h * 0.28))
                }

                Circle()
                    .stroke(SalahTheme.gold, lineWidth: max(1.2, min(w, h) * 0.10))
                    .frame(width: w * 0.68, height: h * 0.68)

                Circle()
                    .fill(SalahTheme.gold)
                    .frame(width: w * 0.35, height: h * 0.35)
            }
        }
    }
}

private struct ReferenceLeafMark: View {
    let color: Color

    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height

            ZStack {
                Path { path in
                    path.move(to: CGPoint(x: w * 0.5, y: h * 0.08))
                    path.addCurve(
                        to: CGPoint(x: w * 0.18, y: h * 0.72),
                        control1: CGPoint(x: w * 0.12, y: h * 0.18),
                        control2: CGPoint(x: w * 0.02, y: h * 0.48)
                    )
                    path.addCurve(
                        to: CGPoint(x: w * 0.5, y: h * 0.92),
                        control1: CGPoint(x: w * 0.30, y: h * 0.90),
                        control2: CGPoint(x: w * 0.42, y: h * 0.98)
                    )
                    path.addCurve(
                        to: CGPoint(x: w * 0.82, y: h * 0.72),
                        control1: CGPoint(x: w * 0.56, y: h * 0.98),
                        control2: CGPoint(x: w * 0.68, y: h * 0.90)
                    )
                    path.addCurve(
                        to: CGPoint(x: w * 0.5, y: h * 0.08),
                        control1: CGPoint(x: w * 0.98, y: h * 0.48),
                        control2: CGPoint(x: w * 0.88, y: h * 0.18)
                    )
                    path.closeSubpath()
                }
                .fill(color)

                Path { path in
                    path.move(to: CGPoint(x: w * 0.5, y: h * 0.12))
                    path.addLine(to: CGPoint(x: w * 0.5, y: h * 0.88))
                }
                .stroke(color.opacity(0.72), lineWidth: max(1.2, w * 0.06))

                Path { path in
                    path.move(to: CGPoint(x: w * 0.28, y: h * 0.52))
                    path.addLine(to: CGPoint(x: w * 0.72, y: h * 0.52))
                }
                .stroke(color.opacity(0.68), lineWidth: max(1.1, w * 0.05))
            }
        }
    }
}

private struct ReferenceMosqueSkyline: View {
    var body: some View {
        ZStack(alignment: .bottom) {
            LinearGradient(
                colors: [Color.clear, SalahTheme.gold.opacity(0.16)],
                startPoint: .top,
                endPoint: .bottom
            )

            HStack(alignment: .bottom, spacing: 3) {
                minaret(height: 49)
                dome(width: 26, height: 35)
                minaret(height: 61)
                dome(width: 38, height: 45)
                minaret(height: 55)
                dome(width: 27, height: 33)
                minaret(height: 46)
            }
            .foregroundStyle(SalahTheme.teal.opacity(0.92))
            .padding(.bottom, 3)
        }
        .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
        .accessibilityHidden(true)
    }

    private func minaret(height: CGFloat) -> some View {
        VStack(spacing: 0) {
            Image(systemName: "triangle.fill")
                .font(.system(size: 5))
            Capsule()
                .frame(width: 4, height: height - 7)
        }
        .frame(height: height)
    }

    private func dome(width: CGFloat, height: CGFloat) -> some View {
        VStack(spacing: 0) {
            Circle()
                .frame(width: width, height: width)
                .mask(Rectangle().frame(width: width, height: width / 2).offset(y: width / 4))
                .frame(height: width / 2)
            Rectangle()
                .frame(width: width, height: max(8, height - width / 2))
        }
        .frame(height: height, alignment: .bottom)
    }
}

private struct DashboardTile: View {
    let title: String
    let subtitle: String
    let icon: String

    var body: some View {
        VStack(spacing: 4) {
            ZStack {
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [SalahTheme.softTeal, SalahTheme.cream],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 42, height: 42)

                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.52), lineWidth: 1)
                    .frame(width: 42, height: 42)

                ReferenceDashboardGlyph(kind: glyphKind)
                    .frame(width: 27, height: 27)
            }

            Text(title)
                .font(.system(size: 8.8, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .multilineTextAlignment(.center)
                .lineLimit(2)
                .fixedSize(horizontal: false, vertical: true)
                .minimumScaleFactor(0.70)

            if !subtitle.isEmpty {
                Text(subtitle)
                    .font(.system(size: 6.8, weight: .semibold))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .multilineTextAlignment(.center)
                    .lineLimit(1)
                    .minimumScaleFactor(0.72)
            } else {
                Color.clear.frame(height: 7)
            }
        }
        .frame(maxWidth: .infinity, minHeight: 89, alignment: .center)
        .padding(.horizontal, 3)
        .padding(.vertical, 5)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.44), lineWidth: 0.7)
        }
    }

    private var glyphKind: String {
        switch icon {
        case "quran_audio": return "quran_audio"
        case "fav": return "bookmarks"
        default: return icon
        }
    }
}

struct ReferenceDashboardGlyph: View {
    let kind: String

    var body: some View {
        glyph
    }

    private var glyph: AnyView {
        switch kind {
        case "quran":
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    ZStack {
                        Path { p in
                            p.move(to: CGPoint(x: w * 0.08, y: h * 0.20))
                            p.addQuadCurve(
                                to: CGPoint(x: w * 0.47, y: h * 0.28),
                                control: CGPoint(x: w * 0.28, y: h * 0.13)
                            )
                            p.addLine(to: CGPoint(x: w * 0.47, y: h * 0.86))
                            p.addQuadCurve(
                                to: CGPoint(x: w * 0.08, y: h * 0.74),
                                control: CGPoint(x: w * 0.27, y: h * 0.65)
                            )
                            p.closeSubpath()

                            p.move(to: CGPoint(x: w * 0.92, y: h * 0.20))
                            p.addQuadCurve(
                                to: CGPoint(x: w * 0.53, y: h * 0.28),
                                control: CGPoint(x: w * 0.72, y: h * 0.13)
                            )
                            p.addLine(to: CGPoint(x: w * 0.53, y: h * 0.86))
                            p.addQuadCurve(
                                to: CGPoint(x: w * 0.92, y: h * 0.74),
                                control: CGPoint(x: w * 0.73, y: h * 0.65)
                            )
                            p.closeSubpath()
                        }
                        .fill(SalahTheme.teal)

                        Rectangle()
                            .fill(SalahTheme.cream.opacity(0.86))
                            .frame(width: max(1.2, w * 0.035), height: h * 0.60)
                            .offset(y: h * 0.08)
                    }
                }
            )

        case "quran_audio":
            return AnyView(
                ZStack {
                    ReferenceDashboardGlyph(kind: "quran")
                        .scaleEffect(0.78)
                        .offset(x: -3, y: 1)
                    Image(systemName: "speaker.wave.2.fill")
                        .font(.system(size: 9, weight: .bold))
                        .foregroundStyle(SalahTheme.gold)
                        .offset(x: 10, y: -9)
                }
            )

        case "bookmarks":
            return AnyView(
                ZStack {
                    RoundedRectangle(cornerRadius: 5, style: .continuous)
                        .fill(SalahTheme.teal)
                        .frame(width: 23, height: 28)
                    Image(systemName: "bookmark.fill")
                        .font(.system(size: 13, weight: .bold))
                        .foregroundStyle(SalahTheme.cream)
                        .offset(y: -1)
                }
            )

        case "dhikr":
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    ZStack {
                        ForEach(0..<10, id: \.self) { index in
                            let angle = Double(index) * 25.0 - 90.0
                            Circle()
                                .fill(SalahTheme.teal)
                                .frame(width: w * 0.14, height: w * 0.14)
                                .offset(
                                    x: cos(angle * .pi / 180.0) * w * 0.26,
                                    y: sin(angle * .pi / 180.0) * h * 0.26
                                )
                        }

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.10, height: h * 0.32)
                            .rotationEffect(.degrees(28))
                            .offset(x: -w * 0.20, y: h * 0.25)
                    }
                }
            )

        case "prayer":
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.18, height: w * 0.18)
                            .offset(y: -h * 0.30)

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.16, height: h * 0.43)
                            .rotationEffect(.degrees(-14))
                            .offset(x: -w * 0.06, y: -h * 0.04)

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.12, height: h * 0.34)
                            .rotationEffect(.degrees(72))
                            .offset(x: w * 0.12, y: h * 0.18)

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.11, height: h * 0.30)
                            .rotationEffect(.degrees(95))
                            .offset(x: -w * 0.08, y: h * 0.30)

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.66, height: max(3, h * 0.07))
                            .offset(y: h * 0.39)
                    }
                }
            )

        case "wudu":
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    Path { p in
                        p.move(to: CGPoint(x: w * 0.50, y: h * 0.04))
                        p.addCurve(
                            to: CGPoint(x: w * 0.18, y: h * 0.62),
                            control1: CGPoint(x: w * 0.33, y: h * 0.29),
                            control2: CGPoint(x: w * 0.18, y: h * 0.45)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.50, y: h * 0.94),
                            control1: CGPoint(x: w * 0.18, y: h * 0.81),
                            control2: CGPoint(x: w * 0.32, y: h * 0.94)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.82, y: h * 0.62),
                            control1: CGPoint(x: w * 0.68, y: h * 0.94),
                            control2: CGPoint(x: w * 0.82, y: h * 0.81)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.50, y: h * 0.04),
                            control1: CGPoint(x: w * 0.82, y: h * 0.45),
                            control2: CGPoint(x: w * 0.67, y: h * 0.29)
                        )
                    }
                    .fill(SalahTheme.teal)
                }
            )

        case "times":
            return AnyView(
                ZStack {
                    Circle()
                        .stroke(SalahTheme.teal, lineWidth: 3)
                    Rectangle()
                        .fill(SalahTheme.teal)
                        .frame(width: 2.4, height: 10)
                        .offset(y: -5)
                    Rectangle()
                        .fill(SalahTheme.teal)
                        .frame(width: 9, height: 2.4)
                        .offset(x: -4.5)
                }
                .padding(2)
            )

        case "qibla":
            return AnyView(
                ZStack {
                    Circle()
                        .stroke(SalahTheme.teal, lineWidth: 3)
                    Path { p in
                        p.move(to: CGPoint(x: 24, y: 7))
                        p.addLine(to: CGPoint(x: 18, y: 20))
                        p.addLine(to: CGPoint(x: 7, y: 27))
                        p.addLine(to: CGPoint(x: 13, y: 14))
                        p.closeSubpath()
                    }
                    .fill(SalahTheme.teal)
                    .scaleEffect(0.85)
                }
                .padding(2)
            )

        case "calendar":
            return AnyView(
                VStack(spacing: 2) {
                    HStack(spacing: 2) {
                        ForEach(0..<3, id: \.self) { _ in
                            Capsule().frame(width: 5, height: 3)
                        }
                    }
                    .foregroundStyle(SalahTheme.teal)
                    RoundedRectangle(cornerRadius: 4)
                        .stroke(SalahTheme.teal, lineWidth: 2)
                        .frame(width: 26, height: 20)
                    ForEach(0..<5, id: \.self) { index in
                        HStack(spacing: 2) {
                            ForEach(0..<7, id: \.self) { day in
                                Rectangle()
                                    .fill(index == 2 && day == 3 ? SalahTheme.gold : SalahTheme.teal.opacity(0.18))
                                    .frame(width: 2.4, height: 2.8)
                            }
                        }
                    }
                }
            )

        case "checkmark":
            return AnyView(
                ZStack {
                    Circle()
                        .stroke(SalahTheme.teal, lineWidth: 2.6)
                    Path { p in
                        p.move(to: CGPoint(x: 9, y: 12))
                        p.addLine(to: CGPoint(x: 15, y: 19))
                        p.addLine(to: CGPoint(x: 23, y: 7))
                    }
                    .stroke(SalahTheme.teal, style: StrokeStyle(lineWidth: 3, lineCap: .round, lineJoin: .round))
                }
                .padding(2)
            )

        case "settings":
            return AnyView(
                ZStack {
                    Circle()
                        .stroke(SalahTheme.teal, lineWidth: 2.5)
                    ForEach(0..<8, id: \.self) { index in
                        Rectangle()
                            .fill(SalahTheme.teal)
                            .frame(width: 2.5, height: 8)
                            .rotationEffect(.degrees(Double(index) * 45.0))
                            .offset(y: -10)
                    }
                    Circle()
                        .fill(SalahTheme.teal)
                        .frame(width: 10, height: 10)
                }
            )

        case "info":
            return AnyView(
                VStack(spacing: 1) {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: 23, height: 23)
                        Rectangle()
                            .fill(SalahTheme.cream)
                            .frame(width: 3, height: 10)
                            .offset(y: 4)
                    }
                    Capsule()
                        .fill(SalahTheme.teal)
                        .frame(width: 17, height: 5)
                    Capsule()
                        .fill(SalahTheme.teal)
                        .frame(width: 12, height: 3)
                }
            )

        default:
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    Path { p in
                        p.move(to: CGPoint(x: w * 0.50, y: h * 0.90))
                        p.addCurve(
                            to: CGPoint(x: w * 0.08, y: h * 0.36),
                            control1: CGPoint(x: w * 0.19, y: h * 0.69),
                            control2: CGPoint(x: w * 0.04, y: h * 0.53)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.50, y: h * 0.22),
                            control1: CGPoint(x: w * 0.10, y: h * 0.10),
                            control2: CGPoint(x: w * 0.36, y: h * 0.14)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.92, y: h * 0.36),
                            control1: CGPoint(x: w * 0.64, y: h * 0.14),
                            control2: CGPoint(x: w * 0.90, y: h * 0.10)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.50, y: h * 0.90),
                            control1: CGPoint(x: w * 0.96, y: h * 0.53),
                            control2: CGPoint(x: w * 0.81, y: h * 0.69)
                        )
                    }
                    .fill(SalahTheme.teal)
                }
            )
        }
    }
}

private struct PrayerRow: View {
    @EnvironmentObject private var settings: SettingsStore
    let prayer: PrayerOccurrence
    let isNext: Bool

    var body: some View {
        HStack(spacing: 11) {
            Image(systemName: prayer.kind.systemImage)
                .frame(width: 28)
                .foregroundStyle(isNext ? SalahTheme.gold : SalahTheme.teal)
            VStack(alignment: .leading, spacing: 2) {
                HStack(spacing: 6) {
                    Text(prayer.kind.localizedName(settings.language)).font(.subheadline.bold())
                    if isNext {
                        Text(settings.t("NÄCHSTES", "SIRADAKİ"))
                            .font(.system(size: 9, weight: .bold))
                            .padding(.horizontal, 6).padding(.vertical, 3)
                            .background(SalahTheme.gold.opacity(0.18), in: Capsule())
                    }
                }
                Text(prayer.kind.fullSequence(settings.language))
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }
            Spacer()
            Text(timeString(prayer.date, use24Hour: settings.use24Hour, language: settings.language))
                .font(.headline.monospacedDigit())
                .foregroundStyle(SalahTheme.ink)
        }
        .padding(.vertical, 10)
        .contentShape(Rectangle())
    }
}

extension View {
    func salahCard() -> some View {
        self
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(14)
            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 20))
            .overlay { RoundedRectangle(cornerRadius: 20).stroke(SalahTheme.cardStroke(), lineWidth: 1) }
    }
}
