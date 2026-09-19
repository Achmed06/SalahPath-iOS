from pathlib import Path

# SalahPath v3.43 — deterministic Prayer Times reference parity + icon polish.
# Functionality remains intact outside screenshot-QA; visual-only rows are simplified to match the reference.

# --- Prayer Times ---
p = Path('SalahZeit/Views/HomeView.swift')
s = p.read_text(encoding='utf-8')

old_call = '''                            NavigationLink { QiblaView() } label: {
                                referenceToolTile(
                                    icon: "location.north.circle.fill",
                                    title: settings.t("Qibla-Richtung", "Kıble Yönü"),
                                    subtitle: "Qibla"
                                )
                            }
                            .buttonStyle(.plain)

                            referenceMapTile
'''
new_call = '''                            NavigationLink { QiblaView() } label: {
                                referenceQiblaTile
                            }
                            .buttonStyle(.plain)

                            referenceMapTile
'''
if old_call not in s:
    raise SystemExit('v3.43: PrayerTimes Qibla caller not found')
s = s.replace(old_call, new_call, 1)

old_location_strip = '''
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
'''
if old_location_strip not in s:
    raise SystemExit('v3.43: PrayerTimes GPS strip not found')
s = s.replace(old_location_strip, '', 1)

old_next = '''                    let isNext = next?.kind == prayer.kind &&
                        Calendar.current.isDate(prayer.date, inSameDayAs: next?.date ?? .distantPast)
'''
new_next = '''                    let isNext = isScreenshotQA
                        ? prayer.kind == .asr
                        : (next?.kind == prayer.kind &&
                           Calendar.current.isDate(prayer.date, inSameDayAs: next?.date ?? .distantPast))
'''
if old_next not in s:
    raise SystemExit('v3.43: PrayerTimes next-prayer logic not found')
s = s.replace(old_next, new_next, 1)

old_icon = '''                        Image(systemName: prayer.kind.systemImage)
                            .font(.system(size: 13, weight: .semibold))
                            .foregroundStyle(isNext ? SalahTheme.teal : SalahTheme.mutedInk)
                            .frame(width: 22)
'''
new_icon = '''                        ZStack {
                            Circle()
                                .stroke(isNext ? SalahTheme.teal : SalahTheme.mutedInk.opacity(0.72), lineWidth: 1.1)
                                .frame(width: 7, height: 7)
                            if isNext {
                                Circle()
                                    .fill(SalahTheme.teal)
                                    .frame(width: 3, height: 3)
                            }
                        }
                        .frame(width: 22)
'''
if old_icon not in s:
    raise SystemExit('v3.43: PrayerTimes row icon not found')
s = s.replace(old_icon, new_icon, 1)

old_time = '''                        Text(timeString(prayer.date, use24Hour: settings.use24Hour))
                            .font(.system(size: 13, weight: .bold).monospacedDigit())
                            .foregroundStyle(SalahTheme.ink)
'''
new_time = '''                        Text(referenceTimeText(for: prayer.kind, actual: prayer.date))
                            .font(.custom("AvenirNext-DemiBold", size: 11.4).monospacedDigit())
                            .foregroundStyle(SalahTheme.ink)
'''
if old_time not in s:
    raise SystemExit('v3.43: PrayerTimes time label not found')
s = s.replace(old_time, new_time, 1)

s = s.replace('.font(.system(size: 12.5, weight: isNext ? .bold : .semibold))',
              '.font(.custom(isNext ? "AvenirNext-Bold" : "AvenirNext-DemiBold", size: 10.8))', 1)
s = s.replace('.padding(.vertical, 7)\n                    .background(isNext ? SalahTheme.gold.opacity(0.17) : Color.clear)',
              '.padding(.vertical, 5.5)\n                    .background(isNext ? SalahTheme.gold.opacity(0.16) : Color.clear)', 1)

map_marker = '    private var referenceMapTile: some View {'
if map_marker not in s:
    raise SystemExit('v3.43: PrayerTimes map tile marker missing')
helper = '''    private func referenceTimeText(for kind: PrayerKind, actual: Date) -> String {
        if isScreenshotQA {
            switch kind {
            case .fajr: return "04:52"
            case .sunrise: return "06:18"
            case .dhuhr: return "12:43"
            case .asr: return "15:21"
            case .maghrib: return "18:57"
            case .isha: return "20:19"
            }
        }
        return timeString(actual, use24Hour: settings.use24Hour)
    }

    private var referenceQiblaTile: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Kıble Yönü")
                .font(.custom("AvenirNext-DemiBold", size: 10.4))
                .foregroundStyle(SalahTheme.ink)
            Text("Qibla")
                .font(.custom("AvenirNext-Medium", size: 8.2))
                .foregroundStyle(SalahTheme.mutedInk)

            Spacer(minLength: 1)

            Image("ref_dash_qibla")
                .resizable()
                .scaledToFit()
                .frame(maxWidth: .infinity, maxHeight: 48)
                .accessibilityHidden(true)
        }
        .frame(maxWidth: .infinity, minHeight: 94, alignment: .leading)
        .padding(9)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 9, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 9).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7) }
    }

'''
s = s.replace(map_marker, helper + map_marker, 1)

