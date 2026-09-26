import SwiftUI
import UIKit

enum SalahTheme {
    // The navigation/header tone remains brand-stable; content colors adapt to iOS appearance.
    static let navigationTeal = Color(red: 36/255, green: 79/255, blue: 77/255)

    static let teal = adaptive(
        light: UIColor(red: 43/255, green: 86/255, blue: 82/255, alpha: 1),
        dark: UIColor(red: 91/255, green: 188/255, blue: 174/255, alpha: 1)
    )
    static let deepTeal = adaptive(
        light: UIColor(red: 36/255, green: 79/255, blue: 77/255, alpha: 1),
        dark: UIColor(red: 116/255, green: 207/255, blue: 192/255, alpha: 1)
    )
    static let gold = adaptive(
        light: UIColor(red: 234/255, green: 185/255, blue: 80/255, alpha: 1),
        dark: UIColor(red: 244/255, green: 200/255, blue: 103/255, alpha: 1)
    )
    static let cream = adaptive(
        light: UIColor(red: 250/255, green: 250/255, blue: 241/255, alpha: 1),
        dark: UIColor(red: 28/255, green: 34/255, blue: 32/255, alpha: 1)
    )
    static let page = adaptive(
        light: UIColor(red: 235/255, green: 232/255, blue: 216/255, alpha: 1),
        dark: UIColor(red: 14/255, green: 20/255, blue: 19/255, alpha: 1)
    )
    static let ink = adaptive(
        light: UIColor(red: 15/255, green: 39/255, blue: 50/255, alpha: 1),
        dark: UIColor(red: 239/255, green: 244/255, blue: 240/255, alpha: 1)
    )
    static let mutedInk = adaptive(
        light: UIColor(red: 82/255, green: 103/255, blue: 101/255, alpha: 1),
        dark: UIColor(red: 170/255, green: 187/255, blue: 183/255, alpha: 1)
    )
    static let softTeal = adaptive(
        light: UIColor(red: 230/255, green: 238/255, blue: 232/255, alpha: 1),
        dark: UIColor(red: 34/255, green: 58/255, blue: 54/255, alpha: 1)
    )

    static func cardStroke(_ opacity: Double = 0.34) -> Color { gold.opacity(opacity) }

    private static func adaptive(light: UIColor, dark: UIColor) -> Color {
        Color(UIColor { traits in
            traits.userInterfaceStyle == .dark ? dark : light
        })
    }
}
