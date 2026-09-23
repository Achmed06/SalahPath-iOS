import Foundation
import Combine
import Adhan

enum AppLanguage: String, CaseIterable, Identifiable {
    case german
    case turkish

    var id: String { rawValue }
    var title: String { self == .german ? "Deutsch" : "Türkçe" }
}

enum AppAppearance: String, CaseIterable, Identifiable {
    case system
    case light
    case dark

    var id: String { rawValue }

    func title(_ language: AppLanguage) -> String {
        switch (self, language) {
        case (.system, .german): return "System"
        case (.system, .turkish): return "Sistem"
        case (.light, .german): return "Hell"
        case (.light, .turkish): return "Açık"
        case (.dark, .german): return "Dunkel"
        case (.dark, .turkish): return "Koyu"
        }
    }
}

enum PrayerAudience: String, CaseIterable, Identifiable {
    case male
    case female

    var id: String { rawValue }
    func title(_ language: AppLanguage) -> String {
        switch (self, language) {
        case (.male, .german): return "Junge / Mann"
        case (.male, .turkish): return "Erkek / Çocuk"
        case (.female, .german): return "Mädchen / Frau"
        case (.female, .turkish): return "Kız / Kadın"
        }
    }
}


enum QuranReciter: String, CaseIterable, Identifiable {
    case alafasy
    case husary
    case minshawi
    case sudais
    case shuraim

    var id: String { rawValue }

    var edition: String {
        switch self {
        case .alafasy: return "ar.alafasy"
        case .husary: return "ar.husary"
        case .minshawi: return "ar.minshawi"
        // Live AlQuran.cloud audio-edition identifier. The older ar.sudais alias
        // appears in some CDN documentation but does not currently return ayah audio.
        case .sudais: return "ar.abdurrahmaansudais"
        case .shuraim: return "ar.saoodshuraym"
        }
    }

    var bitrate: Int {
        switch self {
        case .sudais: return 192
        case .shuraim: return 64
        default: return 128
        }
    }

    var alternateAudioSource: (edition: String, bitrate: Int)? {
        switch self {
        case .sudais: return ("ar.sudais", 192)
        case .shuraim: return ("ar.shuraim", 128)
        default: return nil
        }
    }

    var title: String {
        switch self {
        case .alafasy: return "Mishary Rashid Alafasy"
        case .husary: return "Mahmoud Khalil Al-Husary"
        case .minshawi: return "Mohamed Siddiq al-Minshawi"
        case .sudais: return "Abdul Rahman Al-Sudais"
        case .shuraim: return "Saud Al-Shuraim"
        }
    }
}

enum CalculationPreset: String, CaseIterable, Identifiable {
    case muslimWorldLeague
    case moonsightingCommittee
    case turkey
    case egyptian
    case karachi
    case ummAlQura
    case northAmerica
    case dubai
    case qatar
    case kuwait
    case singapore
    case tehran

    var id: String { rawValue }

    func title(_ language: AppLanguage) -> String {
        switch self {
        case .muslimWorldLeague: return "Muslim World League"
        case .moonsightingCommittee: return "Moonsighting Committee"
        case .turkey:
            return language == .german ? "Diyanet / Türkei (Annäherung)" : "Diyanet / Türkiye (yaklaşım)"
        case .egyptian: return "Egyptian General Authority"
        case .karachi: return "Karachi"
        case .ummAlQura: return "Umm al-Qura"
        case .northAmerica:
            return language == .german ? "ISNA / Nordamerika" : "ISNA / Kuzey Amerika"
        case .dubai: return "Dubai"
        case .qatar: return "Qatar"
        case .kuwait: return "Kuwait"
        case .singapore: return "Singapur"
        case .tehran:
            return language == .german ? "Teheran" : "Tahran"
        }
    }

    var method: CalculationMethod {
        switch self {
        case .muslimWorldLeague: return .muslimWorldLeague
        case .moonsightingCommittee: return .moonsightingCommittee
        case .turkey: return .turkey
        case .egyptian: return .egyptian
        case .karachi: return .karachi
        case .ummAlQura: return .ummAlQura
        case .northAmerica: return .northAmerica
        case .dubai: return .dubai
        case .qatar: return .qatar
        case .kuwait: return .kuwait
        case .singapore: return .singapore
        case .tehran: return .tehran
        }
    }

    func note(_ language: AppLanguage) -> String {
        let de: String
        let tr: String
        switch self {
        case .turkey:
            de = "Die Adhan-Bibliothek bezeichnet diese Methode als Annäherung an Diyanet; außerhalb der Türkei kann sie abweichen."
            tr = "Adhan kütüphanesi bu yöntemi Diyanet'e yaklaşık bir hesap olarak tanımlar; Türkiye dışında farklılık gösterebilir."
        case .ummAlQura:
            de = "Umm al-Qura ist vor allem für Saudi-Arabien vorgesehen."
            tr = "Umm al-Qura özellikle Suudi Arabistan için tasarlanmıştır."
        case .northAmerica:
            de = "ISNA ist vor allem für Nordamerika vorgesehen."
            tr = "ISNA özellikle Kuzey Amerika için tasarlanmıştır."
        case .moonsightingCommittee:
            de = "Mit saisonalen Regeln und Hochbreiten-Behandlung."
            tr = "Mevsimsel kurallar ve yüksek enlem düzeltmeleri içerir."
        default:
            de = "Die Methode bestimmt insbesondere Fajr und Isha."
            tr = "Bu yöntem özellikle imsak/sabah ve yatsı vakitlerini etkiler."
        }
        return language == .german ? de : tr
    }
}

