from pathlib import Path

# SalahPath v3.27 — recover from broken binary payload and continue with
# screenshot-driven vector artwork. This patch intentionally applies on top
# of v3.25; v3.26 is skipped by the workflows.

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# Deterministic QA location/date path. Production behavior remains unchanged.
needle = '''    private let engine = PrayerEngine()
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()
'''
replacement = '''    private let engine = PrayerEngine()
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    private var isScreenshotQA: Bool {
        ProcessInfo.processInfo.environment["SALAH_QA_SCREENSHOT"] == "1"
    }

    private var qaNow: Date {
        var components = DateComponents()
        components.calendar = Calendar(identifier: .gregorian)
        components.timeZone = TimeZone(identifier: "Europe/Istanbul")
        components.year = 2025
        components.month = 3
        components.day = 14
        components.hour = 12
        components.minute = 43
        components.second = 0
        return components.date ?? Date()
    }

    private var effectiveNow: Date {
        isScreenshotQA ? qaNow : now
    }

    private var effectiveLocation: CLLocation? {
        if isScreenshotQA {
            return CLLocation(latitude: 41.0082, longitude: 28.9784)
        }
        return locationManager.location
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
                   let today = engine.calculateDay(for: effectiveNow, location: location, settings: settings) {
''', 1)

s = s.replace(
'''        .onAppear { locationManager.requestAccessAndStart() }
        .onReceive(timer) { now = $0 }
''',
'''        .onAppear {
            if !isScreenshotQA {
                locationManager.requestAccessAndStart()
            }
        }
        .onReceive(timer) {
            if !isScreenshotQA { now = $0 }
        }
''', 1)

s = s.replace(
'''            if let location = locationManager.location,
               let today = engine.calculateDay(for: prayer.date, location: location, settings: settings),
''',
'''            if let location = effectiveLocation,
               let today = engine.calculateDay(for: prayer.date, location: location, settings: settings),
''', 1)

# Use effective date consistently on Home for QA.
s = s.replace('engine.nextPrayer(now: now, location: location, settings: settings)',
              'engine.nextPrayer(now: effectiveNow, location: location, settings: settings)', 1)
s = s.replace('let dua = DailyDuaStore.item(for: now)', 'let dua = DailyDuaStore.item(for: effectiveNow)', 1)
s = s.replace('PrayerTrackerStore.streak(upTo: now)', 'PrayerTrackerStore.streak(upTo: effectiveNow)', 1)

# Brand mark: replace generic SF leaf-in-rounded-square with a bespoke vector mark.
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
new_logo = '''            ReferenceLeafMark()
                .frame(width: 37, height: 45)
                .accessibilityHidden(true)
'''
if old_logo not in s:
    raise SystemExit("Brand logo target not found")
s = s.replace(old_logo, new_logo, 1)

# Mosque artwork: the ReferenceMosqueSkyline type below is replaced with a
# true custom Canvas drawing, no SF Symbols.
s = s.replace(
'''            ReferenceMosqueSkyline()
                .frame(width: 188, height: 102)
                .opacity(0.74)
                .offset(x: 10, y: -8)
''',
'''            ReferenceMosqueSkyline()
                .frame(width: 192, height: 112)
                .opacity(0.92)
                .offset(x: 9, y: -2)
''', 1)

# QA/reference location label.
s = s.replace(
'''                    Text(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
''',
'''                    Text(effectiveLocality)
''', 1)

# Date in the reference is the visual target during QA.
s = s.replace('Text(gregorianDateShort(now))', 'Text(gregorianDateShort(effectiveNow))', 1)
s = s.replace('Text(shortWeekday(now))', 'Text(shortWeekday(effectiveNow))', 1)
s = s.replace('Text(countdownString(from: now, to: prayer.date))',
              'Text(countdownString(from: effectiveNow, to: prayer.date))', 1)

# One unified white prayer sequence strip, matching the reference artwork.
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
                .background(Color.white.opacity(0.95), in: RoundedRectangle(cornerRadius: 7, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 7, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.30), lineWidth: 0.7)
                }