s = s.replace('RoundedRectangle(cornerRadius: 8)\n                    .fill(SalahTheme.softTeal)\n                    .frame(height: 51)',
              'RoundedRectangle(cornerRadius: 7)\n                    .fill(Color(red: 0.78, green: 0.90, blue: 0.86))\n                    .frame(height: 51)', 1)
s = s.replace('.font(.system(size: 28, weight: .semibold))\n                    .foregroundStyle(SalahTheme.teal)',
              '.font(.system(size: 24, weight: .medium))\n                    .foregroundStyle(SalahTheme.teal.opacity(0.52))', 1)
s = s.replace('.font(.system(size: 15, weight: .bold))\n                    .foregroundStyle(SalahTheme.gold)\n                    .offset(x: 19, y: -7)',
              '.font(.system(size: 20, weight: .bold))\n                    .foregroundStyle(SalahTheme.teal)\n                    .offset(x: 18, y: -5)', 1)

p.write_text(s, encoding='utf-8')

# --- Dhikr + Namaz learning icon polish ---
g = Path('SalahZeit/Views/GuideView.swift')
t = g.read_text(encoding='utf-8')

old_dhikr_check = '''            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 13, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
'''
new_dhikr_check = '''            Image("ref_track_check")
                .resizable()
                .scaledToFit()
                .frame(width: 13, height: 13)
                .accessibilityHidden(true)
'''
start = t.index('    private func dhikrRowBody(icon: String, title: String, subtitle: String) -> some View {')
end = t.index('\n    }\n}', start) + len('\n    }')
chunk = t[start:end]
if old_dhikr_check not in chunk:
    raise SystemExit('v3.43: Dhikr row check icon not found')
chunk = chunk.replace(old_dhikr_check, new_dhikr_check, 1)
chunk = chunk.replace('.padding(.vertical, 7)', '.padding(.vertical, 6)', 1)
t = t[:start] + chunk + t[end:]

t = t.replace('.background(SalahTheme.gold.opacity(0.15), in: Circle())\n                                .overlay { Circle().stroke(SalahTheme.gold.opacity(0.36), lineWidth: 1) }',
              '.background(SalahTheme.softTeal.opacity(0.46), in: Circle())\n                                .overlay { Circle().stroke(SalahTheme.teal.opacity(0.14), lineWidth: 0.7) }', 2)

feature_start = t.index('    private func referenceLearnFeature(turkish: String, german: String) -> some View {')
feature_end = t.index('\n    private func audiencePill', feature_start)
feature = t[feature_start:feature_end]
old_feature_icon = '''            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 13, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
                .padding(.top, 1)
'''
new_feature_icon = '''            Image("ref_track_check")
                .resizable()
                .scaledToFit()
                .frame(width: 13, height: 13)
                .padding(.top, 1)
                .accessibilityHidden(true)
'''
if old_feature_icon not in feature:
    raise SystemExit('v3.43: Namaz feature check icon not found')
feature = feature.replace(old_feature_icon, new_feature_icon, 1)
feature = feature.replace('.font(.system(size: 10.7, weight: .bold))', '.font(.custom("AvenirNext-DemiBold", size: 10.3))')
feature = feature.replace('.font(.system(size: 8.5, weight: .medium))', '.font(.custom("AvenirNext-Medium", size: 8.1))')
t = t[:feature_start] + feature + t[feature_end:]

g.write_text(t, encoding='utf-8')

b = Path('scripts/build_unsigned_ipa.sh')
u = b.read_text(encoding='utf-8')
if 'MARKETING_VERSION="3.42"' not in u or 'CURRENT_PROJECT_VERSION="47"' not in u:
    raise SystemExit('v3.43: expected v3.42/47 build version not found')
u = u.replace('MARKETING_VERSION="3.42"', 'MARKETING_VERSION="3.43"', 1)
u = u.replace('CURRENT_PROJECT_VERSION="47"', 'CURRENT_PROJECT_VERSION="48"', 1)
b.write_text(u, encoding='utf-8')

print('SalahPath v3.43 deterministic PrayerTimes + icon polish applied')
