from pathlib import Path

# SalahPath v3.22: fix v3.20 streak literal so the strict parity branch compiles.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")
broken = '''                Text(settings.language == .german ? "Günlük Seri
Tage in Folge" : "Günlük Seri
Tage in Folge")
'''
fixed = '''                Text("Günlük Seri\\nTage in Folge")
'''
if broken not in s:
    raise SystemExit("Broken streak literal not found")
s = s.replace(broken, fixed, 1)
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.21"', 'MARKETING_VERSION="3.22"')
t = t.replace('CURRENT_PROJECT_VERSION="26"', 'CURRENT_PROJECT_VERSION="27"')
b.write_text(t, encoding="utf-8")
print("SalahPath v3.22 compile hotfix applied")
