from pathlib import Path

# SalahPath v3.20: central Home screen parity pass against the supplied reference phone.

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# 1) Header: the reference phone uses one continuous dark-teal top area, not a floating rounded card.
start = s.index("    private var brandHeader: some View {")
end = s.index("\n    private func nextPrayerHero", start)
new_header = r'''    private var brandHeader: some View {
        HStack(spacing: 9) {
            ZStack {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.72), lineWidth: 1)
                    .frame(width: 37, height: 37)
                Image(systemName: "leaf.fill")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundStyle(SalahTheme.gold)
                    .rotationEffect(.degrees(-8))
            }

            VStack(alignment: .leading, spacing: 1) {
                Text("SalahPath")
                    .font(.system(size: 21, weight: .bold, design: .serif))
                    .foregroundStyle(.white)
                    .lineLimit(1)
                Text("İbadetle Daha Güzel Bir Hayat")
                    .font(.system(size: 8.8, weight: .semibold))
                    .foregroundStyle(.white.opacity(0.78))
                    .lineLimit(1)
            }

            Spacer(minLength: 5)

            VStack(alignment: .trailing, spacing: 2) {
                Text(settings.language == .german
                    ? "„Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.“"
                    : "„Şüphesiz namaz, müminlere vakitleri belirli bir farzdır.“")
                    .font(.system(size: 7.7, weight: .medium, design: .serif))
                    .italic()
                    .foregroundStyle(.white.opacity(0.90))
                    .multilineTextAlignment(.trailing)
                    .lineLimit(3)
                    .frame(maxWidth: 108, alignment: .trailing)

                HStack(spacing: 5) {
                    Text("(Nisâ, 103)")
                        .font(.system(size: 7.4, weight: .semibold))
                        .foregroundStyle(SalahTheme.gold)
                    Image(systemName: settings.notificationsEnabled ? "bell.fill" : "bell")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(.white)
                }
            }
        }
        .padding(.horizontal, 7)
        .padding(.vertical, 5)
        .frame(maxWidth: .infinity)
        .background(Color.clear)
        .accessibilityElement(children: .contain)
    }
'''
s = s[:start] + new_header + s[end:]

# 2) Hero: mosque skyline becomes a large soft background layer like the reference,
# rather than a small isolated illustration.
start = s.index("    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {")
end = s.index("\n    private var prayerLegendCard", start)
hero = r'''    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {
        ZStack(alignment: .bottomTrailing) {
            ReferenceMosqueSkyline()
                .frame(width: 210, height: 88)
                .opacity(0.17)
                .offset(x: 15, y: 4)

            VStack(alignment: .leading, spacing: 6) {
                HStack(alignment: .top) {
                    Text("Sıradaki Namaz / Nächstes Gebet")
                        .font(.system(size: 12.5, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)

                    Spacer()

                    VStack(alignment: .trailing, spacing: 0) {
                        Text(gregorianDateShort(now))
                            .font(.system(size: 9.4, weight: .bold))
                        Text(shortWeekday(now))
                            .font(.system(size: 8.3, weight: .semibold))
                            .foregroundStyle(SalahTheme.mutedInk)
                    }
                }

                HStack(alignment: .center, spacing: 9) {
                    Image(systemName: prayer.kind.systemImage)
                        .font(.system(size: 25, weight: .medium))
                        .symbolRenderingMode(.hierarchical)
                        .foregroundStyle(SalahTheme.gold)
                        .frame(width: 35)

                    VStack(alignment: .leading, spacing: 0) {
                        Text(prayer.kind.localizedName(settings.language))
                            .font(.system(size: 20, weight: .bold, design: .rounded))
                            .foregroundStyle(SalahTheme.ink)

                        Text(countdownString(from: now, to: prayer.date))
                            .font(.system(size: 27, weight: .bold, design: .rounded).monospacedDigit())
                            .foregroundStyle(Color(red: 0.03, green: 0.17, blue: 0.28))
                            .lineLimit(1)
                            .minimumScaleFactor(0.72)
                    }

                    Spacer()

                    VStack(alignment: .trailing, spacing: 2) {
                        Image(systemName: "building.columns.fill")
                            .font(.system(size: 25))
                            .foregroundStyle(SalahTheme.teal.opacity(0.64))
                        Text(timeString(prayer.date, use24Hour: settings.use24Hour))
                            .font(.system(size: 10.5, weight: .bold).monospacedDigit())
                            .foregroundStyle(SalahTheme.ink)
                    }
                }

                HStack(spacing: 5) {
                    Image(systemName: "location.fill")
                        .font(.system(size: 10, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
                        .font(.system(size: 10.4, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                        .lineLimit(1)
                    Spacer()
                }

                HStack(spacing: 3) {
                    let segments = referenceSequence(for: prayer.kind)
                    ForEach(Array(segments.enumerated()), id: \.offset) { index, segment in
                        HStack(spacing: 3) {
                            Text(segment.0)
                                .font(.system(size: 9.2, weight: .bold))
                            Text(segment.1)
                                .font(.system(size: 7.5, weight: .semibold))
                        }
                        .foregroundStyle(SalahTheme.ink)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 5)
                        .background(Color.white.opacity(0.62), in: Capsule())
                        .overlay { Capsule().stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }

                        if index < segments.count - 1 {
                            Image(systemName: "arrow.right")
                                .font(.system(size: 7, weight: .black))
                                .foregroundStyle(SalahTheme.gold)
                        }
                    }
                }

                Text(settings.language == .german
                    ? "„Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.“ (Nisâ, 103)"
                    : "„Namaz, müminlere vakitleri belirlenmiş bir farzdır.“ (Nisâ, 103)")
                    .font(.system(size: 8.6, weight: .medium, design: .serif))
                    .italic()
                    .foregroundStyle(SalahTheme.mutedInk)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
            }
            .padding(10)
        }
        .background(
            LinearGradient(
                colors: [SalahTheme.cream, Color(red: 1.00, green: 0.955, blue: 0.82)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            ),
            in: RoundedRectangle(cornerRadius: 16, style: .continuous)
        )
        .overlay {
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.70), lineWidth: 1)
        }
        .shadow(color: SalahTheme.deepTeal.opacity(0.055), radius: 6, y: 2)
        .clipped()
    }
'''
s = s[:start] + hero + s[end:]

