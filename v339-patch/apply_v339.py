from pathlib import Path

p = Path('SalahZeit/Views/HomeView.swift')
s = p.read_text(encoding='utf-8')

old = '''        ZStack(alignment: .bottomTrailing) {
            Image("home_mosque")
'''
new = '''        ZStack(alignment: .bottomTrailing) {
            LinearGradient(
                colors: [
                    Color.clear,
                    SalahTheme.gold.opacity(0.08),
                    Color(red: 0.98, green: 0.85, blue: 0.69).opacity(0.18)
                ],
                startPoint: .leading,
                endPoint: .trailing
            )
            .frame(width: 205, height: 116)
            .offset(x: 9, y: -40)
            .allowsHitTesting(false)

            Image("home_mosque")
'''
if old in s:
    s = s.replace(old, new, 1)

old = '''                    Image(systemName: prayer.kind.systemImage)
                        .font(.system(size: 18.2, weight: .regular))
                        .symbolRenderingMode(.hierarchical)
                        .foregroundStyle(SalahTheme.gold)
                        .frame(width: 31)
'''
new = '''                    Group {
                        if isScreenshotQA || prayer.kind == .asr {
                            ReferenceSunGlyph()
                                .frame(width: 29, height: 29)
                        } else {
                            Image(systemName: prayer.kind.systemImage)
                                .font(.system(size: 18, weight: .regular))
                                .symbolRenderingMode(.hierarchical)
                                .foregroundStyle(SalahTheme.gold)
                        }
                    }
                    .frame(width: 31, height: 31)
'''
if old in s:
    s = s.replace(old, new, 1)

s = s.replace('Image(systemName: "location.fill")', 'Image(systemName: "mappin")', 1)

old = '''                    Image(systemName: prayer.kind.systemImage)
                        .font(.system(size: 10, weight: .semibold))
                        .foregroundStyle(SalahTheme.gold)
'''
new = '''                    Group {
                        if isScreenshotQA || prayer.kind == .asr {
                            ReferenceSunGlyph()
                                .frame(width: 15, height: 15)
                        } else {
                            Image(systemName: prayer.kind.systemImage)
                                .font(.system(size: 10, weight: .semibold))
                                .foregroundStyle(SalahTheme.gold)
                        }
                    }
'''
if old in s:
    s = s.replace(old, new, 1)

s = s.replace(
    '.font(.system(size: 7.4, weight: .medium, design: .serif))',
    '.font(.custom("Georgia-Italic", size: 6.9))',
    1
)

old = '''                ZStack {
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(SalahTheme.softTeal)
                        .frame(width: 27, height: 27)
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(SalahTheme.teal)
                }
'''
new = '''                ZStack {
                    Circle()
                        .fill(Color(red: 0.97, green: 0.93, blue: 0.79))
                        .frame(width: 27, height: 27)
                    ReferenceLeafMark(color: SalahTheme.teal)
                        .frame(width: 14, height: 18)
                }
'''
if old in s:
    s = s.replace(old, new, 1)

old = '''                Image(systemName: "flame.fill")
                    .font(.system(size: 16))
                    .foregroundStyle(SalahTheme.gold)
'''
new = '''                ReferenceFlameGlyph()
                    .frame(width: 18, height: 22)
'''
if old in s:
    s = s.replace(old, new, 1)

s = s.replace('.font(.system(size: 6.5, weight: .bold))',
              '.font(.custom("AvenirNext-DemiBold", size: 6.2))', 1)

s = s.replace('''ReferenceLeafMark()
                .frame(width: 20, height: 25)''',
              '''ReferenceLeafMark(color: SalahTheme.teal)
                .frame(width: 18, height: 23)''', 1)

s = s.replace('''        .background(
            SalahTheme.cream,
            in: RoundedRectangle(cornerRadius: 9, style: .continuous)
        )
''',
'''        .background(
            Color(red: 0.97, green: 0.95, blue: 0.86),
            in: RoundedRectangle(cornerRadius: 8, style: .continuous)
        )
''', 1)

s = s.replace('''private struct ReferenceLeafMark: View {
    var body: some View {''',
              '''private struct ReferenceLeafMark: View {
    var color: Color = SalahTheme.gold

    var body: some View {''', 1)
s = s.replace('''.fill(SalahTheme.gold)
''', '''.fill(color)
''', 1)
s = s.replace('''.fill(SalahTheme.gold.opacity(0.96))
''', '''.fill(color.opacity(0.96))
''', 1)

