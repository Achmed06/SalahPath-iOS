from pathlib import Path
import base64
import hashlib
import io
import json
import plistlib
import zipfile

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
assets_root = root / "SalahZeit" / "Assets.xcassets"

# Install the exact user-approved prayer reference image as four app-sized rows.
payload_dir = root / "v438-assets"
parts = sorted(payload_dir.glob("part-*.b64"))
if len(parts) != 4:
    raise SystemExit(f"v438: expected 4 prayer payload parts, found {len(parts)}")

encoded = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
archive = base64.b64decode(encoded)
expected_sha256 = "5bebe4919ab13f0b65903e6f5e98ec5ce856a44b04caf2d5066cef3af019301c"
actual_sha256 = hashlib.sha256(archive).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v438: prayer payload checksum mismatch: {actual_sha256}")

asset_names = (
    "prayer_reference_male_1",
    "prayer_reference_male_2",
    "prayer_reference_female_1",
    "prayer_reference_female_2",
)

with zipfile.ZipFile(io.BytesIO(archive)) as zf:
    for asset_name in asset_names:
        source_name = f"{asset_name}.jpg"
        data = zf.read(source_name)
        imageset = assets_root / f"{asset_name}.imageset"
        imageset.mkdir(parents=True, exist_ok=True)
        (imageset / source_name).write_bytes(data)
        (imageset / "Contents.json").write_text(
            json.dumps(
                {
                    "images": [
                        {
                            "filename": source_name,
                            "idiom": "universal",
                            "scale": "1x",
                        }
                    ],
                    "info": {"author": "xcode", "version": 1},
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

text = guide.read_text(encoding="utf-8")

# Native Calendar editor support.
if "import EventKit\n" not in text:
    text = text.replace(
        "import SwiftUI\n",
        "import SwiftUI\nimport EventKit\nimport EventKitUI\n",
        1,
    )

# Prayer reference: preserve the approved image exactly; only split it into
# two vertically stacked rows per audience so it stays legible on iPhone.
start_marker = "struct PrayerSequenceReferenceView: View {"
end_marker = "// MARK: - Dhikr"
start = text.find(start_marker)
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("v438: PrayerSequenceReferenceView block missing")

new_prayer = r'''struct PrayerSequenceReferenceView: View {
    @EnvironmentObject private var settings: SettingsStore

    private var assetNames: [String] {
        settings.prayerAudience == .female
            ? ["prayer_reference_female_1", "prayer_reference_female_2"]
            : ["prayer_reference_male_1", "prayer_reference_male_2"]
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                ForEach(assetNames, id: \.self) { assetName in
                    Image(assetName)
                        .resizable()
                        .scaledToFit()
                        .frame(maxWidth: .infinity)
                        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                        .overlay {
                            RoundedRectangle(cornerRadius: 16, style: .continuous)
                                .stroke(SalahTheme.gold.opacity(0.30), lineWidth: 1)
                        }
                }
            }
            .padding(12)
        }
        .scrollIndicators(.hidden)
        .background(SalahTheme.page)
        .navigationTitle(settings.t("Gebetspositionen", "Namaz duruşları"))
        .navigationBarTitleDisplayMode(.inline)
    }
}

'''
text = text[:start] + new_prayer + text[end:]

event_detail_marker = "private struct IslamicCalendarEventDetailView: View {"
event_pos = text.find(event_detail_marker)
if event_pos < 0:
    raise SystemExit("v438: IslamicCalendarEventDetailView missing")

calendar_support = r'''private struct IslamicCalendarDraft: Identifiable {
    let id = UUID()
    let title: String
    let date: Date
    let notes: String
}

private struct CalendarEventEditor: UIViewControllerRepresentable {
    let draft: IslamicCalendarDraft
    @Environment(\.dismiss) private var dismiss

    final class Coordinator: NSObject, EKEventEditViewDelegate {
        let parent: CalendarEventEditor

        init(parent: CalendarEventEditor) {
            self.parent = parent
        }

        func eventEditViewController(
            _ controller: EKEventEditViewController,
            didCompleteWith action: EKEventEditViewAction
        ) {
            parent.dismiss()
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(parent: self)
    }

    func makeUIViewController(context: Context) -> EKEventEditViewController {
        let eventStore = EKEventStore()
        let event = EKEvent(eventStore: eventStore)
        let start = Calendar.current.startOfDay(for: draft.date)

        event.title = draft.title
        event.startDate = start
        event.endDate = Calendar.current.date(byAdding: .day, value: 1, to: start) ?? start
        event.isAllDay = true
        event.notes = draft.notes

        let controller = EKEventEditViewController()
        controller.eventStore = eventStore
        controller.event = event
        controller.editViewDelegate = context.coordinator
        return controller
    }

    func updateUIViewController(
        _ uiViewController: EKEventEditViewController,
        context: Context
    ) {}
}

'''
text = text[:event_pos] + calendar_support + text[event_pos:]

start = text.find(event_detail_marker)
end_marker = "\n}\n\nstruct HijriCalendarView: View {"
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("v438: IslamicCalendarEventDetailView boundary missing")
end += 2

new_detail = r'''private struct IslamicCalendarEventDetailView: View {
    @EnvironmentObject private var settings: SettingsStore
    @State private var calendarDraft: IslamicCalendarDraft?

    let date: Date
    let event: IslamicCalendarEvent

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                eventHeaderCard
                calendarExportButton
                eventMeaningCard
                eventRecommendationsCard
                eventCautionCard
                eventSourceCard
            }
            .padding()
        }
        .background(SalahTheme.page)
        .navigationTitle(localizedEventTitle)
        .navigationBarTitleDisplayMode(.inline)
        .sheet(item: $calendarDraft) { draft in
            CalendarEventEditor(draft: draft)
        }
    }

    private var localizedEventTitle: String {
        settings.language == .german ? event.deTitle : event.trTitle
    }

    private var eventHeaderCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Label(localizedEventTitle, systemImage: event.symbol)
                .font(.title2.bold())
                .foregroundStyle(SalahTheme.deepTeal)

            Text(gregorianDateString(date, language: settings.language))
                .font(.subheadline.bold())
                .foregroundStyle(SalahTheme.teal)

            Text(hijriDateString(date, language: settings.language))
                .font(.headline)
        }
        .cardStyle(material: true)
    }

    private var calendarExportButton: some View {
        Button {
            calendarDraft = IslamicCalendarDraft(
                title: localizedEventTitle,
                date: date,
                notes: settings.t(
                    "SalahPath · berechnetes Hijri-Datum nach Umm al-Qura. Regionale Mondsichtung kann abweichen.",
                    "SalahPath · Ummü'l-Kurâ'ya göre hesaplanan hicrî tarih. Bölgesel hilal gözlemi farklı olabilir."
                )
            )
        } label: {
            Label(
                settings.t("In Apple Kalender eintragen", "Apple Takvim'e ekle"),
                systemImage: "calendar.badge.plus"
            )
            .font(.headline.bold())
            .frame(maxWidth: .infinity)
            .padding(.vertical, 13)
        }
        .buttonStyle(.plain)
        .foregroundStyle(.white)
        .background(
            SalahTheme.deepTeal,
            in: RoundedRectangle(cornerRadius: 15, style: .continuous)
        )
    }

    private var eventMeaningCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(settings.t("Was bedeutet dieser Tag?", "Bu gün ne anlama gelir?"))
                .font(.headline)
            Text(settings.language == .german ? event.deMeaning : event.trMeaning)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle()
    }

    private var eventRecommendationsCard: some View {
        let items = settings.language == .german ? event.deRecommended : event.trRecommended
        return VStack(alignment: .leading, spacing: 10) {
            Text(settings.t("Was ist empfohlen?", "Neler tavsiye edilir?"))
                .font(.headline)

            ForEach(items.indices, id: \.self) { index in
                HStack(alignment: .top, spacing: 9) {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundStyle(SalahTheme.teal)
                    Text(items[index])
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
        }
        .cardStyle()
    }

    private var eventCautionCard: some View {
        VStack(alignment: .leading, spacing: 7) {
            Label(
                settings.t("Nicht verwechseln", "Karıştırma"),
                systemImage: "exclamationmark.triangle.fill"
            )
            .font(.headline)
            .foregroundStyle(SalahTheme.gold)

            Text(settings.language == .german ? event.deCaution : event.trCaution)
                .font(.subheadline)
                .fixedSize(horizontal: false, vertical: true)
        }
        .cardStyle(material: true)
    }

    private var eventSourceCard: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(settings.t("Quelle & Kalenderhinweis", "Kaynak ve takvim notu"))
                .font(.headline)
            Text(settings.t(
                "Religiöse Einordnung nach Qur'an, authentischen Hadithen und Diyanet-Grunddarstellung. Das angezeigte Hijri-Datum wird mit Umm-al-Qura berechnet; regionale Mondsichtung kann den tatsächlichen Monatsbeginn verschieben.",
                "Dinî açıklama Kur'an, sahih hadisler ve Diyanet temel anlatımına dayanır. Gösterilen hicrî tarih Ummü'l-Kurâ hesabıdır; bölgesel hilal gözlemi gerçek ay başlangıcını değiştirebilir."
            ))
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .cardStyle(material: true)
    }
}
'''
text = text[:start] + new_detail + text[end:]
guide.write_text(text, encoding="utf-8")

# EventKit privacy descriptions for generated Info.plist builds.
usage_text = "SalahPath öffnet den Apple-Kalender, damit islamische Tage als Termine gespeichert werden können."
pbx = root / "SalahZeit.xcodeproj" / "project.pbxproj"
pbx_text = pbx.read_text(encoding="utf-8")
if "INFOPLIST_KEY_NSCalendarsWriteOnlyAccessUsageDescription" not in pbx_text:
    anchor = "GENERATE_INFOPLIST_FILE = YES;"
    if anchor in pbx_text:
        replacement = (
            anchor
            + '\n\t\t\t\tINFOPLIST_KEY_NSCalendarsUsageDescription = "'
            + usage_text
            + '";'
            + '\n\t\t\t\tINFOPLIST_KEY_NSCalendarsWriteOnlyAccessUsageDescription = "'
            + usage_text
            + '";'
        )
        pbx_text = pbx_text.replace(anchor, replacement)
        pbx.write_text(pbx_text, encoding="utf-8")
    else:
        plist = root / "SalahZeit" / "Info.plist"
        if not plist.exists():
            raise SystemExit("v438: could not add calendar usage descriptions")
        data = plistlib.loads(plist.read_bytes())
        data["NSCalendarsUsageDescription"] = usage_text
        data["NSCalendarsWriteOnlyAccessUsageDescription"] = usage_text
        plist.write_bytes(plistlib.dumps(data))

print("v438 applied: exact user-approved prayer rows + native Apple Calendar event export")
