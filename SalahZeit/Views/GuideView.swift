import SwiftUI
import EventKit
import EventKitUI
import AVFoundation
import MediaPlayer
import UIKit

// MARK: - Learning hub

struct GuideView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                learningHero
                quickLearningLinks
            }
            .padding(.horizontal, 11)
            .padding(.vertical, 10)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebet lernen", "Namaz Öğren"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }

    private var learningHero: some View {
        VStack(spacing: 9) {
            HStack(spacing: 4) {
                audiencePill(.male, title: settings.t("Mann", "Erkek"))
                audiencePill(.female, title: settings.t("Frau", "Kadın"))

                Button {
                    settings.language = settings.language == .german ? .turkish : .german
                } label: {
                    Text(settings.language == .german ? "Türkçe" : "Deutsch")
                        .font(.system(size: 10.4, weight: .bold))
                        .foregroundStyle(SalahTheme.deepTeal)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 6)
                        .background(
                            SalahTheme.gold.opacity(0.18),
                            in: RoundedRectangle(cornerRadius: 8, style: .continuous)
                        )
                }
                .buttonStyle(.plain)
            }
            .padding(3)
            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
            .overlay { RoundedRectangle(cornerRadius: 8).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7) }

            ZStack(alignment: .trailing) {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .fill(Color(red: 0.96, green: 0.93, blue: 0.84))

                HStack(alignment: .bottom, spacing: 10) {
                    ReferencePrayerPerson(
                        imageName: "male_intention",
                        rugWidth: 120,
                        rugRotation: -1.5
                    )

                    ReferencePrayerPerson(
                        imageName: "female_intention",
                        rugWidth: 120,
                        rugRotation: 1.5
                    )
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 2)

                NavigationLink {
                    PrayerHowToView()
                } label: {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: 32, height: 32)
                        Image(systemName: "chevron.right")
                            .font(.system(size: 12, weight: .black))
                            .foregroundStyle(.white)
                    }
                }
                .buttonStyle(.plain)
                .padding(.trailing, 4)
            }
            .frame(height: 300)
            .overlay {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.30), lineWidth: 0.7)
            }

            VStack(alignment: .leading, spacing: 11) {
                referenceLearnFeature(
                    turkish: "Namaz nasıl kılınır?",
                    german: "Wie betet man?"
                )
                referenceLearnFeature(
                    turkish: "Adım adım anlatım",
                    german: "Schritt-für-Schritt Anleitung"
                )
                referenceLearnFeature(
                    turkish: "Görsel ve okunan metinlerle",
                    german: "Mit Bildern und Rezitationstexten"
                )
                referenceLearnFeature(
                    turkish: "Hanefî mezhebine göre",
                    german: "Nach hanafitischem Verständnis"
                )
            }
            .padding(.horizontal, 3)

        }
        .padding(9)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 10).stroke(SalahTheme.gold.opacity(0.44), lineWidth: 0.7) }
    }

    private var quickLearningLinks: some View {
        VStack(spacing: 0) {
            NavigationLink { PrayerCatalogView() } label: {
                referenceRow(
                    icon: "rectangle.stack.badge.play.fill",
                    title: settings.t("Alle Gebete einzeln", "Tüm namazlar tek tek"),
                    subtitle: settings.t("Fajr bis Jumuah, Witr, Tarawih und mehr", "Sabah'tan Cuma'ya, Vitir, Teravih ve daha fazlası")
                )
            }

            NavigationLink { WuduGuideView() } label: {
                referenceRow(
                    icon: "drop.fill",
                    title: settings.t("Wudu Schritt für Schritt", "Abdest adım adım"),
                    subtitle: settings.t("Mit Bildern und genauer Erklärung", "Görseller ve ayrıntılı anlatım")
                )
            }

            NavigationLink { HanafiPrayerPlanView() } label: {
                referenceRow(
                    icon: "list.number",
                    title: settings.t("Rakʿat & Gebetsarten", "Rekât ve namaz türleri"),
                    subtitle: settings.t("2, 3 und 4 Rakʿat richtig einordnen", "2, 3 ve 4 rekâtı doğru öğren")
                )
            }

            NavigationLink { PrayerTextsHubView() } label: {
                referenceRow(
                    icon: "books.vertical.fill",
                    title: settings.t("Suren, Duas & Ayat fürs Gebet", "Namaz Sûreleri, Duaları & Ayetler"),
                    subtitle: settings.t("Inklusive Yasin und Qunūt", "Yasin ve Kunut dahil")
                )
            }

            NavigationLink { PrayerDuaAudioView() } label: {
                referenceRow(
                    icon: "text.book.closed.fill",
                    title: settings.t("Gebetsduas", "Namaz duaları"),
                    subtitle: settings.t("Arabisch, Umschrift und Bedeutung", "Arapça, okunuş ve anlam")
                )
            }

            NavigationLink { ShortSurahLearningView() } label: {
                referenceRow(
                    icon: "play.square.stack.fill",
                    title: settings.t("Kurze Suren", "Kısa sûreler"),
                    subtitle: settings.t("Lesen, lernen und hören", "Oku, öğren ve dinle")
                )
            }
        }
        .buttonStyle(.plain)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 14, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1)
        }
    }

    private func referenceLearnFeature(turkish: String, german: String) -> some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 15, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .padding(.top, 1)
                .accessibilityHidden(true)

            Text(settings.language == .german ? german : turkish)
                .font(.custom("AvenirNext-DemiBold", size: 12.0))
                .foregroundStyle(SalahTheme.ink)
                .fixedSize(horizontal: false, vertical: true)

            Spacer(minLength: 0)
        }
        .padding(.vertical, 4)
    }

    private func audiencePill(_ audience: PrayerAudience, title: String) -> some View {
        Button {
            settings.prayerAudience = audience
        } label: {
            Text(title)
                .font(.system(size: 10.5, weight: .bold))
                .foregroundStyle(settings.prayerAudience == audience ? .white : SalahTheme.deepTeal)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 8)
                .background(
                    settings.prayerAudience == audience ? SalahTheme.teal : Color.clear,
                    in: RoundedRectangle(cornerRadius: 8, style: .continuous)
                )
        }
        .buttonStyle(.plain)
    }

    private func learnFeature(_ text: String) -> some View {
        HStack(spacing: 8) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 13, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
            Text(text)
                .font(.system(size: 11, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer(minLength: 0)
        }
    }

    private func learnTile(icon: String, title: String, subtitle: String) -> some View {
        VStack(spacing: 7) {
            Image(systemName: icon)
                .font(.system(size: 25, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
            Text(title)
                .font(.system(size: 11, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .multilineTextAlignment(.center)
                .lineLimit(2)
            Text(subtitle)
                .font(.system(size: 8.5, weight: .medium))
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)
                .lineLimit(2)
        }
        .frame(maxWidth: .infinity, minHeight: 108)
        .padding(10)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 16).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }
    }

    private func referenceRow(icon: String, title: String, subtitle: String) -> some View {
        HStack(spacing: 10) {
            Image(systemName: icon)
                .font(.system(size: 17, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 31, height: 31)
                .background(SalahTheme.softTeal, in: Circle())
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.system(size: 12, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                Text(subtitle)
                    .font(.system(size: 9, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
            }
            Spacer()
            Image(systemName: "chevron.right")
                .font(.caption.bold())
                .foregroundStyle(SalahTheme.teal)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 10)
        .contentShape(Rectangle())
        .overlay(alignment: .bottom) { Divider().padding(.leading, 53).opacity(0.40) }
    }
}

// MARK: - Rak'ah overview

private struct PrayerPoseArtwork: View {
    let assetName: String

    private var female: Bool { assetName.hasPrefix("female_") }
    private var pose: String {
        assetName
            .replacingOccurrences(of: "male_", with: "")
            .replacingOccurrences(of: "female_", with: "")
    }

    private var garmentColor: Color {
        female
            ? Color(red: 0.60, green: 0.42, blue: 0.50)
            : Color.white.opacity(0.98)
    }

    private var garmentOutline: Color {
        female
            ? Color(red: 0.34, green: 0.24, blue: 0.29)
            : SalahTheme.deepTeal.opacity(0.66)
    }

    private var skinTone: Color {
        Color(red: 0.86, green: 0.68, blue: 0.52)
    }

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.42)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            Canvas { graphics, size in
                var context = graphics

                let arch = CGRect(
                    x: size.width * 0.13,
                    y: size.height * 0.06,
                    width: size.width * 0.74,
                    height: size.height * 0.74
                )
                context.fill(
                    Path(roundedRect: arch, cornerRadius: min(size.width, size.height) * 0.32),
                    with: .color(SalahTheme.softTeal.opacity(0.28))
                )

                var rug = Path()
                rug.move(to: point(0.25, 0.82, in: size))
                rug.addLine(to: point(0.75, 0.82, in: size))
                rug.addLine(to: point(0.82, 0.95, in: size))
                rug.addLine(to: point(0.18, 0.95, in: size))
                rug.closeSubpath()
                context.fill(rug, with: .color(SalahTheme.teal.opacity(0.90)))
                context.stroke(rug, with: .color(SalahTheme.gold.opacity(0.86)), lineWidth: 2)

                drawPose(context: &context, size: size)
            }
            .padding(4)
        }
        .clipShape(RoundedRectangle(cornerRadius: 24, style: .continuous))
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

    private func garmentLine(
        _ context: inout GraphicsContext,
        _ a: CGPoint,
        _ b: CGPoint,
        width: CGFloat
    ) {
        line(&context, a, b, width: width + 4, color: garmentOutline)
        line(&context, a, b, width: width, color: garmentColor)
    }

    private func garmentPolyline(
        _ context: inout GraphicsContext,
        _ points: [CGPoint],
        width: CGFloat
    ) {
        polyline(&context, points, width: width + 4, color: garmentOutline)
        polyline(&context, points, width: width, color: garmentColor)
    }

    private func handDot(_ context: inout GraphicsContext, center: CGPoint, radius: CGFloat) {
        let rect = CGRect(
            x: center.x - radius,
            y: center.y - radius,
            width: radius * 2,
            height: radius * 2
        )
        context.fill(Path(ellipseIn: rect), with: .color(skinTone))
        context.stroke(Path(ellipseIn: rect), with: .color(SalahTheme.deepTeal.opacity(0.45)), lineWidth: 1.2)
    }

    private func head(_ context: inout GraphicsContext, center: CGPoint, radius: CGFloat) {
        let rect = CGRect(x: center.x - radius, y: center.y - radius, width: radius * 2, height: radius * 2)
        context.fill(Path(ellipseIn: rect), with: .color(skinTone))
        context.stroke(Path(ellipseIn: rect), with: .color(SalahTheme.deepTeal), lineWidth: 5)

        if female {
            let hood = CGRect(x: center.x - radius * 1.22, y: center.y - radius * 1.22, width: radius * 2.44, height: radius * 2.62)
            context.stroke(Path(ellipseIn: hood), with: .color(garmentColor), lineWidth: 8)
        } else {
            var hair = Path()
            hair.addArc(
                center: CGPoint(x: center.x, y: center.y - radius * 0.10),
                radius: radius * 0.82,
                startAngle: .degrees(198),
                endAngle: .degrees(342),
                clockwise: false
            )
            context.stroke(
                hair,
                with: .color(SalahTheme.deepTeal),
                style: StrokeStyle(lineWidth: max(radius * 0.19, 3), lineCap: .round)
            )
        }

        drawFace(&context, center: center, radius: radius)
    }

    private func drawFace(_ context: inout GraphicsContext, center: CGPoint, radius: CGFloat) {
        let turn: CGFloat
        if pose == "salam_right" {
            turn = -0.22
        } else if pose == "salam_left" {
            turn = 0.22
        } else {
            turn = 0
        }

        let downward = pose == "bowing" || pose == "sujud"
        let featureY = center.y + (downward ? radius * 0.10 : 0)
        let featureX = center.x + radius * turn
        let eyeGap = radius * 0.34
        let eyeWidth = max(radius * 0.22, 3)
        let ink = SalahTheme.deepTeal

        for direction in [-1.0, 1.0] {
            let x = featureX + eyeGap * CGFloat(direction)
            var eye = Path()
            eye.move(to: CGPoint(x: x - eyeWidth / 2, y: featureY - radius * 0.12))
            eye.addQuadCurve(
                to: CGPoint(x: x + eyeWidth / 2, y: featureY - radius * 0.12),
                control: CGPoint(x: x, y: featureY - radius * (downward ? 0.04 : 0.16))
            )
            context.stroke(eye, with: .color(ink), style: StrokeStyle(lineWidth: max(radius * 0.07, 1.4), lineCap: .round))
        }

        var nose = Path()
        nose.move(to: CGPoint(x: featureX, y: featureY - radius * 0.02))
        nose.addLine(to: CGPoint(x: featureX + radius * 0.05 * (turn == 0 ? 1 : turn.sign == .plus ? 1 : -1), y: featureY + radius * 0.16))
        context.stroke(nose, with: .color(ink.opacity(0.72)), style: StrokeStyle(lineWidth: max(radius * 0.055, 1.1), lineCap: .round))

        var mouth = Path()
        mouth.move(to: CGPoint(x: featureX - radius * 0.20, y: featureY + radius * 0.31))
        mouth.addQuadCurve(
            to: CGPoint(x: featureX + radius * 0.20, y: featureY + radius * 0.31),
            control: CGPoint(x: featureX, y: featureY + radius * 0.37)
        )
        context.stroke(mouth, with: .color(ink), style: StrokeStyle(lineWidth: max(radius * 0.055, 1.1), lineCap: .round))

        if !female {
            var beard = Path()
            beard.move(to: CGPoint(x: featureX - radius * 0.50, y: featureY + radius * 0.30))
            beard.addQuadCurve(
                to: CGPoint(x: featureX + radius * 0.50, y: featureY + radius * 0.30),
                control: CGPoint(x: featureX, y: featureY + radius * 0.82)
            )
            context.stroke(beard, with: .color(ink.opacity(0.92)), style: StrokeStyle(lineWidth: max(radius * 0.12, 2.0), lineCap: .round))
        }
    }

    private func torso(_ context: inout GraphicsContext, shoulder: CGPoint, hip: CGPoint, width: CGFloat) {
        garmentLine(&context, shoulder, hip, width: width)
        if female {
            var skirt = Path()
            skirt.move(to: CGPoint(x: hip.x - 18, y: hip.y - 2))
            skirt.addLine(to: CGPoint(x: hip.x - 34, y: hip.y + 70))
            skirt.addLine(to: CGPoint(x: hip.x + 34, y: hip.y + 70))
            skirt.addLine(to: CGPoint(x: hip.x + 18, y: hip.y - 2))
            skirt.closeSubpath()
            context.fill(skirt, with: .color(garmentColor.opacity(0.97)))
            context.stroke(skirt, with: .color(garmentOutline), lineWidth: 3)
        }
    }

    private func drawPose(context: inout GraphicsContext, size: CGSize) {
        switch pose {
        case "bowing": drawBowing(&context, size: size)
        case "sujud", "second_sujud": drawSujud(&context, size: size)
        case "sitting", "final_sitting": drawSitting(&context, size: size, turn: 0, showFinger: false)
        case "finger": drawSitting(&context, size: size, turn: 0, showFinger: true)
        case "salam_right": drawSitting(&context, size: size, turn: 1, showFinger: false)
        case "salam_left": drawSitting(&context, size: size, turn: -1, showFinger: false)
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
        let footSpread: CGFloat = female ? 0.035 : 0.045
        let leftFoot = point(c - footSpread, 0.91, in: size)
        let rightFoot = point(c + footSpread, 0.91, in: size)

        torso(&context, shoulder: shoulder, hip: hip, width: female ? 38 : 34)

        if !female {
            var robe = Path()
            robe.move(to: point(c - 0.095, 0.34, in: size))
            robe.addLine(to: point(c + 0.095, 0.34, in: size))
            robe.addLine(to: point(c + 0.105, 0.89, in: size))
            robe.addQuadCurve(
                to: point(c - 0.105, 0.89, in: size),
                control: point(c, 0.915, in: size)
            )
            robe.closeSubpath()
            context.fill(robe, with: .color(garmentColor.opacity(0.98)))
            context.stroke(robe, with: .color(garmentOutline), lineWidth: 3)
        }

        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.072)

        if female {
            line(&context, point(c - footSpread, 0.67, in: size), leftFoot, width: 14)
            line(&context, point(c + footSpread, 0.67, in: size), rightFoot, width: 14)
        } else {
            let footWidth = max(size.width * 0.048, 8)
            let footHeight = max(size.height * 0.025, 5)
            let y = size.height * 0.885
            let leftRect = CGRect(
                x: size.width * (c - 0.055) - footWidth / 2,
                y: y,
                width: footWidth,
                height: footHeight
            )
            let rightRect = CGRect(
                x: size.width * (c + 0.055) - footWidth / 2,
                y: y,
                width: footWidth,
                height: footHeight
            )
            context.fill(Path(roundedRect: leftRect, cornerRadius: footHeight / 2), with: .color(skinTone))
            context.fill(Path(roundedRect: rightRect, cornerRadius: footHeight / 2), with: .color(skinTone))
        }

        switch mode {
        case .takbir:
            let handY: CGFloat = female ? 0.29 : 0.22
            let leftHand = point(c - 0.17, handY, in: size)
            let rightHand = point(c + 0.17, handY, in: size)
            garmentPolyline(&context, [leftShoulder, point(c - 0.18, 0.28, in: size), leftHand], width: 11)
            garmentPolyline(&context, [rightShoulder, point(c + 0.18, 0.28, in: size), rightHand], width: 11)
            handDot(&context, center: leftHand, radius: 8)
            handDot(&context, center: rightHand, radius: 8)
        case .bound:
            let handY: CGFloat = female ? 0.47 : 0.56
            let leftHand = point(c + 0.02, handY, in: size)
            let rightHand = point(c - 0.02, handY, in: size)
            garmentPolyline(&context, [leftShoulder, point(c - 0.08, 0.48, in: size), leftHand], width: 10)
            garmentPolyline(&context, [rightShoulder, point(c + 0.08, 0.48, in: size), rightHand], width: 10)
            let handRect = CGRect(x: size.width * c - 18, y: size.height * handY - 7, width: 36, height: 14)
            context.fill(Path(roundedRect: handRect, cornerRadius: 7), with: .color(skinTone))
            context.stroke(Path(roundedRect: handRect, cornerRadius: 7), with: .color(SalahTheme.deepTeal.opacity(0.35)), lineWidth: 1)
        case .intention, .relaxed:
            let handY: CGFloat = 0.64
            let leftHand = point(c - 0.10, handY, in: size)
            let rightHand = point(c + 0.10, handY, in: size)
            garmentLine(&context, leftShoulder, leftHand, width: 10)
            garmentLine(&context, rightShoulder, rightHand, width: 10)
            handDot(&context, center: leftHand, radius: 6)
            handDot(&context, center: rightHand, radius: 6)
        }
    }

    private func drawBowing(_ context: inout GraphicsContext, size: CGSize) {
        let hip = point(female ? 0.43 : 0.40, 0.58, in: size)
        let shoulder = point(female ? 0.61 : 0.66, female ? 0.49 : 0.46, in: size)
        let headCenter = point(female ? 0.72 : 0.78, female ? 0.47 : 0.45, in: size)

        torso(&context, shoulder: shoulder, hip: hip, width: female ? 36 : 31)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.067)
        garmentLine(&context, point(0.38, 0.60, in: size), point(0.37, 0.90, in: size), width: 13)
        garmentLine(&context, point(0.46, 0.60, in: size), point(0.48, 0.90, in: size), width: 13)
        let leftHand = point(0.48, 0.69, in: size)
        let rightHand = point(0.49, 0.70, in: size)
        garmentPolyline(&context, [shoulder, point(0.58, 0.61, in: size), leftHand], width: 10)
        garmentPolyline(&context, [point(shoulder.x / size.width + 0.02, shoulder.y / size.height + 0.01, in: size), point(0.66, 0.62, in: size), rightHand], width: 10)
        handDot(&context, center: leftHand, radius: 6)
        handDot(&context, center: rightHand, radius: 6)
    }

    private func drawSujud(_ context: inout GraphicsContext, size: CGSize) {
        let knee = point(female ? 0.41 : 0.35, 0.73, in: size)
        let hip = point(female ? 0.46 : 0.43, female ? 0.58 : 0.52, in: size)
        let shoulder = point(female ? 0.61 : 0.62, female ? 0.69 : 0.65, in: size)
        let headCenter = point(female ? 0.72 : 0.76, 0.75, in: size)

        garmentPolyline(&context, [knee, hip, shoulder], width: female ? 34 : 30)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.062)
        garmentPolyline(&context, [knee, point(0.30, 0.82, in: size), point(0.24, 0.82, in: size)], width: 13)
        let leftHand = point(female ? 0.69 : 0.63, 0.83, in: size)
        let rightHand = point(female ? 0.73 : 0.78, 0.83, in: size)
        garmentPolyline(&context, [shoulder, point(female ? 0.66 : 0.58, 0.79, in: size), leftHand], width: 10)
        garmentPolyline(&context, [shoulder, point(female ? 0.70 : 0.72, 0.78, in: size), rightHand], width: 10)
        handDot(&context, center: leftHand, radius: 6)
        handDot(&context, center: rightHand, radius: 6)
        line(&context, point(0.67, 0.84, in: size), point(0.82, 0.84, in: size), width: 5, color: SalahTheme.gold)
    }

    private func drawSitting(_ context: inout GraphicsContext, size: CGSize, turn: Int, showFinger: Bool) {
        let hip = point(0.48, 0.62, in: size)
        let shoulder = point(0.48, 0.40, in: size)
        // Keep the whole body and head centered. For Salam only the facial
        // features indicate the head turn; the torso never appears to rotate.
        let headCenter = point(0.48, 0.27, in: size)

        torso(&context, shoulder: shoulder, hip: hip, width: female ? 37 : 31)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.068)
        garmentLine(&context, point(0.39, 0.42, in: size), point(0.39, 0.61, in: size), width: 10)
        garmentLine(&context, point(0.57, 0.42, in: size), point(0.57, 0.61, in: size), width: 10)
        line(&context, point(0.39, 0.60, in: size), point(0.53, 0.68, in: size), width: 9, color: skinTone)
        line(&context, point(0.57, 0.60, in: size), point(0.67, 0.68, in: size), width: 9, color: skinTone)

        if showFinger {
            // Hanafi tashahhud detail: the worshipper's right index finger.
            // Front-facing artwork means the worshipper's right is on the viewer's left.
            line(
                &context,
                point(0.39, 0.59, in: size),
                point(0.36, 0.51, in: size),
                width: 5,
                color: skinTone
            )
            let tip = CGRect(
                x: size.width * 0.36 - 4,
                y: size.height * 0.51 - 4,
                width: 8,
                height: 8
            )
            context.fill(Path(ellipseIn: tip), with: .color(SalahTheme.gold))
        }

        if female {
            garmentPolyline(&context, [hip, point(0.60, 0.70, in: size), point(0.74, 0.80, in: size)], width: 15)
            garmentPolyline(&context, [point(0.46, 0.65, in: size), point(0.57, 0.77, in: size), point(0.71, 0.84, in: size)], width: 15)
        } else {
            garmentPolyline(&context, [hip, point(0.40, 0.76, in: size), point(0.29, 0.84, in: size)], width: 14)
            garmentPolyline(&context, [point(0.51, 0.65, in: size), point(0.62, 0.78, in: size), point(0.72, 0.84, in: size)], width: 14)
        }

        // No body-direction arrow here: the worshipper remains facing Qibla.
        // PrayerPoseArtwork.drawFace shifts only the facial features for Salam.
    }
}

private struct ReferencePrayerPerson: View {
    let imageName: String
    let rugWidth: CGFloat
    let rugRotation: Double

    var body: some View {
        ZStack(alignment: .bottom) {
            GeometryReader { proxy in
                let w = min(rugWidth, proxy.size.width * 0.92)
                let h: CGFloat = 64

                Path { p in
                    p.move(to: CGPoint(x: (proxy.size.width - w) * 0.5 + 8, y: proxy.size.height - h))
                    p.addLine(to: CGPoint(x: (proxy.size.width + w) * 0.5 - 8, y: proxy.size.height - h))
                    p.addLine(to: CGPoint(x: (proxy.size.width + w) * 0.5, y: proxy.size.height))
                    p.addLine(to: CGPoint(x: (proxy.size.width - w) * 0.5, y: proxy.size.height))
                    p.closeSubpath()
                }
                .fill(SalahTheme.teal.opacity(0.88))
                .overlay {
                    Path { p in
                        p.move(to: CGPoint(x: (proxy.size.width - w) * 0.5 + 9, y: proxy.size.height - h + 5))
                        p.addLine(to: CGPoint(x: (proxy.size.width + w) * 0.5 - 9, y: proxy.size.height - h + 5))
                        p.addLine(to: CGPoint(x: (proxy.size.width + w) * 0.5 - 4, y: proxy.size.height - 6))
                        p.addLine(to: CGPoint(x: (proxy.size.width - w) * 0.5 + 4, y: proxy.size.height - 6))
                        p.closeSubpath()
                    }
                    .stroke(SalahTheme.gold.opacity(0.80), lineWidth: 1.2)
                }
                .rotationEffect(.degrees(rugRotation))
            }
            .frame(height: 78)

            PrayerPoseArtwork(assetName: imageName)
                .frame(maxWidth: .infinity, maxHeight: 230)
                .padding(.horizontal, 8)
                .padding(.bottom, 5)
        }
        .frame(maxWidth: .infinity, minHeight: 286, maxHeight: 286, alignment: .bottom)
    }
}

struct RakatOverviewView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section {
                ForEach(PrayerKind.allCases.filter { $0 != .sunrise }) { kind in
                    VStack(alignment: .leading, spacing: 7) {
                        HStack {
                            Label(kind.localizedName(settings.language), systemImage: kind.systemImage)
                                .font(.headline)
                            Spacer()
                            if let fard = kind.fardRakats {
                                Text("\(fard) \(settings.t("Fard", "farz"))")
                                    .font(.subheadline.bold())
                            }
                        }
                        Text(kind.fullSequence(settings.language))
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                        Text(kind.detailNote(settings.language))
                            .font(.caption)
                            .foregroundStyle(.tertiary)
                    }
                    .padding(.vertical, 5)
                }
            } header: {
                Text(settings.t("Tägliche Gebete", "Günlük namazlar"))
            } footer: {
                Text(settings.t(
                    "Die Übersicht folgt beim Sunnah-/Witr-Ablauf primär der hanafitischen Darstellung, wie sie auch in türkischen Diyanet-Lehrmaterialien üblich ist. Andere sunnitische Rechtsschulen unterscheiden sich in einzelnen Sunnah-Gebeten.",
                    "Sünnet ve vitir sıralaması öncelikle Diyanet öğretim materyallerinde de kullanılan Hanefî uygulamayı gösterir. Diğer Sünnî mezheplerde bazı sünnet namazlarda farklılıklar vardır."
                ))
            }

            Section(settings.t("Freitag / Jumuʿah", "Cuma")) {
                Text(settings.t(
                    "Jumuʿah hat 2 Rakʿat Fard in Gemeinschaft. Wer nicht am Jumuʿah teilnimmt, betet das normale Dhuhr mit 4 Rakʿat Fard. Die Sunnah-Zahl rund um Jumuʿah wird je nach Rechtsschule unterschiedlich dargestellt.",
                    "Cuma namazının cemaatle kılınan farzı 2 rekâttır. Cumaya katılmayan kişi normal öğle namazının 4 rekât farzını kılar. Cumanın öncesi ve sonrasındaki sünnet rekâtları mezheplere göre farklı anlatılabilir."
                ))
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Rakʿat", "Rekât"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Prayer guide

private enum PrayerPose: String {
    case intention, takbir, standing, bowing, upright, prostration, sitting, finalSitting, salam
}

private struct PrayerRecitation: Identifiable {
    let id = UUID()
    let deLabel: String
    let trLabel: String
    let arabic: String
    let transliteration: String
    let deMeaning: String
    let trMeaning: String
    let deNote: String?
    let trNote: String?
}

private struct PrayerTutorialStep: Identifiable {
    let id = UUID()
    let number: String
    let pose: PrayerPose
    let imageKey: String?
    let deTitle: String
    let trTitle: String
    let deAction: String
    let trAction: String
    let deHanafi: String?
    let trHanafi: String?
    let recitations: [PrayerRecitation]
}

private enum PrayerText {
    static let takbir = PrayerRecitation(
        deLabel: "Beim Beginn / beim Übergang", trLabel: "Başlarken / geçişte",
        arabic: "اللّٰهُ أَكْبَرُ", transliteration: "Allāhu akbar",
        deMeaning: "Allah ist größer / der Größte.", trMeaning: "Allah en büyüktür.",
        deNote: nil, trNote: nil)

    static let subhanaka = PrayerRecitation(
        deLabel: "Sübhaneke", trLabel: "Sübhâneke",
        arabic: "سُبْحَانَكَ اللَّهُمَّ وَبِحَمْدِكَ وَتَبَارَكَ اسْمُكَ وَتَعَالَى جَدُّكَ وَلَا إِلٰهَ غَيْرُكَ",
        transliteration: "Sübhâneke Allâhümme ve bi hamdik. Ve tebârekesmük. Ve teâlâ ceddük. Ve lâ ilâhe ğayrük.",
        deMeaning: "Gepriesen bist Du, o Allah, und Dir gebührt Lob. Gesegnet ist Dein Name, erhaben ist Deine Majestät, und es gibt keinen Gott außer Dir.",
        trMeaning: "Allah'ım! Sen eksik sıfatlardan uzaksın. Seni överim. Senin adın mübarektir, şanın yücedir. Senden başka ilâh yoktur.",
        deNote: "Im ersten Rakʿah nach dem Eröffnungstakbir.", trNote: "İlk rekâtta iftitah tekbirinden sonra.")

    static let audhu = PrayerRecitation(
        deLabel: "Eʿūḏu", trLabel: "Eûzü",
        arabic: "أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ", transliteration: "Eʿûzü billâhi mineş-şeytânirracîm",
        deMeaning: "Ich suche Zuflucht bei Allah vor dem verfluchten Satan.", trMeaning: "Kovulmuş şeytandan Allah'a sığınırım.",
        deNote: "Im ersten Rakʿah vor der Fātiha.", trNote: "İlk rekâtta Fâtiha'dan önce.")

    static let basmala = PrayerRecitation(
        deLabel: "Basmala", trLabel: "Besmele",
        arabic: "بِسْمِ اللَّهِ الرَّحْمٰنِ الرَّحِيمِ", transliteration: "Bismillâhirrahmânirrahîm",
        deMeaning: "Im Namen Allahs, des Allerbarmers, des Barmherzigen.", trMeaning: "Rahmân ve Rahîm olan Allah'ın adıyla.",
        deNote: nil, trNote: nil)

    static let fatiha = PrayerRecitation(
        deLabel: "Al-Fātiha", trLabel: "Fâtiha Sûresi",
        arabic: "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\nالرَّحْمٰنِ الرَّحِيمِ\nمَالِكِ يَوْمِ الدِّينِ\nإِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ\nاهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ\nصِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
        transliteration: "Elhamdülillâhi rabbil âlemîn. Errahmânirrahîm. Mâliki yevmiddîn. İyyâke na'büdü ve iyyâke neste'în. İhdinessırâtal müstakîm. Sırâtallezîne en'amte aleyhim ğayril mağdûbi aleyhim ve leddâllîn. Âmîn.",
        deMeaning: "Die eröffnende Sura. Beim Gebet allein oder als Imam wird al-Fātiha in jedem Rakʿah rezitiert; nach ihrem Ende sagt man Âmîn.",
        trMeaning: "Açılış sûresi. Yalnız kılarken veya imam olarak her rekâtta Fâtiha okunur; sonunda Âmin denir.",
        deNote: "Hanafi: Wer einem Imam folgt, rezitiert Fātiha und Zusatzsura nicht selbst. Wortlaut und Audio findest du zusätzlich im Quran-Bereich.", trNote: "Hanefî: İmama uyan kişi Fâtiha ve zamm-ı sûreyi kendisi okumaz. Metin ve ses ayrıca Kur'an bölümündedir.")

    static let ikhlas = PrayerRecitation(
        deLabel: "Beispiel Zusatzsura: Al-Ikhlāṣ", trLabel: "Örnek zamm-ı sûre: İhlâs",
        arabic: "قُلْ هُوَ اللَّهُ أَحَدٌ\nاللَّهُ الصَّمَدُ\nلَمْ يَلِدْ وَلَمْ يُولَدْ\nوَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ",
        transliteration: "Kul hüvallâhü ehad. Allâhüssamed. Lem yelid ve lem yûled. Ve lem yekün lehû küfüven ehad.",
        deMeaning: "Sprich: Er ist Allah, der Eine …", trMeaning: "De ki: O Allah birdir …",
        deNote: "Nur ein Beispiel. Eine andere passende Sura oder Quranverse sind ebenfalls möglich.", trNote: "Sadece örnektir. Başka uygun bir sûre veya ayetler de okunabilir.")

    static let ruku = PrayerRecitation(
        deLabel: "Im Rukūʿ", trLabel: "Rükûda",
        arabic: "سُبْحَانَ رَبِّيَ الْعَظِيمِ", transliteration: "Sübhâne rabbiyel-azîm (3×)",
        deMeaning: "Gepriesen sei mein gewaltiger Herr.", trMeaning: "Yüce Rabbimi noksan sıfatlardan tenzih ederim.", deNote: nil, trNote: nil)

    static let rising = PrayerRecitation(
        deLabel: "Beim Aufrichten", trLabel: "Doğrulurken",
        arabic: "سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ", transliteration: "Semi'allāhu limen hamideh",
        deMeaning: "Allah hört den, der Ihn lobt.", trMeaning: "Allah kendisine hamd edeni işitir.",
        deNote: "Hanafi: Imam und allein Betender sagen dies beim Aufrichten.", trNote: "Hanefî: İmam ve yalnız kılan doğrulurken bunu söyler.")

    static let upright = PrayerRecitation(
        deLabel: "Vollständig aufgerichtet", trLabel: "Tam doğrulunca",
        arabic: "رَبَّنَا لَكَ الْحَمْدُ", transliteration: "Rabbenâ lekel-hamd",
        deMeaning: "Unser Herr, Dir gebührt das Lob.", trMeaning: "Rabbimiz, hamd Sana mahsustur.",
        deNote: "Hanafi: Der Mitbetende hinter dem Imam sagt dies; der allein Betende ebenfalls nach dem Aufrichten.", trNote: "Hanefî: İmama uyan bunu söyler; yalnız kılan da doğrulunca söyler.")

    static let sujud = PrayerRecitation(
        deLabel: "In der Secde", trLabel: "Secdede",
        arabic: "سُبْحَانَ رَبِّيَ الْأَعْلَى", transliteration: "Sübhâne rabbiyel-a'lâ (3×)",
        deMeaning: "Gepriesen sei mein höchster Herr.", trMeaning: "Yüce Rabbimi noksan sıfatlardan tenzih ederim.", deNote: nil, trNote: nil)

    static let rabbighfirli = PrayerRecitation(
        deLabel: "Mögliche Dua zwischen den Secden", trLabel: "İki secde arasında okunabilecek dua",
        arabic: "رَبِّ اغْفِرْ لِي", transliteration: "Rabbighfir lī",
        deMeaning: "Mein Herr, vergib mir.", trMeaning: "Rabbim, beni bağışla.",
        deNote: "Keine Pflichtformel; die kurze ruhige Sitzphase selbst soll nicht ausgelassen werden.", trNote: "Zorunlu bir söz değildir; kısa ve sakin oturuş atlanmamalıdır.")

    static let tahiyyat = PrayerRecitation(
        deLabel: "Ettehiyyâtü / Tashahhud", trLabel: "Ettehiyyâtü / Tahiyyat",
        arabic: "التَّحِيَّاتُ لِلَّهِ وَالصَّلَوَاتُ وَالطَّيِّبَاتُ، السَّلَامُ عَلَيْكَ أَيُّهَا النَّبِيُّ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ، السَّلَامُ عَلَيْنَا وَعَلَى عِبَادِ اللَّهِ الصَّالِحِينَ، أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللَّهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ",
        transliteration: "Ettehiyyâtü lillâhi vessalevâtü vettayyibât. Esselâmü aleyke eyyühen-nebiyyü ve rahmetullâhi ve berekâtüh. Esselâmü aleynâ ve alâ ibâdillâhis-sâlihîn. Eşhedü en lâ ilâhe illallâh ve eşhedü enne Muhammeden abdühû ve resûlüh.",
        deMeaning: "Die Grüße, Gebete und guten Dinge gehören Allah … Ich bezeuge, dass es keinen Gott außer Allah gibt und dass Muhammad Sein Diener und Gesandter ist.",
        trMeaning: "Bütün hürmetler, dualar ve güzel sözler Allah'a mahsustur … Allah'tan başka ilâh olmadığına ve Muhammed'in O'nun kulu ve elçisi olduğuna şahitlik ederim.", deNote: nil, trNote: nil)

    static let salli = PrayerRecitation(
        deLabel: "Allahümme Salli", trLabel: "Allâhümme Salli",
        arabic: "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ مَجِيدٌ",
        transliteration: "Allâhümme salli alâ Muhammedin ve alâ âli Muhammed. Kemâ salleyte alâ İbrâhîme ve alâ âli İbrâhîm. İnneke hamîdün mecîd.",
        deMeaning: "O Allah, segne Muhammad und die Familie Muhammads, wie Du Ibrahim und die Familie Ibrahims gesegnet hast. Du bist der Lobenswerte, der Ruhmreiche.",
        trMeaning: "Allah'ım, İbrahim'e ve ailesine rahmet ettiğin gibi Muhammed'e ve ailesine de rahmet et. Şüphesiz Sen övülmeye lâyık ve şan sahibisin.", deNote: nil, trNote: nil)

    static let barik = PrayerRecitation(
        deLabel: "Allahümme Bârik", trLabel: "Allâhümme Bârik",
        arabic: "اللَّهُمَّ بَارِكْ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا بَارَكْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ مَجِيدٌ",
        transliteration: "Allâhümme bârik alâ Muhammedin ve alâ âli Muhammed. Kemâ bârekte alâ İbrâhîme ve alâ âli İbrâhîm. İnneke hamîdün mecîd.",
        deMeaning: "O Allah, schenke Muhammad und der Familie Muhammads Segen, wie Du Ibrahim und der Familie Ibrahims Segen geschenkt hast.",
        trMeaning: "Allah'ım, İbrahim'e ve ailesine bereket verdiğin gibi Muhammed'e ve ailesine de bereket ver.", deNote: nil, trNote: nil)

    static let rabbana = PrayerRecitation(
        deLabel: "Rabbenâ Âtinâ", trLabel: "Rabbenâ Âtinâ",
        arabic: "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
        transliteration: "Rabbenâ âtinâ fid-dünyâ haseneten ve fil-âhireti haseneten ve kınâ azâben-nâr.",
        deMeaning: "Unser Herr, gib uns Gutes im Diesseits und Gutes im Jenseits und bewahre uns vor der Strafe des Feuers.",
        trMeaning: "Rabbimiz, bize dünyada da iyilik, ahirette de iyilik ver ve bizi ateş azabından koru.", deNote: "Quran 2:201", trNote: "Kur'an 2:201")

    static let salam = PrayerRecitation(
        deLabel: "Rechts und anschließend links", trLabel: "Önce sağa, sonra sola",
        arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ", transliteration: "Es-selâmü aleyküm ve rahmetullâh",
        deMeaning: "Friede und Allahs Barmherzigkeit seien mit euch.", trMeaning: "Allah'ın selâmı ve rahmeti üzerinize olsun.",
        deNote: "Den Satz einmal beim Drehen nach rechts und danach erneut beim Drehen nach links sprechen.", trNote: "Cümleyi önce sağa dönerken, sonra sola dönerken tekrar söyle.")
}

struct PrayerHowToView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var currentStepIndex: Int

    init(initialStepIndex: Int = 0) {
        _currentStepIndex = State(initialValue: min(max(initialStepIndex, 0), 17))
    }

    private var safeCurrentStepIndex: Int {
        min(max(currentStepIndex, 0), max(steps.count - 1, 0))
    }

    private var steps: [PrayerTutorialStep] {
        [
            .init(
                number: "1",
                pose: .intention,
                imageKey: "intention",
                deTitle: "Niyyah – Absicht",
                trTitle: "Niyet",
                deAction: "Stehe sauber bedeckt und zur Qibla. Fasse im Herzen die Absicht für genau das Gebet, das du jetzt betest. Eine bestimmte gesprochene Niyyah-Formel ist nicht erforderlich.",
                trAction: "Temiz ve örtülü şekilde kıbleye dön. Kılacağın namaza kalben niyet et. Niyeti belirli bir cümleyle sesli söylemek şart değildir.",
                deHanafi: nil,
                trHanafi: nil,
                recitations: []
            ),
            .init(
                number: "2",
                pose: .takbir,
                imageKey: "takbir",
                deTitle: "Eröffnungstakbir",
                trTitle: "İftitah tekbiri",
                deAction: "Heb beide Hände an und sage einmal Allāhu akbar. Danach bindest du die Hände für den Qiyām.",
                trAction: "İki eli kaldır, bir kez Allāhu ekber de. Sonra kıyam için elleri bağla.",
                deHanafi: settings.prayerAudience == .male ? "Hanafi Mann: Daumen etwa auf Höhe der Ohrläppchen." : "Hanafi Frau: Fingerspitzen etwa bis Schulterhöhe.",
                trHanafi: settings.prayerAudience == .male ? "Hanefî erkek: Başparmaklar yaklaşık kulak memesi hizasında." : "Hanefî kadın: Parmak uçları yaklaşık omuz hizasına kadar.",
                recitations: [.init(deLabel: "Einmal", trLabel: "Bir kez", arabic: PrayerText.takbir.arabic, transliteration: PrayerText.takbir.transliteration, deMeaning: PrayerText.takbir.deMeaning, trMeaning: PrayerText.takbir.trMeaning, deNote: nil, trNote: nil)]
            ),
            .init(
                number: "3",
                pose: .standing,
                imageKey: "standing",
                deTitle: "Qiyām – 1. Rakʿah",
                trTitle: "Kıyam – 1. rekât",
                deAction: "Stehe ruhig mit gebundenen Händen und schaue zum Ort der Niederwerfung. Im ersten Rakʿah liest du Sübhaneke, danach Eʿūḏu, Basmala, al-Fātiha, Âmîn und anschließend eine zusätzliche Sura oder passende Verse.",
                trAction: "Eller bağlı şekilde sakin dur ve secde edeceğin yere bak. İlk rekâtta Sübhâneke, ardından Eûzü, Besmele, Fâtiha, Âmin ve sonra zamm-ı sûre veya uygun ayetler okunur.",
                deHanafi: (settings.prayerAudience == .male ? "Mann: rechte Hand über die linke unterhalb des Nabels; rechte Hand umfasst das linke Handgelenk." : "Frau: rechte Hand über die linke auf der Brust; Handgelenk nicht wie beim Mann umfassen.") + " Hinter einem Imam werden Fātiha und Zusatzsura nicht selbst rezitiert.",
                trHanafi: (settings.prayerAudience == .male ? "Erkek: sağ el sol elin üzerinde, göbek altında; sağ el sol bileği kavrar." : "Kadın: sağ el sol elin üzerinde göğüs üstünde; bilek erkeklerdeki gibi kavranmaz.") + " İmama uyarken Fâtiha ve zamm-ı sûre ayrıca okunmaz.",
                recitations: [PrayerText.subhanaka, PrayerText.audhu, PrayerText.basmala, PrayerText.fatiha, PrayerText.ikhlas]
            ),
            .init(
                number: "4",
                pose: .bowing,
                imageKey: "bowing",
                deTitle: "Rukūʿ – 1. Rakʿah",
                trTitle: "Rükû – 1. rekât",
                deAction: "Sage beim Hinuntergehen Allāhu akbar. Beuge dich und halte die Position kurz ruhig. Sprich danach den Rukūʿ-Dhikr dreimal.",
                trAction: "Rükûya giderken Allāhu ekber de. Rükûda kısa bir an sakin dur. Sonra rükû tesbihini üç kez söyle.",
                deHanafi: settings.prayerAudience == .male ? "Mann: Rücken möglichst gerade, Hände auf den Knien, Knie gestreckt." : "Frau: kompaktere Haltung; Rücken weniger waagerecht, Hände auf den Knien, Knie etwas gebeugt.",
                trHanafi: settings.prayerAudience == .male ? "Erkek: sırt mümkün olduğunca düz, eller dizlerde, dizler dik." : "Kadın: daha toplu duruş; sırt daha az yatay, eller dizlerde, dizler biraz bükülü.",
                recitations: [PrayerText.takbir, PrayerText.ruku]
            ),
            .init(
                number: "5",
                pose: .upright,
                imageKey: "upright",
                deTitle: "Aufrichten – 1. Rakʿah",
                trTitle: "Doğrulma – 1. rekât",
                deAction: "Richte dich vollständig aus dem Rukūʿ auf. Stehe kurz ganz ruhig, bevor du in die Secde gehst.",
                trAction: "Rükûdan tamamen doğrul. Secdeye gitmeden önce kısa bir an tamamen dik ve sakin dur.",
                deHanafi: "Allein/Imam: beim Hochkommen Semi'allāhu limen hamideh; vollständig stehend Rabbenâ lekel-hamd. Hinter dem Imam: Rabbenâ lekel-hamd.",
                trHanafi: "Yalnız/İmam: doğrulurken Semi'allāhu limen hamideh; tam doğrulunca Rabbenâ lekel-hamd. İmama uyan: Rabbenâ lekel-hamd.",
                recitations: [PrayerText.rising, PrayerText.upright]
            ),
            .init(
                number: "6",
                pose: .prostration,
                imageKey: "sujud",
                deTitle: "Erste Secde – 1. Rakʿah",
                trTitle: "Birinci secde – 1. rekât",
                deAction: "Sage Allāhu akbar und gehe in die Niederwerfung. Stirn und Nase liegen auf; die Hände stehen neben dem Kopf. Bleibe ruhig und sprich den Secde-Dhikr dreimal.",
                trAction: "Allāhu ekber diyerek secdeye git. Alın ve burun yere gelir; eller başın yanında olur. Sakin dur ve secde tesbihini üç kez söyle.",
                deHanafi: settings.prayerAudience == .male ? "Mann: Unterarme vom Boden und Arme vom Körper fernhalten, sofern ohne Mühe möglich." : "Frau: Arme näher am Körper, Bauch näher an den Oberschenkeln; kompaktere Haltung.",
                trHanafi: settings.prayerAudience == .male ? "Erkek: mümkünse dirsekleri yere koymaz, kolları gövdeden açık tutar." : "Kadın: kollar gövdeye, karın uyluklara daha yakın; daha toplu duruş.",
                recitations: [PrayerText.takbir, PrayerText.sujud]
            ),
            .init(
                number: "7",
                pose: .sitting,
                imageKey: "sitting",
                deTitle: "Sitzen zwischen den Secden",
                trTitle: "İki secde arası oturuş",
                deAction: "Sage Allāhu akbar und setze dich vollständig auf. Bleibe kurz ruhig sitzen. Erst danach gehst du in die zweite Secde.",
                trAction: "Allāhu ekber diyerek tamamen otur. Kısa bir an sakin otur. Ancak sonra ikinci secdeye git.",
                deHanafi: settings.prayerAudience == .male ? "Mann: auf dem linken Fuß sitzen; rechter Fuß aufgestellt, Zehen Richtung Qibla." : "Frau: beide Füße zur rechten Seite herausnehmen und auf dem Boden sitzen.",
                trHanafi: settings.prayerAudience == .male ? "Erkek: sol ayak üzerine oturur; sağ ayak dik, parmaklar kıbleye yönelir." : "Kadın: iki ayağını sağ tarafa çıkararak yere oturur.",
                recitations: [PrayerText.takbir, PrayerText.rabbighfirli]
            ),
            .init(
                number: "8",
                pose: .prostration,
                imageKey: "second_sujud",
                deTitle: "Zweite Secde – 1. Rakʿah",
                trTitle: "İkinci secde – 1. rekât",
                deAction: "Sage Allāhu akbar, gehe erneut in die Secde und sprich den Dhikr dreimal. Damit ist die erste Rakʿah beendet.",
                trAction: "Allāhu ekber diyerek tekrar secdeye git ve tesbihi üç kez söyle. Böylece birinci rekât tamamlanır.",
                deHanafi: nil,
                trHanafi: nil,
                recitations: [PrayerText.takbir, PrayerText.sujud]
            ),
            .init(
                number: "9",
                pose: .standing,
                imageKey: "standing",
                deTitle: "Aufstehen zum 2. Rakʿah",
                trTitle: "2. rekâta kalkış",
                deAction: "Nach der zweiten Secde stehst du mit Allāhu akbar zum zweiten Rakʿah auf. Richte dich vollständig auf und binde die Hände wieder wie zuvor.",
                trAction: "İkinci secdeden sonra Allāhu ekber diyerek ikinci rekâta kalk. Tamamen doğrul ve ellerini önceki gibi yeniden bağla.",
                deHanafi: nil,
                trHanafi: nil,
                recitations: [PrayerText.takbir]
            ),
            .init(
                number: "10",
                pose: .standing,
                imageKey: "standing",
                deTitle: "Qiyām – 2. Rakʿah",
                trTitle: "Kıyam – 2. rekât",
                deAction: "Im zweiten Rakʿah liest du nicht noch einmal Sübhaneke und Eʿūḏu. Beginne mit der Basmala, lies al-Fātiha, sage Âmîn und lies anschließend eine zusätzliche Sura oder passende Verse.",
                trAction: "İkinci rekâtta Sübhâneke ve Eûzü yeniden okunmaz. Besmele ile başla, Fâtiha'yı oku, Âmin de ve ardından zamm-ı sûre veya uygun ayetler oku.",
                deHanafi: nil,
                trHanafi: nil,
                recitations: [PrayerText.basmala, PrayerText.fatiha, PrayerText.ikhlas]
            ),
            .init(
                number: "11",
                pose: .bowing,
                imageKey: "bowing",
                deTitle: "Rukūʿ – 2. Rakʿah",
                trTitle: "Rükû – 2. rekât",
                deAction: "Sage Allāhu akbar, gehe wieder in den Rukūʿ und bleibe kurz ruhig. Sprich den Rukūʿ-Dhikr dreimal.",
                trAction: "Allāhu ekber diyerek tekrar rükûya git ve kısa bir an sakin dur. Rükû tesbihini üç kez söyle.",
                deHanafi: settings.prayerAudience == .male ? "Mann: Rücken möglichst gerade, Hände auf den Knien, Knie gestreckt." : "Frau: kompaktere Haltung; Rücken weniger waagerecht, Hände auf den Knien, Knie etwas gebeugt.",
                trHanafi: settings.prayerAudience == .male ? "Erkek: sırt mümkün olduğunca düz, eller dizlerde, dizler dik." : "Kadın: daha toplu duruş; sırt daha az yatay, eller dizlerde, dizler biraz bükülü.",
                recitations: [PrayerText.takbir, PrayerText.ruku]
            ),
            .init(
                number: "12",
                pose: .upright,
                imageKey: "upright",
                deTitle: "Aufrichten – 2. Rakʿah",
                trTitle: "Doğrulma – 2. rekât",
                deAction: "Richte dich wieder vollständig aus dem Rukūʿ auf und bleibe kurz ruhig stehen, bevor du zur Secde gehst.",
                trAction: "Rükûdan yeniden tamamen doğrul ve secdeye gitmeden önce kısa bir an sakin dur.",
                deHanafi: "Allein/Imam: beim Hochkommen Semi'allāhu limen hamideh; vollständig stehend Rabbenâ lekel-hamd. Hinter dem Imam: Rabbenâ lekel-hamd.",
                trHanafi: "Yalnız/İmam: doğrulurken Semi'allāhu limen hamideh; tam doğrulunca Rabbenâ lekel-hamd. İmama uyan: Rabbenâ lekel-hamd.",
                recitations: [PrayerText.rising, PrayerText.upright]
            ),
            .init(
                number: "13",
                pose: .prostration,
                imageKey: "sujud",
                deTitle: "Erste Secde – 2. Rakʿah",
                trTitle: "Birinci secde – 2. rekât",
                deAction: "Sage Allāhu akbar und gehe wieder in die erste Secde. Bleibe ruhig und sprich den Secde-Dhikr dreimal.",
                trAction: "Allāhu ekber diyerek yeniden birinci secdeye git. Sakin dur ve secde tesbihini üç kez söyle.",
                deHanafi: settings.prayerAudience == .male ? "Mann: Unterarme vom Boden und Arme vom Körper fernhalten, sofern ohne Mühe möglich." : "Frau: Arme näher am Körper, Bauch näher an den Oberschenkeln; kompaktere Haltung.",
                trHanafi: settings.prayerAudience == .male ? "Erkek: mümkünse dirsekleri yere koymaz, kolları gövdeden açık tutar." : "Kadın: kollar gövdeye, karın uyluklara daha yakın; daha toplu duruş.",
                recitations: [PrayerText.takbir, PrayerText.sujud]
            ),
            .init(
                number: "14",
                pose: .sitting,
                imageKey: "sitting",
                deTitle: "Sitzen zwischen den Secden – 2. Rakʿah",
                trTitle: "İki secde arası – 2. rekât",
                deAction: "Sage Allāhu akbar und setze dich vollständig auf. Bleibe kurz ruhig sitzen. Danach gehst du in die zweite Secde.",
                trAction: "Allāhu ekber diyerek tamamen otur. Kısa bir an sakin otur. Ardından ikinci secdeye git.",
                deHanafi: settings.prayerAudience == .male ? "Mann: auf dem linken Fuß sitzen; rechter Fuß aufgestellt, Zehen Richtung Qibla." : "Frau: beide Füße zur rechten Seite herausnehmen und auf dem Boden sitzen.",
                trHanafi: settings.prayerAudience == .male ? "Erkek: sol ayak üzerine oturur; sağ ayak dik, parmaklar kıbleye yönelir." : "Kadın: iki ayağını sağ tarafa çıkararak yere oturur.",
                recitations: [PrayerText.takbir, PrayerText.rabbighfirli]
            ),
            .init(
                number: "15",
                pose: .prostration,
                imageKey: "second_sujud",
                deTitle: "Zweite Secde – 2. Rakʿah",
                trTitle: "İkinci secde – 2. rekât",
                deAction: "Sage Allāhu akbar und gehe in die zweite Secde. Sprich den Secde-Dhikr dreimal. Danach ist auch die zweite Rakʿah beendet.",
                trAction: "Allāhu ekber diyerek ikinci secdeye git. Secde tesbihini üç kez söyle. Böylece ikinci rekât da tamamlanır.",
                deHanafi: nil,
                trHanafi: nil,
                recitations: [PrayerText.takbir, PrayerText.sujud]
            ),
            .init(
                number: "16",
                pose: .finalSitting,
                imageKey: "final_sitting",
                deTitle: "Sitzen nach dem 2. Rakʿah",
                trTitle: "2. rekâttan sonra oturuş",
                deAction: "Bleibe nach der zweiten Secde sitzen. Endet dein Gebet nach zwei Rakʿah, ist dies das vollständige Schluss-Sitzen: Ettehiyyâtü, danach Allahümme Salli, Allahümme Bârik und eine Abschlussdua wie Rabbenâ Âtinâ. Bei einem 3-/4-Rakʿah-Fard liest du hier Ettehiyyâtü und stehst anschließend mit Allāhu akbar zur nächsten Rakʿah auf.",
                trAction: "İkinci secdeden sonra oturmaya devam et. Namazın iki rekâtta bitiyorsa bu son oturuştur: Ettehiyyâtü, ardından Allâhümme Salli, Allâhümme Bârik ve Rabbenâ Âtinâ gibi bir dua okunur. 3/4 rekât farz devam ediyorsa burada Ettehiyyâtü okunur ve sonra Allāhu ekber diyerek sonraki rekâta kalkılır.",
                deHanafi: "Die folgenden Schritte 17 und 18 beenden ein Gebet, das an dieser Stelle endet.",
                trHanafi: "Aşağıdaki 17. ve 18. adımlar burada biten namazı selâmla tamamlar.",
                recitations: [PrayerText.tahiyyat, PrayerText.salli, PrayerText.barik, PrayerText.rabbana]
            ),
            .init(
                number: "17",
                pose: .finalSitting,
                imageKey: "salam_right",
                deTitle: "Salām – zuerst rechts",
                trTitle: "Selâm – önce sağa",
                deAction: "Der Oberkörper bleibt nach vorn. Drehe nur Kopf und Gesicht zu deiner EIGENEN rechten Schulter und sprich den Salām einmal.",
                trAction: "Gövde önde kalır. Yalnız başını ve yüzünü KENDİ sağ omzuna çevir ve selâmı bir kez söyle.",
                deHanafi: "Zuerst rechts. Danach folgt Schritt 18 nach links.",
                trHanafi: "Önce sağa. Ardından 18. adımda sola dönülür.",
                recitations: [PrayerText.salam]
            ),
            .init(
                number: "18",
                pose: .finalSitting,
                imageKey: "salam_left",
                deTitle: "Salām – danach links",
                trTitle: "Selâm – sonra sola",
                deAction: "Kehre über die Mitte zurück und drehe Kopf und Gesicht zu deiner EIGENEN linken Schulter. Sprich denselben Salām erneut. Damit ist das Gebet beendet.",
                trAction: "Ortadan geçerek başını ve yüzünü KENDİ sol omzuna çevir. Aynı selâmı tekrar söyle. Böylece namaz tamamlanır.",
                deHanafi: "Reihenfolge: rechts, dann links.",
                trHanafi: "Sıra: önce sağ, sonra sol.",
                recitations: [PrayerText.salam]
            )
        ]
    }

    private var prayerLearningHero: some View {
        VStack(spacing: 12) {
            Picker(settings.t("Lernmodus", "Öğrenme modu"), selection: $settings.prayerAudience) {
                Text(settings.t("Mann", "Erkek")).tag(PrayerAudience.male)
                Text(settings.t("Frau", "Kadın")).tag(PrayerAudience.female)
            }
            .pickerStyle(.segmented)

            HStack(spacing: 14) {
                PrayerPoseArtwork(assetName: settings.prayerAudience == .male ? "male_intention" : "female_intention")
                    .frame(width: 104, height: 132)
                    .background(SalahTheme.cream)
                    .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))

                VStack(alignment: .leading, spacing: 8) {
                    Text(settings.t("Ganz von vorne lernen", "En baştan öğren"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Du siehst immer nur einen Schritt. Lies ihn in Ruhe, schau dir die Haltung an und tippe erst dann auf Weiter.",
                        "Her seferinde yalnız bir adım görürsün. Sakin şekilde oku, duruşa bak ve sonra İleri'ye dokun."
                    ))
                    .font(.subheadline)
                    .foregroundStyle(SalahTheme.ink)
                    .fixedSize(horizontal: false, vertical: true)
                }
                Spacer(minLength: 0)
            }

            VStack(alignment: .leading, spacing: 7) {
                learningFeature(settings.t("Eine Haltung pro Schritt", "Her adımda tek duruş"), icon: "checkmark.circle.fill")
                learningFeature(settings.t("Arabisch, Umschrift und Bedeutung", "Arapça, okunuş ve anlam"), icon: "checkmark.circle.fill")
                learningFeature(settings.t("Mann/Frau getrennt dargestellt", "Erkek/Kadın ayrı gösterilir"), icon: "checkmark.circle.fill")
                learningFeature(settings.t("Hanafi/Diyanet-Grunddarstellung", "Hanefî/Diyanet temel anlatımı"), icon: "checkmark.circle.fill")
            }
        }
        .padding(13)
        .background(
            LinearGradient(
                colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.72)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            ),
            in: RoundedRectangle(cornerRadius: 18, style: .continuous)
        )
        .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.52), lineWidth: 1) }
    }

    private func learningFeature(_ text: String, icon: String) -> some View {
        HStack(spacing: 8) {
            Image(systemName: icon)
                .font(.system(size: 13, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
            Text(text)
                .font(.system(size: 11, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer(minLength: 0)
        }
    }

    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(spacing: 14) {
                    Color.clear.frame(height: 1).id("prayer-step-top")
                    prayerLearningHero

                    NavigationLink { HanafiPrayerPlanView() } label: {
                        HStack {
                            Label(settings.t("Rak'a einfach verstehen", "Rekâtı kolayca anla"), systemImage: "list.number")
                                .font(.headline)
                            Spacer()
                            Image(systemName: "chevron.right")
                        }
                        .cardStyle()
                    }
                    .buttonStyle(.plain)

                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text("0")
                                .font(.headline.bold())
                                .frame(width: 34, height: 34)
                                .background(SalahTheme.gold.opacity(0.22), in: Circle())
                            Text(settings.t("Bevor du anfängst", "Başlamadan önce"))
                                .font(.title3.bold())
                        }
                        Text(settings.t(
                            "Prüfe: Die Gebetszeit hat begonnen, du hast Wudu, dein Körper, deine Kleidung und dein Gebetsplatz sind sauber, die vorgeschriebenen Körperstellen sind bedeckt und du stehst zur Qibla. Danach gehst du Schritt für Schritt weiter.",
                            "Kontrol et: Namaz vakti girmiş olsun, abdestli ol, bedenin, elbisen ve namaz yerin temiz olsun, örtülmesi gereken yerler örtülü olsun ve kıbleye dön. Sonra adım adım ilerle."
                        ))
                        .font(.subheadline)
                        .fixedSize(horizontal: false, vertical: true)
                    }
                    .cardStyle()

                    VStack(spacing: 8) {
                        HStack {
                            Text(settings.t("Schritt", "Adım") + " \(currentStepIndex + 1) / \(steps.count)")
                                .font(.headline.bold())
                                .foregroundStyle(SalahTheme.deepTeal)
                            Spacer()
                            Text(settings.prayerAudience.title(settings.language))
                                .font(.caption.bold())
                                .padding(.horizontal, 9)
                                .padding(.vertical, 5)
                                .background(SalahTheme.softTeal, in: Capsule())
                        }
                        ProgressView(value: Double(currentStepIndex + 1), total: Double(steps.count))
                            .tint(SalahTheme.teal)
                    }
                    .padding(12)
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                    .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }

                    PrayerTutorialStepCard(step: steps[safeCurrentStepIndex], audience: settings.prayerAudience)
                        .id("prayer-step-card-\(currentStepIndex)")

                    HStack(spacing: 12) {
                        Button {
                            guard currentStepIndex > 0 else { return }
                            let target = currentStepIndex - 1
                            withAnimation(.easeInOut(duration: 0.2)) {
                                currentStepIndex = target
                            }
                            Task { @MainActor in
                                await Task.yield()
                                withAnimation(.easeInOut(duration: 0.2)) {
                                    proxy.scrollTo("prayer-step-card-\(target)", anchor: .top)
                                }
                            }
                        } label: {
                            Label(settings.t("Zurück", "Geri"), systemImage: "chevron.left")
                                .font(.headline.bold())
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 13)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(currentStepIndex > 0 ? SalahTheme.deepTeal : SalahTheme.mutedInk.opacity(0.45))
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }
                        .disabled(currentStepIndex == 0)

                        Button {
                            guard currentStepIndex < steps.count - 1 else { return }
                            let target = currentStepIndex + 1
                            withAnimation(.easeInOut(duration: 0.2)) {
                                currentStepIndex = target
                            }
                            Task { @MainActor in
                                await Task.yield()
                                withAnimation(.easeInOut(duration: 0.2)) {
                                    proxy.scrollTo("prayer-step-card-\(target)", anchor: .top)
                                }
                            }
                        } label: {
                            HStack {
                                Text(currentStepIndex == steps.count - 1 ? settings.t("Fertig", "Bitti") : settings.t("Weiter", "İleri"))
                                Image(systemName: currentStepIndex == steps.count - 1 ? "checkmark" : "chevron.right")
                            }
                            .font(.headline.bold())
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 13)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(.white)
                        .background(currentStepIndex == steps.count - 1 ? SalahTheme.mutedInk : SalahTheme.deepTeal, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .disabled(currentStepIndex == steps.count - 1)
                    }

                    VStack(alignment: .leading, spacing: 8) {
                        Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama")).font(.headline)
                        Text(settings.t(
                            "Die Gebetsreihenfolge und die gekennzeichneten Mann/Frau-Haltungsdetails orientieren sich an der hanafitischen Diyanet-Darstellung. Unterschiede anderer Rechtsschulen werden nicht als Fehler dargestellt.",
                            "Namaz sırası ve belirtilen erkek/kadın duruş ayrıntıları Diyanet'in Hanefî anlatımına dayanır. Diğer mezheplerin farklı uygulamaları hata olarak gösterilmez."
                        ))
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    }
                    .cardStyle(material: true)
                }
                .padding()
            }
            .background(SalahTheme.page)
            .navigationTitle(settings.t("Gebet lernen", "Namaz öğren"))
            .navigationBarTitleDisplayMode(.inline)
            .onAppear {
                guard currentStepIndex > 0 else { return }
                Task { @MainActor in
                    await Task.yield()
                    proxy.scrollTo("prayer-step-card-\(currentStepIndex)", anchor: .top)
                }
            }
            .onChange(of: settings.prayerAudience) { _, _ in
                currentStepIndex = 0
                proxy.scrollTo("prayer-step-top", anchor: .top)
            }
        }
    }

}

private struct PrayerTutorialStepCard: View {
    @EnvironmentObject private var settings: SettingsStore
    let step: PrayerTutorialStep
    let audience: PrayerAudience

    private var imageName: String? {
        guard let key = step.imageKey else { return nil }
        let resolvedKey: String
        switch key {
        case "sitting":
            resolvedKey = "final_sitting"
        default:
            resolvedKey = key
        }
        return "\(audience == .male ? "male" : "female")_\(resolvedKey)"
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack(spacing: 10) {
                Text(step.number)
                    .font(.headline.bold())
                    .foregroundStyle(SalahTheme.deepTeal)
                    .frame(width: 34, height: 34)
                    .background(SalahTheme.gold.opacity(0.95), in: Circle())

                Text(settings.language == .german ? step.deTitle : step.trTitle)
                    .font(.headline.bold())
                    .foregroundStyle(.white)
                    .fixedSize(horizontal: false, vertical: true)

                Spacer(minLength: 4)
            }
            .padding(.horizontal, 14)
            .padding(.vertical, 11)
            .background(SalahTheme.teal)

            VStack(alignment: .leading, spacing: 13) {
                if step.pose == .salam {
                    PrayerSalamVisual()
                } else if let imageName {
                    PrayerPoseArtwork(assetName: imageName)
                        .frame(maxWidth: .infinity)
                        .frame(height: 205)
                        .padding(.vertical, 6)
                        .background(SalahTheme.cream)
                }

                if step.number == "16" {
                    HStack(alignment: .center, spacing: 12) {
                        PrayerPoseArtwork(
                            assetName: "\(audience == .male ? "male" : "female")_finger"
                        )
                        .frame(width: 92, height: 120)
                        .background(SalahTheme.cream)
                        .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))

                        VStack(alignment: .leading, spacing: 4) {
                            Text(settings.t("Zeigefinger im Tashahhud", "Teşehhüdde işaret parmağı"))
                                .font(.subheadline.bold())
                                .foregroundStyle(SalahTheme.deepTeal)

                            Text(settings.t(
                                "Hanefî: Im Schahada-Abschnitt des Ettehiyyâtü wird der rechte Zeigefinger erhoben und bei „illallāh“ wieder gesenkt.",
                                "Hanefî: Ettehiyyâtü içindeki kelime-i şehadet bölümünde sağ işaret parmağı kaldırılır; „illallah“ derken indirilir."
                            ))
                            .font(.caption)
                            .foregroundStyle(SalahTheme.mutedInk)
                            .fixedSize(horizontal: false, vertical: true)
                        }

                        Spacer(minLength: 0)
                    }
                    .padding(10)
                    .background(SalahTheme.gold.opacity(0.10), in: RoundedRectangle(cornerRadius: 13, style: .continuous))
                }

                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("WAS MACHE ICH?", "NE YAPACAĞIM?"), systemImage: "figure.walk")
                        .font(.caption.bold())
                        .foregroundStyle(SalahTheme.teal)
                    Text(settings.language == .german ? step.deAction : step.trAction)
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .padding(12)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(SalahTheme.softTeal, in: RoundedRectangle(cornerRadius: 14))

                if let note = settings.language == .german ? step.deHanafi : step.trHanafi {
                    Label(note, systemImage: "info.circle.fill")
                        .font(.caption)
                        .foregroundStyle(SalahTheme.mutedInk)
                        .padding(11)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(SalahTheme.gold.opacity(0.10), in: RoundedRectangle(cornerRadius: 13))
                }

                if !step.recitations.isEmpty {
                    VStack(alignment: .leading, spacing: 10) {
                        Label(settings.t("WAS SAGE ICH?", "NE SÖYLÜYORUM?"), systemImage: "text.bubble.fill")
                            .font(.caption.bold())
                            .foregroundStyle(SalahTheme.teal)
                        ForEach(step.recitations) { rec in
                            PrayerRecitationView(recitation: rec)
                        }
                    }
                }
            }
            .padding(14)
            .background(SalahTheme.cream)
        }
        .clipShape(RoundedRectangle(cornerRadius: 20))
        .overlay {
            RoundedRectangle(cornerRadius: 20)
                .stroke(SalahTheme.gold.opacity(0.48), lineWidth: 1)
        }
        .shadow(color: SalahTheme.deepTeal.opacity(0.05), radius: 7, y: 3)
    }
}

private struct PrayerRecitationView: View {
    @EnvironmentObject private var settings: SettingsStore
    let recitation: PrayerRecitation
    @State private var showMeaning = false

    var body: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(settings.language == .german ? recitation.deLabel : recitation.trLabel)
                .font(.caption.bold())
                .foregroundStyle(.secondary)
            Text(recitation.arabic)
                .font(.title3)
                .multilineTextAlignment(.trailing)
                .frame(maxWidth: .infinity, alignment: .trailing)
            Text(recitation.transliteration)
                .font(.subheadline.weight(.semibold))
            Button(showMeaning ? settings.t("Bedeutung ausblenden", "Anlamı gizle") : settings.t("Bedeutung anzeigen", "Anlamı göster")) {
                withAnimation(.easeInOut(duration: 0.2)) { showMeaning.toggle() }
            }
            .font(.caption)
            if showMeaning {
                Text(settings.language == .german ? recitation.deMeaning : recitation.trMeaning)
                    .font(.footnote)
                    .foregroundStyle(.secondary)
            }
            if let note = settings.language == .german ? recitation.deNote : recitation.trNote {
                Text(note).font(.caption2).foregroundStyle(.tertiary)
            }
        }
        .padding(10)
        .background(SalahTheme.gold.opacity(0.07), in: RoundedRectangle(cornerRadius: 12))
    }
}

private struct PrayerSalamVisual: View {
    @EnvironmentObject private var settings: SettingsStore

    private var prefix: String { settings.prayerAudience == .male ? "male" : "female" }

    var body: some View {
        VStack(spacing: 14) {
            salamDirection(
                number: "1",
                direction: settings.t("RECHTS", "SAĞA"),
                imageName: "\(prefix)_salam_right",
                arrow: "arrow.right",
                instruction: settings.t(
                    "Oberkörper bleibt nach vorn. Drehe Kopf und Gesicht zu deiner EIGENEN rechten Schulter und sprich den Salām.",
                    "Gövde önde kalır. Başını ve yüzünü KENDİ sağ omzuna çevir ve selâmı söyle."
                )
            )

            salamDirection(
                number: "2",
                direction: settings.t("LINKS", "SOLA"),
                imageName: "\(prefix)_salam_left",
                arrow: "arrow.left",
                instruction: settings.t(
                    "Danach über die Mitte zur EIGENEN linken Schulter drehen und denselben Salām erneut sprechen.",
                    "Sonra ortadan geçerek KENDİ sol omzuna dön ve aynı selâmı tekrar söyle."
                )
            )
        }
        .accessibilityElement(children: .contain)
    }

    private func salamDirection(number: String, direction: String, imageName: String, arrow: String, instruction: String) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text(number)
                    .font(.headline.bold())
                    .foregroundStyle(SalahTheme.deepTeal)
                    .frame(width: 32, height: 32)
                    .background(SalahTheme.gold.opacity(0.82), in: Circle())
                Text(direction)
                    .font(.title2.bold())
                    .foregroundStyle(SalahTheme.teal)
                Spacer()
                Image(systemName: arrow)
                    .font(.system(size: 25, weight: .bold))
                    .foregroundStyle(SalahTheme.gold)
            }

            HStack(alignment: .center, spacing: 14) {
                PrayerPoseArtwork(assetName: imageName)
                    .frame(width: 118, height: 150)
                    .background(SalahTheme.cream)
                    .clipShape(RoundedRectangle(cornerRadius: 14))

                Text(instruction)
                    .font(.subheadline)
                    .foregroundStyle(SalahTheme.ink)
                    .fixedSize(horizontal: false, vertical: true)
            }

            Text("السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ")
                .font(.title3)
                .frame(maxWidth: .infinity, alignment: .trailing)
            Text("As-salāmu ʿalaykum wa raḥmatullāh")
                .font(.subheadline.bold())
                .foregroundStyle(SalahTheme.ink)
        }
        .padding(11)
        .background(SalahTheme.softTeal, in: RoundedRectangle(cornerRadius: 16))
        .overlay { RoundedRectangle(cornerRadius: 16).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }
    }
}

struct HanafiPrayerPlanView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var showSpecialCases = false

    private struct PlanRow: Identifiable {
        let id = UUID()
        let de: String
        let tr: String
        let sequence: String
        let deNote: String
        let trNote: String
    }

    private let rows: [PlanRow] = [
        .init(de: "Fajr", tr: "Sabah", sequence: "2 Sunnah → 2 Fard", deNote: "Die 2 Sunnah vor Fajr sind Sunnah mu'akkadah.", trNote: "Farzdan önceki 2 rekât sünnet-i müekkededir."),
        .init(de: "Dhuhr", tr: "Öğle", sequence: "4 Sunnah → 4 Fard → 2 Sunnah", deNote: "Die erste 4er-Sunnah und die 2 Sunnah danach sind besonders betonte Sunnah.", trNote: "Önceki 4 ve sonraki 2 rekât kuvvetli sünnetlerdendir."),
        .init(de: "Asr", tr: "İkindi", sequence: "4 Sunnah → 4 Fard", deNote: "Die 4 Sunnah davor gelten als ghayr mu'akkadah.", trNote: "Önceki 4 rekât sünnet gayr-i müekkededir."),
        .init(de: "Maghrib", tr: "Akşam", sequence: "3 Fard → 2 Sunnah", deNote: "Nach den 3 Fard folgen 2 Sunnah.", trNote: "3 rekât farzdan sonra 2 rekât sünnet kılınır."),
        .init(de: "Isha", tr: "Yatsı", sequence: "4 Sunnah → 4 Fard → 2 Sunnah → 3 Witr", deNote: "Die ersten 4 sind ghayr mu'akkadah; die 2 danach mu'akkadah. Witr ist hanafitisch wajib.", trNote: "İlk 4 gayr-i müekkede, sonraki 2 müekkede sünnettir. Vitir Hanefî fıkhında vaciptir.")
    ]

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 9) {
                    Label(settings.t("Was bedeutet Rakʿa?", "Rekât ne demek?"), systemImage: "1.circle.fill")
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Eine Rakʿa ist EIN kompletter Gebetsdurchgang. Stell dir vor, du gehst immer dieselbe kleine Runde durch. Erst nach dem zweiten Sujud ist diese Runde fertig.",
                        "Bir rekât, namazın TAM bir bölümüdür. Her rekâtta aynı temel sıra tekrar eder. İkinci secde bittikten sonra bir rekât tamamlanır."
                    ))
                    .font(.subheadline)
                    .fixedSize(horizontal: false, vertical: true)
                    Text(settings.t(
                        "Beim allerersten Rakʿa beginnt das Gebet vorher mit dem Eröffnungstakbir. Danach kommt der folgende Grundablauf.",
                        "İlk rekâtta bu sıradan önce iftitah tekbiriyle namaza başlanır. Sonra aşağıdaki temel akış gelir."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("1 Rakʿa ganz langsam", "1 rekâtı yavaşça öğren"))
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    flowRow("1", settings.t("Stehen und lesen", "Ayakta dur ve oku"), settings.t("Stehe zur Qibla. Lies die vorgeschriebenen Texte dieser Rakʿa.", "Kıbleye dönük dur. Bu rekâtta okunacak metinleri oku."), "person.fill")
                    flowRow("2", settings.t("Rukūʿ", "Rükû"), settings.t("Sage Allāhu akbar, beuge dich und bleib kurz ruhig im Rukūʿ.", "Allāhu ekber de, rükûya eğil ve kısa bir an sakin kal."), "arrow.down.forward")
                    flowRow("3", settings.t("Ganz aufrichten", "Tam doğrul"), settings.t("Komm vollständig hoch und steh kurz ruhig. Nicht direkt in den Sujud gehen.", "Tamamen doğrul ve kısa bir an ayakta sakin kal. Doğrudan secdeye geçme."), "arrow.up")
                    flowRow("4", settings.t("Sujud 1", "1. secde"), settings.t("Gehe in den ersten Sujud und bleib kurz ruhig.", "Birinci secdeye git ve kısa bir an sakin kal."), "arrow.down")
                    flowRow("5", settings.t("Sitzen", "Otur"), settings.t("Setze dich vollständig zwischen den beiden Sujud.", "İki secde arasında tamamen otur."), "figure.seated.side")
                    flowRow("6", settings.t("Sujud 2", "2. secde"), settings.t("Mache den zweiten Sujud genauso ruhig wie den ersten.", "İkinci secdeyi birincisi gibi sakin şekilde yap."), "arrow.down")
                    HStack(alignment: .top, spacing: 10) {
                        Image(systemName: "checkmark.circle.fill")
                            .font(.title2)
                            .foregroundStyle(.green)
                        Text(settings.t(
                            "JETZT ist 1 Rakʿa fertig. Erst jetzt entscheidest du: zur nächsten Rakʿa aufstehen oder zum vorgesehenen Sitzen übergehen.",
                            "ŞİMDİ 1 rekât tamamlandı. Ancak şimdi karar verilir: sonraki rekâta kalk veya gereken oturuşa geç."
                        ))
                        .font(.subheadline.bold())
                        .fixedSize(horizontal: false, vertical: true)
                    }
                    .padding(11)
                    .background(Color.green.opacity(0.09), in: RoundedRectangle(cornerRadius: 13, style: .continuous))
                }
                .cardStyle()

                planCard(
                    title: settings.t("2 Rakʿa", "2 rekât"),
                    subtitle: settings.t("Beispiel: Fajr-Fard und viele 2er-Sunnah-Gebete", "Örnek: Sabah farzı ve birçok 2 rekât sünnet"),
                    lines: settings.language == .german ? [
                        "Rakʿa 1 komplett machen. Nach Sujud 2 wieder aufstehen.",
                        "Rakʿa 2 komplett machen. Nach Sujud 2 NICHT mehr aufstehen.",
                        "Im letzten Sitzen: Ettehiyyâtü → Salli → Bârik → Abschlussdua.",
                        "Dann Salam: nur den Kopf nach rechts, danach nur den Kopf nach links. Der Körper bleibt zur Qibla."
                    ] : [
                        "1. rekâtı tamamla. 2. secdeden sonra yeniden ayağa kalk.",
                        "2. rekâtı tamamla. 2. secdeden sonra artık ayağa kalkma.",
                        "Son oturuşta: Ettehiyyâtü → Salli → Bârik → kapanış duası.",
                        "Sonra selâm: yalnız baş sağa, ardından yalnız baş sola döner. Gövde kıbleye dönük kalır."
                    ]
                )

                planCard(
                    title: settings.t("3 Rakʿa Fard", "3 rekât farz"),
                    subtitle: settings.t("Beispiel: Maghrib-Fard", "Örnek: Akşam farzı"),
                    lines: settings.language == .german ? [
                        "Rakʿa 1 komplett machen und zu Rakʿa 2 aufstehen.",
                        "Rakʿa 2 komplett machen. Danach sitzen und Ettehiyyâtü lesen.",
                        "Nach Ettehiyyâtü mit Allāhu akbar zu Rakʿa 3 aufstehen.",
                        "Rakʿa 3: Basmala + Al-Fātiha; bei diesem Fard keine Zusatzsura nötig. Dann Rukūʿ, Aufrichten, Sujud 1, Sitzen, Sujud 2.",
                        "Danach letztes Sitzen vollständig und Salam rechts, dann links."
                    ] : [
                        "1. rekâtı tamamla ve 2. rekâta kalk.",
                        "2. rekâtı tamamla. Sonra otur ve Ettehiyyâtü oku.",
                        "Ettehiyyâtü'den sonra Allāhu ekber diyerek 3. rekâta kalk.",
                        "3. rekât: Besmele + Fâtiha; bu farzda zamm-ı sûre gerekmez. Sonra rükû, doğrulma, 1. secde, oturuş, 2. secde.",
                        "Sonra tam son oturuş ve sağa, ardından sola selâm."
                    ]
                )

                planCard(
                    title: settings.t("4 Rakʿa Fard", "4 rekât farz"),
                    subtitle: settings.t("Beispiel: Dhuhr, Asr und Isha-Fard", "Örnek: Öğle, İkindi ve Yatsı farzı"),
                    lines: settings.language == .german ? [
                        "Rakʿa 1 komplett machen und zu Rakʿa 2 aufstehen.",
                        "Rakʿa 2 komplett machen. Danach sitzen und Ettehiyyâtü lesen.",
                        "Zu Rakʿa 3 aufstehen. Dort Basmala + Al-Fātiha lesen, dann die Rakʿa vollständig beenden.",
                        "Zu Rakʿa 4 aufstehen. Wieder Basmala + Al-Fātiha lesen, dann Rukūʿ, Aufrichten und beide Sujud.",
                        "Nach Rakʿa 4 letztes Sitzen: Ettehiyyâtü → Salli → Bârik → Abschlussdua → Salam rechts und links."
                    ] : [
                        "1. rekâtı tamamla ve 2. rekâta kalk.",
                        "2. rekâtı tamamla. Sonra otur ve Ettehiyyâtü oku.",
                        "3. rekâta kalk. Besmele + Fâtiha oku ve rekâtı tamamla.",
                        "4. rekâta kalk. Yine Besmele + Fâtiha oku; sonra rükû, doğrulma ve iki secdeyi tamamla.",
                        "4. rekâttan sonra son oturuş: Ettehiyyâtü → Salli → Bârik → kapanış duası → sağa ve sola selâm."
                    ]
                )

                DisclosureGroup(isExpanded: $showSpecialCases) {
                    VStack(alignment: .leading, spacing: 12) {
                        Text(settings.t(
                            "4-Rakʿa-Sunnah: In allen Rakʿa werden Al-Fātiha und eine Zusatzsura gelesen. Bei der betonten 4er-Sunnah von Dhuhr liest man im ersten Sitzen Ettehiyyâtü und steht auf. Bei den 4 ghayr-mu'akkadah vor Asr/Isha werden im ersten Sitzen zusätzlich Salli/Bârik gelesen; Rakʿa 3 beginnt wieder mit Sübhaneke.",
                            "4 rekât sünnet: Her rekâtta Fâtiha ve zamm-ı sûre okunur. Öğlenin kuvvetli 4 rekât sünnetinde ilk oturuşta Ettehiyyâtü okunup kalkılır. İkindi/Yatsı öncesi 4 gayr-i müekkede sünnette ilk oturuşta Salli/Bârik de okunur; 3. rekâta yeniden Sübhâneke ile başlanır."
                        ))
                        .font(.subheadline)

                        Text(settings.t(
                            "Witr (hanafitisch): 3 Rakʿa. In Rakʿa 3 werden nach Fātiha und Zusatzsura vor dem Rukūʿ erneut die Hände gehoben, Allāhu akbar gesagt, die Hände wieder gebunden und die Qunūt-Duas gelesen.",
                            "Vitir (Hanefî): 3 rekât. 3. rekâtta Fâtiha ve zamm-ı sûreden sonra rükûdan önce eller tekrar kaldırılır, Allāhu ekber denir, eller yeniden bağlanır ve Kunut duaları okunur."
                        ))
                        .font(.subheadline)

                        NavigationLink { QunutDuaView() } label: {
                            Label(settings.t("Qunūt-Duas vollständig", "Kunut duaları tam metin"), systemImage: "text.book.closed")
                                .font(.headline)
                        }
                    }
                    .padding(.top, 8)
                } label: {
                    Label(settings.t("Sonderfälle: 4er-Sunnah & Witr", "Özel durumlar: 4 rekât sünnet ve vitir"), systemImage: "chevron.down.circle")
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                }
                .padding(14)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 16).stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1) }

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Wie viele Rakʿa haben die täglichen Gebete?", "Günlük namazlar kaç rekât?"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    ForEach(rows) { row in
                        VStack(alignment: .leading, spacing: 4) {
                            HStack {
                                Text(settings.language == .german ? row.de : row.tr).font(.headline)
                                Spacer()
                                Text(row.sequence).font(.subheadline.bold()).foregroundStyle(SalahTheme.teal)
                            }
                            Text(settings.language == .german ? row.deNote : row.trNote)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        .padding(.vertical, 4)
                        if row.id != rows.last?.id { Divider() }
                    }
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 6) {
                    Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama")).font(.headline)
                    Text(settings.t(
                        "Diyanet Namaz İlmihali · hanafitische Grunddarstellung. Andere Rechtsschulen können einzelne Sunnah-Details anders einordnen.",
                        "Diyanet Namaz İlmihali · Hanefî temel anlatım. Diğer mezhepler bazı sünnet ayrıntılarını farklı değerlendirebilir."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Rakʿa verstehen", "Rekâtı anla"))
        .navigationBarTitleDisplayMode(.inline)
    }

    private func flowRow(_ number: String, _ title: String, _ detail: String, _ icon: String) -> some View {
        HStack(alignment: .top, spacing: 11) {
            ZStack {
                Circle().fill(SalahTheme.gold.opacity(0.20)).frame(width: 34, height: 34)
                Text(number).font(.headline.bold()).foregroundStyle(SalahTheme.deepTeal)
            }
            VStack(alignment: .leading, spacing: 3) {
                Label(title, systemImage: icon)
                    .font(.headline)
                    .foregroundStyle(SalahTheme.ink)
                Text(detail)
                    .font(.subheadline)
                    .foregroundStyle(SalahTheme.mutedInk)
                    .fixedSize(horizontal: false, vertical: true)
            }
            Spacer(minLength: 0)
        }
    }

    private func planCard(title: String, subtitle: String, lines: [String]) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title)
                .font(.title3.bold())
                .foregroundStyle(SalahTheme.deepTeal)
            Text(subtitle)
                .font(.caption.bold())
                .foregroundStyle(SalahTheme.teal)
            ForEach(lines.indices, id: \.self) { index in
                HStack(alignment: .top, spacing: 10) {
                    Text("\(index + 1)")
                        .font(.caption.bold())
                        .foregroundStyle(.white)
                        .frame(width: 24, height: 24)
                        .background(SalahTheme.teal, in: Circle())
                    Text(lines[index])
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                    Spacer(minLength: 0)
                }
            }
        }
        .cardStyle()
    }
}

private struct QunutDuaView: View {
    @EnvironmentObject private var settings: SettingsStore
    var body: some View {
        List {
            Section("Kunut 1") {
                Text("اللَّهُمَّ إِنَّا نَسْتَعِينُكَ وَنَسْتَغْفِرُكَ وَنَسْتَهْدِيكَ وَنُؤْمِنُ بِكَ وَنَتُوبُ إِلَيْكَ وَنَتَوَكَّلُ عَلَيْكَ وَنُثْنِي عَلَيْكَ الْخَيْرَ كُلَّهُ نَشْكُرُكَ وَلَا نَكْفُرُكَ وَنَخْلَعُ وَنَتْرُكُ مَنْ يَفْجُرُكَ").font(.title3).multilineTextAlignment(.trailing)
                Text("Allâhümme innâ nesteînüke ve nestağfirüke ve nestehdîk. Ve nü'minü bike ve netûbü ileyk. Ve netevekkelü aleyke ve nüsnî aleykel-hayra küllehû neşkürüke ve lâ nekfürük. Ve nahleu ve netrükü men yefcürük.")
            }
            Section("Kunut 2") {
                Text("اللَّهُمَّ إِيَّاكَ نَعْبُدُ وَلَكَ نُصَلِّي وَنَسْجُدُ وَإِلَيْكَ نَسْعَى وَنَحْفِدُ نَرْجُو رَحْمَتَكَ وَنَخْشَى عَذَابَكَ إِنَّ عَذَابَكَ بِالْكُفَّارِ مُلْحِقٌ").font(.title3).multilineTextAlignment(.trailing)
                Text("Allâhümme iyyâke na'büdü ve leke nusallî ve nescüd. Ve ileyke nes'â ve nahfid. Nercû rahmeteke ve nahşâ azâbek. İnne azâbeke bil-küffâri mülhik.")
            }
            Section {
                Text(settings.t("Die in der Türkei verbreiteten hanafitischen Qunūt-Texte für Witr. Für Aussprachetraining sollte eine verlässliche menschliche Aufnahme verwendet werden; SalahPath erzeugt hierfür keine KI-Stimme.", "Türkiye'de yaygın Hanefî vitir Kunut metinleridir. Telaffuz eğitimi için güvenilir insan kaydı kullanılmalıdır; SalahPath bunun için yapay zekâ sesi üretmez."))
                    .font(.footnote).foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Qunūt", "Kunut"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Wudu

private struct WuduTutorialStep: Identifiable {
    let id = UUID()
    let number: Int
    let image: String?
    let deTitle: String
    let trTitle: String
    let deAction: String
    let trAction: String
    let repeatText: String?
    let hanafiFard: Bool
}

private struct WuduInstructionVisual: View {
    let key: String
    let stepNumber: Int

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 26, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.48)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            Circle()
                .fill(SalahTheme.softTeal.opacity(0.44))
                .frame(width: 176, height: 176)
                .offset(x: 72, y: -38)

            Group {
                switch stepNumber {
                case 1: intentionVisual
                case 2: basmalaVisual
                case 3: handsVisual
                case 4: mouthVisual
                case 5: noseVisual
                case 6: faceVisual(highlightY: 4, dropsY: -8, largeHighlight: true)
                case 7: armVisual(mirrored: false)
                case 8: armVisual(mirrored: true)
                case 9: headVisual
                case 10: earsVisual
                case 11: neckVisual
                case 12: footVisual(mirrored: false)
                case 13: footVisual(mirrored: true)
                default: genericVisual
                }
            }
            .scaleEffect(0.95)
        }
        .frame(maxWidth: .infinity)
        .frame(height: 188)
        .clipShape(RoundedRectangle(cornerRadius: 26, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 26, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
        }
        .accessibilityHidden(true)
    }

    private var intentionVisual: some View {
        ZStack {
            neutralFace
                .scaleEffect(0.86)
                .offset(y: 3)

            Image(systemName: "heart.fill")
                .font(.system(size: 27, weight: .bold))
                .foregroundStyle(SalahTheme.gold)
                .offset(x: 53, y: 43)

            Image(systemName: "drop.fill")
                .font(.system(size: 22, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
                .offset(x: 82, y: -63)
        }
    }

    private var basmalaVisual: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(Color.white.opacity(0.76))
                .frame(width: 250, height: 118)
                .overlay {
                    RoundedRectangle(cornerRadius: 28, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.64), lineWidth: 1.5)
                }

            Text("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ")
                .font(.system(size: 27, weight: .semibold))
                .foregroundStyle(SalahTheme.deepTeal)
                .multilineTextAlignment(.center)
                .minimumScaleFactor(0.75)
                .padding(.horizontal, 20)

            Image(systemName: "drop.fill")
                .font(.system(size: 22, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
                .offset(x: 116, y: -48)

            Image(systemName: "sparkles")
                .font(.system(size: 18, weight: .bold))
                .foregroundStyle(SalahTheme.gold)
                .offset(x: -118, y: -48)
        }
    }

    private var handsVisual: some View {
        HStack(spacing: 18) {
            Image(systemName: "hand.raised.fill")
                .font(.system(size: 73, weight: .regular))
            Image(systemName: "hand.raised.fill")
                .font(.system(size: 73, weight: .regular))
                .scaleEffect(x: -1, y: 1)
        }
        .foregroundStyle(SalahTheme.deepTeal)
        .overlay(alignment: .top) {
            HStack(spacing: 20) {
                drop(size: 19); drop(size: 25); drop(size: 19)
            }
            .offset(y: -41)
        }
    }

    private var mouthVisual: some View {
        ZStack {
            neutralFace
                .offset(x: 18)

            Image(systemName: "hand.raised.fill")
                .font(.system(size: 50, weight: .regular))
                .foregroundStyle(SalahTheme.deepTeal)
                .rotationEffect(.degrees(-68))
                .offset(x: -58, y: 26)

            HStack(spacing: 5) {
                drop(size: 12)
                drop(size: 16)
                drop(size: 12)
            }
            .offset(x: -24, y: 54)

            Capsule()
                .fill(SalahTheme.gold.opacity(0.72))
                .frame(width: 42, height: 10)
                .offset(x: 13, y: 31)
        }
    }

    private var noseVisual: some View {
        ZStack {
            neutralFace
                .offset(x: 12)

            Image(systemName: "hand.raised.fill")
                .font(.system(size: 46, weight: .regular))
                .foregroundStyle(SalahTheme.deepTeal)
                .rotationEffect(.degrees(-72))
                .offset(x: -55, y: 4)

            Image(systemName: "hand.raised.fill")
                .font(.system(size: 34, weight: .regular))
                .foregroundStyle(SalahTheme.teal.opacity(0.92))
                .rotationEffect(.degrees(72))
                .scaleEffect(x: -1, y: 1)
                .offset(x: 70, y: 42)

            HStack(spacing: 4) {
                drop(size: 10)
                drop(size: 14)
            }
            .offset(x: -20, y: 36)

            Ellipse()
                .fill(SalahTheme.gold.opacity(0.58))
                .frame(width: 34, height: 18)
                .offset(x: 8, y: 2)
        }
    }

    private func faceVisual(highlightY: CGFloat, dropsY: CGFloat, largeHighlight: Bool = false) -> some View {
        ZStack {
            neutralFace

            Ellipse()
                .fill(SalahTheme.gold.opacity(largeHighlight ? 0.16 : 0.24))
                .overlay {
                    Ellipse()
                        .stroke(SalahTheme.gold.opacity(0.90), lineWidth: largeHighlight ? 4 : 3)
                }
                .frame(
                    width: largeHighlight ? 118 : 58,
                    height: largeHighlight ? 128 : 34
                )
                .offset(y: highlightY)

            HStack(spacing: 5) {
                drop(size: 14)
                drop(size: 18)
                drop(size: 14)
            }
            .offset(x: 76, y: dropsY)
        }
    }

    private var neutralFace: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(Color.white.opacity(0.98))
                .frame(width: 154, height: 104)
                .offset(y: 82)
                .overlay {
                    RoundedRectangle(cornerRadius: 28, style: .continuous)
                        .stroke(SalahTheme.deepTeal.opacity(0.28), lineWidth: 2)
                        .frame(width: 154, height: 104)
                        .offset(y: 82)
                }

            Circle()
                .fill(Color(red: 0.86, green: 0.68, blue: 0.52))
                .frame(width: 132, height: 132)
                .overlay {
                    Circle()
                        .stroke(SalahTheme.deepTeal.opacity(0.72), lineWidth: 4)
                }

            Capsule()
                .fill(SalahTheme.deepTeal)
                .frame(width: 82, height: 22)
                .offset(y: -54)

            HStack(spacing: 34) {
                Capsule()
                    .fill(SalahTheme.deepTeal)
                    .frame(width: 18, height: 4)
                Capsule()
                    .fill(SalahTheme.deepTeal)
                    .frame(width: 18, height: 4)
            }
            .offset(y: -16)

            Capsule()
                .fill(SalahTheme.deepTeal.opacity(0.70))
                .frame(width: 4, height: 17)
                .offset(y: 3)

            Capsule()
                .fill(SalahTheme.deepTeal)
                .frame(width: 64, height: 23)
                .offset(y: 42)

            Capsule()
                .fill(Color(red: 0.86, green: 0.68, blue: 0.52))
                .frame(width: 35, height: 12)
                .offset(y: 31)

            HStack(spacing: 118) {
                Circle()
                    .fill(Color(red: 0.86, green: 0.68, blue: 0.52))
                    .frame(width: 18, height: 26)
                Circle()
                    .fill(Color(red: 0.86, green: 0.68, blue: 0.52))
                    .frame(width: 18, height: 26)
            }
        }
    }

    private func armVisual(mirrored: Bool) -> some View {
        ZStack {
            Capsule()
                .fill(SalahTheme.deepTeal.opacity(0.90))
                .frame(width: 150, height: 46)
                .rotationEffect(.degrees(mirrored ? -12 : 12))
            Image(systemName: "hand.raised.fill")
                .font(.system(size: 54, weight: .regular))
                .foregroundStyle(SalahTheme.deepTeal)
                .rotationEffect(.degrees(mirrored ? 78 : -78))
                .scaleEffect(x: mirrored ? -1 : 1, y: 1)
                .offset(x: mirrored ? -86 : 86, y: -18)
            HStack(spacing: 7) {
                drop(size: 15); drop(size: 20); drop(size: 15)
            }
            .offset(x: mirrored ? 20 : -20, y: -58)
        }
    }

    private var headVisual: some View {
        ZStack {
            neutralFace
                .offset(y: 8)

            HStack(spacing: 46) {
                Image(systemName: "hand.raised.fill")
                Image(systemName: "hand.raised.fill")
                    .scaleEffect(x: -1, y: 1)
            }
            .font(.system(size: 42, weight: .regular))
            .foregroundStyle(SalahTheme.deepTeal)
            .offset(y: -58)

            HStack(spacing: 9) {
                drop(size: 12)
                drop(size: 16)
                drop(size: 12)
            }
            .offset(x: 74, y: -48)
        }
    }

    private var earsVisual: some View {
        ZStack {
            neutralFace

            HStack(spacing: 106) {
                Capsule()
                    .fill(SalahTheme.gold.opacity(0.72))
                    .frame(width: 20, height: 40)
                Capsule()
                    .fill(SalahTheme.gold.opacity(0.72))
                    .frame(width: 20, height: 40)
            }

            HStack(spacing: 124) {
                drop(size: 16)
                drop(size: 16)
            }
            .offset(y: -2)
        }
    }

    private var neckVisual: some View {
        ZStack {
            neutralFace
                .offset(y: -10)

            HStack(spacing: 38) {
                Capsule()
                    .fill(SalahTheme.gold.opacity(0.74))
                    .frame(width: 30, height: 11)
                    .rotationEffect(.degrees(18))
                Capsule()
                    .fill(SalahTheme.gold.opacity(0.74))
                    .frame(width: 30, height: 11)
                    .rotationEffect(.degrees(-18))
            }
            .offset(y: 57)

            HStack(spacing: 74) {
                Image(systemName: "hand.raised.fill")
                Image(systemName: "hand.raised.fill")
                    .scaleEffect(x: -1, y: 1)
            }
            .font(.system(size: 33))
            .foregroundStyle(SalahTheme.teal)
            .offset(y: 55)
        }
    }

    private func footVisual(mirrored: Bool) -> some View {
        ZStack {
            VStack(spacing: -4) {
                HStack(alignment: .bottom, spacing: 3) {
                    Circle().frame(width: 10, height: 10)
                    Circle().frame(width: 12, height: 12)
                    Circle().frame(width: 14, height: 14)
                    Circle().frame(width: 12, height: 12)
                    Circle().frame(width: 9, height: 9)
                }
                .offset(x: 11)

                Capsule()
                    .frame(width: 66, height: 118)
                    .rotationEffect(.degrees(-11))
            }
            .foregroundStyle(SalahTheme.deepTeal)
            .scaleEffect(x: mirrored ? -1 : 1, y: 1)

            Capsule()
                .fill(SalahTheme.gold.opacity(0.62))
                .frame(width: 54, height: 19)
                .offset(x: mirrored ? 9 : -9, y: 31)
                .rotationEffect(.degrees(mirrored ? 11 : -11))

            HStack(spacing: 10) {
                drop(size: 16)
                drop(size: 22)
                drop(size: 16)
            }
            .offset(x: mirrored ? 45 : -45, y: -58)
        }
    }

    private var genericVisual: some View {
        ZStack {
            Image(systemName: "drop.fill")
                .font(.system(size: 72))
                .foregroundStyle(SalahTheme.teal)
            Image(systemName: "sparkles")
                .font(.system(size: 28, weight: .bold))
                .foregroundStyle(SalahTheme.gold)
                .offset(x: 60, y: -55)
        }
    }

    private func drop(size: CGFloat) -> some View {
        Image(systemName: "drop.fill")
            .font(.system(size: size, weight: .semibold))
            .foregroundStyle(SalahTheme.teal)
    }
}

struct WuduGuideView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var currentStepIndex: Int
    @State private var showExactDetail = true

    init(initialStepIndex: Int = 0) {
        _currentStepIndex = State(initialValue: min(max(initialStepIndex, 0), 12))
    }

    private var safeCurrentStepIndex: Int {
        min(max(currentStepIndex, 0), max(steps.count - 1, 0))
    }

    private let steps: [WuduTutorialStep] = [
        .init(number: 1, image: "wudu_intention", deTitle: "Niyyah / Absicht", trTitle: "Niyet", deAction: "Fasse im Herzen die Absicht, Wudu zu nehmen. In der hanafitischen Lehre ist die Niyyah Sunnah und gehört nicht zu den vier Fard-Bestandteilen.", trAction: "Kalben abdest almaya niyet et. Hanefî mezhebinde niyet sünnettir; abdestin dört farzından biri değildir.", repeatText: nil, hanafiFard: false),
        .init(number: 2, image: "wudu_basmala", deTitle: "Basmala", trTitle: "Besmele", deAction: "Beginne mit Bismillāh. Dies gehört zur dargestellten Wudu-Praxis und ist kein eigener Fard-Bestandteil.", trAction: "Bismillâh diyerek başla. Bu, gösterilen abdest uygulamasının bir parçasıdır; ayrı bir farz değildir.", repeatText: nil, hanafiFard: false),
        .init(number: 3, image: "wudu_hands", deTitle: "Hände", trTitle: "Eller", deAction: "Beide Hände bis zu den Handgelenken waschen und die Fingerzwischenräume erreichen.", trAction: "İki eli bileklere kadar yıka ve parmak aralarına su ulaştır.", repeatText: "3×", hanafiFard: false),
        .init(number: 4, image: "wudu_mouth", deTitle: "Mund", trTitle: "Ağız", deAction: "Mit der rechten Hand Wasser in den Mund nehmen und gründlich spülen.", trAction: "Sağ elle ağza su alıp iyice çalkala.", repeatText: "3×", hanafiFard: false),
        .init(number: 5, image: "wudu_nose", deTitle: "Nase: Wasser & reinigen", trTitle: "Buruna su verme ve temizleme", deAction: "Nimm mit der rechten Hand Wasser an die Nase, ziehe es vorsichtig hinein und reinige bzw. schnäuze die Nase mit der linken Hand.", trAction: "Sağ avuçla burnuna su verip dikkatlice içine çek; ardından sol elle burnunu temizle ve sümkür.", repeatText: "3×", hanafiFard: false),
        .init(number: 6, image: "wudu_face", deTitle: "Gesicht", trTitle: "Yüz", deAction: "Wasche das ganze Gesicht: vom normalen Haaransatz bis zum Kinn und seitlich von Ohr zu Ohr. Kein Bereich darf trocken bleiben. Einmal vollständig ist Farz; dreimal entspricht der Sunnah-Praxis.", trAction: "Yüzün tamamını normal saç çizgisinden çeneye ve bir kulaktan diğer kulağa kadar yıka. Kuru yer kalmamalı. Bir kez tam yıkamak farzdır; üç kez yıkamak sünnet uygulamasıdır.", repeatText: "3×", hanafiFard: true),
        .init(number: 7, image: "wudu_leftarm", deTitle: "Rechter Arm", trTitle: "Sağ kol", deAction: "Wasche die rechte Hand und den rechten Arm vollständig bis einschließlich Ellenbogen. Achte auf Fingerzwischenräume und darauf, dass der Ellenbogen nass wird.", trAction: "Sağ eli ve sağ kolu dirsek dahil tamamen yıka. Parmak aralarına ve dirseğin tamamen ıslanmasına dikkat et.", repeatText: "3×", hanafiFard: true),
        .init(number: 8, image: "wudu_rightarm", deTitle: "Linker Arm", trTitle: "Sol kol", deAction: "Wasche die linke Hand und den linken Arm vollständig bis einschließlich Ellenbogen. Achte auf Fingerzwischenräume und darauf, dass der Ellenbogen nass wird.", trAction: "Sol eli ve sol kolu dirsek dahil tamamen yıka. Parmak aralarına ve dirseğin tamamen ıslanmasına dikkat et.", repeatText: "3×", hanafiFard: true),
        .init(number: 9, image: "wudu_head", deTitle: "Masah des Kopfes", trTitle: "Başın meshi", deAction: "Mit feuchten Händen direkt über Kopf bzw. Haar streichen. Die feuchte Hand muss Kopf oder Haar erreichen; eine Kopfbedeckung, die das verhindert, darf nicht dazwischenliegen. Hanafi: Für die Gültigkeit muss mindestens ein Viertel des Kopfes vom Masah erfasst werden; die vollständige Masah wird in dieser Lernreihenfolge einmal gezeigt.", trAction: "Islak ellerle başı veya saçı doğrudan mesh et. Islak el başa ya da saça ulaşmalıdır; bunu engelleyen takke, bone vb. arada olmamalıdır. Hanefî: Geçerlilik için başın en az dörtte biri mesh edilmelidir; bu öğrenme sıralamasında tam baş meshi bir kez gösterilir.", repeatText: "1×", hanafiFard: true),
        .init(number: 10, image: "wudu_ears", deTitle: "Ohren", trTitle: "Kulaklar", deAction: "Mit erneut angefeuchteten Händen die Ohren abwischen: außen mit den Daumen, innen mit Zeige- oder kleinen Fingern. Nicht einer der vier Fard-Bestandteile.", trAction: "Eller tekrar ıslatılarak kulakların dışı başparmakla, içi işaret veya serçe parmakla mesh edilir. Dört farzdan biri değildir.", repeatText: "1×", hanafiFard: false),
        .init(number: 11, image: "wudu_neck", deTitle: "Nacken / Ense", trTitle: "Boyun / ense", deAction: "In der Diyanet/Hanafi-Lernreihenfolge wird die Nacken- bzw. Ensenpartie mit der Rückseite der feuchten Finger gewischt. Nicht die Kehle oder Vorderseite des Halses wischen. Dieser Schritt ist Sunnah und gehört NICHT zu den vier Farz-Bestandteilen.", trAction: "Diyanet/Hanefî öğrenme sıralamasında ense, ıslak parmakların dış kısmıyla mesh edilir. Boğazın ön tarafı mesh edilmez. Bu adım sünnettir ve abdestin dört farzından biri DEĞİLDİR.", repeatText: "1×", hanafiFard: false),
        .init(number: 12, image: "wudu_leftfoot", deTitle: "Rechter Fuß", trTitle: "Sağ ayak", deAction: "Wasche den rechten Fuß vollständig bis einschließlich beider Knöchel. Führe Wasser auch zwischen die Zehen und kontrolliere Ferse, Fußsohle und Knöchel auf trockene Stellen.", trAction: "Sağ ayağı iki aşık kemiği dahil tamamen yıka. Parmak aralarına da su ulaştır; topuk, ayak tabanı ve aşık kemiklerinde kuru yer kalmadığını kontrol et.", repeatText: "3×", hanafiFard: true),
        .init(number: 13, image: "wudu_rightfoot", deTitle: "Linker Fuß", trTitle: "Sol ayak", deAction: "Wasche den linken Fuß vollständig bis einschließlich beider Knöchel. Führe Wasser auch zwischen die Zehen und kontrolliere Ferse, Fußsohle und Knöchel auf trockene Stellen.", trAction: "Sol ayağı iki aşık kemiği dahil tamamen yıka. Parmak aralarına da su ulaştır; topuk, ayak tabanı ve aşık kemiklerinde kuru yer kalmadığını kontrol et.", repeatText: "3×", hanafiFard: true)
    ]

    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(spacing: 14) {
                    Color.clear.frame(height: 1).id("wudu-step-top")

                    VStack(alignment: .leading, spacing: 9) {
                        Label(settings.t("Wudu ganz von vorne", "Abdesti en baştan öğren"), systemImage: "drop.fill")
                            .font(.title3.bold())
                            .foregroundStyle(SalahTheme.deepTeal)

                        Text(settings.t(
                            "Männer und Frauen machen Wudu grundsätzlich gleich. Du siehst immer nur einen Schritt. Mach ihn in Ruhe fertig und gehe dann weiter.",
                            "Erkekler ve kadınlar abdesti temelde aynı şekilde alır. Her seferinde yalnız bir adım görürsün. Adımı sakin şekilde tamamla, sonra devam et."
                        ))
                        .font(.subheadline)
                        .fixedSize(horizontal: false, vertical: true)

                        Divider()

                        Text(settings.t(
                            "Die 4 Farz-Bestandteile im Hanafi/Diyanet-Ablauf sind: 1) Gesicht waschen, 2) Arme mit Ellenbogen waschen, 3) mindestens ein Viertel des Kopfes mit nasser Hand wischen, 4) Füße mit Knöcheln waschen.",
                            "Hanefî/Diyanet anlatımında abdestin 4 farzı: 1) yüzü yıkamak, 2) kolları dirseklerle yıkamak, 3) başın en az dörtte birini mesh etmek, 4) ayakları aşık kemikleriyle yıkamaktır."
                        ))
                        .font(.footnote.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                        Text(settings.t(
                            "Bei den Farz-Waschschritten reicht für die Gültigkeit eine vollständige Waschung; dreimaliges Waschen ist die Sunnah-Praxis. Kopf-Masah wird einmal gezeigt.",
                            "Farz olan yıkama bölümlerinde geçerlilik için bir kez tam yıkamak yeterlidir; üç kez yıkamak sünnettir. Baş meshi bir kez gösterilir."
                        ))
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    }
                    .cardStyle(material: true)

                    VStack(spacing: 8) {
                        HStack {
                            Text(settings.t("Schritt", "Adım") + " \(currentStepIndex + 1) / \(steps.count)")
                                .font(.headline.bold())
                                .foregroundStyle(SalahTheme.deepTeal)
                            Spacer()
                            Text(steps[safeCurrentStepIndex].hanafiFard ? settings.t("FARZ · PFLICHT", "FARZ") : settings.t("SUNNAH", "SÜNNET"))
                                .font(.caption.bold())
                                .padding(.horizontal, 9)
                                .padding(.vertical, 5)
                                .background(
                                    (steps[safeCurrentStepIndex].hanafiFard ? SalahTheme.gold : SalahTheme.softTeal),
                                    in: Capsule()
                                )
                                .foregroundStyle(SalahTheme.deepTeal)
                        }
                        ProgressView(value: Double(currentStepIndex + 1), total: Double(steps.count))
                            .tint(SalahTheme.teal)
                    }
                    .padding(12)
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                    .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }

                    wuduStepCard(steps[safeCurrentStepIndex])
                        .id("wudu-step-card-\(currentStepIndex)")

                    HStack(spacing: 12) {
                        Button {
                            guard currentStepIndex > 0 else { return }
                            let target = currentStepIndex - 1
                            withAnimation(.easeInOut(duration: 0.2)) {
                                currentStepIndex = target
                            }
                            Task { @MainActor in
                                await Task.yield()
                                withAnimation(.easeInOut(duration: 0.2)) {
                                    proxy.scrollTo("wudu-step-card-\(target)", anchor: .top)
                                }
                            }
                        } label: {
                            Label(settings.t("Zurück", "Geri"), systemImage: "chevron.left")
                                .font(.headline.bold())
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 13)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(currentStepIndex > 0 ? SalahTheme.deepTeal : SalahTheme.mutedInk.opacity(0.45))
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }
                        .disabled(currentStepIndex == 0)

                        Button {
                            guard currentStepIndex < steps.count - 1 else { return }
                            let target = currentStepIndex + 1
                            withAnimation(.easeInOut(duration: 0.2)) {
                                currentStepIndex = target
                            }
                            Task { @MainActor in
                                await Task.yield()
                                withAnimation(.easeInOut(duration: 0.2)) {
                                    proxy.scrollTo("wudu-step-card-\(target)", anchor: .top)
                                }
                            }
                        } label: {
                            HStack {
                                Text(currentStepIndex == steps.count - 1 ? settings.t("Wudu fertig", "Abdest tamam") : settings.t("Weiter", "İleri"))
                                Image(systemName: currentStepIndex == steps.count - 1 ? "checkmark" : "chevron.right")
                            }
                            .font(.headline.bold())
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 13)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(.white)
                        .background(currentStepIndex == steps.count - 1 ? SalahTheme.mutedInk : SalahTheme.deepTeal, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .disabled(currentStepIndex == steps.count - 1)
                    }

                    if currentStepIndex == steps.count - 1 {
                        VStack(alignment: .leading, spacing: 8) {
                            Text(settings.t("Nach dem Wudu", "Abdestten sonra"))
                                .font(.headline)
                            Text("أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ")
                                .font(.title3)
                                .multilineTextAlignment(.trailing)
                                .frame(maxWidth: .infinity, alignment: .trailing)
                            Text("Eşhedü en lâ ilâhe illallâhü vahdehû lâ şerîke leh, ve eşhedü enne Muhammeden abdühû ve resûlüh.")
                                .font(.subheadline.weight(.semibold))
                            Text(settings.t(
                                "Ich bezeuge, dass es keinen Gott außer Allah gibt, ohne Teilhaber, und dass Muhammad Sein Diener und Gesandter ist.",
                                "Allah'tan başka ilâh olmadığına, O'nun ortağı bulunmadığına ve Muhammed'in O'nun kulu ve elçisi olduğuna şahitlik ederim."
                            ))
                            .font(.footnote)
                            .foregroundStyle(.secondary)
                        }
                        .cardStyle()
                    }

                    VStack(alignment: .leading, spacing: 9) {
                        Text(settings.t("Weitere rituelle Reinigung", "Diğer hükmî temizlikler"))
                            .font(.headline.bold())
                            .foregroundStyle(SalahTheme.deepTeal)

                        NavigationLink { GhuslGuideView() } label: {
                            Label(settings.t("Ghusl · Ganzkörperwaschung", "Gusül · boy abdesti"), systemImage: "shower.fill")
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        .buttonStyle(.plain)

                        Divider()

                        NavigationLink { TayammumGuideView() } label: {
                            Label(settings.t("Tayammum · wenn Wasser nicht nutzbar ist", "Teyemmüm · su kullanılamadığında"), systemImage: "hand.raised.fill")
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        .buttonStyle(.plain)
                    }
                    .cardStyle()

                    VStack(alignment: .leading, spacing: 7) {
                        Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama"))
                            .font(.headline)
                        Text(settings.t(
                            "Diyanet Namaz İlmihali und Din İşleri Yüksek Kurulu. Die vier Farz-Bestandteile und die vollständige hanafitische Lernreihenfolge werden direkt in SalahPath erklärt. Nacken/Ense ist hier als Sunnah dargestellt, nicht als Farz.",
                            "Diyanet Namaz İlmihali ve Din İşleri Yüksek Kurulu. Abdestin dört farzı ve tam Hanefî öğrenme sırası doğrudan SalahPath içinde açıklanır. Boyun/ense burada sünnet olarak gösterilir, farz değildir."
                        ))
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    }
                    .cardStyle(material: true)
                }
                .padding()
            }
            .background(SalahTheme.page)
            .navigationTitle(settings.t("Wudu lernen", "Abdest öğren"))
            .navigationBarTitleDisplayMode(.inline)
            .onAppear {
                guard currentStepIndex > 0 else { return }
                Task { @MainActor in
                    await Task.yield()
                    proxy.scrollTo("wudu-step-card-\(currentStepIndex)", anchor: .top)
                }
            }
        }
    }

    @ViewBuilder
    private func wuduStepCard(_ step: WuduTutorialStep) -> some View {
        VStack(spacing: 0) {
            HStack(spacing: 12) {
                Text("\(step.number)")
                    .font(.title3.bold())
                    .frame(width: 40, height: 40)
                    .background(SalahTheme.gold.opacity(0.95), in: Circle())
                    .foregroundStyle(SalahTheme.deepTeal)

                Text(settings.language == .german ? step.deTitle : step.trTitle)
                    .font(.title3.bold())
                    .foregroundStyle(.white)
                    .fixedSize(horizontal: false, vertical: true)

                Spacer(minLength: 6)

                Text(repeatLabel(for: step))
                    .font(.caption.bold())
                    .multilineTextAlignment(.trailing)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 5)
                    .background(Color.white.opacity(0.92), in: Capsule())
                    .foregroundStyle(SalahTheme.deepTeal)
            }
            .padding(14)
            .background(SalahTheme.navigationTeal)

            VStack(alignment: .leading, spacing: 14) {
                if let image = step.image {
                    WuduInstructionVisual(key: image, stepNumber: step.number)
                        .accessibilityElement(children: .ignore)
                        .accessibilityLabel(accessibilityDescription(for: step))
                }

                VStack(alignment: .leading, spacing: 6) {
                    Label(settings.t("SO MACHST DU ES", "BÖYLE YAP"), systemImage: "hand.point.right.fill")
                        .font(.caption.bold())
                        .foregroundStyle(SalahTheme.teal)
                    Text(settings.language == .german ? step.deAction : step.trAction)
                        .font(.body)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                }

                DisclosureGroup(isExpanded: $showExactDetail) {
                    Text(exactDetail(for: step.number))
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.mutedInk)
                        .fixedSize(horizontal: false, vertical: true)
                        .padding(.top, 5)
                } label: {
                    Label(settings.t("Ganz genau", "Ayrıntılı anlatım"), systemImage: "magnifyingglass")
                        .font(.subheadline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                }
            }
            .padding(16)
            .background(SalahTheme.cream)
        }
        .clipShape(RoundedRectangle(cornerRadius: 22, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 22, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.65), lineWidth: 1)
        }
    }

    private func repeatLabel(for step: WuduTutorialStep) -> String {
        if [6, 7, 8, 12, 13].contains(step.number) {
            return settings.t("1× Farz · 3× Sunnah", "1× Farz · 3× Sünnet")
        }
        if step.number == 9 { return "1×" }
        if let repeatText = step.repeatText {
            return settings.t("\(repeatText) Sunnah", "\(repeatText) Sünnet")
        }
        return settings.t("Sunnah", "Sünnet")
    }

    private func exactDetail(for number: Int) -> String {
        let de: [Int: String] = [
            1: "Die Absicht ist im Herzen. Du musst keinen bestimmten deutschen oder arabischen Satz laut sprechen.",
            2: "Sprich Bismillāh vor dem eigentlichen Waschen. Es ist in dieser hanafitischen Lernreihenfolge Sunnah, nicht einer der vier Farz-Bestandteile.",
            3: "Wasche Handflächen, Handrücken, Finger und Fingerzwischenräume bis einschließlich Handgelenk. Schmuck darf Wasser nicht von der Haut abhalten.",
            4: "Nimm Wasser mit der rechten Hand in den Mund und spüle gründlich. Beim Fasten nicht übertreiben, damit kein Wasser geschluckt wird.",
            5: "Nimm das Wasser mit der rechten Hand zur Nase. Nach jedem Einziehen wird die Nase mit der linken Hand gereinigt bzw. geschnäuzt. Beim Fasten nicht tief hochziehen, damit kein Wasser in den Rachen gelangt.",
            6: "Gesichtsgrenze: oben der normale Haaransatz, unten das Kinn, seitlich ungefähr von Ohr zu Ohr. Wasser muss die gesamte zu waschende Haut erreichen. Bei dichtem Bart die Haare mit den Fingern durchfahren, damit Wasser gut verteilt wird.",
            7: "Beginne bei der rechten Hand und wasche bis über den Ellenbogen. Drehe den Arm so, dass Innen- und Außenseite sowie der Ellenbogen sicher nass werden.",
            8: "Genauso links: von der Hand bis einschließlich Ellenbogen. Kontrolliere besonders den Ellenbogen und Stellen unter eng anliegendem Schmuck.",
            9: "Masah bedeutet wischen, nicht den Kopf wie das Gesicht waschen. Die Hände sind feucht. Hanafi: mindestens ein Viertel des Kopfes ist Farz; die vollständige Kopf-Masah wird als Sunnah gezeigt.",
            10: "Mit feuchten Fingern die Innenbereiche der Ohren vorsichtig wischen, außen mit den Daumen. Kein Wasser tief in den Gehörgang drücken.",
            11: "Dieser Schritt ist NICHT Farz. In der Diyanet/Hanafi-Darstellung wird die Ense/Nackenpartie mit feuchten Fingerrücken gewischt. Die Vorderseite des Halses bzw. Kehle nicht wischen.",
            12: "Wasche Oberseite, Sohle, Ferse, beide Knöchel und die Zehenzwischenräume. Erst wenn überall Wasser angekommen ist, ist der Fuß vollständig gewaschen.",
            13: "Wie beim rechten Fuß: Oberseite, Sohle, Ferse, beide Knöchel und alle Zehenzwischenräume vollständig erreichen."
        ]
        let tr: [Int: String] = [
            1: "Niyet kalptedir. Belirli bir Türkçe veya Arapça cümleyi sesli söylemek zorunda değilsin.",
            2: "Asıl yıkamaya başlamadan önce Bismillāh de. Bu Hanefî öğrenme sıralamasında sünnettir; dört farzdan biri değildir.",
            3: "Avuçları, el üstlerini, parmakları ve parmak aralarını bileklerle birlikte yıka. Takı suyun deriye ulaşmasını engellememeli.",
            4: "Sağ elle ağza su alıp iyice çalkala. Oruçluyken suyun yutulmaması için aşırıya kaçma.",
            5: "Suyu sağ elinle burnuna ver. Her çekişten sonra sol elle burnunu temizleyip sümkür. Oruçluyken suyun boğaza kaçmaması için derine çekme.",
            6: "Yüz sınırı: normal saç çizgisinden çeneye, yanlarda yaklaşık bir kulaktan diğer kulağa kadar. Yıkanması gereken her yere su ulaşmalı. Sık sakalda suyun iyi dağılması için parmaklarla arala.",
            7: "Sağ elden başlayıp dirsek dahil kolu yıka. Kolun içi, dışı ve dirseğin tamamen ıslandığından emin ol.",
            8: "Aynı şekilde sol eli ve kolu dirsek dahil yıka. Özellikle dirsek ve sıkı takı altlarını kontrol et.",
            9: "Mesh, başı yüz gibi yıkamak değil, ıslak elle silmektir. Hanefî: başın en az dörtte birini mesh etmek farzdır; tam baş meshi sünnet olarak gösterilir.",
            10: "Islak parmaklarla kulakların iç kısmını nazikçe, dışını başparmaklarla mesh et. Suyu kulak kanalına derin itme.",
            11: "Bu adım farz DEĞİLDİR. Diyanet/Hanefî anlatımında ense ıslak parmakların dış kısmıyla mesh edilir. Boğazın ön tarafı mesh edilmez.",
            12: "Ayağın üstünü, tabanını, topuğunu, iki aşık kemiğini ve parmak aralarını yıka. Her yere su ulaşınca ayak tamamen yıkanmış olur.",
            13: "Sağ ayakta olduğu gibi ayağın üstü, tabanı, topuğu, iki aşık kemiği ve bütün parmak aralarına su ulaştır."
        ]
        return settings.language == .german ? (de[number] ?? "") : (tr[number] ?? "")
    }

    private func accessibilityDescription(for step: WuduTutorialStep) -> String {
        settings.language == .german
            ? "Wudu Schritt \(step.number): \(step.deTitle). \(step.deAction)"
            : "Abdest adım \(step.number): \(step.trTitle). \(step.trAction)"
    }

}


// MARK: - Ghusl and Tayammum

struct GhuslGuideView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 8) {
                    Label(settings.t("Was ist Ghusl?", "Gusül nedir?"), systemImage: "shower.fill")
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Ghusl ist die rituelle Ganzkörperwaschung. Sie wird nötig, wenn der Zustand großer ritueller Unreinheit beendet werden muss, zum Beispiel nach Geschlechtsverkehr, nach Samenerguss oder nach einem feuchten Traum, wenn beim Aufwachen entsprechende Flüssigkeit festgestellt wird, sowie nach Ende von Menstruation oder Wochenbett.",
                        "Gusül, hükmî büyük kirlilik hâlini gidermek için yapılan boy abdestidir. Cinsel ilişki, meni gelmesi veya ihtilamdan sonra uyandığında ıslaklık görülmesi ile hayız ya da nifasın sona ermesi gibi durumlarda gerekir."
                    ))
                    .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 9) {
                    Text(settings.t("Die 3 Farz im Hanafi/Diyanet-Ablauf", "Hanefî/Diyanet'e göre 3 farz"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    numbered("1", settings.t(
                        "Den Mund vollständig ausspülen, sodass Wasser den ganzen Mundraum erreicht.",
                        "Ağzı, su ağız boşluğunun her yerine ulaşacak şekilde tamamen çalkalamak."
                    ))
                    numbered("2", settings.t(
                        "Wasser in die Nase geben und die Nase reinigen.",
                        "Buruna su vermek ve burnu temizlemek."
                    ))
                    numbered("3", settings.t(
                        "Den gesamten Körper waschen, ohne eine waschpflichtige Stelle trocken zu lassen.",
                        "Yıkanması gereken hiçbir yeri kuru bırakmadan bütün bedeni yıkamak."
                    ))

                    Text(settings.t(
                        "Wichtig: Nach hanafitischer Auffassung gehören Mund und Nase zum Farz des Ghusl. Niyyah und Bismillah sind Sunnah. In anderen Rechtsschulen kann die Einordnung einzelner Punkte abweichen.",
                        "Önemli: Hanefî görüşte ağız ve burun guslün farzlarındandır. Niyet ve besmele sünnettir. Diğer mezheplerde bazı ayrıntıların hükmü farklı olabilir."
                    ))
                    .font(.footnote.bold())
                    .foregroundStyle(SalahTheme.deepTeal)
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Vollständiger Sunnah-Ablauf", "Sünnete uygun tam uygulama"))
                        .font(.headline.bold())

                    step("1", settings.t("Absicht fassen und Bismillah sagen.", "Niyet et ve besmele çek."))
                    step("2", settings.t("Hände waschen. Sichtbare Verunreinigung am Körper entfernen und Intimbereich reinigen.", "Ellerini yıka. Bedendeki görünen necaseti gider ve avret bölgesini temizle."))
                    step("3", settings.t("Mund gründlich 3× ausspülen.", "Ağzı 3 kez iyice çalkala."))
                    step("4", settings.t("Nase 3× mit Wasser reinigen.", "Burnu 3 kez suyla temizle."))
                    step("5", settings.t("Wudu wie für das Gebet durchführen. Wenn sich Wasser am Boden sammelt, können die Füße bis zum Ende warten.", "Namaz abdesti gibi abdest al. Su ayak altında birikiyorsa ayakları sona bırakabilirsin."))
                    step("6", settings.t("Den ganzen Körper vollständig waschen. Wasser muss Haut und erreichbare Haarbereiche überall erreichen.", "Bütün bedeni tamamen yıka. Su derinin ve ulaşılabilir saç bölgelerinin her yerine ulaşmalı."))
                    step("7", settings.t("Besonders kontrollieren: Haaransatz, hinter den Ohren, Bauchnabel, Achseln, Hautfalten, zwischen Fingern und Zehen sowie Stellen unter Schmuck.", "Özellikle saç diplerini, kulak arkasını, göbeği, koltuk altını, deri kıvrımlarını, parmak aralarını ve takı altlarını kontrol et."))
                    step("8", settings.t("Falls die Füße vorher ausgelassen wurden, zum Schluss vollständig waschen.", "Ayaklar önce bırakıldıysa sonunda tamamen yıka."))
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 8) {
                    Text(settings.t("Haare & Frauen", "Saç ve kadınlar"))
                        .font(.headline.bold())
                    Text(settings.t(
                        "Das Wasser muss die Kopfhaut und die Haarwurzeln erreichen. Bei zusammengebundenen oder geflochtenen Haaren ist entscheidend, dass Wasser die Wurzeln erreicht; unnötiges Erschweren soll vermieden werden. Bei konkreten Fragen zu sehr dichtem Haar, Extensions oder wasserundurchlässigen Produkten die hanafitische Regel gezielt prüfen.",
                        "Su saç derisine ve saç diplerine ulaşmalıdır. Toplu veya örgülü saçta önemli olan suyun köklere ulaşmasıdır; gereksiz zorluk çıkarılmaz. Çok sık saç, ek saç veya su geçirmeyen ürünler gibi özel durumda Hanefî hükmü ayrıca kontrol edilmelidir."
                    ))
                    .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 8) {
                    Text(settings.t("Brauche ich danach noch Wudu?", "Sonra yeniden abdest gerekir mi?"))
                        .font(.headline.bold())
                    Text(settings.t(
                        "Ein gültiger Ghusl umfasst auch Wudu. Wenn während oder nach dem Ghusl nichts passiert, was Wudu bricht, ist danach kein zusätzliches Wudu nötig.",
                        "Geçerli bir gusül abdesti de kapsar. Gusül sırasında veya sonrasında abdesti bozan bir durum olmazsa ayrıca yeniden abdest almak gerekmez."
                    ))
                }
                .cardStyle(material: true)

                sourceNote
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Ghusl lernen", "Gusül öğren"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func numbered(_ n: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Text(n)
                .font(.caption.bold())
                .foregroundStyle(.white)
                .frame(width: 26, height: 26)
                .background(SalahTheme.teal, in: Circle())
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }

    @ViewBuilder
    private func step(_ n: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Text(n)
                .font(.caption.bold())
                .foregroundStyle(SalahTheme.deepTeal)
                .frame(width: 26, height: 26)
                .background(SalahTheme.gold.opacity(0.22), in: Circle())
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }

    private var sourceNote: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama")).font(.headline)
            Text(settings.t(
                "Qur'an 4:43 und 5:6 · Diyanet Din İşleri Yüksek Kurulu: Ghusl/Boy abdesti. Darstellung: hanafitischer Grundablauf.",
                "Kur'an 4:43 ve 5:6 · Diyanet Din İşleri Yüksek Kurulu: Gusül/boy abdesti. Anlatım: Hanefî temel uygulama."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }
}

struct TayammumGuideView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 8) {
                    Label(settings.t("Was ist Tayammum?", "Teyemmüm nedir?"), systemImage: "hand.raised.fill")
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Tayammum ist eine erlaubte Ersatzreinigung, wenn kein Wasser vorhanden ist oder Wasser aus einem anerkannten Grund nicht benutzt werden kann. Es ersetzt unter diesen Voraussetzungen Wudu oder Ghusl.",
                        "Teyemmüm, su bulunmadığında veya geçerli bir sebeple su kullanılamadığında yapılan hükmî temizliktir. Şartları oluştuğunda abdestin veya guslün yerine geçer."
                    ))
                    .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 9) {
                    Text(settings.t("Wann darf ich Tayammum machen?", "Ne zaman teyemmüm yapılır?"))
                        .font(.headline.bold())
                    bullet(settings.t("Es ist kein ausreichendes Wasser erreichbar.", "Yeterli su bulunamıyor veya ulaşılamıyor."))
                    bullet(settings.t("Wasser zu benutzen würde wegen Krankheit oder Verletzung voraussichtlich schaden.", "Hastalık veya yara nedeniyle su kullanmak zarar verecek."))
                    bullet(settings.t("Eine anerkannte Unmöglichkeit der Wassernutzung liegt vor; bloße Bequemlichkeit reicht nicht.", "Suyu kullanmaya gerçek bir engel var; yalnız kolaylık istemek yeterli değildir."))
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Tayammum Schritt für Schritt", "Teyemmüm adım adım"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    step("1", settings.t(
                        "Fasse die Absicht, Tayammum für Wudu oder Ghusl zu machen.",
                        "Abdest veya gusül yerine teyemmüm etmeye niyet et."
                    ))
                    step("2", settings.t(
                        "Lege bzw. schlage beide geöffneten Hände auf saubere Erde oder etwas von erdiger/mineralischer Art. Bewege sie leicht vor und zurück und klopfe überschüssigen Staub ab.",
                        "Parmaklar açık şekilde iki elini temiz toprağa veya toprak cinsinden bir yüzeye vur/temas ettir; hafifçe ileri geri hareket ettir ve fazla tozu silk."
                    ))
                    step("3", settings.t(
                        "Wische mit beiden Handflächen das gesamte Gesicht einmal.",
                        "İki elin içiyle yüzün tamamını bir kez mesh et."
                    ))
                    step("4", settings.t(
                        "Berühre die saubere Erdoberfläche ein zweites Mal.",
                        "Ellerini temiz toprağa ikinci kez temas ettir."
                    ))
                    step("5", settings.t(
                        "Wische zuerst den rechten Arm einschließlich Ellenbogen mit der linken Hand.",
                        "Sol elinle sağ kolu dirsekle birlikte mesh et."
                    ))
                    step("6", settings.t(
                        "Wische danach den linken Arm einschließlich Ellenbogen mit der rechten Hand.",
                        "Sağ elinle sol kolu dirsekle birlikte mesh et."
                    ))
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 9) {
                    Text(settings.t("Was beendet Tayammum?", "Teyemmümü ne bozar?"))
                        .font(.headline.bold())
                    bullet(settings.t("Alles, was normalerweise Wudu bricht, beendet auch Tayammum.", "Abdesti bozan şeyler teyemmümü de bozar."))
                    bullet(settings.t("Wenn wieder ausreichend Wasser verfügbar und nutzbar wird, endet die Tayammum-Erlaubnis.", "Yeterli su bulunur ve kullanılabilir hale gelirse teyemmüm ruhsatı sona erer."))
                    bullet(settings.t("Wenn der medizinische oder andere Grund entfällt, der Wasser unmöglich machte, endet die Ersatzregel.", "Suyu kullanmaya engel olan hastalık veya diğer mazeret ortadan kalkarsa teyemmüm hükmü sona erer."))
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 6) {
                    Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama")).font(.headline)
                    Text(settings.t(
                        "Qur'an 4:43 und 5:6 · Diyanet Din İşleri Yüksek Kurulu: Tayammum. Darstellung: hanafitischer Grundablauf.",
                        "Kur'an 4:43 ve 5:6 · Diyanet Din İşleri Yüksek Kurulu: Teyemmüm. Anlatım: Hanefî temel uygulama."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Tayammum lernen", "Teyemmüm öğren"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func step(_ n: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Text(n)
                .font(.caption.bold())
                .foregroundStyle(.white)
                .frame(width: 26, height: 26)
                .background(SalahTheme.teal, in: Circle())
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }

    @ViewBuilder
    private func bullet(_ text: String) -> some View {
        HStack(alignment: .top, spacing: 9) {
            Image(systemName: "checkmark.circle.fill")
                .foregroundStyle(SalahTheme.teal)
                .padding(.top, 2)
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }
}

// MARK: - Terms


struct PrayerTermsView: View {
    @EnvironmentObject private var settings: SettingsStore
    private let terms: [(String,String,String)] = [
        ("Fard / Farz", "Pflichtbestandteil oder Pflichtgebet.", "Yapılması kesin olarak gerekli ibadet veya namaz bölümü."),
        ("Sunnah / Sünnet", "Überlieferte und empfohlene Praxis des Propheten ﷺ; juristische Einordnung kann variieren.", "Peygamberimizin ﷺ uyguladığı ve tavsiye edilen amel; fıkhî derecesi değişebilir."),
        ("Wajib / Vacip", "Im hanafitischen Fiqh eine starke Verpflichtungsstufe unter Fard.", "Hanefî fıkhında farzdan sonra gelen güçlü yükümlülük derecesi."),
        ("Rakʿah / Rekât", "Eine Gebetseinheit aus Stehen, Rukūʿ und zwei Sujūd.", "Kıyam, rükû ve iki secdeden oluşan namaz birimi."),
        ("Rukūʿ / Rükû", "Verbeugung im Gebet.", "Namazdaki eğilme bölümü."),
        ("Sujūd / Secde", "Niederwerfung im Gebet.", "Namazdaki secde bölümü."),
        ("Qibla / Kıble", "Gebetsrichtung zur Kaaba in Mekka.", "Mekke'deki Kâbe yönü."),
        ("Adhān / Ezan", "Gebetsruf zum Beginn der Gebetszeit.", "Namaz vaktini bildiren çağrı."),
        ("Iqāmah / Kamet", "Kurzer Ruf unmittelbar vor dem Gemeinschaftsgebet.", "Cemaat namazından hemen önce okunan çağrı."),
        ("Dhikr / Zikir", "Gedenken Allahs durch Worte, Duʿāʾ und Qurʾān-Rezitation.", "Allah'ı söz, dua ve Kur'an ile anmak."),
        ("Witr / Vitir", "Gebet nach Isha; hanafitisch drei Rakʿat wajib.", "Yatsıdan sonra kılınır; Hanefî mezhebinde üç rekât vaciptir.")
    ]

    var body: some View {
        List(terms, id: \.0) { term in
            VStack(alignment:.leading,spacing:4) {
                Text(term.0).font(.headline)
                Text(settings.language == .german ? term.1 : term.2).font(.subheadline).foregroundStyle(.secondary)
            }.padding(.vertical,3)
        }.scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Begriffe", "Kavramlar"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Complete prayer catalogue

private struct PrayerCatalogItem: Identifiable {
    let id: String
    let group: String
    let deTitle: String
    let trTitle: String
    let deRuling: String
    let trRuling: String
    let rakaLabel: String
    let deSummary: String
    let trSummary: String
    let deSteps: [String]
    let trSteps: [String]
    let deNotes: [String]
    let trNotes: [String]
    let source: String
}

struct PrayerCatalogView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var search = ""

    private var items: [PrayerCatalogItem] {
        [
            .init(
                id: "fajr_sunnah", group: "daily",
                deTitle: "Fajr · 2 Sunnah", trTitle: "Sabah · 2 Rekât Sünnet",
                deRuling: "Sunnah muʾakkadah", trRuling: "Sünnet-i müekkede", rakaLabel: "2",
                deSummary: "Die stark betonte Sunnah unmittelbar vor dem Fajr-Fard.",
                trSummary: "Sabah farzından önce kılınan kuvvetli sünnet.",
                deSteps: [
                    "1. Rakʿah: Niyyah → Takbir → Sübhaneke → Eʿūḏu/Basmala → Fātiha + Sura → Rukūʿ → 2 Sujud.",
                    "2. Rakʿah: Basmala → Fātiha + Sura → Rukūʿ → 2 Sujud → Schluss-Sitzen.",
                    "Im Schluss-Sitzen: Ettehiyyâtü → Salli → Bârik → Abschlussdua → Salām rechts, dann links."
                ],
                trSteps: [
                    "1. rekât: Niyet → tekbir → Sübhâneke → Eûzü/Besmele → Fâtiha + sûre → rükû → 2 secde.",
                    "2. rekât: Besmele → Fâtiha + sûre → rükû → 2 secde → son oturuş.",
                    "Son oturuşta: Ettehiyyâtü → Salli → Bârik → kapanış duası → önce sağa, sonra sola selâm."
                ],
                deNotes: ["Die PDF beginnt genau mit diesem Gebet und zeigt die Schritte einschließlich Tesbihat."],
                trNotes: ["PDF'deki ayrıntılı namaz anlatımı bu sünnetle başlıyor ve tesbihata kadar ilerliyor."],
                source: "Diyanet · Namaz İlmihali"
            ),
            .init(
                id: "fajr_fard", group: "daily",
                deTitle: "Fajr · 2 Fard", trTitle: "Sabah · 2 Rekât Farz",
                deRuling: "Fard", trRuling: "Farz", rakaLabel: "2",
                deSummary: "Das zweirakʿatige Pflichtgebet des Morgens.",
                trSummary: "Sabah vaktinin iki rekât farz namazı.",
                deSteps: [
                    "Beide Rakʿah folgen dem normalen 2-Rakʿah-Ablauf.",
                    "In beiden Rakʿah werden Fātiha und eine zusätzliche Sura bzw. passende Verse gelesen.",
                    "Nach der zweiten Rakʿah vollständiges Schluss-Sitzen und Salām."
                ],
                trSteps: [
                    "İki rekât da normal 2 rekât düzenine göre kılınır.",
                    "Her iki rekâtta Fâtiha ile birlikte zamm-ı sûre veya yeterli ayet okunur.",
                    "İkinci rekâttan sonra tam son oturuş ve selâm yapılır."
                ],
                deNotes: ["Bei Gemeinschaftsgebet gelten zusätzlich Imam-/Mitbeter-Regeln für die Rezitation."],
                trNotes: ["Cemaatle kılınırken kıraat açısından imam ve cemaat hükümleri ayrıca dikkate alınır."],
                source: "Diyanet · Namaz İlmihali"
            ),
            .init(
                id: "dhuhr_first_sunnah", group: "daily",
                deTitle: "Dhuhr · 4 erste Sunnah", trTitle: "Öğle · 4 Rekât İlk Sünnet",
                deRuling: "Sunnah muʾakkadah", trRuling: "Sünnet-i müekkede", rakaLabel: "4",
                deSummary: "Vier betonte Sunnah-Rakʿah vor dem Dhuhr-Fard.",
                trSummary: "Öğle farzından önceki dört rekât kuvvetli sünnet.",
                deSteps: [
                    "1.–2. Rakʿah: wie ein normales 2-Rakʿah-Gebet; nach Rakʿah 2 nur Ettehiyyâtü lesen.",
                    "Zur 3. Rakʿah aufstehen: Basmala → Fātiha + Sura; danach Rukūʿ und 2 Sujud.",
                    "4. Rakʿah: Basmala → Fātiha + Sura → Rukūʿ → 2 Sujud → vollständiges Schluss-Sitzen → Salām."
                ],
                trSteps: [
                    "1–2. rekât normal 2 rekât düzenindedir; 2. rekât oturuşunda yalnız Ettehiyyâtü okunur.",
                    "3. rekâta kalkınca Besmele → Fâtiha + sûre; ardından rükû ve 2 secde.",
                    "4. rekât: Besmele → Fâtiha + sûre → rükû → 2 secde → tam son oturuş → selâm."
                ],
                deNotes: ["Anders als bei der Asr-/Isha-Vorsunnah wird nach Rakʿah 2 nicht Salli-Bârik gelesen und Rakʿah 3 nicht erneut mit Sübhaneke begonnen."],
                trNotes: ["İkindi/Yatsı ilk sünnetinden farklı olarak 2. rekâtta Salli-Bârik okunmaz; 3. rekâta yeniden Sübhâneke ile başlanmaz."],
                source: "Diyanet · Namaz İlmihali"
            ),
            .init(
                id: "dhuhr_fard", group: "daily",
                deTitle: "Dhuhr · 4 Fard", trTitle: "Öğle · 4 Rekât Farz",
                deRuling: "Fard", trRuling: "Farz", rakaLabel: "4",
                deSummary: "Das vier-rakʿatige Pflichtgebet am Mittag.",
                trSummary: "Öğle vaktinin dört rekât farz namazı.",
                deSteps: [
                    "Rakʿah 1 und 2: Fātiha + zusätzliche Sura/Verse; nach Rakʿah 2 Ettehiyyâtü.",
                    "Rakʿah 3 und 4: im Hanafi-Gebet genügt jeweils Fātiha; danach die normalen Rukūʿ-/Sujud-Schritte.",
                    "Nach Rakʿah 4 vollständiges Schluss-Sitzen und Salām."
                ],
                trSteps: [
                    "1 ve 2. rekât: Fâtiha + zamm-ı sûre/ayet; 2. rekâttan sonra Ettehiyyâtü.",
                    "3 ve 4. rekât: Hanefî farz namazında yalnız Fâtiha okunur; sonra normal rükû ve secdeler.",
                    "4. rekâttan sonra tam son oturuş ve selâm."
                ],
                deNotes: [], trNotes: [],
                source: "Diyanet · Namaz İlmihali"
            ),
            .init(
                id: "dhuhr_last_sunnah", group: "daily",
                deTitle: "Dhuhr · 2 letzte Sunnah", trTitle: "Öğle · 2 Rekât Son Sünnet",
                deRuling: "Sunnah muʾakkadah", trRuling: "Sünnet-i müekkede", rakaLabel: "2",
                deSummary: "Die übliche zweirakʿatige Sunnah nach dem Dhuhr-Fard.",
                trSummary: "Öğle farzından sonra kılınan yaygın iki rekât sünnet.",
                deSteps: [
                    "Wie das zweirakʿatige Fajr-Sunnah-Gebet, nur mit entsprechender Niyyah.",
                    "Beide Rakʿah enthalten Fātiha + zusätzliche Sura/Verse.",
                    "Nach Rakʿah 2 vollständiges Schluss-Sitzen und Salām."
                ],
                trSteps: [
                    "Sabah sünnetinin iki rekât düzeni gibidir; yalnız niyet öğle son sünnetine yapılır.",
                    "Her iki rekâtta Fâtiha + zamm-ı sûre/ayet okunur.",
                    "2. rekâttan sonra tam son oturuş ve selâm."
                ],
                deNotes: ["Diyanet weist darauf hin, dass sie auch vier Rakʿah gebetet werden kann; die verbreitete Praxis sind zwei."],
                trNotes: ["Diyanet'e göre dört rekât da kılınabilir; yaygın uygulama iki rekâttır."],
                source: "Diyanet · Din İşleri Yüksek Kurulu"
            ),
            .init(
                id: "asr_sunnah", group: "daily",
                deTitle: "Asr · 4 Sunnah", trTitle: "İkindi · 4 Rekât Sünnet",
                deRuling: "Sunnah ghayr muʾakkadah", trRuling: "Sünnet-i gayr-i müekkede", rakaLabel: "4",
                deSummary: "Vier freiwillige Sunnah-Rakʿah vor dem Asr-Fard.",
                trSummary: "İkindi farzından önceki dört rekât gayr-i müekked sünnet.",
                deSteps: [
                    "Rakʿah 1–2: normal; im ersten Sitzen Ettehiyyâtü UND Salli-Bârik lesen.",
                    "Rakʿah 3: wieder mit Sübhaneke → Eʿūḏu/Basmala → Fātiha + Sura beginnen.",
                    "Rakʿah 4: Basmala → Fātiha + Sura; anschließend vollständiges Schluss-Sitzen und Salām."
                ],
                trSteps: [
                    "1–2. rekât normaldir; ilk oturuşta Ettehiyyâtü ile birlikte Salli-Bârik okunur.",
                    "3. rekâta Sübhâneke → Eûzü/Besmele → Fâtiha + sûre ile yeniden başlanır.",
                    "4. rekât: Besmele → Fâtiha + sûre; sonra tam son oturuş ve selâm."
                ],
                deNotes: ["Diese Besonderheit gilt ebenso für die erste Sunnah vor dem Isha-Fard."],
                trNotes: ["Aynı özellik Yatsı farzından önceki dört rekât sünnette de vardır."],
                source: "Diyanet · Din İşleri Yüksek Kurulu"
            ),
            .init(
                id: "asr_fard", group: "daily",
                deTitle: "Asr · 4 Fard", trTitle: "İkindi · 4 Rekât Farz",
                deRuling: "Fard", trRuling: "Farz", rakaLabel: "4",
                deSummary: "Vier Pflicht-Rakʿah am Nachmittag.",
                trSummary: "İkindi vaktinin dört rekât farz namazı.",
                deSteps: [
                    "Wie Dhuhr-Fard: in Rakʿah 1–2 Fātiha + zusätzliche Sura/Verse.",
                    "Rakʿah 3–4: Fātiha; normale Rukūʿ-/Sujud-Abfolge.",
                    "Nach Rakʿah 4 vollständiges Schluss-Sitzen und Salām."
                ],
                trSteps: [
                    "Öğle farzı gibidir: 1–2. rekâtta Fâtiha + zamm-ı sûre/ayet.",
                    "3–4. rekâtta Fâtiha; normal rükû ve secde sırası.",
                    "4. rekâttan sonra tam son oturuş ve selâm."
                ],
                deNotes: [], trNotes: [],
                source: "Diyanet · Namaz İlmihali"
            ),
            .init(
                id: "maghrib_fard", group: "daily",
                deTitle: "Maghrib · 3 Fard", trTitle: "Akşam · 3 Rekât Farz",
                deRuling: "Fard", trRuling: "Farz", rakaLabel: "3",
                deSummary: "Das dreirakʿatige Pflichtgebet nach Sonnenuntergang.",
                trSummary: "Akşam vaktinin üç rekât farz namazı.",
                deSteps: [
                    "Rakʿah 1–2: Fātiha + zusätzliche Sura/Verse; nach Rakʿah 2 Ettehiyyâtü.",
                    "Rakʿah 3: Basmala → Fātiha; danach Rukūʿ und 2 Sujud.",
                    "Nach Rakʿah 3 vollständiges Schluss-Sitzen und Salām."
                ],
                trSteps: [
                    "1–2. rekât: Fâtiha + zamm-ı sûre/ayet; 2. rekâttan sonra Ettehiyyâtü.",
                    "3. rekât: Besmele → Fâtiha; sonra rükû ve 2 secde.",
                    "3. rekâttan sonra tam son oturuş ve selâm."
                ],
                deNotes: [], trNotes: [],
                source: "Diyanet · Namaz İlmihali"
            ),
            .init(
                id: "maghrib_sunnah", group: "daily",
                deTitle: "Maghrib · 2 Sunnah", trTitle: "Akşam · 2 Rekât Sünnet",
                deRuling: "Sunnah muʾakkadah", trRuling: "Sünnet-i müekkede", rakaLabel: "2",
                deSummary: "Zwei betonte Sunnah-Rakʿah nach dem Maghrib-Fard.",
                trSummary: "Akşam farzından sonra kılınan iki rekât kuvvetli sünnet.",
                deSteps: ["Normaler 2-Rakʿah-Sunnah-Ablauf mit Fātiha + Sura in beiden Rakʿah.", "Nach Rakʿah 2 vollständiges Schluss-Sitzen und Salām."],
                trSteps: ["İki rekâtta da Fâtiha + sûre okunan normal 2 rekât sünnet düzeni.", "2. rekâttan sonra tam son oturuş ve selâm."],
                deNotes: [], trNotes: [],
                source: "Diyanet · Namaz İlmihali"
            ),
            .init(
                id: "isha_first_sunnah", group: "daily",
                deTitle: "Isha · 4 erste Sunnah", trTitle: "Yatsı · 4 Rekât İlk Sünnet",
                deRuling: "Sunnah ghayr muʾakkadah", trRuling: "Sünnet-i gayr-i müekkede", rakaLabel: "4",
                deSummary: "Vier Sunnah-Rakʿah vor dem Isha-Fard.",
                trSummary: "Yatsı farzından önceki dört rekât gayr-i müekked sünnet.",
                deSteps: [
                    "Wie die vier Sunnah vor Asr.",
                    "Im ersten Sitzen nach Rakʿah 2: Ettehiyyâtü + Salli-Bârik.",
                    "Rakʿah 3 erneut mit Sübhaneke → Eʿūḏu/Basmala → Fātiha + Sura beginnen; Rakʿah 4 ebenso mit Fātiha + Sura."
                ],
                trSteps: [
                    "İkindi sünnetinin dört rekât düzeni gibidir.",
                    "2. rekât ilk oturuşunda Ettehiyyâtü + Salli-Bârik okunur.",
                    "3. rekâta Sübhâneke → Eûzü/Besmele → Fâtiha + sûre ile başlanır; 4. rekâtta da Fâtiha + sûre okunur."
                ],
                deNotes: [], trNotes: [],
                source: "Diyanet · Din İşleri Yüksek Kurulu"
            ),
            .init(
                id: "isha_fard", group: "daily",
                deTitle: "Isha · 4 Fard", trTitle: "Yatsı · 4 Rekât Farz",
                deRuling: "Fard", trRuling: "Farz", rakaLabel: "4",
                deSummary: "Vier Pflicht-Rakʿah in der Nacht.",
                trSummary: "Yatsı vaktinin dört rekât farz namazı.",
                deSteps: ["Wie Dhuhr-/Asr-Fard: Rakʿah 1–2 Fātiha + Sura, Rakʿah 3–4 Fātiha.", "Nach Rakʿah 4 vollständiges Schluss-Sitzen und Salām."],
                trSteps: ["Öğle/ikindi farzı gibi: 1–2. rekâtta Fâtiha + sûre, 3–4. rekâtta Fâtiha.", "4. rekâttan sonra tam son oturuş ve selâm."],
                deNotes: [], trNotes: [],
                source: "Diyanet · Namaz İlmihali"
            ),
            .init(
                id: "isha_last_sunnah", group: "daily",
                deTitle: "Isha · 2 letzte Sunnah", trTitle: "Yatsı · 2 Rekât Son Sünnet",
                deRuling: "Sunnah muʾakkadah", trRuling: "Sünnet-i müekkede", rakaLabel: "2",
                deSummary: "Zwei betonte Sunnah-Rakʿah nach dem Isha-Fard.",
                trSummary: "Yatsı farzından sonra kılınan iki rekât kuvvetli sünnet.",
                deSteps: ["Normaler 2-Rakʿah-Sunnah-Ablauf.", "Beide Rakʿah: Fātiha + Sura; danach Schluss-Sitzen und Salām."],
                trSteps: ["Normal iki rekât sünnet düzeni.", "İki rekâtta da Fâtiha + sûre; ardından son oturuş ve selâm."],
                deNotes: ["Diyanet erwähnt auch die Möglichkeit von vier Rakʿah; verbreitet sind zwei."],
                trNotes: ["Diyanet dört rekât kılınabileceğini de belirtir; yaygın uygulama ikidir."],
                source: "Diyanet · Din İşleri Yüksek Kurulu"
            ),
            .init(
                id: "witr", group: "special",
                deTitle: "Witr · 3 Rakʿah", trTitle: "Vitir · 3 Rekât",
                deRuling: "Hanafi: Wajib", trRuling: "Hanefî: Vacip", rakaLabel: "3",
                deSummary: "Das dreirakʿatige Witr nach Isha mit Qunūt im dritten Rakʿah.",
                trSummary: "Yatsıdan sonra, üçüncü rekâtta kunut bulunan üç rekât vitir.",
                deSteps: [
                    "Rakʿah 1–2: Fātiha + Sura; nach Rakʿah 2 nur Ettehiyyâtü, dann zur dritten aufstehen.",
                    "Rakʿah 3: Fātiha + Sura lesen. Danach zusätzlich Takbir: Hände heben, wieder binden und die Qunūt-Duas lesen.",
                    "Dann Rukūʿ → 2 Sujud → vollständiges Schluss-Sitzen → Salām."
                ],
                trSteps: [
                    "1–2. rekât: Fâtiha + sûre; 2. rekât sonunda yalnız Ettehiyyâtü, sonra üçüncü rekâta kalkılır.",
                    "3. rekât: Fâtiha + sûre. Sonra kunut tekbiri alınır; eller kaldırılıp yeniden bağlanır ve Kunut duaları okunur.",
                    "Ardından rükû → 2 secde → tam son oturuş → selâm."
                ],
                deNotes: ["Wer die bekannten Qunūt-Duas noch nicht kann, soll sie lernen; Diyanet nennt bis dahin u. a. Rabbenā ātinā oder dreimal Allāhumma-ghfir lī als Möglichkeit."],
                trNotes: ["Kunut dualarını bilmeyen kişi öğrenmeye çalışır; öğrenene kadar Diyanet Rabbenâ âtinâ veya üç kez Allahümmağfir lî gibi bir dua zikreder."],
                source: "Diyanet · Din İşleri Yüksek Kurulu"
            ),
            .init(
                id: "eid", group: "special",
                deTitle: "Eid-Gebet", trTitle: "Bayram Namazı",
                deRuling: "Hanafi: Wajib · gemeinschaftlich", trRuling: "Hanefî: Vacip · cemaatle", rakaLabel: "2",
                deSummary: "Zwei Rakʿah mit zusätzlichen Takbiren; danach folgt die Eid-Khutbah.",
                trSummary: "İlave tekbirlerle kılınan iki rekât; ardından bayram hutbesi.",
                deSteps: [
                    "1. Rakʿah: Eröffnungstakbir und Hände binden → Sübhaneke → drei zusätzliche Takbire. Bei den ersten zwei Händen lösen, beim dritten wieder binden.",
                    "Imam rezitiert Fātiha + Sura; danach Rukūʿ und 2 Sujud.",
                    "2. Rakʿah: Imam rezitiert Fātiha + Sura → danach drei zusätzliche Takbire mit Lösen der Hände → mit dem nächsten Takbir direkt in Rukūʿ.",
                    "Nach 2 Sujud Schluss-Sitzen und Salām. Die Eid-Khutbah folgt nach dem Gebet."
                ],
                trSteps: [
                    "1. rekât: İftitah tekbiri ve eller bağlanır → Sübhâneke → üç zevaid tekbiri. İlk ikisinde eller salınır, üçüncüde bağlanır.",
                    "İmam Fâtiha + sûre okur; ardından rükû ve 2 secde.",
                    "2. rekât: İmam Fâtiha + sûre okur → sonra üç zevaid tekbiri alınır ve eller salınır → sonraki tekbirle doğrudan rükûya gidilir.",
                    "2 secdeden sonra son oturuş ve selâm. Bayram hutbesi namazdan sonra okunur."
                ],
                deNotes: ["Keine Adhan/Iqama für das Eid-Gebet."],
                trNotes: ["Bayram namazında ezan ve kamet yoktur."],
                source: "Diyanet · Bayram Namazı"
            ),
            .init(
                id: "tarawih", group: "special",
                deTitle: "Tarawih", trTitle: "Teravih Namazı",
                deRuling: "Sunnah muʾakkadah im Ramadan", trRuling: "Ramazan'da sünnet-i müekkede", rakaLabel: "20*",
                deSummary: "Ramadan-Nachtgebet nach dem Isha-Fard. In der türkisch-hanafitischen Praxis sind 20 Rakʿah etabliert.",
                trSummary: "Yatsı farzından sonra kılınan Ramazan gece namazı. Türkiye Hanefî uygulamasında 20 rekât yerleşmiştir.",
                deSteps: [
                    "Am übersichtlichsten jeweils 2 Rakʿah beten und Salām geben; Diyanet bezeichnet dies als vorzugswürdig.",
                    "Jede 2er-Einheit folgt grundsätzlich dem normalen 2-Rakʿah-Sunnah-Ablauf.",
                    "Nach jeweils vier Rakʿah kann eine kurze Pause eingelegt werden; daher der Name Tarāwīḥ.",
                    "Witr folgt üblicherweise nach Tarawih."
                ],
                trSteps: [
                    "En kolay ve Diyanet'in daha faziletli gördüğü uygulama, ikişer rekât kılıp selâm vermektir.",
                    "Her iki rekâtlık bölüm normal 2 rekât sünnet düzenine göre kılınır.",
                    "Her dört rekâttan sonra kısa dinlenme verilebilir; Teravih adı buradan gelir.",
                    "Vitir genellikle teravihten sonra kılınır."
                ],
                deNotes: ["*Diyanet beschreibt 20 Rakʿah als historisch etablierte Gemeinschaftspraxis, betont aber zugleich, dass Tarawih freiwillig ist und auch eine geringere gerade Zahl gebetet werden kann."],
                trNotes: ["*Diyanet 20 rekâtı yerleşmiş cemaat uygulaması olarak açıklar; teravihin nafile olduğunu ve daha az çift rekâtla da kılınabileceğini belirtir."],
                source: "Diyanet · Din İşleri Yüksek Kurulu"
            ),
            .init(
                id: "tasbih_prayer", group: "special",
                deTitle: "Tasbih-Gebet", trTitle: "Tesbih Namazı",
                deRuling: "Nafila", trRuling: "Nafile", rakaLabel: "4",
                deSummary: "Vier Rakʿah mit insgesamt 300 Wiederholungen des bekannten Tasbih.",
                trSummary: "Toplam 300 tesbih içeren dört rekât nafile namaz.",
                deSteps: [
                    "Nach Sübhaneke 15×: Subḥānallāhi wa-l-ḥamdu lillāhi wa lā ilāha illallāhu wa-llāhu akbar.",
                    "Nach Fātiha + Sura 10×; im Rukūʿ 10×; nach dem Aufrichten 10×; in Sujud 1 10×; im Sitzen 10×; in Sujud 2 10×.",
                    "So entstehen 75 Tasbih pro Rakʿah. Vier Rakʿah ergeben 300."
                ],
                trSteps: [
                    "Sübhâneke'den sonra 15×: Sübhânellâhi ve'l-hamdülillâhi velâ ilâhe illallâhü vallâhü ekber.",
                    "Fâtiha + sûreden sonra 10×; rükûda 10×; doğrulunca 10×; 1. secdede 10×; oturuşta 10×; 2. secdede 10×.",
                    "Böylece her rekâtta 75, dört rekâtta toplam 300 tesbih olur."
                ],
                deNotes: ["Diyanet empfiehlt, dieses Nafila-Gebet allein zu beten und nicht in den verbotenen/makruh Gebetszeiten."],
                trNotes: ["Diyanet bu nafile namazın tek başına kılınmasını ve kerahat vakitlerinde kılınmamasını belirtir."],
                source: "Diyanet · Din İşleri Yüksek Kurulu"
            ),
            .init(
                id: "jumuah", group: "special",
                deTitle: "Freitagsgebet", trTitle: "Cuma Namazı",
                deRuling: "Fard für Verpflichtete · gemeinschaftlich", trRuling: "Yükümlüler için farz · cemaatle", rakaLabel: "2 Fard",
                deSummary: "Das Freitagsgebet ersetzt für Verpflichtete am Freitag das Dhuhr-Fard und enthält eine verpflichtende Khutbah.",
                trSummary: "Yükümlüler için cuma günü öğle farzı yerine kılınan, hutbeli cemaat namazı.",
                deSteps: [
                    "Verbreitete hanafitische Praxis: 4 Sunnah vor dem Fard.",
                    "Khutbah anhören; danach 2 Rakʿah Fard hinter dem Imam.",
                    "Danach nach Abū Ḥanīfa 4 Sunnah; bei den hanafitischen Schülern ist auch eine zusätzliche 2er-Einheit überliefert."
                ],
                trSteps: [
                    "Yaygın Hanefî uygulaması: farzdan önce 4 rekât sünnet.",
                    "Hutbeyi dinle; ardından imam arkasında 2 rekât cuma farzı.",
                    "Ardından Ebû Hanîfe'ye göre 4 rekât sünnet; Hanefî imameyn görüşünde ilave 2 rekât da aktarılmıştır."
                ],
                deNotes: ["Die 2 Fard werden vom Imam laut rezitiert."],
                trNotes: ["İki rekât farzda imam kıraati sesli yapar."],
                source: "Diyanet · Cuma Namazı"
            ),
            .init(
                id: "janazah", group: "special",
                deTitle: "Totengebet", trTitle: "Cenaze Namazı",
                deRuling: "Fard kifāyah", trRuling: "Farz-ı kifâye", rakaLabel: "4 Takbir",
                deSummary: "Stehendes Gebet ohne Rukūʿ und Sujud; vier Takbire.",
                trSummary: "Rükû ve secdesi olmayan, ayakta dört tekbirle kılınan namaz.",
                deSteps: [
                    "Zur Qibla und zum Verstorbenen ausrichten, Niyyah; Eröffnungstakbir und Hände binden.",
                    "Sübhaneke mit „wa jalla thanāʾuk“; zweiter Takbir ohne erneutes Händeheben → Salli/Bārik.",
                    "Dritter Takbir → Janazah-Dua bzw. passende Dua; vierter Takbir → Salām rechts und links."
                ],
                trSteps: [
                    "Kıbleye ve cenazeye dön, niyet et; iftitah tekbiri alıp elleri bağla.",
                    "„Ve celle senâük“ ile Sübhâneke; elleri kaldırmadan ikinci tekbir → Salli/Bârik.",
                    "Üçüncü tekbir → cenaze duası veya uygun dua; dördüncü tekbir → sağa ve sola selâm."
                ],
                deNotes: ["Kein Rukūʿ und kein Sujud."],
                trNotes: ["Rükû ve secde yoktur."],
                source: "Diyanet · Din İşleri Yüksek Kurulu"
            ),
            .init(
                id: "tesbihat", group: "after",
                deTitle: "Tesbihat nach dem Gebet", trTitle: "Namaz Sonrası Tesbihat",
                deRuling: "Dhikr/Dua", trRuling: "Zikir/Dua", rakaLabel: "—",
                deSummary: "Dhikr und Dua nach dem Pflichtgebet; die PDF zeigt diesen Abschnitt direkt nach dem Fajr-Beispiel.",
                trSummary: "Farz namazdan sonra zikir ve dua; PDF'de sabah örneğinin hemen ardından gösteriliyor.",
                deSteps: [
                    "Nach dem Gebet Istighfār und die bekannten Abschluss-Duas sprechen.",
                    "Āyat al-Kursī lesen.",
                    "33× Subḥānallāh, 33× al-ḥamdu lillāh, 33× Allāhu akbar; anschließend den Dhikr vervollständigen und Dua machen."
                ],
                trSteps: [
                    "Namazdan sonra istiğfar ve bilinen kapanış dualarını oku.",
                    "Âyetel Kürsî'yi oku.",
                    "33× Sübhânallah, 33× Elhamdülillah, 33× Allahü ekber; ardından zikri tamamlayıp dua et."
                ],
                deNotes: ["SalahPath hat dafür bereits Dhikr- und Dua-Bereiche; dieser Eintrag verbindet sie mit dem Gebetsablauf."],
                trNotes: ["SalahPath'te zikir ve dua alanları zaten var; bu bölüm onları namaz akışıyla birleştiriyor."],
                source: "PDF-Referenz + Diyanet · Ezan, Kamet ve Tesbihat"
            )
        ]
    }

    private var filteredItems: [PrayerCatalogItem] {
        let q = search.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !q.isEmpty else { return items }
        return items.filter {
            $0.deTitle.localizedCaseInsensitiveContains(q) ||
            $0.trTitle.localizedCaseInsensitiveContains(q) ||
            $0.deRuling.localizedCaseInsensitiveContains(q) ||
            $0.trRuling.localizedCaseInsensitiveContains(q)
        }
    }

    private var dailyItems: [PrayerCatalogItem] { filteredItems.filter { $0.group == "daily" } }
    private var specialItems: [PrayerCatalogItem] { filteredItems.filter { $0.group == "special" } }
    private var afterItems: [PrayerCatalogItem] { filteredItems.filter { $0.group == "after" } }

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("Alle Gebete aus der PDF-Struktur", "PDF yapısındaki tüm namazlar"), systemImage: "list.bullet.rectangle.portrait.fill")
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Nicht nur ein allgemeiner 2-Rakʿah-Ablauf: hier findest du die einzelnen Tagesgebete und die Sondergebete, die im PDF-Menü separat aufgeführt sind.",
                        "Yalnız genel bir 2 rekât anlatımı değil: PDF menüsünde ayrı gösterilen vakit namazlarını ve özel namazları burada tek tek bulabilirsin."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .padding(.vertical, 3)
            }

            Section {
                HStack(spacing: 8) {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(SalahTheme.teal)
                    TextField(settings.t("Gebet suchen", "Namaz ara"), text: $search)
                }
            }

            if !dailyItems.isEmpty {
                Section(settings.t("Tagesgebete", "Vakit Namazları")) {
                    ForEach(dailyItems) { item in
                        NavigationLink { PrayerCatalogDetailView(item: item) } label: {
                            prayerRow(item)
                        }
                    }
                }
            }

            if !specialItems.isEmpty {
                Section(settings.t("Sondergebete", "Özel Namazlar")) {
                    ForEach(specialItems) { item in
                        NavigationLink { PrayerCatalogDetailView(item: item) } label: {
                            prayerRow(item)
                        }
                    }
                }
            }

            if !afterItems.isEmpty {
                Section(settings.t("Nach dem Gebet", "Namaz Sonrası")) {
                    ForEach(afterItems) { item in
                        NavigationLink { PrayerCatalogDetailView(item: item) } label: {
                            prayerRow(item)
                        }
                    }
                }
            }
        }
        .navigationTitle(settings.t("Alle Gebete", "Tüm Namazlar"))
        .navigationBarTitleDisplayMode(.inline)
    }

    private func prayerRow(_ item: PrayerCatalogItem) -> some View {
        HStack(spacing: 10) {
            Text(item.rakaLabel)
                .font(.caption.bold().monospacedDigit())
                .foregroundStyle(SalahTheme.deepTeal)
                .frame(width: 42, height: 42)
                .background(SalahTheme.gold.opacity(0.18), in: Circle())

            VStack(alignment: .leading, spacing: 2) {
                Text(settings.language == .german ? item.deTitle : item.trTitle)
                    .font(.headline)
                Text(settings.language == .german ? item.deRuling : item.trRuling)
                    .font(.caption)
                    .foregroundStyle(SalahTheme.teal)
            }
        }
    }
}

private struct PrayerCatalogDetailView: View {
    @EnvironmentObject private var settings: SettingsStore
    let item: PrayerCatalogItem

    private var steps: [String] { settings.language == .german ? item.deSteps : item.trSteps }
    private var notes: [String] { settings.language == .german ? item.deNotes : item.trNotes }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 8) {
                    HStack(alignment: .top) {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(settings.language == .german ? item.deTitle : item.trTitle)
                                .font(.title2.bold())
                                .foregroundStyle(SalahTheme.deepTeal)
                            Text(settings.language == .german ? item.deRuling : item.trRuling)
                                .font(.subheadline.bold())
                                .foregroundStyle(SalahTheme.teal)
                        }
                        Spacer()
                        Text(item.rakaLabel)
                            .font(.title3.bold().monospacedDigit())
                            .foregroundStyle(SalahTheme.deepTeal)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 8)
                            .background(SalahTheme.gold.opacity(0.18), in: Capsule())
                    }

                    Text(settings.language == .german ? item.deSummary : item.trSummary)
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 10) {
                    Label(settings.t("Ablauf", "Kılınışı"), systemImage: "list.number")
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    ForEach(Array(steps.enumerated()), id: \.offset) { index, step in
                        HStack(alignment: .top, spacing: 9) {
                            Text("\(index + 1)")
                                .font(.caption.bold())
                                .foregroundStyle(SalahTheme.deepTeal)
                                .frame(width: 25, height: 25)
                                .background(SalahTheme.gold.opacity(0.18), in: Circle())
                            Text(step)
                                .font(.subheadline)
                                .foregroundStyle(SalahTheme.ink)
                                .fixedSize(horizontal: false, vertical: true)
                            Spacer(minLength: 0)
                        }
                    }
                }
                .cardStyle()

                if !notes.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Label(settings.t("Wichtig", "Önemli"), systemImage: "info.circle.fill")
                            .font(.headline.bold())
                            .foregroundStyle(SalahTheme.deepTeal)

                        ForEach(Array(notes.enumerated()), id: \.offset) { _, note in
                            Label(note, systemImage: "checkmark.circle")
                                .font(.footnote)
                                .foregroundStyle(SalahTheme.ink)
                                .fixedSize(horizontal: false, vertical: true)
                        }
                    }
                    .cardStyle()
                }

                NavigationLink { PrayerHowToView() } label: {
                    Label(
                        settings.t("Körperhaltungen mit Bildern öffnen", "Hareketleri görsellerle aç"),
                        systemImage: "figure.mind.and.body"
                    )
                    .font(.headline.bold())
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 12)
                }
                .buttonStyle(.borderedProminent)
                .tint(SalahTheme.teal)

                Text(settings.t("Quelle für diese Zusammenfassung: ", "Bu özetin kaynağı: ") + item.source)
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.language == .german ? item.deTitle : item.trTitle)
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Hajj / Umrah and Ramadan hierarchy

struct HajjUmrahGuideView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var section = 0

    private let makkahPlaces = [
        ("Kâbe", "Mescid-i Harâm'ın merkezindeki kıble ve tavafın merkezi.", "Die Kaaba im Zentrum von al-Masjid al-Haram; Qibla und Mittelpunkt des Tawaf."),
        ("Mescid-i Haram", "Kâbe'yi çevreleyen kutsal mescid.", "Die heilige Moschee, die die Kaaba umgibt."),
        ("Safa", "Sa'y ibadetinin başladığı nokta.", "Startpunkt des Saʿy."),
        ("Merve", "Sa'y ibadetinin tamamlandığı nokta.", "Endpunkt des Saʿy."),
        ("Arafat", "Haccın temel rükünlerinden vakfenin yapıldığı bölge.", "Gebiet der Arafat-Wuqūf, eines zentralen Hajj-Ritus."),
        ("Müzdelife", "Arafat'tan sonra vakfe ve geceleme bölgesi.", "Station nach Arafat für Wuqūf/Übernachtung."),
        ("Mina", "Cemrelere taş atma ve hac günlerindeki konaklama bölgesi.", "Bereich für die Jamarat-Riten und Aufenthalt an den Hajj-Tagen.")
    ]

    private let medinaPlaces = [
        ("Mescid-i Nebevî", "Medine'deki Peygamber Mescidi.", "Die Prophetenmoschee in Medina."),
        ("Kubâ Mescidi", "Medine'deki tarihî mescidlerden biri.", "Eine der historischen Moscheen Medinas."),
        ("Uhud", "Uhud Gazvesi'nin gerçekleştiği bölge.", "Gebiet der Schlacht von Uhud."),
        ("Cennetü'l-Bakî", "Medine'deki tarihî mezarlık.", "Historischer Friedhof in Medina.")
    ]

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                Picker("", selection: $section) {
                    Text("Umrah").tag(0)
                    Text("Hajj").tag(1)
                    Text(settings.t("Orte", "Ziyaret")).tag(2)
                    Text(settings.t("Duas", "Dualar")).tag(3)
                }
                .pickerStyle(.segmented)

                switch section {
                case 0: umrahContent
                case 1: hajjContent
                case 2: placesContent
                default: duaContent
                }
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Hajj & Umrah", "Hac & Umre"))
        .navigationBarTitleDisplayMode(.inline)
    }

    private var umrahContent: some View {
        VStack(spacing: 12) {
            infoCard(
                title: settings.t("Umrah Schritt für Schritt", "Umre adım adım"),
                icon: "figure.walk",
                lines: settings.language == .german ? [
                    "Vor dem Überschreiten des Miqāt in Ihram eintreten und die Umrah beabsichtigen; Talbiyah sprechen.",
                    "In al-Masjid al-Haram den Umrah-Tawaf ausführen: sieben Umrundungen ab der Linie des Schwarzen Steins, Kaaba links.",
                    "Nach dem Tawaf zwei Rakʿah Tawaf-Gebet an einem geeigneten Ort verrichten.",
                    "Saʿy: bei Safa beginnen und sieben Teilstrecken gehen – Safa→Marwa zählt als 1, Marwa→Safa als 2; die siebte endet in Marwa.",
                    "Danach Haare kürzen bzw. bei Männern rasieren/kürzen. Damit wird der Ihram beendet."
                ] : [
                    "Mikat sınırını geçmeden ihrama gir, umreye niyet et ve telbiye getir.",
                    "Mescid-i Haram'da umre tavafını yap: Hacerülesved hizasından başlayarak Kâbe sol tarafta kalacak şekilde yedi şavt.",
                    "Tavaftan sonra uygun bir yerde iki rekât tavaf namazı kıl.",
                    "Sa'y: Safa'dan başla ve yedi şavt yap; Safa→Merve 1, Merve→Safa 2 sayılır ve 7. şavt Merve'de biter.",
                    "Ardından saçları kısalt veya erkek için tıraş/kısalt. Böylece ihramdan çıkılır."
                ]
            )

            infoCard(
                title: settings.t("Hanafi-Hinweis", "Hanefî notu"),
                icon: "info.circle.fill",
                lines: settings.language == .german ? [
                    "Tawaf ist für die Umrah grundlegend/fard.",
                    "Saʿy ist im Hanafi-Madhhab wajib und folgt einem gültigen Tawaf.",
                    "Tawaf, Saʿy und anschließendes Haarkürzen möglichst ohne unnötige lange Unterbrechung nacheinander durchführen."
                ] : [
                    "Umre tavafı umrenin farzıdır.",
                    "Sa'y Hanefî mezhebinde vaciptir ve geçerli bir tavaftan sonra yapılır.",
                    "Tavaf, sa'y ve ardından saç tıraşını gereksiz uzun ara vermeden peş peşe yapmak sünnettir."
                ]
            )
        }
    }

    private var hajjContent: some View {
        VStack(spacing: 12) {
            infoCard(
                title: settings.t("Hajj-Ablauf · Orientierung", "Hac akışı · genel rehber"),
                icon: "map.fill",
                lines: settings.language == .german ? [
                    "Für Hajj gibt es Ifrād, Qirān und Tamattuʿ; einzelne Schritte und Ihram-Zeitpunkte unterscheiden sich deshalb.",
                    "Zu den zentralen Hajj-Riten gehören Ihram/Niyyah, Arafat-Wuqūf, Muzdalifah, die Riten in Mina, Tawaf az-Ziyārah/Ifāḍah und – je nach Hajj-Form und Reihenfolge – Saʿy.",
                    "Für die konkrete Reise soll der Ablauf der eigenen Hajj-Art und die Anleitung der zuständigen Hajj-Gruppe/Religionsbegleitung beachtet werden.",
                    "SalahPath verwendet diesen Bereich als Lernübersicht und ersetzt keine individuelle Fatwa bei Fehlern, Krankheit, Menstruation oder ausgelassenen Riten."
                ] : [
                    "Hac; ifrad, kıran ve temettu çeşitlerine ayrılır. Bu nedenle bazı ihram zamanları ve ayrıntılar değişir.",
                    "Temel hac menasiki arasında ihram/niyet, Arafat vakfesi, Müzdelife, Mina'daki görevler, ziyaret/ifâda tavafı ve hac türüne göre sa'y bulunur.",
                    "Gerçek yolculukta kendi hac türünün sırasına ve kafile din görevlisinin rehberliğine uy.",
                    "SalahPath bu alanı öğrenme özeti olarak sunar; eksik menasik, hastalık veya özel hâller için kişisel fetvanın yerini tutmaz."
                ]
            )

            infoCard(
                title: settings.t("Tawaf", "Tavaf"),
                icon: "arrow.triangle.2.circlepath",
                lines: settings.language == .german ? [
                    "Ein Tawaf besteht aus sieben Shawt.",
                    "Beginn an der Linie des Schwarzen Steins; die Kaaba bleibt links.",
                    "Bei großem Gedränge niemals andere Menschen gefährden, nur um Sunnah-Handlungen wie Ramal auszuführen."
                ] : [
                    "Bir tavaf yedi şavttan oluşur.",
                    "Hacerülesved hizasından başlanır ve Kâbe sol tarafta tutulur.",
                    "İzdihamda remel gibi sünnetleri yapacağım diye insanlara eziyet verilmez."
                ]
            )
        }
    }

    private var placesContent: some View {
        VStack(spacing: 12) {
            placeGroup(title: settings.t("Mekka", "Mekke"), items: makkahPlaces)
            placeGroup(title: settings.t("Medina", "Medine"), items: medinaPlaces)
            Text(settings.t(
                "Diese Liste ist eine Lernübersicht. Öffnungszeiten, Zugang, Verkehrsführung und aktuelle Besuchsregeln können sich ändern.",
                "Bu liste öğrenme amaçlı bir özettir. Açılış, erişim, ulaşım ve güncel ziyaret kuralları değişebilir."
            ))
            .font(.caption)
            .foregroundStyle(.secondary)
        }
    }

    private var duaContent: some View {
        VStack(spacing: 12) {
            infoCard(
                title: settings.t("Talbiyah", "Telbiye"),
                icon: "quote.bubble.fill",
                lines: [
                    "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيكَ لَكَ",
                    "Labbayka-llāhumma labbayk, labbayka lā sharīka laka labbayk. Inna-l-ḥamda wa-n-niʿmata laka wa-l-mulk, lā sharīka lak."
                ]
            )

            infoCard(
                title: settings.t("Tawaf- & Saʿy-Duas", "Tavaf ve Sa'y Duaları"),
                icon: "hands.sparkles.fill",
                lines: settings.language == .german ? [
                    "Diyanets Hajj-Ausbildung stellt Duas für einzelne Shawt bereit, erklärt aber ausdrücklich: Diese Formulierungen sind nicht verpflichtend.",
                    "Du darfst Quran-Duas, authentisch überlieferte Duas, Dhikr oder eigene aufrichtige Bitten sprechen.",
                    "Zwischen der jemenitischen Ecke und dem Schwarzen Stein ist „Rabbanā ātinā fi-d-dunyā ḥasanah …“ eine bekannte überlieferte Dua."
                ] : [
                    "Diyanet Hac Eğitimi her şavt için dua örnekleri verir; ancak bu metinlerin okunmasının zorunlu olmadığını açıkça belirtir.",
                    "Kur'an duaları, rivayet edilen dualar, zikirler veya içinden gelen samimi dualar okunabilir.",
                    "Rükn-i Yemânî ile Hacerülesved arasında „Rabbenâ âtinâ fi'd-dünyâ haseneten …“ duası bilinen bir sünnet duadır."
                ]
            )

            NavigationLink { QuranicDuaLibraryView() } label: {
                Label(settings.t("SalahPath Dua-Sammlung öffnen", "SalahPath dua koleksiyonunu aç"), systemImage: "text.book.closed.fill")
                    .font(.headline)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 11)
            }
            .buttonStyle(.borderedProminent)
            .tint(SalahTheme.teal)
        }
    }

    private func infoCard(title: String, icon: String, lines: [String]) -> some View {
        VStack(alignment: .leading, spacing: 9) {
            Label(title, systemImage: icon)
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            ForEach(Array(lines.enumerated()), id: \.offset) { _, line in
                Text(line)
                    .font(line.first?.isArabicLetter == true ? .title3 : .subheadline)
                    .foregroundStyle(SalahTheme.ink)
                    .fixedSize(horizontal: false, vertical: true)
                    .frame(maxWidth: .infinity, alignment: line.first?.isArabicLetter == true ? .trailing : .leading)
            }
        }
        .cardStyle()
    }

    private func placeGroup(title: String, items: [(String, String, String)]) -> some View {
        VStack(alignment: .leading, spacing: 9) {
            Text(title)
                .font(.title3.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            ForEach(Array(items.enumerated()), id: \.offset) { _, item in
                VStack(alignment: .leading, spacing: 3) {
                    Text(item.0)
                        .font(.headline)
                    Text(settings.language == .german ? item.2 : item.1)
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
                .frame(maxWidth: .infinity, alignment: .leading)

                Divider().opacity(0.28)
            }
        }
        .cardStyle()
    }
}

private extension Character {
    var isArabicLetter: Bool {
        unicodeScalars.contains { scalar in
            (0x0600...0x06FF).contains(Int(scalar.value)) ||
            (0x0750...0x077F).contains(Int(scalar.value))
        }
    }
}

struct RamadanGuideIndexView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Die PDF führt Ramadan als eigenen Bereich mit Fastenwissen, Tarawih, Tasbih-/Eid-Gebet, Duas, Quran-Ayat und Laylat al-Qadr. SalahPath verbindet diese Unterpunkte jetzt an einer Stelle.",
                    "PDF Ramazan'ı; oruç bilgisi, teravih, tesbih/bayram namazı, dualar, ayetler ve Kadir Gecesi ile ayrı bir bölüm olarak gösteriyor. SalahPath artık bu alt başlıkları tek yerde topluyor."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Fasten", "Oruç")) {
                NavigationLink { FastingBasicsView() } label: {
                    Label(settings.t("Grundlagen & Weisheiten", "Temel bilgiler & hikmetler"), systemImage: "moon.stars.fill")
                }
                NavigationLink { FastingRulesView() } label: {
                    Label(settings.t("Regeln: was bricht das Fasten?", "Hükümler: orucu ne bozar?"), systemImage: "checklist")
                }
                NavigationLink { FastingExceptionsView() } label: {
                    Label(settings.t("Ausnahmen & Erleichterungen", "Mazeretler & ruhsatlar"), systemImage: "cross.case.fill")
                }
                NavigationLink { FastingTrackerView() } label: {
                    Label(settings.t("Fasten-Tracker", "Oruç takibi"), systemImage: "checkmark.circle.fill")
                }
            }

            Section(settings.t("Ramadan-Gebete", "Ramazan Namazları")) {
                NavigationLink { PrayerCatalogView() } label: {
                    Label(settings.t("Tarawih, Tasbih & Eid-Gebet", "Teravih, Tesbih & Bayram Namazı"), systemImage: "figure.mind.and.body")
                }
            }

            Section(settings.t("Quran & Dua", "Kur'an & Dua")) {
                QuranReferenceLink(
                    surah: 2, ayah: 183,
                    title: settings.t("Fasten-Ayat · Al-Baqara 183 ff.", "Oruç Ayetleri · Bakara 183 vd.")
                )
                QuranReferenceLink(
                    surah: 97, ayah: 1,
                    title: settings.t("Laylat al-Qadr · Sura 97", "Kadir Gecesi · Kadir Sûresi")
                )
                NavigationLink { QuranicDuaLibraryView() } label: {
                    Label(settings.t("Duas", "Dualar"), systemImage: "hands.sparkles.fill")
                }
            }
        }
        .navigationTitle(settings.t("Ramadan", "Ramazan"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Esmaül Hüsna

private struct EsmaName: Identifiable {
    let number: Int
    let arabic: String
    let name: String
    let deMeaning: String
    let trMeaning: String
    var id: Int { number }
}

struct EsmaulHusnaView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var search = ""

    private let names: [EsmaName] = [
        .init(number: 1, arabic: "اللَّهُ", name: "Allah", deMeaning: "Der eine wahre Gott; der Eigenname Allahs.", trMeaning: "Tek gerçek ilâh; Allah'ın özel ismi."),
        .init(number: 2, arabic: "الرَّحْمٰنُ", name: "er-Rahmân", deMeaning: "Der unermesslich Barmherzige.", trMeaning: "Sonsuz rahmet sahibi."),
        .init(number: 3, arabic: "الرَّحِيمُ", name: "er-Rahîm", deMeaning: "Der besonders Barmherzige.", trMeaning: "Rahmeti her şeyi kuşatan."),
        .init(number: 4, arabic: "الْمَلِكُ", name: "el-Melik", deMeaning: "Der absolute Herrscher und Besitzer.", trMeaning: "Bütün varlıkların gerçek sahibi ve hükümdarı."),
        .init(number: 5, arabic: "الْقُدُّوسُ", name: "el-Kuddûs", deMeaning: "Der vollkommen Reine, frei von jedem Mangel.", trMeaning: "Her türlü eksiklikten uzak olan."),
        .init(number: 6, arabic: "السَّلَامُ", name: "es-Selâm", deMeaning: "Der Quell von Frieden und Unversehrtheit.", trMeaning: "Esenlik ve selâmet veren."),
        .init(number: 7, arabic: "الْمُؤْمِنُ", name: "el-Mü’min", deMeaning: "Der Sicherheit und Vertrauen schenkt.", trMeaning: "Güven ve emniyet veren."),
        .init(number: 8, arabic: "الْمُهَيْمِنُ", name: "el-Müheymin", deMeaning: "Der alles überwacht und beschützt.", trMeaning: "Her şeyi gözetip yöneten."),
        .init(number: 9, arabic: "الْعَزِيزُ", name: "el-Azîz", deMeaning: "Der Unüberwindliche, Erhabene.", trMeaning: "Mutlak izzet ve üstünlük sahibi."),
        .init(number: 10, arabic: "الْجَبَّارُ", name: "el-Cebbâr", deMeaning: "Der allmächtig Durchsetzende.", trMeaning: "Mutlak kudretiyle hükmünü yürüten."),
        .init(number: 11, arabic: "الْمُتَكَبِّرُ", name: "el-Mütekebbir", deMeaning: "Der wahrhaft Große und Erhabene.", trMeaning: "Büyüklükte eşsiz ve yüce olan."),
        .init(number: 12, arabic: "الْخَالِقُ", name: "el-Hâlik", deMeaning: "Der Schöpfer aller Dinge.", trMeaning: "Her şeyin yaratıcısı."),
        .init(number: 13, arabic: "الْبَارِئُ", name: "el-Bâri’", deMeaning: "Der aus dem Nichts erschafft.", trMeaning: "Örneksiz ve maddesiz yaratan."),
        .init(number: 14, arabic: "الْمُصَوِّرُ", name: "el-Musavvir", deMeaning: "Der den Geschöpfen Gestalt gibt.", trMeaning: "Varlıklara şekil ve suret veren."),
        .init(number: 15, arabic: "الْغَفَّارُ", name: "el-Gaffâr", deMeaning: "Der immer wieder viel vergibt.", trMeaning: "Çokça bağışlayan."),
        .init(number: 16, arabic: "الْقَهَّارُ", name: "el-Kahhâr", deMeaning: "Der alles bezwingt, dem alles untersteht.", trMeaning: "Her şeye galip gelen."),
        .init(number: 17, arabic: "الْوَهَّابُ", name: "el-Vehhâb", deMeaning: "Der freigebig und ohne Gegenleistung schenkt.", trMeaning: "Karşılıksız çokça nimet veren."),
        .init(number: 18, arabic: "الرَّزَّاقُ", name: "er-Rezzâk", deMeaning: "Der alle Versorgung gewährt.", trMeaning: "Bütün rızıkları veren."),
        .init(number: 19, arabic: "الْفَتَّاحُ", name: "el-Fettâh", deMeaning: "Der Wege öffnet und gerecht entscheidet.", trMeaning: "Hayır kapılarını açan ve hükmeden."),
        .init(number: 20, arabic: "الْعَلِيمُ", name: "el-Alîm", deMeaning: "Der alles weiß.", trMeaning: "Her şeyi bilen."),
        .init(number: 21, arabic: "الْقَابِضُ", name: "el-Kâbız", deMeaning: "Der nach Weisheit begrenzt und zurückhält.", trMeaning: "Hikmetiyle daraltan ve tutan."),
        .init(number: 22, arabic: "الْبَاسِطُ", name: "el-Bâsıt", deMeaning: "Der nach Weisheit weitet und reichlich gibt.", trMeaning: "Hikmetiyle genişleten."),
        .init(number: 23, arabic: "الْخَافِضُ", name: "el-Hâfıd", deMeaning: "Der erniedrigt, wen Er will.", trMeaning: "Dilediğini alçaltan."),
        .init(number: 24, arabic: "الرَّافِعُ", name: "er-Râfi‘", deMeaning: "Der erhöht und erhebt.", trMeaning: "Dilediğini yükselten."),
        .init(number: 25, arabic: "الْمُعِزُّ", name: "el-Muizz", deMeaning: "Der Ehre und Stärke gibt.", trMeaning: "İzzet ve güç veren."),
        .init(number: 26, arabic: "الْمُذِلُّ", name: "el-Müzill", deMeaning: "Der Demütigung zulässt und unterwirft.", trMeaning: "Dilediğini zelil kılan."),
        .init(number: 27, arabic: "السَّمِيعُ", name: "es-Semî‘", deMeaning: "Der alles hört.", trMeaning: "Her şeyi işiten."),
        .init(number: 28, arabic: "الْبَصِيرُ", name: "el-Basîr", deMeaning: "Der alles sieht.", trMeaning: "Her şeyi gören."),
        .init(number: 29, arabic: "الْحَكَمُ", name: "el-Hakem", deMeaning: "Der endgültige Richter.", trMeaning: "Nihai hükmü veren."),
        .init(number: 30, arabic: "الْعَدْلُ", name: "el-Adl", deMeaning: "Der vollkommen Gerechte.", trMeaning: "Mutlak adalet sahibi."),
        .init(number: 31, arabic: "اللَّطِيفُ", name: "el-Latîf", deMeaning: "Der Feinfühlige, der auch das Verborgenste kennt.", trMeaning: "En ince şeyleri bilen ve lütfeden."),
        .init(number: 32, arabic: "الْخَبِيرُ", name: "el-Habîr", deMeaning: "Der über alles vollständig informiert ist.", trMeaning: "Her şeyden haberdar olan."),
        .init(number: 33, arabic: "الْحَلِيمُ", name: "el-Halîm", deMeaning: "Der Nachsichtige und Milde.", trMeaning: "Hemen cezalandırmayan, yumuşak davranan."),
        .init(number: 34, arabic: "الْعَظِيمُ", name: "el-Azîm", deMeaning: "Der unermesslich Erhabene.", trMeaning: "Azamet ve yücelik sahibi."),
        .init(number: 35, arabic: "الْغَفُورُ", name: "el-Gafûr", deMeaning: "Der sehr viel vergibt.", trMeaning: "Çok bağışlayan."),
        .init(number: 36, arabic: "الشَّكُورُ", name: "eş-Şekûr", deMeaning: "Der gute Taten reich belohnt.", trMeaning: "Az amele çok karşılık veren."),
        .init(number: 37, arabic: "الْعَلِيُّ", name: "el-Aliyy", deMeaning: "Der Höchste und Erhabenste.", trMeaning: "Yücelikte eşsiz olan."),
        .init(number: 38, arabic: "الْكَبِيرُ", name: "el-Kebîr", deMeaning: "Der unvergleichlich Große.", trMeaning: "Büyüklüğü sınırsız olan."),
        .init(number: 39, arabic: "الْحَفِيظُ", name: "el-Hafîz", deMeaning: "Der alles bewahrt und beschützt.", trMeaning: "Her şeyi koruyup gözeten."),
        .init(number: 40, arabic: "الْمُقِيتُ", name: "el-Mukît", deMeaning: "Der Nahrung und Kraft gewährt.", trMeaning: "Rızık ve güç veren, koruyan."),
        .init(number: 41, arabic: "الْحَسِيبُ", name: "el-Hasîb", deMeaning: "Der abrechnet und für alles genügt.", trMeaning: "Hesaba çeken ve kullarına yeten."),
        .init(number: 42, arabic: "الْجَلِيلُ", name: "el-Celîl", deMeaning: "Der Besitzer vollkommener Majestät.", trMeaning: "Azamet ve yücelik sahibi."),
        .init(number: 43, arabic: "الْكَرِيمُ", name: "el-Kerîm", deMeaning: "Der überaus Großzügige.", trMeaning: "Çok cömert ve ikram sahibi."),
        .init(number: 44, arabic: "الرَّقِيبُ", name: "er-Rakîb", deMeaning: "Der alles wachsam überwacht.", trMeaning: "Her şeyi gözeten."),
        .init(number: 45, arabic: "الْمُجِيبُ", name: "el-Mücîb", deMeaning: "Der Gebete erhört.", trMeaning: "Dualara icabet eden."),
        .init(number: 46, arabic: "الْوَاسِعُ", name: "el-Vâsi‘", deMeaning: "Dessen Wissen, Macht und Barmherzigkeit alles umfasst.", trMeaning: "İlmi, rahmeti ve kudreti geniş olan."),
        .init(number: 47, arabic: "الْحَكِيمُ", name: "el-Hakîm", deMeaning: "Der vollkommen Weise.", trMeaning: "Her işi hikmetli olan."),
        .init(number: 48, arabic: "الْوَدُودُ", name: "el-Vedûd", deMeaning: "Der Liebende und Liebe Schenkende.", trMeaning: "Seven ve sevilen."),
        .init(number: 49, arabic: "الْمَجِيدُ", name: "el-Mecîd", deMeaning: "Der Ruhmreiche und Großzügige.", trMeaning: "Şanı yüce ve ikramı bol olan."),
        .init(number: 50, arabic: "الْبَاعِثُ", name: "el-Bâis", deMeaning: "Der auferweckt und entsendet.", trMeaning: "Dirilten ve elçiler gönderen."),
        .init(number: 51, arabic: "الشَّهِيدُ", name: "eş-Şehîd", deMeaning: "Der über alles Zeuge ist.", trMeaning: "Her şeye şahit olan."),
        .init(number: 52, arabic: "الْحَقُّ", name: "el-Hakk", deMeaning: "Der absolute und beständige Wahre.", trMeaning: "Varlığı ve hükmü gerçek olan."),
        .init(number: 53, arabic: "الْوَكِيلُ", name: "el-Vekîl", deMeaning: "Der vollkommen Verlässliche, dem man sich anvertraut.", trMeaning: "Kendisine güvenilip dayanılan."),
        .init(number: 54, arabic: "الْقَوِيُّ", name: "el-Kaviyy", deMeaning: "Der Allstarke.", trMeaning: "Gücü her şeye yeten."),
        .init(number: 55, arabic: "الْمَتِينُ", name: "el-Metîn", deMeaning: "Der unerschütterlich Starke.", trMeaning: "Kuvveti sarsılmaz olan."),
        .init(number: 56, arabic: "الْوَلِيُّ", name: "el-Veliyy", deMeaning: "Der Schutzherr und Helfer der Gläubigen.", trMeaning: "Müminlerin dostu ve yardımcısı."),
        .init(number: 57, arabic: "الْحَمِيدُ", name: "el-Hamîd", deMeaning: "Der allen Lobes Würdige.", trMeaning: "Her türlü övgüye layık olan."),
        .init(number: 58, arabic: "الْمُحْصِي", name: "el-Muhsî", deMeaning: "Der alles bis ins Einzelne zählt und kennt.", trMeaning: "Her şeyin sayısını ve ölçüsünü bilen."),
        .init(number: 59, arabic: "الْمُبْدِئُ", name: "el-Mübdi’", deMeaning: "Der die Schöpfung erstmals hervorbringt.", trMeaning: "Varlıkları ilk defa yaratan."),
        .init(number: 60, arabic: "الْمُعِيدُ", name: "el-Muîd", deMeaning: "Der die Schöpfung wieder hervorbringt.", trMeaning: "Ölümden sonra yeniden yaratan."),
        .init(number: 61, arabic: "الْمُحْيِي", name: "el-Muhyî", deMeaning: "Der Leben gibt.", trMeaning: "Hayat veren ve dirilten."),
        .init(number: 62, arabic: "الْمُمِيتُ", name: "el-Mümît", deMeaning: "Der den Tod bestimmt.", trMeaning: "Öldüren, canları alan."),
        .init(number: 63, arabic: "الْحَيُّ", name: "el-Hayy", deMeaning: "Der ewig Lebendige.", trMeaning: "Ezelî ve ebedî diri olan."),
        .init(number: 64, arabic: "الْقَيُّومُ", name: "el-Kayyûm", deMeaning: "Der aus sich selbst besteht und alles erhält.", trMeaning: "Varlığı kendinden, her şeyi ayakta tutan."),
        .init(number: 65, arabic: "الْوَاجِدُ", name: "el-Vâcid", deMeaning: "Der nichts entbehrt und alles findet.", trMeaning: "Hiçbir şeye muhtaç olmayan."),
        .init(number: 66, arabic: "الْمَاجِدُ", name: "el-Mâcid", deMeaning: "Der Edle und Ruhmreiche.", trMeaning: "Şanı yüce, keremi bol olan."),
        .init(number: 67, arabic: "الْوَاحِدُ", name: "el-Vâhid", deMeaning: "Der Eine ohne Teilhaber.", trMeaning: "Tek ve ortağı olmayan."),
        .init(number: 68, arabic: "الصَّمَدُ", name: "es-Samed", deMeaning: "Der Unabhängige, auf den alle angewiesen sind.", trMeaning: "Herkesin muhtaç olduğu, kimseye muhtaç olmayan."),
        .init(number: 69, arabic: "الْقَادِرُ", name: "el-Kâdir", deMeaning: "Der zu allem Fähige.", trMeaning: "Her şeye gücü yeten."),
        .init(number: 70, arabic: "الْمُقْتَدِرُ", name: "el-Muktedir", deMeaning: "Dessen Macht ohne Grenze ist.", trMeaning: "Kudreti sınırsız olan."),
        .init(number: 71, arabic: "الْمُقَدِّمُ", name: "el-Mukaddim", deMeaning: "Der nach Weisheit voranstellt.", trMeaning: "Hikmetiyle öne alan."),
        .init(number: 72, arabic: "الْمُؤَخِّرُ", name: "el-Muahhir", deMeaning: "Der nach Weisheit zurückstellt.", trMeaning: "Hikmetiyle geriye bırakan."),
        .init(number: 73, arabic: "الأَوَّلُ", name: "el-Evvel", deMeaning: "Der Erste ohne Anfang.", trMeaning: "Başlangıcı olmayan ilk."),
        .init(number: 74, arabic: "الآخِرُ", name: "el-Âhir", deMeaning: "Der Letzte ohne Ende.", trMeaning: "Sonu olmayan son."),
        .init(number: 75, arabic: "الظَّاهِرُ", name: "ez-Zâhir", deMeaning: "Der Offenbare, dessen Zeichen sichtbar sind.", trMeaning: "Varlığı delilleriyle açık olan."),
        .init(number: 76, arabic: "الْبَاطِنُ", name: "el-Bâtın", deMeaning: "Der Verborgene, der alles Verborgene kennt.", trMeaning: "Zatı gizli, gizlilikleri bilen."),
        .init(number: 77, arabic: "الْوَالِي", name: "el-Vâlî", deMeaning: "Der alles lenkt und verwaltet.", trMeaning: "Kâinatı yöneten."),
        .init(number: 78, arabic: "الْمُتَعَالِي", name: "el-Müteâlî", deMeaning: "Der über jede Unvollkommenheit Erhabene.", trMeaning: "Her türlü noksanlıktan yüce olan."),
        .init(number: 79, arabic: "الْبَرُّ", name: "el-Berr", deMeaning: "Der überreich Gutes tut.", trMeaning: "Çok iyilik eden."),
        .init(number: 80, arabic: "التَّوَّابُ", name: "et-Tevvâb", deMeaning: "Der Reue immer wieder annimmt.", trMeaning: "Tövbeleri çokça kabul eden."),
        .init(number: 81, arabic: "الْمُنْتَقِمُ", name: "el-Müntakim", deMeaning: "Der gerechte Vergeltung übt.", trMeaning: "Suçlara adaletle karşılık veren."),
        .init(number: 82, arabic: "الْعَفُوُّ", name: "el-Afüvv", deMeaning: "Der Sünden auslöscht und vergibt.", trMeaning: "Çokça affeden."),
        .init(number: 83, arabic: "الرَّؤُوفُ", name: "er-Raûf", deMeaning: "Der voller Mitgefühl ist.", trMeaning: "Şefkat ve merhameti çok olan."),
        .init(number: 84, arabic: "مَالِكُ الْمُلْكِ", name: "Mâlikü’l-Mülk", deMeaning: "Der wahre Besitzer aller Herrschaft.", trMeaning: "Mülkün gerçek sahibi."),
        .init(number: 85, arabic: "ذُو الْجَلَالِ وَالْإِكْرَامِ", name: "Zü’l-Celâli ve’l-İkrâm", deMeaning: "Der Besitzer von Majestät und Großzügigkeit.", trMeaning: "Celâl ve ikram sahibi."),
        .init(number: 86, arabic: "الْمُقْسِطُ", name: "el-Muksit", deMeaning: "Der vollkommen gerecht ausgleicht.", trMeaning: "Adaletle hükmeden."),
        .init(number: 87, arabic: "الْجَامِعُ", name: "el-Câmi‘", deMeaning: "Der zusammenführt und versammelt.", trMeaning: "Toplayan ve bir araya getiren."),
        .init(number: 88, arabic: "الْغَنِيُّ", name: "el-Ganî", deMeaning: "Der völlig Unabhängige und Reiche.", trMeaning: "Hiçbir şeye muhtaç olmayan."),
        .init(number: 89, arabic: "الْمُغْنِي", name: "el-Muğnî", deMeaning: "Der reich und unabhängig macht.", trMeaning: "Zenginlik ve yeterlilik veren."),
        .init(number: 90, arabic: "الْمَانِعُ", name: "el-Mâni‘", deMeaning: "Der nach Weisheit verhindert.", trMeaning: "Hikmetiyle engel olan."),
        .init(number: 91, arabic: "الضَّارُّ", name: "ed-Dârr", deMeaning: "Der auch schädliche Dinge nach Weisheit erschafft.", trMeaning: "Hikmetiyle zarar veren şeyleri yaratan."),
        .init(number: 92, arabic: "النَّافِعُ", name: "en-Nâfi‘", deMeaning: "Der Nutzen und Gutes gewährt.", trMeaning: "Fayda ve hayır veren."),
        .init(number: 93, arabic: "النُّورُ", name: "en-Nûr", deMeaning: "Der Licht und Rechtleitung schenkt.", trMeaning: "Nurlandıran ve kalpleri aydınlatan."),
        .init(number: 94, arabic: "الْهَادِي", name: "el-Hâdî", deMeaning: "Der den rechten Weg zeigt.", trMeaning: "Doğru yola ileten."),
        .init(number: 95, arabic: "الْبَدِيعُ", name: "el-Bedî‘", deMeaning: "Der ohne Vorbild erschafft.", trMeaning: "Örneksiz ve benzersiz yaratan."),
        .init(number: 96, arabic: "الْبَاقِي", name: "el-Bâkî", deMeaning: "Der ewig Bleibende.", trMeaning: "Varlığı sonsuz olan."),
        .init(number: 97, arabic: "الْوَارِثُ", name: "el-Vâris", deMeaning: "Der letztlich alles besitzt und überdauert.", trMeaning: "Her şeyin gerçek mirasçısı."),
        .init(number: 98, arabic: "الرَّشِيدُ", name: "er-Reşîd", deMeaning: "Der vollkommen recht leitet und richtig führt.", trMeaning: "Doğru yolu gösteren, işi isabetli olan."),
        .init(number: 99, arabic: "الصَّبُورُ", name: "es-Sabûr", deMeaning: "Der unendlich Geduldige.", trMeaning: "Cezada acele etmeyen, çok sabırlı olan.")
    ]

    private var filtered: [EsmaName] {
        let q = search.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !q.isEmpty else { return names }
        return names.filter {
            $0.name.localizedCaseInsensitiveContains(q) ||
            $0.arabic.localizedCaseInsensitiveContains(q) ||
            $0.deMeaning.localizedCaseInsensitiveContains(q) ||
            $0.trMeaning.localizedCaseInsensitiveContains(q) ||
            String($0.number) == q
        }
    }

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("Allahs schöne Namen", "Esmâü'l-Hüsnâ"), systemImage: "sparkles")
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Die bekannte 99er-Liste hilft beim Lernen und Nachdenken über Allahs Namen. Die Namen Allahs sind nach Diyanet nicht auf diese Zahl begrenzt.",
                        "Meşhur 99 isim listesi Allah'ın isimlerini öğrenmeye ve anlamları üzerinde düşünmeye yardımcı olur. Diyanet'e göre Allah'ın isimleri yalnız 99 ile sınırlı değildir."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)

                    Text("99 / 99")
                        .font(.caption.bold().monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
                }
                .padding(.vertical, 3)
            }

            Section {
                HStack(spacing: 8) {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(SalahTheme.teal)
                    TextField(settings.t("Name oder Bedeutung suchen", "İsim veya anlam ara"), text: $search)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                }
            }

            Section(settings.t("99 Namen", "99 İsim")) {
                ForEach(filtered) { item in
                    VStack(alignment: .leading, spacing: 7) {
                        HStack(spacing: 10) {
                            Text("\(item.number)")
                                .font(.caption.bold().monospacedDigit())
                                .foregroundStyle(.white)
                                .frame(width: 34, height: 34)
                                .background(SalahTheme.navigationTeal, in: Circle())

                            VStack(alignment: .leading, spacing: 2) {
                                Text(item.name)
                                    .font(.headline.bold())
                                    .foregroundStyle(SalahTheme.ink)
                                Text(settings.language == .german ? item.deMeaning : item.trMeaning)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                                    .fixedSize(horizontal: false, vertical: true)
                            }

                            Spacer()

                            Text(item.arabic)
                                .font(.system(size: 23, weight: .medium))
                                .foregroundStyle(SalahTheme.deepTeal)
                        }
                    }
                    .padding(.vertical, 3)
                }
            }

            Section(settings.t("Quelle", "Kaynak")) {
                Text(settings.t(
                    "Namensliste: Din İşleri Yüksek Kurulu, „Allah'ın 99 ismi“. Die kurzen deutschen/türkischen Bedeutungen in SalahPath sind bewusst knapp formulierte Lernhilfen.",
                    "İsim listesi: Din İşleri Yüksek Kurulu, „Allah'ın 99 ismi“. SalahPath'teki kısa anlamlar öğrenme amaçlı özlü açıklamalardır."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Esmaül Hüsna", "Esmâü'l-Hüsnâ"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Farewell Sermon

struct FarewellSermonView: View {
    @EnvironmentObject private var settings: SettingsStore

    private var principles: [(String, String, String, String)] {
        [
            (
                "shield.lefthalf.filled",
                "Schutz von Leben, Vermögen und Würde",
                "Can, mal ve onur dokunulmazlığı",
                settings.t(
                    "Der Prophet betonte während der Abschiedspilgerfahrt die Unverletzlichkeit von Leben, Vermögen und persönlicher Würde und stellte sie in den Zusammenhang der Heiligkeit von Tag, Monat und Ort.",
                    "Hz. Peygamber Veda Haccı sırasında canın, malın ve kişilik onurunun dokunulmazlığını vurguladı; bunu günün, ayın ve Mekke'nin dokunulmazlığıyla birlikte anlattı."
                )
            ),
            (
                "banknote.fill",
                "Ende von Riba und alten Vergeltungsforderungen",
                "Faiz ve eski kan davalarının kaldırılması",
                settings.t(
                    "Überlieferungen der Abschiedspilgerfahrt erklären vorislamische Zinsforderungen und alte Blutracheansprüche für aufgehoben. Damit wurden wirtschaftliche Ausbeutung und fortgesetzte Vergeltung ausdrücklich zurückgewiesen.",
                    "Veda Haccı rivayetlerinde cahiliye döneminden kalan faiz alacaklarının ve kan davalarının kaldırıldığı bildirilir. Böylece ekonomik sömürü ve bitmeyen intikam döngüsü reddedilmiştir."
                )
            ),
            (
                "person.2.fill",
                "Rechte und Verantwortung in der Familie",
                "Ailede hak ve sorumluluk",
                settings.t(
                    "Die Überlieferungen erinnern Ehepartner an gegenseitige Rechte und Pflichten und fordern einen verantwortungsvollen und guten Umgang miteinander.",
                    "Rivayetler eşlerin karşılıklı hak ve sorumluluklarını hatırlatır; aile içinde sorumlu ve güzel muameleyi öğütler."
                )
            ),
            (
                "hand.raised.fill",
                "Treuhand, Schulden und Eigentum",
                "Emanet, borç ve mülkiyet",
                settings.t(
                    "Anvertrautes soll seinem Eigentümer zurückgegeben, Schulden sollen erfüllt und fremdes Vermögen nicht ohne Zustimmung angeeignet werden.",
                    "Emanet sahibine verilmeli, borçlar ödenmeli ve başkasının malı rızası olmadan alınmamalıdır."
                )
            ),
            (
                "person.3.fill",
                "Gemeinschaft ohne Stammesüberheblichkeit",
                "Irk ve sınıf üstünlüğünü reddeden toplum",
                settings.t(
                    "Diyanets Darstellung hebt die gemeinsame menschliche Herkunft hervor und liest die Abschiedsrede als Absage an Überheblichkeit aufgrund von Herkunft, Hautfarbe oder gesellschaftlicher Stellung.",
                    "Diyanet'in açıklaması insanların ortak kökenine dikkat çeker; Veda Hutbesi'ni ırk, renk veya toplumsal sınıf sebebiyle üstünlük iddiasının reddi olarak açıklar."
                )
            ),
            (
                "book.closed.fill",
                "An Offenbarung und prophetischer Orientierung festhalten",
                "Vahye ve peygamberî rehberliğe bağlılık",
                settings.t(
                    "In den überlieferten Abschiedsworten wird die Gemeinschaft dazu aufgerufen, an Allahs Buch und der prophetischen Orientierung festzuhalten und die anvertraute Botschaft weiterzugeben.",
                    "Veda sözlerinin rivayetlerinde ümmete Allah'ın kitabına ve peygamberî rehberliğe bağlı kalması, kendisine ulaşan mesajı başkalarına aktarması öğütlenir."
                )
            )
        ]
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 8) {
                    Label(settings.t("Veda Hutbesi · Abschiedsrede", "Veda Hutbesi"), systemImage: "text.quote")
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Während der Abschiedspilgerfahrt im Jahr 10 n. H. / 632 hielt der Prophet Muhammad Ansprachen in Arafat und Mina. Diese Worte gehören zu den bekanntesten überlieferten Zusammenfassungen seiner sozialen und religiösen Mahnungen.",
                        "Hz. Muhammed hicretin 10. yılında / 632'de yaptığı Veda Haccı sırasında Arafat ve Mina'da konuşmalar yaptı. Bu sözler onun dinî ve toplumsal öğütlerinin en çok bilinen özetleri arasındadır."
                    ))
                    .font(.subheadline)
                    .foregroundStyle(SalahTheme.ink)
                    .fixedSize(horizontal: false, vertical: true)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 20, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .stroke(SalahTheme.cardStroke(), lineWidth: 1)
                }

                VStack(alignment: .leading, spacing: 8) {
                    Label(settings.t("Wichtiger Quellenhinweis", "Önemli kaynak notu"), systemImage: "info.circle.fill")
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Die heute verbreitete „Veda-Hutbe“ ist kein einzelner wortgleich überlieferter Block. Diyanet weist darauf hin, dass Aussagen aus mehreren Reden der Abschiedspilgerfahrt und aus verschiedenen Hadith- und Sīra-Überlieferungen zusammengeführt wurden. SalahPath präsentiert deshalb die gut belegten Kernaussagen als Lernübersicht und behauptet keinen einzigen verbindlichen Wortlaut.",
                        "Bugün yaygın biçimde okunan „Veda Hutbesi“ tek parça ve kelimesi kelimesine tek rivayet değildir. Diyanet, Veda Haccı sırasındaki farklı konuşmalardan ve çeşitli hadis/siyer rivayetlerinden bölümlerin bir araya getirildiğini belirtir. Bu yüzden SalahPath iyi belgelenmiş ana mesajları öğrenme özeti olarak sunar ve tek bir zorunlu tam metin iddiasında bulunmaz."
                    ))
                    .font(.footnote)
                    .foregroundStyle(SalahTheme.mutedInk)
                    .fixedSize(horizontal: false, vertical: true)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(SalahTheme.gold.opacity(0.10), in: RoundedRectangle(cornerRadius: 18, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1)
                }

                ForEach(Array(principles.enumerated()), id: \.offset) { _, item in
                    VStack(alignment: .leading, spacing: 8) {
                        Label(
                            settings.language == .german ? item.1 : item.2,
                            systemImage: item.0
                        )
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                        Text(item.3)
                            .font(.subheadline)
                            .foregroundStyle(SalahTheme.ink)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 18, style: .continuous))
                    .overlay {
                        RoundedRectangle(cornerRadius: 18, style: .continuous)
                            .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
                    }
                }

                VStack(alignment: .leading, spacing: 6) {
                    Text(settings.t("Quellenbasis", "Kaynak temeli"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Diyanet Din İşleri Yüksek Kurulu · „Veda haccı ve veda hutbesi nedir?“; Diyanet Aylık Dergi · „İnsan Hakları Bağlamında Nebevi Emanet: Veda Hutbesi“; einschlägige Überlieferungen bei Buhārī und Muslim.",
                        "Diyanet Din İşleri Yüksek Kurulu · „Veda haccı ve veda hutbesi nedir?“; Diyanet Aylık Dergi · „İnsan Hakları Bağlamında Nebevi Emanet: Veda Hutbesi“; Buhârî ve Müslim'deki ilgili rivayetler."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                    .fixedSize(horizontal: false, vertical: true)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.horizontal, 2)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Abschiedsrede", "Veda Hutbesi"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Four Rightly Guided Caliphs

private struct CaliphLesson: Identifiable {
    let id: String
    let order: Int
    let arabic: String
    let deName: String
    let trName: String
    let years: String
    let deIntro: String
    let trIntro: String
    let dePoints: [String]
    let trPoints: [String]
    let source: String
}

struct FourCaliphsView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let lessons: [CaliphLesson] = [
        .init(
            id: "abu_bakr",
            order: 1,
            arabic: "أبو بكر",
            deName: "Abū Bakr as-Siddīq",
            trName: "Hz. Ebû Bekir es-Sıddîk",
            years: "632–634",
            deIntro: "Einer der frühesten Muslime, enger Gefährte des Propheten Muhammad und der erste Kalif nach dessen Tod.",
            trIntro: "İlk Müslümanlardan, Hz. Muhammed'in yakın dostu ve vefatından sonra ilk halifedir.",
            dePoints: [
                "Begleitete den Propheten bei der Hidschra von Mekka nach Medina.",
                "Nach dem Tod des Propheten wurde er in Medina zum ersten Kalifen gewählt.",
                "Während seiner Amtszeit wurden schwere innere Krisen der jungen muslimischen Gemeinschaft bewältigt.",
                "Nach hohen Verlusten unter Quran-Rezitatoren in der Yamāma-Schlacht unterstützte er die Sammlung des Quran in einem Mushaf; Zayd ibn Thābit leitete die Arbeit."
            ],
            trPoints: [
                "Mekke'den Medine'ye hicrette Hz. Peygamber'e yol arkadaşlığı yaptı.",
                "Hz. Peygamber'in vefatından sonra Medine'de ilk halife seçildi.",
                "Halifeliği sırasında genç Müslüman toplumun ciddi iç krizleriyle karşılaşıldı.",
                "Yemâme'de çok sayıda hâfızın şehit olmasının ardından Kur'an'ın mushaf hâlinde toplanmasını destekledi; çalışmayı Zeyd b. Sâbit yürüttü."
            ],
            source: "TDV İslâm Ansiklopedisi · Ebû Bekir; Diyanet · Cem'u'l-Kur'ân"
        ),
        .init(
            id: "umar",
            order: 2,
            arabic: "عمر",
            deName: "ʿUmar ibn al-Khattāb",
            trName: "Hz. Ömer b. Hattâb",
            years: "634–644",
            deIntro: "Der zweite Kalif. Er gehörte zu den engen Gefährten des Propheten und war bereits unter Abū Bakr ein wichtiger Berater.",
            trIntro: "İkinci halifedir. Hz. Peygamber'in yakın sahabilerindendi ve Hz. Ebû Bekir döneminde önemli bir danışmandı.",
            dePoints: [
                "Nahm den Islam in Mekka an und wanderte später nach Medina aus.",
                "Übernahm 634 nach Abū Bakrs Tod das Kalifat.",
                "Seine Regierungszeit war von starkem territorialem Wachstum und dem Aufbau dauerhafter Verwaltungsstrukturen geprägt.",
                "Er setzte Richter ein und entwickelte staatliche Verwaltungs- und Finanzstrukturen weiter.",
                "In seiner Zeit wurde die Hidschra als Ausgangspunkt der islamischen Zeitrechnung festgelegt."
            ],
            trPoints: [
                "Mekke'de Müslüman oldu ve daha sonra Medine'ye hicret etti.",
                "Hz. Ebû Bekir'in vefatından sonra 634 yılında halifeliği devraldı.",
                "Döneminde İslâm coğrafyası büyük ölçüde genişledi ve kalıcı idarî kurumlar gelişti.",
                "Kadılar görevlendirdi; devlet ve maliye teşkilatını geliştirdi.",
                "Hicret, onun döneminde İslâm takviminin başlangıcı olarak kabul edildi."
            ],
            source: "TDV İslâm Ansiklopedisi · Ömer; Diyanet yayınları"
        ),
        .init(
            id: "uthman",
            order: 3,
            arabic: "عثمان",
            deName: "ʿUthmān ibn ʿAffān",
            trName: "Hz. Osman b. Affân",
            years: "644–656",
            deIntro: "Einer der frühesten Muslime, Schwiegersohn des Propheten und der dritte Kalif.",
            trIntro: "İlk Müslümanlardan, Hz. Peygamber'in damadı ve üçüncü halifedir.",
            dePoints: [
                "Nahm früh den Islam an und gehörte zu den Muslimen, die nach Abessinien auswanderten.",
                "War mit Ruqayya und nach deren Tod mit Umm Kulthūm, zwei Töchtern des Propheten, verheiratet; daher ist der Beiname Dhū n-Nūrayn bekannt.",
                "Wurde nach dem von ʿUmar eingesetzten Schūrā-Verfahren zum dritten Kalifen gewählt.",
                "Unter seiner Leitung wurde der bereits gesammelte Qurantext durch eine Kommission vervielfältigt und an wichtige Zentren versandt.",
                "Die letzten Jahre seiner Amtszeit waren von schweren politischen Spannungen geprägt; historische Quellen zu Ursachen und Verantwortlichkeiten enthalten unterschiedliche und teils widersprüchliche Berichte."
            ],
            trPoints: [
                "İslâm'ı erken dönemde kabul etti ve Habeşistan'a hicret eden Müslümanlar arasında yer aldı.",
                "Hz. Peygamber'in kızları Rukıyye ve onun vefatından sonra Ümmü Külsûm ile evlendi; bu sebeple Zinnûreyn lakabıyla tanındı.",
                "Hz. Ömer'in belirlediği şûra sürecinin ardından üçüncü halife seçildi.",
                "Daha önce toplanan Kur'an metni onun döneminde bir komisyon tarafından çoğaltılarak önemli merkezlere gönderildi.",
                "Halifeliğinin son yılları ciddi siyasî gerilimlerle geçti; sebepler ve sorumluluklar hakkında tarihî kaynaklarda farklı ve birbiriyle çelişen rivayetler bulunur."
            ],
            source: "TDV İslâm Ansiklopedisi · Osman; Diyanet · Cem'u'l-Kur'ân"
        ),
        .init(
            id: "ali",
            order: 4,
            arabic: "علي",
            deName: "ʿAlī ibn Abī Tālib",
            trName: "Hz. Ali b. Ebî Tâlib",
            years: "656–661",
            deIntro: "Cousin und Schwiegersohn des Propheten, einer der frühesten Muslime und der vierte Kalif.",
            trIntro: "Hz. Peygamber'in amcasının oğlu ve damadı, ilk Müslümanlardan ve dördüncü halifedir.",
            dePoints: [
                "Wuchs bereits als Kind im Haushalt des Propheten auf und gehörte zu den frühesten Gläubigen.",
                "Blieb bei der Hidschra zunächst in Mekka, um ihm anvertraute Güter ihren Eigentümern zurückzugeben, und wanderte anschließend nach Medina aus.",
                "Heiratete Fātima, die Tochter des Propheten; zu ihren Kindern gehörten Hasan und Husayn.",
                "War für sein Wissen über Quran, Hadith und Fiqh bekannt und wurde auch von früheren Kalifen in Rechtsfragen konsultiert.",
                "Seine Amtszeit fiel in eine Phase schwerer innerer Konflikte. SalahPath behandelt die unterschiedlichen historischen und konfessionellen Deutungen nicht als eine einzige unumstrittene Version."
            ],
            trPoints: [
                "Çocukluğundan itibaren Hz. Peygamber'in yanında yetişti ve ilk iman edenler arasında yer aldı.",
                "Hicret sırasında emanetleri sahiplerine ulaştırmak için önce Mekke'de kaldı, ardından Medine'ye hicret etti.",
                "Hz. Peygamber'in kızı Fâtıma ile evlendi; Hasan ve Hüseyin çocukları arasındaydı.",
                "Kur'an, hadis ve özellikle fıkıh bilgisiyle tanındı; önceki halifeler de hukukî konularda görüşüne başvurdu.",
                "Halifeliği ağır iç çatışmaların yaşandığı bir döneme denk geldi. SalahPath farklı tarihî ve mezhebî yorumları tek ve tartışmasız bir anlatım gibi sunmaz."
            ],
            source: "TDV İslâm Ansiklopedisi · Ali"
        )
    ]

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("Die ersten vier Kalifen", "Dört Halife"), systemImage: "person.3.sequence.fill")
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Dieser Lernbereich fasst die vier als Hulefâ-yi Râşidîn bekannten frühen Kalifen biografisch zusammen. Politisch und konfessionell umstrittene Ereignisse werden bewusst neutral beschrieben.",
                        "Bu bölüm Hulefâ-yi Râşidîn olarak bilinen ilk dört halifeyi biyografik olarak özetler. Siyasî ve mezhebî açıdan ihtilaflı olaylar özellikle tarafsız biçimde anlatılır."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                    .fixedSize(horizontal: false, vertical: true)
                }
                .padding(.vertical, 4)
            }

            Section(settings.t("Chronologische Reihenfolge", "Kronolojik sıra")) {
                ForEach(lessons) { lesson in
                    NavigationLink {
                        FourCaliphDetailView(lesson: lesson)
                    } label: {
                        HStack(spacing: 11) {
                            Text("\(lesson.order)")
                                .font(.caption.bold())
                                .foregroundStyle(.white)
                                .frame(width: 36, height: 36)
                                .background(SalahTheme.navigationTeal, in: Circle())

                            VStack(alignment: .leading, spacing: 2) {
                                Text(settings.language == .german ? lesson.deName : lesson.trName)
                                    .font(.headline)
                                    .foregroundStyle(SalahTheme.ink)
                                Text(lesson.years)
                                    .font(.caption.bold().monospacedDigit())
                                    .foregroundStyle(SalahTheme.teal)
                            }

                            Spacer()

                            Text(lesson.arabic)
                                .font(.system(size: 20, weight: .medium))
                                .foregroundStyle(SalahTheme.deepTeal)
                        }
                        .padding(.vertical, 3)
                    }
                }
            }

            Section(settings.t("Quellen", "Kaynaklar")) {
                Text(settings.t(
                    "Biografische Grundlage: TDV İslâm Ansiklopedisi und Diyanet-Veröffentlichungen. Bei Ereignissen der ersten innerislamischen Konflikte gibt es in den historischen Quellen unterschiedliche Bewertungen.",
                    "Biyografik temel: TDV İslâm Ansiklopedisi ve Diyanet yayınları. İlk iç çatışmalarla ilgili tarihî kaynaklarda farklı değerlendirmeler bulunur."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Vier Kalifen", "Dört Halife"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

private struct FourCaliphDetailView: View {
    @EnvironmentObject private var settings: SettingsStore
    let lesson: CaliphLesson

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                VStack(spacing: 5) {
                    Text(lesson.arabic)
                        .font(.system(size: 34, weight: .medium))
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.language == .german ? lesson.deName : lesson.trName)
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.ink)

                    Text(settings.t("\(lesson.order). Kalif · \(lesson.years)", "\(lesson.order). Halife · \(lesson.years)"))
                        .font(.subheadline.bold().monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 20, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .stroke(SalahTheme.cardStroke(), lineWidth: 1)
                }

                VStack(alignment: .leading, spacing: 9) {
                    Text(settings.language == .german ? lesson.deIntro : lesson.trIntro)
                        .font(.body)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)

                    Divider().opacity(0.3)

                    let points = settings.language == .german ? lesson.dePoints : lesson.trPoints
                    ForEach(Array(points.enumerated()), id: \.offset) { index, point in
                        HStack(alignment: .top, spacing: 9) {
                            Text("\(index + 1)")
                                .font(.caption.bold())
                                .foregroundStyle(SalahTheme.deepTeal)
                                .frame(width: 25, height: 25)
                                .background(SalahTheme.gold.opacity(0.18), in: Circle())

                            Text(point)
                                .font(.subheadline)
                                .foregroundStyle(SalahTheme.ink)
                                .fixedSize(horizontal: false, vertical: true)

                            Spacer(minLength: 0)
                        }
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 20, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .stroke(SalahTheme.cardStroke(), lineWidth: 1)
                }

                Label(lesson.source, systemImage: "checkmark.seal.fill")
                    .font(.caption)
                    .foregroundStyle(SalahTheme.mutedInk)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.language == .german ? lesson.deName : lesson.trName)
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Ilmihal directory

private struct IlmihalTopic: Identifiable {
    let id: String
    let icon: String
    let deTitle: String
    let trTitle: String
    let deIntro: String
    let trIntro: String
    let dePoints: [String]
    let trPoints: [String]
}

private struct IlmihalTopicView: View {
    @EnvironmentObject private var settings: SettingsStore
    let topic: IlmihalTopic

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 8) {
                    Label(
                        settings.language == .german ? topic.deTitle : topic.trTitle,
                        systemImage: topic.icon
                    )
                    .font(.title2.bold())
                    .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.language == .german ? topic.deIntro : topic.trIntro)
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Lernübersicht", "Öğrenme özeti"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    let points = settings.language == .german ? topic.dePoints : topic.trPoints
                    ForEach(Array(points.enumerated()), id: \.offset) { index, point in
                        HStack(alignment: .top, spacing: 9) {
                            Text("\(index + 1)")
                                .font(.caption.bold())
                                .foregroundStyle(SalahTheme.deepTeal)
                                .frame(width: 25, height: 25)
                                .background(SalahTheme.gold.opacity(0.18), in: Circle())

                            Text(point)
                                .font(.subheadline)
                                .foregroundStyle(SalahTheme.ink)
                                .fixedSize(horizontal: false, vertical: true)

                            Spacer(minLength: 0)
                        }
                    }
                }
                .cardStyle()

                Text(settings.t(
                    "Dieser Bereich ist eine kompakte Lernorientierung. Für individuelle Fälle, strittige Fragen oder konkrete Rechtsfolgen sollte eine qualifizierte religiöse Beratungsstelle gefragt werden.",
                    "Bu bölüm kısa bir öğrenme rehberidir. Kişisel durumlar, ihtilaflı meseleler veya özel fıkhî sonuçlar için ehil bir dinî danışmana başvurulmalıdır."
                ))
                .font(.caption)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.language == .german ? topic.deTitle : topic.trTitle)
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct IlmihalDirectoryView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let zakat = IlmihalTopic(
        id: "zakat", icon: "banknote.fill",
        deTitle: "Zakat & Sadaqa", trTitle: "Zekât & Sadaka",
        deIntro: "Zakat ist eine verpflichtende Vermögensabgabe, wenn die persönlichen und vermögensbezogenen Voraussetzungen erfüllt sind. Sadaqa bezeichnet freiwillige Wohltätigkeit.",
        trIntro: "Zekât, kişisel ve malî şartlar oluştuğunda farz olan malî ibadettir. Sadaka ise gönüllü yardımlaşmayı kapsar.",
        dePoints: [
            "Nicht jedes Vermögen wird gleich behandelt; Art des Vermögens, Besitzdauer und Nisab können entscheidend sein.",
            "Zakat darf nur an die religiös vorgesehenen Empfängergruppen gegeben werden.",
            "Zakat, Sadaqat al-Fitr/Fitra und freiwillige Sadaqa sind unterschiedliche Kategorien.",
            "Bei Geschäftswaren, Schulden, Gold, Sparguthaben oder gemischten Vermögen sollte die konkrete Berechnung separat geprüft werden."
        ],
        trPoints: [
            "Her mal aynı hükme tabi değildir; malın türü, üzerinden geçen süre ve nisap önemlidir.",
            "Zekât dinen belirlenen hak sahibi gruplara verilir.",
            "Zekât, fitre ve gönüllü sadaka farklı hükümlere sahiptir.",
            "Ticaret malı, borç, altın, birikim ve karma mal varlığında özel hesap ayrıca kontrol edilmelidir."
        ]
    )

    private let sacrifice = IlmihalTopic(
        id: "sacrifice", icon: "gift.fill",
        deTitle: "Kurban / Opfer", trTitle: "Kurban",
        deIntro: "Das Opferfest und das rituelle Opfer haben eigene Voraussetzungen, Zeiten und Regeln. Im hanafitischen Fiqh wird die Opferpflicht für entsprechend vermögende Personen als wajib behandelt.",
        trIntro: "Kurban ibadetinin şartları, vakti ve uygulama hükümleri vardır. Hanefî fıkhında gerekli malî şartları taşıyan kişi için kurban vacip kabul edilir.",
        dePoints: [
            "Opferzeit, Opferfähigkeit der Person und Eignung des Tieres müssen zusammen geprüft werden.",
            "Das Tier darf bestimmte gesundheitliche Mängel nicht aufweisen.",
            "Vertretung/Vollmacht beim Opfer ist möglich; Absicht und Eigentumsfragen müssen klar sein.",
            "Fleischverteilung ist Teil guter Praxis; konkrete Pflichtanteile sollten nicht ohne Beleg behauptet werden."
        ],
        trPoints: [
            "Kurban vakti, kişinin yükümlülüğü ve hayvanın uygunluğu birlikte değerlendirilir.",
            "Hayvanda kurbana engel olacak belirli kusurlar bulunmamalıdır.",
            "Vekâletle kurban mümkündür; niyet ve mülkiyet açık olmalıdır.",
            "Etin paylaşımı güzel bir uygulamadır; delilsiz zorunlu oranlar ileri sürülmemelidir."
        ]
    )

    private let vows = IlmihalTopic(
        id: "vows", icon: "signature",
        deTitle: "Gelübde, Eide & Sühne", trTitle: "Adak, Yemin & Kefaret",
        deIntro: "Gelübde, Eide und Kaffara haben unterschiedliche Voraussetzungen. Umgangssprache und rechtlich bindende Formulierungen sind nicht automatisch dasselbe.",
        trIntro: "Adak, yemin ve kefaretin şartları farklıdır. Günlük konuşmadaki her söz fıkhen bağlayıcı yemin veya adak sayılmaz.",
        dePoints: [
            "Zuerst klären, ob überhaupt ein religiös bindendes Gelübde oder ein Eid entstanden ist.",
            "Ein Gelübde macht eine ursprünglich verbotene Handlung nicht erlaubt.",
            "Kaffara hängt vom konkreten Anlass ab; Fasten-Kaffara, Eid-Kaffara und andere Fälle dürfen nicht vermischt werden.",
            "Bei unklaren eigenen Formulierungen sollte der exakte Wortlaut fachkundig geprüft werden."
        ],
        trPoints: [
            "Önce dinen bağlayıcı bir adak veya yeminin gerçekten oluşup oluşmadığı belirlenir.",
            "Adak, haram olan bir işi helal hâle getirmez.",
            "Kefaret sebebe göre değişir; oruç kefareti, yemin kefareti ve diğerleri karıştırılmamalıdır.",
            "Kendi sözünün hükmü belirsizse kullanılan ifade aynen aktarılıp ehil kişiye sorulmalıdır."
        ]
    )

    private let family = IlmihalTopic(
        id: "family", icon: "house.and.flag.fill",
        deTitle: "Familie, Ehe & Scheidung", trTitle: "Aile, Nikâh & Boşanma",
        deIntro: "Das islamische Familienrecht behandelt Ehe, Ehehindernisse, gegenseitige Rechte, Unterhalt, Scheidung, Wartezeit und verwandte Themen.",
        trIntro: "İslâm aile hukuku nikâh, evlenme engelleri, karşılıklı haklar, nafaka, boşanma, iddet ve ilgili konuları kapsar.",
        dePoints: [
            "Eine gültige Ehe hat definierte Voraussetzungen; kulturelle Bräuche ersetzen diese nicht automatisch.",
            "Ehepartner haben gegenseitige Rechte und Verantwortlichkeiten; Gewalt oder Unrecht werden dadurch nicht legitimiert.",
            "Scheidungsfragen hängen stark vom exakten Wortlaut, der Situation und der Rechtsschule ab.",
            "Staatliches Familienrecht und religiöse Bewertung können unterschiedliche Ebenen betreffen; beides muss beachtet werden."
        ],
        trPoints: [
            "Geçerli nikâhın belirli şartları vardır; kültürel adetler bu şartların yerini otomatik olarak tutmaz.",
            "Eşlerin karşılıklı hak ve sorumlulukları vardır; bunlar şiddet veya haksızlığı meşrulaştırmaz.",
            "Boşama hükümleri kullanılan tam ifadeye, duruma ve mezhebe göre değişebilir.",
            "Devlet aile hukuku ile dinî değerlendirme farklı düzlemlerdir; ikisi de dikkate alınmalıdır."
        ]
    )

    private let inheritance = IlmihalTopic(
        id: "inheritance", icon: "doc.text.fill",
        deTitle: "Testament, Erbe & Stiftung", trTitle: "Vasiyet, Miras & Vakıf",
        deIntro: "Vermögensnachfolge umfasst Schulden, Testament/Vermächtnis, Erbanteile und gegebenenfalls Stiftungen. Diese Themen sind rechnerisch und rechtlich sensibel.",
        trIntro: "Malın ölüm sonrası intikali; borçlar, vasiyet, miras payları ve vakıf gibi konuları kapsar. Bu alan hem hesap hem hukuk bakımından hassastır.",
        dePoints: [
            "Vor einer Erbverteilung werden relevante Nachlasspflichten und Schulden berücksichtigt.",
            "Nicht jede gewünschte testamentarische Verteilung ist religiös oder staatlich ohne Weiteres wirksam.",
            "Erbanteile hängen von der tatsächlich vorhandenen Verwandtschaftskonstellation ab.",
            "Für einen realen Nachlass sind qualifizierte religiöse und staatlich-rechtliche Beratung sinnvoll."
        ],
        trPoints: [
            "Miras paylaşımından önce ilgili tereke yükümlülükleri ve borçlar dikkate alınır.",
            "İstenen her vasiyet düzenlemesi dinen veya hukukta otomatik olarak geçerli değildir.",
            "Miras payları mevcut mirasçıların kim olduğuna göre değişir.",
            "Gerçek bir tereke için hem dinî hem resmî hukuk açısından uzman desteği gerekir."
        ]
    )

    private let commerce = IlmihalTopic(
        id: "commerce", icon: "cart.fill",
        deTitle: "Handel & Erwerb", trTitle: "Ticaret & Kazanç",
        deIntro: "Islamische Handelsregeln betonen freiwillige Zustimmung, Klarheit, Ehrlichkeit und den Schutz vor unrechtmäßiger Vermögensaneignung.",
        trIntro: "İslâm ticaret ahlakı rızayı, açıklığı, dürüstlüğü ve haksız mal edinmekten kaçınmayı öne çıkarır.",
        dePoints: [
            "Täuschung, Betrug, Bestechung und unrechtmäßige Aneignung sind keine legitimen Erwerbswege.",
            "Verträge und Versprechen sollen klar und eingehalten werden.",
            "Riba/Zinsfragen sind juristisch differenziert; konkrete moderne Finanzprodukte müssen einzeln geprüft werden.",
            "Arbeitnehmer und Arbeitgeber tragen wechselseitige Rechte und Pflichten."
        ],
        trPoints: [
            "Aldatma, hile, rüşvet ve haksız mal edinme meşru kazanç değildir.",
            "Akitler ve verilen sözler açık olmalı ve yerine getirilmelidir.",
            "Faiz/riba meseleleri ayrıntılıdır; modern finans ürünleri tek tek değerlendirilmelidir.",
            "İşçi ve işverenin karşılıklı hak ve sorumlulukları vardır."
        ]
    )

    private let social = IlmihalTopic(
        id: "social", icon: "person.3.fill",
        deTitle: "Soziales Leben & Rechte", trTitle: "Sosyal Hayat & Haklar",
        deIntro: "Nachbarschaft, Familie, Öffentlichkeit, Eigentum und persönliche Würde gehören ebenfalls zum praktischen islamischen Leben.",
        trIntro: "Komşuluk, aile, toplum, mülkiyet ve insan onuru da günlük dinî hayatın konularındandır.",
        dePoints: [
            "Rechte anderer Menschen dürfen nicht durch vermeintliche Frömmigkeit übergangen werden.",
            "Üble Nachrede, Verleumdung, Spott und ungerechte Verdächtigung sind ethisch-religiöse Probleme.",
            "Nachbarschaft und Verwandtschaft beinhalten Verantwortung, aber auch persönliche Grenzen und Schutzrechte.",
            "Gutes Verhalten gilt auch gegenüber Menschen anderer Religionen und Überzeugungen."
        ],
        trPoints: [
            "Başkalarının hakları dindarlık iddiasıyla çiğnenemez.",
            "Gıybet, iftira, alay ve haksız suizan ahlâkî ve dinî sorunlardır.",
            "Komşuluk ve akrabalık sorumluluk getirir; aynı zamanda kişisel sınırlar ve korunma hakları vardır.",
            "Güzel muamele farklı din ve görüşten insanlara karşı da geçerlidir."
        ]
    )

    private let health = IlmihalTopic(
        id: "health", icon: "cross.case.fill",
        deTitle: "Medizin & Gesundheit", trTitle: "Tıp & Sağlık",
        deIntro: "Krankheit kann Einfluss auf Reinheit, Gebet, Fasten und andere Pflichten haben. Medizinische und religiöse Fragen sollten dabei getrennt, aber gemeinsam berücksichtigt werden.",
        trIntro: "Hastalık; abdest, namaz, oruç ve diğer ibadetleri etkileyebilir. Tıbbî ve dinî değerlendirme birbirine karıştırılmadan birlikte ele alınmalıdır.",
        dePoints: [
            "Bei Krankheit kennt der Fiqh Erleichterungen; deren Anwendung hängt von der tatsächlichen Situation ab.",
            "Medizinische Diagnose und Behandlung gehören in die Hand qualifizierter Gesundheitsfachkräfte.",
            "Religiöse Fragen zu Medikamenten, Eingriffen, Fasten oder Reinheit benötigen den konkreten medizinischen Sachverhalt.",
            "Notlagen und ernsthafte Gesundheitsgefahren werden nicht ignoriert, um eine freiwillige Praxis aufrechtzuerhalten."
        ],
        trPoints: [
            "Hastalıkta fıkhın ruhsatları vardır; hangi ruhsatın uygulanacağı gerçek duruma bağlıdır.",
            "Tıbbî teşhis ve tedavi yetkili sağlık uzmanlarının alanıdır.",
            "İlaç, ameliyat, oruç veya temizlikle ilgili dinî hüküm için tıbbî durum doğru bilinmelidir.",
            "Nafile uygulamayı sürdürmek uğruna ciddi sağlık tehlikesi görmezden gelinmez."
        ]
    )

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("İlmihal · Alltag des Glaubens", "İlmihal · Dini hayat rehberi"), systemImage: "books.vertical.fill")
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Die PDF zeigt einen tiefen İlmihal-Themenbaum. SalahPath führt vorhandene ausführliche Bereiche hier zusammen und ergänzt fehlende Hauptkapitel als kompakte Lernorientierung.",
                        "PDF derin bir ilmihal konu ağacı gösteriyor. SalahPath mevcut ayrıntılı bölümleri burada birleştiriyor ve eksik ana başlıkları kısa öğrenme rehberleriyle tamamlıyor."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .padding(.vertical, 3)
            }

            Section(settings.t("Glaube & Grundlagen", "İman & Temel Bilgiler")) {
                NavigationLink { IslamLearningHubView() } label: {
                    Label(settings.t("Glaubenslehre, Islam & Charakter", "İman, İslâm & Ahlâk"), systemImage: "book.pages.fill")
                }
                NavigationLink { ThirtyTwoFardView() } label: {
                    Label("32 Farz", systemImage: "checklist")
                }
                NavigationLink { EsmaulHusnaView() } label: {
                    Label(settings.t("Esmaül Hüsna · 99 Namen", "Esmâü'l-Hüsnâ · 99 İsim"), systemImage: "sparkles")
                }
                NavigationLink { FourCaliphsView() } label: {
                    Label(settings.t("Die vier Kalifen", "Dört Halife"), systemImage: "person.3.sequence.fill")
                }
            }

            Section(settings.t("Reinheit", "Taharet")) {
                NavigationLink { WuduGuideView() } label: { Label(settings.t("Wudu", "Abdest"), systemImage: "drop.fill") }
                NavigationLink { GhuslGuideView() } label: { Label(settings.t("Ghusl", "Gusül"), systemImage: "shower.fill") }
                NavigationLink { TayammumGuideView() } label: { Label("Tayammum", systemImage: "hand.raised.fill") }
            }

            Section(settings.t("Gebet", "Namaz")) {
                NavigationLink { PrayerCatalogView() } label: { Label(settings.t("Alle Gebetsarten", "Tüm namaz türleri"), systemImage: "rectangle.stack.fill") }
                NavigationLink { PrayerHowToView() } label: { Label(settings.t("Körperhaltungen & Rezitation", "Hareketler & kıraat"), systemImage: "figure.mind.and.body") }
                NavigationLink { PrayerTextsHubView() } label: { Label(settings.t("Suren, Duas & Ayat", "Sûre, dua & ayetler"), systemImage: "text.book.closed.fill") }
                NavigationLink { PrayerDebtTrackerView() } label: { Label(settings.t("Qada-Tracker", "Kaza Takibi"), systemImage: "clock.arrow.circlepath") }
            }

            Section(settings.t("Fasten, Zakat & Hajj", "Oruç, Zekât & Hac")) {
                NavigationLink { RamadanGuideIndexView() } label: { Label(settings.t("Fasten & Ramadan", "Oruç & Ramazan"), systemImage: "moon.stars.fill") }
                NavigationLink { IlmihalTopicView(topic: zakat) } label: { Label(settings.t("Zakat & Sadaqa", "Zekât & Sadaka"), systemImage: zakat.icon) }
                NavigationLink { HajjUmrahGuideView() } label: { Label(settings.t("Hajj & Umrah", "Hac & Umre"), systemImage: "map.fill") }
                NavigationLink { IlmihalTopicView(topic: sacrifice) } label: { Label(settings.t("Kurban / Opfer", "Kurban"), systemImage: sacrifice.icon) }
                NavigationLink { IlmihalTopicView(topic: vows) } label: { Label(settings.t("Gelübde, Eide & Sühne", "Adak, Yemin & Kefaret"), systemImage: vows.icon) }
            }

            Section(settings.t("Familie & Vermögen", "Aile & Malî Hayat")) {
                NavigationLink { IlmihalTopicView(topic: family) } label: { Label(settings.t("Ehe & Familie", "Nikâh & Aile"), systemImage: family.icon) }
                NavigationLink { IlmihalTopicView(topic: inheritance) } label: { Label(settings.t("Testament & Erbe", "Vasiyet & Miras"), systemImage: inheritance.icon) }
                NavigationLink { IlmihalTopicView(topic: commerce) } label: { Label(settings.t("Handel & Erwerb", "Ticaret & Kazanç"), systemImage: commerce.icon) }
            }

            Section(settings.t("Soziales & Gesundheit", "Sosyal Hayat & Sağlık")) {
                NavigationLink { IlmihalTopicView(topic: social) } label: { Label(settings.t("Soziale Rechte & Verhalten", "Sosyal Haklar & Davranış"), systemImage: social.icon) }
                NavigationLink { FarewellSermonView() } label: { Label(settings.t("Veda Hutbesi · Abschiedsrede", "Veda Hutbesi"), systemImage: "text.quote") }
                NavigationLink { IlmihalTopicView(topic: health) } label: { Label(settings.t("Medizin & Gesundheit", "Tıp & Sağlık"), systemImage: health.icon) }
            }

            Section(settings.t("Quelle & Umfang", "Kaynak & Kapsam")) {
                Text(settings.t(
                    "Struktur abgeglichen mit Diyanet İlmihal/Fetva-Hauptbereichen: Glaube, Reinheit, Gebet, Zakat, Fasten, Hajj/Umrah, Kurban, Gelübde/Eide, Quran/Dua, Familie, Erbe, Halal/Haram, soziales, medizinisches und kommerzielles Leben.",
                    "Yapı Diyanet İlmihal/Fetva ana alanlarıyla eşleştirildi: iman, taharet, namaz, zekât, oruç, hac/umre, kurban, adak/yemin, Kur'an/dua, aile, miras, helal-haram, sosyal, tıbbî ve ticarî hayat."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("İlmihal", "İlmihal"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Supplementary reference utilities

struct PrayerDebtTrackerView: View {
    @EnvironmentObject private var settings: SettingsStore

    @AppStorage("salahpath.qada.fajr") private var fajr = 0
    @AppStorage("salahpath.qada.dhuhr") private var dhuhr = 0
    @AppStorage("salahpath.qada.asr") private var asr = 0
    @AppStorage("salahpath.qada.maghrib") private var maghrib = 0
    @AppStorage("salahpath.qada.isha") private var isha = 0
    @AppStorage("salahpath.qada.witr") private var witr = 0
    @AppStorage("salahpath.qada.fasting") private var fasting = 0

    var body: some View {
        ScrollView {
            VStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("Qada-Tracker", "Kaza Takibi"), systemImage: "clock.arrow.circlepath")
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Ein persönlicher Zähler für nachzuholende Gebete und Fastentage. SalahPath entscheidet hier nicht, ob oder wie viele Qada-Pflichten bei dir bestehen.",
                        "Kaza namazları ve oruç günleri için kişisel sayaç. SalahPath burada sende kaç kaza bulunduğuna dair hüküm vermez."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)

                qadaRow(title: settings.t("Fajr", "Sabah"), value: $fajr)
                qadaRow(title: settings.t("Dhuhr", "Öğle"), value: $dhuhr)
                qadaRow(title: settings.t("Asr", "İkindi"), value: $asr)
                qadaRow(title: settings.t("Maghrib", "Akşam"), value: $maghrib)
                qadaRow(title: settings.t("Isha", "Yatsı"), value: $isha)
                qadaRow(title: settings.t("Witr", "Vitir"), value: $witr)
                qadaRow(title: settings.t("Fastentage", "Oruç"), value: $fasting)

                Button(role: .destructive) {
                    fajr = 0
                    dhuhr = 0
                    asr = 0
                    maghrib = 0
                    isha = 0
                    witr = 0
                    fasting = 0
                } label: {
                    Label(settings.t("Alle Zähler zurücksetzen", "Tüm sayaçları sıfırla"), systemImage: "arrow.counterclockwise")
                        .font(.headline)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                }
                .buttonStyle(.bordered)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Qada-Tracker", "Kaza Takibi"))
        .navigationBarTitleDisplayMode(.inline)
    }

    private func qadaRow(title: String, value: Binding<Int>) -> some View {
        HStack(spacing: 12) {
            Circle()
                .fill(SalahTheme.softTeal)
                .frame(width: 12, height: 12)

            Text(title)
                .font(.headline)
                .foregroundStyle(SalahTheme.ink)

            Spacer()

            Button {
                let current = max(0, value.wrappedValue)
                value.wrappedValue = current > 0 ? current - 1 : 0
            } label: {
                Image(systemName: "minus")
                    .font(.headline.bold())
                    .frame(width: 38, height: 38)
            }
            .buttonStyle(.bordered)
            .disabled(value.wrappedValue <= 0)

            Text("\(max(0, value.wrappedValue))")
                .font(.title3.bold().monospacedDigit())
                .foregroundStyle(SalahTheme.deepTeal)
                .frame(minWidth: 42)

            Button {
                let current = max(0, value.wrappedValue)
                let (next, overflow) = current.addingReportingOverflow(1)
                value.wrappedValue = overflow ? Int.max : next
            } label: {
                Image(systemName: "plus")
                    .font(.headline.bold())
                    .frame(width: 38, height: 38)
            }
            .buttonStyle(.borderedProminent)
            .tint(SalahTheme.teal)
        }
        .padding(12)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 14, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.32), lineWidth: 1)
        }
    }
}

struct ThirtyTwoFardView: View {
    @EnvironmentObject private var settings: SettingsStore

    private struct SectionData: Identifiable {
        let id = UUID()
        let deTitle: String
        let trTitle: String
        let deItems: [String]
        let trItems: [String]
    }

    private var sections: [SectionData] {
        [
            .init(
                deTitle: "6 Grundlagen des Glaubens",
                trTitle: "İmanın 6 şartı",
                deItems: ["Glaube an Allah", "Glaube an die Engel", "Glaube an die offenbarten Bücher", "Glaube an die Propheten", "Glaube an den Jüngsten Tag", "Glaube an Qadar und göttliche Bestimmung"],
                trItems: ["Allah’a iman", "Meleklere iman", "Kitaplara iman", "Peygamberlere iman", "Ahiret gününe iman", "Kader ve kazaya iman"]
            ),
            .init(
                deTitle: "5 Säulen / Bedingungen des Islam",
                trTitle: "İslam’ın 5 şartı",
                deItems: ["Schahada sprechen", "Gebet verrichten", "Im Ramadan fasten", "Zakat geben", "Hajj verrichten, wenn die Voraussetzungen erfüllt sind"],
                trItems: ["Kelime-i şehadet getirmek", "Namaz kılmak", "Oruç tutmak", "Zekât vermek", "Hacca gitmek"]
            ),
            .init(
                deTitle: "4 Farz des Wudu",
                trTitle: "Abdestin 4 farzı",
                deItems: ["Gesicht waschen", "Arme einschließlich Ellenbogen waschen", "Mindestens ein Viertel des Kopfes wischen", "Füße einschließlich Knöchel waschen"],
                trItems: ["Yüzü yıkamak", "Kolları dirseklerle beraber yıkamak", "Başın dörtte birini mesh etmek", "Ayakları topuklarla beraber yıkamak"]
            ),
            .init(
                deTitle: "3 Farz des Ghusl",
                trTitle: "Guslün 3 farzı",
                deItems: ["Mund ausspülen", "Nase mit Wasser reinigen", "Den ganzen Körper vollständig waschen"],
                trItems: ["Ağza su vermek", "Buruna su vermek", "Bütün bedeni kuru yer kalmayacak şekilde yıkamak"]
            ),
            .init(
                deTitle: "2 Farz des Tayammum",
                trTitle: "Teyemmümün 2 farzı",
                deItems: ["Absicht fassen", "Mit sauberer Erde oder erdähnlicher Oberfläche die vorgeschriebenen Wischhandlungen ausführen"],
                trItems: ["Niyet etmek", "Temiz toprağa elleri vurup gerekli meshleri yapmak"]
            ),
            .init(
                deTitle: "6 äußere Bedingungen des Gebets",
                trTitle: "Namazın dışındaki 6 farz",
                deItems: ["Rituelle Reinheit", "Reinheit von Körper, Kleidung und Gebetsplatz", "Bedeckung der ʿAwra", "Ausrichtung zur Qibla", "Eintritt der Gebetszeit", "Absicht"],
                trItems: ["Hadesten taharet", "Necasetten taharet", "Setr-i avret", "İstikbâl-i kıble", "Vakit", "Niyet"]
            ),
            .init(
                deTitle: "6 innere Bestandteile des Gebets",
                trTitle: "Namazın içindeki 6 farz",
                deItems: ["Eröffnungstakbir", "Stehen (Qiyām)", "Qirāʾa / Quran-Rezitation", "Rukūʿ", "Sujud", "Letztes Sitzen"],
                trItems: ["İftitah tekbiri", "Kıyam", "Kıraat", "Rükû", "Secde", "Ka’de-i âhire"]
            )
        ]
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 6) {
                    Label(settings.t("32 Farz – kompakter Lernzettel", "32 Farz – kısa öğrenme özeti"), systemImage: "checklist")
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Diese Ansicht ergänzt die ausführlichen SalahPath-Lernbereiche. Für die praktische Ausführung öffnest du weiterhin Wudu, Ghusl, Tayammum oder Gebet lernen.",
                        "Bu ekran ayrıntılı SalahPath derslerini tamamlar. Uygulama için yine Abdest, Gusül, Teyemmüm veya Namaz Öğren bölümlerini kullan."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)

                ForEach(sections) { section in
                    VStack(alignment: .leading, spacing: 8) {
                        Text(settings.language == .german ? section.deTitle : section.trTitle)
                            .font(.headline.bold())
                            .foregroundStyle(SalahTheme.deepTeal)

                        let items = settings.language == .german ? section.deItems : section.trItems
                        ForEach(Array(items.enumerated()), id: \.offset) { index, item in
                            HStack(alignment: .top, spacing: 9) {
                                Text("\(index + 1)")
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.deepTeal)
                                    .frame(width: 24, height: 24)
                                    .background(SalahTheme.gold.opacity(0.20), in: Circle())

                                Text(item)
                                    .font(.subheadline)
                                    .foregroundStyle(SalahTheme.ink)
                                    .fixedSize(horizontal: false, vertical: true)

                                Spacer(minLength: 0)
                            }
                        }
                    }
                    .cardStyle()
                }
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle("32 Farz")
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Human-recorded prayer/Quran audio

private enum QuranNetworkLimits {
    static let maxJSONBytes = 5 * 1024 * 1024
    static let maxAudioCacheFileBytes: Int64 = 32 * 1024 * 1024
}

actor QuranAudioCache {
    static let shared = QuranAudioCache()

    private let fileManager = FileManager.default
    private let maxBytes: Int64 = 300 * 1024 * 1024
    private var inFlightDownloads: Set<String> = []

    private var directoryURL: URL {
        let base = fileManager.urls(for: .applicationSupportDirectory, in: .userDomainMask).first
            ?? fileManager.temporaryDirectory
        return base.appendingPathComponent("SalahPathAudioCache", isDirectory: true)
    }

    func playbackURL(for remoteURL: URL) async -> URL {
        guard remoteURL.scheme?.lowercased() == "https" else { return remoteURL }

        do {
            try ensureDirectory()
            let localURL = destinationURL(for: remoteURL)

            if isValidFile(localURL) {
                touch(localURL)
                return localURL
            }

            let downloadKey = remoteURL.absoluteString
            guard !inFlightDownloads.contains(downloadKey) else {
                // Another caller is already filling this cache entry. Stream this
                // request instead of downloading and writing the same file twice.
                return remoteURL
            }
            inFlightDownloads.insert(downloadKey)
            defer { inFlightDownloads.remove(downloadKey) }

            var request = URLRequest(url: remoteURL)
            request.timeoutInterval = 30

            let (temporaryURL, response) = try await URLSession.shared.download(for: request)
            guard let http = response as? HTTPURLResponse,
                  (200...299).contains(http.statusCode),
                  Self.isAcceptableAudioMIMEType(http.mimeType) else {
                throw URLError(.badServerResponse)
            }

            let attributes = try fileManager.attributesOfItem(atPath: temporaryURL.path)
            let size = (attributes[.size] as? NSNumber)?.int64Value ?? 0
            guard size > 0 else { throw URLError(.zeroByteResource) }
            guard size <= QuranNetworkLimits.maxAudioCacheFileBytes else {
                throw URLError(.dataLengthExceedsMaximum)
            }

            if fileManager.fileExists(atPath: localURL.path) {
                try fileManager.removeItem(at: localURL)
            }

            try fileManager.moveItem(at: temporaryURL, to: localURL)
            touch(localURL)
            trimIfNeeded()
            return localURL
        } catch {
            // If caching fails, streaming must still work.
            return remoteURL
        }
    }

    func stats() -> (count: Int, bytes: Int64) {
        guard let files = try? fileManager.contentsOfDirectory(
            at: directoryURL,
            includingPropertiesForKeys: [.fileSizeKey],
            options: [.skipsHiddenFiles]
        ) else {
            return (0, 0)
        }

        var count = 0
        var total: Int64 = 0
        for url in files {
            guard let values = try? url.resourceValues(forKeys: [.isRegularFileKey, .fileSizeKey]),
                  values.isRegularFile == true else { continue }

            if count < Int.max { count += 1 }
            let bytes = max(Int64(values.fileSize ?? 0), 0)
            let (nextTotal, overflow) = total.addingReportingOverflow(bytes)
            total = overflow ? Int64.max : nextTotal
        }
        return (count, total)
    }

    func clear() {
        guard fileManager.fileExists(atPath: directoryURL.path) else { return }
        try? fileManager.removeItem(at: directoryURL)
    }

    func invalidate(_ localURL: URL) {
        guard localURL.isFileURL else { return }

        let cacheDirectory = directoryURL.standardizedFileURL
        let parentDirectory = localURL.deletingLastPathComponent().standardizedFileURL
        guard parentDirectory == cacheDirectory else { return }

        try? fileManager.removeItem(at: localURL)
    }

    private func ensureDirectory() throws {
        if !fileManager.fileExists(atPath: directoryURL.path) {
            try fileManager.createDirectory(at: directoryURL, withIntermediateDirectories: true)
        }

        var values = URLResourceValues()
        values.isExcludedFromBackup = true
        var url = directoryURL
        try? url.setResourceValues(values)
    }

    private nonisolated static func isAcceptableAudioMIMEType(_ mimeType: String?) -> Bool {
        guard let mimeType = mimeType?.lowercased(), !mimeType.isEmpty else {
            // Some CDNs omit Content-Type for byte-range/media responses.
            return true
        }

        return mimeType.hasPrefix("audio/") ||
            mimeType == "application/octet-stream" ||
            mimeType == "binary/octet-stream"
    }

    private func destinationURL(for remoteURL: URL) -> URL {
        let rawExtension = remoteURL.pathExtension.lowercased()
        let ext = ["mp3", "m4a", "aac"].contains(rawExtension) ? rawExtension : "mp3"
        return directoryURL.appendingPathComponent("\(String(fnv1a(remoteURL.absoluteString), radix: 16)).\(ext)")
    }

    private func fnv1a(_ value: String) -> UInt64 {
        var hash: UInt64 = 14695981039346656037
        for byte in value.utf8 {
            hash ^= UInt64(byte)
            hash &*= 1099511628211
        }
        return hash
    }

    private func isValidFile(_ url: URL) -> Bool {
        guard fileManager.fileExists(atPath: url.path),
              let attributes = try? fileManager.attributesOfItem(atPath: url.path),
              let size = (attributes[.size] as? NSNumber)?.int64Value else {
            return false
        }
        return size > 0 && size <= QuranNetworkLimits.maxAudioCacheFileBytes
    }

    private func touch(_ url: URL) {
        try? fileManager.setAttributes([.modificationDate: Date()], ofItemAtPath: url.path)
    }

    private func trimIfNeeded() {
        guard let files = try? fileManager.contentsOfDirectory(
            at: directoryURL,
            includingPropertiesForKeys: [.fileSizeKey, .contentModificationDateKey],
            options: [.skipsHiddenFiles]
        ) else { return }

        var entries: [(URL, Int64, Date)] = []
        var total: Int64 = 0

        for url in files {
            guard let values = try? url.resourceValues(
                forKeys: [.isRegularFileKey, .fileSizeKey, .contentModificationDateKey]
            ),
            values.isRegularFile == true else { continue }

            let size = max(Int64(values.fileSize ?? 0), 0)
            let (nextTotal, overflow) = total.addingReportingOverflow(size)
            total = overflow ? Int64.max : nextTotal
            entries.append((url, size, values.contentModificationDate ?? .distantPast))
        }

        guard total > maxBytes else { return }

        for entry in entries.sorted(by: { $0.2 < $1.2 }) {
            try? fileManager.removeItem(at: entry.0)
            total -= entry.1
            if total <= maxBytes { break }
        }
    }
}

@MainActor
final class RemoteAudioPlayer: ObservableObject {
    static let shared = RemoteAudioPlayer()

    @Published var activeURL: URL?
    @Published var isPlaying = false
    @Published var isLoading = false
    @Published var lastError: String?
    @Published var queueIndex = 0
    @Published var queueCount = 0
    @Published private(set) var currentTime: Double = 0
    @Published private(set) var duration: Double = 0
    @Published var playbackRate: Float = 1.0

    private var player: AVPlayer?
    private var queueURLs: [URL] = []
    private var playbackRevision = 0
    private var statusObservation: NSKeyValueObservation?
    private var timeControlObservation: NSKeyValueObservation?
    private var periodicTimeObserver: Any?
    private var endObserver: NSObjectProtocol?
    private var failedObserver: NSObjectProtocol?
    private var remoteCommandTargets: [Any] = []

    private var mediaTitle = "SalahPath Audio"
    private var mediaArtist = "SalahPath"
    private var mediaContext: String?
    private var prayerContext: String?

    private init() {
        configureRemoteCommands()
    }

    var hasNext: Bool { queueIndex + 1 < queueURLs.count }
    var hasPrevious: Bool { queueIndex > 0 }

    func setPrayerContext(_ text: String?) {
        let trimmed = text?.trimmingCharacters(in: .whitespacesAndNewlines)
        prayerContext = (trimmed?.isEmpty == false) ? trimmed : nil
        updateNowPlaying()
    }

    func toggle(
        _ url: URL,
        title: String = "SalahPath Audio",
        artist: String = "SalahPath",
        context: String? = nil
    ) {
        if activeURL == url, player != nil {
            if isPlaying {
                pause()
            } else {
                resume()
            }
            return
        }
        playQueue([url], title: title, artist: artist, context: context)
    }

    func play(
        _ url: URL,
        title: String = "SalahPath Audio",
        artist: String = "SalahPath",
        context: String? = nil
    ) {
        playQueue([url], title: title, artist: artist, context: context)
    }

    func playQueue(
        _ urls: [URL],
        title: String = "SalahPath Audio",
        artist: String = "SalahPath",
        context: String? = nil
    ) {
        let cleaned = urls.filter { $0.isFileURL || $0.scheme?.lowercased() == "https" }
        guard !cleaned.isEmpty else {
            stop()
            lastError = "Audio nicht verfügbar / Ses mevcut değil."
            return
        }

        mediaTitle = title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
            ? "SalahPath Audio"
            : title
        mediaArtist = artist.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
            ? "SalahPath"
            : artist
        let trimmedContext = context?.trimmingCharacters(in: .whitespacesAndNewlines)
        mediaContext = (trimmedContext?.isEmpty == false) ? trimmedContext : nil

        queueURLs = cleaned
        queueCount = cleaned.count
        queueIndex = 0
        updateRemoteCommandAvailability()
        loadCurrentAndPlay()
    }

    func next() {
        guard hasNext else { return }
        queueIndex += 1
        updateRemoteCommandAvailability()
        loadCurrentAndPlay()
    }

    func previous() {
        guard hasPrevious else { return }
        queueIndex -= 1
        updateRemoteCommandAvailability()
        loadCurrentAndPlay()
    }

    func pause() {
        player?.pause()
        isPlaying = false
        updateNowPlaying()
    }

    func resume() {
        guard let player else {
            guard !queueURLs.isEmpty else { return }
            loadCurrentAndPlay()
            return
        }
        lastError = nil
        player.playImmediately(atRate: playbackRate)
        isPlaying = true
        updateNowPlaying()
    }

    func setPlaybackRate(_ rate: Float) {
        let supported: [Float] = [0.75, 1.0, 1.25, 1.5]
        let selected = supported.min(by: { abs($0 - rate) < abs($1 - rate) }) ?? 1.0
        playbackRate = selected
        player?.defaultRate = selected

        if isPlaying {
            player?.rate = selected
        }
        updateNowPlaying()
    }

    func stop() {
        playbackRevision &+= 1
        removeObservers()
        player?.pause()
        player = nil
        queueURLs = []
        queueIndex = 0
        queueCount = 0
        activeURL = nil
        isPlaying = false
        isLoading = false
        currentTime = 0
        duration = 0
        updateRemoteCommandAvailability()
        MPNowPlayingInfoCenter.default().nowPlayingInfo = nil
        MPNowPlayingInfoCenter.default().playbackState = .stopped
    }

    private func loadCurrentAndPlay() {
        guard queueURLs.indices.contains(queueIndex) else { return }

        playbackRevision &+= 1
        let revision = playbackRevision
        removeObservers()
        player?.pause()
        player = nil

        do {
            try AVAudioSession.sharedInstance().setCategory(
                .playback,
                mode: .spokenAudio,
                options: [.allowAirPlay, .allowBluetoothA2DP]
            )
            try AVAudioSession.sharedInstance().setActive(true, options: [])
        } catch {
            lastError = "Audio konnte nicht gestartet werden. Erneut versuchen. / Ses başlatılamadı. Tekrar dene."
            isLoading = false
            isPlaying = false
            return
        }

        lastError = nil
        isLoading = true
        isPlaying = false
        currentTime = 0
        duration = 0

        let sourceURL = queueURLs[queueIndex]
        let expectedIndex = queueIndex
        activeURL = sourceURL
        updateNowPlaying()

        Task { [weak self] in
            let playbackURL = await QuranAudioCache.shared.playbackURL(for: sourceURL)
            guard let self,
                  self.playbackRevision == revision,
                  self.queueIndex == expectedIndex,
                  self.activeURL == sourceURL else { return }
            self.startPlayback(playbackURL)
        }
    }

    private func startPlayback(_ url: URL) {
        let item = AVPlayerItem(url: url)
        let newPlayer = AVPlayer(playerItem: item)
        newPlayer.defaultRate = playbackRate
        player = newPlayer

        periodicTimeObserver = newPlayer.addPeriodicTimeObserver(
            forInterval: CMTime(seconds: 0.5, preferredTimescale: 600),
            queue: .main
        ) { [weak self, weak newPlayer] time in
            Task { @MainActor in
                guard let self else { return }
                let seconds = time.seconds
                self.currentTime = seconds.isFinite && seconds >= 0 ? seconds : 0
                if let itemDuration = newPlayer?.currentItem?.duration.seconds,
                   itemDuration.isFinite,
                   itemDuration > 0 {
                    self.duration = itemDuration
                }
                self.updateNowPlaying()
            }
        }

        statusObservation = item.observe(\.status, options: [.initial, .new]) { [weak self] item, _ in
            Task { @MainActor in
                guard let self else { return }
                switch item.status {
                case .readyToPlay:
                    self.isLoading = false
                    self.lastError = nil
                    let itemDuration = item.duration.seconds
                    if itemDuration.isFinite, itemDuration > 0 {
                        self.duration = itemDuration
                    }
                    self.updateNowPlaying()
                case .failed:
                    self.isLoading = false
                    self.isPlaying = false
                    self.lastError = item.error?.localizedDescription ?? "Audio konnte nicht geladen werden / Ses yüklenemedi."
                    self.updateNowPlaying()
                    if url.isFileURL {
                        Task { await QuranAudioCache.shared.invalidate(url) }
                    }
                default:
                    self.isLoading = true
                }
            }
        }

        timeControlObservation = newPlayer.observe(\.timeControlStatus, options: [.initial, .new]) { [weak self] player, _ in
            Task { @MainActor in
                guard let self else { return }
                self.isPlaying = player.timeControlStatus == .playing
                if player.timeControlStatus == .waitingToPlayAtSpecifiedRate {
                    self.isLoading = true
                }
                if player.timeControlStatus == .playing {
                    self.isLoading = false
                }
                self.updateNowPlaying()
            }
        }

        endObserver = NotificationCenter.default.addObserver(
            forName: .AVPlayerItemDidPlayToEndTime,
            object: item,
            queue: .main
        ) { [weak self] _ in
            Task { @MainActor in
                guard let self else { return }
                if self.hasNext {
                    self.next()
                } else {
                    self.player?.seek(to: .zero)
                    self.currentTime = 0
                    self.isPlaying = false
                    self.isLoading = false
                    self.updateNowPlaying()
                }
            }
        }

        failedObserver = NotificationCenter.default.addObserver(
            forName: .AVPlayerItemFailedToPlayToEndTime,
            object: item,
            queue: .main
        ) { [weak self] note in
            let errorDescription = (note.userInfo?[AVPlayerItemFailedToPlayToEndTimeErrorKey] as? Error)?.localizedDescription

            Task { @MainActor in
                guard let self else { return }
                self.isLoading = false
                self.isPlaying = false
                self.lastError = errorDescription ?? "Audio-Wiedergabe fehlgeschlagen / Ses oynatılamadı."
                self.updateNowPlaying()
                if url.isFileURL {
                    Task { await QuranAudioCache.shared.invalidate(url) }
                }
            }
        }

        newPlayer.playImmediately(atRate: playbackRate)
        isPlaying = true
        updateNowPlaying()
    }

    private func seek(to seconds: Double) {
        guard let player, seconds.isFinite else { return }
        let bounded = min(max(seconds, 0), duration > 0 ? duration : seconds)
        player.seek(to: CMTime(seconds: bounded, preferredTimescale: 600))
        currentTime = bounded
        updateNowPlaying()
    }

    private func updateNowPlaying() {
        guard activeURL != nil else { return }

        var info: [String: Any] = [
            MPMediaItemPropertyTitle: queueCount > 1
                ? "\(mediaTitle) · \(queueIndex + 1)/\(queueCount)"
                : mediaTitle,
            MPMediaItemPropertyArtist: mediaArtist,
            MPNowPlayingInfoPropertyElapsedPlaybackTime: currentTime,
            MPNowPlayingInfoPropertyPlaybackRate: isPlaying ? playbackRate : 0,
            MPNowPlayingInfoPropertyDefaultPlaybackRate: playbackRate,
            MPNowPlayingInfoPropertyPlaybackQueueIndex: queueIndex,
            MPNowPlayingInfoPropertyPlaybackQueueCount: queueCount
        ]

        if duration.isFinite, duration > 0 {
            info[MPMediaItemPropertyPlaybackDuration] = duration
        }

        let context = [mediaContext, prayerContext]
            .compactMap { $0 }
            .filter { !$0.isEmpty }
            .joined(separator: " • ")
        if !context.isEmpty {
            info[MPMediaItemPropertyAlbumTitle] = context
        } else {
            info[MPMediaItemPropertyAlbumTitle] = "SalahPath"
        }

        MPNowPlayingInfoCenter.default().nowPlayingInfo = info
        MPNowPlayingInfoCenter.default().playbackState = isPlaying ? .playing : .paused
    }

    private func configureRemoteCommands() {
        let commands = MPRemoteCommandCenter.shared()

        commands.playCommand.isEnabled = true
        commands.pauseCommand.isEnabled = true
        commands.togglePlayPauseCommand.isEnabled = true
        commands.changePlaybackPositionCommand.isEnabled = true

        remoteCommandTargets.append(
            commands.playCommand.addTarget { [weak self] _ in
                Task { @MainActor [weak self] in self?.resume() }
                return .success
            }
        )
        remoteCommandTargets.append(
            commands.pauseCommand.addTarget { [weak self] _ in
                Task { @MainActor [weak self] in self?.pause() }
                return .success
            }
        )
        remoteCommandTargets.append(
            commands.togglePlayPauseCommand.addTarget { [weak self] _ in
                Task { @MainActor [weak self] in
                    guard let self else { return }
                    self.isPlaying ? self.pause() : self.resume()
                }
                return .success
            }
        )
        remoteCommandTargets.append(
            commands.nextTrackCommand.addTarget { [weak self] _ in
                Task { @MainActor [weak self] in self?.next() }
                return .success
            }
        )
        remoteCommandTargets.append(
            commands.previousTrackCommand.addTarget { [weak self] _ in
                Task { @MainActor [weak self] in self?.previous() }
                return .success
            }
        )
        remoteCommandTargets.append(
            commands.changePlaybackPositionCommand.addTarget { [weak self] event in
                guard let event = event as? MPChangePlaybackPositionCommandEvent else {
                    return .commandFailed
                }
                let position = event.positionTime
                Task { @MainActor [weak self] in self?.seek(to: position) }
                return .success
            }
        )

        updateRemoteCommandAvailability()
    }

    private func updateRemoteCommandAvailability() {
        let commands = MPRemoteCommandCenter.shared()
        commands.nextTrackCommand.isEnabled = hasNext
        commands.previousTrackCommand.isEnabled = hasPrevious
    }

    private func removeObservers() {
        statusObservation = nil
        timeControlObservation = nil
        if let periodicTimeObserver, let player {
            player.removeTimeObserver(periodicTimeObserver)
        }
        periodicTimeObserver = nil
        if let endObserver { NotificationCenter.default.removeObserver(endObserver) }
        if let failedObserver { NotificationCenter.default.removeObserver(failedObserver) }
        endObserver = nil
        failedObserver = nil
    }
}

private struct AudioSpeedControl: View {
    @EnvironmentObject private var settings: SettingsStore
    @ObservedObject var audio: RemoteAudioPlayer
    var compact = false

    private let rates: [Float] = [0.75, 1.0, 1.25, 1.5]

    var body: some View {
        Menu {
            ForEach(rates, id: \.self) { rate in
                Button {
                    audio.setPlaybackRate(rate)
                } label: {
                    if audio.playbackRate == rate {
                        Label(rateLabel(rate), systemImage: "checkmark")
                    } else {
                        Text(rateLabel(rate))
                    }
                }
            }
        } label: {
            HStack(spacing: compact ? 2 : 3) {
                Text(rateLabel(audio.playbackRate))
                    .font(.system(size: compact ? 9 : 11.5, weight: .bold))
                Image(systemName: "chevron.down")
                    .font(.system(size: compact ? 7 : 8, weight: .bold))
            }
            .foregroundStyle(SalahTheme.ink)
            .padding(.horizontal, compact ? 7 : 9)
            .padding(.vertical, compact ? 5 : 6)
            .background(SalahTheme.softTeal, in: Capsule())
        }
        .buttonStyle(.plain)
        .accessibilityLabel(settings.t("Wiedergabegeschwindigkeit", "Oynatma hızı"))
        .accessibilityValue(rateLabel(audio.playbackRate))
    }

    private func rateLabel(_ rate: Float) -> String {
        switch rate {
        case 0.75: return "0.75x"
        case 1.0: return "1.0x"
        case 1.25: return "1.25x"
        case 1.5: return "1.5x"
        default: return String(format: "%.2gx", rate)
        }
    }
}

private struct AudioEditionResponse: Decodable { let data: AudioSurahData }
private struct AudioSurahData: Decodable { let ayahs: [AudioAyahData] }
private struct AudioAyahData: Decodable {
    let number: Int
    let numberInSurah: Int
    let audio: String?
}

enum QuranAudioResolver {
    static func urls(surah: Int, reciter: QuranReciter) async throws -> [URL] {
        guard (1...114).contains(surah) else {
            throw URLError(.badURL)
        }

        var sources: [(edition: String, bitrate: Int)] = [
            (reciter.edition, reciter.bitrate)
        ]
        if let alternate = reciter.alternateAudioSource,
           alternate.edition != reciter.edition {
            sources.append(alternate)
        }

        var lastError: Error = URLError(.resourceUnavailable)

        for source in sources {
            do {
                return try await urls(
                    surah: surah,
                    edition: source.edition,
                    bitrate: source.bitrate
                )
            } catch {
                if Task.isCancelled { throw CancellationError() }
                lastError = error
            }
        }

        throw lastError
    }

    private static func urls(
        surah: Int,
        edition: String,
        bitrate: Int
    ) async throws -> [URL] {
        guard let url = URL(string: "https://api.alquran.cloud/v1/surah/\(surah)/\(edition)") else {
            throw URLError(.badURL)
        }

        var request = URLRequest(url: url)
        request.timeoutInterval = 20

        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse,
              (200...299).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
        guard data.count <= QuranNetworkLimits.maxJSONBytes else {
            throw URLError(.dataLengthExceedsMaximum)
        }

        let decoded = try JSONDecoder().decode(AudioEditionResponse.self, from: data)
        let ayahs = decoded.data.ayahs.sorted { $0.numberInSurah < $1.numberInSurah }
        guard !ayahs.isEmpty else {
            throw URLError(.resourceUnavailable)
        }

        var urls: [URL] = []
        var seenAyahs = Set<Int>()

        for item in ayahs {
            let expectedNumberInSurah = urls.count + 1
            guard item.number > 0,
                  item.numberInSurah == expectedNumberInSurah,
                  seenAyahs.insert(item.numberInSurah).inserted else {
                throw URLError(.cannotParseResponse)
            }

            if let raw = item.audio {
                let secureRaw = raw.replacingOccurrences(of: "http://", with: "https://")
                if let resolved = URL(string: secureRaw),
                   resolved.scheme?.lowercased() == "https" {
                    urls.append(resolved)
                    continue
                }
            }

            let fallback = "https://cdn.islamic.network/quran/audio/\(bitrate)/\(edition)/\(item.number).mp3"
            guard let resolved = URL(string: fallback),
                  resolved.scheme?.lowercased() == "https" else {
                throw URLError(.resourceUnavailable)
            }
            urls.append(resolved)
        }

        return urls
    }
}

private struct PrayerDuaLesson: Identifiable {
    let id = UUID()
    let deTitle: String
    let trTitle: String
    let deDetail: String
    let trDetail: String
    let recitations: [PrayerRecitation]
}

struct PrayerDuaAudioView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let duas: [PrayerDuaLesson] = [
        .init(
            deTitle: "Sübhaneke", trTitle: "Sübhâneke",
            deDetail: "Einstiegsdua im ersten Rakʿah direkt nach dem Eröffnungstakbir.",
            trDetail: "İlk rekâtta iftitah tekbirinden hemen sonra okunan başlangıç duası.",
            recitations: [PrayerText.subhanaka]
        ),
        .init(
            deTitle: "Ettehiyyatü / Tahiyyat", trTitle: "Ettehiyyâtü / Tahiyyat",
            deDetail: "Wird im ersten Sitzen nach zwei Rakʿah und erneut im letzten Sitzen gelesen.",
            trDetail: "İki rekâttan sonraki ilk oturuşta ve son oturuşta okunur.",
            recitations: [PrayerText.tahiyyat]
        ),
        .init(
            deTitle: "Allahümme Salli & Barik", trTitle: "Allâhümme Salli ve Bârik",
            deDetail: "Im letzten Sitzen nach Ettehiyyatü lesen.",
            trDetail: "Son oturuşta Ettehiyyâtü'den sonra okunur.",
            recitations: [PrayerText.salli, PrayerText.barik]
        ),
        .init(
            deTitle: "Rabbena-Dua", trTitle: "Rabbenâ duası",
            deDetail: "Abschlussdua im letzten Sitzen vor dem Salam.",
            trDetail: "Son oturuşta selâmdan önce okunan kapanış duası.",
            recitations: [PrayerText.rabbana]
        ),
        .init(
            deTitle: "Rabbighfirli", trTitle: "Rabbenağfirli / Rabbighfir lî",
            deDetail: "Kurze Bitte um Vergebung; SalahPath zeigt sie auch zwischen den beiden Secden.",
            trDetail: "Kısa bağışlanma duası; SalahPath iki secde arasındaki oturuşta da gösterir.",
            recitations: [PrayerText.rabbighfirli]
        )
    ]

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Alle Gebetsduas stehen direkt in SalahPath: Arabisch, Umschrift und Bedeutung. Es wird keine externe Webseite geöffnet. Ein Audio-Button wird nur dort angezeigt, wo SalahPath auch wirklich Audio abspielen kann.",
                    "Namaz dualarının tamamı doğrudan SalahPath içinde yer alır: Arapça, okunuş ve anlam. Harici web sitesi açılmaz. Ses düğmesi yalnız SalahPath gerçekten ses çalabildiğinde gösterilir."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            ForEach(duas) { item in
                Section(settings.language == .german ? item.deTitle : item.trTitle) {
                    Text(settings.language == .german ? item.deDetail : item.trDetail)
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    ForEach(item.recitations) { recitation in
                        PrayerRecitationView(recitation: recitation)
                    }
                }
            }

            Section(settings.t("Witr", "Vitir")) {
                NavigationLink { QunutDuaView() } label: {
                    Label(settings.t("Qunūt 1 & 2 vollständig", "Kunut 1 ve 2 tam metin"), systemImage: "text.book.closed.fill")
                }
            }

            Section(settings.t("Quelle", "Kaynak")) {
                Text(settings.t(
                    "Diyanet Namaz İlmihali · Gebetsduas und hanafitischer Gebetsablauf.",
                    "Diyanet Namaz İlmihali · namaz duaları ve Hanefî namaz akışı."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetsduas", "Namaz duaları"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct PrayerTextsHubView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Die PDF teilt den Lernstoff in Gebetssuren, Gebetsduas, besondere Ayat und Yasin. SalahPath bildet diese Unterpunkte jetzt direkt ab und öffnet den vollständigen Quran-Text dort, wo er benötigt wird.",
                    "PDF öğrenme bölümünü Namaz Sûreleri, Namaz Duaları, özel ayetler ve Yasin olarak ayırıyor. SalahPath artık bu alt başlıkları doğrudan gösteriyor ve gereken yerde tam Kur'an metnini açıyor."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Gebetssuren", "Namaz Sûreleri")) {
                NavigationLink { ShortSurahLearningView() } label: {
                    Label(settings.t(
                        "Fātiha, Fil, Quraysh, Maun, Kawthar, Kafirun, Nasr, Tebbet, Ikhlas, Falaq, Nas",
                        "Fâtiha, Fîl, Kureyş, Mâûn, Kevser, Kâfirûn, Nasr, Tebbet, İhlâs, Felak, Nâs"
                    ), systemImage: "play.square.stack.fill")
                }
            }

            Section(settings.t("Gebetsduas", "Namaz Duaları")) {
                NavigationLink { PrayerDuaAudioView() } label: {
                    Label(settings.t(
                        "Sübhaneke, Ettehiyyâtü, Salli, Bârik, Rabbena und mehr",
                        "Sübhâneke, Ettehiyyâtü, Salli, Bârik, Rabbenâ ve devamı"
                    ), systemImage: "text.book.closed.fill")
                }

                NavigationLink { QunutDuaView() } label: {
                    Label(settings.t("Qunūt 1 & 2", "Kunut Duaları 1 & 2"), systemImage: "text.quote")
                }
            }

            Section(settings.t("Besondere Ayat", "Ayetler")) {
                QuranReferenceLink(
                    surah: 2, ayah: 255,
                    title: settings.t("Āyat al-Kursī · Al-Baqara 255", "Âyetel Kürsî · Bakara 255")
                )
                QuranReferenceLink(
                    surah: 59, ayah: 22,
                    title: settings.t("Huwa-llāhu lladhī · Al-Hashr 22–24", "Hüvallahüllezi · Haşr 22–24")
                )
                QuranReferenceLink(
                    surah: 2, ayah: 285,
                    title: settings.t("Āmana-r-Rasūlu · Al-Baqara 285–286", "Âmenerresûlü · Bakara 285–286")
                )
            }

            Section("Yasin") {
                QuranReferenceLink(
                    surah: 36, ayah: 1,
                    title: settings.t("Sura Yā-Sīn vollständig öffnen", "Yâsîn Sûresi tam metni aç")
                )
                Text(settings.t(
                    "Im vollständigen Quran-Reader kannst du Arabisch, türkische/deutsche Bedeutung, Audio, Lesezeichen und Lesefortschritt verwenden.",
                    "Tam Kur'an okuyucusunda Arapça, Türkçe/Almanca meal, ses, yer imi ve okuma ilerlemesini kullanabilirsin."
                ))
                .font(.caption)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Gebetstexte", "Namaz Metinleri"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

private struct QuranReferenceLink: View {
    @EnvironmentObject private var settings: SettingsStore
    let surah: Int
    let ayah: Int
    let title: String

    var body: some View {
        NavigationLink {
            QuranReferenceJumpView(surahNumber: surah, ayah: ayah)
        } label: {
            HStack(spacing: 10) {
                Image(systemName: "book.closed.fill")
                    .foregroundStyle(SalahTheme.teal)
                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(.headline)
                    Text("\(surah):\(ayah)")
                        .font(.caption.monospacedDigit())
                        .foregroundStyle(.secondary)
                }
            }
        }
    }
}

private struct QuranReferenceJumpView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()

    let surahNumber: Int
    let ayah: Int

    var body: some View {
        Group {
            if let chapter = store.chapters.first(where: { $0.number == surahNumber }) {
                QuranSurahView(surah: chapter, initialAyah: ayah)
            } else if store.isLoading {
                ProgressView(settings.t("Quran wird geladen…", "Kur'an yükleniyor…"))
            } else if let error = store.error {
                VStack(spacing: 12) {
                    ContentUnavailableView(
                        settings.t("Quran konnte nicht geladen werden", "Kur'an yüklenemedi"),
                        systemImage: "wifi.exclamationmark",
                        description: Text(error)
                    )

                    Button {
                        Task { await store.loadChapters() }
                    } label: {
                        Label(settings.t("Erneut versuchen", "Tekrar dene"), systemImage: "arrow.clockwise")
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(SalahTheme.teal)
                }
                .padding()
            } else {
                ProgressView()
            }
        }
        .task { await store.loadChapters() }
    }
}

private struct ShortSurahAudio: Identifiable {
    let id = UUID()
    let surahNumber: Int
    let arabicName: String
    let latinName: String
    let deDetail: String
    let trDetail: String
}

struct ShortSurahLearningView: View {
    @EnvironmentObject private var settings: SettingsStore
    @ObservedObject private var audio = RemoteAudioPlayer.shared
    @State private var loadingSurah: Int?
    @State private var audioRequestGeneration = 0
    @AppStorage("surahRepeatCount") private var repeatCount = 1

    private let surahs: [ShortSurahAudio] = [
        .init(surahNumber: 1, arabicName: "الفاتحة", latinName: "Al-Fatiha", deDetail: "Grundlage jeder Rakʿah.", trDetail: "Her rekâtın temel kıraatidir."),
        .init(surahNumber: 105, arabicName: "الفيل", latinName: "Al-Fil", deDetail: "Sura aus der Lernliste fürs Gebet.", trDetail: "PDF namaz sûreleri listesindeki Fîl sûresi."),
        .init(surahNumber: 106, arabicName: "قريش", latinName: "Quraysh", deDetail: "Sura aus der Lernliste fürs Gebet.", trDetail: "PDF namaz sûreleri listesindeki Kureyş sûresi."),
        .init(surahNumber: 107, arabicName: "الماعون", latinName: "Al-Maun", deDetail: "Sura aus der Lernliste fürs Gebet.", trDetail: "PDF namaz sûreleri listesindeki Mâûn sûresi."),
        .init(surahNumber: 108, arabicName: "الكوثر", latinName: "Al-Kawthar", deDetail: "Sehr kurze Sura für Lernende.", trDetail: "Öğrenenler için çok kısa sûre."),
        .init(surahNumber: 109, arabicName: "الكافرون", latinName: "Al-Kafirun", deDetail: "Bekannte kurze Sura.", trDetail: "Bilinen kısa sûre."),
        .init(surahNumber: 110, arabicName: "النصر", latinName: "An-Nasr", deDetail: "Sura aus der Lernliste fürs Gebet.", trDetail: "PDF namaz sûreleri listesindeki Nasr sûresi."),
        .init(surahNumber: 111, arabicName: "المسد", latinName: "Al-Masad / Tebbet", deDetail: "In der türkischen Lerntradition oft „Tebbet“ genannt.", trDetail: "Türkçe namaz sûreleri eğitiminde genellikle „Tebbet“ diye anılır."),
        .init(surahNumber: 112, arabicName: "الإخلاص", latinName: "Al-Ikhlas", deDetail: "Kurze und sehr bekannte Sura.", trDetail: "Kısa ve çok bilinen sûre."),
        .init(surahNumber: 113, arabicName: "الفلق", latinName: "Al-Falaq", deDetail: "Schutzsura.", trDetail: "Koruyucu sûre."),
        .init(surahNumber: 114, arabicName: "الناس", latinName: "An-Nas", deDetail: "Schutzsura.", trDetail: "Koruyucu sûre.")
    ]

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Tippe auf Play: SalahPath fragt die aktuelle Audio-URL über die AlQuran.cloud-API ab und spielt danach die Ayat nacheinander. Dadurch sind wir nicht mehr von einem fest eingebauten CDN-Link abhängig.",
                    "Oynat'a dokun: SalahPath güncel ses bağlantılarını AlQuran.cloud API üzerinden alır ve ayetleri sırayla çalar. Böylece sabit bir CDN bağlantısına bağlı kalmaz."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
                if let error = audio.lastError {
                    Label(error, systemImage: "exclamationmark.triangle.fill")
                        .font(.caption)
                        .foregroundStyle(.orange)
                }
            }
            Section(settings.t("Lernmodus", "Öğrenme modu")) {
                Picker(settings.t("Wiederholen", "Tekrar"), selection: $repeatCount) {
                    Text("1×").tag(1)
                    Text("3×").tag(3)
                    Text("5×").tag(5)
                }
                .pickerStyle(.segmented)
                Text(settings.t(
                    "Fürs Auswendiglernen kann die komplette Sura automatisch mehrfach abgespielt werden.",
                    "Ezber için tüm sûre otomatik olarak birkaç kez tekrar çalınabilir."
                ))
                .font(.caption)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Kurze Suren", "Kısa sureler")) {
                ForEach(surahs) { item in
                    HStack(spacing: 12) {
                        VStack(alignment: .leading, spacing: 3) {
                            Text(item.latinName).font(.headline)
                            Text(item.arabicName).font(.subheadline)
                            Text(settings.language == .german ? item.deDetail : item.trDetail)
                                .font(.caption).foregroundStyle(.secondary)
                        }
                        Spacer()
                        Button {
                            Task { await play(item) }
                        } label: {
                            if loadingSurah == item.surahNumber { ProgressView() }
                            else { Image(systemName: "play.circle.fill").font(.title2) }
                        }
                        .buttonStyle(.plain)
                    }
                    .padding(.vertical, 4)
                }
            }
            Section {
                Text("\(settings.t("Rezitator", "Kâri")): \(settings.quranReciter.title)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Suren lernen", "Sureleri öğren"))
        .navigationBarTitleDisplayMode(.inline)
        .onChange(of: settings.quranReciter) { _, _ in
            audioRequestGeneration &+= 1
            loadingSurah = nil
            audio.stop()
        }
        .onDisappear {
            audioRequestGeneration &+= 1
            loadingSurah = nil
        }
    }

    @MainActor
    private func play(_ item: ShortSurahAudio) async {
        audioRequestGeneration &+= 1
        let generation = audioRequestGeneration
        let reciter = settings.quranReciter
        loadingSurah = item.surahNumber
        audio.lastError = nil

        do {
            let urls = try await QuranAudioResolver.urls(
                surah: item.surahNumber,
                reciter: reciter
            )
            guard generation == audioRequestGeneration,
                  reciter == settings.quranReciter else { return }

            let allowedRepeatCounts = [1, 3, 5]
            let safeRepeatCount = allowedRepeatCounts.contains(repeatCount) ? repeatCount : 1
            if repeatCount != safeRepeatCount {
                repeatCount = safeRepeatCount
            }

            audio.playQueue(
                Array(repeating: urls, count: safeRepeatCount).flatMap { $0 },
                title: item.latinName,
                artist: reciter.title,
                context: settings.t("Quran · Sura \(item.surahNumber)", "Kur'an · \(item.surahNumber). sûre")
            )
        } catch {
            guard generation == audioRequestGeneration else { return }
            audio.lastError = error.localizedDescription
        }

        if generation == audioRequestGeneration {
            loadingSurah = nil
        }
    }
}

private struct QuranicDua: Identifiable {
    let id = UUID()
    let reference: String
    let arabic: String
    let transliteration: String
    let de: String
    let tr: String
}

struct QuranicDuaLibraryView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let items: [QuranicDua] = [
        .init(reference: "Quran 2:201", arabic: "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", transliteration: "Rabbanā ātinā fi-d-dunyā ḥasanah wa fi-l-ākhirati ḥasanah wa qinā ʿadhāba-n-nār", de: "Unser Herr, gib uns Gutes im Diesseits und Gutes im Jenseits und bewahre uns vor der Strafe des Feuers.", tr: "Rabbimiz, bize dünyada da iyilik ver, ahirette de iyilik ver ve bizi ateş azabından koru."),
        .init(reference: "Quran 20:114 · excerpt", arabic: "رَبِّ زِدْنِي عِلْمًا", transliteration: "Rabbi zidnī ʿilmā", de: "Mein Herr, mehre mein Wissen.", tr: "Rabbim, ilmimi artır."),
        .init(reference: "Quran 25:74", arabic: "رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا", transliteration: "Rabbanā hab lanā min azwājinā wa dhurriyyātinā qurrata aʿyunin wajʿalnā lil-muttaqīna imāmā.", de: "Unser Herr, schenke uns an unseren Ehepartnern und Nachkommen Freude und mache uns zu Vorbildern für Gottesbewusste.", tr: "Rabbimiz, eşlerimizi ve çocuklarımızı bize göz aydınlığı kıl ve bizi takvâ sahiplerine önder eyle."),
        .init(reference: "Quran 3:8", arabic: "رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِنْ لَدُنْكَ رَحْمَةً إِنَّكَ أَنْتَ الْوَهَّابُ", transliteration: "Rabbanā lā tuzigh qulūbanā baʿda idh hadaytanā wa hab lanā min ladunka raḥmatan innaka anta-l-Wahhāb", de: "Unser Herr, lass unsere Herzen nicht abweichen, nachdem Du uns rechtgeleitet hast, und schenke uns Barmherzigkeit von Dir. Du bist wahrlich der Schenkende.", tr: "Rabbimiz, bize hidayet verdikten sonra kalplerimizi eğriltme; bize katından rahmet bağışla. Şüphesiz Sen çok bağışta bulunansın.")
    ]

    var body: some View {
        List(items) { item in
            VStack(alignment: .leading, spacing: 8) {
                Text(item.reference).font(.caption.bold()).foregroundStyle(.secondary)
                Text(item.arabic).font(.title3).frame(maxWidth: .infinity, alignment: .trailing).multilineTextAlignment(.trailing)
                Text(item.transliteration).font(.subheadline.weight(.semibold))
                Text(settings.language == .german ? item.de : item.tr).font(.footnote).foregroundStyle(.secondary)
            }
            .padding(.vertical, 5)
        }
        .navigationTitle(settings.t("Dua-Sammlung", "Dua koleksiyonu"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Morning / evening adhkar

private struct AdhkarEntry: Identifiable {
    let id: String
    let deTitle: String
    let trTitle: String
    let arabic: String
    let transliteration: String
    let deMeaning: String
    let trMeaning: String
    let count: Int
    let source: String
}

private enum AdhkarProgressStore {
    static func key(id: String, period: String, date: Date) -> String {
        "adhkar-\(LocalDay.token(for: date))-\(period)-\(id)"
    }

    static func value(id: String, period: String, date: Date) -> Int {
        UserDefaults.standard.integer(forKey: key(id: id, period: period, date: date))
    }

    static func set(_ value: Int, id: String, period: String, date: Date) {
        UserDefaults.standard.set(value, forKey: key(id: id, period: period, date: date))
    }
}

struct MorningEveningAdhkarView: View {
    @EnvironmentObject private var settings: SettingsStore
    @Environment(\.scenePhase) private var scenePhase
    @State private var category = 0
    @State private var selectedID = "istighfar"
    @State private var refresh = 0
    @State private var now = Date()

    private let items: [AdhkarEntry] = [
        .init(id: "ayatkursi", deTitle: "Ayat al-Kursi", trTitle: "Âyetel Kürsî", arabic: "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ …", transliteration: "Allāhu lā ilāha illā huwa-l-Ḥayyul-Qayyūm…", deMeaning: "Quran 2:255. Für den vollständigen Text öffne die Sura al-Baqara im Quran-Bereich.", trMeaning: "Kur'an 2:255. Tam metin için Kur'an bölümünde Bakara sûresini aç.", count: 1, source: "Quran 2:255 · Hisn al-Muslim 75"),
        .init(id: "threequls", deTitle: "Al-Ikhlas, Al-Falaq, An-Nas", trTitle: "İhlâs, Felak, Nâs", arabic: "قُلْ هُوَ اللَّهُ أَحَدٌ · قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ · قُلْ أَعُوذُ بِرَبِّ النَّاسِ", transliteration: "Qul huwa-llāhu aḥad · Qul aʿūdhu bi-rabbi-l-falaq · Qul aʿūdhu bi-rabbi-n-nās", deMeaning: "Angezeigt sind nur die Anfangszeilen. Rezitiert werden die vollständigen Suren Al-Ikhlas, Al-Falaq und An-Nas jeweils dreimal.", trMeaning: "Burada yalnız başlangıç satırları gösterilir. İhlâs, Felak ve Nâs sûrelerinin tamamı ayrı ayrı üçer kez okunur.", count: 3, source: "Hisn al-Muslim 76"),
        .init(id: "bika", deTitle: "Allahumma bika asbahna / amsayna", trTitle: "Allahümme bike asbahnâ / emseynâ", arabic: "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ", transliteration: "Allāhumma bika aṣbaḥnā wa bika amsaynā wa bika naḥyā wa bika namūtu wa ilayka-n-nushūr.", deMeaning: "O Allah, durch Dich erreichen wir Morgen und Abend, durch Dich leben und sterben wir, und zu Dir ist die Rückkehr.", trMeaning: "Allah'ım, Senin yardımınla sabaha ve akşama erişiriz; Seninle yaşar ve ölürüz. Dönüş Sanadır.", count: 1, source: "Diyanet Riyâzü’s-Sâlihîn 1458 · Ebû Dâvûd 5068 · Tirmizî 3391"),
        .init(id: "istighfar", deTitle: "Astaghfirullah", trTitle: "Estağfirullâh", arabic: "أَسْتَغْفِرُ اللَّهَ", transliteration: "Astaghfirullāh", deMeaning: "Ich bitte Allah um Vergebung. Hier wird keine bestimmte überlieferte Anzahl behauptet.", trMeaning: "Allah'tan bağışlanma dilerim. Burada rivayet edilmiş belirli bir sayı iddia edilmez.", count: 1, source: "Allgemeines Istighfar / genel istiğfar"),
        .init(id: "protection", deTitle: "Bismillahi alladhi la yadurru", trTitle: "Bismillâhillezî lâ yadurru", arabic: "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ", transliteration: "Bismillāhi-lladhī lā yaḍurru maʿa-smihi shay'un fi-l-arḍi wa lā fi-s-samā' wa huwa-s-Samīʿu-l-ʿAlīm", deMeaning: "Bitte um Schutz, dreimal morgens und dreimal abends überliefert.", trMeaning: "Korunma duası; sabah ve akşam üçer kez rivayet edilmiştir.", count: 3, source: "Hisn al-Muslim 86 · Abu Dawud / Tirmidhi"),
        .init(id: "raditu", deTitle: "Raditu billahi Rabban", trTitle: "Radîtü billâhi Rabben", arabic: "رَضِيتُ بِاللَّهِ رَبًّا وَبِالْإِسْلَامِ دِينًا وَبِمُحَمَّدٍ نَبِيًّا", transliteration: "Raḍītu billāhi Rabban, wa bi-l-Islāmi dīnan, wa bi-Muḥammadin nabiyyan", deMeaning: "Bekenntnis der Zufriedenheit mit Allah als Herrn, Islam als Religion und Muhammad als Propheten.", trMeaning: "Allah'ı Rab, İslâm'ı din ve Muhammed'i peygamber olarak kabul ve hoşnutluk ifadesi.", count: 3, source: "Hisn al-Muslim 87 · Ahmad / Tirmidhi")
    ]

    var body: some View {
        ScrollView {
            VStack(spacing: 12) {
                Picker(settings.t("Kategorie", "Kategori"), selection: $category) {
                    Text(settings.t("Morgen", "Sabah")).tag(0)
                    Text(settings.t("Abend", "Akşam")).tag(1)
                    Text(settings.t("Täglich", "Günlük")).tag(2)
                    Text(settings.t("Speziell", "Özel")).tag(3)
                }
                .pickerStyle(.segmented)
                .padding(6)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))

                if let item = selectedItem {
                    featuredDhikr(item)
                }

                VStack(spacing: 0) {
                    ForEach(visibleItems) { item in
                        Button {
                            selectedID = item.id
                        } label: {
                            HStack(spacing: 10) {
                                Image(systemName: item.id == selectedID ? "checkmark.circle.fill" : "circle")
                                    .foregroundStyle(SalahTheme.teal)
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(settings.language == .german ? item.deTitle : item.trTitle)
                                        .font(.system(size: 13, weight: .bold))
                                        .foregroundStyle(SalahTheme.ink)
                                    Text(item.source)
                                        .font(.system(size: 8.5, weight: .medium))
                                        .foregroundStyle(SalahTheme.mutedInk)
                                        .lineLimit(1)
                                }
                                Spacer()
                                Text("\(progress(item))/\(item.count)")
                                    .font(.caption.bold().monospacedDigit())
                                    .foregroundStyle(SalahTheme.mutedInk)
                                Image(systemName: "chevron.right")
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.teal)
                            }
                            .padding(.horizontal, 13)
                            .padding(.vertical, 11)
                            .contentShape(Rectangle())
                        }
                        .buttonStyle(.plain)
                        if item.id != visibleItems.last?.id { Divider().opacity(0.45) }
                    }
                }
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 17, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 17).stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1) }

                Text(settings.t(
                    "Die Zähler sind eine lokale Hilfe. Überlieferte Varianten und unterschiedliche Einstufungen können existieren.",
                    "Sayaçlar cihaz içi bir yardımcıdır. Rivayetlerde farklılıklar ve farklı değerlendirmeler bulunabilir."
                ))
                .font(.caption2)
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 10)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 10)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Dua & Dhikr", "Dua & Zikir"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            now = Date()
            normalizeSelection()
        }
        .onChange(of: category) { _, _ in normalizeSelection() }
        .onChange(of: scenePhase) { _, phase in
            if phase == .active {
                now = Date()
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
            now = Date()
        }
    }

    private func featuredDhikr(_ item: AdhkarEntry) -> some View {
        let current = progress(item)
        return VStack(spacing: 11) {
            Text(displayArabic(for: item))
                .font(.system(size: displayArabic(for: item).count < 30 ? 34 : 24, weight: .medium))
                .multilineTextAlignment(.center)
                .frame(maxWidth: .infinity)
                .foregroundStyle(SalahTheme.ink)

            Text(settings.language == .german ? item.deTitle : item.trTitle)
                .font(.system(size: 15, weight: .bold))
                .foregroundStyle(SalahTheme.ink)

            Text(settings.language == .german ? item.deMeaning : item.trMeaning)
                .font(.system(size: 11, weight: .medium))
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)

            if item.id == "ayatkursi" {
                NavigationLink {
                    QuranReferenceJumpView(surahNumber: 2, ayah: 255)
                } label: {
                    Label(
                        settings.t("Âyetel-Kürsî vollständig öffnen", "Âyetel Kürsî tam metni aç"),
                        systemImage: "book.closed.fill"
                    )
                    .font(.caption.bold())
                }
                .buttonStyle(.bordered)
                .tint(SalahTheme.teal)
            } else if item.id == "threequls" {
                NavigationLink {
                    ShortSurahLearningView()
                } label: {
                    Label(
                        settings.t("Ikhlas, Falaq und Nas vollständig öffnen", "İhlâs, Felak ve Nâs tam metni aç"),
                        systemImage: "books.vertical.fill"
                    )
                    .font(.caption.bold())
                }
                .buttonStyle(.bordered)
                .tint(SalahTheme.teal)
            }

            HStack(spacing: 18) {
                Button {
                    if current > 0 { setProgress(current - 1, item) }
                } label: {
                    Image(systemName: "minus")
                        .font(.system(size: 16, weight: .bold))
                        .frame(width: 38, height: 38)
                        .background(SalahTheme.softTeal, in: Circle())
                }
                .buttonStyle(.plain)
                .disabled(current == 0)

                Text("\(current)")
                    .font(.system(size: 32, weight: .bold, design: .rounded).monospacedDigit())
                    .foregroundStyle(SalahTheme.ink)
                    .frame(minWidth: 54)

                Button {
                    if current < item.count { setProgress(current + 1, item) }
                } label: {
                    Image(systemName: "plus")
                        .font(.system(size: 16, weight: .bold))
                        .frame(width: 38, height: 38)
                        .background(SalahTheme.gold.opacity(0.22), in: Circle())
                }
                .buttonStyle(.plain)
                .disabled(current >= item.count)
            }
            .foregroundStyle(SalahTheme.teal)

            ProgressView(value: Double(current), total: Double(item.count))
                .tint(SalahTheme.teal)
                .scaleEffect(x: 1, y: 0.78, anchor: .center)

            HStack {
                Text(displayTransliteration(for: item))
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .lineLimit(2)
                Spacer(minLength: 8)
                Text("×\(item.count)")
                    .font(.caption.bold())
                    .padding(.horizontal, 8)
                    .padding(.vertical, 5)
                    .background(SalahTheme.teal.opacity(0.10), in: Capsule())
                    .foregroundStyle(SalahTheme.teal)
            }
        }
        .padding(15)
        .background(
            LinearGradient(
                colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.64)],
                startPoint: .top,
                endPoint: .bottom
            ),
            in: RoundedRectangle(cornerRadius: 18, style: .continuous)
        )
        .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.58), lineWidth: 1) }
        .shadow(color: SalahTheme.deepTeal.opacity(0.055), radius: 7, y: 3)
    }

    private func displayArabic(for item: AdhkarEntry) -> String {
        guard item.id == "bika", category == 1 else { return item.arabic }
        return "اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ أَصْبَحْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ"
    }

    private func displayTransliteration(for item: AdhkarEntry) -> String {
        guard item.id == "bika", category == 1 else { return item.transliteration }
        return "Allāhumma bika amsaynā wa bika aṣbaḥnā wa bika naḥyā wa bika namūtu wa ilayka-l-maṣīr."
    }

    private var visibleItems: [AdhkarEntry] {
        switch category {
        case 0: return items
        case 1: return items
        case 2: return items.filter { ["istighfar", "raditu", "ayatkursi"].contains($0.id) }
        default: return items.filter { ["protection", "threequls"].contains($0.id) }
        }
    }

    private var selectedItem: AdhkarEntry? {
        visibleItems.first(where: { $0.id == selectedID }) ?? visibleItems.first
    }

    private var periodKey: String {
        switch category {
        case 0: return "morning"
        case 1: return "evening"
        case 2: return "daily"
        default: return "special"
        }
    }

    private func normalizeSelection() {
        if !visibleItems.contains(where: { $0.id == selectedID }) {
            selectedID = visibleItems.first?.id ?? "istighfar"
        }
    }

    private func progress(_ item: AdhkarEntry) -> Int {
        let stored = AdhkarProgressStore.value(id: item.id, period: periodKey, date: now)
        return min(max(stored, 0), max(item.count, 0))
    }

    private func setProgress(_ value: Int, _ item: AdhkarEntry) {
        let sanitized = min(max(value, 0), max(item.count, 0))
        AdhkarProgressStore.set(sanitized, id: item.id, period: periodKey, date: now)
        refresh &+= 1
    }
}

// MARK: - Fasting tracker

private enum FastingStore {
    private static let key = "fastingDays"

    static func token(_ date: Date) -> String {
        LocalDay.token(for: date)
    }
    static func tokens() -> Set<String> { Set(UserDefaults.standard.stringArray(forKey: key) ?? []) }
    static func contains(_ date: Date) -> Bool { tokens().contains(token(date)) }
    static func toggle(_ date: Date) {
        var set = tokens(); let t = token(date)
        if set.contains(t) { set.remove(t) } else { set.insert(t) }
        UserDefaults.standard.set(Array(set).sorted(), forKey: key)
    }
}

struct FastingTrackerView: View {
    @EnvironmentObject private var settings: SettingsStore
    @Environment(\.scenePhase) private var scenePhase
    @State private var refresh = 0
    @State private var now = Date()

    private var localCalendar: Calendar {
        LocalDay.calendar()
    }

    private var hijriCalendar: Calendar {
        var calendar = Calendar(identifier: .islamicUmmAlQura)
        calendar.timeZone = .autoupdatingCurrent
        return calendar
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                fastingHeaderCard
                fastingLearningLinks
                fastingTrackerCard
                fastingHistoryCard
                fastingSourceCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Fasten & Ramadan", "Oruç ve Ramazan"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            now = Date()
        }
        .onChange(of: scenePhase) { _, phase in
            if phase == .active {
                now = Date()
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
            now = Date()
        }
    }

    private var fastingHeaderCard: some View {
        VStack(alignment: .leading, spacing: 9) {
            Label(settings.t("Fasten & Ramadan", "Oruç ve Ramazan"), systemImage: "moon.stars.fill")
                .font(.title2.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            Text(settings.t(
                "Hier lernst du das Fasten von Anfang an: wann es beginnt und endet, was es ungültig macht, was nur die Belohnung schädigt und welche Erleichterungen es bei Krankheit, Reise oder anderen Gründen gibt.",
                "Burada orucu en baştan öğrenirsin: ne zaman başlayıp bittiğini, nelerin orucu bozduğunu, nelerin sevabını azalttığını ve hastalık, yolculuk gibi durumlarda hangi ruhsatların bulunduğunu."
            ))
            .font(.subheadline)
            .fixedSize(horizontal: false, vertical: true)

            if hijriCalendar.component(.month, from: now) == 9 {
                Label(
                    settings.t(
                        "Ramadan · Tag \(hijriCalendar.component(.day, from: now))",
                        "Ramazan · \(hijriCalendar.component(.day, from: now)). gün"
                    ),
                    systemImage: "sparkles"
                )
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.teal)
            }
        }
        .cardStyle(material: true)
    }

    @ViewBuilder
    private var fastingLearningLinks: some View {
        fastingNavigationCard(
            title: settings.t("1 · Fasten ganz einfach", "1 · Orucu en kolay şekilde öğren"),
            subtitle: settings.t("Absicht, Sahur, Fajr, Tagesablauf und Iftar", "Niyet, sahur, imsak, günün akışı ve iftar"),
            icon: "1.circle.fill",
            destination: AnyView(FastingBasicsView())
        )

        fastingNavigationCard(
            title: settings.t("2 · Was bricht das Fasten?", "2 · Orucu neler bozar?"),
            subtitle: settings.t("Klare Beispiele, Qada, Kaffarah und häufige Fragen", "Açık örnekler, kaza, kefaret ve sık sorulanlar"),
            icon: "2.circle.fill",
            destination: AnyView(FastingRulesView())
        )

        fastingNavigationCard(
            title: settings.t("3 · Krankheit, Reise & besondere Situationen", "3 · Hastalık, yolculuk ve özel durumlar"),
            subtitle: settings.t("Wann verschieben? Wann Qada? Wann Fidya?", "Ne zaman erteleme, kaza veya fidye gerekir?"),
            icon: "3.circle.fill",
            destination: AnyView(FastingExceptionsView())
        )
    }

    private var fastingTrackerCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(settings.t("Mein Fasten-Tracker", "Oruç takibim"))
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            Toggle(isOn: Binding(
                get: { FastingStore.contains(now) },
                set: { _ in
                    FastingStore.toggle(now)
                    refresh &+= 1
                }
            )) {
                Label(
                    settings.t("Heute als Fastentag markieren", "Bugünü oruç günü olarak işaretle"),
                    systemImage: "checkmark.circle"
                )
            }

            Text(settings.t(
                "Der Tracker speichert nur deine persönliche Liste lokal auf diesem Gerät. Er entscheidet nicht, ob ein Fasten religiös gültig oder verpflichtend ist.",
                "Takip bölümü yalnız kişisel listenizi bu cihazda yerel olarak saklar. Bir orucun dinen geçerli veya zorunlu olup olmadığına karar vermez."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle()
    }

    private var fastingHistoryCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(settings.t("Letzte 14 Tage", "Son 14 gün"))
                .font(.headline.bold())

            ForEach(lastDays, id: \.self) { day in
                fastingHistoryRow(day)
                if day != lastDays.last { Divider() }
            }
        }
        .cardStyle()
    }

    private func fastingHistoryRow(_ day: Date) -> some View {
        Button {
            FastingStore.toggle(day)
            refresh &+= 1
        } label: {
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text(gregorianDateString(day, language: settings.language))
                        .foregroundStyle(SalahTheme.ink)
                    Text(hijriDateString(day, language: settings.language))
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
                Spacer()
                Image(systemName: FastingStore.contains(day) ? "checkmark.circle.fill" : "circle")
                    .foregroundStyle(FastingStore.contains(day) ? .green : .secondary)
            }
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }

    private var fastingSourceCard: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama"))
                .font(.headline)
            Text(settings.t(
                "Die Lerntexte orientieren sich an Diyanet / Din İşleri Yüksek Kurulu und der hanafitischen Grunddarstellung. Wo eine relevante Rechtsschul-Differenz besteht, wird sie ausdrücklich genannt.",
                "Öğrenme metinleri Diyanet / Din İşleri Yüksek Kurulu ve Hanefî temel anlatımına dayanır. Önemli bir mezhep farkı varsa açıkça belirtilir."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }

    @ViewBuilder
    private func fastingNavigationCard(title: String, subtitle: String, icon: String, destination: AnyView) -> some View {
        NavigationLink { destination } label: {
            HStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundStyle(SalahTheme.gold)
                    .frame(width: 44, height: 44)
                    .background(SalahTheme.navigationTeal, in: Circle())
                VStack(alignment: .leading, spacing: 4) {
                    Text(title)
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(subtitle)
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.mutedInk)
                        .fixedSize(horizontal: false, vertical: true)
                }
                Spacer()
                Image(systemName: "chevron.right")
                    .font(.headline.bold())
                    .foregroundStyle(SalahTheme.teal)
            }
            .cardStyle()
        }
        .buttonStyle(.plain)
    }

    private var lastDays: [Date] {
        let calendar = localCalendar
        return (0..<14).compactMap {
            calendar.date(byAdding: .day, value: -$0, to: calendar.startOfDay(for: now))
        }
    }
}

struct FastingBasicsView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section(settings.t("Was bedeutet Fasten?", "Oruç nedir?")) {
                learningText(
                    settings.t("Ganz einfach", "En basit haliyle"),
                    settings.t(
                        "Beim islamischen Fasten verzichtest du mit der Absicht des Fastens vom Beginn des Fajr-Zeitpunkts bis zum Sonnenuntergang auf Essen, Trinken und sexuelle Beziehungen.",
                        "İslâmî oruçta, oruç niyetiyle fecrin başlangıcından güneş batıncaya kadar yeme, içme ve cinsel ilişkiden uzak durulur."
                    )
                )
                learningText(
                    settings.t("Wann beginnt es?", "Ne zaman başlar?"),
                    settings.t(
                        "Das Fasten beginnt mit dem echten Fajr / Im­sak. Suhoor muss vorher beendet sein. 'Sonnenaufgang' ist zu spät.",
                        "Oruç fecr-i sâdık / imsak ile başlar. Sahur bundan önce bitmiş olmalıdır. Güneşin doğuşunu beklemek doğru değildir."
                    )
                )
                learningText(
                    settings.t("Wann endet es?", "Ne zaman biter?"),
                    settings.t(
                        "Sobald die Sonne vollständig untergegangen ist, beginnt die Maghrib-Zeit und du darfst das Fasten brechen.",
                        "Güneş tamamen battığında akşam vakti girer ve oruç açılabilir."
                    )
                )
            }

            Section(settings.t("Niyyah / Absicht", "Niyet")) {
                Text(settings.t(
                    "Die Absicht ist Voraussetzung. Die Absicht im Herzen reicht. Für jeden Ramadan-Tag wird neu beabsichtigt zu fasten; schon das bewusste Aufstehen zum Suhoor kann die Absicht ausdrücken.",
                    "Niyet orucun şartıdır. Kalpten niyet etmek yeterlidir. Ramazan'ın her günü için yeniden niyet edilir; sahura oruç tutmak amacıyla kalkmak da niyet sayılabilir."
                ))
                .fixedSize(horizontal: false, vertical: true)

                Text(settings.t(
                    "Hanafi/Diyanet: Für Ramadan kann unter bestimmten Voraussetzungen auch nach Imsak bis vor die islamische Mittagsgrenze niyet gemacht werden, sofern seit Fajr nichts Fastenwidriges getan wurde. Sicherer und besser ist die Absicht in der Nacht. Andere Rechtsschulen können hier strenger sein.",
                    "Hanefî/Diyanet: Ramazan orucuna, imsaktan sonra oruca aykırı bir şey yapılmamışsa belirli şartlarla gündüz kuşluk/öğle sınırından önce de niyet edilebilir. Geceden niyet etmek daha güvenli ve faziletlidir. Diğer mezheplerde hüküm daha sıkı olabilir."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Ein Fastentag Schritt für Schritt", "Bir oruç günü adım adım")) {
                numbered("1", settings.t("Vor Fajr: Suhoor essen und trinken. Nicht bis zur letzten Sekunde hetzen.", "Fecrden önce: Sahur yap, ye ve iç. Son saniyeye bırakma."))
                numbered("2", settings.t("Absicht im Herzen: Heute faste ich den Ramadan-Tag für Allah.", "Kalben niyet et: Bugünkü Ramazan orucunu Allah için tutuyorum."))
                numbered("3", settings.t("Ab Fajr: nichts essen oder trinken und die Fastenregeln einhalten.", "Fecrden itibaren: yeme-içmeyi bırak ve oruç hükümlerine uy."))
                numbered("4", settings.t("Tagsüber: Gebete, Quran, Dhikr, Dua, gute Taten und gutes Verhalten pflegen.", "Gündüz: namaz, Kur'an, zikir, dua, iyi ameller ve güzel ahlâka özen göster."))
                numbered("5", settings.t("Bei Sonnenuntergang: Iftar. Danach Maghrib nicht unnötig hinauszögern.", "Güneş batınca: İftar et. Ardından akşam namazını gereksiz yere geciktirme."))
            }

            Section(settings.t("Verhalten im Ramadan", "Ramazan'da davranış")) {
                Text(settings.t(
                    "Fasten bedeutet mehr als Hunger und Durst. Lügen, Beleidigungen, Streit, üble Nachrede und andere Sünden widersprechen dem Sinn des Fastens und können seinen Lohn stark schmälern. Sie machen den Fastentag aber nicht automatisch in jedem Fall fiqh-rechtlich ungültig. Deshalb trennt SalahPath 'Fasten ungültig' von 'Belohnung schädigen'.",
                    "Oruç yalnız açlık ve susuzluk değildir. Yalan, hakaret, kavga, gıybet ve diğer günahlar orucun ruhuna aykırıdır ve sevabını ciddi şekilde azaltabilir. Ancak bunlar her durumda fıkhen orucu otomatik olarak bozmaz. Bu nedenle SalahPath 'orucu bozar' ile 'sevabını azaltır' ifadelerini ayırır."
                ))
                .fixedSize(horizontal: false, vertical: true)
            }

            Section(settings.t("Quelle", "Kaynak")) {
                Text(settings.t(
                    "Diyanet / Din İşleri Yüksek Kurulu · Orucun mahiyeti, niyet, sünnetler ve adab.",
                    "Diyanet / Din İşleri Yüksek Kurulu · Orucun mahiyeti, niyet, sünnetleri ve adabı."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Fasten lernen", "Orucu öğren"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func learningText(_ title: String, _ text: String) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title).font(.headline)
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }

    @ViewBuilder
    private func numbered(_ number: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Text(number)
                .font(.caption.bold())
                .foregroundStyle(.white)
                .frame(width: 24, height: 24)
                .background(SalahTheme.teal, in: Circle())
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }
}

struct FastingRulesView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section(settings.t("Grundregel", "Temel kural")) {
                Text(settings.t(
                    "Bewusstes Essen, Trinken oder Geschlechtsverkehr während eines begonnenen Ramadan-Fastens macht das Fasten ungültig. Ob nur Qada oder zusätzlich Kaffarah nötig ist, hängt vom konkreten Fall ab.",
                    "Başlanmış Ramazan orucunda bilerek yemek, içmek veya cinsel ilişki orucu bozar. Yalnız kaza mı yoksa ayrıca kefaret mi gerektiği somut duruma göre değişir."
                ))
            }

            Section(settings.t("Bricht das Fasten", "Orucu bozar")) {
                rule("fork.knife", settings.t("Bewusst essen oder trinken", "Bilerek yemek veya içmek"), settings.t("Bei absichtlichem Bruch eines gültig begonnenen Ramadan-Fastens kann nach hanafitischer Einordnung zusätzlich zur Qada auch Kaffarah nötig sein.", "Geçerli başlanmış Ramazan orucunun bilerek bozulmasında Hanefî hükme göre kazaya ek olarak kefaret de gerekebilir."))
                rule("smoke.fill", settings.t("Rauchen / Nargile", "Sigara / nargile"), settings.t("Das Fasten wird dadurch ungültig.", "Oruç bozulur."))
                rule("drop.triangle.fill", settings.t("Nährende Infusionen / Nahrung über den Körper", "Besleyici serum / gıda niteliğinde uygulamalar"), settings.t("Nährende oder einer Nahrungsaufnahme gleichkommende Zuführung bricht nach Diyanet das Fasten; medizinische Einzelfälle separat prüfen.", "Besleyici veya gıda hükmündeki uygulamalar Diyanet'e göre orucu bozar; tıbbî özel durumlar ayrıca değerlendirilmelidir."))
                rule("arrow.uturn.down", settings.t("Absichtlich mundvoll erbrechen", "Bilerek ağız dolusu kusmak"), settings.t("Erfordert nach der hanafitischen Darstellung Qada.", "Hanefî anlatıma göre kaza gerekir."))
                rule("drop.fill", settings.t("Beim Wudu versehentlich Wasser schlucken", "Abdestte yanlışlıkla su yutmak"), settings.t("Wenn du wusstest, dass du fastest, und Wasser versehentlich in den Rachen gelangt, gilt das im Hanafi/Diyanet-Ablauf als gebrochen und Qada ist nötig. Shafi'i kann hier anders urteilen.", "Oruçlu olduğunu bilirken abdest suyunun yanlışlıkla boğaza kaçması Hanefî/Diyanet hükmünde orucu bozar ve kaza gerekir. Şafiî mezhebinde hüküm farklı olabilir."))
            }

            Section(settings.t("Bricht nicht automatisch", "Otomatik olarak bozmaz")) {
                rule("brain.head.profile", settings.t("Vergessen essen oder trinken", "Unutarak yemek veya içmek"), settings.t("Bricht das Fasten nicht. Sobald du dich erinnerst, sofort aufhören und weiterfasten.", "Orucu bozmaz. Hatırlayınca hemen bırak ve oruca devam et."))
                rule("cross.case.fill", settings.t("Nicht nährende Spritze / Impfung", "Besleyici olmayan iğne / aşı"), settings.t("Diyanet bewertet nicht nährende Behandlungsinjektionen und Impfungen grundsätzlich als nicht fastenbrechend.", "Diyanet, besleyici olmayan tedavi iğneleri ve aşıları genel olarak orucu bozmayan uygulamalar arasında değerlendirir."))
                rule("mouth.fill", settings.t("Zähne putzen", "Diş fırçalamak"), settings.t("Das Putzen selbst bricht nicht; Zahnpasta oder Wasser darf nicht geschluckt werden. Wegen des Risikos empfiehlt Diyanet besondere Vorsicht.", "Fırçalamak tek başına orucu bozmaz; macun veya su yutulmamalıdır. Diyanet risk nedeniyle dikkat tavsiye eder."))
                rule("arrow.up.to.line", settings.t("Unfreiwilliges Erbrechen", "İstem dışı kusmak"), settings.t("Spontanes Erbrechen bricht das Fasten nicht.", "Kendiliğinden kusmak orucu bozmaz."))
            }

            Section(settings.t("Qada, Kaffarah, Fidya – nicht verwechseln", "Kaza, kefaret, fidye – karıştırma")) {
                definition(settings.t("Qada", "Kaza"), settings.t("Einen verpassten oder ungültig gewordenen Fastentag später nachholen.", "Kaçırılan veya bozulan oruç gününü daha sonra tutmak."))
                definition(settings.t("Kaffarah", "Kefaret"), settings.t("Zusätzliche Sühne bei bestimmten bewusst begangenen Brüchen eines Ramadan-Fastens. Nicht jeder gebrochene Fastentag löst Kaffarah aus.", "Ramazan orucunun belirli kasıtlı ihlallerinde gereken ek kefarettir. Her bozulan oruç kefaret gerektirmez."))
                definition(settings.t("Fidya", "Fidye"), settings.t("Ausgleich für Menschen, die dauerhaft nicht fasten und später auch nicht nachholen können, z. B. wegen sehr hohen Alters oder unheilbarer chronischer Krankheit.", "Yaşlılık veya iyileşme ümidi olmayan kalıcı hastalık gibi nedenlerle oruç tutup daha sonra kaza etme imkânı bulunmayanlar için verilen bedeldir."))
            }

            Section(settings.t("Wichtig", "Önemli")) {
                Text(settings.t(
                    "Bei einem konkreten medizinischen Eingriff oder einer persönlichen Sonderlage zeigt SalahPath keine pauschale 'Fatwa-Automatik'. Nutze die allgemeinen Regeln hier und kläre einen unklaren Einzelfall mit einer qualifizierten religiösen Stelle und bei Gesundheitsthemen mit medizinischem Fachpersonal.",
                    "Belirli bir tıbbî işlem veya kişisel özel durumda SalahPath otomatik fetva vermez. Buradaki genel kuralları kullan; belirsiz bireysel durumu ehil bir dinî merciden, sağlık konusunu da sağlık uzmanından doğrula."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Was bricht das Fasten?", "Orucu ne bozar?"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func rule(_ icon: String, _ title: String, _ detail: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Image(systemName: icon)
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 24)
            VStack(alignment: .leading, spacing: 3) {
                Text(title).font(.headline)
                Text(detail).font(.subheadline).foregroundStyle(.secondary).fixedSize(horizontal: false, vertical: true)
            }
        }
    }

    @ViewBuilder
    private func definition(_ title: String, _ detail: String) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(title).font(.headline).foregroundStyle(SalahTheme.deepTeal)
            Text(detail).fixedSize(horizontal: false, vertical: true)
        }
    }
}

struct FastingExceptionsView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section(settings.t("Wer ist grundsätzlich verpflichtet?", "Kimlere farzdır?")) {
                Text(settings.t(
                    "Ramadan-Fasten ist für muslimische, geistig zurechnungsfähige und pubertäre Personen verpflichtend. Kinder vor der Pubertät sind nicht verpflichtet; sie können altersgerecht und ohne Schaden ans Fasten herangeführt werden.",
                    "Ramazan orucu Müslüman, akıllı ve buluğa ermiş kişilere farzdır. Buluğa ermemiş çocuklar yükümlü değildir; zarar vermeden yaşına uygun şekilde oruca alıştırılabilir."
                ))
            }

            Section(settings.t("Vorübergehender Grund → später Qada", "Geçici mazeret → sonra kaza")) {
                exception(settings.t("Krankheit", "Hastalık"), settings.t("Wenn Fasten die Krankheit verschlimmern, verlängern oder voraussichtlich krank machen würde, darf verschoben und später nachgeholt werden.", "Oruç hastalığı artıracak, uzatacak veya kişiyi hasta edecekse ertelenebilir; daha sonra kaza edilir."))
                exception(settings.t("Reise", "Yolculuk"), settings.t("Eine religiös als Reise geltende Fahrt kann eine Erleichterung geben. Nach Diyanet/Hanafi gelten konkrete Reisebedingungen; verpasste Tage werden später nachgeholt.", "Dinî sefer sayılan yolculuk ruhsat sebebi olabilir. Diyanet/Hanefî ölçülerinde belirli şartlar vardır; tutulmayan günler sonra kaza edilir."))
                exception(settings.t("Schwangerschaft / Stillzeit", "Hamilelik / emzirme"), settings.t("Besteht begründete Sorge um Mutter oder Kind, darf nicht gefastet und später Qada gemacht werden.", "Anne veya çocuk için zarar endişesi varsa oruç tutulmayabilir; daha sonra kaza edilir."))
                exception(settings.t("Menstruation / Nifas", "Hayız / nifas"), settings.t("Während Menstruation und Wochenbett/Nifas wird nicht gefastet; diese Ramadan-Tage werden später als Qada nachgeholt.", "Hayız ve nifas döneminde oruç tutulmaz; Ramazan'da tutulmayan günler daha sonra kaza edilir."))
            }

            Section(settings.t("Dauerhaft nicht möglich → Fidya", "Kalıcı olarak mümkün değil → fidye")) {
                exception(settings.t("Sehr hohes Alter", "İleri yaş"), settings.t("Wer dauerhaft nicht mehr fasten kann und auch später keine Möglichkeit zur Qada hat, fällt unter die Fidya-Regel.", "Kalıcı olarak oruç tutamayan ve daha sonra kaza imkânı bulunmayan ileri yaştaki kişi fidye hükmüne girer."))
                exception(settings.t("Unheilbare chronische Krankheit", "İyileşme ümidi olmayan kronik hastalık"), settings.t("Wenn nach realistischer Einschätzung keine spätere Fastenfähigkeit zu erwarten ist, gilt ebenfalls die Fidya-Regel.", "Daha sonra oruç tutabilecek hale gelme ümidi yoksa fidye hükmü uygulanır."))
                Text(settings.t(
                    "Wird jemand später doch wieder dauerhaft fastenfähig, beschreibt Diyanet für die hanafitische Einordnung, dass die versäumten Tage nachgeholt werden; eine zuvor gezahlte Fidya gilt dann als freiwillige Sadaqah.",
                    "Kişi daha sonra yeniden sürekli oruç tutabilecek hale gelirse Diyanet'in Hanefî açıklamasına göre kaçırdığı günleri kaza eder; önceden verilen fidye nafile sadaka sayılır."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Nicht pauschal entscheiden", "Genelleme yapma")) {
                Text(settings.t(
                    "Gesundheit ist individuell. Bei Krankheit, Schwangerschaft, Medikamenten oder anderen medizinischen Fragen darf die App keine Diagnose ersetzen. Religiöse Erleichterung und medizinische Belastbarkeit müssen im konkreten Fall sauber beurteilt werden.",
                    "Sağlık kişiye özeldir. Hastalık, hamilelik, ilaç veya diğer tıbbî konularda uygulama teşhis yerine geçmez. Dinî ruhsat ve sağlık açısından dayanıklılık somut durumda doğru değerlendirilmelidir."
                ))
            }

            Section(settings.t("Quelle", "Kaynak")) {
                Text(settings.t(
                    "Diyanet / Din İşleri Yüksek Kurulu · Bedingungen der Fastenpflicht, erlaubte Entschuldigungsgründe, Qada und Fidya.",
                    "Diyanet / Din İşleri Yüksek Kurulu · oruç yükümlülüğü, mazeretler, kaza ve fidye."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Erleichterungen", "Ruhsatlar"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func exception(_ title: String, _ detail: String) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(title).font(.headline)
            Text(detail).font(.subheadline).foregroundStyle(.secondary).fixedSize(horizontal: false, vertical: true)
        }
    }
}

// MARK: - Hijri calendar

private struct IslamicCalendarEvent: Identifiable {
    let id = UUID()
    let symbol: String
    let deTitle: String
    let trTitle: String
    let deMeaning: String
    let trMeaning: String
    let deRecommended: [String]
    let trRecommended: [String]
    let deCaution: String
    let trCaution: String
}

private struct IslamicCalendarDraft: Identifiable {
    let id = UUID()
    let title: String
    let date: Date
    let notes: String
}

private struct CalendarEventEditor: UIViewControllerRepresentable {
    let draft: IslamicCalendarDraft
    @Environment(\.dismiss) private var dismiss

    final class Coordinator: NSObject, EKEventEditViewDelegate {
        private let onDismiss: @MainActor @Sendable () -> Void

        init(onDismiss: @escaping @MainActor @Sendable () -> Void) {
            self.onDismiss = onDismiss
        }

        func eventEditViewController(
            _ controller: EKEventEditViewController,
            didCompleteWith action: EKEventEditViewAction
        ) {
            let onDismiss = onDismiss
            Task { @MainActor in
                onDismiss()
            }
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator {
            dismiss()
        }
    }

    func makeUIViewController(context: Context) -> EKEventEditViewController {
        let eventStore = EKEventStore()
        let event = EKEvent(eventStore: eventStore)
        var calendar = Calendar.autoupdatingCurrent
        calendar.timeZone = .autoupdatingCurrent
        let start = calendar.startOfDay(for: draft.date)

        event.title = draft.title
        event.startDate = start
        event.endDate = calendar.date(byAdding: .day, value: 1, to: start) ?? start
        event.isAllDay = true
        event.notes = draft.notes

        let controller = EKEventEditViewController()
        controller.eventStore = eventStore
        controller.event = event
        controller.editViewDelegate = context.coordinator
        return controller
    }

    func updateUIViewController(
        _ uiViewController: EKEventEditViewController,
        context: Context
    ) {}
}

private struct IslamicCalendarEventDetailView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var calendarDraft: IslamicCalendarDraft?

    let date: Date
    let event: IslamicCalendarEvent

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                eventHeaderCard
                calendarExportButton
                eventMeaningCard
                eventRecommendationsCard
                eventCautionCard
                eventSourceCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(localizedEventTitle)
        .navigationBarTitleDisplayMode(.inline)
        .sheet(item: $calendarDraft) { draft in
            CalendarEventEditor(draft: draft)
        }
    }

    private var localizedEventTitle: String {
        settings.language == .german ? event.deTitle : event.trTitle
    }

    private var eventHeaderCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Label(localizedEventTitle, systemImage: event.symbol)
                .font(.title2.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            Text(gregorianDateString(date, language: settings.language))
                .font(.subheadline.bold())
                .foregroundStyle(SalahTheme.teal)

            Text(hijriDateString(date, language: settings.language))
                .font(.headline)
        }
        .cardStyle(material: true)
    }

    private var calendarExportButton: some View {
        Button {
            calendarDraft = IslamicCalendarDraft(
                title: localizedEventTitle,
                date: date,
                notes: settings.t(
                    "SalahPath · berechnetes Hijri-Datum nach Umm al-Qura. Regionale Mondsichtung kann abweichen.",
                    "SalahPath · Ummü'l-Kurâ'ya göre hesaplanan hicrî tarih. Bölgesel hilal gözlemi farklı olabilir."
                )
            )
        } label: {
            Label(
                settings.t("In Apple Kalender eintragen", "Apple Takvim'e ekle"),
                systemImage: "calendar.badge.plus"
            )
            .font(.headline.bold())
            .frame(maxWidth: .infinity)
            .padding(.vertical, 13)
        }
        .buttonStyle(.plain)
        .foregroundStyle(.white)
        .background(
            SalahTheme.deepTeal,
            in: RoundedRectangle(cornerRadius: 15, style: .continuous)
        )
    }

    private var eventMeaningCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(settings.t("Was bedeutet dieser Tag?", "Bu gün ne anlama gelir?"))
                .font(.headline)
            Text(settings.language == .german ? event.deMeaning : event.trMeaning)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle()
    }

    private var eventRecommendationsCard: some View {
        let items = settings.language == .german ? event.deRecommended : event.trRecommended
        return VStack(alignment: .leading, spacing: 10) {
            Text(settings.t("Was ist empfohlen?", "Neler tavsiye edilir?"))
                .font(.headline)

            ForEach(items.indices, id: \.self) { index in
                HStack(alignment: .top, spacing: 9) {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundStyle(SalahTheme.teal)
                    Text(items[index])
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
        }
        .cardStyle()
    }

    private var eventCautionCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Label(
                settings.t("Nicht verwechseln", "Karıştırma"),
                systemImage: "exclamationmark.triangle.fill"
            )
            .font(.headline)
            .foregroundStyle(SalahTheme.gold)

            Text(settings.language == .german ? event.deCaution : event.trCaution)
                .font(.subheadline)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle(material: true)
    }

    private var eventSourceCard: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(settings.t("Quelle & Kalenderhinweis", "Kaynak ve takvim notu"))
                .font(.headline)
            Text(settings.t(
                "Religiöse Einordnung nach Qur'an, Hadithquellen und Diyanet-Grunddarstellung. Bei Überlieferungen können unterschiedliche Einstufungen bestehen. Das angezeigte Hijri-Datum wird mit Umm-al-Qura berechnet; regionale Mondsichtung kann den tatsächlichen Monatsbeginn verschieben.",
                "Dinî açıklama Kur'an, hadis kaynakları ve Diyanet temel anlatımına dayanır. Rivayetlerin değerlendirilmesinde farklılıklar bulunabilir. Gösterilen hicrî tarih Ummü'l-Kurâ hesabıdır; bölgesel hilal gözlemi gerçek ay başlangıcını değiştirebilir."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }
}


struct HijriCalendarView: View {
    @EnvironmentObject private var settings: SettingsStore
    @Environment(\.scenePhase) private var scenePhase
    @State private var now = Date()

    private var localCalendar: Calendar {
        LocalDay.calendar()
    }

    private var hijriCalendar: Calendar {
        var calendar = Calendar(identifier: .islamicUmmAlQura)
        calendar.timeZone = .autoupdatingCurrent
        return calendar
    }

    var body: some View {
        List {
            hijriTodaySection
            hijriImportantEventsSection
            hijriNextThirtyDaysSection
            hijriRecommendedFastingSection
        }
        .navigationTitle(settings.t("Hijri-Kalender", "Hicrî takvim"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            now = Date()
        }
        .onChange(of: scenePhase) { _, phase in
            if phase == .active {
                now = Date()
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
            now = Date()
        }
    }

    @ViewBuilder
    private var hijriTodaySection: some View {
        Section {
            VStack(alignment: .leading, spacing: 8) {
                Text(settings.t("Heute", "Bugün"))
                    .font(.caption.bold())
                    .foregroundStyle(SalahTheme.teal)
                Text(hijriDateString(now, language: settings.language))
                    .font(.title2.bold())
                    .foregroundStyle(SalahTheme.deepTeal)
                Text(gregorianDateString(now, language: settings.language))
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
            .padding(.vertical, 4)

            Text(settings.t(
                "Umm-al-Qura ist ein berechneter Kalender. Tatsächliche Monatsanfänge können je nach regionaler Mondsichtung abweichen. SalahPath kennzeichnet deshalb zukünftige religiöse Daten als berechnet.",
                "Ummü'l-Kurâ hesaplanmış bir takvimdir. Gerçek ay başlangıçları bölgesel hilal gözlemine göre değişebilir. Bu nedenle SalahPath gelecekteki dinî tarihleri hesaplanan tarih olarak gösterir."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
    }

    @ViewBuilder
    private var hijriImportantEventsSection: some View {
        Section(settings.t("Nächste wichtige islamische Tage", "Yaklaşan önemli İslâmî günler")) {
            ForEach(nextImportantEvents) { item in
                NavigationLink {
                    IslamicCalendarEventDetailView(date: item.date, event: item.event)
                } label: {
                    importantEventRow(item)
                }
            }
        }
    }

    private func importantEventRow(_ item: DatedEvent) -> some View {
        HStack(spacing: 11) {
            Image(systemName: item.event.symbol)
                .font(.title3)
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 30)

            VStack(alignment: .leading, spacing: 3) {
                Text(settings.language == .german ? item.event.deTitle : item.event.trTitle)
                    .font(.headline)
                Text(hijriDateString(item.date, language: settings.language))
                    .font(.subheadline)
                Text(gregorianDateString(item.date, language: settings.language))
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
    }

    @ViewBuilder
    private var hijriNextThirtyDaysSection: some View {
        Section(settings.t("Die nächsten 30 Tage", "Önümüzdeki 30 gün")) {
            ForEach(days, id: \.self) { date in
                hijriDayRow(date)
            }
        }
    }

    private func hijriDayRow(_ date: Date) -> some View {
        HStack {
            VStack(alignment: .leading, spacing: 3) {
                Text(gregorianDateString(date, language: settings.language))
                    .font(.subheadline)
                Text(hijriDateString(date, language: settings.language))
                    .font(.headline)
                if let event = eventInfo(date) {
                    Label(
                        settings.language == .german ? event.deTitle : event.trTitle,
                        systemImage: event.symbol
                    )
                    .font(.caption)
                    .foregroundStyle(SalahTheme.teal)
                }
            }

            Spacer()

            if localCalendar.isDateInToday(date) {
                Text(settings.t("Heute", "Bugün"))
                    .font(.caption.bold())
                    .foregroundStyle(.tint)
            }
        }
    }

    @ViewBuilder
    private var hijriRecommendedFastingSection: some View {
        Section(settings.t("Regelmäßig empfohlene Fastentage", "Düzenli tavsiye edilen oruç günleri")) {
            calendarInfo(
                settings.t("Weiße Tage · 13., 14. und 15. jedes Hijri-Monats", "Eyyâm-ı bîd · her hicrî ayın 13, 14 ve 15'i"),
                settings.t(
                    "Freiwilliges Fasten an diesen drei Tagen ist empfohlen. Es ist kein Pflichtfasten.",
                    "Bu üç günde nafile oruç tavsiye edilir. Farz değildir."
                )
            )
            calendarInfo(
                settings.t("Montag und Donnerstag", "Pazartesi ve Perşembe"),
                settings.t(
                    "Freiwilliges Fasten an diesen Wochentagen ist aus der Sunnah bekannt. Es ist kein Pflichtfasten.",
                    "Bu günlerde nafile oruç sünnette yer alır. Farz değildir."
                )
            )
            calendarInfo(
                settings.t("6 Tage im Shawwal", "Şevval'de 6 gün"),
                settings.t(
                    "Nach Ramadan sind sechs freiwillige Fastentage im Shawwal empfohlen; sie müssen nicht an feste Kalendertage gebunden sein und ersetzen keine offenen Ramadan-Qada-Tage.",
                    "Ramazan'dan sonra Şevval ayında altı gün nafile oruç tavsiye edilir; sabit günlere bağlı değildir ve tutulmamış Ramazan kazalarının yerine geçmez."
                )
            )
        }
    }

    private var days: [Date] {
        (0..<30).compactMap { localCalendar.date(byAdding: .day, value: $0, to: localCalendar.startOfDay(for: now)) }
    }

    private struct DatedEvent: Identifiable {
        let id: String
        let date: Date
        let event: IslamicCalendarEvent
    }

    private var nextImportantEvents: [DatedEvent] {
        var result: [DatedEvent] = []
        let start = localCalendar.startOfDay(for: now)

        for offset in 0..<400 {
            guard let date = localCalendar.date(byAdding: .day, value: offset, to: start),
                  let event = eventInfo(date) else { continue }

            let components = hijriCalendar.dateComponents([.year, .month, .day], from: date)
            let token = "\(components.year ?? 0)-\(components.month ?? 0)-\(components.day ?? 0)-\(event.deTitle)"
            result.append(.init(id: token, date: date, event: event))

            if result.count >= 10 { break }
        }

        return result
    }

    private func eventInfo(_ date: Date) -> IslamicCalendarEvent? {
        let m = hijriCalendar.component(.month, from: date)
        let d = hijriCalendar.component(.day, from: date)

        if m == 1 && d == 1 {
            return .init(
                symbol: "calendar.badge.clock",
                deTitle: "1. Muharram · Beginn des Hijri-Jahres",
                trTitle: "1 Muharrem · Hicrî yılın başlangıcı",
                deMeaning: "Muharram ist der erste Monat des Hijri-Kalenders und gehört zu den vier heiligen Monaten. Der Jahresbeginn ist ein Kalenderdatum; im Islam gibt es dafür kein vorgeschriebenes 'Neujahrsfest'.",
                trMeaning: "Muharrem hicrî takvimin ilk ayıdır ve dört haram aydan biridir. Yıl başlangıcı bir takvim tarihidir; bunun için dinen zorunlu bir 'yılbaşı kutlaması' yoktur.",
                deRecommended: ["Muharram als besonderen Monat kennen.", "Freiwilliges Fasten ist in Muharram besonders verdienstvoll.", "Sich auf ʿAshura am 10. Muharram vorbereiten."],
                trRecommended: ["Muharrem ayının önemini öğren.", "Muharrem'de nafile oruç faziletlidir.", "10 Muharrem Aşure gününe hazırlan."],
                deCaution: "Keine bestimmte Feier, Dekoration oder besondere Gebetsform als verpflichtende Sunnah darstellen.",
                trCaution: "Belirli bir kutlama, süsleme veya özel namaz şeklini zorunlu sünnet gibi gösterme."
            )
        }

        if m == 1 && d == 10 {
            return .init(
                symbol: "moon.stars",
                deTitle: "ʿAshura · 10. Muharram",
                trTitle: "Aşure · 10 Muharrem",
                deMeaning: "ʿAshura ist der 10. Muharram. Freiwilliges Fasten an diesem Tag ist aus der Sunnah bekannt.",
                trMeaning: "Aşure günü 10 Muharrem'dir. Bu günde nafile oruç tutmak sünnette yer alır.",
                deRecommended: ["Am 10. Muharram freiwillig fasten.", "Nach hanafitischer/Diyanet-Empfehlung zusätzlich den 9. oder 11. Muharram mitfasten."],
                trRecommended: ["10 Muharrem'de nafile oruç tut.", "Hanefî/Diyanet tavsiyesinde 9. veya 11. Muharrem'i de ekle."],
                deCaution: "Das Fasten ist freiwillig, nicht Farz. Regionale Kulturbräuche rund um 'Aşure' sind nicht mit einer verpflichtenden Gottesdienstform gleichzusetzen.",
                trCaution: "Bu oruç farz değil, nafiledir. Aşure etrafındaki kültürel gelenekler zorunlu ibadet şekliyle aynı değildir."
            )
        }

        if m == 9 && d == 1 {
            return .init(
                symbol: "moon.fill",
                deTitle: "Beginn des Ramadan",
                trTitle: "Ramazan başlangıcı",
                deMeaning: "Ramadan ist der neunte Hijri-Monat. Das Fasten dieses Monats gehört zu den fünf Säulen des Islam für diejenigen, die die Voraussetzungen erfüllen.",
                trMeaning: "Ramazan hicrî takvimin dokuzuncu ayıdır. Şartları taşıyanlar için bu ayın orucu İslâm'ın beş şartından biridir.",
                deRecommended: ["Das Fasten mit bewusster Absicht beginnen.", "Gebete, Qur'an, Dua, Dhikr und Sadaqah bewusst verstärken.", "Sahur und Iftar ohne Verschwendung gestalten."],
                trRecommended: ["Niyet ederek oruca başla.", "Namaz, Kur'an, dua, zikir ve sadakayı artır.", "Sahur ve iftarda israftan kaçın."],
                deCaution: "Der genaue Beginn kann regional von der Mondsichtung abhängen. SalahPath zeigt hier ein berechnetes Datum.",
                trCaution: "Kesin başlangıç bölgesel hilal gözlemine göre değişebilir. SalahPath burada hesaplanan tarihi gösterir."
            )
        }

        if m == 9 && d == 21 {
            return .init(
                symbol: "sparkles",
                deTitle: "Beginn der letzten zehn Ramadan-Nächte",
                trTitle: "Ramazan'ın son on gecesinin başlangıcı",
                deMeaning: "In den letzten zehn Nächten wird Laylat al-Qadr besonders gesucht. Die authentische Überlieferung lenkt auf die ungeraden Nächte dieser letzten zehn.",
                trMeaning: "Son on gecede Kadir Gecesi özellikle aranır. Sahih rivayetler son on gecenin tek gecelerine yönlendirir.",
                deRecommended: ["Gebet, Qur'an, Dua und Dhikr verstärken.", "Besonders die ungeraden Nächte ernst nehmen.", "Die bekannte Dua um Vergebung lernen."],
                trRecommended: ["Namaz, Kur'an, dua ve zikri artır.", "Özellikle tek geceleri değerlendirmeye çalış.", "Af dileme duasını öğren."],
                deCaution: "Laylat al-Qadr nicht sicher ausschließlich auf die 27. Nacht festlegen. Sie wird in den ungeraden Nächten der letzten zehn gesucht.",
                trCaution: "Kadir Gecesi'ni kesin olarak yalnız 27. geceye sabitleme. Son on gecenin tek gecelerinde aranır."
            )
        }

        if m == 10 && d == 1 {
            return .init(
                symbol: "party.popper.fill",
                deTitle: "Eid al-Fitr · 1. Shawwal",
                trTitle: "Ramazan Bayramı · 1 Şevval",
                deMeaning: "Eid al-Fitr beginnt nach Abschluss des Ramadan. An diesem Festtag wird nicht gefastet.",
                trMeaning: "Ramazan Bayramı Ramazan'ın tamamlanmasından sonra başlar. Bayramın birinci gününde oruç tutulmaz.",
                deRecommended: ["Eid-Gebet entsprechend der örtlichen Gemeinde beachten.", "Familie besuchen, Freude teilen und Bedürftige nicht vergessen.", "Offene Ramadan-Qada-Tage später nachholen."],
                trRecommended: ["Bayram namazını yerel cemaatle değerlendirmeye çalış.", "Aileyi ziyaret et, sevinci paylaş, ihtiyaç sahiplerini unutma.", "Eksik Ramazan kazalarını daha sonra tamamla."],
                deCaution: "Am ersten Shawwal ist Fasten verboten. Die empfohlenen sechs Shawwal-Tage beginnen daher erst nach dem Eid-Tag.",
                trCaution: "1 Şevval'de oruç tutulmaz. Tavsiye edilen altı Şevval orucu bayramın ilk gününden sonra tutulur."
            )
        }

        if m == 12 && d == 9 {
            return .init(
                symbol: "mountain.2.fill",
                deTitle: "Tag von ʿArafah · 9. Dhu l-Hijjah",
                trTitle: "Arefe günü · 9 Zilhicce",
                deMeaning: "Der 9. Dhu l-Hijjah ist der Tag von ʿArafah und ein zentraler Tag des Hajj.",
                trMeaning: "9 Zilhicce Arefe günüdür ve haccın en önemli günlerinden biridir.",
                deRecommended: ["Für Nicht-Pilger ist freiwilliges Fasten an ʿArafah besonders empfohlen.", "Dua, Dhikr und gute Taten vermehren."],
                trRecommended: ["Hacda olmayanlar için Arefe orucu özellikle tavsiye edilir.", "Dua, zikir ve hayırlı amelleri artır."],
                deCaution: "Pilger auf ʿArafah werden nicht pauschal wie Nicht-Pilger zum Fasten angehalten; Kraft für die Hajj-Handlungen hat Vorrang.",
                trCaution: "Arafat'taki hacılar, hac dışındaki kişiler gibi genel olarak oruca teşvik edilmez; hac ibadetlerine güç ayırmak önceliklidir."
            )
        }

        if m == 12 && d == 10 {
            return .init(
                symbol: "gift.fill",
                deTitle: "Eid al-Adha · 10. Dhu l-Hijjah",
                trTitle: "Kurban Bayramı · 10 Zilhicce",
                deMeaning: "Eid al-Adha ist das Opferfest und fällt in die Hajj-Zeit.",
                trMeaning: "Kurban Bayramı hac mevsimindeki büyük bayramdır.",
                deRecommended: ["Eid-Gebet beachten.", "Opferpflicht bzw. Opfer-Sunnah nach den persönlichen hanafitischen Voraussetzungen prüfen.", "Familie und Bedürftige am Fest teilhaben lassen."],
                trRecommended: ["Bayram namazını değerlendir.", "Kurban yükümlülüğünü kişisel Hanefî şartlara göre kontrol et.", "Aileyi ve ihtiyaç sahiplerini bayram sevincine ortak et."],
                deCaution: "Am Eid-Tag wird nicht gefastet.",
                trCaution: "Bayram günü oruç tutulmaz."
            )
        }

        if m == 12 && (11...13).contains(d) {
            return .init(
                symbol: "sun.max.fill",
                deTitle: "Tage des Tashriq · \(d). Dhu l-Hijjah",
                trTitle: "Teşrik günleri · \(d) Zilhicce",
                deMeaning: "Die Tage nach dem ersten Opferfesttag heißen Tage des Tashriq.",
                trMeaning: "Kurban Bayramı'nın ilk gününden sonraki bu günlere teşrik günleri denir.",
                deRecommended: ["Nach den Farz-Gebeten die hanafitischen Tashriq-Takbire entsprechend ihrer Zeit beachten.", "Allah gedenken, essen, trinken und die Festtage bewusst verbringen."],
                trRecommended: ["Hanefî uygulamada farz namazlardan sonra teşrik tekbirlerini zamanına göre getir.", "Allah'ı zikret, yiyip iç ve bayram günlerini bilinçli geçir."],
                deCaution: "Diese Tage sind keine gewöhnlichen freiwilligen Fastentage.",
                trCaution: "Bu günler normal nafile oruç günleri değildir."
            )
        }

        return nil
    }

    @ViewBuilder
    private func calendarInfo(_ title: String, _ detail: String) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(title).font(.headline)
            Text(detail)
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}

// MARK: - Islam learning hub

private struct IslamLearningStore {
    private static let key = "islamLearningCompletedIDs"

    static func completed() -> Set<String> {
        Set(UserDefaults.standard.stringArray(forKey: key) ?? [])
    }

    static func isCompleted(_ id: String) -> Bool {
        completed().contains(id)
    }

    static func toggle(_ id: String) {
        var set = completed()
        if set.contains(id) {
            set.remove(id)
        } else {
            set.insert(id)
        }
        UserDefaults.standard.set(Array(set).sorted(), forKey: key)
    }
}

private struct IslamLearningLesson: Identifiable {
    let id: String
    let icon: String
    let deTitle: String
    let trTitle: String
    let deIntro: String
    let trIntro: String
    let dePoints: [String]
    let trPoints: [String]
    let deDetail: String
    let trDetail: String
}

private struct IslamLearningLessonView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var refresh = 0
    let lesson: IslamLearningLesson

    private var completed: Bool {
        _ = refresh
        return IslamLearningStore.isCompleted(lesson.id)
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                lessonHeaderCard
                lessonPointsCard
                lessonDetailCard
                lessonCompletionButton
                lessonSourceCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.language == .german ? lesson.deTitle : lesson.trTitle)
        .navigationBarTitleDisplayMode(.inline)
    }

    private var lessonHeaderCard: some View {
        VStack(alignment: .leading, spacing: 9) {
            Label(
                settings.language == .german ? lesson.deTitle : lesson.trTitle,
                systemImage: lesson.icon
            )
            .font(.title2.bold())
            .foregroundStyle(SalahTheme.deepTeal)

            Text(settings.language == .german ? lesson.deIntro : lesson.trIntro)
                .font(.body)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle(material: true)
    }

    private var lessonPointsCard: some View {
        let points = settings.language == .german ? lesson.dePoints : lesson.trPoints
        return VStack(alignment: .leading, spacing: 10) {
            Text(settings.t("Das solltest du zuerst verstehen", "Önce bunları anlamalısın"))
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            ForEach(points.indices, id: \.self) { index in
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundStyle(SalahTheme.teal)
                        .padding(.top, 2)
                    Text(points[index])
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
        }
        .cardStyle()
    }

    private var lessonDetailCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(settings.t("Etwas genauer", "Biraz daha ayrıntılı"))
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.deepTeal)
            Text(settings.language == .german ? lesson.deDetail : lesson.trDetail)
                .font(.body)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle()
    }

    private var lessonCompletionButton: some View {
        Button {
            IslamLearningStore.toggle(lesson.id)
            refresh &+= 1
        } label: {
            Label(
                completed
                    ? settings.t("Als gelernt markiert", "Öğrenildi olarak işaretli")
                    : settings.t("Als gelernt markieren", "Öğrendim olarak işaretle"),
                systemImage: completed ? "checkmark.seal.fill" : "checkmark.seal"
            )
            .font(.headline.bold())
            .frame(maxWidth: .infinity)
            .padding(.vertical, 13)
        }
        .buttonStyle(.plain)
        .foregroundStyle(completed ? .white : SalahTheme.deepTeal)
        .background(
            completed ? SalahTheme.deepTeal : SalahTheme.cream,
            in: RoundedRectangle(cornerRadius: 15, style: .continuous)
        )
        .overlay {
            RoundedRectangle(cornerRadius: 15, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.50), lineWidth: 1)
        }
    }

    private var lessonSourceCard: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama"))
                .font(.headline)
            Text(settings.t(
                "Grundlage: Qur'an, Hadithquellen und Diyanet Temel İslâm Bilgileri / İlmihal. Bei Hadith-Einstufungen und strittigen Fiqh-Fragen können Unterschiede bestehen; Rechtsschulunterschiede werden soweit relevant gekennzeichnet.",
                "Temel kaynak: Kur'an, hadis kaynakları ve Diyanet Temel İslâm Bilgileri / İlmihal. Hadis değerlendirmelerinde ve ihtilaflı fıkıh konularında farklılıklar olabilir; ilgili mezhep farkları ayrıca belirtilir."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }

}

struct IslamLearningHubView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var refresh = 0

    private let lessons: [IslamLearningLesson] = [
        .init(
            id: "what_is_islam",
            icon: "moon.stars.fill",
            deTitle: "Was bedeutet Islam?",
            trTitle: "İslâm ne demektir?",
            deIntro: "Islam bedeutet, sich Allah anzuvertrauen, Ihm allein zu dienen und Seiner Rechtleitung zu folgen.",
            trIntro: "İslâm, Allah'a teslim olmak, yalnız O'na kulluk etmek ve O'nun hidayetine uymaktır.",
            dePoints: [
                "Muslime glauben an den einen Gott: Allah.",
                "Islam verbindet Glauben, Gottesdienst und Charakter – nicht nur einzelne Rituale.",
                "Die Offenbarung des Qur'an und das Vorbild des Propheten Muhammad ﷺ bilden die zentrale Grundlage."
            ],
            trPoints: [
                "Müslümanlar tek olan Allah'a iman eder.",
                "İslâm yalnız ritüellerden ibaret değildir; iman, ibadet ve ahlâkı birlikte kapsar.",
                "Kur'an vahyi ve Hz. Muhammed'in ﷺ örnekliği temel kaynaktır."
            ],
            deDetail: "Das arabische Wort Islam hängt mit Hingabe und Frieden zusammen. Muslim zu sein bedeutet nicht, fehlerlos zu sein. Der Mensch glaubt, bemüht sich um Gehorsam, bereut Fehler und kehrt zu Allah zurück. Wissen soll dabei zu Gottesdienst und gutem Verhalten führen.",
            trDetail: "İslâm kelimesi teslimiyet ve selâmet anlamlarıyla ilişkilidir. Müslüman olmak hatasız olmak demek değildir. İnsan iman eder, itaat için çaba gösterir, hatalarından tövbe eder ve Allah'a döner. Bilgi ibadete ve güzel ahlâka götürmelidir."
        ),
        .init(
            id: "shahada",
            icon: "quote.bubble.fill",
            deTitle: "Shahada · Glaubensbekenntnis",
            trTitle: "Kelime-i şehadet",
            deIntro: "Die Shahada fasst den Kern des islamischen Glaubens zusammen: Allah allein ist anbetungswürdig und Muhammad ﷺ ist Sein Gesandter.",
            trIntro: "Kelime-i şehadet İslâm inancının özünü özetler: Allah'tan başka ilâh yoktur ve Muhammed ﷺ O'nun elçisidir.",
            dePoints: [
                "Arabisch: أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللّٰهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ",
                "Bedeutung: Ich bezeuge, dass niemand außer Allah anbetungswürdig ist, und ich bezeuge, dass Muhammad Sein Diener und Gesandter ist.",
                "Das Bekenntnis ist nicht nur ein Satz: Es drückt Glauben und Annahme aus."
            ],
            trPoints: [
                "Arapça: أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللّٰهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ",
                "Anlamı: Allah'tan başka ilâh olmadığına ve Muhammed'in O'nun kulu ve elçisi olduğuna şahitlik ederim.",
                "Şehadet yalnız söylenen bir cümle değil; iman ve kabul ifadesidir."
            ],
            deDetail: "Die erste Hälfte schützt den Tawhid: Gottesdienst richtet sich an Allah allein. Die zweite Hälfte bedeutet, Muhammad ﷺ als letzten Propheten und Gesandten anzuerkennen und seiner authentisch überlieferten Lehre zu folgen.",
            trDetail: "İlk bölüm tevhidi ifade eder: ibadet yalnız Allah'a yapılır. İkinci bölüm Hz. Muhammed'i ﷺ son peygamber ve elçi olarak kabul etmeyi ve sahih sünnetine uymayı ifade eder."
        ),
        .init(
            id: "five_pillars",
            icon: "building.columns.fill",
            deTitle: "Die fünf Säulen",
            trTitle: "İslâm'ın beş şartı",
            deIntro: "Die fünf Säulen beschreiben die grundlegenden praktischen Pflichten des muslimischen Lebens.",
            trIntro: "İslâm'ın beş şartı Müslüman hayatının temel amelî ibadetlerini özetler.",
            dePoints: [
                "Shahada: Glaubensbekenntnis.",
                "Salah: die fünf täglichen Pflichtgebete.",
                "Zakat: verpflichtende Abgabe für Berechtigte, wenn die Voraussetzungen erfüllt sind.",
                "Sawm: Fasten im Ramadan.",
                "Hajj: Pilgerfahrt nach Mekka einmal im Leben, wenn die Voraussetzungen erfüllt sind."
            ],
            trPoints: [
                "Kelime-i şehadet: iman ikrarı.",
                "Namaz: beş vakit farz namaz.",
                "Zekât: şartları oluşan kişilerin vermesi gereken malî ibadet.",
                "Oruç: Ramazan orucu.",
                "Hac: şartları oluşan kişinin ömründe bir kez Mekke'ye hac yapması."
            ],
            deDetail: "Nicht jede Säule gilt in jeder Lebenssituation identisch. Zakat und Hajj haben z. B. finanzielle und weitere Voraussetzungen. Fasten kennt erlaubte Entschuldigungsgründe. Salah bleibt die tägliche zentrale körperliche Pflicht; Details lernst du in den eigenen SalahPath-Bereichen.",
            trDetail: "Her şart her durumda aynı şekilde yükümlülük doğurmaz. Örneğin zekât ve hac için malî ve başka şartlar vardır. Oruçta ruhsat sebepleri bulunur. Namaz günlük temel bedenî ibadettir; ayrıntıları SalahPath'in ilgili bölümlerinde öğrenebilirsin."
        ),
        .init(
            id: "six_beliefs",
            icon: "hexagon.fill",
            deTitle: "Die sechs Glaubensgrundsätze",
            trTitle: "İmanın altı esası",
            deIntro: "In der bekannten Zusammenfassung werden sechs grundlegende Glaubensbereiche genannt.",
            trIntro: "Yaygın özette iman esasları altı başlık altında anlatılır.",
            dePoints: [
                "Glaube an Allah.",
                "Glaube an Seine Engel.",
                "Glaube an Seine offenbarten Bücher.",
                "Glaube an Seine Propheten und Gesandten.",
                "Glaube an den Jüngsten Tag und das Jenseits.",
                "Glaube an Qadar: Allahs Wissen und Bestimmung – ohne die menschliche Verantwortung aufzuheben."
            ],
            trPoints: [
                "Allah'a iman.",
                "Meleklerine iman.",
                "Kitaplarına iman.",
                "Peygamberlerine iman.",
                "Âhiret gününe iman.",
                "Kadere iman: Allah'ın bilgisi ve takdiri; insanın sorumluluğunu ortadan kaldırmaz."
            ],
            deDetail: "Diese Grundlagen bilden die ʿAqida. Bei Qadar ist wichtig: Allahs Wissen und Schöpfungsmacht bedeuten nicht, dass der Mensch keine Verantwortung für seine bewussten Entscheidungen hätte. Details dieser theologischen Fragen sollten nicht auf vereinfachte Schlagworte reduziert werden.",
            trDetail: "Bu esaslar akaidin temelini oluşturur. Kader konusunda önemli nokta şudur: Allah'ın bilgisi ve yaratma kudreti, insanın bilinçli tercihlerindeki sorumluluğunu ortadan kaldırmaz. Bu teolojik konu basit sloganlara indirgenmemelidir."
        ),
        .init(
            id: "allah_tawhid",
            icon: "sparkles",
            deTitle: "Allah & Tawhid",
            trTitle: "Allah ve tevhid",
            deIntro: "Tawhid bedeutet, Allah als den Einen anzuerkennen und Gottesdienst ausschließlich Ihm zu widmen.",
            trIntro: "Tevhid, Allah'ı bir bilmek ve ibadeti yalnız O'na yöneltmektir.",
            dePoints: [
                "Allah ist der Schöpfer und nichts ist Ihm gleich.",
                "Dua, Anbetung und letztliche Hingabe richten sich an Allah.",
                "Allah wird nicht als Mensch, Bild oder geschaffene Gestalt vorgestellt."
            ],
            trPoints: [
                "Allah yaratıcıdır ve hiçbir şey O'nun benzeri değildir.",
                "Dua, ibadet ve kulluk Allah'a yöneltilir.",
                "Allah insan, resim veya yaratılmış bir şekil gibi düşünülmez."
            ],
            deDetail: "Der Qur'an betont Allahs Einzigkeit, Wissen, Macht, Barmherzigkeit und Gerechtigkeit. Muslime lernen Allah durch die Namen und Eigenschaften kennen, die in Qur'an und authentischer Sunnah überliefert sind, ohne Ihn mit der Schöpfung gleichzusetzen.",
            trDetail: "Kur'an Allah'ın birliğini, ilmini, kudretini, rahmetini ve adaletini vurgular. Müslümanlar Allah'ı Kur'an ve sahih sünnette bildirilen isim ve sıfatlarla tanır; O'nu yaratılmışlara benzetmez."
        ),
        .init(
            id: "prophet",
            icon: "person.text.rectangle.fill",
            deTitle: "Prophet Muhammad ﷺ",
            trTitle: "Hz. Muhammed ﷺ",
            deIntro: "Muhammad ﷺ ist im Islam der letzte Prophet und Gesandte Allahs.",
            trIntro: "Hz. Muhammed ﷺ İslâm'da Allah'ın son peygamberi ve elçisidir.",
            dePoints: [
                "Er übermittelte den Qur'an und erklärte die Religion durch Wort und Praxis.",
                "Muslime lieben und respektieren ihn, beten ihn aber nicht an.",
                "Sunnah bedeutet sein authentisch überliefertes Vorbild."
            ],
            trPoints: [
                "Kur'an'ı tebliğ etti ve dini sözleriyle ve uygulamasıyla açıkladı.",
                "Müslümanlar onu sever ve saygı gösterir; fakat ona ibadet etmez.",
                "Sünnet, onun sahih şekilde aktarılan örnekliğidir."
            ],
            deDetail: "Seine Biografie heißt Sira. Für religiöse Regeln ist wichtig, zwischen authentisch überlieferten Hadithen, schwachen Berichten und späteren kulturellen Geschichten zu unterscheiden. SalahPath soll deshalb keine beliebte Geschichte automatisch als religiöse Tatsache behandeln.",
            trDetail: "Hayatını anlatan alana siyer denir. Dinî hükümler açısından sahih hadisleri, zayıf rivayetleri ve sonradan oluşmuş kültürel anlatıları ayırmak önemlidir. SalahPath popüler bir hikâyeyi otomatik olarak dinî gerçek gibi sunmamalıdır."
        ),
        .init(
            id: "quran",
            icon: "book.closed.fill",
            deTitle: "Der Qur'an",
            trTitle: "Kur'an",
            deIntro: "Der Qur'an ist für Muslime Allahs Offenbarung an Muhammad ﷺ in arabischer Sprache.",
            trIntro: "Kur'an Müslümanlara göre Allah'ın Hz. Muhammed'e ﷺ Arapça olarak indirdiği vahiydir.",
            dePoints: [
                "Er besteht aus 114 Suren.",
                "Eine Übersetzung hilft beim Verstehen, ist aber nicht identisch mit dem arabischen Qur'an-Text.",
                "Lesen, verstehen und danach handeln gehören zusammen."
            ],
            trPoints: [
                "114 sûreden oluşur.",
                "Meal anlamayı kolaylaştırır; fakat Arapça Kur'an metninin kendisiyle aynı değildir.",
                "Okumak, anlamak ve yaşamak birlikte düşünülmelidir."
            ],
            deDetail: "Für Anfänger ist es sinnvoll, kurze Suren, Al-Fatiha und grundlegende Bedeutungen zu lernen. SalahPath trennt deshalb arabischen Text, Umschrift und Übersetzung. Die Umschrift ist nur eine Lernhilfe und ersetzt das korrekte arabische Lesen nicht dauerhaft.",
            trDetail: "Yeni başlayanlar için kısa sûreleri, Fâtiha'yı ve temel anlamları öğrenmek faydalıdır. SalahPath bu nedenle Arapça metni, okunuşu ve meali ayırır. Latin harfli okunuş yalnız öğrenme yardımıdır; doğru Arapça okumanın kalıcı olarak yerini tutmaz."
        ),
        .init(
            id: "purity_worship",
            icon: "drop.fill",
            deTitle: "Reinheit & Gottesdienst",
            trTitle: "Temizlik ve ibadet",
            deIntro: "Rituelle Reinheit ist eine Voraussetzung für bestimmte Gottesdienste, besonders das Gebet.",
            trIntro: "Hükmî temizlik bazı ibadetlerin, özellikle namazın şartlarındandır.",
            dePoints: [
                "Wudu für die kleine rituelle Unreinheit.",
                "Ghusl in Situationen, in denen die Ganzkörperwaschung erforderlich ist.",
                "Tayammum als erlaubte Ersatzreinigung, wenn die Voraussetzungen erfüllt sind."
            ],
            trPoints: [
                "Küçük hadeste abdest.",
                "Boy abdesti gereken durumlarda gusül.",
                "Şartları oluştuğunda su yerine teyemmüm."
            ],
            deDetail: "Reinheit im Islam umfasst sowohl körperliche Sauberkeit als auch rechtlich definierte rituelle Reinheit. Beides darf nicht verwechselt werden. Ein sauber aussehender Körper bedeutet nicht automatisch Wudu, und Wudu ersetzt nicht jede Situation, in der Ghusl erforderlich ist.",
            trDetail: "İslâm'da temizlik hem beden temizliğini hem de fıkhî hükmî temizliği kapsar. Bunlar aynı şey değildir. Bedenin temiz görünmesi otomatik olarak abdestli olmak demek değildir; abdest de gusül gereken her durumun yerine geçmez."
        ),
        .init(
            id: "akhlaq",
            icon: "heart.fill",
            deTitle: "Akhlaq · guter Charakter",
            trTitle: "Ahlâk",
            deIntro: "Islamische Religiosität betrifft nicht nur Gebet und Fasten, sondern auch den Umgang mit Menschen.",
            trIntro: "İslâmî hayat yalnız namaz ve oruçtan ibaret değildir; insanlarla ilişkileri de kapsar.",
            dePoints: [
                "Wahrhaftigkeit, Vertrauenswürdigkeit und Gerechtigkeit.",
                "Respekt gegenüber Eltern, Familie, Nachbarn und anderen Menschen.",
                "Keine Verleumdung, üble Nachrede, Betrug oder bewusstes Unrecht."
            ],
            trPoints: [
                "Doğruluk, güvenilirlik ve adalet.",
                "Anne-baba, aile, komşu ve diğer insanlara saygı.",
                "İftira, gıybet, hile ve bilinçli haksızlıktan uzak durmak."
            ],
            deDetail: "Guter Charakter ist kein Zusatzmodul neben der Religion. Qur'an und Sunnah verbinden Gottesdienst mit Verantwortung gegenüber anderen. Eine Person kann deshalb nicht schlechte Behandlung anderer damit rechtfertigen, dass sie viele freiwillige Rituale verrichtet.",
            trDetail: "Güzel ahlâk dinin dışında ek bir bölüm değildir. Kur'an ve sünnet ibadeti insanlara karşı sorumlulukla birlikte ele alır. Bu nedenle çok nafile ibadet yapmak, başkalarına kötü davranmayı meşrulaştırmaz."
        ),
        .init(
            id: "halal_haram",
            icon: "scale.3d",
            deTitle: "Halal, Haram & Zweifel",
            trTitle: "Helâl, haram ve şüpheli şeyler",
            deIntro: "Halal bedeutet religiös erlaubt; Haram bedeutet religiös verboten. Nicht jede persönliche Abneigung ist automatisch Haram.",
            trIntro: "Helâl dinen izin verilen, haram ise dinen yasaklanan şeydir. Kişisel hoşnutsuzluk her şeyi otomatik olarak haram yapmaz.",
            dePoints: [
                "Klare Verbote brauchen eine religiöse Grundlage.",
                "Zwischen Farz, Wajib, Sunnah, Makruh, Mubah und Haram unterscheiden.",
                "Bei strittigen Fragen Rechtsschule und Beleg nennen statt pauschal zu urteilen."
            ],
            trPoints: [
                "Açık yasak için dinî delil gerekir.",
                "Farz, vacip, sünnet, mekruh, mubah ve haramı birbirinden ayır.",
                "İhtilaflı konularda kesin genelleme yerine mezhep ve delili belirt."
            ],
            deDetail: "SalahPath soll Begriffe nicht inflationär verwenden. 'Haram' ist eine rechtliche Bewertung, nicht bloß 'ich finde es schlecht'. Ebenso bedeutet 'Sunnah' nicht automatisch Pflicht. In Hanafi-Fiqh gibt es zusätzlich die Kategorie Wajib, die von Farz unterschieden wird.",
            trDetail: "SalahPath kavramları gelişigüzel kullanmamalıdır. 'Haram' fıkhî bir hükümdür; yalnız 'bence kötü' anlamına gelmez. 'Sünnet' de otomatik olarak farz değildir. Hanefî fıkhında ayrıca farzdan ayrı 'vacip' kategorisi vardır."
        ),
        .init(
            id: "repentance",
            icon: "arrow.uturn.backward.circle.fill",
            deTitle: "Tawbah · Reue und Neubeginn",
            trTitle: "Tövbe ve yeniden başlamak",
            deIntro: "Ein Muslim, der einen Fehler macht, soll nicht glauben, dass Rückkehr zu Allah unmöglich geworden ist.",
            trIntro: "Hata yapan Müslüman Allah'a dönüş yolunun kapandığını düşünmemelidir.",
            dePoints: [
                "Sünde beenden.",
                "Ehrlich bereuen.",
                "Entschlossen sein, nicht bewusst zurückzukehren.",
                "Wenn Rechte anderer verletzt wurden, diese Rechte soweit möglich zurückgeben oder wiedergutmachen."
            ],
            trPoints: [
                "Günahı bırak.",
                "Samimiyetle pişman ol.",
                "Bilinçli olarak tekrar etmemeye karar ver.",
                "Kul hakkı varsa mümkün olduğunca hakkı iade et veya telafi et."
            ],
            deDetail: "Tawbah ist nicht nur ein gesprochener Satz. Sie verbindet Reue mit Veränderung. Gleichzeitig soll Verzweiflung an Allahs Barmherzigkeit vermieden werden. Bei wiederholten Fehlern wird die Tür zur ehrlichen Reue nicht dadurch geschlossen, dass ein Mensch zuvor schon gefallen ist.",
            trDetail: "Tövbe yalnız söylenen bir cümle değildir; pişmanlığı değişimle birleştirir. Aynı zamanda Allah'ın rahmetinden ümit kesilmez. Bir insan daha önce tekrar hata etmiş olsa bile samimi tövbe kapısı kapanmış sayılmaz."
        ),
        .init(
            id: "afterlife",
            icon: "hourglass.bottomhalf.filled",
            deTitle: "Tod & Jenseits",
            trTitle: "Ölüm ve âhiret",
            deIntro: "Der Glaube an Auferstehung, Gericht und das Jenseits gehört zu den Grundlagen des islamischen Glaubens.",
            trIntro: "Diriliş, hesap ve âhirete iman İslâm inancının temel esaslarındandır.",
            dePoints: [
                "Das irdische Leben ist begrenzt und verantwortliches Handeln hat Folgen.",
                "Menschen werden auferweckt und für ihr Handeln zur Rechenschaft gezogen.",
                "Paradies und Hölle gehören zur islamischen Jenseitslehre."
            ],
            trPoints: [
                "Dünya hayatı sınırlıdır ve sorumlu davranışın sonuçları vardır.",
                "İnsanlar diriltilecek ve yaptıklarından hesaba çekilecektir.",
                "Cennet ve cehennem İslâm'ın âhiret inancının parçalarıdır."
            ],
            deDetail: "Jenseitswissen kommt aus Offenbarung. SalahPath soll deshalb keine spekulativen Geschichten über Grab, Engel oder Endzeit als sichere Tatsachen erzählen, wenn sie nicht zuverlässig belegt sind. Details werden nur mit sauberer Quellenlage ergänzt.",
            trDetail: "Âhiret bilgisi vahye dayanır. Bu yüzden SalahPath kabir, melekler veya kıyametle ilgili güvenilir delili olmayan hikâyeleri kesin gerçek gibi anlatmamalıdır. Ayrıntılar ancak sağlam kaynakla eklenir."
        )
    ]

    private var completedCount: Int {
        _ = refresh
        return lessons.filter { IslamLearningStore.isCompleted($0.id) }.count
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 13) {
                islamProgressCard
                islamLessonList
                islamLearningCautionCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Islam lernen", "İslâm'ı öğren"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear { refresh &+= 1 }
    }

    private var islamProgressCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Label(
                settings.t("Islam Schritt für Schritt lernen", "İslâm'ı adım adım öğren"),
                systemImage: "book.pages.fill"
            )
            .font(.title2.bold())
            .foregroundStyle(SalahTheme.deepTeal)

            Text(settings.t(
                "Du musst nicht alles auf einmal verstehen. Beginne oben und arbeite dich Modul für Modul weiter. Gebet, Wudu, Qur'an und Fasten haben zusätzlich eigene ausführliche Bereiche in SalahPath.",
                "Her şeyi bir anda öğrenmek zorunda değilsin. Yukarıdan başla ve modül modül ilerle. Namaz, abdest, Kur'an ve oruç için SalahPath'te ayrıca ayrıntılı bölümler var."
            ))
            .font(.subheadline)
            .fixedSize(horizontal: false, vertical: true)

            ProgressView(value: Double(completedCount), total: Double(lessons.count))
                .tint(SalahTheme.teal)

            Text(settings.t(
                "\(completedCount) von \(lessons.count) Grundlagen markiert",
                "\(lessons.count) temel konudan \(completedCount) tanesi işaretlendi"
            ))
            .font(.caption.bold())
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }

    @ViewBuilder
    private var islamLessonList: some View {
        ForEach(lessons) { lesson in
            NavigationLink {
                IslamLearningLessonView(lesson: lesson)
            } label: {
                islamLessonRow(lesson)
            }
            .buttonStyle(.plain)
        }
    }

    private func islamLessonRow(_ lesson: IslamLearningLesson) -> some View {
        HStack(spacing: 12) {
            Image(systemName: lesson.icon)
                .font(.title3)
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 34, height: 34)
                .background(SalahTheme.softTeal.opacity(0.55), in: Circle())

            VStack(alignment: .leading, spacing: 3) {
                Text(settings.language == .german ? lesson.deTitle : lesson.trTitle)
                    .font(.headline)
                    .foregroundStyle(SalahTheme.ink)
                Text(settings.language == .german ? lesson.deIntro : lesson.trIntro)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            Spacer(minLength: 6)

            Image(systemName: IslamLearningStore.isCompleted(lesson.id) ? "checkmark.circle.fill" : "chevron.right")
                .foregroundStyle(IslamLearningStore.isCompleted(lesson.id) ? .green : SalahTheme.teal)
        }
        .padding(13)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 15, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.36), lineWidth: 1)
        }
    }

    private var islamLearningCautionCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(settings.t("Wichtig", "Önemli"))
                .font(.headline)
            Text(settings.t(
                "Dieser Kurs ist eine strukturierte Einführung. Er ersetzt kein vollständiges jahrelanges Studium. Bei komplexen Fiqh-, Glaubens- oder persönlichen Lebensfragen zeigt SalahPath Unterschiede und Grenzen, statt eine unbelegte Schnellantwort als sicher auszugeben.",
                "Bu kurs düzenli bir başlangıçtır; yıllar süren kapsamlı din eğitiminin yerini tutmaz. Karmaşık fıkıh, akaid veya kişisel meselelerde SalahPath delilsiz hızlı cevabı kesin hüküm gibi sunmak yerine farklılıkları ve sınırları gösterir."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }

}

// MARK: - Prayer position reference

struct PrayerSequenceReferenceView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let sequence: [(pose: String, de: String, tr: String)] = [
        ("intention", "Absicht vor Beginn", "Namaza niyet"),
        ("takbir", "Eröffnungstakbīr", "İftitah tekbiri"),
        ("standing", "Stehen · Qiyām", "Kıyam"),
        ("bowing", "Rukūʿ", "Rükû"),
        ("upright", "Ganz aufrichten", "Tam doğrulma"),
        ("sujud", "Sujud 1", "1. secde"),
        ("sitting", "Zwischen den Sujud", "İki secde arası"),
        ("sujud", "Sujud 2 · Rakʿa fertig", "2. secde · rekât tamam"),
        ("final_sitting", "Letztes Sitzen", "Son oturuş"),
        ("salam_right", "Salām rechts · nur Kopf", "Sağa selâm · yalnız baş"),
        ("salam_left", "Salām links · nur Kopf", "Sola selâm · yalnız baş")
    ]

    private var audiencePrefix: String {
        settings.prayerAudience == .female ? "female_" : "male_"
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 14) {
                HStack(spacing: 9) {
                    Image(systemName: "figure.mind.and.body")
                        .font(.system(size: 18, weight: .semibold))
                        .foregroundStyle(SalahTheme.teal)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(settings.t("Gebetsablauf im Überblick", "Namaz akışı özeti"))
                            .font(.headline)
                            .foregroundStyle(SalahTheme.ink)
                        Text(settings.t(
                            "Darstellung: " + settings.prayerAudience.title(settings.language),
                            "Gösterim: " + settings.prayerAudience.title(settings.language)
                        ))
                        .font(.caption)
                        .foregroundStyle(SalahTheme.mutedInk)
                    }
                }
                .padding(13)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }

                VStack(alignment: .leading, spacing: 8) {
                    Label(
                        settings.t("Wichtig: Das Gebet besteht nicht nur aus 1 Rakʿa", "Önemli: Namaz yalnız 1 rekâttan oluşmaz"),
                        systemImage: "info.circle.fill"
                    )
                    .font(.headline.bold())
                    .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Nach dem zweiten Sujud ist genau EINE Rakʿa abgeschlossen. Je nach Gebet stehst du danach zur nächsten Rakʿa auf oder bleibst zum vorgeschriebenen Sitzen. Das letzte Sitzen und der Salām kommen erst nach der letzten Rakʿa.",
                        "İkinci secdeden sonra tam BİR rekât tamamlanır. Namaza göre bundan sonra sonraki rekâta kalkarsın veya gereken oturuşta kalırsın. Son oturuş ve selâm yalnız son rekâttan sonra gelir."
                    ))
                    .font(.subheadline)
                    .fixedSize(horizontal: false, vertical: true)

                    Text(settings.t(
                        "Rukūʿ und Sujud werden teilweise von der Seite gezeichnet, damit die Haltung erkennbar ist. Du änderst dabei NICHT deine Richtung zur Qibla.",
                        "Rükû ve secde duruşu anlaşılır olsun diye bazı çizimler yandan gösterilir. Bu sırada kıble yönünü DEĞİŞTİRMEZSİN."
                    ))
                    .font(.footnote.bold())
                    .foregroundStyle(SalahTheme.teal)
                }
                .padding(13)
                .background(SalahTheme.softTeal.opacity(0.45), in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.teal.opacity(0.30), lineWidth: 1) }

                LazyVGrid(
                    columns: [
                        GridItem(.flexible(), spacing: 9),
                        GridItem(.flexible(), spacing: 9)
                    ],
                    spacing: 9
                ) {
                    ForEach(Array(sequence.enumerated()), id: \.offset) { index, item in
                        VStack(spacing: 7) {
                            HStack {
                                Text("\(index + 1)")
                                    .font(.caption.bold().monospacedDigit())
                                    .foregroundStyle(SalahTheme.deepTeal)
                                    .frame(width: 24, height: 24)
                                    .background(SalahTheme.gold.opacity(0.22), in: Circle())
                                Spacer()
                            }

                            PrayerPoseArtwork(assetName: audiencePrefix + item.pose)
                                .frame(height: 145)

                            Text(settings.language == .german ? item.de : item.tr)
                                .font(.system(size: 11.5, weight: .bold))
                                .foregroundStyle(SalahTheme.ink)
                        }
                        .padding(9)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
                    }
                }

                Text(settings.t(
                    "Beim Salām dreht sich nur der Kopf: zuerst zur eigenen rechten Schulter, danach zur eigenen linken Schulter. Der Oberkörper bleibt zur Qibla. Die männlichen und weiblichen Haltungen werden in SalahPath getrennt nach der hanafitischen/Diyanet-Lernpraxis dargestellt; andere Rechtsschulen können einzelne Sunnah-Details anders lehren.",
                    "Selâm verirken yalnız baş çevrilir: önce kendi sağ omzuna, sonra kendi sol omzuna. Gövde kıbleye dönük kalır. SalahPath erkek ve kadın duruşlarını Hanefî/Diyanet öğrenme uygulamasına göre ayrı gösterir; diğer mezhepler bazı sünnet ayrıntılarını farklı öğretebilir."
                ))
                .font(.footnote)
                .foregroundStyle(SalahTheme.mutedInk)
                .padding(.horizontal, 2)
            }
            .padding(12)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetspositionen", "Namaz duruşları"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Dhikr

private struct DhikrItem: Identifiable {
    let id = UUID(); let title:String; let arabic:String; let transliteration:String; let de:String; let tr:String; let count:Int?
}

struct DhikrView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var counter = 33
    @State private var section = 0

    private var tabs: [String] {
        [
            settings.t("Morgen", "Sabah"),
            settings.t("Abend", "Akşam"),
            settings.t("Täglich", "Günlük"),
            settings.t("Spezial", "Özel")
        ]
    }

    private var activeDhikr: (arabic: String, latin: String, translation: String) {
        switch section {
        case 1:
            return (
                "سُبْحَانَ اللّٰهِ وَبِحَمْدِهِ",
                "Sübhânallâhi ve bihamdihî",
                settings.t("Gepriesen sei Allah und Ihm gebührt Lob.", "Allah'ı hamdiyle tesbih ederim.")
            )
        case 2:
            return (
                "لَا إِلٰهَ إِلَّا اللّٰهُ",
                "Lâ ilâhe illallâh",
                settings.t("Es gibt keinen Gott außer Allah.", "Allah'tan başka ilah yoktur.")
            )
        case 3:
            return (
                "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ",
                "Allâhümme salli alâ Muhammed",
                settings.t("Allah, segne Muhammad.", "Allah'ım, Muhammed'e salât eyle.")
            )
        default:
            return (
                "أَسْتَغْفِرُ اللّٰهَ",
                "Estağfirullâh",
                settings.t("Ich bitte Allah um Vergebung.", "Allah'tan bağışlanma dilerim.")
            )
        }
    }

    var body: some View {
        ScrollView {
            VStack(spacing: 9) {
                HStack(spacing: 4) {
                    ForEach(Array(tabs.enumerated()), id: \.offset) { index, title in
                        Button {
                            withAnimation(.easeOut(duration: 0.15)) {
                                section = index
                                counter = 33
                            }
                        } label: {
                            Text(title)
                                .font(.system(size: 11.4, weight: .bold))
                                .foregroundStyle(section == index ? .white : SalahTheme.deepTeal)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 7)
                                .background(
                                    section == index ? SalahTheme.teal : Color.clear,
                                    in: RoundedRectangle(cornerRadius: 8, style: .continuous)
                                )
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(3)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 8).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7) }

                VStack(spacing: 14) {
                    Text(activeDhikr.arabic)
                        .font(.system(size: 37, weight: .regular))
                        .foregroundStyle(SalahTheme.ink)
                        .frame(maxWidth: .infinity)

                    Text(activeDhikr.latin)
                        .font(.custom("AvenirNext-DemiBold", size: 15.6))
                        .foregroundStyle(SalahTheme.ink)

                    Text(activeDhikr.translation)
                        .font(.custom("AvenirNext-Medium", size: 12.1))
                        .foregroundStyle(SalahTheme.mutedInk)
                        .multilineTextAlignment(.center)

                    HStack(spacing: 24) {
                        Button {
                            if counter > 0 { counter -= 1 }
                        } label: {
                            Image(systemName: "minus")
                                .font(.system(size: 17, weight: .bold))
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 42, height: 42)
                                .background(SalahTheme.softTeal.opacity(0.46), in: Circle())
                                .overlay { Circle().stroke(SalahTheme.teal.opacity(0.14), lineWidth: 0.7) }
                        }
                        .buttonStyle(.plain)

                        Text("\(counter)")
                            .font(.system(size: 42, weight: .bold, design: .rounded).monospacedDigit())
                            .foregroundStyle(SalahTheme.deepTeal)
                            .contentTransition(.numericText())
                            .frame(minWidth: 88)
                            .contextMenu {
                                Button {
                                    counter = 33
                                } label: {
                                    Label(settings.t("Zurücksetzen", "Sıfırla"), systemImage: "arrow.counterclockwise")
                                }
                            }

                        Button {
                            if counter < Int.max { counter += 1 }
                        } label: {
                            Image(systemName: "plus")
                                .font(.system(size: 17, weight: .bold))
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 42, height: 42)
                                .background(SalahTheme.softTeal.opacity(0.46), in: Circle())
                                .overlay { Circle().stroke(SalahTheme.teal.opacity(0.14), lineWidth: 0.7) }
                        }
                        .buttonStyle(.plain)
                    }

                }
                .padding(.horizontal, 16)
                .padding(.vertical, 18)
                .frame(maxWidth: .infinity)
                .aspectRatio(1.18, contentMode: .fit)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 10).stroke(SalahTheme.gold.opacity(0.44), lineWidth: 0.7) }

                VStack(spacing: 0) {
                    dhikrReferenceRow(
                        icon: "sunrise.fill",
                        title: settings.t("Morgen- & Abend-Adhkar", "Sabah & Akşam Zikirleri"),
                        subtitle: settings.t("Morgen- & Abend-Adhkar", "Sabah ve akşam")
                    ) {
                        MorningEveningAdhkarView()
                    }

                    dhikrReferenceRow(
                        icon: "hands.sparkles.fill",
                        title: settings.t("Tägliche Duas", "Günlük Dualar"),
                        subtitle: settings.t("Tägliche Duas", "Günlük dualar")
                    ) {
                        QuranicDuaLibraryView()
                    }

                    dhikrReferenceRow(
                        icon: "circle.grid.cross.fill",
                        title: settings.t("Tasbih-Zähler", "Tesbih Sayacı"),
                        subtitle: settings.t("Tasbih-Zähler", "Tesbih sayacı")
                    ) {
                        TasbihCounterView()
                    }

                    dhikrReferenceRow(
                        icon: "character.book.closed.fill",
                        title: settings.t("Arabisch, Türkisch, Deutsch", "Arapça, Türkçe, Almanca"),
                        subtitle: settings.t("Dreisprachige Begleitung", "Üç dilde kullanım")
                    ) {
                        SettingsView()
                    }

                    dhikrReferenceRow(
                        icon: "text.book.closed.fill",
                        title: settings.t("Gebetsduas", "Namaz duaları"),
                        subtitle: settings.t("Offizielle Lernquellen", "Resmî öğrenme kaynakları")
                    ) {
                        PrayerDuaAudioView()
                    }
                }
                .frame(minHeight: 235)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 10).stroke(SalahTheme.gold.opacity(0.36), lineWidth: 0.7) }


            }
            .padding(.horizontal, 11)
            .padding(.vertical, 9)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Dua & Dhikr", "Dua & Zikir"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }

    private func dhikrReferenceRow<Destination: View>(
        icon: String,
        title: String,
        subtitle: String,
        @ViewBuilder destination: () -> Destination
    ) -> some View {
        NavigationLink(destination: destination()) {
            dhikrRowBody(icon: icon, title: title, subtitle: subtitle)
        }
        .buttonStyle(.plain)
    }

    private func dhikrStaticRow(icon: String, title: String, subtitle: String) -> some View {
        dhikrRowBody(icon: icon, title: title, subtitle: subtitle)
    }

    private func dhikrRowBody(icon: String, title: String, subtitle: String) -> some View {
        HStack(spacing: 8) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 16, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .accessibilityHidden(true)

            Text(title)
                .font(.custom("AvenirNext-DemiBold", size: 13.1))
                .foregroundStyle(SalahTheme.ink)

            Spacer()

            Image(systemName: "chevron.right")
                .font(.system(size: 10.8, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 22)
        .contentShape(Rectangle())
        .overlay(alignment: .bottom) {
            Divider()
                .padding(.leading, 31)
                .opacity(0.28)
        }
    }
}


struct TasbihCounterView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var count = 0

    var body: some View {
        VStack(spacing: 24) {
            Spacer()
            Text(settings.t("Tasbih-Zähler", "Tesbih Sayacı"))
                .font(.title2.bold())
                .foregroundStyle(SalahTheme.ink)

            Text("\(count)")
                .font(.system(size: 72, weight: .bold, design: .rounded).monospacedDigit())
                .foregroundStyle(SalahTheme.deepTeal)

            HStack(spacing: 28) {
                Button {
                    if count > 0 { count -= 1 }
                } label: {
                    Image(systemName: "minus")
                        .font(.title2.bold())
                        .frame(width: 58, height: 58)
                        .background(SalahTheme.softTeal, in: Circle())
                }

                Button {
                    if count < Int.max { count += 1 }
                } label: {
                    Image(systemName: "plus")
                        .font(.title2.bold())
                        .frame(width: 58, height: 58)
                        .background(SalahTheme.teal, in: Circle())
                        .foregroundStyle(.white)
                }
            }
            .buttonStyle(.plain)

            Button(settings.t("Zurücksetzen", "Sıfırla")) {
                count = 0
            }
            .buttonStyle(.bordered)

            Spacer()
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Tasbih-Zähler", "Tesbih Sayacı"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }
}

private struct DhikrTextCard: View {
    @EnvironmentObject private var settings: SettingsStore
    let item: DhikrItem
    var body: some View {
        VStack(alignment:.leading,spacing:7) {
            HStack { Text(item.title).font(.headline); Spacer(); if let c=item.count { Text("×\(c)").font(.subheadline.bold()) } }
            Text(item.arabic).font(.title3).frame(maxWidth:.infinity,alignment:.trailing)
            Text(item.transliteration).font(.subheadline.weight(.semibold))
            Text(settings.language == .german ? item.de : item.tr).font(.footnote).foregroundStyle(.secondary)
        }.cardStyle()
    }
}

// MARK: - Quran: Arabic + DE/TR translation + human recitation

private struct SurahListResponse: Decodable { let data: [SurahMeta] }
private struct SurahMeta: Decodable, Identifiable {
    let number:Int; let name:String; let englishName:String; let englishNameTranslation:String; let numberOfAyahs:Int; let revelationType:String
    var id:Int { number }
}
private struct SurahResponse: Decodable { let data: SurahData }
private struct SurahData: Decodable { let number:Int; let name:String; let englishName:String; let ayahs:[AyahData] }
private struct AyahData: Decodable, Identifiable {
    let number:Int
    let numberInSurah:Int
    let text:String
    let audio:String?
    var id:Int { number }
}

actor QuranTextCache {
    static let shared = QuranTextCache()

    private let fileManager = FileManager.default
    private let maxBytes: Int64 = 48 * 1024 * 1024

    private var directoryURL: URL {
        let base = fileManager.urls(for: .applicationSupportDirectory, in: .userDomainMask).first
            ?? fileManager.temporaryDirectory
        return base.appendingPathComponent("SalahPathQuranTextCache", isDirectory: true)
    }

    func data(for key: String) -> Data? {
        do {
            try ensureDirectory()
            let url = fileURL(for: key)
            guard fileManager.fileExists(atPath: url.path) else { return nil }

            let attributes = try fileManager.attributesOfItem(atPath: url.path)
            let size = (attributes[.size] as? NSNumber)?.int64Value ?? 0
            guard size > 0,
                  size <= Int64(QuranNetworkLimits.maxJSONBytes) else {
                try? fileManager.removeItem(at: url)
                return nil
            }

            let data = try Data(contentsOf: url, options: [.mappedIfSafe])
            guard !data.isEmpty,
                  data.count <= QuranNetworkLimits.maxJSONBytes else {
                try? fileManager.removeItem(at: url)
                return nil
            }
            touch(url)
            return data
        } catch {
            return nil
        }
    }

    func store(_ data: Data, for key: String) {
        guard !data.isEmpty,
              data.count <= QuranNetworkLimits.maxJSONBytes else { return }

        do {
            try ensureDirectory()
            let url = fileURL(for: key)
            try data.write(to: url, options: [.atomic])
            touch(url)
            trimIfNeeded()
        } catch {
            // Quran networking must remain usable even if local caching fails.
        }
    }

    func stats() -> (count: Int, bytes: Int64) {
        guard let files = try? fileManager.contentsOfDirectory(
            at: directoryURL,
            includingPropertiesForKeys: [.isRegularFileKey, .fileSizeKey],
            options: [.skipsHiddenFiles]
        ) else {
            return (0, 0)
        }

        var count = 0
        var total: Int64 = 0

        for url in files {
            guard let values = try? url.resourceValues(forKeys: [.isRegularFileKey, .fileSizeKey]),
                  values.isRegularFile == true else { continue }

            if count < Int.max { count += 1 }
            let bytes = max(Int64(values.fileSize ?? 0), 0)
            let (nextTotal, overflow) = total.addingReportingOverflow(bytes)
            total = overflow ? Int64.max : nextTotal
        }

        return (count, total)
    }

    func clear() {
        guard fileManager.fileExists(atPath: directoryURL.path) else { return }
        try? fileManager.removeItem(at: directoryURL)
    }

    func remove(for key: String) {
        let url = fileURL(for: key)
        guard fileManager.fileExists(atPath: url.path) else { return }
        try? fileManager.removeItem(at: url)
    }

    private func ensureDirectory() throws {
        if !fileManager.fileExists(atPath: directoryURL.path) {
            try fileManager.createDirectory(at: directoryURL, withIntermediateDirectories: true)
        }

        var values = URLResourceValues()
        values.isExcludedFromBackup = true
        var url = directoryURL
        try? url.setResourceValues(values)
    }

    private func fileURL(for key: String) -> URL {
        let safe = key.map { character -> Character in
            if character.isLetter || character.isNumber || character == "." || character == "-" || character == "_" {
                return character
            }
            return "_"
        }
        return directoryURL.appendingPathComponent(String(safe), isDirectory: false)
    }

    private func touch(_ url: URL) {
        try? fileManager.setAttributes([.modificationDate: Date()], ofItemAtPath: url.path)
    }

    private func trimIfNeeded() {
        guard let files = try? fileManager.contentsOfDirectory(
            at: directoryURL,
            includingPropertiesForKeys: [.isRegularFileKey, .fileSizeKey, .contentModificationDateKey],
            options: [.skipsHiddenFiles]
        ) else { return }

        var entries: [(url: URL, bytes: Int64, date: Date)] = []
        var total: Int64 = 0

        for url in files {
            guard let values = try? url.resourceValues(
                forKeys: [.isRegularFileKey, .fileSizeKey, .contentModificationDateKey]
            ),
            values.isRegularFile == true else { continue }

            let bytes = max(Int64(values.fileSize ?? 0), 0)
            let (nextTotal, overflow) = total.addingReportingOverflow(bytes)
            total = overflow ? Int64.max : nextTotal
            entries.append((url, bytes, values.contentModificationDate ?? .distantPast))
        }

        guard total > maxBytes else { return }

        for entry in entries.sorted(by: { $0.date < $1.date }) {
            try? fileManager.removeItem(at: entry.url)
            total -= entry.bytes
            if total <= maxBytes { break }
        }
    }
}

@MainActor
private final class QuranStore: ObservableObject {
    private static var bundledUthmani: QuranFullData?

    @Published var chapters:[SurahMeta] = []
    @Published var isLoading = false
    @Published var error:String?

    func loadChapters() async {
        guard chapters.isEmpty, !isLoading else { return }
        error = nil
        isLoading = true
        defer { isLoading = false }

        if let bundled = try? bundledChapters(),
           !bundled.isEmpty {
            chapters = bundled
            return
        }

        let cacheKey = "chapters-v1.json"

        if let cached = await QuranTextCache.shared.data(for: cacheKey) {
            if let decoded = try? JSONDecoder().decode(SurahListResponse.self, from: cached) {
                let sanitized = sanitizedChapters(decoded.data)
                if !sanitized.isEmpty {
                    chapters = sanitized
                    return
                }
            }
            await QuranTextCache.shared.remove(for: cacheKey)
        }

        do {
            guard let url = URL(string: "https://api.alquran.cloud/v1/surah") else {
                throw URLError(.badURL)
            }
            var request = URLRequest(url: url)
            request.timeoutInterval = 20
            let (data, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse,
                  (200...299).contains(http.statusCode) else {
                throw URLError(.badServerResponse)
            }
            guard data.count <= QuranNetworkLimits.maxJSONBytes else {
                throw URLError(.dataLengthExceedsMaximum)
            }

            let decoded = try JSONDecoder().decode(SurahListResponse.self, from: data)
            let sanitized = sanitizedChapters(decoded.data)
            guard !sanitized.isEmpty else {
                throw URLError(.cannotParseResponse)
            }

            chapters = sanitized
            await QuranTextCache.shared.store(data, for: cacheKey)
            error = nil
        } catch {
            self.error = error.localizedDescription
        }
    }

    private func bundledCorpus() throws -> QuranFullData {
        if let cached = Self.bundledUthmani {
            return cached
        }

        guard let url = Bundle.main.url(forResource: "quran-uthmani", withExtension: "json") else {
            throw URLError(.fileDoesNotExist)
        }
        let data = try Data(contentsOf: url, options: [.mappedIfSafe])
        guard data.count <= 4 * 1024 * 1024 else {
            throw URLError(.dataLengthExceedsMaximum)
        }

        let decoded = try JSONDecoder().decode(QuranFullResponse.self, from: data)
        guard decoded.data.surahs.count == 114 else {
            throw URLError(.cannotParseResponse)
        }
        Self.bundledUthmani = decoded.data
        return decoded.data
    }

    private func bundledChapters() throws -> [SurahMeta] {
        let full = try bundledCorpus()
        let chapters = full.surahs.map { surah in
            SurahMeta(
                number: surah.number,
                name: surah.name,
                englishName: surah.englishName,
                englishNameTranslation: surah.englishNameTranslation ?? surah.englishName,
                numberOfAyahs: surah.ayahs.count,
                revelationType: surah.revelationType ?? ""
            )
        }
        return sanitizedChapters(chapters)
    }

    private func bundledSurah(_ number: Int) throws -> SurahData {
        let full = try bundledCorpus()
        guard let surah = full.surahs.first(where: { $0.number == number }) else {
            throw URLError(.cannotParseResponse)
        }

        let ayahs = surah.ayahs.map {
            AyahData(
                number: $0.number,
                numberInSurah: $0.numberInSurah,
                text: $0.text,
                audio: nil
            )
        }
        return SurahData(
            number: surah.number,
            name: surah.name,
            englishName: surah.englishName,
            ayahs: ayahs
        )
    }

    private func sanitizedChapters(_ values: [SurahMeta]) -> [SurahMeta] {
        var seen = Set<Int>()
        var sanitized: [SurahMeta] = []

        for chapter in values {
            guard (1...114).contains(chapter.number),
                  chapter.numberOfAyahs > 0,
                  !chapter.name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  !chapter.englishName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  seen.insert(chapter.number).inserted else {
                continue
            }
            sanitized.append(chapter)
        }

        guard sanitized.count == 114 else { return [] }
        return sanitized.sorted { $0.number < $1.number }
    }

    func loadSurah(_ number:Int, language:AppLanguage) async throws -> (SurahData,SurahData,SurahData) {
        let translationEdition = language == .german ? "de.bubenheim" : "tr.diyanet"
        async let arabic = fetch(number:number, edition:"quran-uthmani")
        async let translated = fetch(number:number, edition:translationEdition)
        async let transliterated = fetch(number:number, edition:"en.transliteration")
        return try await (arabic, translated, transliterated)
    }

    struct SurahReferenceBundle {
        let arabic: SurahData
        let turkish: SurahData?
        let german: SurahData?
        let transliterated: SurahData?
    }

    func loadArabicSurah(_ number: Int) async throws -> SurahData {
        try await fetch(number: number, edition: "quran-uthmani")
    }

    func loadSurahReference(_ number:Int) async throws -> SurahReferenceBundle {
        async let arabic = fetch(number:number, edition:"quran-uthmani")
        async let turkish: SurahData? = try? fetch(number:number, edition:"tr.diyanet")
        async let german: SurahData? = try? fetch(number:number, edition:"de.bubenheim")
        async let transliterated: SurahData? = try? fetch(number:number, edition:"en.transliteration")

        let arabicResult = try await arabic
        let optionalResults = await (turkish, german, transliterated)

        return SurahReferenceBundle(
            arabic: arabicResult,
            turkish: optionalResults.0,
            german: optionalResults.1,
            transliterated: optionalResults.2
        )
    }

    private func fetch(number:Int, edition:String) async throws -> SurahData {
        guard (1...114).contains(number) else {
            throw URLError(.badURL)
        }

        if edition == "quran-uthmani",
           let bundled = try? bundledSurah(number),
           let sanitized = sanitizedSurah(bundled, expectedNumber: number) {
            return sanitized
        }

        let cacheKey = "surah-\(number)-\(edition).json"

        if let cached = await QuranTextCache.shared.data(for: cacheKey) {
            if let decoded = try? JSONDecoder().decode(SurahResponse.self, from: cached),
               let sanitized = sanitizedSurah(decoded.data, expectedNumber: number) {
                return sanitized
            }
            await QuranTextCache.shared.remove(for: cacheKey)
        }

        guard let url = URL(string: "https://api.alquran.cloud/v1/surah/\(number)/\(edition)") else {
            throw URLError(.badURL)
        }

        var request = URLRequest(url: url)
        request.timeoutInterval = 20
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse,
              (200...299).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
        guard data.count <= QuranNetworkLimits.maxJSONBytes else {
            throw URLError(.dataLengthExceedsMaximum)
        }

        let decoded = try JSONDecoder().decode(SurahResponse.self, from: data)
        guard let sanitized = sanitizedSurah(decoded.data, expectedNumber: number) else {
            throw URLError(.cannotParseResponse)
        }

        await QuranTextCache.shared.store(data, for: cacheKey)
        return sanitized
    }

    private func sanitizedSurah(_ value: SurahData, expectedNumber: Int) -> SurahData? {
        guard value.number == expectedNumber,
              (1...114).contains(value.number),
              !value.name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
              !value.englishName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            return nil
        }

        let ayahs = value.ayahs.sorted { $0.numberInSurah < $1.numberInSurah }
        guard !ayahs.isEmpty else { return nil }

        var seenGlobalNumbers = Set<Int>()
        for (index, ayah) in ayahs.enumerated() {
            guard ayah.number > 0,
                  ayah.numberInSurah == index + 1,
                  !ayah.text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  seenGlobalNumbers.insert(ayah.number).inserted else {
                return nil
            }
        }

        return SurahData(
            number: value.number,
            name: value.name,
            englishName: value.englishName,
            ayahs: ayahs
        )
    }
}

struct QuranAudioCacheQAView: View {
    @State private var status = "Prüfe Offline-Audio …"
    @State private var detail = ""
    @State private var passed = false

    var body: some View {
        VStack(spacing: 18) {
            Image(systemName: passed ? "checkmark.seal.fill" : "arrow.down.circle.fill")
                .font(.system(size: 64))
                .foregroundStyle(passed ? .green : SalahTheme.teal)

            Text("Quran Offline-Audio")
                .font(.title2.bold())

            Text(status)
                .font(.headline)
                .multilineTextAlignment(.center)

            Text(detail)
                .font(.footnote.monospaced())
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding(24)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(SalahTheme.page)
        .task { await runTest() }
    }

    private func writeQAResult(_ value: String) {
        let fileManager = FileManager.default
        guard let base = fileManager.urls(for: .applicationSupportDirectory, in: .userDomainMask).first else { return }
        try? fileManager.createDirectory(at: base, withIntermediateDirectories: true)
        let url = base.appendingPathComponent("SalahPathAudioCacheQA.txt")
        try? value.write(to: url, atomically: true, encoding: .utf8)
    }

    @MainActor
    private func runTest() async {
        UserDefaults.standard.set(false, forKey: "audioCacheQAPassed")
        UserDefaults.standard.set(false, forKey: "audioCacheQACompleted")
        UserDefaults.standard.set("running", forKey: "audioCacheQADetail")
        UserDefaults.standard.synchronize()
        writeQAResult("RUNNING")
        await QuranAudioCache.shared.clear()

        do {
            let urls = try await QuranAudioResolver.urls(surah: 1, reciter: .alafasy)
            guard let remote = urls.first else {
                throw URLError(.badServerResponse)
            }

            let firstLocal = await QuranAudioCache.shared.playbackURL(for: remote)
            let firstStats = await QuranAudioCache.shared.stats()
            let secondLocal = await QuranAudioCache.shared.playbackURL(for: remote)
            let secondStats = await QuranAudioCache.shared.stats()

            let sameFile = firstLocal == secondLocal
            let localFile = firstLocal.isFileURL
            let hasBytes = firstStats.count >= 1 && firstStats.bytes > 0
            let reusedWithoutDuplicate = secondStats.count == firstStats.count
                && secondStats.bytes == firstStats.bytes

            passed = sameFile && localFile && hasBytes && reusedWithoutDuplicate
            status = passed ? "PASS · lokal gespeichert und wiederverwendet" : "FAIL · Cache-Prüfung fehlgeschlagen"
            detail = "Dateien: \(secondStats.count) · Bytes: \(secondStats.bytes)\nLokal: \(localFile) · Gleiche Datei: \(sameFile)"
            UserDefaults.standard.set(passed, forKey: "audioCacheQAPassed")
            UserDefaults.standard.set(detail, forKey: "audioCacheQADetail")
            UserDefaults.standard.set(true, forKey: "audioCacheQACompleted")
            UserDefaults.standard.synchronize()
            writeQAResult((passed ? "PASS" : "FAIL") + "\n" + detail)
        } catch {
            passed = false
            status = "FAIL · \(error.localizedDescription)"
            detail = error.localizedDescription
            UserDefaults.standard.set(false, forKey: "audioCacheQAPassed")
            UserDefaults.standard.set(detail, forKey: "audioCacheQADetail")
            UserDefaults.standard.set(true, forKey: "audioCacheQACompleted")
            UserDefaults.standard.synchronize()
            writeQAResult("FAIL\n" + detail)
        }
    }
}

struct QuranProgressQAView: View {
    var body: some View {
        QuranView(initialLastReadSurah: 2, initialLastReadAyah: 142)
    }
}

struct QuranJuzQAView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()

    var body: some View {
        Group {
            if store.isLoading && store.chapters.isEmpty {
                ProgressView(settings.t("Quran wird geladen…", "Kur'an yükleniyor…"))
            } else if let error = store.error, store.chapters.isEmpty {
                ContentUnavailableView(
                    settings.t("Juz konnten nicht geladen werden", "Cüzler yüklenemedi"),
                    systemImage: "wifi.exclamationmark",
                    description: Text(error)
                )
            } else {
                QuranJuzLandingView(chapters: store.chapters)
            }
        }
        .task { await store.loadChapters() }
    }
}

struct QuranReaderQAView: View {
    var body: some View {
        QuranSurahView(
            surah: SurahMeta(
                number: 1,
                name: "سُورَةُ ٱلْفَاتِحَةِ",
                englishName: "Al-Faatiha",
                englishNameTranslation: "The Opening",
                numberOfAyahs: 7,
                revelationType: "Meccan"
            ),
            initialAyah: 1
        )
    }
}

private struct QuranBookmark: Hashable {
    let surah: Int
    let ayah: Int

    var token: String { "\(surah):\(ayah)" }
}

private enum QuranBookmarkStore {
    static let key = "quranBookmarks"
    static let lastReadKey = "quranLastRead"

    static func tokens() -> Set<String> {
        let defaults = UserDefaults.standard
        let stored = defaults.stringArray(forKey: key) ?? []
        let sanitized = Set(stored.compactMap { parse($0)?.token })

        if Set(stored) != sanitized {
            defaults.set(Array(sanitized).sorted(), forKey: key)
        }
        return sanitized
    }

    static func contains(_ bookmark: QuranBookmark) -> Bool {
        guard isValid(bookmark) else { return false }
        return tokens().contains(bookmark.token)
    }

    static func toggle(_ bookmark: QuranBookmark) -> Bool {
        guard isValid(bookmark) else { return false }

        var values = tokens()
        let added: Bool
        if values.contains(bookmark.token) { values.remove(bookmark.token); added = false }
        else { values.insert(bookmark.token); added = true }
        UserDefaults.standard.set(Array(values).sorted(), forKey: key)
        return added
    }

    static func setLastRead(surah: Int, ayah: Int) {
        let bookmark = QuranBookmark(surah: surah, ayah: ayah)
        guard isValid(bookmark) else {
            UserDefaults.standard.removeObject(forKey: lastReadKey)
            return
        }
        UserDefaults.standard.set(bookmark.token, forKey: lastReadKey)
    }

    static func lastRead() -> QuranBookmark? {
        let defaults = UserDefaults.standard
        guard let token = defaults.string(forKey: lastReadKey) else { return nil }
        guard let bookmark = parse(token) else {
            defaults.removeObject(forKey: lastReadKey)
            return nil
        }
        return bookmark
    }

    private static func parse(_ token: String) -> QuranBookmark? {
        let parts = token.split(separator: ":", omittingEmptySubsequences: false)
        guard parts.count == 2,
              let surah = Int(parts[0]),
              let ayah = Int(parts[1]) else { return nil }

        let bookmark = QuranBookmark(surah: surah, ayah: ayah)
        return isValid(bookmark) ? bookmark : nil
    }

    private static func isValid(_ bookmark: QuranBookmark) -> Bool {
        (1...114).contains(bookmark.surah) && bookmark.ayah > 0
    }
}

struct QuranView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()
    @ObservedObject private var previewAudio = RemoteAudioPlayer.shared
    @State private var languageTab = 0
    @State private var search = ""
    @State private var previewAudioURLs: [URL] = []
    @State private var isResolvingPreviewAudio = false
    @State private var previewAudioRequestGeneration = 0
    @State private var lastRead: QuranBookmark?
    private let usesInjectedLastRead: Bool

    init(initialLastReadSurah: Int? = nil, initialLastReadAyah: Int? = nil) {
        if let surah = initialLastReadSurah,
           let ayah = initialLastReadAyah,
           (1...114).contains(surah),
           ayah > 0 {
            _lastRead = State(initialValue: QuranBookmark(surah: surah, ayah: ayah))
            usesInjectedLastRead = true
        } else {
            _lastRead = State(initialValue: QuranBookmarkStore.lastRead())
            usesInjectedLastRead = false
        }
    }

    var body: some View {
        Group {
            if store.isLoading && store.chapters.isEmpty {
                ProgressView(settings.t("Quran wird geladen…", "Kur'an yükleniyor…"))
            } else if let error = store.error, store.chapters.isEmpty {
                VStack(spacing: 12) {
                    ContentUnavailableView(
                        settings.t("Quran konnte nicht geladen werden", "Kur'an yüklenemedi"),
                        systemImage: "wifi.exclamationmark",
                        description: Text(error)
                    )

                    Button {
                        Task { await store.loadChapters() }
                    } label: {
                        Label(settings.t("Erneut versuchen", "Tekrar dene"), systemImage: "arrow.clockwise")
                            .font(.headline)
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(SalahTheme.teal)
                }
                .padding()
            } else {
                ScrollView {
                    VStack(spacing: 8) {
                        HStack(spacing: 3) {
                            let quranLanguageTabs = [
                                settings.t("Arabisch", "Arapça"),
                                settings.t("Türkisch", "Türkçe"),
                                settings.t("Deutsch", "Almanca")
                            ]
                            ForEach(Array(quranLanguageTabs.enumerated()), id: \.offset) { index, title in
                                Button {
                                    withAnimation(.easeOut(duration: 0.12)) { languageTab = index }
                                } label: {
                                    Text(title)
                                        .font(.custom("AvenirNext-DemiBold", size: 11.2))
                                        .foregroundStyle(languageTab == index ? SalahTheme.deepTeal : SalahTheme.mutedInk)
                                        .frame(maxWidth: .infinity)
                                        .padding(.vertical, 7)
                                        .background(languageTab == index ? SalahTheme.gold.opacity(0.18) : Color.clear,
                                                    in: RoundedRectangle(cornerRadius: 6, style: .continuous))
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding(3)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 8).stroke(SalahTheme.gold.opacity(0.32), lineWidth: 0.7) }

                        NavigationLink {
                            QuranDirectoryView()
                        } label: {
                            HStack(spacing: 10) {
                                Image(systemName: "books.vertical.fill")
                                    .font(.system(size: 18, weight: .semibold))
                                    .foregroundStyle(SalahTheme.gold)
                                    .frame(width: 42, height: 42)
                                    .background(SalahTheme.navigationTeal, in: Circle())

                                VStack(alignment: .leading, spacing: 2) {
                                    Text(settings.t("Vollständiges Quran-Verzeichnis", "Tam Kur'an Dizini"))
                                        .font(.headline.bold())
                                        .foregroundStyle(SalahTheme.deepTeal)
                                    Text(settings.t(
                                        "114 Suren · Offenbarungsfolge · 604 Seiten · 30 Juz",
                                        "114 sûre · İniş sırası · 604 sayfa · 30 cüz"
                                    ))
                                    .font(.caption)
                                    .foregroundStyle(SalahTheme.mutedInk)
                                }

                                Spacer()
                                Image(systemName: "chevron.right")
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.teal)
                            }
                            .padding(11)
                            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                            .overlay {
                                RoundedRectangle(cornerRadius: 14, style: .continuous)
                                    .stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1)
                            }
                        }
                        .buttonStyle(.plain)

                        if let lastRead,
                           let chapter = store.chapters.first(where: { $0.number == lastRead.surah }),
                           lastRead.ayah <= chapter.numberOfAyahs {
                            NavigationLink {
                                QuranSurahView(surah: chapter, initialAyah: lastRead.ayah)
                            } label: {
                                VStack(alignment: .leading, spacing: 10) {
                                    HStack(spacing: 12) {
                                        Image(systemName: "bookmark.fill")
                                            .font(.system(size: 18, weight: .bold))
                                            .foregroundStyle(SalahTheme.gold)
                                            .frame(width: 42, height: 42)
                                            .background(SalahTheme.navigationTeal, in: Circle())

                                        VStack(alignment: .leading, spacing: 3) {
                                            Text(settings.t("Weiterlesen", "Okumaya devam et"))
                                                .font(.headline.bold())
                                                .foregroundStyle(SalahTheme.deepTeal)
                                            Text("\(chapter.englishName) · \(settings.t("Vers", "Ayet")) \(lastRead.ayah)")
                                                .font(.subheadline)
                                                .foregroundStyle(SalahTheme.ink)
                                            Text(chapter.name)
                                                .font(.system(size: 18, weight: .medium))
                                                .foregroundStyle(SalahTheme.mutedInk)
                                        }

                                        Spacer()
                                        Image(systemName: "chevron.right")
                                            .font(.headline.bold())
                                            .foregroundStyle(SalahTheme.teal)
                                    }

                                    if let progress = readingProgress {
                                        VStack(spacing: 5) {
                                            HStack {
                                                Text(settings.t("Lesefortschritt", "Okuma ilerlemesi"))
                                                    .font(.caption.bold())
                                                    .foregroundStyle(SalahTheme.mutedInk)
                                                Spacer()
                                                Text("\(Int((progress * 100).rounded())) %")
                                                    .font(.caption.bold().monospacedDigit())
                                                    .foregroundStyle(SalahTheme.deepTeal)
                                            }

                                            ProgressView(value: progress)
                                                .tint(SalahTheme.teal)
                                        }
                                    }
                                }
                                .padding(12)
                                .background(
                                    LinearGradient(
                                        colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.72)],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    ),
                                    in: RoundedRectangle(cornerRadius: 15, style: .continuous)
                                )
                                .overlay {
                                    RoundedRectangle(cornerRadius: 15, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.46), lineWidth: 1)
                                }
                            }
                            .buttonStyle(.plain)
                            .accessibilityLabel(settings.t(
                                "Quran weiterlesen bei \(chapter.englishName), Vers \(lastRead.ayah)",
                                "Kur'an okumaya \(chapter.englishName), \(lastRead.ayah). ayetten devam et"
                            ))
                        }

                        VStack(spacing: 0) {
                            VStack(alignment: .leading, spacing: 14) {
                                Text("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ")
                                    .font(.system(size: 29, weight: .regular))
                                    .frame(maxWidth: .infinity, alignment: .trailing)
                                    .foregroundStyle(SalahTheme.ink)

                                Text("1. Bismillâhirrahmânirrahîm")
                                    .font(.custom("AvenirNext-DemiBold", size: 14.2))
                                    .foregroundStyle(SalahTheme.ink)

                                if languageTab == 1 {
                                    Text("Rahmân ve Rahîm olan Allah'ın adıyla.")
                                        .font(.custom("AvenirNext-Medium", size: 13.2))
                                        .foregroundStyle(SalahTheme.ink)
                                        .fixedSize(horizontal: false, vertical: true)
                                }

                                if languageTab == 2 {
                                    Text("Im Namen Allahs, des Allerbarmers, des Barmherzigen.")
                                        .font(.custom("AvenirNext-Medium", size: 13.2))
                                        .foregroundStyle(SalahTheme.ink)
                                        .fixedSize(horizontal: false, vertical: true)
                                }

                                Spacer(minLength: 18)

                                VStack(spacing: 7) {
                                    HStack {
                                        Text(audioTimeString(previewAudio.currentTime))
                                        Spacer()
                                        Text(audioTimeString(previewAudio.duration))
                                    }
                                    .font(.system(size: 10.5, weight: .semibold).monospacedDigit())
                                    .foregroundStyle(SalahTheme.mutedInk)

                                    ProgressView(
                                        value: min(previewAudio.currentTime, max(previewAudio.duration, 1)),
                                        total: max(previewAudio.duration, 1)
                                    )
                                    .tint(SalahTheme.teal)
                                }

                                HStack(spacing: 24) {
                                    Button { previewAudio.previous() } label: {
                                        Image(systemName: "backward.end.fill")
                                            .font(.system(size: 17, weight: .semibold))
                                    }
                                    .buttonStyle(.plain)
                                    .disabled(!previewAudio.hasPrevious)

                                    Button {
                                        Task { await togglePreviewAudio() }
                                    } label: {
                                        ZStack {
                                            Circle()
                                                .fill(SalahTheme.navigationTeal)
                                                .frame(width: 54, height: 54)
                                            if isResolvingPreviewAudio || previewAudio.isLoading {
                                                ProgressView()
                                                    .tint(.white)
                                            } else {
                                                Image(systemName: previewAudio.isPlaying ? "pause.fill" : "play.fill")
                                                    .font(.system(size: 18, weight: .semibold))
                                                    .foregroundStyle(.white)
                                            }
                                        }
                                    }
                                    .buttonStyle(.plain)
                                    .disabled(isResolvingPreviewAudio || previewAudio.isLoading)

                                    Button { previewAudio.next() } label: {
                                        Image(systemName: "forward.end.fill")
                                            .font(.system(size: 17, weight: .semibold))
                                    }
                                    .buttonStyle(.plain)
                                    .disabled(!previewAudio.hasNext)

                                    Spacer()

                                    AudioSpeedControl(audio: previewAudio)
                                }
                                .foregroundStyle(SalahTheme.teal)
                            }
                            .padding(.horizontal, 15)
                            .padding(.top, 17)
                            .padding(.bottom, 8)
                            .frame(maxWidth: .infinity)

                            Divider()
                                .opacity(0.25)
                                .padding(.horizontal, 8)

                            HStack(spacing: 0) {
                                if let first = store.chapters.first {
                                    NavigationLink {
                                        QuranSurahView(surah: first, initialAyah: 1)
                                    } label: {
                                        quranAction(icon: "square.and.pencil", title: settings.t("Verse", "Ayetler"))
                                    }
                                    .buttonStyle(.plain)
                                } else {
                                    quranAction(icon: "square.and.pencil", title: settings.t("Verse", "Ayetler"))
                                }

                                Button {
                                    Task { await togglePreviewAudio() }
                                } label: {
                                    quranAction(
                                        icon: previewAudio.isPlaying ? "pause.circle" : "play.circle",
                                        title: settings.t("Hören", "Dinle")
                                    )
                                }
                                .buttonStyle(.plain)

                                NavigationLink {
                                    QuranFavoritesView(chapters: store.chapters)
                                } label: {
                                    quranAction(icon: "heart", title: settings.t("Favorit", "Favori"))
                                }
                                .buttonStyle(.plain)

                                NavigationLink {
                                    QuranJuzLandingView(chapters: store.chapters)
                                } label: {
                                    quranAction(icon: "text.book.closed", title: settings.t("Juz", "Cüz"))
                                }
                                .buttonStyle(.plain)
                            }
                            .padding(.horizontal, 5)
                            .padding(.top, 3)
                            .padding(.bottom, 6)
                        }
                        .frame(maxWidth: .infinity)
                        .background(
                            SalahTheme.cream,
                            in: RoundedRectangle(cornerRadius: 10, style: .continuous)
                        )
                        .overlay {
                            RoundedRectangle(cornerRadius: 10, style: .continuous)
                                .stroke(SalahTheme.gold.opacity(0.40), lineWidth: 0.7)
                        }

                        HStack(spacing: 8) {
                            Image(systemName: "magnifyingglass")
                                .foregroundStyle(SalahTheme.teal)
                            TextField(settings.t("Sura suchen", "Sure ara"), text: $search)
                                .textInputAutocapitalization(.never)
                                .autocorrectionDisabled()
                        }
                        .padding(.horizontal, 12)
                        .frame(height: 42)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13, style: .continuous))

                        if filtered.isEmpty {
                            VStack(spacing: 10) {
                                ContentUnavailableView(
                                    settings.t("Keine Sura gefunden", "Sûre bulunamadı"),
                                    systemImage: "magnifyingglass",
                                    description: Text(settings.t(
                                        "Prüfe den Suchbegriff oder lösche die Suche.",
                                        "Arama ifadesini kontrol et veya aramayı temizle."
                                    ))
                                )

                                if !search.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                                    Button {
                                        search = ""
                                    } label: {
                                        Label(settings.t("Suche löschen", "Aramayı temizle"), systemImage: "xmark.circle")
                                    }
                                    .buttonStyle(.bordered)
                                    .tint(SalahTheme.teal)
                                }
                            }
                            .padding(.vertical, 8)
                        } else {
                            ForEach(filtered.prefix(8)) { surah in
                                NavigationLink {
                                    QuranSurahView(surah: surah, initialAyah: nil)
                                } label: {
                                HStack(spacing: 10) {
                                    Text("\(surah.number)")
                                        .font(.caption.bold())
                                        .foregroundStyle(SalahTheme.deepTeal)
                                        .frame(width: 32, height: 32)
                                        .background(SalahTheme.gold.opacity(0.20), in: Circle())
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(surah.englishName)
                                            .font(.system(size: 13, weight: .bold))
                                            .foregroundStyle(SalahTheme.ink)
                                        Text("\(surah.numberOfAyahs) \(settings.t("Verse", "ayet"))")
                                            .font(.caption2)
                                            .foregroundStyle(SalahTheme.mutedInk)
                                    }
                                    Spacer()
                                    Text(surah.name)
                                        .font(.system(size: 19, weight: .medium))
                                        .foregroundStyle(SalahTheme.ink)
                                    Image(systemName: "chevron.right")
                                        .font(.caption.bold())
                                        .foregroundStyle(SalahTheme.teal)
                                }
                                .padding(10)
                                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                                .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.teal.opacity(0.14), lineWidth: 1) }
                            }
                                .buttonStyle(.plain)
                            }
                        }
                    }
                    .padding(.horizontal, 11)
                    .padding(.vertical, 10)
                }
                .scrollIndicators(.hidden)
            }
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Quran", "Kur'an"))
        .navigationBarTitleDisplayMode(.inline)
        .task { await store.loadChapters() }
        .onAppear {
            if !usesInjectedLastRead {
                lastRead = QuranBookmarkStore.lastRead()
            }
            languageTab = settings.language == .german ? 2 : 1
        }
        .onChange(of: settings.quranReciter) { _, _ in
            previewAudioRequestGeneration &+= 1
            isResolvingPreviewAudio = false
            previewAudioURLs.removeAll()
            previewAudio.stop()
        }
        .onDisappear {
            previewAudioRequestGeneration &+= 1
            isResolvingPreviewAudio = false
        }
        .tint(SalahTheme.teal)
    }

    private var quranShareText: String {
        "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ\nBismillâhirrahmânirrahîm"
    }

    private func audioTimeString(_ seconds: Double) -> String {
        guard seconds.isFinite, seconds > 0 else { return "0:00" }
        let total = Int(seconds.rounded(.down))
        return String(format: "%d:%02d", total / 60, total % 60)
    }

    private var readingProgress: Double? {
        guard let lastRead, !store.chapters.isEmpty else { return nil }

        var totalAyahs = 0
        var ayahsBeforeSurah = 0

        for chapter in store.chapters {
            guard chapter.numberOfAyahs >= 0 else { return nil }

            let (nextTotal, totalOverflow) = totalAyahs.addingReportingOverflow(chapter.numberOfAyahs)
            guard !totalOverflow else { return nil }
            totalAyahs = nextTotal

            if chapter.number < lastRead.surah {
                let (nextBefore, beforeOverflow) = ayahsBeforeSurah.addingReportingOverflow(chapter.numberOfAyahs)
                guard !beforeOverflow else { return nil }
                ayahsBeforeSurah = nextBefore
            }
        }

        guard totalAyahs > 0 else { return nil }

        let (current, currentOverflow) = ayahsBeforeSurah.addingReportingOverflow(lastRead.ayah)
        guard !currentOverflow else { return 1 }

        return min(max(Double(current) / Double(totalAyahs), 0), 1)
    }

    @MainActor
    private func togglePreviewAudio() async {
        if !previewAudioURLs.isEmpty,
           let active = previewAudio.activeURL,
           previewAudioURLs.contains(active) {
            previewAudio.isPlaying ? previewAudio.pause() : previewAudio.resume()
            return
        }

        if !previewAudioURLs.isEmpty {
            previewAudio.playQueue(
                previewAudioURLs,
                title: "Al-Fatiha",
                artist: settings.quranReciter.title,
                context: settings.t("Quran-Vorschau", "Kur'an önizleme")
            )
            return
        }

        previewAudioRequestGeneration &+= 1
        let generation = previewAudioRequestGeneration
        let reciter = settings.quranReciter
        isResolvingPreviewAudio = true

        do {
            let urls = try await QuranAudioResolver.urls(surah: 1, reciter: reciter)
            guard generation == previewAudioRequestGeneration,
                  reciter == settings.quranReciter else { return }

            previewAudioURLs = urls
            previewAudio.playQueue(
                urls,
                title: "Al-Fatiha",
                artist: reciter.title,
                context: settings.t("Quran-Vorschau", "Kur'an önizleme")
            )
        } catch {
            guard generation == previewAudioRequestGeneration else { return }
            previewAudio.lastError = settings.t(
                "Audio konnte nicht geladen werden. Erneut versuchen.",
                "Ses yüklenemedi. Tekrar dene."
            )
        }

        if generation == previewAudioRequestGeneration {
            isResolvingPreviewAudio = false
        }
    }

    private func quranAction(icon: String, title: String) -> some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .font(.system(size: 17, weight: .medium))
                .foregroundStyle(SalahTheme.teal)
            Text(title)
                .font(.custom("AvenirNext-DemiBold", size: 9.2))
                .foregroundStyle(SalahTheme.ink)
                .lineLimit(1)
        }
        .frame(maxWidth: .infinity, minHeight: 58)
        .background(Color.clear)
    }

    private var filtered: [SurahMeta] {
        guard !search.isEmpty else { return store.chapters }
        return store.chapters.filter {
            $0.englishName.localizedCaseInsensitiveContains(search) ||
            $0.englishNameTranslation.localizedCaseInsensitiveContains(search) ||
            $0.name.contains(search) ||
            String($0.number) == search
        }
    }
}


// MARK: - Complete Quran directory (Surah · revelation · page · Juz)

private struct QuranPageResponse: Decodable {
    let data: QuranPageData
}

private struct QuranPageData: Decodable {
    let number: Int
    let ayahs: [QuranPageAyah]
}

private struct QuranFullResponse: Decodable {
    let data: QuranFullData
}

private struct QuranFullData: Decodable {
    let surahs: [QuranFullSurah]
}

private struct QuranFullSurah: Decodable {
    let number: Int
    let name: String
    let englishName: String
    let englishNameTranslation: String?
    let revelationType: String?
    let ayahs: [QuranFullAyah]
}

private struct QuranFullAyah: Decodable {
    let number: Int
    let text: String
    let numberInSurah: Int
    let page: Int
}

private struct QuranPageSurah: Decodable {
    let number: Int
    let name: String
    let englishName: String
}

private struct QuranPageAyah: Decodable, Identifiable {
    let number: Int
    let text: String
    let numberInSurah: Int
    let surah: QuranPageSurah

    var id: Int { number }
}

@MainActor
private final class QuranPageStore: ObservableObject {
    @Published var arabic: QuranPageData?
    @Published var translation: QuranPageData?
    @Published var transliteration: QuranPageData?
    @Published var translationUnavailable = false
    @Published var transliterationUnavailable = false
    @Published var isLoading = false
    @Published var error: String?
    private var loadRevision = 0
    private static var bundledUthmani: QuranFullData?

    func load(
        page: Int,
        language: AppLanguage,
        includeTranslation: Bool,
        includeTransliteration: Bool
    ) async {
        loadRevision &+= 1
        let revision = loadRevision
        guard (1...604).contains(page) else {
            if revision == loadRevision {
                error = "Invalid Mushaf page."
                isLoading = false
            }
            return
        }

        isLoading = true
        error = nil
        arabic = nil
        translation = nil
        transliteration = nil
        translationUnavailable = false
        transliterationUnavailable = false
        defer {
            if revision == loadRevision {
                isLoading = false
            }
        }

        let translationEdition = language == .german ? "de.bubenheim" : "tr.diyanet"

        do {
            let arabicResult = try await fetch(page: page, edition: "quran-uthmani")
            guard revision == loadRevision else { return }

            // Arabic is bundled locally. Publish it immediately so a slow or offline
            // translation request can never leave the Mushaf page visually empty.
            arabic = arabicResult
            error = nil

            async let translatedPage: QuranPageData? = includeTranslation
                ? (try? fetch(page: page, edition: translationEdition))
                : nil
            async let transliteratedPage: QuranPageData? = includeTransliteration
                ? (try? fetch(page: page, edition: "en.transliteration"))
                : nil

            let translatedResult = await translatedPage
            let transliteratedResult = await transliteratedPage

            guard revision == loadRevision else { return }
            translation = translatedResult
            transliteration = transliteratedResult
            translationUnavailable = includeTranslation && translatedResult == nil
            transliterationUnavailable = includeTransliteration && transliteratedResult == nil
        } catch {
            guard revision == loadRevision else { return }
            arabic = nil
            translation = nil
            transliteration = nil
            translationUnavailable = false
            transliterationUnavailable = false
            self.error = error.localizedDescription
        }
    }

    private func fetch(page: Int, edition: String) async throws -> QuranPageData {
        guard (1...604).contains(page) else {
            throw URLError(.badURL)
        }

        if edition == "quran-uthmani",
           let bundled = try? bundledPage(page: page),
           let sanitized = sanitizedPage(bundled, expectedPage: page) {
            return sanitized
        }

        let cacheKey = "page-\(page)-\(edition).json"

        if let cached = await QuranTextCache.shared.data(for: cacheKey) {
            if let decoded = try? JSONDecoder().decode(QuranPageResponse.self, from: cached),
               let sanitized = sanitizedPage(decoded.data, expectedPage: page) {
                return sanitized
            }
            await QuranTextCache.shared.remove(for: cacheKey)
        }

        do {
            guard let url = URL(string: "https://api.alquran.cloud/v1/page/\(page)/\(edition)") else {
                throw URLError(.badURL)
            }

            var request = URLRequest(url: url)
            request.timeoutInterval = 20

            let (data, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse,
                  (200...299).contains(http.statusCode) else {
                throw URLError(.badServerResponse)
            }
            guard data.count <= QuranNetworkLimits.maxJSONBytes else {
                throw URLError(.dataLengthExceedsMaximum)
            }

            let decoded = try JSONDecoder().decode(QuranPageResponse.self, from: data)
            guard let sanitized = sanitizedPage(decoded.data, expectedPage: page) else {
                throw URLError(.cannotParseResponse)
            }

            await QuranTextCache.shared.store(data, for: cacheKey)
            return sanitized
        } catch {
            let fallback = try await fetchPageFromFullQuran(page: page, edition: edition)
            guard let sanitized = sanitizedPage(fallback, expectedPage: page) else {
                throw error
            }
            return sanitized
        }
    }

    private func bundledPage(page: Int) throws -> QuranPageData {
        let full: QuranFullData
        if let cached = Self.bundledUthmani {
            full = cached
        } else {
            guard let url = Bundle.main.url(forResource: "quran-uthmani", withExtension: "json") else {
                throw URLError(.fileDoesNotExist)
            }
            let data = try Data(contentsOf: url, options: [.mappedIfSafe])
            guard data.count <= 4 * 1024 * 1024 else {
                throw URLError(.dataLengthExceedsMaximum)
            }
            let decoded = try JSONDecoder().decode(QuranFullResponse.self, from: data)
            guard decoded.data.surahs.count == 114 else {
                throw URLError(.cannotParseResponse)
            }
            Self.bundledUthmani = decoded.data
            full = decoded.data
        }

        var pageAyahs: [QuranPageAyah] = []
        for surah in full.surahs {
            guard (1...114).contains(surah.number),
                  !surah.name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  !surah.englishName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
                continue
            }
            let pageSurah = QuranPageSurah(
                number: surah.number,
                name: surah.name,
                englishName: surah.englishName
            )
            for ayah in surah.ayahs where ayah.page == page {
                pageAyahs.append(
                    QuranPageAyah(
                        number: ayah.number,
                        text: ayah.text,
                        numberInSurah: ayah.numberInSurah,
                        surah: pageSurah
                    )
                )
            }
        }

        pageAyahs.sort { $0.number < $1.number }
        guard !pageAyahs.isEmpty else {
            throw URLError(.cannotParseResponse)
        }
        return QuranPageData(number: page, ayahs: pageAyahs)
    }

    private func fetchPageFromFullQuran(page: Int, edition: String) async throws -> QuranPageData {
        let fullCacheKey = "quran-full-\(edition).json"
        let data: Data

        if let cached = await QuranTextCache.shared.data(for: fullCacheKey) {
            data = cached
        } else {
            guard let url = URL(string: "https://api.alquran.cloud/v1/quran/\(edition)") else {
                throw URLError(.badURL)
            }
            var request = URLRequest(url: url)
            request.timeoutInterval = 30
            let (downloaded, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse,
                  (200...299).contains(http.statusCode) else {
                throw URLError(.badServerResponse)
            }
            // Full Quran text is larger than one page response, but still bounded.
            guard downloaded.count <= 24 * 1024 * 1024 else {
                throw URLError(.dataLengthExceedsMaximum)
            }
            data = downloaded
            await QuranTextCache.shared.store(downloaded, for: fullCacheKey)
        }

        let decoded = try JSONDecoder().decode(QuranFullResponse.self, from: data)
        var pageAyahs: [QuranPageAyah] = []

        for surah in decoded.data.surahs {
            guard (1...114).contains(surah.number),
                  !surah.name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  !surah.englishName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
                continue
            }

            let pageSurah = QuranPageSurah(
                number: surah.number,
                name: surah.name,
                englishName: surah.englishName
            )

            for ayah in surah.ayahs where ayah.page == page {
                pageAyahs.append(
                    QuranPageAyah(
                        number: ayah.number,
                        text: ayah.text,
                        numberInSurah: ayah.numberInSurah,
                        surah: pageSurah
                    )
                )
            }
        }

        pageAyahs.sort { $0.number < $1.number }
        guard !pageAyahs.isEmpty else {
            throw URLError(.cannotParseResponse)
        }
        return QuranPageData(number: page, ayahs: pageAyahs)
    }

    private func sanitizedPage(_ value: QuranPageData, expectedPage: Int) -> QuranPageData? {
        guard value.number == expectedPage,
              (1...604).contains(value.number),
              !value.ayahs.isEmpty else {
            return nil
        }

        var seenAyahs = Set<Int>()
        var previousGlobalNumber: Int?

        for ayah in value.ayahs {
            guard ayah.number > 0,
                  ayah.numberInSurah > 0,
                  (1...114).contains(ayah.surah.number),
                  !ayah.text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  !ayah.surah.name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  !ayah.surah.englishName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  seenAyahs.insert(ayah.number).inserted else {
                return nil
            }

            if let previousGlobalNumber, ayah.number <= previousGlobalNumber {
                return nil
            }
            previousGlobalNumber = ayah.number
        }

        return value
    }
}

struct QuranPageReaderView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranPageStore()
    @ObservedObject private var audio = RemoteAudioPlayer.shared
    @State private var bookmarkedTokens = QuranBookmarkStore.tokens()
    @State private var audioURLsBySurah: [String: [URL]] = [:]
    @State private var resolvingAyahNumber: Int?
    @State private var audioRequestGeneration = 0
    @State private var page: Int

    init(page: Int) {
        _page = State(initialValue: min(max(page, 1), 604))
    }

    private var translationByAyah: [Int: QuranPageAyah] {
        (store.translation?.ayahs ?? []).reduce(into: [:]) { result, ayah in
            result[ayah.number] = ayah
        }
    }

    private var transliterationByAyah: [Int: QuranPageAyah] {
        (store.transliteration?.ayahs ?? []).reduce(into: [:]) { result, ayah in
            result[ayah.number] = ayah
        }
    }

    var body: some View {
        Group {
            if store.isLoading && store.arabic == nil {
                ProgressView(settings.t(
                    "Quran-Seite \(page) wird geladen…",
                    "Kur'an \(page). sayfa yükleniyor…"
                ))
            } else if let error = store.error, store.arabic == nil {
                VStack(spacing: 12) {
                    ContentUnavailableView(
                        settings.t("Seite konnte nicht geladen werden", "Sayfa yüklenemedi"),
                        systemImage: "wifi.exclamationmark",
                        description: Text(error)
                    )

                    Button {
                        Task {
                            await store.load(
                                page: page,
                                language: settings.language,
                                includeTranslation: settings.quranShowTranslation,
                                includeTransliteration: settings.quranShowTransliteration
                            )
                        }
                    } label: {
                        Label(settings.t("Erneut versuchen", "Tekrar dene"), systemImage: "arrow.clockwise")
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(SalahTheme.teal)
                }
                .padding()
            } else if let arabic = store.arabic {
                ScrollView {
                    LazyVStack(spacing: 0) {
                        pageNavigation(top: true)

                        if let audioError = audio.lastError {
                            HStack(alignment: .top, spacing: 8) {
                                Image(systemName: "exclamationmark.triangle.fill")
                                    .foregroundStyle(SalahTheme.gold)
                                Text(audioError)
                                    .font(.caption)
                                    .foregroundStyle(SalahTheme.mutedInk)
                                    .fixedSize(horizontal: false, vertical: true)
                                Spacer(minLength: 0)
                            }
                            .padding(10)
                            .background(SalahTheme.gold.opacity(0.10), in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                            .padding(.horizontal)
                            .padding(.bottom, 8)
                        }

                        if audio.activeURL != nil {
                            HStack(spacing: 9) {
                                Button {
                                    if audio.isPlaying {
                                        audio.pause()
                                    } else {
                                        audio.resume()
                                    }
                                } label: {
                                    Image(systemName: audio.isPlaying ? "pause.fill" : "play.fill")
                                        .font(.system(size: 14, weight: .bold))
                                        .frame(width: 34, height: 34)
                                }
                                .buttonStyle(.borderedProminent)
                                .tint(SalahTheme.teal)
                                .accessibilityLabel(settings.t(
                                    audio.isPlaying ? "Audio pausieren" : "Audio fortsetzen",
                                    audio.isPlaying ? "Sesi duraklat" : "Sesi sürdür"
                                ))

                                VStack(alignment: .leading, spacing: 3) {
                                    ProgressView(
                                        value: audio.currentTime,
                                        total: max(audio.duration, 1)
                                    )
                                    .tint(SalahTheme.teal)

                                    Text("\(audioTimeString(audio.currentTime)) / \(audioTimeString(audio.duration))")
                                        .font(.caption2.monospacedDigit())
                                        .foregroundStyle(SalahTheme.mutedInk)
                                }

                                AudioSpeedControl(audio: audio, compact: true)

                                Button {
                                    audio.stop()
                                } label: {
                                    Image(systemName: "stop.fill")
                                        .font(.system(size: 11, weight: .bold))
                                        .frame(width: 30, height: 30)
                                }
                                .buttonStyle(.bordered)
                                .tint(SalahTheme.teal)
                                .accessibilityLabel(settings.t("Audio stoppen", "Sesi durdur"))
                            }
                            .padding(10)
                            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                            .overlay {
                                RoundedRectangle(cornerRadius: 12, style: .continuous)
                                    .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
                            }
                            .padding(.horizontal)
                            .padding(.bottom, 8)
                        }

                        if settings.quranShowTranslation && store.translationUnavailable {
                            HStack(alignment: .top, spacing: 8) {
                                Image(systemName: "icloud.slash.fill")
                                    .foregroundStyle(SalahTheme.gold)
                                Text(settings.t(
                                    "Arabischer Quran ist verfügbar; die gewählte Übersetzung konnte gerade nicht geladen werden.",
                                    "Arapça Kur'an kullanılabilir; seçili meal şu anda yüklenemedi."
                                ))
                                .font(.caption)
                                .foregroundStyle(SalahTheme.mutedInk)
                                .fixedSize(horizontal: false, vertical: true)
                                Spacer(minLength: 0)
                            }
                            .padding(10)
                            .background(SalahTheme.gold.opacity(0.10), in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                            .padding(.horizontal)
                            .padding(.bottom, 8)
                        }

                        if settings.quranShowTransliteration && store.transliterationUnavailable {
                            HStack(alignment: .top, spacing: 8) {
                                Image(systemName: "icloud.slash.fill")
                                    .foregroundStyle(SalahTheme.gold)
                                Text(settings.t(
                                    "Arabischer Quran ist verfügbar; die Umschrift konnte gerade nicht geladen werden.",
                                    "Arapça Kur'an kullanılabilir; Latin harfli okunuş şu anda yüklenemedi."
                                ))
                                .font(.caption)
                                .foregroundStyle(SalahTheme.mutedInk)
                                .fixedSize(horizontal: false, vertical: true)
                                Spacer(minLength: 0)
                            }
                            .padding(10)
                            .background(SalahTheme.gold.opacity(0.10), in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                            .padding(.horizontal)
                            .padding(.bottom, 8)
                        }

                        VStack(spacing: 0) {
                            ForEach(Array(arabic.ayahs.enumerated()), id: \.offset) { index, ayah in
                                if index == 0 || arabic.ayahs[index - 1].surah.number != ayah.surah.number {
                                    VStack(spacing: 5) {
                                        Text(ayah.surah.name)
                                            .font(.system(size: 25, weight: .semibold))
                                            .foregroundStyle(SalahTheme.deepTeal)
                                        Text("\(ayah.surah.englishName) · \(ayah.surah.number)")
                                            .font(.caption.bold())
                                            .foregroundStyle(SalahTheme.mutedInk)
                                    }
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 12)
                                    .background(SalahTheme.gold.opacity(0.10))
                                }

                                VStack(alignment: .leading, spacing: 9) {
                                    HStack(spacing: 9) {
                                        Text("\(ayah.numberInSurah)")
                                            .font(.caption.bold().monospacedDigit())
                                            .foregroundStyle(SalahTheme.deepTeal)
                                            .frame(width: 30, height: 30)
                                            .background(SalahTheme.gold.opacity(0.20), in: Circle())

                                        Spacer()

                                        let bookmark = QuranBookmark(
                                            surah: ayah.surah.number,
                                            ayah: ayah.numberInSurah
                                        )
                                        let ayahAudioURL = resolvedAudioURL(for: ayah)

                                        Button {
                                            Task { await toggleAudio(for: ayah) }
                                        } label: {
                                            Group {
                                                if resolvingAyahNumber == ayah.number {
                                                    ProgressView()
                                                        .controlSize(.small)
                                                } else {
                                                    Image(systemName:
                                                        ayahAudioURL != nil &&
                                                        audio.activeURL == ayahAudioURL &&
                                                        audio.isPlaying
                                                        ? "pause.circle.fill"
                                                        : "play.circle"
                                                    )
                                                    .font(.system(size: 17, weight: .semibold))
                                                }
                                            }
                                            .foregroundStyle(SalahTheme.teal)
                                            .frame(width: 32, height: 32)
                                        }
                                        .buttonStyle(.plain)
                                        .disabled(resolvingAyahNumber != nil && resolvingAyahNumber != ayah.number)
                                        .accessibilityLabel(settings.t(
                                            ayahAudioURL != nil && audio.activeURL == ayahAudioURL && audio.isPlaying
                                                ? "Vers \(ayah.numberInSurah) pausieren"
                                                : "Vers \(ayah.numberInSurah) abspielen",
                                            ayahAudioURL != nil && audio.activeURL == ayahAudioURL && audio.isPlaying
                                                ? "\(ayah.numberInSurah). ayeti duraklat"
                                                : "\(ayah.numberInSurah). ayeti dinle"
                                        ))

                                        Button {
                                            _ = QuranBookmarkStore.toggle(bookmark)
                                            bookmarkedTokens = QuranBookmarkStore.tokens()
                                        } label: {
                                            Image(systemName: bookmarkedTokens.contains(bookmark.token) ? "bookmark.fill" : "bookmark")
                                                .font(.system(size: 15, weight: .semibold))
                                                .foregroundStyle(SalahTheme.teal)
                                                .frame(width: 32, height: 32)
                                        }
                                        .buttonStyle(.plain)
                                        .accessibilityLabel(
                                            bookmarkedTokens.contains(bookmark.token)
                                                ? settings.t("Lesezeichen entfernen", "Yer imini kaldır")
                                                : settings.t("Lesezeichen setzen", "Yer imi ekle")
                                        )
                                    }

                                    Text(ayah.text)
                                        .font(.system(size: max(settings.safeQuranFontSize, 28)))
                                        .frame(maxWidth: .infinity, alignment: .trailing)
                                        .multilineTextAlignment(.trailing)
                                        .textSelection(.enabled)

                                    if settings.quranShowTransliteration,
                                       let transliterated = transliterationByAyah[ayah.number] {
                                        Divider().opacity(0.18)
                                        Text(transliterated.text)
                                            .font(.subheadline.weight(.medium))
                                            .foregroundStyle(SalahTheme.mutedInk)
                                            .fixedSize(horizontal: false, vertical: true)
                                            .textSelection(.enabled)
                                    }

                                    if settings.quranShowTranslation,
                                       let translated = translationByAyah[ayah.number] {
                                        Divider().opacity(0.24)
                                        Text(translated.text)
                                            .font(.subheadline)
                                            .foregroundStyle(SalahTheme.ink)
                                            .fixedSize(horizontal: false, vertical: true)
                                            .textSelection(.enabled)
                                    }
                                }
                                .padding(.horizontal, 13)
                                .padding(.vertical, 12)
                                .onAppear {
                                    QuranBookmarkStore.setLastRead(
                                        surah: ayah.surah.number,
                                        ayah: ayah.numberInSurah
                                    )
                                }

                                if index < arabic.ayahs.count - 1 {
                                    Divider().opacity(0.28)
                                }
                            }
                        }
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                        .overlay {
                            RoundedRectangle(cornerRadius: 16, style: .continuous)
                                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
                        }
                        .padding(.horizontal)

                        pageNavigation(top: false)

                        Text(settings.t(
                            "Der vollständige arabische Uthmani-Text ist im SalahPath-App-Bundle enthalten und steht für alle 604 Mushaf-Seiten offline bereit. Übersetzung und Transliteration werden bei Bedarf über AlQuran.cloud geladen und lokal gecacht. Schriftgröße, Übersetzungsanzeige, Lesezeichen und Lesefortschritt verwenden dieselben SalahPath-Quran-Einstellungen wie der Suren-Reader.",
                            "Tam Uthmani Arapça metin SalahPath uygulamasına gömülüdür ve 604 Mushaf sayfasının tamamı çevrimdışı okunabilir. Meal ve Latin harfli okunuş gerektiğinde AlQuran.cloud üzerinden yüklenir ve yerel olarak önbelleğe alınır. Yazı boyutu, meal görünümü, yer imleri ve okuma ilerlemesi sûre okuyucusuyla aynı SalahPath Kur'an ayarlarını kullanır."
                        ))
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal)
                        .padding(.bottom, 16)
                    }
                }
                .background(SalahTheme.page)
            } else {
                ProgressView(settings.t(
                    "Quran-Seite \(page) wird geladen…",
                    "Kur'an \(page). sayfa yükleniyor…"
                ))
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(SalahTheme.page)
            }
        }
        .navigationTitle(settings.t("Quran · Seite \(page)", "Kur'an · \(page). Sayfa"))
        .navigationBarTitleDisplayMode(.inline)
        .task(id: "\(page)-\(settings.language.rawValue)-\(settings.quranShowTranslation)-\(settings.quranShowTransliteration)") {
            await store.load(
                page: page,
                language: settings.language,
                includeTranslation: settings.quranShowTranslation,
                includeTransliteration: settings.quranShowTransliteration
            )
        }
        .onChange(of: settings.quranReciter) { _, _ in
            audioRequestGeneration &+= 1
            resolvingAyahNumber = nil
            audioURLsBySurah.removeAll()
            audio.stop()
        }
        .onDisappear {
            audioRequestGeneration &+= 1
            resolvingAyahNumber = nil
        }
    }

    private func audioKey(surah: Int, reciter: QuranReciter) -> String {
        "\(reciter.rawValue)-\(surah)"
    }

    private func resolvedAudioURL(for ayah: QuranPageAyah) -> URL? {
        let key = audioKey(surah: ayah.surah.number, reciter: settings.quranReciter)
        guard let urls = audioURLsBySurah[key] else { return nil }
        return urls[safe: ayah.numberInSurah - 1]
    }

    @MainActor
    private func toggleAudio(for ayah: QuranPageAyah) async {
        let reciter = settings.quranReciter
        let key = audioKey(surah: ayah.surah.number, reciter: reciter)

        if let urls = audioURLsBySurah[key] {
            playFromAyah(ayah, urls: urls, reciter: reciter)
            return
        }

        audioRequestGeneration &+= 1
        let generation = audioRequestGeneration
        resolvingAyahNumber = ayah.number
        audio.lastError = nil

        do {
            let urls = try await QuranAudioResolver.urls(surah: ayah.surah.number, reciter: reciter)
            guard generation == audioRequestGeneration,
                  reciter == settings.quranReciter else { return }

            audioURLsBySurah[key] = urls
            playFromAyah(ayah, urls: urls, reciter: reciter)
        } catch {
            guard generation == audioRequestGeneration else { return }
            audio.lastError = settings.t(
                "Audio konnte nicht geladen werden. Prüfe die Verbindung und versuche es erneut.",
                "Ses yüklenemedi. Bağlantıyı kontrol edip tekrar dene."
            )
        }

        if generation == audioRequestGeneration {
            resolvingAyahNumber = nil
        }
    }

    @MainActor
    private func playFromAyah(_ ayah: QuranPageAyah, urls: [URL], reciter: QuranReciter) {
        let startIndex = ayah.numberInSurah - 1
        guard urls.indices.contains(startIndex) else {
            audio.lastError = settings.t("Audio für diesen Vers ist nicht verfügbar.", "Bu ayet için ses mevcut değil.")
            return
        }

        let selectedURL = urls[startIndex]
        QuranBookmarkStore.setLastRead(surah: ayah.surah.number, ayah: ayah.numberInSurah)

        if audio.activeURL == selectedURL {
            audio.isPlaying ? audio.pause() : audio.resume()
            return
        }

        audio.playQueue(
            Array(urls.dropFirst(startIndex)),
            title: ayah.surah.englishName,
            artist: reciter.title,
            context: settings.t(
                "Quran \(ayah.surah.number):\(ayah.numberInSurah) · automatisch weiter",
                "Kur'an \(ayah.surah.number):\(ayah.numberInSurah) · otomatik devam"
            )
        )
    }

    private func movePage(by offset: Int) {
        let next = page + offset
        guard (1...604).contains(next) else { return }

        audioRequestGeneration &+= 1
        resolvingAyahNumber = nil
        audio.stop()
        page = next
    }

    private func audioTimeString(_ seconds: Double) -> String {
        guard seconds.isFinite, seconds > 0 else { return "0:00" }
        let total = Int(seconds.rounded(.down))
        return String(format: "%d:%02d", total / 60, total % 60)
    }

    @ViewBuilder
    private func pageNavigation(top: Bool) -> some View {
        HStack(spacing: 10) {
            if page > 1 {
                Button {
                    movePage(by: -1)
                } label: {
                    Label(settings.t("Zurück", "Önceki"), systemImage: "chevron.left")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)
            } else {
                Color.clear.frame(maxWidth: .infinity, minHeight: 32)
            }

            Text(settings.t("Seite \(page) / 604", "Sayfa \(page) / 604"))
                .font(.subheadline.bold().monospacedDigit())
                .foregroundStyle(SalahTheme.deepTeal)
                .fixedSize()

            if page < 604 {
                Button {
                    movePage(by: 1)
                } label: {
                    Label(settings.t("Weiter", "Sonraki"), systemImage: "chevron.right")
                        .labelStyle(.titleAndIcon)
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)
            } else {
                Color.clear.frame(maxWidth: .infinity, minHeight: 32)
            }
        }
        .tint(SalahTheme.teal)
        .padding(.horizontal)
        .padding(.vertical, top ? 12 : 14)
    }
}

struct QuranDirectoryView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()
    @State private var tab = 0
    @State private var search = ""
    @State private var pageSearch = ""

    // Diyanet's common nuzul-order list, indexed by Mushaf surah number.
    // 0 is an unused sentinel so array index == surah number.
    private let revelationOrderBySurah: [Int] = [
        0,
        5, 87, 89, 92, 112, 55, 39, 88, 113, 51, 52, 53, 96, 72, 54, 70, 50, 69, 44, 45,
        73, 103, 74, 102, 42, 47, 48, 49, 85, 84, 57, 75, 90, 58, 43, 41, 56, 38, 59, 60,
        61, 62, 63, 64, 65, 66, 95, 111, 106, 34, 67, 76, 23, 37, 97, 46, 94, 105, 101, 91,
        109, 110, 104, 108, 99, 107, 77, 2, 78, 79, 71, 40, 3, 4, 31, 98, 33, 80, 81, 24,
        7, 82, 86, 83, 27, 36, 8, 68, 10, 35, 26, 9, 11, 12, 28, 1, 25, 100, 93, 14,
        30, 16, 13, 32, 19, 29, 17, 15, 18, 114, 6, 22, 20, 21
    ]

    private var filteredChapters: [SurahMeta] {
        let q = search.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !q.isEmpty else { return store.chapters }

        return store.chapters.filter { chapter in
            chapter.name.localizedCaseInsensitiveContains(q) ||
            chapter.englishName.localizedCaseInsensitiveContains(q) ||
            chapter.englishNameTranslation.localizedCaseInsensitiveContains(q) ||
            String(chapter.number) == q
        }
    }

    private var revelationChapters: [SurahMeta] {
        filteredChapters.sorted {
            revelationNumber(for: $0.number) < revelationNumber(for: $1.number)
        }
    }

    var body: some View {
        Group {
            if store.isLoading && store.chapters.isEmpty {
                ProgressView(settings.t("Quran-Verzeichnis wird geladen…", "Kur'an dizini yükleniyor…"))
            } else if let error = store.error, store.chapters.isEmpty {
                VStack(spacing: 12) {
                    ContentUnavailableView(
                        settings.t("Quran-Verzeichnis konnte nicht geladen werden", "Kur'an dizini yüklenemedi"),
                        systemImage: "wifi.exclamationmark",
                        description: Text(error)
                    )

                    Button {
                        Task { await store.loadChapters() }
                    } label: {
                        Label(settings.t("Erneut versuchen", "Tekrar dene"), systemImage: "arrow.clockwise")
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(SalahTheme.teal)
                }
                .padding()
            } else {
                VStack(spacing: 8) {
                    Picker("", selection: $tab) {
                        Text(settings.t("Suren", "Sûreler")).tag(0)
                        Text(settings.t("Offenbarung", "İniş Sırası")).tag(1)
                        Text(settings.t("Seiten", "Sayfa")).tag(2)
                        Text(settings.t("Juz", "Cüz")).tag(3)
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal)
                    .padding(.top, 8)

                    if tab == 0 || tab == 1 {
                        searchField
                    }

                    content
                }
                .background(SalahTheme.page)
            }
        }
        .navigationTitle(settings.t("Quran-Verzeichnis", "Kur'an Dizini"))
        .navigationBarTitleDisplayMode(.inline)
        .task { await store.loadChapters() }
    }

    @ViewBuilder
    private var content: some View {
        switch tab {
        case 0:
            surahList(filteredChapters, showRevelation: false)
        case 1:
            surahList(revelationChapters, showRevelation: true)
        case 2:
            pageGrid
        default:
            juzList
        }
    }

    private var searchField: some View {
        HStack(spacing: 8) {
            Image(systemName: "magnifyingglass")
                .foregroundStyle(SalahTheme.teal)
            TextField(settings.t("Sura suchen", "Sûre ara"), text: $search)
                .textInputAutocapitalization(.never)
                .autocorrectionDisabled()
        }
        .padding(.horizontal, 12)
        .frame(height: 42)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 12, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.35), lineWidth: 1)
        }
        .padding(.horizontal)
    }

    @ViewBuilder
    private func surahList(_ chapters: [SurahMeta], showRevelation: Bool) -> some View {
        if chapters.isEmpty {
            VStack(spacing: 10) {
                ContentUnavailableView(
                    settings.t("Keine Sura gefunden", "Sûre bulunamadı"),
                    systemImage: "magnifyingglass",
                    description: Text(settings.t(
                        "Für diese Suche gibt es keinen Treffer.",
                        "Bu arama için sonuç bulunamadı."
                    ))
                )

                if !search.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                    Button {
                        search = ""
                    } label: {
                        Label(settings.t("Suche löschen", "Aramayı temizle"), systemImage: "xmark.circle")
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(SalahTheme.teal)
                }
            }
            .padding()
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        } else {
            List(chapters) { chapter in
                NavigationLink {
                    QuranSurahView(surah: chapter, initialAyah: nil)
                } label: {
                HStack(spacing: 10) {
                    VStack(spacing: 2) {
                        Text(showRevelation ? "#\(revelationNumber(for: chapter.number))" : "\(chapter.number)")
                            .font(.caption.bold().monospacedDigit())
                            .foregroundStyle(SalahTheme.deepTeal)
                        if showRevelation {
                            Text(settings.t("Nüzul", "Nüzul"))
                                .font(.system(size: 8, weight: .semibold))
                                .foregroundStyle(.secondary)
                        }
                    }
                    .frame(width: 42, height: 42)
                    .background(SalahTheme.gold.opacity(0.18), in: Circle())

                    VStack(alignment: .leading, spacing: 2) {
                        Text(chapter.englishName)
                            .font(.headline)
                            .foregroundStyle(SalahTheme.ink)
                        Text("\(chapter.numberOfAyahs) \(settings.t("Verse", "ayet")) · \(localizedRevelationType(chapter.revelationType))")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }

                    Spacer()

                    Text(chapter.name)
                        .font(.system(size: 18))
                        .foregroundStyle(SalahTheme.ink)
                }
                .padding(.vertical, 2)
                }
            }
            .listStyle(.plain)
            .scrollContentBackground(.hidden)
        }
    }

    private var pageGrid: some View {
        let trimmed = pageSearch.trimmingCharacters(in: .whitespacesAndNewlines)
        let requestedPage = Int(trimmed)
        let pages: [Int] = {
            guard !trimmed.isEmpty else { return Array(1...604) }
            guard let requestedPage, (1...604).contains(requestedPage) else { return [] }
            return [requestedPage]
        }()

        return ScrollView {
            VStack(spacing: 10) {
                HStack(spacing: 8) {
                    Image(systemName: "number")
                        .foregroundStyle(SalahTheme.teal)

                    TextField(settings.t("Seite 1–604", "Sayfa 1–604"), text: $pageSearch)
                        .keyboardType(.numberPad)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                        .accessibilityLabel(settings.t("Quran-Seitennummer", "Kur'an sayfa numarası"))

                    if !pageSearch.isEmpty {
                        Button {
                            pageSearch = ""
                        } label: {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundStyle(SalahTheme.mutedInk)
                        }
                        .buttonStyle(.plain)
                        .accessibilityLabel(settings.t("Seitensuche löschen", "Sayfa aramasını temizle"))
                    }
                }
                .padding(.horizontal, 12)
                .frame(height: 42)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 12, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.35), lineWidth: 1)
                }

                if pages.isEmpty {
                    ContentUnavailableView(
                        settings.t("Ungültige Seitennummer", "Geçersiz sayfa numarası"),
                        systemImage: "number.square",
                        description: Text(settings.t(
                            "Gib eine Zahl zwischen 1 und 604 ein.",
                            "1 ile 604 arasında bir sayı gir."
                        ))
                    )
                    .frame(maxWidth: .infinity, minHeight: 220)
                } else {
                    LazyVGrid(columns: [
                        GridItem(.adaptive(minimum: 64), spacing: 8)
                    ], spacing: 8) {
                        ForEach(pages, id: \.self) { page in
                            NavigationLink {
                                QuranPageReaderView(page: page)
                            } label: {
                                VStack(spacing: 3) {
                                    Text("\(page)")
                                        .font(.headline.bold().monospacedDigit())
                                        .foregroundStyle(SalahTheme.deepTeal)
                                    Text(settings.t("Seite", "Sayfa"))
                                        .font(.caption2)
                                        .foregroundStyle(SalahTheme.mutedInk)
                                }
                                .frame(maxWidth: .infinity, minHeight: 58)
                                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 11, style: .continuous))
                                .overlay {
                                    RoundedRectangle(cornerRadius: 11, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.32), lineWidth: 1)
                                }
                            }
                            .buttonStyle(.plain)
                            .accessibilityLabel(settings.t(
                                "Quran Seite \(page) öffnen",
                                "Kur'an \(page). sayfayı aç"
                            ))
                        }
                    }
                }
            }
            .padding()
        }
    }

    private var juzList: some View {
        List(QuranJuzStart.all) { juz in
            if let chapter = store.chapters.first(where: { $0.number == juz.surah }) {
                NavigationLink {
                    QuranSurahView(surah: chapter, initialAyah: juz.ayah)
                } label: {
                    HStack(spacing: 11) {
                        Text("\(juz.number)")
                            .font(.caption.bold())
                            .foregroundStyle(.white)
                            .frame(width: 36, height: 36)
                            .background(SalahTheme.navigationTeal, in: Circle())

                        VStack(alignment: .leading, spacing: 2) {
                            Text(settings.t("Juz \(juz.number)", "\(juz.number). Cüz"))
                                .font(.headline)
                            Text("\(chapter.englishName) · \(settings.t("Vers", "Ayet")) \(juz.ayah)")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }

                        Spacer()
                        Text(chapter.name)
                            .font(.system(size: 17))
                    }
                    .padding(.vertical, 2)
                }
            }
        }
        .listStyle(.plain)
        .scrollContentBackground(.hidden)
    }

    private func revelationNumber(for surah: Int) -> Int {
        guard revelationOrderBySurah.indices.contains(surah) else { return 999 }
        return revelationOrderBySurah[surah]
    }

    private func localizedRevelationType(_ value: String) -> String {
        switch value.lowercased() {
        case "meccan":
            return settings.t("mekkanisch", "Mekkî")
        case "medinan":
            return settings.t("medinensisch", "Medenî")
        default:
            return value
        }
    }
}

private struct QuranJuzStart: Identifiable {
    let number: Int
    let surah: Int
    let ayah: Int
    var id: Int { number }

    static let all: [QuranJuzStart] = [
        .init(number: 1,  surah: 1,  ayah: 1),
        .init(number: 2,  surah: 2,  ayah: 142),
        .init(number: 3,  surah: 2,  ayah: 253),
        .init(number: 4,  surah: 3,  ayah: 93),
        .init(number: 5,  surah: 4,  ayah: 24),
        .init(number: 6,  surah: 4,  ayah: 148),
        .init(number: 7,  surah: 5,  ayah: 82),
        .init(number: 8,  surah: 6,  ayah: 111),
        .init(number: 9,  surah: 7,  ayah: 88),
        .init(number: 10, surah: 8,  ayah: 41),
        .init(number: 11, surah: 9,  ayah: 93),
        .init(number: 12, surah: 11, ayah: 6),
        .init(number: 13, surah: 12, ayah: 53),
        .init(number: 14, surah: 15, ayah: 1),
        .init(number: 15, surah: 17, ayah: 1),
        .init(number: 16, surah: 18, ayah: 75),
        .init(number: 17, surah: 21, ayah: 1),
        .init(number: 18, surah: 23, ayah: 1),
        .init(number: 19, surah: 25, ayah: 21),
        .init(number: 20, surah: 27, ayah: 56),
        .init(number: 21, surah: 29, ayah: 46),
        .init(number: 22, surah: 33, ayah: 31),
        .init(number: 23, surah: 36, ayah: 28),
        .init(number: 24, surah: 39, ayah: 32),
        .init(number: 25, surah: 41, ayah: 47),
        .init(number: 26, surah: 46, ayah: 1),
        .init(number: 27, surah: 51, ayah: 31),
        .init(number: 28, surah: 58, ayah: 1),
        .init(number: 29, surah: 67, ayah: 1),
        .init(number: 30, surah: 78, ayah: 1)
    ]
}

private struct QuranJuzLandingView: View {
    @EnvironmentObject private var settings: SettingsStore
    let chapters: [SurahMeta]

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("30 Juz des Quran", "Kur'an'ın 30 cüzü"), systemImage: "text.book.closed.fill")
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Tippe auf einen Juz. SalahPath öffnet direkt die Ayah, an der dieser Juz beginnt. Von dort kannst du normal weiterlesen, hören und Lesezeichen setzen.",
                        "Bir cüze dokun. SalahPath doğrudan o cüzün başladığı ayeti açar. Oradan normal şekilde okumaya, dinlemeye ve yer imi eklemeye devam edebilirsin."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                    .fixedSize(horizontal: false, vertical: true)
                }
                .padding(.vertical, 4)
            }

            Section(settings.t("Juz auswählen", "Cüz seç")) {
                ForEach(QuranJuzStart.all) { juz in
                    if let chapter = chapters.first(where: { $0.number == juz.surah }) {
                        NavigationLink {
                            QuranSurahView(surah: chapter, initialAyah: juz.ayah)
                        } label: {
                            HStack(spacing: 11) {
                                Text("\(juz.number)")
                                    .font(.caption.bold())
                                    .foregroundStyle(.white)
                                    .frame(width: 34, height: 34)
                                    .background(SalahTheme.navigationTeal, in: Circle())

                                VStack(alignment: .leading, spacing: 3) {
                                    Text(settings.t("Juz \(juz.number)", "\(juz.number). Cüz"))
                                        .font(.headline)
                                        .foregroundStyle(SalahTheme.ink)

                                    Text("\(chapter.englishName) · \(settings.t("Vers", "Ayet")) \(juz.ayah)")
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }

                                Spacer()

                                Text(chapter.name)
                                    .font(.system(size: 17, weight: .medium))
                                    .foregroundStyle(SalahTheme.mutedInk)
                            }
                            .padding(.vertical, 3)
                        }
                        .accessibilityLabel(settings.t(
                            "Juz \(juz.number), beginnt bei \(chapter.englishName), Vers \(juz.ayah)",
                            "\(juz.number). Cüz, \(chapter.englishName) suresi \(juz.ayah). ayette başlar"
                        ))
                    }
                }
            }

            Section {
                Text(settings.t(
                    "Die Juz-Einteilung ist eine Leseeinteilung des Quran in 30 Teile. Sie verändert weder Suren- noch Ayah-Nummern.",
                    "Cüz sistemi Kur'an'ı okumayı kolaylaştırmak için 30 bölüme ayırır. Sure ve ayet numaralarını değiştirmez."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Juz", "Cüz"))
        .navigationBarTitleDisplayMode(.inline)
    }
}


struct QuranFavoritesLandingView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()

    var body: some View {
        Group {
            if store.isLoading && store.chapters.isEmpty {
                ProgressView(settings.t("Quran wird geladen…", "Kur'an yükleniyor…"))
            } else if let error = store.error, store.chapters.isEmpty {
                VStack(spacing: 12) {
                    ContentUnavailableView(
                        settings.t("Favoriten konnten nicht geladen werden", "Favoriler yüklenemedi"),
                        systemImage: "wifi.exclamationmark",
                        description: Text(error)
                    )

                    Button {
                        Task { await store.loadChapters() }
                    } label: {
                        Label(settings.t("Erneut versuchen", "Tekrar dene"), systemImage: "arrow.clockwise")
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(SalahTheme.teal)
                }
                .padding()
            } else {
                QuranFavoritesView(chapters: store.chapters)
            }
        }
        .task { await store.loadChapters() }
    }
}

private struct QuranFavoritesView: View {
    @EnvironmentObject private var settings: SettingsStore
    let chapters: [SurahMeta]
    @State private var refresh = 0

    var body: some View {
        List {
            if favorites.isEmpty {
                ContentUnavailableView(
                    settings.t("Noch keine Favoriten", "Henüz favori yok"),
                    systemImage: "bookmark",
                    description: Text(settings.t("Tippe bei einer Ayah auf das Lesezeichen.", "Bir ayette yer imi simgesine dokun."))
                )
            } else {
                ForEach(favorites, id: \.token) { favorite in
                    if let surah = chapters.first(where: { $0.number == favorite.surah }) {
                        NavigationLink {
                            QuranSurahView(surah: surah, initialAyah: favorite.ayah)
                        } label: {
                            VStack(alignment: .leading, spacing: 3) {
                                Text(surah.englishName).font(.headline)
                                Text("\(settings.t("Ayah", "Ayet")) \(favorite.ayah)")
                                    .font(.caption).foregroundStyle(.secondary)
                            }
                        }
                        .swipeActions {
                            Button(role: .destructive) {
                                _ = QuranBookmarkStore.toggle(QuranBookmark(surah: favorite.surah, ayah: favorite.ayah))
                                refresh &+= 1
                            } label: { Label(settings.t("Entfernen", "Kaldır"), systemImage: "trash") }
                        }
                    }
                }
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Favoriten", "Favoriler"))
        .navigationBarTitleDisplayMode(.inline)
    }

    private var favorites: [(token: String, surah: Int, ayah: Int)] {
        QuranBookmarkStore.tokens().compactMap { token in
            let parts = token.split(separator: ":")
            guard parts.count == 2, let surah = Int(parts[0]), let ayah = Int(parts[1]) else { return nil }
            return (token, surah, ayah)
        }.sorted { lhs, rhs in lhs.surah == rhs.surah ? lhs.ayah < rhs.ayah : lhs.surah < rhs.surah }
    }
}

private struct QuranSurahView: View {
    @EnvironmentObject private var settings: SettingsStore
    let surah: SurahMeta
    let initialAyah: Int?

    @StateObject private var store = QuranStore()
    @ObservedObject private var audio = RemoteAudioPlayer.shared
    @State private var arabic: SurahData?
    @State private var turkishTranslation: SurahData?
    @State private var germanTranslation: SurahData?
    @State private var transliteration: SurahData?
    @State private var resolvedAudioURLs: [URL] = []
    @State private var isResolvingAudio = false
    @State private var error: String?
    @State private var contentWarning: String?
    @State private var bookmarkedTokens = QuranBookmarkStore.tokens()
    @State private var hasScrolledToInitial = false
    @State private var displayMode = 0
    @State private var didSetInitialDisplayMode = false
    @State private var contentLoadRevision = 0
    @State private var audioLoadRevision = 0

    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(spacing: 10) {
                    headerSection
                    versesSection
                    sourceFooter
                }
                .padding(.horizontal, 11)
                .padding(.vertical, 10)
            }
            .scrollIndicators(.hidden)
            .background(SalahTheme.page)
            .navigationTitle(settings.t("Quran", "Kur'an"))
            .navigationBarTitleDisplayMode(.inline)
            .task(id: settings.quranReciter.rawValue) {
                await loadContent()
                scrollToInitialIfNeeded(proxy)
            }
            .onChange(of: arabic?.ayahs.count ?? 0) { _, _ in scrollToInitialIfNeeded(proxy) }
            .onAppear {
                if !didSetInitialDisplayMode {
                    displayMode = settings.language == .german ? 2 : 1
                    didSetInitialDisplayMode = true
                }
            }
            .onDisappear {
                contentLoadRevision &+= 1
                audioLoadRevision &+= 1
                isResolvingAudio = false
            }
        }
    }

    private var headerSection: some View {
        VStack(spacing: 10) {
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text(surah.englishName)
                        .font(.system(size: 17, weight: .bold, design: .serif))
                        .foregroundStyle(SalahTheme.ink)
                    Text("\(surah.numberOfAyahs) \(settings.t("Verse", "ayet"))")
                        .font(.caption2.weight(.semibold))
                        .foregroundStyle(SalahTheme.mutedInk)
                }
                Spacer()
                Text(surah.name)
                    .font(.system(size: 24, weight: .medium))
                    .foregroundStyle(SalahTheme.ink)
            }

            Picker(settings.t("Ansicht", "Görünüm"), selection: $displayMode) {
                Text(settings.t("Arabisch", "Arapça")).tag(0)
                Text(settings.t("Türkisch", "Türkçe")).tag(1)
                Text(settings.t("Deutsch", "Almanca")).tag(2)
            }
            .pickerStyle(.segmented)

            HStack(spacing: 12) {
                Button { audio.previous() } label: {
                    Image(systemName: "backward.fill")
                        .frame(width: 34, height: 34)
                }
                .disabled(!audio.hasPrevious)

                Button(action: toggleFullSurah) {
                    ZStack {
                        Circle()
                            .fill(audioReady ? SalahTheme.teal : Color.secondary.opacity(0.34))
                            .frame(width: 46, height: 46)
                        if isResolvingAudio || audio.isLoading {
                            ProgressView().tint(.white)
                        } else {
                            Image(systemName: audio.isPlaying ? "pause.fill" : (audioReady ? "play.fill" : "speaker.slash.fill"))
                                .foregroundStyle(.white)
                                .font(.system(size: 16, weight: .bold))
                        }
                    }
                }
                .buttonStyle(.plain)
                .disabled(!audioReady || isResolvingAudio || audio.isLoading)

                Button { audio.next() } label: {
                    Image(systemName: "forward.fill")
                        .frame(width: 34, height: 34)
                }
                .disabled(!audio.hasNext)

                VStack(alignment: .leading, spacing: 4) {
                    ProgressView(
                        value: Double(audio.queueCount > 0 ? audio.queueIndex + 1 : 0),
                        total: Double(max(audio.queueCount, 1))
                    )
                    .tint(SalahTheme.teal)
                    Text(settings.quranReciter.title)
                        .font(.system(size: 8.5, weight: .semibold))
                        .foregroundStyle(SalahTheme.mutedInk)
                        .lineLimit(1)
                }

                AudioSpeedControl(audio: audio, compact: true)
            }
            .foregroundStyle(SalahTheme.teal)

            if let audioError = audio.lastError {
                HStack(spacing: 8) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundStyle(.orange)
                    Text(audioError)
                        .font(.caption2)
                        .foregroundStyle(SalahTheme.mutedInk)
                    Spacer()
                    Button(settings.t("Erneut", "Tekrar")) { Task { await loadAudio() } }
                        .font(.caption2.bold())
                }
            }

            if let contentWarning {
                HStack(alignment: .top, spacing: 8) {
                    Image(systemName: "icloud.slash.fill")
                        .foregroundStyle(SalahTheme.gold)
                    Text(contentWarning)
                        .font(.caption2)
                        .foregroundStyle(SalahTheme.mutedInk)
                        .fixedSize(horizontal: false, vertical: true)
                    Spacer(minLength: 0)
                }
            }
        }
        .padding(11)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.56), lineWidth: 1) }
    }

    @ViewBuilder
    private var versesSection: some View {
        if let arabic {
            ForEach(Array(arabic.ayahs.enumerated()), id: \.offset) { index, ar in
                ayahCard(
                    ar: ar,
                    turkish: turkishTranslation?.ayahs[safe: index],
                    german: germanTranslation?.ayahs[safe: index],
                    transliterated: transliteration?.ayahs[safe: index],
                    index: index
                )
                .id(ar.numberInSurah)
            }
        } else if let error {
            VStack(spacing: 12) {
                ContentUnavailableView(
                    settings.t("Inhalt nicht geladen", "İçerik yüklenemedi"),
                    systemImage: "wifi.exclamationmark",
                    description: Text(error)
                )

                Button {
                    Task { await loadContent() }
                } label: {
                    Label(settings.t("Erneut versuchen", "Tekrar dene"), systemImage: "arrow.clockwise")
                        .font(.headline)
                }
                .buttonStyle(.borderedProminent)
                .tint(SalahTheme.teal)
            }
        } else {
            ProgressView().padding(.top, 40)
        }
    }

    private func ayahCard(ar: AyahData, turkish: AyahData?, german: AyahData?, transliterated: AyahData?, index: Int) -> some View {
        let token = "\(surah.number):\(ar.numberInSurah)"
        let audioURL = resolvedAudioURLs[safe: index]
        let shareText = shareTextFor(ar: ar, turkish: turkish, german: german)

        return VStack(alignment: .leading, spacing: 10) {
            HStack(spacing: 12) {
                Text("\(ar.numberInSurah)")
                    .font(.caption.bold())
                    .frame(width: 30, height: 30)
                    .background(SalahTheme.gold.opacity(0.18), in: Circle())
                    .foregroundStyle(SalahTheme.deepTeal)
                Spacer()

                if let audioURL {
                    Button {
                        QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)
                        playFromAyah(index: index, ayahNumber: ar.numberInSurah)
                    } label: {
                        Image(systemName: audio.activeURL == audioURL && audio.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(settings.t(
                        audio.activeURL == audioURL && audio.isPlaying
                            ? "Vers \(ar.numberInSurah) pausieren"
                            : "Vers \(ar.numberInSurah) abspielen",
                        audio.activeURL == audioURL && audio.isPlaying
                            ? "\(ar.numberInSurah). ayeti duraklat"
                            : "\(ar.numberInSurah). ayeti oynat"
                    ))
                } else {
                    Image(systemName: "speaker.slash")
                        .foregroundStyle(.secondary)
                        .accessibilityLabel(settings.t(
                            "Audio für Vers \(ar.numberInSurah) nicht verfügbar",
                            "\(ar.numberInSurah). ayet için ses mevcut değil"
                        ))
                }

                ShareLink(item: shareText) { Image(systemName: "square.and.arrow.up") }
                    .buttonStyle(.plain)
                    .accessibilityLabel(settings.t(
                        "Vers \(ar.numberInSurah) teilen",
                        "\(ar.numberInSurah). ayeti paylaş"
                    ))

                Button {
                    let bookmark = QuranBookmark(surah: surah.number, ayah: ar.numberInSurah)
                    _ = QuranBookmarkStore.toggle(bookmark)
                    bookmarkedTokens = QuranBookmarkStore.tokens()
                } label: {
                    Image(systemName: bookmarkedTokens.contains(token) ? "bookmark.fill" : "bookmark")
                }
                .buttonStyle(.plain)
                .accessibilityLabel(settings.t(
                    bookmarkedTokens.contains(token)
                        ? "Lesezeichen für Vers \(ar.numberInSurah) entfernen"
                        : "Vers \(ar.numberInSurah) als Lesezeichen speichern",
                    bookmarkedTokens.contains(token)
                        ? "\(ar.numberInSurah). ayetin yer imini kaldır"
                        : "\(ar.numberInSurah). ayeti yer imine ekle"
                ))
                .accessibilityValue(bookmarkedTokens.contains(token)
                    ? settings.t("Gespeichert", "Kayıtlı")
                    : settings.t("Nicht gespeichert", "Kayıtlı değil"))
            }
            .foregroundStyle(SalahTheme.teal)

            Text(ar.text)
                .font(.system(size: max(settings.safeQuranFontSize, 28), weight: .regular))
                .multilineTextAlignment(.trailing)
                .frame(maxWidth: .infinity, alignment: .trailing)
                .textSelection(.enabled)

            if settings.quranShowTransliteration, let transliterated {
                Divider().overlay(SalahTheme.gold.opacity(0.30))
                Text(transliterated.text)
                    .font(.system(size: 12, weight: .semibold))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .textSelection(.enabled)
            }

            if settings.quranShowTranslation && displayMode == 1, let turkish {
                Divider().overlay(SalahTheme.gold.opacity(0.30))
                VStack(alignment: .leading, spacing: 3) {
                    Text(settings.t("Türkisch", "Türkçe"))
                        .font(.system(size: 8.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(turkish.text)
                        .font(.system(size: 13, weight: .medium))
                        .foregroundStyle(SalahTheme.ink)
                        .textSelection(.enabled)
                }
            }

            if settings.quranShowTranslation && displayMode == 2, let german {
                Divider().overlay(SalahTheme.gold.opacity(0.30))
                VStack(alignment: .leading, spacing: 3) {
                    Text(settings.t("Deutsch", "Almanca"))
                        .font(.system(size: 8.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(german.text)
                        .font(.system(size: 13, weight: .medium))
                        .foregroundStyle(SalahTheme.ink)
                        .textSelection(.enabled)
                }
            }
        }
        .padding(11)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 14)
                .stroke(
                    audio.queueCount == resolvedAudioURLs.count && audio.queueCount > 1 && audio.queueIndex == index && audio.isPlaying
                        ? SalahTheme.gold
                        : SalahTheme.gold.opacity(0.34),
                    lineWidth: audio.queueIndex == index && audio.isPlaying ? 1.7 : 1
                )
        }
        .onAppear { QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah) }
    }

    private var sourceFooter: some View {
        Text(settings.t(
            "Quran: lokal gebündelter Uthmani-Text · Quelle AlQuran.cloud / Islamic Network. Türkisch: Diyanet. Deutsch: Bubenheim & Elyas. Rezitation: menschliche Audioedition des Islamic Network.",
            "Kur'an: uygulamaya gömülü Uthmani metin · kaynak AlQuran.cloud / Islamic Network. Türkçe: Diyanet. Almanca: Bubenheim & Elyas. Tilavet: Islamic Network insan ses kaydı."
        ))
        .font(.caption2)
        .foregroundStyle(SalahTheme.mutedInk)
        .multilineTextAlignment(.center)
        .padding(10)
    }

    @MainActor
    private func loadContent() async {
        contentLoadRevision &+= 1
        let revision = contentLoadRevision
        error = nil
        contentWarning = nil

        do {
            let arabicResult = try await store.loadArabicSurah(surah.number)
            guard revision == contentLoadRevision else { return }

            // The Arabic surah is local and must render immediately. Network-backed
            // translations/transliteration are enhancements, never blockers.
            arabic = arabicResult
            error = nil

            let result = try await store.loadSurahReference(surah.number)
            guard revision == contentLoadRevision else { return }

            turkishTranslation = result.turkish
            germanTranslation = result.german
            transliteration = result.transliterated

            let missingSupplement = result.turkish == nil || result.german == nil || result.transliterated == nil
            if missingSupplement {
                contentWarning = settings.t(
                    "Arabischer Quran ist verfügbar. Einige Übersetzungen oder die Transliteration konnten gerade nicht geladen werden; bereits gecachte Inhalte bleiben nutzbar.",
                    "Arapça Kur'an kullanılabilir. Bazı mealler veya Latin harfli okunuş şu anda yüklenemedi; daha önce önbelleğe alınan içerikler kullanılmaya devam eder."
                )
            }
        } catch {
            guard revision == contentLoadRevision else { return }

            arabic = nil
            turkishTranslation = nil
            germanTranslation = nil
            transliteration = nil
            self.error = error.localizedDescription
            return
        }

        guard revision == contentLoadRevision else { return }
        await loadAudio()
    }

    @MainActor
    private func loadAudio() async {
        audioLoadRevision &+= 1
        let revision = audioLoadRevision
        let reciter = settings.quranReciter

        isResolvingAudio = true
        audio.lastError = nil
        defer {
            if revision == audioLoadRevision {
                isResolvingAudio = false
            }
        }

        do {
            let urls = try await QuranAudioResolver.urls(surah: surah.number, reciter: reciter)
            guard revision == audioLoadRevision,
                  reciter == settings.quranReciter else { return }

            resolvedAudioURLs = urls
            if urls.isEmpty {
                audio.lastError = settings.t("Audio derzeit nicht verfügbar.", "Ses şu anda mevcut değil.")
            }
        } catch {
            guard revision == audioLoadRevision else { return }

            resolvedAudioURLs = []
            audio.lastError = settings.t("Audio konnte nicht geladen werden. Erneut versuchen.", "Ses yüklenemedi. Tekrar dene.")
        }
    }

    private var audioReady: Bool { !resolvedAudioURLs.isEmpty }

    private func playFromAyah(index: Int, ayahNumber: Int) {
        guard resolvedAudioURLs.indices.contains(index) else {
            audio.lastError = settings.t("Audio für diesen Vers ist nicht verfügbar.", "Bu ayet için ses mevcut değil.")
            return
        }

        let selectedURL = resolvedAudioURLs[index]
        if audio.activeURL == selectedURL {
            audio.isPlaying ? audio.pause() : audio.resume()
            return
        }

        audio.playQueue(
            Array(resolvedAudioURLs.dropFirst(index)),
            title: surah.englishName,
            artist: settings.quranReciter.title,
            context: settings.t(
                "Quran \(surah.number):\(ayahNumber) · automatisch weiter",
                "Kur'an \(surah.number):\(ayahNumber) · otomatik devam"
            )
        )
    }

    private func toggleFullSurah() {
        guard audioReady else {
            audio.lastError = settings.t("Audio derzeit nicht verfügbar.", "Ses şu anda mevcut değil.")
            return
        }

        if let active = audio.activeURL, resolvedAudioURLs.contains(active) {
            audio.isPlaying ? audio.pause() : audio.resume()
        } else {
            audio.playQueue(
                resolvedAudioURLs,
                title: surah.englishName,
                artist: settings.quranReciter.title,
                context: settings.t("Quran · Sura \(surah.number)", "Kur'an · \(surah.number). sûre")
            )
        }
    }

    private func shareTextFor(ar: AyahData, turkish: AyahData?, german: AyahData?) -> String {
        var parts = [ar.text]
        if settings.quranShowTranslation {
            if displayMode == 1, let turkish { parts.append(turkish.text) }
            if displayMode == 2, let german { parts.append(german.text) }
        }
        parts.append("Quran \(surah.number):\(ar.numberInSurah)")
        return parts.joined(separator: "\n\n")
    }

    private func scrollToInitialIfNeeded(_ proxy: ScrollViewProxy) {
        guard !hasScrolledToInitial, let initialAyah else { return }
        guard arabic?.ayahs.contains(where: { $0.numberInSurah == initialAyah }) == true else { return }
        hasScrolledToInitial = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
            withAnimation { proxy.scrollTo(initialAyah, anchor: .top) }
        }
    }
}

private extension Collection {
    subscript(safe index: Index) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}

// MARK: - Shared card style

private extension View {
    func cardStyle(material:Bool=false) -> some View {
        self.frame(maxWidth:.infinity,alignment:.leading)
            .padding()
            .background(material ? AnyShapeStyle(SalahTheme.cream.opacity(0.94)) : AnyShapeStyle(SalahTheme.cream), in: RoundedRectangle(cornerRadius:20))
            .overlay { RoundedRectangle(cornerRadius:20).stroke(SalahTheme.cardStroke(),lineWidth:1) }
    }
}
