from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

replacements = [
    (
        'settings.t("Niyyah, Suhoor, Fajr, Tagesablauf und Iftar", "Niyet, sahur, imsak, günün akışı ve iftar")',
        'settings.t("Absicht, Sahur, Fajr, Tagesablauf und Iftar", "Niyet, sahur, imsak, günün akışı ve iftar")'
    ),
    (
        'settings.t("Nährende oder gıdaähnliche Zuführung bricht nach Diyanet das Fasten; medizinische Einzelfälle separat prüfen.", "Besleyici veya gıda hükmündeki uygulamalar Diyanet\'e göre orucu bozar; tıbbî özel durumlar ayrıca değerlendirilmelidir.")',
        'settings.t("Nährende oder einer Nahrungsaufnahme gleichkommende Zuführung bricht nach Diyanet das Fasten; medizinische Einzelfälle separat prüfen.", "Besleyici veya gıda hükmündeki uygulamalar Diyanet\'e göre orucu bozar; tıbbî özel durumlar ayrıca değerlendirilmelidir.")'
    ),
    (
        'settings.t("Absichtlich mundvoll erbrechen", "Kasten ağız dolusu kusmak")',
        'settings.t("Absichtlich mundvoll erbrechen", "Bilerek ağız dolusu kusmak")'
    ),
    (
        '"Ghusl ist die rituelle Ganzkörperwaschung. Sie wird nötig, wenn der Zustand großer ritueller Unreinheit beendet werden muss, zum Beispiel nach Geschlechtsverkehr, Samenerguss/feuchtem Traum sowie nach Ende von Menstruation oder Wochenbett.",',
        '"Ghusl ist die rituelle Ganzkörperwaschung. Sie wird nötig, wenn der Zustand großer ritueller Unreinheit beendet werden muss, zum Beispiel nach Geschlechtsverkehr, nach Samenerguss oder nach einem feuchten Traum, wenn beim Aufwachen entsprechende Flüssigkeit festgestellt wird, sowie nach Ende von Menstruation oder Wochenbett.",'
    ),
    (
        '"Gusül, hükmî büyük kirlilik hâlini gidermek için yapılan boy abdestidir. Cinsel ilişki, meni gelmesi/ihtilam ve hayız veya nifasın sona ermesi gibi durumlarda gerekir."',
        '"Gusül, hükmî büyük kirlilik hâlini gidermek için yapılan boy abdestidir. Cinsel ilişki, meni gelmesi veya ihtilamdan sonra uyandığında ıslaklık görülmesi ile hayız ya da nifasın sona ermesi gibi durumlarda gerekir."'
    ),
    (
        'deRecommended: ["Fasten mit Niyyah beginnen.", "Gebete, Qur\'an, Dua, Dhikr und Sadaqah bewusst verstärken.", "Suhur und Iftar ohne Verschwendung gestalten."]',
        'deRecommended: ["Das Fasten mit bewusster Absicht beginnen.", "Gebete, Qur\'an, Dua, Dhikr und Sadaqah bewusst verstärken.", "Sahur und Iftar ohne Verschwendung gestalten."]'
    )
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f"v414: copy anchor missing: {old[:90]}")
    text = text.replace(old, new, 1)

guide.write_text(text, encoding="utf-8")
print("v414 applied: beginner wording, fasting copy, and wet-dream Ghusl precision corrected")
