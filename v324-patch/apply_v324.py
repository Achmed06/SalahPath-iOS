from pathlib import Path

# SalahPath v3.24: Namaz Öğren top-screen parity pass.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

start = s.index("    private var learningHero: some View {")
end = s.index("\n    private func audiencePill", start)

new = r'''    private var learningHero: some View {
        VStack(spacing: 9) {
            HStack {
                HStack(spacing: 7) {
                    Image(systemName: "figure.mind.and.body")
                        .font(.system(size: 15, weight: .semibold))
                        .foregroundStyle(SalahTheme.teal)
                    Text("Namaz Öğren")
                        .font(.system(size: 17, weight: .bold, design: .serif))
                        .foregroundStyle(SalahTheme.ink)
                }
                Spacer()
                Image(systemName: "ellipsis.circle")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(SalahTheme.teal)
            }
            .padding(.horizontal, 1)

            HStack(spacing: 4) {
                audiencePill(.male, title: "Erkek")
                audiencePill(.female, title: "Kadın")

                Text("Deutsch")
                    .font(.system(size: 9.4, weight: .bold))
                    .foregroundStyle(SalahTheme.deepTeal)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 7)
                    .background(
                        SalahTheme.gold.opacity(settings.language == .german ? 0.24 : 0.12),
                        in: RoundedRectangle(cornerRadius: 8, style: .continuous)
                    )
            }
            .padding(4)
            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
            .overlay { RoundedRectangle(cornerRadius: 12).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }

            ZStack {
                RoundedRectangle(cornerRadius: 14, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [SalahTheme.softTeal.opacity(0.92), SalahTheme.cream.opacity(0.90)],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )

                Image(systemName: "moon.stars.fill")
                    .font(.system(size: 20, weight: .medium))
                    .foregroundStyle(SalahTheme.gold.opacity(0.36))
                    .offset(x: 120, y: -67)

                HStack(alignment: .bottom, spacing: 6) {
                    VStack(spacing: 3) {
                        Image("male_intention")
                            .resizable()
                            .scaledToFit()
                            .frame(height: 150)
                            .opacity(settings.prayerAudience == .male ? 1 : 0.52)

                        Text("Erkek")
                            .font(.system(size: 8.7, weight: .bold))
                            .foregroundStyle(SalahTheme.deepTeal)
                    }
                    .frame(maxWidth: .infinity)

                    Button {
                        settings.prayerAudience = settings.prayerAudience == .male ? .female : .male
                    } label: {
                        ZStack {
                            Circle()
                                .fill(SalahTheme.teal)
                                .frame(width: 31, height: 31)
                            Image(systemName: "arrow.right")
                                .font(.system(size: 12, weight: .black))
                                .foregroundStyle(.white)
                        }
                    }
                    .buttonStyle(.plain)
                    .padding(.bottom, 56)

                    VStack(spacing: 3) {
                        Image("female_intention")
                            .resizable()
                            .scaledToFit()
                            .frame(height: 150)
                            .opacity(settings.prayerAudience == .female ? 1 : 0.52)

                        Text("Kadın")
                            .font(.system(size: 8.7, weight: .bold))
                            .foregroundStyle(SalahTheme.deepTeal)
                    }
                    .frame(maxWidth: .infinity)
                }
                .padding(.horizontal, 7)
                .padding(.vertical, 7)
            }
            .frame(height: 191)
            .overlay {
                RoundedRectangle(cornerRadius: 14, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.32), lineWidth: 1)
            }

            VStack(alignment: .leading, spacing: 8) {
                referenceLearnFeature(
                    turkish: "Namaz nasıl kılınır?",
                    german: "Wie betet man?"
                )
                referenceLearnFeature(
                    turkish: "Adım adım anlatım",
                    german: "Schritt-für-Schritt Anleitung"
                )
                referenceLearnFeature(
                    turkish: "Görsel & sesli destek",
                    german: "Mit Bildern & Audio"
                )
                referenceLearnFeature(
                    turkish: "Hanefî mezhebine göre",
                    german: "Nach hanafitischem Verständnis"
                )
            }
            .padding(.horizontal, 3)

            HStack(spacing: 7) {
                Image(systemName: "person.2.fill")
                    .font(.system(size: 12, weight: .bold))
                    .foregroundStyle(SalahTheme.teal)

                VStack(alignment: .leading, spacing: 1) {
                    Text("Männer/Frauen Lernmodus")
                        .font(.system(size: 9.4, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                    Text("Erkek-Kadın öğrenim modu")
                        .font(.system(size: 7.8, weight: .semibold))
                        .foregroundStyle(SalahTheme.mutedInk)
                }

                Spacer()

                Image(systemName: "chevron.right")
                    .font(.system(size: 9, weight: .black))
                    .foregroundStyle(SalahTheme.teal)
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 8)
            .background(SalahTheme.gold.opacity(0.12), in: RoundedRectangle(cornerRadius: 11, style: .continuous))
        }
        .padding(11)
        .background(
            LinearGradient(
                colors: [SalahTheme.cream, Color.white.opacity(0.90)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            ),
            in: RoundedRectangle(cornerRadius: 17, style: .continuous)
        )
        .overlay { RoundedRectangle(cornerRadius: 17).stroke(SalahTheme.gold.opacity(0.55), lineWidth: 1) }
        .shadow(color: SalahTheme.deepTeal.opacity(0.05), radius: 6, y: 2)
    }

    private func referenceLearnFeature(turkish: String, german: String) -> some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 13, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
                .padding(.top, 1)

            VStack(alignment: .leading, spacing: 1) {
                Text(turkish)
                    .font(.system(size: 10.7, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                Text(german)
                    .font(.system(size: 8.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
            }

            Spacer(minLength: 0)
        }
    }
'''
s = s[:start] + new + s[end:]

# Keep the content below the reference screen, but reduce its visual prominence.
s = s.replace(
'''                NavigationLink { PrayerHowToView() } label: {
                    HStack(spacing: 10) {
''',
'''                NavigationLink { PrayerHowToView() } label: {
                    HStack(spacing: 9) {
''',
1
)
s = s.replace('.frame(width: 42, height: 42)', '.frame(width: 36, height: 36)', 1)
s = s.replace('.font(.system(size: 15, weight: .bold))', '.font(.system(size: 13, weight: .bold))', 1)
s = s.replace('.font(.system(size: 14, weight: .bold))', '.font(.system(size: 12.5, weight: .bold))', 1)
s = s.replace('.padding(12)\n                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 17, style: .continuous))',
              '.padding(10)\n                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))', 1)
s = s.replace('RoundedRectangle(cornerRadius: 17).stroke(SalahTheme.gold.opacity(0.50), lineWidth: 1)',
              'RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1)', 1)

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.23"', 'MARKETING_VERSION="3.24"')
t = t.replace('CURRENT_PROJECT_VERSION="28"', 'CURRENT_PROJECT_VERSION="29"')
b.write_text(t, encoding="utf-8")
print("SalahPath v3.24 Namaz Öğren strict parity pass applied")
