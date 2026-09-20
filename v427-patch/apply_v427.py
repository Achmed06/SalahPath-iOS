from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old_init = '''    @State private var lastRead: QuranBookmark?

    init(initialLastReadSurah: Int? = nil, initialLastReadAyah: Int? = nil) {
        if let surah = initialLastReadSurah, let ayah = initialLastReadAyah {
            _lastRead = State(initialValue: QuranBookmark(surah: surah, ayah: ayah))
        } else {
            _lastRead = State(initialValue: QuranBookmarkStore.lastRead())
        }
    }
'''
new_init = '''    @State private var lastRead: QuranBookmark?
    private let usesInjectedLastRead: Bool

    init(initialLastReadSurah: Int? = nil, initialLastReadAyah: Int? = nil) {
        if let surah = initialLastReadSurah, let ayah = initialLastReadAyah {
            _lastRead = State(initialValue: QuranBookmark(surah: surah, ayah: ayah))
            usesInjectedLastRead = true
        } else {
            _lastRead = State(initialValue: QuranBookmarkStore.lastRead())
            usesInjectedLastRead = false
        }
    }
'''
if old_init not in text:
    raise SystemExit("v427: Quran injected-last-read initializer anchor missing")
text = text.replace(old_init, new_init, 1)

old_appear = '''        .onAppear {
            lastRead = QuranBookmarkStore.lastRead()
            languageTab = settings.language == .german ? 2 : 1
        }
'''
new_appear = '''        .onAppear {
            if !usesInjectedLastRead {
                lastRead = QuranBookmarkStore.lastRead()
            }
            languageTab = settings.language == .german ? 2 : 1
        }
'''
if old_appear not in text:
    raise SystemExit("v427: Quran onAppear last-read anchor missing")
text = text.replace(old_appear, new_appear, 1)

guide.write_text(text, encoding="utf-8")
print("v427 applied: preserve injected Quran last-read value only for deterministic QA")
