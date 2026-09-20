from pathlib import Path

root = Path.cwd()

# SalahPath v3.62 FAST — make visible affordances functional and close audio UX gaps.

# ---------- Home / prayer tracking ----------
home = root / "SalahZeit" / "Views" / "HomeView.swift"
s = home.read_text(encoding="utf-8")

old = '''struct TrackerPauseView: View {
'''
new = '''struct PrayerTrackerOverviewView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var refresh = 0

    var body: some View {
        let today = Date()
        let completed = PrayerTrackerStore.completedCount(on: today)
        let streak = PrayerTrackerStore.streak(upTo: today)

        List {
            Section {
                HStack {
                    Label(settings.t("Heute", "Bugün"), systemImage: "checkmark.circle.fill")
                    Spacer()
                    Text("\\(completed)/\\(PrayerTrackerStore.requiredKinds.count)")
                        .font(.headline.monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
                }

                HStack {
                    Label(settings.t("Serie", "Seri"), systemImage: "flame.fill")
                    Spacer()
                    Text("\\(streak) \\(settings.t("Tage", "gün"))")
                        .font(.headline.monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
                }
            }

            Section(settings.t("Heutige Gebete", "Bugünkü namazlar")) {
                ForEach(PrayerTrackerStore.requiredKinds, id: \\.id) { kind in
                    let done = PrayerTrackerStore.isCompleted(kind, on: today)
                    Button {
                        _ = PrayerTrackerStore.toggle(kind, on: today)
                        refresh += 1
                    } label: {
                        HStack {
                            Text(kind.localizedName(settings.language))
                                .foregroundStyle(SalahTheme.ink)
                            Spacer()
                            Image(systemName: done ? "checkmark.circle.fill" : "circle")
                                .foregroundStyle(done ? SalahTheme.teal : .secondary)
                        }
                        .contentShape(Rectangle())
                    }
                    .buttonStyle(.plain)
                }
            }

            Section(settings.t("Tracker", "Takip")) {
                Toggle(isOn: Binding(
                    get: { PrayerTrackerStore.isPaused(today) },
                    set: { newValue in
                        if PrayerTrackerStore.isPaused(today) != newValue {
                            PrayerTrackerStore.togglePause(today)
                        }
                        refresh += 1
                    }
                )) {
                    Label(settings.t("Tracker heute pausieren", "Bugün takibi duraklat"), systemImage: "pause.circle")
                }

                Text(settings.t(
                    "Die Pause verändert nur Statistik und Streak. Sie ändert keine religiöse Pflicht.",
                    "Duraklatma yalnızca istatistik ve seriyi etkiler; dinî yükümlülüğü değiştirmez."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .navigationTitle(settings.t("Gebets-Tracking", "Namaz Takibi"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }
}

struct TrackerPauseView: View {
'''
if old not in s:
    raise SystemExit("v3.62: tracker insertion anchor missing")
s = s.replace(old, new, 1)

old = '''                dailyDuaCard
                streakCard
                dashboardGrid
'''
new = '''                dailyDuaCard
                NavigationLink { PrayerTrackerOverviewView() } label: { streakCard }
                    .buttonStyle(.plain)
                    .accessibilityHint(settings.t("Gebets-Tracking öffnen", "Namaz takibini aç"))
                dashboardGrid
'''
if old not in s:
    raise SystemExit("v3.62: streak card anchor missing")
s = s.replace(old, new, 1)

old = '''                    Image(systemName: settings.notificationsEnabled ? "bell.fill" : "bell")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(.white)
'''
new = '''                    NavigationLink { SettingsView() } label: {
                        Image(systemName: settings.notificationsEnabled ? "bell.fill" : "bell")
                            .font(.system(size: 12, weight: .semibold))
                            .foregroundStyle(.white)
                            .frame(width: 24, height: 24)
                            .contentShape(Rectangle())
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(settings.t("Benachrichtigungseinstellungen", "Bildirim ayarları"))
'''
if old not in s:
    raise SystemExit("v3.62: static home bell anchor missing")
s = s.replace(old, new, 1)
home.write_text(s, encoding="utf-8")

# ---------- Prayer detail: the tracker now has a real write path ----------
detail = root / "SalahZeit" / "Views" / "PrayerDetailView.swift"
s = detail.read_text(encoding="utf-8")
old = '''    @Environment(\\.dismiss) private var dismiss

    let prayer: PrayerOccurrence
'''
new = '''    @Environment(\\.dismiss) private var dismiss
    @State private var trackerRefresh = 0

    let prayer: PrayerOccurrence
'''
if old not in s:
    raise SystemExit("v3.62: prayer detail state anchor missing")
s = s.replace(old, new, 1)

old = '''    var body: some View {
        NavigationStack {
            List {
'''
new = '''    var body: some View {
        let isTrackable = PrayerTrackerStore.requiredKinds.contains(prayer.kind)
        let isCompleted = PrayerTrackerStore.isCompleted(prayer.kind, on: prayer.date)

        NavigationStack {
            List {
'''
if old not in s:
    raise SystemExit("v3.62: prayer detail body anchor missing")
