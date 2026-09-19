from pathlib import Path

# SalahPath v3.14: strict visual parity pass for Quran, Dua/Dhikr and Home copy.

p = Path("SalahZeit/Views/GuideView.swift")
s = p.read_text(encoding="utf-8")

start = s.index("struct DhikrView: View {")
end = s.index("\nprivate struct DhikrTextCard", start)
new = r'''struct DhikrView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var counter = 33
    @State private var section = 0

    var body: some View {
        ScrollView {
            VStack(spacing: 10) {
                Picker(settings.t("Bereich", "Bölüm"), selection: $section) {
                    Text(settings.t("Morgen", "Sabah")).tag(0)
                    Text(settings.t("Abend", "Akşam")).tag(1)
                    Text(settings.t("Täglich", "Günlük")).tag(2)
                    Text(settings.t("Spezial", "Özel")).tag(3)
                }
                .pickerStyle(.segmented)
                .padding(5)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 13).stroke(SalahTheme.gold.opacity(0.35), lineWidth: 1) }

                VStack(spacing: 9) {
                    Text("أَسْتَغْفِرُ اللّٰهَ")
                        .font(.system(size: 34, weight: .medium))
                        .foregroundStyle(SalahTheme.ink)
                        .padding(.top, 3)

                    Text("Estağfirullâh")
                        .font(.system(size: 15, weight: .bold))
                        .foregroundStyle(SalahTheme.ink)

                    Text(settings.t("Ich bitte Allah um Vergebung.", "Allah'tan bağışlanma dilerim."))
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(SalahTheme.mutedInk)

                    HStack(spacing: 19) {
                        Button { counter = max(0, counter - 1) } label: {
                            Image(systemName: "minus")
                                .font(.system(size: 18, weight: .bold))
                                .frame(width: 38, height: 38)
                                .background(SalahTheme.gold.opacity(0.15), in: Circle())
                        }
                        .buttonStyle(.plain)

                        Text("\(counter)")
                            .font(.system(size: 34, weight: .bold, design: .rounded).monospacedDigit())
                            .foregroundStyle(SalahTheme.deepTeal)
                            .frame(minWidth: 72)
                            .contentTransition(.numericText())

                        Button { counter += 1 } label: {
                            Image(systemName: "plus")
                                .font(.system(size: 18, weight: .bold))
                                .frame(width: 38, height: 38)
                                .background(SalahTheme.gold.opacity(0.15), in: Circle())
                        }
                        .buttonStyle(.plain)
                    }
                    .foregroundStyle(SalahTheme.teal)
                }
                .padding(.vertical, 18)
                .frame(maxWidth: .infinity)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 18, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.50), lineWidth: 1) }

                VStack(spacing: 0) {
                    dhikrReferenceRow(icon: "sunrise.fill", title: settings.t("Morgen- & Abend-Adhkar", "Sabah & Akşam Zikirleri")) {
                        MorningEveningAdhkarView()
                    }
                    dhikrReferenceRow(icon: "hands.sparkles.fill", title: settings.t("Tägliche Duas", "Günlük Dualar")) {
                        QuranicDuaLibraryView()
                    }
                    dhikrStaticRow(icon: "circle.grid.cross.fill", title: settings.t("Tasbih-Zähler", "Tesbih Sayacı"))
                    dhikrStaticRow(icon: "character.book.closed.fill", title: settings.t("Arabisch, Türkisch, Deutsch", "Arapça, Türkçe, Deutsch"))
                    dhikrStaticRow(icon: "speaker.wave.2.fill", title: settings.t("Mit Audio anhören", "Sesli dinleme"))
                }
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 17, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 17).stroke(SalahTheme.gold.opacity(0.38), lineWidth: 1) }
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 10)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Dua & Dhikr", "Dua & Zikir"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
    }

    private func dhikrReferenceRow<Destination: View>(icon: String, title: String, @ViewBuilder destination: () -> Destination) -> some View {
        NavigationLink(destination: destination()) {
            dhikrRowBody(icon: icon, title: title, chevron: true)
        }
        .buttonStyle(.plain)
    }

    private func dhikrStaticRow(icon: String, title: String) -> some View {
        dhikrRowBody(icon: icon, title: title, chevron: true)
    }

    private func dhikrRowBody(icon: String, title: String, chevron: Bool) -> some View {
        HStack(spacing: 9) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 15, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
            Image(systemName: icon)
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 20)
            Text(title)
                .font(.system(size: 12, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer()
            if chevron {
                Image(systemName: "chevron.right")
                    .font(.caption.bold())
                    .foregroundStyle(SalahTheme.teal)
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 11)
        .contentShape(Rectangle())
        .overlay(alignment: .bottom) { Divider().padding(.leading, 55).opacity(0.35) }
    }
}
'''
s = s[:start] + new + s[end:]

