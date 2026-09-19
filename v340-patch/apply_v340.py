from pathlib import Path
import base64, io, json, tarfile

# SalahPath v3.40 — exact dashboard icon pass from the supplied reference.
payload = base64.b64decode(Path("v340-patch/reference_dashboard_icons.tgz.b64").read_text(encoding="utf-8").strip())
assets_root = Path("SalahZeit/Assets.xcassets")

with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tf:
    for name in ["quran", "dhikr", "prayer", "wudu", "times", "qibla", "info", "fav"]:
        data = tf.extractfile(f"{name}.png").read()
        folder = assets_root / f"ref_dash_{name}.imageset"
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"ref_dash_{name}.png"
        (folder / filename).write_bytes(data)
        (folder / "Contents.json").write_text(json.dumps({
            "images": [{"filename": filename, "idiom": "universal", "scale": "1x"}],
            "info": {"author": "xcode", "version": 1}
        }, indent=2), encoding="utf-8")

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

old = '''            ReferenceDashboardGlyph(kind: icon)
                .frame(width: 29, height: 29)
'''
new = '''            Image("ref_dash_\(icon)")
                .resizable()
                .scaledToFit()
                .frame(width: 30, height: 30)
                .accessibilityHidden(true)
'''
if old in s:
    s = s.replace(old, new, 1)
else:
    old2 = '''            ReferenceDashboardGlyph(kind: icon)
                .frame(width: 31, height: 31)
'''
    if old2 in s:
        s = s.replace(old2, new, 1)
    else:
        raise SystemExit("Dashboard glyph renderer target not found")

# The reference dashboard uses very small spacing and subtle borders.
start = s.index("private struct DashboardTile: View {")
end = s.index("\nprivate struct ReferenceDashboardGlyph", start)
tile = s[start:end]
tile = tile.replace("VStack(spacing: 4)", "VStack(spacing: 3)", 1)
tile = tile.replace(".padding(.horizontal, 3)", ".padding(.horizontal, 2)", 1)
tile = tile.replace(".padding(.vertical, 4)", ".padding(.vertical, 3)", 1)
tile = tile.replace(".frame(maxWidth: .infinity, minHeight: 82, alignment: .center)",
                    ".frame(maxWidth: .infinity, minHeight: 81, alignment: .center)", 1)
tile = tile.replace(".stroke(SalahTheme.gold.opacity(0.44), lineWidth: 0.7)",
                    ".stroke(SalahTheme.gold.opacity(0.40), lineWidth: 0.65)", 1)
s = s[:start] + tile + s[end:]

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.39"' in t:
    t = t.replace('MARKETING_VERSION="3.39"', 'MARKETING_VERSION="3.40"', 1)
if 'CURRENT_PROJECT_VERSION="44"' in t:
    t = t.replace('CURRENT_PROJECT_VERSION="44"', 'CURRENT_PROJECT_VERSION="45"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.40 exact reference dashboard icons applied")
