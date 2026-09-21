# SalahPath content-rights audit

Audit date: 21 September 2026  
Target build: SalahPath 3.62 (76)

## Current Quran integration

The current build requests Quran text, translations and recitation audio from AlQuran.cloud / Islamic Network. It uses the edition identifiers `quran-uthmani`, `de.bubenheim`, `tr.diyanet`, and the selectable recitation editions exposed by the service. The app visibly attributes AlQuran.cloud / Islamic Network, Diyanet, Bubenheim & Elyas, and the selected reciter in the Quran reader.

No StoreKit, advertising SDK, analytics SDK, subscription framework or in-app purchase implementation is present in the audited build.

## Provider terms checked

AlQuran.cloud Terms & Conditions, last updated 14 June 2026:
https://alquran.cloud/terms-and-conditions

The published terms state that:

- the Arabic Quran text may be reproduced, embedded, stored and displayed, with faithful preservation of the Uthmani text;
- translations are contributed by rights-holders or sourced from public-domain editions and republishing should attribute the translator;
- recitations are licensed to AlQuran.cloud by reciters or their estates for free, non-commercial redistribution at the published bitrates;
- streaming, embedding and downloading for personal and educational use are allowed;
- the underlying copyrights remain with the reciters/rightsholders and they may request removal.

Islamic Network also publicly answered a 2026 commercial-use question by referring developers back to those published terms, and stated that Quran/API content should not be put behind a paywall. The current SalahPath build does not put Quran text or audio behind a paywall.

Relevant community clarification:
https://community.islamic.network/d/257-commercial-use-of-quran-audio-text-via-your-cdnapi-educational-app

## Release decision for the audited build

For the current build, the documented provider terms support the way SalahPath uses the Quran service: reading, streaming and local audio caching are not paywalled, source/translator attribution is present, and the app does not redistribute the files as a separate media product.

Because reciters and translation rightsholders retain their rights, this audit is not a transfer of copyright. If SalahPath later introduces paid Quran access, subscriptions that gate Quran content, advertising tied to Quran access, resale, redistribution outside the app, or a different Quran/audio provider, the rights review must be repeated before release.

## App Store evidence

Keep this file, the current AlQuran.cloud Terms & Conditions, and the in-app attribution available for App Review. Apple App Review Guideline 5.2.2 requires permission under a third-party service's terms when an app uses or displays third-party content.
