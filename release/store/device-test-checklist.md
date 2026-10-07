# SalahPath: Testprotokoll auf einem echten iPhone

**Status: noch nicht ausgeführt.** Simulatorbilder und der erfolgreiche Archiv-Build ersetzen diese Tests nicht.

Gerät: __________  iOS: __________  TestFlight-Version / Build: __________  Datum: __________

Eine signierte TestFlight-Installation verwenden. Für einen Test mit leerem Datenbestand ein Testgerät oder entbehrliche Testdaten nutzen; bestehende persönliche Aufzeichnungen nicht für den Test löschen. Jede Zeile mit Ergebnis, kurzer Beobachtung und bei Fehlern Reproduktionsschritten ergänzen.

| Fall | Ablauf | Erwartetes Verhalten | Ergebnis / Beleg |
| --- | --- | --- | --- |
| Frische Einrichtung | Installation ohne vorhandene Einstellungen öffnen, Einrichtung mit abgelehntem Standort abschließen. | Kein erzwungenes Konto, kein Absturz; Lesen und Lernen sind erreichbar. | Offen |
| System- und App-Sprache | Erststart mit deutscher und türkischer Gerätesprache prüfen; danach Sprache im Profil wechseln. | Passende Standardsprache; sichtbare Texte und Systemsteuerelemente wechseln konsistent. Berechtigungstext passt zur iOS-App-Sprache. | Offen |
| Standort zulassen | Standort während der Nutzung erlauben, Gebetszeiten und Qibla öffnen. | Standortstatus aktualisiert sich; keine endlose Ladeanzeige. | Offen |
| Standort ablehnen / wieder erlauben | Zugriff in iOS-Einstellungen entziehen, App öffnen, später wieder erlauben. | Verständlicher Status; Wiederherstellung ohne Neuinstallation. | Offen |
| Manueller Ort | Stadt wählen, App beenden und erneut öffnen; manuellen Ort anschließend löschen. | Ort und Zeitzone bleiben bis zum Löschen erhalten; keine Vermischung mit dem Standort des Kompasses. | Offen |
| Qibla | Mit Standortzugriff das Gerät drehen; grobe Richtung unabhängig prüfen. | Richtungsanzeige reagiert; fehlender oder ungenauer Kompass wird nicht als sichere Messung dargestellt. | Offen |
| Moscheensuche | Mit aktuellem Standort suchen; danach bei entzogenem Zugriff wiederholen. | Ergebnisse oder klarer Leer-/Fehlerzustand; keine stillschweigende Suche um eine falsche Stadt. | Offen |
| Benachrichtigungen | Zugriff zunächst ablehnen, später in iOS erlauben und in der App aktivieren. | Status und Planung erholen sich; keine doppelt geplanten Erinnerungen. | Offen |
| Echte Gebetserinnerung | Eine bevorstehende Gebetszeit mit passenden Einstellungen abwarten; App in den Hintergrund legen. | Richtige Zeit und Sprache; vereinbarter Klang im Rahmen der iOS-Einstellungen. Zeitpunkt und Beobachtung notieren. | Offen |
| Lautlos / Fokus | Erinnerung bei aktivem Lautlosmodus und separat mit Fokus testen. | Kein Versprechen einer Umgehung; Time Sensitive hängt von den tatsächlichen iOS-Einstellungen ab. | Offen |
| Erinnerung deaktivieren | Erinnerungen in der App ausschalten; Diagnose und späteren Termin prüfen. | Geplante Gebetserinnerungen werden entfernt. | Offen |
| Hintergrund-Audio | Quran-Audio starten, Bildschirm sperren; Pause/Fortsetzen und Kopfhörertrennung prüfen. | Wiedergabe und Bedienelemente reagieren korrekt; keine unerwartete parallele Wiedergabe. | Offen |
| Netzverlust | Während Laden und Audio das Netz trennen, anschließend wieder verbinden. | Kein Absturz oder endlos blockierter Bildschirm; erneuter Versuch funktioniert. | Offen |
| Quran offline | Download-Caches löschen; im Flugmodus erste, mittlere und letzte Quran-Seite öffnen. | Arabischer Text bleibt vorhanden; fehlende Zusatzdaten werden verständlich behandelt. | Offen |
| Gespeicherte Zusatzdaten | Übersetzung und Audio online öffnen, dann offline wieder öffnen; Cache löschen und erneut prüfen. | Vorhandener Cache wird genutzt; gelöschte Zusatzdaten werden nicht fälschlich als verfügbar angezeigt. | Offen |
| Gebetsanleitung | Für Mann und Frau alle Schritte vor/zurück durchgehen, dabei mehrfach zügig wechseln und scrollen. | Richtiger Schritt, Bild und Text; keine leere Ansicht nach Navigation. Salām rechts und links bleiben getrennt. | Offen |
| Wudu | Alle Schritte vor/zurück durchgehen; mehrfach zwischen Anleitungen wechseln. | Keine verschwundenen Inhalte, falsche Reihenfolge oder blockierte Navigation. | Offen |
| Hell / Dunkel / große Schrift | Systemmodus wechseln; größere Schrift und VoiceOver an ausgewählten Kernansichten prüfen. | Lesbare Beschriftungen und bedienbare Steuerelemente. Beobachtete Einschränkungen dokumentieren, keine Accessibility-Angaben raten. | Offen |
| Kalender | Datum hinzufügen; einmal abbrechen, einmal speichern. | Abbruch erzeugt keinen Eintrag; Speichern folgt der Auswahl im Apple-Editor. | Offen |
| Lokale Daten | Tracker, Lesezeichen und letzten Lesestand ändern; App neu starten und Sprache wechseln. | Aufzeichnungen bleiben erhalten und werden konsistent angezeigt. | Offen |
| Upgrade | Vorhandene signierte Vorgängerversion mit Testdaten auf den Kandidaten aktualisieren. | Einstellungen und lokale Aufzeichnungen bleiben erhalten. Falls keine Vorgängerversion existiert: nachvollziehbar als nicht anwendbar markieren. | Offen |
| Support / Lizenzen | Links im Profil öffnen und Lizenzen offline anzeigen. | URLs erreichbar, freigegebene Kontaktadresse vorhanden, Lizenztext lesbar. | Offen |

Freigabe erst nach dokumentierten Ergebnissen. Fehler zuerst beheben und nur betroffene Fälle erneut prüfen. Die Kopfzeile muss den tatsächlich getesteten Build nennen.
