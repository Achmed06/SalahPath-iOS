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
    "UserDefaults.standard.set(Array(current).sorted(), forKey: key(for: day))",
    "guard day <= today else { return false }",
    "static func setPaused(_ paused: Bool, on date: Date)",
    "guard day <= today else { return }",
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
for route in ('case "quran-page":', 'case "quran-page-mid":', 'case "quran-page-last":', 'case "prayer-tracker":', 'case "wudu-leftfoot":', 'case "wudu-leftarm":', 'case "namaz-salam-left":', 'case "mosques":'):
    if route not in app:
        fail(f"QA route missing: {route}")

capture = read(".github/workflows/capture-ui.yml")
for token in (
    '*"[full-ui]"*|*"[release-ui]"*) CAPTURE_MODE="full"',
    'UI_HINT="$UI_COMMIT_MESSAGE"',
    'CAPTURE_MODE="core"',
):
    if token not in capture:
        fail(f"targeted/release UI coverage regression: missing {token}")

required_captures = [
    "B78-DE-QuranPage1.png",
    "B78-DE-QuranPage302.png",
    "B78-DE-QuranPage604.png",
    "B78-DE-PrayerTracker.png",
    "B78-DE-PrayerHowTo.png",
    "B78-DE-FemalePrayerHowTo.png",
    "B78-DE-PrayerFinger.png",
    "B78-DE-FemalePrayerFinger.png",
    "B78-DE-PrayerSalam.png",
    "B78-DE-PrayerSalamLeft.png",
    "B78-DE-FemalePrayerSalam.png",
    "B78-DE-FemalePrayerSalamLeft.png",
    "B78-DE-WuduHead.png",
    "B78-DE-WuduArm.png",
    "B78-DE-WuduLeftArm.png",
    "B78-DE-WuduFoot.png",
    "B78-DE-WuduLeftFoot.png",
    "B78-DE-Qibla.png",
    "B78-DE-Onboarding.png",
    "B78-DE-Mosques.png",
    "B78-DE-DailyDua.png",
    "B78-TR-Onboarding.png",
    "B78-TR-Mosques.png",
    "B78-TR-DailyDua.png",
]
for name in required_captures:
    if name not in capture:
        fail(f"visual QA coverage missing: {name}")

if capture.count("B78-DE-PrayerSalamLeft.png") < 1 or "B78-DE-MalePrayerStep18.png" not in capture:
    fail("male final Salam must be captured in both full UI and 18-step prayer QA modes")

for step_number in range(1, 19):
    name = f"B78-DE-MalePrayerStep{step_number:02d}.png"
    if name not in capture:
        fail(f"complete male prayer visual QA coverage missing: {name}")

# 3b) Prayer calculations must remain Gregorian and location-time-zone aware.
location_manager = read("SalahZeit/Services/LocationManager.swift")
prayer_engine = read("SalahZeit/Services/PrayerEngine.swift")
notifications = read("SalahZeit/Services/NotificationManager.swift")
app_source = read("SalahZeit/SalahZeitApp.swift")
home_source = read("SalahZeit/Views/HomeView.swift")

for token in (
    'static let timeZone = "manualLocationTimeZone"',
    '@Published private(set) var prayerTimeZone: TimeZone = .autoupdatingCurrent',
    'defaults.set(resolvedTimeZone.identifier, forKey: ManualLocationKeys.timeZone)',
):
    if token not in location_manager:
        fail(f"manual-location timezone regression: missing {token}")

for token in (
    'Calendar(identifier: .gregorian)',
    'timeZone: TimeZone = .autoupdatingCurrent',
    'parameters.highLatitudeRule = HighLatitudeRule.recommended(for: coordinates)',
):
    if token not in prayer_engine:
        fail(f"prayer calculation timezone/calendar regression: missing {token}")

for token in (
    'timeZone: locationManager.prayerTimeZone',
    'locationManager.prayerTimeZone.identifier',
):
    if token not in app_source:
        fail(f"notification timezone scheduling regression: missing {token}")

for token in (
    'let diagnostics = await NotificationManager.shared.diagnostics()',
    'diagnostics.authorizationStatus == .denied',
    'settings.notificationsEnabled = false',
):
    if token not in app_source:
        fail(f"global notification permission-sync regression: missing {token}")

if notifications.count('components.timeZone = timeZone') < 2:
    fail("notification trigger timezone regression")

for token in (
    'return locationManager.prayerTimeZone',
    'timeZone: effectiveTimeZone',
    'locationManager.$prayerTimeZone',
):
    if token not in home_source:
        fail(f"prayer UI timezone regression: missing {token}")

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

for token in (
    'settings.t("Abschiedsrede", "Veda Hutbesi")',
):
    if token not in guide and token not in root_tab:
        fail(f"German farewell-sermon localization regression: missing {token}")

for forbidden in (
    'settings.t("Veda Hutbesi", "Veda Hutbesi")',
    'settings.t("Veda Hutbesi · Abschiedsrede", "Veda Hutbesi")',
):
    if forbidden in guide or forbidden in root_tab:
        fail(f"German farewell-sermon localization regression: found {forbidden}")

# 4b) Release learning UI must stay user-facing and use SalahPath artwork for content headers.
for token in (
    'struct SalahFeatureIconLabel: View',
):
    if token not in root_tab:
        fail(f"shared SalahPath icon label regression: missing {token}")

for token in (
    'private struct TutorialSectionHeader: View',
    'iconKind: "prayer"',
    'iconKind: "duas"',
    'SalahFeatureIconLabel(title: settings.t("Wudu Schritt für Schritt", "Abdest adım adım"), kind: "wudu"',
    'SalahFeatureIconLabel(title: settings.t("Gebete einzeln erklärt", "Namazlar tek tek anlatılıyor"), kind: "list"',
    'SalahFeatureIconLabel(title: localizedEventTitle, kind: "moon"',
    'deLabel: "Salām", trLabel: "Selâm"',
    'deNote: nil, trNote: nil',
):
    if token not in guide:
        fail(f"learning UI polish regression: missing {token}")

