#!/usr/bin/env bash
# Release checkpoint: SalahPath v3.62 build 76; cleanup chain validated through v422.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "PRECHECK ERROR: $*" >&2
  exit 1
}

echo "== SalahPath preflight =="

test -d SalahZeit || fail "SalahZeit source directory missing"
test -f SalahZeit/SalahZeitApp.swift || fail "SalahZeitApp.swift missing"
test -f SalahZeit/Views/HomeView.swift || fail "HomeView.swift missing"
test -f SalahZeit/Views/RootTabView.swift || fail "RootTabView.swift missing"
test -f SalahZeit/Views/GuideView.swift || fail "GuideView.swift missing"
test -f scripts/build_unsigned_ipa.sh || fail "build script missing"

# Patch/merge integrity.
if grep -RInE '^(<<<<<<<|=======|>>>>>>>)' SalahZeit scripts 2>/dev/null; then
  fail "merge-conflict markers found"
fi

# Current expected app version after the v3.62 build 76 release checkpoint.
grep -q 'MARKETING_VERSION="3.62"' scripts/build_unsigned_ipa.sh   || fail "expected MARKETING_VERSION 3.62 not present"
grep -q 'CURRENT_PROJECT_VERSION="76"' scripts/build_unsigned_ipa.sh   || fail "expected build number 76 not present"

# Reference assets introduced by the visual parity passes.
required_assets=(
  home_mosque
  ref_dash_quran ref_dash_dhikr ref_dash_prayer ref_dash_wudu
  ref_dash_times ref_dash_qibla ref_dash_info ref_dash_fav
)

for asset in "${required_assets[@]}"; do
  dir="SalahZeit/Assets.xcassets/${asset}.imageset"
  test -d "$dir" || fail "asset imageset missing: $asset"
  test -f "$dir/Contents.json" || fail "Contents.json missing: $asset"
done

# Validate every asset-catalog JSON file and all PNG signatures.
python3 - <<'PY'
from pathlib import Path
import json, sys

