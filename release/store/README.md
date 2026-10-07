# SalahPath: Unterlagen für App Store Connect

Vorbereiteter Stand: **3.62 / Build 79**, App-Quellstand `2d00fa91c3315908c062a8714cb280b954347800`.

Dieses Paket enthält Texte zum Übertragen in App Store Connect, echte Simulatoraufnahmen, einen Gerätetestplan und einen Entwurf für die offene Anbieteranfrage. Es enthält keine signierte App und ist keine Bestätigung einer Apple-Freigabe.

Eigentümerangaben vom 7. Oktober 2026: Die Apple-Developer-Anmeldung ist noch **pending**. Als öffentliche Support- und Datenschutzadresse ist **Muhammed_Y@outlook.de** freigegeben. Der Kontostatus wurde vom Eigentümer mitgeteilt und nicht im Apple-Konto geprüft.

## Dateien verwenden

Zum Einstieg **`START-HIER.md`** öffnen. `app-store-connect-fields.md` ordnet die vorbereiteten Werte den Apple-Feldern zu. `signing-setup.md` erklärt den manuell startbaren GitHub-Ablauf für einen signierten Export und optionalen TestFlight-Upload. `testflight-de.txt` und `testflight-tr.txt` enthalten die vorbereiteten Beta-Texte. Dieser Ablauf wurde noch nicht mit echten Apple-Zugangsdaten ausgeführt.

1. `metadata/de-DE/` enthält die deutschen Texte, `metadata/tr/` die türkischen Texte. Die TXT-Dateien sind Klartext zum Kopieren. `metadata-validation.json` enthält die geprüften Textlängen. Keywords werden vorsichtshalber sowohl auf Zeichen als auch auf UTF-8-Bytes begrenzt.
2. `screenshots/de-DE/` und `screenshots/tr/` enthalten jeweils sieben Bilder in der vorgeschlagenen Reihenfolge. Die ersten Bilder zeigen Start, Quran und Gebetsanleitung; ein weiteres Bild zeigt den dunklen Modus. Alle Bilder sind PNGs mit 1206 × 2622 Pixeln und ohne Alphakanal. Beim Export wird ausschließlich der vollständig deckende Alphakanal entfernt; die RGB-Pixel werden danach exakt verglichen.
3. `review-notes.txt` enthält englische Erläuterungen für App Review. Kein Testkonto ist erforderlich. Die persönlichen Kontaktdaten für App Review müssen separat ergänzt werden.
4. `device-test-checklist.md` auf einem echten iPhone mit der signierten TestFlight-Version abarbeiten. Die aufgeführten Fälle sind noch nicht als bestanden bestätigt.
5. `owner-details.template.json` enthält die bereits bestätigten Eigentümerangaben. Die übrigen Kontodaten und Entscheidungen lokal ergänzen. Private Telefonnummern, Adressen, Schlüssel oder Zertifikate gehören nicht in das öffentliche Repository.
6. `provider-privacy-request.txt` ist ein noch nicht versendeter Anfrageentwurf. `provider-evidence.md` trennt die gefundenen Quellen von den weiterhin offenen Fragen.
7. `SUPPORT.md` und `PRIVACY.md` enthalten die aktuellen öffentlichen Kontakt- und Datenschutzhinweise. Die freigegebene E-Mail-Adresse ist in beiden Dokumenten eingetragen.

## Herkunft der Bilder

Die Aufnahmen stammen aus UI-Lauf **1048**, erzeugt für PR #66, und wurden visuell geprüft. Der geprüfte App-Quellbaum ist identisch mit dem App-Quellstand auf `main` bei `2d00fa9`. Die Dateinamen des ursprünglichen CI-Artefakts enthalten noch `B78`, weil sie bestehende Vergleichsdateien bezeichnen; die tatsächlich kompilierte App ist Build 79. `provenance.json` hält Herkunft, Originaldateinamen und Prüfsummen fest.

Es sind reale Ansichten eines Debug-Simulators mit vorbereiteten Beispieldaten. Sie belegen das Aussehen dieser Ansichten, keine Interaktionstests und keine Messungen an einem echten Gerät. Die Qibla-Ansicht mit sichtbarem QA-Ortsnamen wird nicht als Store-Material übernommen. Die Originalbilder werden nicht beschnitten, skaliert, retuschiert oder inhaltlich ergänzt.

Apple führt 1206 × 2622 als akzeptierte Größe für iPhones mit Dynamic Island und mittlerem Display. Die aktuelle Spezifikation benennt dieses Display als erforderlich; dieselbe Seite enthält zusätzliche Regeln für große Displays. Deshalb muss die tatsächliche Medienauswahl im App-Store-Connect-Konto vor dem Einreichen geprüft werden. Falls sie weitere Größen verlangt, sind dafür native Aufnahmen zu erstellen.

## Noch vor dem Upload zu erledigen

- Die noch ausstehende Apple-Developer-Anmeldung abschließen; danach aktive Mitgliedschaft, Team, App-ID und App-Store-Connect-Eintrag bestätigen und prüfen, ob Build 79 noch unbenutzt ist.
- Die Datenverarbeitung des Quran-Anbieters für die tatsächlich verwendeten API-/CDN-Endpunkte klären. Erst dann die finalen Privacy-Antworten festlegen.
- Altersfreigabe, Länder, Preis, EU-Händlerstatus und Review-Kontakt anhand der tatsächlichen Situation im Konto ausfüllen. Es werden keine Werte geraten.
- Signierten Export ausführen, Apples Validierung und Verarbeitung prüfen und die Gerätetests dokumentieren.

Die Store-Texte enthalten keine Aussage über eine bestandene rechtliche oder religiöse Zertifizierung. Für Accessibility-Angaben ist die tatsächliche Unterstützung auf dem Gerät zu prüfen; es werden keine ungeprüften Labels zugesagt.

## Paket erneut erstellen

Python 3 und Pillow werden benötigt. Das offizielle Artefakt von UI-Lauf 1048 entpacken und aus dem Repository ausführen:

```bash
python3 scripts/prepare_store_materials.py --screenshots /pfad/zum/ui-artefakt --output build/store-materials-b79
```

Das Ziel darf noch nicht existieren. Der Export prüft den unveränderten App-Quellstand, die Original-Prüfsummen, Bildgrößen, Alphakanäle, Pixelgleichheit und Textlängen. Daneben entsteht eine ZIP-Datei. Für eine spätere App-Version müssen neue Bilder aufgenommen und die Herkunftsdaten nach Prüfung aktualisiert werden.

## Quellen, geprüft am 7. Oktober 2026

- Screenshot-Vorgaben: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
- Textfelder: https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information
- App-Name und Untertitel: https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/
- Produktseite: https://developer.apple.com/app-store/product-page/
- UI-Lauf: https://github.com/Achmed06/SalahPath-iOS/actions/runs/37601611815
- Main-Build: https://github.com/Achmed06/SalahPath-iOS/actions/runs/37604351348

Kann Richtigkeit nicht garantieren – bitte verifizieren.
