from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = '''    private let sequence: [(pose: String, de: String, tr: String)] = [
        ("intention", "Absicht", "Niyet"),
        ("takbir", "Takbīr", "Tekbir"),
        ("standing", "Stehen", "Kıyam"),
        ("bowing", "Verbeugung", "Rükû"),
        ("upright", "Aufrichten", "Kavme"),
        ("sujud", "Niederwerfung", "Secde"),
        ("sitting", "Sitzen", "Oturuş"),
        ("salam_right", "Salām", "Selâm")
    ]
'''
new = '''    private let sequence: [(pose: String, de: String, tr: String)] = [
        ("intention", "Absicht vor Beginn", "Namaza niyet"),
        ("takbir", "Eröffnungstakbīr", "İftitah tekbiri"),
        ("standing", "Stehen · Qiyām", "Kıyam"),
        ("bowing", "Rukūʿ", "Rükû"),
        ("upright", "Ganz aufrichten", "Tam doğrulma"),
        ("sujud", "Sujud 1", "1. secde"),
        ("sitting", "Zwischen den Sujud", "İki secde arası"),
        ("sujud", "Sujud 2 · Rakʿa fertig", "2. secde · rekât tamam"),
        ("final_sitting", "Letztes Sitzen", "Son oturuş"),
        ("salam_right", "Salām rechts · nur Kopf", "Sağa selâm · yalnız baş"),
        ("salam_left", "Salām links · nur Kopf", "Sola selâm · yalnız baş")
    ]
'''
if old not in text:
    raise SystemExit("v432: prayer overview sequence anchor missing")
text = text.replace(old, new, 1)

old = '''                .padding(13)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }

                LazyVGrid(
'''
new = '''                .padding(13)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }

                VStack(alignment: .leading, spacing: 8) {
                    Label(
                        settings.t("Wichtig: Das Gebet besteht nicht nur aus 1 Rakʿa", "Önemli: Namaz yalnız 1 rekâttan oluşmaz"),
                        systemImage: "info.circle.fill"
                    )
                    .font(.headline.bold())
                    .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Nach dem zweiten Sujud ist genau EINE Rakʿa abgeschlossen. Je nach Gebet stehst du danach zur nächsten Rakʿa auf oder bleibst zum vorgeschriebenen Sitzen. Das letzte Sitzen und der Salām kommen erst nach der letzten Rakʿa.",
                        "İkinci secdeden sonra tam BİR rekât tamamlanır. Namaza göre bundan sonra sonraki rekâta kalkarsın veya gereken oturuşta kalırsın. Son oturuş ve selâm yalnız son rekâttan sonra gelir."
                    ))
                    .font(.subheadline)
                    .fixedSize(horizontal: false, vertical: true)

                    Text(settings.t(
                        "Rukūʿ und Sujud werden teilweise von der Seite gezeichnet, damit die Haltung erkennbar ist. Du änderst dabei NICHT deine Richtung zur Qibla.",
                        "Rükû ve secde duruşu anlaşılır olsun diye bazı çizimler yandan gösterilir. Bu sırada kıble yönünü DEĞİŞTİRMEZSİN."
                    ))
                    .font(.footnote.bold())
                    .foregroundStyle(SalahTheme.teal)
                }
                .padding(13)
                .background(SalahTheme.softTeal.opacity(0.45), in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.teal.opacity(0.30), lineWidth: 1) }

                LazyVGrid(
'''
if old not in text:
    raise SystemExit("v432: prayer overview explainer insertion anchor missing")
text = text.replace(old, new, 1)

old = '''                Text(settings.t(
                    "Die Übersicht zeigt die Grundbewegungen. Für Rezitationen, Rakʿah-Details und hanafitische Unterschiede nutze die Schritt-für-Schritt-Anleitung.",
                    "Bu özet temel hareketleri gösterir. Okunan metinler, rekât ayrıntıları ve Hanefî farklılıklar için adım adım anlatımı kullan."
                ))
                .font(.footnote)
                .foregroundStyle(SalahTheme.mutedInk)
                .padding(.horizontal, 2)
'''
new = '''                Text(settings.t(
                    "Beim Salām dreht sich nur der Kopf: zuerst zur eigenen rechten Schulter, danach zur eigenen linken Schulter. Der Oberkörper bleibt zur Qibla. Die männlichen und weiblichen Haltungen werden in SalahPath getrennt nach der hanafitischen/Diyanet-Lernpraxis dargestellt; andere Rechtsschulen können einzelne Sunnah-Details anders lehren.",
                    "Selâm verirken yalnız baş çevrilir: önce kendi sağ omzuna, sonra kendi sol omzuna. Gövde kıbleye dönük kalır. SalahPath erkek ve kadın duruşlarını Hanefî/Diyanet öğrenme uygulamasına göre ayrı gösterir; diğer mezhepler bazı sünnet ayrıntılarını farklı öğretebilir."
                ))
                .font(.footnote)
                .foregroundStyle(SalahTheme.mutedInk)
                .padding(.horizontal, 2)
'''
if old not in text:
    raise SystemExit("v432: prayer overview footer anchor missing")
text = text.replace(old, new, 1)

old = '''        let hip = point(0.48, 0.62, in: size)
        let shoulder = point(0.48, 0.40, in: size)
        let headX = 0.48 + CGFloat(turn) * 0.035
        let headCenter = point(headX, 0.27, in: size)
'''
new = '''        let hip = point(0.48, 0.62, in: size)
        let shoulder = point(0.48, 0.40, in: size)
        // Keep the whole body and head centered. For Salam only the facial
        // features indicate the head turn; the torso never appears to rotate.
        let headCenter = point(0.48, 0.27, in: size)
'''
if old not in text:
    raise SystemExit("v432: sitting head-position anchor missing")
text = text.replace(old, new, 1)

old = '''        if turn != 0 {
            let x = turn > 0 ? size.width * 0.76 : size.width * 0.20
            var arrow = Path()
            arrow.move(to: CGPoint(x: size.width * 0.50, y: size.height * 0.20))
            arrow.addLine(to: CGPoint(x: x, y: size.height * 0.20))
            context.stroke(arrow, with: .color(SalahTheme.gold), style: StrokeStyle(lineWidth: 5, lineCap: .round))
        }
'''
new = '''        // No body-direction arrow here: the worshipper remains facing Qibla.
        // PrayerPoseArtwork.drawFace shifts only the facial features for Salam.
'''
if old not in text:
    raise SystemExit("v432: Salam direction-arrow anchor missing")
text = text.replace(old, new, 1)

guide.write_text(text, encoding="utf-8")
print("v432 applied: complete Rakʿa overview and head-only Salam direction")
