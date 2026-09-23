# SalahPath audio provenance

Release target: SalahPath 3.62 (77)

## Doha Adhan notification clips

SalahPath build 77 bundles two short iOS notification sounds derived from the Internet Archive item **“Adhan Recordings from Doha, Qatar”**.

Source item:
- Internet Archive identifier: `adhan.recordings.from.doha.qatar`
- Recorded: 2013–2014 according to the item metadata
- Usage shown by the source item: **Public Domain Mark 1.0**
- Source item page: https://archive.org/details/adhan.recordings.from.doha.qatar
- Creative Commons Public Domain Mark explanation: https://creativecommons.org/publicdomain/mark/1.0/

The Public Domain Mark states that the work has been identified as free of known copyright restrictions and may be copied, modified, distributed and performed, including commercially. It is a public-domain status mark rather than a license grant; Creative Commons also notes jurisdiction and other-rights caveats. SalahPath therefore keeps the original source identity and hashes below for auditability.

### `SalahZeit/Resources/adhan-fajr.caf`

- Source file: `Adhan_Doha_Qatar_01_Fajr_Adhan.mp3`
- Used for: Fajr / Sabah prayer-time notification
- Source SHA-256: `a64afe612048e2e068d9475cf481f34acc1fe3c7f34de700bebe6779fa3d1bc0`
- Bundled derivative: first 28 seconds, mono Linear PCM CAF, 44.1 kHz, 1.5-second fade-out
- Bundled SHA-256: `e0641b2e4a04f38f38c7cc8479a0a3e4d8c5d9a577d04e9acd32c135fb2df47f`
- Bundled Git blob: `546fee5cde9e0e4e9041ed02c44bc0dc5290eb19`

### `SalahZeit/Resources/adhan-standard.caf`

- Source file: `Adhan_Doha_Qatar_02_Dhuhr_Adhan.mp3`
- Used for: Dhuhr, Asr, Maghrib and Isha prayer-time notifications
- Source SHA-256: `106b6c632799eb1da7e87782b3cf160e27a76dde086f9557e920cdcb1883dc3b`
- Bundled derivative: first 28 seconds, mono Linear PCM CAF, 44.1 kHz, 1.5-second fade-out
- Bundled SHA-256: `8752346b8fab95baa41b991790233ef99e85e86728fb8d296113aba274eeef43`
- Bundled Git blob: `5af226c758c556e318f0fe667b415a02807a8c2c`

The generated source and derivative hashes are also stored in `qa/adhan-audio-hashes.txt`. Release preflight and IPA verification pin the derivative content so the audio cannot silently change.

## iOS behavior

The clips are intentionally shorter than 30 seconds because they are used as iOS custom notification sounds.

- Fajr uses the dedicated Fajr recording.
- Dhuhr, Asr, Maghrib and Isha use the standard Doha recording.
- Advance reminders use the normal iOS notification sound.
- If a bundled audio file cannot be resolved, SalahPath falls back to the normal iOS notification sound instead of failing the notification.

## Future recordings

Do not add another Adhan, Sela, dua or other third-party recording unless its redistribution status is verified and recorded here before release.