for forbidden in (
    'Den Satz einmal beim Drehen nach rechts',
    'Rechts und anschließend links',
    'systemImage: "figure.walk"',
    'systemImage: "text.bubble.fill"',
    'SalahPath verwendet diesen Bereich',
    'SalahPath entscheidet hier nicht',
    'SalahPath soll',
    'Fatwa-Automatik',
    'AlQuran.cloud-API',
    'CDN-Link',
    'SalahPath Dua-Sammlung öffnen',
    'Hier findest du die täglichen Gebete',
    'gegen Diyanet-Lehrmaterial gegengeprüft',
    'menschliche Audioedition',
    'insan ses kaydı',
    'Du siehst immer nur einen Schritt. Unten wechselst du eindeutig',
    'Her seferinde yalnız bir adım görürsün. Alttaki „Geri“ ve „Devam“',
    '2: "Nimm Wasser mit der rechten Hand in den Mund und spüle gründlich."',
    '5: "Wasche die rechte Hand und den rechten Arm bis einschließlich Ellenbogen vollständig."',
    '8: "Wische die Ohren mit feuchten Fingern innen und außen vorsichtig ab."',
    '11: "Wasche danach den linken Fuß genauso vollständig."',
    '2: "Sağ elle ağza su alıp iyice çalkala."',
    '5: "Sağ eli ve sağ kolu dirsek dahil tamamen yıka."',
    '8: "Islak parmaklarla kulakların içini ve dışını nazikçe mesh et."',
    '11: "Ardından sol ayağı da aynı şekilde tamamen yıka."',
):
    if forbidden in guide:
        fail(f"developer/meta or duplicate learning UI regression: found {forbidden}")

for token in (
    'Folge Bild, Haltung und Rezitation Schritt für Schritt.',
    'Görseli, duruşu ve okuyuşu adım adım takip et.',
    'Hanafitische Qunūt-Texte für Witr. Die Umschrift dient nur als Aussprachehilfe.',
    'Rezitation: Islamic Network.',
    'Tilavet: Islamic Network.',
):
    if token not in guide:
        fail(f"clean user-facing learning copy regression: missing {token}")

# Prayer step cards must never repeat the main action as a decorative posture tip.
for token in (
    'private var malePoseTipData: (title: String, text: String)?',
    'if isMale, let imageName, let tip = malePoseTipData',
    'private var maleSupplementalHanafiNote: String?',
):
    if token not in guide:
        fail(f"prayer tutorial de-duplication regression: missing {token}")

for forbidden in (
    'private var maleTipText: String',
    'return settings.language == .german ? step.deAction : step.trAction',
    'Die folgenden Schritte 17 und 18 beenden ein Gebet',
    'Aşağıdaki 17. ve 18. adımlar burada biten namazı selâmla tamamlar',
    'Zuerst rechts. Danach folgt Schritt 18 nach links.',
    'Önce sağa. Ardından 18. adımda sola dönülür.',
    'Reihenfolge: rechts, dann links.',
    'Sıra: önce sağ, sonra sol.',
):
    if forbidden in guide:
        fail(f"duplicate prayer tutorial copy regression: found {forbidden}")

for token in (
    'SalahFeatureIconLabel(\n                        title: settings.t("Heute wird beim Streak neutral behandelt."',
    'SalahFeatureIconLabel(title: repetition, kind: "dhikr", iconSize: 17)',
    'title: dua.localizedSource(settings.language),\n                    kind: "info"',
):
    if token not in home:
        fail(f"Home content icon regression: missing {token}")

# 5) Prayer/Wudu illustration system must stay unified and direction-safe.
if '.replacingOccurrences(of: "male_", with: "")' in guide:
    fail("female prayer pose routing regression: male_ substring stripping breaks female_ assets")

for token in (
    'Image(key)',
    'Image(assetName)',
    'number: 5, image: "wudu_rightarm", deTitle: "Rechter Arm"',
    'number: 6, image: "wudu_leftarm", deTitle: "Linker Arm"',
    'number: 10, image: "wudu_rightfoot", deTitle: "Rechter Fuß"',
    'number: 11, image: "wudu_leftfoot", deTitle: "Linker Fuß"',
    'imageKey: "salam_right",\n                deTitle: "Salām – zuerst rechts"',
    'imageKey: "salam_left",\n                deTitle: "Salām – danach links"',
    'let isRight = side == .right',
    'imageName: "\\(prefix)_\\(isRight ? "salam_right" : "salam_left")"',
    'private func salamDirection(number: String, direction: String, imageName: String, instruction: String)',
):
    if token not in guide:
        fail(f"standalone illustration regression: missing {token}")

for obsolete in (
    'case 7: armVisual(mirrored: false)',
    'case 8: armVisual(mirrored: true)',
    'case 12: footVisual(mirrored: false)',
    'case 13: footVisual(mirrored: true)',
):
    if obsolete in guide:
        fail(f"obsolete generated illustration fallback returned: {obsolete}")

if 'arrow: isRight ? "arrow.right" : "arrow.left"' in guide or 'Image(systemName: arrow)' in guide:
    fail("Salam direction arrow regression: approved female steps 17/18 must not show decorative arrows")

if '.scaleEffect(x: key == "wudu_leftfoot" ? -1 : 1, y: 1)' in guide:
    fail("Wudu left/right foot assets must not be mirrored in code")

for token in (
    'SalahFeatureIcon(kind: guideFeatureKind(for: icon))',
    'private func guideFeatureKind(for symbol: String) -> String',
    'return "wudu"',
    'return "quran_audio"',
    'return "list"',
    'return "info"',
):
    if token not in guide:
        fail(f"Guide content icon regression: missing {token}")

# 5a) Prayer/Wudu step navigation must never strand the viewport outside newly rendered content.
for token in (
    'ScrollView {\n                VStack(spacing: 14) {\n                    Color.clear.frame(height: 1).id("prayer-step-top")',
    'ScrollView {\n                VStack(spacing: 14) {\n                    Color.clear.frame(height: 1).id("wudu-step-top")',
    'private func scrollPrayerGuide(_ proxy: ScrollViewProxy, to target: String)',
    'private func scrollWuduGuide(_ proxy: ScrollViewProxy, to target: String)',
    'transaction.disablesAnimations = true',
):
    if token not in guide:
        fail(f"stable Prayer/Wudu navigation regression: missing {token}")

