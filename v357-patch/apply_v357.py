from pathlib import Path

# SalahPath v3.57 FAST preview — Quran first-viewport parity only.
# UI-only during iteration: no version bump. Full release checkpoint comes
# after screenshot approval.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

q_start = s.index("struct QuranView: View {")
q_end = s.index("\nprivate struct QuranFavoritesView", q_start)
q = s[q_start:q_end]

card_start = q.index('                        VStack(alignment: .leading, spacing: 14) {')
search_start = q.index('                        HStack(spacing: 8) {', card_start)

new_card = r'''                        VStack(spacing: 0) {
                            VStack(alignment: .leading, spacing: 14) {
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
                            .padding(.top, 17)
                            .padding(.bottom, 8)
                            .frame(maxWidth: .infinity, maxHeight: .infinity)

                            Divider()
                                .opacity(0.25)
                                .padding(.horizontal, 8)

                            HStack(spacing: 0) {
                                quranAction(icon: "square.and.pencil", title: settings.t("Verse", "Ayetler"))
                                quranAction(icon: "play.circle", title: settings.t("Hören", "Dinle"))
                                NavigationLink {
                                    QuranFavoritesView(chapters: store.chapters)
                                } label: {
                                    quranAction(icon: "heart", title: settings.t("Favorit", "Favori"))
                                }
                                .buttonStyle(.plain)
                                quranAction(icon: "star", title: settings.t("Teilen", "Paylaş"))
                            }
                            .padding(.horizontal, 5)
                            .padding(.top, 3)
                            .padding(.bottom, 6)
                        }
                        .frame(maxWidth: .infinity)
                        .aspectRatio(0.56, contentMode: .fit)
                        .background(
                            SalahTheme.cream,
                            in: RoundedRectangle(cornerRadius: 10, style: .continuous)
                        )
                        .overlay {
                            RoundedRectangle(cornerRadius: 10, style: .continuous)
                                .stroke(SalahTheme.gold.opacity(0.40), lineWidth: 0.7)
                        }

'''

q = q[:card_start] + new_card + q[search_start:]
s = s[:q_start] + q + s[q_end:]
p.write_text(s, encoding="utf-8")

print("SalahPath v3.57 FAST Quran combined-card preview applied")
