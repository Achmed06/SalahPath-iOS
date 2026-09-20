from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
text = guide.read_text(encoding="utf-8")

old_state = """struct PrayerHowToView: View {
    @EnvironmentObject private var settings: SettingsStore
"""
new_state = """struct PrayerHowToView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var currentStepIndex = 0
"""
if old_state not in text:
    raise SystemExit("v396: PrayerHowToView state anchor missing")
text = text.replace(old_state, new_state, 1)

hero_start_marker = "    private var prayerLearningHero: some View {"
hero_end_marker = "\n    private func learningFeature"
hero_start = text.index(hero_start_marker)
hero_end = text.index(hero_end_marker, hero_start)
new_hero = '''    private var prayerLearningHero: some View {
        VStack(spacing: 12) {
            Picker(settings.t("Lernmodus", "Öğrenme modu"), selection: $settings.prayerAudience) {
                Text(settings.t("Mann", "Erkek")).tag(PrayerAudience.male)
                Text(settings.t("Frau", "Kadın")).tag(PrayerAudience.female)
            }
            .pickerStyle(.segmented)

            HStack(spacing: 14) {
                PrayerPoseArtwork(assetName: settings.prayerAudience == .male ? "male_intention" : "female_intention")
                    .frame(width: 118, height: 150)
                    .background(SalahTheme.cream)
                    .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))

                VStack(alignment: .leading, spacing: 8) {
                    Text(settings.t("Ganz von vorne lernen", "En baştan öğren"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Du siehst immer nur einen Schritt. Lies ihn in Ruhe, schau dir die Haltung an und tippe erst dann auf Weiter.",
                        "Her seferinde yalnız bir adım görürsün. Sakin şekilde oku, duruşa bak ve sonra İleri'ye dokun."
                    ))
                    .font(.subheadline)
                    .foregroundStyle(SalahTheme.ink)
                    .fixedSize(horizontal: false, vertical: true)
                }
                Spacer(minLength: 0)
            }

            VStack(alignment: .leading, spacing: 7) {
                learningFeature(settings.t("Eine Haltung pro Schritt", "Her adımda tek duruş"), icon: "checkmark.circle.fill")
                learningFeature(settings.t("Arabisch, Umschrift und Bedeutung", "Arapça, okunuş ve anlam"), icon: "checkmark.circle.fill")
                learningFeature(settings.t("Mann/Frau getrennt dargestellt", "Erkek/Kadın ayrı gösterilir"), icon: "checkmark.circle.fill")
                learningFeature(settings.t("Hanafi/Diyanet-Grunddarstellung", "Hanefî/Diyanet temel anlatımı"), icon: "checkmark.circle.fill")
            }
        }
        .padding(13)
        .background(
            LinearGradient(
                colors: [SalahTheme.cream, Color.white.opacity(0.80)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            ),
            in: RoundedRectangle(cornerRadius: 18, style: .continuous)
        )
        .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.52), lineWidth: 1) }
    }
'''
text = text[:hero_start] + new_hero + text[hero_end:]

