from pathlib import Path

# SalahPath v3.47 — make the reference navigation appearance deterministic for
# both the real tab flow and the direct QA routes used to capture the four
# side-phone reference screens.

app = Path("SalahZeit/SalahZeitApp.swift")
s = app.read_text(encoding="utf-8")

needle = '''struct SalahPathApp: App {
    @StateObject private var locationManager = LocationManager()
    @StateObject private var settings = SettingsStore()
'''
replacement = '''struct SalahPathApp: App {
    @StateObject private var locationManager = LocationManager()
    @StateObject private var settings = SettingsStore()

    init() {
        let navigation = UINavigationBarAppearance()
        navigation.configureWithOpaqueBackground()
        navigation.backgroundColor = UIColor(red: 36/255, green: 79/255, blue: 77/255, alpha: 1)
        navigation.shadowColor = UIColor(red: 234/255, green: 185/255, blue: 80/255, alpha: 0.28)
        navigation.titleTextAttributes = [.foregroundColor: UIColor.white]
        navigation.largeTitleTextAttributes = [.foregroundColor: UIColor.white]
        UINavigationBar.appearance().standardAppearance = navigation
        UINavigationBar.appearance().scrollEdgeAppearance = navigation
        UINavigationBar.appearance().compactAppearance = navigation
        UINavigationBar.appearance().tintColor = UIColor.white
    }
'''
if needle not in s:
    raise SystemExit("v3.47: SalahPathApp insertion point not found")
s = s.replace(needle, replacement, 1)
app.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.46"' not in t or 'CURRENT_PROJECT_VERSION="51"' not in t:
    raise SystemExit("v3.47: expected v3.46/51 build version not found")
t = t.replace('MARKETING_VERSION="3.46"', 'MARKETING_VERSION="3.47"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="51"', 'CURRENT_PROJECT_VERSION="52"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.47 global reference navigation appearance applied")
