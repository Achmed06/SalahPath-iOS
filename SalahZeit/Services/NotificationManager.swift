import Foundation
import CoreLocation
import UserNotifications
import AVFoundation

@MainActor
struct NotificationDiagnostics: Sendable {
    let authorizationStatus: UNAuthorizationStatus
    let alertsEnabled: Bool
    let soundsEnabled: Bool
    let pendingPrayerRequests: Int
    let pendingTotalRequests: Int
    let standardAdhanInstalled: Bool
    let fajrAdhanInstalled: Bool
}

@MainActor
final class NotificationManager: NSObject, UNUserNotificationCenterDelegate {
    static let shared = NotificationManager()
    private let center = UNUserNotificationCenter.current()
    private let engine = PrayerEngine()
    private let prayerIdentifierPrefix = "salahzeit.prayer."
    private let adhanPreviewIdentifier = "salahzeit.adhan.preview"
    private let standardAdhanSoundFileName = "adhan-standard.caf"
    private let fajrAdhanSoundFileName = "adhan-fajr.caf"
    private let maximumPrayerRequests = 60
    private let notificationPreviewIdentifier = "salahzeit.notification.preview"
    private var schedulingRevision = 0
    private var adhanPreviewPlayer: AVAudioPlayer?

    private override init() {
        super.init()
        center.delegate = self
        installNotificationSoundsIfNeeded()
    }

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

