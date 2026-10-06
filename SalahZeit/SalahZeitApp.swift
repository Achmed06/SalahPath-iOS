import SwiftUI

@main
struct SalahPathApp: App {
    @Environment(\.scenePhase) private var scenePhase
    @StateObject private var locationManager = LocationManager()
    @StateObject private var settings = SettingsStore()
    @State private var notificationScheduleRevision = 0

    init() {
        let navigation = UINavigationBarAppearance()
        navigation.configureWithOpaqueBackground()
        navigation.backgroundColor = UIColor(red: 36/255, green: 79/255, blue: 77/255, alpha: 1)
        navigation.shadowColor = UIColor(red: 234/255, green: 185/255, blue: 80/255, alpha: 0.28)
        navigation.titleTextAttributes = [.foregroundColor: UIColor.white]
        navigation.largeTitleTextAttributes = [.foregroundColor: UIColor.white]
        UINavigationBar.appearance().standardAppearance = navigation
        UINavigationBar.appearance().scrollEdgeAppearance = navigation
        UINavigationBar.appearance().compactAppearance = navigation
        UINavigationBar.appearance().tintColor = UIColor.white
    }

    var body: some Scene {
        WindowGroup {
            appRoot
                .environmentObject(locationManager)
                .environmentObject(settings)
                .task(id: prayerNotificationScheduleID) {
                    await refreshPrayerNotificationSchedule()
                }
                .onChange(of: scenePhase) { _, phase in
                    guard phase == .active else { return }
                    locationManager.refresh()
                    notificationScheduleRevision &+= 1
                }
                .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
                    notificationScheduleRevision &+= 1
                }
        }
    }

    private var isQAMode: Bool {
#if DEBUG
        ProcessInfo.processInfo.environment["SALAH_QA_SCREEN"] != nil
#else
        false
#endif
    }

    @ViewBuilder
    private var appRoot: some View {
#if DEBUG
        qaRoot
#else
        if settings.onboardingCompleted {
            RootTabView()
        } else {
            OnboardingFlowView()
        }
#endif
    }

    private var prayerNotificationScheduleID: String {
        guard settings.onboardingCompleted,
              settings.notificationsEnabled,
              let location = locationManager.location,
              !isQAMode else {
            return "disabled|\(notificationScheduleRevision)"
        }

        let coordinate = location.coordinate
        guard coordinate.latitude.isFinite,
              coordinate.longitude.isFinite,
              (-90.0...90.0).contains(coordinate.latitude),
              (-180.0...180.0).contains(coordinate.longitude) else {
            return "invalid-location|\(notificationScheduleRevision)"
        }

        let lat = Int((coordinate.latitude * 1_000).rounded())
        let lon = Int((coordinate.longitude * 1_000).rounded())
        let prayerFlags = [
            settings.fajrNotificationEnabled,
            settings.dhuhrNotificationEnabled,
            settings.asrNotificationEnabled,
            settings.maghribNotificationEnabled,
            settings.ishaNotificationEnabled
        ]
        .map { $0 ? "1" : "0" }
        .joined()
        let offsets = [
            settings.fajrOffset,
            settings.dhuhrOffset,
            settings.asrOffset,
            settings.maghribOffset,
            settings.ishaOffset
        ]
        .map(String.init)
        .joined(separator: ",")
        var prayerCalendar = Calendar(identifier: .gregorian)
        prayerCalendar.timeZone = locationManager.prayerTimeZone
        let dayKey = prayerCalendar.ordinality(of: .day, in: .era, for: Date()) ?? 1

        return [
            String(lat),
            String(lon),
            settings.calculationPreset.rawValue,
            settings.asrRule.rawValue,
            String(settings.notificationLeadMinutes),
            settings.notifyAtPrayerTime ? "1" : "0",
            settings.adhanSoundEnabled ? "adhan" : "system",
            prayerFlags,
            offsets,
            settings.language.rawValue,
            settings.use24Hour ? "24h" : "12h",
            locationManager.prayerTimeZone.identifier,
            String(dayKey),
            String(notificationScheduleRevision)
        ].joined(separator: "|")
    }

    @MainActor
    private func refreshPrayerNotificationSchedule() async {
        guard settings.onboardingCompleted, !isQAMode else { return }

        guard settings.notificationsEnabled else {
            NotificationManager.shared.removePrayerNotifications()
            return
        }

        // The toggle may have been persisted from an older installation while
        // iOS notification permission was reset. Ask for authorization before
        // requiring a location so the app cannot remain "enabled" but ungranted.
        let granted = await NotificationManager.shared.requestAuthorization()
        guard granted else {
            let diagnostics = await NotificationManager.shared.diagnostics()
            if diagnostics.authorizationStatus == .denied {
                settings.notificationsEnabled = false
            }
            NotificationManager.shared.removePrayerNotifications()
            return
        }

        guard let location = locationManager.location else {
            NotificationManager.shared.removePrayerNotifications()
            return
        }

        _ = await NotificationManager.shared.scheduleNextSevenDays(
            location: location,
            settings: settings,
            timeZone: locationManager.prayerTimeZone
        )
    }

