import SwiftUI

struct SettingsView: View {
    @EnvironmentObject private var settings: SettingsStore
    @EnvironmentObject private var locationManager: LocationManager
    @State private var notificationStatusText: String?
    @State private var audioCacheText = "—"
    @State private var isClearingAudioCache = false

    var body: some View {
        ScrollView {
            VStack(spacing: 11) {
                profileHero

                referenceSection(settings.t("Sprache & Lernprofil", "Dil ve öğrenme profili")) {
                    Menu {
                        ForEach(AppLanguage.allCases) { language in
                            Button(language.title) { settings.language = language }
                        }
                    } label: {
                        profileRow(icon: "globe", title: settings.t("Sprache", "Dil"), value: settings.language.title)
                    }

                    Menu {
                        ForEach(PrayerAudience.allCases) { audience in
                            Button(audience.title(settings.language)) { settings.prayerAudience = audience }
                        }
                    } label: {
                        profileRow(icon: "person.2.fill", title: settings.t("Gebetsanleitung", "Namaz anlatımı"), value: settings.prayerAudience.title(settings.language))
                    }
                }

                referenceSection(settings.t("Gebetszeiten", "Namaz vakitleri")) {
                    Menu {
                        ForEach(CalculationPreset.allCases) { method in
                            Button(method.title(settings.language)) { settings.calculationPreset = method }
                        }
                    } label: {
                        profileRow(icon: "clock.fill", title: settings.t("Berechnung", "Hesaplama"), value: settings.calculationPreset.title(settings.language))
                    }

                    Menu {
                        ForEach(AsrRule.allCases) { rule in
                            Button(rule.title(settings.language)) { settings.asrRule = rule }
                        }
                    } label: {
                        profileRow(icon: "sun.max.fill", title: settings.t("Asr-Regel", "İkindi kuralı"), value: settings.asrRule.title(settings.language))
                    }

                    referenceToggle(icon: "24.circle.fill", title: settings.t("24-Stunden-Zeit", "24 saat biçimi"), isOn: $settings.use24Hour)
                }

                referenceSection(settings.t("Quran & Audio", "Kur'an ve Ses")) {
                    Menu {
                        ForEach(QuranReciter.allCases) { reciter in
                            Button(reciter.title) { settings.quranReciter = reciter }
                        }
                    } label: {
                        profileRow(icon: "waveform", title: settings.t("Rezitation", "Kâri"), value: settings.quranReciter.title)
                    }

                    VStack(spacing: 8) {
                        HStack {
                            Label(settings.t("Arabische Schriftgröße", "Arapça yazı boyutu"), systemImage: "textformat.size")
                                .font(.system(size: 11.5, weight: .semibold))
                                .foregroundStyle(SalahTheme.ink)
                            Spacer()
                            Text("\(Int(settings.quranFontSize))")
                                .font(.system(size: 11, weight: .bold).monospacedDigit())
                                .foregroundStyle(SalahTheme.teal)
                        }
                        Stepper("", value: $settings.quranFontSize, in: 20...40, step: 2)
                            .labelsHidden()
                            .frame(maxWidth: .infinity, alignment: .trailing)
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 10)

                    referenceToggle(icon: "text.bubble.fill", title: settings.t("Übersetzung anzeigen", "Meali göster"), isOn: $settings.quranShowTranslation)
                    referenceToggle(icon: "character.cursor.ibeam", title: settings.t("Transliteration anzeigen", "Latin harfli okunuşu göster"), isOn: $settings.quranShowTransliteration)

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
                }

                referenceSection(settings.t("Benachrichtigungen", "Bildirimler")) {
                    referenceToggle(icon: "bell.fill", title: settings.t("Gebetsbeginn erinnern", "Namaz vaktini hatırlat"), isOn: $settings.notificationsEnabled)

                    Picker(settings.t("Erinnerung", "Hatırlatma"), selection: $settings.notificationLeadMinutes) {
                        Text(settings.t("Bei Beginn", "Vakit girince")).tag(0)
                        Text(settings.t("5 Min. vorher", "5 dk önce")).tag(5)
                        Text(settings.t("10 Min. vorher", "10 dk önce")).tag(10)
                        Text(settings.t("15 Min. vorher", "15 dk önce")).tag(15)
                    }
                    .pickerStyle(.menu)
                    .disabled(!settings.notificationsEnabled)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)

                    Button {
                        Task {
                            guard let location = locationManager.location else {
                                notificationStatusText = settings.t("Standort noch nicht verfügbar.", "Konum henüz hazır değil.")
                                return
                            }
                            await NotificationManager.shared.scheduleNextSevenDays(location: location, settings: settings)
                            notificationStatusText = settings.notificationsEnabled
                                ? settings.t("Für die nächsten 7 Tage geplant.", "Önümüzdeki 7 gün için planlandı.")
                                : settings.t("Deaktiviert.", "Kapalı.")
                        }
                    } label: {
                        HStack {
                            Image(systemName: "arrow.clockwise.circle.fill")
                            Text(settings.t("Benachrichtigungen aktualisieren", "Bildirimleri güncelle"))
                                .font(.system(size: 11.5, weight: .bold))
                            Spacer()
                            Image(systemName: "chevron.right")
                                .font(.caption.bold())
                        }
                        .foregroundStyle(SalahTheme.teal)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                    }
                    .buttonStyle(.plain)

                    if let notificationStatusText {
                        Text(notificationStatusText)
                            .font(.system(size: 9.5, weight: .medium))
                            .foregroundStyle(SalahTheme.mutedInk)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(.horizontal, 12)
                            .padding(.bottom, 9)
                    }
                }

                referenceSection(settings.t("Standort & Datenschutz", "Konum ve gizlilik")) {
                    profileRow(icon: "location.fill", title: settings.t("Standortstatus", "Konum durumu"), value: statusText)

                    Text(settings.t(
                        "Gebetszeiten und Qibla werden auf dem Gerät aus GPS-Koordinaten berechnet. Die App speichert deinen aktuellen Standort nicht dauerhaft.",
                        "Namaz vakitleri ve kıble cihaz üzerinde GPS koordinatlarından hesaplanır. Uygulama mevcut konumunu kalıcı olarak saklamaz."
                    ))
                    .font(.system(size: 9.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 10)
                }

                referenceSection(settings.t("Feinabstimmung", "İnce ayar")) {
                    offsetRow(settings.language == .german ? "Fajr" : "Sabah", value: $settings.fajrOffset)
                    offsetRow(settings.language == .german ? "Dhuhr" : "Öğle", value: $settings.dhuhrOffset)
                    offsetRow(settings.language == .german ? "Asr" : "İkindi", value: $settings.asrOffset)
                    offsetRow(settings.language == .german ? "Maghrib" : "Akşam", value: $settings.maghribOffset)
                    offsetRow(settings.language == .german ? "Isha" : "Yatsı", value: $settings.ishaOffset)

                    Button {
                        settings.resetOffsets()
                    } label: {
                        HStack {
                            Image(systemName: "arrow.uturn.backward.circle.fill")
                            Text(settings.t("Korrekturen zurücksetzen", "Düzeltmeleri sıfırla"))
                                .font(.system(size: 11.5, weight: .bold))
                            Spacer()
                        }
                        .foregroundStyle(SalahTheme.teal)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                    }
                    .buttonStyle(.plain)
                }

                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("SalahPath")
                            .font(.system(size: 14, weight: .bold, design: .serif))
                            .foregroundStyle(SalahTheme.deepTeal)
                        Text(settings.t("Ein schöneres Leben durch Anbetung", "İbadetle Daha Güzel Bir Hayat"))
                            .font(.system(size: 8.5, weight: .semibold))
                            .foregroundStyle(SalahTheme.mutedInk)
                    }
                    Spacer()
                    Text(appVersionText)
                        .font(.system(size: 9, weight: .bold).monospacedDigit())
                        .foregroundStyle(SalahTheme.teal)
                }
                .padding(12)
                .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
            }
            .padding(.horizontal, 11)
            .padding(.vertical, 10)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .tint(SalahTheme.teal)
        .navigationTitle(settings.t("Profil", "Profil"))
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            locationManager.requestAccessAndStart()
            Task { await refreshAudioCacheText() }
        }
        .onChange(of: settings.notificationsEnabled) { _, enabled in
            if !enabled { NotificationManager.shared.removePrayerNotifications() }
        }
    }

    @MainActor
    private func refreshAudioCacheText() async {
        let stats = await QuranAudioCache.shared.stats()
        let size = ByteCountFormatter.string(fromByteCount: stats.bytes, countStyle: .file)
        audioCacheText = stats.count == 0
            ? settings.t("Leer", "Boş")
            : "\(size) · \(stats.count)"
    }

    private var appVersionText: String {
        let info = Bundle.main.infoDictionary
        let version = info?["CFBundleShortVersionString"] as? String ?? "—"
        let build = info?["CFBundleVersion"] as? String ?? "—"
        return "v\(version) · \(build)"
    }

    private var profileHero: some View {
        HStack(spacing: 11) {
            ZStack {
                Circle()
                    .fill(SalahTheme.gold.opacity(0.18))
                    .frame(width: 58, height: 58)
                Image(systemName: "person.crop.circle.fill")
                    .font(.system(size: 38))
                    .foregroundStyle(SalahTheme.teal)
            }

            VStack(alignment: .leading, spacing: 3) {
                Text(settings.t("Mein SalahPath", "SalahPath Profilim"))
                    .font(.system(size: 20, weight: .bold, design: .serif))
                    .foregroundStyle(.white)
                Text(settings.t("Deine Einstellungen & Begleitung", "Ayarların ve ibadet rehberin"))
                    .font(.system(size: 9.5, weight: .semibold))
                    .foregroundStyle(.white.opacity(0.82))
                HStack(spacing: 5) {
                    Image(systemName: "globe")
                    Text(settings.language.title)
                    Text("·")
                    Image(systemName: settings.prayerAudience == .male ? "person.fill" : "person.fill")
                    Text(settings.prayerAudience.title(settings.language))
                }
                .font(.system(size: 8.5, weight: .bold))
                .foregroundStyle(SalahTheme.gold)
            }
            Spacer()
        }
        .padding(13)
        .background(
            LinearGradient(colors: [SalahTheme.deepTeal, SalahTheme.teal], startPoint: .topLeading, endPoint: .bottomTrailing),
            in: RoundedRectangle(cornerRadius: 18, style: .continuous)
        )
        .overlay { RoundedRectangle(cornerRadius: 18).stroke(SalahTheme.gold.opacity(0.58), lineWidth: 1) }
    }

    @ViewBuilder
    private func referenceSection<Content: View>(_ title: String, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title)
                .font(.system(size: 10, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
                .padding(.horizontal, 3)

            VStack(spacing: 0) {
                content()
            }
            .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
            .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
        }
    }

    private func profileRow(icon: String, title: String, value: String, showsChevron: Bool = true) -> some View {
        HStack(spacing: 9) {
            Image(systemName: icon)
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 28, height: 28)
                .background(SalahTheme.softTeal, in: Circle())
            Text(title)
                .font(.system(size: 11.5, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer()
            Text(value)
                .font(.system(size: 10, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
                .multilineTextAlignment(.trailing)
                .lineLimit(2)
            if showsChevron {
                Image(systemName: "chevron.right")
                    .font(.system(size: 9, weight: .bold))
                    .foregroundStyle(SalahTheme.teal)
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 10)
        .contentShape(Rectangle())
        .overlay(alignment: .bottom) { Divider().padding(.leading, 50).opacity(0.34) }
    }

    private func referenceToggle(icon: String, title: String, isOn: Binding<Bool>) -> some View {
        HStack(spacing: 9) {
            Image(systemName: icon)
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 28, height: 28)
                .background(SalahTheme.softTeal, in: Circle())
            Text(title)
                .font(.system(size: 11.5, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer()
            Toggle("", isOn: isOn)
                .labelsHidden()
                .scaleEffect(0.82)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 7)
        .overlay(alignment: .bottom) { Divider().padding(.leading, 50).opacity(0.34) }
    }

    private func offsetRow(_ title: String, value: Binding<Int>) -> some View {
        HStack {
            Text(title)
                .font(.system(size: 11.5, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer()
            Stepper("", value: value, in: -15...15)
                .labelsHidden()
            Text(value.wrappedValue == 0 ? "0" : String(format: "%+d", value.wrappedValue))
                .font(.system(size: 10.5, weight: .bold).monospacedDigit())
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 28, alignment: .trailing)
            Text("Min.")
                .font(.system(size: 9, weight: .semibold))
                .foregroundStyle(SalahTheme.mutedInk)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 7)
        .overlay(alignment: .bottom) { Divider().padding(.leading, 12).opacity(0.34) }
    }

    private var statusText: String {
        switch locationManager.authorizationStatus {
        case .authorizedAlways, .authorizedWhenInUse: return settings.t("Erlaubt", "İzin verildi")
        case .denied: return settings.t("Abgelehnt", "Reddedildi")
        case .restricted: return settings.t("Eingeschränkt", "Kısıtlı")
        case .notDetermined: return settings.t("Nicht gefragt", "Sorulmadı")
        @unknown default: return settings.t("Unbekannt", "Bilinmiyor")
        }
    }
}
