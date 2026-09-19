from pathlib import Path

# SalahPath v3.16: central Home + custom bottom navigation parity.

p = Path("SalahZeit/Views/RootTabView.swift")
s = p.read_text(encoding="utf-8")
start = s.index("struct RootTabView: View {")
end = s.index("\nstruct MoreView: View {", start)

new = r'''struct RootTabView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var selection = 0

    init() {
        let navigation = UINavigationBarAppearance()
        navigation.configureWithOpaqueBackground()
        navigation.backgroundColor = UIColor(red: 0.012, green: 0.25, blue: 0.25, alpha: 1)
        navigation.shadowColor = UIColor(red: 0.80, green: 0.62, blue: 0.25, alpha: 0.32)
        navigation.titleTextAttributes = [.foregroundColor: UIColor.white]
        navigation.largeTitleTextAttributes = [.foregroundColor: UIColor.white]
        UINavigationBar.appearance().standardAppearance = navigation
        UINavigationBar.appearance().scrollEdgeAppearance = navigation
        UINavigationBar.appearance().compactAppearance = navigation
        UINavigationBar.appearance().tintColor = UIColor.white
    }

    var body: some View {
        TabView(selection: $selection) {
            NavigationStack { HomeView() }
                .tag(0)

            NavigationStack { QuranView() }
                .tag(1)

            NavigationStack { GuideView() }
                .tag(2)

            NavigationStack { MoreView() }
                .tag(3)

            NavigationStack { SettingsView() }
                .tag(4)
        }
        .toolbar(.hidden, for: .tabBar)
        .safeAreaInset(edge: .bottom, spacing: 0) {
            ReferenceBottomBar(selection: $selection)
                .environmentObject(settings)
        }
        .preferredColorScheme(.light)
        .tint(SalahTheme.teal)
    }
}

private struct ReferenceBottomBar: View {
    @EnvironmentObject private var settings: SettingsStore
    @Binding var selection: Int

    private var items: [(String, String)] {
        [
            ("house.fill", settings.t("Startseite", "Ana Sayfa")),
            ("book.closed.fill", settings.t("Quran", "Kur'an")),
            ("building.columns.fill", settings.t("Namaz", "Namaz")),
            ("safari.fill", settings.t("Entdecken", "Keşfet")),
            ("person.crop.circle.fill", settings.t("Profil", "Profil"))
        ]
    }

    var body: some View {
        HStack(spacing: 0) {
            ForEach(Array(items.enumerated()), id: \.offset) { index, item in
                Button {
                    withAnimation(.easeOut(duration: 0.16)) {
                        selection = index
                    }
                } label: {
                    VStack(spacing: 3) {
                        ZStack {
                            if selection == index {
                                Capsule()
                                    .fill(SalahTheme.teal.opacity(0.10))
                                    .frame(width: 39, height: 24)
                            }
                            Image(systemName: item.0)
                                .font(.system(size: 17, weight: selection == index ? .bold : .semibold))
                                .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                        }
                        .frame(height: 25)

                        Text(item.1)
                            .font(.system(size: 8.1, weight: selection == index ? .bold : .semibold))
                            .foregroundStyle(selection == index ? SalahTheme.teal : SalahTheme.mutedInk)
                            .lineLimit(1)
                            .minimumScaleFactor(0.72)

                        Circle()
                            .fill(selection == index ? SalahTheme.gold : Color.clear)
                            .frame(width: 3.5, height: 3.5)
                    }
                    .frame(maxWidth: .infinity)
                    .contentShape(Rectangle())
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 5)
        .padding(.top, 7)
        .padding(.bottom, 3)
        .background(
            SalahTheme.cream
                .overlay(alignment: .top) {
                    Rectangle()
                        .fill(SalahTheme.gold.opacity(0.42))
                        .frame(height: 0.7)
                }
        )
        .shadow(color: SalahTheme.deepTeal.opacity(0.08), radius: 7, y: -2)
    }
}
'''

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8")

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# Tighten the central phone proportions to the supplied reference.
s = s.replace('.frame(height: 86)', '.frame(height: 76)', 1)
s = s.replace('LazyVStack(spacing: 10)', 'LazyVStack(spacing: 8)', 1)
s = s.replace('.padding(.horizontal, 10)\n            .padding(.top, 6)\n            .padding(.bottom, 18)',
              '.padding(.horizontal, 9)\n            .padding(.top, 5)\n            .padding(.bottom, 10)', 1)

