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
                let coordinates = Coordinates(latitude: location.coordinate.latitude, longitude: location.coordinate.longitude)
                let qibla = Qibla(coordinates: coordinates).direction
                let qiblaDegrees = qibla.isFinite ? Int(qibla.rounded()) : nil
                let heading = currentHeading
                let headingDegrees = heading.map { Int($0.rounded()) }
                let rotation = qibla.isFinite ? heading.map { normalized(qibla - $0) } : nil

                ScrollView {
                    VStack(spacing: 11) {
                        HStack(spacing: 11) {
                            ZStack {
                                Circle()
                                    .fill(
                                        LinearGradient(
                                            colors: [
                                                SalahTheme.deepTeal,
                                                SalahTheme.teal
                                            ],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .frame(width: 46, height: 46)
                                    .shadow(color: SalahTheme.deepTeal.opacity(0.20), radius: 10, y: 5)

                                QiblaKaabaGlyph()
                                    .frame(width: 28, height: 28)
                            }

                            VStack(alignment: .leading, spacing: 2) {
                                Text(settings.t("Qibla", "Kıble"))
                                    .font(.system(size: 23, weight: .bold, design: .serif))
                                    .foregroundStyle(SalahTheme.ink)
                                Text(settings.t("Richte dein Herz zur Kaaba", "Kalbini Kâbe'ye yönelt"))
                                    .font(.system(size: 11, weight: .semibold))
                                    .foregroundStyle(SalahTheme.mutedInk)
                            }

                            Spacer()
                        }
                        .padding(.horizontal, 4)

                        QiblaCompassVisual(rotation: rotation)
                        .accessibilityElement(children: .ignore)
                        .accessibilityLabel(settings.t("Qibla-Kompass", "Kıble pusulası"))
                        .accessibilityValue(
                            compassAccessibilityValue(
                                qiblaDegrees: qiblaDegrees,
                                headingDegrees: headingDegrees
                            )
                        )
                        .accessibilityHint(settings.t(
                            "Die Pfeilspitze zeigt immer direkt zur Kaaba. Drehe das iPhone, bis die Kaaba oben auf 12 Uhr steht.",
                            "Okun ucu her zaman doğrudan Kâbe'yi gösterir. Kâbe saat 12 yönünde üstte olana kadar iPhone'u çevir."
                        ))

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
                            infoRow(
                                icon: "location.fill",
                                title: isScreenshotQA
                                    ? settings.t("Köln · QA-Teststandort", "Köln · QA test konumu")
                                    : (locationManager.locality ?? settings.t("Aktueller Standort", "Mevcut konum"))
                            )
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

    private func compassAccessibilityValue(qiblaDegrees: Int?, headingDegrees: Int?) -> String {
        guard let qiblaDegrees else {
            return settings.t(
                "Qibla-Richtung momentan nicht verfügbar.",
                "Kıble yönü şu anda kullanılamıyor."
            )
        }

        if let headingDegrees {
            return settings.t(
                "Qibla \(qiblaDegrees) Grad. Gerät \(headingDegrees) Grad.",
                "Kıble \(qiblaDegrees) derece. Cihaz \(headingDegrees) derece."
            )
        }

        return settings.t(
            "Qibla \(qiblaDegrees) Grad. Geräteausrichtung noch nicht verfügbar.",
            "Kıble \(qiblaDegrees) derece. Cihaz yönü henüz mevcut değil."
        )
    }

    private func compactInfoTile(icon: String, title: String, value: String) -> some View {
        VStack(spacing: 4) {
            Group {
                if icon == "location.north.circle.fill" {
                    SalahFeatureIcon(kind: "qibla")
                        .frame(width: 28, height: 28)
                } else {
                    Image(systemName: icon)
                        .font(.system(size: 21, weight: .semibold))
                        .foregroundStyle(SalahTheme.teal)
                }
            }
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


private struct QiblaCompassVisual: View {
    @EnvironmentObject private var settings: SettingsStore
    let rotation: Double?

    private var isAligned: Bool {
        guard let rotation else { return false }
        return abs(rotation) <= 4
    }

    var body: some View {
        ZStack {
            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color.white.opacity(0.98),
                            SalahTheme.cream,
                            SalahTheme.softTeal.opacity(0.24)
                        ],
                        center: .topLeading,
                        startRadius: 10,
                        endRadius: 155
                    )
                )
                .frame(width: 286, height: 286)
                .overlay {
                    Circle()
                        .stroke(
                            LinearGradient(
                                colors: [
                                    SalahTheme.gold.opacity(0.95),
                                    SalahTheme.gold.opacity(0.32),
                                    SalahTheme.teal.opacity(0.32),
                                    SalahTheme.gold.opacity(0.82)
                                ],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ),
                            lineWidth: 2.2
                        )
                }
                .shadow(color: SalahTheme.deepTeal.opacity(0.12), radius: 18, y: 9)
                .shadow(color: SalahTheme.gold.opacity(0.12), radius: 2, y: -1)

            Circle()
                .stroke(SalahTheme.teal.opacity(0.09), lineWidth: 18)
                .frame(width: 250, height: 250)

            Circle()
                .stroke(SalahTheme.gold.opacity(0.26), lineWidth: 1)
                .frame(width: 232, height: 232)

            ForEach(0..<72, id: \.self) { index in
                Capsule()
                    .fill(
                        index % 18 == 0
                            ? SalahTheme.deepTeal.opacity(0.88)
                            : index % 6 == 0
                                ? SalahTheme.teal.opacity(0.48)
                                : SalahTheme.teal.opacity(0.18)
                    )
                    .frame(
                        width: index % 18 == 0 ? 3 : (index % 6 == 0 ? 2 : 1),
                        height: index % 18 == 0 ? 17 : (index % 6 == 0 ? 11 : 6)
                    )
                    .offset(y: -121)
                    .rotationEffect(.degrees(Double(index) * 5))
            }

            compassLabel(settings.t("N", "K"), x: 0, y: -100, emphasized: true)
            compassLabel(settings.t("O", "D"), x: 100, y: 0)
            compassLabel(settings.t("S", "G"), x: 0, y: 100)
            compassLabel(settings.t("W", "B"), x: -100, y: 0)

            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            SalahTheme.gold.opacity(isAligned ? 0.22 : 0.10),
                            SalahTheme.teal.opacity(0.035),
                            .clear
                        ],
                        center: .center,
                        startRadius: 6,
                        endRadius: 92
                    )
                )
                .frame(width: 184, height: 184)
                .animation(.easeOut(duration: 0.2), value: isAligned)

            if let rotation {
                let radians = rotation * .pi / 180
                let targetRadius: CGFloat = 104
                let targetX = sin(radians) * targetRadius
                let targetY = -cos(radians) * targetRadius

                ZStack {
                    QiblaNeedleShape()
                        .fill(
                            LinearGradient(
                                colors: [
                                    SalahTheme.gold,
                                    SalahTheme.teal,
                                    SalahTheme.deepTeal
                                ],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .overlay {
                            QiblaNeedleShape()
                                .stroke(Color.white.opacity(0.70), lineWidth: 0.8)
                        }
                        .frame(width: 226, height: 226)
                        .shadow(color: SalahTheme.deepTeal.opacity(0.24), radius: 4, y: 2)
                        .rotationEffect(.degrees(rotation))

                    QiblaKaabaMarker(aligned: isAligned)
                        .offset(x: targetX, y: targetY)
                }
                .frame(width: 226, height: 226)
                .animation(.easeOut(duration: 0.16), value: rotation)
            } else {
                ProgressView()
                    .tint(SalahTheme.teal)
            }

            ZStack {
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [SalahTheme.deepTeal, SalahTheme.teal],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 31, height: 31)
                    .shadow(color: SalahTheme.deepTeal.opacity(0.24), radius: 5, y: 2)

                Circle()
                    .stroke(SalahTheme.gold, lineWidth: 3)
                    .frame(width: 17, height: 17)

                Circle()
                    .fill(SalahTheme.gold)
                    .frame(width: 5, height: 5)
            }

            if isAligned {
                Text(settings.t("AUSGERICHTET", "HİZALI"))
                    .font(.system(size: 8.5, weight: .black))
                    .tracking(1.2)
                    .foregroundStyle(SalahTheme.deepTeal)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 5)
                    .background(.ultraThinMaterial, in: Capsule())
                    .overlay {
                        Capsule()
                            .stroke(SalahTheme.gold.opacity(0.65), lineWidth: 1)
                    }
                    .offset(y: 91)
                    .transition(.scale.combined(with: .opacity))
            }
        }
        .frame(width: 300, height: 300)
    }

    private func compassLabel(
        _ text: String,
        x: CGFloat,
        y: CGFloat,
        emphasized: Bool = false
    ) -> some View {
        Text(text)
            .font(.system(size: emphasized ? 12 : 9, weight: .black, design: .rounded))
            .foregroundStyle(emphasized ? SalahTheme.deepTeal : SalahTheme.mutedInk.opacity(0.82))
            .offset(x: x, y: y)
    }
}

