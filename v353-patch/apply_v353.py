from pathlib import Path

# SalahPath v3.53 — Namaz first-viewport poster parity.
# The supplied lower-left phone shows only:
# tabs -> large seated prayer hero -> four learning points.
# Keep the deeper learning views in the project, but remove their extra launcher
# cards from this first screen and size the hero to fill the reference viewport.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

# Remove non-reference launchers from the GuideView first screen.
body_start = s.index("                NavigationLink { PrayerHowToView() }")
body_end_marker = '''            }
            .padding(.horizontal, 11)
            .padding(.vertical, 10)
'''
body_end = s.index(body_end_marker, body_start)
s = s[:body_start] + s[body_end:]

# Remove the poster-external "Männer/Frauen Lernmodus" promo from inside the app.
promo = '''            HStack(spacing: 7) {
                Image(systemName: "person.2.fill")
                    .font(.system(size: 12, weight: .bold))
                    .foregroundStyle(SalahTheme.teal)

                VStack(alignment: .leading, spacing: 1) {
                    Text("Männer/Frauen Lernmodus")
                        .font(.system(size: 9.4, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)
                    Text("Erkek-Kadın öğrenim modu")
                        .font(.system(size: 7.8, weight: .semibold))
                        .foregroundStyle(SalahTheme.mutedInk)
                }

                Spacer()

                Image(systemName: "chevron.right")
                    .font(.system(size: 9, weight: .black))
                    .foregroundStyle(SalahTheme.teal)
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 8)
            .background(SalahTheme.gold.opacity(0.12), in: RoundedRectangle(cornerRadius: 11, style: .continuous))
'''
if promo not in s:
    raise SystemExit("v3.53: Namaz promo block not found")
s = s.replace(promo, "", 1)

# Give the reference content the same visual weight as the poster phone.
replacements = [
    ('VStack(spacing: 6) {', 'VStack(spacing: 9) {', 1),
    ('.font(.system(size: 9.4, weight: .bold))', '.font(.system(size: 10.4, weight: .bold))', 1),
    ('.font(.system(size: 9.5, weight: .bold))', '.font(.system(size: 10.5, weight: .bold))', 1),
    ('.padding(.vertical, 7)', '.padding(.vertical, 8)', 1),
    ('.frame(height: 176)', '.frame(height: 300)', 1),
    ('VStack(alignment: .leading, spacing: 8) {', 'VStack(alignment: .leading, spacing: 11) {', 1),
    ('.font(.system(size: 13, weight: .semibold))', '.font(.system(size: 15, weight: .semibold))', 1),
    ('.font(.custom("AvenirNext-DemiBold", size: 10.3))', '.font(.custom("AvenirNext-DemiBold", size: 12.0))', 1),
    ('.font(.custom("AvenirNext-Medium", size: 8.1))', '.font(.custom("AvenirNext-Medium", size: 9.3))', 1),
]
for old, new, count in replacements:
    if s.count(old) < count:
        raise SystemExit(f"v3.53: expected token missing: {old}")
    s = s.replace(old, new, count)

# Add vertical breathing room to the four reference learning rows.
feature_end = '''            Spacer(minLength: 0)
        }
    }

    private func audiencePill'''
feature_new = '''            Spacer(minLength: 0)
        }
        .padding(.vertical, 4)
    }

    private func audiencePill'''
if feature_end not in s:
    raise SystemExit("v3.53: referenceLearnFeature tail not found")
s = s.replace(feature_end, feature_new, 1)

# Refine the v3.52 prayer-person helper: larger container, whole body visible,
# no scaleEffect overflow into the tabs.
helper_replacements = [
    ('let h: CGFloat = 48', 'let h: CGFloat = 64', 1),
    ('.frame(height: 58)', '.frame(height: 78)', 1),
    ('.frame(maxWidth: .infinity, maxHeight: 170)', '.frame(maxWidth: .infinity, maxHeight: 230)', 1),
    ('.scaleEffect(1.12, anchor: .bottom)\n', '', 1),
    ('.frame(maxWidth: .infinity, minHeight: 178, maxHeight: 178, alignment: .bottom)',
     '.frame(maxWidth: .infinity, minHeight: 286, maxHeight: 286, alignment: .bottom)', 1),
]
for old, new, count in helper_replacements:
    if s.count(old) < count:
        raise SystemExit(f"v3.53: prayer helper token missing: {old}")
    s = s.replace(old, new, count)

# Slightly narrower rugs, closer to the two distinct mats in the poster.
s = s.replace('rugWidth: 128,', 'rugWidth: 120,', 2)

p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.52"' not in t or 'CURRENT_PROJECT_VERSION="57"' not in t:
    raise SystemExit("v3.53: expected v3.52/57 build version not found")
t = t.replace('MARKETING_VERSION="3.52"', 'MARKETING_VERSION="3.53"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="57"', 'CURRENT_PROJECT_VERSION="58"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.53 Namaz first-viewport poster parity applied")
