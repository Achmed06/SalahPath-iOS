from pathlib import Path

# SalahPath v3.25 — first real screenshot-driven parity correction.
home = Path("SalahZeit/Views/HomeView.swift")
s = home.read_text(encoding="utf-8")

# Exact reference palette measured from the supplied artwork/screenshot.
s = s.replace(
'''    static let teal = Color(red: 0.015, green: 0.36, blue: 0.33)
    static let deepTeal = Color(red: 0.012, green: 0.25, blue: 0.25)
    static let gold = Color(red: 0.80, green: 0.62, blue: 0.25)
    static let cream = Color(red: 0.992, green: 0.973, blue: 0.905)
    static let page = Color(red: 0.958, green: 0.939, blue: 0.856)
    static let ink = Color(red: 0.035, green: 0.14, blue: 0.17)
    static let mutedInk = Color(red: 0.27, green: 0.34, blue: 0.34)
    static let softTeal = Color(red: 0.91, green: 0.955, blue: 0.93)
''',
'''    static let teal = Color(red: 43/255, green: 86/255, blue: 82/255)
    static let deepTeal = Color(red: 36/255, green: 79/255, blue: 77/255)
    static let gold = Color(red: 234/255, green: 185/255, blue: 80/255)
    static let cream = Color(red: 250/255, green: 250/255, blue: 241/255)
    static let page = Color(red: 235/255, green: 232/255, blue: 216/255)
    static let ink = Color(red: 15/255, green: 39/255, blue: 50/255)
    static let mutedInk = Color(red: 82/255, green: 103/255, blue: 101/255)
    static let softTeal = Color(red: 230/255, green: 238/255, blue: 232/255)
''')

# Home must read as cream cut-outs on a petrol sheet.
s = s.replace(
'''        ZStack(alignment: .top) {
            SalahTheme.page.ignoresSafeArea()
            ReferencePagePattern()
                .ignoresSafeArea()
                .allowsHitTesting(false)
            SalahTheme.deepTeal
''',
'''        ZStack(alignment: .top) {
            SalahTheme.deepTeal.ignoresSafeArea()
            SalahTheme.deepTeal
''', 1)

s = s.replace('LazyVStack(spacing: 8)', 'LazyVStack(spacing: 5)', 1)
s = s.replace('.padding(.horizontal, 9)\n            .padding(.top, 5)\n            .padding(.bottom, 10)',
              '.padding(.horizontal, 7)\n            .padding(.top, 3)\n            .padding(.bottom, 4)', 1)

# Header copy matches the reference phone, independent from app language.
s = s.replace(
'''                Text(settings.language == .german
                    ? "„Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.“"
                    : "„Şüphesiz namaz, müminlere vakitleri belirli bir farzdır.“")
''',
'''                Text("„Şüphesiz namaz, müminlere vakitleri belli bir farzdır.“")
''', 1)

