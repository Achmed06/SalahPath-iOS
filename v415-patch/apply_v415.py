from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

def replace_scoped(source: str, struct_name: str, start_marker: str, end_marker: str, replacement: str) -> str:
    struct_pos = source.index(struct_name)
    start = source.index(start_marker, struct_pos)
    end = source.index(end_marker, start)
    return source[:start] + replacement + source[end:]

# 1) FastingTrackerView: split one huge body into small cards.
fasting_body = r'''    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                fastingHeaderCard
                fastingLearningLinks
                fastingTrackerCard
                fastingHistoryCard
                fastingSourceCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Fasten & Ramadan", "Oruç ve Ramazan"))
        .navigationBarTitleDisplayMode(.inline)
    }

    private var fastingHeaderCard: some View {
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
                Label(
                    settings.t(
                        "Ramadan · Tag \(hijri.component(.day, from: Date()))",
                        "Ramazan · \(hijri.component(.day, from: Date())). gün"
                    ),
                    systemImage: "sparkles"
                )
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.teal)
            }
        }
        .cardStyle(material: true)
    }

    @ViewBuilder
    private var fastingLearningLinks: some View {
        fastingNavigationCard(
            title: settings.t("1 · Fasten ganz einfach", "1 · Orucu en kolay şekilde öğren"),
            subtitle: settings.t("Absicht, Sahur, Fajr, Tagesablauf und Iftar", "Niyet, sahur, imsak, günün akışı ve iftar"),
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
    }

    private var fastingTrackerCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(settings.t("Mein Fasten-Tracker", "Oruç takibim"))
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            Toggle(isOn: Binding(
                get: { FastingStore.contains(Date()) },
                set: { _ in
                    FastingStore.toggle(Date())
                    refresh += 1
                }
            )) {
                Label(
                    settings.t("Heute als Fastentag markieren", "Bugünü oruç günü olarak işaretle"),
                    systemImage: "checkmark.circle"
                )
            }

            Text(settings.t(
                "Der Tracker speichert nur deine persönliche Liste lokal auf diesem Gerät. Er entscheidet nicht, ob ein Fasten religiös gültig oder verpflichtend ist.",
                "Takip bölümü yalnız kişisel listenizi bu cihazda yerel olarak saklar. Bir orucun dinen geçerli veya zorunlu olup olmadığına karar vermez."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle()
    }

    private var fastingHistoryCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(settings.t("Letzte 14 Tage", "Son 14 gün"))
                .font(.headline.bold())

            ForEach(lastDays, id: \.self) { day in
                fastingHistoryRow(day)
                if day != lastDays.last { Divider() }
            }
        }
        .cardStyle()
    }

    private func fastingHistoryRow(_ day: Date) -> some View {
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
    }

    private var fastingSourceCard: some View {
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

'''
text = replace_scoped(
    text,
    "struct FastingTrackerView: View {",
    "    var body: some View {",
    "    @ViewBuilder\n    private func fastingNavigationCard",
    fasting_body
)

# 2) IslamicCalendarEventDetailView: split detail cards.
event_detail_body = r'''    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                eventHeaderCard
                eventMeaningCard
                eventRecommendationsCard
                eventCautionCard
                eventSourceCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(localizedEventTitle)
        .navigationBarTitleDisplayMode(.inline)
    }

    private var localizedEventTitle: String {
        settings.language == .german ? event.deTitle : event.trTitle
    }

    private var eventHeaderCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Label(localizedEventTitle, systemImage: event.symbol)
                .font(.title2.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            Text(gregorianDateString(date, language: settings.language))
                .font(.subheadline.bold())
                .foregroundStyle(SalahTheme.teal)
            Text(hijriDateString(date, language: settings.language))
                .font(.headline)
        }
        .cardStyle(material: true)
    }

    private var eventMeaningCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(settings.t("Was bedeutet dieser Tag?", "Bu gün ne anlama gelir?"))
                .font(.headline)
            Text(settings.language == .german ? event.deMeaning : event.trMeaning)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle()
    }

    private var eventRecommendationsCard: some View {
        let items = settings.language == .german ? event.deRecommended : event.trRecommended
        return VStack(alignment: .leading, spacing: 10) {
            Text(settings.t("Was ist empfohlen?", "Neler tavsiye edilir?"))
                .font(.headline)

            ForEach(items.indices, id: \.self) { index in
                HStack(alignment: .top, spacing: 9) {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundStyle(SalahTheme.teal)
                    Text(items[index])
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
        }
        .cardStyle()
    }

    private var eventCautionCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Label(
                settings.t("Nicht verwechseln", "Karıştırma"),
                systemImage: "exclamationmark.triangle.fill"
            )
            .font(.headline)
            .foregroundStyle(SalahTheme.gold)

            Text(settings.language == .german ? event.deCaution : event.trCaution)
                .font(.subheadline)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle(material: true)
    }

    private var eventSourceCard: some View {
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
'''
text = replace_scoped(
    text,
    "private struct IslamicCalendarEventDetailView: View {",
    "    var body: some View {",
    "\n}\n\nstruct HijriCalendarView: View {",
    event_detail_body
) + "\n}\n\nstruct HijriCalendarView: View {" + text.split("\n}\n\nstruct HijriCalendarView: View {",1)[1] if False else text

