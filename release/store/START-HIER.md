# SalahPath: Start zur Veröffentlichung

Vorbereitet am 7. Oktober 2026 für **3.62 / Build 79**. Die Apple-Anmeldung steht nach deiner Angabe auf **pending**. Ein signierter Build oder Apple-Upload wurde noch nicht ausgeführt.

## Fertig vorbereitet

- Store-Texte auf Deutsch und Türkisch, jeweils sieben geprüfte Screenshots und englische Review-Hinweise.
- Öffentlicher Support und Datenschutzkontakt: **Muhammed_Y@outlook.de**.
- Manueller GitHub-Ablauf für Signierung, Prüfung und optionalen Upload. Der Build läuft auf einem GitHub-Mac; lokal ist dafür kein Xcode nötig. Die Apple-Zugangsdaten müssen nach Freischaltung einmal eingerichtet werden.
- TestFlight-Texte und ein Protokoll für echte iPhone-Tests.
- Unversendete Anfrage zu den offenen Datenschutzfragen des Quran-Anbieters.

## Reihenfolge nach der Freischaltung

1. **Konto und App einrichten.** Mit `app-store-connect-fields.md` die Kontofelder ausfüllen. Bestehenden App-Eintrag weiterverwenden. App-ID `com.achmed06.salahpath`, Team und freien Build 79 prüfen; erforderliche Apple-Vereinbarungen im Konto lesen und selbst bestätigen.
2. **Signierung einrichten.** `signing-setup.md` beschreibt die Secrets und den Start über GitHub Actions. Zuerst nur den signierten Export starten. Er muss einschließlich Zertifikat-, Profil- und Bundle-Prüfung erfolgreich sein.
3. **Zu TestFlight hochladen.** Bei erneutem manuellem Start den Upload aktivieren. Nach erfolgreicher Übertragung zusätzlich Apples Verarbeitung im Konto prüfen. Der Ablauf wählt keinen Tester aus und reicht die App nicht zur öffentlichen Prüfung ein.
4. **Auf dem iPhone testen.** Den verarbeiteten Build in TestFlight installieren und `device-test-checklist.md` ausfüllen. Testinformationen stehen in `testflight-de.txt` und `testflight-tr.txt`.
5. **Datenschutz und Store-Angaben abschließen.** Antwort des Quran-Anbieters auswerten; App Privacy, Datenschutzhinweise und gegebenenfalls Manifest gemeinsam abgleichen. Altersfragebogen, EU-Status, Preis/Länder, Rechteangaben und privaten Review-Kontakt bestätigen.
6. **Einreichen.** Tatsächlich geprüften Build auswählen, Store-Vorschau kontrollieren und zur Prüfung einreichen. Freigabeoption bewusst auswählen; als Vorschlag ist eine manuelle Veröffentlichung vorgesehen.

## Noch benötigte Angaben und Nachweise

| Angabe | Stand |
| --- | --- |
| Aktive Apple-Mitgliedschaft und Team-ID | Pending laut Eigentümer; im Konto noch nicht geprüft |
| Distribution-Zertifikat mit privatem Schlüssel und App-Store-Profil | Noch nicht eingerichtet |
| App-Eintrag und unbenutzte Buildnummer | Im Konto prüfen |
| Name, E-Mail und Telefonnummer für App Review | Separat ergänzen; öffentlicher Supportkontakt bestätigt |
| Copyright-Inhaber, Preis, Länder und EU-Händlerstatus | Eigentümerentscheidung offen |
| Quran-Provider-Datenschutz und vollständiger Altersfragebogen | Offen |
| Signierter Export, Apple-Verarbeitung und iPhone-Tests | Noch nicht ausgeführt |

Private Angaben ausschließlich in die vorgesehenen Kontofelder bzw. GitHub Secrets eintragen. Das öffentliche Repository enthält nur Vorlagen. Eine ausgefüllte Kopie von `owner-details.template.json` kann lokal unter `build/private/owner-details.local.json` liegen; der bestehende Ordner `build/` ist vom Git-Tracking ausgeschlossen. Schlüsseldateien außerhalb des Repositorys aufbewahren.

Technisch vorbereitet bedeutet: Dateien und Abläufe sind vorhanden und die verfügbaren Prüfungen werden ausgeführt. Erfolgreiche Signierung mit deinem Apple-Konto und Store-Zulassung lassen sich erst nach den offenen Schritten bestätigen.