# 3) Prayer tracking: the reference shows week circles + streak only.
# Remove the extra five individual prayer buttons and progress bar from this dashboard card.
old = r'''                HStack(spacing: 3) {
                    ForEach(PrayerTrackerStore.requiredKinds) { kind in
                        let done = PrayerTrackerStore.isCompleted(kind, on: now)
                        Button {
                            guard !paused else { return }
                            _ = PrayerTrackerStore.toggle(kind, on: now)
                            trackerRefresh += 1
                        } label: {
                            Image(systemName: done ? "checkmark.circle.fill" : "circle")
                                .font(.system(size: 14, weight: .semibold))
                                .foregroundStyle(done ? SalahTheme.teal : SalahTheme.mutedInk.opacity(0.62))
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.plain)
                        .disabled(paused)
                    }
                }

                ProgressView(value: Double(completed), total: Double(PrayerTrackerStore.requiredKinds.count))
                    .tint(SalahTheme.teal)
                    .scaleEffect(x: 1, y: 0.68, anchor: .center)
'''
if old not in s:
    raise SystemExit("Tracker extra controls block not found")
s = s.replace(old, '', 1)

# The week dots are the main visual: slightly larger, with day labels in the same rhythm as the mockup.
s = s.replace('.frame(width: 23, height: 23)', '.frame(width: 25, height: 25)', 1)
s = s.replace('Circle().fill(SalahTheme.teal).frame(width: 23, height: 23)',
              'Circle().fill(SalahTheme.teal).frame(width: 25, height: 25)', 1)
s = s.replace('.font(.system(size: 7.5, weight: .bold))', '.font(.system(size: 7.8, weight: .bold))', 1)

# 4) Exact streak copy hierarchy from the visual reference.
s = s.replace(
    'Text(settings.t("Tage in Folge", "Günlük Seri"))',
    'Text(settings.language == .german ? "Günlük Seri\nTage in Folge" : "Günlük Seri\nTage in Folge")',
    1
)

# 5) Make quick-action cards visually closer to the thin gold framed 4x2 reference grid.
tile_start = s.index("private struct DashboardTile")
tile_end = s.index("\nprivate struct PrayerRow", tile_start)
tile = s[tile_start:tile_end]
tile = tile.replace('.frame(maxWidth: .infinity, minHeight: 74, alignment: .center)',
                    '.frame(maxWidth: .infinity, minHeight: 70, alignment: .center)')
tile = tile.replace('.padding(.vertical, 7)', '.padding(.vertical, 6)')
tile = tile.replace('.font(.system(size: 21, weight: .semibold))', '.font(.system(size: 19, weight: .semibold))')
tile = tile.replace('.stroke(SalahTheme.gold.opacity(0.48), lineWidth: 1)',
                    '.stroke(SalahTheme.gold.opacity(0.56), lineWidth: 1)')
s = s[:tile_start] + tile + s[tile_end:]

# 6) Quote ribbon is thinner in the reference.
s = s.replace('.padding(.vertical, 9)\n        .background(\n            LinearGradient(',
              '.padding(.vertical, 7)\n        .background(\n            LinearGradient(', 1)

p.write_text(s, encoding="utf-8")

build = Path("scripts/build_unsigned_ipa.sh")
b = build.read_text(encoding="utf-8")
b = b.replace('MARKETING_VERSION="3.19"', 'MARKETING_VERSION="3.20"')
b = b.replace('CURRENT_PROJECT_VERSION="24"', 'CURRENT_PROJECT_VERSION="25"')
build.write_text(b, encoding="utf-8")

print("SalahPath v3.20 central Home parity pass applied")
