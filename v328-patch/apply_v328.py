from pathlib import Path
import base64, io, json, tarfile

# SalahPath v3.28 — screenshot-driven Home geometry + real extracted reference artwork.
# Applies on top of v3.27.

# Reconstruct the small, verified artwork payload from chunk files already in the repo.
encoded = "".join(
    (Path("v326-patch") / f"asset-{i:02d}.b64").read_text(encoding="utf-8").strip()
    for i in range(5)
)
payload = base64.b64decode(encoded)
with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tf:
    logo = tf.extractfile("salahpath_logo.png").read()
    mosque = tf.extractfile("home_mosque.png").read()

assets = Path("SalahZeit/Assets.xcassets")
for folder, filename, data in [
    ("salahpath_logo.imageset", "salahpath_logo.png", logo),
    ("home_mosque.imageset", "home_mosque.png", mosque),
]:
    target = assets / folder
    target.mkdir(parents=True, exist_ok=True)
    (target / filename).write_bytes(data)
    (target / "Contents.json").write_text(json.dumps({
        "images": [{"filename": filename, "idiom": "universal", "scale": "1x"}],
        "info": {"author": "xcode", "version": 1}
    }, indent=2), encoding="utf-8")

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# Reference screenshot is 14 March 2025 and visually targets the Asr/İkindi state.
s = s.replace(
'''        components.hour = 12
        components.minute = 43
''',
'''        components.hour = 14
        components.minute = 0
''', 1)

# Use the actual extracted visual-reference artwork rather than approximating it with SF Symbols/Canvas.
s = s.replace(
'''            ReferenceLeafMark()
                .frame(width: 37, height: 45)
                .accessibilityHidden(true)
''',
'''            Image("salahpath_logo")
                .resizable()
                .scaledToFit()
                .frame(width: 39, height: 48)
                .accessibilityHidden(true)
''', 1)

s = s.replace(
'''            ReferenceMosqueSkyline()
                .frame(width: 192, height: 112)
                .opacity(0.92)
                .offset(x: 9, y: -2)
''',
'''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 205, height: 126)
                .opacity(0.98)
                .offset(x: 10, y: -1)
                .accessibilityHidden(true)
''', 1)

# The real reference phone uses more of the available vertical height than v3.27.
hero_tail = '''        .shadow(color: SalahTheme.deepTeal.opacity(0.025), radius: 2, y: 1)
        .clipped()
    }

    private var prayerLegendCard'''
hero_repl = '''        .shadow(color: SalahTheme.deepTeal.opacity(0.025), radius: 2, y: 1)
        .frame(minHeight: 178)
        .clipped()
    }

    private var prayerLegendCard'''
if hero_tail not in s:
    raise SystemExit("next prayer geometry target not found")
s = s.replace(hero_tail, hero_repl, 1)

dua_tail = '''                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
    }

    private var streakCard'''
dua_repl = '''                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
        .frame(minHeight: 104)
    }

    private var streakCard'''
if dua_tail not in s:
    raise SystemExit("dua geometry target not found")
s = s.replace(dua_tail, dua_repl, 1)

track_tail = '''                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
    }

    private var dailyDeenCard'''
track_repl = '''                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 0.8)
        }
        .frame(minHeight: 100)
    }

    private var dailyDeenCard'''
if track_tail not in s:
    raise SystemExit("tracking geometry target not found")
s = s.replace(track_tail, track_repl, 1)

# Week circles in the QA screenshot must use the same fixed reference day.
s = s.replace(
'''        let today = calendar.startOfDay(for: now)
''',
'''        let today = calendar.startOfDay(for: effectiveNow)
''', 1)

# Turkish reference date format is "14 Mart 2025", not a numeric date.
old_date = '''    private func gregorianDateShort(_ date: Date) -> String {
        let f = DateFormatter(); f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR"); f.dateFormat = "dd.MM.yyyy"
        return f.string(from: date)
    }
'''
new_date = '''    private func gregorianDateShort(_ date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: settings.language == .german ? "de_DE" : "tr_TR")
        f.dateFormat = settings.language == .german ? "dd.MM.yyyy" : "d MMMM yyyy"
        return f.string(from: date)
    }
'''
if old_date not in s:
    raise SystemExit("date formatter target not found")
s = s.replace(old_date, new_date, 1)

# Quote strip in the source artwork is a flat cream paper cut-out, not a gradient.
old_quote_bg = '''        .background(
            LinearGradient(
                colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.82)],
                startPoint: .leading,
                endPoint: .trailing
            ),
            in: RoundedRectangle(cornerRadius: 9, style: .continuous)
        )
'''
new_quote_bg = '''        .background(
            SalahTheme.cream,
            in: RoundedRectangle(cornerRadius: 9, style: .continuous)
        )
        .frame(minHeight: 48)
'''
if old_quote_bg not in s:
    raise SystemExit("quote background target not found")
s = s.replace(old_quote_bg, new_quote_bg, 1)

# Dashboard occupies ~one quarter of the visible reference screen.
old_tile_height = '''        .frame(maxWidth: .infinity, minHeight: 61, alignment: .center)
'''
new_tile_height = '''        .frame(maxWidth: .infinity, minHeight: 82, alignment: .center)
'''
if old_tile_height not in s:
    raise SystemExit("dashboard tile height target not found")
s = s.replace(old_tile_height, new_tile_height, 1)

# Slightly stronger reference icon scale inside the taller tiles.
s = s.replace(
'''                .font(.system(size: 18, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(height: 22)
''',
'''                .font(.system(size: 21, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(height: 26)
''', 1)

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.27"', 'MARKETING_VERSION="3.28"')
t = t.replace('CURRENT_PROJECT_VERSION="32"', 'CURRENT_PROJECT_VERSION="33"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.28 real reference assets + Home geometry pass applied")
