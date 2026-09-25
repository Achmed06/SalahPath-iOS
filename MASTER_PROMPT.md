# MASTER PROMPT — SalahPath iOS autonomous repair & browser-first QA

Repository: `Achmed06/SalahPath-iOS`  
Default branch: `main`

## Operating rule

Always inspect the current real repository state first. Never assume an old chat commit, build number, patch folder or reconstructed source is authoritative. Work from the checked-in source on `main`, preserve stable features, make real code changes, keep CI green, and verify visually through the simulator/browser-oriented screenshot workflows before asking for iPhone testing.

When the user says **weiter**, continue autonomously from the current repo state. Do not ask for approval, do not repeat already completed work, and do not stop after a single micro-fix when more verified work can be completed safely.

## Current baseline

Treat SalahPath v3.63 Build 79 and the newest `main` HEAD as the working baseline. Version/build labels must be read from the repository, not memory.

## Browser-first development workflow

1. Prefer GitHub Actions simulator screenshots and targeted FAST previews over repeated physical iPhone installs.
2. FAST preview must build the checked-in current source directly. It must never reconstruct an old v3.56 source tree and replay historical patch scripts.
3. Use one-screen/focused preview targets for iteration; use the full UI suite only at meaningful checkpoints.
4. Every screenshot workflow must fail on build errors, launch crashes, blank screens or missing screenshots.
5. Keep deterministic QA routes for Home, Quran, Quran pages 1/302/604, prayer guide, male/female poses, Wudu steps, Qibla, prayer tracker, onboarding, settings, daily dua and other major screens.
6. Physical iPhone testing is reserved for device-only behavior such as sensors, signing, background execution and final acceptance.

## Non-negotiable product constraints

- German and Turkish remain first-class.
- Hanafi/Diyanet presentation stays explicit where school-specific details exist.
- Do not machine-retranslate vetted Quran text.
- Bundled Uthmani Quran must remain complete: 114 surahs, 6236 ayahs, pages 1–604.
- Prayer times must use Gregorian date handling, the correct effective timezone and location-aware calculation.
- Qibla must use the actual location plus true/geographic north where available. The visual arrow tip and Kaaba marker must indicate the same physical target direction.
- Prayer tracker must cover the five obligatory prayers, persist correctly, refresh across screens, reject future-day mutation and keep pause logic intact.
- Audio must not silently regress: Quran recitation, continuous playback, cache/fallback behavior, daily dua audio, background audio, Now Playing controls and Adhan preview/notifications need explicit checks.
- No LiveContainer-specific startup blocker may be required for the normal app path.
- Onboarding must cover welcome/language, prayer audience (man/woman), location choice including manual location, and a reliable fully tappable Continue action.

## Prayer and Wudu visual rules

- Prayer and Wudu are the highest-risk visual areas.
- Do not regenerate or replace unrelated assets while fixing them.
- For prayer/Wudu images, prefer the last repository-contained visuals known to be correct from **23 September 2026 or earlier** when current later replacements are visibly wrong.
- Restore/copy only the affected prayer/Wudu assets; do not roll back unrelated code or screens.
- Right/left semantics are from the worshipper's own perspective.
- Wudu order must remain correct: right arm before left arm; right foot before left foot.
- Prayer sequence must contain the complete second rakʿah, not a shortened placeholder.
- Final Salam is right first, then left.
- Male/female assets must route independently; never derive female names by unsafe string replacement of `male_`.
- Images must be standalone clean assets, consistently framed, not collage crops or visibly clipped atlas fragments.
- Avoid text or step numbers baked into instructional artwork unless the existing vetted design explicitly requires it.
- Prayer/Wudu progression should be scroll-driven/automatic as requested; do not add persistent Next/Back step buttons. A normal navigation back affordance may return to the previous step/screen.

## Icons

- Keep a coherent SalahPath icon system.
- Never crop the wrong cell from an icon atlas.
- Validate the atlas geometry, row/column mapping and every visible Home/Discover/tab icon.
- If an individual standalone icon exists and is the more reliable source, prefer it over fragile runtime atlas cropping.
- The small brand/header icon must reflect its intended prayer/day state rather than an arbitrary decorative icon.
- Do not replace unrelated icons while fixing one broken icon.

## Quran

- Quran list, favorites, Juz, progress and reader must remain populated.
- Pages 1, 302 and 604 are mandatory regression screenshots.
- Offline bundled Arabic Quran is the primary content source.
- Network calls may enrich/fallback but must not create empty reader pages when the bundled corpus is available.
- Audio must continue across verses/surahs according to the current product behavior and retain background playback support.

## Qibla

- Recheck the math and the visual composition together.
- `rotation = normalized(qiblaBearing - trueHeading)` or its mathematically equivalent formulation is the intended relationship.
- The arrow tip must point toward the Kaaba; the Kaaba marker must not visually sit behind the arrow in the opposite direction.
- If magnetic heading is used, convert with true heading where available and handle unavailable heading gracefully.
- Manual prayer-time location must not be overwritten merely to obtain device heading calibration.

## Audio

- Treat audio as functional logic, not visual-only QA.
- Detect failures to resolve URLs, start playback, continue queues, cache files and resume from mini-player/lock screen controls.
- Keep legal/source attribution files intact.
- Do not claim audio works merely because the build compiles.

## Code-quality / regression discipline

- Do not use patch-script replay as the release source of truth.
- Avoid force unwraps / force tries in startup and user-content paths.
- Remove dead/obsolete compatibility paths when they can conflict with the current implementation.
- Prefer one canonical implementation over parallel legacy implementations.
- Keep accessibility labels and Dynamic Type behavior intact where practical.
- Do not rewrite giant files unnecessarily; make focused edits.
- Every fix should be protected by an automated regression check when a stable textual/structural invariant is available.

## Required QA order

1. Preflight and build.
2. Launch smoke test.
3. Home + tab/discover icons.
4. Onboarding/location/audience.
5. Prayer guide male and female, including sitting, finger, second rakʿah and Salam.
6. Wudu all 13 steps, especially right/left arm, head/ears and right/left foot.
7. Quran list + pages 1/302/604 + audio.
8. Qibla.
9. Prayer times.
10. Prayer tracker.
11. Daily dua + global audio mini-player.
12. Settings/Adhan test.
13. Full DE visual pass, then TR spot-check.
14. Unsigned IPA only at a checkpoint or when explicitly requested.

## Completion standard

Do not report "finished" because one build is green. A checkpoint is complete only when:
- current-source preflight passes,
- simulator build passes,
- app launches,
- targeted screenshots are nonblank and visually checked,
- known user-reported regressions are addressed,
- no unrelated stable section was rolled back,
- the final commit SHA and remaining device-only limitations are stated accurately.