# The prior helper cannot preserve the struct boundary when end marker contains it;
# do this replacement directly and safely instead.
# Re-read original current text for this one operation.
current = guide.read_text(encoding="utf-8")
# Re-apply already finished fasting change to current by taking from 'text' up to event struct only.
event_struct_pos = text.index("private struct IslamicCalendarEventDetailView: View {")
current_event_pos = current.index("private struct IslamicCalendarEventDetailView: View {")
current = text[:event_struct_pos] + current[current_event_pos:]

event_start = current.index("    var body: some View {", current.index("private struct IslamicCalendarEventDetailView: View {"))
event_end = current.index("\n}\n\nstruct HijriCalendarView: View {", event_start)
current = current[:event_start] + event_detail_body + current[event_end:]

# 3) HijriCalendarView body into sections.
hijri_body = r'''    var body: some View {
        List {
            hijriTodaySection
            hijriImportantEventsSection
            hijriNextThirtyDaysSection
            hijriRecommendedFastingSection
        }
        .navigationTitle(settings.t("Hijri-Kalender", "Hicrî takvim"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private var hijriTodaySection: some View {
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
    }

    @ViewBuilder
    private var hijriImportantEventsSection: some View {
        Section(settings.t("Nächste wichtige islamische Tage", "Yaklaşan önemli İslâmî günler")) {
            ForEach(nextImportantEvents) { item in
                NavigationLink {
                    IslamicCalendarEventDetailView(date: item.date, event: item.event)
                } label: {
                    importantEventRow(item)
                }
            }
        }
    }

    private func importantEventRow(_ item: DatedEvent) -> some View {
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

    @ViewBuilder
    private var hijriNextThirtyDaysSection: some View {
        Section(settings.t("Die nächsten 30 Tage", "Önümüzdeki 30 gün")) {
            ForEach(days, id: \.self) { date in
                hijriDayRow(date)
            }
        }
    }

    private func hijriDayRow(_ date: Date) -> some View {
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

    @ViewBuilder
    private var hijriRecommendedFastingSection: some View {
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

'''
current = replace_scoped(
    current,
    "struct HijriCalendarView: View {",
    "    var body: some View {",
    "    private var days: [Date] {",
    hijri_body
)

# 4) IslamLearningLessonView split into small cards.
lesson_body = r'''    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                lessonHeaderCard
                lessonPointsCard
                lessonDetailCard
                lessonCompletionButton
                lessonSourceCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.language == .german ? lesson.deTitle : lesson.trTitle)
        .navigationBarTitleDisplayMode(.inline)
    }

    private var lessonHeaderCard: some View {
        VStack(alignment: .leading, spacing: 9) {
            Label(
                settings.language == .german ? lesson.deTitle : lesson.trTitle,
                systemImage: lesson.icon
            )
            .font(.title2.bold())
            .foregroundStyle(SalahTheme.deepTeal)

            Text(settings.language == .german ? lesson.deIntro : lesson.trIntro)
                .font(.body)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle(material: true)
    }

    private var lessonPointsCard: some View {
        let points = settings.language == .german ? lesson.dePoints : lesson.trPoints
        return VStack(alignment: .leading, spacing: 10) {
            Text(settings.t("Das solltest du zuerst verstehen", "Önce bunları anlamalısın"))
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            ForEach(points.indices, id: \.self) { index in
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundStyle(SalahTheme.teal)
                        .padding(.top, 2)
                    Text(points[index])
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
        }
        .cardStyle()
    }

    private var lessonDetailCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(settings.t("Etwas genauer", "Biraz daha ayrıntılı"))
                .font(.headline.bold())
                .foregroundStyle(SalahTheme.deepTeal)
            Text(settings.language == .german ? lesson.deDetail : lesson.trDetail)
                .font(.body)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle()
    }

    private var lessonCompletionButton: some View {
        Button {
            IslamLearningStore.toggle(lesson.id)
            refresh += 1
        } label: {
            Label(
                completed
                    ? settings.t("Als gelernt markiert", "Öğrenildi olarak işaretli")
                    : settings.t("Als gelernt markieren", "Öğrendim olarak işaretle"),
                systemImage: completed ? "checkmark.seal.fill" : "checkmark.seal"
            )
            .font(.headline.bold())
            .frame(maxWidth: .infinity)
            .padding(.vertical, 13)
        }
        .buttonStyle(.plain)
        .foregroundStyle(completed ? .white : SalahTheme.deepTeal)
        .background(
            completed ? SalahTheme.deepTeal : SalahTheme.cream,
            in: RoundedRectangle(cornerRadius: 15, style: .continuous)
        )
        .overlay {
            RoundedRectangle(cornerRadius: 15, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.50), lineWidth: 1)
        }
    }

    private var lessonSourceCard: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama"))
                .font(.headline)
            Text(settings.t(
                "Grundlage: Qur'an, authentische Hadithe und Diyanet Temel İslâm Bilgileri / İlmihal. SalahPath erklärt Grundlagen; bei strittigen Fiqh-Fragen werden Rechtsschulunterschiede gesondert gekennzeichnet.",
                "Temel kaynak: Kur'an, sahih hadisler ve Diyanet Temel İslâm Bilgileri / İlmihal. SalahPath temel bilgileri açıklar; ihtilaflı fıkıh konularında mezhep farkları ayrıca belirtilir."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }
'''
current = replace_scoped(
    current,
    "private struct IslamLearningLessonView: View {",
    "    var body: some View {",
    "\n}\n\nstruct IslamLearningHubView: View {",
    lesson_body
) + "\n}\n\nstruct IslamLearningHubView: View {" + current.split("\n}\n\nstruct IslamLearningHubView: View {",1)[1] if False else current

