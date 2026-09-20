from pathlib import Path
import shutil
import subprocess

# SalahPath v3.61 FAST — guide artwork fit + visible-control functionality.
root = Path.cwd()
assets = root / "SalahZeit" / "Assets.xcassets"

# Normalize all prayer illustrations onto one square canvas and all Wudu
# illustrations onto one 4:3 canvas. A few source images include old captions;
# crop those captions before fitting the artwork. sips is built into macOS,
# which is the platform used by every Xcode workflow in this repository.
sips = shutil.which("sips")

crop_specs = {
    "female_bowing": (195, 185, 30, 0),
    "male_bowing": (188, 200, 0, 0),
    "male_standing": (190, 97, 0, 0),
    "male_takbir": (142, 165, 0, 0),
}

prayer_assets = [
    "female_bowing", "female_final_sitting", "female_intention",
    "female_salam_left", "female_salam_right", "female_sitting",
    "female_standing", "female_sujud", "female_takbir", "female_upright",
    "male_bowing", "male_final_sitting", "male_intention",
    "male_salam_left", "male_salam_right", "male_sitting",
    "male_standing", "male_sujud", "male_takbir", "male_upright",
]

wudu_assets = [
    "wudu_ears", "wudu_face", "wudu_feet", "wudu_hands", "wudu_head",
    "wudu_intention", "wudu_leftarm", "wudu_mouth", "wudu_neck",
    "wudu_nose", "wudu_rightarm",
]


def jpeg_for(asset: str) -> Path:
    folder = assets / f"{asset}.imageset"
    candidates = list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg"))
    if len(candidates) != 1:
        raise SystemExit(f"v3.61: expected exactly one JPEG for {asset}, found {len(candidates)}")
    return candidates[0]


def run_sips(*args: str) -> None:
    assert sips is not None
    subprocess.run([sips, *args], check=True, stdout=subprocess.DEVNULL)


if sips:
    for asset, (height, width, y, x) in crop_specs.items():
        path = jpeg_for(asset)
        run_sips("-c", str(height), str(width), "--cropOffset", str(y), str(x), str(path))

    for asset in prayer_assets:
        path = jpeg_for(asset)
        run_sips("-Z", "292", str(path))
        run_sips("-p", "320", "320", "--padColor", "FAF6EB", str(path))

    for asset in wudu_assets:
        path = jpeg_for(asset)
        run_sips("-Z", "332", str(path))
        run_sips("-p", "270", "360", "--padColor", "FAF6EB", str(path))
else:
    # Allows patch-source inspection on non-macOS hosts. Xcode CI always has sips.
    print("v3.61: sips unavailable; skipped guide-image normalization on this host")

# ---------- Home: make the visibly tappable next-prayer card open its existing detail sheet ----------
home = root / "SalahZeit" / "Views" / "HomeView.swift"
s = home.read_text(encoding="utf-8")
old = '''    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {
        ZStack(alignment: .bottomTrailing) {
'''
new = '''    private func nextPrayerHero(_ prayer: PrayerOccurrence) -> some View {
        Button {
            selectedPrayer = prayer
        } label: {
            ZStack(alignment: .bottomTrailing) {
'''
if old not in s:
    raise SystemExit("v3.61: next-prayer hero opening anchor missing")
s = s.replace(old, new, 1)

old = '''        .shadow(color: SalahTheme.deepTeal.opacity(0.025), radius: 2, y: 1)
        .clipped()
    }

    private var prayerLegendCard: some View {
'''
new = '''            .shadow(color: SalahTheme.deepTeal.opacity(0.025), radius: 2, y: 1)
            .clipped()
        }
        .buttonStyle(.plain)
        .contentShape(Rectangle())
        .accessibilityHint(settings.t("Gebetsdetails öffnen", "Namaz ayrıntılarını aç"))
    }

    private var prayerLegendCard: some View {
'''
if old not in s:
    raise SystemExit("v3.61: next-prayer hero closing anchor missing")
s = s.replace(old, new, 1)
home.write_text(s, encoding="utf-8")

