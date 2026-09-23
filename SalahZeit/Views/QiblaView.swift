import SwiftUI
import Adhan
import UIKit

struct QiblaView: View {
    @EnvironmentObject private var locationManager: LocationManager
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        Group {
            if let location = locationManager.location {
                let coordinates = Coordinates(latitude: location.coordinate.latitude, longitude: location.coordinate.longitude)
                let qibla = Qibla(coordinates: coordinates).direction
                let heading = currentHeading
                let rotation = heading.map { normalized(qibla - $0) }

                ScrollView {
                    VStack(spacing: 11) {
                        VStack(spacing: 2) {
                            Text(settings.t("Qibla", "Kıble"))
                                .font(.system(size: 20, weight: .bold, design: .serif))
                                .foregroundStyle(SalahTheme.ink)
                            Text(settings.t("Qibla-Richtung", "Kıble Yönü"))
                                .font(.system(size: 10, weight: .semibold))
                                .foregroundStyle(SalahTheme.mutedInk)
                        }

                        ZStack {
                            Circle()
                                .fill(SalahTheme.cream)
                                .frame(width: 268, height: 268)
                                .shadow(color: SalahTheme.deepTeal.opacity(0.055), radius: 8, y: 3)

                            Circle()
                                .stroke(SalahTheme.gold.opacity(0.60), lineWidth: 1.5)
                                .frame(width: 258, height: 258)

                            Circle()
                                .stroke(SalahTheme.teal.opacity(0.14), lineWidth: 1)
                                .frame(width: 226, height: 226)

                            ForEach(0..<36, id: \.self) { index in
                                Capsule()
                                    .fill(SalahTheme.teal.opacity(index % 9 == 0 ? 0.78 : 0.22))
                                    .frame(width: index % 9 == 0 ? 2.8 : 1.3, height: index % 9 == 0 ? 15 : 7)
                                    .offset(y: -120)
                                    .rotationEffect(.degrees(Double(index) * 10))
                            }

                            Text("N")
                                .font(.system(size: 10, weight: .black))
                                .foregroundStyle(SalahTheme.teal)
                                .offset(y: -103)

                            ZStack {
                                RoundedRectangle(cornerRadius: 4)
                                    .fill(Color.black.opacity(0.90))
                                    .frame(width: 45, height: 39)
                                Rectangle()
                                    .fill(SalahTheme.gold)
                                    .frame(width: 45, height: 4)
                                    .offset(y: -7)
                            }
                            .offset(y: 27)

                            if let rotation {
                                Image(systemName: "location.north.fill")
                                    .font(.system(size: 88, weight: .medium))
                                    .foregroundStyle(SalahTheme.teal.opacity(0.92))
                                    .rotationEffect(.degrees(rotation))
                                    .offset(y: -25)
                                    .animation(.easeOut(duration: 0.18), value: rotation)
                            } else {
                                ProgressView()
                                    .tint(SalahTheme.teal)
                                    .offset(y: -25)
                            }
                        }
                        .accessibilityElement(children: .ignore)
                        .accessibilityLabel(settings.t("Qibla-Kompass", "Kıble pusulası"))
                        .accessibilityValue(
                            heading.map {
                                settings.t(
                                    "Qibla \(Int(qibla.rounded())) Grad. Gerät \(Int($0.rounded())) Grad.",
                                    "Kıble \(Int(qibla.rounded())) derece. Cihaz \(Int($0.rounded())) derece."
                                )
                            } ?? settings.t(
                                "Qibla \(Int(qibla.rounded())) Grad. Geräteausrichtung noch nicht verfügbar.",
                                "Kıble \(Int(qibla.rounded())) derece. Cihaz yönü henüz mevcut değil."
                            )
                        )
                        .accessibilityHint(settings.t(
                            "Drehe das iPhone, bis der Qibla-Pfeil nach oben zeigt.",
                            "Kıble oku yukarıyı gösterene kadar iPhone'u çevir."
                        ))

                        HStack(spacing: 8) {
                            compactInfoTile(icon: "location.north.circle.fill", title: settings.t("Qibla", "Kıble"), value: "\(Int(qibla.rounded()))°")
                            compactInfoTile(
                                icon: "iphone",
                                title: settings.t("Gerät", "Cihaz"),
                                value: heading.map { "\(Int($0.rounded()))°" } ?? "—"
                            )
                        }

                        if locationManager.usesManualLocation && !deviceLocationAuthorized {
                            VStack(alignment: .leading, spacing: 9) {
                                HStack(alignment: .top, spacing: 9) {
                                    Image(systemName: "location.slash.fill")
                                        .foregroundStyle(SalahTheme.gold)
                                    Text(settings.t(
                                        "Für eine exakt drehende Qibla-Nadel braucht iOS zusätzlich den aktuellen Gerätestandort, damit magnetischer Norden in geografischen Norden umgerechnet werden kann. Dein manuell gewählter Ort für Gebetszeiten bleibt dabei unverändert.",
                                        "Kıble ibresinin doğru dönmesi için iOS ayrıca cihazın güncel konumuna ihtiyaç duyar; böylece manyetik kuzey gerçek kuzeye çevrilebilir. Namaz vakitleri için manuel seçtiğin konum değişmeden kalır."
                                    ))
                                    .font(.system(size: 10, weight: .semibold))
                                    .foregroundStyle(SalahTheme.ink)
                                    .fixedSize(horizontal: false, vertical: true)
                                }

                                Button {
                                    if locationManager.authorizationStatus == .denied ||
                                        locationManager.authorizationStatus == .restricted {
                                        openAppSettings()
                                    } else {
                                        locationManager.requestQiblaDeviceLocationAccess()
                                    }
                                } label: {
                                    Label(
                                        settings.t(
                                            locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                                ? "iPhone-Einstellungen öffnen"
                                                : "Gerätestandort für Kompass erlauben",
                                            locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                                ? "iPhone ayarlarını aç"
                                                : "Pusula için cihaz konumuna izin ver"
                                        ),
                                        systemImage: locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                            ? "gear"
                                            : "location.fill"
                                    )
                                    .font(.system(size: 10.5, weight: .bold))
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 8)
                                }
                                .buttonStyle(.borderedProminent)
                                .tint(SalahTheme.teal)
                            }
                            .padding(10)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(SalahTheme.gold.opacity(0.12), in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                        }

                        if let accuracy = headingAccuracy, accuracy > 20 {
                            HStack(alignment: .top, spacing: 9) {
                                Image(systemName: "exclamationmark.triangle.fill")
                                    .foregroundStyle(SalahTheme.gold)
                                Text(settings.t(
                                    "Kompassgenauigkeit ist gerade niedrig (±\(Int(accuracy.rounded()))°). Entferne magnetische Hüllen/Zubehör und bewege das iPhone kurz in einer Acht.",
                                    "Pusula doğruluğu şu anda düşük (±\(Int(accuracy.rounded()))°). Manyetik kılıf/aksesuarları uzaklaştır ve iPhone'u kısa süre sekiz şeklinde hareket ettir."
                                ))
                                .font(.system(size: 10, weight: .semibold))
                                .foregroundStyle(SalahTheme.ink)
                                .fixedSize(horizontal: false, vertical: true)
                            }
                            .padding(10)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(SalahTheme.gold.opacity(0.12), in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                        }

                        VStack(spacing: 0) {
                            infoRow(icon: "location.fill", title: locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
                            infoRow(icon: "compass.drawing", title: settings.t("iPhone flach halten", "iPhone'u düz tut"))
                            infoRow(icon: "arrow.triangle.2.circlepath", title: settings.t("Bei Bedarf kurz in einer Acht bewegen", "Gerekirse kısa süre sekiz şeklinde hareket ettir"))
                        }
                        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 15, style: .continuous))
                        .overlay { RoundedRectangle(cornerRadius: 15).stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1) }
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 10)
                }
                .scrollIndicators(.hidden)
            } else {
                VStack(spacing: 14) {
                    ContentUnavailableView(
                        settings.t("Standort benötigt", "Konum gerekli"),
                        systemImage: "location.slash",
                        description: Text(settings.t(
                            "Die Qibla-Richtung wird aus deinem Standort berechnet. Du kannst den Gerätestandort verwenden oder im Profil einen Ort manuell festlegen.",
                            "Kıble yönü konumuna göre hesaplanır. Cihaz konumunu kullanabilir veya profilde bir yeri manuel seçebilirsin."
                        ))
                    )

                    Button {
                        if locationManager.authorizationStatus == .denied ||
                            locationManager.authorizationStatus == .restricted {
                            openAppSettings()
                        } else {
                            locationManager.useDeviceLocation()
                        }
                    } label: {
                        Label(
                            settings.t(
                                locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                    ? "iPhone-Einstellungen öffnen"
                                    : "Aktuellen Standort verwenden",
                                locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                    ? "iPhone ayarlarını aç"
                                    : "Mevcut konumu kullan"
                            ),
                            systemImage: locationManager.authorizationStatus == .denied || locationManager.authorizationStatus == .restricted
                                ? "gear"
                                : "location.fill"
                        )
                        .font(.headline)
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(SalahTheme.teal)
                }
                .padding()
            }
        }
        .background(SalahTheme.page.ignoresSafeArea())
        .navigationTitle(settings.t("Qibla", "Kıble"))
        .navigationBarTitleDisplayMode(.inline)
        .tint(SalahTheme.teal)
        .onAppear {
            UIDevice.current.beginGeneratingDeviceOrientationNotifications()
            locationManager.updateHeadingOrientation(for: UIDevice.current.orientation)

            if deviceLocationAuthorized {
                locationManager.prepareQiblaHeading()
            }
        }
        .onChange(of: locationManager.authorizationStatus) { _, status in
            if status == .authorizedWhenInUse || status == .authorizedAlways {
                locationManager.prepareQiblaHeading()
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: UIDevice.orientationDidChangeNotification)) { _ in
            locationManager.updateHeadingOrientation(for: UIDevice.current.orientation)
        }
        .onDisappear {
            locationManager.stopQiblaHeading()
            UIDevice.current.endGeneratingDeviceOrientationNotifications()
        }
    }

    private func compactInfoTile(icon: String, title: String, value: String) -> some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .font(.system(size: 21, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
            Text(title)
                .font(.system(size: 9, weight: .bold))
                .foregroundStyle(SalahTheme.mutedInk)
            Text(value)
                .font(.system(size: 18, weight: .bold).monospacedDigit())
                .foregroundStyle(SalahTheme.ink)
        }
        .frame(maxWidth: .infinity, minHeight: 82)
        .background(SalahTheme.cream, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay { RoundedRectangle(cornerRadius: 14).stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1) }
    }

    private func infoRow(icon: String, title: String) -> some View {
        HStack(spacing: 9) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 14, weight: .bold))
                .foregroundStyle(SalahTheme.teal)
            Image(systemName: icon)
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(SalahTheme.teal)
                .frame(width: 20)
            Text(title)
                .font(.system(size: 10.5, weight: .semibold))
                .foregroundStyle(SalahTheme.ink)
            Spacer()
        }
        .padding(.horizontal, 11)
        .padding(.vertical, 10)
        .overlay(alignment: .bottom) { Divider().padding(.leading, 50).opacity(0.34) }
    }

    private func openAppSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
    }

    private var headingAccuracy: Double? {
        guard let heading = locationManager.heading,
              heading.headingAccuracy.isFinite,
              heading.headingAccuracy >= 0 else { return nil }
        return heading.headingAccuracy
    }

    private var deviceLocationAuthorized: Bool {
        locationManager.authorizationStatus == .authorizedWhenInUse ||
        locationManager.authorizationStatus == .authorizedAlways
    }

    private var currentHeading: Double? {
        guard let heading = locationManager.heading,
              heading.headingAccuracy.isFinite,
              heading.headingAccuracy >= 0,
              heading.trueHeading.isFinite,
              heading.trueHeading >= 0 else { return nil }
        return heading.trueHeading
    }

    private func normalized(_ angle: Double) -> Double {
        var result = angle.truncatingRemainder(dividingBy: 360)
        if result > 180 { result -= 360 }
        if result < -180 { result += 360 }
        return result
    }
}
