from pathlib import Path

# SalahPath v3.51 — Dhikr reference-phone proportions.
# Match the supplied right-phone screenshot: larger dhikr hero, larger five-row
# list, no extra motivation ribbon inside the app viewport.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

d_start = s.index("struct DhikrView: View {")
d_end = s.index("\nprivate struct DhikrTextCard", d_start)
d = s[d_start:d_end]

replacements = [
    ('.font(.system(size: 9.5, weight: .bold))',
     '.font(.system(size: 11.4, weight: .bold))', 1),
    ('.padding(.vertical, 5)',
     '.padding(.vertical, 7)', 1),
    ('VStack(spacing: 10) {',
     'VStack(spacing: 14) {', 1),
    ('.font(.system(size: 30, weight: .regular))',
     '.font(.system(size: 37, weight: .regular))', 1),
    ('.font(.custom("AvenirNext-DemiBold", size: 13.2))',
     '.font(.custom("AvenirNext-DemiBold", size: 15.6))', 1),
    ('.font(.custom("AvenirNext-Medium", size: 9.8))',
     '.font(.custom("AvenirNext-Medium", size: 12.1))', 1),
    ('HStack(spacing: 18) {',
     'HStack(spacing: 24) {', 1),
    ('.font(.system(size: 14, weight: .bold))',
     '.font(.system(size: 17, weight: .bold))', 2),
    ('.frame(width: 30, height: 30)',
     '.frame(width: 42, height: 42)', 2),
    ('.font(.system(size: 32, weight: .bold, design: .rounded).monospacedDigit())',
     '.font(.system(size: 42, weight: .bold, design: .rounded).monospacedDigit())', 1),
    ('.frame(minWidth: 70)',
     '.frame(minWidth: 88)', 1),
    ('.padding(.horizontal, 13)',
     '.padding(.horizontal, 16)', 1),
    ('.padding(.vertical, 13)',
     '.padding(.vertical, 18)', 1),
]
for old, new, count in replacements:
    if d.count(old) < count:
        raise SystemExit(f"v3.51: Dhikr token missing: {old}")
    d = d.replace(old, new, count)

# Give the hero approximately the same width:height ratio as the poster phone.
hero_anchor = '''                .frame(maxWidth: .infinity)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
'''
hero_new = '''                .frame(maxWidth: .infinity)
                .aspectRatio(1.42, contentMode: .fit)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
'''
if hero_anchor not in d:
    raise SystemExit("v3.51: Dhikr hero frame anchor missing")
d = d.replace(hero_anchor, hero_new, 1)

# Scale the five reference rows so the list card carries the same visual weight.
row_replacements = [
    ('.font(.system(size: 13, weight: .semibold))',
     '.font(.system(size: 16, weight: .semibold))', 1),
    ('.font(.custom("AvenirNext-DemiBold", size: 10.6))',
     '.font(.custom("AvenirNext-DemiBold", size: 13.1))', 1),
    ('.font(.system(size: 8.5, weight: .bold))',
     '.font(.system(size: 10.8, weight: .bold))', 1),
    ('.padding(.horizontal, 10)',
     '.padding(.horizontal, 12)', 1),
    ('.padding(.vertical, 6)',
     '.padding(.vertical, 12)', 1),
]
for old, new, count in row_replacements:
    if d.count(old) < count:
        raise SystemExit(f"v3.51: Dhikr row token missing: {old}")
    d = d.replace(old, new, count)

list_anchor = '''                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 10).stroke(SalahTheme.gold.opacity(0.36), lineWidth: 0.7) }

                HStack(spacing: 7) {
'''
list_new = '''                .frame(minHeight: 235)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 10).stroke(SalahTheme.gold.opacity(0.36), lineWidth: 0.7) }

                HStack(spacing: 7) {
'''
if list_anchor not in d:
    raise SystemExit("v3.51: Dhikr list anchor missing")
d = d.replace(list_anchor, list_new, 1)

# Remove the extra motivation ribbon; it is outside the reference phone UI.
ribbon_start = d.index('                HStack(spacing: 7) {')
ribbon_end = d.index('\n            }\n            .padding(.horizontal, 11)', ribbon_start)
d = d[:ribbon_start] + d[ribbon_end:]

s = s[:d_start] + d + s[d_end:]
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.50"' not in t or 'CURRENT_PROJECT_VERSION="55"' not in t:
    raise SystemExit("v3.51: expected v3.50/55 build version not found")
t = t.replace('MARKETING_VERSION="3.50"', 'MARKETING_VERSION="3.51"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="55"', 'CURRENT_PROJECT_VERSION="56"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.51 Dhikr reference-phone proportions applied")
