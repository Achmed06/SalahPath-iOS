import Foundation

extension Notification.Name {
    static let prayerTrackerDidChange = Notification.Name("salahpath.prayerTrackerDidChange")
}

enum PrayerTrackerStore {
    private static let prefix = "prayerTracker-"

    static let requiredKinds: [PrayerKind] = [.fajr, .dhuhr, .asr, .maghrib, .isha]

    private static func localDayToken(for date: Date) -> String {
        LocalDay.token(for: date)
    }

    private static func key(for date: Date) -> String {
        prefix + localDayToken(for: date)
    }

    static func completedKinds(for date: Date) -> Set<String> {
        let allowed = Set(requiredKinds.map(\.rawValue))
        let stored = Set(UserDefaults.standard.stringArray(forKey: key(for: date)) ?? [])
        return stored.intersection(allowed)
    }

    static func isCompleted(_ kind: PrayerKind, on date: Date) -> Bool {
        completedKinds(for: date).contains(kind.rawValue)
    }

    @discardableResult
    static func toggle(_ kind: PrayerKind, on date: Date) -> Bool {
        let calendar = LocalDay.calendar()
        let day = calendar.startOfDay(for: date)
        let today = calendar.startOfDay(for: Date())
        guard day <= today else { return false }

        var current = completedKinds(for: day)
        let inserted: Bool
        if current.contains(kind.rawValue) {
            current.remove(kind.rawValue)
            inserted = false
        } else {
            current.insert(kind.rawValue)
            inserted = true
        }
        UserDefaults.standard.set(Array(current).sorted(), forKey: key(for: day))
        NotificationCenter.default.post(name: .prayerTrackerDidChange, object: nil)
        return inserted
    }

    private static let pausePrefix = "prayerTrackerPause-"

    private static func pauseKey(for date: Date) -> String {
        pausePrefix + localDayToken(for: date)
    }

    static func isPaused(_ date: Date) -> Bool {
        UserDefaults.standard.bool(forKey: pauseKey(for: date))
    }

    static func setPaused(_ paused: Bool, on date: Date) {
        let calendar = LocalDay.calendar()
        let day = calendar.startOfDay(for: date)
        let today = calendar.startOfDay(for: Date())
        guard day <= today else { return }
        guard isPaused(day) != paused else { return }

        UserDefaults.standard.set(paused, forKey: pauseKey(for: day))
        NotificationCenter.default.post(name: .prayerTrackerDidChange, object: nil)
    }

    static func togglePause(_ date: Date) {
        setPaused(!isPaused(date), on: date)
    }

    static func completedCount(on date: Date) -> Int {
        requiredKinds.filter { isCompleted($0, on: date) }.count
    }

    static func streak(upTo date: Date) -> Int {
        let calendar = LocalDay.calendar()
        var day = calendar.startOfDay(for: date)

        if !isPaused(day) && completedCount(on: day) < requiredKinds.count,
           let yesterday = calendar.date(byAdding: .day, value: -1, to: day) {
            day = yesterday
        }

        var total = 0
        var safety = 0
        while safety < 730 {
            safety += 1
            if isPaused(day) {
                guard let previous = calendar.date(byAdding: .day, value: -1, to: day) else { break }
                day = previous
                continue
            }
            guard completedCount(on: day) == requiredKinds.count else { break }
            total += 1
            guard let previous = calendar.date(byAdding: .day, value: -1, to: day) else { break }
            day = previous
        }
        return total
    }
}
