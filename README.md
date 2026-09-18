# SalahPath v3.6

Native SwiftUI prayer, Quran and daily-worship companion for iPhone.

## Release focus

- Native petrol/cream/gold SalahPath visual system inspired by the supplied reference designs.
- German and Turkish as first-class app languages.
- GPS prayer times, countdown, sunrise, calculation settings, Hanafi/standard Asr, manual offsets and local notifications.
- Full daily rak'ah sequence shown in context (Fard, Sunnah and Hanafi Witr), not only obligatory rak'ah.
- Qibla compass, Hijri date, middle of the night and last-third calculation.
- Daily dua, prayer tracker, optional streak, Daily Deen goals and fasting tracker.
- Morning/evening Adhkar and Dhikr/Tasbih.
- Quran reader with Arabic text, DE/TR translation, bookmarks, last-read state and human recitation.
- Short-surah learning with repetition.
- Detailed Salah learning for male/female profiles with explicit Hanafi/Turkish labels where posture details differ.
- Detailed Wudu learning with the four Hanafi fard components distinguished from sunnah/recommended steps.
- Final Salam is shown as two separate actions: right first, then left; no circular head arrow.

## Audio QA

Quran audio is resolved from the AlQuran.cloud / Islamic Network audio data. The CI release workflow makes a live HTTP/audio probe before building.

Live-verified reciters for this release:

- Mishary Rashid Alafasy
- Mahmoud Khalil Al-Husary
- Mohamed Siddiq al-Minshawi

Al-Sudais is intentionally not exposed in v3.6 because the current AlQuran API response did not provide the required per-ayah audio URL and the direct CDN fallback returned HTTP 403 during release QA. A non-working selector is not shipped.

Prayer-dua learning must not show a fake play control when no verified human recording is available. External Diyanet learning sources may be linked where appropriate.

## Religious presentation

The reference artwork is a design reference, not a religious authority. Hanafi/Turkish learning details are labelled as such and should be reviewed against reliable sources (including Diyanet) before public distribution. Quran text/translations are not machine-rewritten by SalahPath.

## Privacy

- Precise coordinates are not intentionally persisted or displayed on the dashboard.
- Daily worship tracking is local.
- No account is required for the current prototype.

## Build

Open `SalahZeit.xcodeproj` in Xcode or run:

```bash
./scripts/build_unsigned_ipa.sh
```

Output: `SalahPath-unsigned.ipa`.

The generated IPA is unsigned and must be signed before installation on a normal iPhone.

## Verification boundary

The GitHub Actions release verifies source restoration, live Quran-audio reachability for the exposed reciters, Swift package resolution, Xcode compilation and IPA creation. Sensor behaviour, notification delivery and playback through iOS hardware/audio routes are **not practically verified on a real iPhone** by CI.