from pathlib import Path
import re

root = Path('SalahZeit')

# ---------- Location: friendly city/area label, never persist coordinates ----------
p = root / 'Services' / 'LocationManager.swift'
s = p.read_text(encoding='utf-8')
s = s.replace('@Published private(set) var lastError: String?\n\n    private let manager = CLLocationManager()', '@Published private(set) var lastError: String?\n    @Published private(set) var locality: String?\n\n    private let manager = CLLocationManager()\n    private let geocoder = CLGeocoder()\n    private var lastGeocodedLocation: CLLocation?')
s = s.replace('''        Task { @MainActor in\n            self.location = newest\n            self.lastError = nil\n        }''', '''        Task { @MainActor in\n            self.location = newest\n            self.lastError = nil\n            self.updateLocalityIfNeeded(for: newest)\n        }''')
insert = '''\n    private func updateLocalityIfNeeded(for location: CLLocation) {\n        if let lastGeocodedLocation, lastGeocodedLocation.distance(from: location) < 1_000, locality != nil { return }\n        lastGeocodedLocation = location\n        Task {\n            do {\n                let placemarks = try await geocoder.reverseGeocodeLocation(location)\n                guard let placemark = placemarks.first else { return }\n                let value = placemark.locality ?? placemark.subLocality ?? placemark.administrativeArea ?? placemark.country\n                if let value, !value.isEmpty { locality = value }\n            } catch {\n                // Prayer time calculation must continue even when reverse geocoding is unavailable.\n            }\n        }\n    }\n'''
s = s.replace('\n    nonisolated func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {', insert + '\n    nonisolated func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {')
p.write_text(s, encoding='utf-8')

# ---------- Home: native visual overhaul based on user's SalahPath references ----------
p = root / 'Views' / 'HomeView.swift'
s = p.read_text(encoding='utf-8')
if 'import UIKit' not in s:
    s = s.replace('import CoreLocation\n', 'import CoreLocation\nimport UIKit\n')
