# MASTER PROMPT — SalahPath iOS autonomous repair, browser-first QA & regression recovery

Repository: `Achmed06/SalahPath-iOS`  
Authoritative branch: `main`

## Mission

Repair SalahPath from the current checked-in repository state until the app is visually coherent, functionally stable and regression-protected. Work autonomously. The browser/simulator screenshot workflow is the primary iteration loop. Physical iPhone installs are reserved for device-only verification and final checkpoints.

Never trust an old chat state, old build number, stale patch directory, generated reconstruction, or remembered implementation over the newest real `main` source. Always inspect HEAD first.

When the user writes **weiter**, continue immediately from the current repo state without asking what to do next.

## Operating rules

1. Inspect current HEAD, recent commits, CI state and affected source before editing.
2. Make real source changes. Do not only analyse or describe.
3. Prefer focused, reversible changes over broad rewrites.
4. Never reintroduce obsolete patch-script replay as the source of truth.
5. Do not stop after one micro-fix when additional verified repairs can be completed safely.
6. Do not claim a feature is fixed merely because Swift compiles.
7. Do not claim the app is finished until the defined acceptance gates pass.
8. Keep stable existing behavior unless a concrete regression or product requirement requires change.
9. Every recurring regression should gain a deterministic guard where practical.
10. Browser/simulator QA must always use the current checked-in source, not reconstructed legacy source.

## Current product baseline

Read version/build from the repository on every session. Do not hard-code a remembered version as authoritative.

The current repair baseline is the latest `main` HEAD after the browser-first QA work introduced on 25 September 2026.

## Priority: current user-reported regressions

Treat all of the following as open until specifically verified:

### Startup / global stability
- App must launch without a LiveContainer-specific blocker.
- No startup crash, blank root screen, dead tab, or unrecoverable loading state.
- Browser/simulator screenshot jobs must fail if launch or capture fails.
- Root navigation must remain stable after repeated tab changes and deep links used by QA.

### Icons / visual identity
- Home, Discover/Entdecken, tab bar and feature icons must use the correct individual asset.
- No icon may be visibly clipped, cropped from the wrong atlas cell, stretched, padded strangely or show parts of neighboring icons.
- Prefer standalone assets over fragile atlas cropping where possible.
- All visible feature icons must share one coherent SalahPath visual language.
- The small header/day-state icon near the top must represent the intended dynamic prayer/day state. It must not be a random static symbol.
- Verify sunrise/sunset-related state changes explicitly.
- Do not replace unrelated correct icons while repairing one broken icon.

### Prayer guide
- Male and female prayer illustrations must be routed independently.
- Never derive female asset names through unsafe string substitution.
- Right/left meaning is from the worshipper's perspective.
- Complete first rakʿah and complete second rakʿah must exist.
- The second rakʿah must not be shortened to a placeholder.
- Sitting/Tashahhud posture and raised-finger state must use the correct matching illustration.
- Final Salam sequence is RIGHT first, then LEFT.
- Prayer guide progression must be scroll-driven/automatic as requested.
- Do not add permanent Next/Back step buttons inside the prayer sequence.
- Standard navigation back may still leave the guide.
- Images must be standalone, correctly framed, consistent in size and style and not collage fragments.

### Wudu / Abdest
- Wudu must contain all intended steps in correct sequence.
- Correct right/left mirroring is mandatory.
- Right arm before left arm.
- Right foot before left foot.
- Head/ears steps must use the intended illustrations.
- Male/female presentation must not accidentally swap sides.
- Wudu progression must be scroll-driven/automatic, without permanent Next/Back step controls.
- Verify every Wudu image individually in screenshot QA.

### Quran
- Quran list, Surah navigation, Juz, favorites/progress and reader must never be empty when bundled data exists.
- Bundled Uthmani Quran remains authoritative offline content.
- Corpus integrity: 114 surahs, 6236 ayahs, pages 1–604.
- Mandatory reader regression screenshots: page 1, page 302, page 604.
- No network failure may create blank Quran pages if bundled content is available.
- Do not machine-retranslate vetted Quran text.

### Audio — treat as a complete subsystem
Audio is currently considered unverified until all paths are tested.

Verify:
- Quran verse playback actually starts.
- Queue/continuous playback advances correctly.
- Surah transition behavior works.
- Cached audio resolves and replays.
- Network fallback resolves usable audio URLs.
- Daily Dua audio starts.
- Global mini-player controls work.
- Pause/resume works.
- Background audio session is configured.
- Now Playing metadata/controls remain coherent.
- Adhan preview works.
- Notification sound configuration remains valid.
- Failures expose a recoverable state instead of silently doing nothing.
- Keep legal/source attribution for audio assets and remote providers intact.

A green build is not evidence that audio works.

### Qibla
- Recheck location source, heading source, bearing math and visual composition together.
- Intended relationship is mathematically equivalent to:
  `rotation = normalized(qiblaBearing - trueHeading)`
- Prefer true/geographic heading where available.
- Handle unavailable heading gracefully.
- The arrow tip must point toward the Kaaba.
- The Kaaba marker must be visually on the same target direction, never behind the arrow by 180°.
- Manual prayer-time location must not be overwritten merely to calibrate device heading.
- Simulator/browser QA should verify deterministic visual states.
- Physical device test is still required for real magnetometer behavior.

### Prayer times / location
- Gregorian date handling only for calculation flow unless an explicit display transformation is intended.
- Correct effective timezone for selected/manual/current location.
- Manual location must remain available.
- Current-device location and manual location must be distinguishable in state.
- Changing location must refresh dependent prayer-time/Qibla views coherently.

