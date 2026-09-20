from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = '''                            NavigationLink {
                                QuranSurahView(surah: chapter, initialAyah: lastRead.ayah)
                            } label: {
                                HStack(spacing: 12) {
                                    Image(systemName: "bookmark.fill")
                                        .font(.system(size: 18, weight: .bold))
                                        .foregroundStyle(SalahTheme.gold)
                                        .frame(width: 42, height: 42)
                                        .background(SalahTheme.deepTeal, in: Circle())

                                    VStack(alignment: .leading, spacing: 3) {
                                        Text(settings.t("Weiterlesen", "Okumaya devam et"))
                                            .font(.headline.bold())
                                            .foregroundStyle(SalahTheme.deepTeal)
                                        Text("\(chapter.englishName) · \(settings.t("Vers", "Ayet")) \(lastRead.ayah)")
                                            .font(.subheadline)
                                            .foregroundStyle(SalahTheme.ink)
                                        Text(chapter.name)
                                            .font(.system(size: 18, weight: .medium))
                                            .foregroundStyle(SalahTheme.mutedInk)
                                    }

                                    Spacer()
                                    Image(systemName: "chevron.right")
                                        .font(.headline.bold())
                                        .foregroundStyle(SalahTheme.teal)
                                }
                                .padding(12)
                                .background(
                                    LinearGradient(
                                        colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.72)],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    ),
                                    in: RoundedRectangle(cornerRadius: 15, style: .continuous)
                                )
                                .overlay {
                                    RoundedRectangle(cornerRadius: 15, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.46), lineWidth: 1)
                                }
                            }
'''
new = '''                            NavigationLink {
                                QuranSurahView(surah: chapter, initialAyah: lastRead.ayah)
                            } label: {
                                VStack(alignment: .leading, spacing: 10) {
                                    HStack(spacing: 12) {
                                        Image(systemName: "bookmark.fill")
                                            .font(.system(size: 18, weight: .bold))
                                            .foregroundStyle(SalahTheme.gold)
                                            .frame(width: 42, height: 42)
                                            .background(SalahTheme.deepTeal, in: Circle())

                                        VStack(alignment: .leading, spacing: 3) {
                                            Text(settings.t("Weiterlesen", "Okumaya devam et"))
                                                .font(.headline.bold())
                                                .foregroundStyle(SalahTheme.deepTeal)
                                            Text("\(chapter.englishName) · \(settings.t("Vers", "Ayet")) \(lastRead.ayah)")
                                                .font(.subheadline)
                                                .foregroundStyle(SalahTheme.ink)
                                            Text(chapter.name)
                                                .font(.system(size: 18, weight: .medium))
                                                .foregroundStyle(SalahTheme.mutedInk)
                                        }

                                        Spacer()
                                        Image(systemName: "chevron.right")
                                            .font(.headline.bold())
                                            .foregroundStyle(SalahTheme.teal)
                                    }

                                    if let progress = readingProgress {
                                        VStack(spacing: 5) {
                                            HStack {
                                                Text(settings.t("Lesefortschritt", "Okuma ilerlemesi"))
                                                    .font(.caption.bold())
                                                    .foregroundStyle(SalahTheme.mutedInk)
                                                Spacer()
                                                Text("\(Int((progress * 100).rounded())) %")
                                                    .font(.caption.bold().monospacedDigit())
                                                    .foregroundStyle(SalahTheme.deepTeal)
                                            }

                                            ProgressView(value: progress)
                                                .tint(SalahTheme.teal)
                                        }
                                    }
                                }
                                .padding(12)
                                .background(
                                    LinearGradient(
                                        colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.72)],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    ),
                                    in: RoundedRectangle(cornerRadius: 15, style: .continuous)
                                )
                                .overlay {
                                    RoundedRectangle(cornerRadius: 15, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.46), lineWidth: 1)
                                }
                            }
'''
if old not in text:
    raise SystemExit("v424: Quran Continue Reading card anchor missing")
text = text.replace(old, new, 1)

anchor = '    private var quranShareText: String {\n'
helper = '''    private var readingProgress: Double? {
        guard let lastRead, !store.chapters.isEmpty else { return nil }

        let totalAyahs = store.chapters.reduce(0) { $0 + $1.numberOfAyahs }
        guard totalAyahs > 0 else { return nil }

        let ayahsBeforeSurah = store.chapters
            .filter { $0.number < lastRead.surah }
            .reduce(0) { $0 + $1.numberOfAyahs }

        let current = ayahsBeforeSurah + lastRead.ayah
        return min(max(Double(current) / Double(totalAyahs), 0), 1)
    }

'''
if anchor not in text:
    raise SystemExit("v424: quranShareText declaration anchor missing")
text = text.replace(anchor, helper + anchor, 1)

guide.write_text(text, encoding="utf-8")
print("v424 applied: Quran Continue Reading now shows whole-Quran reading progress")