prefix = s.split('struct HomeView: View {', 1)[0]
new_tail = r'''enum SalahTheme {
    static let teal = Color(red: 0.015, green: 0.34, blue: 0.32)
    static let deepTeal = Color(red: 0.012, green: 0.22, blue: 0.22)
    static let gold = Color(red: 0.78, green: 0.61, blue: 0.25)
    static let cream = Color(uiColor: UIColor { traits in
        traits.userInterfaceStyle == .dark
            ? UIColor(red: 0.10, green: 0.15, blue: 0.15, alpha: 1)
            : UIColor(red: 0.985, green: 0.965, blue: 0.89, alpha: 1)
    })
    static let page = Color(uiColor: UIColor { traits in
        traits.userInterfaceStyle == .dark
            ? UIColor(red: 0.035, green: 0.075, blue: 0.075, alpha: 1)
            : UIColor(red: 0.945, green: 0.93, blue: 0.84, alpha: 1)
    })
    static let ink = Color(uiColor: UIColor { traits in
        traits.userInterfaceStyle == .dark ? .white : UIColor(red: 0.04, green: 0.14, blue: 0.17, alpha: 1)
    })

    static func cardStroke(_ opacity: Double = 0.34) -> Color { gold.opacity(opacity) }
}

struct HomeView: View {
    @EnvironmentObject private var locationManager: LocationManager
    @EnvironmentObject private var settings: SettingsStore

    @State private var now = Date()
    @State private var selectedPrayer: PrayerOccurrence?
    @State private var trackerRefresh = 0
    @State private var dailyDeenRefresh = 0
    private let engine = PrayerEngine()
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    var body: some View {
        ZStack {
            SalahTheme.page.ignoresSafeArea()
            Group {
                if let location = locationManager.location,
                   let today = engine.calculateDay(for: now, location: location, settings: settings) {
                    prayerContent(location: location, today: today)
                } else {
                    locationState
                }
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar(.hidden, for: .navigationBar)
        .onAppear { locationManager.requestAccessAndStart() }
        .onReceive(timer) { now = $0 }
        .sheet(item: $selectedPrayer) { prayer in
            if let location = locationManager.location,
               let today = engine.calculateDay(for: prayer.date, location: location, settings: settings),
               let tomorrowDate = Calendar.current.date(byAdding: .day, value: 1, to: prayer.date),
               let tomorrow = engine.calculateDay(for: tomorrowDate, location: location, settings: settings) {
                PrayerDetailView(prayer: prayer, day: today, nextDay: tomorrow)
                    .environmentObject(settings)
            }
        }
    }

    @ViewBuilder
    private func prayerContent(location: CLLocation, today: PrayerDay) -> some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                brandHeader

                if let next = engine.nextPrayer(now: now, location: location, settings: settings) {
                    nextPrayerHero(next)
                }

                prayerLegendCard
                dailyDuaCard
                streakCard
                dailyDeenCard
                dashboardGrid
                prayerTimesCard(today: today, location: location)

                if Calendar.current.component(.weekday, from: now) == 6 { fridayCard }
                qiyamCard(today)

                Text(settings.t(
                    "Gebetszeiten sind astronomische Beginnzeiten für deinen aktuellen Standort. Iqāmah- und Jumuʿah-Zeiten einer Moschee sind separate Zeiten.",
                    "Namaz vakitleri mevcut konuma göre astronomik başlangıç vakitleridir. Caminin kamet ve cuma saatleri ayrı vakitlerdir."
                ))
                .font(.caption)
                .foregroundStyle(.secondary)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.horizontal, 4)
            }
            .padding(.horizontal, 14)
            .padding(.top, 10)
            .padding(.bottom, 24)
        }
        .refreshable {
            locationManager.refresh()
            if settings.notificationsEnabled {
                await NotificationManager.shared.scheduleNextSevenDays(location: location, settings: settings)
            }
        }
        .task(id: notificationTaskID(location: location)) {
            if settings.notificationsEnabled {
                await NotificationManager.shared.scheduleNextSevenDays(location: location, settings: settings)
            }
        }
    }

    private var brandHeader: some View {
        HStack(spacing: 12) {
            ZStack {
                RoundedRectangle(cornerRadius: 15)
                    .fill(SalahTheme.gold.opacity(0.16))
                    .frame(width: 48, height: 48)
                Image(systemName: "leaf.fill")
                    .font(.title2)
                    .foregroundStyle(SalahTheme.gold)
            }
            VStack(alignment: .leading, spacing: 2) {
                Text("SalahPath")
                    .font(.system(.title2, design: .serif, weight: .bold))
                    .foregroundStyle(.white)
                Text(settings.t("Ibadetle näher. Schritt für Schritt.", "İbadetle daha yakın. Adım adım."))
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.78))
            }
            Spacer()
            VStack(alignment: .trailing, spacing: 3) {
                Label(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"), systemImage: "location.fill")
                    .font(.caption.bold())
                    .lineLimit(1)
                Text(hijriDateString(now, language: settings.language))
                    .font(.caption2)
                    .opacity(0.8)
            }
            .foregroundStyle(.white)
        }
        .padding(16)
        .background(
            LinearGradient(colors: [SalahTheme.deepTeal, SalahTheme.teal], startPoint: .topLeading, endPoint: .bottomTrailing),
            in: RoundedRectangle(cornerRadius: 24)
        )
        .overlay { RoundedRectangle(cornerRadius: 24).stroke(SalahTheme.gold.opacity(0.65), lineWidth: 1) }
    }

    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Label(settings.t("Nächstes Gebet", "Sıradaki namaz"), systemImage: prayer.kind.systemImage)
                    .font(.caption.bold())
                    .textCase(.uppercase)
                Spacer()
                Text(gregorianDateShort(now))
                    .font(.caption)
            }
            .foregroundStyle(.white.opacity(0.83))

            HStack(alignment: .center, spacing: 12) {
                VStack(alignment: .leading, spacing: 5) {
                    Text(prayer.kind.localizedName(settings.language))
                        .font(.system(size: 30, weight: .bold, design: .rounded))
                    Text(settings.t("in", "kalan"))
                        .font(.caption)
                        .opacity(0.8)
                    Text(countdownString(from: now, to: prayer.date))
                        .font(.system(size: 34, weight: .bold, design: .rounded).monospacedDigit())
                }
                Spacer()
                VStack(alignment: .trailing, spacing: 4) {
                    Text(settings.t("Beginn", "Vakit"))
                        .font(.caption)
                        .opacity(0.8)
                    Text(timeString(prayer.date, use24Hour: settings.use24Hour))
                        .font(.title.bold().monospacedDigit())
                }
            }
            .foregroundStyle(.white)

            VStack(alignment: .leading, spacing: 6) {
                Text(prayer.kind.fullSequence(settings.language))
                    .font(.subheadline.bold())
                    .foregroundStyle(SalahTheme.ink)
                Text(prayer.kind.detailNote(settings.language))
                    .font(.caption)
                    .foregroundStyle(SalahTheme.ink.opacity(0.72))
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(12)
            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15))
        }
        .padding(16)
        .background(
            LinearGradient(colors: [SalahTheme.teal, SalahTheme.deepTeal], startPoint: .topLeading, endPoint: .bottomTrailing),
            in: RoundedRectangle(cornerRadius: 24)
        )
        .overlay { RoundedRectangle(cornerRadius: 24).stroke(SalahTheme.gold.opacity(0.8), lineWidth: 1.2) }
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

    private var dailyDuaCard: some View {
        let dua = DailyDuaStore.item(for: now)
        return VStack(alignment: .leading, spacing: 9) {
            HStack {
                Label(settings.t("Tagesdua", "Günün duası"), systemImage: "sparkles")
                    .font(.headline)
                    .foregroundStyle(SalahTheme.teal)
                Spacer()
                Text(dua.source).font(.caption2.bold()).foregroundStyle(.secondary)
            }
            Text(settings.language == .german ? dua.deTitle : dua.trTitle)
                .font(.subheadline.bold())
            Text(dua.arabic)
                .font(.title2)
                .multilineTextAlignment(.trailing)
                .frame(maxWidth: .infinity, alignment: .trailing)
            Text(dua.transliteration).font(.subheadline.weight(.semibold))
            Text(settings.language == .german ? dua.deMeaning : dua.trMeaning)
                .font(.footnote)
                .foregroundStyle(.secondary)
            if let repetition = dua.repetition {
                Text(repetition).font(.caption.bold()).foregroundStyle(SalahTheme.gold)
            }
        }
        .salahCard()
    }

    private var streakCard: some View {
        let completed = PrayerTrackerStore.completedCount(on: now)
        let streak = PrayerTrackerStore.streak(upTo: now)
        let paused = PrayerTrackerStore.isPaused(now)
        return VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 3) {
                    Text(settings.t("Gebets-Tracking", "Namaz takibi")).font(.headline)
                    Text(settings.t("Motivation ohne Druck.", "Baskı değil, istikrar."))
                        .font(.caption).foregroundStyle(.secondary)
                }
                Spacer()
                HStack(spacing: 6) {
                    Image(systemName: "flame.fill").foregroundStyle(.orange)
                    Text("\(streak)").font(.title3.bold().monospacedDigit())
                    Text(settings.t("Tage", "gün")).font(.caption).foregroundStyle(.secondary)
                }
            }

            HStack(spacing: 8) {
                ForEach(PrayerTrackerStore.requiredKinds) { kind in
                    let done = PrayerTrackerStore.isCompleted(kind, on: now)
                    Button {
                        guard !paused else { return }
                        _ = PrayerTrackerStore.toggle(kind, on: now)
                        trackerRefresh += 1
                    } label: {
                        VStack(spacing: 5) {
                            Image(systemName: done ? "checkmark.circle.fill" : "circle")
                                .font(.title3)
                                .foregroundStyle(done ? SalahTheme.teal : Color.secondary)
                            Text(kind.localizedName(settings.language))
                                .font(.caption2.bold())
                                .lineLimit(1)
                                .minimumScaleFactor(0.62)
                        }
                        .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel("\(kind.localizedName(settings.language)) \(done ? settings.t("erledigt", "tamamlandı") : settings.t("offen", "açık"))")
                }
            }
            if paused {
                Label(settings.t("Tracker heute pausiert", "Takip bugün duraklatıldı"), systemImage: "pause.circle.fill")
                    .font(.caption).foregroundStyle(.secondary)
            } else {
                ProgressView(value: Double(completed), total: 5).tint(SalahTheme.teal)
            }
        }
        .salahCard()
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
                    dailyDeenRefresh += 1
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
        LazyVGrid(columns: [GridItem(.flexible(), spacing: 10), GridItem(.flexible(), spacing: 10)], spacing: 10) {
            NavigationLink { QuranView() } label: { DashboardTile(title: settings.t("Quran", "Kur'an"), subtitle: settings.t("Lesen & hören", "Oku & dinle"), icon: "book.fill") }
            NavigationLink { MorningEveningAdhkarView() } label: { DashboardTile(title: settings.t("Dua & Dhikr", "Dua & Zikir"), subtitle: settings.t("Morgen & Abend", "Sabah & akşam"), icon: "hands.sparkles.fill") }
            NavigationLink { PrayerHowToView() } label: { DashboardTile(title: settings.t("Namaz lernen", "Namaz öğren"), subtitle: settings.t("Mann & Frau", "Erkek & kadın"), icon: "figure.stand") }
            NavigationLink { WuduGuideView() } label: { DashboardTile(title: settings.t("Wudu", "Abdest"), subtitle: settings.t("Schritt für Schritt", "Adım adım"), icon: "drop.fill") }
            NavigationLink { RakatOverviewView() } label: { DashboardTile(title: settings.t("Gebetszeiten", "Namaz vakitleri"), subtitle: settings.t("Fard · Sunnah · Witr", "Farz · sünnet · vitir"), icon: "clock.fill") }
            NavigationLink { QiblaView() } label: { DashboardTile(title: settings.t("Qibla", "Kıble"), subtitle: settings.t("Kompass", "Pusula"), icon: "location.north.circle.fill") }
            NavigationLink { PrayerTermsView() } label: { DashboardTile(title: settings.t("Islamisches Wissen", "İslami bilgiler"), subtitle: settings.t("Begriffe verstehen", "Kavramları öğren"), icon: "lightbulb.fill") }
            NavigationLink { QuranView() } label: { DashboardTile(title: settings.t("Favoriten", "Favoriler"), subtitle: settings.t("Quran-Lesezeichen", "Kur'an işaretleri"), icon: "heart.fill") }
        }
        .buttonStyle(.plain)
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
                    valueRow(settings.t("Mitte der Nacht", "Gecenin yarısı"), timeString(middle, use24Hour: settings.use24Hour))
                }
                if let lastThird = day.lastThirdOfNight {
                    valueRow(settings.t("Letztes Drittel beginnt", "Son üçte birlik bölüm başlar"), timeString(lastThird, use24Hour: settings.use24Hour))
                }
            }
            .salahCard()
        }
    }

    private func valueRow(_ title: String, _ value: String) -> some View {
        HStack { Text(title).font(.subheadline); Spacer(); Text(value).font(.subheadline.bold().monospacedDigit()) }
    }

    private var locationState: some View {
        ContentUnavailableView {
            Label(settings.t("Standort benötigt", "Konum gerekli"), systemImage: "location.slash")
        } description: {
            Text(settings.t(
                "SalahPath benötigt deinen Standort nur für Gebetszeiten und Qibla. Exakte Koordinaten werden nicht auf dem Dashboard angezeigt.",
                "SalahPath konumunu yalnızca namaz vakitleri ve kıble için kullanır. Kesin koordinatlar ana ekranda gösterilmez."
            ))
        } actions: {
            Button(settings.t("Standort erlauben", "Konuma izin ver")) { locationManager.requestAccessAndStart() }
                .buttonStyle(.borderedProminent)
                .tint(SalahTheme.teal)
        }
    }

    private func isNext(_ prayer: PrayerOccurrence, location: CLLocation) -> Bool {
        guard let next = engine.nextPrayer(now: now, location: location, settings: settings) else { return false }
        return prayer.kind == next.kind && Calendar.current.isDate(prayer.date, inSameDayAs: next.date)
    }

    private func notificationTaskID(location: CLLocation) -> String {
        let lat = Int((location.coordinate.latitude * 10).rounded())
        let lon = Int((location.coordinate.longitude * 10).rounded())
        return "\(lat)-\(lon)-\(settings.calculationPreset.rawValue)-\(settings.asrRule.rawValue)-\(settings.notificationLeadMinutes)-\(settings.notificationsEnabled)"
    }

    private func gregorianDateShort(_ date: Date) -> String {
        let f = DateFormatter(); f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR"); f.dateFormat = "dd.MM.yyyy"
        return f.string(from: date)
    }
}

private struct DashboardTile: View {
    let title: String
    let subtitle: String
    let icon: String

    var body: some View {
        VStack(alignment: .leading, spacing: 9) {
            ZStack {
                Circle().fill(SalahTheme.teal.opacity(0.11)).frame(width: 38, height: 38)
                Image(systemName: icon).foregroundStyle(SalahTheme.teal).font(.headline)
            }
            Text(title).font(.subheadline.bold()).foregroundStyle(SalahTheme.ink)
            Text(subtitle).font(.caption2).foregroundStyle(.secondary).lineLimit(2)
        }
        .frame(maxWidth: .infinity, minHeight: 104, alignment: .leading)
        .padding(12)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 18))
        .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.cardStroke(0.34), lineWidth: 1) }
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
            Text(timeString(prayer.date, use24Hour: settings.use24Hour))
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
'''
p.write_text(prefix + new_tail, encoding='utf-8')

