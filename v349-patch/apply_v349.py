from pathlib import Path

# SalahPath v3.49 — Prayer Times poster parity.
# Rebuild the two lower tiles from the supplied right-phone reference:
# - Qibla card with diagonal compass needle + Kaaba
# - map artwork with large location pin and no generic labels/icons

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

q_start = s.index("    private var referenceQiblaTile: some View {")
q_end = s.index("\n    private var referenceMapTile: some View {", q_start)
m_start = q_end + 1
m_end = s.index("\n    private func referenceToolTile", m_start)

new_qibla = r'''    private var referenceQiblaTile: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Kıble Yönü")
                .font(.custom("AvenirNext-DemiBold", size: 10.6))
                .foregroundStyle(SalahTheme.ink)
            Text("Qibla")
                .font(.custom("AvenirNext-Medium", size: 8.4))
                .foregroundStyle(SalahTheme.mutedInk)

            Spacer(minLength: 2)

            ReferencePosterQiblaArt()
                .frame(maxWidth: .infinity, minHeight: 73, maxHeight: 73)
                .accessibilityHidden(true)
        }
        .frame(maxWidth: .infinity, minHeight: 126, alignment: .leading)
        .padding(10)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7)
        }
    }
'''

new_map = r'''    private var referenceMapTile: some View {
        ReferencePosterMapArt()
            .frame(maxWidth: .infinity, minHeight: 146, maxHeight: 146)
            .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
            .overlay {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 0.7)
            }
            .accessibilityHidden(true)
    }
'''

s = s[:q_start] + new_qibla + "\n" + new_map + s[m_end:]

marker = "private struct ReferencePagePattern: View {"
if marker not in s:
    raise SystemExit("v3.49: reference helper insertion point missing")