'''
if old_sequence not in s:
    raise SystemExit("Prayer sequence target not found")
s = s.replace(old_sequence, new_sequence, 1)

# Current-week calculations should use the QA reference date for screenshot comparison.
s = s.replace('let startOfWeek = calendar.dateInterval(of: .weekOfYear, for: now)?.start ?? now',
              'let startOfWeek = calendar.dateInterval(of: .weekOfYear, for: effectiveNow)?.start ?? effectiveNow', 1)

# Replace the old SF-symbol-based mosque view.
mosque_start = s.index("private struct ReferenceMosqueSkyline: View {")
mosque_end = s.index("\nprivate struct DashboardTile: View {", mosque_start)
custom_art = r'''private struct ReferenceLeafMark: View {
    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height

            ZStack {
                Path { path in
                    path.move(to: CGPoint(x: w * 0.50, y: h * 0.92))
                    path.addCurve(
                        to: CGPoint(x: w * 0.19, y: h * 0.34),
                        control1: CGPoint(x: w * 0.30, y: h * 0.77),
                        control2: CGPoint(x: w * 0.16, y: h * 0.56)
                    )
                    path.addCurve(
                        to: CGPoint(x: w * 0.51, y: h * 0.08),
                        control1: CGPoint(x: w * 0.22, y: h * 0.20),
                        control2: CGPoint(x: w * 0.36, y: h * 0.10)
                    )
                    path.addCurve(
                        to: CGPoint(x: w * 0.50, y: h * 0.92),
                        control1: CGPoint(x: w * 0.58, y: h * 0.35),
                        control2: CGPoint(x: w * 0.55, y: h * 0.68)
                    )
                }
                .fill(SalahTheme.gold)

                Path { path in
                    path.move(to: CGPoint(x: w * 0.48, y: h * 0.91))
                    path.addCurve(
                        to: CGPoint(x: w * 0.83, y: h * 0.27),
                        control1: CGPoint(x: w * 0.61, y: h * 0.67),
                        control2: CGPoint(x: w * 0.78, y: h * 0.49)
                    )
                    path.addCurve(
                        to: CGPoint(x: w * 0.57, y: h * 0.16),
                        control1: CGPoint(x: w * 0.74, y: h * 0.18),
                        control2: CGPoint(x: w * 0.65, y: h * 0.16)
                    )
                    path.addCurve(
                        to: CGPoint(x: w * 0.48, y: h * 0.91),
                        control1: CGPoint(x: w * 0.58, y: h * 0.43),
                        control2: CGPoint(x: w * 0.51, y: h * 0.70)
                    )
                }
                .fill(SalahTheme.gold.opacity(0.96))

                Path { path in
                    path.move(to: CGPoint(x: w * 0.49, y: h * 0.87))
                    path.addCurve(
                        to: CGPoint(x: w * 0.60, y: h * 0.20),
                        control1: CGPoint(x: w * 0.49, y: h * 0.62),
                        control2: CGPoint(x: w * 0.55, y: h * 0.38)
                    )
                }
                .stroke(Color.white.opacity(0.72), lineWidth: max(1, w * 0.045))
            }
        }
    }
}