# ---------- Root tabs / discover / profile ----------
p = root / 'Views' / 'RootTabView.swift'
p.write_text(r'''import SwiftUI

struct RootTabView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        TabView {
            NavigationStack { HomeView() }
                .tabItem { Label(settings.t("Start", "Ana sayfa"), systemImage: "house.fill") }

            NavigationStack { QuranView() }
                .tabItem { Label(settings.t("Quran", "Kur'an"), systemImage: "book.fill") }

            NavigationStack { GuideView() }
                .tabItem { Label(settings.t("Namaz", "Namaz"), systemImage: "figure.stand") }

            NavigationStack { MoreView() }
                .tabItem { Label(settings.t("Entdecken", "Keşfet"), systemImage: "safari.fill") }

            NavigationStack { SettingsView() }
                .tabItem { Label(settings.t("Profil", "Profil"), systemImage: "person.crop.circle.fill") }
        }
        .tint(SalahTheme.teal)
    }
}

struct MoreView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section(settings.t("Täglich", "Günlük")) {
                NavigationLink { MorningEveningAdhkarView() } label: { Label(settings.t("Morgen & Abend Adhkar", "Sabah & Akşam Ezkârı"), systemImage: "sun.and.horizon.fill") }
                NavigationLink { DhikrView() } label: { Label(settings.t("Dhikr & Tasbih", "Zikir & Tesbih"), systemImage: "circle.grid.cross.fill") }
                NavigationLink { QuranicDuaLibraryView() } label: { Label(settings.t("Dua-Sammlung", "Dua koleksiyonu"), systemImage: "hands.sparkles.fill") }
                NavigationLink { FastingTrackerView() } label: { Label(settings.t("Fasten-Tracker", "Oruç takibi"), systemImage: "moon.fill") }
            }

            Section(settings.t("Lernen", "Öğren")) {
                NavigationLink { PrayerHowToView() } label: { Label(settings.t("Gebet Schritt für Schritt", "Namaz adım adım"), systemImage: "figure.stand") }
                NavigationLink { WuduGuideView() } label: { Label(settings.t("Wudu / Abdest", "Abdest"), systemImage: "drop.fill") }
                NavigationLink { ShortSurahLearningView() } label: { Label(settings.t("Suren lernen", "Sure öğren"), systemImage: "play.square.stack") }
                NavigationLink { PrayerDuaAudioView() } label: { Label(settings.t("Gebetsduas", "Namaz duaları"), systemImage: "text.book.closed.fill") }
            }

            Section(settings.t("Werkzeuge", "Araçlar")) {
                NavigationLink { QiblaView() } label: { Label(settings.t("Qibla-Kompass", "Kıble pusulası"), systemImage: "location.north.circle.fill") }
                NavigationLink { HijriCalendarView() } label: { Label(settings.t("Hicri-Kalender", "Hicrî takvim"), systemImage: "calendar") }
                NavigationLink { TrackerPauseView() } label: { Label(settings.t("Tracker-Pause", "Takip duraklatma"), systemImage: "pause.circle") }
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Entdecken", "Keşfet"))
        .tint(SalahTheme.teal)
    }
}
''', encoding='utf-8')

