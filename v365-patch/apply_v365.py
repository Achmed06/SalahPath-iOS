from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''        let leftFoot = point(c - (female ? 0.055 : 0.075), 0.91, in: size)
        let rightFoot = point(c + (female ? 0.055 : 0.075), 0.91, in: size)

        torso(&context, shoulder: shoulder, hip: hip, width: female ? 38 : 32)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.072)
        line(&context, point(c - 0.04, 0.67, in: size), leftFoot, width: 13)
        line(&context, point(c + 0.04, 0.67, in: size), rightFoot, width: 13)
'''
new = '''        let footSpread: CGFloat = female ? 0.035 : 0.045
        let leftFoot = point(c - footSpread, 0.91, in: size)
        let rightFoot = point(c + footSpread, 0.91, in: size)

        torso(&context, shoulder: shoulder, hip: hip, width: female ? 38 : 34)
        head(&context, center: headCenter, radius: min(size.width, size.height) * 0.072)
        line(&context, point(c - footSpread, 0.67, in: size), leftFoot, width: 14)
        line(&context, point(c + footSpread, 0.67, in: size), rightFoot, width: 14)
'''
if old not in s:
    raise SystemExit("v3.65: standing legs anchor missing")
s = s.replace(old, new, 1)

old = '''        case .intention, .relaxed:
            line(&context, leftShoulder, point(c - 0.12, 0.64, in: size), width: 10)
            line(&context, rightShoulder, point(c + 0.12, 0.64, in: size), width: 10)
            if mode == .intention {
                let heartRect = CGRect(x: size.width * c - 8, y: size.height * 0.43 - 8, width: 16, height: 16)
                context.fill(Path(ellipseIn: heartRect), with: .color(SalahTheme.gold))
            }
'''
new = '''        case .intention, .relaxed:
            let handY: CGFloat = 0.64
            line(&context, leftShoulder, point(c - 0.10, handY, in: size), width: 10)
            line(&context, rightShoulder, point(c + 0.10, handY, in: size), width: 10)
'''
if old not in s:
    raise SystemExit("v3.65: intention arms anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.65 prayer standing pose refinement applied")
