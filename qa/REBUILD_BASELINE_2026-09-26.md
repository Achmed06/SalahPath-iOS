# SalahPath rebuild baseline · 2026-09-26

## Verified source

- GitHub repository: `Achmed06/SalahPath-iOS`; authenticated connector reports push permission.
- Default branch: `main`, HEAD before this branch: `7d25042d9495332841f6bfaf7efe4dc62f1ea7f2` (`[ci] Keep full UI capture manual for direct main iteration`). The original tree is retained at that immutable commit. Working copy was clean at checkout.
- 58 remote branches, no Git tags at checkout. Existing workflows: `actions-recovery-smoke`, `build-unsigned-ipa`, `capture-ui`, `fast-preview`, `restore-legacy-prayer-wudu`.
- Xcode project: `SalahZeit.xcodeproj`, iPhone target, deployment target iOS 17, bundle identifier `com.achmed06.salahpath`, version 3.64 (80). CI uses `macos-26`, `iphoneos`, `CODE_SIGNING_ALLOWED=NO`.

## Verified components retained

- `scripts/preflight_reference_build.sh` validates the bundled Arabic Quran corpus across all 604 pages, audio-file hashes, asset structure and release regression guards. It runs locally without Xcode.
- Existing `PrayerEngine`, `LocationManager`, notification service and bundled Quran data are kept pending device-level verification. Their presence and static guards do not prove runtime correctness.
- The current audio player adds one intro URL when starting a queue and has a resume path. Actual audio behavior has not been observed on a device.

## Changes on rebuild branch

- Extract tracker persistence from `HomeView` into `Models/PrayerTrackerStore.swift` and adaptive design colors into `Design/SalahTheme.swift`. This preserves their existing behavior and starts clear ownership boundaries.
- Bind left arm and left foot Abdest steps to their left-side images without an additional mirror transform. Preserve Salam order right then left.
- Move compass rotation to `Domain/QiblaGeometry.swift` and add a focused executable angle regression test. Only a valid true-north heading activates the arrow; invalid readings cannot silently turn into a wrong needle direction.

## Open release risks

- The legacy SwiftUI presentation still spans very large files. A comprehensive visual rebuild and full screen-by-screen QA are not complete.
- The original artwork has small JPEG assets and no verified licensing metadata for every image. Static file integrity is not a visual or rights audit.
- This Linux workspace has no Xcode or Apple signing identity. An unsigned iPhoneOS `.ipa` from CI, if produced, is not installable on an ordinary iPhone until signed. A device launch test is pending.
