from pathlib import Path

# SalahPath v3.30 — compile-safe tracking refactor for the v3.29 visual pass.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

start = s.index("    private var streakCard: some View {")
end = s.index("\n    private var dailyDeenCard", start)

replacement = r'''    private var streakCard: some View {
        let streakValue = isScreenshotQA ? 12 : PrayerTrackerStore.streak(upTo: effectiveNow)
        let weekDates = currentWeekDates()

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
                    ForEach(Array(weekDates.enumerated()), id: \.offset) { item in
                        trackingDay(index: item.offset, date: item.element)
                    }
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            Rectangle()
                .fill(SalahTheme.gold.opacity(0.28))
                .frame(width: 0.7, height: 72)

            streakSummary(streakValue)
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

    private func trackingDay(index: Int, date: Date) -> some View {
        let qaLabels = ["Pzt", "Sal", "Çar", "Prş", "Cum", "Cts", "Paz"]
        let done: Bool
        let paused: Bool

        if isScreenshotQA {
            done = index < 4
            paused = false
        } else {
            done = PrayerTrackerStore.completedCount(on: date) == PrayerTrackerStore.requiredKinds.count
            paused = PrayerTrackerStore.isPaused(date)
        }

        let label = isScreenshotQA ? qaLabels[index] : shortWeekdayLetter(date)

        return VStack(spacing: 2) {
            ZStack {
                Circle()
                    .stroke(done ? SalahTheme.teal : SalahTheme.teal.opacity(0.30), lineWidth: 1)
                    .frame(width: 21, height: 21)

                if done {
                    Circle()
                        .fill(SalahTheme.teal)
                        .frame(width: 21, height: 21)

                    Image(systemName: "checkmark")
                        .font(.system(size: 7.5, weight: .black))
                        .foregroundStyle(.white)
                } else if paused {
                    Image(systemName: "pause.fill")
                        .font(.system(size: 6.5, weight: .bold))
                        .foregroundStyle(SalahTheme.mutedInk)
                }
            }

            Text(label)
                .font(.system(size: 6.5, weight: .bold))
                .foregroundStyle(SalahTheme.mutedInk)
        }
        .frame(maxWidth: .infinity)
    }

    private func streakSummary(_ value: Int) -> some View {
        VStack(spacing: 0) {
            HStack(spacing: 4) {
                Image(systemName: "flame.fill")
                    .font(.system(size: 18))
                    .foregroundStyle(SalahTheme.gold)

                Text("\(value)")
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
    }
'''
s = s[:start] + replacement + s[end:]
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.29"', 'MARKETING_VERSION="3.30"')
t = t.replace('CURRENT_PROJECT_VERSION="34"', 'CURRENT_PROJECT_VERSION="35"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.30 compile-safe tracking refactor applied")
