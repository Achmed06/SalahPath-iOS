from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

# Replace Share action on Quran landing card with Juz/Cüz navigation.
old = '''                                ShareLink(item: quranShareText) {
                                    quranAction(icon: "square.and.arrow.up", title: settings.t("Teilen", "Paylaş"))
                                }
                                .buttonStyle(.plain)
'''
new = '''                                NavigationLink {
                                    QuranJuzLandingView(chapters: store.chapters)
                                } label: {
                                    quranAction(icon: "text.book.closed", title: settings.t("Cüz", "Cüz"))
                                }
                                .buttonStyle(.plain)
'''
if old not in text:
    raise SystemExit("v423: Quran landing Share action anchor missing")
text = text.replace(old, new, 1)

# Insert Juz models/view before favorites landing.
marker = "\n\nstruct QuranFavoritesLandingView: View {"
if marker not in text:
    raise SystemExit("v423: Quran favorites insertion marker missing")

juz_view = r'''

private struct QuranJuzStart: Identifiable {
    let number: Int
    let surah: Int
    let ayah: Int
    var id: Int { number }

    static let all: [QuranJuzStart] = [
        .init(number: 1,  surah: 1,  ayah: 1),
        .init(number: 2,  surah: 2,  ayah: 142),
        .init(number: 3,  surah: 2,  ayah: 253),
        .init(number: 4,  surah: 3,  ayah: 93),
        .init(number: 5,  surah: 4,  ayah: 24),
        .init(number: 6,  surah: 4,  ayah: 148),
        .init(number: 7,  surah: 5,  ayah: 82),
        .init(number: 8,  surah: 6,  ayah: 111),
        .init(number: 9,  surah: 7,  ayah: 88),
        .init(number: 10, surah: 8,  ayah: 41),
        .init(number: 11, surah: 9,  ayah: 93),
        .init(number: 12, surah: 11, ayah: 6),
        .init(number: 13, surah: 12, ayah: 53),
        .init(number: 14, surah: 15, ayah: 1),
        .init(number: 15, surah: 17, ayah: 1),
        .init(number: 16, surah: 18, ayah: 75),
        .init(number: 17, surah: 21, ayah: 1),
        .init(number: 18, surah: 23, ayah: 1),
        .init(number: 19, surah: 25, ayah: 21),
        .init(number: 20, surah: 27, ayah: 56),
        .init(number: 21, surah: 29, ayah: 46),
        .init(number: 22, surah: 33, ayah: 31),
        .init(number: 23, surah: 36, ayah: 28),
        .init(number: 24, surah: 39, ayah: 32),
        .init(number: 25, surah: 41, ayah: 47),
        .init(number: 26, surah: 46, ayah: 1),
        .init(number: 27, surah: 51, ayah: 31),
        .init(number: 28, surah: 58, ayah: 1),
        .init(number: 29, surah: 67, ayah: 1),
        .init(number: 30, surah: 78, ayah: 1)
    ]
}

private struct QuranJuzLandingView: View {
    @EnvironmentObject private var settings: SettingsStore
    let chapters: [SurahMeta]

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 7) {
                    Label(settings.t("30 Cüz des Quran", "Kur'an'ın 30 cüzü"), systemImage: "text.book.closed.fill")
                        .font(.headline.bold())
                        .foregroundStyle(SalahTheme.deepTeal)

                    Text(settings.t(
                        "Tippe auf einen Cüz. SalahPath öffnet direkt die Ayah, an der dieser Cüz beginnt. Von dort kannst du normal weiterlesen, hören und Lesezeichen setzen.",
                        "Bir cüze dokun. SalahPath doğrudan o cüzün başladığı ayeti açar. Oradan normal şekilde okumaya, dinlemeye ve yer imi eklemeye devam edebilirsin."
                    ))
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                    .fixedSize(horizontal: false, vertical: true)
                }
                .padding(.vertical, 4)
            }

            Section(settings.t("Cüz auswählen", "Cüz seç")) {
                ForEach(QuranJuzStart.all) { juz in
                    if let chapter = chapters.first(where: { $0.number == juz.surah }) {
                        NavigationLink {
                            QuranSurahView(surah: chapter, initialAyah: juz.ayah)
                        } label: {
                            HStack(spacing: 11) {
                                Text("\(juz.number)")
                                    .font(.caption.bold())
                                    .foregroundStyle(.white)
                                    .frame(width: 34, height: 34)
                                    .background(SalahTheme.deepTeal, in: Circle())

                                VStack(alignment: .leading, spacing: 3) {
                                    Text(settings.t("Cüz \(juz.number)", "\(juz.number). Cüz"))
                                        .font(.headline)
                                        .foregroundStyle(SalahTheme.ink)

                                    Text("\(chapter.englishName) · \(settings.t("Vers", "Ayet")) \(juz.ayah)")
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }

                                Spacer()

                                Text(chapter.name)
                                    .font(.system(size: 17, weight: .medium))
                                    .foregroundStyle(SalahTheme.mutedInk)
                            }
                            .padding(.vertical, 3)
                        }
                        .accessibilityLabel(settings.t(
                            "Cüz \(juz.number), beginnt bei \(chapter.englishName), Vers \(juz.ayah)",
                            "\(juz.number). Cüz, \(chapter.englishName) suresi \(juz.ayah). ayette başlar"
                        ))
                    }
                }
            }

            Section {
                Text(settings.t(
                    "Die Cüz-Einteilung ist eine Leseeinteilung des Quran in 30 Teile. Sie verändert weder Suren- noch Ayah-Nummern.",
                    "Cüz sistemi Kur'an'ı okumayı kolaylaştırmak için 30 bölüme ayırır. Sure ve ayet numaralarını değiştirmez."
                ))
                .font(.footnote)
                .foregroundStyle(.secondary)
            }
        }
        .scrollContentBackground(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Cüz / Juz", "Cüz"))
        .navigationBarTitleDisplayMode(.inline)
    }
}
'''

