import Foundation
import CoreLocation
import UserNotifications

@MainActor
final class NotificationManager {
    static let shared = NotificationManager()
    private let center = UNUserNotificationCenter.current()
    private let engine = PrayerEngine()
    private let prayerIdentifierPrefix = "salahzeit.prayer."
    private var schedulingRevision = 0

    private init() {}

    func requestAuthorization() async -> Bool {
        do {
            return try await center.requestAuthorization(options: [.alert, .sound, .badge])
        } catch {
            return false
        }
    }

    func removePrayerNotifications() {
        schedulingRevision &+= 1
        let revision = schedulingRevision
        let center = center
        let prefix = prayerIdentifierPrefix

        center.getPendingNotificationRequests { requests in
            let ids = requests
                .map(\.identifier)
                .filter { $0.hasPrefix(prefix) }
            guard !ids.isEmpty else { return }

            Task { @MainActor [weak self] in
                guard let self, revision == self.schedulingRevision else { return }
                center.removePendingNotificationRequests(withIdentifiers: ids)
            }
        }
    }

    @discardableResult
    func scheduleNextSevenDays(location: CLLocation, settings: SettingsStore) async -> Bool {
        schedulingRevision &+= 1
        let revision = schedulingRevision

        await removeExistingPrayerNotifications(for: revision)
        guard revision == schedulingRevision else { return false }
        guard settings.notificationsEnabled else { return false }

        let granted = await ensureAuthorization()
        guard revision == schedulingRevision, granted else { return false }

        let calendar = Calendar.current
        let now = Date()

        for dayOffset in 0..<7 {
            guard revision == schedulingRevision else { return false }
            guard let date = calendar.date(byAdding: .day, value: dayOffset, to: now),
                  let day = engine.calculateDay(for: date, location: location, settings: settings, calendar: calendar) else {
                continue
            }

            for prayer in day.prayers where prayer.kind != .sunrise {
                guard revision == schedulingRevision else { return false }
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
                        let identifier = "salahzeit.prayer.r\(revision).\(dayOffset).\(prayer.kind.rawValue).pre"
                        await add(
                            UNNotificationRequest(identifier: identifier, content: reminder, trigger: trigger),
                            revision: revision
                        )
                        guard revision == schedulingRevision else { return false }
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
                    let identifier = "salahzeit.prayer.r\(revision).\(dayOffset).\(prayer.kind.rawValue).time"
                    await add(
                        UNNotificationRequest(identifier: identifier, content: content, trigger: trigger),
                        revision: revision
                    )
                    guard revision == schedulingRevision else { return false }
                }
            }
        }

        return revision == schedulingRevision
    }

    private func ensureAuthorization() async -> Bool {
        let settings = await center.notificationSettings()
        switch settings.authorizationStatus {
        case .authorized, .provisional, .ephemeral:
            return true
        case .notDetermined:
            return await requestAuthorization()
        case .denied:
            return false
        @unknown default:
            return false
        }
    }

    private func removeExistingPrayerNotifications(for revision: Int) async {
        let requests = await center.pendingNotificationRequests()
        guard revision == schedulingRevision else { return }

        let ids = requests
            .map(\.identifier)
            .filter { $0.hasPrefix(prayerIdentifierPrefix) }
        guard !ids.isEmpty else { return }
        center.removePendingNotificationRequests(withIdentifiers: ids)
    }

    private func add(_ request: UNNotificationRequest, revision: Int) async {
        guard revision == schedulingRevision else { return }

        do {
            try await center.add(request)
        } catch {
            return
        }

        guard revision != schedulingRevision else { return }
        center.removePendingNotificationRequests(withIdentifiers: [request.identifier])
    }

    private func format(_ date: Date, use24Hour: Bool, language: AppLanguage) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: language == .german ? "de_DE" : "tr_TR")
        formatter.dateFormat = use24Hour ? "HH:mm" : "h:mm a"
        return formatter.string(from: date)
    }
}
