import SwiftUI
import MapKit

struct RootTabView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var selection = 0

    init() {
        let navigation = UINavigationBarAppearance()
        navigation.configureWithOpaqueBackground()
        navigation.backgroundColor = UIColor(red: 36/255, green: 79/255, blue: 77/255, alpha: 1)
        navigation.shadowColor = UIColor(red: 234/255, green: 185/255, blue: 80/255, alpha: 0.28)
        navigation.titleTextAttributes = [.foregroundColor: UIColor.white]
        navigation.largeTitleTextAttributes = [.foregroundColor: UIColor.white]

        let backButton = UIBarButtonItemAppearance()
        backButton.normal.titleTextAttributes = [.foregroundColor: UIColor.white]
        backButton.highlighted.titleTextAttributes = [.foregroundColor: UIColor.white]
        navigation.backButtonAppearance = backButton

        let backIndicator = UIImage(
            systemName: "chevron.left",
            withConfiguration: UIImage.SymbolConfiguration(pointSize: 18, weight: .bold)
        )?.withTintColor(.white, renderingMode: .alwaysOriginal)
        navigation.setBackIndicatorImage(backIndicator, transitionMaskImage: backIndicator)

        UINavigationBar.appearance().standardAppearance = navigation
        UINavigationBar.appearance().scrollEdgeAppearance = navigation
        UINavigationBar.appearance().compactAppearance = navigation
        UINavigationBar.appearance().tintColor = UIColor.white
    }

    var body: some View {
        TabView(selection: $selection) {
            NavigationStack { HomeView() }
                .toolbarBackground(SalahTheme.deepTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(0)

            NavigationStack { QuranView() }
                .toolbarBackground(SalahTheme.deepTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(1)

            NavigationStack { GuideView() }
                .toolbarBackground(SalahTheme.deepTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(2)

            NavigationStack { MoreView() }
                .toolbarBackground(SalahTheme.deepTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(3)

            NavigationStack { SettingsView() }
                .toolbarBackground(SalahTheme.deepTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(4)
        }
        .toolbar(.hidden, for: .tabBar)
        .safeAreaInset(edge: .bottom, spacing: 0) {
            ReferenceBottomBar(selection: $selection)
                .environmentObject(settings)
        }
        .preferredColorScheme(.light)
        .tint(SalahTheme.teal)
    }
}

@MainActor
private final class NearbyMosqueStore: ObservableObject {
    @Published var mapItems: [MKMapItem] = []
    @Published var isLoading = false
    @Published var errorMessage: String?

    func load(around location: CLLocation, query: String) async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        var request = MKLocalSearch.Request()
        request.naturalLanguageQuery = query
        request.resultTypes = .pointOfInterest
        request.region = MKCoordinateRegion(
            center: location.coordinate,
            latitudinalMeters: 20_000,
            longitudinalMeters: 20_000
        )

        do {
            let response = try await MKLocalSearch(request: request).start()
            let origin = location

            mapItems = response.mapItems
                .filter { $0.placemark.location != nil }
                .sorted {
                    let lhs = $0.placemark.location?.distance(from: origin) ?? .greatestFiniteMagnitude
                    let rhs = $1.placemark.location?.distance(from: origin) ?? .greatestFiniteMagnitude
                    return lhs < rhs
                }
        } catch {
            mapItems = []
            errorMessage = error.localizedDescription
        }
    }
}

struct NearbyMosquesView: View {
    @EnvironmentObject private var settings: SettingsStore
    @EnvironmentObject private var locationManager: LocationManager
    @StateObject private var store = NearbyMosqueStore()

    private var taskID: String {
        guard let location = locationManager.location else { return "no-location" }
        let lat = Int((location.coordinate.latitude * 10_000).rounded())
        let lon = Int((location.coordinate.longitude * 10_000).rounded())
        return "\(lat):\(lon):\(settings.language.rawValue)"
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 10) {
                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("Moscheen in der Nähe", "Yakındaki Camiler"), systemImage: "building.columns.fill")
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "SalahPath sucht live in Apple Karten rund um deinen aktuellen oder manuell gewählten Standort. Die Treffer stammen von Apple Maps und werden nicht von SalahPath kuratiert.",
                        "SalahPath, mevcut veya manuel seçtiğin konum çevresinde Apple Haritalar'da canlı arama yapar. Sonuçlar Apple Maps'ten gelir ve SalahPath tarafından düzenlenmez."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)

                if locationManager.location == nil {
                    VStack(spacing: 10) {
                        Image(systemName: "location.slash")
                            .font(.system(size: 30))
                            .foregroundStyle(SalahTheme.mutedInk)

                        Text(settings.t(
                            "Für die Umgebungssuche wird ein Standort benötigt.",
                            "Yakındaki camileri aramak için konum gerekiyor."
                        ))
                        .font(.subheadline)
                        .multilineTextAlignment(.center)

                        Button {
                            locationManager.requestAccessAndStart()
                        } label: {
                            Label(settings.t("Standort verwenden", "Konumu kullan"), systemImage: "location.fill")
                                .font(.headline)
                        }
                        .buttonStyle(.borderedProminent)
                        .tint(SalahTheme.teal)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(18)
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                } else if store.isLoading && store.mapItems.isEmpty {
                    ProgressView(settings.t("Moscheen werden gesucht …", "Camiler aranıyor …"))
                        .padding(24)
                        .frame(maxWidth: .infinity)
                } else if let error = store.errorMessage, store.mapItems.isEmpty {
                    VStack(spacing: 10) {
                        Image(systemName: "wifi.exclamationmark")
                            .font(.system(size: 30))
                            .foregroundStyle(SalahTheme.gold)

                        Text(error)
                            .font(.footnote)
                            .foregroundStyle(.secondary)
                            .multilineTextAlignment(.center)

                        Button(settings.t("Erneut versuchen", "Tekrar dene")) {
                            Task { await reload() }
                        }
                        .buttonStyle(.borderedProminent)
                        .tint(SalahTheme.teal)
                    }
                    .padding(18)
                    .frame(maxWidth: .infinity)
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                } else if store.mapItems.isEmpty {
                    ContentUnavailableView(
                        settings.t("Keine Treffer gefunden", "Sonuç bulunamadı"),
                        systemImage: "building.columns",
                        description: Text(settings.t(
                            "Apple Karten hat in der Umgebung keine passenden Moscheen geliefert.",
                            "Apple Haritalar yakın çevrede uygun cami sonucu döndürmedi."
                        ))
                    )
                } else {
                    ForEach(Array(store.mapItems.enumerated()), id: .offset) { _, item in
                        mosqueRow(item)
                    }
                }
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Moscheen", "Camiler"))
        .navigationBarTitleDisplayMode(.inline)
        .task(id: taskID) {
            if locationManager.location == nil {
                locationManager.requestAccessAndStart()
            }
            await reload()
        }
        .refreshable {
            locationManager.refresh()
            await reload()
        }
    }

    @MainActor
    private func reload() async {
        guard let location = locationManager.location else { return }
        await store.load(
            around: location,
            query: settings.language == .turkish ? "Cami" : "Moschee"
        )
    }

    private func mosqueRow(_ item: MKMapItem) -> some View {
        let origin = locationManager.location
        let distance = origin.flatMap { start in
            item.placemark.location.map { $0.distance(from: start) }
        }

        return VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .top, spacing: 10) {
                Image(systemName: "building.columns.fill")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundStyle(SalahTheme.teal)
                    .frame(width: 34, height: 34)
                    .background(SalahTheme.softTeal, in: Circle())

                VStack(alignment: .leading, spacing: 3) {
                    Text(item.name ?? settings.t("Moschee", "Cami"))
                        .font(.headline)
                        .foregroundStyle(SalahTheme.ink)

                    if let address = item.placemark.title, !address.isEmpty {
                        Text(address)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                            .fixedSize(horizontal: false, vertical: true)
                    }

                    if let distance {
                        Text(distanceString(distance))
                            .font(.caption.bold())
                            .foregroundStyle(SalahTheme.deepTeal)
                    }
                }

                Spacer(minLength: 0)
            }

            Button {
                item.openInMaps()
            } label: {
                Label(settings.t("In Apple Karten öffnen", "Apple Haritalar'da aç"), systemImage: "map.fill")
                    .font(.subheadline.bold())
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
            .tint(SalahTheme.teal)
        }
        .padding(12)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 15, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
        }
    }

    private func distanceString(_ meters: CLLocationDistance) -> String {
        if meters < 1_000 {
            return String(format: "%.0f m", meters)
        }
        return String(format: "%.1f km", meters / 1_000)
    }
}