s = s.replace(old, new, 1)

old = '''                Section(settings.t("Hinweis", "Not")) {
                    Text(prayer.kind.detailNote(settings.language))
                }
'''
new = '''                if isTrackable {
                    Section(settings.t("Gebets-Tracking", "Namaz Takibi")) {
                        Button {
                            _ = PrayerTrackerStore.toggle(prayer.kind, on: prayer.date)
                            trackerRefresh += 1
                        } label: {
                            HStack {
                                Label(
                                    isCompleted
                                        ? settings.t("Als gebetet markiert", "Kılındı olarak işaretlendi")
                                        : settings.t("Als gebetet markieren", "Kılındı olarak işaretle"),
                                    systemImage: isCompleted ? "checkmark.circle.fill" : "circle"
                                )
                                Spacer()
                                Text(isCompleted ? settings.t("Erledigt", "Tamam") : settings.t("Offen", "Açık"))
                                    .font(.caption.bold())
                            }
                            .contentShape(Rectangle())
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(isCompleted ? SalahTheme.teal : SalahTheme.ink)
                    }
                }

                Section(settings.t("Hinweis", "Not")) {
                    Text(prayer.kind.detailNote(settings.language))
                }
'''
if old not in s:
    raise SystemExit("v3.62: prayer detail section anchor missing")
s = s.replace(old, new, 1)
detail.write_text(s, encoding="utf-8")

# ---------- Quran preview: pause/resume correctly and show failures instead of silent taps ----------
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''    func cyclePlaybackRate() {
        let rates: [Float] = [0.75, 1.0, 1.25, 1.5]
        let current = rates.firstIndex(where: { abs($0 - playbackRate) < 0.001 }) ?? 1
        playbackRate = rates[(current + 1) % rates.count]
        player?.defaultRate = playbackRate
        if isPlaying { player?.rate = playbackRate }
    }

    func stop() {
'''
new = '''    func cyclePlaybackRate() {
        let rates: [Float] = [0.75, 1.0, 1.25, 1.5]
        let current = rates.firstIndex(where: { abs($0 - playbackRate) < 0.001 }) ?? 1
        playbackRate = rates[(current + 1) % rates.count]
        player?.defaultRate = playbackRate
        if isPlaying { player?.rate = playbackRate }
    }

    func pause() {
        player?.pause()
        isPlaying = false
    }

    func resume() {
        guard let player else { return }
        lastError = nil
        player.defaultRate = playbackRate
        player.playImmediately(atRate: playbackRate)
    }

    func stop() {
'''
if old not in s:
    raise SystemExit("v3.62: audio pause/resume anchor missing")
s = s.replace(old, new, 1)

old = '''                                }
                                .foregroundStyle(SalahTheme.teal)
                            }
'''
new = '''                                }
                                .foregroundStyle(SalahTheme.teal)

                                if let error = previewAudio.lastError {
                                    Label(error, systemImage: "exclamationmark.triangle.fill")
                                        .font(.caption2)
                                        .foregroundStyle(.red)
                                        .frame(maxWidth: .infinity, alignment: .leading)
                                }
                            }
'''
if old not in s:
    raise SystemExit("v3.62: Quran preview error anchor missing")
s = s.replace(old, new, 1)

old = '''    private func togglePreviewAudio() async {
        if previewAudio.isPlaying {
            previewAudio.stop()
            return
        }

        if !previewAudioURLs.isEmpty {
            previewAudio.playQueue(previewAudioURLs)
            return
        }
'''
new = '''    private func togglePreviewAudio() async {
        if previewAudio.isPlaying {
            previewAudio.pause()
            return
        }

        if previewAudio.activeURL != nil,
           previewAudio.duration > 0,
           previewAudio.currentTime + 0.5 < previewAudio.duration {
            previewAudio.resume()
            return
        }

        if !previewAudioURLs.isEmpty {
            previewAudio.playQueue(previewAudioURLs)
            return
        }
'''
if old not in s:
    raise SystemExit("v3.62: Quran preview toggle anchor missing")
s = s.replace(old, new, 1)
guide.write_text(s, encoding="utf-8")

# ---------- QA route for the new tracker screen ----------
app = root / "SalahZeit" / "SalahZeitApp.swift"
s = app.read_text(encoding="utf-8")
old = '''        case "wudu":
            NavigationStack { WuduGuideView() }
        case "tasbih":
'''
new = '''        case "wudu":
            NavigationStack { WuduGuideView() }
        case "tracker":
            NavigationStack { PrayerTrackerOverviewView() }
        case "tasbih":
'''
if old not in s:
    raise SystemExit("v3.62: tracker QA route anchor missing")
s = s.replace(old, new, 1)
app.write_text(s, encoding="utf-8")

print("SalahPath v3.62 FAST functionality patch applied")
