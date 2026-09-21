from pathlib import Path
import base64
import io
import json
import zipfile

root = Path.cwd()
assets_root = root / "SalahZeit" / "Assets.xcassets"

# Restore the original prayer reference sheets from the v3.5 source package.
archive_b64 = (root / "v35-assets" / "illustrations.b64").read_text(encoding="utf-8")
archive = base64.b64decode("".join(archive_b64.split()))

with zipfile.ZipFile(io.BytesIO(archive)) as zf:
    sources = {
        "prayer_reference_male": "PrayerMaleSheet.jpg",
        "prayer_reference_female": "PrayerFemaleSheet.jpg",
    }
    for asset_name, source_name in sources.items():
        data = zf.read(source_name)
        imageset = assets_root / f"{asset_name}.imageset"
        imageset.mkdir(parents=True, exist_ok=True)
        jpg_name = f"{asset_name}.jpg"
        (imageset / jpg_name).write_bytes(data)
        (imageset / "Contents.json").write_text(
            json.dumps({
                "images": [{
                    "filename": jpg_name,
                    "idiom": "universal",
                    "scale": "1x"
                }],
                "info": {
                    "author": "xcode",
                    "version": 1
                }
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

guide = root / "SalahZeit" / "Views" / "GuideView.swift"
text = guide.read_text(encoding="utf-8")

start_marker = "struct PrayerSequenceReferenceView: View {"
end_marker = "// MARK: - Dhikr"
start = text.find(start_marker)
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("v437: PrayerSequenceReferenceView block missing")

new_block = r'''struct PrayerSequenceReferenceView: View {
    @EnvironmentObject private var settings: SettingsStore

    private var referenceAssetName: String {
        settings.prayerAudience == .female
            ? "prayer_reference_female"
            : "prayer_reference_male"
    }

    var body: some View {
        ScrollView {
            Image(referenceAssetName)
                .resizable()
                .scaledToFit()
                .frame(maxWidth: .infinity)
                .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
                }
                .padding(12)
                .accessibilityLabel(settings.t(
                    "Gebetspositionen als Bildfolge",
                    "Namaz duruşları görsel sırası"
                ))
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetspositionen", "Namaz duruşları"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

'''

text = text[:start] + new_block + text[end:]
guide.write_text(text, encoding="utf-8")

print("v437 applied: restored original male/female prayer reference sheets")
