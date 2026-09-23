# SalahPath audio licenses and provenance

Release target: SalahPath 3.62 (77)

## `SalahZeit/Resources/adhan-short.caf`

Purpose: optional custom iOS notification sound used exactly at the selected prayer time. Pre-reminders continue to use the normal iOS notification sound.

- Recording: **Beautiful adhan**
- Original author: **Adam-synagda**
- Original source: Wikimedia Commons
- Source page: https://commons.wikimedia.org/wiki/File:Beautiful_adhan.ogg
- License: **CC0 1.0 Universal**
- License page: https://creativecommons.org/publicdomain/zero/1.0/
- Original upload date shown by Wikimedia Commons: 29 April 2022
- SalahPath bundled derivative: 18.0-second opening phrase group, Linear PCM, 44.1 kHz mono, with a short fade at the end
- Audited Git blob SHA: `3145c872878db49bcab080a10efb6545faec423d`

The bundled CAF is the same audited derivative documented in the Darul-Irfan open-source project's audio provenance record at commit `47f1ed0e1330a6e75b0f3ec981e0f8d86f3a5cc1`. The file is pinned by content hash in SalahPath's release preflight and IPA build checks.

CC0 permits copying, modification and redistribution, including commercial redistribution, without requiring attribution. SalahPath keeps this record anyway so App Review and future maintainers can trace the recording and license.

## iOS notification constraint

The short derivative is intentionally used instead of the full recording because iOS custom notification sounds must stay below Apple's notification-sound duration limit. The full recording is not bundled or auto-played in the background by SalahPath.

## Future audio

Do not add another adhan, Fajr-specific adhan, Sela, dua or other third-party recording unless its redistribution rights are verified and recorded here before release.
