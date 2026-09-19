from pathlib import Path

# SalahPath v3.31 — normalized vertical geometry pass from v3.30 screenshot.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# The reference phone uses ~11.5% of the viewport before the prayer card.
# v3.30 used ~16%. Pull the content upward while keeping it scroll-safe.
s = s.replace(
'''            .padding(.horizontal, 7)
            .padding(.top, 3)
            .padding(.bottom, 4)
''',
'''            .padding(.horizontal, 7)
            .padding(.top, -37)
            .padding(.bottom, 4)
''', 1)

# Keep branding compact when it moves closer to the status area.
s = s.replace('.frame(width: 34, height: 41)', '.frame(width: 31, height: 37)', 1)
s = s.replace('.font(.system(size: 19.5, weight: .bold, design: .serif))',
              '.font(.system(size: 18.5, weight: .bold, design: .serif))', 1)
s = s.replace('.font(.system(size: 7.8, weight: .semibold))',
              '.font(.system(size: 7.2, weight: .semibold))', 1)
s = s.replace('.frame(maxWidth: .infinity, minHeight: 50)',
              '.frame(maxWidth: .infinity, minHeight: 44)', 1)

# Reference hero is ~24% of the visible screen; v3.30 was ~17%.
s = s.replace('.frame(minHeight: 190)', '.frame(minHeight: 246)', 1)

# Mosque should dissolve into the cream card instead of reading as a rectangular photo.
old_mosque = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 190, height: 116)
                .opacity(0.98)
                .offset(x: 5, y: -4)
                .accessibilityHidden(true)
'''
new_mosque = '''            Image("home_mosque")
                .resizable()
                .scaledToFill()
                .frame(width: 198, height: 128)
                .clipped()
                .blendMode(.multiply)
                .opacity(0.88)
                .offset(x: 7, y: -7)
                .mask(
                    LinearGradient(
                        stops: [
                            .init(color: .clear, location: 0.00),
                            .init(color: .white, location: 0.15),
                            .init(color: .white, location: 0.91),
                            .init(color: .clear, location: 1.00)
                        ],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .accessibilityHidden(true)
'''
if old_mosque not in s:
    raise SystemExit("mosque target not found")
s = s.replace(old_mosque, new_mosque, 1)

# Slightly taller dua, matching the reference normalized height.
s = s.replace('.frame(minHeight: 98)', '.frame(minHeight: 108)', 1)

# Grid was a little too tall after the v3.30 fill pass.
tile_start = s.index("private struct DashboardTile: View {")
tile_end = s.index("\nprivate struct PrayerRow", tile_start)
tile = s[tile_start:tile_end]
tile = tile.replace('.frame(maxWidth: .infinity, minHeight: 92, alignment: .center)',
                    '.frame(maxWidth: .infinity, minHeight: 89, alignment: .center)')
s = s[:tile_start] + tile + s[tile_end:]

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.30"', 'MARKETING_VERSION="3.31"')
t = t.replace('CURRENT_PROJECT_VERSION="35"', 'CURRENT_PROJECT_VERSION="36"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.31 normalized Home geometry pass applied")
