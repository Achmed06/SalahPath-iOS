from pathlib import Path

# SalahPath v3.36 — remove broken raster mosque dependency, strengthen reference typography,
# refine dashboard glyph treatment and bottom navigation.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# Hero: render the in-repo custom mosque skyline directly so it cannot disappear
# because of a corrupt or malformed raster asset.
old = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 188, height: 116)
                .opacity(1.0)
                .offset(x: 8, y: -4)
                .accessibilityHidden(true)
'''
new = '''            ReferenceMosqueSkyline()
                .frame(width: 196, height: 122)
                .opacity(0.96)
                .offset(x: 9, y: -2)
                .accessibilityHidden(true)
'''
if old not in s:
    raise SystemExit("home_mosque renderer not found")
s = s.replace(old, new, 1)

# Brand/title typography closer to the poster.
s = s.replace(
'''Text("SalahPath")
                    .font(.system(size: 18.5, weight: .bold, design: .serif))''',
'''Text("SalahPath")
                    .font(.custom("Georgia-Bold", size: 18.8))''', 1)

s = s.replace(
'''Text("İbadetle Daha Güzel Bir Hayat")
                    .font(.system(size: 7.2, weight: .semibold))''',
'''Text("İbadetle Daha Güzel Bir Hayat")
                    .font(.custom("AvenirNext-DemiBold", size: 7.0))''', 1)

s = s.replace(
'''Text("„Şüphesiz namaz, müminlere vakitleri belli bir farzdır.“")
                    .font(.system(size: 6.8, weight: .medium, design: .serif))''',
'''Text("„Şüphesiz namaz, müminlere vakitleri belli bir farzdır.“")
                    .font(.custom("Georgia-Italic", size: 6.7))''', 1)

# Main Hero typographic hierarchy.
s = s.replace(
'''Text("Sıradaki Namaz / Nächstes Gebet")
                        .font(.system(size: 11.6, weight: .bold))''',
'''Text("Sıradaki Namaz / Nächstes Gebet")
                        .font(.custom("AvenirNext-Bold", size: 11.1))''', 1)

s = s.replace(
'''Text(isScreenshotQA ? "İkindi" : prayer.kind.localizedName(settings.language))
                            .font(.system(size: 19, weight: .bold, design: .rounded))''',
'''Text(isScreenshotQA ? "İkindi" : prayer.kind.localizedName(settings.language))
                            .font(.custom("AvenirNext-Bold", size: 19.0))''', 1)

s = s.replace(
'''Text(isScreenshotQA ? "2:38:15" : countdownString(from: effectiveNow, to: prayer.date))
                            .font(.system(size: 27, weight: .bold, design: .rounded).monospacedDigit())''',
'''Text(isScreenshotQA ? "2:38:15" : countdownString(from: effectiveNow, to: prayer.date))
                            .font(.system(size: 27.0, weight: .bold, design: .rounded).monospacedDigit())''', 1)

# Daily dua title gets the same compact Avenir family.
s = s.replace(
'''Text("Günün Duası / Dua des Tages")
                    .font(.system(size: 10.8, weight: .bold))''',
'''Text("Günün Duası / Dua des Tages")
                    .font(.custom("AvenirNext-Bold", size: 10.2))''', 1)

# Tracking title.
s = s.replace(
'''Text("Namaz Takibi / Gebets-Tracking")
                        .font(.system(size: 9.5, weight: .bold))''',
'''Text("Namaz Takibi / Gebets-Tracking")
                        .font(.custom("AvenirNext-Bold", size: 9.2))''', 1)

# Dashboard tile type treatment: smaller, less system-heavy, closer to the poster.
start = s.index("private struct DashboardTile: View {")
end = s.index("\nprivate struct ReferenceDashboardGlyph", start)
chunk = s[start:end]
chunk = chunk.replace(
'''.font(.system(size: 8.1, weight: .bold))''',
'''.font(.custom("AvenirNext-Bold", size: 7.9))''')
chunk = chunk.replace(
'''.font(.system(size: 6.2, weight: .semibold))''',
'''.font(.custom("AvenirNext-DemiBold", size: 6.0))''')
chunk = chunk.replace('.frame(width: 32, height: 32)', '.frame(width: 31, height: 31)')
chunk = chunk.replace('.frame(maxWidth: .infinity, minHeight: 89, alignment: .center)',
                      '.frame(maxWidth: .infinity, minHeight: 87, alignment: .center)')
s = s[:start] + chunk + s[end:]

# Improve skyline visual treatment: stronger teal silhouette, softer haze, less blocky city baseline.
sky_start = s.index("private struct ReferenceMosqueSkyline: View {")
sky_end = s.index("\nprivate struct DashboardTile: View {", sky_start)
sky = s[sky_start:sky_end]
sky = sky.replace('SalahTheme.softTeal.opacity(0.22)', 'SalahTheme.softTeal.opacity(0.13)')
sky = sky.replace('SalahTheme.gold.opacity(0.06)', 'SalahTheme.gold.opacity(0.10)')
sky = sky.replace('fill(shaft, opacity: 0.94)', 'fill(shaft, opacity: 0.98)')
sky = sky.replace('fill(cap, opacity: 0.96)', 'fill(cap, opacity: 0.99)')
sky = sky.replace('fill(body, opacity: 0.92)', 'fill(body, opacity: 0.95)')
sky = sky.replace('fill(roof, opacity: 0.94)', 'fill(roof, opacity: 0.98)')
sky = sky.replace('fill(city, opacity: 0.54)', 'fill(city, opacity: 0.28)')
sky = sky.replace('.init(color: .white, location: 0.12)', '.init(color: .white, location: 0.06)')
sky = sky.replace('.init(color: .white, location: 0.82)', '.init(color: .white, location: 0.92)')
s = s[:sky_start] + sky + s[sky_end:]

# Quote ribbon uses Georgia like the reference poster.
s = s.replace(
'''.font(.system(size: 9.3, weight: .semibold, design: .serif))''',
'''.font(.custom("Georgia-Italic", size: 9.1))''', 1)

p.write_text(s, encoding="utf-8")

# Bottom navigation typography/icon weight.
root = Path("SalahZeit/Views/RootTabView.swift")
r = root.read_text(encoding="utf-8")
r = r.replace(
'''.font(.system(size: 16, weight: selection == index ? .bold : .semibold))''',
'''.font(.system(size: 15, weight: selection == index ? .bold : .medium))''', 1)
r = r.replace(
'''.font(.system(size: 7.7, weight: selection == index ? .bold : .semibold))''',
'''.font(.custom(selection == index ? "AvenirNext-Bold" : "AvenirNext-Medium", size: 7.2))''', 1)
r = r.replace('.frame(width: 29, height: 29)', '.frame(width: 27, height: 27)', 1)
r = r.replace('.frame(height: 22)', '.frame(height: 20)', 1)
r = r.replace('.padding(.top, 4)', '.padding(.top, 3)', 1)
root.write_text(r, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.35"', 'MARKETING_VERSION="3.36"')
t = t.replace('CURRENT_PROJECT_VERSION="40"', 'CURRENT_PROJECT_VERSION="41"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.36 vector mosque + typography refinement applied")