# ---------- Quran preview: replace the decorative 0:00/0:45 bar and 1.0x pill with real state ----------
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")
old = '''    @Published var queueIndex = 0
    @Published var queueCount = 0

    private var player: AVPlayer?
'''
new = '''    @Published var queueIndex = 0
    @Published var queueCount = 0
    @Published var playbackRate: Float = 1.0
    @Published var currentTime: Double = 0
    @Published var duration: Double = 0

    private var player: AVPlayer?
'''
if old not in s:
    raise SystemExit("v3.61: audio state anchor missing")
s = s.replace(old, new, 1)

old = '''    private var failedObserver: NSObjectProtocol?

    var hasNext: Bool { queueIndex + 1 < queueURLs.count }
    var hasPrevious: Bool { queueIndex > 0 }
'''
new = '''    private var failedObserver: NSObjectProtocol?
    private var periodicTimeObserver: Any?

    var hasNext: Bool { queueIndex + 1 < queueURLs.count }
    var hasPrevious: Bool { queueIndex > 0 }
    var progress: Double {
        guard duration.isFinite, duration > 0 else { return 0 }
        return min(max(currentTime / duration, 0), 1)
    }
    var playbackRateLabel: String {
        switch playbackRate {
        case 0.75: return "0.75x"
        case 1.25: return "1.25x"
        case 1.5: return "1.5x"
        default: return "1.0x"
        }
    }
'''
if old not in s:
    raise SystemExit("v3.61: audio observer anchor missing")
s = s.replace(old, new, 1)

old = '''        if activeURL == url, let player {
            if isPlaying { player.pause() } else { lastError = nil; player.play() }
            return
        }
'''
new = '''        if activeURL == url, let player {
            if isPlaying {
                player.pause()
            } else {
                lastError = nil
                player.defaultRate = playbackRate
                player.playImmediately(atRate: playbackRate)
            }
            return
        }
'''
if old not in s:
    raise SystemExit("v3.61: audio toggle anchor missing")
s = s.replace(old, new, 1)

old = '''    func previous() {
        guard hasPrevious else { return }
        queueIndex -= 1
        loadCurrentAndPlay()
    }

    func stop() {
'''
new = '''    func previous() {
        guard hasPrevious else { return }
        queueIndex -= 1
        loadCurrentAndPlay()
    }

    func cyclePlaybackRate() {
        let rates: [Float] = [0.75, 1.0, 1.25, 1.5]
        let current = rates.firstIndex(where: { abs($0 - playbackRate) < 0.001 }) ?? 1
        playbackRate = rates[(current + 1) % rates.count]
        player?.defaultRate = playbackRate
        if isPlaying { player?.rate = playbackRate }
    }

    func stop() {
'''
if old not in s:
    raise SystemExit("v3.61: audio previous/stop anchor missing")
s = s.replace(old, new, 1)

old = '''        lastError = nil
        isLoading = true
        isPlaying = false
        let url = queueURLs[queueIndex]
'''
new = '''        lastError = nil
        isLoading = true
        isPlaying = false
        currentTime = 0
        duration = 0
        let url = queueURLs[queueIndex]
'''
if old not in s:
    raise SystemExit("v3.61: audio load reset anchor missing")
s = s.replace(old, new, 1)

old = '''        let item = AVPlayerItem(url: url)
        let newPlayer = AVPlayer(playerItem: item)
        player = newPlayer

        statusObservation = item.observe(\.status, options: [.initial, .new]) { [weak self] item, _ in
'''
new = '''        let item = AVPlayerItem(url: url)
        let newPlayer = AVPlayer(playerItem: item)
        newPlayer.defaultRate = playbackRate
        player = newPlayer

        periodicTimeObserver = newPlayer.addPeriodicTimeObserver(
            forInterval: CMTime(seconds: 0.25, preferredTimescale: 600),
            queue: .main
        ) { [weak self, weak newPlayer] time in
            Task { @MainActor in
                guard let self else { return }
                let seconds = time.seconds
                self.currentTime = seconds.isFinite && seconds >= 0 ? seconds : 0
                if let itemDuration = newPlayer?.currentItem?.duration.seconds, itemDuration.isFinite, itemDuration > 0 {
                    self.duration = itemDuration
                }
            }
        }

        statusObservation = item.observe(\.status, options: [.initial, .new]) { [weak self] item, _ in
'''
if old not in s:
    raise SystemExit("v3.61: audio player creation anchor missing")
