import Foundation
import CoreLocation
import UserNotifications

@MainActor
final class NotificationManager {
    static let shared = NotificationManager()
    private let center = UNUserNotificationCenter.current()
    private let engine = PrayerEngine()

    private init() {}

    func requestAuthorization() async -> Bool {
        do {
            return try await center.requestAuthorization(options: [.alert, .sound, .badge])
        } catch {
            return false
        }
    }

    func removePrayerNotifications() {
        center.getPendingNotificationRequests { requests in
            let ids = requests
                .map(\.identifier)
                .filter { $0.hasPrefix("salahzeit.prayer.") }
            guard !ids.isEmpty else { return }
            self.center.removePendingNotificationRequests(withIdentifiers: ids)
        }
    }

    func scheduleNextSevenDays(location: CLLocation, settings: SettingsStore) async {
        removePrayerNotifications()
        guard settings.notificationsEnabled else { return }

        let granted = await requestAuthorization()
        guard granted else { return }

        let calendar = Calendar.current
        let now = Date()

        for dayOffset in 0..<7 {
            guard let date = calendar.date(byAdding: .day, value: dayOffset, to: now),
                  let day = engine.calculateDay(for: date, location: location, settings: settings, calendar: calendar) else {
                continue
            }

            for prayer in day.prayers where prayer.kind != .sunrise {
                guard settings.notificationEnabled(for: prayer.kind) else { continue }

                let prayerName = prayer.kind.localizedName(settings.language)

                if settings.notificationLeadMinutes > 0 {
                    let reminderDate = prayer.date.addingTimeInterval(TimeInterval(-settings.notificationLeadMinutes * 60))
                    if reminderDate > now {
                        let reminder = UNMutableNotificationContent()
                        reminder.title = settings.t(
                            "\(prayerName) in \(settings.notificationLeadMinutes) Min.",
                            "\(prayerName) için \(settings.notificationLeadMinutes) dk kaldı"
                        )
                        reminder.body = settings.t(
                            "Gebetszeit: \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language))",
                            "Namaz vakti: \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language))"
                        )
                        reminder.sound = .default

                        var components = calendar.dateComponents([.year, .month, .day, .hour, .minute], from: reminderDate)
                        components.timeZone = .current
                        let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)
                        let identifier = "salahzeit.prayer.\(dayOffset).\(prayer.kind.rawValue).pre"
                        try? await center.add(UNNotificationRequest(identifier: identifier, content: reminder, trigger: trigger))
                    }
                }

                if settings.notifyAtPrayerTime, prayer.date > now {
                    let content = UNMutableNotificationContent()
                    content.title = settings.t("\(prayerName) beginnt", "\(prayerName) vakti başladı")
                    if let rakats = prayer.kind.fardRakats {
                        content.body = settings.t(
                            "\(rakats) Rakʿat Fard • \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language))",
                            "\(rakats) rekât farz • \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language))"
                        )
                    }
                    content.sound = .default

                    var components = calendar.dateComponents([.year, .month, .day, .hour, .minute], from: prayer.date)
                    components.timeZone = .current
                    let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)
                    let identifier = "salahzeit.prayer.\(dayOffset).\(prayer.kind.rawValue).time"
                    try? await center.add(UNNotificationRequest(identifier: identifier, content: content, trigger: trigger))
                }
            }
        }
    }

    private func format(_ date: Date, use24Hour: Bool, language: AppLanguage) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: language == .german ? "de_DE" : "tr_TR")
        formatter.dateFormat = use24Hour ? "HH:mm" : "h:mm a"
        return formatter.string(from: date)
    }
}
