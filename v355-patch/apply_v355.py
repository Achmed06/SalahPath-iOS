from pathlib import Path

# SalahPath v3.55 — Home hero blend + dashboard icon parity.
# Keep the verified v3.54 reference mosque asset, soften its leading edge into
# the cream card, lower/reduce it slightly, and normalize all eight dashboard
# icons through the in-source reference glyphs so their visual weight matches.

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

old_mosque = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 195, height: 130)
                .opacity(0.98)
                .offset(x: 4, y: -26)
                .accessibilityHidden(true)
'''
new_mosque = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 184, height: 116)
                .opacity(0.98)
                .mask {
                    LinearGradient(
                        stops: [
                            .init(color: .clear, location: 0.00),
                            .init(color: .white.opacity(0.45), location: 0.08),
                            .init(color: .white, location: 0.20),
                            .init(color: .white, location: 1.00)
                        ],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                }
                .offset(x: 7, y: -15)
                .accessibilityHidden(true)
'''
if old_mosque not in s:
    raise SystemExit("v3.55: v3.54 mosque renderer not found")
s = s.replace(old_mosque, new_mosque, 1)

old_icon = '''            Group {
                if icon == "quran" {
                    ReferenceDashboardGlyph(kind: icon)
                } else {
                    Image("ref_dash_\(icon)")
                        .resizable()
                        .scaledToFit()
                }
            }
            .frame(width: 30, height: 30)
            .accessibilityHidden(true)
'''
new_icon = '''            ReferenceDashboardGlyph(kind: icon)
                .frame(width: 31, height: 31)
                .accessibilityHidden(true)
'''
if old_icon not in s:
    raise SystemExit("v3.55: dashboard icon renderer not found")
s = s.replace(old_icon, new_icon, 1)

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.54"' not in t or 'CURRENT_PROJECT_VERSION="59"' not in t:
    raise SystemExit("v3.55: expected v3.54/59 build version not found")
t = t.replace('MARKETING_VERSION="3.54"', 'MARKETING_VERSION="3.55"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="59"', 'CURRENT_PROJECT_VERSION="60"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.55 Home hero blend + dashboard icon parity applied")
