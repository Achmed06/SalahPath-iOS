from pathlib import Path
import base64, io, json, tarfile

# SalahPath v3.41 — exact small icon/artwork pass from the supplied reference phone.
payload = base64.b64decode(Path("v341-patch/reference_special_icons.tgz.b64").read_text(encoding="utf-8").strip())
assets_root = Path("SalahZeit/Assets.xcassets")
names = [
    "logo", "sun", "dua_leaf", "speaker", "track_check", "flame",
    "quote_leaf", "tab_home", "tab_quran", "tab_prayer", "tab_discover", "tab_profile"
]

with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tf:
    for name in names:
        data = tf.extractfile(f"{name}.png").read()
        asset_name = f"ref_{name}"
        folder = assets_root / f"{asset_name}.imageset"
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"{asset_name}.png"
        (folder / filename).write_bytes(data)
        (folder / "Contents.json").write_text(json.dumps({
            "images": [{"filename": filename, "idiom": "universal", "scale": "1x"}],
            "info": {"author": "xcode", "version": 1}
        }, indent=2), encoding="utf-8")

home = Path("SalahZeit/Views/HomeView.swift")
s = home.read_text(encoding="utf-8")

# Header logo: use the exact mark extracted from the reference phone.
s = s.replace('Image("salahpath_logo")', 'Image("ref_logo")', 1)

# Hero sun: replace the approximated vector with the exact reference glyph.
s = s.replace(
'''                            ReferenceSunGlyph()
                                .frame(width: 29, height: 29)
''',
'''                            Image("ref_sun")
                                .resizable()
                                .scaledToFit()
                                .frame(width: 29, height: 29)
''', 1)
s = s.replace(
'''                            ReferenceSunGlyph()
                                .frame(width: 15, height: 15)
''',
'''                            Image("ref_sun")
                                .resizable()
                                .scaledToFit()
                                .frame(width: 15, height: 15)
''', 1)

# Daily dua card: exact leaf and speaker glyphs from the reference.
daily_start = s.index("    private var dailyDuaCard: some View {")
daily_end = s.index("\n    private var streakCard", daily_start)
daily = s[daily_start:daily_end]
daily = daily.replace(
'''                    ReferenceLeafMark(color: SalahTheme.teal)
                        .frame(width: 14, height: 18)
''',
'''                    Image("ref_dua_leaf")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 16, height: 20)
''', 1)
daily = daily.replace(
'''                    Image(systemName: "speaker.wave.2.fill")
                        .font(.system(size: 11.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                        .frame(width: 28, height: 28)
''',
'''                    Image("ref_speaker")
                        .renderingMode(.template)
                        .resizable()
                        .scaledToFit()
                        .foregroundStyle(SalahTheme.teal)
                        .frame(width: 15, height: 15)
                        .frame(width: 28, height: 28)
''', 1)
s = s[:daily_start] + daily + s[daily_end:]

# Tracking card: exact reference check badge and flame.
track_start = s.index("    private var streakCard: some View {")
track_end = s.index("\n    private var dailyDeenCard", track_start)
track = s[track_start:track_end]
old_check = '''                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: 20, height: 20)
                        Image(systemName: "checkmark")
                            .font(.system(size: 8, weight: .black))
                            .foregroundStyle(.white)
                    }
'''
new_check = '''                    Image("ref_track_check")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 21, height: 21)
'''
if old_check in track:
    track = track.replace(old_check, new_check, 1)
track = track.replace(
'''                ReferenceFlameGlyph()
                    .frame(width: 18, height: 22)
''',
'''                Image("ref_flame")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 19, height: 23)
''', 1)
s = s[:track_start] + track + s[track_end:]

# Quote ribbon: exact floral/leaf glyph from the reference.
quote_start = s.index("    private var referenceQuoteStrip: some View {")
quote_end = s.index("\n    private func referenceSequence", quote_start)
quote = s[quote_start:quote_end]
quote = quote.replace(
'''            ReferenceLeafMark(color: SalahTheme.teal)
                .frame(width: 18, height: 23)
''',
'''            Image("ref_quote_leaf")
                .resizable()
                .scaledToFit()
                .frame(width: 22, height: 25)
''', 1)
s = s[:quote_start] + quote + s[quote_end:]

home.write_text(s, encoding="utf-8")

# Bottom navigation: exact reference shapes, rendered as templates so active/inactive tint still works.
root = Path("SalahZeit/Views/RootTabView.swift")
r = root.read_text(encoding="utf-8")
old_tabs = '''        [
            ("house.fill", "Ana Sayfa"),
            ("book.fill", "Kur'an"),
            ("figure.mind.and.body", "Namaz"),
            ("location.north.circle", "Keşfet"),
            ("person.crop.circle", "Profil")
        ]
'''
new_tabs = '''        [
            ("ref_tab_home", "Ana Sayfa"),
            ("ref_tab_quran", "Kur'an"),
            ("ref_tab_prayer", "Namaz"),
            ("ref_tab_discover", "Keşfet"),
            ("ref_tab_profile", "Profil")
        ]
'''
if old_tabs in r:
    r = r.replace(old_tabs, new_tabs, 1)
else:
    # Fallback for earlier tab tuple spellings.
    r = r.replace('("house.fill", "Ana Sayfa")', '("ref_tab_home", "Ana Sayfa")')
    r = r.replace('("book.fill", "Kur\'an")', '("ref_tab_quran", "Kur\'an")')
    r = r.replace('("figure.mind.and.body", "Namaz")', '("ref_tab_prayer", "Namaz")')
    r = r.replace('("location.north.circle", "Keşfet")', '("ref_tab_discover", "Keşfet")')
    r = r.replace('("person.crop.circle", "Profil")', '("ref_tab_profile", "Profil")')

old_image = '''                        Image(systemName: item.0)
                            .font(.system(size: selection == index ? 14.2 : 13.2, weight: selection == index ? .semibold : .regular))
                            .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                            .frame(height: 18)
'''
new_image = '''                        Image(item.0)
                            .renderingMode(.template)
                            .resizable()
                            .scaledToFit()
                            .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                            .frame(width: 17, height: 17)
                            .frame(height: 18)
'''
if old_image in r:
    r = r.replace(old_image, new_image, 1)
else:
    # Older v3.36 style fallback.
    old2 = '''                            Image(systemName: item.0)
                                .font(.system(size: 13.5, weight: selection == index ? .semibold : .regular))
                                .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
'''
    if old2 in r:
        r = r.replace(old2, '''                            Image(item.0)
                                .renderingMode(.template)
                                .resizable()
                                .scaledToFit()
                                .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                                .frame(width: 17, height: 17)
''', 1)

root.write_text(r, encoding="utf-8")

build = Path("scripts/build_unsigned_ipa.sh")
t = build.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.40"' in t:
    t = t.replace('MARKETING_VERSION="3.40"', 'MARKETING_VERSION="3.41"', 1)
if 'CURRENT_PROJECT_VERSION="45"' in t:
    t = t.replace('CURRENT_PROJECT_VERSION="45"', 'CURRENT_PROJECT_VERSION="46"', 1)
build.write_text(t, encoding="utf-8")

print("SalahPath v3.41 exact reference icon/artwork pass applied")
