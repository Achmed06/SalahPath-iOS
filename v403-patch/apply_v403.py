from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

start_marker = "struct HijriCalendarView: View {"
end_marker = "\n// MARK: - Prayer position reference"
if start_marker not in text or end_marker not in text:
    raise SystemExit("v403: Hijri calendar anchors missing")

start = text.index(start_marker)
end = text.index(end_marker, start)

new_section = r'''private struct IslamicCalendarEvent: Identifiable {
    let id = UUID()
    let symbol: String
    let deTitle: String
    let trTitle: String
    let deMeaning: String
    let trMeaning: String
    let deRecommended: [String]
    let trRecommended: [String]
    let deCaution: String
    let trCaution: String
}

private struct IslamicCalendarEventDetailView: View {
    @EnvironmentObject private var settings: SettingsStore
    let date: Date
    let event: IslamicCalendarEvent

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                VStack(alignment: .leading, spacing: 8) {
                    Label(
                        settings.language == .german ? event.deTitle : event.trTitle,
                        systemImage: event.symbol
                    )
                    .font(.title2.bold())
                    .foregroundStyle(SalahTheme.deepTeal)

                    Text(gregorianDateString(date, language: settings.language))
                        .font(.subheadline.bold())
                        .foregroundStyle(SalahTheme.teal)
                    Text(hijriDateString(date, language: settings.language))
                        .font(.headline)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 7) {
                    Text(settings.t("Was bedeutet dieser Tag?", "Bu gün ne anlama gelir?"))
                        .font(.headline)
                    Text(settings.language == .german ? event.deMeaning : event.trMeaning)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Was ist empfohlen?", "Neler tavsiye edilir?"))
                        .font(.headline)
                    let items = settings.language == .german ? event.deRecommended : event.trRecommended
                    ForEach(items.indices, id: .self) { index in
                        HStack(alignment: .top, spacing: 9) {
                            Image(systemName: "checkmark.circle.fill")
                                .foregroundStyle(SalahTheme.teal)
                            Text(items[index])
                                .fixedSize(horizontal: false, vertical: true)
                        }
                    }
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("Nicht verwechseln", "Karıştırma"), systemImage: "exclamationmark.triangle.fill")
                        .font(.headline)
                        .foregroundStyle(SalahTheme.gold)
                    Text(settings.language == .german ? event.deCaution : event.trCaution)
                        .font(.subheadline)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 6) {
                    Text(settings.t("Quelle & Kalenderhinweis", "Kaynak ve takvim notu"))
                        .font(.headline)
                    Text(settings.t(
                        "Religiöse Einordnung nach Qur'an, authentischen Hadithen und Diyanet-Grunddarstellung. Das angezeigte Hijri-Datum wird mit Umm-al-Qura berechnet; regionale Mondsichtung kann den tatsächlichen Monatsbeginn verschieben.",
                        "Dinî açıklama Kur'an, sahih hadisler ve Diyanet temel anlatımına dayanır. Gösterilen hicrî tarih Ummü'l-Kurâ hesabıdır; bölgesel hilal gözlemi gerçek ay başlangıcını değiştirebilir."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.language == .german ? event.deTitle : event.trTitle)
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct HijriCalendarView: View {
    @EnvironmentObject private var settings: SettingsStore
    private let calendar = Calendar.current
    private let hijri = Calendar(identifier: .islamicUmmAlQura)

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 8) {
                    Text(settings.t("Heute", "Bugün"))
                        .font(.caption.bold())
                        .foregroundStyle(SalahTheme.teal)
                    Text(hijriDateString(Date(), language: settings.language))
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(gregorianDateString(Date(), language: settings.language))
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
                .padding(.vertical, 4)

                Text(settings.t(
                    "Umm-al-Qura ist ein berechneter Kalender. Tatsächliche Monatsanfänge können je nach regionaler Mondsichtung abweichen. SalahPath kennzeichnet deshalb zukünftige religiöse Daten als berechnet.",
                    "Ummü'l-Kurâ hesaplanmış bir takvimdir. Gerçek ay başlangıçları bölgesel hilal gözlemine göre değişebilir. Bu nedenle SalahPath gelecekteki dinî tarihleri hesaplanan tarih olarak gösterir."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            Section(settings.t("Nächste wichtige islamische Tage", "Yaklaşan önemli İslâmî günler")) {
                ForEach(nextImportantEvents) { item in
                    NavigationLink {
                        IslamicCalendarEventDetailView(date: item.date, event: item.event)
                    } label: {
                        HStack(spacing: 11) {
                            Image(systemName: item.event.symbol)
                                .font(.title3)
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 30)

                            VStack(alignment: .leading, spacing: 3) {
                                Text(settings.language == .german ? item.event.deTitle : item.event.trTitle)
                                    .font(.headline)
                                Text(hijriDateString(item.date, language: settings.language))
                                    .font(.subheadline)
                                Text(gregorianDateString(item.date, language: settings.language))
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                }
            }

            Section(settings.t("Die nächsten 30 Tage", "Önümüzdeki 30 gün")) {
                ForEach(days, id: .self) { date in
                    HStack {
                        VStack(alignment: .leading, spacing: 3) {
                            Text(gregorianDateString(date, language: settings.language))
                                .font(.subheadline)
                            Text(hijriDateString(date, language: settings.language))
                                .font(.headline)
                            if let event = eventInfo(date) {
                                Label(
                                    settings.language == .german ? event.deTitle : event.trTitle,
                                    systemImage: event.symbol
                                )
                                .font(.caption)
                                .foregroundStyle(SalahTheme.teal)
                            }
                        }
                        Spacer()
                        if calendar.isDateInToday(date) {
                            Text(settings.t("Heute", "Bugün"))
                                .font(.caption.bold())
                                .foregroundStyle(.tint)
                        }
                    }
                }
            }

            Section(settings.t("Regelmäßig empfohlene Fastentage", "Düzenli tavsiye edilen oruç günleri")) {
                calendarInfo(
                    settings.t("Weiße Tage · 13., 14. und 15. jedes Hijri-Monats", "Eyyâm-ı bîd · her hicrî ayın 13, 14 ve 15'i"),
                    settings.t(
                        "Freiwilliges Fasten an diesen drei Tagen ist empfohlen. Es ist kein Pflichtfasten.",
                        "Bu üç günde nafile oruç tavsiye edilir. Farz değildir."
                    )
                )
                calendarInfo(
                    settings.t("Montag und Donnerstag", "Pazartesi ve Perşembe"),
                    settings.t(
                        "Freiwilliges Fasten an diesen Wochentagen ist aus der Sunnah bekannt. Es ist kein Pflichtfasten.",
                        "Bu günlerde nafile oruç sünnette yer alır. Farz değildir."
                    )
                )
                calendarInfo(
                    settings.t("6 Tage im Shawwal", "Şevval'de 6 gün"),
                    settings.t(
                        "Nach Ramadan sind sechs freiwillige Fastentage im Shawwal empfohlen; sie müssen nicht an feste Kalendertage gebunden sein und ersetzen keine offenen Ramadan-Qada-Tage.",
                        "Ramazan'dan sonra Şevval ayında altı gün nafile oruç tavsiye edilir; sabit günlere bağlı değildir ve tutulmamış Ramazan kazalarının yerine geçmez."
                    )
                )
            }
        }
        .navigationTitle(settings.t("Hijri-Kalender", "Hicrî takvim"))
        .navigationBarTitleDisplayMode(.inline)
    }

    private var days: [Date] {
        (0..<30).compactMap { calendar.date(byAdding: .day, value: $0, to: calendar.startOfDay(for: Date())) }
    }

    private struct DatedEvent: Identifiable {
        let id: String
        let date: Date
        let event: IslamicCalendarEvent
    }

    private var nextImportantEvents: [DatedEvent] {
        var result: [DatedEvent] = []
        let start = calendar.startOfDay(for: Date())

        for offset in 0..<400 {
            guard let date = calendar.date(byAdding: .day, value: offset, to: start),
                  let event = eventInfo(date) else { continue }

            let components = hijri.dateComponents([.year, .month, .day], from: date)
            let token = "\(components.year ?? 0)-\(components.month ?? 0)-\(components.day ?? 0)-\(event.deTitle)"
            result.append(.init(id: token, date: date, event: event))

            if result.count >= 10 { break }
        }

        return result
    }

    private func eventInfo(_ date: Date) -> IslamicCalendarEvent? {
        let m = hijri.component(.month, from: date)
        let d = hijri.component(.day, from: date)

        if m == 1 && d == 1 {
            return .init(
                symbol: "calendar.badge.clock",
                deTitle: "1. Muharram · Beginn des Hijri-Jahres",
                trTitle: "1 Muharrem · Hicrî yılın başlangıcı",
                deMeaning: "Muharram ist der erste Monat des Hijri-Kalenders und gehört zu den vier heiligen Monaten. Der Jahresbeginn ist ein Kalenderdatum; im Islam gibt es dafür kein vorgeschriebenes 'Neujahrsfest'.",
                trMeaning: "Muharrem hicrî takvimin ilk ayıdır ve dört haram aydan biridir. Yıl başlangıcı bir takvim tarihidir; bunun için dinen zorunlu bir 'yılbaşı kutlaması' yoktur.",
                deRecommended: ["Muharram als besonderen Monat kennen.", "Freiwilliges Fasten ist in Muharram besonders verdienstvoll.", "Sich auf ʿAshura am 10. Muharram vorbereiten."],
                trRecommended: ["Muharrem ayının önemini öğren.", "Muharrem'de nafile oruç faziletlidir.", "10 Muharrem Aşure gününe hazırlan."],
                deCaution: "Keine bestimmte Feier, Dekoration oder besondere Gebetsform als verpflichtende Sunnah darstellen.",
                trCaution: "Belirli bir kutlama, süsleme veya özel namaz şeklini zorunlu sünnet gibi gösterme."
            )
        }

        if m == 1 && d == 10 {
            return .init(
                symbol: "moon.stars",
                deTitle: "ʿAshura · 10. Muharram",
                trTitle: "Aşure · 10 Muharrem",
                deMeaning: "ʿAshura ist der 10. Muharram. Freiwilliges Fasten an diesem Tag ist aus der Sunnah bekannt.",
                trMeaning: "Aşure günü 10 Muharrem'dir. Bu günde nafile oruç tutmak sünnette yer alır.",
                deRecommended: ["Am 10. Muharram freiwillig fasten.", "Nach hanafitischer/Diyanet-Empfehlung zusätzlich den 9. oder 11. Muharram mitfasten."],
                trRecommended: ["10 Muharrem'de nafile oruç tut.", "Hanefî/Diyanet tavsiyesinde 9. veya 11. Muharrem'i de ekle."],
                deCaution: "Das Fasten ist freiwillig, nicht Farz. Regionale Kulturbräuche rund um 'Aşure' sind nicht mit einer verpflichtenden Gottesdienstform gleichzusetzen.",
                trCaution: "Bu oruç farz değil, nafiledir. Aşure etrafındaki kültürel gelenekler zorunlu ibadet şekliyle aynı değildir."
            )
        }

        if m == 9 && d == 1 {
            return .init(
                symbol: "moon.fill",
                deTitle: "Beginn des Ramadan",
                trTitle: "Ramazan başlangıcı",
                deMeaning: "Ramadan ist der neunte Hijri-Monat. Das Fasten dieses Monats gehört zu den fünf Säulen des Islam für diejenigen, die die Voraussetzungen erfüllen.",
                trMeaning: "Ramazan hicrî takvimin dokuzuncu ayıdır. Şartları taşıyanlar için bu ayın orucu İslâm'ın beş şartından biridir.",
                deRecommended: ["Fasten mit Niyyah beginnen.", "Gebete, Qur'an, Dua, Dhikr und Sadaqah bewusst verstärken.", "Suhur und Iftar ohne Verschwendung gestalten."],
                trRecommended: ["Niyet ederek oruca başla.", "Namaz, Kur'an, dua, zikir ve sadakayı artır.", "Sahur ve iftarda israftan kaçın."],
                deCaution: "Der genaue Beginn kann regional von der Mondsichtung abhängen. SalahPath zeigt hier ein berechnetes Datum.",
                trCaution: "Kesin başlangıç bölgesel hilal gözlemine göre değişebilir. SalahPath burada hesaplanan tarihi gösterir."
            )
        }

        if m == 9 && d == 21 {
            return .init(
                symbol: "sparkles",
                deTitle: "Beginn der letzten zehn Ramadan-Nächte",
                trTitle: "Ramazan'ın son on gecesinin başlangıcı",
                deMeaning: "In den letzten zehn Nächten wird Laylat al-Qadr besonders gesucht. Die authentische Überlieferung lenkt auf die ungeraden Nächte dieser letzten zehn.",
                trMeaning: "Son on gecede Kadir Gecesi özellikle aranır. Sahih rivayetler son on gecenin tek gecelerine yönlendirir.",
                deRecommended: ["Gebet, Qur'an, Dua und Dhikr verstärken.", "Besonders die ungeraden Nächte ernst nehmen.", "Die bekannte Dua um Vergebung lernen."],
                trRecommended: ["Namaz, Kur'an, dua ve zikri artır.", "Özellikle tek geceleri değerlendirmeye çalış.", "Af dileme duasını öğren."],
                deCaution: "Laylat al-Qadr nicht sicher ausschließlich auf die 27. Nacht festlegen. Sie wird in den ungeraden Nächten der letzten zehn gesucht.",
                trCaution: "Kadir Gecesi'ni kesin olarak yalnız 27. geceye sabitleme. Son on gecenin tek gecelerinde aranır."
            )
        }

        if m == 10 && d == 1 {
            return .init(
                symbol: "party.popper.fill",
                deTitle: "Eid al-Fitr · 1. Shawwal",
                trTitle: "Ramazan Bayramı · 1 Şevval",
                deMeaning: "Eid al-Fitr beginnt nach Abschluss des Ramadan. An diesem Festtag wird nicht gefastet.",
                trMeaning: "Ramazan Bayramı Ramazan'ın tamamlanmasından sonra başlar. Bayramın birinci gününde oruç tutulmaz.",
                deRecommended: ["Eid-Gebet entsprechend der örtlichen Gemeinde beachten.", "Familie besuchen, Freude teilen und Bedürftige nicht vergessen.", "Offene Ramadan-Qada-Tage später nachholen."],
                trRecommended: ["Bayram namazını yerel cemaatle değerlendirmeye çalış.", "Aileyi ziyaret et, sevinci paylaş, ihtiyaç sahiplerini unutma.", "Eksik Ramazan kazalarını daha sonra tamamla."],
                deCaution: "Am ersten Shawwal ist Fasten verboten. Die empfohlenen sechs Shawwal-Tage beginnen daher erst nach dem Eid-Tag.",
                trCaution: "1 Şevval'de oruç tutulmaz. Tavsiye edilen altı Şevval orucu bayramın ilk gününden sonra tutulur."
            )
        }

        if m == 12 && d == 9 {
            return .init(
                symbol: "mountain.2.fill",
                deTitle: "Tag von ʿArafah · 9. Dhu l-Hijjah",
                trTitle: "Arefe günü · 9 Zilhicce",
                deMeaning: "Der 9. Dhu l-Hijjah ist der Tag von ʿArafah und ein zentraler Tag des Hajj.",
                trMeaning: "9 Zilhicce Arefe günüdür ve haccın en önemli günlerinden biridir.",
                deRecommended: ["Für Nicht-Pilger ist freiwilliges Fasten an ʿArafah besonders empfohlen.", "Dua, Dhikr und gute Taten vermehren."],
                trRecommended: ["Hacda olmayanlar için Arefe orucu özellikle tavsiye edilir.", "Dua, zikir ve hayırlı amelleri artır."],
                deCaution: "Pilger auf ʿArafah werden nicht pauschal wie Nicht-Pilger zum Fasten angehalten; Kraft für die Hajj-Handlungen hat Vorrang.",
                trCaution: "Arafat'taki hacılar, hac dışındaki kişiler gibi genel olarak oruca teşvik edilmez; hac ibadetlerine güç ayırmak önceliklidir."
            )
        }

        if m == 12 && d == 10 {
            return .init(
                symbol: "gift.fill",
                deTitle: "Eid al-Adha · 10. Dhu l-Hijjah",
                trTitle: "Kurban Bayramı · 10 Zilhicce",
                deMeaning: "Eid al-Adha ist das Opferfest und fällt in die Hajj-Zeit.",
                trMeaning: "Kurban Bayramı hac mevsimindeki büyük bayramdır.",
                deRecommended: ["Eid-Gebet beachten.", "Opferpflicht bzw. Opfer-Sunnah nach den persönlichen hanafitischen Voraussetzungen prüfen.", "Familie und Bedürftige am Fest teilhaben lassen."],
                trRecommended: ["Bayram namazını değerlendir.", "Kurban yükümlülüğünü kişisel Hanefî şartlara göre kontrol et.", "Aileyi ve ihtiyaç sahiplerini bayram sevincine ortak et."],
                deCaution: "Am Eid-Tag wird nicht gefastet.",
                trCaution: "Bayram günü oruç tutulmaz."
            )
        }

        if m == 12 && (11...13).contains(d) {
            return .init(
                symbol: "sun.max.fill",
                deTitle: "Tage des Tashriq · \(d). Dhu l-Hijjah",
                trTitle: "Teşrik günleri · \(d) Zilhicce",
                deMeaning: "Die Tage nach dem ersten Opferfesttag heißen Tage des Tashriq.",
                trMeaning: "Kurban Bayramı'nın ilk gününden sonraki bu günlere teşrik günleri denir.",
                deRecommended: ["Nach den Farz-Gebeten die hanafitischen Tashriq-Takbire entsprechend ihrer Zeit beachten.", "Allah gedenken, essen, trinken und die Festtage bewusst verbringen."],
                trRecommended: ["Hanefî uygulamada farz namazlardan sonra teşrik tekbirlerini zamanına göre getir.", "Allah'ı zikret, yiyip iç ve bayram günlerini bilinçli geçir."],
                deCaution: "Diese Tage sind keine gewöhnlichen freiwilligen Fastentage.",
                trCaution: "Bu günler normal nafile oruç günleri değildir."
            )
        }

        return nil
    }

    @ViewBuilder
    private func calendarInfo(_ title: String, _ detail: String) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(title).font(.headline)
            Text(detail)
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}
'''

guide.write_text(text[:start] + new_section + text[end:], encoding="utf-8")
print("v403 applied: interactive Hijri calendar with in-app Islamic-day explanations")
