import Foundation

struct PrayerOccurrence: Identifiable, Equatable {
    let id = UUID()
    let kind: PrayerKind
    let date: Date
    static func == (lhs: PrayerOccurrence, rhs: PrayerOccurrence) -> Bool { lhs.kind == rhs.kind && lhs.date == rhs.date }
}

enum PrayerKind: String, CaseIterable, Identifiable {
    case fajr = "Fajr"
    case sunrise = "Sonnenaufgang"
    case dhuhr = "Dhuhr"
    case asr = "Asr"
    case maghrib = "Maghrib"
    case isha = "Isha"

    var id: String { rawValue }

    func localizedName(_ language: AppLanguage) -> String {
        guard language == .turkish else { return rawValue }
        switch self {
        case .fajr: return "Sabah"
        case .sunrise: return "Güneş"
        case .dhuhr: return "Öğle"
        case .asr: return "İkindi"
        case .maghrib: return "Akşam"
        case .isha: return "Yatsı"
        }
    }

    var systemImage: String {
        switch self {
        case .fajr: return "sun.horizon"
        case .sunrise: return "sunrise"
        case .dhuhr: return "sun.max"
        case .asr: return "sun.min"
        case .maghrib: return "sunset"
        case .isha: return "moon.stars"
        }
    }

    var fardRakats: Int? {
        switch self {
        case .fajr: return 2
        case .dhuhr: return 4
        case .asr: return 4
        case .maghrib: return 3
        case .isha: return 4
        case .sunrise: return nil
        }
    }

    func fullSequence(_ language: AppLanguage) -> String {
        let de: String
        let tr: String
        switch self {
        case .fajr:
            de = "2 Sunnah muʾakkadah → 2 Fard"
            tr = "2 sünnet → 2 farz"
        case .sunrise:
            de = "Kein Pflichtgebet. Fajr endet mit Sonnenaufgang."
            tr = "Farz namaz yoktur. Sabah vakti güneş doğunca sona erer."
        case .dhuhr:
            de = "4 Sunnah → 4 Fard → 2 Sunnah"
            tr = "4 sünnet → 4 farz → 2 son sünnet"
        case .asr:
            de = "4 Sunnah (ghair muʾakkadah) → 4 Fard"
            tr = "4 sünnet (gayr-i müekked) → 4 farz"
        case .maghrib:
            de = "3 Fard → 2 Sunnah"
            tr = "3 farz → 2 sünnet"
        case .isha:
            de = "4 Sunnah (ghair muʾakkadah) → 4 Fard → 2 Sunnah → 3 Witr (Hanafi: wajib)"
            tr = "4 ilk sünnet → 4 farz → 2 son sünnet → 3 vitir (Hanefî: vacip)"
        }
        return language == .german ? de : tr
    }

    func detailNote(_ language: AppLanguage) -> String {
        let de: String
        let tr: String
        switch self {
        case .fajr:
            de = "Die zwei Sunnah vor Fajr gehören zu den besonders betonten Sunnah-Gebeten."
            tr = "Sabah namazının farzından önceki iki rekât sünnet, en kuvvetli sünnetlerdendir."
        case .sunrise:
            de = "Direkt um den Sonnenaufgang herum wird kein freiwilliges Gebet begonnen."
            tr = "Güneşin doğuş anında nafile namaza başlanmaz."
        case .dhuhr:
            de = "Freitags ersetzt Jumuʿah für Teilnehmende das normale Dhuhr-Fard."
            tr = "Cuma günü cemaatle cuma namazına katılanlar için öğle farzının yerini cuma farzı alır."
        case .asr:
            de = "Die vier Sunnah vor Asr gelten im hanafitischen Ablauf als nicht-muʾakkadah."
            tr = "İkindinin dört rekât sünneti Hanefî uygulamada gayr-i müekkeddir."
        case .maghrib:
            de = "Nach den drei Fard folgen gewöhnlich zwei Sunnah."
            tr = "Üç rekât farzdan sonra iki rekât sünnet kılınır."
        case .isha:
            de = "Im hanafitischen Madhhab sind drei Rakʿat Witr wajib; andere sunnitische Rechtsschulen stufen Witr anders ein."
            tr = "Hanefî mezhebinde üç rekât vitir vaciptir; diğer Sünnî mezheplerde hükmü farklı değerlendirilir."
        }
        return language == .german ? de : tr
    }
}

struct PrayerDay {
    let date: Date
    let prayers: [PrayerOccurrence]
    let middleOfNight: Date?
    let lastThirdOfNight: Date?
    func time(for kind: PrayerKind) -> Date? { prayers.first(where: { $0.kind == kind })?.date }
}