# ---------- Audio robustness + Guide/Quran styling ----------
p = root / 'Views' / 'GuideView.swift'
s = p.read_text(encoding='utf-8')
start = s.index('@MainActor\nfinal class RemoteAudioPlayer')
end = s.index('\nprivate struct AudioEditionResponse', start)
new_audio = r'''@MainActor
final class RemoteAudioPlayer: ObservableObject {
    @Published var activeURL: URL?
    @Published var isPlaying = false
    @Published var isLoading = false
    @Published var lastError: String?
    @Published var queueIndex = 0
    @Published var queueCount = 0

    private var player: AVPlayer?
    private var queueURLs: [URL] = []
    private var statusObservation: NSKeyValueObservation?
    private var timeControlObservation: NSKeyValueObservation?
    private var endObserver: NSObjectProtocol?
    private var failedObserver: NSObjectProtocol?

    var hasNext: Bool { queueIndex + 1 < queueURLs.count }
    var hasPrevious: Bool { queueIndex > 0 }

    func toggle(_ url: URL) {
        if activeURL == url, let player {
            if isPlaying { player.pause() } else { lastError = nil; player.play() }
            return
        }
        playQueue([url])
    }

    func play(_ url: URL) { playQueue([url]) }

    func playQueue(_ urls: [URL]) {
        let cleaned = urls.filter { $0.scheme?.lowercased() == "https" }
        guard !cleaned.isEmpty else {
            stop()
            lastError = "Keine sichere Audiodatei verfügbar."
            return
        }
        queueURLs = cleaned
        queueCount = cleaned.count
        queueIndex = 0
        loadCurrentAndPlay()
    }

    func next() {
        guard hasNext else { return }
        queueIndex += 1
        loadCurrentAndPlay()
    }

    func previous() {
        guard hasPrevious else { return }
        queueIndex -= 1
        loadCurrentAndPlay()
    }

    func stop() {
        player?.pause()
        isPlaying = false
        isLoading = false
    }

    private func loadCurrentAndPlay() {
        guard queueURLs.indices.contains(queueIndex) else { return }
        removeObservers()
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .spokenAudio, options: [.allowAirPlay, .allowBluetoothA2DP])
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            lastError = error.localizedDescription
            isLoading = false
            isPlaying = false
            return
        }

        lastError = nil
        isLoading = true
        isPlaying = false
        let url = queueURLs[queueIndex]
        activeURL = url
        let item = AVPlayerItem(url: url)
        let newPlayer = AVPlayer(playerItem: item)
        player = newPlayer

        statusObservation = item.observe(\.status, options: [.initial, .new]) { [weak self] item, _ in
            Task { @MainActor in
                guard let self else { return }
                switch item.status {
                case .readyToPlay:
                    self.isLoading = false
                    self.lastError = nil
                case .failed:
                    self.isLoading = false
                    self.isPlaying = false
                    self.lastError = item.error?.localizedDescription ?? "Audio konnte nicht geladen werden."
                default:
                    self.isLoading = true
                }
            }
        }

        timeControlObservation = newPlayer.observe(\.timeControlStatus, options: [.initial, .new]) { [weak self] player, _ in
            Task { @MainActor in
                guard let self else { return }
                self.isPlaying = player.timeControlStatus == .playing
                if player.timeControlStatus == .waitingToPlayAtSpecifiedRate { self.isLoading = true }
                if player.timeControlStatus == .playing { self.isLoading = false }
            }
        }

        endObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: item, queue: .main) { [weak self] _ in
            Task { @MainActor in
                guard let self else { return }
                if self.hasNext { self.next() }
                else { self.isPlaying = false; self.isLoading = false }
            }
        }

        failedObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemFailedToPlayToEndTime, object: item, queue: .main) { [weak self] note in
            Task { @MainActor in
                guard let self else { return }
                self.isLoading = false
                self.isPlaying = false
                let error = note.userInfo?[AVPlayerItemFailedToPlayToEndTimeErrorKey] as? Error
                self.lastError = error?.localizedDescription ?? "Audio-Wiedergabe fehlgeschlagen."
            }
        }

        newPlayer.play()
    }

    private func removeObservers() {
        statusObservation = nil
        timeControlObservation = nil
        if let endObserver { NotificationCenter.default.removeObserver(endObserver) }
        if let failedObserver { NotificationCenter.default.removeObserver(failedObserver) }
        endObserver = nil
        failedObserver = nil
    }
}
'''
s = s[:start] + new_audio + s[end:]