body_start = text.index("    var body: some View {", text.index("struct PrayerHowToView"))
body_end = text.index("\n}\n\nprivate struct PrayerTutorialStepCard", body_start)
new_body = '''    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(spacing: 14) {
                    Color.clear.frame(height: 1).id("prayer-step-top")
                    prayerLearningHero

                    NavigationLink { HanafiPrayerPlanView() } label: {
                        HStack {
                            Label(settings.t("Rak'a einfach verstehen", "Rekâtı kolayca anla"), systemImage: "list.number")
                                .font(.headline)
                            Spacer()
                            Image(systemName: "chevron.right")
                        }
                        .cardStyle()
                    }
                    .buttonStyle(.plain)

                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text("0")
                                .font(.headline.bold())
                                .frame(width: 34, height: 34)
                                .background(SalahTheme.gold.opacity(0.22), in: Circle())
                            Text(settings.t("Bevor du anfängst", "Başlamadan önce"))
                                .font(.title3.bold())
                        }
                        Text(settings.t(
                            "Prüfe: Die Gebetszeit hat begonnen, du hast Wudu, dein Körper, deine Kleidung und dein Gebetsplatz sind sauber, die vorgeschriebenen Körperstellen sind bedeckt und du stehst zur Qibla. Danach gehst du Schritt für Schritt weiter.",
                            "Kontrol et: Namaz vakti girmiş olsun, abdestli ol, bedenin, elbisen ve namaz yerin temiz olsun, örtülmesi gereken yerler örtülü olsun ve kıbleye dön. Sonra adım adım ilerle."
                        ))
                        .font(.subheadline)
                        .fixedSize(horizontal: false, vertical: true)
                    }
                    .cardStyle()

                    VStack(spacing: 8) {
                        HStack {
                            Text(settings.t("Schritt", "Adım") + " \\(currentStepIndex + 1) / \\(steps.count)")
                                .font(.headline.bold())
                                .foregroundStyle(SalahTheme.deepTeal)
                            Spacer()
                            Text(settings.prayerAudience.title(settings.language))
                                .font(.caption.bold())
                                .padding(.horizontal, 9)
                                .padding(.vertical, 5)
                                .background(SalahTheme.softTeal, in: Capsule())
                        }
                        ProgressView(value: Double(currentStepIndex + 1), total: Double(steps.count))
                            .tint(SalahTheme.teal)
                    }
                    .padding(12)
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                    .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }

                    PrayerTutorialStepCard(step: steps[currentStepIndex], audience: settings.prayerAudience)

                    HStack(spacing: 12) {
                        Button {
                            guard currentStepIndex > 0 else { return }
                            currentStepIndex -= 1
                            withAnimation(.easeInOut(duration: 0.2)) {
                                proxy.scrollTo("prayer-step-top", anchor: .top)
                            }
                        } label: {
                            Label(settings.t("Zurück", "Geri"), systemImage: "chevron.left")
                                .font(.headline.bold())
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 13)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(currentStepIndex > 0 ? SalahTheme.deepTeal : SalahTheme.mutedInk.opacity(0.45))
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }
                        .disabled(currentStepIndex == 0)

                        Button {
                            guard currentStepIndex < steps.count - 1 else { return }
                            currentStepIndex += 1
                            withAnimation(.easeInOut(duration: 0.2)) {
                                proxy.scrollTo("prayer-step-top", anchor: .top)
                            }
                        } label: {
                            HStack {
                                Text(currentStepIndex == steps.count - 1 ? settings.t("Fertig", "Bitti") : settings.t("Weiter", "İleri"))
                                Image(systemName: currentStepIndex == steps.count - 1 ? "checkmark" : "chevron.right")
                            }
                            .font(.headline.bold())
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 13)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(.white)
                        .background(currentStepIndex == steps.count - 1 ? SalahTheme.mutedInk : SalahTheme.deepTeal, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .disabled(currentStepIndex == steps.count - 1)
                    }

                    VStack(alignment: .leading, spacing: 8) {
                        Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama")).font(.headline)
                        Text(settings.t(
                            "Die Gebetsreihenfolge und die gekennzeichneten Mann/Frau-Haltungsdetails orientieren sich an der hanafitischen Diyanet-Darstellung. Unterschiede anderer Rechtsschulen werden nicht als Fehler dargestellt.",
                            "Namaz sırası ve belirtilen erkek/kadın duruş ayrıntıları Diyanet'in Hanefî anlatımına dayanır. Diğer mezheplerin farklı uygulamaları hata olarak gösterilmez."
                        ))
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    }
                    .cardStyle(material: true)
                }
                .padding()
            }
            .background(SalahTheme.page)
            .navigationTitle(settings.t("Gebet lernen", "Namaz öğren"))
            .navigationBarTitleDisplayMode(.inline)
            .onChange(of: settings.prayerAudience) { _, _ in
                currentStepIndex = 0
                proxy.scrollTo("prayer-step-top", anchor: .top)
            }
        }
    }
'''
text = text[:body_start] + new_body + text[body_end:]

guide.write_text(text, encoding="utf-8")
print("v396 applied: guided one-step prayer learning flow")
