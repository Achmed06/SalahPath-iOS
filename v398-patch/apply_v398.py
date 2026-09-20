from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
text = guide.read_text(encoding="utf-8")

# Add guided state.
old = """struct WuduGuideView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let steps: [WuduTutorialStep] = [
"""
new = """struct WuduGuideView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var currentStepIndex = 0
    @State private var showExactDetail = true

    private let steps: [WuduTutorialStep] = [
"""
if old not in text:
    raise SystemExit("v398: WuduGuideView state anchor missing")
text = text.replace(old, new, 1)

# Make the most important washing boundaries explicit.
replacements = {
'''deAction: "Das ganze Gesicht waschen. Einmal vollständig ist Fard; dreimal entspricht der üblichen Sunnah-Praxis.", trAction: "Yüzün tamamını yıka. Bir kez tam yıkamak farzdır; üç kez yıkamak yaygın sünnet uygulamasıdır."''':
'''deAction: "Wasche das ganze Gesicht: vom normalen Haaransatz bis zum Kinn und seitlich von Ohr zu Ohr. Kein Bereich darf trocken bleiben. Einmal vollständig ist Farz; dreimal entspricht der Sunnah-Praxis.", trAction: "Yüzün tamamını normal saç çizgisinden çeneye ve bir kulaktan diğer kulağa kadar yıka. Kuru yer kalmamalı. Bir kez tam yıkamak farzdır; üç kez yıkamak sünnet uygulamasıdır."''',
'''deAction: "Rechten Arm einschließlich Ellenbogen vollständig waschen.", trAction: "Sağ kolu dirsekle birlikte tamamen yıka."''':
'''deAction: "Wasche die rechte Hand und den rechten Arm vollständig bis einschließlich Ellenbogen. Achte auf Fingerzwischenräume und darauf, dass der Ellenbogen nass wird.", trAction: "Sağ eli ve sağ kolu dirsek dahil tamamen yıka. Parmak aralarına ve dirseğin tamamen ıslanmasına dikkat et."''',
'''deAction: "Linken Arm einschließlich Ellenbogen vollständig waschen.", trAction: "Sol kolu dirsekle birlikte tamamen yıka."''':
'''deAction: "Wasche die linke Hand und den linken Arm vollständig bis einschließlich Ellenbogen. Achte auf Fingerzwischenräume und darauf, dass der Ellenbogen nass wird.", trAction: "Sol eli ve sol kolu dirsek dahil tamamen yıka. Parmak aralarına ve dirseğin tamamen ıslanmasına dikkat et."''',
'''deTitle: "Nacken / Boyun", trTitle: "Boyun", deAction: "Nach der von Diyanet dargestellten Reihenfolge wird mit den Rückseiten beider feuchten Hände über den Nacken gestrichen. Nicht die Kehle/Vorderseite des Halses wischen. Dieser Schritt ist keiner der vier Fard-Bestandteile.", trAction: "Diyanet'in anlattığı sırada, iki ıslak elin tersiyle boyun mesh edilir. Boğazın ön kısmı mesh edilmez. Bu adım abdestin dört farzından biri değildir."''':
'''deTitle: "Nacken / Ense", trTitle: "Boyun / ense", deAction: "In der Diyanet/Hanafi-Lernreihenfolge wird die Nacken- bzw. Ensenpartie mit der Rückseite der feuchten Finger gewischt. Nicht die Kehle oder Vorderseite des Halses wischen. Dieser Schritt ist Sunnah und gehört NICHT zu den vier Farz-Bestandteilen.", trAction: "Diyanet/Hanefî öğrenme sıralamasında ense, ıslak parmakların dış kısmıyla mesh edilir. Boğazın ön tarafı mesh edilmez. Bu adım sünnettir ve abdestin dört farzından biri DEĞİLDİR."''',
'''deAction: "Rechten Fuß einschließlich Knöchel vollständig waschen und Wasser zwischen die Zehen gelangen lassen.", trAction: "Sağ ayağı topuk ve aşık kemikleriyle birlikte tamamen yıka; parmak aralarına su ulaştır."''':
'''deAction: "Wasche den rechten Fuß vollständig bis einschließlich beider Knöchel. Führe Wasser auch zwischen die Zehen und kontrolliere Ferse, Fußsohle und Knöchel auf trockene Stellen.", trAction: "Sağ ayağı iki aşık kemiği dahil tamamen yıka. Parmak aralarına da su ulaştır; topuk, ayak tabanı ve aşık kemiklerinde kuru yer kalmadığını kontrol et."''',
'''deAction: "Linken Fuß einschließlich Knöchel vollständig waschen und Wasser zwischen die Zehen gelangen lassen.", trAction: "Sol ayağı topuk ve aşık kemikleriyle birlikte tamamen yıka; parmak aralarına su ulaştır."''':
'''deAction: "Wasche den linken Fuß vollständig bis einschließlich beider Knöchel. Führe Wasser auch zwischen die Zehen und kontrolliere Ferse, Fußsohle und Knöchel auf trockene Stellen.", trAction: "Sol ayağı iki aşık kemiği dahil tamamen yıka. Parmak aralarına da su ulaştır; topuk, ayak tabanı ve aşık kemiklerinde kuru yer kalmadığını kontrol et."'''
}
for old_snip, new_snip in replacements.items():
    if old_snip not in text:
        raise SystemExit("v398: Wudu copy anchor missing")
    text = text.replace(old_snip, new_snip, 1)

