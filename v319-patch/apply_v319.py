from pathlib import Path

# SalahPath v3.19: detail pass against the supplied phone screenshots.

home = Path("SalahZeit/Views/HomeView.swift")
s = home.read_text(encoding="utf-8")

# Replace the single sequence sentence in the next-prayer card with the reference-style
# individual Sunnah/Fard/Witr capsules and arrows.
old = '''            Text(prayer.kind.fullSequence(settings.language))
                .font(.system(size: 12.5, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .frame(maxWidth: .infinity)
                .padding(.horizontal, 10)
                .padding(.vertical, 8)
                .background(Color.white.opacity(0.63), in: RoundedRectangle(cornerRadius: 10, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .stroke(SalahTheme.gold.opacity(0.28), lineWidth: 1)
                }
'''
new = '''            HStack(spacing: 4) {
                let segments = referenceSequence(for: prayer.kind)
                ForEach(Array(segments.enumerated()), id: \\.offset) { index, segment in
                    VStack(spacing: 1) {
                        Text(segment.0)
                            .font(.system(size: 10.2, weight: .bold))
                            .foregroundStyle(SalahTheme.ink)
                            .lineLimit(1)
                        Text(segment.1)
                            .font(.system(size: 7.5, weight: .semibold))
                            .foregroundStyle(SalahTheme.mutedInk)
                            .lineLimit(1)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 6)
                    .background(Color.white.opacity(0.68), in: RoundedRectangle(cornerRadius: 9, style: .continuous))
                    .overlay {
                        RoundedRectangle(cornerRadius: 9, style: .continuous)
                            .stroke(SalahTheme.gold.opacity(0.36), lineWidth: 1)
                    }

                    if index < segments.count - 1 {
                        Image(systemName: "arrow.right")
                            .font(.system(size: 8, weight: .bold))
                            .foregroundStyle(SalahTheme.gold)
                    }
                }
            }
'''
if old not in s:
    raise SystemExit("Home sequence block not found")
s = s.replace(old, new, 1)

# Make the dua heading visually bilingual exactly like the reference.
s = s.replace(
    'Text(settings.t("Dua des Tages / Günün Duası", "Günün Duası / Dua des Tages"))',
    'Text("Günün Duası / Dua des Tages")',
    1
)

# Reference image uses a flame/gold streak accent rather than the stock orange emphasis.
s = s.replace('.foregroundStyle(.orange)', '.foregroundStyle(SalahTheme.gold)', 1)

# Add helper just before currentWeekDates.
needle = '    private func currentWeekDates() -> [Date] {'
helper = r'''    private func referenceSequence(for kind: PrayerKind) -> [(String, String)] {
        let sunnah = settings.language == .german ? "Sunnah" : "Sünnet"
        let fard = settings.language == .german ? "Fard" : "Farz"
        let witr = settings.language == .german ? "Witr" : "Vitir"

        switch kind {
        case .fajr:
            return [("2", sunnah), ("2", fard)]
        case .sunrise:
            return [("2", settings.language == .german ? "Duha" : "Kuşluk")]
        case .dhuhr:
            return [("4", sunnah), ("4", fard), ("2", sunnah)]
        case .asr:
            return [("4", sunnah), ("4", fard), ("2", sunnah)]
        case .maghrib:
            return [("3", fard), ("2", sunnah)]
        case .isha:
            return [("4", sunnah), ("4", fard), ("2", sunnah), ("3", witr)]
        }
    }

'''
if needle not in s:
    raise SystemExit("Home helper insertion point not found")
s = s.replace(needle, helper + needle, 1)
home.write_text(s, encoding="utf-8")

guide = Path("SalahZeit/Views/GuideView.swift")
g = guide.read_text(encoding="utf-8")

# Learning screen: replace stock segmented control with reference-looking Erkek/Kadın + language tabs.
old_picker = '''            Picker(settings.t("Lernmodus", "Öğrenme modu"), selection: $settings.prayerAudience) {
                Text(settings.t("Mann", "Erkek")).tag(PrayerAudience.male)
                Text(settings.t("Frau", "Kadın")).tag(PrayerAudience.female)
            }
            .pickerStyle(.segmented)
'''
new_picker = '''            HStack(spacing: 5) {
                audiencePill(.male, title: "Erkek")
                audiencePill(.female, title: "Kadın")

                Text(settings.language == .german ? "Deutsch" : "Türkçe")
                    .font(.system(size: 9.5, weight: .bold))
                    .foregroundStyle(SalahTheme.deepTeal)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 7)
                    .background(SalahTheme.gold.opacity(0.18), in: RoundedRectangle(cornerRadius: 8, style: .continuous))
            }
            .padding(4)
            .background(SalahTheme.softTeal.opacity(0.72), in: RoundedRectangle(cornerRadius: 11, style: .continuous))
'''
if old_picker not in g:
    raise SystemExit("Guide picker block not found")