# Network requests: timeout + explicit status validation
s = s.replace('''        let (data, response) = try await URLSession.shared.data(from: url)\n        guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw URLError(.badServerResponse) }''', '''        var request = URLRequest(url: url)\n        request.timeoutInterval = 20\n        let (data, response) = try await URLSession.shared.data(for: request)\n        guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else { throw URLError(.badServerResponse) }''')
# Replace all occurrences of the compact fetch implementation as well
s = s.replace('''            let (data,response)=try await URLSession.shared.data(from:url)\n            guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw URLError(.badServerResponse) }''', '''            var request = URLRequest(url: url); request.timeoutInterval = 20\n            let (data,response)=try await URLSession.shared.data(for: request)\n            guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else { throw URLError(.badServerResponse) }''')
s = s.replace('''        let (data,response)=try await URLSession.shared.data(from:url)\n        guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw URLError(.badServerResponse) }''', '''        var request = URLRequest(url: url); request.timeoutInterval = 20\n        let (data,response)=try await URLSession.shared.data(for: request)\n        guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else { throw URLError(.badServerResponse) }''')

# Salam must be unmistakable: vertical two-step layout, no circular arrows
old_salam = '''private struct PrayerSalamVisual: View {\n    @EnvironmentObject private var settings: SettingsStore\n    var body: some View {\n        HStack(spacing: 10) {\n            VStack(spacing: 8) {\n                Image(systemName: "arrow.right.circle.fill").font(.system(size: 38)).foregroundStyle(Color.accentColor)\n                Text(settings.t("1. RECHTS", "1. SAĞA")).font(.headline)\n                Text(settings.t("Gesicht nach rechts drehen", "Yüzünü sağa çevir")).font(.caption).multilineTextAlignment(.center)\n            }\n            .frame(maxWidth: .infinity)\n            .padding().background(Color.accentColor.opacity(0.08), in: RoundedRectangle(cornerRadius: 14))\n            VStack(spacing: 8) {\n                Image(systemName: "arrow.left.circle.fill").font(.system(size: 38)).foregroundStyle(Color.accentColor)\n                Text(settings.t("2. LINKS", "2. SOLA")).font(.headline)\n                Text(settings.t("Danach Gesicht nach links", "Sonra yüzünü sola çevir")).font(.caption).multilineTextAlignment(.center)\n            }\n            .frame(maxWidth: .infinity)\n            .padding().background(Color.accentColor.opacity(0.08), in: RoundedRectangle(cornerRadius: 14))\n        }\n        .accessibilityElement(children: .combine)\n    }\n}\n'''
new_salam = '''private struct PrayerSalamVisual: View {\n    @EnvironmentObject private var settings: SettingsStore\n\n    var body: some View {\n        VStack(spacing: 12) {\n            salamDirection(\n                number: "1",\n                direction: settings.t("RECHTS", "SAĞA"),\n                icon: "arrow.right",\n                instruction: settings.t("Körper bleibt nach vorn. Drehe nur Kopf und Gesicht deutlich zu deiner eigenen rechten Schulter.", "Gövden öne bakar. Sadece başını ve yüzünü kendi sağ omzuna doğru belirgin şekilde çevir.")\n            )\n            salamDirection(\n                number: "2",\n                direction: settings.t("LINKS", "SOLA"),\n                icon: "arrow.left",\n                instruction: settings.t("Danach wieder durch die Mitte und Kopf/Gesicht deutlich zu deiner eigenen linken Schulter drehen.", "Sonra ortadan geçip başını ve yüzünü kendi sol omzuna doğru belirgin şekilde çevir.")\n            )\n        }\n        .accessibilityElement(children: .contain)\n    }\n\n    private func salamDirection(number: String, direction: String, icon: String, instruction: String) -> some View {\n        VStack(alignment: .leading, spacing: 10) {\n            HStack(spacing: 12) {\n                Text(number).font(.headline.bold()).frame(width: 32, height: 32).background(SalahTheme.gold.opacity(0.2), in: Circle())\n                VStack(alignment: .leading, spacing: 2) {\n                    Text(direction).font(.title2.bold()).foregroundStyle(SalahTheme.teal)\n                    Text(instruction).font(.subheadline)\n                }\n                Spacer()\n                Image(systemName: icon).font(.system(size: 34, weight: .bold)).foregroundStyle(SalahTheme.teal)\n            }\n            Text("السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ")\n                .font(.title3).frame(maxWidth: .infinity, alignment: .trailing)\n            Text("As-salāmu ʿalaykum wa raḥmatullāh").font(.subheadline.bold())\n        }\n        .padding(14)\n        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16))\n        .overlay { RoundedRectangle(cornerRadius: 16).stroke(SalahTheme.cardStroke(), lineWidth: 1) }\n    }\n}\n'''
if old_salam in s:
    s = s.replace(old_salam, new_salam)
