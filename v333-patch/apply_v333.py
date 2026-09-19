from pathlib import Path

# SalahPath v3.33 — dashboard icon + copy parity from the supplied reference.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# Exact reference tile copy/line breaks.
replacements = {
'''DashboardTile(title: settings.t("Qur'an", "Kur'an"), subtitle: settings.t("Lesen & Hören", "Oku & Dinle"), icon: "book.fill")''':
'''DashboardTile(title: "Kur'an", subtitle: "Oku & Dinle", icon: "quran")''',

'''DashboardTile(title: settings.t("Dua & Dhikr", "Dua & Zikir"), subtitle: settings.t("Dua & Zikir", "Dua & Zikir"), icon: "hands.sparkles.fill")''':
'''DashboardTile(title: "Dua &\\nZikir", subtitle: "", icon: "dhikr")''',

'''DashboardTile(title: settings.t("Namaz lernen", "Namaz Öğren"), subtitle: settings.t("Schritt für Schritt", "Adım adım"), icon: "figure.stand")''':
'''DashboardTile(title: "Namaz\\nÖğren", subtitle: "", icon: "prayer")''',

'''DashboardTile(title: settings.t("Wudu Guide", "Abdest Rehberi"), subtitle: settings.t("Abdest", "Abdest"), icon: "drop.fill")''':
'''DashboardTile(title: "Abdest\\nRehberi", subtitle: "", icon: "wudu")''',

'''DashboardTile(title: settings.t("Gebetszeiten", "Namaz Vakitleri"), subtitle: settings.t("Namaz Vakitleri", "Namaz Vakitleri"), icon: "clock.fill")''':
'''DashboardTile(title: "Gebetszeiten", subtitle: "Namaz Vakitleri", icon: "times")''',

'''DashboardTile(title: settings.t("Qibla-Richtung", "Kıble Yönü"), subtitle: "Qibla", icon: "location.north.circle.fill")''':
'''DashboardTile(title: "Kıble Yönü", subtitle: "Qibla", icon: "qibla")''',

'''DashboardTile(title: settings.t("Islamisches Wissen", "İslami Bilgiler"), subtitle: settings.t("Bilgi", "Bilgi"), icon: "lightbulb.fill")''':
'''DashboardTile(title: "İslami Bilgiler", subtitle: "Bilgi", icon: "info")''',

'''DashboardTile(title: settings.t("Favoriten", "Favorilerim"), subtitle: settings.t("Favorilerim", "Favorilerim"), icon: "heart.fill")''':
'''DashboardTile(title: "Favorilerim", subtitle: "Favorilerim", icon: "fav")'''
}
for old,new in replacements.items():
    if old not in s:
        raise SystemExit(f"dashboard target not found: {old[:45]}")
    s=s.replace(old,new,1)

# Quote strip uses the same bespoke leaf family as the brand, not the stock SF leaf.
s=s.replace(
'''            Image(systemName: "leaf.fill")
                .font(.system(size: 15, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
''',
'''            ReferenceLeafMark()
                .frame(width: 20, height: 25)
''', 1)

# Replace stock symbol tile renderer with custom vector glyphs modeled on the reference.
start=s.index("private struct DashboardTile: View {")
end=s.index("\nprivate struct PrayerRow",start)

