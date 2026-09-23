import Foundation

enum LocalDay {
    static func calendar() -> Calendar {
        var calendar = Calendar.autoupdatingCurrent
        calendar.timeZone = .autoupdatingCurrent
        return calendar
    }

    static func token(for date: Date) -> String {
        let parts = calendar().dateComponents([.year, .month, .day], from: date)
        guard let year = parts.year,
              let month = parts.month,
              let day = parts.day else {
            return "unknown"
        }
        return String(format: "%04d-%02d-%02d", year, month, day)
    }

    static func ordinal(for date: Date) -> Int {
        calendar().ordinality(of: .day, in: .era, for: date) ?? 1
    }

    static func startOfDay(for date: Date) -> Date {
        calendar().startOfDay(for: date)
    }

    static func addingDays(_ value: Int, to date: Date) -> Date? {
        calendar().date(byAdding: .day, value: value, to: date)
    }
}


func timeString(_ date: Date, use24Hour: Bool, language: AppLanguage) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: language == .german ? "de_DE" : "tr_TR")
    formatter.timeZone = .autoupdatingCurrent
    formatter.dateFormat = use24Hour ? "HH:mm" : "h:mm a"
    return formatter.string(from: date)
}

func gregorianDateString(_ date: Date, language: AppLanguage = .german) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: language == .german ? "de_DE" : "tr_TR")
    formatter.timeZone = .autoupdatingCurrent
    formatter.dateStyle = .full
    return formatter.string(from: date)
}

func hijriDateString(_ date: Date, language: AppLanguage = .german) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: language == .german ? "de_DE" : "tr_TR")
    var calendar = Calendar(identifier: .islamicUmmAlQura)
    calendar.timeZone = .autoupdatingCurrent
    formatter.calendar = calendar
    formatter.timeZone = .autoupdatingCurrent
    formatter.dateFormat = "d MMMM yyyy"
    return formatter.string(from: date)
}

func countdownString(from now: Date, to future: Date) -> String {
    let interval = future.timeIntervalSince(now)
    guard interval.isFinite, interval > 0 else { return "00:00" }

    let cappedInterval = min(interval.rounded(.down), Double(Int.max))
    let seconds = Int(cappedInterval)
    let hours = seconds / 3600
    let minutes = (seconds % 3600) / 60
    let secs = seconds % 60
    if hours > 0 { return String(format: "%02d:%02d:%02d", hours, minutes, secs) }
    return String(format: "%02d:%02d", minutes, secs)
}
