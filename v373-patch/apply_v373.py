from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = r'''private struct ReferencePrayerPerson: View {
    let imageName: String
    let rugWidth: CGFloat
    let rugRotation: Double

    var body: some View {
        PrayerPoseArtwork(assetName: imageName)
            .frame(maxWidth: .infinity, minHeight: 286, maxHeight: 286)
            .padding(.horizontal, 4)
    }
}
'''
new = r'''private struct ReferencePrayerPerson: View {
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
'''
if old not in s:
    raise SystemExit("v3.73: simplified ReferencePrayerPerson from v3.71 not found")
s = s.replace(old, new, 1)

old_bg = '''            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .fill(SalahTheme.softTeal.opacity(0.38))
'''
new_bg = '''            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .fill(SalahTheme.cream)
'''
if old_bg not in s:
    raise SystemExit("v3.73: prayer artwork background anchor missing")
s = s.replace(old_bg, new_bg, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.73 restored stable prayer hero layout with opaque artwork surface")
