from pathlib import Path

# SalahPath v3.52 — Namaz hero parity.
# Match the supplied lower-left reference phone:
# - seated male/female fill the hero
# - distinct green prayer rugs under each person
# - action arrow sits on the right edge, not between the figures

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

old = '''            ZStack {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .fill(Color(red: 0.96, green: 0.93, blue: 0.84))

                HStack(alignment: .bottom, spacing: 1) {
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

                    Button {
                        settings.prayerAudience = settings.prayerAudience == .male ? .female : .male
                    } label: {
                        ZStack {
                            Circle()
                                .fill(SalahTheme.teal)
                                .frame(width: 30, height: 30)
                            Image(systemName: "chevron.right")
                                .font(.system(size: 11, weight: .black))
                                .foregroundStyle(.white)
                        }
                    }
                    .buttonStyle(.plain)
                    .padding(.bottom, 50)

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
                .padding(.horizontal, 5)
                .padding(.vertical, 5)
            }
            .frame(height: 176)
'''
new = '''            ZStack(alignment: .trailing) {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .fill(Color(red: 0.96, green: 0.93, blue: 0.84))

                HStack(alignment: .bottom, spacing: 10) {
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
                .padding(.horizontal, 12)
                .padding(.vertical, 2)

                Button {
                    settings.prayerAudience = settings.prayerAudience == .male ? .female : .male
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
            .frame(height: 176)
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
