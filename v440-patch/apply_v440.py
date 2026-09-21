from pathlib import Path

root = Path.cwd()
home = root / 'SalahZeit' / 'Views' / 'HomeView.swift'
guide = root / 'SalahZeit' / 'Views' / 'GuideView.swift'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'v440 {label}: expected exactly 1 match, found {count}')
    return text.replace(old, new, 1)

# Home daily-dua excerpts: label excerpts honestly and remove the mixed-language typo.
h = home.read_text(encoding='utf-8')
h = replace_once(h,
'        .init(deTitle: "Rabbi zidni ilma", trTitle: "Rabbî zidnî ilmâ", arabic: "رَبِّ زِدْنِي عِلْمًا", transliteration: "Rabbi zidnī ʿilmā", deMeaning: "Mein Herr, mehre mein Wissen.", trMeaning: "Rabbim, ilmimi artır.", repetition: nil, source: "Quran 20:114"),',
'        .init(deTitle: "Rabbi zidni ilma", trTitle: "Rabbî zidnî ilmâ", arabic: "رَبِّ زِدْنِي عِلْمًا", transliteration: "Rabbi zidnī ʿilmā", deMeaning: "Mein Herr, mehre mein Wissen.", trMeaning: "Rabbim, ilmimi artır.", repetition: nil, source: "Quran 20:114 · excerpt"),',
'home Quran 20:114 excerpt')
h = replace_once(h,
'        .init(deTitle: "Hasbunallahu", trTitle: "Hasbünallahu", arabic: "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ", transliteration: "Ḥasbunallāhu wa niʿma-l-wakīl", deMeaning: "Allah genügt uns, und Er ist der beste Sachwalter.", trMeaning: "Allah bize yeter, O ne güzel vekildir.", repetition: nil, source: "Quran 3:173"),',
'        .init(deTitle: "Hasbunallahu", trTitle: "Hasbünallahu", arabic: "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ", transliteration: "Ḥasbunallāhu wa niʿma-l-wakīl", deMeaning: "Allah genügt uns, und Er ist der beste Sachwalter.", trMeaning: "Allah bize yeter, O ne güzel vekildir.", repetition: nil, source: "Quran 3:173 · excerpt"),',
'home Quran 3:173 excerpt')
h = replace_once(h,
'        .init(deTitle: "Sayyidul Istighfar", trTitle: "Seyyidü\'l-istiğfar", arabic: "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلٰهَ إِلَّا أَنْتَ...", transliteration: "Allāhumma anta rabbī lā ilāha illā anta...", deMeaning: "Große Bittformel um Vergebung.", trMeaning: "Bağışlanma için çok faziletli dua.", repetition: "Morgens / agşam", source: "Bukhari 6306")',
'        .init(deTitle: "Sayyidul Istighfar · Beginn", trTitle: "Seyyidü\'l-istiğfar · başlangıç", arabic: "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلٰهَ إِلَّا أَنْتَ…", transliteration: "Allāhumma anta rabbī lā ilāha illā anta…", deMeaning: "Hier wird nur der Anfang der längeren Bittformel angezeigt.", trMeaning: "Burada uzun duanın yalnız başlangıcı gösterilir.", repetition: nil, source: "Bukhari 6306 · excerpt")',
'home Sayyidul excerpt')
home.write_text(h, encoding='utf-8')

# Prayer/Quran/adhkar content accuracy fixes.
g = guide.read_text(encoding='utf-8')
g = replace_once(g,
'        deMeaning: "Die eröffnende Sura. In jedem Rakʿah wird al-Fātiha rezitiert; nach ihrem Ende sagt man Âmîn.",\n        trMeaning: "Açılış sûresi. Her rekâtta Fâtiha okunur; sonunda Âmin denir.",\n        deNote: "Für den Wortlaut und Audio kannst du zusätzlich den Quran-Bereich öffnen.", trNote: "Metin ve ses için ayrıca Kur\'an bölümünü açabilirsin.")',
'        deMeaning: "Die eröffnende Sura. Beim Gebet allein oder als Imam wird al-Fātiha in jedem Rakʿah rezitiert; nach ihrem Ende sagt man Âmîn.",\n        trMeaning: "Açılış sûresi. Yalnız kılarken veya imam olarak her rekâtta Fâtiha okunur; sonunda Âmin denir.",\n        deNote: "Hanafi: Wer einem Imam folgt, rezitiert Fātiha und Zusatzsura nicht selbst. Wortlaut und Audio findest du zusätzlich im Quran-Bereich.", trNote: "Hanefî: İmama uyan kişi Fâtiha ve zamm-ı sûreyi kendisi okumaz. Metin ve ses ayrıca Kur\'an bölümündedir.")',
'prayer Fatiha congregational nuance')

