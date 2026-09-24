#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

def fail(message: str) -> None:
    print(f"REGRESSION GUARD: {message}", file=sys.stderr)
    raise SystemExit(1)

def read(path: str) -> str:
    p = ROOT / path
    if not p.is_file():
        fail(f"missing required file: {path}")
    return p.read_text(encoding="utf-8")

# 1) Bundled Quran: the Arabic reader must never depend on the network.
quran_path = ROOT / "SalahZeit/Resources/quran-uthmani.json"
if not quran_path.is_file():
    fail("bundled quran-uthmani.json is missing")

try:
    quran = json.loads(quran_path.read_text(encoding="utf-8"))
except Exception as exc:
    fail(f"invalid quran-uthmani.json: {exc}")

if quran.get("code") != 200:
    fail("bundled Quran response code is not 200")

surahs = quran.get("data", {}).get("surahs", [])
if len(surahs) != 114:
    fail(f"expected 114 surahs, found {len(surahs)}")

ayahs = [ayah for surah in surahs for ayah in surah.get("ayahs", [])]
if len(ayahs) != 6236:
    fail(f"expected 6236 ayahs, found {len(ayahs)}")

numbers = [ayah.get("number") for ayah in ayahs]
if set(numbers) != set(range(1, 6237)):
    fail("global ayah numbers are incomplete or duplicated")

pages = {ayah.get("page") for ayah in ayahs if isinstance(ayah.get("page"), int)}
if pages != set(range(1, 605)):
    missing = sorted(set(range(1, 605)) - pages)
    fail(f"Quran page coverage is incomplete; missing {missing[:12]}")

for surah in surahs:
    if not (1 <= int(surah.get("number", 0)) <= 114):
        fail("invalid surah number")
    if not str(surah.get("name", "")).strip():
        fail("empty Arabic surah name")
    if not str(surah.get("englishName", "")).strip():
        fail("empty English surah name")

for ayah in ayahs:
    if not str(ayah.get("text", "")).strip():
        fail(f"empty Quran text at ayah {ayah.get('number')}")
    if not (1 <= int(ayah.get("page", 0)) <= 604):
        fail(f"invalid page at ayah {ayah.get('number')}")

guide = read("SalahZeit/Views/GuideView.swift")
local_gate = 'if edition == "quran-uthmani"'
bundle_lookup = 'Bundle.main.url(forResource: "quran-uthmani", withExtension: "json")'
network_lookup = 'https://api.alquran.cloud/v1/page/'
for token in (local_gate, bundle_lookup, network_lookup):
    if token not in guide:
        fail(f"Quran reader guard missing token: {token}")

if guide.index(local_gate) > guide.index(network_lookup):
    fail("bundled Uthmani Quran is no longer preferred before page-network access")

if "private func bundledPage(page: Int) throws -> QuranPageData" not in guide:
    fail("bundled Quran page extraction function is missing")

# 2) Prayer tracker: five obligatory prayers, persisted state and cross-view refresh.
home = read("SalahZeit/Views/HomeView.swift")
tracker_tokens = [
    "static let prayerTrackerDidChange",
    "static let requiredKinds: [PrayerKind] = [.fajr, .dhuhr, .asr, .maghrib, .isha]",
    "UserDefaults.standard.set(Array(current).sorted(), forKey: key(for: date))",
    "NotificationCenter.default.post(name: .prayerTrackerDidChange, object: nil)",
    "static func completedCount(on date: Date) -> Int",
    "static func streak(upTo date: Date) -> Int",
    "NotificationCenter.default.publisher(for: .prayerTrackerDidChange)",
]
for token in tracker_tokens:
    if token not in home:
        fail(f"prayer tracker regression: missing {token}")

if home.count("NotificationCenter.default.publisher(for: .prayerTrackerDidChange)") < 3:
    fail("tracker mutations no longer refresh Home + tracker screens consistently")

if home.count("NotificationCenter.default.post(name: .prayerTrackerDidChange, object: nil)") < 2:
    fail("tracker toggle/pause mutations no longer broadcast changes")

