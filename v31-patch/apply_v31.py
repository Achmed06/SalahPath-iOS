from pathlib import Path

def replace_once(path, old, new):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'Expected block not found in {path}: {old[:80]!r}')
    p.write_text(s.replace(old, new, 1), encoding='utf-8')

# Settings model: selectable Quran reciter, persisted.
p = Path('SalahZeit/Models/AppSettings.swift')
s = p.read_text(encoding='utf-8')
insert = '''\nenum QuranReciter: String, CaseIterable, Identifiable {\n    case alafasy\n    case husary\n    case minshawi\n    case sudais\n\n    var id: String { rawValue }\n\n    var edition: String {\n        switch self {\n        case .alafasy: return "ar.alafasy"\n        case .husary: return "ar.husary"\n        case .minshawi: return "ar.minshawi"\n        case .sudais: return "ar.sudais"\n        }\n    }\n\n    var bitrate: Int { self == .sudais ? 192 : 128 }\n\n    var title: String {\n        switch self {\n        case .alafasy: return "Mishary Rashid Alafasy"\n        case .husary: return "Mahmoud Khalil Al-Husary"\n        case .minshawi: return "Mohamed Siddiq al-Minshawi"\n        case .sudais: return "Abdul Rahman Al-Sudais"\n        }\n    }\n}\n'''
s = s.replace('enum CalculationPreset:', insert + '\nenum CalculationPreset:', 1)
s = s.replace('static let audience = "prayerAudience"', 'static let audience = "prayerAudience"\n        static let quranReciter = "quranReciter"', 1)
s = s.replace('@Published var prayerAudience: PrayerAudience { didSet { defaults.set(prayerAudience.rawValue, forKey: Keys.audience) } }', '@Published var prayerAudience: PrayerAudience { didSet { defaults.set(prayerAudience.rawValue, forKey: Keys.audience) } }\n    @Published var quranReciter: QuranReciter { didSet { defaults.set(quranReciter.rawValue, forKey: Keys.quranReciter) } }', 1)
s = s.replace('self.prayerAudience = PrayerAudience(rawValue: defaults.string(forKey: Keys.audience) ?? "") ?? .male', 'self.prayerAudience = PrayerAudience(rawValue: defaults.string(forKey: Keys.audience) ?? "") ?? .male\n        self.quranReciter = QuranReciter(rawValue: defaults.string(forKey: Keys.quranReciter) ?? "") ?? .alafasy', 1)
p.write_text(s, encoding='utf-8')

# Settings UI: reciter choice and version.
p = Path('SalahZeit/Views/SettingsView.swift')
s = p.read_text(encoding='utf-8')
needle = '            Section(settings.t("Benachrichtigungen", "Bildirimler")) {'
block = '''            Section(settings.t("Quran & Audio", "Kur'an ve Ses")) {\n                Picker(settings.t("Rezitation", "Kâri"), selection: $settings.quranReciter) {\n                    ForEach(QuranReciter.allCases) { reciter in\n                        Text(reciter.title).tag(reciter)\n                    }\n                }\n                Text(settings.t(\n                    "Die Quran-Rezitation wird als menschliche Aufnahme über den Islamic Network CDN gestreamt.",\n                    "Kur'an tilaveti Islamic Network CDN üzerinden gerçek insan kaydı olarak yayınlanır."\n                ))\n                .font(.caption)\n                .foregroundStyle(.secondary)\n            }\n\n'''
if needle not in s: raise SystemExit('Settings insertion point not found')
s = s.replace(needle, block + needle, 1)
s = s.replace('value: "3.0"', 'value: "3.1"', 1)
p.write_text(s, encoding='utf-8')

