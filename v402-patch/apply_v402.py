from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

start_marker = "struct FastingTrackerView: View {"
end_marker = "\n// MARK: - Hijri calendar"
if start_marker not in text or end_marker not in text:
    raise SystemExit("v402: fasting section anchors missing")

start = text.index(start_marker)
end = text.index(end_marker, start)

new_section = r'''struct FastingTrackerView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var refresh = 0
    private let calendar = Calendar.current
    private let hijri = Calendar(identifier: .islamicUmmAlQura)

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 9) {
                    Label(settings.t("Fasten & Ramadan", "Oruç ve Ramazan"), systemImage: "moon.stars.fill")
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Hier lernst du das Fasten von Anfang an: wann es beginnt und endet, was es ungültig macht, was nur die Belohnung schädigt und welche Erleichterungen es bei Krankheit, Reise oder anderen Gründen gibt.",
                        "Burada orucu en baştan öğrenirsin: ne zaman başlayıp bittiğini, nelerin orucu bozduğunu, nelerin sevabını azalttığını ve hastalık, yolculuk gibi durumlarda hangi ruhsatların bulunduğunu."
                    ))
                    .font(.subheadline)
                    .fixedSize(horizontal: false, vertical: true)

                    if hijri.component(.month, from: Date()) == 9 {
                        let day = hijri.component(.day, from: Date())
                        Label(
                            settings.t("Ramadan · Tag \(day)", "Ramazan · \(day). gün"),
                            systemImage: "sparkles"
                        )
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.teal)
                    }
                }
                .cardStyle(material: true)

                fastingNavigationCard(
                    title: settings.t("1 · Fasten ganz einfach", "1 · Orucu en kolay şekilde öğren"),
                    subtitle: settings.t("Niyyah, Suhoor, Fajr, Tagesablauf und Iftar", "Niyet, sahur, imsak, günün akışı ve iftar"),
                    icon: "1.circle.fill",
                    destination: AnyView(FastingBasicsView())
                )

                fastingNavigationCard(
                    title: settings.t("2 · Was bricht das Fasten?", "2 · Orucu neler bozar?"),
                    subtitle: settings.t("Klare Beispiele, Qada, Kaffarah und häufige Fragen", "Açık örnekler, kaza, kefaret ve sık sorulanlar"),
                    icon: "2.circle.fill",
                    destination: AnyView(FastingRulesView())
                )

                fastingNavigationCard(
                    title: settings.t("3 · Krankheit, Reise & besondere Situationen", "3 · Hastalık, yolculuk ve özel durumlar"),
                    subtitle: settings.t("Wann verschieben? Wann Qada? Wann Fidya?", "Ne zaman erteleme, kaza veya fidye gerekir?"),
                    icon: "3.circle.fill",
                    destination: AnyView(FastingExceptionsView())
                )

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Mein Fasten-Tracker", "Oruç takibim"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Toggle(isOn: Binding(
                        get: { FastingStore.contains(Date()) },
                        set: { _ in FastingStore.toggle(Date()); refresh += 1 }
                    )) {
                        Label(settings.t("Heute als Fastentag markieren", "Bugünü oruç günü olarak işaretle"), systemImage: "checkmark.circle")
                    }

                    Text(settings.t(
                        "Der Tracker speichert nur deine persönliche Liste lokal auf diesem Gerät. Er entscheidet nicht, ob ein Fasten religiös gültig oder verpflichtend ist.",
                        "Takip bölümü yalnız kişisel listenizi bu cihazda yerel olarak saklar. Bir orucun dinen geçerli veya zorunlu olup olmadığına karar vermez."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 8) {
                    Text(settings.t("Letzte 14 Tage", "Son 14 gün"))
                        .font(.headline.bold())
                    ForEach(lastDays, id: .self) { day in
                        Button {
                            FastingStore.toggle(day)
                            refresh += 1
                        } label: {
                            HStack {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(gregorianDateString(day, language: settings.language))
                                        .foregroundStyle(SalahTheme.ink)
                                    Text(hijriDateString(day, language: settings.language))
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                                Spacer()
                                Image(systemName: FastingStore.contains(day) ? "checkmark.circle.fill" : "circle")
                                    .foregroundStyle(FastingStore.contains(day) ? .green : .secondary)
                            }
                            .contentShape(Rectangle())
                        }
                        .buttonStyle(.plain)
                        if day != lastDays.last { Divider() }
                    }
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 6) {
                    Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama"))
                        .font(.headline)
                    Text(settings.t(
                        "Die Lerntexte orientieren sich an Diyanet / Din İşleri Yüksek Kurulu und der hanafitischen Grunddarstellung. Wo eine relevante Rechtsschul-Differenz besteht, wird sie ausdrücklich genannt.",
                        "Öğrenme metinleri Diyanet / Din İşleri Yüksek Kurulu ve Hanefî temel anlatımına dayanır. Önemli bir mezhep farkı varsa açıkça belirtilir."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Fasten & Ramadan", "Oruç ve Ramazan"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func fastingNavigationCard(title: String, subtitle: String, icon: String, destination: AnyView) -> some View {
        NavigationLink { destination } label: {
            HStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundStyle(SalahTheme.gold)
                    .frame(width: 44, height: 44)
                    .background(SalahTheme.deepTeal, in: Circle())
                VStack(alignment: .leading, spacing: 4) {
                    Text(title)
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(subtitle)
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.mutedInk)
                        .fixedSize(horizontal: false, vertical: true)
                }
                Spacer()
                Image(systemName: "chevron.right")
                    .font(.headline.bold())
                    .foregroundStyle(SalahTheme.teal)
            }
            .cardStyle()
        }
        .buttonStyle(.plain)
    }

    private var lastDays: [Date] {
        (0..<14).compactMap { calendar.date(byAdding: .day, value: -$0, to: calendar.startOfDay(for: Date())) }
    }
}

private struct FastingBasicsView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section(settings.t("Was bedeutet Fasten?", "Oruç nedir?")) {
                learningText(
                    settings.t("Ganz einfach", "En basit haliyle"),
                    settings.t(
                        "Beim islamischen Fasten verzichtest du mit der Absicht des Fastens vom Beginn des Fajr-Zeitpunkts bis zum Sonnenuntergang auf Essen, Trinken und sexuelle Beziehungen.",
                        "İslâmî oruçta, oruç niyetiyle fecrin başlangıcından güneş batıncaya kadar yeme, içme ve cinsel ilişkiden uzak durulur."
                    )
                )
                learningText(
                    settings.t("Wann beginnt es?", "Ne zaman başlar?"),
                    settings.t(
                        "Das Fasten beginnt mit dem echten Fajr / Im­sak. Suhoor muss vorher beendet sein. 'Sonnenaufgang' ist zu spät.",
                        "Oruç fecr-i sâdık / imsak ile başlar. Sahur bundan önce bitmiş olmalıdır. Güneşin doğuşunu beklemek doğru değildir."
                    )
                )
                learningText(
                    settings.t("Wann endet es?", "Ne zaman biter?"),
                    settings.t(
                        "Sobald die Sonne vollständig untergegangen ist, beginnt die Maghrib-Zeit und du darfst das Fasten brechen.",
                        "Güneş tamamen battığında akşam vakti girer ve oruç açılabilir."
                    )
                )
            }

            Section(settings.t("Niyyah / Absicht", "Niyet")) {
                Text(settings.t(
                    "Die Absicht ist Voraussetzung. Die Absicht im Herzen reicht. Für jeden Ramadan-Tag wird neu beabsichtigt zu fasten; schon das bewusste Aufstehen zum Suhoor kann die Absicht ausdrücken.",
                    "Niyet orucun şartıdır. Kalpten niyet etmek yeterlidir. Ramazan'ın her günü için yeniden niyet edilir; sahura oruç tutmak amacıyla kalkmak da niyet sayılabilir."
                ))
                .fixedSize(horizontal: false, vertical: true)

                Text(settings.t(
                    "Hanafi/Diyanet: Für Ramadan kann unter bestimmten Voraussetzungen auch nach Imsak bis vor die islamische Mittagsgrenze niyet gemacht werden, sofern seit Fajr nichts Fastenwidriges getan wurde. Sicherer und besser ist die Absicht in der Nacht. Andere Rechtsschulen können hier strenger sein.",
                    "Hanefî/Diyanet: Ramazan orucuna, imsaktan sonra oruca aykırı bir şey yapılmamışsa belirli şartlarla gündüz kuşluk/öğle sınırından önce de niyet edilebilir. Geceden niyet etmek daha güvenli ve faziletlidir. Diğer mezheplerde hüküm daha sıkı olabilir."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Ein Fastentag Schritt für Schritt", "Bir oruç günü adım adım")) {
                numbered("1", settings.t("Vor Fajr: Suhoor essen und trinken. Nicht bis zur letzten Sekunde hetzen.", "Fecrden önce: Sahur yap, ye ve iç. Son saniyeye bırakma."))
                numbered("2", settings.t("Absicht im Herzen: Heute faste ich den Ramadan-Tag für Allah.", "Kalben niyet et: Bugünkü Ramazan orucunu Allah için tutuyorum."))
                numbered("3", settings.t("Ab Fajr: nichts essen oder trinken und die Fastenregeln einhalten.", "Fecrden itibaren: yeme-içmeyi bırak ve oruç hükümlerine uy."))
                numbered("4", settings.t("Tagsüber: Gebete, Quran, Dhikr, Dua, gute Taten und gutes Verhalten pflegen.", "Gündüz: namaz, Kur'an, zikir, dua, iyi ameller ve güzel ahlâka özen göster."))
                numbered("5", settings.t("Bei Sonnenuntergang: Iftar. Danach Maghrib nicht unnötig hinauszögern.", "Güneş batınca: İftar et. Ardından akşam namazını gereksiz yere geciktirme."))
            }

            Section(settings.t("Verhalten im Ramadan", "Ramazan'da davranış")) {
                Text(settings.t(
                    "Fasten bedeutet mehr als Hunger und Durst. Lügen, Beleidigungen, Streit, üble Nachrede und andere Sünden widersprechen dem Sinn des Fastens und können seinen Lohn stark schmälern. Sie machen den Fastentag aber nicht automatisch in jedem Fall fiqh-rechtlich ungültig. Deshalb trennt SalahPath 'Fasten ungültig' von 'Belohnung schädigen'.",
                    "Oruç yalnız açlık ve susuzluk değildir. Yalan, hakaret, kavga, gıybet ve diğer günahlar orucun ruhuna aykırıdır ve sevabını ciddi şekilde azaltabilir. Ancak bunlar her durumda fıkhen orucu otomatik olarak bozmaz. Bu nedenle SalahPath 'orucu bozar' ile 'sevabını azaltır' ifadelerini ayırır."
                ))
                .fixedSize(horizontal: false, vertical: true)
            }

            Section(settings.t("Quelle", "Kaynak")) {
                Text(settings.t(
                    "Diyanet / Din İşleri Yüksek Kurulu · Orucun mahiyeti, niyet, sünnetler ve adab.",
                    "Diyanet / Din İşleri Yüksek Kurulu · Orucun mahiyeti, niyet, sünnetleri ve adabı."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Fasten lernen", "Orucu öğren"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func learningText(_ title: String, _ text: String) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title).font(.headline)
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }

    @ViewBuilder
    private func numbered(_ number: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Text(number)
                .font(.caption.bold())
                .foregroundStyle(.white)
                .frame(width: 24, height: 24)
                .background(SalahTheme.teal, in: Circle())
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }
}

private struct FastingRulesView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section(settings.t("Grundregel", "Temel kural")) {
                Text(settings.t(
                    "Bewusstes Essen, Trinken oder Geschlechtsverkehr während eines begonnenen Ramadan-Fastens macht das Fasten ungültig. Ob nur Qada oder zusätzlich Kaffarah nötig ist, hängt vom konkreten Fall ab.",
                    "Başlanmış Ramazan orucunda bilerek yemek, içmek veya cinsel ilişki orucu bozar. Yalnız kaza mı yoksa ayrıca kefaret mi gerektiği somut duruma göre değişir."
                ))
            }

            Section(settings.t("Bricht das Fasten", "Orucu bozar")) {
                rule("fork.knife", settings.t("Bewusst essen oder trinken", "Bilerek yemek veya içmek"), settings.t("Bei absichtlichem Bruch eines gültig begonnenen Ramadan-Fastens kann nach hanafitischer Einordnung zusätzlich zur Qada auch Kaffarah nötig sein.", "Geçerli başlanmış Ramazan orucunun bilerek bozulmasında Hanefî hükme göre kazaya ek olarak kefaret de gerekebilir."))
                rule("smoke.fill", settings.t("Rauchen / Nargile", "Sigara / nargile"), settings.t("Das Fasten wird dadurch ungültig.", "Oruç bozulur."))
                rule("drop.triangle.fill", settings.t("Nährende Infusionen / Nahrung über den Körper", "Besleyici serum / gıda niteliğinde uygulamalar"), settings.t("Nährende oder gıdaähnliche Zuführung bricht nach Diyanet das Fasten; medizinische Einzelfälle separat prüfen.", "Besleyici veya gıda hükmündeki uygulamalar Diyanet'e göre orucu bozar; tıbbî özel durumlar ayrıca değerlendirilmelidir."))
                rule("arrow.uturn.down", settings.t("Absichtlich mundvoll erbrechen", "Kasten ağız dolusu kusmak"), settings.t("Erfordert nach der hanafitischen Darstellung Qada.", "Hanefî anlatıma göre kaza gerekir."))
                rule("drop.fill", settings.t("Beim Wudu versehentlich Wasser schlucken", "Abdestte yanlışlıkla su yutmak"), settings.t("Wenn du wusstest, dass du fastest, und Wasser versehentlich in den Rachen gelangt, gilt das im Hanafi/Diyanet-Ablauf als gebrochen und Qada ist nötig. Shafi'i kann hier anders urteilen.", "Oruçlu olduğunu bilirken abdest suyunun yanlışlıkla boğaza kaçması Hanefî/Diyanet hükmünde orucu bozar ve kaza gerekir. Şafiî mezhebinde hüküm farklı olabilir."))
            }

            Section(settings.t("Bricht nicht automatisch", "Otomatik olarak bozmaz")) {
                rule("brain.head.profile", settings.t("Vergessen essen oder trinken", "Unutarak yemek veya içmek"), settings.t("Bricht das Fasten nicht. Sobald du dich erinnerst, sofort aufhören und weiterfasten.", "Orucu bozmaz. Hatırlayınca hemen bırak ve oruca devam et."))
                rule("cross.case.fill", settings.t("Nicht nährende Spritze / Impfung", "Besleyici olmayan iğne / aşı"), settings.t("Diyanet bewertet nicht nährende Behandlungsinjektionen und Impfungen grundsätzlich als nicht fastenbrechend.", "Diyanet, besleyici olmayan tedavi iğneleri ve aşıları genel olarak orucu bozmayan uygulamalar arasında değerlendirir."))
                rule("mouth.fill", settings.t("Zähne putzen", "Diş fırçalamak"), settings.t("Das Putzen selbst bricht nicht; Zahnpasta oder Wasser darf nicht geschluckt werden. Wegen des Risikos empfiehlt Diyanet besondere Vorsicht.", "Fırçalamak tek başına orucu bozmaz; macun veya su yutulmamalıdır. Diyanet risk nedeniyle dikkat tavsiye eder."))
                rule("arrow.up.to.line", settings.t("Unfreiwilliges Erbrechen", "İstem dışı kusmak"), settings.t("Spontanes Erbrechen bricht das Fasten nicht.", "Kendiliğinden kusmak orucu bozmaz."))
            }

            Section(settings.t("Qada, Kaffarah, Fidya – nicht verwechseln", "Kaza, kefaret, fidye – karıştırma")) {
                definition(settings.t("Qada", "Kaza"), settings.t("Einen verpassten oder ungültig gewordenen Fastentag später nachholen.", "Kaçırılan veya bozulan oruç gününü daha sonra tutmak."))
                definition(settings.t("Kaffarah", "Kefaret"), settings.t("Zusätzliche Sühne bei bestimmten bewusst begangenen Brüchen eines Ramadan-Fastens. Nicht jeder gebrochene Fastentag löst Kaffarah aus.", "Ramazan orucunun belirli kasıtlı ihlallerinde gereken ek kefarettir. Her bozulan oruç kefaret gerektirmez."))
                definition(settings.t("Fidya", "Fidye"), settings.t("Ausgleich für Menschen, die dauerhaft nicht fasten und später auch nicht nachholen können, z. B. wegen sehr hohen Alters oder unheilbarer chronischer Krankheit.", "Yaşlılık veya iyileşme ümidi olmayan kalıcı hastalık gibi nedenlerle oruç tutup daha sonra kaza etme imkânı bulunmayanlar için verilen bedeldir."))
            }

            Section(settings.t("Wichtig", "Önemli")) {
                Text(settings.t(
                    "Bei einem konkreten medizinischen Eingriff oder einer persönlichen Sonderlage zeigt SalahPath keine pauschale 'Fatwa-Automatik'. Nutze die allgemeinen Regeln hier und kläre einen unklaren Einzelfall mit einer qualifizierten religiösen Stelle und bei Gesundheitsthemen mit medizinischem Fachpersonal.",
                    "Belirli bir tıbbî işlem veya kişisel özel durumda SalahPath otomatik fetva vermez. Buradaki genel kuralları kullan; belirsiz bireysel durumu ehil bir dinî merciden, sağlık konusunu da sağlık uzmanından doğrula."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Was bricht das Fasten?", "Orucu ne bozar?"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func rule(_ icon: String, _ title: String, _ detail: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Image(systemName: icon)
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 24)
            VStack(alignment: .leading, spacing: 3) {
                Text(title).font(.headline)
                Text(detail).font(.subheadline).foregroundStyle(.secondary).fixedSize(horizontal: false, vertical: true)
            }
        }
    }

    @ViewBuilder
    private func definition(_ title: String, _ detail: String) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(title).font(.headline).foregroundStyle(SalahTheme.deepTeal)
            Text(detail).fixedSize(horizontal: false, vertical: true)
        }
    }
}

private struct FastingExceptionsView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        List {
            Section(settings.t("Wer ist grundsätzlich verpflichtet?", "Kimlere farzdır?")) {
                Text(settings.t(
                    "Ramadan-Fasten ist für muslimische, geistig zurechnungsfähige und pubertäre Personen verpflichtend. Kinder vor der Pubertät sind nicht verpflichtet; sie können altersgerecht und ohne Schaden ans Fasten herangeführt werden.",
                    "Ramazan orucu Müslüman, akıllı ve buluğa ermiş kişilere farzdır. Buluğa ermemiş çocuklar yükümlü değildir; zarar vermeden yaşına uygun şekilde oruca alıştırılabilir."
                ))
            }

            Section(settings.t("Vorübergehender Grund → später Qada", "Geçici mazeret → sonra kaza")) {
                exception(settings.t("Krankheit", "Hastalık"), settings.t("Wenn Fasten die Krankheit verschlimmern, verlängern oder voraussichtlich krank machen würde, darf verschoben und später nachgeholt werden.", "Oruç hastalığı artıracak, uzatacak veya kişiyi hasta edecekse ertelenebilir; daha sonra kaza edilir."))
                exception(settings.t("Reise", "Yolculuk"), settings.t("Eine religiös als Reise geltende Fahrt kann eine Erleichterung geben. Nach Diyanet/Hanafi gelten konkrete Reisebedingungen; verpasste Tage werden später nachgeholt.", "Dinî sefer sayılan yolculuk ruhsat sebebi olabilir. Diyanet/Hanefî ölçülerinde belirli şartlar vardır; tutulmayan günler sonra kaza edilir."))
                exception(settings.t("Schwangerschaft / Stillzeit", "Hamilelik / emzirme"), settings.t("Besteht begründete Sorge um Mutter oder Kind, darf nicht gefastet und später Qada gemacht werden.", "Anne veya çocuk için zarar endişesi varsa oruç tutulmayabilir; daha sonra kaza edilir."))
                exception(settings.t("Menstruation / Nifas", "Hayız / nifas"), settings.t("Während Menstruation und Wochenbett/Nifas wird nicht gefastet; diese Ramadan-Tage werden später als Qada nachgeholt.", "Hayız ve nifas döneminde oruç tutulmaz; Ramazan'da tutulmayan günler daha sonra kaza edilir."))
            }

            Section(settings.t("Dauerhaft nicht möglich → Fidya", "Kalıcı olarak mümkün değil → fidye")) {
                exception(settings.t("Sehr hohes Alter", "İleri yaş"), settings.t("Wer dauerhaft nicht mehr fasten kann und auch später keine Möglichkeit zur Qada hat, fällt unter die Fidya-Regel.", "Kalıcı olarak oruç tutamayan ve daha sonra kaza imkânı bulunmayan ileri yaştaki kişi fidye hükmüne girer."))
                exception(settings.t("Unheilbare chronische Krankheit", "İyileşme ümidi olmayan kronik hastalık"), settings.t("Wenn nach realistischer Einschätzung keine spätere Fastenfähigkeit zu erwarten ist, gilt ebenfalls die Fidya-Regel.", "Daha sonra oruç tutabilecek hale gelme ümidi yoksa fidye hükmü uygulanır."))
                Text(settings.t(
                    "Wird jemand später doch wieder dauerhaft fastenfähig, beschreibt Diyanet für die hanafitische Einordnung, dass die versäumten Tage nachgeholt werden; eine zuvor gezahlte Fidya gilt dann als freiwillige Sadaqah.",
                    "Kişi daha sonra yeniden sürekli oruç tutabilecek hale gelirse Diyanet'in Hanefî açıklamasına göre kaçırdığı günleri kaza eder; önceden verilen fidye nafile sadaka sayılır."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Nicht pauschal entscheiden", "Genelleme yapma")) {
                Text(settings.t(
                    "Gesundheit ist individuell. Bei Krankheit, Schwangerschaft, Medikamenten oder anderen medizinischen Fragen darf die App keine Diagnose ersetzen. Religiöse Erleichterung und medizinische Belastbarkeit müssen im konkreten Fall sauber beurteilt werden.",
                    "Sağlık kişiye özeldir. Hastalık, hamilelik, ilaç veya diğer tıbbî konularda uygulama teşhis yerine geçmez. Dinî ruhsat ve sağlık açısından dayanıklılık somut durumda doğru değerlendirilmelidir."
                ))
            }

            Section(settings.t("Quelle", "Kaynak")) {
                Text(settings.t(
                    "Diyanet / Din İşleri Yüksek Kurulu · Bedingungen der Fastenpflicht, erlaubte Entschuldigungsgründe, Qada und Fidya.",
                    "Diyanet / Din İşleri Yüksek Kurulu · oruç yükümlülüğü, mazeretler, kaza ve fidye."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Erleichterungen", "Ruhsatlar"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func exception(_ title: String, _ detail: String) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(title).font(.headline)
            Text(detail).font(.subheadline).foregroundStyle(.secondary).fixedSize(horizontal: false, vertical: true)
        }
    }
}
'''

guide.write_text(text[:start] + new_section + text[end:], encoding="utf-8")
print("v402 applied: complete in-app fasting and Ramadan learning hub")