marker = 'private struct ReferenceLeafMark: View {'
if marker in s and 'private struct ReferenceSunGlyph: View {' not in s:
    glyphs = r'''private struct ReferenceSunGlyph: View {
    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height
            let c = SalahTheme.gold
            ZStack {
                Circle()
                    .fill(c)
                    .frame(width: w * 0.46, height: h * 0.46)

                ForEach(0..<8, id: .self) { index in
                    Capsule()
                        .fill(c)
                        .frame(width: max(1.1, w * 0.07), height: h * 0.20)
                        .offset(y: -h * 0.39)
                        .rotationEffect(.degrees(Double(index) * 45.0))
                }
            }
            .frame(width: w, height: h)
        }
        .accessibilityHidden(true)
    }
}

private struct ReferenceFlameGlyph: View {
    var body: some View {
        GeometryReader { proxy in
            let w = proxy.size.width
            let h = proxy.size.height
            ZStack(alignment: .bottom) {
                Path { p in
                    p.move(to: CGPoint(x: w * 0.50, y: h * 0.02))
                    p.addCurve(
                        to: CGPoint(x: w * 0.18, y: h * 0.63),
                        control1: CGPoint(x: w * 0.45, y: h * 0.25),
                        control2: CGPoint(x: w * 0.18, y: h * 0.35)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.50, y: h * 0.98),
                        control1: CGPoint(x: w * 0.18, y: h * 0.85),
                        control2: CGPoint(x: w * 0.34, y: h * 0.98)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.82, y: h * 0.60),
                        control1: CGPoint(x: w * 0.70, y: h * 0.98),
                        control2: CGPoint(x: w * 0.84, y: h * 0.79)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.50, y: h * 0.02),
                        control1: CGPoint(x: w * 0.82, y: h * 0.39),
                        control2: CGPoint(x: w * 0.63, y: h * 0.27)
                    )
                    p.closeSubpath()
                }
                .fill(Color(red: 0.91, green: 0.31, blue: 0.13))

                Path { p in
                    p.move(to: CGPoint(x: w * 0.50, y: h * 0.43))
                    p.addCurve(
                        to: CGPoint(x: w * 0.35, y: h * 0.76),
                        control1: CGPoint(x: w * 0.44, y: h * 0.56),
                        control2: CGPoint(x: w * 0.35, y: h * 0.64)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.50, y: h * 0.91),
                        control1: CGPoint(x: w * 0.36, y: h * 0.86),
                        control2: CGPoint(x: w * 0.43, y: h * 0.91)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.65, y: h * 0.75),
                        control1: CGPoint(x: w * 0.58, y: h * 0.91),
                        control2: CGPoint(x: w * 0.65, y: h * 0.85)
                    )
                    p.addCurve(
                        to: CGPoint(x: w * 0.50, y: h * 0.43),
                        control1: CGPoint(x: w * 0.65, y: h * 0.62),
                        control2: CGPoint(x: w * 0.57, y: h * 0.54)
                    )
                    p.closeSubpath()
                }
                .fill(SalahTheme.gold)
            }
        }
        .accessibilityHidden(true)
    }
}

'''
    s = s.replace(marker, glyphs + marker, 1)

p.write_text(s, encoding='utf-8')

root = Path('SalahZeit/Views/RootTabView.swift')
r = root.read_text(encoding='utf-8')
r = r.replace('''                        ZStack {
                            if selection == index {
                                Circle()
                                    .fill(SalahTheme.teal.opacity(0.10))
                                    .frame(width: 24, height: 24)
                            }
                            Image(systemName: item.0)
                                .font(.system(size: 13.5, weight: selection == index ? .semibold : .regular))
                                .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                        }
                        .frame(height: 18)
''',
'''                        Image(systemName: item.0)
                            .font(.system(size: selection == index ? 14.2 : 13.2, weight: selection == index ? .semibold : .regular))
                            .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                            .frame(height: 18)
''', 1)
r = r.replace('("book.closed.fill", "Kur'an")', '("book.fill", "Kur'an")', 1)
r = r.replace('("building.columns.fill", "Namaz")', '("figure.mind.and.body", "Namaz")', 1)
r = r.replace('("safari.fill", "Keşfet")', '("location.north.circle", "Keşfet")', 1)
r = r.replace('("person.crop.circle.fill", "Profil")', '("person.crop.circle", "Profil")', 1)
root.write_text(r, encoding='utf-8')

b = Path('scripts/build_unsigned_ipa.sh')
t = b.read_text(encoding='utf-8')
t = t.replace('MARKETING_VERSION="3.38"', 'MARKETING_VERSION="3.39"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="43"', 'CURRENT_PROJECT_VERSION="44"', 1)
b.write_text(t, encoding='utf-8')

print('SalahPath v3.39 hero atmosphere, glyphs and bottom-nav parity applied')