# Header proportions.
s = s.replace('.frame(width: 46, height: 46)', '.frame(width: 41, height: 41)', 1)
s = s.replace('.font(.system(size: 24, weight: .semibold))', '.font(.system(size: 21, weight: .semibold))', 1)
s = s.replace('.font(.system(size: 25, weight: .bold, design: .serif))', '.font(.system(size: 22, weight: .bold, design: .serif))', 1)
s = s.replace('.font(.system(size: 10.5, weight: .semibold))', '.font(.system(size: 9.5, weight: .semibold))', 1)
s = s.replace('.frame(maxWidth: 126, alignment: .trailing)', '.frame(maxWidth: 116, alignment: .trailing)', 1)
s = s.replace('.padding(.horizontal, 14)\n        .padding(.vertical, 12)', '.padding(.horizontal, 12)\n        .padding(.vertical, 9)', 1)
s = s.replace('in: RoundedRectangle(cornerRadius: 20, style: .continuous)', 'in: RoundedRectangle(cornerRadius: 17, style: .continuous)', 1)
s = s.replace('RoundedRectangle(cornerRadius: 20, style: .continuous)', 'RoundedRectangle(cornerRadius: 17, style: .continuous)', 1)

# Hero/card rhythm.
s = s.replace('VStack(alignment: .leading, spacing: 9) {', 'VStack(alignment: .leading, spacing: 7) {', 1)
s = s.replace('.font(.system(size: 31, weight: .medium))', '.font(.system(size: 28, weight: .medium))', 1)
s = s.replace('.font(.system(size: 22, weight: .bold, design: .rounded))', '.font(.system(size: 21, weight: .bold, design: .rounded))', 1)
s = s.replace('.font(.system(size: 31, weight: .bold, design: .rounded).monospacedDigit())',
              '.font(.system(size: 29, weight: .bold, design: .rounded).monospacedDigit())', 1)
s = s.replace('.frame(width: 118, height: 70)', '.frame(width: 108, height: 64)', 1)
s = s.replace('.padding(13)\n        .background(\n            LinearGradient(', '.padding(11)\n        .background(\n            LinearGradient(', 1)

# Dua should visually match the reference's compact middle card.
s = s.replace('.font(.system(size: 27, weight: .medium))', '.font(.system(size: 24, weight: .medium))', 1)
s = s.replace('.padding(12)\n        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 17, style: .continuous))',
              '.padding(10)\n        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))', 1)
s = s.replace('RoundedRectangle(cornerRadius: 17, style: .continuous)\n                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1)',
              'RoundedRectangle(cornerRadius: 15, style: .continuous)\n                .stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1)', 1)

# Tracker compactness.
streak_pos = s.index("private var streakCard")
streak_tail = s.index("private var dailyDeenCard", streak_pos)
chunk = s[streak_pos:streak_tail]
chunk = chunk.replace('.frame(width: 25, height: 25)', '.frame(width: 23, height: 23)')
chunk = chunk.replace('Circle().fill(SalahTheme.teal).frame(width: 25, height: 25)',
                      'Circle().fill(SalahTheme.teal).frame(width: 23, height: 23)')
chunk = chunk.replace('.font(.system(size: 24))', '.font(.system(size: 22))')
chunk = chunk.replace('.font(.system(size: 24, weight: .bold).monospacedDigit())',
                      '.font(.system(size: 22, weight: .bold).monospacedDigit())')
chunk = chunk.replace('.frame(width: 96)', '.frame(width: 90)')
chunk = chunk.replace('.padding(12)', '.padding(10)')
chunk = chunk.replace('RoundedRectangle(cornerRadius: 17, style: .continuous)',
                      'RoundedRectangle(cornerRadius: 15, style: .continuous)')
s = s[:streak_pos] + chunk + s[streak_tail:]

# Exact reference-oriented dashboard labels and two-row grid.
s = s.replace('let columns = Array(repeating: GridItem(.flexible(), spacing: 6), count: 4)',
              'let columns = Array(repeating: GridItem(.flexible(), spacing: 5), count: 4)', 1)
