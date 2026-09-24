# SalahPath App Store submission checklist

Prepared for SalahPath v3.62 / build 78 / bundle identifier `com.achmed06.salahpath`.

## Store identity

- App name: `SalahPath`
- Suggested German subtitle: `Gebet, Quran & Qibla`
- Suggested Turkish subtitle: `Namaz, Kur'an ve Kıble`
- Primary category: `Lifestyle`
- Bundle identifier: `com.achmed06.salahpath`
- Version: `3.62`
- Build: `78`
- Minimum iOS version: `17.0`

## Required URLs

- Privacy Policy URL: `https://github.com/Achmed06/SalahPath-iOS/blob/main/PRIVACY.md`
- Support URL: `https://github.com/Achmed06/SalahPath-iOS/issues`

The Privacy Policy link is also exposed inside the app under Profile > Rechtliches & Hilfe / Yasal bilgiler & yardım.

## App Review notes

SalahPath does not require an account or login.

Location permission is used while the app is in use to calculate prayer times, determine Qibla direction, resolve a nearby locality label, and search for nearby mosques through Apple MapKit. Device-location updates are not intentionally retained as a location history or sent to a SalahPath-operated server. If the user chooses a city or postal code manually, the resolved latitude, longitude, and locality are stored locally so that manual selection persists until the user clears it.

Prayer reminders are local notifications. Build 78 adds optional 28-second custom Adhan sounds exactly at prayer time: a dedicated Fajr recording and a standard Doha recording for Dhuhr, Asr, Maghrib and Isha. Advance reminders keep the normal iOS notification sound. Both are derivatives of the Internet Archive item “Adhan Recordings from Doha, Qatar”, whose source page marks the recordings with Public Domain Mark 1.0; provenance and hashes are recorded in `AUDIO_LICENSES.md`. The Islamic calendar export opens Apple's native event editor and does not read the user's calendar.

The validated Arabic Uthmani Quran corpus is bundled locally from AlQuran.cloud / Islamic Network for offline reading. Translations and recitation audio are requested from the same service and cached where supported. The app attributes the Quran sources in the reader. A dated rights audit is stored in `CONTENT_RIGHTS_AUDIT.md`.

There are no ads, advertising SDKs, analytics SDKs, StoreKit purchases, subscriptions, or cross-app tracking features in the audited build.

## App Privacy / privacy manifest

The binary includes `PrivacyInfo.xcprivacy` and declares:

- Tracking: No
- Collected data type: Device ID — used only for App Functionality; not linked to the user; not used for tracking. This is a conservative disclosure for the source IP necessarily visible to AlQuran.cloud / Islamic Network while serving Quran API/CDN requests.
- Required Reason API: UserDefaults — `CA92.1`
- Required Reason API: File timestamps inside the app container — `C617.1`

### Final App Store Connect privacy answer for the Quran service

Apple defines data as “collected” when it is transmitted off device and retained by the developer or a third party longer than needed to service the request in real time. Apple also instructs developers who collect and store IP addresses to disclose the data category according to how the IP address is used.

AlQuran.cloud's current terms state that the API applies a per-IP rate limit. As of 23 September 2026, the public AlQuran.cloud / Islamic Network material reviewed for release still does not provide a request-log retention period. Because retention cannot be confirmed, SalahPath will not rely on the “real-time only” exception.

For App Store Connect, answer **Yes, data is collected** and disclose:

- Category: **Identifiers → Device ID**
- Purpose: **App Functionality**
- Linked to the user: **No**
- Used for tracking: **No**

This is intentionally conservative: the provider receives the source IP as normal connection metadata and uses it for API rate limiting / service protection. SalahPath does not create an account identifier and does not use the IP for advertising, analytics, profiling, or cross-app tracking.

Do **not** declare Precise Location or Coarse Location for the Quran service. SalahPath does not send GPS coordinates, manually selected latitude/longitude, prayer history, fasting state, Quran bookmarks, or other local worship data to AlQuran.cloud / Islamic Network.

If Islamic Network later publishes a verifiable statement that API/CDN source IPs and request metadata are discarded immediately after servicing the request, the App Store Connect disclosure can be revisited.

## Export compliance

The project declares `ITSAppUsesNonExemptEncryption = NO`. Current network encryption is provided through Apple's HTTPS networking stack; there is no proprietary cryptography in SalahPath's own source.

## Content rights and attribution

The dated content-rights review is in `CONTENT_RIGHTS_AUDIT.md`. The Arabic Uthmani Quran corpus is also bundled locally for offline page reading; its exact validated source hash is recorded in `qa/quran-text-hash.txt` and the app keeps visible AlQuran.cloud / Islamic Network attribution. Bundled audio provenance is recorded in `AUDIO_LICENSES.md`.

The current build ships the validated AlQuran.cloud / Islamic Network Uthmani corpus locally and uses the service for translations/recitations; it visibly attributes the service, Diyanet, Bubenheim & Elyas, and the selected reciter. AlQuran.cloud's terms reviewed on 21 September 2026 support the current free/non-paywalled use while retaining the underlying rights with translators and reciters/rightsholders. If monetisation or a paywall is introduced, repeat the rights review before release.

## Religious-content review

The dated religious-content audit is in `RELIGIOUS_CONTENT_AUDIT.md`. The current native source corrects or clarifies Quran excerpts, a previously incomplete Quran 3:8 display, morning/evening adhkar wording, the unsupported fixed Istighfar counter, and the Hanafi congregational Fatiha distinction.

## Manual items that require the Apple Developer / App Store Connect account

- Create the App ID for `com.achmed06.salahpath`.
- Create the App Store Connect app record.
- Complete the age-rating questionnaire.
- Enter App Privacy answers and the Privacy Policy URL using the final privacy decision above.
- Upload screenshots for the required iPhone display sizes.
- Provide the Support URL.
- Sign/archive with the paid Apple Developer team and upload the signed build.
- Run TestFlight device testing for location, Qibla heading, notifications, calendar export, Quran streaming/cache, and both German/Turkish UI before review submission.