# Replace next-prayer card with a tighter, reference-proportioned composition.
start = s.index("    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {")
end = s.index("\n    private var prayerLegendCard", start)
hero = r'''    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {
        ZStack(alignment: .bottomTrailing) {
            ReferenceMosqueSkyline()
                .frame(width: 188, height: 102)
                .opacity(0.74)
                .offset(x: 10, y: -8)

            VStack(alignment: .leading, spacing: 4) {
                HStack(alignment: .top) {
                    Text("Sıradaki Namaz / Nächstes Gebet")
                        .font(.system(size: 11.6, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)

                    Spacer()

                    VStack(alignment: .trailing, spacing: 0) {
                        Text(gregorianDateShort(now))
                            .font(.system(size: 8.8, weight: .bold))
                            .foregroundStyle(SalahTheme.ink)
                        Text(shortWeekday(now))
                            .font(.system(size: 7.8, weight: .semibold))
                            .foregroundStyle(SalahTheme.mutedInk)
                    }
                }

                HStack(alignment: .center, spacing: 7) {
                    Image(systemName: prayer.kind.systemImage)
                        .font(.system(size: 22, weight: .medium))
                        .symbolRenderingMode(.hierarchical)
                        .foregroundStyle(SalahTheme.gold)
                        .frame(width: 31)

                    VStack(alignment: .leading, spacing: 0) {
                        Text(prayer.kind.localizedName(settings.language))
                            .font(.system(size: 18, weight: .bold, design: .rounded))
                            .foregroundStyle(SalahTheme.ink)

                        Text(countdownString(from: now, to: prayer.date))
                            .font(.system(size: 25, weight: .bold, design: .rounded).monospacedDigit())
                            .foregroundStyle(Color(red: 0.03, green: 0.17, blue: 0.28))
                            .lineLimit(1)
                            .minimumScaleFactor(0.72)
                    }

                    Spacer(minLength: 90)
                }

                HStack(spacing: 4) {
                    Image(systemName: "location.fill")
                        .font(.system(size: 9.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
                        .font(.system(size: 9.8, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                        .lineLimit(1)
                    Spacer()
                }

                HStack(spacing: 3) {
                    let segments = referenceSequence(for: prayer.kind)
                    ForEach(Array(segments.enumerated()), id: \.offset) { index, segment in
                        HStack(spacing: 3) {
                            Text(segment.0)
                                .font(.system(size: 9.4, weight: .bold))
                            Text(segment.1)
                                .font(.system(size: 7.4, weight: .semibold))
                        }
                        .foregroundStyle(SalahTheme.ink)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 4)
                        .background(Color.white.opacity(0.90), in: RoundedRectangle(cornerRadius: 7, style: .continuous))
                        .overlay {
                            RoundedRectangle(cornerRadius: 7, style: .continuous)
                                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7)
                        }

                        if index < segments.count - 1 {
                            Image(systemName: "arrow.right")
                                .font(.system(size: 7, weight: .black))
                                .foregroundStyle(SalahTheme.teal)
                        }
                    }
                }

                Text("„Namaz, müminlere vakitleri belirlenmiş bir farzdır.“ (Nisâ, 103)")
                    .font(.system(size: 7.4, weight: .medium, design: .serif))
                    .italic()
                    .foregroundStyle(SalahTheme.mutedInk)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
            }
            .padding(.horizontal, 8)
            .padding(.vertical, 7)
        }
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.66), lineWidth: 0.8)
        }
        .shadow(color: SalahTheme.deepTeal.opacity(0.025), radius: 2, y: 1)
        .clipped()
    }
'''
s = s[:start] + hero + s[end:]

# Daily dua — screenshot showed this at roughly twice the intended height.
start = s.index("    private var dailyDuaCard: some View {")
end = s.index("\n    private var streakCard", start)
dua = r'''    private var dailyDuaCard: some View {
        let dua = DailyDuaStore.item(for: now)
        return VStack(spacing: 3) {
            HStack(spacing: 6) {
                ZStack {
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(SalahTheme.softTeal)
                        .frame(width: 27, height: 27)
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(SalahTheme.teal)
                }

                Text("Günün Duası / Dua des Tages")
                    .font(.system(size: 11.3, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)

                Spacer()

                Button {
                    DailyDuaSpeaker.speak(dua.arabic)
                } label: {
                    Image(systemName: "speaker.wave.2.fill")
                        .font(.system(size: 11.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                        .frame(width: 28, height: 28)
                        .background(Color.white.opacity(0.88), in: RoundedRectangle(cornerRadius: 8))
                }
                .buttonStyle(.plain)
            }

            Text(dua.arabic)
                .font(.system(size: 19.5, weight: .medium))
                .frame(maxWidth: .infinity)
                .multilineTextAlignment(.center)
                .lineLimit(1)
                .minimumScaleFactor(0.82)

            Text(settings.language == .german ? dua.deMeaning : dua.trMeaning)
                .font(.system(size: 9.2, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
                .frame(maxWidth: .infinity)
                .multilineTextAlignment(.center)
                .lineLimit(1)
                .minimumScaleFactor(0.80)

            Text(dua.source)
                .font(.system(size: 7.4, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)
                .frame(maxWidth: .infinity)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 6)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
    }
'''
s = s[:start] + dua + s[end:]

