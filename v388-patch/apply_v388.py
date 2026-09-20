from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

replacements = {
    'Link("Diyanet · Kadın/erkek namaz farkları", destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/kilinis-bakimindan-kadinlarin-namazi-ile-erkeklerin-namazi/0193c42d-64a5-7ba1-9af3-f9f4a7f97245")!)':
    'Link(settings.t("Diyanet · Gebet von Frauen und Männern", "Diyanet · Kadın/erkek namaz farkları"), destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/kilinis-bakimindan-kadinlarin-namazi-ile-erkeklerin-namazi/0193c42d-64a5-7ba1-9af3-f9f4a7f97245")!)',

    'Link("Diyanet · Ta\'dîl-i erkân", destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/namazda-tadil-i-erkanin-hukmu-nedir/0193c42d-4ed9-7a2a-78a0-a569a0ff598a")!)':
    'Link(settings.t("Diyanet · Ruhe in den Gebetspositionen", "Diyanet · Ta\'dîl-i erkân"), destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/namazda-tadil-i-erkanin-hukmu-nedir/0193c42d-4ed9-7a2a-78a0-a569a0ff598a")!)',

    'Link("Diyanet · Selâm", destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/namazdan-cikarken-verilen-selamin-hukmu-nedir/0193c42d-4f73-7e54-2687-55f6addfa71f")!)':
    'Link(settings.t("Diyanet · Salām zum Gebetsabschluss", "Diyanet · Selâm"), destination: URL(string: "https://kurul.diyanet.gov.tr/tr/fetva/namazdan-cikarken-verilen-selamin-hukmu-nedir/0193c42d-4f73-7e54-2687-55f6addfa71f")!)',

    'Link("Diyanet · Abdest nasıl alınır?", destination: URL(string:"https://kurul.diyanet.gov.tr/tr/fetva/abdest-nedir-ve-nasil-alinir/0193c42d-4493-7cd5-0d48-874d6be1a7d3")!)':
    'Link(settings.t("Diyanet · Wie wird Wudu durchgeführt?", "Diyanet · Abdest nasıl alınır?"), destination: URL(string:"https://kurul.diyanet.gov.tr/tr/fetva/abdest-nedir-ve-nasil-alinir/0193c42d-4493-7cd5-0d48-874d6be1a7d3")!)',

    'Link("Diyanet · Abdestin farzları", destination: URL(string:"https://kurul.diyanet.gov.tr/tr/fetva/mezhepler-arasinda-abdestin-farzlari-konusunda-farklilik/0193c42d-44c2-71a2-18f9-9a29fcdbaa43")!)':
    'Link(settings.t("Diyanet · Pflichtbestandteile des Wudu", "Diyanet · Abdestin farzları"), destination: URL(string:"https://kurul.diyanet.gov.tr/tr/fetva/mezhepler-arasinda-abdestin-farzlari-konusunda-farklilik/0193c42d-44c2-71a2-18f9-9a29fcdbaa43")!)',
}

for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f"v3.88: link anchor missing: {old[:60]}")
    s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.88 localized Diyanet source labels applied")
