from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

anchor = """struct WuduGuideView: View {
"""
visual = r'''private struct WuduInstructionVisual: View {
    let key: String
    let stepNumber: Int

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(SalahTheme.softTeal.opacity(0.78))

            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)

            switch key {
            case "wudu_intention":
                if stepNumber == 1 { intentionVisual } else { basmalaVisual }
            case "wudu_hands": handsVisual
            case "wudu_mouth": faceVisual(highlightY: 31, dropsY: 34)
            case "wudu_nose": faceVisual(highlightY: 18, dropsY: 21)
            case "wudu_face": faceVisual(highlightY: 0, dropsY: -2, largeHighlight: true)
            case "wudu_rightarm": armVisual(mirrored: false)
            case "wudu_leftarm": armVisual(mirrored: true)
            case "wudu_head": headVisual
            case "wudu_ears": earsVisual
            case "wudu_neck": neckVisual
            case "wudu_feet": feetVisual
            default: genericVisual
            }
        }
        .frame(maxWidth: .infinity)
        .frame(height: 214)
        .accessibilityHidden(true)
    }

    private var intentionVisual: some View {
        ZStack {
            Image(systemName: "person.fill")
                .font(.system(size: 112, weight: .regular))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.82))
            Image(systemName: "heart.fill")
                .font(.system(size: 31, weight: .bold))
                .foregroundStyle(SalahTheme.gold)
                .offset(y: 4)
            Image(systemName: "drop.fill")
                .font(.system(size: 24, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
                .offset(x: 72, y: -58)
        }
    }

    private var basmalaVisual: some View {
        ZStack {
            Circle()
                .fill(Color.white.opacity(0.72))
                .frame(width: 122, height: 122)
            Image(systemName: "drop.fill")
                .font(.system(size: 68, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
            Image(systemName: "sparkles")
                .font(.system(size: 29, weight: .bold))
                .foregroundStyle(SalahTheme.gold)
                .offset(x: 58, y: -47)
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

    private func faceVisual(highlightY: CGFloat, dropsY: CGFloat, largeHighlight: Bool = false) -> some View {
        ZStack {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 142, weight: .regular))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.86))
            Ellipse()
                .fill(SalahTheme.gold.opacity(0.50))
                .frame(width: largeHighlight ? 76 : 42, height: largeHighlight ? 84 : 25)
                .offset(y: highlightY)
            HStack(spacing: 5) {
                drop(size: 14); drop(size: 18); drop(size: 14)
            }
            .offset(x: 71, y: dropsY)
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
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 142))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.86))
            Capsule()
                .fill(SalahTheme.gold.opacity(0.68))
                .frame(width: 90, height: 22)
                .offset(y: -48)
            HStack(spacing: 8) { drop(size: 14); drop(size: 18); drop(size: 14) }
                .offset(x: 70, y: -47)
        }
    }

    private var earsVisual: some View {
        ZStack {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 142))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.86))
            HStack(spacing: 92) {
                Circle().fill(SalahTheme.gold.opacity(0.70)).frame(width: 24, height: 42)
                Circle().fill(SalahTheme.gold.opacity(0.70)).frame(width: 24, height: 42)
            }
            HStack(spacing: 118) { drop(size: 16); drop(size: 16) }
                .offset(y: -4)
        }
    }

    private var neckVisual: some View {
        ZStack {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 142))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.86))
            Capsule()
                .fill(SalahTheme.gold.opacity(0.70))
                .frame(width: 72, height: 20)
                .offset(y: 65)
            HStack(spacing: 74) {
                Image(systemName: "hand.raised.fill")
                Image(systemName: "hand.raised.fill").scaleEffect(x: -1, y: 1)
            }
            .font(.system(size: 34))
            .foregroundStyle(SalahTheme.teal)
            .offset(y: 54)
        }
    }

    private var feetVisual: some View {
        ZStack {
            HStack(spacing: 20) {
                Capsule().fill(SalahTheme.deepTeal).frame(width: 58, height: 112).rotationEffect(.degrees(-16))
                Capsule().fill(SalahTheme.deepTeal).frame(width: 58, height: 112).rotationEffect(.degrees(16))
            }
            HStack(spacing: 18) { drop(size: 17); drop(size: 24); drop(size: 17) }
                .offset(y: -70)
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

'''
if anchor not in s:
    raise SystemExit("v3.63: WuduGuideView anchor missing")
s = s.replace(anchor, visual + anchor, 1)

old = """                            if let image = step.image {
                                Image(image)
                                    .resizable()
                                    .scaledToFit()
                                    .frame(maxWidth: .infinity)
                                    .frame(maxHeight: 275)
                                    .padding(8)
                                    .background(Color.white.opacity(0.55), in: RoundedRectangle(cornerRadius: 18))
                                    .accessibilityHidden(true)
                            }
"""
new = """                            if let image = step.image {
                                WuduInstructionVisual(key: image, stepNumber: step.number)
                            }
"""
if old not in s:
    raise SystemExit("v3.63: Wudu image block anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.63 Wudu vector visuals applied")
