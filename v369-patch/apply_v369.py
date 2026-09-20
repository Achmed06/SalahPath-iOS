from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''        torso(&context, shoulder: shoulder, hip: hip, width: female ? 38 : 34)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.072)
        line(&context, point(c - footSpread, 0.67, in: size), leftFoot, width: 14)
        line(&context, point(c + footSpread, 0.67, in: size), rightFoot, width: 14)

        switch mode {
'''
new = '''        torso(&context, shoulder: shoulder, hip: hip, width: female ? 38 : 34)

        if !female {
            var robe = Path()
            robe.move(to: point(c - 0.095, 0.34, in: size))
            robe.addLine(to: point(c + 0.095, 0.34, in: size))
            robe.addLine(to: point(c + 0.075, 0.83, in: size))
            robe.addLine(to: point(c - 0.075, 0.83, in: size))
            robe.closeSubpath()
            context.fill(robe, with: .color(SalahTheme.teal.opacity(0.96)))
        }

        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.072)
        let legTop: CGFloat = female ? 0.67 : 0.81
        line(&context, point(c - footSpread, legTop, in: size), leftFoot, width: 14)
        line(&context, point(c + footSpread, legTop, in: size), rightFoot, width: 14)

        switch mode {
'''
if old not in s:
    raise SystemExit("v3.69: prayer standing body anchor missing")
s = s.replace(old, new, 1)

old = '''                referenceLearnFeature(
                    turkish: "Görsel & video destekli",
                    german: "Mit Bildern & Videos"
                )
'''
new = '''                referenceLearnFeature(
                    turkish: "Görsel ve okunan metinlerle",
                    german: "Mit Bildern und gesprochenem Text"
                )
'''
if old not in s:
    raise SystemExit("v3.69: unsupported video-copy anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.69 prayer standing artwork + truthful guide copy applied")
