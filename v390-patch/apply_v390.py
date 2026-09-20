from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

replacements = {
    '            case "wudu_feet": feetVisual':
    '''            case "wudu_rightfoot": footVisual(mirrored: false)
            case "wudu_leftfoot": footVisual(mirrored: true)
            case "wudu_feet": footVisual(mirrored: false)''',

    '''    private var feetVisual: some View {
        ZStack {
            HStack(spacing: 20) {
                Capsule().fill(SalahTheme.deepTeal).frame(width: 58, height: 112).rotationEffect(.degrees(-16))
                Capsule().fill(SalahTheme.deepTeal).frame(width: 58, height: 112).rotationEffect(.degrees(16))
            }
            HStack(spacing: 18) { drop(size: 17); drop(size: 24); drop(size: 17) }
                .offset(y: -70)
        }
    }''':
    '''    private func footVisual(mirrored: Bool) -> some View {
        ZStack {
            VStack(spacing: -4) {
                HStack(alignment: .bottom, spacing: 3) {
                    Circle().frame(width: 10, height: 10)
                    Circle().frame(width: 12, height: 12)
                    Circle().frame(width: 14, height: 14)
                    Circle().frame(width: 12, height: 12)
                    Circle().frame(width: 9, height: 9)
                }
                .offset(x: 11)

                Capsule()
                    .frame(width: 66, height: 118)
                    .rotationEffect(.degrees(-11))
            }
            .foregroundStyle(SalahTheme.deepTeal)
            .scaleEffect(x: mirrored ? -1 : 1, y: 1)

            Capsule()
                .fill(SalahTheme.gold.opacity(0.62))
                .frame(width: 54, height: 19)
                .offset(x: mirrored ? 9 : -9, y: 31)
                .rotationEffect(.degrees(mirrored ? 11 : -11))

            HStack(spacing: 10) {
                drop(size: 16)
                drop(size: 22)
                drop(size: 16)
            }
            .offset(x: mirrored ? 45 : -45, y: -58)
        }
    }''',

    '.init(number: 12, image: "wudu_feet", deTitle: "Rechter Fuß", trTitle: "Sağ ayak"':
    '.init(number: 12, image: "wudu_rightfoot", deTitle: "Rechter Fuß", trTitle: "Sağ ayak"',

    '.init(number: 13, image: "wudu_feet", deTitle: "Linker Fuß", trTitle: "Sol ayak"':
    '.init(number: 13, image: "wudu_leftfoot", deTitle: "Linker Fuß", trTitle: "Sol ayak"',

    '''                            VStack(alignment: .leading, spacing: 2) {
                                Text(step.deTitle)
                                    .font(.headline.bold())
                                    .foregroundStyle(.white)
                                Text(step.trTitle)
                                    .font(.caption.weight(.semibold))
                                    .foregroundStyle(.white.opacity(0.82))
                            }''':
    '''                            Text(settings.language == .german ? step.deTitle : step.trTitle)
                                .font(.headline.bold())
                                .foregroundStyle(.white)
                                .fixedSize(horizontal: false, vertical: true)''',

    '                                Text("FARZ")':
    '                                Text(settings.t("FARD", "FARZ"))',

    '''                            VStack(alignment: .leading, spacing: 6) {
                                Label("WAS MACHE ICH?", systemImage: "book.closed.fill")
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.teal)
                                Text(step.deAction)
                                    .font(.subheadline)
                                    .foregroundStyle(SalahTheme.ink)
                            }

                            Divider().overlay(SalahTheme.gold.opacity(0.35))

                            VStack(alignment: .leading, spacing: 6) {
                                Label("NE YAPACAĞIM?", systemImage: "text.bubble.fill")
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.teal)
                                Text(step.trAction)
                                    .font(.subheadline)
                                    .foregroundStyle(SalahTheme.ink)
                            }''':
    '''                            VStack(alignment: .leading, spacing: 6) {
                                Label(settings.t("WAS MACHE ICH?", "NE YAPACAĞIM?"), systemImage: "book.closed.fill")
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.teal)
                                Text(settings.language == .german ? step.deAction : step.trAction)
                                    .font(.subheadline)
                                    .foregroundStyle(SalahTheme.ink)
                                    .fixedSize(horizontal: false, vertical: true)
                            }''',

    '.navigationTitle(settings.t("Abdest / Wudu", "Abdest / Wudu"))':
    '.navigationTitle(settings.t("Wudu", "Abdest"))',
}

for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f"v3.90: Wudu cleanup anchor missing: {old[:90]}")
    s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.90 localized Wudu cards + distinct foot artwork applied")