# Tracking — use one compact card with a subtle vertical separator, like the reference.
start = s.index("    private var streakCard: some View {")
end = s.index("\n    private var dailyDeenCard", start)
track = r'''    private var streakCard: some View {
        let streak = PrayerTrackerStore.streak(upTo: now)
        let week = currentWeekDates()

        return HStack(spacing: 7) {
            VStack(alignment: .leading, spacing: 5) {
                HStack(spacing: 5) {
                    Image(systemName: "checkmark.circle.fill")
                        .font(.system(size: 11, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text("Namaz Takibi / Gebets-Tracking")
                        .font(.system(size: 10.8, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                }

                HStack(spacing: 3) {
                    ForEach(Array(week.enumerated()), id: \.offset) { _, date in
                        let done = PrayerTrackerStore.completedCount(on: date) == PrayerTrackerStore.requiredKinds.count
                        let pausedDay = PrayerTrackerStore.isPaused(date)
                        VStack(spacing: 2) {
                            ZStack {
                                Circle()
                                    .stroke(done ? SalahTheme.teal : SalahTheme.teal.opacity(0.30), lineWidth: 1)
                                    .frame(width: 19, height: 19)
                                if done {
                                    Circle().fill(SalahTheme.teal).frame(width: 19, height: 19)
                                    Image(systemName: "checkmark")
                                        .font(.system(size: 7.5, weight: .black))
                                        .foregroundStyle(.white)
                                } else if pausedDay {
                                    Image(systemName: "pause.fill")
                                        .font(.system(size: 6.5, weight: .bold))
                                        .foregroundStyle(SalahTheme.mutedInk)
                                }
                            }
                            Text(shortWeekdayLetter(date))
                                .font(.system(size: 6.8, weight: .bold))
                                .foregroundStyle(Calendar.current.isDateInToday(date) ? SalahTheme.teal : SalahTheme.mutedInk)
                        }
                        .frame(maxWidth: .infinity)
                    }
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            Rectangle()
                .fill(SalahTheme.gold.opacity(0.26))
                .frame(width: 0.7, height: 61)

            VStack(spacing: 0) {
                HStack(spacing: 4) {
                    Image(systemName: "flame.fill")
                        .font(.system(size: 16))
                        .foregroundStyle(SalahTheme.gold)
                    Text("\(streak)")
                        .font(.system(size: 19, weight: .bold).monospacedDigit())
                        .foregroundStyle(SalahTheme.ink)
                }
                Text("Günlük Seri")
                    .font(.system(size: 7.1, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                Text("Tage in Folge")
                    .font(.system(size: 6.5, weight: .semibold))
                    .foregroundStyle(SalahTheme.mutedInk)
                Text("İstikrar başarının anahtarıdır.")
                    .font(.system(size: 5.9, weight: .medium, design: .serif))
                    .italic()
                    .multilineTextAlignment(.center)
                    .foregroundStyle(SalahTheme.mutedInk)
                    .lineLimit(2)
                    .padding(.top, 3)
            }
            .frame(width: 82)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 7)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
    }
'''
s = s[:start] + track + s[end:]

# Grid + quote: tighter corners, thinner borders, no floating-card shadow.
s = s.replace('let columns = Array(repeating: GridItem(.flexible(), spacing: 5), count: 4)',
              'let columns = Array(repeating: GridItem(.flexible(), spacing: 4), count: 4)', 1)
s = s.replace('return LazyVGrid(columns: columns, spacing: 5)',
              'return LazyVGrid(columns: columns, spacing: 4)', 1)

s = s.replace('in: RoundedRectangle(cornerRadius: 14, style: .continuous)',
              'in: RoundedRectangle(cornerRadius: 9, style: .continuous)', 1)
s = s.replace('RoundedRectangle(cornerRadius: 14, style: .continuous)\n                .stroke(SalahTheme.gold.opacity(0.36), lineWidth: 1)',
              'RoundedRectangle(cornerRadius: 9, style: .continuous)\n                .stroke(SalahTheme.gold.opacity(0.36), lineWidth: 0.8)', 1)

