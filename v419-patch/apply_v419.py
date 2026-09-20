from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = '''                                if languageTab != 2 {
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
'''
new = '''                                if languageTab == 1 {
                                    Text("Rahmân ve Rahîm olan Allah'ın adıyla.")
                                        .font(.custom("AvenirNext-Medium", size: 13.2))
                                        .foregroundStyle(SalahTheme.ink)
                                        .fixedSize(horizontal: false, vertical: true)
                                }

                                if languageTab == 2 {
                                    Text("Im Namen Allahs, des Allerbarmers, des Barmherzigen.")
                                        .font(.custom("AvenirNext-Medium", size: 13.2))
                                        .foregroundStyle(SalahTheme.ink)
                                        .fixedSize(horizontal: false, vertical: true)
                                }
'''
if old not in text:
    raise SystemExit("v419: Quran overview translation anchor missing")
text = text.replace(old, new, 1)

old = '''        .task { await store.loadChapters() }
        .onAppear { lastRead = QuranBookmarkStore.lastRead() }
        .onDisappear { previewAudio.stop() }
'''
new = '''        .task { await store.loadChapters() }
        .onAppear {
            lastRead = QuranBookmarkStore.lastRead()
            languageTab = settings.language == .german ? 2 : 1
        }
        .onDisappear { previewAudio.stop() }
'''
if old not in text:
    raise SystemExit("v419: Quran overview onAppear anchor missing")
text = text.replace(old, new, 1)

guide.write_text(text, encoding="utf-8")
print("v419 applied: Quran overview shows only selected language and defaults to app language")