else:
    raise SystemExit('PrayerSalamVisual block not found')

# Quran header: real playback state + transport controls
old_header = '''    private var headerSection: some View {\n        VStack(spacing: 8) {\n            Text(surah.name).font(.largeTitle)\n            Text(surah.englishName).font(.title3.bold())\n            Button(action: toggleFullSurah) {\n                Label(\n                    audio.isPlaying ? settings.t("Pause", "Duraklat") : settings.t("Sura anhören", "Sureyi dinle"),\n                    systemImage: audio.isPlaying ? "pause.fill" : "play.fill"\n                )\n            }\n            .buttonStyle(.borderedProminent)\n            Text("\\(settings.quranReciter.title) · AlQuran.cloud / Islamic Network")\n                .font(.caption)\n                .foregroundStyle(.secondary)\n            if let audioError = audio.lastError {\n                Label(audioError, systemImage: "exclamationmark.triangle.fill")\n                    .font(.caption)\n                    .foregroundStyle(.orange)\n            }\n        }\n        .cardStyle(material: true)\n    }\n'''
new_header = '''    private var headerSection: some View {\n        VStack(spacing: 10) {\n            Text(surah.name).font(.largeTitle)\n            Text(surah.englishName).font(.title3.bold())\n\n            HStack(spacing: 18) {\n                Button { audio.previous() } label: { Image(systemName: "backward.fill") }\n                    .disabled(!audio.hasPrevious)\n                Button(action: toggleFullSurah) {\n                    ZStack {\n                        Circle().fill(SalahTheme.teal).frame(width: 52, height: 52)\n                        if audio.isLoading { ProgressView().tint(.white) }\n                        else { Image(systemName: audio.isPlaying ? "pause.fill" : "play.fill").foregroundStyle(.white).font(.title3) }\n                    }\n                }\n                .buttonStyle(.plain)\n                Button { audio.next() } label: { Image(systemName: "forward.fill") }\n                    .disabled(!audio.hasNext)\n            }\n            .font(.title3)\n            .foregroundStyle(SalahTheme.teal)\n\n            if audio.queueCount > 1 {\n                Text("\\(settings.t("Ayah", "Ayet")) \\(audio.queueIndex + 1)/\\(audio.queueCount)")\n                    .font(.caption.bold()).monospacedDigit()\n            }\n            Text("\\(settings.quranReciter.title) · AlQuran.cloud / Islamic Network")\n                .font(.caption)\n                .foregroundStyle(.secondary)\n            if let audioError = audio.lastError {\n                Label(audioError, systemImage: "exclamationmark.triangle.fill")\n                    .font(.caption)\n                    .foregroundStyle(.orange)\n            }\n        }\n        .cardStyle(material: true)\n    }\n'''
if old_header in s:
    s = s.replace(old_header, new_header)