start = s.index("struct QuranView: View {")
end = s.index("\nprivate struct QuranFavoritesView", start)
newq = r'''struct QuranView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()
    @State private var languageTab = 0
    @State private var search = ""

    var body: some View {
        Group {
            if store.isLoading && store.chapters.isEmpty {
                ProgressView(settings.t("Quran wird geladen…", "Kur'an yükleniyor…"))
            } else if let error = store.error, store.chapters.isEmpty {
                ContentUnavailableView(
                    settings.t("Quran konnte nicht geladen werden", "Kur'an yüklenemedi"),
                    systemImage: "wifi.exclamationmark",
                    description: Text(error)
                )
            } else {
                ScrollView {
                    VStack(spacing: 10) {
                        Picker(settings.t("Sprache", "Dil"), selection: $languageTab) {
                            Text(settings.t("Arabisch", "Arapça")).tag(0)
                            Text(settings.t("Türkisch", "Türkçe")).tag(1)
                            Text("Deutsch").tag(2)
                        }
                        .pickerStyle(.segmented)
                        .padding(5)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 13).stroke(SalahTheme.gold.opacity(0.35), lineWidth: 1) }

                        VStack(alignment: .leading, spacing: 11) {
                            Text("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ")
                                .font(.system(size: 27, weight: .medium))
                                .frame(maxWidth: .infinity, alignment: .trailing)
                                .foregroundStyle(SalahTheme.ink)

                            Text("1.")
                                .font(.system(size: 12, weight: .bold))
                                .foregroundStyle(SalahTheme.teal)

                            if languageTab == 0 {
                                Text("الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ")
                                    .font(.system(size: 24, weight: .medium))
                                    .frame(maxWidth: .infinity, alignment: .trailing)
                            } else if languageTab == 1 {
                                Text("Rahmân ve Rahîm olan Allah'ın adıyla.")
                                    .font(.system(size: 14, weight: .semibold))
                                    .foregroundStyle(SalahTheme.ink)
                            } else {
                                Text("Im Namen Allahs, des Allerbarmers, des Barmherzigen.")
                                    .font(.system(size: 14, weight: .semibold))
                                    .foregroundStyle(SalahTheme.ink)
                            }

                            VStack(spacing: 5) {
                                HStack {
                                    Text("0:00")
                                    Spacer()
                                    Text("0:45")
                                }
                                .font(.system(size: 8.5, weight: .semibold).monospacedDigit())
                                .foregroundStyle(SalahTheme.mutedInk)

                                ZStack(alignment: .leading) {
                                    Capsule().fill(SalahTheme.teal.opacity(0.14)).frame(height: 3)
                                    Capsule().fill(SalahTheme.teal).frame(width: 78, height: 3)
                                }
                            }

                            HStack(spacing: 22) {
                                Image(systemName: "backward.end.fill")
                                ZStack {
                                    Circle().fill(SalahTheme.deepTeal).frame(width: 48, height: 48)
                                    Image(systemName: "play.fill").foregroundStyle(.white)
                                }
                                Image(systemName: "forward.end.fill")
                                Spacer()
                                Text("1.0x")
                                    .font(.system(size: 10, weight: .bold))
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 5)
                                    .background(SalahTheme.softTeal, in: Capsule())
                            }
                            .foregroundStyle(SalahTheme.teal)
                        }
                        .padding(14)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 18, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.50), lineWidth: 1) }

                        HStack(spacing: 7) {
                            quranAction(icon: "text.book.closed.fill", title: settings.t("Verse", "Ayetler"))
                            quranAction(icon: "play.circle.fill", title: settings.t("Hören", "Dinle"))
                            NavigationLink {
                                QuranFavoritesView(chapters: store.chapters)
                            } label: {
                                quranAction(icon: "heart.fill", title: settings.t("Favorit", "Favori"))
                            }
                            .buttonStyle(.plain)
                            quranAction(icon: "square.and.arrow.up", title: settings.t("Teilen", "Paylaş"))
                        }

                        HStack(spacing: 8) {
                            Image(systemName: "magnifyingglass")
                                .foregroundStyle(SalahTheme.teal)
                            TextField(settings.t("Sura suchen", "Sure ara"), text: $search)
                                .textInputAutocapitalization(.never)
                                .autorrectionDisabled()
                        }
                        .padding(.horizontal, 12)
                        .frame(height: 42)
                        .background(Color.white.opacity(0.76), in: RoundedRectangle(cornerRadius: 13, style: .continuous))

                        ForEach(filtered.prefix(8)) { surah in
                            NavigationLink {
                                QuranSurahView(surah: surah, initialAyah: nil)
                            } label: {
                                HStack(spacing: 10) {
                                    Text("\(surah.number)")
                                        .font(.caption.bold())
                                        .foregroundStyle(SalahTheme.deepTeal)
                                        .frame(width: 32, height: 32)
                                        .background(SalahTheme.gold.opacity(0.20), in: Circle())
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(surah.englishName)
                                            .font(.system(size: 13, weight: .bold))
                                            .foregroundStyle(SalahTheme.ink)
                                        Text("\(surah.numberOfAyahs) \(settings.t("Verse", "ayet"))")
                                            .font(.caption2)
                                            .foregroundStyle(SalahTheme.mutedInk)
                                    }
                                    Spacer()
                                    Text(surah.name)
                                        .font(.system(size: 19, weight: .medium))
                                        .foregroundStyle(SalahTheme.ink)
                                    Image(systemName: "chevron.right")
                                        .font(.caption.bold())
                                        .foregroundStyle(SalahTheme.teal)
                                }
                                .padding(10)
                                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                                .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.teal.opacity(0.14), lineWidth: 1) }
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal, 11)
                    .padding(.vertical, 10)
                }
                .scrollIndicators(.hidden)
            }
        }
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Quran", "Kur'an"))
        .navigationBarTitleDisplayMode(.inline)
        .task { await store.loadChapters() }
        .tint(SalahTheme.teal)
    }

    private func quranAction(icon: String, title: String) -> some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .font(.system(size: 17, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
            Text(title)
                .font(.system(size: 8.5, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
                .lineLimit(1)
        }
        .frame(maxWidth: .infinity, minHeight: 52)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 13, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 13).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
    }

    private var filtered: [SurahMeta] {
        guard !search.isEmpty else { return store.chapters }
        return store.chapters.filter {
            $0.englishName.localizedCaseInsensitiveContains(search) ||
            $0.englishNameTranslation.localizedCaseInsensitiveContains(search) ||
            $0.name.contains(search) ||
            String($0.number) == search
        }
    }
}
'''
# correct modifier spelling in generated block
newq = newq.replace(".autorrectionDisabled()", ".autocorrectionDisabled()")
s = s[:start] + newq + s[end:]
p.write_text(s, encoding="utf-8")