root = Path("SalahZeit/Assets.xcassets")
for path in root.rglob("Contents.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"PRECHECK ERROR: invalid asset JSON {path}: {exc}", file=sys.stderr)
        raise SystemExit(1)

import struct, zlib

png_sig = b"\x89PNG\r\n\x1a\n"
for path in root.rglob("*.png"):
    data = path.read_bytes()
    if len(data) < 8 or data[:8] != png_sig:
        print(f"PRECHECK ERROR: invalid PNG signature: {path}", file=sys.stderr)
        raise SystemExit(1)

    offset = 8
    saw_iend = False
    while offset < len(data):
        if offset + 12 > len(data):
            print(f"PRECHECK ERROR: truncated PNG chunk header: {path}", file=sys.stderr)
            raise SystemExit(1)
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            print(f"PRECHECK ERROR: truncated PNG chunk payload: {path}", file=sys.stderr)
            raise SystemExit(1)
        payload = data[offset + 8:offset + 8 + length]
        stored_crc = struct.unpack(">I", data[offset + 8 + length:chunk_end])[0]
        actual_crc = zlib.crc32(chunk_type)
        actual_crc = zlib.crc32(payload, actual_crc) & 0xffffffff
        if stored_crc != actual_crc:
            print(f"PRECHECK ERROR: PNG CRC mismatch: {path}", file=sys.stderr)
            raise SystemExit(1)
        offset = chunk_end
        if chunk_type == b"IEND":
            saw_iend = True
            break

    if not saw_iend:
        print(f"PRECHECK ERROR: PNG missing IEND: {path}", file=sys.stderr)
        raise SystemExit(1)

print("Asset JSON + PNG structural integrity: OK")
PY

# Ensure QA routing added for the five visual-reference screens exists.
grep -Rqs 'SALAH_QA_SCREEN' SalahZeit   || fail "multi-screen screenshot QA routing missing"

# Ensure required reference copy/data survived the patch chain.
grep -q '2:38:15' SalahZeit/Views/HomeView.swift   || fail "reference countdown missing"
grep -q 'Rabbim, ilmimi artır.' SalahZeit/Views/HomeView.swift   || fail "reference daily dua missing"
grep -q 'Text(settings.t("Dua des Tages", "Günün Duası"))' SalahZeit/Views/HomeView.swift \
  || fail "localized daily-dua heading missing"
grep -q 'Text(settings.t("Gebets-Tracking", "Namaz Takibi"))' SalahZeit/Views/HomeView.swift \
  || fail "localized prayer-tracking heading missing"
grep -q 'Text(settings.t("Nächstes Gebet", "Sıradaki Namaz"))' SalahZeit/Views/HomeView.swift \
  || fail "localized next-prayer heading missing"
grep -q 'Text(settings.t("(An-Nisāʾ 4:103)", "(Nisâ, 103)"))' SalahZeit/Views/HomeView.swift \
  || fail "localized Home Quran citation missing"

# Language-consistency regressions fixed after v3.62.
grep -q 'settings.t("Gebetszeiten", "Namaz Vakitleri")' SalahZeit/Views/HomeView.swift \
  || fail "localized prayer-times title missing"
grep -q 'settings.t("Morgen", "Sabah")' SalahZeit/Views/GuideView.swift \
  || fail "localized Dhikr tabs missing"
grep -q 'Text(activeDhikr.translation)' SalahZeit/Views/GuideView.swift \
  || fail "localized Dhikr translation output missing"
grep -q 'settings.t("Arabisch", "Arapça")' SalahZeit/Views/GuideView.swift \
  || fail "localized Quran language tabs missing"
grep -q 'audiencePill(.male, title: settings.t("Mann", "Erkek"))' SalahZeit/Views/GuideView.swift \
  || fail "localized prayer audience selector missing"
grep -q 'settings.language = settings.language == .german ? .turkish : .german' SalahZeit/Views/GuideView.swift \
  || fail "bidirectional prayer language toggle missing"
grep -q 'settings.language == .german ? german : turkish' SalahZeit/Views/GuideView.swift \
  || fail "language-specific prayer feature copy missing"
grep -q 'settings.t("Arabisch", "Arapça")' SalahZeit/Views/GuideView.swift \
  || fail "localized Quran reader language copy missing"
grep -q 'settings.t("Tägliche Serie", "Günlük Seri")' SalahZeit/Views/HomeView.swift \
  || fail "localized Home streak copy missing"
grep -q '.navigationBarTitleDisplayMode(.inline)' SalahZeit/Views/GuideView.swift \
  || fail "compact navigation headers missing"
grep -q 'settings.t("Gebet lernen", "Namaz Öğren")' SalahZeit/Views/GuideView.swift \
  || fail "localized German prayer-learning title missing"
grep -q 'settings.t("Gebet lernen", "Namaz öğren")' SalahZeit/Views/GuideView.swift \
  || fail "localized German prayer-howto title missing"
grep -q 'settings.t("Hijri-Kalender", "Hicrî takvim")' SalahZeit/Views/GuideView.swift \
  || fail "localized German Hijri title missing"
grep -q 'settings.t("Gebet lernen", "Namaz Öğren")' SalahZeit/Views/RootTabView.swift \
  || fail "localized Discover prayer title missing"
grep -q 'settings.t("Wudu", "Abdest Rehberi")' SalahZeit/Views/RootTabView.swift \
  || fail "localized Discover Wudu title missing"
grep -q 'settings.t("Qibla", "Kıble")' SalahZeit/Views/RootTabView.swift \
  || fail "localized Discover Qibla title missing"
grep -q 'settings.t("Qibla", "Kıble")' SalahZeit/Views/QiblaView.swift \
  || fail "localized Qibla screen heading missing"
grep -q 'settings.t("Hijri-Kalender", "Hicrî Takvim")' SalahZeit/Views/RootTabView.swift \
  || fail "localized Discover Hijri title missing"
grep -q 'settings.t("FARZ · PFLICHT", "FARZ")' SalahZeit/Views/GuideView.swift \
  || fail "localized guided-Wudu obligation badge missing"
grep -q 'case "wudu_rightfoot": footVisual(mirrored: false)' SalahZeit/Views/GuideView.swift \
  || fail "right-foot Wudu artwork mapping missing"
grep -q 'case "wudu_leftfoot": footVisual(mirrored: true)' SalahZeit/Views/GuideView.swift \
  || fail "left-foot Wudu artwork mapping missing"
grep -q '.navigationTitle(settings.t("Wudu lernen", "Abdest öğren"))' SalahZeit/Views/GuideView.swift \
  || fail "localized guided-Wudu navigation title missing"

# Phase-1 interaction regressions fixed in v394.
grep -q 'navigation.setBackIndicatorImage(backIndicator' SalahZeit/Views/RootTabView.swift \
  || fail "high-contrast navigation back indicator missing"
grep -q '.toolbarColorScheme(.dark, for: .navigationBar)' SalahZeit/Views/RootTabView.swift \
  || fail "dark navigation toolbar color scheme missing"
grep -q 'private let playbackRateDefaultsKey = "quranPlaybackRate"' SalahZeit/Views/GuideView.swift \
  || fail "persistent Quran playback-rate state missing"
grep -q 'Button { audio.cyclePlaybackRate() } label:' SalahZeit/Views/GuideView.swift \
  || fail "Quran reader playback-rate button missing"
if grep -q 'Text("1.0x")' SalahZeit/Views/GuideView.swift; then
  fail "stale non-interactive Quran 1.0x label still present"
fi

# Learning content stays inside SalahPath as of v395.
if grep -RIn 'Link(' SalahZeit/Views --include='*.swift' | grep -v 'NavigationLink' | grep -v 'ShareLink'; then
  fail "external SwiftUI Link remains in learning UI"
fi
grep -q 'private struct PrayerDuaLesson: Identifiable' SalahZeit/Views/GuideView.swift \
  || fail "in-app prayer dua lessons missing"
grep -q 'Alle Gebetsduas stehen direkt in SalahPath' SalahZeit/Views/GuideView.swift \
  || fail "in-app prayer dua explanation missing"

# Guided prayer learning introduced in v396.
grep -q '@State private var currentStepIndex = 0' SalahZeit/Views/GuideView.swift \
  || fail "guided prayer step state missing"
grep -q 'PrayerTutorialStepCard(step: steps\[currentStepIndex\]' SalahZeit/Views/GuideView.swift \
  || fail "single-step prayer tutorial card missing"
grep -q 'settings.t("Weiter", "İleri")' SalahZeit/Views/GuideView.swift \
  || fail "guided prayer next control missing"

# Beginner Rakʿa flow introduced in v397.
grep -q 'Was bedeutet Rakʿa?' SalahZeit/Views/GuideView.swift \
  || fail "beginner Rakʿa introduction missing"
grep -q 'JETZT ist 1 Rakʿa fertig' SalahZeit/Views/GuideView.swift \
  || fail "Rakʿa completion explanation missing"
grep -q '@State private var showSpecialCases = false' SalahZeit/Views/GuideView.swift \
  || fail "Rakʿa progressive-disclosure state missing"
grep -q 'navigationTitle(settings.t("Rakʿa verstehen", "Rekâtı anla"))' SalahZeit/Views/GuideView.swift \
  || fail "Rakʿa beginner navigation title missing"

# Guided Wudu flow introduced in v398.
grep -q 'Wudu ganz von vorne' SalahZeit/Views/GuideView.swift \
  || fail "guided Wudu introduction missing"
grep -q 'Nacken / Ense' SalahZeit/Views/GuideView.swift \
  || fail "Wudu nape wording missing"
grep -q 'normalen Haaransatz bis zum Kinn' SalahZeit/Views/GuideView.swift \
  || fail "Wudu face boundary explanation missing"
grep -q '1× Farz · 3× Sunnah' SalahZeit/Views/GuideView.swift \
  || fail "Wudu Farz and Sunnah repetition label missing"
grep -q 'navigationTitle(settings.t("Wudu lernen", "Abdest öğren"))' SalahZeit/Views/GuideView.swift \
  || fail "guided Wudu navigation title missing"

# Stable indexed Rakʿa plan iteration in v399.
grep -q 'ForEach(lines.indices, id: \\.self)' SalahZeit/Views/GuideView.swift \
  || fail "stable indexed Rakʿa plan iteration missing"

# v400: controlled prayer artwork now includes simple facial features.
grep -q 'private func drawFace(_ context: inout GraphicsContext' SalahZeit/Views/GuideView.swift \
  || fail "prayer facial-feature drawing missing"

# v401: Quran Continue Reading restores the last Surah/Ayah.
grep -q 'static func lastRead() -> QuranBookmark?' SalahZeit/Views/GuideView.swift \
  || fail "Quran last-read getter missing"
grep -q 'settings.t("Weiterlesen", "Okumaya devam et")' SalahZeit/Views/GuideView.swift \
  || fail "Quran Continue Reading card missing"
grep -q 'QuranSurahView(surah: chapter, initialAyah: lastRead.ayah)' SalahZeit/Views/GuideView.swift \
  || fail "Quran Continue Reading deep link missing"

# v402: complete fasting/Ramadan learning hub.
grep -q 'Fasten ganz einfach' SalahZeit/Views/GuideView.swift \
  || fail "fasting beginner lesson missing"
grep -q 'Was bricht das Fasten?' SalahZeit/Views/GuideView.swift \
  || fail "fasting invalidators lesson missing"
grep -q 'Qada, Kaffarah, Fidya' SalahZeit/Views/GuideView.swift \
  || fail "fasting compensation terminology missing"

# v403: interactive Hijri calendar and internal event explanations.
grep -q 'Nächste wichtige islamische Tage' SalahZeit/Views/GuideView.swift \
  || fail "important Islamic days section missing"
grep -q 'Beginn der letzten zehn Ramadan-Nächte' SalahZeit/Views/GuideView.swift \
  || fail "last ten Ramadan nights guidance missing"
grep -q 'Tage des Tashriq' SalahZeit/Views/GuideView.swift \
  || fail "Tashriq guidance missing"
grep -q 'Weiße Tage · 13., 14. und 15.' SalahZeit/Views/GuideView.swift \
  || fail "white days guidance missing"

# v404-v405: structured Islam-learning course.
grep -q 'Islam Schritt für Schritt lernen' SalahZeit/Views/GuideView.swift \
  || fail "Islam learning hub missing"
grep -q 'Die fünf Säulen' SalahZeit/Views/GuideView.swift \
  || fail "five pillars lesson missing"
grep -q 'Die sechs Glaubensgrundsätze' SalahZeit/Views/GuideView.swift \
  || fail "six beliefs lesson missing"
grep -q 'Tawbah · Reue und Neubeginn' SalahZeit/Views/GuideView.swift \
  || fail "repentance lesson missing"
grep -q 'NavigationLink { IslamLearningHubView() }' SalahZeit/Views/RootTabView.swift \
  || fail "Islam learning Discover tile missing"
if grep -q 'ersetzen etmez' SalahZeit/Views/GuideView.swift; then
  fail "stale mixed-language Turkish copy remains"
fi

if grep -q 'gıdaähnliche' SalahZeit/Views/GuideView.swift; then
  fail "mixed-language German fasting copy remains"
fi
grep -q 'Bilerek ağız dolusu kusmak' SalahZeit/Views/GuideView.swift \
  || fail "beginner-friendly Turkish vomiting wording missing"
grep -q 'feuchten Traum, wenn beim Aufwachen entsprechende Flüssigkeit festgestellt wird' SalahZeit/Views/GuideView.swift \
  || fail "precise Ghusl wet-dream wording missing"

# v406-v407: QA coverage for new learning screens.
grep -q 'case "fasting-basics":' SalahZeit/SalahZeitApp.swift \
  || fail "fasting basics QA route missing"
grep -q 'case "fasting-rules":' SalahZeit/SalahZeitApp.swift \
  || fail "fasting rules QA route missing"
grep -q 'case "fasting-exceptions":' SalahZeit/SalahZeitApp.swift \
  || fail "fasting exceptions QA route missing"
grep -q 'case "islam-learning":' SalahZeit/SalahZeitApp.swift \
  || fail "Islam learning QA route missing"

# v408-v409: Ghusl and Tayammum learning + QA routes.
grep -q 'navigationTitle(settings.t("Ghusl lernen", "Gusül öğren"))' SalahZeit/Views/GuideView.swift \
  || fail "Ghusl learning view missing"
grep -q 'Die 3 Farz im Hanafi/Diyanet-Ablauf' SalahZeit/Views/GuideView.swift \
  || fail "Ghusl Hanafi farz explanation missing"
grep -q 'navigationTitle(settings.t("Tayammum lernen", "Teyemmüm öğren"))' SalahZeit/Views/GuideView.swift \
  || fail "Tayammum learning view missing"
grep -q 'case "ghusl":' SalahZeit/SalahZeitApp.swift \
  || fail "Ghusl QA route missing"
grep -q 'case "tayammum":' SalahZeit/SalahZeitApp.swift \
  || fail "Tayammum QA route missing"

# v410: automatic Ramadan Home integration.
grep -q 'private func isRamadan(_ date: Date) -> Bool' SalahZeit/Views/HomeView.swift \
  || fail "Ramadan month detection missing"
grep -q 'ramadanHomeCard(today: today)' SalahZeit/Views/HomeView.swift \
  || fail "Ramadan Home card missing"
grep -q 'settings.t("Sahur endet", "Sahur biter")' SalahZeit/Views/HomeView.swift \
  || fail "Ramadan Sahur timing missing"
grep -q 'settings.t("Iftar", "İftar")' SalahZeit/Views/HomeView.swift \
  || fail "Ramadan Iftar timing missing"

# v411: Discover fasting entry now reflects the full learning hub.
grep -q 'settings.t("Fasten & Ramadan", "Oruç & Ramazan")' SalahZeit/Views/RootTabView.swift \
  || fail "updated fasting Discover title missing"
grep -q 'settings.t("Lernen & Tracker", "Öğren & takip")' SalahZeit/Views/RootTabView.swift \
  || fail "updated fasting Discover subtitle missing"

# v412: unified SalahPath duotone Discover icon system.
grep -q 'private func salahFeatureIcon' SalahZeit/Views/RootTabView.swift \
  || fail "unified Discover feature icon helper missing"
grep -q 'LinearGradient(' SalahZeit/Views/RootTabView.swift \
  || fail "Discover icon gradient styling missing"

# v415: compiler-friendly learning subviews.
grep -q 'private var fastingHeaderCard: some View' SalahZeit/Views/GuideView.swift \
  || fail "split fasting header subview missing"
grep -q 'private var eventHeaderCard: some View' SalahZeit/Views/GuideView.swift \
  || fail "split Hijri event header subview missing"
grep -q 'private var lessonHeaderCard: some View' SalahZeit/Views/GuideView.swift \
  || fail "split Islam lesson header subview missing"
grep -q 'private var islamProgressCard: some View' SalahZeit/Views/GuideView.swift \
  || fail "split Islam progress subview missing"

# v416: Quran reader shows one selected translation only.
grep -q '@State private var didSetInitialDisplayMode = false' SalahZeit/Views/GuideView.swift \
  || fail "Quran reader initial language state missing"
grep -q 'displayMode = settings.language == .german ? 2 : 1' SalahZeit/Views/GuideView.swift \
  || fail "Quran reader app-language default missing"
grep -q 'settings.quranShowTranslation && displayMode == 1' SalahZeit/Views/GuideView.swift \
  || fail "Quran Turkish-only translation condition missing"
grep -q 'settings.quranShowTranslation && displayMode == 2' SalahZeit/Views/GuideView.swift \
  || fail "Quran German-only translation condition missing"
grep -q 'settings.t("Deutsch", "Almanca")' SalahZeit/Views/GuideView.swift \
  || fail "Quran localized German language label missing"

# v417: clearer frontal Wudu artwork and direct QA access to every step.
grep -q 'private var neutralFace: some View' SalahZeit/Views/GuideView.swift \
  || fail "clear frontal Wudu face artwork missing"
grep -q 'init(initialStepIndex: Int = 0)' SalahZeit/Views/GuideView.swift \
  || fail "Wudu initial-step QA initializer missing"
grep -q 'case "wudu-step-1":' SalahZeit/SalahZeitApp.swift \
  || fail "Wudu step 1 QA route missing"
grep -q 'case "wudu-step-13":' SalahZeit/SalahZeitApp.swift \
  || fail "Wudu step 13 QA route missing"

# v419: Quran overview follows the selected/app language without duplicate translation.
grep -q 'if languageTab == 1 {' SalahZeit/Views/GuideView.swift \
  || fail "Quran overview Turkish-only condition missing"
grep -q 'if languageTab == 2 {' SalahZeit/Views/GuideView.swift \
  || fail "Quran overview German-only condition missing"
grep -q 'languageTab = settings.language == .german ? 2 : 1' SalahZeit/Views/GuideView.swift \
  || fail "Quran overview app-language default missing"

# v422: Build 76 checkpoint.
grep -q 'CURRENT_PROJECT_VERSION="76"' scripts/build_unsigned_ipa.sh \
  || fail "Build 76 checkpoint missing"

# Parse every Swift file before Xcode build. This catches syntax damage from a patch
# before package resolution/build spends several minutes.
if command -v xcrun >/dev/null 2>&1; then
  echo "Parsing Swift sources..."
  while IFS= read -r -d '' file; do
    xcrun swiftc -frontend -parse "$file" >/dev/null
  done < <(find SalahZeit -name '*.swift' -type f -print0)
  echo "Swift parse: OK"
else
  echo "xcrun unavailable: skipping Swift parse on this host"
fi

echo "SalahPath preflight: PASS"

# v422: Build 76 checkpoint.
grep -q 'CURRENT_PROJECT_VERSION="76"' scripts/build_unsigned_ipa.sh \
  || fail "Build 76 checkpoint missing"

# v421: Turkish UI must use Almanca instead of Deutsch.
grep -q 'settings.t("Deutsch + Türkisch", "Almanca + Türkçe")' SalahZeit/Views/RootTabView.swift \
  || fail "Turkish language-pair label still mixed"
grep -q 'settings.t("Arabisch, Türkisch, Deutsch", "Arapça, Türkçe, Almanca")' SalahZeit/Views/GuideView.swift \
  || fail "Turkish Quran language-list label still mixed"
