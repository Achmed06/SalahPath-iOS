from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''        if !female {
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
new = '''        if !female {
            var robe = Path()
            robe.move(to: point(c - 0.095, 0.34, in: size))
            robe.addLine(to: point(c + 0.095, 0.34, in: size))
            robe.addLine(to: point(c + 0.105, 0.89, in: size))
            robe.addQuadCurve(
                to: point(c - 0.105, 0.89, in: size),
                control: point(c, 0.915, in: size)
            )
            robe.closeSubpath()
            context.fill(robe, with: .color(SalahTheme.teal.opacity(0.96)))
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
            context.fill(Path(roundedRect: leftRect, cornerRadius: footHeight / 2), with: .color(SalahTheme.deepTeal))
            context.fill(Path(roundedRect: rightRect, cornerRadius: footHeight / 2), with: .color(SalahTheme.deepTeal))
        }

        switch mode {
'''
if old not in s:
    raise SystemExit("v3.70: male standing silhouette anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.70 straight male standing silhouette applied")
