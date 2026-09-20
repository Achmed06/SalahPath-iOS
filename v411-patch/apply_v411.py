from pathlib import Path

root = Path("SalahZeit/Views/RootTabView.swift")
text = root.read_text(encoding="utf-8")

old = '''                    NavigationLink { FastingTrackerView() } label: {
                        discoverTile(icon: "moon.stars.fill", title: settings.t("Fasten", "Oruç"), subtitle: settings.t("Tracker", "Takip"))
                    }
'''
new = '''                    NavigationLink { FastingTrackerView() } label: {
                        discoverTile(
                            icon: "moon.stars.fill",
                            title: settings.t("Fasten & Ramadan", "Oruç & Ramazan"),
                            subtitle: settings.t("Lernen & Tracker", "Öğren & takip")
                        )
                    }
'''
if old not in text:
    raise SystemExit("v411: fasting Discover tile anchor missing")
root.write_text(text.replace(old, new, 1), encoding="utf-8")
print("v411 applied: Discover fasting tile reflects Ramadan learning hub")
