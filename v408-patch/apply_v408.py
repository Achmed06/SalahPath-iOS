from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

anchor = '''                    VStack(alignment: .leading, spacing: 7) {
                        Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama"))
'''
insert = '''                    VStack(alignment: .leading, spacing: 9) {
                        Text(settings.t("Weitere rituelle Reinigung", "Diğer hükmî temizlikler"))
                            .font(.headline.bold())
                            .foregroundStyle(SalahTheme.deepTeal)

                        NavigationLink { GhuslGuideView() } label: {
                            Label(settings.t("Ghusl · Ganzkörperwaschung", "Gusül · boy abdesti"), systemImage: "shower.fill")
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        .buttonStyle(.plain)

                        Divider()

                        NavigationLink { TayammumGuideView() } label: {
                            Label(settings.t("Tayammum · wenn Wasser nicht nutzbar ist", "Teyemmüm · su kullanılamadığında"), systemImage: "hand.raised.fill")
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        .buttonStyle(.plain)
                    }
                    .cardStyle()

''' + anchor
if anchor not in text:
    raise SystemExit("v408: Wudu source-card anchor missing")
text = text.replace(anchor, insert, 1)

insert_marker = "\n// MARK: - Terms"
if insert_marker not in text:
    raise SystemExit("v408: terms insertion marker missing")

