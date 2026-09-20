from pathlib import Path

root = Path.cwd()
guide = root / 'SalahZeit' / 'Views' / 'GuideView.swift'
s = guide.read_text(encoding='utf-8')

anchor = '''// MARK: - Rak'ah overview

private struct ReferencePrayerPerson: View {
'''
art = r'''// MARK: - Rak'ah overview

private struct PrayerPoseArtwork: View {
    let assetName: String

    private var female: Bool { assetName.hasPrefix("female_") }
    private var pose: String {
        assetName
            .replacingOccurrences(of: "male_", with: "")
            .replacingOccurrences(of: "female_", with: "")
    }

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .fill(SalahTheme.softTeal.opacity(0.38))

            VStack {
                Spacer()
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(SalahTheme.teal.opacity(0.14))
                    .overlay {
                        RoundedRectangle(cornerRadius: 12, style: .continuous)
                            .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
                    }
                    .frame(height: 38)
                    .padding(.horizontal, 18)
                    .padding(.bottom, 10)
            }

            Canvas { context, size in
                drawPose(context: &context, size: size)
            }
            .padding(8)
        }
        .accessibilityHidden(true)
    }

    private func point(_ x: CGFloat, _ y: CGFloat, in size: CGSize) -> CGPoint {
        CGPoint(x: size.width * x, y: size.height * y)
    }

    private func line(_ context: inout GraphicsContext, _ a: CGPoint, _ b: CGPoint, width: CGFloat, color: Color = SalahTheme.deepTeal) {
        var p = Path()
        p.move(to: a)
        p.addLine(to: b)
        context.stroke(p, with: .color(color), style: StrokeStyle(lineWidth: width, lineCap: .round, lineJoin: .round))
    }

    private func polyline(_ context: inout GraphicsContext, _ points: [CGPoint], width: CGFloat, color: Color = SalahTheme.deepTeal) {
        guard let first = points.first else { return }
        var p = Path()
        p.move(to: first)
        for point in points.dropFirst() { p.addLine(to: point) }
        context.stroke(p, with: .color(color), style: StrokeStyle(lineWidth: width, lineCap: .round, lineJoin: .round))
    }

    private func head(_ context: inout GraphicsContext, center: CGPoint, radius: CGFloat) {
        let rect = CGRect(x: center.x - radius, y: center.y - radius, width: radius * 2, height: radius * 2)
        context.fill(Path(ellipseIn: rect), with: .color(Color.white.opacity(0.96)))
        context.stroke(Path(ellipseIn: rect), with: .color(SalahTheme.deepTeal), lineWidth: 5)

        if female {
            let hood = CGRect(x: center.x - radius * 1.22, y: center.y - radius * 1.22, width: radius * 2.44, height: radius * 2.62)
            context.stroke(Path(ellipseIn: hood), with: .color(SalahTheme.teal), lineWidth: 7)
        } else {
            var cap = Path()
            cap.move(to: CGPoint(x: center.x - radius * 0.72, y: center.y - radius * 0.76))
            cap.addLine(to: CGPoint(x: center.x + radius * 0.72, y: center.y - radius * 0.76))
            context.stroke(cap, with: .color(SalahTheme.gold), style: StrokeStyle(lineWidth: 6, lineCap: .round))
        }
    }

    private func torso(_ context: inout GraphicsContext, shoulder: CGPoint, hip: CGPoint, width: CGFloat) {
        line(&context, shoulder, hip, width: width, color: SalahTheme.teal)
        if female {
            var skirt = Path()
            skirt.move(to: CGPoint(x: hip.x - 18, y: hip.y - 2))
            skirt.addLine(to: CGPoint(x: hip.x - 34, y: hip.y + 70))
            skirt.addLine(to: CGPoint(x: hip.x + 34, y: hip.y + 70))
            skirt.addLine(to: CGPoint(x: hip.x + 18, y: hip.y - 2))
            skirt.closeSubpath()
            context.fill(skirt, with: .color(SalahTheme.teal.opacity(0.94)))
        }
    }

    private func drawPose(context: inout GraphicsContext, size: CGSize) {
        switch pose {
        case "bowing": drawBowing(&context, size: size)
        case "sujud": drawSujud(&context, size: size)
        case "sitting", "final_sitting": drawSitting(&context, size: size, turn: 0)
        case "salam_right": drawSitting(&context, size: size, turn: 1)
        case "salam_left": drawSitting(&context, size: size, turn: -1)
        case "takbir": drawStanding(&context, size: size, mode: .takbir)
        case "standing": drawStanding(&context, size: size, mode: .bound)
        case "upright": drawStanding(&context, size: size, mode: .relaxed)
        default: drawStanding(&context, size: size, mode: .intention)
        }
    }

    private enum StandingMode: Equatable { case intention, takbir, bound, relaxed }

    private func drawStanding(_ context: inout GraphicsContext, size: CGSize, mode: StandingMode) {
        let c: CGFloat = 0.50
        let headCenter = point(c, 0.20, in: size)
        let shoulder = point(c, 0.34, in: size)
        let hip = point(c, 0.66, in: size)
        let leftShoulder = point(c - 0.10, 0.35, in: size)
        let rightShoulder = point(c + 0.10, 0.35, in: size)
        let leftFoot = point(c - (female ? 0.055 : 0.075), 0.91, in: size)
        let rightFoot = point(c + (female ? 0.055 : 0.075), 0.91, in: size)

        torso(&context, shoulder: shoulder, hip: hip, width: female ? 38 : 32)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.072)
        line(&context, point(c - 0.04, 0.67, in: size), leftFoot, width: 13)
        line(&context, point(c + 0.04, 0.67, in: size), rightFoot, width: 13)

        switch mode {
        case .takbir:
            let handY: CGFloat = female ? 0.29 : 0.22
            polyline(&context, [leftShoulder, point(c - 0.18, 0.28, in: size), point(c - 0.17, handY, in: size)], width: 11)
            polyline(&context, [rightShoulder, point(c + 0.18, 0.28, in: size), point(c + 0.17, handY, in: size)], width: 11)
        case .bound:
            let handY: CGFloat = female ? 0.47 : 0.56
            polyline(&context, [leftShoulder, point(c - 0.08, 0.48, in: size), point(c + 0.02, handY, in: size)], width: 10)
            polyline(&context, [rightShoulder, point(c + 0.08, 0.48, in: size), point(c - 0.02, handY, in: size)], width: 10)
            let handRect = CGRect(x: size.width * c - 18, y: size.height * handY - 8, width: 36, height: 16)
            context.fill(Path(roundedRect: handRect, cornerRadius: 8), with: .color(SalahTheme.gold))
        case .intention, .relaxed:
            line(&context, leftShoulder, point(c - 0.12, 0.64, in: size), width: 10)
            line(&context, rightShoulder, point(c + 0.12, 0.64, in: size), width: 10)
            if mode == .intention {
                let heartRect = CGRect(x: size.width * c - 8, y: size.height * 0.43 - 8, width: 16, height: 16)
                context.fill(Path(ellipseIn: heartRect), with: .color(SalahTheme.gold))
            }
        }
    }

    private func drawBowing(_ context: inout GraphicsContext, size: CGSize) {
        let hip = point(female ? 0.43 : 0.40, 0.58, in: size)
        let shoulder = point(female ? 0.61 : 0.66, female ? 0.49 : 0.46, in: size)
        let headCenter = point(female ? 0.72 : 0.78, female ? 0.47 : 0.45, in: size)

        torso(&context, shoulder: shoulder, hip: hip, width: female ? 36 : 31)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.067)
        line(&context, point(0.38, 0.60, in: size), point(0.37, 0.90, in: size), width: 13)
        line(&context, point(0.46, 0.60, in: size), point(0.48, 0.90, in: size), width: 13)
        polyline(&context, [shoulder, point(0.58, 0.61, in: size), point(0.48, 0.69, in: size)], width: 10)
        polyline(&context, [point(shoulder.x / size.width + 0.02, shoulder.y / size.height + 0.01, in: size), point(0.66, 0.62, in: size), point(0.49, 0.70, in: size)], width: 10)
    }

    private func drawSujud(_ context: inout GraphicsContext, size: CGSize) {
        let knee = point(female ? 0.41 : 0.35, 0.73, in: size)
        let hip = point(female ? 0.46 : 0.43, female ? 0.58 : 0.52, in: size)
        let shoulder = point(female ? 0.61 : 0.62, female ? 0.69 : 0.65, in: size)
        let headCenter = point(female ? 0.72 : 0.76, 0.75, in: size)

        polyline(&context, [knee, hip, shoulder], width: female ? 34 : 30, color: SalahTheme.teal)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.062)
        polyline(&context, [knee, point(0.30, 0.82, in: size), point(0.24, 0.82, in: size)], width: 13)
        polyline(&context, [shoulder, point(female ? 0.66 : 0.58, 0.79, in: size), point(female ? 0.69 : 0.63, 0.83, in: size)], width: 10)
        polyline(&context, [shoulder, point(female ? 0.70 : 0.72, 0.78, in: size), point(female ? 0.73 : 0.78, 0.83, in: size)], width: 10)
        line(&context, point(0.67, 0.84, in: size), point(0.82, 0.84, in: size), width: 5, color: SalahTheme.gold)
    }

    private func drawSitting(_ context: inout GraphicsContext, size: CGSize, turn: Int) {
        let hip = point(0.48, 0.62, in: size)
        let shoulder = point(0.48, 0.40, in: size)
        let headX = 0.48 + CGFloat(turn) * 0.035
        let headCenter = point(headX, 0.27, in: size)

        torso(&context, shoulder: shoulder, hip: hip, width: female ? 37 : 31)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.068)
        line(&context, point(0.39, 0.42, in: size), point(0.39, 0.61, in: size), width: 10)
        line(&context, point(0.57, 0.42, in: size), point(0.57, 0.61, in: size), width: 10)
        line(&context, point(0.39, 0.60, in: size), point(0.53, 0.68, in: size), width: 9, color: SalahTheme.gold)
        line(&context, point(0.57, 0.60, in: size), point(0.67, 0.68, in: size), width: 9, color: SalahTheme.gold)

        if female {
            polyline(&context, [hip, point(0.60, 0.70, in: size), point(0.74, 0.80, in: size)], width: 15)
            polyline(&context, [point(0.46, 0.65, in: size), point(0.57, 0.77, in: size), point(0.71, 0.84, in: size)], width: 15)
        } else {
            polyline(&context, [hip, point(0.40, 0.76, in: size), point(0.29, 0.84, in: size)], width: 14)
            polyline(&context, [point(0.51, 0.65, in: size), point(0.62, 0.78, in: size), point(0.72, 0.84, in: size)], width: 14)
        }

        if turn != 0 {
            let x = turn > 0 ? size.width * 0.76 : size.width * 0.20
            var arrow = Path()
            arrow.move(to: CGPoint(x: size.width * 0.50, y: size.height * 0.20))
            arrow.addLine(to: CGPoint(x: x, y: size.height * 0.20))
            context.stroke(arrow, with: .color(SalahTheme.gold), style: StrokeStyle(lineWidth: 5, lineCap: .round))
        }
    }
}

private struct ReferencePrayerPerson: View {
'''
if anchor not in s:
    raise SystemExit('v3.64: prayer artwork insertion anchor missing')
