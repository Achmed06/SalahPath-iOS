from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = '''    private func head(_ context: inout GraphicsContext, center: CGPoint, radius: CGFloat) {
        let rect = CGRect(x: center.x - radius, y: center.y - radius, width: radius * 2, height: radius * 2)
        context.fill(Path(ellipseIn: rect), with: .color(Color.white.opacity(0.96)))
        context.stroke(Path(ellipseIn: rect), with: .color(SalahTheme.deepTeal), lineWidth: 5)

        if female {
            let hood = CGRect(x: center.x - radius * 1.22, y: center.y - radius * 1.22, width: radius * 2.44, height: radius * 2.62)
            context.stroke(Path(ellipseIn: hood), with: .color(SalahTheme.teal), lineWidth: 7)
        } else {
            var cap = Path()
            cap.move(to: CGPoint(x: center.x - radius * 0.72, y: center.y - radius * 0.76))
            cap.addLine(to: CGPoint(x: center.x + radius * 0.72, y: center.y - radius * 0.76))
            context.stroke(cap, with: .color(SalahTheme.gold), style: StrokeStyle(lineWidth: 6, lineCap: .round))
        }
    }
'''
new = '''    private func head(_ context: inout GraphicsContext, center: CGPoint, radius: CGFloat) {
        let rect = CGRect(x: center.x - radius, y: center.y - radius, width: radius * 2, height: radius * 2)
        context.fill(Path(ellipseIn: rect), with: .color(Color(red: 0.86, green: 0.68, blue: 0.52)))
        context.stroke(Path(ellipseIn: rect), with: .color(SalahTheme.deepTeal), lineWidth: 5)

        if female {
            let hood = CGRect(x: center.x - radius * 1.22, y: center.y - radius * 1.22, width: radius * 2.44, height: radius * 2.62)
            context.stroke(Path(ellipseIn: hood), with: .color(SalahTheme.teal), lineWidth: 7)
        } else {
            var cap = Path()
            cap.move(to: CGPoint(x: center.x - radius * 0.72, y: center.y - radius * 0.76))
            cap.addLine(to: CGPoint(x: center.x + radius * 0.72, y: center.y - radius * 0.76))
            context.stroke(cap, with: .color(SalahTheme.gold), style: StrokeStyle(lineWidth: 6, lineCap: .round))
        }

        drawFace(&context, center: center, radius: radius)
    }

    private func drawFace(_ context: inout GraphicsContext, center: CGPoint, radius: CGFloat) {
        let turn: CGFloat
        if pose == "salam_right" {
            turn = 0.22
        } else if pose == "salam_left" {
            turn = -0.22
        } else {
            turn = 0
        }

        let downward = pose == "bowing" || pose == "sujud"
        let featureY = center.y + (downward ? radius * 0.10 : 0)
        let featureX = center.x + radius * turn
        let eyeGap = radius * 0.34
        let eyeWidth = max(radius * 0.22, 3)
        let ink = SalahTheme.deepTeal

        for direction in [-1.0, 1.0] {
            let x = featureX + eyeGap * CGFloat(direction)
            var eye = Path()
            eye.move(to: CGPoint(x: x - eyeWidth / 2, y: featureY - radius * 0.12))
            eye.addQuadCurve(
                to: CGPoint(x: x + eyeWidth / 2, y: featureY - radius * 0.12),
                control: CGPoint(x: x, y: featureY - radius * (downward ? 0.04 : 0.16))
            )
            context.stroke(eye, with: .color(ink), style: StrokeStyle(lineWidth: max(radius * 0.07, 1.4), lineCap: .round))
        }

        var nose = Path()
        nose.move(to: CGPoint(x: featureX, y: featureY - radius * 0.02))
        nose.addLine(to: CGPoint(x: featureX + radius * 0.05 * (turn == 0 ? 1 : turn.sign == .plus ? 1 : -1), y: featureY + radius * 0.16))
        context.stroke(nose, with: .color(ink.opacity(0.72)), style: StrokeStyle(lineWidth: max(radius * 0.055, 1.1), lineCap: .round))

        var mouth = Path()
        mouth.move(to: CGPoint(x: featureX - radius * 0.20, y: featureY + radius * 0.31))
        mouth.addQuadCurve(
            to: CGPoint(x: featureX + radius * 0.20, y: featureY + radius * 0.31),
            control: CGPoint(x: featureX, y: featureY + radius * 0.37)
        )
        context.stroke(mouth, with: .color(ink), style: StrokeStyle(lineWidth: max(radius * 0.055, 1.1), lineCap: .round))

        if !female {
            var beard = Path()
            beard.move(to: CGPoint(x: featureX - radius * 0.50, y: featureY + radius * 0.30))
            beard.addQuadCurve(
                to: CGPoint(x: featureX + radius * 0.50, y: featureY + radius * 0.30),
                control: CGPoint(x: featureX, y: featureY + radius * 0.82)
            )
            context.stroke(beard, with: .color(ink.opacity(0.92)), style: StrokeStyle(lineWidth: max(radius * 0.12, 2.0), lineCap: .round))
        }
    }
'''
if old not in text:
    raise SystemExit("v400: prayer head artwork anchor missing")
guide.write_text(text.replace(old, new, 1), encoding="utf-8")
print("v400 applied: simple respectful facial features for prayer artwork")
