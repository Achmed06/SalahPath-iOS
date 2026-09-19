from pathlib import Path
import json

# SalahPath v3.56 — transparent reference mosque blend.
# Use the alpha-cleaned mosque extracted from the supplied center-phone
# reference. This removes the visible rectangular sky crop while preserving
# the actual mosque silhouette/details from the reference.

asset_root = Path("SalahZeit/Assets.xcassets/home_mosque.imageset")
asset_root.mkdir(parents=True, exist_ok=True)

src = Path("v356-patch/reference_home_mosque_alpha.png")
if not src.exists():
    raise SystemExit("v3.56: transparent reference mosque asset missing")

payload = src.read_bytes()
if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
    raise SystemExit("v3.56: transparent mosque asset is not a PNG")

dst = asset_root / "home_mosque.png"
dst.write_bytes(payload)

contents = {
    "images": [
        {"filename": "home_mosque.png", "idiom": "universal", "scale": "1x"},
        {"idiom": "universal", "scale": "2x"},
        {"idiom": "universal", "scale": "3x"},
    ],
    "info": {"author": "xcode", "version": 1},
}
(asset_root / "Contents.json").write_text(
    json.dumps(contents, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

old = '''            Image("home_mosque")
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

new = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 188, height: 118)
                .opacity(0.98)
                .offset(x: 8, y: -15)
                .accessibilityHidden(true)
'''

if old not in s:
    raise SystemExit("v3.56: v3.55 Home mosque renderer not found")

s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.55"' not in t or 'CURRENT_PROJECT_VERSION="60"' not in t:
    raise SystemExit("v3.56: expected v3.55/60 build version not found")
t = t.replace('MARKETING_VERSION="3.55"', 'MARKETING_VERSION="3.56"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="60"', 'CURRENT_PROJECT_VERSION="61"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.56 transparent reference mosque applied")