#if DEBUG
    @ToolbarContentBuilder
    private var referenceQAToolbar: some ToolbarContent {
        ToolbarItem(placement: .topBarLeading) {
            Image(systemName: "chevron.left")
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(.white)
        }
        ToolbarItem(placement: .topBarTrailing) {
            Image(systemName: "bell.fill")
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(.white)
        }
    }

    @ViewBuilder
    private var qaRoot: some View {
        switch ProcessInfo.processInfo.environment["SALAH_QA_SCREEN"] {
        case "onboarding":
            OnboardingFlowView()
        case "daily-dua":
            NavigationStack { DailyDuaQAView() }
        case "home":
            RootTabView(initialSelection: 0)
        case "quran":
            RootTabView(initialSelection: 1)
        case "dhikr":
            NavigationStack {
                DhikrView()
                    .toolbar { referenceQAToolbar }
            }
        case "namaz":
            RootTabView(initialSelection: 2)
        case "times":
            NavigationStack {
                PrayerTimesOverviewView()
                    .toolbar { referenceQAToolbar }
            }
        case "quran-favorites":
            NavigationStack { QuranFavoritesLandingView() }
        case "quran-juz":
            NavigationStack {
                QuranJuzQAView()
            }
        case "quran-progress":
            NavigationStack {
                QuranProgressQAView()
            }
        case "audio-cache":
            NavigationStack {
                QuranAudioCacheQAView()
            }
        case "quran-reader":
            NavigationStack { QuranReaderQAView() }
        case "quran-page":
            NavigationStack { QuranPageReaderView(page: 1) }
        case "quran-page-mid":
            NavigationStack { QuranPageReaderView(page: 302) }
        case "quran-page-last":
            NavigationStack { QuranPageReaderView(page: 604) }
        case "namaz-howto":
            NavigationStack { PrayerHowToView() }
        case "namaz-step-01":
            NavigationStack { PrayerHowToView(initialStepIndex: 0) }
        case "namaz-step-02":
            NavigationStack { PrayerHowToView(initialStepIndex: 1) }
        case "namaz-step-03":
            NavigationStack { PrayerHowToView(initialStepIndex: 2) }
        case "namaz-step-04":
            NavigationStack { PrayerHowToView(initialStepIndex: 3) }
        case "namaz-step-05":
            NavigationStack { PrayerHowToView(initialStepIndex: 4) }
        case "namaz-step-06":
            NavigationStack { PrayerHowToView(initialStepIndex: 5) }
        case "namaz-step-07":
            NavigationStack { PrayerHowToView(initialStepIndex: 6) }
        case "namaz-step-08":
            NavigationStack { PrayerHowToView(initialStepIndex: 7) }
        case "namaz-step-09":
            NavigationStack { PrayerHowToView(initialStepIndex: 8) }
        case "namaz-step-10":
            NavigationStack { PrayerHowToView(initialStepIndex: 9) }
        case "namaz-step-11":
            NavigationStack { PrayerHowToView(initialStepIndex: 10) }
        case "namaz-step-12":
            NavigationStack { PrayerHowToView(initialStepIndex: 11) }
        case "namaz-step-13":
            NavigationStack { PrayerHowToView(initialStepIndex: 12) }
        case "namaz-step-14":
            NavigationStack { PrayerHowToView(initialStepIndex: 13) }
        case "namaz-step-15":
            NavigationStack { PrayerHowToView(initialStepIndex: 14) }
        case "namaz-step-16":
            NavigationStack { PrayerHowToView(initialStepIndex: 15) }
        case "namaz-step-17":
            NavigationStack { PrayerHowToView(initialStepIndex: 16) }
        case "namaz-step-18":
            NavigationStack { PrayerHowToView(initialStepIndex: 17) }
        case "namaz-bowing":
            NavigationStack { PrayerHowToView(initialStepIndex: 3) }
        case "namaz-sujud":
            NavigationStack { PrayerHowToView(initialStepIndex: 5) }
        case "namaz-second-standing":
            NavigationStack { PrayerHowToView(initialStepIndex: 8) }
        case "namaz-second-upright":
            NavigationStack { PrayerHowToView(initialStepIndex: 11) }
        case "namaz-sitting":
            NavigationStack { PrayerHowToView(initialStepIndex: 6) }
        case "namaz-finger":
            NavigationStack { PrayerHowToView(initialStepIndex: 15) }
        case "namaz-salam":
            NavigationStack { PrayerHowToView(initialStepIndex: 16) }
        case "namaz-salam-left":
            NavigationStack { PrayerHowToView(initialStepIndex: 17) }
        case "wudu":
            NavigationStack { WuduGuideView() }
        case "wudu-arm":
            NavigationStack { WuduGuideView(initialStepIndex: 4) }
        case "wudu-leftarm":
            NavigationStack { WuduGuideView(initialStepIndex: 5) }
        case "wudu-head":
            NavigationStack { WuduGuideView(initialStepIndex: 6) }
        case "wudu-ears":
            NavigationStack { WuduGuideView(initialStepIndex: 7) }
        case "wudu-foot":
            NavigationStack { WuduGuideView(initialStepIndex: 9) }
        case "wudu-leftfoot":
            NavigationStack { WuduGuideView(initialStepIndex: 10) }
        case "ghusl":
            NavigationStack { GhuslGuideView() }
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
            RootTabView(initialSelection: 4)
        case "more":
            RootTabView(initialSelection: 3)
        case "mosques":
            NavigationStack { NearbyMosquesView() }
        case "fasting":
            NavigationStack { FastingTrackerView() }
        case "fasting-basics":
            NavigationStack { FastingBasicsView() }
        case "fasting-rules":
            NavigationStack { FastingRulesView() }
        case "fasting-exceptions":
            NavigationStack { FastingExceptionsView() }
        case "islam-learning":
            NavigationStack { IslamLearningHubView() }
        case "hijri":
            NavigationStack { HijriCalendarView() }
        case "terms":
            NavigationStack { PrayerTermsView() }
        case "surahs":
            NavigationStack { ShortSurahLearningView() }
        case "positions":
            NavigationStack { PrayerSequenceReferenceView() }
        case "rakats":
            NavigationStack { RakatOverviewView() }
        case "hanafi-plan":
            NavigationStack { PrayerCatalogView() }
        case "prayer-tracker":
            NavigationStack { PrayerTrackerOverviewView() }
        case "tracker-pause":
            NavigationStack { TrackerPauseView() }
        default:
            if settings.onboardingCompleted {
                RootTabView()
            } else {
                OnboardingFlowView()
            }
        }
    }
