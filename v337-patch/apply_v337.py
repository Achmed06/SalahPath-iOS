from pathlib import Path

# SalahPath v3.37 — robust screenshot-driven Home polish.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

replacements = [
(
'''            ReferenceMosqueSkyline()
                .frame(width: 196, height: 122)
                .opacity(0.96)
                .offset(x: 9, y: -2)
                .accessibilityHidden(true)
''',
'''            ReferenceMosqueSkyline()
                .frame(width: 171, height: 104)
                .opacity(0.90)
                .offset(x: 7, y: -48)
                .accessibilityHidden(true)
'''
),
('.frame(minHeight: 200)', '.frame(minHeight: 184)'),
('.font(.custom("AvenirNext-Bold", size: 11.1))', '.font(.custom("AvenirNext-DemiBold", size: 10.7))'),
('.font(.system(size: 8.4, weight: .bold))', '.font(.custom("AvenirNext-DemiBold", size: 7.8))'),
('.font(.system(size: 7.4, weight: .semibold))', '.font(.custom("AvenirNext-Medium", size: 7.0))'),
('.font(.custom("AvenirNext-Bold", size: 10.2))', '.font(.custom("AvenirNext-DemiBold", size: 9.7))'),
('.font(.system(size: 19.5, weight: .medium))', '.font(.system(size: 18.2, weight: .regular))'),
('.frame(minHeight: 112)', '.frame(minHeight: 103)'),
('.frame(width: 0.7, height: 72)', '.frame(width: 0.7, height: 63)'),
('.frame(width: 31, height: 31)', '.frame(width: 29, height: 29)'),
('.font(.custom("AvenirNext-Bold", size: 7.9))', '.font(.custom("AvenirNext-DemiBold", size: 7.5))'),
('.font(.custom("AvenirNext-DemiBold", size: 6.0))', '.font(.custom("AvenirNext-Medium", size: 5.8))'),
('.frame(maxWidth: .infinity, minHeight: 87, alignment: .center)', '.frame(maxWidth: .infinity, minHeight: 82, alignment: .center)'),
('.frame(minHeight: 52)', '.frame(minHeight: 44)'),
('.font(.custom("Georgia-Italic", size: 9.1))', '.font(.custom("Georgia-Italic", size: 8.4))'),
('.font(.system(size: 7.6, weight: .medium))', '.font(.custom("AvenirNext-Medium", size: 6.9))')
]

for old, new in replacements:
    if old in s:
        s = s.replace(old, new, 1)

# Only reduce the first hero vertical padding occurrence if still present.
hero_pad = '.padding(.vertical, 7)'
if hero_pad in s:
    s = s.replace(hero_pad, '.padding(.vertical, 6)', 1)

p.write_text(s, encoding="utf-8")

root = Path("SalahZeit/Views/RootTabView.swift")
r = root.read_text(encoding="utf-8")
root_replacements = [
('.frame(width: 27, height: 27)', '.frame(width: 24, height: 24)'),
('.font(.system(size: 15, weight: selection == index ? .bold : .medium))', '.font(.system(size: 13.5, weight: selection == index ? .semibold : .regular))'),
('.font(.custom(selection == index ? "AvenirNext-Bold" : "AvenirNext-Medium", size: 7.2))', '.font(.custom(selection == index ? "AvenirNext-DemiBold" : "AvenirNext-Medium", size: 6.6))'),
('.frame(height: 20)', '.frame(height: 18)'),
('.padding(.top, 3)', '.padding(.top, 2)'),
('.padding(.bottom, 1)', '.padding(.bottom, 0)')
]
for old, new in root_replacements:
    if old in r:
        r = r.replace(old, new, 1)
root.write_text(r, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.36"' in t:
    t = t.replace('MARKETING_VERSION="3.36"', 'MARKETING_VERSION="3.37"', 1)
if 'CURRENT_PROJECT_VERSION="41"' in t:
    t = t.replace('CURRENT_PROJECT_VERSION="41"', 'CURRENT_PROJECT_VERSION="42"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.37 robust Home polish applied")
