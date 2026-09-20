from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''                audiencePill(.male, title: "Erkek")
                audiencePill(.female, title: "Kadın")

                Button {
                    settings.language = .german
                } label: {
                    Text("Deutsch")
'''
new = '''                audiencePill(.male, title: settings.t("Mann", "Erkek"))
                audiencePill(.female, title: settings.t("Frau", "Kadın"))

                Button {
                    settings.language = settings.language == .german ? .turkish : .german
                } label: {
                    Text(settings.language == .german ? "Türkçe" : "Deutsch")
'''
if old not in s:
    raise SystemExit("v3.77: prayer learning language/audience selector anchor missing")
s = s.replace(old, new, 1)

old = '''                            SalahTheme.gold.opacity(settings.language == .german ? 0.24 : 0.12),
'''
new = '''                            SalahTheme.gold.opacity(0.18),
'''
if old not in s:
    raise SystemExit("v3.77: language selector highlight anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.77 prayer learning selector localization/toggle applied")