#endif
}

private struct OnboardingFlowView: View {
    @EnvironmentObject private var settings: SettingsStore
    @EnvironmentObject private var locationManager: LocationManager

    @State private var step = 0
    @State private var manualLocation = ""
    @State private var resolvingLocation = false
    @State private var locationError: String?

    var body: some View {
        ZStack {
            SalahTheme.page.ignoresSafeArea()

            VStack(spacing: 16) {
                Spacer(minLength: 12)

                Image("salahpath_logo")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 72, height: 72)

                Group {
                    switch step {
                    case 0: welcomeStep
                    case 1: profileStep
                    case 2: locationStep
                    default: readyStep
                    }
                }
                .frame(maxWidth: 520)

                Spacer(minLength: 12)

                if step < 3 {
                    HStack(spacing: 10) {
                        if step > 0 {
                            Button {
                                if step == 2 {
                                    locationManager.cancelPendingLocationIntent()
                                    resolvingLocation = false
                                    locationError = nil
                                }
                                withAnimation(.easeInOut(duration: 0.18)) { step -= 1 }
                            } label: {
                                ZStack {
                                    RoundedRectangle(cornerRadius: 13, style: .continuous)
                                        .fill(SalahTheme.cream)
                                    Text(settings.t("Zurück", "Geri"))
                                        .font(.headline)
                                        .foregroundStyle(SalahTheme.deepTeal)
                                }
                                .frame(maxWidth: .infinity)
                                .frame(height: 48)
                                .contentShape(Rectangle())
                            }
                            .buttonStyle(.plain)
                            .frame(maxWidth: .infinity)
                            .contentShape(Rectangle())
                        }

                        if step < 2 {
                            Button {
                                withAnimation(.easeInOut(duration: 0.18)) { step += 1 }
                            } label: {
                                ZStack {
                                    RoundedRectangle(cornerRadius: 13, style: .continuous)
                                        .fill(SalahTheme.navigationTeal)
                                    Text(settings.t("Weiter", "İleri"))
                                        .font(.headline.bold())
                                        .foregroundStyle(.white)
                                }
                                .frame(maxWidth: .infinity)
                                .frame(height: 48)
                                .contentShape(Rectangle())
                            }
                            .buttonStyle(.plain)
                            .frame(maxWidth: .infinity)
                            .contentShape(Rectangle())
                        }
                    }
                    .frame(maxWidth: 520)
                }
            }
            .padding(.horizontal, 18)
            .padding(.vertical, 16)
        }
        .preferredColorScheme(preferredColorScheme)
        .onChange(of: locationManager.location) { _, newLocation in
            guard step == 2,
                  newLocation != nil,
                  !locationManager.usesManualLocation else { return }
            locationError = nil
            withAnimation(.easeInOut(duration: 0.18)) { step = 3 }
        }
        .onChange(of: locationManager.lastError) { _, newError in
            guard step == 2,
                  let newError,
                  !newError.isEmpty else { return }
            locationError = locationManager.localizedLastError(settings.language)
        }
    }

    private var preferredColorScheme: ColorScheme? {
        switch settings.appearance {
        case .system: return nil
        case .light: return .light
        case .dark: return .dark
        }
    }

    private var welcomeStep: some View {
        setupCard {
            VStack(spacing: 14) {
                Text("السلام عليكم")
                    .font(.system(size: 31, weight: .semibold))
                    .foregroundStyle(SalahTheme.deepTeal)

                Text("As-salāmu ʿalaykum")
                    .font(.title2.bold())
                    .foregroundStyle(SalahTheme.ink)

                Text(settings.t(
                    "Willkommen bei SalahPath. Wir richten nur die Dinge ein, die dir später Suche in den Einstellungen sparen.",
                    "SalahPath'e hoş geldin. Sonradan ayarlarda aramak zorunda kalmaman için yalnızca önemli şeyleri şimdi ayarlıyoruz."
                ))
                .font(.subheadline)
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)

                Picker("", selection: $settings.language) {
                    ForEach(AppLanguage.allCases) { language in
                        Text(language.title).tag(language)
                    }
                }
                .pickerStyle(.segmented)
            }
        }
    }

    private var profileStep: some View {
        setupCard {
            VStack(spacing: 14) {
                Text(settings.t("Welche Gebetsanleitung passt zu dir?", "Hangi namaz anlatımı sana uygun?"))
                    .font(.title3.bold())
                    .foregroundStyle(SalahTheme.deepTeal)
                    .multilineTextAlignment(.center)

                Text(settings.t(
                    "Damit direkt die passenden Mann- oder Frau-Abbildungen angezeigt werden.",
                    "Doğrudan uygun erkek veya kadın görsellerinin gösterilmesi için."
                ))
                .font(.subheadline)
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)

                ForEach(PrayerAudience.allCases) { audience in
                    Button {
                        settings.prayerAudience = audience
                    } label: {
                        HStack(spacing: 10) {
                            Image(audience == .male ? "male_intention" : "female_intention")
                                .resizable()
                                .interpolation(.high)
                                .scaledToFit()
                                .frame(width: 34, height: 34)
                                .accessibilityHidden(true)

                            Text(audience.title(settings.language))
                                .font(.headline)
                            Spacer()
                            SalahFeatureIcon(kind: "checkmark")
                                .frame(width: 22, height: 22)
                                .opacity(settings.prayerAudience == audience ? 1 : 0.18)
                        }
                        .padding(12)
                    }
                    .buttonStyle(.plain)
                    .foregroundStyle(SalahTheme.deepTeal)
                    .background(
                        settings.prayerAudience == audience ? SalahTheme.softTeal : SalahTheme.cream,
                        in: RoundedRectangle(cornerRadius: 13)
                    )
                    .overlay {
                        RoundedRectangle(cornerRadius: 13)
                            .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1)
                    }
                }
            }
        }
    }

    private var locationStep: some View {
        setupCard {
            VStack(spacing: 12) {
                Text(settings.t("Standort für Gebetszeiten", "Namaz vakitleri için konum"))
                    .font(.title3.bold())
                    .foregroundStyle(SalahTheme.deepTeal)
                    .multilineTextAlignment(.center)

                Text(settings.t(
                    "Du entscheidest. Für Gebetszeiten reicht auch ein manuell eingegebener Ort. Die physische Qibla-Kompassrichtung verwendet später den tatsächlichen Gerätestandort, wenn du Standortzugriff erlaubst. Du kannst diesen Schritt auch überspringen.",
                    "Karar senin. Namaz vakitleri için manuel girdiğin bir konum yeterlidir. Fiziksel kıble pusulası daha sonra, konum izni verirsen, gerçek cihaz konumunu kullanır. Bu adımı tamamen atlayabilirsin."
                ))
                .font(.subheadline)
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)

                Button {
                    locationError = nil
                    locationManager.useDeviceLocation()
                } label: {
                    SalahFeatureIconLabel(
                        title: settings.t("Aktuellen Standort verwenden", "Mevcut konumu kullan"),
                        kind: "qibla",
                        iconSize: 22
                    )
                        .font(.headline.bold())
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                }
                .buttonStyle(.plain)
                .foregroundStyle(.white)
                .background(SalahTheme.navigationTeal, in: RoundedRectangle(cornerRadius: 13))

                HStack(spacing: 8) {
                    TextField(settings.t("Stadt oder PLZ", "Şehir veya posta kodu"), text: $manualLocation)
                        .textInputAutocapitalization(.words)
                        .autocorrectionDisabled()
                        .padding(.horizontal, 11)
                        .frame(height: 44)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 11))
                        .overlay {
                            RoundedRectangle(cornerRadius: 11)
                                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1)
                        }

                    Button {
                        Task {
                            resolvingLocation = true
                            locationError = nil
                            let success = await locationManager.setManualLocation(searchText: manualLocation)
                            guard step == 2 else {
                                resolvingLocation = false
                                return
                            }
                            resolvingLocation = false
                            if success {
                                withAnimation(.easeInOut(duration: 0.18)) { step = 3 }
                            } else {
                                locationError = locationManager.localizedLastError(settings.language)
                            }
                        }
                    } label: {
                        if resolvingLocation {
                            ProgressView()
                                .frame(width: 44, height: 44)
                        } else {
                            Image(systemName: "checkmark")
                                .font(.headline.bold())
                                .frame(width: 44, height: 44)
                        }
                    }
                    .buttonStyle(.plain)
                    .foregroundStyle(.white)
                    .background(SalahTheme.navigationTeal, in: RoundedRectangle(cornerRadius: 11))
                    .disabled(manualLocation.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || resolvingLocation)
                }

                if let locationError {
                    Text(locationError)
                        .font(.caption)
                        .foregroundStyle(.red)
                        .frame(maxWidth: .infinity, alignment: .leading)
                }

                Button {
                    locationManager.cancelPendingLocationIntent()
                    resolvingLocation = false
                    locationError = nil
                    withAnimation(.easeInOut(duration: 0.18)) { step = 3 }
                } label: {
                    Text(settings.t("Jetzt überspringen", "Şimdi atla"))
                        .font(.subheadline.bold())
                        .foregroundStyle(SalahTheme.teal)
                        .padding(.vertical, 6)
                }
                .buttonStyle(.plain)
            }
        }
    }

    private var readyStep: some View {
        setupCard {
            VStack(spacing: 14) {
                SalahFeatureIcon(kind: "checkmark")
                    .frame(width: 54, height: 54)

                Text(settings.t("Fertig eingerichtet", "Kurulum tamam"))
                    .font(.title2.bold())
                    .foregroundStyle(SalahTheme.deepTeal)

                VStack(alignment: .leading, spacing: 7) {
                    SalahFeatureIconLabel(title: settings.language.title, kind: "language")
                    SalahFeatureIconLabel(title: settings.prayerAudience.title(settings.language), kind: "profile")
                    SalahFeatureIconLabel(
                        title: locationManager.locality ?? settings.t("Standort übersprungen", "Konum atlandı"),
                        kind: "qibla",
                        iconSize: 20
                    )
                }
                .font(.subheadline.weight(.semibold))
                .foregroundStyle(SalahTheme.ink)
                .frame(maxWidth: .infinity, alignment: .leading)

                Button {
                    settings.completeOnboarding()
                } label: {
                    ZStack {
                        RoundedRectangle(cornerRadius: 13, style: .continuous)
                            .fill(SalahTheme.navigationTeal)
                        Text(settings.t("SalahPath öffnen", "SalahPath'i aç"))
                            .font(.headline.bold())
                            .foregroundStyle(.white)
                    }
                    .frame(maxWidth: .infinity)
                    .frame(height: 48)
                    .contentShape(Rectangle())
                }
                .buttonStyle(.plain)
                .frame(maxWidth: .infinity)
                .contentShape(Rectangle())
            }
        }
    }

    private func setupCard<Content: View>(@ViewBuilder content: () -> Content) -> some View {
        content()
            .padding(18)
            .frame(maxWidth: .infinity)
            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 20, style: .continuous))
            .overlay {
                RoundedRectangle(cornerRadius: 20, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.48), lineWidth: 1)
            }
    }
}