for forbidden in (
    'LazyVStack(spacing: 14) {\n                    Color.clear.frame(height: 1).id("prayer-step-top")',
    'LazyVStack(spacing: 14) {\n                    Color.clear.frame(height: 1).id("wudu-step-top")',
    'withAnimation(.easeInOut(duration: 0.2)) {\n                    proxy.scrollTo("prayer-step-content-top"',
    'withAnimation(.easeInOut(duration: 0.2)) {\n                    proxy.scrollTo("wudu-step-content-top"',
):
    if forbidden in guide:
        fail(f"blank step-navigation regression returned: {forbidden}")

# White action labels must stay on the brand-stable dark surface in both appearances.
for token in (
    'index == safePrayerStepIndex ? SalahTheme.navigationTeal : SalahTheme.softTeal',
    'index == safeCurrentStepIndex ? SalahTheme.navigationTeal : SalahTheme.softTeal',
    '.tint(SalahTheme.navigationTeal)',
):
    if token not in guide:
        fail(f"Prayer/Wudu appearance contrast regression: missing {token}")

for name in (
    "B78-DE-Dark-Home.png",
    "B78-DE-Dark-Quran.png",
    "B78-DE-Dark-Dhikr.png",
    "B78-DE-Dark-Namaz.png",
    "B78-DE-Dark-PrayerTimes.png",
    "B78-DE-Dark-PrayerHowTo.png",
    "B78-DE-Dark-MalePrayerStep10.png",
    "B78-DE-Dark-FemalePrayerHowTo.png",
    "B78-DE-Dark-Wudu.png",
    "B78-DE-Dark-WuduHead.png",
):
    if name not in capture:
        fail(f"light/dark visual QA coverage missing: {name}")

# 5a.1) Prayer learning hero keeps male/female choices equally visible and language switching separate.
for token in (
    'audiencePreviewCard(\n                    .male',
    'audiencePreviewCard(\n                    .female',
    'Text(settings.t("Wähle deine Anleitung", "Rehberini seç"))',
    'Text(settings.t("2 Rakʿāt Schritt für Schritt", "2 rekât adım adım"))',
    'SalahFeatureIcon(kind: "language")',
    '.accessibilityLabel(settings.t("Sprache wechseln", "Dili değiştir"))',
):
    if token not in guide:
        fail(f"prayer learning selector regression: missing {token}")

for token in (
    'Niyet ettim Allah rızası için bugünkü öğle namazının farzını kılmaya.',
    'SalahFeatureIconLabel(title: settings.t("Bildanleitung folgt bald", "Görsel anlatım yakında"), kind: "prayer")',
    '2-Rakʿāt-Bildanleitung für Mann/Frau öffnen',
):
    if token not in guide:
        fail(f"prayer guidance completeness regression: missing {token}")

for forbidden in (
    'HanafiPrayerPlanView',
    'Rak\'a einfach verstehen',
    'PDF',
    'KI-Stimme',
    'yapay zekâ sesi',
):
    if forbidden in guide:
        fail(f"internal/unfinished prayer guidance wording regression: found {forbidden}")

# 5a.2) Learning/content row icons must use standalone SalahPath artwork only.
for token in (
    'SalahFeatureIcon(kind: guideFeatureKind(for: icon))',
    '.frame(width: 31, height: 31)',
    'private func guideFeatureKind(for symbol: String) -> String',
):
    if token not in guide:
        fail(f"premium learning-row icon regression: missing {token}")

for forbidden in (
    'if let kind = guideFeatureKind(for: icon)',
    'Image(systemName: icon)\n                        .font(.system(size: 15, weight: .semibold))',
):
    if forbidden in guide:
        fail(f"premium learning-row icon regression: generic decorative fallback returned: {forbidden}")

# 5b) Nearby mosque filtering must reject substring false positives.
root_tab_source = read("SalahZeit/Views/RootTabView.swift")
for token in (
    'components(separatedBy: CharacterSet.alphanumerics.inverted)',
    'let tokenSignals: Set<String>',
    'if !tokens.isDisjoint(with: tokenSignals)',
    'let phraseSignals = [',
):
    if token not in root_tab_source:
        fail(f"nearby mosque token-filter regression: missing {token}")

if 'searchable.contains("cami")' in root_tab_source:
    fail('nearby mosque substring regression: "cami" must be a whole token')

for token in (
    '@Published var searchFailed = false',
    'searchFailed = mapItems.isEmpty && successfulSearchCount == 0 && lastSearchError != nil',
    'Apple Karten konnte die Moscheensuche gerade nicht laden.',
    'Apple Haritalar cami aramasını şu anda yükleyemedi.',
):
    if token not in root_tab_source:
        fail(f"nearby mosque localized-error regression: missing {token}")

if 'lastSearchError.localizedDescription' in root_tab_source:
    fail("nearby mosque raw system error leaked into localized UI")

for token in (
    'Map(position: $mapPosition)',
    'MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeDefault',
    'locationManager.requestDeviceLocationSnapshot()',
    'maximumDistance: CLLocationDistance = 50_000',
):
    if token not in root_tab_source:
        fail(f"nearby mosque map/route regression: missing {token}")


# 6) Navigation/discovery icons stay in the same standalone SalahPath system.
home = (ROOT / "SalahZeit/Views/HomeView.swift").read_text(encoding="utf-8")
root_tabs = (ROOT / "SalahZeit/Views/RootTabView.swift").read_text(encoding="utf-8")
app_source = (ROOT / "SalahZeit/SalahZeitApp.swift").read_text(encoding="utf-8")
for token in (
    'SalahFeatureIcon(kind: glyphKind)',
    'SalahFeatureIcon(kind: icon)',
    'icon: "times"',
    'icon: "checkmark"',
    'icon: "quran"',
    'case "quran_audio":',
    'case "bookmarks":',
    'LinearGradient(',
):
    if token not in home:
        fail(f"standalone dashboard icon regression: missing {token}")

