from pathlib import Path

app = Path("SalahZeit/SalahZeitApp.swift")
text = app.read_text(encoding="utf-8")

anchor = '''        case "fasting":
            NavigationStack { FastingTrackerView() }
        case "hijri":
            NavigationStack { HijriCalendarView() }
'''
replacement = '''        case "fasting":
            NavigationStack { FastingTrackerView() }
        case "fasting-basics":
            NavigationStack { FastingBasicsView() }
        case "fasting-rules":
            NavigationStack { FastingRulesView() }
        case "fasting-exceptions":
            NavigationStack { FastingExceptionsView() }
        case "islam-learning":
            NavigationStack { IslamLearningHubView() }
        case "hijri":
            NavigationStack { HijriCalendarView() }
'''
if anchor not in text:
    raise SystemExit("v406: QA fasting/hijri route anchor missing")
app.write_text(text.replace(anchor, replacement, 1), encoding="utf-8")

print("v406 applied: QA routes for Islam learning and detailed fasting screens")
