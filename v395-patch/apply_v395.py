from pathlib import Path

def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"v395: anchor missing for {label}: {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

root = Path.cwd()

home = root / "SalahZeit" / "Views" / "HomeView.swift"
replace_once(
    home,
    '''                Link(settings.t("Diyanet-Quelle öffnen", "Diyanet kaynağını aç"), destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/kadinlarin-adet-veya-lohusalik-hallerinde-yapamayacaklari/0193c42d-4b21-7774-1a09-738831304296")!)
                    .font(.caption)
''',
    '''                Text(settings.t("Quelle: Diyanet Din İşleri Yüksek Kurulu.", "Kaynak: Diyanet Din İşleri Yüksek Kurulu."))
                    .font(.caption)
                    .foregroundStyle(.secondary)
''',
    "tracker Diyanet source link",
)
replace_once(
    home,
    '''                            Link(destination: URL(string: "https://maps.apple.com/?q=Kaaba&ll=21.4225,39.8262")!) {
                                referenceMapTile
                            }
                            .buttonStyle(.plain)
                            .accessibilityLabel(settings.t(
                                "Kaaba in Apple Maps öffnen",
                                "Kâbe'yi Apple Maps'te aç"
                            ))
''',
    '''                            referenceMapTile
                                .accessibilityElement(children: .ignore)
                                .accessibilityLabel(settings.t(
                                    "Kaaba und Gebetsrichtung",
                                    "Kâbe ve kıble yönü"
                                ))
''',
    "external Kaaba maps link",
)

guide = root / "SalahZeit" / "Views" / "GuideView.swift"
replace_once(
    guide,
    '''                    Link(settings.t("Diyanet · Gebet von Frauen und Männern", "Diyanet · Kadın/erkek namaz farkları"), destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/kilinis-bakimindan-kadinlarin-namazi-ile-erkeklerin-namazi/0193c42d-64a5-7ba1-9af3-f9f4a7f97245")!)
                    Link(settings.t("Diyanet · Ruhe in den Gebetspositionen", "Diyanet · Ta'dîl-i erkân"), destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/namazda-tadil-i-erkanin-hukmu-nedir/0193c42d-4ed9-7a2a-78a0-a569a0ff598a")!)
                    Link(settings.t("Diyanet · Salām zum Gebetsabschluss", "Diyanet · Selâm"), destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/namazdan-cikarken-verilen-selamin-hukmu-nedir/0193c42d-4f73-7e54-2687-55f6addfa71f")!)
''',
    '''                    Text(settings.t(
                        "Quelle in SalahPath: Diyanet Namaz İlmihali und Din İşleri Yüksek Kurulu – hanafitische Darstellung zu Gebetshaltungen, Ruhe in den Positionen und Salām.",
                        "SalahPath içi kaynak: Diyanet Namaz İlmihali ve Din İşleri Yüksek Kurulu – namaz duruşları, ta'dîl-i erkân ve selâm için Hanefî anlatım."
                    ))
                    .font(.caption)
                    .foregroundStyle(.secondary)
''',
    "prayer external source links",
)
replace_once(
    guide,
    '''            Section {
                Link("Diyanet · Namaz İlmihali", destination: URL(string: "https://dijital.diyanet.gov.tr/File/Download?id=394&path=namaz_ilmihali.pdf")!)
            }
''',
    '''            Section(settings.t("Quelle", "Kaynak")) {
                Text(settings.t(
                    "Diyanet Namaz İlmihali · hanafitische Grunddarstellung. Alle für diesen Ablauf benötigten Erklärungen stehen direkt in SalahPath.",
                    "Diyanet Namaz İlmihali · Hanefî temel anlatım. Bu akış için gereken açıklamaların tamamı doğrudan SalahPath içinde yer alır."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
''',
    "prayer plan PDF link",
)
replace_once(
    guide,
    '''                VStack(alignment:.leading,spacing:6) {
                    Link(settings.t("Diyanet · Wie wird Wudu durchgeführt?", "Diyanet · Abdest nasıl alınır?"), destination: URL(string:"https://kurul.diyanet.gov.tr/tr/fetva/abdest-nedir-ve-nasil-alinir/0193c42d-4493-7cd5-0d48-874d6be1a7d3")!)
                    Link(settings.t("Diyanet · Pflichtbestandteile des Wudu", "Diyanet · Abdestin farzları"), destination: URL(string:"https://kurul.diyanet.gov.tr/tr/fetva/mezhepler-arasinda-abdestin-farzlari-konusunda-farklilik/0193c42d-44c2-71a2-18f9-9a29fcdbaa43")!)
                }.cardStyle(material:true)
''',
    '''                VStack(alignment:.leading,spacing:6) {
                    Text(settings.t("Quelle", "Kaynak")).font(.headline)
                    Text(settings.t(
                        "Diyanet Namaz İlmihali und Din İşleri Yüksek Kurulu. Die vollständige Lernreihenfolge und die vier Farz-Bestandteile sind oben direkt erklärt; du musst SalahPath dafür nicht verlassen.",
                        "Diyanet Namaz İlmihali ve Din İşleri Yüksek Kurulu. Tam öğrenme sırası ve abdestin dört farzı yukarıda doğrudan açıklanır; bunun için SalahPath'ten çıkman gerekmez."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                }.cardStyle(material:true)
''',
    "Wudu external source links",
)

