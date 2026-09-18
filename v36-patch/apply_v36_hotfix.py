from pathlib import Path

# Guide palette + honest external-link icon
p=Path('SalahZeit/Views/GuideView.swift')
s=p.read_text(encoding='utf-8')
s=s.replace('Color.blue', 'SalahTheme.teal')
s=s.replace('Image(systemName: "play.rectangle.fill")', 'Image(systemName: "arrow.up.right.square")')
s=s.replace('deDetail: "Einstiegsdua im Gebet. Offizielle Diyanet-Aufnahme öffnen."', 'deDetail: "Einstiegsdua im Gebet. Offizielle Diyanet-Lernquelle öffnen."')
s=s.replace('trDetail: "Namaza giriş duası. Resmî Diyanet kaydını aç."', 'trDetail: "Namaza giriş duası. Resmî Diyanet öğrenme kaynağını aç."')
# Generic player fallback errors shown bilingual rather than falsely localized only in German
s=s.replace('lastError = "Keine sichere Audiodatei verfügbar."', 'lastError = "Audio nicht verfügbar / Ses mevcut değil."')
s=s.replace('?? "Audio konnte nicht geladen werden."', '?? "Audio konnte nicht geladen werden / Ses yüklenemedi."')
s=s.replace('?? "Audio-Wiedergabe fehlgeschlagen."', '?? "Audio-Wiedergabe fehlgeschlagen / Ses oynatılamadı."')
# Additional list backgrounds
for title in [
    '.navigationTitle(settings.t("Rakʿat", "Rekât"))',
    '.navigationTitle(settings.t("Gebetsduas", "Namaz duaları"))',
    '.navigationTitle(settings.t("Suren lernen", "Sureleri öğren"))',
    '.navigationTitle(settings.t("Begriffe", "Kavramlar"))'
]:
    s=s.replace(title, '.scrollContentBackground(.hidden)\n        .background(SalahTheme.page)\n        '+title)
p.write_text(s,encoding='utf-8')

# Home header gets notification state
p=Path('SalahZeit/Views/HomeView.swift')
s=p.read_text(encoding='utf-8')
old='''            Spacer()\n            VStack(alignment: .trailing, spacing: 3) {\n                Label(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"), systemImage: "location.fill")'''
new='''            Spacer()\n            Image(systemName: settings.notificationsEnabled ? "bell.fill" : "bell.slash")\n                .foregroundStyle(settings.notificationsEnabled ? SalahTheme.gold : .white.opacity(0.55))\n                .accessibilityLabel(settings.notificationsEnabled ? settings.t("Benachrichtigungen aktiv", "Bildirimler açık") : settings.t("Benachrichtigungen aus", "Bildirimler kapalı"))\n            VStack(alignment: .trailing, spacing: 3) {\n                Label(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"), systemImage: "location.fill")'''
if old not in s: raise SystemExit('brand header location block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# Settings: version + reference palette
p=Path('SalahZeit/Views/SettingsView.swift')
s=p.read_text(encoding='utf-8')
s=s.replace('LabeledContent(settings.t("Version", "Sürüm"), value: "3.4")','LabeledContent(settings.t("Version", "Sürüm"), value: "3.6")')
s=s.replace('''        .navigationTitle(settings.t("Einstellungen", "Ayarlar"))''','''        .scrollContentBackground(.hidden)\n        .background(SalahTheme.page)\n        .tint(SalahTheme.teal)\n        .navigationTitle(settings.t("Einstellungen", "Ayarlar"))''')
p.write_text(s,encoding='utf-8')

# Qibla: native reference styling
p=Path('SalahZeit/Views/QiblaView.swift')
s=p.read_text(encoding='utf-8')
s=s.replace('''                VStack(spacing: 28) {\n                    Spacer()\n                    ZStack {\n                        Circle().stroke(.secondary.opacity(0.35), lineWidth: 2).frame(width: 280, height: 280)''','''                VStack(spacing: 22) {\n                    Spacer()\n                    VStack(spacing: 4) {\n                        Text(settings.t("Qibla-Richtung", "Kıble yönü")).font(.title2.bold()).foregroundStyle(SalahTheme.ink)\n                        Text(locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum")).font(.caption).foregroundStyle(.secondary)\n                    }\n                    ZStack {\n                        Circle().fill(SalahTheme.cream).frame(width: 292, height: 292)\n                        Circle().stroke(SalahTheme.gold.opacity(0.7), lineWidth: 2).frame(width: 280, height: 280)''')
s=s.replace('Capsule().fill(.secondary.opacity(index % 3 == 0 ? 0.8 : 0.35))','Capsule().fill(SalahTheme.teal.opacity(index % 3 == 0 ? 0.8 : 0.35))')
s=s.replace('Image(systemName: "location.north.fill").font(.system(size: 90, weight: .medium))','Image(systemName: "location.north.fill").font(.system(size: 90, weight: .medium)).foregroundStyle(SalahTheme.teal)')
s=s.replace('''        .navigationTitle(settings.t("Qibla", "Kıble"))''','''        .background(SalahTheme.page.ignoresSafeArea())\n        .navigationTitle(settings.t("Qibla", "Kıble"))\n        .tint(SalahTheme.teal)''')
p.write_text(s,encoding='utf-8')

# bump build number for hotfix build while keeping v3.6
p=Path('scripts/build_unsigned_ipa.sh')
s=p.read_text(encoding='utf-8').replace('CURRENT_PROJECT_VERSION="9"','CURRENT_PROJECT_VERSION="10"')
p.write_text(s,encoding='utf-8')
print('v3.6 hotfix applied')