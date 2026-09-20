from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
root_tab = Path("SalahZeit/Views/RootTabView.swift")

text = guide.read_text(encoding="utf-8")
insert_marker = "\n// MARK: - Prayer position reference"
if insert_marker not in text:
    raise SystemExit("v404: GuideView insertion marker missing")

new_views = r'''
// MARK: - Islam learning hub

private struct IslamLearningStore {
    private static let key = "islamLearningCompletedIDs"

    static func completed() -> Set<String> {
        Set(UserDefaults.standard.stringArray(forKey: key) ?? [])
    }

    static func isCompleted(_ id: String) -> Bool {
        completed().contains(id)
    }

    static func toggle(_ id: String) {
        var set = completed()
        if set.contains(id) {
            set.remove(id)
        } else {
            set.insert(id)
        }
        UserDefaults.standard.set(Array(set).sorted(), forKey: key)
    }
}

private struct IslamLearningLesson: Identifiable {
    let id: String
    let icon: String
    let deTitle: String
    let trTitle: String
    let deIntro: String
    let trIntro: String
    let dePoints: [String]
    let trPoints: [String]
    let deDetail: String
    let trDetail: String
}

private struct IslamLearningLessonView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var refresh = 0
    let lesson: IslamLearningLesson

    private var completed: Bool {
        _ = refresh
        return IslamLearningStore.isCompleted(lesson.id)
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
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

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Das solltest du zuerst verstehen", "Önce bunları anlamalısın"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    let points = settings.language == .german ? lesson.dePoints : lesson.trPoints
                    ForEach(points.indices, id: .self) { index in
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

                VStack(alignment: .leading, spacing: 7) {
                    Text(settings.t("Etwas genauer", "Biraz daha ayrıntılı"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.language == .german ? lesson.deDetail : lesson.trDetail)
                        .font(.body)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle()

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
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.language == .german ? lesson.deTitle : lesson.trTitle)
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct IslamLearningHubView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var refresh = 0

    private let lessons: [IslamLearningLesson] = [
        .init(
            id: "what_is_islam",
            icon: "moon.stars.fill",
            deTitle: "Was bedeutet Islam?",
            trTitle: "İslâm ne demektir?",
            deIntro: "Islam bedeutet, sich Allah anzuvertrauen, Ihm allein zu dienen und Seiner Rechtleitung zu folgen.",
            trIntro: "İslâm, Allah'a teslim olmak, yalnız O'na kulluk etmek ve O'nun hidayetine uymaktır.",
            dePoints: [
                "Muslime glauben an den einen Gott: Allah.",
                "Islam verbindet Glauben, Gottesdienst und Charakter – nicht nur einzelne Rituale.",
                "Die Offenbarung des Qur'an und das Vorbild des Propheten Muhammad ﷺ bilden die zentrale Grundlage."
            ],
            trPoints: [
                "Müslümanlar tek olan Allah'a iman eder.",
                "İslâm yalnız ritüellerden ibaret değildir; iman, ibadet ve ahlâkı birlikte kapsar.",
                "Kur'an vahyi ve Hz. Muhammed'in ﷺ örnekliği temel kaynaktır."
            ],
            deDetail: "Das arabische Wort Islam hängt mit Hingabe und Frieden zusammen. Muslim zu sein bedeutet nicht, fehlerlos zu sein. Der Mensch glaubt, bemüht sich um Gehorsam, bereut Fehler und kehrt zu Allah zurück. Wissen soll dabei zu Gottesdienst und gutem Verhalten führen.",
            trDetail: "İslâm kelimesi teslimiyet ve selâmet anlamlarıyla ilişkilidir. Müslüman olmak hatasız olmak demek değildir. İnsan iman eder, itaat için çaba gösterir, hatalarından tövbe eder ve Allah'a döner. Bilgi ibadete ve güzel ahlâka götürmelidir."
        ),
        .init(
            id: "shahada",
            icon: "quote.bubble.fill",
            deTitle: "Shahada · Glaubensbekenntnis",
            trTitle: "Kelime-i şehadet",
            deIntro: "Die Shahada fasst den Kern des islamischen Glaubens zusammen: Allah allein ist anbetungswürdig und Muhammad ﷺ ist Sein Gesandter.",
            trIntro: "Kelime-i şehadet İslâm inancının özünü özetler: Allah'tan başka ilâh yoktur ve Muhammed ﷺ O'nun elçisidir.",
            dePoints: [
                "Arabisch: أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللّٰهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ",
                "Bedeutung: Ich bezeuge, dass niemand außer Allah anbetungswürdig ist, und ich bezeuge, dass Muhammad Sein Diener und Gesandter ist.",
                "Das Bekenntnis ist nicht nur ein Satz: Es drückt Glauben und Annahme aus."
            ],
            trPoints: [
                "Arapça: أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللّٰهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ",
                "Anlamı: Allah'tan başka ilâh olmadığına ve Muhammed'in O'nun kulu ve elçisi olduğuna şahitlik ederim.",
                "Şehadet yalnız söylenen bir cümle değil; iman ve kabul ifadesidir."
            ],
            deDetail: "Die erste Hälfte schützt den Tawhid: Gottesdienst richtet sich an Allah allein. Die zweite Hälfte bedeutet, Muhammad ﷺ als letzten Propheten und Gesandten anzuerkennen und seiner authentisch überlieferten Lehre zu folgen.",
            trDetail: "İlk bölüm tevhidi ifade eder: ibadet yalnız Allah'a yapılır. İkinci bölüm Hz. Muhammed'i ﷺ son peygamber ve elçi olarak kabul etmeyi ve sahih sünnetine uymayı ifade eder."
        ),
        .init(
            id: "five_pillars",
            icon: "building.columns.fill",
            deTitle: "Die fünf Säulen",
            trTitle: "İslâm'ın beş şartı",
            deIntro: "Die fünf Säulen beschreiben die grundlegenden praktischen Pflichten des muslimischen Lebens.",
            trIntro: "İslâm'ın beş şartı Müslüman hayatının temel amelî ibadetlerini özetler.",
            dePoints: [
                "Shahada: Glaubensbekenntnis.",
                "Salah: die fünf täglichen Pflichtgebete.",
                "Zakat: verpflichtende Abgabe für Berechtigte, wenn die Voraussetzungen erfüllt sind.",
                "Sawm: Fasten im Ramadan.",
                "Hajj: Pilgerfahrt nach Mekka einmal im Leben, wenn die Voraussetzungen erfüllt sind."
            ],
            trPoints: [
                "Kelime-i şehadet: iman ikrarı.",
                "Namaz: beş vakit farz namaz.",
                "Zekât: şartları oluşan kişilerin vermesi gereken malî ibadet.",
                "Oruç: Ramazan orucu.",
                "Hac: şartları oluşan kişinin ömründe bir kez Mekke'ye hac yapması."
            ],
            deDetail: "Nicht jede Säule gilt in jeder Lebenssituation identisch. Zakat und Hajj haben z. B. finanzielle und weitere Voraussetzungen. Fasten kennt erlaubte Entschuldigungsgründe. Salah bleibt die tägliche zentrale körperliche Pflicht; Details lernst du in den eigenen SalahPath-Bereichen.",
            trDetail: "Her şart her durumda aynı şekilde yükümlülük doğurmaz. Örneğin zekât ve hac için malî ve başka şartlar vardır. Oruçta ruhsat sebepleri bulunur. Namaz günlük temel bedenî ibadettir; ayrıntıları SalahPath'in ilgili bölümlerinde öğrenebilirsin."
        ),
        .init(
            id: "six_beliefs",
            icon: "hexagon.fill",
            deTitle: "Die sechs Glaubensgrundsätze",
            trTitle: "İmanın altı esası",
            deIntro: "In der bekannten Zusammenfassung werden sechs grundlegende Glaubensbereiche genannt.",
            trIntro: "Yaygın özette iman esasları altı başlık altında anlatılır.",
            dePoints: [
                "Glaube an Allah.",
                "Glaube an Seine Engel.",
                "Glaube an Seine offenbarten Bücher.",
                "Glaube an Seine Propheten und Gesandten.",
                "Glaube an den Jüngsten Tag und das Jenseits.",
                "Glaube an Qadar: Allahs Wissen und Bestimmung – ohne die menschliche Verantwortung aufzuheben."
            ],
            trPoints: [
                "Allah'a iman.",
                "Meleklerine iman.",
                "Kitaplarına iman.",
                "Peygamberlerine iman.",
                "Âhiret gününe iman.",
                "Kadere iman: Allah'ın bilgisi ve takdiri; insanın sorumluluğunu ortadan kaldırmaz."
            ],
            deDetail: "Diese Grundlagen bilden die ʿAqida. Bei Qadar ist wichtig: Allahs Wissen und Schöpfungsmacht bedeuten nicht, dass der Mensch keine Verantwortung für seine bewussten Entscheidungen hätte. Details dieser theologischen Fragen sollten nicht auf vereinfachte Schlagworte reduziert werden.",
            trDetail: "Bu esaslar akaidin temelini oluşturur. Kader konusunda önemli nokta şudur: Allah'ın bilgisi ve yaratma kudreti, insanın bilinçli tercihlerindeki sorumluluğunu ortadan kaldırmaz. Bu teolojik konu basit sloganlara indirgenmemelidir."
        ),
        .init(
            id: "allah_tawhid",
            icon: "sparkles",
            deTitle: "Allah & Tawhid",
            trTitle: "Allah ve tevhid",
            deIntro: "Tawhid bedeutet, Allah als den Einen anzuerkennen und Gottesdienst ausschließlich Ihm zu widmen.",
            trIntro: "Tevhid, Allah'ı bir bilmek ve ibadeti yalnız O'na yöneltmektir.",
            dePoints: [
                "Allah ist der Schöpfer und nichts ist Ihm gleich.",
                "Dua, Anbetung und letztliche Hingabe richten sich an Allah.",
                "Allah wird nicht als Mensch, Bild oder geschaffene Gestalt vorgestellt."
            ],
            trPoints: [
                "Allah yaratıcıdır ve hiçbir şey O'nun benzeri değildir.",
                "Dua, ibadet ve kulluk Allah'a yöneltilir.",
                "Allah insan, resim veya yaratılmış bir şekil gibi düşünülmez."
            ],
            deDetail: "Der Qur'an betont Allahs Einzigkeit, Wissen, Macht, Barmherzigkeit und Gerechtigkeit. Muslime lernen Allah durch die Namen und Eigenschaften kennen, die in Qur'an und authentischer Sunnah überliefert sind, ohne Ihn mit der Schöpfung gleichzusetzen.",
            trDetail: "Kur'an Allah'ın birliğini, ilmini, kudretini, rahmetini ve adaletini vurgular. Müslümanlar Allah'ı Kur'an ve sahih sünnette bildirilen isim ve sıfatlarla tanır; O'nu yaratılmışlara benzetmez."
        ),
        .init(
            id: "prophet",
            icon: "person.text.rectangle.fill",
            deTitle: "Prophet Muhammad ﷺ",
            trTitle: "Hz. Muhammed ﷺ",
            deIntro: "Muhammad ﷺ ist im Islam der letzte Prophet und Gesandte Allahs.",
            trIntro: "Hz. Muhammed ﷺ İslâm'da Allah'ın son peygamberi ve elçisidir.",
            dePoints: [
                "Er übermittelte den Qur'an und erklärte die Religion durch Wort und Praxis.",
                "Muslime lieben und respektieren ihn, beten ihn aber nicht an.",
                "Sunnah bedeutet sein authentisch überliefertes Vorbild."
            ],
            trPoints: [
                "Kur'an'ı tebliğ etti ve dini sözleriyle ve uygulamasıyla açıkladı.",
                "Müslümanlar onu sever ve saygı gösterir; fakat ona ibadet etmez.",
                "Sünnet, onun sahih şekilde aktarılan örnekliğidir."
            ],
            deDetail: "Seine Biografie heißt Sira. Für religiöse Regeln ist wichtig, zwischen authentisch überlieferten Hadithen, schwachen Berichten und späteren kulturellen Geschichten zu unterscheiden. SalahPath soll deshalb keine beliebte Geschichte automatisch als religiöse Tatsache behandeln.",
            trDetail: "Hayatını anlatan alana siyer denir. Dinî hükümler açısından sahih hadisleri, zayıf rivayetleri ve sonradan oluşmuş kültürel anlatıları ayırmak önemlidir. SalahPath popüler bir hikâyeyi otomatik olarak dinî gerçek gibi sunmamalıdır."
        ),
        .init(
            id: "quran",
            icon: "book.closed.fill",
            deTitle: "Der Qur'an",
            trTitle: "Kur'an",
            deIntro: "Der Qur'an ist für Muslime Allahs Offenbarung an Muhammad ﷺ in arabischer Sprache.",
            trIntro: "Kur'an Müslümanlara göre Allah'ın Hz. Muhammed'e ﷺ Arapça olarak indirdiği vahiydir.",
            dePoints: [
                "Er besteht aus 114 Suren.",
                "Eine Übersetzung hilft beim Verstehen, ist aber nicht identisch mit dem arabischen Qur'an-Text.",
                "Lesen, verstehen und danach handeln gehören zusammen."
            ],
            trPoints: [
                "114 sûreden oluşur.",
                "Meal anlamayı kolaylaştırır; fakat Arapça Kur'an metninin kendisiyle aynı değildir.",
                "Okumak, anlamak ve yaşamak birlikte düşünülmelidir."
            ],
            deDetail: "Für Anfänger ist es sinnvoll, kurze Suren, Al-Fatiha und grundlegende Bedeutungen zu lernen. SalahPath trennt deshalb arabischen Text, Umschrift und Übersetzung. Die Umschrift ist nur eine Lernhilfe und ersetzt das korrekte arabische Lesen nicht dauerhaft.",
            trDetail: "Yeni başlayanlar için kısa sûreleri, Fâtiha'yı ve temel anlamları öğrenmek faydalıdır. SalahPath bu nedenle Arapça metni, okunuşu ve meali ayırır. Latin harfli okunuş yalnız öğrenme yardımıdır; doğru Arapça okumayı kalıcı olarak ersetzen etmez."
        ),
        .init(
            id: "purity_worship",
            icon: "drop.fill",
            deTitle: "Reinheit & Gottesdienst",
            trTitle: "Temizlik ve ibadet",
            deIntro: "Rituelle Reinheit ist eine Voraussetzung für bestimmte Gottesdienste, besonders das Gebet.",
            trIntro: "Hükmî temizlik bazı ibadetlerin, özellikle namazın şartlarındandır.",
            dePoints: [
                "Wudu für die kleine rituelle Unreinheit.",
                "Ghusl in Situationen, in denen die Ganzkörperwaschung erforderlich ist.",
                "Tayammum als erlaubte Ersatzreinigung, wenn die Voraussetzungen erfüllt sind."
            ],
            trPoints: [
                "Küçük hadeste abdest.",
                "Boy abdesti gereken durumlarda gusül.",
                "Şartları oluştuğunda su yerine teyemmüm."
            ],
            deDetail: "Reinheit im Islam umfasst sowohl körperliche Sauberkeit als auch rechtlich definierte rituelle Reinheit. Beides darf nicht verwechselt werden. Ein sauber aussehender Körper bedeutet nicht automatisch Wudu, und Wudu ersetzt nicht jede Situation, in der Ghusl erforderlich ist.",
            trDetail: "İslâm'da temizlik hem beden temizliğini hem de fıkhî hükmî temizliği kapsar. Bunlar aynı şey değildir. Bedenin temiz görünmesi otomatik olarak abdestli olmak demek değildir; abdest de gusül gereken her durumun yerine geçmez."
        ),
        .init(
            id: "akhlaq",
            icon: "heart.fill",
            deTitle: "Akhlaq · guter Charakter",
            trTitle: "Ahlâk",
            deIntro: "Islamische Religiosität betrifft nicht nur Gebet und Fasten, sondern auch den Umgang mit Menschen.",
            trIntro: "İslâmî hayat yalnız namaz ve oruçtan ibaret değildir; insanlarla ilişkileri de kapsar.",
            dePoints: [
                "Wahrhaftigkeit, Vertrauenswürdigkeit und Gerechtigkeit.",
                "Respekt gegenüber Eltern, Familie, Nachbarn und anderen Menschen.",
                "Keine Verleumdung, üble Nachrede, Betrug oder bewusstes Unrecht."
            ],
            trPoints: [
                "Doğruluk, güvenilirlik ve adalet.",
                "Anne-baba, aile, komşu ve diğer insanlara saygı.",
                "İftira, gıybet, hile ve bilinçli haksızlıktan uzak durmak."
            ],
            deDetail: "Guter Charakter ist kein Zusatzmodul neben der Religion. Qur'an und Sunnah verbinden Gottesdienst mit Verantwortung gegenüber anderen. Eine Person kann deshalb nicht schlechte Behandlung anderer damit rechtfertigen, dass sie viele freiwillige Rituale verrichtet.",
            trDetail: "Güzel ahlâk dinin dışında ek bir bölüm değildir. Kur'an ve sünnet ibadeti insanlara karşı sorumlulukla birlikte ele alır. Bu nedenle çok nafile ibadet yapmak, başkalarına kötü davranmayı meşrulaştırmaz."
        ),
        .init(
            id: "halal_haram",
            icon: "scale.3d",
            deTitle: "Halal, Haram & Zweifel",
            trTitle: "Helâl, haram ve şüpheli şeyler",
            deIntro: "Halal bedeutet religiös erlaubt; Haram bedeutet religiös verboten. Nicht jede persönliche Abneigung ist automatisch Haram.",
            trIntro: "Helâl dinen izin verilen, haram ise dinen yasaklanan şeydir. Kişisel hoşnutsuzluk her şeyi otomatik olarak haram yapmaz.",
            dePoints: [
                "Klare Verbote brauchen eine religiöse Grundlage.",
                "Zwischen Farz, Wajib, Sunnah, Makruh, Mubah und Haram unterscheiden.",
                "Bei strittigen Fragen Rechtsschule und Beleg nennen statt pauschal zu urteilen."
            ],
            trPoints: [
                "Açık yasak için dinî delil gerekir.",
                "Farz, vacip, sünnet, mekruh, mubah ve haramı birbirinden ayır.",
                "İhtilaflı konularda kesin genelleme yerine mezhep ve delili belirt."
            ],
            deDetail: "SalahPath soll Begriffe nicht inflationär verwenden. 'Haram' ist eine rechtliche Bewertung, nicht bloß 'ich finde es schlecht'. Ebenso bedeutet 'Sunnah' nicht automatisch Pflicht. In Hanafi-Fiqh gibt es zusätzlich die Kategorie Wajib, die von Farz unterschieden wird.",
            trDetail: "SalahPath kavramları gelişigüzel kullanmamalıdır. 'Haram' fıkhî bir hükümdür; yalnız 'bence kötü' anlamına gelmez. 'Sünnet' de otomatik olarak farz değildir. Hanefî fıkhında ayrıca farzdan ayrı 'vacip' kategorisi vardır."
        ),
        .init(
            id: "repentance",
            icon: "arrow.uturn.backward.circle.fill",
            deTitle: "Tawbah · Reue und Neubeginn",
            trTitle: "Tövbe ve yeniden başlamak",
            deIntro: "Ein Muslim, der einen Fehler macht, soll nicht glauben, dass Rückkehr zu Allah unmöglich geworden ist.",
            trIntro: "Hata yapan Müslüman Allah'a dönüş yolunun kapandığını düşünmemelidir.",
            dePoints: [
                "Sünde beenden.",
                "Ehrlich bereuen.",
                "Entschlossen sein, nicht bewusst zurückzukehren.",
                "Wenn Rechte anderer verletzt wurden, diese Rechte soweit möglich zurückgeben oder wiedergutmachen."
            ],
            trPoints: [
                "Günahı bırak.",
                "Samimiyetle pişman ol.",
                "Bilinçli olarak tekrar etmemeye karar ver.",
                "Kul hakkı varsa mümkün olduğunca hakkı iade et veya telafi et."
            ],
            deDetail: "Tawbah ist nicht nur ein gesprochener Satz. Sie verbindet Reue mit Veränderung. Gleichzeitig soll Verzweiflung an Allahs Barmherzigkeit vermieden werden. Bei wiederholten Fehlern wird die Tür zur ehrlichen Reue nicht dadurch geschlossen, dass ein Mensch zuvor schon gefallen ist.",
            trDetail: "Tövbe yalnız söylenen bir cümle değildir; pişmanlığı değişimle birleştirir. Aynı zamanda Allah'ın rahmetinden ümit kesilmez. Bir insan daha önce tekrar hata etmiş olsa bile samimi tövbe kapısı kapanmış sayılmaz."
        ),
        .init(
            id: "afterlife",
            icon: "hourglass.bottomhalf.filled",
            deTitle: "Tod & Jenseits",
            trTitle: "Ölüm ve âhiret",
            deIntro: "Der Glaube an Auferstehung, Gericht und das Jenseits gehört zu den Grundlagen des islamischen Glaubens.",
            trIntro: "Diriliş, hesap ve âhirete iman İslâm inancının temel esaslarındandır.",
            dePoints: [
                "Das irdische Leben ist begrenzt und verantwortliches Handeln hat Folgen.",
                "Menschen werden auferweckt und für ihr Handeln zur Rechenschaft gezogen.",
                "Paradies und Hölle gehören zur islamischen Jenseitslehre."
            ],
            trPoints: [
                "Dünya hayatı sınırlıdır ve sorumlu davranışın sonuçları vardır.",
                "İnsanlar diriltilecek ve yaptıklarından hesaba çekilecektir.",
                "Cennet ve cehennem İslâm'ın âhiret inancının parçalarıdır."
            ],
            deDetail: "Jenseitswissen kommt aus Offenbarung. SalahPath soll deshalb keine spekulativen Geschichten über Grab, Engel oder Endzeit als sichere Tatsachen erzählen, wenn sie nicht zuverlässig belegt sind. Details werden nur mit sauberer Quellenlage ergänzt.",
            trDetail: "Âhiret bilgisi vahye dayanır. Bu yüzden SalahPath kabir, melekler veya kıyametle ilgili güvenilir delili olmayan hikâyeleri kesin gerçek gibi anlatmamalıdır. Ayrıntılar ancak sağlam kaynakla eklenir."
        )
    ]

    private var completedCount: Int {
        _ = refresh
        return lessons.filter { IslamLearningStore.isCompleted($0.id) }.count
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 13) {
                VStack(alignment: .leading, spacing: 10) {
                    Label(settings.t("Islam Schritt für Schritt lernen", "İslâm'ı adım adım öğren"), systemImage: "book.pages.fill")
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

                ForEach(lessons) { lesson in
                    NavigationLink {
                        IslamLearningLessonView(lesson: lesson)
                    } label: {
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
                    .buttonStyle(.plain)
                }

                VStack(alignment: .leading, spacing: 7) {
                    Text(settings.t("Wichtig", "Önemli"))
                        .font(.headline)
                    Text(settings.t(
                        "Dieser Kurs ist eine strukturierte Einführung. Er ersetzt kein vollständiges jahrelanges Studium. Bei komplexen Fiqh-, Glaubens- oder persönlichen Lebensfragen zeigt SalahPath Unterschiede und Grenzen, statt eine unbelegte Schnellantwort als sicher auszugeben.",
                        "Bu kurs düzenli bir başlangıçtır; yıllar süren kapsamlı din eğitimini ersetzen etmez. Karmaşık fıkıh, akaid veya kişisel meselelerde SalahPath delilsiz hızlı cevabı kesin hüküm gibi sunmak yerine farklılıkları ve sınırları gösterir."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Islam lernen", "İslâm'ı öğren"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear { refresh += 1 }
    }
}
'''

text = text.replace(insert_marker, new_views + insert_marker, 1)
guide.write_text(text, encoding="utf-8")

rt = root_tab.read_text(encoding="utf-8")
anchor = '''                    NavigationLink { FastingTrackerView() } label: {
                        discoverTile(icon: "moon.stars.fill", title: settings.t("Fasten", "Oruç"), subtitle: settings.t("Tracker", "Takip"))
                    }
'''
replacement = anchor + '''                    NavigationLink { IslamLearningHubView() } label: {
                        discoverTile(icon: "book.pages.fill", title: settings.t("Islam lernen", "İslâm'ı Öğren"), subtitle: settings.t("Von den Grundlagen", "Temelden başla"))
                    }
'''
if anchor not in rt:
    raise SystemExit("v404: MoreView fasting tile anchor missing")
root_tab.write_text(rt.replace(anchor, replacement, 1), encoding="utf-8")

print("v404 applied: structured in-app Islam learning course + Discover tile")