enum AsrRule: String, CaseIterable, Identifiable {
    case standard
    case hanafi

    var id: String { rawValue }
    func title(_ language: AppLanguage) -> String {
        switch (self, language) {
        case (.standard, .german): return "Standard (Schafiʿi / Maliki / Hanbali)"
        case (.standard, .turkish): return "Standart (Şafiî / Malikî / Hanbelî)"
        case (.hanafi, .german): return "Hanafi"
        case (.hanafi, .turkish): return "Hanefî"
        }
    }

    var madhab: Madhab { self == .hanafi ? .hanafi : .shafi }
}

@MainActor
final class SettingsStore: ObservableObject {
    private enum Keys {
        static let method = "calculationMethod"
        static let asr = "asrRule"
        static let use24Hour = "use24Hour"
        static let notifications = "notificationsEnabled"
        static let notifyAtPrayerTime = "notifyAtPrayerTime"
        static let leadMinutes = "notificationLeadMinutes"
        static let fajrNotification = "fajrNotificationEnabled"
        static let dhuhrNotification = "dhuhrNotificationEnabled"
        static let asrNotification = "asrNotificationEnabled"
        static let maghribNotification = "maghribNotificationEnabled"
        static let ishaNotification = "ishaNotificationEnabled"
        static let fajrOffset = "fajrOffset"
        static let dhuhrOffset = "dhuhrOffset"
        static let asrOffset = "asrOffset"
        static let maghribOffset = "maghribOffset"
        static let ishaOffset = "ishaOffset"
        static let language = "appLanguage"
        static let audience = "prayerAudience"
        static let appearance = "appAppearance"
        static let quranReciter = "quranReciter"
        static let quranFontSize = "quranFontSize"
        static let quranShowTranslation = "quranShowTranslation"
        static let quranShowTransliteration = "quranShowTransliteration"
        static let onboardingCompleted = "onboardingCompleted"
    }

    @Published var calculationPreset: CalculationPreset { didSet { defaults.set(calculationPreset.rawValue, forKey: Keys.method) } }
    @Published var asrRule: AsrRule { didSet { defaults.set(asrRule.rawValue, forKey: Keys.asr) } }
    @Published var use24Hour: Bool { didSet { defaults.set(use24Hour, forKey: Keys.use24Hour) } }
    @Published var notificationsEnabled: Bool { didSet { defaults.set(notificationsEnabled, forKey: Keys.notifications) } }
    @Published var notifyAtPrayerTime: Bool { didSet { defaults.set(notifyAtPrayerTime, forKey: Keys.notifyAtPrayerTime) } }
    @Published var notificationLeadMinutes: Int { didSet { defaults.set(notificationLeadMinutes, forKey: Keys.leadMinutes) } }
    @Published var fajrNotificationEnabled: Bool { didSet { defaults.set(fajrNotificationEnabled, forKey: Keys.fajrNotification) } }
    @Published var dhuhrNotificationEnabled: Bool { didSet { defaults.set(dhuhrNotificationEnabled, forKey: Keys.dhuhrNotification) } }
    @Published var asrNotificationEnabled: Bool { didSet { defaults.set(asrNotificationEnabled, forKey: Keys.asrNotification) } }
    @Published var maghribNotificationEnabled: Bool { didSet { defaults.set(maghribNotificationEnabled, forKey: Keys.maghribNotification) } }
    @Published var ishaNotificationEnabled: Bool { didSet { defaults.set(ishaNotificationEnabled, forKey: Keys.ishaNotification) } }
    @Published var fajrOffset: Int { didSet { defaults.set(fajrOffset, forKey: Keys.fajrOffset) } }
    @Published var dhuhrOffset: Int { didSet { defaults.set(dhuhrOffset, forKey: Keys.dhuhrOffset) } }
    @Published var asrOffset: Int { didSet { defaults.set(asrOffset, forKey: Keys.asrOffset) } }
    @Published var maghribOffset: Int { didSet { defaults.set(maghribOffset, forKey: Keys.maghribOffset) } }
    @Published var ishaOffset: Int { didSet { defaults.set(ishaOffset, forKey: Keys.ishaOffset) } }
    @Published var language: AppLanguage { didSet { defaults.set(language.rawValue, forKey: Keys.language) } }
    @Published var prayerAudience: PrayerAudience { didSet { defaults.set(prayerAudience.rawValue, forKey: Keys.audience) } }
    @Published var appearance: AppAppearance { didSet { defaults.set(appearance.rawValue, forKey: Keys.appearance) } }
    @Published var quranReciter: QuranReciter { didSet { defaults.set(quranReciter.rawValue, forKey: Keys.quranReciter) } }
    @Published var quranFontSize: Double { didSet { defaults.set(quranFontSize, forKey: Keys.quranFontSize) } }
    @Published var quranShowTranslation: Bool { didSet { defaults.set(quranShowTranslation, forKey: Keys.quranShowTranslation) } }
    @Published var quranShowTransliteration: Bool { didSet { defaults.set(quranShowTransliteration, forKey: Keys.quranShowTransliteration) } }
    @Published var onboardingCompleted: Bool { didSet { defaults.set(onboardingCompleted, forKey: Keys.onboardingCompleted) } }

