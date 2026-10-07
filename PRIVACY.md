# SalahPath Privacy Policy

Last updated: 7 October 2026

SalahPath is designed to work without an account, advertising profile, or analytics account. The app does not contain advertising SDKs or tracking SDKs.

## Data used on the device

SalahPath stores app settings and worship-related state locally on the iPhone. This can include language and prayer-calculation preferences, prayer and fasting tracker state, Quran bookmarks and last-read position, memorisation settings, a manually selected place, and locally cached Quran text and recitation audio.

This information is used only to provide app functionality. SalahPath does not operate a developer backend that receives these local records.

## Location

With permission, SalahPath uses the device's location while the app is in use to calculate prayer times, determine Qibla direction, show a nearby locality name, and search for nearby mosques. Device-location updates are not intentionally stored as a location history and are not sent to a SalahPath-operated server.

If you manually choose a city or postal code, SalahPath resolves that place and stores the selected latitude, longitude, and locality locally on the device so the manual location remains available between launches. You can clear the saved manual location in the app.

Apple system services, including Core Location, geocoding, and MapKit local search, may process location information and nearby-search requests according to Apple's own privacy terms.

You can revoke location access at any time in iOS Settings. Prayer-time and Qibla features that require the current location may then be unavailable or less accurate.

## Notifications

Prayer reminders are scheduled as local iOS notifications. SalahPath does not use a remote push-notification server for these reminders.

## Calendar

When you choose to add an Islamic date to your calendar, SalahPath opens Apple's native event editor with a prepared event. You choose whether to save it and which calendar to use. SalahPath does not read your calendar contents through this feature.

## Quran content and audio

The validated Arabic Uthmani Quran corpus is bundled with SalahPath and can be read without contacting a Quran-content provider. Optional translation/transliteration data and recitation audio are requested from AlQuran.cloud and the Islamic Network media CDN when needed. These services necessarily receive normal network request information such as the requesting IP address while serving content. Their current published terms state that the AlQuran API applies rate limits by source IP.

SalahPath does not intentionally send your GPS coordinates, manually selected latitude/longitude, worship tracker data, Quran bookmarks, prayer history, fasting tracker state, or other local app state to these Quran services.

SalahPath does not create, read, or transmit an advertising identifier or another device-level identifier. Normal HTTPS requests to Quran-content providers necessarily expose ordinary connection metadata such as the requesting IP address to those providers while the request is served. SalahPath does not receive or store those providers' server logs. The provider terms reviewed on 7 October 2026 do not specify how long API/CDN request logs are retained. We therefore cannot state that all connection metadata is discarded immediately or that the provider never links requests. Provider-side data handling must be established before finalizing the App Store privacy disclosures.

Provider terms: https://alquran.cloud/terms-and-conditions

## Tracking, advertising, and sale of data

SalahPath does not use App Tracking Transparency identifiers, advertising identifiers, advertising SDKs, or cross-app tracking. SalahPath does not sell personal data.

## Retention and deletion

Local app settings and tracker data remain on the device until changed, reset where the app provides that option, or removed with the app. The operating system may include local settings in a device backup according to your Apple backup settings; restoring such a backup can restore them. Downloaded Quran translation/transliteration cache data and audio cache files can be deleted from SalahPath's settings and are also removed when the app is deleted. A saved manual location can also be cleared from SalahPath's settings.

SalahPath has no user account database from which an account needs to be deleted. Data that may be processed independently by Apple or external Quran-content providers is subject to those providers' retention policies.

## Changes

This policy may be updated when SalahPath's features or data practices change. The current version is published in this repository.

## Contact and support

The following support page is public. Reading it does not require an account; posting an issue requires a GitHub account. Do not include private worship records, precise location, or other sensitive information in public issues. A private contact channel must be established before handling requests that require personal information.

For general questions or non-sensitive bug reports:

https://github.com/Achmed06/SalahPath-iOS/issues
