from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

old = '''            VStack(alignment: .leading, spacing: 1) {
                Text(turkish)
                    .font(.custom("AvenirNext-DemiBold", size: 12.0))
                    .foregroundStyle(SalahTheme.ink)
                Text(german)
                    .font(.custom("AvenirNext-Medium", size: 9.3))
                    .foregroundStyle(SalahTheme.mutedInk)
            }
'''
new = '''            Text(settings.language == .german ? german : turkish)
                .font(.custom("AvenirNext-DemiBold", size: 12.0))
                .foregroundStyle(SalahTheme.ink)
                .fixedSize(horizontal: false, vertical: true)
'''
if old not in s:
    raise SystemExit("v3.81: bilingual prayer feature anchor missing")
s = s.replace(old, new, 1)

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.81 prayer learning feature copy follows app language")
