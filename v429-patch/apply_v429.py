from pathlib import Path

settings = Path("SalahZeit/Views/SettingsView.swift")
text = settings.read_text(encoding="utf-8")

state_anchor = '    @State private var notificationStatusText: String?\n'
if state_anchor not in text:
    raise SystemExit("v429: Settings state anchor missing")
text = text.replace(
    state_anchor,
    state_anchor + '    @State private var audioCacheText = "—"\n    @State private var isClearingAudioCache = false\n',
    1
)

section_anchor = '''                    referenceToggle(icon: "text.bubble.fill", title: settings.t("Übersetzung anzeigen", "Meali göster"), isOn: $settings.quranShowTranslation)
                    referenceToggle(icon: "character.cursor.ibeam", title: settings.t("Transliteration anzeigen", "Latin harfli okunuşu göster"), isOn: $settings.quranShowTransliteration)
'''
if section_anchor not in text:
    raise SystemExit("v429: Quran settings section anchor missing")

extra = section_anchor + '''
                    profileRow(
                        icon: "arrow.down.circle.fill",
                        title: settings.t("Offline-Audio", "Çevrimdışı ses"),
                        value: audioCacheText,
                        showsChevron: false
                    )

                    Button {
                        Task {
                            isClearingAudioCache = true
                            await QuranAudioCache.shared.clear()
                            await refreshAudioCacheText()
                            isClearingAudioCache = false
                        }
                    } label: {
                        HStack(spacing: 9) {
                            Image(systemName: "trash.circle.fill")
                                .font(.system(size: 14, weight: .semibold))
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 28, height: 28)
                                .background(SalahTheme.softTeal, in: Circle())

                            Text(settings.t("Audio-Cache leeren", "Ses önbelleğini temizle"))
                                .font(.system(size: 11.5, weight: .semibold))
                                .foregroundStyle(SalahTheme.ink)

                            Spacer()

                            if isClearingAudioCache {
                                ProgressView()
                                    .controlSize(.small)
                            }
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                    }
                    .buttonStyle(.plain)

                    Text(settings.t(
                        "Bereits gehörte Quran-Audios werden automatisch auf diesem Gerät gespeichert. So können sie später ohne erneuten Download abgespielt werden. Der Cache wird automatisch auf etwa 300 MB begrenzt.",
                        "Dinlediğin Kur'an sesleri bu cihazda otomatik olarak saklanır. Böylece daha sonra yeniden indirmeden oynatılabilir. Önbellek otomatik olarak yaklaşık 300 MB ile sınırlandırılır."
                    ))
                    .font(.system(size: 9.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 9)
'''
text = text.replace(section_anchor, extra, 1)

lifecycle_anchor = '''        .navigationBarTitleDisplayMode(.inline)
        .onAppear { locationManager.requestAccessAndStart() }
        .onChange(of: settings.notificationsEnabled) { _, enabled in
'''
if lifecycle_anchor not in text:
    raise SystemExit("v429: Settings lifecycle anchor missing")
text = text.replace(
    lifecycle_anchor,
    '''        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            locationManager.requestAccessAndStart()
            Task { await refreshAudioCacheText() }
        }
        .onChange(of: settings.notificationsEnabled) { _, enabled in
''',
    1
)

helper_anchor = '''    private var appVersionText: String {
'''
if helper_anchor not in text:
    raise SystemExit("v429: Settings helper anchor missing")

helper = r'''    @MainActor
    private func refreshAudioCacheText() async {
        let stats = await QuranAudioCache.shared.stats()
        let size = ByteCountFormatter.string(fromByteCount: stats.bytes, countStyle: .file)
        audioCacheText = stats.count == 0
            ? settings.t("Leer", "Boş")
            : "\(size) · \(stats.count)"
    }

'''
text = text.replace(helper_anchor, helper + helper_anchor, 1)

settings.write_text(text, encoding="utf-8")
print("v429 applied: Quran offline-audio cache status and clear control in Settings")