# Replace the all-at-once Wudu body with a guided one-step flow.
struct_start = text.index("struct WuduGuideView: View {")
body_start = text.index("    var body: some View {", struct_start)
struct_end = text.index("\n}\n\n\n// MARK: - Terms", body_start)

new_body = r'''    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(spacing: 14) {
                    Color.clear.frame(height: 1).id("wudu-step-top")

                    VStack(alignment: .leading, spacing: 9) {
                        Label(settings.t("Wudu ganz von vorne", "Abdesti en baştan öğren"), systemImage: "drop.fill")
                            .font(.title3.bold())
                            .foregroundStyle(SalahTheme.deepTeal)

                        Text(settings.t(
                            "Männer und Frauen machen Wudu grundsätzlich gleich. Du siehst immer nur einen Schritt. Mach ihn in Ruhe fertig und gehe dann weiter.",
                            "Erkekler ve kadınlar abdesti temelde aynı şekilde alır. Her seferinde yalnız bir adım görürsün. Adımı sakin şekilde tamamla, sonra devam et."
                        ))
                        .font(.subheadline)
                        .fixedSize(horizontal: false, vertical: true)

                        Divider()

                        Text(settings.t(
                            "Die 4 Farz-Bestandteile im Hanafi/Diyanet-Ablauf sind: 1) Gesicht waschen, 2) Arme mit Ellenbogen waschen, 3) mindestens ein Viertel des Kopfes mit nasser Hand wischen, 4) Füße mit Knöcheln waschen.",
                            "Hanefî/Diyanet anlatımında abdestin 4 farzı: 1) yüzü yıkamak, 2) kolları dirseklerle yıkamak, 3) başın en az dörtte birini mesh etmek, 4) ayakları aşık kemikleriyle yıkamaktır."
                        ))
                        .font(.footnote.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                        Text(settings.t(
                            "Bei den Farz-Waschschritten reicht für die Gültigkeit eine vollständige Waschung; dreimaliges Waschen ist die Sunnah-Praxis. Kopf-Masah wird einmal gezeigt.",
                            "Farz olan yıkama bölümlerinde geçerlilik için bir kez tam yıkamak yeterlidir; üç kez yıkamak sünnettir. Baş meshi bir kez gösterilir."
                        ))
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    }
                    .cardStyle(material: true)

                    VStack(spacing: 8) {
                        HStack {
                            Text(settings.t("Schritt", "Adım") + " \(currentStepIndex + 1) / \(steps.count)")
                                .font(.headline.bold())
                                .foregroundStyle(SalahTheme.deepTeal)
                            Spacer()
                            Text(steps[currentStepIndex].hanafiFard ? settings.t("FARZ · PFLICHT", "FARZ") : settings.t("SUNNAH", "SÜNNET"))
                                .font(.caption.bold())
                                .padding(.horizontal, 9)
                                .padding(.vertical, 5)
                                .background(
                                    (steps[currentStepIndex].hanafiFard ? SalahTheme.gold : SalahTheme.softTeal),
                                    in: Capsule()
                                )
                                .foregroundStyle(SalahTheme.deepTeal)
                        }
                        ProgressView(value: Double(currentStepIndex + 1), total: Double(steps.count))
                            .tint(SalahTheme.teal)
                    }
                    .padding(12)
                    .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                    .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }

                    wuduStepCard(steps[currentStepIndex])

                    HStack(spacing: 12) {
                        Button {
                            guard currentStepIndex > 0 else { return }
                            currentStepIndex -= 1
                            withAnimation(.easeInOut(duration: 0.2)) {
                                proxy.scrollTo("wudu-step-top", anchor: .top)
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
                                proxy.scrollTo("wudu-step-top", anchor: .top)
                            }
                        } label: {
                            HStack {
                                Text(currentStepIndex == steps.count - 1 ? settings.t("Wudu fertig", "Abdest tamam") : settings.t("Weiter", "İleri"))
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

                    if currentStepIndex == steps.count - 1 {
                        VStack(alignment: .leading, spacing: 8) {
                            Text(settings.t("Nach dem Wudu", "Abdestten sonra"))
                                .font(.headline)
                            Text("أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ")
                                .font(.title3)
                                .multilineTextAlignment(.trailing)
                                .frame(maxWidth: .infinity, alignment: .trailing)
                            Text("Eşhedü en lâ ilâhe illallâhü vahdehû lâ şerîke leh, ve eşhedü enne Muhammeden abdühû ve resûlüh.")
                                .font(.subheadline.weight(.semibold))
                            Text(settings.t(
                                "Ich bezeuge, dass es keinen Gott außer Allah gibt, ohne Teilhaber, und dass Muhammad Sein Diener und Gesandter ist.",
                                "Allah'tan başka ilâh olmadığına, O'nun ortağı bulunmadığına ve Muhammed'in O'nun kulu ve elçisi olduğuna şahitlik ederim."
                            ))
                            .font(.footnote)
                            .foregroundStyle(.secondary)
                        }
                        .cardStyle()
                    }

                    VStack(alignment: .leading, spacing: 7) {
                        Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama"))
                            .font(.headline)
                        Text(settings.t(
                            "Diyanet Namaz İlmihali und Din İşleri Yüksek Kurulu. Die vier Farz-Bestandteile und die vollständige hanafitische Lernreihenfolge werden direkt in SalahPath erklärt. Nacken/Ense ist hier als Sunnah dargestellt, nicht als Farz.",
                            "Diyanet Namaz İlmihali ve Din İşleri Yüksek Kurulu. Abdestin dört farzı ve tam Hanefî öğrenme sırası doğrudan SalahPath içinde açıklanır. Boyun/ense burada sünnet olarak gösterilir, farz değildir."
                        ))
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    }
                    .cardStyle(material: true)
                }
                .padding()
            }
            .background(SalahTheme.page)
            .navigationTitle(settings.t("Wudu lernen", "Abdest öğren"))
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    @ViewBuilder
    private func wuduStepCard(_ step: WuduTutorialStep) -> some View {
        VStack(spacing: 0) {
            HStack(spacing: 12) {
                Text("\(step.number)")
                    .font(.title3.bold())
                    .frame(width: 40, height: 40)
                    .background(SalahTheme.gold.opacity(0.95), in: Circle())
                    .foregroundStyle(SalahTheme.deepTeal)

                Text(settings.language == .german ? step.deTitle : step.trTitle)
                    .font(.title3.bold())
                    .foregroundStyle(.white)
                    .fixedSize(horizontal: false, vertical: true)

                Spacer(minLength: 6)

                Text(repeatLabel(for: step))
                    .font(.caption.bold())
                    .multilineTextAlignment(.trailing)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 5)
                    .background(Color.white.opacity(0.92), in: Capsule())
                    .foregroundStyle(SalahTheme.deepTeal)
            }
            .padding(14)
            .background(SalahTheme.deepTeal)

            VStack(alignment: .leading, spacing: 14) {
                if let image = step.image {
                    WuduInstructionVisual(key: image, stepNumber: step.number)
                        .accessibilityElement(children: .ignore)
                        .accessibilityLabel(accessibilityDescription(for: step))
                }

                VStack(alignment: .leading, spacing: 6) {
                    Label(settings.t("SO MACHST DU ES", "BÖYLE YAP"), systemImage: "hand.point.right.fill")
                        .font(.caption.bold())
                        .foregroundStyle(SalahTheme.teal)
                    Text(settings.language == .german ? step.deAction : step.trAction)
                        .font(.body)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                }

                DisclosureGroup(isExpanded: $showExactDetail) {
                    Text(exactDetail(for: step.number))
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.mutedInk)
                        .fixedSize(horizontal: false, vertical: true)
                        .padding(.top, 5)
                } label: {
                    Label(settings.t("Ganz genau", "Ayrıntılı anlatım"), systemImage: "magnifyingglass")
                        .font(.subheadline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                }
            }
            .padding(16)
            .background(SalahTheme.cream)
        }
        .clipShape(RoundedRectangle(cornerRadius: 22, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 22, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.65), lineWidth: 1)
        }
    }

    private func repeatLabel(for step: WuduTutorialStep) -> String {
        if [6, 7, 8, 12, 13].contains(step.number) {
            return settings.t("1× Farz · 3× Sunnah", "1× Farz · 3× Sünnet")
        }
        if step.number == 9 { return "1×" }
        if let repeatText = step.repeatText {
            return settings.t("\(repeatText) Sunnah", "\(repeatText) Sünnet")
        }
        return settings.t("Sunnah", "Sünnet")
    }

    private func exactDetail(for number: Int) -> String {
        let de: [Int: String] = [
            1: "Die Absicht ist im Herzen. Du musst keinen bestimmten deutschen oder arabischen Satz laut sprechen.",
            2: "Sprich Bismillāh vor dem eigentlichen Waschen. Es ist in dieser hanafitischen Lernreihenfolge Sunnah, nicht einer der vier Farz-Bestandteile.",
            3: "Wasche Handflächen, Handrücken, Finger und Fingerzwischenräume bis einschließlich Handgelenk. Schmuck darf Wasser nicht von der Haut abhalten.",
            4: "Nimm Wasser mit der rechten Hand in den Mund und spüle gründlich. Beim Fasten nicht übertreiben, damit kein Wasser geschluckt wird.",
            5: "Ziehe Wasser vorsichtig in die Nase. Reinige die Nase; beim Fasten nicht tief hochziehen, damit kein Wasser in den Rachen gelangt.",
            6: "Gesichtsgrenze: oben der normale Haaransatz, unten das Kinn, seitlich ungefähr von Ohr zu Ohr. Wasser muss die gesamte zu waschende Haut erreichen. Bei dichtem Bart die Haare mit den Fingern durchfahren, damit Wasser gut verteilt wird.",
            7: "Beginne bei der rechten Hand und wasche bis über den Ellenbogen. Drehe den Arm so, dass Innen- und Außenseite sowie der Ellenbogen sicher nass werden.",
            8: "Genauso links: von der Hand bis einschließlich Ellenbogen. Kontrolliere besonders den Ellenbogen und Stellen unter eng anliegendem Schmuck.",
            9: "Masah bedeutet wischen, nicht den Kopf wie das Gesicht waschen. Die Hände sind feucht. Hanafi: mindestens ein Viertel des Kopfes ist Farz; die vollständige Kopf-Masah wird als Sunnah gezeigt.",
            10: "Mit feuchten Fingern die Innenbereiche der Ohren vorsichtig wischen, außen mit den Daumen. Kein Wasser tief in den Gehörgang drücken.",
            11: "Dieser Schritt ist NICHT Farz. In der Diyanet/Hanafi-Darstellung wird die Ense/Nackenpartie mit feuchten Fingerrücken gewischt. Die Vorderseite des Halses bzw. Kehle nicht wischen.",
            12: "Wasche Oberseite, Sohle, Ferse, beide Knöchel und die Zehenzwischenräume. Erst wenn überall Wasser angekommen ist, ist der Fuß vollständig gewaschen.",
            13: "Wie beim rechten Fuß: Oberseite, Sohle, Ferse, beide Knöchel und alle Zehenzwischenräume vollständig erreichen."
        ]
        let tr: [Int: String] = [
            1: "Niyet kalptedir. Belirli bir Türkçe veya Arapça cümleyi sesli söylemek zorunda değilsin.",
            2: "Asıl yıkamaya başlamadan önce Bismillāh de. Bu Hanefî öğrenme sıralamasında sünnettir; dört farzdan biri değildir.",
            3: "Avuçları, el üstlerini, parmakları ve parmak aralarını bileklerle birlikte yıka. Takı suyun deriye ulaşmasını engellememeli.",
            4: "Sağ elle ağza su alıp iyice çalkala. Oruçluyken suyun yutulmaması için aşırıya kaçma.",
            5: "Burnuna dikkatlice su ver ve temizle. Oruçluyken suyun boğaza kaçmaması için derine çekme.",
            6: "Yüz sınırı: normal saç çizgisinden çeneye, yanlarda yaklaşık bir kulaktan diğer kulağa kadar. Yıkanması gereken her yere su ulaşmalı. Sık sakalda suyun iyi dağılması için parmaklarla arala.",
            7: "Sağ elden başlayıp dirsek dahil kolu yıka. Kolun içi, dışı ve dirseğin tamamen ıslandığından emin ol.",
            8: "Aynı şekilde sol eli ve kolu dirsek dahil yıka. Özellikle dirsek ve sıkı takı altlarını kontrol et.",
            9: "Mesh, başı yüz gibi yıkamak değil, ıslak elle silmektir. Hanefî: başın en az dörtte birini mesh etmek farzdır; tam baş meshi sünnet olarak gösterilir.",
            10: "Islak parmaklarla kulakların iç kısmını nazikçe, dışını başparmaklarla mesh et. Suyu kulak kanalına derin itme.",
            11: "Bu adım farz DEĞİLDİR. Diyanet/Hanefî anlatımında ense ıslak parmakların dış kısmıyla mesh edilir. Boğazın ön tarafı mesh edilmez.",
            12: "Ayağın üstünü, tabanını, topuğunu, iki aşık kemiğini ve parmak aralarını yıka. Her yere su ulaşınca ayak tamamen yıkanmış olur.",
            13: "Sağ ayakta olduğu gibi ayağın üstü, tabanı, topuğu, iki aşık kemiği ve bütün parmak aralarına su ulaştır."
        ]
        return settings.language == .german ? (de[number] ?? "") : (tr[number] ?? "")
    }

    private func accessibilityDescription(for step: WuduTutorialStep) -> String {
        settings.language == .german
            ? "Wudu Schritt \(step.number): \(step.deTitle). \(step.deAction)"
            : "Abdest adım \(step.number): \(step.trTitle). \(step.trAction)"
    }
'''

text = text[:body_start] + new_body + text[struct_end:]
guide.write_text(text, encoding="utf-8")
print("v398 applied: guided Wudu with exact beginner details and clear Farz/Sunnah labeling")