        Task { @MainActor [weak self] in
            guard let self else { return }
            let requests = await self.center.pendingNotificationRequests()
            guard revision == self.schedulingRevision else { return }

            let ids = requests
                .map(\.identifier)
                .filter { $0.hasPrefix(self.prayerIdentifierPrefix) }
            guard !ids.isEmpty else { return }

            self.center.removePendingNotificationRequests(withIdentifiers: ids)
        }
    }

    @discardableResult
    func scheduleNextSevenDays(
        location: CLLocation,
        settings: SettingsStore,
        timeZone: TimeZone = .autoupdatingCurrent
    ) async -> Bool {
        schedulingRevision &+= 1
        let revision = schedulingRevision

        await removeExistingPrayerNotifications(for: revision)
        guard revision == schedulingRevision else { return false }
        guard settings.notificationsEnabled else { return false }

        let granted = await ensureAuthorization()
        guard revision == schedulingRevision, granted else { return false }

        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = timeZone
        let now = Date()
        var allRequestsScheduled = true
        var scheduledIdentifiers = Set<String>()
        var scheduledRequestCount = 0

        // Phase 1: reserve capacity for every enabled prayer-time alert first.
        // With 5 prayers over 7 days this is at most 35 requests, so exact
        // prayer-time notifications cannot be crowded out by advance reminders.
        if settings.notifyAtPrayerTime {
            for dayOffset in 0..<7 {
                guard revision == schedulingRevision else { return false }
                guard let date = calendar.date(byAdding: .day, value: dayOffset, to: now),
                      let day = engine.calculateDay(
                          for: date,
                          location: location,
                          settings: settings,
                          timeZone: timeZone
                      ) else {
                    allRequestsScheduled = false
                    continue
                }

                for prayer in day.prayers where prayer.kind != .sunrise {
                    guard revision == schedulingRevision else { return false }
                    guard settings.notificationEnabled(for: prayer.kind),
                          prayer.date > now,
                          scheduledRequestCount < maximumPrayerRequests else { continue }

                    let prayerName = prayer.kind.localizedName(settings.language)
                    let content = UNMutableNotificationContent()
                    content.title = settings.t("\(prayerName) beginnt", "\(prayerName) vakti başladı")
                    if let rakats = prayer.kind.fardRakats {
                        content.body = settings.t(
                            "\(rakats) Rakʿāt Fard • \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language, timeZone: timeZone))",
                            "\(rakats) rekât farz • \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language, timeZone: timeZone))"
                        )
                    }
                    content.sound = prayerTimeSound(for: prayer.kind, settings: settings)

                    var components = calendar.dateComponents([.year, .month, .day, .hour, .minute], from: prayer.date)
                    components.timeZone = timeZone
                    let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)
                    let identifier = "salahzeit.prayer.r\(revision).\(dayOffset).\(prayer.kind.rawValue).time"
                    let added = await add(
                        UNNotificationRequest(identifier: identifier, content: content, trigger: trigger),
                        revision: revision
                    )
                    allRequestsScheduled = allRequestsScheduled && added
                    if added {
                        scheduledIdentifiers.insert(identifier)
                        scheduledRequestCount += 1
                    }
                    guard revision == schedulingRevision else { return false }
                }
            }
        }

        // Phase 2: spend the remaining request budget on the nearest advance
        // reminders, after every exact prayer-time alert has been reserved.
        let allowedLeadMinutes = [0, 5, 10, 15, 30]
        let leadMinutes = allowedLeadMinutes.contains(settings.notificationLeadMinutes)
            ? settings.notificationLeadMinutes
            : 10

        if leadMinutes > 0 {
            for dayOffset in 0..<7 {
                guard revision == schedulingRevision else { return false }
                guard scheduledRequestCount < maximumPrayerRequests else { break }
                guard let date = calendar.date(byAdding: .day, value: dayOffset, to: now),
                      let day = engine.calculateDay(
                          for: date,
                          location: location,
                          settings: settings,
                          timeZone: timeZone
                      ) else {
                    allRequestsScheduled = false
                    continue
                }

                for prayer in day.prayers where prayer.kind != .sunrise {
                    guard revision == schedulingRevision else { return false }
                    guard scheduledRequestCount < maximumPrayerRequests else { break }
                    guard settings.notificationEnabled(for: prayer.kind) else { continue }

                    let reminderDate = prayer.date.addingTimeInterval(-TimeInterval(leadMinutes) * 60)
                    guard reminderDate > now else { continue }

                    let prayerName = prayer.kind.localizedName(settings.language)
                    let reminder = UNMutableNotificationContent()
                    reminder.title = settings.t(
                        "\(prayerName) in \(leadMinutes) Min.",
                        "\(prayerName) için \(leadMinutes) dk kaldı"
                    )
                    reminder.body = settings.t(
                        "Gebetszeit: \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language, timeZone: timeZone))",
                        "Namaz vakti: \(format(prayer.date, use24Hour: settings.use24Hour, language: settings.language, timeZone: timeZone))"
                    )
                    reminder.sound = .default

                    var components = calendar.dateComponents([.year, .month, .day, .hour, .minute], from: reminderDate)
                    components.timeZone = timeZone
                    let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)
                    let identifier = "salahzeit.prayer.r\(revision).\(dayOffset).\(prayer.kind.rawValue).pre"
                    let added = await add(
                        UNNotificationRequest(identifier: identifier, content: reminder, trigger: trigger),
                        revision: revision
                    )
                    allRequestsScheduled = allRequestsScheduled && added
                    if added {
                        scheduledIdentifiers.insert(identifier)
                        scheduledRequestCount += 1
                    }
                    guard revision == schedulingRevision else { return false }
                }
            }
        }

        guard revision == schedulingRevision else { return false }

        let pending = await center.pendingNotificationRequests()
        guard revision == schedulingRevision else { return false }
        let pendingIDs = Set(
            pending
                .map(\.identifier)
                .filter { $0.hasPrefix(prayerIdentifierPrefix) }
        )

        let anyPrayerEnabled =
            settings.fajrNotificationEnabled ||
            settings.dhuhrNotificationEnabled ||
            settings.asrNotificationEnabled ||
            settings.maghribNotificationEnabled ||
            settings.ishaNotificationEnabled
        let expectsPrayerRequests =
            anyPrayerEnabled &&
            (settings.notifyAtPrayerTime || leadMinutes > 0)

        if !expectsPrayerRequests {
            return allRequestsScheduled &&
                scheduledIdentifiers.isEmpty &&
                pendingIDs.isEmpty
        }

        return allRequestsScheduled &&
            !scheduledIdentifiers.isEmpty &&
            scheduledIdentifiers.isSubset(of: pendingIDs)
    }

    @discardableResult
    func playAdhanPreviewDirect(fajr: Bool) -> Bool {
        let resourceName = fajr ? "adhan-fajr" : "adhan-standard"
        guard let url = Bundle.main.url(forResource: resourceName, withExtension: "caf") else {
            return false
        }

        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .default)
            try session.setActive(true, options: [])
            let player = try AVAudioPlayer(contentsOf: url)
            player.volume = 1
            player.prepareToPlay()
            adhanPreviewPlayer?.stop()
            adhanPreviewPlayer = player
            return player.play()
        } catch {
            adhanPreviewPlayer = nil
            return false
        }
    }

    @discardableResult
    func scheduleAdhanPreview(settings: SettingsStore, fajr: Bool) async -> Bool {
        guard await ensureAuthorization() else { return false }

        center.removePendingNotificationRequests(withIdentifiers: [adhanPreviewIdentifier])

        let content = UNMutableNotificationContent()
        content.title = settings.t(
            fajr ? "Fajr Gebetsruf · Test" : "Gebetsruf · Test",
            fajr ? "Sabah ezanı · Test" : "Ezan · Test"
        )
        content.body = settings.t(
            "So klingt der Gebetsruf bei einer Gebetszeit-Benachrichtigung.",
            "Namaz vakti bildiriminde ezan bu şekilde çalar."
        )
        content.sound = adhanSound(fajr: fajr)

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 5, repeats: false)
        do {
            try await center.add(
                UNNotificationRequest(
                    identifier: adhanPreviewIdentifier,
                    content: content,
                    trigger: trigger
                )
            )
            let pending = await center.pendingNotificationRequests()
            return pending.contains { $0.identifier == adhanPreviewIdentifier }
        } catch {
            return false
        }
    }

    @discardableResult
    func scheduleNotificationPreview(settings: SettingsStore) async -> Bool {
        guard await ensureAuthorization() else { return false }

        center.removePendingNotificationRequests(withIdentifiers: [notificationPreviewIdentifier])

        let content = UNMutableNotificationContent()
        content.title = settings.t("SalahPath Test", "SalahPath Test")
        content.body = settings.t(
            "Wenn du diese Mitteilung siehst, funktioniert die iOS-Zustellung.",
            "Bu bildirimi görüyorsan iOS teslimatı çalışıyor."
        )
        content.sound = .default

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 5, repeats: false)
        do {
            try await center.add(
                UNNotificationRequest(
                    identifier: notificationPreviewIdentifier,
                    content: content,
                    trigger: trigger
                )
            )
            let pending = await center.pendingNotificationRequests()
            return pending.contains { $0.identifier == notificationPreviewIdentifier }
        } catch {
            return false
        }
    }

    func diagnostics() async -> NotificationDiagnostics {
        let systemSettings = await center.notificationSettings()
        let pending = await center.pendingNotificationRequests()

        let standardInstalled = soundExists(resourceName: "adhan-standard", fileName: standardAdhanSoundFileName)
        let fajrInstalled = soundExists(resourceName: "adhan-fajr", fileName: fajrAdhanSoundFileName)

        return NotificationDiagnostics(
            authorizationStatus: systemSettings.authorizationStatus,
            alertsEnabled: systemSettings.alertSetting == .enabled ||
                systemSettings.notificationCenterSetting == .enabled ||
                systemSettings.lockScreenSetting == .enabled,
            soundsEnabled: systemSettings.soundSetting == .enabled,
            pendingPrayerRequests: pending.filter { $0.identifier.hasPrefix(prayerIdentifierPrefix) }.count,
            pendingTotalRequests: pending.count,
            standardAdhanInstalled: standardInstalled,
            fajrAdhanInstalled: fajrInstalled
        )
    }

    private func soundExists(resourceName: String, fileName: String) -> Bool {
        let bundled = Bundle.main.url(forResource: resourceName, withExtension: "caf") != nil
        let installed = notificationSoundURL(fileName: fileName)
            .map { FileManager.default.fileExists(atPath: $0.path) } ?? false
        return bundled || installed
    }

    private func prayerTimeSound(for kind: PrayerKind, settings: SettingsStore) -> UNNotificationSound {
        guard settings.adhanSoundEnabled else { return .default }
        let isFajr: Bool
        switch kind {
        case .fajr:
            isFajr = true
        default:
            isFajr = false
        }
        return adhanSound(fajr: isFajr)
    }

    private func adhanSound(fajr: Bool) -> UNNotificationSound {
        let resourceName = fajr ? "adhan-fajr" : "adhan-standard"
        let fileName = fajr ? fajrAdhanSoundFileName : standardAdhanSoundFileName
        let bundled = Bundle.main.url(forResource: resourceName, withExtension: "caf")
        let installed = notificationSoundURL(fileName: fileName)
        let existsInLibrary = installed.map { FileManager.default.fileExists(atPath: $0.path) } ?? false
        guard bundled != nil || existsInLibrary else {
            return .default
        }
        return UNNotificationSound(named: UNNotificationSoundName(rawValue: fileName))
    }

    private func notificationSoundURL(fileName: String) -> URL? {
        FileManager.default.urls(for: .libraryDirectory, in: .userDomainMask)
            .first?
            .appendingPathComponent("Sounds", isDirectory: true)
            .appendingPathComponent(fileName, isDirectory: false)
    }

    private func installNotificationSoundsIfNeeded() {
        guard let library = FileManager.default.urls(for: .libraryDirectory, in: .userDomainMask).first else {
            return
        }

        let soundsDirectory = library.appendingPathComponent("Sounds", isDirectory: true)
        do {
            try FileManager.default.createDirectory(
                at: soundsDirectory,
                withIntermediateDirectories: true
            )
        } catch {
            return
        }

        for resourceName in ["adhan-standard", "adhan-fajr"] {
            guard let source = Bundle.main.url(forResource: resourceName, withExtension: "caf") else {
                continue
            }
            let destination = soundsDirectory.appendingPathComponent("\(resourceName).caf")
            do {
                if FileManager.default.fileExists(atPath: destination.path) {
                    let sourceSize = (try? source.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? -1
                    let destinationSize = (try? destination.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? -2
                    if sourceSize == destinationSize, sourceSize > 0 {
                        continue
                    }
                    try FileManager.default.removeItem(at: destination)
                }
                try FileManager.default.copyItem(at: source, to: destination)
            } catch {
                continue
            }
        }
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

    private func add(_ request: UNNotificationRequest, revision: Int) async -> Bool {
        guard revision == schedulingRevision else { return false }

        do {
            try await center.add(request)
        } catch {
            return false
        }

        guard revision != schedulingRevision else { return true }
        center.removePendingNotificationRequests(withIdentifiers: [request.identifier])
        return false
    }

    nonisolated func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        [.banner, .list, .sound]
    }

    private func format(
        _ date: Date,
        use24Hour: Bool,
        language: AppLanguage,
        timeZone: TimeZone
    ) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: language == .german ? "de_DE" : "tr_TR")
        formatter.timeZone = timeZone
        formatter.dateFormat = use24Hour ? "HH:mm" : "h:mm a"
        return formatter.string(from: date)
    }
}
