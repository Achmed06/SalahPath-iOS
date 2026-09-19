from pathlib import Path

# SalahPath v3.15: strict visual parity for Gebetszeiten / Qibla.

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")
start = s.index("struct PrayerTimesOverviewView: View {")
end = s.index("\nprivate struct ReferencePagePattern", start)

new = r'''struct PrayerTimesOverviewView: View {
    @EnvironmentObject private var locationManager: LocationManager
    @EnvironmentObject private var settings: SettingsStore
    @State private var period = 0
    private let engine = PrayerEngine()

    var body: some View {
        ScrollView {
            VStack(spacing: 10) {
                Picker(settings.t("Zeitraum", "Dönem"), selection: $period) {
                    Text(settings.t("Heute", "Bugün")).tag(0)
                    Text(settings.t("Wöchentlich", "Haftalık")).tag(1)
                    Text(settings.t("Monatlich", "Aylık")).tag(2)
                }
                .pickerStyle(.segmented)
                .padding(5)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 13).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }

                if let location = locationManager.location {
                    if period == 0, let day = engine.calculateDay(for: Date(), location: location, settings: settings) {
                        referenceTodayCard(day: day, location: location)

                        HStack(spacing: 8) {
                            NavigationLink { QiblaView() } label: {
                                referenceToolTile(
                                    icon: "location.north.circle.fill",
                                    title: settings.t("Qibla-Richtung", "Kıble Yönü"),
                                    subtitle: "Qibla"
                                )
                            }
                            .buttonStyle(.plain)

                            referenceMapTile
                        }

                        HStack(spacing: 7) {
                            Image(systemName: "location.fill")
                                .font(.system(size: 10, weight: .bold))
                                .foregroundStyle(SalahTheme.teal)
                            Text(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
                                .font(.system(size: 9.5, weight: .bold))
                                .foregroundStyle(SalahTheme.ink)
                            Spacer()
                            Text(settings.t("GPS-basiert", "GPS tabanlı"))
                                .font(.system(size: 8, weight: .semibold))
                                .foregroundStyle(SalahTheme.mutedInk)
                        }
                        .padding(.horizontal, 11)
                        .padding(.vertical, 8)
                        .background(SalahTheme.softTeal.opacity(0.80), in: RoundedRectangle(cornerRadius: 12))
                    } else {
                        ForEach(days, id: \.self) { date in
                            if let day = engine.calculateDay(for: date, location: location, settings: settings) {
                                compactDayCard(day: day, date: date)
                            }
                        }
                    }
                } else {
                    ContentUnavailableView(
                        settings.t("Standort benötigt", "Konum gerekli"),
                        systemImage: "location.slash",
                        description: Text(settings.t("Für Gebetszeiten wird dein aktueller Standort benötigt.", "Namaz vakitleri için mevcut konumun gerekir."))
                    )
                }
            }
            .padding(.horizontal, 11)
            .padding(.vertical, 10)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetszeiten", "Gebetszeiten"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear { locationManager.requestAccessAndStart() }
    }

    private func referenceTodayCard(day: PrayerDay, location: CLLocation) -> some View {
        let next = engine.nextPrayer(now: Date(), location: location, settings: settings)

        return VStack(spacing: 0) {
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text(settings.t("Gebetszeiten", "Gebetszeiten"))
                        .font(.system(size: 18, weight: .bold, design: .serif))
                    Text(settings.t("Namaz vakitleri", "Namaz vakitleri"))
                        .font(.system(size: 9, weight: .semibold))
                        .opacity(0.78)
                }
                Spacer()
                Image(systemName: "bell.fill")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundStyle(SalahTheme.gold)
            }
            .padding(.horizontal, 13)
            .padding(.vertical, 10)
            .background(
                LinearGradient(colors: [SalahTheme.deepTeal, SalahTheme.teal], startPoint: .leading, endPoint: .trailing)
            )
            .foregroundStyle(.white)

            VStack(spacing: 0) {
                ForEach(Array(day.prayers.enumerated()), id: \.element.id) { index, prayer in
                    let isNext = next?.kind == prayer.kind &&
                        Calendar.current.isDate(prayer.date, inSameDayAs: next?.date ?? .distantPast)

                    HStack(spacing: 9) {
                        Image(systemName: prayer.kind.systemImage)
                            .font(.system(size: 13, weight: .semibold))
                            .foregroundStyle(isNext ? SalahTheme.teal : SalahTheme.mutedInk)
                            .frame(width: 22)

                        Text(referencePrayerName(prayer.kind))
                            .font(.system(size: 12.5, weight: isNext ? .bold : .semibold))
                            .foregroundStyle(SalahTheme.ink)

                        Spacer()

                        Text(timeString(prayer.date, use24Hour: settings.use24Hour))
                            .font(.system(size: 13, weight: .bold).monospacedDigit())
                            .foregroundStyle(SalahTheme.ink)
                    }
                    .padding(.horizontal, 13)
                    .padding(.vertical, 9)
                    .background(isNext ? SalahTheme.gold.opacity(0.17) : Color.clear)

                    if index < day.prayers.count - 1 {
                        Divider().padding(.leading, 44).opacity(0.38)
                    }
                }
            }
            .background(SalahTheme.cream)
        }
        .clipShape(RoundedRectangle(cornerRadius: 17, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 17).stroke(SalahTheme.gold.opacity(0.52), lineWidth: 1) }
        .shadow(color: SalahTheme.deepTeal.opacity(0.055), radius: 7, y: 3)
    }

    private var referenceMapTile: some View {
        VStack(spacing: 6) {
            ZStack {
                RoundedRectangle(cornerRadius: 8)
                    .fill(SalahTheme.softTeal)
                    .frame(height: 51)
                Image(systemName: "map.fill")
                    .font(.system(size: 28, weight: .semibold))
                    .foregroundStyle(SalahTheme.teal)
                Image(systemName: "mappin.circle.fill")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundStyle(SalahTheme.gold)
                    .offset(x: 19, y: -7)
            }
            Text(settings.t("Standort", "Konum"))
                .font(.system(size: 10.5, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
            Text(settings.t("Karte", "Harita"))
                .font(.system(size: 8.5, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)
        }
        .frame(maxWidth: .infinity, minHeight: 102)
        .padding(9)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }
    }

    private func referenceToolTile(icon: String, title: String, subtitle: String) -> some View {
        VStack(spacing: 5) {
            ZStack {
                Circle()
                    .fill(SalahTheme.softTeal)
                    .frame(width: 51, height: 51)
                Image(systemName: icon)
                    .font(.system(size: 29, weight: .semibold))
                    .foregroundStyle(SalahTheme.teal)
            }
            Text(title)
                .font(.system(size: 10.5, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .multilineTextAlignment(.center)
                .lineLimit(2)
            Text(subtitle)
                .font(.system(size: 8.5, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)
        }
        .frame(maxWidth: .infinity, minHeight: 102)
        .padding(9)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }
    }

    private func referencePrayerName(_ kind: PrayerKind) -> String {
        if settings.language == .turkish {
            switch kind {
            case .fajr: return "İmsak"
            case .sunrise: return "Sabah"
            case .dhuhr: return "Öğle"
            case .asr: return "İkindi"
            case .maghrib: return "Akşam"
            case .isha: return "Yatsı"
            }
        }
        switch kind {
        case .fajr: return "Fajr"
        case .sunrise: return "Sonnenaufgang"
        case .dhuhr: return "Dhuhr"
        case .asr: return "Asr"
        case .maghrib: return "Maghrib"
        case .isha: return "Isha"
        }
    }

    private func compactDayCard(day: PrayerDay, date: Date) -> some View {
        VStack(alignment: .leading, spacing: 7) {
            HStack {
                VStack(alignment: .leading, spacing: 1) {
                    Text(shortDate(date))
                        .font(.system(size: 13, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                    Text(hijriDateString(date, language: settings.language))
                        .font(.system(size: 8.5, weight: .medium))
                        .foregroundStyle(SalahTheme.mutedInk)
                }
                Spacer()
                if Calendar.current.isDateInToday(date) {
                    Text(settings.t("HEUTE", "BUGÜN"))
                        .font(.system(size: 8, weight: .black))
                        .foregroundStyle(SalahTheme.teal)
                        .padding(.horizontal, 7)
                        .padding(.vertical, 4)
                        .background(SalahTheme.softTeal, in: Capsule())
                }
            }

            ForEach(day.prayers) { prayer in
                HStack {
                    Text(referencePrayerName(prayer.kind))
                        .font(.system(size: 10.5, weight: .semibold))
                    Spacer()
                    Text(timeString(prayer.date, use24Hour: settings.use24Hour))
                        .font(.system(size: 10.5, weight: .bold).monospacedDigit())
                }
                .foregroundStyle(SalahTheme.ink)
            }
        }
        .padding(12)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
    }

    private var days: [Date] {
        let count = period == 1 ? 7 : 30
        let start = Calendar.current.startOfDay(for: Date())
        return (0..<count).compactMap { Calendar.current.date(byAdding: .day, value: $0, to: start) }
    }

    private func shortDate(_ date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        f.dateFormat = "EEE, d. MMM"
        return f.string(from: date)
    }
}
'''

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8")