for token in (
    'init(initialSelection: Int = 0)',
    '_selection = State(initialValue: min(max(initialSelection, 0), 4))',
    '.frame(width: selection == index ? 24 : 22, height: selection == index ? 24 : 22)',
):
    if token not in root_tabs:
        fail(f"real tab shell / premium bottom bar regression: missing {token}")

if '.fill(selection == index ? SalahTheme.softTeal.opacity(0.72) : Color.clear)' in root_tabs:
    fail("redundant circular tab icon badge returned")

for token in (
    'case "home":\n            RootTabView(initialSelection: 0)',
    'case "quran":\n            RootTabView(initialSelection: 1)',
    'case "namaz":\n            RootTabView(initialSelection: 2)',
    'case "more":\n            RootTabView(initialSelection: 3)',
    'case "settings":\n            RootTabView(initialSelection: 4)',
):
    if token not in app_source:
        fail(f"core UI QA no longer uses the real tab shell: missing {token}")

for token in (
    'subtitle: settings.t("Qibla", "Kıble")',
    'Text(settings.t("Qibla", "Kıble"))',
):
    if token not in home:
        fail(f"Turkish Qibla label regression: missing {token}")

for token in (
    'SalahFeatureIcon(kind: discoverDashboardGlyphKind(for: symbol))',
    'private func discoverDashboardGlyphKind(for symbol: String) -> String',
    'return "prayer"',
    'return "wudu"',
    'return "quran"',
    'return "qibla"',
    'return "info"',
    'SalahFeatureIcon(kind: selection == index ? item.active : item.inactive)',
    '("home_active", "home_inactive", settings.t("Start", "Ana Sayfa"))',
    '("quran_active", "quran_inactive", settings.t("Quran", "Kur\'an"))',
    '("prayer_active", "prayer_inactive", settings.t("Gebet", "Namaz"))',
    '("discover", "discover", settings.t("Entdecken", "Keşfet"))',
    '("profile", "profile", settings.t("Profil", "Profil"))',
    'SalahFeatureIcon(kind: "discover")',
    'GlobalAudioMiniPlayer(audio: audio)',
    'private struct GlobalAudioMiniPlayer: View',
    'audio.isPlaying ? audio.pause() : audio.resume()',
):
    if token not in root_tabs:
        fail(f"standalone tab/discover icon regression: missing {token}")

for forbidden in (
    'if let glyphKind = discoverDashboardGlyphKind(for: symbol)',
    'if let glyphKind = discoverDashboardGlyphKind(for: icon)',
):
    if forbidden in root_tabs:
        fail(f"standalone tab/discover icon regression: decorative SF fallback returned: {forbidden}")

for token in (
    'struct SalahFeatureIcon: View',
    'private var standaloneAssetName: String?',
    'case "home", "start", "home_active", "home_inactive":',
    'return "feature_home"',
    'case "prayer", "prayer_active", "prayer_inactive":',
    'return "feature_prayer"',
    'case "wudu", "wudu_active", "wudu_inactive":',
    'return "feature_wudu"',
    'case "quran", "quran_active", "quran_inactive":',
    'return "feature_quran"',
    'return "feature_discover"',
    'return "feature_qibla"',
    'return "feature_profile"',
    'return "home_mosque"',
    'private var systemSymbolName: String',
    'case "videos": return "play.rectangle.fill"',
    'case "mute": return "speaker.slash.fill"',
    'case "community", "forum": return "person.3.fill"',
    'case "sparkles": return "sparkles"',
    'return "feature_mute"',
    'return "feature_community"',
    'return "feature_sparkles"',
    'case "map": return "map.fill"',
    'case "history": return "clock.arrow.circlepath"',
    'case "hadith": return "text.quote"',
    'if let standaloneAssetName, UIImage(named: standaloneAssetName) != nil',
):
    if token not in root_tabs:
        fail(f"transparent standalone icon routing regression: missing {token}")

for forbidden in (
    'UIImage(named: "SalahFeatureSheet")',
    'cgImage.cropping',
    'croppedUIImage',
    'salahFeatureIndex(',
):
    if forbidden in root_tabs:
        fail(f"atlas-cut icon rendering returned: {forbidden}")

for token in (
    'SalahFeatureIcon(kind: discoverDashboardGlyphKind(for: symbol))',
    '.frame(width: size * 0.78, height: size * 0.78)',
    '.frame(width: 23, height: 23)',
    'default:\n            return "info"',
):
    if token not in root_tabs:
        fail(f"transparent premium tile rendering regression: missing {token}")

for forbidden in (
    'SF Symbols are the fallback only.',
    'Premium artwork is already a finished transparent asset.',
    'Image(systemName: symbol)\n                    .symbolRenderingMode(.hierarchical)',
):
    if forbidden in root_tabs:
        fail(f"transparent premium tile rendering regression: legacy decorative fallback returned: {forbidden}")

for forbidden in (
    '.background(SalahTheme.softTeal, in: Circle())\n            .overlay { Circle().stroke(SalahTheme.gold.opacity(0.55), lineWidth: 0.8) }',
):
    if forbidden in root_tabs:
        fail("discover section icon badge returned")

for token in (
    '.frame(width: 25, height: 25)',
    'Küçük adımlar büyük değişimler getirir.',
):
    if token not in home:
        fail(f"home premium polish regression: missing {token}")

premium_png_icons = (
    "home", "prayer", "wudu", "quran", "discover", "profile", "qibla", "times",
    "dhikr", "reminder", "settings", "quran_audio", "bookmarks", "calendar",
    "checkmark", "language", "info", "more", "moon", "list",
)
for icon_name in premium_png_icons:
    contents_path = ROOT / f"SalahZeit/Assets.xcassets/feature_{icon_name}.imageset/Contents.json"
    contents = contents_path.read_text(encoding="utf-8")
    required_filename = f'"filename": "feature_{icon_name}.png"'
    if required_filename not in contents:
        fail(f"generated premium icon regression: {icon_name} is not routed to its PNG asset")
    if f'"filename": "feature_{icon_name}.svg"' in contents:
        fail(f"legacy SVG icon returned as active asset: {icon_name}")
    legacy_svg_path = ROOT / f"SalahZeit/Assets.xcassets/feature_{icon_name}.imageset/feature_{icon_name}.svg"
    if legacy_svg_path.exists():
        fail(f"legacy SVG sidecar returned beside premium PNG asset: {icon_name}")