else:
    raise SystemExit('Quran header block not found')

# Highlight currently playing ayah for full-surah playback
old_card_end = '''        .cardStyle()\n        .onAppear {\n            QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)\n        }\n    }\n'''
new_card_end = '''        .cardStyle()\n        .overlay {\n            if audio.queueCount == audioURLs.count, audio.queueCount > 1, audio.queueIndex == index, audio.isPlaying {\n                RoundedRectangle(cornerRadius: 20).stroke(SalahTheme.gold, lineWidth: 2)\n            }\n        }\n        .onAppear {\n            QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)\n        }\n    }\n'''
if old_card_end in s:
    s = s.replace(old_card_end, new_card_end, 1)
else:
    raise SystemExit('Ayah card ending not found')

# Native reference styling across main learning/Quran screens
s = s.replace('.navigationTitle(settings.t("Lernen", "Öğren"))\n    }\n}', '.scrollContentBackground(.hidden)\n        .background(SalahTheme.page)\n        .navigationTitle(settings.t("Lernen", "Öğren"))\n        .tint(SalahTheme.teal)\n    }\n}', 1)
s = s.replace('.navigationTitle(settings.t("Gebet komplett", "Namaz tamamen"))\n        .navigationBarTitleDisplayMode(.inline)', '.background(SalahTheme.page)\n        .navigationTitle(settings.t("Gebet komplett", "Namaz tamamen"))\n        .navigationBarTitleDisplayMode(.inline)')
s = s.replace('.navigationTitle(settings.t("Wudu komplett", "Abdest tamamen"))\n        .navigationBarTitleDisplayMode(.inline)', '.background(SalahTheme.page)\n        .navigationTitle(settings.t("Wudu komplett", "Abdest tamamen"))\n        .navigationBarTitleDisplayMode(.inline)')
s = s.replace('.navigationTitle(settings.t("Quran", "Kur\'an"))\n        .task { await store.loadChapters() }', '.scrollContentBackground(.hidden)\n        .background(SalahTheme.page)\n        .navigationTitle(settings.t("Quran", "Kur\'an"))\n        .task { await store.loadChapters() }')
s = s.replace('''        .navigationTitle(surah.englishName)\n        .navigationBarTitleDisplayMode(.inline)''', '''        .background(SalahTheme.page)\n        .navigationTitle(surah.englishName)\n        .navigationBarTitleDisplayMode(.inline)''')

