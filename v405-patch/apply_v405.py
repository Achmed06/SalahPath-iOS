from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = "Bu kurs düzenli bir başlangıçtır; yıllar süren kapsamlı din eğitimini ersetzen etmez."
new = "Bu kurs düzenli bir başlangıçtır; yıllar süren kapsamlı din eğitiminin yerini tutmaz."
if old not in text:
    raise SystemExit("v405: Turkish Islam-learning wording anchor missing")
text = text.replace(old, new, 1)
guide.write_text(text, encoding="utf-8")
print("v405 applied: Turkish Islam-learning copy corrected")