helpers = r'''private struct ReferencePosterQiblaArt: View {
    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height

            ZStack {
                // Long diagonal compass needle from the supplied poster.
                Path { p in
                    p.move(to: CGPoint(x: w * 0.08, y: h * 0.18))
                    p.addLine(to: CGPoint(x: w * 0.66, y: h * 0.48))
                    p.addLine(to: CGPoint(x: w * 0.22, y: h * 0.41))
                    p.closeSubpath()
                }
                .fill(SalahTheme.teal)

                Path { p in
                    p.move(to: CGPoint(x: w * 0.08, y: h * 0.18))
                    p.addLine(to: CGPoint(x: w * 0.50, y: h * 0.36))
                    p.addLine(to: CGPoint(x: w * 0.22, y: h * 0.41))
                    p.closeSubpath()
                }
                .fill(SalahTheme.gold)

                Circle()
                    .fill(Color(red: 0.94, green: 0.72, blue: 0.21))
                    .frame(width: max(5, w * 0.055), height: max(5, w * 0.055))
                    .position(x: w * 0.28, y: h * 0.33)

                // Kaaba: front, side face, top face and the gold kiswah band.
                Path { p in
                    p.move(to: CGPoint(x: w * 0.46, y: h * 0.49))
                    p.addLine(to: CGPoint(x: w * 0.79, y: h * 0.58))
                    p.addLine(to: CGPoint(x: w * 0.79, y: h * 0.91))
                    p.addLine(to: CGPoint(x: w * 0.46, y: h * 0.82))
                    p.closeSubpath()
                }
                .fill(Color.black.opacity(0.92))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.79, y: h * 0.58))
                    p.addLine(to: CGPoint(x: w * 0.91, y: h * 0.49))
                    p.addLine(to: CGPoint(x: w * 0.91, y: h * 0.81))
                    p.addLine(to: CGPoint(x: w * 0.79, y: h * 0.91))
                    p.closeSubpath()
                }
                .fill(Color.black.opacity(0.76))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.46, y: h * 0.49))
                    p.addLine(to: CGPoint(x: w * 0.60, y: h * 0.41))
                    p.addLine(to: CGPoint(x: w * 0.91, y: h * 0.49))
                    p.addLine(to: CGPoint(x: w * 0.79, y: h * 0.58))
                    p.closeSubpath()
                }
                .fill(Color.black.opacity(0.64))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.47, y: h * 0.60))
                    p.addLine(to: CGPoint(x: w * 0.79, y: h * 0.68))
                    p.addLine(to: CGPoint(x: w * 0.79, y: h * 0.73))
                    p.addLine(to: CGPoint(x: w * 0.47, y: h * 0.65))
                    p.closeSubpath()
                }
                .fill(SalahTheme.gold)

                Path { p in
                    p.move(to: CGPoint(x: w * 0.79, y: h * 0.68))
                    p.addLine(to: CGPoint(x: w * 0.91, y: h * 0.60))
                    p.addLine(to: CGPoint(x: w * 0.91, y: h * 0.65))
                    p.addLine(to: CGPoint(x: w * 0.79, y: h * 0.73))
                    p.closeSubpath()
                }
                .fill(SalahTheme.gold.opacity(0.78))
            }
            .frame(width: w, height: h)
        }
    }
}

private struct ReferencePosterMapArt: View {
    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height

            ZStack {
                Color(red: 0.72, green: 0.88, blue: 0.87)

                // Soft simplified world-map land masses matching the poster tile.
                Path { p in
                    p.move(to: CGPoint(x: w * 0.03, y: h * 0.18))
                    p.addCurve(
                        to: CGPoint(x: w * 0.25, y: h * 0.31),
                        control1: CGPoint(x: w * 0.09, y: h * 0.10),
                        control2: CGPoint(x: w * 0.22, y: h * 0.13)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.19, y: h * 0.50),
                        control1: CGPoint(x: w * 0.27, y: h * 0.39),
                        control2: CGPoint(x: w * 0.23, y: h * 0.46)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.08, y: h * 0.42),
                        control1: CGPoint(x: w * 0.15, y: h * 0.53),
                        control2: CGPoint(x: w * 0.09, y: h * 0.50)
                    )
                    p.closeSubpath()
                }
                .fill(Color.white.opacity(0.58))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.30, y: h * 0.14))
                    p.addCurve(
                        to: CGPoint(x: w * 0.60, y: h * 0.20),
                        control1: CGPoint(x: w * 0.38, y: h * 0.06),
                        control2: CGPoint(x: w * 0.52, y: h * 0.08)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.66, y: h * 0.39),
                        control1: CGPoint(x: w * 0.68, y: h * 0.24),
                        control2: CGPoint(x: w * 0.69, y: h * 0.32)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.49, y: h * 0.45),
                        control1: CGPoint(x: w * 0.59, y: h * 0.44),
                        control2: CGPoint(x: w * 0.54, y: h * 0.42)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.36, y: h * 0.34),
                        control1: CGPoint(x: w * 0.43, y: h * 0.49),
                        control2: CGPoint(x: w * 0.35, y: h * 0.44)
                    )
                    p.closeSubpath()
                }
                .fill(Color.white.opacity(0.64))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.43, y: h * 0.42))
                    p.addCurve(
                        to: CGPoint(x: w * 0.52, y: h * 0.79),
                        control1: CGPoint(x: w * 0.55, y: h * 0.49),
                        control2: CGPoint(x: w * 0.58, y: h * 0.65)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.37, y: h * 0.59),
                        control1: CGPoint(x: w * 0.44, y: h * 0.75),
                        control2: CGPoint(x: w * 0.37, y: h * 0.68)
                    )
                    p.closeSubpath()
                }
                .fill(Color.white.opacity(0.57))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.69, y: h * 0.24))
                    p.addCurve(
                        to: CGPoint(x: w * 0.96, y: h * 0.31),
                        control1: CGPoint(x: w * 0.80, y: h * 0.16),
                        control2: CGPoint(x: w * 0.91, y: h * 0.20)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.78, y: h * 0.49),
                        control1: CGPoint(x: w * 0.95, y: h * 0.42),
                        control2: CGPoint(x: w * 0.87, y: h * 0.48)
                    )
                    p.closeSubpath()
                }
                .fill(Color.white.opacity(0.55))

                Image(systemName: "mappin.circle.fill")
                    .font(.system(size: min(w, h) * 0.25, weight: .bold))
                    .symbolRenderingMode(.palette)
                    .foregroundStyle(SalahTheme.teal, Color.white)
                    .offset(x: w * 0.08, y: h * 0.08)
            }
            .frame(width: w, height: h)
        }
    }
}

'''
s = s.replace(marker, helpers + marker, 1)

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.48"' not in t or 'CURRENT_PROJECT_VERSION="53"' not in t:
    raise SystemExit("v3.49: expected v3.48/53 build version not found")
t = t.replace('MARKETING_VERSION="3.48"', 'MARKETING_VERSION="3.49"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="53"', 'CURRENT_PROJECT_VERSION="54"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.49 Prayer Times poster parity applied")
