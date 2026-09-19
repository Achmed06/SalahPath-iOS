from pathlib import Path
import json

# SalahPath v3.54 — exact Home mosque artwork from the supplied center-phone
# reference. The binary PNG is stored as a real Git blob in v354-patch so no
# text/base64 transfer touches the image bytes.

root = Path("SalahZeit/Assets.xcassets/home_mosque.imageset")
root.mkdir(parents=True, exist_ok=True)

src = Path("v354-patch/reference_home_mosque.png")
if not src.exists():
    raise SystemExit("v3.54: reference mosque binary missing")

dst = root / "home_mosque.png"
dst.write_bytes(src.read_bytes())

contents = {
    "images": [
        {"filename": "home_mosque.png", "idiom": "universal", "scale": "1x"},
        {"idiom": "universal", "scale": "2x"},
        {"idiom": "universal", "scale": "3x"},
    ],
    "info": {"author": "xcode", "version": 1},
}
(root / "Contents.json").write_text(
    json.dumps(contents, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

old = '''            LinearGradient(
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

new = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 195, height: 130)
                .opacity(0.98)
                .offset(x: 4, y: -26)
                .accessibilityHidden(true)
'''

if old not in s:
    raise SystemExit("v3.54: current Home mosque renderer not found")

s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.53"' not in t or 'CURRENT_PROJECT_VERSION="58"' not in t:
    raise SystemExit("v3.54: expected v3.53/58 build version not found")
t = t.replace('MARKETING_VERSION="3.53"', 'MARKETING_VERSION="3.54"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="58"', 'CURRENT_PROJECT_VERSION="59"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.54 exact Home mosque artwork applied")
