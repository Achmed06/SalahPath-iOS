# App Store Connect: Felder zum Übertragen

Stand 7. Oktober 2026. Angaben aus dem geprüften Quellstand sind als bestätigt bezeichnet; Vorschläge werden erst durch Auswahl im Konto verbindlich. Keine Angaben wurden in App Store Connect eingetragen.

## App-Eintrag und Version

| Feld | Vorbereiteter Wert | Status |
| --- | --- | --- |
| Plattform | iOS | Bestätigt |
| App-Name | SalahPath | Aus der App; Store-Verfügbarkeit im Konto prüfen |
| Primärsprache | Deutsch (Deutschland) | Vorschlag |
| Weitere Lokalisierung | Türkisch | Vorbereitet |
| Bundle-ID | `com.achmed06.salahpath` | Bestätigt; dieselbe explizite App-ID für Profil und Store |
| SKU bei neuem Eintrag | `salahpath-ios` | Vorschlag; im Konto auf Eindeutigkeit prüfen |
| Version | `3.62` | Bestätigt |
| Build | `79` | Im Projekt bestätigt; Verwendung im Konto noch prüfen |
| Geräte | iPhone; iOS 17 oder neuer | Bestätigt |
| Primäre Kategorie | Lifestyle | Vorschlag |
| Sekundäre Kategorie | Education | Optionaler Vorschlag |
| Copyright | Jahr und tatsächlicher Rechteinhaber | Eigentümer muss ergänzen |
| Veröffentlichung | Manuell nach Freigabe | Vorschlag |
| Preis und Länder | Noch festzulegen | Keine Preisentscheidung aus fehlenden In-App-Käufen ableiten |
| Mac mit Apple Silicon / Apple Vision Pro | Verfügbarkeit bewusst prüfen | Keine ungeprüfte Gerätefreigabe behaupten |

Bei einem bestehenden App-Eintrag dessen SKU und Identität weiterverwenden. Falls Build 79 schon hochgeladen wurde, die Buildnummer im Projekt und die zugehörigen Release-Prüfungen gemeinsam aktualisieren; keine nachträgliche Änderung an einer signierten IPA.

## Texte und Medien

| Store-Feld | Datei oder Wert |
| --- | --- |
| Name, Untertitel, Werbetext, Keywords, Beschreibung | Einzelne TXT-Dateien unter `metadata/de-DE/` und `metadata/tr/` |
| Screenshots | `screenshots/de-DE/` bzw. `screenshots/tr/`, nummerierte Reihenfolge |
| Support-URL | https://github.com/Achmed06/SalahPath-iOS/blob/main/SUPPORT.md |
| Datenschutz-URL | https://github.com/Achmed06/SalahPath-iOS/blob/main/PRIVACY.md |
| Öffentlicher Kontakt | Muhammed_Y@outlook.de |
| Marketing-URL | Optional; leer lassen, solange keine passende Seite festgelegt ist |
| App-Icon | Kommt aus dem Build; Marketing-Icon ist im Asset-Katalog vorhanden |
| Review Notes | `review-notes.txt` |
| Anmeldung für App Review | Keine Anmeldung erforderlich; kein erfundenes Testkonto |
| Review-Kontakt | Reale Kontaktperson mit erreichbarer E-Mail und Telefonnummer separat eintragen |
| TestFlight-Beschreibung / Was soll getestet werden? | `testflight-de.txt` und `testflight-tr.txt` |

Vorhandene PNGs: 1206 × 2622 Pixel. Pflichtfelder für Geräte und Displaygrößen im Konto prüfen. Weitere verlangte Größen aus einem passenden Simulatorlauf erstellen; vorhandene Bilder nicht als Aufnahmen anderer Geräte ausgeben.

## Fragebögen

**App Privacy:** Der geprüfte Code verwendet keine Werbung, kein Tracking-SDK und kein Benutzerkonto. Persönliche Gebetsaufzeichnungen bleiben lokal. Quran-API und Audio-CDN erhalten normale Anfragedaten einschließlich der IP-Adresse. Deren Speicherung und Nutzung sind noch ungeklärt. Daher ist noch keine finale Antwort „Keine Daten erfasst“ freigegeben. Siehe `provider-evidence.md` und den Anfrageentwurf.

**Altersfreigabe:** Die App enthält keine eigenen Chats, Benutzerbeiträge, Werbeplätze, Glücksspiele, Lootboxen oder In-App-Käufe. Sie enthält religiöse Texte, vollständigen Quran und Erläuterungen unter anderem zu Ghusl und Janazah. Inhaltliche Fragen anhand aller zugänglichen Texte und Übersetzungen bewerten; nicht pauschal überall „Nein“ wählen oder eine Alterszahl vorab zusagen. Externe Links bei Fragen zu Webzugriff berücksichtigen. Die endgültige Einstufung entsteht durch Apples aktuellen Fragebogen. „Made for Kids“ ist nicht vorbereitet.

**Verschlüsselung:** Das Projekt setzt `ITSAppUsesNonExemptEncryption` auf `NO` und verwendet System-HTTPS. Den Export-Fragebogen für diesen Build beantworten; keine selbst entwickelte Verschlüsselung behaupten.

**Inhaltsrechte:** Die Prüfung steht in `CONTENT_RIGHTS_AUDIT.md`, `AUDIO_LICENSES.md` und den Provider-Unterlagen im Repository. Tatsächliche Berechtigung bestätigen; öffentliche Erreichbarkeit allein ist keine Rechtefreigabe.

**EU-Händlerstatus:** Nach der tatsächlichen Veröffentlichungssituation beantworten. Kostenloser Preis oder frühere Gewerbeangaben ersetzen diese Bewertung nicht. Erforderliche öffentliche Kontaktdaten in den vorgesehenen Kontobereich eintragen.

**Accessibility:** Nur tatsächlich auf dem Gerät geprüfte Merkmale auswählen. Dunkler Modus oder Schriftgrößenoption allein belegen keine vollständige Unterstützung aller Kriterien.

## Nach dem Upload

Die Erfolgsmeldung des Upload-Befehls bestätigt die Übertragung. Nach Apples Verarbeitung den Build auswählen, TestFlight prüfen und später mit finalen Store-Angaben einreichen. Den Gerätetestbericht auf die tatsächlich verwendete Version, Buildnummer und IPA-Prüfsumme beziehen.

## Geprüfte Quellen

- Apple, App-Eintrag: https://developer.apple.com/help/app-store-connect/create-an-app-record/add-a-new-app/
- Apple, Upload: https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/
- Apple, Altersfragebogen: https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/
- Apple, Testinformationen: https://developer.apple.com/help/app-store-connect/test-a-beta-version/provide-test-information

Kann Richtigkeit nicht garantieren – bitte verifizieren.
