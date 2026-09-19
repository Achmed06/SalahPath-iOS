from pathlib import Path

# SalahPath v3.45 — center-phone reference geometry pass.
# Keeps the verified v3.44 asset repairs and brings the Home composition back to
# the vertical proportions visible in the supplied five-iPhone reference.

p = Path('SalahZeit/Views/HomeView.swift')
s = p.read_text(encoding='utf-8')

old_mosque = '''            LinearGradient(
                colors: [
                    Color.clear,
                    SalahTheme.gold.opacity(0.08),
                    Color(red: 0.98, green: 0.85, blue: 0.69).opacity(0.18)
                ],
                startPoint: .leading,
                endPoint: .trailing
            )
            .frame(width: 205, height: 116)
            .offset(x: 9, y: -40)
            .allowsHitTesting(false)

            ReferenceMosqueSkyline()
                .frame(width: 181, height: 113)
                .opacity(0.62)
                .offset(x: 10, y: -33)
                .accessibilityHidden(true)
'''
new_mosque = '''            LinearGradient(
                colors: [
                    Color.clear,
                    SalahTheme.gold.opacity(0.06),
                    Color(red: 0.98, green: 0.85, blue: 0.69).opacity(0.13)
                ],
                startPoint: .leading,
                endPoint: .trailing
            )
            .frame(width: 218, height: 126)
            .offset(x: 10, y: -34)
            .allowsHitTesting(false)

            ReferenceMosqueSkyline()
                .frame(width: 198, height: 124)
                .opacity(0.82)
                .offset(x: 10, y: -27)
                .accessibilityHidden(true)
'''
if old_mosque not in s:
    raise SystemExit('v3.45: current Home mosque block not found')
s = s.replace(old_mosque, new_mosque, 1)

# The v3.37 compaction left a large petrol gap above the tab bar on the current
# simulator. The reference phone fills this space with the actual UI cards.
replacements = [
    ('.frame(minHeight: 184)', '.frame(minHeight: 200)', 1),
    ('.frame(minHeight: 108)', '.frame(minHeight: 112)', 1),
    ('.frame(width: 0.7, height: 63)', '.frame(width: 0.7, height: 72)', 1),
    ('streakSummary(streakValue)\n                .frame(width: 82)', 'streakSummary(streakValue)\n                .frame(width: 98)', 1),
    ('.frame(minHeight: 103)', '.frame(minHeight: 112)', 1),
    ('.frame(maxWidth: .infinity, minHeight: 81, alignment: .center)', '.frame(maxWidth: .infinity, minHeight: 87, alignment: .center)', 1),
    ('.font(.custom("Georgia-Italic", size: 8.4))', '.font(.custom("Georgia-Italic", size: 9.1))', 1),
    ('.font(.custom("AvenirNext-Medium", size: 6.9))', '.font(.custom("AvenirNext-Medium", size: 7.6))', 1),
    ('.frame(minHeight: 44)', '.frame(minHeight: 52)', 1),
]
for old, new, count in replacements:
    if old not in s:
        raise SystemExit(f'v3.45: expected Home geometry token missing: {old}')
    s = s.replace(old, new, count)

p.write_text(s, encoding='utf-8')

root = Path('SalahZeit/Views/RootTabView.swift')
r = root.read_text(encoding='utf-8')
nav_replacements = [
    ('.font(.system(size: selection == index ? 14.2 : 13.2, weight: selection == index ? .semibold : .regular))',
     '.font(.system(size: selection == index ? 15.2 : 14.0, weight: selection == index ? .semibold : .regular))'),
    ('.frame(height: 18)', '.frame(height: 20)'),
    ('.font(.custom(selection == index ? "AvenirNext-DemiBold" : "AvenirNext-Medium", size: 6.6))',
     '.font(.custom(selection == index ? "AvenirNext-DemiBold" : "AvenirNext-Medium", size: 7.1))'),
    ('.padding(.top, 2)', '.padding(.top, 3)'),
    ('.padding(.bottom, 0)', '.padding(.bottom, 1)'),
]
for old, new in nav_replacements:
    if old not in r:
        raise SystemExit(f'v3.45: expected bottom-nav token missing: {old}')
    r = r.replace(old, new, 1)
root.write_text(r, encoding='utf-8')

b = Path('scripts/build_unsigned_ipa.sh')
t = b.read_text(encoding='utf-8')
if 'MARKETING_VERSION="3.44"' not in t or 'CURRENT_PROJECT_VERSION="49"' not in t:
    raise SystemExit('v3.45: expected v3.44/49 build version not found')
t = t.replace('MARKETING_VERSION="3.44"', 'MARKETING_VERSION="3.45"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="49"', 'CURRENT_PROJECT_VERSION="50"', 1)
b.write_text(t, encoding='utf-8')

print('SalahPath v3.45 center-phone reference geometry applied')
