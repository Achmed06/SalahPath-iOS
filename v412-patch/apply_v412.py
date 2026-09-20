from pathlib import Path

root = Path("SalahZeit/Views/RootTabView.swift")
text = root.read_text(encoding="utf-8")

old_tile = '''            ZStack {
                Circle()
                    .fill(SalahTheme.softTeal)
                    .frame(width: 42, height: 42)
                Image(systemName: icon)
                    .font(.system(size: 20, weight: .semibold))
                    .foregroundStyle(SalahTheme.teal)
            }
'''
new_tile = '''            salahFeatureIcon(icon, size: 44)
'''
if old_tile not in text:
    raise SystemExit("v412: discover tile icon anchor missing")
text = text.replace(old_tile, new_tile, 1)

old_row = '''            Image(systemName: icon)
                .font(.system(size: 17, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 32, height: 32)
                .background(SalahTheme.softTeal, in: Circle())
'''
new_row = '''            salahFeatureIcon(icon, size: 34)
'''
if old_row not in text:
    raise SystemExit("v412: discover row icon anchor missing")
text = text.replace(old_row, new_row, 1)

marker = '''    private func discoverTile(icon: String, title: String, subtitle: String) -> some View {
'''
helper = r'''    @ViewBuilder
    private func salahFeatureIcon(_ symbol: String, size: CGFloat) -> some View {
        ZStack {
            RoundedRectangle(cornerRadius: size * 0.28, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [SalahTheme.softTeal, SalahTheme.cream],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: size, height: size)

            RoundedRectangle(cornerRadius: size * 0.28, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.52), lineWidth: 1)
                .frame(width: size, height: size)

            Circle()
                .fill(Color.white.opacity(0.64))
                .frame(width: size * 0.66, height: size * 0.66)

            Image(systemName: symbol)
                .symbolRenderingMode(.hierarchical)
                .font(.system(size: size * 0.43, weight: .semibold))
                .foregroundStyle(SalahTheme.deepTeal)

            Circle()
                .fill(SalahTheme.gold)
                .frame(width: max(5, size * 0.14), height: max(5, size * 0.14))
                .overlay {
                    Circle().stroke(Color.white.opacity(0.90), lineWidth: 1)
                }
                .offset(x: size * 0.31, y: -size * 0.31)
        }
        .accessibilityHidden(true)
    }

'''
if marker not in text:
    raise SystemExit("v412: discoverTile function marker missing")
text = text.replace(marker, helper + marker, 1)

root.write_text(text, encoding="utf-8")
print("v412 applied: unified SalahPath duotone feature icon system")