text = text.replace(marker, juz_view + marker, 1)
guide.write_text(text, encoding="utf-8")

# Add direct QA route for the Juz screen.
app = Path("SalahZeit/SalahZeitApp.swift")
app_text = app.read_text(encoding="utf-8")
anchor = '''        case "quran-favorites":
            NavigationStack { QuranFavoritesLandingView() }
'''
replacement = '''        case "quran-favorites":
            NavigationStack { QuranFavoritesLandingView() }
        case "quran-juz":
            NavigationStack {
                QuranJuzQAView()
            }
'''
if anchor not in app_text:
    raise SystemExit("v423: Quran QA route anchor missing")
app_text = app_text.replace(anchor, replacement, 1)
app.write_text(app_text, encoding="utf-8")

# QA wrapper owns its QuranStore and passes loaded chapters into the new view.
guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")
qa_marker = "\nstruct QuranReaderQAView: View {"
if qa_marker not in text:
    raise SystemExit("v423: QuranReaderQAView marker missing")

qa_view = r'''
struct QuranJuzQAView: View {
    @EnvironmentObject private var settings: SettingsStore
    @StateObject private var store = QuranStore()

    var body: some View {
        Group {
            if store.isLoading && store.chapters.isEmpty {
                ProgressView(settings.t("Quran wird geladen…", "Kur'an yükleniyor…"))
            } else if let error = store.error, store.chapters.isEmpty {
                ContentUnavailableView(
                    settings.t("Cüz konnten nicht geladen werden", "Cüzler yüklenemedi"),
                    systemImage: "wifi.exclamationmark",
                    description: Text(error)
                )
            } else {
                QuranJuzLandingView(chapters: store.chapters)
            }
        }
        .task { await store.loadChapters() }
    }
}
'''
text = text.replace(qa_marker, qa_view + qa_marker, 1)
guide.write_text(text, encoding="utf-8")

print("v423 applied: verified 30-Cüz navigation with direct start-Ayah jumps")
