from pathlib import Path

# SalahPath v3.50 — Quran reference-phone proportion pass.
# The poster's Quran screen is dominated by one tall audio/ayah card. Rebuild
# that top composition with the same tall aspect ratio so search/list content
# naturally sits below the initial viewport instead of being hidden by QA hacks.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

q_start = s.index("struct QuranView: View {")
q_end = s.index("\nprivate struct QuranFavoritesView", q_start)
q = s[q_start:q_end]

# Reference segmented control is more legible and vertically stronger.
q = q.replace(
    '.font(.custom("AvenirNext-DemiBold", size: 8.8))',
    '.font(.custom("AvenirNext-DemiBold", size: 11.2))',
    1
)
q = q.replace('.padding(.vertical, 5)', '.padding(.vertical, 7)', 1)

card_start = q.index('                        VStack(alignment: .leading, spacing: 12) {')
card_end = q.index('\n                        HStack(spacing: 0) {', card_start)

new_card = r'''                        VStack(alignment: .leading, spacing: 14) {
                            Text("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ")
                                .font(.system(size: 29, weight: .regular))
                                .frame(maxWidth: .infinity, alignment: .trailing)
                                .foregroundStyle(SalahTheme.ink)

                            Text("1. Bismillâhirrahmânirrahîm")
                                .font(.custom("AvenirNext-DemiBold", size: 14.2))
                                .foregroundStyle(SalahTheme.ink)

                            if languageTab != 2 {
                                Text("Rahmân ve Rahîm olan Allah'ın adıyla.")
                                    .font(.custom("AvenirNext-Medium", size: 13.2))
                                    .foregroundStyle(SalahTheme.ink)
                                    .fixedSize(horizontal: false, vertical: true)
                            }

                            if languageTab != 1 {
                                Text("Im Namen Allahs, des Allerbarmers, des Barmherzigen.")
                                    .font(.custom("AvenirNext-Medium", size: 13.2))
                                    .foregroundStyle(SalahTheme.ink)
                                    .fixedSize(horizontal: false, vertical: true)
                            }

                            Spacer(minLength: 18)

                            VStack(spacing: 7) {
                                HStack {
                                    Text("0:00")
                                    Spacer()
                                    Text("0:45")
                                }
                                .font(.system(size: 10.5, weight: .semibold).monospacedDigit())
                                .foregroundStyle(SalahTheme.mutedInk)

                                ZStack(alignment: .leading) {
                                    Capsule()
                                        .fill(SalahTheme.teal.opacity(0.14))
                                        .frame(height: 3.5)
                                    Capsule()
                                        .fill(SalahTheme.teal)
                                        .frame(width: 104, height: 3.5)
                                }
                            }

                            HStack(spacing: 24) {
                                Image(systemName: "backward.end.fill")
                                    .font(.system(size: 17, weight: .semibold))

                                ZStack {
                                    Circle()
                                        .fill(SalahTheme.deepTeal)
                                        .frame(width: 54, height: 54)
                                    Image(systemName: "play.fill")
                                        .font(.system(size: 18, weight: .semibold))
                                        .foregroundStyle(.white)
                                }

                                Image(systemName: "forward.end.fill")
                                    .font(.system(size: 17, weight: .semibold))

                                Spacer()

                                Text("1.0x")
                                    .font(.system(size: 11.5, weight: .bold))
                                    .padding(.horizontal, 9)
                                    .padding(.vertical, 6)
                                    .background(SalahTheme.softTeal, in: Capsule())
                            }
                            .foregroundStyle(SalahTheme.teal)
                        }
                        .padding(.horizontal, 15)
                        .padding(.vertical, 17)
                        .frame(maxWidth: .infinity)
                        .aspectRatio(0.72, contentMode: .fit)
                        .background(
                            SalahTheme.cream,
                            in: RoundedRectangle(cornerRadius: 10, style: .continuous)
                        )
                        .overlay {
                            RoundedRectangle(cornerRadius: 10, style: .continuous)
                                .stroke(SalahTheme.gold.opacity(0.40), lineWidth: 0.7)
                        }
'''

q = q[:card_start] + new_card + q[card_end:]

# Poster action strip has larger outlined icons and labels.
q = q.replace(
    '.font(.system(size: 15, weight: .medium))',
    '.font(.system(size: 17, weight: .medium))',
    1
)
q = q.replace(
    '.font(.custom("AvenirNext-DemiBold", size: 7.7))',
    '.font(.custom("AvenirNext-DemiBold", size: 9.2))',
    1
)
q = q.replace(
    '.frame(maxWidth: .infinity, minHeight: 45)',
    '.frame(maxWidth: .infinity, minHeight: 58)',
    1
)

s = s[:q_start] + q + s[q_end:]
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
if 'MARKETING_VERSION="3.49"' not in t or 'CURRENT_PROJECT_VERSION="54"' not in t:
    raise SystemExit("v3.50: expected v3.49/54 build version not found")
t = t.replace('MARKETING_VERSION="3.49"', 'MARKETING_VERSION="3.50"', 1)
t = t.replace('CURRENT_PROJECT_VERSION="54"', 'CURRENT_PROJECT_VERSION="55"', 1)
b.write_text(t, encoding="utf-8")

print("SalahPath v3.50 Quran reference-phone proportions applied")