mosque_contents = (ROOT / "SalahZeit/Assets.xcassets/home_mosque.imageset/Contents.json").read_text(encoding="utf-8")
if '"filename": "home_mosque.png"' not in mosque_contents:
    fail("generated premium mosque icon regression")
if (ROOT / "SalahZeit/Assets.xcassets/home_mosque.imageset/home_mosque.svg").exists():
    fail("legacy home_mosque SVG sidecar returned")

for token in (
    'case "play.square.stack.fill":\n            return "quran_audio"',
    'case "hands.sparkles.fill":\n            return "duas"',
    'case "circle.grid.cross.fill":\n            return "dhikr"',
    'case "sparkles":\n            return "sparkles"',
    'case "location.north.circle.fill", "map.fill":\n            return "qibla"',
    'case "clock.arrow.circlepath":\n            return "times"',
    'case "building.columns.fill":\n            return "mosques"',
    'case "text.quote":\n            return "info"',
    'case "moon.stars.fill":\n            return "moon"',
    'case "slider.horizontal.3":\n            return "settings"',
):
    if token not in root_tabs:
        fail(f"semantic icon routing regression: missing {token}")

# Nine standalone v2 vectors must remain background-free and must never fall back to cropped atlas artwork.
standalone_svg_icons = ("fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha", "mute", "community", "sparkles")
for icon_name in standalone_svg_icons:
    svg_path = ROOT / f"SalahZeit/Assets.xcassets/feature_{icon_name}.imageset/feature_{icon_name}.svg"
    svg = svg_path.read_text(encoding="utf-8")
    if f"SalahPath standalone v2 {icon_name}" not in svg:
        fail(f"standalone v2 icon regression: {icon_name} marker missing")
    if "<rect" in svg:
        fail(f"standalone v2 icon regression: {icon_name} must stay background-free")

for forbidden in (
    'prefersTransparentArtwork',
    '.brightness(colorScheme == .dark',
):
    if forbidden in root_tabs or forbidden in home:
        fail(f"theme-specific icon artwork regression returned: {forbidden}")

for token in (
    'SalahFeatureIcon(kind: today.map { brandHeaderFeatureKind(today: $0) } ?? "sunrise")',
    'private func brandHeaderFeatureKind(today: PrayerDay) -> String',
    'return "fajr"',
    'return "sunrise"',
    'return "dhuhr"',
    'return "asr"',
    'return "maghrib"',
    'return "isha"',
    'SalahFeatureIcon(kind: salahPrayerFeatureKind(for: prayer.kind))',
):
    if token not in home:
        fail(f"time-aware SalahPath prayer artwork regression: missing {token}")

for forbidden in (
    'Image(systemName: today.map { brandHeaderSymbolName',
    'private func brandHeaderSymbolName(today: PrayerDay)',
    'SalahFeatureIcon(kind: today.map { brandHeaderIconKind',
    'private func brandHeaderIconKind(today: PrayerDay)',
):
    if forbidden in home:
        fail(f"legacy home header artwork returned: {forbidden}")

capture_workflow = read(".github/workflows/capture-ui.yml")

# Screenshot QA must use one deterministic clock for both the iOS status bar and HomeView.
# Otherwise a screenshot can visibly say 09:41 while time-aware prayer artwork renders for
# the runner's real wall-clock time.
for token in (
    'private static var initialNow: Date',
    'environment["SALAH_QA_NOW"]',
):
    if token not in home:
        fail(f"deterministic home screenshot clock regression: missing {token}")
for token in (
    'SIMCTL_CHILD_SALAH_QA_NOW=2026-10-02T06:41:00Z',
):
    if token not in capture_workflow:
        fail(f"deterministic screenshot launch clock regression: missing {token}")

for token in (
    'Invalid/blank screenshot for $SCREEN; rebooting simulator before the retry.',
    'xcrun simctl terminate "$SIM_UDID" com.achmed06.salahpath || true',
    'xcrun simctl shutdown "$SIM_UDID" || true',
    'run_timeout 240 xcrun simctl bootstatus "$SIM_UDID" -b',
    'sleep 10',
):
    if token not in capture_workflow:
        fail(f"blank screenshot retry regression: missing {token}")
for token in (
    'appAppearance system',
    'simctl ui "$SIM_UDID" appearance light',
    'simctl ui "$SIM_UDID" appearance dark',
    'Dark-mode QA failed:',
    'cmp -s "$LIGHT" "$DARK"',
    'SalahPath-v3.62-B78-DE-Dark-Home.png',
    'SalahPath-v3.62-B78-DE-Dark-More.png',
    'SalahPath-v3.62-B78-DE-Dark-Qibla.png',
    'SalahPath-v3.62-B78-DE-Settings.png',
    'SalahPath-v3.62-B78-DE-Dark-Settings.png',
):
    if token not in capture_workflow:
        fail(f"dark-mode icon screenshot regression: missing {token}")

for legacy_prefix in ("sp_icon_", "ref_dash_"):
    if legacy_prefix in home or legacy_prefix in root_tabs:
        fail(f"legacy icon asset reference returned: {legacy_prefix}")

# 6a.1) Daily dua source labels must not expose both languages at once.
for token in (
    'func localizedSource(_ language: AppLanguage) -> String',
    'with: language == .german ? "Auszug" : "alıntı"',
    'title: dua.localizedSource(settings.language)',
    'kind: "info"',
    'context: dua.localizedSource(settings.language)',
):
    if token not in home:
        fail(f"daily dua source localization regression: missing {token}")

for forbidden in (
    'Text(dua.source)',
    'Label(dua.source, systemImage: "checkmark.seal.fill")',
    'Label(dua.localizedSource(settings.language), systemImage: "checkmark.seal.fill")',
    'context: dua.source',
):
    if forbidden in home:
        fail(f"bilingual or generic-icon daily dua source rendering returned: {forbidden}")

