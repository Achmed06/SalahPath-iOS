# SalahPath v3

Private iOS prayer companion built with SwiftUI.

## v3

- German and Turkish UI foundation
- GPS prayer times, Qibla, countdown and notifications
- Full daily prayer sequence with Fard, Sunnah and Witr overview
- Separate male/female learning profiles based primarily on the Hanafi/Turkish teaching presentation, with explicit madhhab caveats
- Child-friendly vector prayer illustrations instead of stick figures
- Wudu guide
- Dhikr / Tasbih counter
- Full Quran chapter browser loaded from AlQuran.cloud
- Arabic Quran text plus German (Bubenheim & Elyas) or Turkish (Diyanet) translation
- Human Quran recitation via Islamic Network CDN (Mishary Rashid Alafasy)
- Human-recorded prayer-dua streaming links with source attribution

## Data and content sources

- Prayer calculation: Adhan Swift (MIT)
- Quran text, translations and Quran audio: AlQuran.cloud / Islamic Network. Keep edition attribution visible and comply with the source terms.
- Turkish fiqh/teaching structure is based on Diyanet educational material, especially its Hanafi prayer sequence and stated male/female posture differences.
- Prayer-dua recordings currently stream from externally hosted teaching pages and should be rights-cleared before any public App Store distribution.

## Build

Open `SalahZeit.xcodeproj` in Xcode or run:

```bash
./scripts/build_unsigned_ipa.sh
```

Output: `SalahPath-unsigned.ipa`.

The IPA is unsigned and must be signed before installation on a stock iPhone.
