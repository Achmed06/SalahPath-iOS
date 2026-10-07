# SalahPath App Store submission

Reviewed: 7 October 2026. Candidate: **3.62 (79)**, `com.achmed06.salahpath`, iPhone, iOS 17 or later.

**Status: technical release preparation; submission is not yet verified.** A successful unsigned archive is not a signed App Store export, a TestFlight device test, or an Apple approval. See `qa/APP_STORE_READINESS_2026-10-07.md` for evidence and unresolved items.

Prepared Store material is in `release/store/`: localized metadata, review notes, a real-device test record, an owner-details template and an unsent provider-privacy inquiry. `scripts/prepare_store_materials.py` exports the reviewed CI screenshots as opaque RGB PNGs with unchanged visible pixels, validates metadata limits and packages the material with provenance. The current screenshot set covers 1206 × 2622; check the actual media slots in App Store Connect for any additional required sizes. None of this performs an upload.

## Identity and build

The Xcode project is the source of truth for version/build; packaging no longer overrides these values. Before uploading, compare build 79 with the actual App Store Connect record and choose a new build number if 79 is already used.

- App name: SalahPath
- German subtitle: Gebet, Quran & Qibla
- Turkish subtitle: Namaz, Kur'an ve Kıble
- Suggested primary category: Lifestyle
- Supported app languages: German and Turkish
- Privacy URL: https://github.com/Achmed06/SalahPath-iOS/blob/main/PRIVACY.md
- Support URL: https://github.com/Achmed06/SalahPath-iOS/blob/main/SUPPORT.md
- Owner-approved public support and privacy email: Muhammed_Y@outlook.de

The app links to the privacy policy and public issue tracker under Profile > Rechtliches & Hilfe / Yasal bilgiler & yardım. The linked privacy policy and the Support URL above provide the approved email contact. Email does not require a GitHub account; public issue posting does. The owner approved publication of this address on 7 October 2026. App Review's separate contact fields remain to be completed.

## Build and signing

Owner-reported status on 7 October 2026: Apple Developer enrollment is **pending**. Account approval, team access and signed distribution have not been independently verified. Do not mark enrollment or signing as complete based on the unsigned builds.

Apple's requirements checked on 7 October 2026 require Xcode 26 or later and the iOS 26 SDK or later. Both the local preflight and the built-bundle check enforce the relevant minimums.

- `scripts/build_unsigned_ipa.sh` runs a Release **archive** and verifies the unmodified `.app` before producing `SalahPath-unsigned.ipa` for testing.
- `scripts/archive_app_store.sh` runs the signed archive/export path on a Mac with the enrolled team and signing keychain configured. Set `SALAH_DEVELOPMENT_TEAM` to that team's identifier. This script exports locally and does not upload or submit anything.
- Enable Time Sensitive Notifications for the App ID; the signed export checks its entitlement.
- Signing credentials belong in the keychain/secret store, never in this repository.
- The signed path still requires a real execution with the developer account. It has not been proven merely by the unsigned CI build.

For a setup without local Xcode, `.github/workflows/app-store-release.yml` provides a manual, main-only signed export. It requires an exact source SHA and preconfigured distribution credentials; its optional Apple upload defaults to off. `scripts/ci_app_store_release.sh` installs credentials on an ephemeral GitHub-hosted Mac, validates profile/team/certificate consistency, and cleans up. The export helper supports automatic local signing and manual CI signing. The first credentialed run, Apple processing and TestFlight device tests remain unexecuted. Start with `release/store/START-HIER.md` and `release/store/signing-setup.md`.

Shared `SalahZeit/Info.plist` contains the audio background mode before signing. German/Turkish location purpose strings and the Adhan Swift MIT notice are bundled in both build paths. The verifier checks metadata, actual SDK, approved Quran/Adhan hashes, permissions, privacy reasons, localization resources, and absence of internal QA markers. It does not certify legal compliance or device behavior.

## App Review notes

SalahPath requires no account. On first launch, choose German or Turkish, a prayer-learning profile, and optionally a location. The onboarding can be completed without granting location access. A manually selected city remains available across launches. Learning, Quran Arabic reading, and local trackers remain available without location permission.

Location supports prayer-time calculation, Qibla direction, nearby place names and mosque search using Apple system services. GPS updates are not kept as a location history by SalahPath. A manually selected location is stored locally until cleared in Profile. Qibla heading requires a physical device and its current position; it is separate from a saved prayer-time city.

Prayer reminders are local notifications. Optional Adhan sounds are 28-second excerpts; they do not override the silent switch. The app refreshes a finite notification schedule when opened, so reminders are not promised indefinitely without reopening. Background audio is used only for user-started recitation/playback. Calendar export uses Apple's event editor and does not read the user's calendar.

The complete Arabic Quran is bundled for offline reading. Translations, transliteration and recitation audio use AlQuran.cloud / Islamic Network and local caches. The reader attributes the content sources. Cache clearing does not delete the bundled Arabic text. The two-rak'ah tutorial is illustrated; other prayer forms have written instructions. Do not advertise every prayer form as illustrated.

The audited source has no advertising, analytics SDK, login, subscription or in-app purchase implementation. Local worship records are not uploaded to a SalahPath backend. The selected reciter and translator attributions remain visible. Adhan notification audio provenance is documented in `AUDIO_LICENSES.md`; the Adhan Swift MIT notice is available offline under Profile > Lizenzen / Lisanslar.

## App Privacy: unresolved provider evidence

`PrivacyInfo.xcprivacy` currently declares no tracking, no collected-data entries, and required reasons `CA92.1` (UserDefaults) and `C617.1` (app-container file timestamps).

