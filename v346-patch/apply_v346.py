from pathlib import Path

# SalahPath v3.46 — bottom safe-area parity.
# Keep the verified v3.45 Home artwork and extend the custom bottom bar through
# the iPhone home-indicator area like the supplied reference.

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

print("SalahPath v3.46 bottom safe-area parity applied")
