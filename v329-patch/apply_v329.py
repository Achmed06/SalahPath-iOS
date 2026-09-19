from pathlib import Path

# SalahPath v3.29 — exact QA state + Home geometry correction from v3.28 screenshot.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# A QA-only prayer occurrence lets the simulator screenshot match the supplied reference
# without changing production prayer calculations.
needle = '''    private var effectiveLocality: String {
        if isScreenshotQA { return "İstanbul" }
        return locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum")
    }
'''
replacement = '''    private var effectiveLocality: String {
        if isScreenshotQA { return "İstanbul" }
        return locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum")
    }

    private var qaReferencePrayer: PrayerOccurrence {
        PrayerOccurrence(
            kind: .asr,
            date: effectiveNow.addingTimeInterval((2 * 60 * 60) + (38 * 60) + 15)
        )
    }
'''
if needle not in s:
    raise SystemExit("effectiveLocality block not found")
s = s.replace(needle, replacement, 1)

old = '''                if let next = engine.nextPrayer(now: effectiveNow, location: location, settings: settings) {
                    nextPrayerHero(next)
                }
'''
new = '''                if isScreenshotQA {
                    nextPrayerHero(qaReferencePrayer)
                } else if let next = engine.nextPrayer(now: effectiveNow, location: location, settings: settings) {
                    nextPrayerHero(next)
                }
'''
if old not in s:
    raise SystemExit("next prayer rendering block not found")
s = s.replace(old, new, 1)

# Header: the v3.28 screenshot was visibly too tall.
s = s.replace('.frame(width: 39, height: 48)', '.frame(width: 34, height: 41)', 1)
s = s.replace('.font(.system(size: 21, weight: .bold, design: .serif))',
              '.font(.system(size: 19.5, weight: .bold, design: .serif))', 1)
s = s.replace('.font(.system(size: 8.8, weight: .semibold))',
              '.font(.system(size: 7.8, weight: .semibold))', 1)
s = s.replace('.font(.system(size: 7.7, weight: .medium, design: .serif))',
              '.font(.system(size: 6.8, weight: .medium, design: .serif))', 1)
s = s.replace('.frame(maxWidth: 108, alignment: .trailing)',
              '.frame(maxWidth: 101, alignment: .trailing)', 1)
s = s.replace('.padding(.vertical, 5)\n        .frame(maxWidth: .infinity)',
              '.padding(.vertical, 2)\n        .frame(maxWidth: .infinity, minHeight: 50)', 1)

# Hero: exact QA strings from the poster.
s = s.replace(
'''                        Text(gregorianDateShort(effectiveNow))
                            .font(.system(size: 8.8, weight: .bold))
                            .foregroundStyle(SalahTheme.ink)
                        Text(shortWeekday(effectiveNow))
                            .font(.system(size: 7.8, weight: .semibold))
''',
'''                        Text(isScreenshotQA ? "14 Mart 2025" : gregorianDateShort(effectiveNow))
                            .font(.system(size: 8.4, weight: .bold))
                            .foregroundStyle(SalahTheme.ink)
                        Text(isScreenshotQA ? "Cuma" : shortWeekday(effectiveNow))
                            .font(.system(size: 7.4, weight: .semibold))
''', 1)

s = s.replace(
'''                        Text(prayer.kind.localizedName(settings.language))
                            .font(.system(size: 18, weight: .bold, design: .rounded))
''',
'''                        Text(isScreenshotQA ? "İkindi" : prayer.kind.localizedName(settings.language))
                            .font(.system(size: 19, weight: .bold, design: .rounded))
''', 1)

s = s.replace(
'''                        Text(countdownString(from: effectiveNow, to: prayer.date))
                            .font(.system(size: 25, weight: .bold, design: .rounded).monospacedDigit())
''',
'''                        Text(isScreenshotQA ? "2:38:15" : countdownString(from: effectiveNow, to: prayer.date))
                            .font(.system(size: 27, weight: .bold, design: .rounded).monospacedDigit())
''', 1)

s = s.replace(
'''                    let segments = referenceSequence(for: prayer.kind)
''',
'''                    let segments = isScreenshotQA
                        ? [("4", "Sünnet"), ("4", "Farz"), ("2", "Sünnet")]
                        : referenceSequence(for: prayer.kind)
''', 1)