private struct ReferenceBottomBar: View {
    @EnvironmentObject private var settings: SettingsStore
    @Binding var selection: Int

    private var items: [(String, String)] {
        [
            ("sp_icon_home", settings.t("Start", "Ana Sayfa")),
            ("sp_icon_quran", settings.t("Koran", "Kur'an")),
            ("sp_icon_prayer", settings.t("Gebet", "Namaz")),
            ("sp_icon_calendar", settings.t("Entdecken", "Keşfet")),
            ("sp_icon_settings", settings.t("Profil", "Profil"))
        ]
    }

    var body: some View {
        HStack(spacing: 0) {
            ForEach(Array(items.enumerated()), id: \.offset) { index, item in
                Button {
                    withAnimation(.easeOut(duration: 0.16)) {
                        selection = index
                    }
                } label: {
                    VStack(spacing: 3) {
                        ZStack {
                            if selection == index {
                                Capsule()
                                    .fill(SalahTheme.teal.opacity(0.10))
                                    .frame(width: 39, height: 24)
                            }
                            Image(item.0)
                                .resizable()
                                .scaledToFit()
                                .frame(
                                    width: (item.0 == "sp_icon_quran" || item.0 == "sp_icon_prayer") ? 17 : 20,
                                    height: (item.0 == "sp_icon_quran" || item.0 == "sp_icon_prayer") ? 17 : 20
                                )
                                .frame(width: 20, height: 20)
                                .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                        }
                        .frame(height: 22)

                        Text(item.1)
                            .font(.system(size: 7.7, weight: selection == index ? .bold : .semibold))
                            .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                            .lineLimit(1)
                            .minimumScaleFactor(0.72)

                        Circle()
                            .fill(selection == index ? SalahTheme.gold : Color.clear)
                            .frame(width: 3.5, height: 3.5)
                    }
                    .frame(maxWidth: .infinity)
                    .contentShape(Rectangle())
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 5)
        .padding(.top, 5)
        .padding(.bottom, 2)
        .background {
            SalahTheme.cream
                .overlay(alignment: .top) {
                    Rectangle()
                        .fill(SalahTheme.gold.opacity(0.42))
                        .frame(height: 0.7)
                }
                .ignoresSafeArea(edges: .bottom)
        }
        .shadow(color: SalahTheme.deepTeal.opacity(0.08), radius: 7, y: -2)
    }
}

struct MoreView: View {
    @EnvironmentObject private var settings: SettingsStore
    @EnvironmentObject private var locationManager: LocationManager

    private let columns = [
        GridItem(.flexible(), spacing: 7),
        GridItem(.flexible(), spacing: 7)
    ]

    var body: some View {
        ScrollView {
            VStack(spacing: 8) {
                discoverHero

                LazyVGrid(columns: columns, spacing: 7) {
                    NavigationLink { MorningEveningAdhkarView() } label: {
                        discoverTile(icon: "hands.sparkles.fill", title: settings.t("Dua & Dhikr", "Dua & Zikir"), subtitle: settings.t("Morgen & Abend", "Sabah & Akşam"))
                    }
                    NavigationLink { DhikrView() } label: {
                        discoverTile(icon: "circle.grid.cross.fill", title: settings.t("Dhikr & Tasbih", "Zikir & Tesbih"), subtitle: settings.t("Zähler", "Sayaç"))
                    }
                    NavigationLink { QuranicDuaLibraryView() } label: {
                        discoverTile(icon: "text.book.closed.fill", title: settings.t("Dua-Sammlung", "Dua Koleksiyonu"), subtitle: settings.t("Quranische Duas", "Kur'an duaları"))
                    }
                    NavigationLink { FastingTrackerView() } label: {
                        discoverTile(
                            icon: "moon.stars.fill",
                            title: settings.t("Fasten & Ramadan", "Oruç & Ramazan"),
                            subtitle: settings.t("Lernen & Tracker", "Öğren & takip")
                        )
                    }
                    NavigationLink { IslamLearningHubView() } label: {
                        discoverTile(icon: "book.pages.fill", title: settings.t("Islam lernen", "İslâm'ı Öğren"), subtitle: settings.t("Von den Grundlagen", "Temelden başla"))
                    }
                    NavigationLink { PrayerHowToView() } label: {
                        discoverTile(icon: "figure.mind.and.body", title: settings.t("Gebet lernen", "Namaz Öğren"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))
                    }
                    NavigationLink { WuduGuideView() } label: {
                        discoverTile(icon: "drop.fill", title: settings.t("Wudu", "Abdest Rehberi"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))
                    }
                    NavigationLink { ShortSurahLearningView() } label: {
                        discoverTile(icon: "play.square.stack.fill", title: settings.t("Kurze Suren", "Kısa Sûreler"), subtitle: settings.t("Lernen & hören", "Öğren & dinle"))
                    }
                    NavigationLink { PrayerDuaAudioView() } label: {
                        discoverTile(icon: "text.book.closed.fill", title: settings.t("Gebetsduas", "Namaz Duaları"), subtitle: settings.t("Lesen & lernen", "Oku & öğren"))
                    }
                    NavigationLink { PrayerDebtTrackerView() } label: {
                        discoverTile(icon: "clock.arrow.circlepath", title: settings.t("Qada-Tracker", "Kaza Takibi"), subtitle: settings.t("Gebet & Fasten", "Namaz & oruç"))
                    }
                    NavigationLink { ThirtyTwoFardView() } label: {
                        discoverTile(icon: "checklist", title: "32 Farz", subtitle: settings.t("Kompakter Lernzettel", "Kısa öğrenme özeti"))
                    }
                    NavigationLink { NearbyMosquesView() } label: {
                        discoverTile(
                            icon: "building.columns.fill",
                            title: settings.t("Moscheen in der Nähe", "Yakındaki Camiler"),
                            subtitle: settings.t("Mit Apple Karten", "Apple Haritalar ile")
                        )
                    }
                }
                .buttonStyle(.plain)

                VStack(spacing: 0) {
                    NavigationLink { QiblaView() } label: {
                        discoverRow(icon: "location.north.circle.fill", title: settings.t("Qibla", "Kıble"), subtitle: settings.t("Richtung zur Kaaba", "Kâbe yönü"))
                    }
                    NavigationLink { HijriCalendarView() } label: {
                        discoverRow(icon: "calendar", title: settings.t("Hijri-Kalender", "Hicrî Takvim"), subtitle: settings.t("Islamischer Kalender", "İslami takvim"))
                    }
                    NavigationLink { TrackerPauseView() } label: {
                        discoverRow(icon: "pause.circle.fill", title: settings.t("Tracker-Pause", "Takip Duraklatma"), subtitle: settings.t("Neutral im Streak", "Seride nötr"))
                    }
                }
                .buttonStyle(.plain)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 16).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }

                featureStrip

                VStack(spacing: 3) {
                    Text(settings.t("Kleine Schritte bringen große Veränderungen.", "Küçük adımlar, büyük değişimler getirir."))
                        .font(.system(size: 11.5, weight: .bold, design: .serif))
                        .foregroundStyle(SalahTheme.deepTeal)
                        .multilineTextAlignment(.center)
                    Text(settings.t("LERNEN  ·  ANWENDEN  ·  DRANBLEIBEN  ·  NÄHER ZU ALLAH", "ÖĞREN  ·  UYGULA  ·  İSTİKRAR ET  ·  DAİMA DAHA YAKIN"))
                        .font(.system(size: 7.4, weight: .bold))
                        .foregroundStyle(SalahTheme.gold)
                        .multilineTextAlignment(.center)
                        .minimumScaleFactor(0.78)
                }
                .padding(.vertical, 10)
                .frame(maxWidth: .infinity)
                .background(SalahTheme.deepTeal, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.gold.opacity(0.55), lineWidth: 1) }
            }
            .padding(.horizontal, 11)
            .padding(.vertical, 10)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Entdecken", "Keşfet"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }

    private var discoverHero: some View {
        ZStack(alignment: .bottomTrailing) {
            LinearGradient(
                colors: [SalahTheme.deepTeal, SalahTheme.teal],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            HStack(spacing: 7) {
                Image(systemName: "building.columns.fill")
                    .font(.system(size: 26))
                Image(systemName: "moon.stars.fill")
                    .font(.system(size: 19))
                Image(systemName: "sparkles")
                    .font(.system(size: 14))
            }
            .foregroundStyle(SalahTheme.gold.opacity(0.34))
            .padding(.trailing, 10)
            .padding(.bottom, 8)

            HStack(spacing: 11) {
                ZStack {
                    RoundedRectangle(cornerRadius: 13, style: .continuous)
                        .fill(Color.white.opacity(0.08))
                        .frame(width: 50, height: 50)
                    RoundedRectangle(cornerRadius: 13, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.65), lineWidth: 1)
                        .frame(width: 50, height: 50)
                    Image(systemName: "safari.fill")
                        .font(.system(size: 23, weight: .semibold))
                        .foregroundStyle(SalahTheme.gold)
                }

                VStack(alignment: .leading, spacing: 3) {
                    Text(settings.t("Entdecken", "Keşfet"))
                        .font(.system(size: 22, weight: .bold, design: .serif))
                        .foregroundStyle(.white)
                    Text(settings.t("Deine islamische All-in-One Begleitung", "İslami hepsi bir arada rehberin"))
                        .font(.system(size: 9.5, weight: .semibold))
                        .foregroundStyle(.white.opacity(0.82))
                    Text(settings.t("Lernen · anwenden · dranbleiben", "Öğren · uygula · istikrar et"))
                        .font(.system(size: 8.5, weight: .bold))
                        .foregroundStyle(SalahTheme.gold)
                }

                Spacer()
            }
            .padding(13)
        }
        .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.58), lineWidth: 1) }
    }

    @ViewBuilder
    private func salahFeatureIcon(_ symbol: String, size: CGFloat) -> some View {
        if let asset = discoverAssetName(for: symbol) {
            Image(asset)
                .resizable()
                .scaledToFit()
                .frame(
                    width: (asset == "sp_icon_quran" || asset == "sp_icon_prayer") ? size * 0.82 : size,
                    height: (asset == "sp_icon_quran" || asset == "sp_icon_prayer") ? size * 0.82 : size
                )
                .frame(width: size, height: size)
                .accessibilityHidden(true)
        } else if let glyphKind = discoverDashboardGlyphKind(for: symbol) {
            ReferenceDashboardGlyph(kind: glyphKind)
                .frame(width: size * 0.82, height: size * 0.82)
                .frame(width: size, height: size)
                .accessibilityHidden(true)
        } else {
            ZStack {
                RoundedRectangle(cornerRadius: size * 0.28, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [SalahTheme.softTeal, SalahTheme.cream],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: size, height: size)

                RoundedRectangle(cornerRadius: size * 0.28, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.52), lineWidth: 1)
                    .frame(width: size, height: size)

                Circle()
                    .fill(Color.white.opacity(0.64))
                    .frame(width: size * 0.66, height: size * 0.66)

                Image(systemName: symbol)
                    .symbolRenderingMode(.hierarchical)
                    .font(.system(size: size * 0.38, weight: .semibold))
                    .foregroundStyle(SalahTheme.deepTeal)
                    .frame(width: size * 0.72, height: size * 0.72)

                Circle()
                    .fill(SalahTheme.gold)
                    .frame(width: max(5, size * 0.14), height: max(5, size * 0.14))
                    .overlay {
                        Circle().stroke(Color.white.opacity(0.90), lineWidth: 1)
                    }
                    .offset(x: size * 0.31, y: -size * 0.31)
            }
            .accessibilityHidden(true)
        }
    }

    private func discoverAssetName(for symbol: String) -> String? {
        switch symbol {
        // Keep only the supplied assets that are clean at larger sizes.
        // The remaining Discover entries use the cut-safe vector/SF fallback below.
        case "text.book.closed.fill":
            return "sp_icon_quran"
        case "figure.mind.and.body":
            return "sp_icon_prayer"
        case "drop.fill":
            return "sp_icon_wudu"
        case "play.square.stack.fill":
            return "sp_icon_quran_audio"
        case "calendar":
            return "sp_icon_calendar"
        case "pause.circle.fill":
            return "sp_icon_progress"
        default:
            return nil
        }
    }

    private func discoverDashboardGlyphKind(for symbol: String) -> String? {
        switch symbol {
        case "hands.sparkles.fill", "circle.grid.cross.fill":
            return "dhikr"
        case "location.north.circle.fill":
            return "qibla"
        default:
            return nil
        }
    }

    private func discoverTile(icon: String, title: String, subtitle: String) -> some View {
        VStack(spacing: 5) {
            salahFeatureIcon(icon, size: 38)

            Text(title)
                .font(.system(size: 11.5, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .multilineTextAlignment(.center)
                .lineLimit(2)

            Text(subtitle)
                .font(.system(size: 8.5, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)
                .lineLimit(2)
        }
        .frame(maxWidth: .infinity, minHeight: 94)
        .padding(7)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1) }
    }

    private func discoverRow(icon: String, title: String, subtitle: String) -> some View {
        HStack(spacing: 10) {
            salahFeatureIcon(icon, size: 30)

            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.system(size: 12, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                Text(subtitle)
                    .font(.system(size: 9, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
            }

            Spacer()

            Image(systemName: "chevron.right")
                .font(.caption.bold())
                .foregroundStyle(SalahTheme.teal)
        }
        .padding(.horizontal, 11)
        .padding(.vertical, 8)
        .contentShape(Rectangle())
        .overlay(alignment: .bottom) { Divider().padding(.leading, 54).opacity(0.34) }
    }

    private var featureStrip: some View {
        HStack(spacing: 6) {
            featureMini(icon: "drop.fill", title: settings.t("Wudu Schritt für Schritt", "Abdest adım adım"))
            featureMini(icon: "character.book.closed.fill", title: settings.t("Deutsch + Türkisch", "Almanca + Türkçe"))
            featureMini(icon: "ellipsis.circle.fill", title: settings.t("Und mehr", "Daha Fazlası"))
        }
    }

    private func featureMini(icon: String, title: String) -> some View {
        VStack(spacing: 5) {
            salahFeatureIcon(icon, size: 23)
            Text(title)
                .font(.system(size: 7.5, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .multilineTextAlignment(.center)
                .lineLimit(2)
                .minimumScaleFactor(0.75)
        }
        .frame(maxWidth: .infinity, minHeight: 62)
        .padding(.horizontal, 5)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 12).stroke(SalahTheme.gold.opacity(0.33), lineWidth: 1) }
    }
}