g = g.replace(old_picker, new_picker, 1)

# Reference artwork has a much tighter image block.
g = g.replace('.frame(height: 142)', '.frame(height: 132)', 2)
g = g.replace('.padding(.bottom, 54)', '.padding(.bottom, 48)', 1)

# The reference says image & video support. Keep wording aligned without claiming video content elsewhere.
g = g.replace(
    'learnFeature(settings.t("Mit Bildern & gesprochenem Text", "Görsel & sesli anlatım"))',
    'learnFeature(settings.t("Mit Bildern & Audio", "Görsel & sesli destek"))',
    1
)

# Add audience pill helper before learnFeature.
needle = '    private func learnFeature(_ text: String) -> some View {'
helper = r'''    private func audiencePill(_ audience: PrayerAudience, title: String) -> some View {
        Button {
            settings.prayerAudience = audience
        } label: {
            Text(title)
                .font(.system(size: 9.5, weight: .bold))
                .foregroundStyle(settings.prayerAudience == audience ? .white : SalahTheme.deepTeal)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 7)
                .background(
                    settings.prayerAudience == audience ? SalahTheme.teal : Color.clear,
                    in: RoundedRectangle(cornerRadius: 8, style: .continuous)
                )
        }
        .buttonStyle(.plain)
    }

'''
if needle not in g:
    raise SystemExit("Guide helper insertion point not found")
g = g.replace(needle, helper + needle, 1)

# Quran reference panel: tighten proportions and add gold ornamental divider under tabs.
g = g.replace(
    '.overlay { RoundedRectangle(cornerRadius: 13).stroke(SalahTheme.gold.opacity(0.35), lineWidth: 1) }\n\n                        VStack(alignment: .leading, spacing: 11) {',
    '''.overlay { RoundedRectangle(cornerRadius: 13).stroke(SalahTheme.gold.opacity(0.35), lineWidth: 1) }

                        HStack(spacing: 7) {
                            Rectangle().fill(SalahTheme.gold.opacity(0.38)).frame(height: 1)
                            Image(systemName: "leaf.fill")
                                .font(.system(size: 8, weight: .bold))
                                .foregroundStyle(SalahTheme.gold)
                            Rectangle().fill(SalahTheme.gold.opacity(0.38)).frame(height: 1)
                        }
                        .padding(.horizontal, 14)

                        VStack(alignment: .leading, spacing: 10) {''',
    1
)
g = g.replace('.font(.system(size: 27, weight: .medium))', '.font(.system(size: 25, weight: .medium))', 1)
g = g.replace('.font(.system(size: 24, weight: .medium))', '.font(.system(size: 22, weight: .medium))', 1)
g = g.replace('Circle().fill(SalahTheme.deepTeal).frame(width: 48, height: 48)',
              'Circle().fill(SalahTheme.deepTeal).frame(width: 44, height: 44)', 1)
g = g.replace('.padding(14)\n                        .background(SalahTheme.cream',
              '.padding(12)\n                        .background(SalahTheme.cream', 1)

# Dhikr reference counter should start at 33 but reset from the UI like a real tasbih.
dhikr_start = g.index("struct DhikrView: View {")
quran_start = g.index("struct QuranView: View {")
dh = g[dhikr_start:quran_start]
dh = dh.replace('Text("\\(counter)")', 'Text("\\(counter)")', 1)
# Add a small reset control below the +/- counter, matching the compact reference control area.
counter_needle = '''                    }
                    .foregroundStyle(SalahTheme.teal)
                }
                .padding(.vertical, 18)
'''
counter_new = '''                    }
                    .foregroundStyle(SalahTheme.teal)

                    Button {
                        counter = 33
                    } label: {
                        Label(settings.t("Zurücksetzen", "Sıfırla"), systemImage: "arrow.counterclockwise")
                            .font(.system(size: 8.5, weight: .bold))
                            .foregroundStyle(SalahTheme.teal)
                    }
                    .buttonStyle(.plain)
                }
                .padding(.vertical, 15)
'''
if counter_needle in dh:
    dh = dh.replace(counter_needle, counter_new, 1)
g = g[:dhikr_start] + dh + g[quran_start:]

guide.write_text(g, encoding="utf-8")

build = Path("scripts/build_unsigned_ipa.sh")
b = build.read_text(encoding="utf-8")
b = b.replace('MARKETING_VERSION="3.18"', 'MARKETING_VERSION="3.19"')
b = b.replace('CURRENT_PROJECT_VERSION="23"', 'CURRENT_PROJECT_VERSION="24"')
build.write_text(b, encoding="utf-8")

print("SalahPath v3.19 strict detail parity pass applied")
