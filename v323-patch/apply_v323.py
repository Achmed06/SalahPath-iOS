from pathlib import Path

# SalahPath v3.23: strict Dua & Zikir parity pass.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

start = s.index("struct DhikrView: View {")
end = s.index("\nprivate struct DhikrTextCard", start)

new = r'''struct DhikrView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var counter = 33
    @State private var section = 0

    private var tabs: [String] { ["Sabah", "Akşam", "Günlük", "Özel"] }

    var body: some View {
        ScrollView {
            VStack(spacing: 9) {
                HStack {
                    HStack(spacing: 7) {
                        Image(systemName: "hands.sparkles.fill")
                            .font(.system(size: 15, weight: .semibold))
                            .foregroundStyle(SalahTheme.teal)
                        Text("Dua & Zikir")
                            .font(.system(size: 17, weight: .bold, design: .serif))
                            .foregroundStyle(SalahTheme.ink)
                    }
                    Spacer()
                    Image(systemName: "ellipsis.circle")
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundStyle(SalahTheme.teal)
                }
                .padding(.horizontal, 3)

                HStack(spacing: 4) {
                    ForEach(Array(tabs.enumerated()), id: \.offset) { index, title in
                        Button {
                            withAnimation(.easeOut(duration: 0.15)) {
                                section = index
                            }
                        } label: {
                            Text(title)
                                .font(.system(size: 9.5, weight: .bold))
                                .foregroundStyle(section == index ? .white : SalahTheme.deepTeal)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 7)
                                .background(
                                    section == index ? SalahTheme.teal : Color.clear,
                                    in: RoundedRectangle(cornerRadius: 8, style: .continuous)
                                )
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(4)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 12).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }

                VStack(spacing: 10) {
                    HStack(spacing: 7) {
                        Rectangle()
                            .fill(SalahTheme.gold.opacity(0.38))
                            .frame(height: 1)
                        Image(systemName: "circle.grid.cross.fill")
                            .font(.system(size: 9, weight: .semibold))
                            .foregroundStyle(SalahTheme.gold)
                        Rectangle()
                            .fill(SalahTheme.gold.opacity(0.38))
                            .frame(height: 1)
                    }

                    Text("أَسْتَغْفِرُ اللّٰهَ")
                        .font(.system(size: 33, weight: .medium))
                        .foregroundStyle(SalahTheme.ink)
                        .frame(maxWidth: .infinity)

                    Text("Estağfirullâh")
                        .font(.system(size: 14.5, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)

                    Text(settings.t("Ich bitte Allah um Vergebung.", "Allah'tan bağışlanma dilerim."))
                        .font(.system(size: 10.5, weight: .medium))
                        .foregroundStyle(SalahTheme.mutedInk)
                        .multilineTextAlignment(.center)

                    HStack(spacing: 18) {
                        Button {
                            if counter > 0 { counter -= 1 }
                        } label: {
                            Image(systemName: "minus")
                                .font(.system(size: 16, weight: .bold))
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 36, height: 36)
                                .background(SalahTheme.gold.opacity(0.15), in: Circle())
                                .overlay { Circle().stroke(SalahTheme.gold.opacity(0.36), lineWidth: 1) }
                        }
                        .buttonStyle(.plain)

                        VStack(spacing: 1) {
                            Text("\(counter)")
                                .font(.system(size: 34, weight: .bold, design: .rounded).monospacedDigit())
                                .foregroundStyle(SalahTheme.deepTeal)
                                .contentTransition(.numericText())
                            Text(settings.t("Zähler", "Sayaç"))
                                .font(.system(size: 7.7, weight: .bold))
                                .foregroundStyle(SalahTheme.mutedInk)
                        }
                        .frame(minWidth: 78)

                        Button {
                            counter += 1
                        } label: {
                            Image(systemName: "plus")
                                .font(.system(size: 16, weight: .bold))
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 36, height: 36)
                                .background(SalahTheme.gold.opacity(0.15), in: Circle())
                                .overlay { Circle().stroke(SalahTheme.gold.opacity(0.36), lineWidth: 1) }
                        }
                        .buttonStyle(.plain)
                    }

                    Button {
                        counter = 33
                    } label: {
                        Label(settings.t("Zurücksetzen", "Sıfırla"), systemImage: "arrow.counterclockwise")
                            .font(.system(size: 8.2, weight: .bold))
                            .foregroundStyle(SalahTheme.teal)
                    }
                    .buttonStyle(.plain)
                }
                .padding(.horizontal, 13)
                .padding(.vertical, 13)
                .frame(maxWidth: .infinity)
                .background(
                    LinearGradient(
                        colors: [SalahTheme.cream, Color.white.opacity(0.82)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    in: RoundedRectangle(cornerRadius: 16, style: .continuous)
                )
                .overlay { RoundedRectangle(cornerRadius: 16).stroke(SalahTheme.gold.opacity(0.55), lineWidth: 1) }
                .shadow(color: SalahTheme.deepTeal.opacity(0.045), radius: 5, y: 2)

                VStack(spacing: 0) {
                    dhikrReferenceRow(
                        icon: "sunrise.fill",
                        title: "Sabah & Akşam Zikirleri",
                        subtitle: settings.t("Morgen- & Abend-Adhkar", "Sabah ve akşam")
                    ) {
                        MorningEveningAdhkarView()
                    }

                    dhikrReferenceRow(
                        icon: "hands.sparkles.fill",
                        title: "Günlük Dualar",
                        subtitle: settings.t("Tägliche Duas", "Günlük dualar")
                    ) {
                        QuranicDuaLibraryView()
                    }

                    dhikrStaticRow(
                        icon: "circle.grid.cross.fill",
                        title: "Tesbih Sayacı",
                        subtitle: settings.t("Tasbih-Zähler", "Tesbih sayacı")
                    )

                    dhikrStaticRow(
                        icon: "character.book.closed.fill",
                        title: "Arapça, Türkçe, Deutsch",
                        subtitle: settings.t("Dreisprachige Begleitung", "Üç dilde kullanım")
                    )

                    dhikrStaticRow(
                        icon: "speaker.wave.2.fill",
                        title: "Sesli dinleme",
                        subtitle: settings.t("Mit Audio anhören", "Sesli dinleme")
                    )
                }
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }

                HStack(spacing: 7) {
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 9, weight: .bold))
                        .foregroundStyle(SalahTheme.gold)
                    Text(settings.t(
                        "Beständigkeit ist der Schlüssel.",
                        "İstikrar başarının anahtarıdır."
                    ))
                    .font(.system(size: 9.2, weight: .bold, design: .serif))
                    .foregroundStyle(SalahTheme.deepTeal)
                    Spacer()
                }
                .padding(.horizontal, 11)
                .padding(.vertical, 8)
                .background(SalahTheme.gold.opacity(0.12), in: RoundedRectangle(cornerRadius: 12))
            }
            .padding(.horizontal, 11)
            .padding(.vertical, 9)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle("Dua & Zikir")
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }

    private func dhikrReferenceRow<Destination: View>(
        icon: String,
        title: String,
        subtitle: String,
        @ViewBuilder destination: () -> Destination
    ) -> some View {
        NavigationLink(destination: destination()) {
            dhikrRowBody(icon: icon, title: title, subtitle: subtitle)
        }
        .buttonStyle(.plain)
    }

    private func dhikrStaticRow(icon: String, title: String, subtitle: String) -> some View {
        dhikrRowBody(icon: icon, title: title, subtitle: subtitle)
    }

    private func dhikrRowBody(icon: String, title: String, subtitle: String) -> some View {
        HStack(spacing: 9) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 14, weight: .bold))
                .foregroundStyle(SalahTheme.teal)

            Image(systemName: icon)
                .font(.system(size: 13.5, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 20)

            VStack(alignment: .leading, spacing: 1) {
                Text(title)
                    .font(.system(size: 11.5, weight: .bold))
                    .foregroundStyle(SalahTheme.ink)
                Text(subtitle)
                    .font(.system(size: 8.3, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
            }

            Spacer()

            Image(systemName: "chevron.right")
                .font(.system(size: 9, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
        }
        .padding(.horizontal, 11)
        .padding(.vertical, 9)
        .contentShape(Rectangle())
        .overlay(alignment: .bottom) {
            Divider()
                .padding(.leading, 53)
                .opacity(0.34)
        }
    }
}
'''

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.22"', 'MARKETING_VERSION="3.23"')
t = t.replace('CURRENT_PROJECT_VERSION="27"', 'CURRENT_PROJECT_VERSION="28"')
b.write_text(t, encoding="utf-8")
print("SalahPath v3.23 Dua & Zikir strict parity pass applied")