# 6a.2) Audio runtime errors must follow the selected app language.
for token in (
    'private func salahLocalizedAudioText(_ german: String, _ turkish: String) -> String',
    'UserDefaults.standard.string(forKey: "appLanguage")',
    'salahLocalizedAudioText("Audio nicht verfügbar.", "Ses mevcut değil.")',
    'salahLocalizedAudioText("Audio konnte nicht geladen werden.", "Ses yüklenemedi.")',
    'salahLocalizedAudioText("Audio-Wiedergabe fehlgeschlagen.", "Ses oynatılamadı.")',
    'salahLocalizedAudioText("Audio lädt zu lange. Der nächste Abschnitt wird versucht.", "Ses çok uzun yükleniyor. Sonraki bölüm deneniyor.")',
    'salahLocalizedAudioText("Nächste Sura konnte nicht geladen werden.", "Sonraki sûre yüklenemedi.")',
    'salahLocalizedAudioText("Quran · automatisch weiter", "Kur\'an · otomatik devam")',
):
    if token not in guide:
        fail(f"audio runtime localization regression: missing {token}")

for forbidden in (
    'Audio nicht verfügbar / Ses mevcut değil.',
    'Audio konnte nicht geladen werden / Ses yüklenemedi.',
    'Audio-Wiedergabe fehlgeschlagen / Ses oynatılamadı.',
    'Audio lädt zu lange. Der nächste Abschnitt wird versucht / Ses çok uzun yükleniyor.',
    'Nächste Sura konnte nicht geladen werden / Sonraki sûre yüklenemedi.',
):
    if forbidden in guide:
        fail(f"bilingual audio runtime text returned: {forbidden}")

# 6a.3) Quran/adhkar source labels must not mix German and Turkish.
for token in (
    'func localizedReference(_ language: AppLanguage) -> String',
    'Text(item.localizedReference(settings.language))',
    'func localizedSource(_ language: AppLanguage) -> String',
    'Text(item.localizedSource(settings.language))',
):
    if token not in guide:
        fail(f"Quran/adhkar source localization regression: missing {token}")

# 6b) Global audio accessibility must follow the selected app language.
for token in (
    '@EnvironmentObject private var settings: SettingsStore',
    'settings.t("Audio-Laden abbrechen", "Ses yüklemeyi iptal et")',
    'settings.t("Audio pausieren", "Sesi duraklat")',
    'settings.t("Audio fortsetzen", "Sesi sürdür")',
    'settings.t("Audio stoppen", "Sesi durdur")',
    'settings.t("Vorheriges Audio", "Önceki ses")',
    'settings.t("Nächstes Audio", "Sonraki ses")',
):
    if token not in root_tabs:
        fail(f"audio accessibility localization regression: missing {token}")

# 6c) Denied notification permission must offer a direct iOS Settings path.
settings_source = read("SalahZeit/Views/SettingsView.swift")
for token in (
    '@State private var notificationAuthorizationDenied = false',
    'notificationAuthorizationDenied = diagnostics.authorizationStatus == .denied',
    'iPhone-Benachrichtigungseinstellungen öffnen',
    'iPhone bildirim ayarlarını aç',
    'UIApplication.openSettingsURLString',
):
    if token not in settings_source:
        fail(f"notification settings recovery regression: missing {token}")

# 6d) Visible Quran load failures must remain localized.
guide_source = read("SalahZeit/Views/GuideView.swift")
for token in (
    'Quran-Daten konnten gerade nicht geladen werden.',
    "Kur'an verileri şu anda yüklenemedi.",
    'Diese Quran-Seite konnte gerade nicht geladen werden.',
    "Bu Kur'an sayfası şu anda yüklenemedi.",
    'Das Quran-Verzeichnis konnte gerade nicht geladen werden.',
    "Kur'an dizini şu anda yüklenemedi.",
    'Der Quran-Inhalt konnte gerade nicht geladen werden.',
    "Kur'an içeriği şu anda yüklenemedi.",
    'Die Juz-Daten konnten gerade nicht geladen werden. Bitte versuche es erneut.',
    "Cüz verileri şu anda yüklenemedi. Lütfen tekrar dene.",
    'Die Quran-Favoriten konnten gerade nicht geladen werden. Bitte versuche es erneut.',
    "Kur'an favorileri şu anda yüklenemedi. Lütfen tekrar dene.",
    'Quran-Audio konnte nicht geladen werden. Bitte versuche es erneut.',
    "Kur'an sesi yüklenemedi. Lütfen tekrar dene.",
):
    if token not in guide_source:
        fail(f"Quran visible-error localization regression: missing {token}")

if 'description: Text(error)' in guide_source:
    fail("Quran raw system error leaked into visible UI")

if 'audio.lastError = error.localizedDescription' in guide_source:
    fail("Quran raw audio system error leaked into visible UI")

if 'let error = store.error' in guide_source:
    fail("Quran visible-error regression: unused raw store error binding returned")

# 6e) Visible location errors must follow the selected app language.
location_source = read("SalahZeit/Services/LocationManager.swift")
for token in (
    'func localizedLastError(_ language: AppLanguage) -> String?',
    'Konum erişimi kapalı. iPhone ayarlarından konum erişimini etkinleştir.',
    'Lütfen konum, şehir veya posta kodu gir.',
    'Konum bulunamadı.',
    'Konum bulunamadı. Lütfen girişini kontrol et.',
    'Güncel konum geçici olarak kullanılamıyor. Lütfen tekrar dene.',
    'Konum güncellenemedi. Lütfen tekrar dene.',
):
    if token not in location_source:
        fail(f"location error localization regression: missing {token}")

for path in (
    "SalahZeit/SalahZeitApp.swift",
    "SalahZeit/Views/HomeView.swift",
    "SalahZeit/Views/SettingsView.swift",
):
    source = read(path)
    if "locationManager.lastError" in source and "localizedLastError" not in source:
        fail(f"raw location error leaked into visible UI: {path}")

