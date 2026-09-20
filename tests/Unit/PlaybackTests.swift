import XCTest
@testable import SalahZeit

@MainActor
final class PlaybackTests: XCTestCase {
    private var defaults: UserDefaults!
    private var suite: String!

    override func setUp() async throws {
        suite = "SalahPathTests.\(UUID().uuidString)"
        defaults = UserDefaults(suiteName: suite)!
    }

    override func tearDown() async throws {
        defaults.removePersistentDomain(forName: suite)
    }

    func testEveryTapAdvancesExactlyOnceAndPersists() {
        let player = RemoteAudioPlayer(defaults: defaults)
        XCTAssertEqual(player.playbackRate, 1)
        for expected in [Float(1.25), 1.5, 0.75, 1] {
            player.cyclePlaybackRate()
            XCTAssertEqual(player.playbackRate, expected)
            XCTAssertEqual(RemoteAudioPlayer(defaults: defaults).playbackRate, expected)
            XCTAssertFalse(player.isPlaybackRequested)
        }
    }

    func testInvalidSavedRateFallsBackToNormal() {
        defaults.set(99, forKey: "audioPlaybackRate")
        XCTAssertEqual(RemoteAudioPlayer(defaults: defaults).playbackRate, 1)
    }

    func testRapidToggleDuringBufferingUsesUserIntent() async throws {
        let player = RemoteAudioPlayer(defaults: defaults)
        let url = URL(string: "https://example.invalid/test.mp3")!
        player.toggle(url)
        XCTAssertTrue(player.isPlaybackRequested)
        player.toggle(url)
        XCTAssertFalse(player.isPlaybackRequested)
        player.toggle(url)
        XCTAssertTrue(player.isPlaybackRequested)
        player.stop()
        try await Task.sleep(for: .milliseconds(300))
        XCTAssertFalse(player.isPlaybackRequested)
        XCTAssertFalse(player.isLoading)
        XCTAssertFalse(player.isPlaying)
        XCTAssertNil(player.activeURL)
        XCTAssertEqual(player.queueCount, 0)
    }

    func testSettingsPersistEachLanguageAndFontChange() {
        let settings = SettingsStore(defaults: defaults)
        settings.language = .turkish
        settings.quranFontSize = 22
        settings.quranShowTranslation = false
        let restored = SettingsStore(defaults: defaults)
        XCTAssertEqual(restored.language, .turkish)
        XCTAssertEqual(restored.quranFontSize, 22)
        XCTAssertFalse(restored.quranShowTranslation)
        restored.language = .german
        XCTAssertEqual(SettingsStore(defaults: defaults).language, .german)
    }
}
