from pathlib import Path
import base64

# SalahPath v3.44 — restore a reliable, softly integrated Home mosque silhouette.
# v3.38 reintroduced a truncated raster PNG. Xcode compiled it but the artwork
# disappeared at runtime. Use the in-source vector skyline and neutralize the
# broken raster payload so the asset catalog remains valid.

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

old = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 171, height: 104)
                .opacity(0.98)
                .offset(x: 8, y: -43)
                .accessibilityHidden(true)
'''
new = '''            ReferenceMosqueSkyline()
                .frame(width: 181, height: 113)
                .opacity(0.62)
                .offset(x: 10, y: -33)
                .accessibilityHidden(true)
'''
if old not in s:
    raise SystemExit("v3.44: current Home mosque renderer not found")
s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")

# v3.40's Quran dashboard PNG is also truncated. Keep all other validated
# reference icon PNGs, but fall back to the existing vector Quran glyph.
old_icon = '''            Image("ref_dash_\\(icon)")
                .resizable()
                .scaledToFit()
                .frame(width: 30, height: 30)
                .accessibilityHidden(true)
'''
new_icon = '''            Group {
                if icon == "quran" {
                    ReferenceDashboardGlyph(kind: icon)
                } else {
                    Image("ref_dash_\\(icon)")
                        .resizable()
                        .scaledToFit()
                }
            }
            .frame(width: 30, height: 30)
            .accessibilityHidden(true)
'''
if old_icon not in s:
    raise SystemExit("v3.44: DashboardTile image renderer not found")
s = s.replace(old_icon, new_icon, 1)
p.write_text(s, encoding="utf-8")

# Keep the legacy imageset structurally valid even though Home no longer renders it.
# This is a valid 1x1 transparent PNG.
transparent_png = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)
asset = Path("SalahZeit/Assets.xcassets/home_mosque.imageset/home_mosque.png")
asset.write_bytes(transparent_png)

quran_asset = Path("SalahZeit/Assets.xcassets/ref_dash_quran.imageset/ref_dash_quran.png")
quran_asset.write_bytes(transparent_png)

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.43"' not in t or 'CURRENT_PROJECT_VERSION="48"' not in t:
    raise SystemExit("v3.44: expected v3.43/48 build version not found")
t = t.replace('MARKETING_VERSION="3.43"', 'MARKETING_VERSION="3.44"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="48"', 'CURRENT_PROJECT_VERSION="49"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.44 reliable vector mosque restoration applied")
