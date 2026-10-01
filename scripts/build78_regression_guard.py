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
if 'scripts/build78_regression_guard\\.py' not in capture:
    fail("final guard changes no longer force release UI coverage")

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

if capture.count("B78-DE-PrayerSalamLeft.png") < 2:
    fail("male final Salam must be captured in prayer and full UI modes")

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

# 5) Prayer/Wudu illustration system must stay unified and direction-safe.
if '.replacingOccurrences(of: "male_", with: "")' in guide:
    fail("female prayer pose routing regression: male_ substring stripping breaks female_ assets")

for token in (
    'Image(key)',
    'Image(assetName)',
    'number: 7, image: "wudu_rightarm", deTitle: "Rechter Arm"',
    'number: 8, image: "wudu_leftarm", deTitle: "Linker Arm"',
    'number: 12, image: "wudu_rightfoot", deTitle: "Rechter Fuß"',
    'number: 13, image: "wudu_leftfoot", deTitle: "Linker Fuß"',
    'imageKey: "salam_right",\n                deTitle: "Salām – zuerst rechts"',
    'imageKey: "salam_left",\n                deTitle: "Salām – danach links"',
    'let isRight = side == .right',
    'imageName: "\\(prefix)_\\(isRight ? "salam_right" : "salam_left")"',
    'arrow: isRight ? "arrow.right" : "arrow.left"',
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

if '.scaleEffect(x: key == "wudu_leftfoot" ? -1 : 1, y: 1)' not in guide:
    fail("Wudu left-foot mirror regression")

for token in (
    'SalahFeatureIcon(kind: kind)',
    'private func guideFeatureKind(for symbol: String) -> String?',
    'return "wudu"',
    'return "quran_audio"',
    'return "list"',
):
    if token not in guide:
        fail(f"Guide content icon regression: missing {token}")

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
    'searchFailed = mapItems.isEmpty && lastSearchError != nil',
    'Apple Karten konnte die Moscheensuche gerade nicht laden.',
    'Apple Haritalar cami aramasını şu anda yükleyemedi.',
):
    if token not in root_tab_source:
        fail(f"nearby mosque localized-error regression: missing {token}")

if 'lastSearchError.localizedDescription' in root_tab_source:
    fail("nearby mosque raw system error leaked into localized UI")

# 6) Navigation/discovery icons stay in the same standalone SalahPath system.
home = (ROOT / "SalahZeit/Views/HomeView.swift").read_text(encoding="utf-8")
root_tabs = (ROOT / "SalahZeit/Views/RootTabView.swift").read_text(encoding="utf-8")
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
    'SalahFeatureIcon(kind: glyphKind)',
    'return "prayer"',
    'return "wudu"',
    'return "quran"',
    'return "qibla"',
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

for token in (
    'func salahFeatureIndex(for kind: String) -> Int?',
    'struct SalahFeatureIcon: View',
    'UIImage(named: "feature_\\(kind)")',
    'UIImage(named: "SalahFeatureSheet")',
    'case "home", "start": return 52',
    'case "prayer": return 1',
    'case "wudu": return 2',
    'case "quran": return 3',
    'case "discover": return 42',
    'case "qibla": return 42',
    'case "profile": return 9',
    'case "fajr": return 10',
    'case "maghrib": return 14',
    'case "isha": return 15',
    'case "home_active": return 52',
    'case "quran_inactive": return 59',
    'let column = index % 10',
    'let row = index / 10',
):
    if token not in root_tabs:
        fail(f"approved icon sheet routing regression: missing {token}")

for token in (
    'case "discover": return 42',
    'case "qibla": return 42',
    'case "notifications": return 17',
    'case "building.columns.fill":\n            return "mosques"',
    'case "text.quote":\n            return "hadith"',
    'case "clock.arrow.circlepath", "checklist", "pause.circle.fill":\n            return "checkmark"',
):
    if token not in root_tabs:
        fail(f"semantic icon routing regression: missing {token}")

for token in (
    '@Environment(\\.colorScheme) private var colorScheme',
    'if let croppedUIImage',
    '.brightness(colorScheme == .dark ? -0.055 : 0)',
    'Emergency fallback only if the approved sheet is unavailable.',
):
    if token not in root_tabs:
        fail(f"dark-mode canonical icon routing regression: missing {token}")

if 'prefersTransparentArtwork' in root_tabs or 'prefersTransparentArtwork' in home:
    fail("legacy dark-mode icon fallback routing returned")

for token in (
    'SalahFeatureIcon(kind: today.map { brandHeaderIconKind(today: $0) } ?? "prayer")',
    'private func brandHeaderIconKind(today: PrayerDay) -> String',
    'return "maghrib"',
    '.clipShape(Circle())',
):
    if token not in home:
        fail(f"time-aware home header icon regression: missing {token}")

capture_workflow = read(".github/workflows/capture-ui.yml")
for token in (
    'appAppearance dark',
    'SalahPath-v3.62-B78-DE-Dark-Home.png',
    'SalahPath-v3.62-B78-DE-Dark-More.png',
    'SalahPath-v3.62-B78-DE-Dark-Qibla.png',
):
    if token not in capture_workflow:
        fail(f"dark-mode icon screenshot regression: missing {token}")

for legacy_prefix in ("sp_icon_", "ref_dash_"):
    if legacy_prefix in home or legacy_prefix in root_tabs:
        fail(f"legacy icon asset reference returned: {legacy_prefix}")

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
    'Konum erişimi kapalı. SalahPath için iPhone ayarlarından etkinleştir.',
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

print("Build 78 regression guard: OK")
