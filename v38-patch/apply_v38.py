from pathlib import Path


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"v3.8 expected block not found: {label}")
    return text.replace(old, new, 1)

# ---------- Fixed reference palette + Home redesign ----------
p = Path('SalahZeit/Views/HomeView.swift')
s = p.read_text(encoding='utf-8')

old_theme = '''enum SalahTheme {
    static let teal = Color(red: 0.015, green: 0.34, blue: 0.32)
    static let deepTeal = Color(red: 0.012, green: 0.22, blue: 0.22)
    static let gold = Color(red: 0.78, green: 0.61, blue: 0.25)
    static let cream = Color(uiColor: UIColor { traits in
        traits.userInterfaceStyle == .dark
            ? UIColor(red: 0.10, green: 0.15, blue: 0.15, alpha: 1)
            : UIColor(red: 0.985, green: 0.965, blue: 0.89, alpha: 1)
    })
    static let page = Color(uiColor: UIColor { traits in
        traits.userInterfaceStyle == .dark
            ? UIColor(red: 0.035, green: 0.075, blue: 0.075, alpha: 1)
            : UIColor(red: 0.945, green: 0.93, blue: 0.84, alpha: 1)
    })
    static let ink = Color(uiColor: UIColor { traits in
        traits.userInterfaceStyle == .dark ? .white : UIColor(red: 0.04, green: 0.14, blue: 0.17, alpha: 1)
    })

    static func cardStroke(_ opacity: Double = 0.34) -> Color { gold.opacity(opacity) }
}'''
new_theme = '''enum SalahTheme {
    // SalahPath reference palette: deliberately stable in iOS light/dark settings.
    static let teal = Color(red: 0.015, green: 0.36, blue: 0.33)
    static let deepTeal = Color(red: 0.012, green: 0.25, blue: 0.25)
    static let gold = Color(red: 0.80, green: 0.62, blue: 0.25)
    static let cream = Color(red: 0.992, green: 0.973, blue: 0.905)
    static let page = Color(red: 0.958, green: 0.939, blue: 0.856)
    static let ink = Color(red: 0.035, green: 0.14, blue: 0.17)
    static let mutedInk = Color(red: 0.27, green: 0.34, blue: 0.34)
    static let softTeal = Color(red: 0.91, green: 0.955, blue: 0.93)

    static func cardStroke(_ opacity: Double = 0.34) -> Color { gold.opacity(opacity) }
}'''
s = replace_once(s, old_theme, new_theme, 'theme')

start = s.index('    private var brandHeader: some View {')
end = s.index('\n    private func nextPrayerHero', start)
new_header = '''    private var brandHeader: some View {
        HStack(alignment: .center, spacing: 10) {
            ZStack {
                RoundedRectangle(cornerRadius: 14)
                    .fill(SalahTheme.gold.opacity(0.18))
                    .frame(width: 44, height: 44)
                Image(systemName: "leaf.fill")
                    .font(.title3.bold())
                    .foregroundStyle(SalahTheme.gold)
            }

            VStack(alignment: .leading, spacing: 1) {
                Text("SalahPath")
                    .font(.system(size: 24, weight: .bold, design: .serif))
                    .foregroundStyle(.white)
                    .fixedSize(horizontal: true, vertical: false)
                    .layoutPriority(2)
                Text(settings.t("Glaube. Wissen. Praxis.", "İman. İlim. İbadet."))
                    .font(.caption2.weight(.medium))
                    .foregroundStyle(.white.opacity(0.78))
                    .lineLimit(1)
            }

            Spacer(minLength: 6)

            VStack(alignment: .trailing, spacing: 2) {
                HStack(spacing: 5) {
                    Image(systemName: settings.notificationsEnabled ? "bell.fill" : "bell.slash")
                        .foregroundStyle(settings.notificationsEnabled ? SalahTheme.gold : .white.opacity(0.65))
                    Text(locationManager.locality ?? settings.t("Standort", "Konum"))
                        .font(.caption.bold())
                        .lineLimit(1)
                        .minimumScaleFactor(0.72)
                        .layoutPriority(1)
                }
                Text(hijriDateString(now, language: settings.language))
                    .font(.caption2)
                    .foregroundStyle(.white.opacity(0.80))
                    .lineLimit(1)
            }
            .frame(maxWidth: 145, alignment: .trailing)
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 12)
        .background(
            LinearGradient(colors: [SalahTheme.deepTeal, SalahTheme.teal], startPoint: .leading, endPoint: .trailing),
            in: RoundedRectangle(cornerRadius: 20)
        )
        .overlay { RoundedRectangle(cornerRadius: 20).stroke(SalahTheme.gold.opacity(0.72), lineWidth: 1.2) }
        .accessibilityElement(children: .contain)
    }
'''
s = s[:start] + new_header + s[end:]

