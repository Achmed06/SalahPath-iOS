from pathlib import Path
import shutil

# SalahPath v3.38 — use the refined reference mosque artwork extracted from the supplied visual reference.
asset_source = Path("v338-patch/home_mosque_ref.png")
asset_target = Path("SalahZeit/Assets.xcassets/home_mosque.imageset/home_mosque.png")
asset_target.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(asset_source, asset_target)

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

old = '''            ReferenceMosqueSkyline()
                .frame(width: 171, height: 104)
                .opacity(0.90)
                .offset(x: 7, y: -48)
                .accessibilityHidden(true)
'''
new = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 171, height: 104)
                .opacity(0.98)
                .offset(x: 8, y: -43)
                .accessibilityHidden(true)
'''
if old in s:
    s = s.replace(old, new, 1)

# Make the hero information hierarchy match the supplied reference more closely.
if '.font(.custom("AvenirNext-Bold", size: 19.0))' in s:
    s = s.replace('.font(.custom("AvenirNext-Bold", size: 19.0))',
                  '.font(.custom("AvenirNext-DemiBold", size: 18.4))', 1)

if '.font(.system(size: 27.0, weight: .bold, design: .rounded).monospacedDigit())' in s:
    s = s.replace('.font(.system(size: 27.0, weight: .bold, design: .rounded).monospacedDigit())',
                  '.font(.system(size: 26.0, weight: .bold, design: .rounded).monospacedDigit())', 1)

# Smaller, softer supporting text like the poster.
if '.font(.system(size: 9.8, weight: .bold))' in s:
    s = s.replace('.font(.system(size: 9.8, weight: .bold))',
                  '.font(.custom("AvenirNext-DemiBold", size: 9.2))', 1)

# Refine dashboard card borders and radii.
start = s.index("private struct DashboardTile: View {")
end = s.index("\nprivate struct ReferenceDashboardGlyph", start)
tile = s[start:end]
tile = tile.replace('RoundedRectangle(cornerRadius: 9, style: .continuous)',
                    'RoundedRectangle(cornerRadius: 8, style: .continuous)')
tile = tile.replace('.stroke(SalahTheme.gold.opacity(0.56), lineWidth: 0.8)',
                    '.stroke(SalahTheme.gold.opacity(0.44), lineWidth: 0.7)')
s = s[:start] + tile + s[end:]

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.37"' in t:
    t = t.replace('MARKETING_VERSION="3.37"', 'MARKETING_VERSION="3.38"', 1)
if 'CURRENT_PROJECT_VERSION="42"' in t:
    t = t.replace('CURRENT_PROJECT_VERSION="42"', 'CURRENT_PROJECT_VERSION="43"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.38 refined reference mosque asset pass applied")
