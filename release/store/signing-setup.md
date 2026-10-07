# Signierter Build über GitHub

Stand: 7. Oktober 2026. Vorbereitet, aber ohne aktive Apple-Mitgliedschaft und Signiermaterial noch nicht mit dem echten Konto ausgeführt. Der unsigned-IPA-Workflow prüft zusätzlich Signierregeln mit synthetischen Daten und die benötigten Upload-Optionen im installierten Apple-Werkzeug.

## Einmalige Einrichtung nach Apple-Freischaltung

Die explizite App-ID `com.achmed06.salahpath` mit **Time Sensitive Notifications** bereitstellen. Benötigt werden ein gültiges **Apple Distribution**-Zertifikat einschließlich privatem Schlüssel als passwortgeschützte `.p12` und ein dazu passendes **App Store Connect**-Provisioning-Profil für iOS. Das Profil muss Zertifikat und Berechtigung enthalten.

Die Beschaffung dieses Materials ist noch ein Einrichtungsschritt. Falls kein Zertifikat mit privatem Schlüssel existiert, muss dieser zunächst erzeugt und das Zertifikat über Apple ausgestellt werden. Eine heruntergeladene `.cer` ersetzt keine `.p12` mit privatem Schlüssel. Für den späteren Build übernimmt GitHub Mac und Xcode.

Beim Repository unter **Settings → Secrets and variables → Actions** eintragen:

| Typ | Exakter Name | Inhalt |
| --- | --- | --- |
| Variable | `SALAH_DEVELOPMENT_TEAM` | Apple Team-ID |
| Secret | `SALAH_CERTIFICATE_BASE64` | Base64 der Distribution-P12 |
| Secret | `SALAH_CERTIFICATE_PASSWORD` | Passwort der P12 |
| Secret | `SALAH_PROFILE_BASE64` | Base64 der passenden `.mobileprovision` |
| Secret, nur Upload | `SALAH_ASC_KEY_BASE64` | Base64 des App-Store-Connect-Team-API-Schlüssels `.p8` |
| Secret, nur Upload | `SALAH_ASC_KEY_ID` | Key ID |
| Secret, nur Upload | `SALAH_ASC_ISSUER_ID` | Issuer ID desselben Teams |

Der optionale Upload verwendet einen **Team-API-Schlüssel** mit ausreichender Build-Upload-Berechtigung. Persönliche API-Schlüssel ohne Issuer-ID sind hier nicht vorgesehen. Apple-Passwort und Zwei-Faktor-Codes nicht in Workflow-Parameter eintragen.

Unter Windows kann PowerShell eine vorhandene Datei als Base64 in die Zwischenablage kopieren. Beispielpfad ersetzen und den Inhalt direkt als passendes Secret speichern:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes('C:\Privat\Distribution.p12')) | Set-Clipboard
```

Für Profil und P8 deren Datei verwenden. Base64 ist nur Kodierung; den Inhalt wie die Schlüsseldatei behandeln. Der Ablauf nutzt einen temporären Schlüsselbund auf dem GitHub-Mac und entfernt seine temporären Dateien nach dem Lauf. Private Schlüssel werden nicht als Artefakte hochgeladen.

## Erster Lauf: nur signieren und prüfen

1. Vollständigen aktuellen Commit von `main` kopieren.
2. **Actions → App Store signed export → Run workflow** öffnen.
3. Branch **main** wählen; vollständigen Commit bei `expected_commit` einfügen.
4. `upload_to_testflight` ausgeschaltet lassen und starten.
5. Bei grünem Ergebnis Artefakt `SalahPath-AppStore-<Commit>` sichern: signierte IPA, Prüfberichte und Prüfsumme. Aufbewahrung im Workflow: sieben Tage.

Der Ablauf stoppt bei abweichendem Commit, falschem Team, abgelaufenem bzw. unpassendem Profil oder fehlenden Berechtigungen. Archiv und Export müssen zur Projektversion passen. Buildnummern werden nicht automatisch geändert.

## Zweiter Lauf: optional zu TestFlight

App-Eintrag in App Store Connect bestätigen und freien Build 79 prüfen. Upload-Secrets ergänzen. Denselben geprüften Quellstand mit aktivem `upload_to_testflight` starten.

Der Ablauf erstellt und prüft einen neuen signierten Export, validiert ihn mit `altool` und überträgt ihn. Bei einer Unterbrechung zuerst prüfen, ob Apple den Build bereits erhalten hat; nicht blind dieselbe Buildnummer erneut übertragen.

Danach Apples Verarbeitung im Konto prüfen, Build für den vorgesehenen Test freigeben und `device-test-checklist.md` ausfüllen. Eine erfolgreiche Übertragung ist noch kein bestandener Gerätetest. App Review und öffentliche Veröffentlichung löst dieser Workflow nicht aus.

## Geprüfte Quellen

- GitHub, Zertifikate auf macOS-Runnern: https://docs.github.com/en/actions/how-tos/deploy/deploy-to-third-party-platforms/sign-xcode-applications
- Apple, Upload: https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/
- Apple, Profilverzeichnis: https://developer.apple.com/documentation/xcode-release-notes/xcode-16-release-notes

Kann Richtigkeit nicht garantieren – bitte verifizieren.
