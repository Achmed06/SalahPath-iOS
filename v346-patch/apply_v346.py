from pathlib import Path
import base64

# SalahPath v3.46 — use the actual mosque artwork extracted from the supplied
# center-phone reference and extend the custom bottom bar through the iPhone
# home-indicator safe area.

# --- Exact reference mosque asset ---
payload = base64.b64decode(
    Path("v346-patch/home_mosque_reference.b64").read_text(encoding="utf-8").strip()
)
asset = Path("SalahZeit/Assets.xcassets/home_mosque.imageset/home_mosque.png")
asset.parent.mkdir(parents=True, exist_ok=True)
asset.write_bytes(payload)

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

old = '''            ReferenceMosqueSkyline()
                .frame(width: 198, height: 124)
                .opacity(0.82)
                .offset(x: 10, y: -27)
                .accessibilityHidden(true)
'''
new = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 184, height: 100)
                .opacity(0.98)
                .offset(x: 6, y: -38)
                .accessibilityHidden(true)
'''
if old not in s:
    raise SystemExit("v3.46: v3.45 mosque renderer not found")
s = s.replace(old, new, 1)

# The extracted artwork already contains the reference's subtle warm atmosphere,
# so reduce the synthetic glow behind it.
s = s.replace(
'''                    SalahTheme.gold.opacity(0.06),
                    Color(red: 0.98, green: 0.85, blue: 0.69).opacity(0.13)
''',
'''                    SalahTheme.gold.opacity(0.035),
                    Color(red: 0.98, green: 0.85, blue: 0.69).opacity(0.08)
''',
1
)

p.write_text(s, encoding="utf-8")

# --- Bottom safe-area parity ---
root = Path("SalahZeit/Views/RootTabView.swift")
r = root.read_text(encoding="utf-8")

old_bg = '''        .background(
            SalahTheme.cream
                .overlay(alignment: .top) {
                    Rectangle()
                        .fill(SalahTheme.gold.opacity(0.42))
                        .frame(height: 0.7)
                }
        )
'''
new_bg = '''        .background {
            SalahTheme.cream
                .overlay(alignment: .top) {
                    Rectangle()
                        .fill(SalahTheme.gold.opacity(0.42))
                        .frame(height: 0.7)
                }
                .ignoresSafeArea(edges: .bottom)
        }
'''
if old_bg not in r:
    raise SystemExit("v3.46: bottom bar background block not found")
r = r.replace(old_bg, new_bg, 1)
root.write_text(r, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.45"' not in t or 'CURRENT_PROJECT_VERSION="50"' not in t:
    raise SystemExit("v3.46: expected v3.45/50 build version not found")
t = t.replace('MARKETING_VERSION="3.45"', 'MARKETING_VERSION="3.46"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="50"', 'CURRENT_PROJECT_VERSION="51"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.46 exact mosque + bottom safe-area parity applied")
