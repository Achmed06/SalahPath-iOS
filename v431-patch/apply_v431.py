from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

# Add persistent per-ayah repeat state beside the existing playback-rate state.
old = '''    private var periodicTimeObserver: Any?
    private let playbackRateDefaultsKey = "quranPlaybackRate"

    init() {
        let savedRate = UserDefaults.standard.float(forKey: playbackRateDefaultsKey)
        let supportedRates: [Float] = [0.75, 1.0, 1.25, 1.5]
        if supportedRates.contains(where: { abs($0 - savedRate) < 0.001 }) {
            playbackRate = savedRate
        }
    }
'''
new = '''    private var periodicTimeObserver: Any?
    private let playbackRateDefaultsKey = "quranPlaybackRate"
    private let repeatCountDefaultsKey = "quranAyahRepeatCount"
    @Published private(set) var repeatCount = 1
    private var repeatIteration = 1

    init() {
        let savedRate = UserDefaults.standard.float(forKey: playbackRateDefaultsKey)
        let supportedRates: [Float] = [0.75, 1.0, 1.25, 1.5]
        if supportedRates.contains(where: { abs($0 - savedRate) < 0.001 }) {
            playbackRate = savedRate
        }

        let savedRepeatCount = UserDefaults.standard.integer(forKey: repeatCountDefaultsKey)
        if [1, 3, 5, -1].contains(savedRepeatCount) {
            repeatCount = savedRepeatCount
        }
    }
'''
if old not in text:
    raise SystemExit("v431: RemoteAudioPlayer persistent settings anchor missing")
text = text.replace(old, new, 1)

old = '''        playbackRate = rates[(current + 1) % rates.count]
        UserDefaults.standard.set(playbackRate, forKey: playbackRateDefaultsKey)
        player?.defaultRate = playbackRate
        if isPlaying { player?.rate = playbackRate }
    }
'''
new = '''        playbackRate = rates[(current + 1) % rates.count]
        UserDefaults.standard.set(playbackRate, forKey: playbackRateDefaultsKey)
        player?.defaultRate = playbackRate
        if isPlaying { player?.rate = playbackRate }
    }

    var repeatModeLabel: String {
        repeatCount == -1 ? "∞×" : "\\(repeatCount)×"
    }

    func cycleRepeatMode() {
        let modes = [1, 3, 5, -1]
        let current = modes.firstIndex(of: repeatCount) ?? 0
        repeatCount = modes[(current + 1) % modes.count]
        repeatIteration = 1
        UserDefaults.standard.set(repeatCount, forKey: repeatCountDefaultsKey)
    }

    private func shouldRepeatCurrentItem() -> Bool {
        if repeatCount == -1 {
            return true
        }
        if repeatIteration < repeatCount {
            repeatIteration += 1
            return true
        }
        repeatIteration = 1
        return false
    }
'''
if old not in text:
    raise SystemExit("v431: playback-rate method anchor missing")
text = text.replace(old, new, 1)

old = '''    private func loadCurrentAndPlay() {
        guard queueURLs.indices.contains(queueIndex) else { return }
        removeObservers()
'''
new = '''    private func loadCurrentAndPlay() {
        guard queueURLs.indices.contains(queueIndex) else { return }
        repeatIteration = 1
        removeObservers()
'''
if old not in text:
    raise SystemExit("v431: queue-load anchor missing")
text = text.replace(old, new, 1)

old = '''        endObserver = NotificationCenter.default.addObserver(
            forName: .AVPlayerItemDidPlayToEndTime,
            object: item,
            queue: .main
        ) { [weak self] _ in
            Task { @MainActor in
                guard let self else { return }
                if self.hasNext {
                    self.next()
                } else {
                    self.isPlaying = false
                    self.isLoading = false
                }
            }
        }
'''
new = '''        endObserver = NotificationCenter.default.addObserver(
            forName: .AVPlayerItemDidPlayToEndTime,
            object: item,
            queue: .main
        ) { [weak self, weak newPlayer] _ in
            Task { @MainActor in
                guard let self else { return }

                if self.shouldRepeatCurrentItem(), let newPlayer {
                    self.currentTime = 0
                    self.isLoading = false
                    newPlayer.seek(to: .zero)
                    newPlayer.playImmediately(atRate: self.playbackRate)
                    self.isPlaying = true
                    return
                }

                if self.hasNext {
                    self.next()
                } else {
                    self.isPlaying = false
                    self.isLoading = false
                }
            }
        }
'''
if old not in text:
    raise SystemExit("v431: playback-end observer anchor missing")
text = text.replace(old, new, 1)

old = '''                Button { audio.cyclePlaybackRate() } label: {
                    Text(audio.playbackRateLabel)
                        .font(.system(size: 11, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                        .padding(.horizontal, 9)
                        .padding(.vertical, 7)
                        .background(Color.white.opacity(0.82), in: Capsule())
                        .contentShape(Capsule())
                }
                .buttonStyle(.plain)
                .accessibilityLabel(settings.t("Wiedergabegeschwindigkeit", "Oynatma hızı"))
                .accessibilityValue(audio.playbackRateLabel)
                .accessibilityHint(settings.t("Tippen, um die Geschwindigkeit zu ändern", "Hızı değiştirmek için dokun"))
'''
new = '''                Button { audio.cyclePlaybackRate() } label: {
                    Text(audio.playbackRateLabel)
                        .font(.system(size: 11, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                        .padding(.horizontal, 9)
                        .padding(.vertical, 7)
                        .background(Color.white.opacity(0.82), in: Capsule())
                        .contentShape(Capsule())
                }
                .buttonStyle(.plain)
                .accessibilityLabel(settings.t("Wiedergabegeschwindigkeit", "Oynatma hızı"))
                .accessibilityValue(audio.playbackRateLabel)
                .accessibilityHint(settings.t("Tippen, um die Geschwindigkeit zu ändern", "Hızı değiştirmek için dokun"))

                Button { audio.cycleRepeatMode() } label: {
                    HStack(spacing: 4) {
                        Image(systemName: "repeat")
                        Text(audio.repeatModeLabel)
                    }
                    .font(.system(size: 11, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                    .padding(.horizontal, 9)
                    .padding(.vertical, 7)
                    .background(Color.white.opacity(0.82), in: Capsule())
                    .contentShape(Capsule())
                }
                .buttonStyle(.plain)
                .accessibilityLabel(settings.t("Vers wiederholen", "Ayet tekrarı"))
                .accessibilityValue(audio.repeatModeLabel)
                .accessibilityHint(settings.t(
                    "1, 3, 5 oder unbegrenzt. Danach geht die Wiedergabe zum nächsten Vers weiter.",
                    "1, 3, 5 veya sınırsız tekrar. Sonra oynatma sonraki ayete geçer."
                ))
'''
if old not in text:
    raise SystemExit("v431: Quran playback-rate control anchor missing")
text = text.replace(old, new, 1)

guide.write_text(text, encoding="utf-8")
print("v431 applied: persistent Quran ayah repeat modes 1x/3x/5x/infinity")
