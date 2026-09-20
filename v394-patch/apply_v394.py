from pathlib import Path

def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"v394: anchor missing for {label}: {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

root = Path.cwd()

# Make the system back button high-contrast on SalahPath's dark navigation bar.
root_tab = root / "SalahZeit" / "Views" / "RootTabView.swift"
replace_once(
    root_tab,
    '''        navigation.largeTitleTextAttributes = [.foregroundColor: UIColor.white]
        UINavigationBar.appearance().standardAppearance = navigation
''',
    '''        navigation.largeTitleTextAttributes = [.foregroundColor: UIColor.white]

        let backButton = UIBarButtonItemAppearance()
        backButton.normal.titleTextAttributes = [.foregroundColor: UIColor.white]
        backButton.highlighted.titleTextAttributes = [.foregroundColor: UIColor.white]
        navigation.backButtonAppearance = backButton

        let backIndicator = UIImage(
            systemName: "chevron.left",
            withConfiguration: UIImage.SymbolConfiguration(pointSize: 18, weight: .bold)
        )?.withTintColor(.white, renderingMode: .alwaysOriginal)
        navigation.setBackIndicatorImage(backIndicator, transitionMaskImage: backIndicator)

        UINavigationBar.appearance().standardAppearance = navigation
''',
    "navigation back button appearance",
)

text = root_tab.read_text(encoding="utf-8")
for view in ["HomeView()", "QuranView()", "GuideView()", "MoreView()", "SettingsView()"]:
    old = f"            NavigationStack {{ {view} }}\n"
    new = (
        f"            NavigationStack {{ {view} }}\n"
        "                .toolbarBackground(SalahTheme.deepTeal, for: .navigationBar)\n"
        "                .toolbarBackground(.visible, for: .navigationBar)\n"
        "                .toolbarColorScheme(.dark, for: .navigationBar)\n"
    )
    if old not in text:
        raise SystemExit(f"v394: navigation stack anchor missing: {view}")
    text = text.replace(old, new, 1)
root_tab.write_text(text, encoding="utf-8")

# Make Quran playback speed a real control on every reader screen and persist it.
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
replace_once(
    guide,
    '''    private var periodicTimeObserver: Any?

    var hasNext: Bool { queueIndex + 1 < queueURLs.count }
''',
    '''    private var periodicTimeObserver: Any?
    private let playbackRateDefaultsKey = "quranPlaybackRate"

    init() {
        let savedRate = UserDefaults.standard.float(forKey: playbackRateDefaultsKey)
        let supportedRates: [Float] = [0.75, 1.0, 1.25, 1.5]
        if supportedRates.contains(where: { abs($0 - savedRate) < 0.001 }) {
            playbackRate = savedRate
        }
    }

    var hasNext: Bool { queueIndex + 1 < queueURLs.count }
''',
    "persistent playback rate",
)
replace_once(
    guide,
    '''        playbackRate = rates[(current + 1) % rates.count]
        player?.defaultRate = playbackRate
        if isPlaying { player?.rate = playbackRate }
''',
    '''        playbackRate = rates[(current + 1) % rates.count]
        UserDefaults.standard.set(playbackRate, forKey: playbackRateDefaultsKey)
        player?.defaultRate = playbackRate
        if isPlaying { player?.rate = playbackRate }
''',
    "save playback rate",
)
replace_once(
    guide,
    '''                Text("1.0x")
                    .font(.system(size: 9, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                    .padding(.horizontal, 7)
                    .padding(.vertical, 5)
                    .background(Color.white.opacity(0.70), in: Capsule())
''',
    '''                Button { audio.cyclePlaybackRate() } label: {
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
''',
    "Quran reader playback rate button",
)

print("v394 applied: visible navigation back button + consistent Quran playback speed")