p = Path("SalahZeit/Views/QiblaView.swift")
p.write_text(r'''import SwiftUI
import Adhan

struct QiblaView: View {
    @EnvironmentObject private var locationManager: LocationManager
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        Group {
            if let location = locationManager.location {
                let coordinates = Coordinates(latitude: location.coordinate.latitude, longitude: location.coordinate.longitude)
                let qibla = Qibla(coordinates: coordinates).direction
                let heading = currentHeading
                let rotation = normalized(qibla - heading)

                ScrollView {
                    VStack(spacing: 11) {
                        VStack(spacing: 2) {
                            Text(settings.t("Qibla / Kıble", "Qibla / Kıble"))
                                .font(.system(size: 20, weight: .bold, design: .serif))
                                .foregroundStyle(SalahTheme.ink)
                            Text(settings.t("Qibla-Richtung", "Kıble Yönü"))
                                .font(.system(size: 10, weight: .semibold))
                                .foregroundStyle(SalahTheme.mutedInk)
                        }

                        ZStack {
                            Circle()
                                .fill(SalahTheme.cream)
                                .frame(width: 268, height: 268)
                                .shadow(color: SalahTheme.deepTeal.opacity(0.055), radius: 8, y: 3)

                            Circle()
                                .stroke(SalahTheme.gold.opacity(0.60), lineWidth: 1.5)
                                .frame(width: 258, height: 258)

                            Circle()
                                .stroke(SalahTheme.teal.opacity(0.14), lineWidth: 1)
                                .frame(width: 226, height: 226)

                            ForEach(0..<36, id: \.self) { index in
                                Capsule()
                                    .fill(SalahTheme.teal.opacity(index % 9 == 0 ? 0.78 : 0.22))
                                    .frame(width: index % 9 == 0 ? 2.8 : 1.3, height: index % 9 == 0 ? 15 : 7)
                                    .offset(y: -120)
                                    .rotationEffect(.degrees(Double(index) * 10))
                            }

                            Text("N")
                                .font(.system(size: 10, weight: .black))
                                .foregroundStyle(SalahTheme.teal)
                                .offset(y: -103)

                            ZStack {
                                RoundedRectangle(cornerRadius: 4)
                                    .fill(Color.black.opacity(0.90))
                                    .frame(width: 45, height: 39)
                                Rectangle()
                                    .fill(SalahTheme.gold)
                                    .frame(width: 45, height: 4)
                                    .offset(y: -7)
                            }
                            .offset(y: 27)

                            Image(systemName: "location.north.fill")
                                .font(.system(size: 88, weight: .medium))
                                .foregroundStyle(SalahTheme.teal.opacity(0.92))
                                .rotationEffect(.degrees(rotation))
                                .offset(y: -25)
                                .animation(.easeOut(duration: 0.18), value: rotation)
                        }

                        HStack(spacing: 8) {
                            compactInfoTile(icon: "location.north.circle.fill", title: settings.t("Qibla", "Kıble"), value: "\(Int(qibla.rounded()))°")
                            compactInfoTile(icon: "iphone", title: settings.t("Gerät", "Cihaz"), value: "\(Int(heading.rounded()))°")
                        }

                        VStack(spacing: 0) {
                            infoRow(icon: "location.fill", title: locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
                            infoRow(icon: "compass.drawing", title: settings.t("iPhone flach halten", "iPhone'u düz tut"))
                            infoRow(icon: "arrow.triangle.2.circlepath", title: settings.t("Bei Bedarf kurz in einer Acht bewegen", "Gerekirse kısa süre sekiz şeklinde hareket ettir"))
                        }
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 10)
                }
                .scrollIndicators(.hidden)
            } else {
                ContentUnavailableView(
                    settings.t("Standort benötigt", "Konum gerekli"),
                    systemImage: "location.slash",
                    description: Text(settings.t("Die Qibla-Richtung wird aus deinem Standort berechnet.", "Kıble yönü konumuna göre hesaplanır."))
                )
            }
        }
        .background(SalahTheme.page.ignoresSafeArea())
        .navigationTitle(settings.t("Qibla", "Kıble"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
        .onAppear { locationManager.requestAccessAndStart() }
    }

    private func compactInfoTile(icon: String, title: String, value: String) -> some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .font(.system(size: 21, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
            Text(title)
                .font(.system(size: 9, weight: .bold))
                .foregroundStyle(SalahTheme.mutedInk)
            Text(value)
                .font(.system(size: 18, weight: .bold).monospacedDigit())
                .foregroundStyle(SalahTheme.ink)
        }
        .frame(maxWidth: .infinity, minHeight: 82)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }
    }

    private func infoRow(icon: String, title: String) -> some View {
        HStack(spacing: 9) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 14, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
            Image(systemName: icon)
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 20)
            Text(title)
                .font(.system(size: 10.5, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer()
        }
        .padding(.horizontal, 11)
        .padding(.vertical, 10)
        .overlay(alignment: .bottom) { Divider().padding(.leading, 50).opacity(0.34) }
    }

    private var currentHeading: Double {
        guard let heading = locationManager.heading else { return 0 }
        return heading.trueHeading >= 0 ? heading.trueHeading : heading.magneticHeading
    }

    private func normalized(_ angle: Double) -> Double {
        var result = angle.truncatingRemainder(dividingBy: 360)
        if result > 180 { result -= 360 }
        if result < -180 { result += 360 }
        return result
    }
}
''', encoding="utf-8")

p = Path("scripts/build_unsigned_ipa.sh")
s = p.read_text(encoding="utf-8")
s = s.replace('MARKETING_VERSION="3.14"', 'MARKETING_VERSION="3.15"')
s = s.replace('CURRENT_PROJECT_VERSION="19"', 'CURRENT_PROJECT_VERSION="20"')
p.write_text(s, encoding="utf-8")

print("SalahPath v3.15 prayer times + qibla reference parity patch applied")
