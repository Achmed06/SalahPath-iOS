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

Location permission is used while the app is in use to calculate prayer times, determine Qibla direction, and resolve a nearby locality label. The app does not intentionally retain a location history or send GPS coordinates to a SalahPath-operated server.

Prayer reminders are local notifications. The Islamic calendar export opens Apple's native event editor and does not read the user's calendar.

Quran text, translations, and recitation audio are loaded from AlQuran.cloud / Islamic Network. The app attributes the Quran sources in the reader.

There are no ads, advertising SDKs, analytics SDKs, or cross-app tracking features in the current build.

## App Privacy / privacy manifest

The binary includes `PrivacyInfo.xcprivacy` and declares:

- Tracking: No
- App-declared collected data types: none
- Required Reason API: UserDefaults — `CA92.1`
- Required Reason API: File timestamps inside the app container — `C617.1`

Before publishing the App Store privacy answers, re-check whether the external Quran API/CDN retains request metadata such as IP addresses beyond the time needed to serve and rate-limit requests. Apple's definition treats retained third-party data as collected; real-time request handling that is not retained is treated differently.

## Export compliance

The project declares `ITSAppUsesNonExemptEncryption = NO`. Current network encryption is provided through Apple's HTTPS networing stack; there is no proprietary cryptography in SalahPath's own source.

## Content rights and attribution

The Quran reader identifies AlQuran.cloud / Islamic Network as the source, Diyanet for Turkish translation, and Bubenheim & Elyas for German translation. AlQuran.cloud's current terms should be re-checked before each major commercial-distribution change, especially if monetisation is introduced.

## Manual items that require the Apple Developer / App Store Connect account

- Create the App ID for `com.achmed06.salahpath`.
- Create the App Store Connect app record.
- Complete the age-rating questionnaire.
- Enter App Privacy answers and the Privacy Policy URL.
- Upload screenshots for the required iPhone display sizes.
- Provide the Support URL.
- Sign/archive with the paid Apple Developer team and upload the signed build.
- Run TestFlight device testing for location, Qibla heading, notifications, calendar export, Quran streaming/cache, and both German/Turkish UI before review submission.
