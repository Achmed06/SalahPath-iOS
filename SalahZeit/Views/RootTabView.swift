import SwiftUI
import UIKit

// Individual SalahPath feature assets are preferred. Missing kinds use native vector glyphs;
// the old sprite-sheet crop fallback is intentionally retired to prevent mis-cropped icons.
struct SalahFeatureIcon: View {
    let kind: String

    private var standaloneUIImage: UIImage? {
        UIImage(named: "feature_\(kind)")
    }

    private var fallbackSymbol: String {
        switch kind {
        case "home", "start", "home_active", "home_inactive": return "house.fill"
        case "prayer", "prayer_active", "prayer_inactive": return "figure.mind.and.body"
        case "wudu", "wudu_active", "wudu_inactive": return "drop.fill"
        case "quran", "quran_active", "quran_inactive": return "book.closed.fill"
        case "discover": return "sparkles"
        case "tracker", "checkmark": return "checkmark.circle.fill"
        case "calendar": return "calendar"
        case "qibla", "qibla_calibration": return "location.north.fill"
        case "settings", "prayer_settings": return "gearshape.fill"
        case "profile": return "person.crop.circle.fill"

        case "fajr": return "sun.horizon.fill"
        case "sunrise": return "sunrise.fill"
        case "dhuhr": return "sun.max.fill"
        case "asr": return "sun.haze.fill"
        case "maghrib": return "sunset.fill"
        case "isha": return "moon.stars.fill"
        case "times", "prayer_schedule", "list": return "clock.fill"
        case "reminder", "notifications": return "bell.fill"
        case "mute": return "speaker.slash.fill"
        case "sound", "quran_audio": return "speaker.wave.2.fill"

        case "mosques": return "building.columns.fill"
        case "duas": return "text.book.closed.fill"
        case "dhikr": return "circle.grid.cross.fill"
        case "hadith": return "text.book.closed.fill"
        case "islamic_knowledge", "knowledge", "info", "sparkles": return "sparkles"
        case "favorites": return "heart.fill"
        case "bookmarks": return "bookmark.fill"
        case "history": return "clock.arrow.circlepath"
        case "downloads": return "arrow.down.circle.fill"

        case "articles": return "doc.text.fill"
        case "courses": return "graduationcap.fill"
        case "videos": return "play.rectangle.fill"
        case "backgrounds": return "photo.fill"
        case "mindfulness": return "leaf.fill"
        case "donations": return "heart.circle.fill"
        case "community": return "person.3.fill"
        case "forum": return "bubble.left.and.bubble.right.fill"
        case "language": return "globe"
        case "islamic_calendar": return "moon.stars.fill"

        case "location": return "location.fill"
        case "map": return "map.fill"
        case "moon", "dark_mode": return "moon.stars.fill"
        case "light_mode": return "sun.max.fill"
        case "font_size": return "textformat.size"
        case "backup": return "externaldrive.fill.badge.timemachine"
        case "sync": return "arrow.triangle.2.circlepath"
        case "back": return "chevron.left"
        case "forward": return "chevron.right"
        case "more": return "ellipsis"
        default: return "sparkles"
        }
    }

    var body: some View {
        GeometryReader { proxy in
            let side = max(1, min(proxy.size.width, proxy.size.height))

            ZStack {
                if let standaloneUIImage {
                    Image(uiImage: standaloneUIImage)
                        .resizable()
                        .interpolation(.high)
                        .scaledToFit()
                } else {
                    Image(systemName: fallbackSymbol)
                        .symbolRenderingMode(.hierarchical)
                        .font(.system(size: side * 0.70, weight: .semibold))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [
                                    SalahTheme.teal,
                                    SalahTheme.deepTeal
                                ],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .shadow(
                            color: side >= 24 ? SalahTheme.deepTeal.opacity(0.16) : .clear,
                            radius: side >= 24 ? 1.5 : 0,
                            y: side >= 24 ? 1 : 0
                        )
                }
            }
            .frame(width: proxy.size.width, height: proxy.size.height)
        }
        .aspectRatio(1, contentMode: .fit)
        .accessibilityHidden(true)
    }
}
func salahPrayerFeatureKind(for kind: PrayerKind) -> String {
    switch kind {
    case .fajr: return "fajr"
    case .sunrise: return "sunrise"
    case .dhuhr: return "dhuhr"
    case .asr: return "asr"
    case .maghrib: return "maghrib"
    case .isha: return "isha"
    }
}