g = replace_once(g,
'            .init(number: "4", pose: .standing, imageKey: "standing", deTitle: "Qiyām – Quran rezitieren", trTitle: "Kıyam – kıraat", deAction: "Im ersten Rakʿah: Eʿūḏu, Basmala, al-Fātiha, Âmîn und anschließend eine zusätzliche Sura oder passende Verse. Im zweiten Rakʿah beginnt man mit der Basmala, dann Fātiha und Zusatzsura.", trAction: "İlk rekâtta: Eûzü, Besmele, Fâtiha, Âmin ve ardından zamm-ı sûre veya uygun ayetler. İkinci rekâtta Besmele, Fâtiha ve zamm-ı sûre okunur.", deHanafi: "Bei 3-/4-Rakʿah-Fard wird im 3. und 4. Rakʿah nach hanafitischer Lehre grundsätzlich nur al-Fātiha gelesen. Vier-Rakʿah-Sunnah hat eigene Regeln – siehe Gebetsplan.", trHanafi: "3/4 rekât farz namazların 3. ve 4. rekâtında Hanefî uygulamada esas olarak yalnız Fâtiha okunur. Dört rekât sünnetlerin ayrıntısı için namaz planına bak.", recitations: [PrayerText.audhu, PrayerText.basmala, PrayerText.fatiha, PrayerText.ikhlas]),',
'            .init(number: "4", pose: .standing, imageKey: "standing", deTitle: "Qiyām – Quran rezitieren", trTitle: "Kıyam – kıraat", deAction: "Im ersten Rakʿah: Eʿūḏu, Basmala, al-Fātiha, Âmîn und anschließend eine zusätzliche Sura oder passende Verse. Im zweiten Rakʿah beginnt man mit der Basmala, dann Fātiha und Zusatzsura.", trAction: "İlk rekâtta: Eûzü, Besmele, Fâtiha, Âmin ve ardından zamm-ı sûre veya uygun ayetler. İkinci rekâtta Besmele, Fâtiha ve zamm-ı sûre okunur.", deHanafi: "Bei 3-/4-Rakʿah-Fard wird im 3. und 4. Rakʿah nach hanafitischer Lehre grundsätzlich nur al-Fātiha gelesen. Wer einem Imam folgt, rezitiert Fātiha und Zusatzsura nicht selbst. Vier-Rakʿah-Sunnah hat eigene Regeln – siehe Gebetsplan.", trHanafi: "3/4 rekât farz namazların 3. ve 4. rekâtında Hanefî uygulamada esas olarak yalnız Fâtiha okunur. İmama uyan kişi Fâtiha ve zamm-ı sûreyi kendisi okumaz. Dört rekât sünnetlerin ayrıntısı için namaz planına bak.", recitations: [PrayerText.audhu, PrayerText.basmala, PrayerText.fatiha, PrayerText.ikhlas]),',
'prayer step congregational nuance')

g = replace_once(g,
'        .init(reference: "Quran 20:114", arabic: "رَبِّ زِدْنِي عِلْمًا", transliteration: "Rabbi zidnī ʿilmā", de: "Mein Herr, mehre mein Wissen.", tr: "Rabbim, ilmimi artır."),',
'        .init(reference: "Quran 20:114 · excerpt", arabic: "رَبِّ زِدْنِي عِلْمًا", transliteration: "Rabbi zidnī ʿilmā", de: "Mein Herr, mehre mein Wissen.", tr: "Rabbim, ilmimi artır."),',
'quran dua 20:114 excerpt')
g = replace_once(g,
'        .init(reference: "Quran 25:74", arabic: "رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا", transliteration: "Rabbanā hab lanā min azwājinā wa dhurriyyātinā qurrata aʿyun...", de: "Unser Herr, schenke uns an unseren Ehepartnern und Nachkommen Freude und mache uns zu Vorbildern für Gottesbewusste.", tr: "Rabbimiz, eşlerimizi ve çocuklarımızı bize göz aydınlığı kıl ve bizi takvâ sahiplerine önder eyle."),',
'        .init(reference: "Quran 25:74", arabic: "رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا", transliteration: "Rabbanā hab lanā min azwājinā wa dhurriyyātinā qurrata aʿyunin wajʿalnā lil-muttaqīna imāmā", de: "Unser Herr, schenke uns an unseren Ehepartnern und Nachkommen Freude und mache uns zu Vorbildern für Gottesbewusste.", tr: "Rabbimiz, eşlerimizi ve çocuklarımızı bize göz aydınlığı kıl ve bizi takvâ sahiplerine önder eyle."),',
'quran dua 25:74 transliteration')
g = replace_once(g,
'        .init(reference: "Quran 3:8", arabic: "رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِنْ لَدُنْكَ رَحْمَةً", transliteration: "Rabbanā lā tuzigh qulūbanā baʿda idh hadaytanā wa hab lanā min ladunka raḥmah", de: "Unser Herr, lass unsere Herzen nicht abweichen, nachdem Du uns rechtgeleitet hast, und schenke uns Barmherzigkeit von Dir.", tr: "Rabbimiz, bize hidayet verdikten sonra kalplerimizi eğriltme; bize katından rahmet bağışla.")',
'        .init(reference: "Quran 3:8", arabic: "رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِنْ لَدُنْكَ رَحْمَةً إِنَّكَ أَنْتَ الْوَهَّابُ", transliteration: "Rabbanā lā tuzigh qulūbanā baʿda idh hadaytanā wa hab lanā min ladunka raḥmatan innaka anta-l-Wahhāb", de: "Unser Herr, lass unsere Herzen nicht abweichen, nachdem Du uns rechtgeleitet hast, und schenke uns Barmherzigkeit von Dir. Du bist wahrlich der Schenkende.", tr: "Rabbimiz, bize hidayet verdikten sonra kalplerimizi eğriltme; bize katından rahmet bağışla. Şüphesiz Sen çok bağışta bulunansın.")',
'quran dua 3:8 completeness')