s = s.replace(anchor, art, 1)

old = '''            Image(imageName)
                .resizable()
                .scaledToFit()
                .frame(maxWidth: .infinity, maxHeight: 230)
                .blendMode(.multiply)
                .padding(.bottom, 5)
'''
new = '''            PrayerPoseArtwork(assetName: imageName)
                .frame(maxWidth: .infinity, maxHeight: 230)
                .padding(.horizontal, 8)
                .padding(.bottom, 5)
'''
if old not in s:
    raise SystemExit('v3.64: reference prayer person image anchor missing')
s = s.replace(old, new, 1)

old = '''                    Image("male_intention")
                        .resizable()
                        .scaledToFit()
                        .frame(height: 128)
                        .opacity(settings.prayerAudience == .male ? 1 : 0.48)
'''
new = '''                    PrayerPoseArtwork(assetName: "male_intention")
                        .frame(height: 128)
                        .opacity(settings.prayerAudience == .male ? 1 : 0.48)
'''
if old not in s:
    raise SystemExit('v3.64: male hero anchor missing')
s = s.replace(old, new, 1)

old = '''                    Image("female_intention")
                        .resizable()
                        .scaledToFit()
                        .frame(height: 128)
                        .opacity(settings.prayerAudience == .female ? 1 : 0.48)
'''
new = '''                    PrayerPoseArtwork(assetName: "female_intention")
                        .frame(height: 128)
                        .opacity(settings.prayerAudience == .female ? 1 : 0.48)
'''
if old not in s:
    raise SystemExit('v3.64: female hero anchor missing')