    private let defaults: UserDefaults

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
        self.calculationPreset = CalculationPreset(rawValue: defaults.string(forKey: Keys.method) ?? "") ?? .muslimWorldLeague
        self.asrRule = AsrRule(rawValue: defaults.string(forKey: Keys.asr) ?? "") ?? .standard
        self.use24Hour = defaults.object(forKey: Keys.use24Hour) as? Bool ?? true
        self.notificationsEnabled = defaults.object(forKey: Keys.notifications) as? Bool ?? false
        self.notifyAtPrayerTime = defaults.object(forKey: Keys.notifyAtPrayerTime) as? Bool ?? true
        let storedLeadMinutes = defaults.object(forKey: Keys.leadMinutes) as? Int ?? 10
        let allowedLeadMinutes = [0, 5, 10, 15, 30]
        self.notificationLeadMinutes = allowedLeadMinutes.contains(storedLeadMinutes) ? storedLeadMinutes : 10
        self.fajrNotificationEnabled = defaults.object(forKey: Keys.fajrNotification) as? Bool ?? true
        self.dhuhrNotificationEnabled = defaults.object(forKey: Keys.dhuhrNotification) as? Bool ?? true
        self.asrNotificationEnabled = defaults.object(forKey: Keys.asrNotification) as? Bool ?? true
        self.maghribNotificationEnabled = defaults.object(forKey: Keys.maghribNotification) as? Bool ?? true
        self.ishaNotificationEnabled = defaults.object(forKey: Keys.ishaNotification) as? Bool ?? true
        func sanitizedOffset(_ key: String) -> Int {
            min(max(defaults.object(forKey: key) as? Int ?? 0, -15), 15)
        }
        self.fajrOffset = sanitizedOffset(Keys.fajrOffset)
        self.dhuhrOffset = sanitizedOffset(Keys.dhuhrOffset)
        self.asrOffset = sanitizedOffset(Keys.asrOffset)
        self.maghribOffset = sanitizedOffset(Keys.maghribOffset)
        self.ishaOffset = sanitizedOffset(Keys.ishaOffset)
        self.language = AppLanguage(rawValue: defaults.string(forKey: Keys.language) ?? "") ?? .german
        self.prayerAudience = PrayerAudience(rawValue: defaults.string(forKey: Keys.audience) ?? "") ?? .male
        self.appearance = AppAppearance(rawValue: defaults.string(forKey: Keys.appearance) ?? "") ?? .system
        self.quranReciter = QuranReciter(rawValue: defaults.string(forKey: Keys.quranReciter) ?? "") ?? .alafasy
        let storedQuranFontSize = defaults.object(forKey: Keys.quranFontSize) as? Double ?? 28
        self.quranFontSize = storedQuranFontSize.isFinite
            ? min(max(storedQuranFontSize, 20), 40)
            : 28
        self.quranShowTranslation = defaults.object(forKey: Keys.quranShowTranslation) as? Bool ?? true
        self.quranShowTransliteration = defaults.object(forKey: Keys.quranShowTransliteration) as? Bool ?? false
        self.onboardingCompleted = defaults.object(forKey: Keys.onboardingCompleted) as? Bool ?? false
    }

    var safeQuranFontSize: Double {
        guard quranFontSize.isFinite else { return 28 }
        return min(max(quranFontSize, 20), 40)
    }

    func t(_ de: String, _ tr: String) -> String { language == .german ? de : tr }

    func completeOnboarding() {
        onboardingCompleted = true
    }

    func restartOnboarding() {
        onboardingCompleted = false
    }

    func notificationEnabled(for kind: PrayerKind) -> Bool {
        switch kind {
        case .fajr: return fajrNotificationEnabled
        case .dhuhr: return dhuhrNotificationEnabled
        case .asr: return asrNotificationEnabled
        case .maghrib: return maghribNotificationEnabled
        case .isha: return ishaNotificationEnabled
        case .sunrise: return false
        }
    }

    func offset(for kind: PrayerKind) -> Int {
        switch kind {
        case .fajr: return fajrOffset
        case .dhuhr: return dhuhrOffset
        case .asr: return asrOffset
        case .maghrib: return maghribOffset
        case .isha: return ishaOffset
        case .sunrise: return 0
        }
    }

    func resetOffsets() {
        fajrOffset = 0; dhuhrOffset = 0; asrOffset = 0; maghribOffset = 0; ishaOffset = 0
    }
}
