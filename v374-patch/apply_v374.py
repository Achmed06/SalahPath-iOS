from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''                    ReferencePrayerPerson(
                        imageName: "male_sitting",
                        rugWidth: 120,
                        rugRotation: -1.5
                    )

                    ReferencePrayerPerson(
                        imageName: "female_sitting",
                        rugWidth: 120,
                        rugRotation: 1.5
                    )
'''
new = '''                    ReferencePrayerPerson(
                        imageName: "male_intention",
                        rugWidth: 120,
                        rugRotation: -1.5
                    )

                    ReferencePrayerPerson(
                        imageName: "female_intention",
                        rugWidth: 120,
                        rugRotation: 1.5
                    )
'''
if old not in s:
    raise SystemExit("v3.74: learning hero sitting-pose anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.74 prayer learning hero now uses standing intention poses")