private struct ReferenceMosqueSkyline: View {
    var body: some View {
        GeometryReader { proxy in
            Canvas { context, size in
                // Soft sky/haze that dissolves into the cream card.
                let hazeRect = CGRect(x: size.width * 0.08, y: size.height * 0.06, width: size.width * 0.92, height: size.height * 0.90)
                context.fill(
                    Path(roundedRect: hazeRect, cornerRadius: size.height * 0.18),
                    with: .linearGradient(
                        Gradient(colors: [
                            SalahTheme.softTeal.opacity(0.02),
                            SalahTheme.softTeal.opacity(0.22),
                            SalahTheme.gold.opacity(0.06)
                        ]),
                        startPoint: CGPoint(x: hazeRect.minX, y: hazeRect.minY),
                        endPoint: CGPoint(x: hazeRect.maxX, y: hazeRect.maxY)
                    )
                )

                func fill(_ path: Path, opacity: Double = 1.0) {
                    context.fill(path, with: .color(SalahTheme.teal.opacity(opacity)))
                }

                func minaret(x: CGFloat, baseY: CGFloat, height: CGFloat, width: CGFloat) {
                    var shaft = Path()
                    shaft.addRoundedRect(
                        in: CGRect(x: x - width / 2, y: baseY - height * 0.72, width: width, height: height * 0.72),
                        cornerSize: CGSize(width: width * 0.25, height: width * 0.25)
                    )
                    fill(shaft, opacity: 0.94)

                    var balcony = Path()
                    balcony.addRect(CGRect(x: x - width * 0.90, y: baseY - height * 0.48, width: width * 1.80, height: max(1.2, width * 0.22)))
                    fill(balcony, opacity: 0.95)

                    var cap = Path()
                    cap.move(to: CGPoint(x: x, y: baseY - height))
                    cap.addLine(to: CGPoint(x: x - width * 0.65, y: baseY - height * 0.72))
                    cap.addLine(to: CGPoint(x: x + width * 0.65, y: baseY - height * 0.72))
                    cap.closeSubpath()
                    fill(cap, opacity: 0.96)

                    var crescentStem = Path()
                    crescentStem.move(to: CGPoint(x: x, y: baseY - height))
                    crescentStem.addLine(to: CGPoint(x: x, y: baseY - height - 4))
                    context.stroke(crescentStem, with: .color(SalahTheme.gold.opacity(0.90)), lineWidth: 1)
                }

                func dome(centerX: CGFloat, baseY: CGFloat, width: CGFloat, wallHeight: CGFloat) {
                    let left = centerX - width / 2
                    let top = baseY - wallHeight - width * 0.38

                    var body = Path()
                    body.addRoundedRect(
                        in: CGRect(x: left, y: baseY - wallHeight, width: width, height: wallHeight),
                        cornerSize: CGSize(width: 2, height: 2)
                    )
                    fill(body, opacity: 0.92)

                    var roof = Path()
                    roof.move(to: CGPoint(x: left, y: baseY - wallHeight))
                    roof.addQuadCurve(
                        to: CGPoint(x: centerX, y: top),
                        control: CGPoint(x: left + width * 0.18, y: top + width * 0.02)
                    )
                    roof.addQuadCurve(
                        to: CGPoint(x: left + width, y: baseY - wallHeight),
                        control: CGPoint(x: left + width * 0.82, y: top + width * 0.02)
                    )
                    roof.closeSubpath()
                    fill(roof, opacity: 0.94)

                    var finial = Path()
                    finial.move(to: CGPoint(x: centerX, y: top))
                    finial.addLine(to: CGPoint(x: centerX, y: top - 5))
                    context.stroke(finial, with: .color(SalahTheme.gold.opacity(0.94)), lineWidth: 1)
                }

                let baseY = size.height * 0.94

                // Main silhouette follows the supplied reference: tall central minaret,
                // one large dome and staggered smaller domes/minarets.
                minaret(x: size.width * 0.31, baseY: baseY, height: size.height * 0.83, width: size.width * 0.026)
                minaret(x: size.width * 0.77, baseY: baseY, height: size.height * 0.66, width: size.width * 0.021)
                minaret(x: size.width * 0.91, baseY: baseY, height: size.height * 0.58, width: size.width * 0.018)

                dome(centerX: size.width * 0.57, baseY: baseY, width: size.width * 0.30, wallHeight: size.height * 0.22)
                dome(centerX: size.width * 0.78, baseY: baseY, width: size.width * 0.18, wallHeight: size.height * 0.17)
                dome(centerX: size.width * 0.42, baseY: baseY, width: size.width * 0.16, wallHeight: size.height * 0.15)

                // Low city silhouette gives the artwork the same cut-out baseline.
                var city = Path()
                city.addRoundedRect(
                    in: CGRect(x: size.width * 0.13, y: baseY - size.height * 0.15, width: size.width * 0.84, height: size.height * 0.16),
                    cornerSize: CGSize(width: 2, height: 2)
                )
                fill(city, opacity: 0.54)

                // Gold pinpoints mimic the warm highlights in the source art.
                for point in [
                    CGPoint(x: size.width * 0.56, y: size.height * 0.27),
                    CGPoint(x: size.width * 0.73, y: size.height * 0.39),
                    CGPoint(x: size.width * 0.88, y: size.height * 0.48)
                ] {
                    context.fill(Path(ellipseIn: CGRect(x: point.x - 1.4, y: point.y - 1.4, width: 2.8, height: 2.8)), with: .color(SalahTheme.gold.opacity(0.90)))
                }
            }
        }
        .mask(
            LinearGradient(
                stops: [
                    .init(color: .clear, location: 0.00),
                    .init(color: .white, location: 0.12),
                    .init(color: .white, location: 0.82),
                    .init(color: .clear, location: 1.00)
                ],
                startPoint: .leading,
                endPoint: .trailing
            )
        )
        .accessibilityHidden(true)
    }
}
'''
s = s[:mosque_start] + custom_art + s[mosque_end:]

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.25"', 'MARKETING_VERSION="3.27"')
t = t.replace('CURRENT_PROJECT_VERSION="30"', 'CURRENT_PROJECT_VERSION="32"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.27 vector reference-art + deterministic QA patch applied")