start = s.index('    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {')
end = s.index('\n    private var prayerLegendCard', start)
new_hero = '''    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Label(settings.t("Nächstes Gebet", "Sıradaki namaz"), systemImage: prayer.kind.systemImage)
                    .font(.caption.bold())
                    .textCase(.uppercase)
                Spacer()
                Text(gregorianDateShort(now)).font(.caption)
            }
            .foregroundStyle(SalahTheme.teal)

            HStack(alignment: .bottom, spacing: 12) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(prayer.kind.localizedName(settings.language))
                        .font(.system(size: 31, weight: .bold, design: .rounded))
                        .foregroundStyle(SalahTheme.ink)
                    Text(settings.t("in", "kalan"))
                        .font(.caption)
                        .foregroundStyle(SalahTheme.mutedInk)
                    Text(countdownString(from: now, to: prayer.date))
                        .font(.system(size: 34, weight: .bold, design: .rounded).monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
                        .minimumScaleFactor(0.75)
                        .lineLimit(1)
                }
                Spacer(minLength: 8)
                VStack(alignment: .trailing, spacing: 3) {
                    Text(settings.t("Beginn", "Vakit"))
                        .font(.caption)
                        .foregroundStyle(SalahTheme.mutedInk)
                    Text(timeString(prayer.date, use24Hour: settings.use24Hour))
                        .font(.title.bold().monospacedDigit())
                        .foregroundStyle(SalahTheme.ink)
                }
            }

            VStack(alignment: .leading, spacing: 5) {
                Text(prayer.kind.fullSequence(settings.language))
                    .font(.subheadline.bold())
                    .foregroundStyle(SalahTheme.ink)
                Text(prayer.kind.detailNote(settings.language))
                    .font(.caption)
                    .foregroundStyle(SalahTheme.mutedInk)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(12)
            .background(SalahTheme.softTeal, in: RoundedRectangle(cornerRadius: 14))
            .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.gold.opacity(0.30), lineWidth: 1) }
        }
        .padding(16)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 22))
        .overlay { RoundedRectangle(cornerRadius: 22).stroke(SalahTheme.gold.opacity(0.75), lineWidth: 1.2) }
        .shadow(color: SalahTheme.deepTeal.opacity(0.07), radius: 8, y: 3)
    }
'''
s = s[:start] + new_hero + s[end:]

# strengthen daily dua reference look
s = s.replace('.font(.title2)\n                .multilineTextAlignment(.trailing)', '.font(.system(size: 27, weight: .medium))\n                .multilineTextAlignment(.trailing)', 1)

p.write_text(s, encoding='utf-8')

# ---------- Bottom tab bar: cream, reference-like, no dark slab ----------
p = Path('SalahZeit/Views/RootTabView.swift')
s = p.read_text(encoding='utf-8')
old = '''struct RootTabView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        TabView {'''
new = '''struct RootTabView: View {
    @EnvironmentObject private var settings: SettingsStore

    init() {
        let appearance = UITabBarAppearance()
        appearance.configureWithOpaqueBackground()
        appearance.backgroundColor = UIColor(red: 0.992, green: 0.973, blue: 0.905, alpha: 0.97)
        appearance.shadowColor = UIColor(red: 0.80, green: 0.62, blue: 0.25, alpha: 0.22)
        let normal = UIColor(red: 0.34, green: 0.40, blue: 0.39, alpha: 1)
        let selected = UIColor(red: 0.015, green: 0.36, blue: 0.33, alpha: 1)
        for item in [appearance.stackedLayoutAppearance, appearance.inlineLayoutAppearance, appearance.compactInlineLayoutAppearance] {
            item.normal.iconColor = normal
            item.normal.titleTextAttributes = [.foregroundColor: normal]
            item.selected.iconColor = selected
            item.selected.titleTextAttributes = [.foregroundColor: selected]
        }
        UITabBar.appearance().standardAppearance = appearance
        UITabBar.appearance().scrollEdgeAppearance = appearance
    }

    var body: some View {
        TabView {'''
s = replace_once(s, old, new, 'RootTabView init')
s = s.replace('        .tint(SalahTheme.teal)\n    }\n}', '        .tint(SalahTheme.teal)\n        .preferredColorScheme(.light)\n    }\n}', 1)
p.write_text(s, encoding='utf-8')