# Card style matches reference palette instead of generic gray material
old_style = '''private extension View {\n    func cardStyle(material:Bool=false) -> some View {\n        self.frame(maxWidth:.infinity,alignment:.leading)\n            .padding()\n            .background(material ? AnyShapeStyle(.thinMaterial) : AnyShapeStyle(Color(.secondarySystemBackground)), in: RoundedRectangle(cornerRadius:20))\n            .overlay { RoundedRectangle(cornerRadius:20).stroke(Color.secondary.opacity(0.12),lineWidth:1) }\n    }\n}\n'''
new_style = '''private extension View {\n    func cardStyle(material:Bool=false) -> some View {\n        self.frame(maxWidth:.infinity,alignment:.leading)\n            .padding()\n            .background(material ? AnyShapeStyle(SalahTheme.cream.opacity(0.94)) : AnyShapeStyle(SalahTheme.cream), in: RoundedRectangle(cornerRadius:20))\n            .overlay { RoundedRectangle(cornerRadius:20).stroke(SalahTheme.cardStroke(),lineWidth:1) }\n    }\n}\n'''
if old_style in s:
    s = s.replace(old_style, new_style)
else:
    raise SystemExit('cardStyle block not found')

p.write_text(s, encoding='utf-8')

# ---------- Settings and build version ----------
p = Path('scripts/build_unsigned_ipa.sh')
b = p.read_text(encoding='utf-8')
b = re.sub(r'MARKETING_VERSION="[^"]+"', 'MARKETING_VERSION="3.6"', b)
b = re.sub(r'CURRENT_PROJECT_VERSION="[^"]+"', 'CURRENT_PROJECT_VERSION="9"', b)
p.write_text(b, encoding='utf-8')

print('SalahPath v3.6 patch applied')