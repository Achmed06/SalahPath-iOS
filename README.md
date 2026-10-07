# SalahPath iOS

Native iPhone prayer companion built with SwiftUI. Current release candidate: **3.62 (79)**.

- German and Turkish interface, including localized location permission text
- Prayer times, Qibla, local reminders and nearby mosque search
- Illustrated two-rak'ah prayer and Wudu lessons; written guides for other prayer forms
- Complete bundled Arabic Quran; optional translation, transliteration and recitation services
- Local prayer/fasting trackers, Dhikr counter, Duas and Islamic calendar
- No login, advertising SDK, analytics SDK or in-app purchase implementation

## Build

Open `SalahZeit.xcodeproj` in Xcode 26 or later. The project owns the app identity and shared Info.plist. Run `scripts/preflight_reference_build.sh` before building.

`scripts/build_unsigned_ipa.sh` creates and checks an unsigned Release archive, then writes `SalahPath-unsigned.ipa`. This is a testing artifact and cannot be uploaded to App Store Connect as a signed distribution build.

`scripts/archive_app_store.sh` prepares and verifies a signed local App Store export on a configured Mac. It requires `SALAH_DEVELOPMENT_TEAM` and signing credentials, and does not upload or submit the app.

See `APP_STORE_SUBMISSION.md` and `qa/APP_STORE_READINESS_2026-10-07.md` for remaining release requirements. Successful CI does not establish TestFlight device behavior or App Review approval.

## Sources and preservation

Prayer calculation uses Adhan Swift 1.5.0 under the MIT license; its full notice is bundled and visible in Profile > Lizenzen / Lisanslar. Quran text, translations and recitation use AlQuran.cloud / Islamic Network; keep source and translator/reciter attribution visible. See `CONTENT_RIGHTS_AUDIT.md`, `AUDIO_LICENSES.md` and `RELIGIOUS_CONTENT_AUDIT.md` for evidence and limits.

Approved prayer/Wudu artwork is protected by `qa/APPROVED_ASSET_POLICY.md`. Do not change it during unrelated fixes.
