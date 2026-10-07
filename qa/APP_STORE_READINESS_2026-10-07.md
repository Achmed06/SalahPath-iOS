# App Store readiness review — 7 October 2026

## Baseline and scope

- Repository: `Achmed06/SalahPath-iOS`; default branch `main` verified through GitHub and Git.
- Starting commit: `75d34c6ee0f11e367720669bbe01160b9a6debbe` (preserved in Git history).
- Verified baseline: unsigned IPA run **1466** and UI Capture run **1047** succeeded for that commit.
- This review targets release packaging, permissions/localization, privacy consistency, content attribution, user-facing settings and existing regression coverage. Prior religious audit and approved artwork remain preserved.
- No App Store Connect account was inspected; no signed upload or review submission was performed.

## Confirmed problems corrected

1. The unsigned builder used a post-build Info.plist patch for background audio, while ordinary archives used a different path. A shared Info.plist now declares the audio array before signing. CI now exercises Archive and validates its unchanged bundle.
2. Version/build values were overridden and repeated in packaging/provenance. The project is now authoritative, build increases to **79**, and provenance uses the verified archive metadata.
3. The product/scheme still used the internal `SalahZeit.app` name when archived without the IPA script's override. Both paths now produce `SalahPath.app`.
4. Location purpose text was a combined German/Turkish sentence, without corresponding localized permission resources. Both languages are now declared and bundled individually. First-launch app language follows supported system localization, and in-app system controls follow the selected language.
5. Adhan Swift's required MIT notice was not in the app's resources/UI. The exact upstream 1.5.0 notice is now bundled and accessible offline.
6. Settings implied that the Arabic Quran only worked offline after opening pages. Copy now distinguishes the always-bundled Arabic corpus from downloaded translations/audio. The font-size control has an accessible label; notification status uses user-facing wording and explains the 28-second Adhan excerpt.
7. The submission checklist falsely described a Device ID collection entry absent from the manifest and treated uncertain provider retention as a final privacy answer. It now records the actual manifest, verified network behavior and the evidence still required. The policy no longer implies known provider log retention.
8. README still described obsolete third-party teaching-page audio. It now describes the current sources and build paths. German/Turkish Store descriptions and review notes match implemented features.

## Verification

- Existing release preflight and content regression guards: passed locally.
- Approved prayer/Wudu asset guard: all 96 protected files unchanged.
- App Store icon source files: RGB PNGs without alpha; 1024-pixel marketing icon present.
- Release-bundle verifier: negative tests cover absent background mode, old SDK, stale build number, leaked debug marker, modified Quran and missing Turkish permission resource.
- Shell syntax and workflow YAML: checked locally.
- Remote archive and UI verification: the owner explicitly authorized publishing, CI validation and merging on 7 October 2026. Results must be read from the checks for this change's exact source commit; the baseline runs above do not validate it. Linux cannot run Xcode or an iPhone simulator locally. Successful CI still does not establish signed distribution or device behavior.
- Visual captures demonstrate rendering, not interactive device behavior or permission/compass accuracy.

## Remaining release gates

1. **External Quran provider privacy:** reviewed terms do not establish retention, linkage and full use of API/CDN request metadata. Resolve and align policy/manifest/App Store privacy answers before submission. Do not guess a data category.
2. **Owner contact:** current support is public GitHub Issues. A private owner-approved support/privacy contact is not established. Do not put sensitive requests into public issues.
3. **Developer account/signing:** team/App ID, distribution signing, Time Sensitive entitlement, unused upload build number, App Store record and Apple's validation/processing remain unverified. The new signed export script is preparation, not proof of successful signing.
4. **Actual iPhone/TestFlight:** clean install, permission denial/recovery, manual location, compass, local notifications under Focus/silent modes, lock-screen audio, calendar save/cancel and network-loss behavior need device evidence.
5. **Store metadata:** current screenshots, age rating, EU trader status, review contact and final privacy answers must be completed in the actual account. Avoid claiming all prayer forms are illustrated.

## Primary references rechecked

- Apple requirements: https://developer.apple.com/news/upcoming-requirements/
- Review requirements: https://developer.apple.com/app-store/review/guidelines/
- Privacy classification: https://developer.apple.com/app-store/app-privacy-details/
- Quran provider terms: https://alquran.cloud/terms-and-conditions
- Adhan Swift notice: https://github.com/batoulapps/adhan-swift/blob/1.5.0/LICENSE

Kann Richtigkeit nicht garantieren – bitte verifizieren.
