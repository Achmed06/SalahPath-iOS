from pathlib import Path

root = Path.cwd()
settings = root / "SalahZeit" / "Views" / "SettingsView.swift"
s = settings.read_text(encoding="utf-8")

old = '''                    Text("v3.17 · 22")
                        .font(.system(size: 9, weight: .bold).monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
'''
new = '''                    Text(appVersionText)
                        .font(.system(size: 9, weight: .bold).monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
'''
if old not in s:
    raise SystemExit("v3.66: stale version label anchor missing")
s = s.replace(old, new, 1)

anchor = '''    private var profileHero: some View {
'''
helper = '''    private var appVersionText: String {
        let info = Bundle.main.infoDictionary
        let version = info?["CFBundleShortVersionString"] as? String ?? "—"
        let build = info?["CFBundleVersion"] as? String ?? "—"
        return "v\\(version) · \\(build)"
    }

'''
if anchor not in s:
    raise SystemExit("v3.66: profile hero anchor missing")
s = s.replace(anchor, helper + anchor, 1)

settings.write_text(s, encoding="utf-8")
print("SalahPath v3.66 dynamic app version label applied")