text = guide.read_text(encoding="utf-8")
start_marker = "private struct PrayerDuaLink: Identifiable {"
end_marker = "\nprivate struct ShortSurahAudio: Identifiable {"
if start_marker not in text or end_marker not in text:
    raise SystemExit("v395: prayer dua external-link section anchor missing")
start = text.index(start_marker)
end = text.index(end_marker, start)
replacement = '''private struct PrayerDuaLesson: Identifiable {
    let id = UUID()
    let deTitle: String
    let trTitle: String
    let deDetail: String
    let trDetail: String
    let recitations: [PrayerRecitation]
}

struct PrayerDuaAudioView: View {
    @EnvironmentObject private var settings: SettingsStore

    private let duas: [PrayerDuaLesson] = [
        .init(
            deTitle: "Sübhaneke", trTitle: "Sübhâneke",
            deDetail: "Einstiegsdua im ersten Rakʿah direkt nach dem Eröffnungstakbir.",
            trDetail: "İlk rekâtta iftitah tekbirinden hemen sonra okunan başlangıç duası.",
            recitations: [PrayerText.subhanaka]
        ),
        .init(
            deTitle: "Ettehiyyatü / Tahiyyat", trTitle: "Ettehiyyâtü / Tahiyyat",
            deDetail: "Wird im ersten Sitzen nach zwei Rakʿah und erneut im letzten Sitzen gelesen.",
            trDetail: "İki rekâttan sonraki ilk oturuşta ve son oturuşta okunur.",
            recitations: [PrayerText.tahiyyat]
        ),
        .init(
            deTitle: "Allahümme Salli & Barik", trTitle: "Allâhümme Salli ve Bârik",
            deDetail: "Im letzten Sitzen nach Ettehiyyatü lesen.",
            trDetail: "Son oturuşta Ettehiyyâtü'den sonra okunur.",
            recitations: [PrayerText.salli, PrayerText.barik]
        ),
        .init(
            deTitle: "Rabbena-Dua", trTitle: "Rabbenâ duası",
            deDetail: "Abschlussdua im letzten Sitzen vor dem Salam.",
            trDetail: "Son oturuşta selâmdan önce okunan kapanış duası.",
            recitations: [PrayerText.rabbana]
        )
    ]

    var body: some View {
        List {
            Section {
                Text(settings.t(
                    "Alle Gebetsduas stehen direkt in SalahPath: Arabisch, Umschrift und Bedeutung. Es wird keine externe Webseite geöffnet. Ein Audio-Button wird nur dort angezeigt, wo SalahPath auch wirklich Audio abspielen kann.",
                    "Namaz dualarının tamamı doğrudan SalahPath içinde yer alır: Arapça, okunuş ve anlam. Harici web sitesi açılmaz. Ses düğmesi yalnız SalahPath gerçekten ses çalabildiğinde gösterilir."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }

            ForEach(duas) { item in
                Section(settings.language == .german ? item.deTitle : item.trTitle) {
                    Text(settings.language == .german ? item.deDetail : item.trDetail)
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    ForEach(item.recitations) { recitation in
                        PrayerRecitationView(recitation: recitation)
                    }
                }
            }

            Section(settings.t("Quelle", "Kaynak")) {
                Text(settings.t(
                    "Diyanet Namaz İlmihali · Gebetsduas und hanafitischer Gebetsablauf.",
                    "Diyanet Namaz İlmihali · namaz duaları ve Hanefî namaz akışı."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetsduas", "Namaz duaları"))
        .navigationBarTitleDisplayMode(.inline)
    }
}
'''
guide.write_text(text[:start] + replacement + text[end:], encoding="utf-8")

print("v395 applied: learning content stays inside SalahPath; fake external prayer-dua links removed")
