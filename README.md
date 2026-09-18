# SalahPath v3.1

Private iPhone prayer and learning companion built with SwiftUI.

## v3.1 additions

- Quran bookmarks and last-read tracking
- Per-ayah human recitation playback
- Reciter selector: Alafasy, Al-Husary, Al-Minshawi and Al-Sudais
- Improved child-friendly prayer figures
- SalahPath-branded bilingual location permission text

## Core

- GPS-based Fajr, sunrise, Dhuhr, Asr, Maghrib and Isha
- Countdown to the next prayer
- Qibla compass
- Hijri date, middle of the night and start of the last third
- Local prayer notifications
- Calculation methods and manual minute corrections
- Selectable Standard or Hanafi Asr rule

## German + Turkish

The learning interface is designed around German and Turkish. Language can be changed in Settings.

## Prayer learning

- Full Fard, Sunnah and Witr rak'ah overview
- Step-by-step salah guide
- Separate male and female learning profiles
- Male/female posture notes are explicitly presented as Hanafi/Turkish teaching where relevant, not as universal differences
- Child-friendly Muslim prayer illustrations instead of stick figures
- Wudu guide
- Arabic prayer formulas with transliteration and German/Turkish explanations
- Dhikr and Tasbih counter

## Quran

SalahPath v3 includes a Quran browser with Arabic text plus German or Turkish translation.

Prototype data:
- Arabic: AlQuran.cloud `quran-uthmani`
- German: `de.bubenheim`
- Turkish: `tr.diyanet`
- Human recitation: Mishary Rashid Alafasy via Islamic Network CDN

For a public/commercial release, Quran text, translations, audio licenses, attribution and API terms must be reviewed again before distribution.

## Dua audio

The prototype contains streaming links for human-recorded prayer-learning audio. These are not AI-generated voices.

Current external prototype recordings include:
- Sübhaneke
- Ettehiyyatü
- Salli / Barik
- Rabbena

Rights for those external recordings have not been confirmed for public redistribution. They should be cleared or replaced with an explicitly licensed source before a public App Store release.

## Prayer calculation

The project uses Adhan Swift by Batoul Apps through Swift Package Manager.

## Build

Requirements:
- macOS with Xcode
- iOS 17 or newer

The Xcode project/scheme remains internally named `SalahZeit` for compatibility, while the built application is branded `SalahPath`.

Run:

```bash
./scripts/build_unsigned_ipa.sh
```

Output:

```text
SalahPath-unsigned.ipa
```

The generated IPA is unsigned and cannot be installed directly on a normal iPhone until it is signed with an Apple development/distribution identity or a sideloading tool.

## Privacy

Location is requested while using the app for prayer-time and Qibla calculations. SalahPath does not intentionally persist the user's precise coordinates.
