import XCTest

final class NavigationTests: XCTestCase {
    func testReaderSpeedRespondsOnEveryTap() {
        let app = XCUIApplication()
        app.launchEnvironment["SALAH_QA_SCREEN"] = "quran-reader"
        app.launchArguments = ["-audioPlaybackRate", "1", "-appLanguage", "german"]
        app.launch()
        let speed = app.buttons["reader.playbackRate"]
        XCTAssertTrue(speed.waitForExistence(timeout: 15))
        for expected in ["1.25x", "1.5x", "0.75x", "1.0x"] {
            speed.tap()
            XCTAssertEqual(speed.value as? String, expected)
        }
        attachScreenshot("DE-reader-speed")
    }

    func testTabSwitching() {
        let app = XCUIApplication()
        app.launchArguments = ["-appLanguage", "german"]
        app.launch()
        app.buttons["tab.2"].tap()
        XCTAssertTrue(app.navigationBars["Gebet lernen"].waitForExistence(timeout: 5))
        app.buttons["tab.4"].tap()
        app.buttons["tab.2"].tap()
        XCTAssertTrue(app.navigationBars["Gebet lernen"].exists)
        attachScreenshot("DE-learning-tab")
    }

    func testScreensInBothLanguages() {
        for language in ["german", "turkish"] {
            for screen in ["namaz", "namaz-howto", "wudu", "quran-reader", "settings"] {
                let app = XCUIApplication()
                app.launchEnvironment["SALAH_QA_SCREEN"] = screen
                app.launchArguments = ["-appLanguage", language]
                app.launch()
                XCTAssertTrue(app.navigationBars.firstMatch.waitForExistence(timeout: 10))
                attachScreenshot("\(language)-\(screen)")
                app.terminate()
            }
        }
    }

    private func attachScreenshot(_ name: String) {
        let attachment = XCTAttachment(screenshot: XCUIScreen.main.screenshot())
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
    }
}
