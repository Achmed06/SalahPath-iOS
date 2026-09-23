# SalahPath App Store submission checklist

Prepared for SalahPath v3.62 / build 76 / bundle identifier `com.achmed06.salahpath`.

## Store identity

- App name: `SalahPath`
- Suggested German subtitle: `Gebet, Quran & Qibla`
- Suggested Turkish subtitle: `Namaz, Kur'an ve Kıble`
- Primary category: `Lifestyle`
- Bundle identifier: `com.achmed06.salahpath`
- Version: `3.62`
- Build: `76`
- Minimum iOS version: `17.0`

## Required URLs

- Privacy Policy URL: `https://github.com/Achmed06/SalahPath-iOS/blob/main/PRIVACY.md`
- Support URL: `https://github.com/Achmed06/SalahPath-iOS/issues`

The Privacy Policy link is also exposed inside the app under Profile > Rechtliches & Hilfe / Yasal bilgiler & yardım.

## App Review notes

SalahPath does not require an account or login.

Location permission is used while the app is in use to calculate prayer times, determine Qibla direction, resolve a nearby locality label, and search for nearby mosques through Apple MapKit. Device-location updates are not intentionally retained as a location history or sent to a SalahPath-operated server. If the user chooses a city or postal code manually, the resolved latitude, longitude, and locality are stored locally so that manual selection persists until the user clears it.

Prayer reminders are local notifications. The Islamic calendar export opens Apple's native event editor and does not read the user's calendar.

Quran text, translations, and recitation audio are loaded from AlQuran.cloud / Islamic Network. The app attributes the Quran sources in the reader. A dated rights audit is stored in `CONTENT_RIGHTS_AUDIT.md`.

There are no ads, advertising SDKs, analytics SDKs, StoreKit purchases, subscriptions, or cross-app tracking features in the audited build.

## App Privacy / privacy manifest

The binary includes `PrivacyInfo.xcprivacy` and declares:

- Tracking: No
- App-declared collected data types: none
- Required Reason API: UserDefaults — `CA92.1`
- Required Reason API: File timestamps inside the app container — `C617.1`

### App Store Connect privacy answer for the Quran service

Apple defines data as “collected” when it is transmitted off device and retained by the developer or a third party longer than needed to service the request in real time. Apple specifically says an IP address that is sent with a server request and not retained does not need to be disclosed; if it is retained, the relevant data category must be declared according to how the IP address is used.

AlQuran.cloud publicly documents per-source-IP rate limiting, so the service necessarily processes the requesting IP address. Its public AlQuran documentation reviewed on 21 September 2026 does not state whether AlQuran/API/CDN request metadata is retained beyond real-time request/rate-limit handling.

Therefore do **not** publish the App Store Connect answer “No data collected” merely by assumption. Before the final App Privacy submission, obtain a current statement from Islamic Network on AlQuran API/CDN log retention, or conservatively disclose the retained connection metadata under the Apple category that matches the provider's actual use. Do not declare GPS location for the Quran service: SalahPath does not send GPS coordinates to AlQuran.cloud / Islamic Network.

## Export compliance

The project declares `ITSAppUsesNonExemptEncryption = NO`. Current network encryption is provided through Apple's HTTPS networking stack; there is no proprietary cryptography in SalahPath's own source.

## Content rights and attribution

The dated content-rights review is in `CONTENT_RIGHTS_AUDIT.md`.

The current build uses AlQuran.cloud / Islamic Network for Quran text/translations/recitations and visibly attributes the service, Diyanet, Bubenheim & Elyas, and the selected reciter. AlQuran.cloud's terms reviewed on 21 September 2026 support the current free/non-paywalled use while retaining the underlying rights with translators and reciters/rightsholders. If monetisation or a paywall is introduced, repeat the rights review before release.

## Religious-content review

The dated religious-content audit is in `RELIGIOUS_CONTENT_AUDIT.md`. The current native source corrects or clarifies Quran excerpts, a previously incomplete Quran 3:8 display, morning/evening adhkar wording, the unsupported fixed Istighfar counter, and the Hanafi congregational Fatiha distinction.

## Manual items that require the Apple Developer / App Store Connect account

- Create the App ID for `com.achmed06.salahpath`.
- Create the App Store Connect app record.
- Complete the age-rating questionnaire.
- Enter App Privacy answers and the Privacy Policy URL using the privacy decision above.
- Upload screenshots for the required iPhone display sizes.
- Provide the Support URL.
- Sign/archive with the paid Apple Developer team and upload the signed build.
- Run TestFlight device testing for location, Qibla heading, notifications, calendar export, Quran streaming/cache, and both German/Turkish UI before review submission.
