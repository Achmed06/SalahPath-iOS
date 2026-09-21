import SwiftUI

struct PrayerDetailView: View {
    @EnvironmentObject private var settings: SettingsStore
    @Environment(\.dismiss) private var dismiss
    @State private var trackerRefresh = 0

    let prayer: PrayerOccurrence
    let day: PrayerDay
    let nextDay: PrayerDay
    private let engine = PrayerEngine()

    var body: some View {
        let isTrackable = PrayerTrackerStore.requiredKinds.contains(prayer.kind)
        let isCompleted = PrayerTrackerStore.isCompleted(prayer.kind, on: prayer.date)

        NavigationStack {
            List {
                Section(settings.t("Beginn", "Başlangıç")) {
                    LabeledContent(settings.t("Zeit", "Vakit"), value: timeString(prayer.date, use24Hour: settings.use24Hour))
                    if let fard = prayer.kind.fardRakats {
                        LabeledContent(settings.t("Pflicht", "Farz"), value: "\(fard) \(settings.t("Rakʿat Fard", "rekât farz"))")
                    }
                    if let window = engine.prayerWindow(for: prayer, day: day, nextDay: nextDay) {
                        LabeledContent(settings.t("Gebetsfenster", "Namaz aralığı"), value: "\(timeString(window.start, use24Hour: settings.use24Hour))–\(timeString(window.end, use24Hour: settings.use24Hour))")
                    }
                }

                Section(settings.t("Fard, Sunnah & Witr", "Farz, sünnet ve vitir")) {
                    Text(prayer.kind.fullSequence(settings.language))
                }

                if isTrackable {
                    Section(settings.t("Gebets-Tracking", "Namaz Takibi")) {
                        Button {
                            _ = PrayerTrackerStore.toggle(prayer.kind, on: prayer.date)
                            trackerRefresh += 1
                        } label: {
                            HStack {
                                Label(
                                    isCompleted
                                        ? settings.t("Als gebetet markiert", "Kılındı olarak işaretlendi")
                                        : settings.t("Als gebetet markieren", "Kılındı olarak işaretle"),
                                    systemImage: isCompleted ? "checkmark.circle.fill" : "circle"
                                )
                                Spacer()
                                Text(isCompleted ? settings.t("Erledigt", "Tamam") : settings.t("Offen", "Açık"))
                                    .font(.caption.bold())
                            }
                            .contentShape(Rectangle())
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(isCompleted ? SalahTheme.teal : SalahTheme.ink)
                    }
                }

                Section(settings.t("Hinweis", "Not")) {
                    Text(prayer.kind.detailNote(settings.language))
                }
            }
            .navigationTitle(prayer.kind.localizedName(settings.language))
            .navigationBarTitleDisplayMode(.inline)
            .toolbar { ToolbarItem(placement: .confirmationAction) { Button(settings.t("Fertig", "Bitti")) { dismiss() } } }
        }
    }
}