s = s.replace('return LazyVGrid(columns: columns, spacing: 6)', 'return LazyVGrid(columns: columns, spacing: 5)', 1)
s = s.replace('DashboardTile(title: settings.t("Dua & Dhikr", "Dua & Zikir"), subtitle: settings.t("Adhkar", "Ezkâr"), icon: "hands.sparkles.fill")',
              'DashboardTile(title: settings.t("Dua & Dhikr", "Dua & Zikir"), subtitle: settings.t("Dua & Zikir", "Dua & Zikir"), icon: "hands.sparkles.fill")')
s = s.replace('DashboardTile(title: settings.t("Wudu Guide", "Abdest Rehberi"), subtitle: settings.t("Schritt für Schritt", "Adım adım"), icon: "drop.fill")',
              'DashboardTile(title: settings.t("Wudu Guide", "Abdest Rehberi"), subtitle: settings.t("Abdest", "Abdest"), icon: "drop.fill")')
s = s.replace('DashboardTile(title: settings.t("Gebetszeiten", "Namaz Vakitleri"), subtitle: settings.t("Heute & mehr", "Bugün & daha"), icon: "clock.fill")',
              'DashboardTile(title: settings.t("Gebetszeiten", "Namaz Vakitleri"), subtitle: settings.t("Namaz Vakitleri", "Namaz Vakitleri"), icon: "clock.fill")')
s = s.replace('DashboardTile(title: settings.t("Islamisches Wissen", "İslami Bilgiler"), subtitle: settings.t("Begriffe", "Bilgi"), icon: "lightbulb.fill")',
              'DashboardTile(title: settings.t("Islamisches Wissen", "İslami Bilgiler"), subtitle: settings.t("Bilgi", "Bilgi"), icon: "lightbulb.fill")')
s = s.replace('DashboardTile(title: settings.t("Favoriten", "Favorilerim"), subtitle: settings.t("Gespeichert", "Kaydedilenler"), icon: "heart.fill")',
              'DashboardTile(title: settings.t("Favoriten", "Favorilerim"), subtitle: settings.t("Favorilerim", "Favorilerim"), icon: "heart.fill")')

# Tile styling closer to reference: cream, gold border, taller icon.
tile_start = s.index("private struct DashboardTile")
tile_end = s.index("\nprivate struct PrayerRow", tile_start)
tile = s[tile_start:tile_end]
tile = tile.replace('.font(.system(size: 22, weight: .semibold))', '.font(.system(size: 21, weight: .semibold))')
tile = tile.replace('.frame(height: 27)', '.frame(height: 25)')
tile = tile.replace('.font(.system(size: 10.5, weight: .bold))', '.font(.system(size: 9.8, weight: .bold))')
tile = tile.replace('.font(.system(size: 8, weight: .semibold))', '.font(.system(size: 7.5, weight: .semibold))')
tile = tile.replace('.frame(maxWidth: .infinity, minHeight: 78, alignment: .center)',
                    '.frame(maxWidth: .infinity, minHeight: 74, alignment: .center)')
tile = tile.replace('.padding(.vertical, 8)', '.padding(.vertical, 7)')
tile = tile.replace('RoundedRectangle(cornerRadius: 13, style: .continuous)',
                    'RoundedRectangle(cornerRadius: 12, style: .continuous)')
tile = tile.replace('.stroke(SalahTheme.teal.opacity(0.32), lineWidth: 1)',
                    '.stroke(SalahTheme.gold.opacity(0.48), lineWidth: 1)')
s = s[:tile_start] + tile + s[tile_end:]

p.write_text(s, encoding="utf-8")

p = Path("scripts/build_unsigned_ipa.sh")
s = p.read_text(encoding="utf-8")
s = s.replace('MARKETING_VERSION="3.15"', 'MARKETING_VERSION="3.16"')
s = s.replace('CURRENT_PROJECT_VERSION="20"', 'CURRENT_PROJECT_VERSION="21"')
p.write_text(s, encoding="utf-8")

print("SalahPath v3.16 Home + reference bottom navigation patch applied")