# Direct safe replacement for lesson struct boundary.
lesson_struct = current.index("private struct IslamLearningLessonView: View {")
lesson_start = current.index("    var body: some View {", lesson_struct)
lesson_end = current.index("\n}\n\nstruct IslamLearningHubView: View {", lesson_start)
current = current[:lesson_start] + lesson_body + current[lesson_end:]

# 5) IslamLearningHubView: compact body and row helpers.
hub_body = r'''    var body: some View {
        ScrollView {
            LazyVStack(spacing: 13) {
                islamProgressCard
                islamLessonList
                islamLearningCautionCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Islam lernen", "İslâm'ı öğren"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear { refresh += 1 }
    }

    private var islamProgressCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Label(
                settings.t("Islam Schritt für Schritt lernen", "İslâm'ı adım adım öğren"),
                systemImage: "book.pages.fill"
            )
            .font(.title2.bold())
            .foregroundStyle(SalahTheme.deepTeal)

            Text(settings.t(
                "Du musst nicht alles auf einmal verstehen. Beginne oben und arbeite dich Modul für Modul weiter. Gebet, Wudu, Qur'an und Fasten haben zusätzlich eigene ausführliche Bereiche in SalahPath.",
                "Her şeyi bir anda öğrenmek zorunda değilsin. Yukarıdan başla ve modül modül ilerle. Namaz, abdest, Kur'an ve oruç için SalahPath'te ayrıca ayrıntılı bölümler var."
            ))
            .font(.subheadline)
            .fixedSize(horizontal: false, vertical: true)

            ProgressView(value: Double(completedCount), total: Double(lessons.count))
                .tint(SalahTheme.teal)

            Text(settings.t(
                "\(completedCount) von \(lessons.count) Grundlagen markiert",
                "\(lessons.count) temel konudan \(completedCount) tanesi işaretlendi"
            ))
            .font(.caption.bold())
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }

    @ViewBuilder
    private var islamLessonList: some View {
        ForEach(lessons) { lesson in
            NavigationLink {
                IslamLearningLessonView(lesson: lesson)
            } label: {
                islamLessonRow(lesson)
            }
            .buttonStyle(.plain)
        }
    }

    private func islamLessonRow(_ lesson: IslamLearningLesson) -> some View {
        HStack(spacing: 12) {
            Image(systemName: lesson.icon)
                .font(.title3)
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 34, height: 34)
                .background(SalahTheme.softTeal.opacity(0.55), in: Circle())

            VStack(alignment: .leading, spacing: 3) {
                Text(settings.language == .german ? lesson.deTitle : lesson.trTitle)
                    .font(.headline)
                    .foregroundStyle(SalahTheme.ink)
                Text(settings.language == .german ? lesson.deIntro : lesson.trIntro)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            Spacer(minLength: 6)

            Image(systemName: IslamLearningStore.isCompleted(lesson.id) ? "checkmark.circle.fill" : "chevron.right")
                .foregroundStyle(IslamLearningStore.isCompleted(lesson.id) ? .green : SalahTheme.teal)
        }
        .padding(13)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 15, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.36), lineWidth: 1)
        }
    }

    private var islamLearningCautionCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(settings.t("Wichtig", "Önemli"))
                .font(.headline)
            Text(settings.t(
                "Dieser Kurs ist eine strukturierte Einführung. Er ersetzt kein vollständiges jahrelanges Studium. Bei komplexen Fiqh-, Glaubens- oder persönlichen Lebensfragen zeigt SalahPath Unterschiede und Grenzen, statt eine unbelegte Schnellantwort als sicher auszugeben.",
                "Bu kurs düzenli bir başlangıçtır; yıllar süren kapsamlı din eğitiminin yerini tutmaz. Karmaşık fıkıh, akaid veya kişisel meselelerde SalahPath delilsiz hızlı cevabı kesin hüküm gibi sunmak yerine farklılıkları ve sınırları gösterir."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }
'''
hub_struct = current.index("struct IslamLearningHubView: View {")
hub_start = current.index("    var body: some View {", hub_struct)
hub_end = current.index("\n}\n\n// MARK: - Prayer position reference", hub_start)
current = current[:hub_start] + hub_body + current[hub_end:]

guide.write_text(current, encoding="utf-8")
print("v415 applied: split large SwiftUI learning screens into compiler-friendly subviews")
