from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = '''    static func setLastRead(surah: Int, ayah: Int) {
        UserDefaults.standard.set("\(surah):\(ayah)", forKey: lastReadKey)
    }
}
'''
new = '''    static func setLastRead(surah: Int, ayah: Int) {
        UserDefaults.standard.set("\(surah):\(ayah)", forKey: lastReadKey)
    }

    static func lastRead() -> QuranBookmark? {
        guard let token = UserDefaults.standard.string(forKey: lastReadKey) else { return nil }
        let parts = token.split(separator: ":")
        guard parts.count == 2,
              let surah = Int(parts[0]),
              let ayah = Int(parts[1]),
              surah > 0,
              ayah > 0 else { return nil }
        return QuranBookmark(surah: surah, ayah: ayah)
    }
}
'''
if old not in text:
    raise SystemExit("v401: QuranBookmarkStore anchor missing")
text = text.replace(old, new, 1)

old_state = '''    @State private var previewAudioURLs: [URL] = []
    @State private var isResolvingPreviewAudio = false
'''
new_state = '''    @State private var previewAudioURLs: [URL] = []
    @State private var isResolvingPreviewAudio = false
    @State private var lastRead = QuranBookmarkStore.lastRead()
'''
if old_state not in text:
    raise SystemExit("v401: QuranView state anchor missing")
text = text.replace(old_state, new_state, 1)

tabs_end = '''                        .padding(3)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 8).stroke(SalahTheme.gold.opacity(0.32), lineWidth: 0.7) }

                        VStack(spacing: 0) {
'''
continue_card = '''                        .padding(3)
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 8).stroke(SalahTheme.gold.opacity(0.32), lineWidth: 0.7) }

                        if let lastRead,
                           let chapter = store.chapters.first(where: { $0.number == lastRead.surah }),
                           lastRead.ayah <= chapter.numberOfAyahs {
                            NavigationLink {
                                QuranSurahView(surah: chapter, initialAyah: lastRead.ayah)
                            } label: {
                                HStack(spacing: 12) {
                                    Image(systemName: "bookmark.fill")
                                        .font(.system(size: 18, weight: .bold))
                                        .foregroundStyle(SalahTheme.gold)
                                        .frame(width: 42, height: 42)
                                        .background(SalahTheme.deepTeal, in: Circle())

                                    VStack(alignment: .leading, spacing: 3) {
                                        Text(settings.t("Weiterlesen", "Okumaya devam et"))
                                            .font(.headline.bold())
                                            .foregroundStyle(SalahTheme.deepTeal)
                                        Text("\(chapter.englishName) · \(settings.t("Vers", "Ayet")) \(lastRead.ayah)")
                                            .font(.subheadline)
                                            .foregroundStyle(SalahTheme.ink)
                                        Text(chapter.name)
                                            .font(.system(size: 18, weight: .medium))
                                            .foregroundStyle(SalahTheme.mutedInk)
                                    }

                                    Spacer()
                                    Image(systemName: "chevron.right")
                                        .font(.headline.bold())
                                        .foregroundStyle(SalahTheme.teal)
                                }
                                .padding(12)
                                .background(
                                    LinearGradient(
                                        colors: [SalahTheme.cream, SalahTheme.softTeal.opacity(0.72)],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    ),
                                    in: RoundedRectangle(cornerRadius: 15, style: .continuous)
                                )
                                .overlay {
                                    RoundedRectangle(cornerRadius: 15, style: .continuous)
                                        .stroke(SalahTheme.gold.opacity(0.46), lineWidth: 1)
                                }
                            }
                            .buttonStyle(.plain)
                            .accessibilityLabel(settings.t(
                                "Quran weiterlesen bei \(chapter.englishName), Vers \(lastRead.ayah)",
                                "Kur'an okumaya \(chapter.englishName), \(lastRead.ayah). ayetten devam et"
                            ))
                        }

                        VStack(spacing: 0) {
'''
if tabs_end not in text:
    raise SystemExit("v401: Quran language tabs insertion anchor missing")
text = text.replace(tabs_end, continue_card, 1)

old_tail = '''        .task { await store.loadChapters() }
        .onDisappear { previewAudio.stop() }
        .tint(SalahTheme.teal)
'''
new_tail = '''        .task { await store.loadChapters() }
        .onAppear { lastRead = QuranBookmarkStore.lastRead() }
        .onDisappear { previewAudio.stop() }
        .tint(SalahTheme.teal)
'''
if old_tail not in text:
    raise SystemExit("v401: QuranView lifecycle anchor missing")
text = text.replace(old_tail, new_tail, 1)

guide.write_text(text, encoding="utf-8")
print("v401 applied: Quran Continue Reading card restores the saved Surah and Ayah")