# ---------- Wudu: complete sequence incl. neck, separate feet, preparation ----------
p = Path('SalahZeit/Views/GuideView.swift')
s = p.read_text(encoding='utf-8')
start = s.index('    private let steps: [WuduTutorialStep] = [', s.index('struct WuduGuideView'))
end = s.index('\n    ]', start) + len('\n    ]')
new_steps = '''    private let steps: [WuduTutorialStep] = [
        .init(number: 1, image: "wudu_intention", deTitle: "Niyyah / Absicht", trTitle: "Niyet", deAction: "Fasse im Herzen die Absicht, Wudu zu nehmen. In der hanafitischen Lehre ist die Niyyah Sunnah und gehört nicht zu den vier Fard-Bestandteilen.", trAction: "Kalben abdest almaya niyet et. Hanefî mezhebinde niyet sünnettir; abdestin dört farzından biri değildir.", repeatText: nil, hanafiFard: false),
        .init(number: 2, image: "wudu_intention", deTitle: "Basmala", trTitle: "Besmele", deAction: "Beginne mit Bismillāh. Dies gehört zur dargestellten Wudu-Praxis und ist kein eigener Fard-Bestandteil.", trAction: "Bismillâh diyerek başla. Bu, gösterilen abdest uygulamasının bir parçasıdır; ayrı bir farz değildir.", repeatText: nil, hanafiFard: false),
        .init(number: 3, image: "wudu_hands", deTitle: "Hände", trTitle: "Eller", deAction: "Beide Hände bis zu den Handgelenken waschen und die Fingerzwischenräume erreichen.", trAction: "İki eli bileklere kadar yıka ve parmak aralarına su ulaştır.", repeatText: "3×", hanafiFard: false),
        .init(number: 4, image: "wudu_mouth", deTitle: "Mund", trTitle: "Ağız", deAction: "Mit der rechten Hand Wasser in den Mund nehmen und gründlich spülen.", trAction: "Sağ elle ağza su alıp iyice çalkala.", repeatText: "3×", hanafiFard: false),
        .init(number: 5, image: "wudu_nose", deTitle: "Nase", trTitle: "Burun", deAction: "Vorsichtig Wasser in die Nase ziehen und die Nase reinigen.", trAction: "Burnuna nazikçe su verip temizle.", repeatText: "3×", hanafiFard: false),
        .init(number: 6, image: "wudu_face", deTitle: "Gesicht", trTitle: "Yüz", deAction: "Das ganze Gesicht waschen. Einmal vollständig ist Fard; dreimal entspricht der üblichen Sunnah-Praxis.", trAction: "Yüzün tamamını yıka. Bir kez tam yıkamak farzdır; üç kez yıkamak yaygın sünnet uygulamasıdır.", repeatText: "3×", hanafiFard: true),
        .init(number: 7, image: "wudu_rightarm", deTitle: "Rechter Arm", trTitle: "Sağ kol", deAction: "Rechten Arm einschließlich Ellenbogen vollständig waschen.", trAction: "Sağ kolu dirsekle birlikte tamamen yıka.", repeatText: "3×", hanafiFard: true),
        .init(number: 8, image: "wudu_leftarm", deTitle: "Linker Arm", trTitle: "Sol kol", deAction: "Linken Arm einschließlich Ellenbogen vollständig waschen.", trAction: "Sol kolu dirsekle birlikte tamamen yıka.", repeatText: "3×", hanafiFard: true),
        .init(number: 9, image: "wudu_head", deTitle: "Masah des Kopfes", trTitle: "Başın meshi", deAction: "Mit feuchten Händen über den Kopf streichen. Hanafi: Für die Gültigkeit muss mindestens ein Viertel des Kopfes vom Masah erfasst werden; die vollständige Masah wird in dieser Lernreihenfolge einmal gezeigt.", trAction: "Islak ellerle başı mesh et. Hanefî: Geçerlilik için başın en az dörtte biri mesh edilmelidir; bu öğrenme sıralamasında tam baş meshi bir kez gösterilir.", repeatText: "1×", hanafiFard: true),
        .init(number: 10, image: "wudu_ears", deTitle: "Ohren", trTitle: "Kulaklar", deAction: "Mit erneut angefeuchteten Händen die Ohren abwischen: außen mit den Daumen, innen mit Zeige- oder kleinen Fingern. Nicht einer der vier Fard-Bestandteile.", trAction: "Eller tekrar ıslatılarak kulakların dışı başparmakla, içi işaret veya serçe parmakla mesh edilir. Dört farzdan biri değildir.", repeatText: "1×", hanafiFard: false),
        .init(number: 11, image: nil, deTitle: "Nacken / Boyun", trTitle: "Boyun", deAction: "Nach der von Diyanet dargestellten Reihenfolge wird mit den Rückseiten beider feuchten Hände über den Nacken gestrichen. Nicht die Kehle/Vorderseite des Halses wischen. Dieser Schritt ist keiner der vier Fard-Bestandteile.", trAction: "Diyanet'in anlattığı sırada, iki ıslak elin tersiyle boyun mesh edilir. Boğazın ön kısmı mesh edilmez. Bu adım abdestin dört farzından biri değildir.", repeatText: "1×", hanafiFard: false),
        .init(number: 12, image: "wudu_feet", deTitle: "Rechter Fuß", trTitle: "Sağ ayak", deAction: "Rechten Fuß einschließlich Knöchel vollständig waschen und Wasser zwischen die Zehen gelangen lassen.", trAction: "Sağ ayağı topuk ve aşık kemikleriyle birlikte tamamen yıka; parmak aralarına su ulaştır.", repeatText: "3×", hanafiFard: true),
        .init(number: 13, image: "wudu_feet", deTitle: "Linker Fuß", trTitle: "Sol ayak", deAction: "Linken Fuß einschließlich Knöchel vollständig waschen und Wasser zwischen die Zehen gelangen lassen.", trAction: "Sol ayağı topuk ve aşık kemikleriyle birlikte tamamen yıka; parmak aralarına su ulaştır.", repeatText: "3×", hanafiFard: true)
    ]'''
