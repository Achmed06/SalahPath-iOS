from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

for name in ["FastingBasicsView", "FastingRulesView", "FastingExceptionsView"]:
    old = f"private struct {name}: View {{"
    new = f"struct {name}: View {{"
    if old not in text:
        raise SystemExit(f"v407: {name} private declaration anchor missing")
    text = text.replace(old, new, 1)

guide.write_text(text, encoding="utf-8")
print("v407 applied: fasting detail views exposed to QA router")