g = replace_once(g,
'        .init(id: "threequls", deTitle: "Al-Ikhlas, Al-Falaq, An-Nas", trTitle: "İhlâs, Felak, Nâs", arabic: "قُلْ هُوَ اللَّهُ أَحَدٌ · قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ · قُلْ أَعُوذُ بِرَبِّ النَّاسِ", transliteration: "Qul huwa-llāhu aḥad · Qul aʿūdhu bi-rabbi-l-falaq · Qul aʿūdhu bi-rabbi-n-nās", deMeaning: "Die drei kurzen Suren werden in dieser Morgen-/Abend-Überlieferung jeweils dreimal rezitiert.", trMeaning: "Bu sabah-akşam zikrinde üç kısa sûre ayrı ayrı üçer kez okunur.", count: 3, source: "Hisn al-Muslim 76"),',
'        .init(id: "threequls", deTitle: "Al-Ikhlas, Al-Falaq, An-Nas", trTitle: "İhlâs, Felak, Nâs", arabic: "قُلْ هُوَ اللَّهُ أَحَدٌ · قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ · قُلْ أَعُوذُ بِرَبِّ النَّاسِ", transliteration: "Qul huwa-llāhu aḥad · Qul aʿūdhu bi-rabbi-l-falaq · Qul aʿūdhu bi-rabbi-n-nās", deMeaning: "Angezeigt sind nur die Anfangszeilen. Rezitiert werden die vollständigen Suren Al-Ikhlas, Al-Falaq und An-Nas jeweils dreimal.", trMeaning: "Burada yalnız başlangıç satırları gösterilir. İhlâs, Felak ve Nâs sûrelerinin tamamı ayrı ayrı üçer kez okunur.", count: 3, source: "Hisn al-Muslim 76"),',
'adhkar three quls excerpt clarification')
g = replace_once(g,
'        .init(id: "bika", deTitle: "Allahumma bika asbahna / amsayna", trTitle: "Allahümme bike asbahnâ / emseynâ", arabic: "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ", transliteration: "Allāhumma bika aṣbaḥnā wa bika amsaynā wa bika naḥyā wa bika namūt", deMeaning: "Bitte um Allahs Beistand für Morgen/Abend, Leben und Tod; abends wird die Formulierung entsprechend angepasst.", trMeaning: "Sabah/akşam, hayat ve ölüm için Allah\'a yöneliş; akşam ifadesi buna göre değiştirilir.", count: 1, source: "Hisn al-Muslim 78 · Tirmidhi"),',
'        .init(id: "bika", deTitle: "Allahumma bika asbahna / amsayna", trTitle: "Allahümme bike asbahnâ / emseynâ", arabic: "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ", transliteration: "Allāhumma bika aṣbaḥnā wa bika amsaynā wa bika naḥyā wa bika namūtu wa ilayka-n-nushūr", deMeaning: "Morgens wird die Morgenform, abends die überlieferte Abendform angezeigt.", trMeaning: "Sabah sabah şekli, akşam ise rivayet edilen akşam şekli gösterilir.", count: 1, source: "Hisn al-Muslim 78"),',
'adhkar bika morning completeness')
g = replace_once(g,
'        .init(id: "istighfar", deTitle: "Astaghfirullah", trTitle: "Estağfirullâh", arabic: "أَسْتَغْفِرُ اللَّهَ", transliteration: "Astaghfirullāh", deMeaning: "Ich bitte Allah um Vergebung.", trMeaning: "Allah\'tan bağışlanma dilerim.", count: 33, source: "Dhikr / İstiğfar"),',
'        .init(id: "istighfar", deTitle: "Astaghfirullah", trTitle: "Estağfirullâh", arabic: "أَسْتَغْفِرُ اللَّهَ", transliteration: "Astaghfirullāh", deMeaning: "Ich bitte Allah um Vergebung. Hier wird keine bestimmte überlieferte Anzahl behauptet.", trMeaning: "Allah\'tan bağışlanma dilerim. Burada rivayet edilmiş belirli bir sayı iddia edilmez.", count: 1, source: "Allgemeines Istighfar / genel istiğfar"),',
'adhkar istighfar fixed count')