import MapKit

struct RootTabView: View {
    @EnvironmentObject private var settings: SettingsStore
    @ObservedObject private var audio = RemoteAudioPlayer.shared
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
                .toolbarBackground(SalahTheme.navigationTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(0)

            NavigationStack { QuranView() }
                .toolbarBackground(SalahTheme.navigationTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(1)

            NavigationStack { GuideView() }
                .toolbarBackground(SalahTheme.navigationTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(2)

            NavigationStack { MoreView() }
                .toolbarBackground(SalahTheme.navigationTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(3)

            NavigationStack { SettingsView() }
                .toolbarBackground(SalahTheme.navigationTeal, for: .navigationBar)
                .toolbarBackground(.visible, for: .navigationBar)
                .toolbarColorScheme(.dark, for: .navigationBar)
                .tag(4)
        }
        .toolbar(.hidden, for: .tabBar)
        .safeAreaInset(edge: .bottom, spacing: 0) {
            VStack(spacing: 0) {
                if audio.activeURL != nil {
                    GlobalAudioMiniPlayer(audio: audio)
                        .transition(.move(edge: .bottom).combined(with: .opacity))
                }

                ReferenceBottomBar(selection: $selection)
                    .environmentObject(settings)
            }
            .animation(.easeInOut(duration: 0.18), value: audio.activeURL != nil)
        }
        .preferredColorScheme(preferredColorScheme)
        .tint(SalahTheme.teal)
    }

    private var preferredColorScheme: ColorScheme? {
        switch settings.appearance {
        case .system: return nil
        case .light: return .light
        case .dark: return .dark
        }
    }
}

private struct GlobalAudioMiniPlayer: View {
    @ObservedObject var audio: RemoteAudioPlayer

    private var progress: Double {
        guard audio.duration.isFinite, audio.duration > 0 else { return 0 }
        return min(max(audio.currentTime / audio.duration, 0), 1)
    }

    var body: some View {
        VStack(spacing: 0) {
            ProgressView(value: progress)
                .progressViewStyle(.linear)
                .tint(SalahTheme.gold)

            HStack(spacing: 10) {
                ZStack {
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(SalahTheme.softTeal)
                        .frame(width: 42, height: 42)

                    Image("salahpath_logo")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 28, height: 32)
                }
                .accessibilityHidden(true)

                VStack(alignment: .leading, spacing: 2) {
                    Text(audio.displayTitle)
                        .font(.system(size: 12.5, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                        .lineLimit(1)

                    Text(audio.displaySubtitle)
                        .font(.system(size: 9.5, weight: .medium))
                        .foregroundStyle(SalahTheme.mutedInk)
                        .lineLimit(1)
                        .minimumScaleFactor(0.72)
                }

                Spacer(minLength: 4)

                Button {
                    audio.previous()
                } label: {
                    Image(systemName: "backward.fill")
                        .font(.system(size: 13, weight: .semibold))
                        .frame(width: 30, height: 30)
                }
                .buttonStyle(.plain)
                .foregroundStyle(SalahTheme.deepTeal)
                .disabled(!audio.hasPrevious)
                .opacity(audio.hasPrevious ? 1 : 0.35)

                Button {
                    audio.isPlaying ? audio.pause() : audio.resume()
                } label: {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.navigationTeal)
                            .frame(width: 36, height: 36)

                        if audio.isLoading {
                            ProgressView()
                                .controlSize(.small)
                                .tint(.white)
                        } else {
                            Image(systemName: audio.isPlaying ? "pause.fill" : "play.fill")
                                .font(.system(size: 13, weight: .bold))
                                .foregroundStyle(.white)
                        }
                    }
                }
                .buttonStyle(.plain)
                .accessibilityLabel(audio.isPlaying ? "Audio pausieren" : "Audio fortsetzen")

                Button {
                    audio.next()
                } label: {
                    Image(systemName: "forward.fill")
                        .font(.system(size: 13, weight: .semibold))
                        .frame(width: 30, height: 30)
                }
                .buttonStyle(.plain)
                .foregroundStyle(SalahTheme.deepTeal)

                Button {
                    audio.stop()
                } label: {
                    Image(systemName: "xmark")
                        .font(.system(size: 10, weight: .bold))
                        .frame(width: 24, height: 30)
                }
                .buttonStyle(.plain)
                .foregroundStyle(SalahTheme.mutedInk)
                .accessibilityLabel("Audio stoppen")
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 7)
            .background(.ultraThinMaterial)
        }
        .overlay(alignment: .top) {
            Divider().opacity(0.35)
        }
    }
}

@MainActor
private final class NearbyMosqueStore: ObservableObject {
    @Published var mapItems: [MKMapItem] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    private var searchRevision = 0

