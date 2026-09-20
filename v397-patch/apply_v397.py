from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
text = guide.read_text(encoding="utf-8")

start_marker = "struct HanafiPrayerPlanView: View {"
end_marker = "\nprivate struct QunutDuaView: View {"
if start_marker not in text or end_marker not in text:
    raise SystemExit("v397: HanafiPrayerPlanView anchors missing")

start = text.index(start_marker)
end = text.index(end_marker, start)

new_struct = r'''struct HanafiPrayerPlanView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var showSpecialCases = false

    private struct PlanRow: Identifiable {
        let id = UUID()
        let de: String
        let tr: String
        let sequence: String
        let deNote: String
        let trNote: String
    }

    private let rows: [PlanRow] = [
        .init(de: "Fajr", tr: "Sabah", sequence: "2 Sunnah → 2 Fard", deNote: "Die 2 Sunnah vor Fajr sind Sunnah mu'akkadah.", trNote: "Farzdan önceki 2 rekât sünnet-i müekkededir."),
        .init(de: "Dhuhr", tr: "Öğle", sequence: "4 Sunnah → 4 Fard → 2 Sunnah", deNote: "Die erste 4er-Sunnah und die 2 Sunnah danach sind besonders betonte Sunnah.", trNote: "Önceki 4 ve sonraki 2 rekât kuvvetli sünnetlerdendir."),
        .init(de: "Asr", tr: "İkindi", sequence: "4 Sunnah → 4 Fard", deNote: "Die 4 Sunnah davor gelten als ghayr mu'akkadah.", trNote: "Önceki 4 rekât sünnet gayr-i müekkededir."),
        .init(de: "Maghrib", tr: "Akşam", sequence: "3 Fard → 2 Sunnah", deNote: "Nach den 3 Fard folgen 2 Sunnah.", trNote: "3 rekât farzdan sonra 2 rekât sünnet kılınır."),
        .init(de: "Isha", tr: "Yatsı", sequence: "4 Sunnah → 4 Fard → 2 Sunnah → 3 Witr", deNote: "Die ersten 4 sind ghayr mu'akkadah; die 2 danach mu'akkadah. Witr ist hanafitisch wajib.", trNote: "İlk 4 gayr-i müekkede, sonraki 2 müekkede sünnettir. Vitir Hanefî fıkhında vaciptir.")
    ]

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 9) {
                    Label(settings.t("Was bedeutet Rakʿa?", "Rekât ne demek?"), systemImage: "1.circle.fill")
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Eine Rakʿa ist EIN kompletter Gebetsdurchgang. Stell dir vor, du gehst immer dieselbe kleine Runde durch. Erst nach dem zweiten Sujud ist diese Runde fertig.",
                        "Bir rekât, namazın TAM bir bölümüdür. Her rekâtta aynı temel sıra tekrar eder. İkinci secde bittikten sonra bir rekât tamamlanır."
                    ))
                    .font(.subheadline)
                    .fixedSize(horizontal: false, vertical: true)
                    Text(settings.t(
                        "Beim allerersten Rakʿa beginnt das Gebet vorher mit dem Eröffnungstakbir. Danach kommt der folgende Grundablauf.",
                        "İlk rekâtta bu sıradan önce iftitah tekbiriyle namaza başlanır. Sonra aşağıdaki temel akış gelir."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("1 Rakʿa ganz langsam", "1 rekâtı yavaşça öğren"))
                        .font(.title3.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    flowRow("1", settings.t("Stehen und lesen", "Ayakta dur ve oku"), settings.t("Stehe zur Qibla. Lies die vorgeschriebenen Texte dieser Rakʿa.", "Kıbleye dönük dur. Bu rekâtta okunacak metinleri oku."), "person.fill")
                    flowRow("2", settings.t("Rukūʿ", "Rükû"), settings.t("Sage Allāhu akbar, beuge dich und bleib kurz ruhig im Rukūʿ.", "Allāhu ekber de, rükûya eğil ve kısa bir an sakin kal."), "arrow.down.forward")
                    flowRow("3", settings.t("Ganz aufrichten", "Tam doğrul"), settings.t("Komm vollständig hoch und steh kurz ruhig. Nicht direkt in den Sujud gehen.", "Tamamen doğrul ve kısa bir an ayakta sakin kal. Doğrudan secdeye geçme."), "arrow.up")
                    flowRow("4", settings.t("Sujud 1", "1. secde"), settings.t("Gehe in den ersten Sujud und bleib kurz ruhig.", "Birinci secdeye git ve kısa bir an sakin kal."), "arrow.down")
                    flowRow("5", settings.t("Sitzen", "Otur"), settings.t("Setze dich vollständig zwischen den beiden Sujud.", "İki secde arasında tamamen otur."), "figure.seated.side")
                    flowRow("6", settings.t("Sujud 2", "2. secde"), settings.t("Mache den zweiten Sujud genauso ruhig wie den ersten.", "İkinci secdeyi birincisi gibi sakin şekilde yap."), "arrow.down")
                    HStack(alignment: .top, spacing: 10) {
                        Image(systemName: "checkmark.circle.fill")
                            .font(.title2)
                            .foregroundStyle(.green)
                        Text(settings.t(
                            "JETZT ist 1 Rakʿa fertig. Erst jetzt entscheidest du: zur nächsten Rakʿa aufstehen oder zum vorgesehenen Sitzen übergehen.",
                            "ŞİMDİ 1 rekât tamamlandı. Ancak şimdi karar verilir: sonraki rekâta kalk veya gereken oturuşa geç."
                        ))
                        .font(.subheadline.bold())
                        .fixedSize(horizontal: false, vertical: true)
                    }
                    .padding(11)
                    .background(Color.green.opacity(0.09), in: RoundedRectangle(cornerRadius: 13, style: .continuous))
                }
                .cardStyle()

                planCard(
                    title: settings.t("2 Rakʿa", "2 rekât"),
                    subtitle: settings.t("Beispiel: Fajr-Fard und viele 2er-Sunnah-Gebete", "Örnek: Sabah farzı ve birçok 2 rekât sünnet"),
                    lines: settings.language == .german ? [
                        "Rakʿa 1 komplett machen. Nach Sujud 2 wieder aufstehen.",
                        "Rakʿa 2 komplett machen. Nach Sujud 2 NICHT mehr aufstehen.",
                        "Im letzten Sitzen: Ettehiyyâtü → Salli → Bârik → Abschlussdua.",
                        "Dann Salam: nur den Kopf nach rechts, danach nur den Kopf nach links. Der Körper bleibt zur Qibla."
                    ] : [
                        "1. rekâtı tamamla. 2. secdeden sonra yeniden ayağa kalk.",
                        "2. rekâtı tamamla. 2. secdeden sonra artık ayağa kalkma.",
                        "Son oturuşta: Ettehiyyâtü → Salli → Bârik → kapanış duası.",
                        "Sonra selâm: yalnız baş sağa, ardından yalnız baş sola döner. Gövde kıbleye dönük kalır."
                    ]
                )

                planCard(
                    title: settings.t("3 Rakʿa Fard", "3 rekât farz"),
                    subtitle: settings.t("Beispiel: Maghrib-Fard", "Örnek: Akşam farzı"),
                    lines: settings.language == .german ? [
                        "Rakʿa 1 komplett machen und zu Rakʿa 2 aufstehen.",
                        "Rakʿa 2 komplett machen. Danach sitzen und Ettehiyyâtü lesen.",
                        "Nach Ettehiyyâtü mit Allāhu akbar zu Rakʿa 3 aufstehen.",
                        "Rakʿa 3: Basmala + Al-Fātiha; bei diesem Fard keine Zusatzsura nötig. Dann Rukūʿ, Aufrichten, Sujud 1, Sitzen, Sujud 2.",
                        "Danach letztes Sitzen vollständig und Salam rechts, dann links."
                    ] : [
                        "1. rekâtı tamamla ve 2. rekâta kalk.",
                        "2. rekâtı tamamla. Sonra otur ve Ettehiyyâtü oku.",
                        "Ettehiyyâtü'den sonra Allāhu ekber diyerek 3. rekâta kalk.",
                        "3. rekât: Besmele + Fâtiha; bu farzda zamm-ı sûre gerekmez. Sonra rükû, doğrulma, 1. secde, oturuş, 2. secde.",
                        "Sonra tam son oturuş ve sağa, ardından sola selâm."
                    ]
                )

                planCard(
                    title: settings.t("4 Rakʿa Fard", "4 rekât farz"),
                    subtitle: settings.t("Beispiel: Dhuhr, Asr und Isha-Fard", "Örnek: Öğle, İkindi ve Yatsı farzı"),
                    lines: settings.language == .german ? [
                        "Rakʿa 1 komplett machen und zu Rakʿa 2 aufstehen.",
                        "Rakʿa 2 komplett machen. Danach sitzen und Ettehiyyâtü lesen.",
                        "Zu Rakʿa 3 aufstehen. Dort Basmala + Al-Fātiha lesen, dann die Rakʿa vollständig beenden.",
                        "Zu Rakʿa 4 aufstehen. Wieder Basmala + Al-Fātiha lesen, dann Rukūʿ, Aufrichten und beide Sujud.",
                        "Nach Rakʿa 4 letztes Sitzen: Ettehiyyâtü → Salli → Bârik → Abschlussdua → Salam rechts und links."
                    ] : [
                        "1. rekâtı tamamla ve 2. rekâta kalk.",
                        "2. rekâtı tamamla. Sonra otur ve Ettehiyyâtü oku.",
                        "3. rekâta kalk. Besmele + Fâtiha oku ve rekâtı tamamla.",
                        "4. rekâta kalk. Yine Besmele + Fâtiha oku; sonra rükû, doğrulma ve iki secdeyi tamamla.",
                        "4. rekâttan sonra son oturuş: Ettehiyyâtü → Salli → Bârik → kapanış duası → sağa ve sola selâm."
                    ]
                )

                DisclosureGroup(isExpanded: $showSpecialCases) {
                    VStack(alignment: .leading, spacing: 12) {
                        Text(settings.t(
                            "4-Rakʿa-Sunnah: In allen Rakʿa werden Al-Fātiha und eine Zusatzsura gelesen. Bei der betonten 4er-Sunnah von Dhuhr liest man im ersten Sitzen Ettehiyyâtü und steht auf. Bei den 4 ghayr-mu'akkadah vor Asr/Isha werden im ersten Sitzen zusätzlich Salli/Bârik gelesen; Rakʿa 3 beginnt wieder mit Sübhaneke.",
                            "4 rekât sünnet: Her rekâtta Fâtiha ve zamm-ı sûre okunur. Öğlenin kuvvetli 4 rekât sünnetinde ilk oturuşta Ettehiyyâtü okunup kalkılır. İkindi/Yatsı öncesi 4 gayr-i müekkede sünnette ilk oturuşta Salli/Bârik de okunur; 3. rekâta yeniden Sübhâneke ile başlanır."
                        ))
                        .font(.subheadline)

                        Text(settings.t(
                            "Witr (hanafitisch): 3 Rakʿa. In Rakʿa 3 werden nach Fātiha und Zusatzsura vor dem Rukūʿ erneut die Hände gehoben, Allāhu akbar gesagt, die Hände wieder gebunden und die Qunūt-Duas gelesen.",
                            "Vitir (Hanefî): 3 rekât. 3. rekâtta Fâtiha ve zamm-ı sûreden sonra rükûdan önce eller tekrar kaldırılır, Allāhu ekber denir, eller yeniden bağlanır ve Kunut duaları okunur."
                        ))
                        .font(.subheadline)

                        NavigationLink { QunutDuaView() } label: {
                            Label(settings.t("Qunūt-Duas vollständig", "Kunut duaları tam metin"), systemImage: "text.book.closed")
                                .font(.headline)
                        }
                    }
                    .padding(.top, 8)
                } label: {
                    Label(settings.t("Sonderfälle: 4er-Sunnah & Witr", "Özel durumlar: 4 rekât sünnet ve vitir"), systemImage: "chevron.down.circle")
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                }
                .padding(14)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 16).stroke(SalahTheme.gold.opacity(0.42), lineWidth: 1) }

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Wie viele Rakʿa haben die täglichen Gebete?", "Günlük namazlar kaç rekât?"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    ForEach(rows) { row in
                        VStack(alignment: .leading, spacing: 4) {
                            HStack {
                                Text(settings.language == .german ? row.de : row.tr).font(.headline)
                                Spacer()
                                Text(row.sequence).font(.subheadline.bold()).foregroundStyle(SalahTheme.teal)
                            }
                            Text(settings.language == .german ? row.deNote : row.trNote)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        .padding(.vertical, 4)
                        if row.id != rows.last?.id { Divider() }
                    }
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 6) {
                    Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama")).font(.headline)
                    Text(settings.t(
                        "Diyanet Namaz İlmihali · hanafitische Grunddarstellung. Andere Rechtsschulen können einzelne Sunnah-Details anders einordnen.",
                        "Diyanet Namaz İlmihali · Hanefî temel anlatım. Diğer mezhepler bazı sünnet ayrıntılarını farklı değerlendirebilir."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Rakʿa verstehen", "Rekâtı anla"))
        .navigationBarTitleDisplayMode(.inline)
    }

    private func flowRow(_ number: String, _ title: String, _ detail: String, _ icon: String) -> some View {
        HStack(alignment: .top, spacing: 11) {
            ZStack {
                Circle().fill(SalahTheme.gold.opacity(0.20)).frame(width: 34, height: 34)
                Text(number).font(.headline.bold()).foregroundStyle(SalahTheme.deepTeal)
            }
            VStack(alignment: .leading, spacing: 3) {
                Label(title, systemImage: icon)
                    .font(.headline)
                    .foregroundStyle(SalahTheme.ink)
                Text(detail)
                    .font(.subheadline)
                    .foregroundStyle(SalahTheme.mutedInk)
                    .fixedSize(horizontal: false, vertical: true)
            }
            Spacer(minLength: 0)
        }
    }

    private func planCard(title: String, subtitle: String, lines: [String]) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title)
                .font(.title3.bold())
                .foregroundStyle(SalahTheme.deepTeal)
            Text(subtitle)
                .font(.caption.bold())
                .foregroundStyle(SalahTheme.teal)
            ForEach(Array(lines.enumerated()), id: .offset) { index, line in
                HStack(alignment: .top, spacing: 10) {
                    Text("\(index + 1)")
                        .font(.caption.bold())
                        .foregroundStyle(.white)
                        .frame(width: 24, height: 24)
                        .background(SalahTheme.teal, in: Circle())
                    Text(line)
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                    Spacer(minLength: 0)
                }
            }
        }
        .cardStyle()
    }
}
'''

guide.write_text(text[:start] + new_struct + text[end:], encoding="utf-8")
print("v397 applied: child-friendly Rakʿa explanation + progressive disclosure")
