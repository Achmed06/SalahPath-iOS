import SwiftUI

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

private struct ReferenceBottomBar: View {
    @EnvironmentObject private var settings: SettingsStore
    @Binding var selection: Int

    private var items: [(String, String)] {
        [
            ("house.fill", settings.t("Start", "Ana Sayfa")),
            ("book.fill", settings.t("Koran", "Kur'an")),
            ("figure.mind.and.body", settings.t("Gebet", "Namaz")),
            ("location.north.circle", settings.t("Entdecken", "Keşfet")),
            ("person.crop.circle", settings.t("Profil", "Profil"))
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
                            Image(systemName: item.0)
                                .font(.system(size: 17, weight: selection == index ? .bold : .semibold))
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

    private let columns = [
        GridItem(.flexible(), spacing: 8),
        GridItem(.flexible(), spacing: 8)
    ]

    var body: some View {
        ScrollView {
            VStack(spacing: 10) {
                discoverHero

                LazyVGrid(columns: columns, spacing: 8) {
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
                .font(.system(size: size * 0.43, weight: .semibold))
                .foregroundStyle(SalahTheme.deepTeal)

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

    private func discoverTile(icon: String, title: String, subtitle: String) -> some View {
        VStack(spacing: 7) {
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
        .frame(maxWidth: .infinity, minHeight: 108)
        .padding(9)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1) }
    }

    private func discoverRow(icon: String, title: String, subtitle: String) -> some View {
        HStack(spacing: 10) {
            salahFeatureIcon(icon, size: 34)

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
        .padding(.horizontal, 12)
        .padding(.vertical, 10)
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
            Image(systemName: icon)
                .font(.system(size: 17, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
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