new_block=r'''private struct DashboardTile: View {
    let title: String
    let subtitle: String
    let icon: String

    var body: some View {
        VStack(spacing: 4) {
            ReferenceDashboardGlyph(kind: icon)
                .frame(width: 34, height: 34)

            Text(title)
                .font(.system(size: 8.8, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .multilineTextAlignment(.center)
                .lineLimit(2)
                .fixedSize(horizontal: false, vertical: true)
                .minimumScaleFactor(0.70)

            if !subtitle.isEmpty {
                Text(subtitle)
                    .font(.system(size: 6.8, weight: .semibold))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .multilineTextAlignment(.center)
                    .lineLimit(1)
                    .minimumScaleFactor(0.72)
            } else {
                Color.clear.frame(height: 7)
            }
        }
        .frame(maxWidth: .infinity, minHeight: 89, alignment: .center)
        .padding(.horizontal, 3)
        .padding(.vertical, 5)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 9, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 9, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.56), lineWidth: 0.8)
        }
    }
}

private struct ReferenceDashboardGlyph: View {
    let kind: String

    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height
            let c = SalahTheme.teal

            ZStack {
                switch kind {
                case "quran":
                    Path { p in
                        p.move(to: CGPoint(x: w*0.08, y: h*0.20))
                        p.addQuadCurve(to: CGPoint(x: w*0.47, y: h*0.28),
                                       control: CGPoint(x: w*0.28, y: h*0.13))
                        p.addLine(to: CGPoint(x: w*0.47, y: h*0.86))
                        p.addQuadCurve(to: CGPoint(x: w*0.08, y: h*0.74),
                                       control: CGPoint(x: w*0.27, y: h*0.65))
                        p.closeSubpath()
                        p.move(to: CGPoint(x: w*0.92, y: h*0.20))
                        p.addQuadCurve(to: CGPoint(x: w*0.53, y: h*0.28),
                                       control: CGPoint(x: w*0.72, y: h*0.13))
                        p.addLine(to: CGPoint(x: w*0.53, y: h*0.86))
                        p.addQuadCurve(to: CGPoint(x: w*0.92, y: h*0.74),
                                       control: CGPoint(x: w*0.73, y: h*0.65))
                        p.closeSubpath()
                    }
                    .fill(c)

                    Path { p in
                        p.move(to: CGPoint(x: w*0.50, y: h*0.25))
                        p.addLine(to: CGPoint(x: w*0.50, y: h*0.87))
                    }.stroke(SalahTheme.cream.opacity(0.85), lineWidth: max(1, w*0.035))

                case "dhikr":
                    Canvas { context, size in
                        let pts:[CGPoint] = [
                            .init(x:.34,y:.78), .init(x:.32,y:.65), .init(x:.35,y:.52),
                            .init(x:.43,y:.40), .init(x:.54,y:.32), .init(x:.66,y:.28),
                            .init(x:.77,y:.31), .init(x:.84,y:.40), .init(x:.84,y:.50),
                            .init(x:.78,y:.58), .init(x:.68,y:.62), .init(x:.57,y:.61),
                            .init(x:.48,y:.57)
                        ].map { .init(x:$0.x*size.width,y:$0.y*size.height) }
                        for pt in pts {
                            let r=size.width*0.075
                            context.fill(Path(ellipseIn:CGRect(x:pt.x-r,y:pt.y-r,width:r*2,height:r*2)),
                                         with:.color(c))
                        }
                        var tail=Path()
                        tail.move(to:CGPoint(x:size.width*0.34,y:size.height*0.75))
                        tail.addCurve(to:CGPoint(x:size.width*0.22,y:size.height*0.94),
                                      control1:CGPoint(x:size.width*0.29,y:size.height*0.80),
                                      control2:CGPoint(x:size.width*0.22,y:size.height*0.87))
                        context.stroke(tail,with:.color(c),lineWidth:size.width*0.08)
                    }

                case "prayer":
                    Canvas { context,size in
                        let col=c
                        context.fill(Path(ellipseIn:CGRect(x:size.width*0.42,y:size.height*0.08,
                                                          width:size.width*0.18,height:size.width*0.18)),
                                     with:.color(col))
                        var body=Path()
                        body.move(to:CGPoint(x:size.width*0.48,y:size.height*0.24))
                        body.addCurve(to:CGPoint(x:size.width*0.42,y:size.height*0.61),
                                      control1:CGPoint(x:size.width*0.39,y:size.height*0.33),
                                      control2:CGPoint(x:size.width*0.39,y:size.height*0.48))
                        body.addCurve(to:CGPoint(x:size.width*0.72,y:size.height*0.75),
                                      control1:CGPoint(x:size.width*0.48,y:size.height*0.69),
                                      control2:CGPoint(x:size.width*0.61,y:size.height*0.73))
                        context.stroke(body,with:.color(col),lineWidth:size.width*0.14)
                        var arm=Path()
                        arm.move(to:CGPoint(x:size.width*0.46,y:size.height*0.39))
                        arm.addLine(to:CGPoint(x:size.width*0.58,y:size.height*0.57))
                        arm.addLine(to:CGPoint(x:size.width*0.71,y:size.height*0.60))
                        context.stroke(arm,with:.color(col),lineWidth:size.width*0.09)
                        var base=Path()
                        base.move(to:CGPoint(x:size.width*0.20,y:size.height*0.82))
                        base.addLine(to:CGPoint(x:size.width*0.78,y:size.height*0.82))
                        context.stroke(base,with:.color(col),lineWidth:size.width*0.10)
                    }

                case "wudu":
                    Path { p in
                        p.move(to:CGPoint(x:w*0.50,y:h*0.04))
                        p.addCurve(to:CGPoint(x:w*0.18,y:h*0.62),
                                   control1:CGPoint(x:w*0.33,y:h*0.29),
                                   control2:CGPoint(x:w*0.18,y:h*0.45))
                        p.addCurve(to:CGPoint(x:w*0.50,y:h*0.94),
                                   control1:CGPoint(x:w*0.18,y:h*0.81),
                                   control2:CGPoint(x:w*0.32,y:h*0.94))
                        p.addCurve(to:CGPoint(x:w*0.82,y:h*0.62),
                                   control1:CGPoint(x:w*0.68,y:h*0.94),
                                   control2:CGPoint(x:w*0.82,y:h*0.81))
                        p.addCurve(to:CGPoint(x:w*0.50,y:h*0.04),
                                   control1:CGPoint(x:w*0.82,y:h*0.45),
                                   control2:CGPoint(x:w*0.67,y:h*0.29))
                    }.fill(c)

                case "times":
                    Circle().stroke(c,lineWidth:max(2,w*0.085))
                        .padding(w*0.09)
                    Path { p in
                        p.move(to:CGPoint(x:w*0.50,y:h*0.50))
                        p.addLine(to:CGPoint(x:w*0.50,y:h*0.29))
                        p.move(to:CGPoint(x:w*0.50,y:h*0.50))
                        p.addLine(to:CGPoint(x:w*0.35,y:h*0.50))
                        p.move(to:CGPoint(x:w*0.50,y:h*0.06))
                        p.addLine(to:CGPoint(x:w*0.50,y:h*0.14))
                    }.stroke(c,lineWidth:max(2,w*0.07),lineCap:.round)

                case "qibla":
                    Circle().stroke(c,lineWidth:max(2,w*0.08))
                        .padding(w*0.08)
                    Path { p in
                        p.move(to:CGPoint(x:w*0.67,y:h*0.28))
                        p.addLine(to:CGPoint(x:w*0.55,y:h*0.58))
                        p.addLine(to:CGPoint(x:w*0.31,y:h*0.72))
                        p.addLine(to:CGPoint(x:w*0.44,y:h*0.42))
                        p.closeSubpath()
                    }.fill(c)
                    Circle().fill(c).frame(width:w*0.08,height:w*0.08)

                case "info":
                    ZStack {
                        Path { p in
                            p.addEllipse(in:CGRect(x:w*0.24,y:h*0.06,width:w*0.52,height:h*0.56))
                            p.move(to:CGPoint(x:w*0.36,y:h*0.59))
                            p.addLine(to:CGPoint(x:w*0.64,y:h*0.59))
                            p.addLine(to:CGPoint(x:w*0.60,y:h*0.78))
                            p.addLine(to:CGPoint(x:w*0.40,y:h*0.78))
                            p.closeSubpath()
                        }.fill(c)
                        Path { p in
                            p.move(to:CGPoint(x:w*0.39,y:h*0.84))
                            p.addLine(to:CGPoint(x:w*0.61,y:h*0.84))
                            p.move(to:CGPoint(x:w*0.42,y:h*0.91))
                            p.addLine(to:CGPoint(x:w*0.58,y:h*0.91))
                        }.stroke(c,lineWidth:max(1.5,w*0.055),lineCap:.round)
                    }

                default:
                    Path { p in
                        p.move(to:CGPoint(x:w*0.50,y:h*0.90))
                        p.addCurve(to:CGPoint(x:w*0.08,y:h*0.36),
                                   control1:CGPoint(x:w*0.19,y:h*0.69),
                                   control2:CGPoint(x:w*0.04,y:h*0.53))
                        p.addCurve(to:CGPoint(x:w*0.50,y:h*0.22),
                                   control1:CGPoint(x:w*0.10,y:h*0.10),
                                   control2:CGPoint(x:w*0.36,y:h*0.14))
                        p.addCurve(to:CGPoint(x:w*0.92,y:h*0.36),
                                   control1:CGPoint(x:w*0.64,y:h*0.14),
                                   control2:CGPoint(x:w*0.90,y:h*0.10))
                        p.addCurve(to:CGPoint(x:w*0.50,y:h*0.90),
                                   control1:CGPoint(x:w*0.96,y:h*0.53),
                                   control2:CGPoint(x:w*0.81,y:h*0.69))
                    }.fill(c)
                }
            }
        }
    }
}
'''
s=s[:start]+new_block+s[end:]

p.write_text(s,encoding="utf-8")

b=Path("scripts/build_unsigned_ipa.sh")
t=b.read_text(encoding="utf-8")
t=t.replace('MARKETING_VERSION="3.32"','MARKETING_VERSION="3.33"')
t=t.replace('CURRENT_PROJECT_VERSION="37"','CURRENT_PROJECT_VERSION="38"')
b.write_text(t,encoding="utf-8")

print("SalahPath v3.33 dashboard reference glyph pass applied")