# v3.28 still had a large rectangular mosque crop. Scale it slightly down and dissolve it
# into the right side of the card.
s = s.replace('.frame(width: 205, height: 126)', '.frame(width: 190, height: 116)', 1)
s = s.replace('.offset(x: 10, y: -1)', '.offset(x: 5, y: -4)', 1)

# Hero needs more vertical weight after shrinking header.
s = s.replace('.frame(minHeight: 178)', '.frame(minHeight: 190)', 1)

# Exact daily dua from the reference in QA.
start = s.index("    private var dailyDuaCard: some View {")
end = s.index("\n    private var streakCard", start)
daily = r'''    private var dailyDuaCard: some View {
        let dua = DailyDuaStore.item(for: effectiveNow)
        let arabic = isScreenshotQA ? "رَبِّ زِدْنِي عِلْمًا" : dua.arabic
        let meaning = isScreenshotQA
            ? "Rabbim, ilmimi artır."
            : (settings.language == .german ? dua.deMeaning : dua.trMeaning)
        let source = isScreenshotQA ? "(Tâhâ, 114)" : dua.source

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
                    .font(.system(size: 10.8, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)

                Spacer()

                Button {
                    DailyDuaSpeaker.speak(arabic)
                } label: {
                    Image(systemName: "speaker.wave.2.fill")
                        .font(.system(size: 11.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                        .frame(width: 28, height: 28)
                        .background(Color.white.opacity(0.88), in: RoundedRectangle(cornerRadius: 8))
                }
                .buttonStyle(.plain)
            }

            Text(arabic)
                .font(.system(size: 22, weight: .medium))
                .frame(maxWidth: .infinity)
                .multilineTextAlignment(.center)
                .lineLimit(1)
                .minimumScaleFactor(0.80)

            Text(meaning)
                .font(.system(size: 9.2, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
                .frame(maxWidth: .infinity)
                .multilineTextAlignment(.center)
                .lineLimit(1)

            Text(source)
                .font(.system(size: 7.3, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)
                .frame(maxWidth: .infinity)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 6)
        .frame(minHeight: 98)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
    }
'''
s = s[:start] + daily + s[end:]

# Exact reference tracking state in QA: first 4 days complete, streak 12.
start = s.index("    private var streakCard: some View {")
end = s.index("\n    private var dailyDeenCard", start)
track = r'''    private var streakCard: some View {
        let streak = isScreenshotQA ? 12 : PrayerTrackerStore.streak(upTo: effectiveNow)
        let week = currentWeekDates()
        let qaLabels = ["Pzt", "Sal", "Çar", "Prş", "Cum", "Cts", "Paz"]

        return HStack(spacing: 7) {
            VStack(alignment: .leading, spacing: 6) {
                HStack(spacing: 5) {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: 20, height: 20)
                        Image(systemName: "checkmark")
                            .font(.system(size: 8, weight: .black))
                            .foregroundStyle(.white)
                    }

                    Text("Namaz Takibi / Gebets-Tracking")
                        .font(.system(size: 10.3, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                }

                HStack(spacing: 3) {
                    ForEach(Array(week.enumerated()), id: .offset) { index, date in
                        let done = isScreenshotQA
                            ? index < 4
                            : PrayerTrackerStore.completedCount(on: date) == PrayerTrackerStore.requiredKinds.count
                        let pausedDay = !isScreenshotQA && PrayerTrackerStore.isPaused(date)

                        VStack(spacing: 2) {
                            ZStack {
                                Circle()
                                    .stroke(done ? SalahTheme.teal : SalahTheme.teal.opacity(0.30), lineWidth: 1)
                                    .frame(width: 21, height: 21)
                                if done {
                                    Circle().fill(SalahTheme.teal).frame(width: 21, height: 21)
                                    Image(systemName: "checkmark")
                                        .font(.system(size: 7.5, weight: .black))
                                        .foregroundStyle(.white)
                                } else if pausedDay {
                                    Image(systemName: "pause.fill")
                                        .font(.system(size: 6.5, weight: .bold))
                                        .foregroundStyle(SalahTheme.mutedInk)
                                }
                            }

                            Text(isScreenshotQA ? qaLabels[index] : shortWeekdayLetter(date))
                                .font(.system(size: 6.5, weight: .bold))
                                .foregroundStyle(SalahTheme.mutedInk)
                        }
                        .frame(maxWidth: .infinity)
                    }
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            Rectangle()
                .fill(SalahTheme.gold.opacity(0.28))
                .frame(width: 0.7, height: 72)

            VStack(spacing: 0) {
                HStack(spacing: 4) {
                    Image(systemName: "flame.fill")
                        .font(.system(size: 18))
                        .foregroundStyle(SalahTheme.gold)
                    Text("\(streak)")
                        .font(.system(size: 21, weight: .bold).monospacedDigit())
                        .foregroundStyle(SalahTheme.ink)
                }

                Text("Günlük Seri")
                    .font(.system(size: 7.0, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                Text("Tage in Folge")
                    .font(.system(size: 6.3, weight: .semibold))
                    .foregroundStyle(SalahTheme.mutedInk)
                Text("İstikrar\nbaşarının anahtarıdır.")
                    .font(.system(size: 5.7, weight: .medium, design: .serif))
                    .italic()
                    .multilineTextAlignment(.center)
                    .foregroundStyle(SalahTheme.mutedInk)
                    .lineLimit(2)
                    .padding(.top, 2)
            }
            .frame(width: 82)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 7)
        .frame(minHeight: 112)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
    }
'''
s = s[:start] + track + s[end:]

