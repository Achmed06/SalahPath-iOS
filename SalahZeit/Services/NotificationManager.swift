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
        center.removeAllPendingNotificationRequests()
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
                let fireDate = prayer.date.addingTimeInterval(TimeInterval(-settings.notificationLeadMinutes * 60))
                guard fireDate > now else { continue }

                let content = UNMutableNotificationContent()
                let prayerName = prayer.kind.localizedName(settings.language)
                content.title = settings.notificationLeadMinutes == 0
                    ? settings.t("\(prayerName) beginnt", "\(prayerName) vakti başladı")
                    : settings.t("\(prayerName) in \(settings.notificationLeadMinutes) Min.", "\(prayerName) için \(settings.notificationLeadMinutes) dk kaldı")
                if let rakats = prayer.kind.fardRakats {
                    content.body = settings.t("\(rakats) Rakʿat Fard • \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language))", "\(rakats) rekât farz • \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language))")
                }
                content.sound = .default

                var components = calendar.dateComponents([.year, .month, .day, .hour, .minute], from: fireDate)
                components.timeZone = .current
                let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)
                let identifier = "salahzeit.\(dayOffset).\(prayer.kind.rawValue)"
                let request = UNNotificationRequest(identifier: identifier, content: content, trigger: trigger)
                try? await center.add(request)
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