    func load(around location: CLLocation) async {
        searchRevision &+= 1
        let revision = searchRevision
        isLoading = true
        errorMessage = nil
        defer {
            if revision == searchRevision {
                isLoading = false
            }
        }

        let region = MKCoordinateRegion(
            center: location.coordinate,
            latitudinalMeters: 20_000,
            longitudinalMeters: 20_000
        )
        let queries = ["Moschee", "Mosque", "Cami"]

        var combined: [MKMapItem] = []
        var lastSearchError: Error?

        for query in queries {
            let request = MKLocalSearch.Request()
            request.naturalLanguageQuery = query
            request.resultTypes = .pointOfInterest
            request.region = region

            do {
                let response = try await MKLocalSearch(request: request).start()
                guard revision == searchRevision else { return }
                combined.append(contentsOf: response.mapItems)
            } catch {
                guard revision == searchRevision else { return }
                lastSearchError = error
            }
        }

        guard revision == searchRevision else { return }
        let origin = location
        var seen = Set<String>()

        mapItems = combined
            .filter { $0.placemark.location != nil }
            .filter { item in
                guard let itemLocation = item.placemark.location else { return false }
                let coordinate = itemLocation.coordinate
                let distance = itemLocation.distance(from: origin)

                guard CLLocationCoordinate2DIsValid(coordinate),
                      coordinate.latitude.isFinite,
                      coordinate.longitude.isFinite,
                      distance.isFinite,
                      distance >= 0 else { return false }

                let name = (item.name ?? "").lowercased()
                let lat = Int((coordinate.latitude * 100_000).rounded())
                let lon = Int((coordinate.longitude * 100_000).rounded())
                return seen.insert("\(name)|\(lat)|\(lon)").inserted
            }
            .sorted {
                let lhs = $0.placemark.location?.distance(from: origin) ?? .greatestFiniteMagnitude
                let rhs = $1.placemark.location?.distance(from: origin) ?? .greatestFiniteMagnitude
                return lhs < rhs
            }
            .prefix(30)
            .map { $0 }

        if mapItems.isEmpty, let lastSearchError {
            errorMessage = lastSearchError.localizedDescription
        }
    }
}

struct NearbyMosquesView: View {
    @EnvironmentObject private var settings: SettingsStore
    @EnvironmentObject private var locationManager: LocationManager
    @StateObject private var store = NearbyMosqueStore()

    private var usableLocation: CLLocation? {
        guard let location = locationManager.location else { return nil }
        let coordinate = location.coordinate
        guard coordinate.latitude.isFinite,
              coordinate.longitude.isFinite,
              (-90.0...90.0).contains(coordinate.latitude),
              (-180.0...180.0).contains(coordinate.longitude) else { return nil }
        return location
    }

    private var taskID: String {
        guard let location = usableLocation else {
            return "no-location:\(settings.language.rawValue)"
        }
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
                .padding(14)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 16, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1)
                }