# Dashboard in the poster is taller than v3.28 and fills the space before the quote strip.
tile_start = s.index("private struct DashboardTile: View {")
tile_end = s.index("\nprivate struct PrayerRow", tile_start)
tile = s[tile_start:tile_end]
tile = tile.replace('.frame(maxWidth: .infinity, minHeight: 82, alignment: .center)',
                    '.frame(maxWidth: .infinity, minHeight: 92, alignment: .center)')
tile = tile.replace('.font(.system(size: 21, weight: .semibold))',
                    '.font(.system(size: 22, weight: .semibold))')
tile = tile.replace('.frame(height: 26)', '.frame(height: 28)')
s = s[:tile_start] + tile + s[tile_end:]

# Quote strip is immediately above tab bar in the reference.
quote_start = s.index("    private var referenceQuoteStrip: some View {")
quote_end = s.index("\n    private func referenceSequence", quote_start)
quote = s[quote_start:quote_end]
quote = quote.replace('.frame(minHeight: 48)', '.frame(minHeight: 52)')
s = s[:quote_start] + quote + s[quote_end:]

p.write_text(s, encoding="utf-8")

# Bottom bar: no gold active dot; reference uses a subtle circular active icon state.
p = Path("SalahZeit/Views/RootTabView.swift")
r = p.read_text(encoding="utf-8")
r = r.replace(
'''                            if selection == index {
                                Capsule()
                                    .fill(SalahTheme.teal.opacity(0.10))
                                    .frame(width: 39, height: 24)
                            }
''',
'''                            if selection == index {
                                Circle()
                                    .fill(SalahTheme.teal.opacity(0.10))
                                    .frame(width: 29, height: 29)
                            }
''', 1)
r = r.replace(
'''                        Circle()
                            .fill(selection == index ? SalahTheme.gold : Color.clear)
                            .frame(width: 3.5, height: 3.5)
''',
'''                        Color.clear
                            .frame(height: 1)
''', 1)
r = r.replace('.font(.system(size: 17, weight: selection == index ? .bold : .semibold))',
              '.font(.system(size: 16, weight: selection == index ? .bold : .semibold))', 1)
r = r.replace('.padding(.top, 5)\n        .padding(.bottom, 2)',
              '.padding(.top, 4)\n        .padding(.bottom, 1)', 1)
r = r.replace('.shadow(color: SalahTheme.deepTeal.opacity(0.08), radius: 7, y: -2)',
              '.shadow(color: SalahTheme.deepTeal.opacity(0.035), radius: 2, y: -1)', 1)
p.write_text(r, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.28"', 'MARKETING_VERSION="3.29"')
t = t.replace('CURRENT_PROJECT_VERSION="33"', 'CURRENT_PROJECT_VERSION="34"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.29 exact QA-state + Home geometry pass applied")
