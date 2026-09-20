from pathlib import Path

root = Path.cwd()

guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

# ---------- Consistent compact navigation titles ----------
title_anchors = [
    '.navigationTitle(settings.t("Rakʿat", "Rekât"))',
    '.navigationTitle(settings.t("Rakʿah-Ablauf", "Rekât düzeni"))',
    '.navigationTitle(settings.t("Qunūt", "Kunut"))',
    '.navigationTitle(settings.t("Begriffe", "Kavramlar"))',
    '.navigationTitle(settings.t("Suren lernen", "Sureleri öğren"))',
    '.navigationTitle(settings.t("Fasten-Tracker", "Oruç takibi"))',
    '.navigationTitle(settings.t("Hicri-Kalender", "Hicrî takvim"))',
]
for anchor in title_anchors:
    if anchor not in s:
        raise SystemExit(f"v3.86: navigation title anchor missing: {anchor}")
    s = s.replace(anchor, anchor + '\n        .navigationBarTitleDisplayMode(.inline)', 1)

# ---------- Replace external prayer-position infographic with app-native artwork ----------
start_marker = 'struct PrayerSequenceReferenceView: View {'
end_marker = '// MARK: - Dhikr'
start = s.find(start_marker)
end = s.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("v3.86: prayer sequence reference block missing")

new_block = '''struct PrayerSequenceReferenceView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let sequence: [(pose: String, de: String, tr: String)] = [
        ("intention", "Absicht", "Niyet"),
        ("takbir", "Takbīr", "Tekbir"),
        ("standing", "Stehen", "Kıyam"),
        ("bowing", "Verbeugung", "Rükû"),
        ("upright", "Aufrichten", "Kavme"),
        ("sujud", "Niederwerfung", "Secde"),
        ("sitting", "Sitzen", "Oturuş"),
        ("salam_right", "Salām", "Selâm")
    ]

    private var audiencePrefix: String {
        settings.prayerAudience == .female ? "female_" : "male_"
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 14) {
                HStack(spacing: 9) {
                    Image(systemName: "figure.mind.and.body")
                        .font(.system(size: 18, weight: .semibold))
                        .foregroundStyle(SalahTheme.teal)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(settings.t("Gebetsablauf im Überblick", "Namaz akışı özeti"))
                            .font(.headline)
                            .foregroundStyle(SalahTheme.ink)
                        Text(settings.t(
                            "Darstellung: " + settings.prayerAudience.title(settings.language),
                            "Gösterim: " + settings.prayerAudience.title(settings.language)
                        ))
                        .font(.caption)
                        .foregroundStyle(SalahTheme.mutedInk)
                    }
                }
                .padding(13)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }

                LazyVGrid(
                    columns: [
                        GridItem(.flexible(), spacing: 9),
                        GridItem(.flexible(), spacing: 9)
                    ],
                    spacing: 9
                ) {
                    ForEach(Array(sequence.enumerated()), id: \.offset) { index, item in
                        VStack(spacing: 7) {
                            HStack {
                                Text("\(index + 1)")
                                    .font(.caption.bold().monospacedDigit())
                                    .foregroundStyle(SalahTheme.deepTeal)
                                    .frame(width: 24, height: 24)
                                    .background(SalahTheme.gold.opacity(0.22), in: Circle())
                                Spacer()
                            }

                            PrayerPoseArtwork(assetName: audiencePrefix + item.pose)
                                .frame(height: 145)

                            Text(settings.language == .german ? item.de : item.tr)
                                .font(.system(size: 11.5, weight: .bold))
                                .foregroundStyle(SalahTheme.ink)
                        }
                        .padding(9)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
                    }
                }

                Text(settings.t(
                    "Die Übersicht zeigt die Grundbewegungen. Für Rezitationen, Rakʿah-Details und hanafitische Unterschiede nutze die Schritt-für-Schritt-Anleitung.",
                    "Bu özet temel hareketleri gösterir. Okunan metinler, rekât ayrıntıları ve Hanefî farklılıklar için adım adım anlatımı kullan."
                ))
                .font(.footnote)
                .foregroundStyle(SalahTheme.mutedInk)
                .padding(.horizontal, 2)
            }
            .padding(12)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetspositionen", "Namaz duruşları"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

'''
s = s[:start] + new_block + s[end:]
guide.write_text(s, encoding="utf-8")

# ---------- Tracker copy cleanup + compact title ----------
home = root / "SalahZeit" / "Views" / "HomeView.swift"
s = home.read_text(encoding="utf-8")

old = 'Section(settings.t("Für Muslimas", "Müslimeler için"))'
new = 'Section(settings.t("Für Musliminnen", "Müslüman kadınlar için"))'
if old not in s:
    raise SystemExit("v3.86: tracker section title anchor missing")
s = s.replace(old, new, 1)

old = "Diyanet'in agtardığı rivayete göre âdet döneminde kılınmayan farz namazlar daha sonra kaza edilmez. Uygulamada sebep kaydetmeden takibi duraklatabilirsin."
new = "Diyanet'in aktardığı rivayete göre âdet döneminde kılınmayan farz namazlar daha sonra kaza edilmez. Uygulamada sebep kaydetmeden takibi duraklatabilirsin."
if old not in s:
    raise SystemExit("v3.86: tracker Turkish copy anchor missing")
s = s.replace(old, new, 1)

anchor = '.navigationTitle(settings.t("Tracker-Pause", "Takip duraklatma"))'
if anchor not in s:
    raise SystemExit("v3.86: tracker-pause navigation title anchor missing")
s = s.replace(anchor, anchor + '\n        .navigationBarTitleDisplayMode(.inline)', 1)

home.write_text(s, encoding="utf-8")

print("SalahPath v3.86 secondary-screen visual consistency patch applied")