private struct QiblaNeedleShape: Shape {
    func path(in rect: CGRect) -> Path {
        let midX = rect.midX
        let midY = rect.midY
        let top = rect.minY + 15
        let shoulderY = rect.minY + 50
        let stemTop = rect.minY + 47
        let stemHalf: CGFloat = 6
        let wing: CGFloat = 20

        var path = Path()
        path.move(to: CGPoint(x: midX, y: top))
        path.addLine(to: CGPoint(x: midX + wing, y: shoulderY))
        path.addLine(to: CGPoint(x: midX + stemHalf, y: stemTop))
        path.addLine(to: CGPoint(x: midX + stemHalf, y: midY))
        path.addLine(to: CGPoint(x: midX - stemHalf, y: midY))
        path.addLine(to: CGPoint(x: midX - stemHalf, y: stemTop))
        path.addLine(to: CGPoint(x: midX - wing, y: shoulderY))
        path.closeSubpath()
        return path
    }
}

private struct QiblaKaabaMarker: View {
    let aligned: Bool

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 7, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [
                            Color.black.opacity(0.98),
                            Color.black.opacity(0.86)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: 48, height: 42)

            Rectangle()
                .fill(
                    LinearGradient(
                        colors: [
                            SalahTheme.gold.opacity(0.98),
                            SalahTheme.gold.opacity(0.68)
                        ],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(width: 48, height: 5)
                .offset(y: -8)

            RoundedRectangle(cornerRadius: 2)
                .stroke(SalahTheme.gold.opacity(0.88), lineWidth: 1)
                .frame(width: 29, height: 19)
                .offset(y: 6)

            Rectangle()
                .fill(SalahTheme.gold.opacity(0.78))
                .frame(width: 4, height: 12)
                .offset(x: 9, y: 7)
        }
        .rotation3DEffect(.degrees(-7), axis: (x: 1, y: -0.7, z: 0))
        .shadow(
            color: aligned ? SalahTheme.gold.opacity(0.52) : SalahTheme.deepTeal.opacity(0.18),
            radius: aligned ? 11 : 5,
            y: 3
        )
        .scaleEffect(aligned ? 1.06 : 1)
        .animation(.easeOut(duration: 0.2), value: aligned)
    }
}

private struct QiblaKaabaGlyph: View {
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 4, style: .continuous)
                .fill(Color.black.opacity(0.92))
                .frame(width: 24, height: 21)

            Rectangle()
                .fill(SalahTheme.gold)
                .frame(width: 24, height: 3)
                .offset(y: -4)

            RoundedRectangle(cornerRadius: 1.5)
                .stroke(SalahTheme.gold.opacity(0.9), lineWidth: 1)
                .frame(width: 14, height: 10)
                .offset(y: 3)
        }
    }
}
