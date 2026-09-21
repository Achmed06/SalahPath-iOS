from pathlib import Path

root = Path.cwd()
settings = root / "SalahZeit" / "Views" / "SettingsView.swift"
pbx = root / "SalahZeit.xcodeproj" / "project.pbxproj"
privacy_manifest = root / "SalahZeit" / "PrivacyInfo.xcprivacy"

# 1) Add public privacy/support links without changing existing settings behavior.
text = settings.read_text(encoding="utf-8")
if "import Foundation\n" not in text:
    text = text.replace("import SwiftUI\n", "import SwiftUI\nimport Foundation\n", 1)

legal_section = r'''

                referenceSection(settings.t("Rechtliches & Hilfe", "Yasal bilgiler & yardım")) {
                    Link(destination: URL(string: "https://github.com/Achmed06/SalahPath-iOS/blob/main/PRIVACY.md")!) {
                        HStack(spacing: 9) {
                            Image(systemName: "hand.raised.fill")
                                .font(.system(size: 14, weight: .semibold))
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 28, height: 28)
                                .background(SalahTheme.softTeal, in: Circle())

                            Text(settings.t("Datenschutzerklärung", "Gizlilik politikası"))
                                .font(.system(size: 11.5, weight: .semibold))
                                .foregroundStyle(SalahTheme.ink)

                            Spacer()

                            Image(systemName: "arrow.up.right.square")
                                .font(.caption.bold())
                                .foregroundStyle(SalahTheme.teal)
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                    }
                    .buttonStyle(.plain)

                    Link(destination: URL(string: "https://github.com/Achmed06/SalahPath-iOS/issues")!) {
                        HStack(spacing: 9) {
                            Image(systemName: "questionmark.circle.fill")
                                .font(.system(size: 14, weight: .semibold))
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 28, height: 28)
                                .background(SalahTheme.softTeal, in: Circle())

                            Text(settings.t("Support", "Destek"))
                                .font(.system(size: 11.5, weight: .semibold))
                                .foregroundStyle(SalahTheme.ink)

                            Spacer()

                            Image(systemName: "arrow.up.right.square")
                                .font(.caption.bold())
                                .foregroundStyle(SalahTheme.teal)
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                    }
                    .buttonStyle(.plain)
                }
'''
anchor = '''                referenceSection(settings.t("Feinabstimmung", "İnce ayar")) {'''
if "Datenschutzerklärung" not in text:
    if anchor not in text:
        raise SystemExit("v439: Settings legal insertion anchor missing")
    text = text.replace(anchor, legal_section + "\n" + anchor, 1)
settings.write_text(text, encoding="utf-8")

# 2) Privacy manifest: no tracking / no declared collection; Required Reason APIs used by app.
privacy_manifest.write_text('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array/>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>C617.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
''', encoding="utf-8")

# 3) Include privacy manifest in target resources and align project metadata with release build.
p = pbx.read_text(encoding="utf-8")
if "PrivacyInfo.xcprivacy in Resources" not in p:
    p = p.replace(
        'A20000000000000000000020 /* Assets.xcassets in Resources */ = {isa = PBXBuildFile; fileRef = A10000000000000000000020 /* Assets.xcassets */; };',
        'A20000000000000000000020 /* Assets.xcassets in Resources */ = {isa = PBXBuildFile; fileRef = A10000000000000000000020 /* Assets.xcassets */; };\n\t\tA20000000000000000000021 /* PrivacyInfo.xcprivacy in Resources */ = {isa = PBXBuildFile; fileRef = A10000000000000000000021 /* PrivacyInfo.xcprivacy */; };',
        1,
    )
if "/* PrivacyInfo.xcprivacy */ = {isa = PBXFileReference" not in p:
    p = p.replace(
        'A10000000000000000000020 /* Assets.xcassets */ = {isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = SalahZeit/Assets.xcassets; sourceTree = "<group>"; };',
        'A10000000000000000000020 /* Assets.xcassets */ = {isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = SalahZeit/Assets.xcassets; sourceTree = "<group>"; };\n\t\tA10000000000000000000021 /* PrivacyInfo.xcprivacy */ = {isa = PBXFileReference; lastKnownFileType = text.xml; path = SalahZeit/PrivacyInfo.xcprivacy; sourceTree = "<group>"; };',
        1,
    )
if "A10000000000000000000021 /* PrivacyInfo.xcprivacy */," not in p:
    p = p.replace(
        'A1000000000000000000020 /* Assets.xcassets */,',
        'A10000000000000000000020 /* Assets.xcassets */,\n\t\t\t\tA10000000000000000000021 /* PrivacyInfo.xcprivacy */,',
        1,
    )
if "A20000000000000000000021 /* PrivacyInfo.xcprivacy in Resources */," not in p:
    p = p.replace(
        'A20000000000000000000020 /* Assets.xcassets in Resources */,',
        'A20000000000000000000020 /* Assets.xcassets in Resources */,\n\t\t\t\tA2000000000000000000021 /* PrivacyInfo.xcprivacy in Resources */,',
        1,
    )

# Keep local Xcode metadata identical to the release build overrides.
p = p.replace("CURRENT_PROJECT_VERSION = 1;", "CURRENT_PROJECT_VERSION = 76;")
p = p.replace("MARKETING_VERSION = 1.0;", "MARKETING_VERSION = 3.62;")
p = p.replace("PRODUCT_BUNDLE_IDENTIFIER = com.salahzeit.private;", "PRODUCT_BUNDLE_IDENTIFIER = com.achmed06.salahpath;")

# Only HTTPS via Apple's networking stack is used; declare exempt encryption to streamline App Store uploads.
if "INFOPLIST_KEY_ITSAppUsesNonExemptEncryption" not in p:
    p = p.replace(
        "GENERATE_INFOPLIST_FILE = YES;",
        "GENERATE_INFOPLIST_FILE = YES;\n\t\t\t\tINFOPLIST_KEY_ITSAppUsesNonExemptEncryption = NO;",
    )

pbx.write_text(p, encoding="utf-8")
print("v439 applied: App Store privacy manifest, legal links and release metadata aligned")
