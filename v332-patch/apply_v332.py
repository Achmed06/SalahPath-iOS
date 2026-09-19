from pathlib import Path

# SalahPath v3.32 — fix SwiftUI modifier order causing invisible hero padding.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# v3.31 proved the main geometry issue: hero minHeight was applied AFTER the
# background, so SwiftUI centered a smaller painted card inside a taller invisible
# frame. This created the large teal gaps above and below the prayer card.
s = s.replace(
'''            .padding(.horizontal, 7)
            .padding(.top, -37)
            .padding(.bottom, 4)
''',
'''            .padding(.horizontal, 7)
            .padding(.top, -7)
            .padding(.bottom, 4)
''', 1)

# Move the hero frame before background/overlay so the cream card actually fills
# its intended height. 200 pt is the normalized reference proportion for this device.
old = '''            .padding(.horizontal, 8)
            .padding(.vertical, 7)
        }
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.66), lineWidth: 0.8)
        }
        .shadow(color: SalahTheme.deepTeal.opacity(0.025), radius: 2, y: 1)
        .frame(minHeight: 246)
        .clipped()
'''
new = '''            .padding(.horizontal, 8)
            .padding(.vertical, 7)
        }
        .frame(minHeight: 200)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.66), lineWidth: 0.8)
        }
        .shadow(color: SalahTheme.deepTeal.opacity(0.025), radius: 2, y: 1)
        .clipped()
'''
if old not in s:
    raise SystemExit("hero modifier-order target not found")
s = s.replace(old, new, 1)

# Slightly reduce the mosque after the card itself now fills the full reference height.
s = s.replace('.frame(width: 198, height: 128)', '.frame(width: 190, height: 121)', 1)
s = s.replace('.offset(x: 7, y: -7)', '.offset(x: 5, y: -5)', 1)

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.31"', 'MARKETING_VERSION="3.32"')
t = t.replace('CURRENT_PROJECT_VERSION="36"', 'CURRENT_PROJECT_VERSION="37"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.32 hero modifier-order geometry fix applied")
