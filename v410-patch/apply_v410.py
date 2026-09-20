from pathlib import Path

home = Path("SalahZeit/Views/HomeView.swift")
text = home.read_text(encoding="utf-8")

old_prop = '''    private let engine = PrayerEngine()
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()
'''
new_prop = '''    private let engine = PrayerEngine()
    private let hijri = Calendar(identifier: .islamicUmmAlQura)
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()
'''
if old_prop not in text:
    raise SystemExit("v410: HomeView engine property anchor missing")
text = text.replace(old_prop, new_prop, 1)

old_content = '''                if isScreenshotQA {
                    nextPrayerHero(qaReferencePrayer)
                } else if let next = engine.nextPrayer(now: effectiveNow, location: location, settings: settings) {
                    nextPrayerHero(next)
                }

                dailyDuaCard
'''
new_content = '''                if isScreenshotQA {
                    nextPrayerHero(qaReferencePrayer)
                } else if let next = engine.nextPrayer(now: effectiveNow, location: location, settings: settings) {
                    nextPrayerHero(next)
                }

                if isRamadan(effectiveNow) {
                    ramadanHomeCard(today: today)
                }

                dailyDuaCard
'''
if old_content not in text:
    raise SystemExit("v410: Home prayer hero insertion anchor missing")
text = text.replace(old_content, new_content, 1)

helper_marker = '''    private var brandHeader: some View {
'''
helpers = r'''    private func isRamadan(_ date: Date) -> Bool {
        hijri.component(.month, from: date) == 9
    }

    @ViewBuilder
    private func ramadanHomeCard(today: PrayerDay) -> some View {
        let day = hijri.component(.day, from: effectiveNow)
        let fajr = today.time(for: .fajr)
        let maghrib = today.time(for: .maghrib)

        NavigationLink {
            FastingTrackerView()
        } label: {
            VStack(alignment: .leading, spacing: 9) {
                HStack {
                    HStack(spacing: 7) {
                        Image(systemName: "moon.stars.fill")
                            .foregroundStyle(SalahTheme.gold)
                        Text(settings.t("Ramadan · Tag \(day)", "Ramazan · \(day). gün"))
                            .font(.headline.bold())
                            .foregroundStyle(.white)
                    }

                    Spacer()

                    Image(systemName: "chevron.right")
                        .font(.caption.bold())
                        .foregroundStyle(.white.opacity(0.82))
                }

                if let fajr, let maghrib {
                    HStack(spacing: 10) {
                        ramadanTimeChip(
                            title: settings.t("Sahur endet", "Sahur biter"),
                            time: timeString(fajr, use24Hour: settings.use24Hour),
                            icon: "sunrise.fill"
                        )
                        ramadanTimeChip(
                            title: settings.t("Iftar", "İftar"),
                            time: timeString(maghrib, use24Hour: settings.use24Hour),
                            icon: "sunset.fill"
                        )
                    }

                    if effectiveNow < fajr {
                        Label(
                            settings.t(
                                "Noch \(countdownString(from: effectiveNow, to: fajr)) bis Fajr",
                                "Fecre \(countdownString(from: effectiveNow, to: fajr)) kaldı"
                            ),
                            systemImage: "timer"
                        )
                        .font(.subheadline.bold())
                        .foregroundStyle(.white)
                    } else if effectiveNow < maghrib {
                        Label(
                            settings.t(
                                "Iftar in \(countdownString(from: effectiveNow, to: maghrib))",
                                "İftara \(countdownString(from: effectiveNow, to: maghrib))"
                            ),
                            systemImage: "timer"
                        )
                        .font(.subheadline.bold())
                        .foregroundStyle(.white)
                    } else {
                        Label(
                            settings.t(
                                "Der heutige Fastentag ist beendet.",
                                "Bugünkü oruç günü tamamlandı."
                            ),
                            systemImage: "checkmark.circle.fill"
                        )
                        .font(.subheadline.bold())
                        .foregroundStyle(.white)
                    }
                }

                Text(settings.t(
                    "Tippen für Fastenregeln, Ramadan-Lernbereich und deinen privaten Tracker.",
                    "Oruç hükümleri, Ramazan öğrenme bölümü ve kişisel takibin için dokun."
                ))
                .font(.caption)
                .foregroundStyle(.white.opacity(0.82))
                .fixedSize(horizontal: false, vertical: true)
            }
            .padding(12)
            .background(
                LinearGradient(
                    colors: [SalahTheme.deepTeal, SalahTheme.teal.opacity(0.92)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                ),
                in: RoundedRectangle(cornerRadius: 17, style: .continuous)
            )
            .overlay {
                RoundedRectangle(cornerRadius: 17, style: .continuous)
                    .stroke(SalahTheme.gold.opacity(0.60), lineWidth: 1)
            }
        }
        .buttonStyle(.plain)
        .accessibilityLabel(settings.t(
            "Ramadan Tag \(day), Fastenbereich öffnen",
            "Ramazan \(day). gün, oruç bölümünü aç"
        ))
    }

    private func ramadanTimeChip(title: String, time: String, icon: String) -> some View {
        HStack(spacing: 6) {
            Image(systemName: icon)
                .font(.caption.bold())
                .foregroundStyle(SalahTheme.gold)
            VStack(alignment: .leading, spacing: 1) {
                Text(title)
                    .font(.system(size: 9, weight: .semibold))
                    .foregroundStyle(.white.opacity(0.76))
                Text(time)
                    .font(.system(size: 13, weight: .bold))
                    .foregroundStyle(.white)
            }
            Spacer(minLength: 0)
        }
        .padding(.horizontal, 9)
        .padding(.vertical, 7)
        .frame(maxWidth: .infinity)
        .background(Color.white.opacity(0.10), in: RoundedRectangle(cornerRadius: 11, style: .continuous))
    }

'''
if helper_marker not in text:
    raise SystemExit("v410: Home brandHeader anchor missing")
text = text.replace(helper_marker, helpers + helper_marker, 1)

home.write_text(text, encoding="utf-8")
print("v410 applied: automatic Ramadan Home card with Sahur/Iftar countdown")
