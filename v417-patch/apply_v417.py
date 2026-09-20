from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = '''    private func faceVisual(highlightY: CGFloat, dropsY: CGFloat, largeHighlight: Bool = false) -> some View {
        ZStack {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 142, weight: .regular))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.86))
            Ellipse()
                .fill(SalahTheme.gold.opacity(0.50))
                .frame(width: largeHighlight ? 76 : 42, height: largeHighlight ? 84 : 25)
                .offset(y: highlightY)
            HStack(spacing: 5) {
                drop(size: 14); drop(size: 18); drop(size: 14)
            }
            .offset(x: 71, y: dropsY)
        }
    }

    private func armVisual(mirrored: Bool) -> some View {
'''
new = '''    private func faceVisual(highlightY: CGFloat, dropsY: CGFloat, largeHighlight: Bool = false) -> some View {
        ZStack {
            neutralFace

            Ellipse()
                .fill(SalahTheme.gold.opacity(largeHighlight ? 0.16 : 0.24))
                .overlay {
                    Ellipse()
                        .stroke(SalahTheme.gold.opacity(0.90), lineWidth: largeHighlight ? 4 : 3)
                }
                .frame(
                    width: largeHighlight ? 118 : 58,
                    height: largeHighlight ? 128 : 34
                )
                .offset(y: highlightY)

            HStack(spacing: 5) {
                drop(size: 14)
                drop(size: 18)
                drop(size: 14)
            }
            .offset(x: 76, y: dropsY)
        }
    }

    private var neutralFace: some View {
        ZStack {
            Circle()
                .fill(Color(red: 0.86, green: 0.68, blue: 0.52))
                .frame(width: 132, height: 132)
                .overlay {
                    Circle()
                        .stroke(SalahTheme.deepTeal, lineWidth: 5)
                }

            Capsule()
                .fill(SalahTheme.deepTeal)
                .frame(width: 72, height: 9)
                .offset(y: -52)

            HStack(spacing: 34) {
                Capsule()
                    .fill(SalahTheme.deepTeal)
                    .frame(width: 18, height: 5)
                Capsule()
                    .fill(SalahTheme.deepTeal)
                    .frame(width: 18, height: 5)
            }
            .offset(y: -16)

            Capsule()
                .fill(SalahTheme.deepTeal.opacity(0.78))
                .frame(width: 5, height: 19)
                .offset(y: 4)

            Capsule()
                .fill(SalahTheme.deepTeal)
                .frame(width: 31, height: 5)
                .offset(y: 30)
        }
    }

    private func armVisual(mirrored: Bool) -> some View {
'''
if old not in text:
    raise SystemExit("v417: Wudu face visual anchor missing")
text = text.replace(old, new, 1)

old = '''    private var headVisual: some View {
        ZStack {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 142))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.86))
            Capsule()
                .fill(SalahTheme.gold.opacity(0.68))
                .frame(width: 90, height: 22)
                .offset(y: -48)
            HStack(spacing: 8) { drop(size: 14); drop(size: 18); drop(size: 14) }
                .offset(x: 70, y: -47)
        }
    }

    private var earsVisual: some View {
        ZStack {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 142))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.86))
            HStack(spacing: 92) {
                Circle().fill(SalahTheme.gold.opacity(0.70)).frame(width: 24, height: 42)
                Circle().fill(SalahTheme.gold.opacity(0.70)).frame(width: 24, height: 42)
            }
            HStack(spacing: 118) { drop(size: 16); drop(size: 16) }
                .offset(y: -4)
        }
    }

    private var neckVisual: some View {
        ZStack {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 142))
                .foregroundStyle(SalahTheme.deepTeal.opacity(0.86))
            Capsule()
                .fill(SalahTheme.gold.opacity(0.70))
                .frame(width: 72, height: 20)
                .offset(y: 65)
            HStack(spacing: 74) {
                Image(systemName: "hand.raised.fill")
                Image(systemName: "hand.raised.fill").scaleEffect(x: -1, y: 1)
            }
            .font(.system(size: 34))
            .foregroundStyle(SalahTheme.teal)
            .offset(y: 54)
        }
    }
'''
new = '''    private var headVisual: some View {
        ZStack {
            neutralFace

            Capsule()
                .fill(SalahTheme.gold.opacity(0.70))
                .frame(width: 92, height: 20)
                .offset(y: -53)

            HStack(spacing: 8) {
                drop(size: 14)
                drop(size: 18)
                drop(size: 14)
            }
            .offset(x: 76, y: -50)
        }
    }

    private var earsVisual: some View {
        ZStack {
            neutralFace

            HStack(spacing: 106) {
                Capsule()
                    .fill(SalahTheme.gold.opacity(0.72))
                    .frame(width: 20, height: 40)
                Capsule()
                    .fill(SalahTheme.gold.opacity(0.72))
                    .frame(width: 20, height: 40)
            }

            HStack(spacing: 124) {
                drop(size: 16)
                drop(size: 16)
            }
            .offset(y: -2)
        }
    }

    private var neckVisual: some View {
        ZStack {
            neutralFace
                .offset(y: -10)

            HStack(spacing: 38) {
                Capsule()
                    .fill(SalahTheme.gold.opacity(0.74))
                    .frame(width: 30, height: 11)
                    .rotationEffect(.degrees(18))
                Capsule()
                    .fill(SalahTheme.gold.opacity(0.74))
                    .frame(width: 30, height: 11)
                    .rotationEffect(.degrees(-18))
            }
            .offset(y: 57)

            HStack(spacing: 74) {
                Image(systemName: "hand.raised.fill")
                Image(systemName: "hand.raised.fill")
                    .scaleEffect(x: -1, y: 1)
            }
            .font(.system(size: 33))
            .foregroundStyle(SalahTheme.teal)
            .offset(y: 55)
        }
    }
'''
if old not in text:
    raise SystemExit("v417: Wudu head/ears/neck visual anchor missing")
text = text.replace(old, new, 1)

old = '''struct WuduGuideView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var currentStepIndex = 0
    @State private var showExactDetail = true

    private let steps: [WuduTutorialStep] = [
'''
new = '''struct WuduGuideView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var currentStepIndex: Int
    @State private var showExactDetail = true

    init(initialStepIndex: Int = 0) {
        _currentStepIndex = State(initialValue: min(max(initialStepIndex, 0), 12))
    }

    private let steps: [WuduTutorialStep] = [
'''
if old not in text:
    raise SystemExit("v417: WuduGuideView initialization anchor missing")
text = text.replace(old, new, 1)

guide.write_text(text, encoding="utf-8")

app = Path("SalahZeit/SalahZeitApp.swift")
app_text = app.read_text(encoding="utf-8")

anchor = '''        case "wudu":
            NavigationStack { WuduGuideView() }
'''
if anchor not in app_text:
    raise SystemExit("v417: Wudu QA route anchor missing")

routes = anchor + ''.join(
    f'''        case "wudu-step-{i}":
            NavigationStack {{ WuduGuideView(initialStepIndex: {i-1}) }}
'''
    for i in range(1, 14)
)
app.write_text(app_text.replace(anchor, routes, 1), encoding="utf-8")

print("v417 applied: clearer frontal Wudu face artwork + QA routes for all 13 steps")