s = s.replace(old, new, 1)

old = '''                } else if let imageName {
                    Image(imageName)
                        .resizable()
                        .scaledToFit()
                        .frame(maxWidth: .infinity)
                        .frame(height: 245)
                        .padding(.vertical, 6)
                        .background(SalahTheme.cream)
                        .accessibilityHidden(true)
                }
'''
new = '''                } else if let imageName {
                    PrayerPoseArtwork(assetName: imageName)
                        .frame(maxWidth: .infinity)
                        .frame(height: 245)
                        .padding(.vertical, 6)
                        .background(SalahTheme.cream)
                }
'''
if old not in s:
    raise SystemExit('v3.64: prayer step image anchor missing')
s = s.replace(old, new, 1)

old = '''                Image(imageName)
                    .resizable()
                    .scaledToFit()
                    .frame(width: 118, height: 150)
                    .background(SalahTheme.cream)
                    .clipShape(RoundedRectangle(cornerRadius: 14))
'''
new = '''                PrayerPoseArtwork(assetName: imageName)
                    .frame(width: 118, height: 150)
                    .background(SalahTheme.cream)
                    .clipShape(RoundedRectangle(cornerRadius: 14))
'''
if old not in s:
    raise SystemExit('v3.64: salam artwork anchor missing')
s = s.replace(old, new, 1)

guide.write_text(s, encoding='utf-8')
print('SalahPath v3.64 prayer pose artwork applied')