new_views = r'''
// MARK: - Ghusl and Tayammum

struct GhuslGuideView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 8) {
                    Label(settings.t("Was ist Ghusl?", "Gusül nedir?"), systemImage: "shower.fill")
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Ghusl ist die rituelle Ganzkörperwaschung. Sie wird nötig, wenn der Zustand großer ritueller Unreinheit beendet werden muss, zum Beispiel nach Geschlechtsverkehr, Samenerguss/feuchtem Traum sowie nach Ende von Menstruation oder Wochenbett.",
                        "Gusül, hükmî büyük kirlilik hâlini gidermek için yapılan boy abdestidir. Cinsel ilişki, meni gelmesi/ihtilam ve hayız veya nifasın sona ermesi gibi durumlarda gerekir."
                    ))
                    .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 9) {
                    Text(settings.t("Die 3 Farz im Hanafi/Diyanet-Ablauf", "Hanefî/Diyanet'e göre 3 farz"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    numbered("1", settings.t(
                        "Den Mund vollständig ausspülen, sodass Wasser den ganzen Mundraum erreicht.",
                        "Ağzı, su ağız boşluğunun her yerine ulaşacak şekilde tamamen çalkalamak."
                    ))
                    numbered("2", settings.t(
                        "Wasser in die Nase geben und die Nase reinigen.",
                        "Buruna su vermek ve burnu temizlemek."
                    ))
                    numbered("3", settings.t(
                        "Den gesamten Körper waschen, ohne eine waschpflichtige Stelle trocken zu lassen.",
                        "Yıkanması gereken hiçbir yeri kuru bırakmadan bütün bedeni yıkamak."
                    ))

                    Text(settings.t(
                        "Wichtig: Nach hanafitischer Auffassung gehören Mund und Nase zum Farz des Ghusl. Niyyah und Bismillah sind Sunnah. In anderen Rechtsschulen kann die Einordnung einzelner Punkte abweichen.",
                        "Önemli: Hanefî görüşte ağız ve burun guslün farzlarındandır. Niyet ve besmele sünnettir. Diğer mezheplerde bazı ayrıntıların hükmü farklı olabilir."
                    ))
                    .font(.footnote.bold())
                    .foregroundStyle(SalahTheme.deepTeal)
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Vollständiger Sunnah-Ablauf", "Sünnete uygun tam uygulama"))
                        .font(.headline.bold())

                    step("1", settings.t("Absicht fassen und Bismillah sagen.", "Niyet et ve besmele çek."))
                    step("2", settings.t("Hände waschen. Sichtbare Verunreinigung am Körper entfernen und Intimbereich reinigen.", "Ellerini yıka. Bedendeki görünen necaseti gider ve avret bölgesini temizle."))
                    step("3", settings.t("Mund gründlich 3× ausspülen.", "Ağzı 3 kez iyice çalkala."))
                    step("4", settings.t("Nase 3× mit Wasser reinigen.", "Burnu 3 kez suyla temizle."))
                    step("5", settings.t("Wudu wie für das Gebet durchführen. Wenn sich Wasser am Boden sammelt, können die Füße bis zum Ende warten.", "Namaz abdesti gibi abdest al. Su ayak altında birikiyorsa ayakları sona bırakabilirsin."))
                    step("6", settings.t("Den ganzen Körper vollständig waschen. Wasser muss Haut und erreichbare Haarbereiche überall erreichen.", "Bütün bedeni tamamen yıka. Su derinin ve ulaşılabilir saç bölgelerinin her yerine ulaşmalı."))
                    step("7", settings.t("Besonders kontrollieren: Haaransatz, hinter den Ohren, Bauchnabel, Achseln, Hautfalten, zwischen Fingern und Zehen sowie Stellen unter Schmuck.", "Özellikle saç diplerini, kulak arkasını, göbeği, koltuk altını, deri kıvrımlarını, parmak aralarını ve takı altlarını kontrol et."))
                    step("8", settings.t("Falls die Füße vorher ausgelassen wurden, zum Schluss vollständig waschen.", "Ayaklar önce bırakıldıysa sonunda tamamen yıka."))
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 8) {
                    Text(settings.t("Haare & Frauen", "Saç ve kadınlar"))
                        .font(.headline.bold())
                    Text(settings.t(
                        "Das Wasser muss die Kopfhaut und die Haarwurzeln erreichen. Bei zusammengebundenen oder geflochtenen Haaren ist entscheidend, dass Wasser die Wurzeln erreicht; unnötiges Erschweren soll vermieden werden. Bei konkreten Fragen zu sehr dichtem Haar, Extensions oder wasserundurchlässigen Produkten die hanafitische Regel gezielt prüfen.",
                        "Su saç derisine ve saç diplerine ulaşmalıdır. Toplu veya örgülü saçta önemli olan suyun köklere ulaşmasıdır; gereksiz zorluk çıkarılmaz. Çok sık saç, ek saç veya su geçirmeyen ürünler gibi özel durumda Hanefî hükmü ayrıca kontrol edilmelidir."
                    ))
                    .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 8) {
                    Text(settings.t("Brauche ich danach noch Wudu?", "Sonra yeniden abdest gerekir mi?"))
                        .font(.headline.bold())
                    Text(settings.t(
                        "Ein gültiger Ghusl umfasst auch Wudu. Wenn während oder nach dem Ghusl nichts passiert, was Wudu bricht, ist danach kein zusätzliches Wudu nötig.",
                        "Geçerli bir gusül abdesti de kapsar. Gusül sırasında veya sonrasında abdesti bozan bir durum olmazsa ayrıca yeniden abdest almak gerekmez."
                    ))
                }
                .cardStyle(material: true)

                sourceNote
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Ghusl lernen", "Gusül öğren"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func numbered(_ n: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Text(n)
                .font(.caption.bold())
                .foregroundStyle(.white)
                .frame(width: 26, height: 26)
                .background(SalahTheme.teal, in: Circle())
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }

    @ViewBuilder
    private func step(_ n: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Text(n)
                .font(.caption.bold())
                .foregroundStyle(SalahTheme.deepTeal)
                .frame(width: 26, height: 26)
                .background(SalahTheme.gold.opacity(0.22), in: Circle())
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }

    private var sourceNote: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama")).font(.headline)
            Text(settings.t(
                "Qur'an 4:43 und 5:6 · Diyanet Din İşleri Yüksek Kurulu: Ghusl/Boy abdesti. Darstellung: hanafitischer Grundablauf.",
                "Kur'an 4:43 ve 5:6 · Diyanet Din İşleri Yüksek Kurulu: Gusül/boy abdesti. Anlatım: Hanefî temel uygulama."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }
}

struct TayammumGuideView: View {
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 8) {
                    Label(settings.t("Was ist Tayammum?", "Teyemmüm nedir?"), systemImage: "hand.raised.fill")
                        .font(.title2.bold())
                        .foregroundStyle(SalahTheme.deepTeal)
                    Text(settings.t(
                        "Tayammum ist eine erlaubte Ersatzreinigung, wenn kein Wasser vorhanden ist oder Wasser aus einem anerkannten Grund nicht benutzt werden kann. Es ersetzt unter diesen Voraussetzungen Wudu oder Ghusl.",
                        "Teyemmüm, su bulunmadığında veya geçerli bir sebeple su kullanılamadığında yapılan hükmî temizliktir. Şartları oluştuğunda abdestin veya guslün yerine geçer."
                    ))
                    .fixedSize(horizontal: false, vertical: true)
                }
                .cardStyle(material: true)

                VStack(alignment: .leading, spacing: 9) {
                    Text(settings.t("Wann darf ich Tayammum machen?", "Ne zaman teyemmüm yapılır?"))
                        .font(.headline.bold())
                    bullet(settings.t("Es ist kein ausreichendes Wasser erreichbar.", "Yeterli su bulunamıyor veya ulaşılamıyor."))
                    bullet(settings.t("Wasser zu benutzen würde wegen Krankheit oder Verletzung voraussichtlich schaden.", "Hastalık veya yara nedeniyle su kullanmak zarar verecek."))
                    bullet(settings.t("Eine anerkannte Unmöglichkeit der Wassernutzung liegt vor; bloße Bequemlichkeit reicht nicht.", "Suyu kullanmaya gerçek bir engel var; yalnız kolaylık istemek yeterli değildir."))
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 10) {
                    Text(settings.t("Tayammum Schritt für Schritt", "Teyemmüm adım adım"))
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    step("1", settings.t(
                        "Fasse die Absicht, Tayammum für Wudu oder Ghusl zu machen.",
                        "Abdest veya gusül yerine teyemmüm etmeye niyet et."
                    ))
                    step("2", settings.t(
                        "Lege bzw. schlage beide geöffneten Hände auf saubere Erde oder etwas von erdiger/mineralischer Art. Bewege sie leicht vor und zurück und klopfe überschüssigen Staub ab.",
                        "Parmaklar açık şekilde iki elini temiz toprağa veya toprak cinsinden bir yüzeye vur/temas ettir; hafifçe ileri geri hareket ettir ve fazla tozu silk."
                    ))
                    step("3", settings.t(
                        "Wische mit beiden Handflächen das gesamte Gesicht einmal.",
                        "İki elin içiyle yüzün tamamını bir kez mesh et."
                    ))
                    step("4", settings.t(
                        "Berühre die saubere Erdoberfläche ein zweites Mal.",
                        "Ellerini temiz toprağa ikinci kez temas ettir."
                    ))
                    step("5", settings.t(
                        "Wische zuerst den rechten Arm einschließlich Ellenbogen mit der linken Hand.",
                        "Sol elinle sağ kolu dirsekle birlikte mesh et."
                    ))
                    step("6", settings.t(
                        "Wische danach den linken Arm einschließlich Ellenbogen mit der rechten Hand.",
                        "Sağ elinle sol kolu dirsekle birlikte mesh et."
                    ))
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 9) {
                    Text(settings.t("Was beendet Tayammum?", "Teyemmümü ne bozar?"))
                        .font(.headline.bold())
                    bullet(settings.t("Alles, was normalerweise Wudu bricht, beendet auch Tayammum.", "Abdesti bozan şeyler teyemmümü de bozar."))
                    bullet(settings.t("Wenn wieder ausreichend Wasser verfügbar und nutzbar wird, endet die Tayammum-Erlaubnis.", "Yeterli su bulunur ve kullanılabilir hale gelirse teyemmüm ruhsatı sona erer."))
                    bullet(settings.t("Wenn der medizinische oder andere Grund entfällt, der Wasser unmöglich machte, endet die Ersatzregel.", "Suyu kullanmaya engel olan hastalık veya diğer mazeret ortadan kalkarsa teyemmüm hükmü sona erer."))
                }
                .cardStyle()

                VStack(alignment: .leading, spacing: 6) {
                    Text(settings.t("Quelle & Einordnung", "Kaynak ve açıklama")).font(.headline)
                    Text(settings.t(
                        "Qur'an 4:43 und 5:6 · Diyanet Din İşleri Yüksek Kurulu: Tayammum. Darstellung: hanafitischer Grundablauf.",
                        "Kur'an 4:43 ve 5:6 · Diyanet Din İşleri Yüksek Kurulu: Teyemmüm. Anlatım: Hanefî temel uygulama."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }
                .cardStyle(material: true)
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Tayammum lernen", "Teyemmüm öğren"))
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func step(_ n: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Text(n)
                .font(.caption.bold())
                .foregroundStyle(.white)
                .frame(width: 26, height: 26)
                .background(SalahTheme.teal, in: Circle())
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }

    @ViewBuilder
    private func bullet(_ text: String) -> some View {
        HStack(alignment: .top, spacing: 9) {
            Image(systemName: "checkmark.circle.fill")
                .foregroundStyle(SalahTheme.teal)
                .padding(.top, 2)
            Text(text).fixedSize(horizontal: false, vertical: true)
        }
    }
}
'''

text = text.replace(insert_marker, new_views + insert_marker, 1)
guide.write_text(text, encoding="utf-8")
print("v408 applied: Ghusl and Tayammum guides integrated under Wudu")
