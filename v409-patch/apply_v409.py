from pathlib import Path

app = Path("SalahZeit/SalahZeitApp.swift")
text = app.read_text(encoding="utf-8")

anchor = '''        case "wudu":
            NavigationStack { WuduGuideView() }
        case "tracker":
'''
replacement = '''        case "wudu":
            NavigationStack { WuduGuideView() }
        case "ghusl":
            NavigationStack { GhuslGuideView() }
        case "tayammum":
            NavigationStack { TayammumGuideView() }
        case "tracker":
'''
if anchor not in text:
    raise SystemExit("v409: Wudu QA route anchor missing")
app.write_text(text.replace(anchor, replacement, 1), encoding="utf-8")
print("v409 applied: QA routes for Ghusl and Tayammum")
