from pathlib import Path
import base64, io, json, tarfile

# SalahPath v3.26 — real reference artwork + deterministic screenshot QA.

# Decode the reference artwork payload into the asset catalog.
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

# Screenshot QA gets a deterministic Istanbul location without changing production behavior.
needle = '''    private let engine = PrayerEngine()
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()
'''
replacement = '''    private let engine = PrayerEngine()
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    private var isScreenshotQA: Bool {
        ProcessInfo.processInfo.environment["SALAH_QA_SCREENSHOT"] == "1"
    }

    private var effectiveLocation: CLLocation? {
        if let live = locationManager.location { return live }
        if isScreenshotQA {
            return CLLocation(latitude: 41.0082, longitude: 28.9784)
        }
        return nil
    }

    private var effectiveLocality: String {
        if isScreenshotQA { return "İstanbul" }
        return locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum")
    }
'''
if needle not in s:
    raise SystemExit("Home QA insertion point not found")
s = s.replace(needle, replacement, 1)

s = s.replace(
'''                if let location = locationManager.location,
                   let today = engine.calculateDay(for: now, location: location, settings: settings) {
''',
'''                if let location = effectiveLocation,
                   let today = engine.calculateDay(for: now, location: location, settings: settings) {
''', 1)

s = s.replace(
'''        .onAppear { locationManager.requestAccessAndStart() }
''',
'''        .onAppear {
            if !isScreenshotQA {
                locationManager.requestAccessAndStart()
            }
        }
''', 1)

s = s.replace(
'''            if let location = locationManager.location,
''',
'''            if let location = effectiveLocation,
''', 1)

# Use the extracted reference logo, not an SF Symbol in a generic rounded square.
old_logo = '''            ZStack {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.72), lineWidth: 1)
                    .frame(width: 37, height: 37)
                Image(systemName: "leaf.fill")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundStyle(SalahTheme.gold)
                    .rotationEffect(.degrees(-8))
            }
'''
new_logo = '''            Image("salahpath_logo")
                .resizable()
                .scaledToFit()
                .frame(width: 37, height: 44)
                .accessibilityHidden(true)
'''
if old_logo not in s:
    raise SystemExit("Reference logo replacement target not found")
s = s.replace(old_logo, new_logo, 1)

# Use the real mosque artwork from the supplied visual reference.
old_mosque = '''            ReferenceMosqueSkyline()
                .frame(width: 188, height: 102)
                .opacity(0.74)
                .offset(x: 10, y: -8)
'''
new_mosque = '''            Image("home_mosque")
                .resizable()
                .scaledToFit()
                .frame(width: 188, height: 108)
                .opacity(0.96)
                .offset(x: 7, y: -4)
                .accessibilityHidden(true)
'''
if old_mosque not in s:
    raise SystemExit("Reference mosque replacement target not found")
s = s.replace(old_mosque, new_mosque, 1)

s = s.replace(
'''                    Text(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
''',
'''                    Text(effectiveLocality)
''', 1)

# The reference has one unified white prayer-sequence strip, not separate floating pills.
old_sequence = '''                HStack(spacing: 3) {
                    let segments = referenceSequence(for: prayer.kind)
                    ForEach(Array(segments.enumerated()), id: \.offset) { index, segment in
                        HStack(spacing: 3) {
                            Text(segment.0)
                                .font(.system(size: 9.4, weight: .bold))
                            Text(segment.1)
                                .font(.system(size: 7.4, weight: .semibold))
                        }
                        .foregroundStyle(SalahTheme.ink)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 4)
                        .background(Color.white.opacity(0.90), in: RoundedRectangle(cornerRadius: 7, style: .continuous))
                        .overlay {
                            RoundedRectangle(cornerRadius: 7, style: .continuous)
                                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7)
                        }

                        if index < segments.count - 1 {
                            Image(systemName: "arrow.right")
                                .font(.system(size: 7, weight: .black))
                                .foregroundStyle(SalahTheme.teal)
                        }
                    }
                }
'''
new_sequence = '''                HStack(spacing: 5) {
                    Image(systemName: prayer.kind.systemImage)
                        .font(.system(size: 10, weight: .semibold))
                        .foregroundStyle(SalahTheme.gold)

                    let segments = referenceSequence(for: prayer.kind)
                    ForEach(Array(segments.enumerated()), id: \.offset) { index, segment in
                        HStack(spacing: 2) {
                            Text(segment.0)
                                .font(.system(size: 9.5, weight: .bold))
                            Text(segment.1)
                                .font(.system(size: 8.0, weight: .bold))
                        }
                        .foregroundStyle(SalahTheme.ink)

                        if index < segments.count - 1 {
                            Image(systemName: "arrow.right")
                                .font(.system(size: 7.5, weight: .black))
                                .foregroundStyle(SalahTheme.teal)
                        }
                    }

                    Spacer(minLength: 0)
                    Image(systemName: "chevron.right")
                        .font(.system(size: 7.5, weight: .bold))
                        .foregroundStyle(SalahTheme.gold)
                }
                .frame(maxWidth: .infinity)
                .padding(.horizontal, 8)
                .padding(.vertical, 5)
                .background(Color.white.opacity(0.94), in: RoundedRectangle(cornerRadius: 7, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 7, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.30), lineWidth: 0.7)
                }
'''
if old_sequence not in s:
    raise SystemExit("Prayer sequence replacement target not found")
s = s.replace(old_sequence, new_sequence, 1)

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.25"', 'MARKETING_VERSION="3.26"')
t = t.replace('CURRENT_PROJECT_VERSION="30"', 'CURRENT_PROJECT_VERSION="31"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.26 reference assets + QA-location patch applied")