s = s.replace(old, new, 1)

old = '''        newPlayer.play()
    }

    private func removeObservers() {
        statusObservation = nil
        timeControlObservation = nil
'''
new = '''        newPlayer.playImmediately(atRate: playbackRate)
    }

    private func removeObservers() {
        if let periodicTimeObserver, let player {
            player.removeTimeObserver(periodicTimeObserver)
        }
        periodicTimeObserver = nil
        statusObservation = nil
        timeControlObservation = nil
'''
if old not in s:
    raise SystemExit("v3.61: audio play/remove anchor missing")
s = s.replace(old, new, 1)

old = '''                                    HStack {
                                        Text("0:00")
                                        Spacer()
                                        Text("0:45")
                                    }
                                    .font(.system(size: 10.5, weight: .semibold).monospacedDigit())
                                    .foregroundStyle(SalahTheme.mutedInk)

                                    ZStack(alignment: .leading) {
                                        Capsule()
                                            .fill(SalahTheme.teal.opacity(0.14))
                                            .frame(height: 3.5)
                                        Capsule()
                                            .fill(SalahTheme.teal)
                                            .frame(width: 104, height: 3.5)
                                    }
'''
new = '''                                    HStack {
                                        Text(audioTimeString(previewAudio.currentTime))
                                        Spacer()
                                        Text(audioTimeString(previewAudio.duration))
                                    }
                                    .font(.system(size: 10.5, weight: .semibold).monospacedDigit())
                                    .foregroundStyle(SalahTheme.mutedInk)

                                    GeometryReader { geometry in
                                        ZStack(alignment: .leading) {
                                            Capsule()
                                                .fill(SalahTheme.teal.opacity(0.14))
                                            Capsule()
                                                .fill(SalahTheme.teal)
                                                .frame(width: geometry.size.width * previewAudio.progress)
                                        }
                                    }
                                    .frame(height: 3.5)
'''
if old not in s:
    raise SystemExit("v3.61: Quran preview progress anchor missing")
s = s.replace(old, new, 1)

old = '''                                    Text("1.0x")
                                        .font(.system(size: 11.5, weight: .bold))
                                        .padding(.horizontal, 9)
                                        .padding(.vertical, 6)
                                        .background(SalahTheme.softTeal, in: Capsule())
'''
new = '''                                    Button { previewAudio.cyclePlaybackRate() } label: {
                                        Text(previewAudio.playbackRateLabel)
                                            .font(.system(size: 11.5, weight: .bold))
                                            .padding(.horizontal, 9)
                                            .padding(.vertical, 6)
                                            .background(SalahTheme.softTeal, in: Capsule())
                                    }
                                    .buttonStyle(.plain)
                                    .accessibilityLabel(settings.t("Wiedergabegeschwindigkeit", "Oynatma hızı"))
'''
if old not in s:
    raise SystemExit("v3.61: Quran playback-rate anchor missing")
s = s.replace(old, new, 1)

anchor = '''private struct QuranBookmark: Hashable {
'''
helper = '''private func audioTimeString(_ seconds: Double) -> String {
    guard seconds.isFinite, seconds > 0 else { return "0:00" }
    let total = Int(seconds.rounded(.down))
    return "\(total / 60):" + String(format: "%02d", total % 60)
}

private struct QuranBookmark: Hashable {
'''
if anchor not in s:
    raise SystemExit("v3.61: Quran bookmark helper anchor missing")
s = s.replace(anchor, helper, 1)
guide.write_text(s, encoding="utf-8")

# ---------- QA: direct Wudu route so CI can screenshot the corrected Abdest images ----------
app = root / "SalahZeit" / "SalahZeitApp.swift"
s = app.read_text(encoding="utf-8")
old = '''        case "namaz-howto":
            NavigationStack { PrayerHowToView() }
        case "tasbih":
'''
new = '''        case "namaz-howto":
            NavigationStack { PrayerHowToView() }
        case "wudu":
            NavigationStack { WuduGuideView() }
        case "tasbih":
'''
if old not in s:
    raise SystemExit("v3.61: Wudu QA route anchor missing")
s = s.replace(old, new, 1)
app.write_text(s, encoding="utf-8")

print("SalahPath v3.61 FAST patch applied")