# Quran: bookmarks, last-read, per-ayah playback, reciter-aware URLs.
p = Path('SalahZeit/Views/GuideView.swift')
s = p.read_text(encoding='utf-8')
needle = 'struct QuranView: View {'
helper = '''private struct QuranBookmark: Hashable {\n    let surah: Int\n    let ayah: Int\n\n    var token: String { "\\(surah):\\(ayah)" }\n}\n\nprivate enum QuranBookmarkStore {\n    static let key = "quranBookmarks"\n    static let lastReadKey = "quranLastRead"\n\n    static func tokens() -> Set<String> {\n        Set(UserDefaults.standard.stringArray(forKey: key) ?? [])\n    }\n\n    static func contains(_ bookmark: QuranBookmark) -> Bool { tokens().contains(bookmark.token) }\n\n    static func toggle(_ bookmark: QuranBookmark) -> Bool {\n        var values = tokens()\n        let added: Bool\n        if values.contains(bookmark.token) { values.remove(bookmark.token); added = false }\n        else { values.insert(bookmark.token); added = true }\n        UserDefaults.standard.set(Array(values).sorted(), forKey: key)\n        return added\n    }\n\n    static func setLastRead(surah: Int, ayah: Int) {\n        UserDefaults.standard.set("\\(surah):\\(ayah)", forKey: lastReadKey)\n    }\n}\n\n'''
if needle not in s: raise SystemExit('QuranView insertion point missing')
s = s.replace(needle, helper + needle, 1)
s = s.replace('@State private var search = ""', '@State private var search = ""\n    @State private var lastRead = UserDefaults.standard.string(forKey: QuranBookmarkStore.lastReadKey)', 1)
old = '''                List(filtered) { surah in\n                    NavigationLink {\n                        QuranSurahView(surah:surah)\n                    } label: {'''
new = '''                List {\n                    if let lastRead {\n                        Section {\n                            Label(settings.t("Zuletzt gelesen: \\(lastRead.replacingOccurrences(of: \":\", with: \" · Ayah \"))", "Son okunan: \\(lastRead.replacingOccurrences(of: \":\", with: \" · Ayet \"))"), systemImage: "bookmark.fill")\n                                .font(.subheadline)\n                        }\n                    }\n                    Section {\n                        ForEach(filtered) { surah in\n                    NavigationLink {\n                        QuranSurahView(surah:surah)\n                    } label: {'''
if old not in s: raise SystemExit('Quran list block start missing')
s = s.replace(old, new, 1)
old = '''                        }.padding(.vertical,3)\n                    }\n                }\n                .searchable'''
new = '''                        }.padding(.vertical,3)\n                    }\n                        }\n                    }\n                }\n                .searchable'''
if old not in s: raise SystemExit('Quran list block end missing')
s = s.replace(old, new, 1)
s = s.replace('@State private var error:String?', '@State private var error:String?\n    @State private var bookmarkedTokens = QuranBookmarkStore.tokens()', 1)
s = s.replace('Text("Mishary Rashid Alafasy · Islamic Network CDN").font(.caption).foregroundStyle(.secondary)', 'Text("\\(settings.quranReciter.title) · Islamic Network CDN").font(.caption).foregroundStyle(.secondary)', 1)
old = '''                        VStack(alignment:.leading,spacing:12) {\n                            Text("\\(ar.numberInSurah)").font(.caption.bold()).foregroundStyle(.secondary)\n                            Text(ar.text).font(.title2).multilineTextAlignment(.trailing).frame(maxWidth:.infinity,alignment:.trailing).textSelection(.enabled)\n                            Divider()\n                            Text(tr.text).font(.body).textSelection(.enabled)\n                        }.cardStyle()'''
new = '''                        VStack(alignment:.leading,spacing:12) {\n                            HStack {\n                                Text("\\(ar.numberInSurah)").font(.caption.bold()).foregroundStyle(.secondary)\n                                Spacer()\n                                Button {\n                                    QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah)\n                                    audio.toggle(ayahAudioURL(globalAyah: ar.number))\n                                } label: {\n                                    Image(systemName: audio.activeURL == ayahAudioURL(globalAyah: ar.number) && audio.isPlaying ? "pause.circle.fill" : "play.circle")\n                                }\n                                .buttonStyle(.plain)\n                                Button {\n                                    let bookmark = QuranBookmark(surah: surah.number, ayah: ar.numberInSurah)\n                                    _ = QuranBookmarkStore.toggle(bookmark)\n                                    bookmarkedTokens = QuranBookmarkStore.tokens()\n                                } label: {\n                                    Image(systemName: bookmarkedTokens.contains("\\(surah.number):\\(ar.numberInSurah)") ? "bookmark.fill" : "bookmark")\n                                }\n                                .buttonStyle(.plain)\n                            }\n                            Text(ar.text).font(.title2).multilineTextAlignment(.trailing).frame(maxWidth:.infinity,alignment:.trailing).textSelection(.enabled)\n                            Divider()\n                            Text(tr.text).font(.body).textSelection(.enabled)\n                        }\n                        .cardStyle()\n                        .onAppear { QuranBookmarkStore.setLastRead(surah: surah.number, ayah: ar.numberInSurah) }'''
if old not in s: raise SystemExit('Ayah card block missing')
s = s.replace(old, new, 1)
old = 'private var audioURL:URL { URL(string:"https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy/\\(surah.number).mp3")! }'
new = '''private var audioURL:URL { URL(string:"https://cdn.islamic.network/quran/audio-surah/\\(settings.quranReciter.bitrate)/\\(settings.quranReciter.edition)/\\(surah.number).mp3")! }\n\n    private func ayahAudioURL(globalAyah: Int) -> URL {\n        URL(string: "https://cdn.islamic.network/quran/audio/\\(settings.quranReciter.bitrate)/\\(settings.quranReciter.edition)/\\(globalAyah).mp3")!\n    }'''
if old not in s: raise SystemExit('Audio URL block missing')
s = s.replace(old, new, 1)
# Make the character visibly child-like rather than a bare stick figure: face details + filled hijab.
s = s.replace('circle(head, h*0.10)\n                        garment', 'circle(head, h*0.10)\n                        circle(CGPoint(x:w*0.47,y:h*0.205), h*0.008)\n                        circle(CGPoint(x:w*0.53,y:h*0.205), h*0.008)\n                        garment', 1)
s = s.replace('context.stroke(hijab, with: .color(.accentColor), style: StrokeStyle(lineWidth: 8))', 'context.fill(hijab, with: .color(.accentColor.opacity(0.28)))\n                            context.stroke(hijab, with: .color(.accentColor), style: StrokeStyle(lineWidth: 7))', 1)
p.write_text(s, encoding='utf-8')

# Build metadata and branding.
p = Path('SalahZeit.xcodeproj/project.pbxproj')
s = p.read_text(encoding='utf-8')
s = s.replace('INFOPLIST_KEY_CFBundleDisplayName = SalahZeit;', 'INFOPLIST_KEY_CFBundleDisplayName = SalahPath;')
s = s.replace('SalahZeit verwendet deinen Standort, um Gebetszeiten und die Qibla-Richtung für deine aktuelle Position zu berechnen.', 'SalahPath nutzt deinen Standort für Gebetszeiten und Qibla. / SalahPath namaz vakitleri ve kıble için konumunuzu kullanır.')
p.write_text(s, encoding='utf-8')

p = Path('scripts/build_unsigned_ipa.sh')
s = p.read_text(encoding='utf-8')
s = s.replace('MARKETING_VERSION="3.0"', 'MARKETING_VERSION="3.1"')
s = s.replace('CURRENT_PROJECT_VERSION="3"', 'CURRENT_PROJECT_VERSION="4"')
p.write_text(s, encoding='utf-8')

print('SalahPath v3.1 patch applied')