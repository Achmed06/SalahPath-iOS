import SwiftUI
import Adhan
import UIKit
import CoreLocation

struct QiblaView: View {
    @EnvironmentObject private var locationManager: LocationManager
    @EnvironmentObject private var settings: SettingsStore

    var body: some View {
        Group {
            if let location = effectiveLocation {
                let coordinates = Coordinates(
                    latitude: location.coordinate.latitude,
                    longitude: location.coordinate.longitude
                )
                let qibla = Qibla(coordinates: coordinates).direction
                let qiblaDegrees = qibla.isFinite ? Int(qibla.rounded()) : nil
                let heading = currentHeading
                let headingDegrees = heading.map { Int($0.rounded()) }
                let relativeAngle = qibla.isFinite ? heading.map { normalized(qibla - $0) } : nil

                ScrollView {
                    VStack(spacing: 12) {
                        VStack(spacing: 3) {
                            Text(settings.t("Qibla", "Kıble"))
                                .font(.system(size: 21, weight: .bold, design: .serif))
                                .foregroundStyle(SalahTheme.ink)

                            Text(settings.t(
                                "Die Pfeilspitze zeigt direkt zur Kaaba.",
                                "Okun ucu doğrudan Kâbe'yi gösterir."
                            ))
                            .font(.system(size: 10.5, weight: .semibold))
                            .foregroundStyle(SalahTheme.mutedInk)
                        }

                        qiblaCompass(
                            relativeAngle: relativeAngle,
                            qiblaDegrees: qiblaDegrees,
                            headingDegrees: headingDegrees
                        )

                        HStack(spacing: 8) {
                            compactInfoTile(
                                icon: "location.north.circle.fill",
                                title: settings.t("Qibla", "Kıble"),
                                value: qiblaDegrees.map { "\($0)°" } ?? "—"
                            )
                            compactInfoTile(
                                icon: "iphone",
                                title: settings.t("Gerät", "Cihaz"),
                                value: headingDegrees.map { "\($0)°" } ?? "—"
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
                                            locationManager.authorizationStatus == .denied ||
                                            locationManager.authorizationStatus == .restricted
                                                ? "iPhone-Einstellungen öffnen"
                                                : "Gerätestandort für Kompass erlauben",
                                            locationManager.authorizationStatus == .denied ||
                                            locationManager.authorizationStatus == .restricted
                                                ? "iPhone ayarlarını aç"
                                                : "Pusula için cihaz konumuna izin ver"
                                        ),
                                        systemImage: locationManager.authorizationStatus == .denied ||
                                        locationManager.authorizationStatus == .restricted
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
                            .background(
                                SalahTheme.gold.opacity(0.12),
                                in: RoundedRectangle(cornerRadius: 12, style: .continuous)
                            )
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
                            .background(
                                SalahTheme.gold.opacity(0.12),
                                in: RoundedRectangle(cornerRadius: 12, style: .continuous)
                            )
                        }

                        VStack(spacing: 0) {
                            infoRow(
                                icon: "location.fill",
                                title: isScreenshotQA
                                    ? settings.t("Köln · QA-Teststandort", "Köln · QA test konumu")
                                    : (locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
                            )
                            infoRow(
                                icon: "compass.drawing",
                                title: settings.t(
                                    "iPhone flach halten. Die Pfeilspitze ist die Gebetsrichtung.",
                                    "iPhone'u düz tut. Okun ucu namaz yönüdür."
                                )
                            )
                            infoRow(
                                icon: "arrow.triangle.2.circlepath",
                                title: settings.t(
                                    "Bei Bedarf kurz in einer Acht bewegen",
                                    "Gerekirse kısa süre sekiz şeklinde hareket ettir"
                                )
                            )
                        }
                        .background(
                            SalahTheme.cream,
                            in: RoundedRectangle(cornerRadius: 15, style: .continuous)
                        )
                        .overlay {
                            RoundedRectangle(cornerRadius: 15)
                                .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
                        }
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
                                locationManager.authorizationStatus == .denied ||
                                locationManager.authorizationStatus == .restricted
                                    ? "iPhone-Einstellungen öffnen"
                                    : "Aktuellen Standort verwenden",
                                locationManager.authorizationStatus == .denied ||
                                locationManager.authorizationStatus == .restricted
                                    ? "iPhone ayarlarını aç"
                                    : "Mevcut konumu kullan"
                            ),
                            systemImage: locationManager.authorizationStatus == .denied ||
                            locationManager.authorizationStatus == .restricted
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
            locationManager.prepareQiblaHeading()
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

    @ViewBuilder
    private func qiblaCompass(
        relativeAngle: Double?,
        qiblaDegrees: Int?,
        headingDegrees: Int?
    ) -> some View {
        let aligned = relativeAngle.map { abs($0) <= 5 } ?? false

        VStack(spacing: 9) {
            ZStack {
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [
                                SalahTheme.cream,
                                SalahTheme.softTeal.opacity(0.45)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 280, height: 280)
                    .shadow(color: SalahTheme.deepTeal.opacity(0.08), radius: 10, y: 4)

                Circle()
                    .stroke(SalahTheme.gold.opacity(0.72), lineWidth: 1.8)
                    .frame(width: 270, height: 270)

                Circle()
                    .stroke(SalahTheme.teal.opacity(0.16), lineWidth: 1)
                    .frame(width: 230, height: 230)

                ForEach(0..<72, id: \.self) { index in
                    Capsule()
                        .fill(
                            index % 18 == 0
                                ? SalahTheme.deepTeal.opacity(0.82)
                                : SalahTheme.teal.opacity(index % 6 == 0 ? 0.34 : 0.16)
                        )
                        .frame(
                            width: index % 18 == 0 ? 3 : 1.1,
                            height: index % 18 == 0 ? 16 : (index % 6 == 0 ? 10 : 6)
                        )
                        .offset(y: -125)
                        .rotationEffect(.degrees(Double(index) * 5))
                }

                cardinalLabel("N", x: 0, y: -104)
                cardinalLabel("O", x: 105, y: 0)
                cardinalLabel("S", x: 0, y: 104)
                cardinalLabel("W", x: -105, y: 0)

                if let relativeAngle {
                    QiblaNeedle()
                        .fill(
                            LinearGradient(
                                colors: [
                                    SalahTheme.gold,
                                    SalahTheme.teal
                                ],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .frame(width: 54, height: 146)
                        .offset(y: -40)
                        .rotationEffect(.degrees(relativeAngle))
                        .shadow(color: SalahTheme.deepTeal.opacity(0.16), radius: 4, y: 2)
                        .animation(.easeOut(duration: 0.18), value: relativeAngle)

                    kaabaMarker
                        .offset(qiblaMarkerOffset(relativeAngle: relativeAngle, radius: 120))

                    Circle()
                        .fill(SalahTheme.deepTeal)
                        .frame(width: 18, height: 18)
                        .overlay {
                            Circle()
                                .fill(SalahTheme.gold)
                                .frame(width: 7, height: 7)
                        }
                } else {
                    ProgressView()
                        .tint(SalahTheme.teal)
                }
            }
            .frame(height: 286)
            .accessibilityElement(children: .ignore)
            .accessibilityLabel(settings.t("Qibla-Kompass", "Kıble pusulası"))
            .accessibilityValue(
                compassAccessibilityValue(
                    qiblaDegrees: qiblaDegrees,
                    headingDegrees: headingDegrees
                )
            )
            .accessibilityHint(settings.t(
                "Die Pfeilspitze zeigt zur Kaaba. Drehe dich, bis die Pfeilspitze nach oben zeigt.",
                "Okun ucu Kâbe'yi gösterir. Ok yukarıyı gösterene kadar dön."
            ))

            HStack(spacing: 7) {
                Image(systemName: aligned ? "checkmark.seal.fill" : "arrow.up.circle.fill")
                    .foregroundStyle(aligned ? SalahTheme.teal : SalahTheme.gold)

                Text(
                    aligned
                        ? settings.t("Qibla ausgerichtet", "Kıbleye hizalandı")
                        : settings.t(
                            "Folge der Pfeilspitze zur Kaaba",
                            "Kâbe için okun ucunu takip et"
                        )
                )
                .font(.system(size: 11, weight: .bold))
                .foregroundStyle(SalahTheme.ink)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(
                (aligned ? SalahTheme.softTeal : SalahTheme.gold.opacity(0.10)),
                in: Capsule()
            )
        }
    }

    private var kaabaMarker: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 5, style: .continuous)
                .fill(Color.black.opacity(0.92))
                .frame(width: 38, height: 31)

            Rectangle()
                .fill(SalahTheme.gold)
                .frame(width: 38, height: 4)
                .offset(y: -6)

            Image(systemName: "star.fill")
                .font(.system(size: 6))
                .foregroundStyle(SalahTheme.gold.opacity(0.9))
                .offset(y: 6)
        }
        .overlay {
            RoundedRectangle(cornerRadius: 5, style: .continuous)
                .stroke(SalahTheme.gold.opacity(0.8), lineWidth: 1)
        }
        .shadow(color: Color.black.opacity(0.12), radius: 3, y: 2)
        .accessibilityHidden(true)
    }

    private func qiblaMarkerOffset(relativeAngle: Double, radius: CGFloat) -> CGSize {
        let radians = relativeAngle * .pi / 180
        return CGSize(
            width: sin(radians) * radius,
            height: -cos(radians) * radius
        )
    }

    private func cardinalLabel(_ text: String, x: CGFloat, y: CGFloat) -> some View {
        Text(text)
            .font(.system(size: 10, weight: .black))
            .foregroundStyle(SalahTheme.deepTeal)
            .offset(x: x, y: y)
    }

    private func compassAccessibilityValue(qiblaDegrees: Int?, headingDegrees: Int?) -> String {
        guard let qiblaDegrees else {
            return settings.t(
                "Qibla-Richtung momentan nicht verfügbar.",
                "Kıble yönü şu anda kullanılamıyor."
            )
        }

        if let headingDegrees {
            return settings.t(
                "Qibla \(qiblaDegrees) Grad. Gerät \(headingDegrees) Grad. Die Pfeilspitze zeigt zur Kaaba.",
                "Kıble \(qiblaDegrees) derece. Cihaz \(headingDegrees) derece. Okun ucu Kâbe'yi gösterir."
            )
        }

        return settings.t(
            "Qibla \(qiblaDegrees) Grad. Geräteausrichtung noch nicht verfügbar.",
            "Kıble \(qiblaDegrees) derece. Cihaz yönü henüz mevcut değil."
        )
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
        .background(
            SalahTheme.cream,
            in: RoundedRectangle(cornerRadius: 14, style: .continuous)
        )
        .overlay {
            RoundedRectangle(cornerRadius: 14)
                .stroke(SalahTheme.gold.opacity(0.40), lineWidth: 1)
        }
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
        .overlay(alignment: .bottom) {
            Divider()
                .padding(.leading, 50)
                .opacity(0.34)
        }
    }

    private func openAppSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
    }

    private var isScreenshotQA: Bool {
        ProcessInfo.processInfo.environment["SALAH_QA_SCREENSHOT"] == "1"
    }

    private var effectiveLocation: CLLocation? {
        if isScreenshotQA {
            return CLLocation(latitude: 50.9375, longitude: 6.9603)
        }
        return locationManager.location
    }

    private var headingAccuracy: Double? {
        guard !isScreenshotQA else { return nil }
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
        if isScreenshotQA { return 0 }

        guard let heading = locationManager.heading,
              heading.headingAccuracy.isFinite,
              heading.headingAccuracy >= 0 else {
            return nil
        }

        if heading.trueHeading.isFinite, heading.trueHeading >= 0 {
            return normalized360(heading.trueHeading)
        }

        if heading.magneticHeading.isFinite, heading.magneticHeading >= 0 {
            return normalized360(heading.magneticHeading)
        }

        return nil
    }

    private func normalized(_ angle: Double) -> Double {
        var result = angle.truncatingRemainder(dividingBy: 360)
        if result > 180 { result -= 360 }
        if result < -180 { result += 360 }
        return result
    }

    private func normalized360(_ angle: Double) -> Double {
        var result = angle.truncatingRemainder(dividingBy: 360)
        if result < 0 { result += 360 }
        return result
    }
}

private struct QiblaNeedle: Shape {
    func path(in rect: CGRect) -> Path {
        let midX = rect.midX
        let headY = rect.minY
        let shoulderY = rect.minY + rect.height * 0.30
        let tailY = rect.maxY

        var path = Path()
        path.move(to: CGPoint(x: midX, y: headY))
        path.addLine(to: CGPoint(x: rect.maxX, y: shoulderY))
        path.addLine(to: CGPoint(x: midX + rect.width * 0.16, y: shoulderY))
        path.addLine(to: CGPoint(x: midX + rect.width * 0.16, y: tailY))
        path.addLine(to: CGPoint(x: midX - rect.width * 0.16, y: tailY))
        path.addLine(to: CGPoint(x: midX - rect.width * 0.16, y: shoulderY))
        path.addLine(to: CGPoint(x: rect.minX, y: shoulderY))
        path.closeSubpath()
        return path
    }
}
