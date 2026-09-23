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
            qaRoot
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
        ProcessInfo.processInfo.environment["SALAH_QA_SCREEN"] != nil
    }

    private var prayerNotificationScheduleID: String {
        guard settings.onboardingCompleted,
              settings.notificationsEnabled,
              let location = locationManager.location,
              !isQAMode else {
            return "disabled|\(notificationScheduleRevision)"
        }

        let lat = Int((location.coordinate.latitude * 1_000).rounded())
        let lon = Int((location.coordinate.longitude * 1_000).rounded())
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
        let dayKey = Calendar.current.ordinality(of: .day, in: .era, for: Date()) ?? 0

        return [
            String(lat),
            String(lon),
            settings.calculationPreset.rawValue,
            settings.asrRule.rawValue,
            String(settings.notificationLeadMinutes),
            settings.notifyAtPrayerTime ? "1" : "0",
            prayerFlags,
            offsets,
            settings.language.rawValue,
            settings.use24Hour ? "24h" : "12h",
            TimeZone.current.identifier,
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

        guard let location = locationManager.location else { return }

        _ = await NotificationManager.shared.scheduleNextSevenDays(
            location: location,
            settings: settings
        )
    }

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
        case "quran":
            NavigationStack {
                QuranView()
                    .toolbar { referenceQAToolbar }
            }
        case "dhikr":
            NavigationStack {
                DhikrView()
                    .toolbar { referenceQAToolbar }
            }
        case "namaz":
            NavigationStack {
                GuideView()
                    .toolbar { referenceQAToolbar }
            }
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
        case "more":
            NavigationStack { MoreView() }
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
            NavigationStack { HanafiPrayerPlanView() }
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
                                withAnimation(.easeInOut(duration: 0.18)) { step -= 1 }
                            } label: {
                                Text(settings.t("Zurück", "Geri"))
                                    .font(.headline)
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 12)
                            }
                            .buttonStyle(.plain)
                            .foregroundStyle(SalahTheme.deepTeal)
                            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13))
                        }

                        if step < 2 {
                            Button {
                                withAnimation(.easeInOut(duration: 0.18)) { step += 1 }
                            } label: {
                                Text(settings.t("Weiter", "İleri"))
                                    .font(.headline.bold())
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 12)
                            }
                            .buttonStyle(.plain)
                            .foregroundStyle(.white)
                            .background(SalahTheme.navigationTeal, in: RoundedRectangle(cornerRadius: 13))
                        }
                    }
                    .frame(maxWidth: 520)
                }
            }
            .padding(.horizontal, 18)
            .padding(.vertical, 16)
        }
        .preferredColorScheme(preferredColorScheme)
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
                    "Damit die App direkt die passenden Mann- oder Frau-Abbildungen zeigt.",
                    "Uygulamanın doğrudan uygun erkek veya kadın görsellerini göstermesi için."
                ))
                .font(.subheadline)
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)

                ForEach(PrayerAudience.allCases) { audience in
                    Button {
                        settings.prayerAudience = audience
                    } label: {
                        HStack {
                            Image(systemName: audience == .male ? "person.fill" : "person.fill")
                            Text(audience.title(settings.language))
                                .font(.headline)
                            Spacer()
                            Image(systemName: settings.prayerAudience == audience ? "checkmark.circle.fill" : "circle")
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
                Text(settings.t("Standort für Gebetszeiten & Qibla", "Namaz vakitleri ve kıble için konum"))
                    .font(.title3.bold())
                    .foregroundStyle(SalahTheme.deepTeal)
                    .multilineTextAlignment(.center)

                Text(settings.t(
                    "Du entscheidest. GPS ist nicht nötig, wenn du deinen Ort manuell eingibst. Du kannst diesen Schritt auch überspringen.",
                    "Karar senin. Şehrini manuel girersen GPS gerekmez. Bu adımı tamamen atlayabilirsin."
                ))
                .font(.subheadline)
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)

                Button {
                    locationManager.useDeviceLocation()
                    locationError = nil
                    withAnimation(.easeInOut(duration: 0.18)) { step = 3 }
                } label: {
                    Label(settings.t("Aktuellen Standort verwenden", "Mevcut konumu kullan"), systemImage: "location.fill")
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
                            resolvingLocation = false
                            if success {
                                withAnimation(.easeInOut(duration: 0.18)) { step = 3 }
                            } else {
                                locationError = locationManager.lastError
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
                    .background(SalahTheme.teal, in: RoundedRectangle(cornerRadius: 11))
                    .disabled(manualLocation.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || resolvingLocation)
                }

                if let locationError {
                    Text(locationError)
                        .font(.caption)
                        .foregroundStyle(.red)
                        .frame(maxWidth: .infinity, alignment: .leading)
                }

                Button {
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
                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 50))
                    .foregroundStyle(SalahTheme.teal)

                Text(settings.t("Fertig eingerichtet", "Kurulum tamam"))
                    .font(.title2.bold())
                    .foregroundStyle(SalahTheme.deepTeal)

                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.language.title, systemImage: "globe")
                    Label(settings.prayerAudience.title(settings.language), systemImage: "person.fill")
                    Label(
                        locationManager.locality ?? settings.t("Standort übersprungen", "Konum atlandı"),
                        systemImage: locationManager.location == nil ? "location.slash" : "location.fill"
                    )
                }
                .font(.subheadline.weight(.semibold))
                .foregroundStyle(SalahTheme.ink)
                .frame(maxWidth: .infinity, alignment: .leading)

                Button {
                    settings.completeOnboarding()
                } label: {
                    Text(settings.t("SalahPath öffnen", "SalahPath'i aç"))
                        .font(.headline.bold())
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                }
                .buttonStyle(.plain)
                .foregroundStyle(.white)
                .background(SalahTheme.navigationTeal, in: RoundedRectangle(cornerRadius: 13))
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
