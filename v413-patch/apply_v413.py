from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = "Latin harfli okunuş yalnız öğrenme yardımıdır; doğru Arapça okumayı kalıcı olarak ersetzen etmez."
new = "Latin harfli okunuş yalnız öğrenme yardımıdır; doğru Arapça okumanın kalıcı olarak yerini tutmaz."
if old not in text:
    raise SystemExit("v413: remaining Turkish mixed-language Quran lesson anchor missing")
text = text.replace(old, new, 1)
guide.write_text(text, encoding="utf-8")
print("v413 applied: remaining Turkish mixed-language Quran lesson corrected")
