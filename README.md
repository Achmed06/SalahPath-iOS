# SalahPath v3.5

Private iPhone prayer, Quran and daily worship companion built with SwiftUI.

## v3.5

- Rebuilt the Salah/Wudu learning flow for one-handed iPhone use.
- Detailed German + Turkish instructions for every major prayer movement.
- Explicit “what you do” and “what you say” sections.
- Male/female Hanafi posture notes based on Diyanet guidance.
- Clear Kavme sequence: rising phrase, complete upright pause, then transition to sujud.
- Clear final Salam: first face right, repeat the Salam phrase, then face left and repeat it; no circular-arrow illustration.
- Full 2-, 3-, 4-rak'ah and Hanafi Witr walkthrough.
- Full core recitation text for Subhanaka, Fatiha, Tashahhud, Salli, Barik and Rabbana.
- Rebuilt Wudu guide with the four Hanafi fard components marked separately.
- Uses cropped artwork from the earlier user-approved SalahPath prayer/Wudu poster style rather than the later replacement sheet.

## v3.4

- Morning and evening Adhkar with daily progress counters and source references.
- Daily Deen goals on the home dashboard.
- Prayer tracker with streaks and a neutral tracker-pause option.
- Optional tracker pause for situations such as menstruation without storing a reason.
- Fasting tracker stored locally on device.
- Umm al-Qura Hijri calendar with calculated Islamic dates and selected events.
- Short-surah memorisation mode with 1×, 3× or 5× playback.
- Quran audio URLs resolved from the AlQuran.cloud audio API rather than relying only on hard-coded CDN URLs.
- Full-surah and per-ayah human recitation.
- CC0 Wikimedia prayer photos plus a CC0 general salah-position reference.
- Precise GPS coordinates are no longer printed on the home screen.

## Prayer

- GPS-based Fajr, sunrise, Dhuhr, Asr, Maghrib and Isha.
- Countdown to the next prayer.
- Full Fard + Sunnah + Witr sequence instead of showing only obligatory rak'ah.
- Selectable Standard or Hanafi Asr rule.
- Calculation methods and manual minute corrections.
- Local prayer notifications.
- Qibla compass.
- Middle of the night and start of the last third.
- Separate male/female learning profile.
- Hanafi-specific posture differences are labelled as Hanafi instead of being presented as universal.
- Wudu and step-by-step Salah learning.

## Daily worship

- Prayer tracker.
- Daily Deen mini-goals.
- Daily dua.
- Morning/evening Adhkar.
- Dhikr/Tasbih counter.
- Fasting tracker.
- Tracker pause.
- Hijri calendar.

The Adhkar library intentionally shows references and does not claim that one list is the only complete form. Current references include Quran 2:255 and entries from Hisn al-Muslim / hadith collections such as Bukhari, Abu Dawud and Tirmidhi.

## Quran

- Arabic Quran text.
- German translation: Bubenheim & Elyas edition exposed by AlQuran.cloud.
- Turkish translation: Diyanet edition exposed by AlQuran.cloud.
- Human recitation with selectable reciter.
- Full-surah playback.
- Per-ayah playback.
- Bookmarks and last-read position.
- Short-surah learning with repetition.

For public/commercial distribution, API terms, translation rights, audio rights and attribution should be reviewed again before App Store publication.

## German + Turkish

German and Turkish are first-class app languages throughout the learning and daily-use interface.

## Prayer visuals

SalahPath uses openly licensed references rather than copying images from commercial apps.

Current visual references include CC0 material from Wikimedia Commons:
- Muslim Kid Praying
- Women performing prayer
- Salat or Muslim Prayers – sequence/posture illustration

The general sequence illustration is not presented as a complete madhhab-specific male/female posture authority.

## Prayer-dua learning

Prayer duas and Quran surahs are separated clearly in the UI. Current prayer-dua learning links point to official Diyanet material where available instead of shipping unverified third-party MP3 files.

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

Location is requested while using the app for prayer-time and Qibla calculations. SalahPath does not intentionally persist precise coordinates. Daily worship tracking uses local UserDefaults and is not designed to upload personal tracking data.
