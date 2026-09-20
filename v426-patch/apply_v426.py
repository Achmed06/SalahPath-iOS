from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old_state = '''    @State private var previewAudioURLs: [URL] = []
    @State private var isResolvingPreviewAudio = false
    @State private var lastRead = QuranBookmarkStore.lastRead()

    var body: some View {
'''
new_state = '''    @State private var previewAudioURLs: [URL] = []
    @State private var isResolvingPreviewAudio = false
    @State private var lastRead: QuranBookmark?

    init(initialLastReadSurah: Int? = nil, initialLastReadAyah: Int? = nil) {
        if let surah = initialLastReadSurah, let ayah = initialLastReadAyah {
            _lastRead = State(initialValue: QuranBookmark(surah: surah, ayah: ayah))
        } else {
            _lastRead = State(initialValue: QuranBookmarkStore.lastRead())
        }
    }

    var body: some View {
'''
if old_state not in text:
    raise SystemExit("v426: QuranView lastRead state anchor missing")
text = text.replace(old_state, new_state, 1)

old_qa = '''struct QuranProgressQAView: View {
    init() {
        QuranBookmarkStore.setLastRead(surah: 2, ayah: 142)
    }

    var body: some View {
        QuranView()
    }
}
'''
new_qa = '''struct QuranProgressQAView: View {
    var body: some View {
        QuranView(initialLastReadSurah: 2, initialLastReadAyah: 142)
    }
}
'''
if old_qa not in text:
    raise SystemExit("v426: QuranProgressQAView anchor missing")
text = text.replace(old_qa, new_qa, 1)

guide.write_text(text, encoding="utf-8")
print("v426 applied: deterministic Quran progress QA injection")
