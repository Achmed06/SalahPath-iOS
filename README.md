# SalahPath

Private iPhone prayer-time app built with SwiftUI.

## Included

- Prayer start times from the iPhone's current GPS location
- Offline astronomical calculation after the app is built
- Calculation methods: Muslim World League, Moonsighting Committee, Diyanet/Turkey approximation, Egyptian, Karachi, Umm al-Qura, ISNA, Dubai, Qatar, Kuwait, Singapore, Tehran
- Selectable Asr rule: standard (Shafi'i/Maliki/Hanbali) or Hanafi
- Fajr, sunrise, Dhuhr, Asr, Maghrib, Isha
- Countdown to the next prayer
- Fard rak'ah count and a compact Sunni rak'ah guide
- Friday/Jumu'ah note
- Qibla compass
- Hijri date (Umm al-Qura calendar)
- Middle of the night and start of the last third
- Local prayer notifications for the next 7 days
- Per-prayer manual minute corrections
- No mosque server and no hard-coded home address

## Prayer calculation

The project uses **Adhan Swift** by Batoul Apps through Swift Package Manager, version 1.5.0 or newer within the same major version.

Repository: https://github.com/batoulapps/adhan-swift
License: MIT

The Adhan documentation states that its Turkey method is an approximation of Diyanet and is less accurate outside Turkey. For that reason the app lets the user choose the calculation method instead of presenting one method as universally authoritative.

## Open in Xcode

Requirements:

- macOS with Xcode
- iOS 17 or newer deployment target

Open `SalahZeit.xcodeproj`. Xcode resolves the Adhan Swift package automatically. Select your Apple Development team under **Signing & Capabilities**, connect the iPhone, and Run.

## Build an unsigned IPA

On a Mac with Xcode:

```bash
./scripts/build_unsigned_ipa.sh
```

Output:

```text
SalahPath-unsigned.ipa
```

An unsigned IPA is not directly installable on a normal iPhone. It still has to be signed with a valid iOS development/distribution identity or by a sideloading tool that performs signing.

## GitHub Actions build

The repository contains `.github/workflows/build-unsigned-ipa.yml`. When uploaded to GitHub, the workflow builds `SalahPath-unsigned.ipa` on a macOS runner and provides it as a workflow artifact.

## Privacy

The app requests location only while in use. Coordinates are used in memory to calculate prayer times and Qibla direction. The app does not intentionally upload or persist the current coordinates.

## Lernen & Dhikr

- Schritt-für-Schritt-Gebetsanleitung mit schematischen Körperhaltungs-Bildern
- Arabisch, Transliteration und deutsche Bedeutung zentraler Formeln
- Wudu-Anleitung mit visuellen Symbolen
- Rakʿat-Übersicht und Begriffserklärungen
- Dhikr nach dem Pflichtgebet
- Integrierter Tasbih-Zähler mit 33er/3er-Vorgaben
