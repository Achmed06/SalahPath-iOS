# SalahPath development audit — 20 September 2026

Baseline: `19a9a74`, SalahPath 3.62 build 73. The existing production build and UI capture runs succeeded. No release version increment is part of this change.

## Architecture and verification

The repository stores a base64 ZIP plus 95 ordered Python patches, not the current Swift tree. The app restores to 13 Swift files. `GuideView.swift` contains learning, Quran networking, playback, bookmarks, fasting and calendar (~3,500 lines); `HomeView.swift` contains theme, home and tracking (~2,100 lines). Settings are an injected observable store backed by UserDefaults. Prayer calculations use Adhan; location uses CoreLocation; reminders use UserNotifications. The Xcode project uses explicit source file entries.

The new portable restoration entry point verifies the original ZIP SHA-256, excludes archived CI/README files, and applies an explicit ordered manifest. Existing release and capture workflows also apply the new patch. FAST already discovers it. The development workflow builds the original Xcode project and generates a separate test harness for XCTest and XCUITest.

## Confirmed phase-one findings and changes

- Reader speed was static `Text("1.0x")`; it is now a real button bound to the player, with spoken value and 44-point target.
- Play/pause decisions used asynchronous AVPlayer status. A second tap during buffering could request play again. A synchronous playback-intent flag now handles taps; stale callbacks are ignored by player/item identity.
- Reader pause previously stopped/restarted the full queue. It now pauses and resumes the same queue.
- Playback rate now persists and validates restored values.
- Both translations rendered in the default Quran mode. Default now follows app language; explicit DE/TR choices persist across Quran screens and sharing.
- Quran listing silently stopped after eight entries. All fetched surahs are now reachable.
- Quran font sizes below 28 were silently overridden despite settings allowing them. The selected size is now respected.
- Quran preview constrained its content to a poster aspect ratio and added 100 points of empty space before navigation. Both constraints are removed.
- Bottom navigation labels were 7.1 points with further shrinking. They now use scalable caption text, wrap, and have at least 44-point targets.
- RootTabView duplicated and overwrote global navigation appearance. It now uses the single app configuration; native back text/chevron have explicit white rendering.
- QA roots previously added a decorative, nonfunctional back chevron. It is removed so screenshots no longer simulate navigation controls.

## Remaining work and release gates

Phase one is NOT visually signed off. Linux has no Xcode/Swift/iOS simulator. Local source restoration and asset/preflight checks pass; CI compile, XCTest, XCUITest and actual screenshot inspection must be recorded separately. Screenshots are evidence of rendering, not of GPS, compass or notification behavior.

Full-app layout, Dynamic Type, dark mode and interactive navigation remain to be reviewed. The app currently forces light mode; theme constants do not yet implement dark mode. Existing learning images are not validated religious references.

Phase two: research Diyanet/Hanafi sources before rebuilding Wudu, prayer units, full male/female lessons and fiqh classifications. Existing lesson contents are not treated as verified sources.

Phase three: research visual design and generate/review consistent per-step assets; retain native text.

Phase four: last-read currently writes from lazy row onAppear (prefetch can change it), has no visible resume entry point, audio has no disk cache/repeat/speed UI consistency audit. Fix visible reading position and stale reciter requests; test reopening.

Phase five: fasting currently is a tracker; calendar currently is a limited list. Research and implement full in-app fasting/Ramadan/calendar content and date uncertainty handling.

Phase six: learning hub, Ghusl/Tayammum, integrated prayer dua content (currently external Diyanet links), broader glossary and sourced dua/dhikr lessons.

Other confirmed issues: Qibla substitutes zero heading when sensor data is missing; notification scheduling requests authorization repeatedly, removes all pending notifications and needs concurrent-reschedule protection; local prayer calculations require DST/day rollover/location regression tests. These are not yet fixed by phase one.

Phase seven: DE/TR, small phone, large type, dark mode, navigation, all learning routes, audio, Quran continuation, Ramadan and calendar. Real iPhone gates: heading/GPS, permissions, reminders, background/lock-screen audio. No new release before these gates pass.