old_feature = """    private func featuredDhikr(_ item: AdhkarEntry) -> some View {
        let current = progress(item)
        return VStack(spacing: 11) {
            Text(item.arabic)
                .font(.system(size: item.arabic.count < 30 ? 34 : 24, weight: .medium))"""
new_feature = """    private func featuredDhikr(_ item: AdhkarEntry) -> some View {
        let current = progress(item)
        let arabic = displayedArabic(for: item)
        let transliteration = displayedTransliteration(for: item)
        return VStack(spacing: 11) {
            Text(arabic)
                .font(.system(size: arabic.count < 30 ? 34 : 24, weight: .medium))"""
g = replace_once(g, old_feature, new_feature, 'adhkar displayed formula variables')
g = replace_once(g,
'                Text(item.transliteration)\n                    .font(.caption.weight(.semibold))',
'                Text(transliteration)\n                    .font(.caption.weight(.semibold))',
'adhkar displayed transliteration')

helper_anchor = """    private var visibleItems: [AdhkarEntry] {"""
helper = """    private func displayedArabic(for item: AdhkarEntry) -> String {
        if item.id == "bika", category == 1 {
            return "اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ أَصْبَحْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ"
        }
        return item.arabic
    }

    private func displayedTransliteration(for item: AdhkarEntry) -> String {
        if item.id == "bika", category == 1 {
            return "Allāhumma bika amsaynā wa bika aṣbaḥnā wa bika naḥyā wa bika namūtu wa ilayka-l-maṣīr"
        }
        return item.transliteration
    }

"""
if helper not in g:
    if g.count(helper_anchor) != 1:
        raise SystemExit('v440 adhkar helper anchor missing/duplicate')
    g = g.replace(helper_anchor, helper + helper_anchor, 1)

g = replace_once(g,
'                "Religiöse Einordnung nach Qur\'an, authentischen Hadithen und Diyanet-Grunddarstellung. Das angezeigte Hijri-Datum wird mit Umm-al-Qura berechnet; regionale Mondsichtung kann den tatsächlichen Monatsbeginn verschieben.",\n                "Dinî açıklama Kur\'an, sahih hadisler ve Diyanet temel anlatımına dayanır. Gösterilen hicrî tarih Ummü\'l-Kurâ hesabıdır; bölgesel hilal gözlemi gerçek ay başlangıcını değiştirebilir."',
'                "Religiöse Einordnung nach Qur\'an, Hadithquellen und Diyanet-Grunddarstellung. Bei Überlieferungen können unterschiedliche Einstufungen bestehen. Das angezeigte Hijri-Datum wird mit Umm-al-Qura berechnet; regionale Mondsichtung kann den tatsächlichen Monatsbeginn verschieben.",\n                "Dinî açıklama Kur\'an, hadis kaynakları ve Diyanet temel anlatımına dayanır. Rivayetlerin değerlendirilmesinde farklılıklar bulunabilir. Gösterilen hicrî tarih Ummü\'l-Kurâ hesabıdır; bölgesel hilal gözlemi gerçek ay başlangıcını değiştirebilir."',
'hijri source grading wording')
g = replace_once(g,
'                "Grundlage: Qur\'an, authentische Hadithe und Diyanet Temel İslâm Bilgileri / İlmihal. SalahPath erklärt Grundlagen; bei strittigen Fiqh-Fragen werden Rechtsschulunterschiede gesondert gekennzeichnet.",\n                "Temel kaynak: Kur\'an, sahih hadisler ve Diyanet Temel İslâm Bilgileri / İlmihal. SalahPath temel bilgileri açıklar; ihtilaflı fıkıh konularında mezhep farkları ayrıca belirtilir."',
'                "Grundlage: Qur\'an, Hadithquellen und Diyanet Temel İslâm Bilgileri / İlmihal. Bei Hadith-Einstufungen und strittigen Fiqh-Fragen können Unterschiede bestehen; Rechtsschulunterschiede werden soweit relevant gekennzeichnet.",\n                "Temel kaynak: Kur\'an, hadis kaynakları ve Diyanet Temel İslâm Bilgileri / İlmihal. Hadis değerlendirmelerinde ve ihtilaflı fıkıh konularında farklılıklar olabilir; ilgili mezhep farkları ayrıca belirtilir."',
'learning source grading wording')

guide.write_text(g, encoding='utf-8')
print('v440 applied: religious-content accuracy and release audits')