p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")
s = s.replace(
    'Text(settings.t("Nächstes Gebet", "Sıradaki Namaz"))\n                        .font(.system(size: 13, weight: .bold))',
    'Text(settings.t("Sıradaki Namaz / Nächstes Gebet", "Sıradaki Namaz / Nächstes Gebet"))\n                        .font(.system(size: 13, weight: .bold))'
)
s = s.replace(
    'Text(settings.t("Vakit / Gebetszeit", "Nächstes Gebet"))\n                        .font(.system(size: 9.5, weight: .semibold))\n                        .foregroundStyle(SalahTheme.mutedInk)',
    'EmptyView()'
)
s = s.replace(
    'Text(settings.t("Glaube. Wissen. Gebet.", "İbadetle Daha Güzel Bir Hayat"))',
    'Text(settings.t("İbadetle Daha Güzel Bir Hayat", "İbadetle Daha Güzel Bir Hayat"))'
)
s = s.replace(
    'DashboardTile(title: settings.t("Qur\'an lesen", "Kur\'an Oku"), subtitle: settings.t("& hören", "& Dinle"), icon: "book.fill")',
    'DashboardTile(title: settings.t("Qur\'an", "Kur\'an"), subtitle: settings.t("Lesen & Hören", "Oku & Dinle"), icon: "book.fill")'
)
s = s.replace(
    'DashboardTile(title: settings.t("Qibla-Richtung", "Kıble Yönü"), subtitle: settings.t("Kompass", "Kıble"), icon: "location.north.circle.fill")',
    'DashboardTile(title: settings.t("Qibla-Richtung", "Kıble Yönü"), subtitle: "Qibla", icon: "location.north.circle.fill")'
)
p.write_text(s, encoding="utf-8")

p = Path("scripts/build_unsigned_ipa.sh")
s = p.read_text(encoding="utf-8")
s = s.replace('MARKETING_VERSION="3.13"', 'MARKETING_VERSION="3.14"')
s = s.replace('CURRENT_PROJECT_VERSION="18"', 'CURRENT_PROJECT_VERSION="19"')
p.write_text(s, encoding="utf-8")

print("SalahPath v3.14 strict reference parity patch applied")
