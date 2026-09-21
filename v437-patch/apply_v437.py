from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
if not guide.is_file():
    raise SystemExit("v437: GuideView.swift missing")

# Compatibility checkpoint only. The old full-sheet restore depended on a
# repository payload that is no longer present. v436 already restores the
# legacy prayer artwork; v438 installs the user-approved prayer reference rows.
print("v437 compatibility checkpoint: prayer reference integration continues in v438")
