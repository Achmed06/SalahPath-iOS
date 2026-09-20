from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

# Quran overview third language tab: localize "German" for Turkish UI.
old = '''                            let quranLanguageTabs = [
                                settings.t("Arabisch", "Arapça"),
                                settings.t("Türkisch", "Türkçe"),
                                "Deutsch"
                            ]
'''
new = '''                            let quranLanguageTabs = [
                                settings.t("Arabisch", "Arapça"),
                                settings.t("Türkisch", "Türkçe"),
                                settings.t("Deutsch", "Almanca")
                            ]
'''
if old not in text:
    raise SystemExit("v416: Quran overview language tabs anchor missing")
text = text.replace(old, new, 1)

# Reader chooses the app language on first appearance.
old = '''    @State private var hasScrolledToInitial = false
    @State private var displayMode = 0
'''
new = '''    @State private var hasScrolledToInitial = false
    @State private var displayMode = 0
    @State private var didSetInitialDisplayMode = false
'''
if old not in text:
    raise SystemExit("v416: Quran reader display state anchor missing")
text = text.replace(old, new, 1)

old = '''            .onChange(of: arabic?.ayahs.count ?? 0) { _, _ in scrollToInitialIfNeeded(proxy) }
            .onDisappear { audio.stop() }
'''
new = '''            .onChange(of: arabic?.ayahs.count ?? 0) { _, _ in scrollToInitialIfNeeded(proxy) }
            .onAppear {
                if !didSetInitialDisplayMode {
                    displayMode = settings.language == .german ? 2 : 1
                    didSetInitialDisplayMode = true
                }
            }
            .onDisappear { audio.stop() }
'''
if old not in text:
    raise SystemExit("v416: Quran reader lifecycle anchor missing")
text = text.replace(old, new, 1)

old = '''            Picker(settings.t("Ansicht", "Görünüm"), selection: $displayMode) {
                Text(settings.t("Arabisch", "Arapça")).tag(0)
                Text(settings.t("Türkisch", "Türkçe")).tag(1)
                Text("Deutsch").tag(2)
            }
'''
new = '''            Picker(settings.t("Ansicht", "Görünüm"), selection: $displayMode) {
                Text(settings.t("Arabisch", "Arapça")).tag(0)
                Text(settings.t("Türkisch", "Türkçe")).tag(1)
                Text(settings.t("Deutsch", "Almanca")).tag(2)
            }
'''
if old not in text:
    raise SystemExit("v416: Quran reader picker anchor missing")
text = text.replace(old, new, 1)

old = '''            if settings.quranShowTranslation && displayMode != 2 {
                Divider().overlay(SalahTheme.gold.opacity(0.30))
                VStack(alignment: .leading, spacing: 3) {
                    Text(settings.t("Türkisch", "Türkçe"))
                        .font(.system(size: 8.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(turkish.text)
                        .font(.system(size: 13, weight: .medium))
                        .foregroundStyle(SalahTheme.ink)
                        .textSelection(.enabled)
                }
            }

            if settings.quranShowTranslation && displayMode != 1 {
                Divider().overlay(SalahTheme.gold.opacity(0.30))
                VStack(alignment: .leading, spacing: 3) {
                    Text("Deutsch")
                        .font(.system(size: 8.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(german.text)
                        .font(.system(size: 13, weight: .medium))
                        .foregroundStyle(SalahTheme.ink)
                        .textSelection(.enabled)
                }
            }
'''
new = '''            if settings.quranShowTranslation && displayMode == 1 {
                Divider().overlay(SalahTheme.gold.opacity(0.30))
                VStack(alignment: .leading, spacing: 3) {
                    Text(settings.t("Türkisch", "Türkçe"))
                        .font(.system(size: 8.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(turkish.text)
                        .font(.system(size: 13, weight: .medium))
                        .foregroundStyle(SalahTheme.ink)
                        .textSelection(.enabled)
                }
            }

            if settings.quranShowTranslation && displayMode == 2 {
                Divider().overlay(SalahTheme.gold.opacity(0.30))
                VStack(alignment: .leading, spacing: 3) {
                    Text(settings.t("Deutsch", "Almanca"))
                        .font(.system(size: 8.5, weight: .bold))
                        .foregroundStyle(SalahTheme.teal)
                    Text(german.text)
                        .font(.system(size: 13, weight: .medium))
                        .foregroundStyle(SalahTheme.ink)
                        .textSelection(.enabled)
                }
            }
'''
if old not in text:
    raise SystemExit("v416: Quran reader translation blocks anchor missing")
text = text.replace(old, new, 1)

old = '''        if settings.quranShowTranslation {
            if displayMode != 2 { parts.append(turkish.text) }
            if displayMode != 1 { parts.append(german.text) }
        }
'''
new = '''        if settings.quranShowTranslation {
            if displayMode == 1 { parts.append(turkish.text) }
            if displayMode == 2 { parts.append(german.text) }
        }
'''
if old not in text:
    raise SystemExit("v416: Quran share translation anchor missing")
text = text.replace(old, new, 1)

guide.write_text(text, encoding="utf-8")
print("v416 applied: one Quran translation at a time, defaulting to app language")
