import SwiftUI
import UIKit

struct SettingsView: View {
    @EnvironmentObject private var settings: SettingsStore
    @EnvironmentObject private var locationManager: LocationManager
    @State private var notificationStatusText: String?
    @State private var audioCacheText = "—"
    @State private var isClearingAudioCache = false
    @State private var quranTextCacheText = "—"
    @State private var isClearingQuranTextCache = false
    @State private var manualLocationText = ""
    @State private var manualLocationError: String?
    @State private var isResolvingManualLocation = false

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

                    Button {
                        settings.restartOnboarding()
                    } label: {
                        profileRow(
                            icon: "wand.and.stars",
                            title: settings.t("Ersteinrichtung erneut öffnen", "İlk kurulumu yeniden aç"),
                            value: settings.t("Start", "Başlat")
                        )
                    }
                    .buttonStyle(.plain)
                }

                referenceSection(settings.t("Darstellung", "Görünüm")) {
                    Menu {
                        ForEach(AppAppearance.allCases) { appearance in
                            Button(appearance.title(settings.language)) {
                                settings.appearance = appearance
                            }
                        }
                    } label: {
                        profileRow(
                            icon: "circle.lefthalf.filled",
                            title: settings.t("Farbschema", "Renk düzeni"),
                            value: settings.appearance.title(settings.language)
                        )
                    }

                    Text(settings.t(
                        "System folgt automatisch der iPhone-Einstellung. Hell und Dunkel erzwingen das gewählte SalahPath-Farbschema.",
                        "Sistem seçeneği iPhone görünümünü otomatik izler. Açık ve Koyu seçenekleri SalahPath görünümünü sabitler."
                    ))
                    .font(.system(size: 9.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
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
                            Text("\(Int(settings.safeQuranFontSize))")
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
                        icon: "doc.text.fill",
                        title: settings.t("Offline-Qurantext", "Çevrimdışı Kur'an metni"),
                        value: quranTextCacheText,
                        showsChevron: false
                    )

                    Button {
                        Task {
                            isClearingQuranTextCache = true
                            await QuranTextCache.shared.clear()
                            await refreshQuranTextCacheText()
                            isClearingQuranTextCache = false
                        }
                    } label: {
                        HStack(spacing: 9) {
                            Image(systemName: "trash.circle.fill")
                                .font(.system(size: 14, weight: .semibold))
                                .foregroundStyle(SalahTheme.teal)
                                .frame(width: 28, height: 28)
                                .background(SalahTheme.softTeal, in: Circle())

                            Text(settings.t("Text-Cache leeren", "Metin önbelleğini temizle"))
                                .font(.system(size: 11.5, weight: .semibold))
                                .foregroundStyle(SalahTheme.ink)

                            Spacer()

                            if isClearingQuranTextCache {
                                ProgressView()
                                    .controlSize(.small)
                            }
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                    }
                    .buttonStyle(.plain)

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
                        "Bereits geöffnete Quran-Suren und Mushaf-Seiten werden automatisch lokal gespeichert und funktionieren danach offline. Der Text-Cache wird auf etwa 48 MB begrenzt. Bereits gehörte Quran-Audios werden separat gespeichert; der Audio-Cache wird automatisch auf etwa 300 MB begrenzt.",
                        "Açtığın Kur'an sûreleri ve Mushaf sayfaları otomatik olarak cihazda saklanır ve daha sonra çevrimdışı çalışır. Metin önbelleği yaklaşık 48 MB ile sınırlandırılır. Dinlediğin Kur'an sesleri ayrı saklanır; ses önbelleği yaklaşık 300 MB ile sınırlandırılır."
                    ))
                    .font(.system(size: 9.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 9)
                }

                referenceSection(settings.t("Benachrichtigungen", "Bildirimler")) {
                    referenceToggle(
                        icon: "bell.fill",
                        title: settings.t("Gebetsbenachrichtigungen", "Namaz bildirimleri"),
                        isOn: $settings.notificationsEnabled
                    )

                    referenceToggle(
                        icon: "clock.badge.checkmark",
                        title: settings.t("Zum Gebetsbeginn erinnern", "Vakit girince bildir"),
                        isOn: $settings.notifyAtPrayerTime
                    )
                    .disabled(!settings.notificationsEnabled)
                    .opacity(settings.notificationsEnabled ? 1 : 0.45)

                    referenceToggle(
                        icon: "speaker.wave.3.fill",
                        title: settings.t("Gebetsruf (Adhan) abspielen", "Ezan sesi çal"),
                        isOn: $settings.adhanSoundEnabled
                    )
                    .disabled(!settings.notificationsEnabled || !settings.notifyAtPrayerTime)
                    .opacity(settings.notificationsEnabled && settings.notifyAtPrayerTime ? 1 : 0.45)

                    HStack(spacing: 8) {
                        Button {
                            Task {
                                let scheduled = await NotificationManager.shared.scheduleAdhanPreview(settings: settings, fajr: false)
                                notificationStatusText = scheduled
                                    ? settings.t("Standard-Gebetsruf startet gleich.", "Standart ezan birazdan çalacak.")
                                    : settings.t("Test konnte nicht geplant werden. Prüfe die iOS-Benachrichtigungsberechtigung.", "Test planlanamadı. iOS bildirim iznini kontrol et.")
                            }
                        } label: {
                            Label(settings.t("Standard testen", "Standart test"), systemImage: "play.circle.fill")
                                .font(.system(size: 10.5, weight: .bold))
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 9)
                        }
                        .buttonStyle(.bordered)

                        Button {
                            Task {
                                let scheduled = await NotificationManager.shared.scheduleAdhanPreview(settings: settings, fajr: true)
                                notificationStatusText = scheduled
                                    ? settings.t("Fajr-Gebetsruf startet gleich.", "Sabah ezanı birazdan çalacak.")
                                    : settings.t("Test konnte nicht geplant werden. Prüfe die iOS-Benachrichtigungsberechtigung.", "Test planlanamadı. iOS bildirim iznini kontrol et.")
                            }
                        } label: {
                            Label(settings.t("Fajr testen", "Sabah test"), systemImage: "sun.horizon.fill")
                                .font(.system(size: 10.5, weight: .bold))
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 9)
                        }
                        .buttonStyle(.bordered)
                    }
                    .tint(SalahTheme.teal)
                    .padding(.horizontal, 12)
                    .disabled(!settings.notificationsEnabled || !settings.notifyAtPrayerTime || !settings.adhanSoundEnabled)
                    .opacity(settings.notificationsEnabled && settings.notifyAtPrayerTime && settings.adhanSoundEnabled ? 1 : 0.45)

                    Text(settings.t(
                        "Fajr verwendet einen eigenen Sabah-Ezan; Dhuhr, Asr, Maghrib und Isha verwenden den Standard-Ezan. Beide stammen aus der Public-Domain-Sammlung „Adhan Recordings from Doha, Qatar“ im Internet Archive. Vorwarnungen behalten den normalen iOS-Ton.",
                        "Sabah namazında ayrı Sabah ezanı; öğle, ikindi, akşam ve yatsıda standart ezan kullanılır. Her ikisi de Internet Archive'daki „Adhan Recordings from Doha, Qatar“ kamu malı koleksiyonundandır. Ön hatırlatmalar normal iOS sesini kullanır."
                    ))
                    .font(.system(size: 9.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)

                    Picker(settings.t("Vorwarnung", "Ön hatırlatma"), selection: $settings.notificationLeadMinutes) {
                        Text(settings.t("Keine", "Kapalı")).tag(0)
                        Text(settings.t("5 Min. vorher", "5 dk önce")).tag(5)
                        Text(settings.t("10 Min. vorher", "10 dk önce")).tag(10)
                        Text(settings.t("15 Min. vorher", "15 dk önce")).tag(15)
                        Text(settings.t("30 Min. vorher", "30 dk önce")).tag(30)
                    }
                    .pickerStyle(.menu)
                    .disabled(!settings.notificationsEnabled)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)

                    VStack(alignment: .leading, spacing: 0) {
                        Text(settings.t("Für welche Gebete?", "Hangi namazlar?"))
                            .font(.system(size: 9.5, weight: .bold))
                            .foregroundStyle(SalahTheme.teal)
                            .padding(.horizontal, 12)
                            .padding(.top, 9)
                            .padding(.bottom, 3)

                        referenceToggle(icon: "sun.horizon.fill", title: settings.t("Fajr", "Sabah"), isOn: $settings.fajrNotificationEnabled)
                        referenceToggle(icon: "sun.max.fill", title: settings.t("Dhuhr", "Öğle"), isOn: $settings.dhuhrNotificationEnabled)
                        referenceToggle(icon: "sun.min.fill", title: settings.t("Asr", "İkindi"), isOn: $settings.asrNotificationEnabled)
                        referenceToggle(icon: "sunset.fill", title: settings.t("Maghrib", "Akşam"), isOn: $settings.maghribNotificationEnabled)
                        referenceToggle(icon: "moon.stars.fill", title: settings.t("Isha", "Yatsı"), isOn: $settings.ishaNotificationEnabled)
                    }
                    .disabled(!settings.notificationsEnabled)
                    .opacity(settings.notificationsEnabled ? 1 : 0.45)

                    Text(settings.t(
                        "Wenn eine Vorwarnung gewählt ist, kann SalahPath zweimal erinnern: einmal vorher und – falls aktiviert – noch einmal genau zum Gebetsbeginn.",
                        "Ön hatırlatma seçilirse SalahPath iki kez bildirebilir: önce seçilen dakika kadar önce ve açıksa tam namaz vaktinde."
                    ))
                    .font(.system(size: 9.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)

                    Button {
                        Task {
                            guard let location = locationManager.location else {
                                notificationStatusText = settings.t("Standort noch nicht verfügbar.", "Konum henüz hazır değil.")
                                return
                            }
                            let scheduled = await NotificationManager.shared.scheduleNextSevenDays(location: location, settings: settings)
                            if !settings.notificationsEnabled {
                                notificationStatusText = settings.t("Deaktiviert.", "Kapalı.")
                            } else if scheduled {
                                notificationStatusText = settings.t(
                                    "Für die nächsten 7 Tage aktualisiert.",
                                    "Önümüzdeki 7 gün için güncellendi."
                                )
                            } else {
                                notificationStatusText = settings.t(
                                    "Benachrichtigungen konnten nicht vollständig geplant werden. Prüfe die iOS-Berechtigung und versuche es erneut.",
                                    "Bildirimler tam olarak planlanamadı. iOS iznini kontrol edip tekrar dene."
                                )
                            }
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
                    profileRow(
                        icon: locationManager.usesManualLocation ? "mappin.and.ellipse" : "location.fill",
                        title: settings.t("Standortstatus", "Konum durumu"),
                        value: locationManager.locality ?? statusText,
                        showsChevron: false
                    )

                    HStack(spacing: 7) {
                        TextField(settings.t("Stadt oder PLZ manuell", "Şehir veya posta kodu"), text: $manualLocationText)
                            .textInputAutocapitalization(.words)
                            .autocorrectionDisabled()
                            .font(.system(size: 10.5, weight: .medium))
                            .padding(.horizontal, 10)
                            .frame(height: 40)
                            .background(SalahTheme.page.opacity(0.62), in: RoundedRectangle(cornerRadius: 9))

                        Button {
                            Task {
                                isResolvingManualLocation = true
                                manualLocationError = nil
                                let success = await locationManager.setManualLocation(searchText: manualLocationText)
                                isResolvingManualLocation = false
                                if !success { manualLocationError = locationManager.lastError }
                            }
                        } label: {
                            Group {
                                if isResolvingManualLocation {
                                    ProgressView().tint(.white)
                                } else {
                                    Image(systemName: "checkmark")
                                        .font(.system(size: 12, weight: .bold))
                                }
                            }
                            .frame(width: 40, height: 40)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(.white)
                        .background(SalahTheme.navigationTeal, in: RoundedRectangle(cornerRadius: 9))
                        .disabled(manualLocationText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || isResolvingManualLocation)
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)

                    HStack(spacing: 8) {
                        Button {
                            manualLocationError = nil
                            if locationManager.authorizationStatus == .denied ||
                                locationManager.authorizationStatus == .restricted {
                                guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
                                UIApplication.shared.open(url)
                            } else {
                                locationManager.useDeviceLocation()
                            }
                        } label: {
                            Label(
                                settings.t(
                                    locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                        ? "iPhone-Einstellungen"
                                        : "GPS verwenden",
                                    locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                        ? "iPhone ayarları"
                                        : "GPS kullan"
                                ),
                                systemImage: locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                    ? "gear"
                                    : "location.fill"
                            )
                            .font(.system(size: 10.5, weight: .bold))
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 9)
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(.white)
                        .background(SalahTheme.teal, in: RoundedRectangle(cornerRadius: 9))

                        if locationManager.usesManualLocation {
                            Button {
                                manualLocationError = nil
                                locationManager.clearManualLocation()
                            } label: {
                                Label(settings.t("Manuell löschen", "Manuel konumu sil"), systemImage: "xmark.circle")
                                    .font(.system(size: 10.5, weight: .bold))
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 9)
                            }
                            .buttonStyle(.plain)
                            .foregroundStyle(SalahTheme.deepTeal)
                            .background(SalahTheme.softTeal, in: RoundedRectangle(cornerRadius: 9))
                        }
                    }
                    .padding(.horizontal, 12)
                    .padding(.bottom, 8)

                    if let manualLocationError {
                        Text(manualLocationError)
                            .font(.system(size: 9, weight: .medium))
                            .foregroundStyle(.red)
                            .padding(.horizontal, 12)
                            .padding(.bottom, 8)
                    }

                    Text(settings.t(
                        "Du kannst GPS verwenden, einen Ort dauerhaft manuell speichern oder ganz ohne Standort weiterarbeiten. Beim Wechsel von manuell zu GPS bleibt dein gespeicherter Ort erhalten, bis ein gültiger Geräte-Standort verfügbar ist.",
                        "GPS kullanabilir, bir konumu manuel olarak kaydedebilir veya konumsuz devam edebilirsin. Manuel konumdan GPS'e geçerken geçerli cihaz konumu alınana kadar kayıtlı konumun korunur."
                    ))
                    .font(.system(size: 9.5, weight: .medium))
                    .foregroundStyle(SalahTheme.mutedInk)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 10)
                }

                referenceSection(settings.t("Rechtliches & Hilfe", "Yasal bilgiler & yardım")) {
                    if let privacyURL = URL(string: "https://github.com/Achmed06/SalahPath-iOS/blob/main/PRIVACY.md") {
                        Link(destination: privacyURL) {
                            HStack(spacing: 9) {
                                Image(systemName: "hand.raised.fill")
                                    .font(.system(size: 14, weight: .semibold))
                                    .foregroundStyle(SalahTheme.teal)
                                    .frame(width: 28, height: 28)
                                    .background(SalahTheme.softTeal, in: Circle())

                                Text(settings.t("Datenschutzerklärung", "Gizlilik politikası"))
                                    .font(.system(size: 11.5, weight: .semibold))
                                    .foregroundStyle(SalahTheme.ink)

                                Spacer()

                                Image(systemName: "arrow.up.right.square")
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.teal)
                            }
                            .padding(.horizontal, 12)
                            .padding(.vertical, 10)
                        }
                        .buttonStyle(.plain)
                    }

                    if let supportURL = URL(string: "https://github.com/Achmed06/SalahPath-iOS/issues") {
                        Link(destination: supportURL) {
                            HStack(spacing: 9) {
                                Image(systemName: "questionmark.circle.fill")
                                    .font(.system(size: 14, weight: .semibold))
                                    .foregroundStyle(SalahTheme.teal)
                                    .frame(width: 28, height: 28)
                                    .background(SalahTheme.softTeal, in: Circle())

                                Text(settings.t("Support", "Destek"))
                                    .font(.system(size: 11.5, weight: .semibold))
                                    .foregroundStyle(SalahTheme.ink)

                                Spacer()

                                Image(systemName: "arrow.up.right.square")
                                    .font(.caption.bold())
                                    .foregroundStyle(SalahTheme.teal)
                            }
                            .padding(.horizontal, 12)
                            .padding(.vertical, 10)
                        }
                        .buttonStyle(.plain)
                    }
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
            if locationManager.authorizationStatus == .authorizedWhenInUse ||
                locationManager.authorizationStatus == .authorizedAlways {
                locationManager.requestAccessAndStart()
            }
            Task {
                await refreshAudioCacheText()
                await refreshQuranTextCacheText()
            }
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

    @MainActor
    private func refreshQuranTextCacheText() async {
        let stats = await QuranTextCache.shared.stats()
        let size = ByteCountFormatter.string(fromByteCount: stats.bytes, countStyle: .file)
        quranTextCacheText = stats.count == 0
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