                if usableLocation == nil {
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
                            if locationManager.authorizationStatus == .denied ||
                                locationManager.authorizationStatus == .restricted {
                                openAppSettings()
                            } else {
                                locationManager.useDeviceLocation()
                            }
                        } label: {
                            Label(
                                settings.t(
                                    locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                        ? "iPhone-Einstellungen öffnen"
                                        : "Standort verwenden",
                                    locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                        ? "iPhone ayarlarını aç"
                                        : "Konumu kullan"
                                ),
                                systemImage: locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                    ? "gear"
                                    : "location.fill"
                            )
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
                    VStack(spacing: 12) {
                        ContentUnavailableView(
                            settings.t("Keine Treffer gefunden", "Sonuç bulunamadı"),
                            systemImage: "building.columns",
                            description: Text(settings.t(
                                "Apple Karten hat in der Umgebung keine passenden Moscheen geliefert. Du kannst erneut suchen oder im Profil einen anderen Ort festlegen.",
                                "Apple Haritalar yakın çevrede uygun cami sonucu döndürmedi. Tekrar arayabilir veya profilde başka bir konum belirleyebilirsin."
                            ))
                        )

                        Button {
                            Task { await reload() }
                        } label: {
                            Label(settings.t("Erneut suchen", "Tekrar ara"), systemImage: "arrow.clockwise")
                                .font(.headline)
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.borderedProminent)
                        .tint(SalahTheme.teal)

                        NavigationLink {
                            SettingsView()
                        } label: {
                            Label(settings.t("Anderen Ort festlegen", "Başka konum belirle"), systemImage: "mappin.and.ellipse")
                                .font(.headline)
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                        .tint(SalahTheme.teal)
                    }
                } else {
                    ForEach(Array(store.mapItems.enumerated()), id: \.offset) { _, item in
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
            if usableLocation == nil {
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
        guard let location = usableLocation else { return }
        await store.load(around: location)
    }

    private func openAppSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
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
        guard meters.isFinite, meters >= 0 else { return "—" }
        if meters < 1_000 {
            return String(format: "%.0f m", meters)
        }
        return String(format: "%.1f km", meters / 1_000)
    }
}

// Branded content/navigation artwork uses the same standalone asset family as Start and Discover.
private struct ReferenceBottomBar: View {
    @EnvironmentObject private var settings: SettingsStore
    @Binding var selection: Int

    private struct Item {
        let activeIcon: String
        let inactiveIcon: String
        let title: String
    }

    private var items: [Item] {
        [
            Item(activeIcon: "home_active", inactiveIcon: "home_inactive", title: settings.t("Start", "Ana Sayfa")),
            Item(activeIcon: "quran_active", inactiveIcon: "quran_inactive", title: settings.t("Koran", "Kur'an")),
            Item(activeIcon: "prayer_active", inactiveIcon: "prayer_inactive", title: settings.t("Gebet", "Namaz")),
            Item(activeIcon: "discover", inactiveIcon: "discover", title: settings.t("Entdecken", "Keşfet")),
            Item(activeIcon: "profile", inactiveIcon: "profile", title: settings.t("Profil", "Profil"))
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

                            SalahFeatureIcon(kind: selection == index ? item.activeIcon : item.inactiveIcon)
                                .frame(width: 25, height: 25)
                        }
                        .frame(height: 25)

                        Text(item.title)
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

                discoverSectionTitle(
                    settings.t("Gebet & Gottesdienst", "Namaz & İbadet"),
                    icon: "figure.mind.and.body"
                )

                LazyVGrid(columns: columns, spacing: 7) {
                    NavigationLink { PrayerHowToView() } label: {
                        discoverTile(icon: "figure.mind.and.body", title: settings.t("Gebet lernen", "Namaz Öğren"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))
                    }
                    NavigationLink { PrayerCatalogView() } label: {
                        discoverTile(
                            icon: "rectangle.stack.badge.play.fill",
                            title: settings.t("Alle Gebete", "Tüm Namazlar"),
                            subtitle: settings.t("Jedes Gebet einzeln", "Her namaz ayrı")
                        )
                    }
                    NavigationLink { WuduGuideView() } label: {
                        discoverTile(icon: "drop.fill", title: settings.t("Wudu", "Abdest Rehberi"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))
                    }
                    NavigationLink { PrayerTextsHubView() } label: {
                        discoverTile(
                            icon: "books.vertical.fill",
                            title: settings.t("Gebetstexte", "Namaz Metinleri"),
                            subtitle: settings.t("Suren · Duas · Ayat", "Sûre · dua · ayet")
                        )
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
                }
                .buttonStyle(.plain)

                discoverSectionTitle(
                    settings.t("Quran, Dua & Dhikr", "Kur'an, Dua & Zikir"),
                    icon: "text.book.closed.fill"
                )

                LazyVGrid(columns: columns, spacing: 7) {
                    NavigationLink { QuranDirectoryView() } label: {
                        discoverTile(
                            icon: "books.vertical.fill",
                            title: settings.t("Quran-Verzeichnis", "Kur'an Dizini"),
                            subtitle: settings.t("Suren · Seiten · Juz", "Sûre · sayfa · cüz")
                        )
                    }
                    NavigationLink { ShortSurahLearningView() } label: {
                        discoverTile(icon: "play.square.stack.fill", title: settings.t("Kurze Suren", "Kısa Sûreler"), subtitle: settings.t("Lernen & hören", "Öğren & dinle"))
                    }
                    NavigationLink { MorningEveningAdhkarView() } label: {
                        discoverTile(icon: "hands.sparkles.fill", title: settings.t("Dua & Dhikr", "Dua & Zikir"), subtitle: settings.t("Morgen & Abend", "Sabah & Akşam"))
                    }
                    NavigationLink { DhikrView() } label: {
                        discoverTile(icon: "circle.grid.cross.fill", title: settings.t("Dhikr & Tasbih", "Zikir & Tesbih"), subtitle: settings.t("Zähler", "Sayaç"))
                    }
                    NavigationLink { QuranicDuaLibraryView() } label: {
                        discoverTile(icon: "text.book.closed.fill", title: settings.t("Dua-Sammlung", "Dua Koleksiyonu"), subtitle: settings.t("Quranische Duas", "Kur'an duaları"))
                    }
                }
                .buttonStyle(.plain)

                discoverSectionTitle(
                    settings.t("Lernen & Alltag", "Öğrenme & Günlük Hayat"),
                    icon: "book.pages.fill"
                )

                LazyVGrid(columns: columns, spacing: 7) {
                    NavigationLink { IslamLearningHubView() } label: {
                        discoverTile(icon: "book.pages.fill", title: settings.t("Islam lernen", "İslâm'ı Öğren"), subtitle: settings.t("Von den Grundlagen", "Temelden başla"))
                    }
                    NavigationLink { IlmihalDirectoryView() } label: {
                        discoverTile(
                            icon: "books.vertical.fill",
                            title: "İlmihal",
                            subtitle: settings.t("Glaube · Gottesdienst · Alltag", "İman · ibadet · hayat")
                        )
                    }
                    NavigationLink { EsmaulHusnaView() } label: {
                        discoverTile(
                            icon: "sparkles",
                            title: settings.t("Esmaül Hüsna", "Esmâü'l-Hüsnâ"),
                            subtitle: settings.t("Allahs 99 schöne Namen", "Allah'ın 99 güzel ismi")
                        )
                    }
                    NavigationLink { FourCaliphsView() } label: {
                        discoverTile(
                            icon: "person.3.sequence.fill",
                            title: settings.t("Vier Kalifen", "Dört Halife"),
                            subtitle: settings.t("Leben & frühe Geschichte", "Hayatları & ilk dönem")
                        )
                    }
                    NavigationLink { FarewellSermonView() } label: {
                        discoverTile(
                            icon: "text.quote",
                            title: settings.t("Veda Hutbesi", "Veda Hutbesi"),
                            subtitle: settings.t("Kernaussagen & Quellen", "Ana mesajlar & kaynaklar")
                        )
                    }
                    NavigationLink { RamadanGuideIndexView() } label: {
                        discoverTile(
                            icon: "moon.stars.fill",
                            title: settings.t("Fasten & Ramadan", "Oruç & Ramazan"),
                            subtitle: settings.t("Lernen · Gebete · Tracker", "Öğren · namaz · takip")
                        )
                    }
                    NavigationLink { HajjUmrahGuideView() } label: {
                        discoverTile(
                            icon: "map.fill",
                            title: settings.t("Hajj & Umrah", "Hac & Umre"),
                            subtitle: settings.t("Ablauf · Orte · Duas", "Akış · ziyaret · dualar")
                        )
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

                discoverSectionTitle(
                    settings.t("Werkzeuge", "Araçlar"),
                    icon: "slider.horizontal.3"
                )

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
                .background(SalahTheme.navigationTeal, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
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

    private func discoverSectionTitle(_ title: String, icon: String) -> some View {
        HStack(spacing: 7) {
            Group {
                if let glyphKind = discoverDashboardGlyphKind(for: icon) {
                    SalahFeatureIcon(kind: glyphKind)
                        .padding(4)
                } else {
                    Image(systemName: icon)
                        .font(.system(size: 12, weight: .bold))
                        .foregroundStyle(SalahTheme.gold)
                }
            }
            .frame(width: 24, height: 24)
            .background(SalahTheme.softTeal, in: Circle())
            .overlay { Circle().stroke(SalahTheme.gold.opacity(0.55), lineWidth: 0.8) }
            .accessibilityHidden(true)

            Text(title)
                .font(.system(size: 13, weight: .bold, design: .rounded))
                .foregroundStyle(SalahTheme.deepTeal)

            Spacer()
        }
        .padding(.top, 4)
        .accessibilityAddTraits(.isHeader)
    }

    private var discoverHero: some View {
        ZStack(alignment: .bottomTrailing) {
            LinearGradient(
                colors: [SalahTheme.deepTeal, SalahTheme.teal],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            HStack(spacing: 7) {
                SalahFeatureIcon(kind: "info")
                    .frame(width: 24, height: 24)
                SalahFeatureIcon(kind: "moon")
                    .frame(width: 21, height: 21)
                SalahFeatureIcon(kind: "sparkles")
                    .frame(width: 18, height: 18)
            }
            .opacity(0.42)
            .padding(.trailing, 10)
            .padding(.bottom, 8)
            .accessibilityHidden(true)

            HStack(spacing: 11) {
                ZStack {
                    RoundedRectangle(cornerRadius: 13, style: .continuous)
                        .fill(Color.white.opacity(0.08))
                        .frame(width: 50, height: 50)
                    RoundedRectangle(cornerRadius: 13, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.65), lineWidth: 1)
                        .frame(width: 50, height: 50)
                    SalahFeatureIcon(kind: "discover")
                        .frame(width: 31, height: 31)
                }
                .accessibilityHidden(true)

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
        ZStack {
            RoundedRectangle(cornerRadius: size * 0.30, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [
                            Color.white.opacity(0.98),
                            SalahTheme.cream,
                            SalahTheme.softTeal.opacity(0.62)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: size, height: size)
                .shadow(
                    color: SalahTheme.deepTeal.opacity(0.12),
                    radius: max(2, size * 0.08),
                    y: max(1, size * 0.05)
                )

            RoundedRectangle(cornerRadius: size * 0.30, style: .continuous)
                .stroke(
                    LinearGradient(
                        colors: [
                            SalahTheme.gold.opacity(0.82),
                            SalahTheme.gold.opacity(0.30),
                            SalahTheme.teal.opacity(0.24)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: max(0.8, size * 0.022)
                )
                .frame(width: size, height: size)

            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color.white.opacity(0.98),
                            SalahTheme.cream.opacity(0.94),
                            SalahTheme.softTeal.opacity(0.46)
                        ],
                        center: .topLeading,
                        startRadius: 2,
                        endRadius: size * 0.42
                    )
                )
                .frame(width: size * 0.72, height: size * 0.72)
                .overlay {
                    Circle()
                        .stroke(Color.white.opacity(0.78), lineWidth: max(0.6, size * 0.015))
                }
                .shadow(
                    color: SalahTheme.deepTeal.opacity(0.08),
                    radius: max(1, size * 0.04),
                    y: 1
                )

            Ellipse()
                .fill(Color.white.opacity(0.58))
                .frame(width: size * 0.42, height: size * 0.16)
                .blur(radius: size * 0.025)
                .offset(x: -size * 0.10, y: -size * 0.20)
                .allowsHitTesting(false)

            if let glyphKind = discoverDashboardGlyphKind(for: symbol) {
                SalahFeatureIcon(kind: glyphKind)
                    .frame(width: size * 0.54, height: size * 0.54)
            } else {
                Image(systemName: symbol)
                    .symbolRenderingMode(.hierarchical)
                    .font(.system(size: size * 0.40, weight: .semibold))
                    .foregroundStyle(
                        LinearGradient(
                            colors: [SalahTheme.teal, SalahTheme.deepTeal],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: size * 0.72, height: size * 0.72)
            }

            ZStack {
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [SalahTheme.gold, SalahTheme.gold.opacity(0.72)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                Circle()
                    .stroke(Color.white.opacity(0.92), lineWidth: max(0.8, size * 0.02))
            }
            .frame(width: max(5, size * 0.14), height: max(5, size * 0.14))
            .offset(x: size * 0.31, y: -size * 0.31)
            .shadow(color: SalahTheme.gold.opacity(0.22), radius: 2, y: 1)
        }
        .frame(width: size, height: size)
        .accessibilityHidden(true)
    }

    private func discoverDashboardGlyphKind(for symbol: String) -> String? {
        switch symbol {
        case "figure.mind.and.body":
            return "prayer"
        case "drop.fill":
            return "wudu"
        case "text.book.closed.fill", "books.vertical.fill", "book.pages.fill":
            return "quran"
        case "play.square.stack.fill":
            return "quran_audio"
        case "rectangle.stack.badge.play.fill":
            return "prayer"
        case "hands.sparkles.fill", "circle.grid.cross.fill":
            return "dhikr"
        case "sparkles":
            return "knowledge"
        case "location.north.circle.fill":
            return "qibla_calibration"
        case "map.fill":
            return "map"
        case "calendar":
            return "calendar"
        case "clock.arrow.circlepath":
            return "history"
        case "checklist", "pause.circle.fill":
            return "tracker"
        case "building.columns.fill":
            return "mosques"
        case "text.quote":
            return "duas"
        case "person.3.sequence.fill":
            return "community"
        case "moon.stars.fill":
            return "islamic_calendar"
        case "character.book.closed.fill":
            return "language"
        case "slider.horizontal.3":
            return "settings"
        case "ellipsis.circle.fill":
            return "more"
        default:
            return nil
        }
    }

    private func discoverTile(icon: String, title: String, subtitle: String) -> some View {
        VStack(spacing: 5) {
            salahFeatureIcon(icon, size: 44)

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
        .frame(maxWidth: .infinity, minHeight: 104)
        .padding(7)
        .background(
            LinearGradient(
                colors: [
                    Color.white.opacity(0.86),
                    SalahTheme.cream,
                    SalahTheme.softTeal.opacity(0.16)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            ),
            in: RoundedRectangle(cornerRadius: 16, style: .continuous)
        )
        .overlay {
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .stroke(
                    LinearGradient(
                        colors: [
                            SalahTheme.gold.opacity(0.58),
                            SalahTheme.gold.opacity(0.24)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: 1
                )
        }
        .shadow(color: SalahTheme.deepTeal.opacity(0.045), radius: 5, y: 2)
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
