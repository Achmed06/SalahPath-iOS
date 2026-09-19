from pathlib import Path

# SalahPath v3.21: strict Quran + Audio visual parity pass.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

# Quran overview header: add compact title row like the reference phone.
needle = '''                    VStack(spacing: 10) {
                        Picker(settings.t("Sprache", "Dil"), selection: $languageTab) {
'''
replacement = '''                    VStack(spacing: 8) {
                        HStack {
                            HStack(spacing: 7) {
                                Image(systemName: "book.closed.fill")
                                    .font(.system(size: 15, weight: .semibold))
                                    .foregroundStyle(SalahTheme.teal)
                                Text(settings.t("Quran", "Kur'an"))
                                    .font(.system(size: 17, weight: .bold, design: .serif))
                                    .foregroundStyle(SalahTheme.ink)
                            }

                            Spacer()

                            HStack(spacing: 8) {
                                Image(systemName: "bookmark.fill")
                                Image(systemName: "bell.fill")
                            }
                            .font(.system(size: 12, weight: .semibold))
                            .foregroundStyle(SalahTheme.teal)
                        }
                        .padding(.horizontal, 3)

                        Picker(settings.t("Sprache", "Dil"), selection: $languageTab) {
'''
if needle not in s:
    raise SystemExit("Quran overview insertion point not found")
s = s.replace(needle, replacement, 1)

# Reference tab labels are fixed Turkish/German labels.
s = s.replace('Text(settings.t("Arabisch", "Arapça")).tag(0)', 'Text("Arapça").tag(0)', 1)
s = s.replace('Text(settings.t("Türkisch", "Türkçe")).tag(1)', 'Text("Türkçe").tag(1)', 1)

# Add Surah title and ayah metadata above the sample verse.
needle = '''                        VStack(alignment: .leading, spacing: 10) {
                            Text("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ")
'''
replacement = '''                        VStack(alignment: .leading, spacing: 9) {
                            HStack(alignment: .center) {
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

                            Text("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ")
'''
if needle not in s:
    raise SystemExit("Quran sample card insertion point not found")
s = s.replace(needle, replacement, 1)

# Make the sample verse panel a little flatter, like the phone screenshot.
s = s.replace('.padding(12)\n                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 18, style: .continuous))',
              '.padding(11)\n                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))', 1)
s = s.replace('RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.50), lineWidth: 1)',
              'RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.54), lineWidth: 1)', 1)

# Reference player: previous / large play / next centered, speed on the far right.
s = s.replace('HStack(spacing: 22) {', 'HStack(spacing: 18) {', 1)
s = s.replace('Circle().fill(SalahTheme.deepTeal).frame(width: 44, height: 44)',
              'Circle().fill(SalahTheme.deepTeal).frame(width: 46, height: 46)', 1)

# Bottom Quran actions in the reference are an icon strip, not four separate card tiles.
old_action = '''        .frame(maxWidth: .infinity, minHeight: 52)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 13).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
'''
new_action = '''        .frame(maxWidth: .infinity, minHeight: 45)
        .background(Color.clear)
'''
if old_action not in s:
    raise SystemExit("Quran action styling not found")
s = s.replace(old_action, new_action, 1)

# Put all actions on one cream strip, matching the reference's bottom toolbar.
s = s.replace(
'''                        HStack(spacing: 7) {
                            quranAction(icon: "text.book.closed.fill", title: settings.t("Verse", "Ayetler"))
''',
'''                        HStack(spacing: 0) {
                            quranAction(icon: "text.book.closed.fill", title: settings.t("Verse", "Ayetler"))
''', 1)
s = s.replace(
'''                        }

                        HStack(spacing: 8) {
                            Image(systemName: "magnifyingglass")
''',
'''                        }
                        .padding(.horizontal, 5)
                        .padding(.vertical, 2)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 13).stroke(SalahTheme.gold.opacity(0.36), lineWidth: 1) }

                        HStack(spacing: 8) {
                            Image(systemName: "magnifyingglass")
''', 1)

# Quran Surah header: make it look like the same reference player.
surah_start = s.index("    private var headerSection: some View {")
surah_end = s.index("\n    @ViewBuilder\n    private var versesSection", surah_start)
chunk = s[surah_start:surah_end]
chunk = chunk.replace('.font(.system(size: 19, weight: .bold, design: .serif))',
                      '.font(.system(size: 17, weight: .bold, design: .serif))', 1)
chunk = chunk.replace('.font(.system(size: 27, weight: .medium))',
                      '.font(.system(size: 24, weight: .medium))', 1)
chunk = chunk.replace('Text("Arapça").tag(0)\n                Text("Türkçe").tag(1)\n                Text("Deutsch").tag(2)',
                      'Text("Arapça").tag(0)\n                Text("Türkçe").tag(1)\n                Text("Deutsch").tag(2)', 1)
chunk = chunk.replace('.frame(width: 50, height: 50)', '.frame(width: 46, height: 46)', 1)
chunk = chunk.replace('.font(.system(size: 18, weight: .bold))', '.font(.system(size: 16, weight: .bold))', 1)
chunk = chunk.replace('.padding(13)\n        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 17, style: .continuous))',
                      '.padding(11)\n        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))', 1)
chunk = chunk.replace('RoundedRectangle(cornerRadius: 17).stroke(SalahTheme.gold.opacity(0.52), lineWidth: 1)',
                      'RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.56), lineWidth: 1)', 1)
s = s[:surah_start] + chunk + s[surah_end:]

# Ayah cards: cream/gold treatment closer to the poster instead of green-bordered cards.
ayah_start = s.index("    private func ayahCard(")
ayah_end = s.index("\n    private var sourceFooter", ayah_start)
chunk = s[ayah_start:ayah_end]
chunk = chunk.replace('.padding(13)', '.padding(11)')
chunk = chunk.replace('RoundedRectangle(cornerRadius: 16, style: .continuous)',
                      'RoundedRectangle(cornerRadius: 14, style: .continuous)')
chunk = chunk.replace('RoundedRectangle(cornerRadius: 16)',
                      'RoundedRectangle(cornerRadius: 14)')
chunk = chunk.replace(': SalahTheme.teal.opacity(0.20),',
                      ': SalahTheme.gold.opacity(0.34),')
s = s[:ayah_start] + chunk + s[ayah_end:]

p.write_text(s, encoding="utf-8")

build = Path("scripts/build_unsigned_ipa.sh")
b = build.read_text(encoding="utf-8")
b = b.replace('MARKETING_VERSION="3.20"', 'MARKETING_VERSION="3.21"')
b = b.replace('CURRENT_PROJECT_VERSION="25"', 'CURRENT_PROJECT_VERSION="26"')
build.write_text(b, encoding="utf-8")

print("SalahPath v3.21 Quran reference parity pass applied")
