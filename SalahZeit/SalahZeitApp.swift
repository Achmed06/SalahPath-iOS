import SwiftUI

@main
struct SalahPathApp: App {
    @StateObject private var locationManager = LocationManager()
    @StateObject private var settings = SettingsStore()

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
        }
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
            RootTabView()
        }
    }
}