# 7) Onboarding hit targets, persistent audio and Now Playing must stay intact.
project = read("SalahZeit.xcodeproj/project.pbxproj")
notification_manager = read("SalahZeit/Services/NotificationManager.swift")
settings_view = read("SalahZeit/Views/SettingsView.swift")

for token in (
    'SalahFeatureIcon(kind: "profile")',
    '.frame(width: 46, height: 46)',
):
    if token not in settings_view:
        fail(f"settings premium profile artwork regression: missing {token}")
if 'Image(systemName: "person.crop.circle.fill")' in settings_view:
    fail("legacy settings profile system icon returned")

for token in (
    '.frame(height: 48)',
    '.contentShape(Rectangle())',
    'Text(settings.t("Weiter", "İleri"))',
):
    if token not in app:
        fail(f"onboarding hit-target regression: missing {token}")

for token in (
    'func cancelPendingLocationIntent()',
    'searchGeocoder.cancelGeocode()',
):
    if token not in location_manager:
        fail(f"onboarding location-cancellation regression: missing {token}")

for token in (
    'locationManager.cancelPendingLocationIntent()',
    'guard step == 2 else {',
):
    if token not in app:
        fail(f"onboarding stale-location regression: missing {token}")

if app.count('locationManager.cancelPendingLocationIntent()') < 2:
    fail("onboarding stale-location regression: back/skip no longer both cancel pending lookup")

for token in (
    'import MediaPlayer',
    'static let shared = RemoteAudioPlayer()',
    'MPNowPlayingInfoCenter.default().nowPlayingInfo',
    'MPRemoteCommandCenter.shared()',
    'func setPrayerContext(_ text: String?)',
    'MPMediaItemPropertyArtwork',
    '@Published private(set) var displayTitle = "SalahPath Audio"',
    '@Published private(set) var displaySubtitle = "SalahPath"',
    'requestContinuationIfAvailable()',
    'queueContinuationDelegate != nil && !continuationRequestInFlight',
    'Array(urls.dropFirst(startIndex))',
    'Array(resolvedAudioURLs.dropFirst(index))',
    'final class QuranContinuousPlaybackCoordinator: RemoteAudioPlayerQueueContinuation',
    'func appendContinuation(',
    'queueContinuationDidReachFinalSurah',
    'QuranContinuousPlaybackCoordinator.shared.play(',
):
    if token not in guide:
        fail(f"background/continuous audio regression: missing {token}")

if 'INFOPLIST_KEY_UIBackgroundModes = audio;' not in project:
    fail("background audio mode was removed")

for token in (
    'static func bismillahURL(reciter: QuranReciter) -> URL?',
    'static func playbackQueue(',
    'guard startAyah == 1, surah != 1, surah != 9,',
    'return [basmalah] + urls',
):
    if token not in guide:
        fail(f"Quran Basmalah playback regression: missing {token}")

if guide.count('isFirstAyahBasmalahActive') < 2:
    fail("Quran Basmalah playback-toggle regression")

settings_model = read("SalahZeit/Models/AppSettings.swift")
for forbidden in (
    'everyayah.com',
    'everyAyahURLs',
    'everyAyahFolder',
):
    if forbidden in guide or forbidden in settings_model:
        fail(f"unaudited Quran audio provider regression: found {forbidden}")

prayer_engine = read("SalahZeit/Services/PrayerEngine.swift")
for token in (
    'func upcomingPrayers(',
    '.filter { $0.kind != .sunrise && $0.date > now }',
):
    if token not in prayer_engine:
        fail(f"lock-screen prayer-time regression: missing {token}")

for token in (
    '@ObservedObject private var audio = RemoteAudioPlayer.shared',
    'let audioSurah: Int',
    'let audioAyah: Int',
    'QuranAudioResolver.urls(surah: dua.audioSurah',
    'updateNowPlayingPrayerContext()',
    'engine.upcomingPrayers(',
    'settings.t("Gebetszeiten", "Namaz vakitleri")',
    'toggleDailyDuaAudio(dua)',
    'speaker.wave.2.fill',
):
    if token not in home:
        fail(f"daily dua / prayer Now Playing regression: missing {token}")

for token in (
    'func playAdhanPreviewDirect(fajr: Bool) -> Bool',
    'AVAudioPlayer(contentsOf: url)',
    'scheduleAdhanPreview(settings: SettingsStore, fajr: Bool)',
    'UNUserNotificationCenterDelegate',
    'willPresent notification: UNNotification',
    '[.banner, .list, .sound]',
    'installNotificationSoundsIfNeeded()',
    '.appendingPathComponent("Sounds", isDirectory: true)',
):
    if token not in notification_manager:
        fail(f"Adhan preview regression: missing {token}")

for token in (
    'Standard-Gebetsruf wird direkt abgespielt.',
    'iOS-Mitteilung testen',
):
    if token not in settings_view:
        fail(f"notification test UI regression: missing {token}")

for token in (
    'settings.notificationsEnabled = false',
    'after.authorizationStatus == .denied',
    'iOS-Benachrichtigungen sind ausgeschaltet.',
    'iOS bildirimleri kapalı.',
):
    if token not in settings_view:
        fail(f"notification permission-sync regression: missing {token}")

