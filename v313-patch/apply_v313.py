from pathlib import Path

# SalahPath v3.13: make the real Namaz tab match the visual reference instead of a generic iOS List.
p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")
start = s.index("struct GuideView: View {")
end = s.index("\n// MARK: - Rak'ah overview")
new = r'''struct GuideView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                learningHero

                NavigationLink { PrayerHowToView() } label: {
                    HStack(spacing: 10) {
                        ZStack {
                            Circle()
                                .fill(SalahTheme.teal)
                                .frame(width: 42, height: 42)
                            Image(systemName: "play.fill")
                                .font(.system(size: 15, weight: .bold))
                                .foregroundStyle(.white)
                        }
                        VStack(alignment: .leading, spacing: 2) {
                            Text(settings.t("Namaz jetzt Schritt für Schritt lernen", "Namazı şimdi adım adım öğren"))
                                .font(.system(size: 14, weight: .bold))
                                .foregroundStyle(SalahTheme.ink)
                            Text(settings.t("Mit Bildern, Texten und Hanafi-Hinweisen", "Görseller, metinler ve Hanefî açıklamalarıyla"))
                                .font(.system(size: 10, weight: .medium))
                                .foregroundStyle(SalahTheme.mutedInk)
                        }
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption.bold())
                            .foregroundStyle(SalahTheme.teal)
                    }
                    .padding(12)
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 17, style: .continuous))
                    .overlay { RoundedRectangle(cornerRadius: 17).stroke(SalahTheme.gold.opacity(0.50), lineWidth: 1) }
                }
                .buttonStyle(.plain)

                LazyVGrid(columns: [GridItem(.flexible(), spacing: 9), GridItem(.flexible(), spacing: 9)], spacing: 9) {
                    NavigationLink { RakatOverviewView() } label: {
                        learnTile(icon: "list.number", title: settings.t("Fard, Sunnah & Witr", "Farz, sünnet & vitir"), subtitle: settings.t("Rakʿah-Übersicht", "Rekât özeti"))
                    }
                    NavigationLink { WuduGuideView() } label: {
                        learnTile(icon: "drop.fill", title: settings.t("Wudu / Abdest", "Abdest"), subtitle: settings.t("Schritt für Schritt", "Adım adım"))
                    }
                    NavigationLink { PrayerDuaAudioView() } label: {
                        learnTile(icon: "speaker.wave.2.fill", title: settings.t("Gebetsduas", "Namaz duaları"), subtitle: settings.t("Lesen & hören", "Oku & dinle"))
                    }
                    NavigationLink { ShortSurahLearningView() } label: {
                        learnTile(icon: "text.book.closed.fill", title: settings.t("Kurze Suren", "Kısa sûreler"), subtitle: settings.t("Lernen & hören", "Öğren & dinle"))
                    }
                }
                .buttonStyle(.plain)

                VStack(spacing: 0) {
                    NavigationLink { HanafiPrayerPlanView() } label: {
                        referenceRow(icon: "checklist", title: settings.t("2, 3, 4 Rakʿah & Witr", "2, 3, 4 rekât & vitir"), subtitle: settings.t("Gebetsablauf im Detail", "Namaz akışı ayrıntılı"))
                    }
                    NavigationLink { QuranicDuaLibraryView() } label: {
                        referenceRow(icon: "heart.text.square.fill", title: settings.t("Dua-Sammlung", "Dua koleksiyonu"), subtitle: settings.t("Quranische Duas", "Kur'an duaları"))
                    }
                    NavigationLink { PrayerTermsView() } label: {
                        referenceRow(icon: "text.book.closed.fill", title: settings.t("Begriffe einfach erklärt", "Kavramlar"), subtitle: settings.t("Gebet verständlich lernen", "Namazı anlaşılır öğren"))
                    }
                }
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 17, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 17).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }

                Text(settings.t(
                    "Die Grundbestandteile des Gebets sind gleich. Körperhaltungs-Hinweise für Männer und Frauen folgen hier primär der hanafitischen, in der Türkei verbreiteten Darstellung.",
                    "Namazın temel unsurları aynıdır. Erkek ve kadın duruşlarına ilişkin açıklamalar burada öncelikle Türkiye'de yaygın Hanefî anlatıma göre verilir."
                ))
                .font(.system(size: 9.5, weight: .medium))
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 12)
            }
            .padding(.horizontal, 11)
            .padding(.vertical, 10)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Namaz lernen", "Namaz Öğren"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }

    private var learningHero: some View {
        VStack(spacing: 10) {
            Picker(settings.t("Lernmodus", "Öğrenme modu"), selection: $settings.prayerAudience) {
                Text(settings.t("Mann", "Erkek")).tag(PrayerAudience.male)
                Text(settings.t("Frau", "Kadın")).tag(PrayerAudience.female)
            }
            .pickerStyle(.segmented)

            HStack(alignment: .bottom, spacing: 7) {
                VStack(spacing: 4) {
                    Image("male_intention")
                        .resizable()
                        .scaledToFit()
                        .frame(height: 142)
                        .opacity(settings.prayerAudience == .male ? 1 : 0.44)
                    Text(settings.t("Mann", "Erkek"))
                        .font(.caption2.bold())
                        .foregroundStyle(SalahTheme.ink)
                }
                .frame(maxWidth: .infinity)

                Image(systemName: "arrow.right.circle.fill")
                    .font(.system(size: 28, weight: .semibold))
                    .foregroundStyle(SalahTheme.teal)
                    .padding(.bottom, 54)

                VStack(spacing: 4) {
                    Image("female_intention")
                        .resizable()
                        .scaledToFit()
                        .frame(height: 142)
                        .opacity(settings.prayerAudience == .female ? 1 : 0.44)
                    Text(settings.t("Frau", "Kadın"))
                        .font(.caption2.bold())
                        .foregroundStyle(SalahTheme.ink)
                }
                .frame(maxWidth: .infinity)
            }
            .padding(.horizontal, 4)
            .padding(.vertical, 2)
            .background(SalahTheme.gold.opacity(0.07), in: RoundedRectangle(cornerRadius: 13, style: .continuous))

            VStack(alignment: .leading, spacing: 7) {
                learnFeature(settings.t("Wie betet man?", "Namaz nasıl kılınır?"))
                learnFeature(settings.t("Schritt-für-Schritt Anleitung", "Adım adım anlatım"))
                learnFeature(settings.t("Mit Bildern & gesprochenem Text", "Görsel & sesli anlatım"))
                learnFeature(settings.t("Nach hanafitischem Verständnis", "Hanefî mezhebine göre"))
            }

            HStack {
                Label(settings.t("Männer/Frauen Lernmodus", "Erkek/Kadın öğrenim modu"), systemImage: "person.2.fill")
                    .font(.system(size: 10, weight: .bold))
                    .foregroundStyle(SalahTheme.teal)
                Spacer()
                Text(settings.language.title)
                    .font(.system(size: 9, weight: .bold))
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(SalahTheme.gold.opacity(0.20), in: Capsule())
                    .foregroundStyle(SalahTheme.deepTeal)
            }
        }
        .padding(13)
        .background(
            LinearGradient(colors: [SalahTheme.cream, Color.white.opacity(0.86)], startPoint: .topLeading, endPoint: .bottomTrailing),
            in: RoundedRectangle(cornerRadius: 18, style: .continuous)
        )
        .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.54), lineWidth: 1) }
        .shadow(color: SalahTheme.deepTeal.opacity(0.055), radius: 7, y: 3)
    }

    private func learnFeature(_ text: String) -> some View {
        HStack(spacing: 8) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 13, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
            Text(text)
                .font(.system(size: 11, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer(minLength: 0)
        }
    }

    private func learnTile(icon: String, title: String, subtitle: String) -> some View {
        VStack(spacing: 7) {
            Image(systemName: icon)
                .font(.system(size: 25, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
            Text(title)
                .font(.system(size: 11, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .multilineTextAlignment(.center)
                .lineLimit(2)
            Text(subtitle)
                .font(.system(size: 8.5, weight: .medium))
                .foregroundStyle(SalahTheme.mutedInk)
                .multilineTextAlignment(.center)
                .lineLimit(2)
        }
        .frame(maxWidth: .infinity, minHeight: 108)
        .padding(10)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 16).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }
    }

    private func referenceRow(icon: String, title: String, subtitle: String) -> some View {
        HStack(spacing: 10) {
            Image(systemName: icon)
                .font(.system(size: 17, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 31, height: 31)
                .background(SalahTheme.softTeal, in: Circle())
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.system(size: 12, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                Text(subtitle)
                    .font(.system(size: 9, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
            }
            Spacer()
            Image(systemName: "chevron.right")
                .font(.caption.bold())
                .foregroundStyle(SalahTheme.teal)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 10)
        .contentShape(Rectangle())
        .overlay(alignment: .bottom) { Divider().padding(.leading, 53).opacity(0.40) }
    }
}
'''
s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.12"', 'MARKETING_VERSION="3.13"')
t = t.replace('CURRENT_PROJECT_VERSION="17"', 'CURRENT_PROJECT_VERSION="18"')
b.write_text(t, encoding="utf-8")
print("SalahPath v3.13 Namaz reference parity patch applied")