s = s[:start] + new_steps + s[end:]

# preparation card before steps
needle = '''                ForEach(steps) { step in'''
prep = '''                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Text("0").font(.headline.bold()).frame(width: 32, height: 32).background(SalahTheme.gold.opacity(0.22), in: Circle())
                        Text(settings.t("Vorbereitung", "Hazırlık")).font(.title3.bold())
                    }
                    Text(settings.t("Sorge dafür, dass Wasser die zu waschenden Stellen erreicht. Entferne nach Möglichkeit Dinge, die den Wasserkontakt verhindern.", "Suyun yıkanması gereken yerlere ulaşmasını sağla. Suyun temasını engelleyen maddeleri imkân ölçüsünde gider."))
                        .font(.subheadline)
                }.cardStyle()

                ForEach(steps) { step in'''
s = replace_once(s, needle, prep, 'wudu preparation')

# neck step gets a clear diagram, using a native symbol instead of a misleading reused photo
needle2 = '''                        if let image = step.image {
                            Image(image).resizable().scaledToFit().frame(maxWidth:.infinity).frame(maxHeight:220).padding(8).background(SalahTheme.teal.opacity(0.045),in:RoundedRectangle(cornerRadius:16)).accessibilityHidden(true)
                        }
                        Text(settings.language == .german ? step.deAction : step.trAction).font(.subheadline)'''
replace2 = '''                        if let image = step.image {
                            Image(image).resizable().scaledToFit().frame(maxWidth:.infinity).frame(maxHeight:220).padding(8).background(SalahTheme.teal.opacity(0.045),in:RoundedRectangle(cornerRadius:16)).accessibilityHidden(true)
                        } else if step.number == 11 {
                            VStack(spacing: 8) {
                                Image(systemName: "person.crop.circle")
                                    .font(.system(size: 62, weight: .light))
                                    .foregroundStyle(SalahTheme.teal)
                                HStack(spacing: 10) {
                                    Image(systemName: "hand.raised.fill")
                                    Image(systemName: "arrow.left.and.right")
                                    Image(systemName: "hand.raised.fill")
                                }
                                .font(.title2)
                                .foregroundStyle(SalahTheme.gold)
                                Text(settings.t("Handrücken → Nacken, nicht Kehle", "El tersleri → boyun, boğaz önü değil"))
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.ink)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(18)
                            .background(SalahTheme.softTeal, in: RoundedRectangle(cornerRadius: 16))
                            .accessibilityElement(children: .combine)
                        }
                        Text(settings.language == .german ? step.deAction : step.trAction).font(.subheadline)'''
s = replace_once(s, needle2, replace2, 'neck diagram')

# clarify source text and style in wudu cards
s = s.replace('.background(SalahTheme.teal, in: Circle()).foregroundStyle(.white)', '.background(SalahTheme.gold.opacity(0.24), in: Circle()).foregroundStyle(SalahTheme.deepTeal)', 1)

p.write_text(s, encoding='utf-8')

# ---------- Version ----------
p = Path('scripts/build_unsigned_ipa.sh')
s = p.read_text(encoding='utf-8')
s = s.replace('MARKETING_VERSION="3.7"', 'MARKETING_VERSION="3.8"')
s = s.replace('CURRENT_PROJECT_VERSION="12"', 'CURRENT_PROJECT_VERSION="13"')
p.write_text(s, encoding='utf-8')

print('SalahPath v3.8 visual parity + Wudu neck patch applied')