# Religious-content audit: keep school-specific rulings and exact qualification wording.
for token in (
    'Hanafi: Wajib für Jumuʿah-Pflichtige · gemeinschaftlich',
    'die Eid-Khutbah ist Sunnah und folgt nach dem Gebet.',
    'Die Khutbah vor dem Gebet ist eine Gültigkeitsbedingung.',
    'Hat die Khutbah begonnen, soll keine Sunnah/Nafila mehr begonnen werden',
    'Dritter Takbir ebenfalls ohne erneutes Händeheben',
    'Samenabgang mit sexueller Erregung bzw. Orgasmus',
    'etwas, das zur Erdsubstanz zählt',
    'Diyanet nennt als Grenze 10 Minuten davor.',
    'Für Qada, Kaffarah und zeitlich nicht festgelegte Gelübdefasten muss die Absicht spätestens bis Imsak vorliegen.',
    'Hisn al-Muslim 78 · Morgen-/Abendfassung; Wortlautvarianten überliefert',
    'Rituelle Reinheit beim Tawaf ist nicht bloß eine Empfehlung',
    'Menstruation oder Nifas verhindern den Eintritt in den Ihram nicht.',
    '80,18 g 24-karätigem Gold',
    'nicht pauschal die gesamte Restschuld abgezogen',
    "Fitra ist nicht einfach 'kleine Zakat'",
    'unnötiges Verschieben über den Eid hinaus ist makruh',
    'Nach Hanafi/Diyanet ist Udhiyah',
    'endet nach Hanafi mit Sonnenuntergang am 3. Eid-Tag',
    'Kamel 5, Rind/Büffel 2, Schaf/Ziege 1 Mondjahr',
    'Geld nur zu spenden ersetzt das Udhiyah-Opfer nicht.',
    'genau sieben Bedürftige zu verteilen',
    'zehn Bedürftige speisen oder kleiden',
    'Haram işlemeye veya farz/vacibi terk etmeye dair yemin yerine getirilmez',
    'Nikah ist ein Vertrag mit freier Zustimmung',
    'Mahr ist ein Recht der Frau',
    'Bei Talak/Scheidung niemals aus einem verkürzten Satz automatisch entscheiden',
    'höchstens ein Drittel des nach Kosten und Schulden verbleibenden Nachlasses',
    'Wasiyyah zugunsten eines ohnehin erbberechtigten Erben',
    'lässt sich aus einer Kurzbeschreibung keine verbindliche individuelle Erbverteilung ableiten',
    'Text(settings.t("Morgen", "Sabah")).tag(0)',
    'Text(settings.t("Abend", "Akşam")).tag(1)',
    'category == 0 ? "morning" : "evening"',
    'source: "Hisn al-Muslim 86"',
    'source: "Hisn al-Muslim 87"',
    'Freiwilliger Geschlechtsverkehr während eines gültig begonnenen Ramadan-Fastens',
    'In der schafiitischen Einordnung kann bei Sorge nur um das Kind zusätzlich Fidya erforderlich sein.',
    'Tashrīq-Takbīre sind für Frauen und Männer wājib',
    'insgesamt 23 Gebetszeiten',
    'Fasten an diesen vier Kurban-/Tashrīq-Tagen ist tahrīman makrūh',
    'Riba ist im Quran verboten.',
    'klassische verzinste Kredite und verzinste Termineinlagen',
    'etwas, das zur Erdsubstanz zählt, die vorgeschriebenen Wischhandlungen',
    'wegen einer normalen Reise nicht einfach als echtes Jamʿ zusammengelegt',
    'Witr ist hier nach Hanafi/Diyanet enthalten',
    'Hanefî mezhebinde vitir vaciptir ve vaktinde kılınmayan vitir kaza edilir',
):
    if token not in guide:
        fail(f"religious-content audit regression: missing {token}")

for forbidden in (
    'Text(settings.t("Täglich", "Günlük")).tag(2)',
    'Text(settings.t("Speziell", "Özel")).tag(3)',
    'case 2: return "daily"',
    'default: return "special"',
    'Opferpflicht bzw. Opfer-Sunnah',
    'erdähnlicher Oberfläche',
):
    if forbidden in guide:
        fail(f"religious-content audit regression: duplicate adhkar session returned: {forbidden}")

for prayer_catalog_id in ('tahajjud', 'duha', 'istikhara', 'tilawah_sajdah'):
    if guide.count(f'id: "{prayer_catalog_id}"') != 1:
        fail(f"religious-content audit regression: prayer catalogue ID must be unique: {prayer_catalog_id}")

# Visual/copy consistency audit: instructional and content cards use SalahPath artwork,
# while SF Symbols remain reserved for native controls, states and status feedback.
for token in (
    'private struct TutorialSectionHeader: View',
    'iconKind: "prayer"',
    'iconKind: "duas"',
    'SalahFeatureIcon(kind: "calendar")',
    'SalahFeatureIcon(kind: lesson.icon)',
    'SalahFeatureIcon(kind: salahPrayerFeatureKind(for: prayer.kind))',
    'SalahFeatureIcon(kind: settingsFeatureKind(for: icon))',
):
    if token not in guide + home + settings_view:
        fail(f"visual consistency regression: missing {token}")

for forbidden in (
    'Label(settings.t("WAS MACHE ICH?", "NE YAPACAĞIM?"), systemImage: "figure.walk")',
    'Label(settings.t("WAS SAGE ICH?", "NE SÖYLÜYORUM?"), systemImage: "text.bubble.fill")',
    'deLabel: "Rechts und anschließend links"',
    'deNote: "Den Satz einmal beim Drehen nach rechts',
    'deNote: "In der ersten Rakʿah nach dem Eröffnungstakbir."',
    'deNote: "In der ersten Rakʿah vor der Fātiha."',
    'Image(systemName: lesson.icon)',
    'systemImage: topic.icon',
    'Image(systemName: item.event.symbol)',
    'systemImage: event.symbol',
    'Image(systemName: prayer.kind.systemImage)',
    'Image(systemName: task.2)',
):
    if forbidden in guide + home:
        fail(f"visual/copy consistency regression: legacy decorative pattern returned: {forbidden}")

for forbidden in (
    'Image(systemName: settings.prayerAudience == audience ? "person.fill" : "person.fill")',
    'Image(systemName: "globe")',
):
    if forbidden in app + settings_view + guide:
        fail(f"visual consistency regression: generic profile/language icon returned: {forbidden}")

if 'systemImage: "building.columns"' in root_tabs:
    fail("visual consistency regression: generic mosque empty-state icon returned")

for forbidden in (
    "LiveContainer",
    "wie in der PDF",
    "wie in PDF",
    "KI-generiert",
    "AI-generated",
    "künstliche Intelligenz",
):
    if forbidden in app + guide + home + settings_view + root_tabs:
        fail(f"release-copy regression: internal/meta wording leaked into UI source: {forbidden}")

if 'Bildanleitung folgt bald' not in guide or 'Görsel anlatım yakında' not in guide:
    fail("unfinished prayer-guide disclosure regression: translated coming-soon notice missing")

print("Build 78 regression guard: OK")