# 3) QA routes and screenshots must keep covering the user-reported regressions.
app = read("SalahZeit/SalahZeitApp.swift")
for route in ('case "quran-page":', 'case "prayer-tracker":'):
    if route not in app:
        fail(f"QA route missing: {route}")

capture = read(".github/workflows/capture-ui.yml")
required_captures = [
    "B78-DE-QuranPage1.png",
    "B78-DE-PrayerTracker.png",
    "B78-DE-PrayerHowTo.png",
    "B78-DE-FemalePrayerHowTo.png",
    "B78-DE-PrayerFinger.png",
    "B78-DE-FemalePrayerFinger.png",
    "B78-DE-PrayerSalam.png",
    "B78-DE-FemalePrayerSalam.png",
    "B78-DE-WuduHead.png",
    "B78-DE-WuduArm.png",
    "B78-DE-WuduFoot.png",
    "B78-DE-Qibla.png",
]
for name in required_captures:
    if name not in capture:
        fail(f"visual QA coverage missing: {name}")

# 4) Wudu copy + German prayer labels must not regress.
root_tab = read("SalahZeit/Views/RootTabView.swift")
for token in (
    'Die feuchte Hand muss Kopf oder Haar erreichen',
    'settings.t("Gebetssuren", "Namaz Sûreleri")',
    'settings.t("Gebetsduas", "Namaz Duaları")',
    'settings.t("Gebetstexte", "Namaz Metinleri")',
):
    if token not in guide and token not in root_tab:
        fail(f"localized prayer/Wudu regression: missing {token}")

for forbidden in (
    'settings.t("Namaz-Suren",',
    'settings.t("Namaz-Duas",',
    'settings.t("Namaz-Texte",',
):
    if forbidden in guide or forbidden in root_tab:
        fail(f"German UI language regression: found {forbidden}")

# 5) Prayer/Wudu illustration system must stay unified and direction-safe.
for token in (
    'Canvas { graphics, size in',
    'case "sujud", "second_sujud": drawSujud(&context, size: size)',
    'case "finger": drawSitting(&context, size: size, turn: 0, showFinger: true)',
    'if pose == "salam_right" {\n            turn = -0.22',
    '} else if pose == "salam_left" {\n            turn = 0.22',
    'switch stepNumber {',
    'case 7: armVisual(mirrored: false)',
    'case 8: armVisual(mirrored: true)',
    'case 12: footVisual(mirrored: false)',
    'case 13: footVisual(mirrored: true)',
    'Text("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ")',
    'imageKey: "salam_right",\n                deTitle: "Salām – zuerst rechts"',
    'imageKey: "salam_left",\n                deTitle: "Salām – danach links"',
    'imageName: "\\(prefix)_salam_right",\n                arrow: "arrow.right"',
    'imageName: "\\(prefix)_salam_left",\n                arrow: "arrow.left"',
):
    if token not in guide:
        fail(f"unified illustration regression: missing {token}")

# 6) Navigation/discovery icons stay in the same native SalahPath system.
home = (ROOT / "SalahZeit/Views/HomeView.swift").read_text(encoding="utf-8")
root_tabs = (ROOT / "SalahZeit/Views/RootTabView.swift").read_text(encoding="utf-8")
for token in (
    'ReferenceDashboardGlyph(kind: glyphKind)',
    'case "quran_audio":',
    'case "bookmarks":',
    'LinearGradient(',
):
    if token not in home:
        fail(f"native dashboard icon regression: missing {token}")

for token in (
    'Image(systemName: item.0)',
    '"house.fill"',
    '"book.closed.fill"',
    '"figure.mind.and.body"',
    '"sparkles.rectangle.stack.fill"',
    '"person.crop.circle.fill"',
):
    if token not in root_tabs:
        fail(f"native tab icon regression: missing {token}")

for legacy_prefix in ("sp_icon_", "ref_dash_"):
    if legacy_prefix in home or legacy_prefix in root_tabs:
        fail(f"legacy icon asset reference returned: {legacy_prefix}")

print("Build 78 regression guard: OK")
