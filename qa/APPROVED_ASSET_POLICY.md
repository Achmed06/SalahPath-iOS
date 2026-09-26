# SalahPath approved asset policy

This file is a hard safety rule for future SalahPath work.

## Non-negotiable rule

The currently approved Prayer and Wudu assets are frozen.

Never regenerate, replace, rename, mirror, crop, reorder, or delete any asset whose path starts with:
- `SalahZeit/Assets.xcassets/male_`
- `SalahZeit/Assets.xcassets/female_`
- `SalahZeit/Assets.xcassets/wudu_`

unless the user explicitly asks to change that exact asset in the current conversation.

For unrelated work such as audio, Quran, Qibla, tracker, notifications, icons, build scripts, or layout:
- do not touch approved Prayer/Wudu assets;
- do not restore a whole old asset directory;
- do not copy a whole asset sheet;
- do not regenerate approved images;
- change only the minimum explicitly targeted files.

## Direction semantics

- `*_salam_right`: the praying person's own RIGHT side.
- `*_salam_left`: the praying person's own LEFT side.
- Salam order is RIGHT first, then LEFT.
- `wudu_rightarm`: the depicted person's right arm.
- `wudu_leftarm`: the depicted person's left arm.
- `wudu_rightfoot`: the depicted person's right foot.
- `wudu_leftfoot`: the depicted person's left foot.

Do not infer right/left from the viewer's perspective.

## Required workflow before every future change

1. Read `qa/approved-prayer-wudu-assets.tsv`.
2. Make the requested non-asset change only.
3. Run `scripts/verify_approved_prayer_wudu_assets.sh`.
4. If verification fails, STOP. Do not "fix" it by updating the manifest.
5. Update the manifest only after explicit user approval of a deliberate Prayer/Wudu asset replacement.

The manifest is a guardrail, not a file to auto-refresh.
