from pathlib import Path

# SalahPath v3.34 — compile-safe dashboard glyph implementation.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

start = s.index("private struct ReferenceDashboardGlyph: View {")
end = s.index("\nprivate struct PrayerRow", start)

new_block = r'''private struct ReferenceDashboardGlyph: View {
    let kind: String

    var body: some View {
        glyph
    }

    private var glyph: AnyView {
        switch kind {
        case "quran":
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    ZStack {
                        Path { p in
                            p.move(to: CGPoint(x: w * 0.08, y: h * 0.20))
                            p.addQuadCurve(
                                to: CGPoint(x: w * 0.47, y: h * 0.28),
                                control: CGPoint(x: w * 0.28, y: h * 0.13)
                            )
                            p.addLine(to: CGPoint(x: w * 0.47, y: h * 0.86))
                            p.addQuadCurve(
                                to: CGPoint(x: w * 0.08, y: h * 0.74),
                                control: CGPoint(x: w * 0.27, y: h * 0.65)
                            )
                            p.closeSubpath()

                            p.move(to: CGPoint(x: w * 0.92, y: h * 0.20))
                            p.addQuadCurve(
                                to: CGPoint(x: w * 0.53, y: h * 0.28),
                                control: CGPoint(x: w * 0.72, y: h * 0.13)
                            )
                            p.addLine(to: CGPoint(x: w * 0.53, y: h * 0.86))
                            p.addQuadCurve(
                                to: CGPoint(x: w * 0.92, y: h * 0.74),
                                control: CGPoint(x: w * 0.73, y: h * 0.65)
                            )
                            p.closeSubpath()
                        }
                        .fill(SalahTheme.teal)

                        Rectangle()
                            .fill(SalahTheme.cream.opacity(0.86))
                            .frame(width: max(1.2, w * 0.035), height: h * 0.60)
                            .offset(y: h * 0.08)
                    }
                }
            )

        case "dhikr":
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    ZStack {
                        ForEach(0..<10, id: \.self) { index in
                            let angle = Double(index) * 25.0 - 90.0
                            Circle()
                                .fill(SalahTheme.teal)
                                .frame(width: w * 0.14, height: w * 0.14)
                                .offset(
                                    x: cos(angle * .pi / 180.0) * w * 0.26,
                                    y: sin(angle * .pi / 180.0) * h * 0.26
                                )
                        }

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.10, height: h * 0.32)
                            .rotationEffect(.degrees(28))
                            .offset(x: -w * 0.20, y: h * 0.25)
                    }
                }
            )

        case "prayer":
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.18, height: w * 0.18)
                            .offset(y: -h * 0.30)

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.16, height: h * 0.43)
                            .rotationEffect(.degrees(-14))
                            .offset(x: -w * 0.06, y: -h * 0.04)

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.12, height: h * 0.34)
                            .rotationEffect(.degrees(72))
                            .offset(x: w * 0.12, y: h * 0.18)

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.11, height: h * 0.30)
                            .rotationEffect(.degrees(95))
                            .offset(x: -w * 0.08, y: h * 0.30)

                        Capsule()
                            .fill(SalahTheme.teal)
                            .frame(width: w * 0.66, height: max(3, h * 0.07))
                            .offset(y: h * 0.39)
                    }
                }
            )

        case "wudu":
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    Path { p in
                        p.move(to: CGPoint(x: w * 0.50, y: h * 0.04))
                        p.addCurve(
                            to: CGPoint(x: w * 0.18, y: h * 0.62),
                            control1: CGPoint(x: w * 0.33, y: h * 0.29),
                            control2: CGPoint(x: w * 0.18, y: h * 0.45)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.50, y: h * 0.94),
                            control1: CGPoint(x: w * 0.18, y: h * 0.81),
                            control2: CGPoint(x: w * 0.32, y: h * 0.94)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.82, y: h * 0.62),
                            control1: CGPoint(x: w * 0.68, y: h * 0.94),
                            control2: CGPoint(x: w * 0.82, y: h * 0.81)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.50, y: h * 0.04),
                            control1: CGPoint(x: w * 0.82, y: h * 0.45),
                            control2: CGPoint(x: w * 0.67, y: h * 0.29)
                        )
                    }
                    .fill(SalahTheme.teal)
                }
            )

        case "times":
            return AnyView(
                ZStack {
                    Circle()
                        .stroke(SalahTheme.teal, lineWidth: 3)
                    Rectangle()
                        .fill(SalahTheme.teal)
                        .frame(width: 2.4, height: 10)
                        .offset(y: -5)
                    Rectangle()
                        .fill(SalahTheme.teal)
                        .frame(width: 9, height: 2.4)
                        .offset(x: -4.5)
                }
                .padding(2)
            )

        case "qibla":
            return AnyView(
                ZStack {
                    Circle()
                        .stroke(SalahTheme.teal, lineWidth: 3)
                    Path { p in
                        p.move(to: CGPoint(x: 24, y: 7))
                        p.addLine(to: CGPoint(x: 18, y: 20))
                        p.addLine(to: CGPoint(x: 7, y: 27))
                        p.addLine(to: CGPoint(x: 13, y: 14))
                        p.closeSubpath()
                    }
                    .fill(SalahTheme.teal)
                    .scaleEffect(0.85)
                }
                .padding(2)
            )

        case "info":
            return AnyView(
                VStack(spacing: 1) {
                    ZStack {
                        Circle()
                            .fill(SalahTheme.teal)
                            .frame(width: 23, height: 23)
                        Rectangle()
                            .fill(SalahTheme.cream)
                            .frame(width: 3, height: 10)
                            .offset(y: 4)
                    }
                    Capsule()
                        .fill(SalahTheme.teal)
                        .frame(width: 17, height: 5)
                    Capsule()
                        .fill(SalahTheme.teal)
                        .frame(width: 12, height: 3)
                }
            )

        default:
            return AnyView(
                GeometryReader { proxy in
                    let w = proxy.size.width
                    let h = proxy.size.height
                    Path { p in
                        p.move(to: CGPoint(x: w * 0.50, y: h * 0.90))
                        p.addCurve(
                            to: CGPoint(x: w * 0.08, y: h * 0.36),
                            control1: CGPoint(x: w * 0.19, y: h * 0.69),
                            control2: CGPoint(x: w * 0.04, y: h * 0.53)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.50, y: h * 0.22),
                            control1: CGPoint(x: w * 0.10, y: h * 0.10),
                            control2: CGPoint(x: w * 0.36, y: h * 0.14)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.92, y: h * 0.36),
                            control1: CGPoint(x: w * 0.64, y: h * 0.14),
                            control2: CGPoint(x: w * 0.90, y: h * 0.10)
                        )
                        p.addCurve(
                            to: CGPoint(x: w * 0.50, y: h * 0.90),
                            control1: CGPoint(x: w * 0.96, y: h * 0.53),
                            control2: CGPoint(x: w * 0.81, y: h * 0.69)
                        )
                    }
                    .fill(SalahTheme.teal)
                }
            )
        }
    }
}
'''

s = s[:start] + new_block + s[end:]
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.33"', 'MARKETING_VERSION="3.34"')
t = t.replace('CURRENT_PROJECT_VERSION="38"', 'CURRENT_PROJECT_VERSION="39"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.34 compile-safe dashboard glyph implementation applied")
