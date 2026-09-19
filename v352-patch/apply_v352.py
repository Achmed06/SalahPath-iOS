from pathlib import Path

# SalahPath v3.52 — Namaz hero parity.
# Match the supplied lower-left reference phone:
# - seated male/female fill the hero
# - distinct green prayer rugs under each person
# - action arrow sits on the right edge, not between the figures

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

old = '''                ZStack {
                    HStack(spacing: 18) {
                        ZStack(alignment: .bottom) {
                            RoundedRectangle(cornerRadius: 5, style: .continuous)
                                .fill(SalahTheme.teal.opacity(0.18))
                                .frame(maxWidth: .infinity, minHeight: 43, maxHeight: 43)
                                .overlay {
                                    RoundedRectangle(cornerRadius: 5, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.28), lineWidth: 0.8)
                                }
                            Image("male_sitting")
                                .resizable()
                                .scaledToFit()
                                .frame(maxWidth: .infinity, maxHeight: 125)
                                .blendMode(.multiply)
                                .padding(.bottom, 5)
                        }
                        .frame(maxWidth: .infinity, maxHeight: 161, alignment: .bottom)

                        ZStack(alignment: .bottom) {
                            RoundedRectangle(cornerRadius: 5, style: .continuous)
                                .fill(SalahTheme.teal.opacity(0.18))
                                .frame(maxWidth: .infinity, minHeight: 43, maxHeight: 43)
                                .overlay {
                                    RoundedRectangle(cornerRadius: 5, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.28), lineWidth: 0.8)
                                }
                            Image("female_sitting")
                                .resizable()
                                .scaledToFit()
                                .frame(maxWidth: .infinity, maxHeight: 125)
                                .blendMode(.multiply)
                                .padding(.bottom, 5)
                        }
                        .frame(maxWidth: .infinity, maxHeight: 161, alignment: .bottom)
                    }

                    Image(systemName: "chevron.right")
                        .font(.system(size: 15, weight: .bold))
                        .foregroundStyle(.white)
                        .frame(width: 34, height: 34)
                        .background(SalahTheme.teal, in: Circle())
                }
'''
new = '''                ZStack(alignment: .trailing) {
                    HStack(spacing: 10) {
                        ReferencePrayerPerson(
                            imageName: "male_sitting",
                            rugWidth: 128,
                            rugRotation: -1.5
                        )

                        ReferencePrayerPerson(
                            imageName: "female_sitting",
                            rugWidth: 128,
                            rugRotation: 1.5
                        )
                    }
                    .padding(.horizontal, 14)

                    Image(systemName: "chevron.right")
                        .font(.system(size: 15, weight: .bold))
                        .foregroundStyle(.white)
                        .frame(width: 34, height: 34)
                        .background(SalahTheme.teal, in: Circle())
                        .offset(x: 4)
                }
                .frame(maxWidth: .infinity, minHeight: 178, maxHeight: 178)
'''
if old not in s:
    raise SystemExit("v3.52: current Namaz hero block not found")
s = s.replace(old, new, 1)

marker = "private struct ReferencePosterQiblaArt: View {"
if marker not in s:
    raise SystemExit("v3.52: helper insertion marker missing")

helper = r'''private struct ReferencePrayerPerson: View {
    let imageName: String
    let rugWidth: CGFloat
    let rugRotation: Double

    var body: some View {
        ZStack(alignment: .bottom) {
            GeometryReader { proxy in
                let w = min(rugWidth, proxy.size.width * 0.92)
                let h: CGFloat = 48

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
            .frame(height: 58)

            Image(imageName)
                .resizable()
                .scaledToFit()
                .frame(maxWidth: .infinity, maxHeight: 170)
                .blendMode(.multiply)
                .padding(.bottom, 5)
                .scaleEffect(1.12, anchor: .bottom)
        }
        .frame(maxWidth: .infinity, minHeight: 178, maxHeight: 178, alignment: .bottom)
    }
}

'''

s = s.replace(marker, helper + marker, 1)
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.51"' not in t or 'CURRENT_PROJECT_VERSION="56"' not in t:
    raise SystemExit("v3.52: expected v3.51/56 build version not found")
t = t.replace('MARKETING_VERSION="3.51"', 'MARKETING_VERSION="3.52"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="56"', 'CURRENT_PROJECT_VERSION="57"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.52 Namaz hero reference parity applied")
