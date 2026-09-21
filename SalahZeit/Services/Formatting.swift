import Foundation

func timeString(_ date: Date, use24Hour: Bool) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: "en_US_POSIX")
    formatter.dateFormat = use24Hour ? "HH:mm" : "h:mm a"
    return formatter.string(from: date)
}

func gregorianDateString(_ date: Date, language: AppLanguage = .german) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: language == .german ? "de_DE" : "tr_TR")
    formatter.dateStyle = .full
    return formatter.string(from: date)
}

func hijriDateString(_ date: Date, language: AppLanguage = .german) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: language == .german ? "de_DE" : "tr_TR")
    formatter.calendar = Calendar(identifier: .islamicUmmAlQura)
    formatter.dateFormat = "d MMMM yyyy"
    return formatter.string(from: date)
}

func countdownString(from now: Date, to future: Date) -> String {
    let seconds = max(0, Int(future.timeIntervalSince(now)))
    let hours = seconds / 3600
    let minutes = (seconds % 3600) / 60
    let secs = seconds % 60
    if hours > 0 { return String(format: "%02d:%02d:%02d", hours, minutes, secs) }
    return String(format: "%02d:%02d", minutes, secs)
}