### Prayer tracker
- Track the five obligatory prayers.
- Persistence must survive view recreation/relaunch.
- UI must refresh immediately after mutation.
- Future-day mutation must be rejected.
- Pause logic must remain intact.
- No stale dashboard state after editing from another screen.

### Onboarding
Onboarding must cover:
1. Welcome / language.
2. Prayer audience: man or woman.
3. Location mode.
4. Manual location option.
5. Reliable Continue action with full intended tappable area.
6. Completion state that does not trap the user on relaunch.

### German / Turkish
- German and Turkish remain first-class.
- No hard-coded German text should leak into Turkish flows where localization already exists.
- Do a full German visual pass and a Turkish spot-check before a checkpoint.

## Browser-first development workflow

1. Use GitHub Actions simulator previews as the normal iteration path.
2. FAST preview must compile current checked-in `SalahZeit` source.
3. Use targeted screens for fast iteration.
4. Use full UI regression only at meaningful checkpoints.
5. Keep deterministic QA routes for at least:
   - launch/root
   - home
   - discover
   - onboarding
   - prayer male standing/bowing/prostration/sitting/salam
   - prayer female equivalents
   - Wudu all steps
   - Quran list
   - Quran pages 1/302/604
   - Quran audio state
   - Qibla
   - prayer times
   - prayer tracker
   - daily dua
   - settings
   - Adhan preview
6. Screenshot jobs must reject:
   - build failure
   - launch failure
   - blank screenshot
   - missing expected screenshot
7. Do not rebuild an old v3.56 tree and replay patch scripts.
8. Cache build artifacts only when the cache key reflects the current Xcode project, Swift sources and assets.

## Visual asset rules

- Prayer/Wudu assets are high-risk. Do not mass-regenerate them casually.
- When current prayer/Wudu artwork is visibly wrong, prefer last known-good repository-contained artwork from 23 September 2026 or earlier.
- Restore only affected assets.
- Do not roll back unrelated code.
- Each imageset must reference exactly one real standalone asset file unless Apple platform conventions require scale variants.
- Valid visual files: SVG, PNG, JPG/JPEG.
- Feature/navigation artwork should remain vector where practical.
- Never use a collage crop as a production asset.
- Never bake unrelated labels or step numbers into instructional artwork unless the approved design intentionally does so.

## Architecture / code quality

- Prefer one canonical implementation for each subsystem.
- Remove obsolete compatibility branches when they conflict with current behavior.
- Avoid force unwraps and force tries in startup, audio, Quran and navigation paths.
- Avoid giant file rewrites.
- Keep state ownership explicit.
- Ensure async work updates UI state on the appropriate actor.
- Avoid duplicated network/audio managers competing for playback.
- Keep accessibility labels and Dynamic Type behavior where practical.
- Preserve privacy manifest and required usage descriptions.
- Do not break App Store privacy or attribution metadata.

## Regression guards

Add a guard whenever a stable invariant can be checked automatically. Examples:
- required Quran corpus files exist and decode
- pages 1/302/604 resolve non-empty content
- required prayer/Wudu asset imagesets exist
- every referenced asset file exists
- Discover/Home icon mappings resolve to expected standalone assets
- prayer sequence contains complete second rakʿah
- Salam order is right then left
- Wudu arm/foot ordering is correct
- prayer tracker has five obligatory prayers
- future-day mutation path is blocked
- no LiveContainer-only startup gate
- screenshot workflow uses checked-in source
- no known blank-screen compatibility branch becomes authoritative again

## Required QA order

1. Read HEAD + recent diffs.
2. Strict preflight.
3. Simulator build.
4. Launch smoke test.
5. Root navigation.
6. Home icons/header state.
7. Discover/Entdecken icons.
8. Onboarding.
9. Prayer male.
10. Prayer female.
11. Wudu every step.
12. Quran list.
13. Quran pages 1/302/604.
14. Quran audio.
15. Qibla.
16. Prayer times/location.
17. Prayer tracker.
18. Daily Dua + global audio player.
19. Settings + Adhan preview.
20. Full German screenshot pass.
21. Turkish spot-check.
22. Only then create an unsigned IPA checkpoint if explicitly requested or strategically useful.

## Acceptance gate

Never say “fertig” unless all applicable points below are confirmed:

- preflight passes
- simulator build passes
- app launches
- root screen is nonblank
- all targeted screenshots exist
- screenshots were visually inspected, not merely generated
- user-reported icon regressions are resolved
- prayer and Wudu sequence/order/mirroring is correct
- second rakʿah is complete
- Salam is right then left
- Quran pages 1/302/604 are populated
- audio has at least one functional runtime verification path, not compile-only evidence
- Qibla composition is mathematically and visually consistent
- prayer tracker persistence/state refresh is verified
- onboarding completes
- no unrelated stable feature was rolled back
- latest commit SHA is reported accurately
- remaining device-only limitations are explicitly listed

## Reporting style

Progress reports must distinguish:
- CONFIRMED: directly verified by source, CI log, screenshot or runtime evidence.
- LIKELY: strong code-level evidence but runtime/device verification still pending.
- UNKNOWN: not yet verified.

Never conceal unverified areas behind a general “fixed” statement.

## Continuation trigger

If the user says **weiter**, immediately:
1. inspect newest HEAD,
2. identify the highest-impact still-unverified item,
3. implement the next repair,
4. trigger or inspect the smallest useful browser/simulator QA path,
5. continue until a meaningful checkpoint or a genuine external/device limitation is reached.
