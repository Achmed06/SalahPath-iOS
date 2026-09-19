from pathlib import Path
import base64

# SalahPath v3.35 — refined mosque artwork + micro-typography parity.
payload = base64.b64decode(Path("v335-patch/home_mosque_refined.b64").read_text(encoding="utf-8").strip())
asset = Path("SalahZeit/Assets.xcassets/home_mosque.imageset/home_mosque.png")
asset.write_bytes(payload)

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

old_mosque = '''            Image("home_mosque")
                .resizable()
                .scaledToFill()
                .frame(width: 190, height: 121)
                .clipped()
                .blendMode(.multiply)
                .opacity(0.88)
                .offset(x: 5, y: -5)
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
new_mosque = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 188, height: 116)
                .opacity(1.0)
                .offset(x: 8, y: -4)
                .accessibilityHidden(true)
'''
if old_mosque not in s:
    raise SystemExit("mosque renderer target not found")
s = s.replace(old_mosque, new_mosque, 1)

# Arabic dua in the screenshot was still visibly larger than the reference.
s = s.replace('.font(.system(size: 22, weight: .medium))',
              '.font(.system(size: 19.5, weight: .medium))', 1)

# Tracking reference uses smaller week circles and a more compact streak block.
s = s.replace('.frame(width: 21, height: 21)', '.frame(width: 18, height: 18)')
s = s.replace('Circle().fill(SalahTheme.teal).frame(width: 21, height: 21)',
              'Circle().fill(SalahTheme.teal).frame(width: 18, height: 18)')
s = s.replace('.font(.system(size: 10.3, weight: .bold))',
              '.font(.system(size: 9.5, weight: .bold))', 1)
s = s.replace('.font(.system(size: 21, weight: .bold).monospacedDigit())',
              '.font(.system(size: 19, weight: .bold).monospacedDigit())', 1)
s = s.replace('.font(.system(size: 18))\n                        .foregroundStyle(SalahTheme.gold)',
              '.font(.system(size: 16))\n                        .foregroundStyle(SalahTheme.gold)', 1)

# Reference quote ribbon uses notably smaller copy than v3.34.
s = s.replace('.font(.system(size: 10.5, weight: .semibold, design: .serif))',
              '.font(.system(size: 9.3, weight: .semibold, design: .serif))', 1)
s = s.replace('.font(.system(size: 8.5, weight: .medium))',
              '.font(.system(size: 7.6, weight: .medium))', 1)

# Custom dashboard glyphs should dominate the tile more than the labels, like the reference.
s = s.replace('.frame(width: 34, height: 34)', '.frame(width: 32, height: 32)', 1)
s = s.replace('.font(.system(size: 8.8, weight: .bold))',
              '.font(.system(size: 8.1, weight: .bold))', 1)
s = s.replace('.font(.system(size: 6.8, weight: .semibold))',
              '.font(.system(size: 6.2, weight: .semibold))', 1)

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.34"', 'MARKETING_VERSION="3.35"')
t = t.replace('CURRENT_PROJECT_VERSION="39"', 'CURRENT_PROJECT_VERSION="40"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.35 refined mosque and typography parity applied")