**Do not treat that manifest as proof for a final “Data Not Collected” answer.** The previous checklist incorrectly said the manifest declared Device ID and prescribed that answer solely because a server sees an IP address. That did not match the file or establish how the provider uses/retains data.

Confirmed source behavior:

- No advertising/device identifier or account identifier is generated or transmitted by SalahPath.
- Quran requests expose source IP and ordinary request metadata to the API/CDN. The provider's terms mention IP rate limiting.
- The reviewed terms do not establish server-log retention, whether requests are linked across sessions, or whether IPs are used for additional purposes.
- Additional hosting-policy and community evidence is recorded in `release/store/provider-evidence.md`. Its scope does not establish Quran API/CDN handling, so it is not treated as a final answer.
- Quran requests do not carry device coordinates, manual-location coordinates, tracker history or bookmarks.
- Apple handles geocoding/MapKit requests. Review those system-service practices separately from the Quran provider.

**Before submission:** obtain provider evidence for retention, purposes, linkage and deletion; then update the policy, privacy manifest (where applicable) and App Store Connect answers together. Apple bases disclosure on actual off-device retention/use. Neither “Device ID” nor “not linked” should be invented to fill this gap. Do not claim “Data Not Collected” while this review remains unresolved.

## Export compliance and content

The project declares `ITSAppUsesNonExemptEncryption = NO`; audited app networking uses system HTTPS and no proprietary encryption implementation. Confirm the export questionnaire for the actual release.

The provider terms were checked again on 7 October 2026; the documented text/translation/recitation permissions remain present. This is provider evidence, not a transfer of underlying copyrights or an independent clearance of every rightsholder. Preserve attribution and the unchanged Quran corpus. If monetization/provider/content changes, repeat the rights review. Religious-content audit records remain in `RELIGIOUS_CONTENT_AUDIT.md`; technical checks are not religious certification.

## Store descriptions — match implemented features

### Deutsch

SalahPath begleitet dich mit Gebetszeiten, Qibla und Anleitungen für Gebet und Gebetswaschung. Lies den vollständigen arabischen Quran offline und ergänze bei bestehender Internetverbindung Übersetzungen, Umschrift und Rezitationen.

Wähle Deutsch oder Türkisch, stelle die Gebetszeitberechnung passend zu deinem Ort ein und aktiviere auf Wunsch lokale Erinnerungen mit einem kurzen Gebetsruf. Ein Gebetstracker, Dhikr-Zähler, Duas und ein islamischer Kalender unterstützen dich im Alltag. Für nahegelegene Moscheen steht eine Kartensuche bereit.

Die bebilderte Gebetsanleitung zeigt zwei Rakʿah für Männer und Frauen; weitere Gebetsformen werden schriftlich erläutert. Die Darstellung orientiert sich überwiegend an der hanafitischen Lehrtradition. Gebetszeiten und islamische Kalenderdaten können von örtlichen Festlegungen abweichen.

Kein Konto erforderlich. Standortzugriff und Benachrichtigungen sind freiwillig. Einstellungen und persönliche Gebetsaufzeichnungen bleiben lokal auf deinem Gerät.

### Türkçe

SalahPath; namaz vakitleri, kıble yönü, namaz ve abdest anlatımlarıyla günlük ibadetlerine eşlik eder. Kur'an'ın Arapça metninin tamamını çevrimdışı okuyabilir; internet bağlantısıyla meal, Latin harfli okunuş ve tilavetlerden yararlanabilirsin.

Almanca veya Türkçe seçebilir, namaz vakti hesaplamasını bulunduğun yere göre ayarlayabilir ve kısa ezan sesiyle yerel hatırlatmalar açabilirsin. Namaz takibi, zikir sayacı, dualar ve İslami takvim de uygulamada yer alır. Yakındaki camileri haritada arayabilirsin.

Görsel namaz anlatımı erkekler ve kadınlar için iki rekâtı gösterir; diğer namaz türleri yazılı olarak açıklanır. Anlatım ağırlıklı olarak Hanefî öğretimine dayanır. Namaz vakitleri ve İslami takvim tarihleri yerel uygulamalardan farklı olabilir.

Hesap gerekmez. Konum izni ve bildirimler isteğe bağlıdır. Ayarların ve kişisel ibadet kayıtların cihazında saklanır.

## Account and device checks still required

- Confirm Apple Developer membership/team, App ID and App Store Connect app record; check that build 79 is unused.
- Complete privacy review above, age-rating questionnaire and EU trader-status declaration based on the owner's actual situation.
- Public support/privacy email is confirmed above. Complete the separate App Review contact details and verify the final public URLs in the actual account.
- Capture current, accurate App Store screenshots for the required display sizes; do not use mockups as evidence of runtime tests.
- Execute signed archive/export, validate/upload in App Store Connect, and inspect Apple's processing result.
- Test TestFlight installation and clean onboarding on a real iPhone; allow/deny/re-enable location and notifications, manual city, real compass, silent/Focus modes, lock-screen audio, calendar save/cancel, network loss, Quran caches, both languages and light/dark appearance.
- Submit for review only after these items are complete.

## Checked primary sources

- https://developer.apple.com/news/upcoming-requirements/
- https://developer.apple.com/app-store/review/guidelines/
- https://developer.apple.com/app-store/app-privacy-details/
- https://alquran.cloud/terms-and-conditions
- https://github.com/batoulapps/adhan-swift/blob/1.5.0/LICENSE

Kann Richtigkeit nicht garantieren – bitte verifizieren.
