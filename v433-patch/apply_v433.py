from pathlib import Path

app = Path("SalahZeit/SalahZeitApp.swift")
text = app.read_text(encoding="utf-8")

anchor = '''        case "wudu":
            NavigationStack { WuduGuideView() }
'''
replacement = '''        case "prayer-sequence":
            NavigationStack { PrayerSequenceReferenceView() }
        case "wudu":
            NavigationStack { WuduGuideView() }
'''
if anchor not in text:
    raise SystemExit("v433: Wudu QA route anchor missing")
if 'case "prayer-sequence":' in text:
    raise SystemExit("v433: prayer-sequence QA route already exists")

app.write_text(text.replace(anchor, replacement, 1), encoding="utf-8")
print("v433 applied: direct prayer-sequence screenshot QA route")
