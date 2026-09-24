import Foundation
import CoreLocation
import Adhan

@MainActor
struct PrayerEngine {
    func calculateDay(
        for date: Date,
        location: CLLocation,
        settings: SettingsStore,
        calendar: Calendar = .current
    ) -> PrayerDay? {
        let coordinate = location.coordinate
        guard coordinate.latitude.isFinite,
              coordinate.longitude.isFinite,
              CLLocationCoordinate2DIsValid(coordinate) else {
            return nil
        }

        let coordinates = Coordinates(latitude: coordinate.latitude, longitude: coordinate.longitude)
        let components = calendar.dateComponents([.year, .month, .day], from: date)

        var parameters = settings.calculationPreset.method.params
        parameters.madhab = settings.asrRule.madhab
        parameters.highLatitudeRule = HighLatitudeRule.recommended(for: coordinates)

        guard let prayerTimes = PrayerTimes(
            coordinates: coordinates,
            date: components,
            calculationParameters: parameters
        ) else {
            return nil
        }

        let items: [PrayerOccurrence] = [
            .init(kind: .fajr, date: adjusted(prayerTimes.fajr, kind: .fajr, settings: settings)),
            .init(kind: .sunrise, date: prayerTimes.sunrise),
            .init(kind: .dhuhr, date: adjusted(prayerTimes.dhuhr, kind: .dhuhr, settings: settings)),
            .init(kind: .asr, date: adjusted(prayerTimes.asr, kind: .asr, settings: settings)),
            .init(kind: .maghrib, date: adjusted(prayerTimes.maghrib, kind: .maghrib, settings: settings)),
            .init(kind: .isha, date: adjusted(prayerTimes.isha, kind: .isha, settings: settings))
        ]

        let sunnah = SunnahTimes(from: prayerTimes)

        return PrayerDay(
            date: date,
            prayers: items,
            middleOfNight: sunnah?.middleOfTheNight,
            lastThirdOfNight: sunnah?.lastThirdOfTheNight
        )
    }

    func nextPrayer(
        now: Date,
        location: CLLocation,
        settings: SettingsStore,
        calendar: Calendar = .current
    ) -> PrayerOccurrence? {
        guard let today = calculateDay(for: now, location: location, settings: settings, calendar: calendar) else {
            return nil
        }

        if let next = today.prayers.first(where: { $0.kind != .sunrise && $0.date > now }) {
            return next
        }

        guard let tomorrow = calendar.date(byAdding: .day, value: 1, to: now),
              let day = calculateDay(for: tomorrow, location: location, settings: settings, calendar: calendar) else {
            return nil
        }

        return day.prayers.first(where: { $0.kind == .fajr })
    }

    func upcomingPrayers(
        now: Date,
        location: CLLocation,
        settings: SettingsStore,
        count: Int = 2,
        calendar: Calendar = .current
    ) -> [PrayerOccurrence] {
        let safeCount = min(max(count, 1), 10)
        var candidates: [PrayerOccurrence] = []

        if let today = calculateDay(
            for: now,
            location: location,
            settings: settings,
            calendar: calendar
        ) {
            candidates.append(contentsOf: today.prayers)
        }

        if let tomorrowDate = calendar.date(byAdding: .day, value: 1, to: now),
           let tomorrow = calculateDay(
               for: tomorrowDate,
               location: location,
               settings: settings,
               calendar: calendar
           ) {
            candidates.append(contentsOf: tomorrow.prayers)
        }

        return Array(
            candidates
                .filter { $0.kind != .sunrise && $0.date > now }
                .sorted { $0.date < $1.date }
                .prefix(safeCount)
        )
    }

    func prayerWindow(
        for occurrence: PrayerOccurrence,
        day: PrayerDay,
        nextDay: PrayerDay?
    ) -> DateInterval? {
        guard occurrence.kind != .sunrise else { return nil }

        let end: Date?
        switch occurrence.kind {
        case .fajr:
            end = day.time(for: .sunrise)
        case .dhuhr:
            end = day.time(for: .asr)
        case .asr:
            end = day.time(for: .maghrib)
        case .maghrib:
            end = day.time(for: .isha)
        case .isha:
            end = nextDay?.time(for: .fajr)
        case .sunrise:
            end = nil
        }

        guard let end, end > occurrence.date else { return nil }
        return DateInterval(start: occurrence.date, end: end)
    }

    private func adjusted(_ date: Date, kind: PrayerKind, settings: SettingsStore) -> Date {
        let minutes = min(max(settings.offset(for: kind), -15), 15)
        return date.addingTimeInterval(TimeInterval(minutes) * 60)
    }
}
