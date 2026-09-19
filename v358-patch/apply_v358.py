from pathlib import Path

# SalahPath v3.58 FAST preview — Dhikr vertical poster proportions only.
# UI-only during iteration; keep counter and navigation behavior unchanged.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

start = s.index("struct DhikrView: View {")
end = s.index("\nprivate struct DhikrTextCard", start)
d = s[start:end]

if '.aspectRatio(1.42, contentMode: .fit)' not in d:
    raise SystemExit("v3.58: Dhikr hero aspect anchor missing")
d = d.replace(
    '.aspectRatio(1.42, contentMode: .fit)',
    '.aspectRatio(1.18, contentMode: .fit)',
    1
)

row_anchor = '''        .padding(.horizontal, 12)
        .padding(.vertical, 12)
        .contentShape(Rectangle())
'''
row_new = '''        .padding(.horizontal, 12)
        .padding(.vertical, 22)
        .contentShape(Rectangle())
'''
if row_anchor not in d:
    raise SystemExit("v3.58: Dhikr row padding anchor missing")
d = d.replace(row_anchor, row_new, 1)

s = s[:start] + d + s[end:]
p.write_text(s, encoding="utf-8")

print("SalahPath v3.58 FAST Dhikr vertical proportions applied")
