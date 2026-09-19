from pathlib import Path

# SalahPath v3.48 — side-phone reference parity pass.
# 1) deterministic back/bell toolbar in direct QA routes,
# 2) Quran top card matches the poster without the extra Al-Fatiha metadata row,
# 3) Namaz hero uses seated prayer posture + prayer-rug treatment.

# --- Direct QA toolbar parity ---
app = Path("SalahZeit/SalahZeitApp.swift")
sa = app.read_text(encoding="utf-8")

routes = {
'''        case "quran":
            NavigationStack { QuranView() }
''':
'''        case "quran":
            NavigationStack {
                QuranView()
                    .toolbar { referenceQAToolbar }
            }
''',
'''        case "dhikr":
            NavigationStack { DhikrView() }
''':
'''        case "dhikr":
            NavigationStack {
                DhikrView()
                    .toolbar { referenceQAToolbar }
            }
''',
'''        case "namaz":
            NavigationStack { GuideView() }
''':
'''        case "namaz":
            NavigationStack {
                GuideView()
                    .toolbar { referenceQAToolbar }
            }
''',
'''        case "times":
            NavigationStack { PrayerTimesOverviewView() }
''':
'''        case "times":
            NavigationStack {
                PrayerTimesOverviewView()
                    .toolbar { referenceQAToolbar }
            }
'''
}
for old, new in routes.items():
    if old not in sa:
        raise SystemExit(f"v3.48: QA route not found: {old.splitlines()[0]}")
    sa = sa.replace(old, new, 1)

needle = '''    @ViewBuilder
    private var qaRoot: some View {
'''
insert = '''    @ToolbarContentBuilder
    private var referenceQAToolbar: some ToolbarContent {
        ToolbarItem(placement: .topBarLeading) {
            Image(systemName: "chevron.left")
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(.white)
        }
        ToolbarItem(placement: .topBarTrailing) {
            Image(systemName: "bell.fill")
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(.white)
        }
    }

    @ViewBuilder
    private var qaRoot: some View {
'''
if needle not in sa:
    raise SystemExit("v3.48: qaRoot insertion point missing")
sa = sa.replace(needle, insert, 1)
app.write_text(sa, encoding="utf-8")

# --- Quran + Namaz content parity ---
p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

q_start = s.index("struct QuranView: View {")
q_end = s.index("\nprivate struct QuranFavoritesView", q_start)
q = s[q_start:q_end]

extra_header = '''                            HStack(alignment: .center) {
                                VStack(alignment: .leading, spacing: 1) {
                                    Text("Al-Fātiḥa")
                                        .font(.system(size: 14, weight: .bold, design: .serif))
                                        .foregroundStyle(SalahTheme.ink)
                                    Text(settings.t("Die Eröffnende · 7 Verse", "Fâtiha · 7 ayet"))
                                        .font(.system(size: 8.5, weight: .semibold))
                                        .foregroundStyle(SalahTheme.mutedInk)
                                }
                                Spacer()
                                Text("الفاتحة")
                                    .font(.system(size: 20, weight: .medium))
                                    .foregroundStyle(SalahTheme.ink)
                            }

                            Divider().overlay(SalahTheme.gold.opacity(0.35))

'''
if extra_header not in q:
    raise SystemExit("v3.48: Quran metadata header not found")
q = q.replace(extra_header, "", 1)

# The reference action strip uses outlined, lighter glyphs.
q = q.replace('quranAction(icon: "text.book.closed.fill", title: settings.t("Verse", "Ayetler"))',
              'quranAction(icon: "square.and.pencil", title: settings.t("Verse", "Ayetler"))', 1)
q = q.replace('quranAction(icon: "play.circle.fill", title: settings.t("Hören", "Dinle"))',
              'quranAction(icon: "play.circle", title: settings.t("Hören", "Dinle"))', 1)
q = q.replace('quranAction(icon: "heart.fill", title: settings.t("Favorit", "Favori"))',
              'quranAction(icon: "heart", title: settings.t("Favorit", "Favori"))', 1)
q = q.replace('quranAction(icon: "square.and.arrow.up", title: settings.t("Teilen", "Paylaş"))',
              'quranAction(icon: "star", title: settings.t("Teilen", "Paylaş"))', 1)

# Slightly more breathing room in the Quran reference card after removing metadata.
q = q.replace('VStack(alignment: .leading, spacing: 9) {',
              'VStack(alignment: .leading, spacing: 12) {', 1)
q = q.replace('.padding(10)\n                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 9, style: .continuous))',
              '.padding(.horizontal, 12)\n                        .padding(.vertical, 14)\n                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 9, style: .continuous))', 1)

s = s[:q_start] + q + s[q_end:]

# Namaz hero: current v3.47 uses standing intention images, while the reference
# clearly shows both people seated in prayer on rugs.
old_male = '''                        Image("male_intention")
                            .resizable()
                            .scaledToFit()
                            .frame(height: 150)
                            .opacity(settings.prayerAudience == .male ? 1 : 0.52)
'''
new_male = '''                        ZStack(alignment: .bottom) {
                            RoundedRectangle(cornerRadius: 5, style: .continuous)
                                .fill(SalahTheme.teal.opacity(0.18))
                                .frame(width: 118, height: 48)
                                .overlay {
                                    RoundedRectangle(cornerRadius: 5, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.28), lineWidth: 0.8)
                                }
                            Image("male_sitting")
                                .resizable()
                                .scaledToFit()
                                .frame(height: 118)
                                .padding(.bottom, 7)
                        }
                        .frame(height: 150, alignment: .bottom)
                        .opacity(settings.prayerAudience == .male ? 1 : 0.52)
'''
if old_male not in s:
    raise SystemExit("v3.48: male Namaz hero image not found")
s = s.replace(old_male, new_male, 1)

old_female = '''                        Image("female_intention")
                            .resizable()
                            .scaledToFit()
                            .frame(height: 150)
                            .opacity(settings.prayerAudience == .female ? 1 : 0.52)
'''
new_female = '''                        ZStack(alignment: .bottom) {
                            RoundedRectangle(cornerRadius: 5, style: .continuous)
                                .fill(SalahTheme.teal.opacity(0.18))
                                .frame(width: 118, height: 48)
                                .overlay {
                                    RoundedRectangle(cornerRadius: 5, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.28), lineWidth: 0.8)
                                }
                            Image("female_sitting")
                                .resizable()
                                .scaledToFit()
                                .frame(height: 118)
                                .padding(.bottom, 7)
                        }
                        .frame(height: 150, alignment: .bottom)
                        .opacity(settings.prayerAudience == .female ? 1 : 0.52)
'''
if old_female not in s:
    raise SystemExit("v3.48: female Namaz hero image not found")
s = s.replace(old_female, new_female, 1)

p.write_text(s, encoding="utf-8")

# --- Version ---
b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.47"' not in t or 'CURRENT_PROJECT_VERSION="52"' not in t:
    raise SystemExit("v3.48: expected v3.47/52 build version not found")
t = t.replace('MARKETING_VERSION="3.47"', 'MARKETING_VERSION="3.48"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="52"', 'CURRENT_PROJECT_VERSION="53"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.48 side-phone reference parity applied")