# DashboardTile definition.
tile_start = s.index("private struct DashboardTile: View {")
tile_end = s.index("\nprivate struct PrayerRow", tile_start)
tile = s[tile_start:tile_end]
tile = tile.replace('.font(.system(size: 19, weight: .semibold))', '.font(.system(size: 18, weight: .semibold))')
tile = tile.replace('.frame(height: 25)', '.frame(height: 22)')
tile = tile.replace('.font(.system(size: 9.8, weight: .bold))', '.font(.system(size: 8.7, weight: .bold))')
tile = tile.replace('.font(.system(size: 7.5, weight: .semibold))', '.font(.system(size: 6.7, weight: .semibold))')
tile = tile.replace('.frame(maxWidth: .infinity, minHeight: 70, alignment: .center)',
                    '.frame(maxWidth: .infinity, minHeight: 61, alignment: .center)')
tile = tile.replace('.padding(.vertical, 6)', '.padding(.vertical, 5)')
tile = tile.replace('RoundedRectangle(cornerRadius: 12, style: .continuous)',
                    'RoundedRectangle(cornerRadius: 9, style: .continuous)')
tile = tile.replace('.stroke(SalahTheme.gold.opacity(0.56), lineWidth: 1)',
                    '.stroke(SalahTheme.gold.opacity(0.56), lineWidth: 0.8)')
tile = tile.replace('.shadow(color: SalahTheme.deepTeal.opacity(0.035), radius: 3, y: 1)', '')
s = s[:tile_start] + tile + s[tile_end:]

home.write_text(s, encoding="utf-8")

# Bottom navigation labels on the central reference phone are fixed Turkish labels.
root = Path("SalahZeit/Views/RootTabView.swift")
r = root.read_text(encoding="utf-8")
r = r.replace(
'''        navigation.backgroundColor = UIColor(red: 0.012, green: 0.25, blue: 0.25, alpha: 1)
        navigation.shadowColor = UIColor(red: 0.80, green: 0.62, blue: 0.25, alpha: 0.32)
''',
'''        navigation.backgroundColor = UIColor(red: 36/255, green: 79/255, blue: 77/255, alpha: 1)
        navigation.shadowColor = UIColor(red: 234/255, green: 185/255, blue: 80/255, alpha: 0.28)
''')
r = r.replace(
'''        [
            ("house.fill", settings.t("Startseite", "Ana Sayfa")),
            ("book.closed.fill", settings.t("Quran", "Kur'an")),
            ("building.columns.fill", settings.t("Namaz", "Namaz")),
            ("safari.fill", settings.t("Entdecken", "Keşfet")),
            ("person.crop.circle.fill", settings.t("Profil", "Profil"))
        ]
''',
'''        [
            ("house.fill", "Ana Sayfa"),
            ("book.closed.fill", "Kur'an"),
            ("building.columns.fill", "Namaz"),
            ("safari.fill", "Keşfet"),
            ("person.crop.circle.fill", "Profil")
        ]
''')
r = r.replace('.padding(.top, 7)\n        .padding(.bottom, 3)',
              '.padding(.top, 5)\n        .padding(.bottom, 2)', 1)
r = r.replace('.frame(height: 25)', '.frame(height: 22)', 1)
r = r.replace('.font(.system(size: 8.1, weight: selection == index ? .bold : .semibold))',
              '.font(.system(size: 7.7, weight: selection == index ? .bold : .semibold))', 1)
root.write_text(r, encoding="utf-8")

build = Path("scripts/build_unsigned_ipa.sh")
b = build.read_text(encoding="utf-8")
b = b.replace('MARKETING_VERSION="3.24"', 'MARKETING_VERSION="3.25"')
b = b.replace('CURRENT_PROJECT_VERSION="29"', 'CURRENT_PROJECT_VERSION="30"')
build.write_text(b, encoding="utf-8")

print("SalahPath v3.25 screenshot-driven Home parity pass applied")
