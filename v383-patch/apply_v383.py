from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

anchors = [
    '.navigationTitle(settings.t("Gebetsduas", "Namaz duaları"))',
    '.navigationTitle(settings.t("Dua-Sammlung", "Dua koleksiyonu"))',
    '.navigationTitle(settings.t("Favoriten", "Favoriler"))',
]

for anchor in anchors:
    if anchor not in s:
        raise SystemExit(f"v3.83: missing navigation title anchor: {anchor}")
    s = s.replace(anchor, anchor + '\n        .navigationBarTitleDisplayMode(.inline)', 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.83 compact navigation titles applied")
