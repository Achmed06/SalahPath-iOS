import Foundation
import CoreLocation
import Combine
import UIKit

@MainActor
final class LocationManager: NSObject, ObservableObject, CLLocationManagerDelegate {
    @Published private(set) var location: CLLocation?
    @Published private(set) var authorizationStatus: CLAuthorizationStatus
    @Published private(set) var heading: CLHeading?
    @Published private(set) var lastError: String?
    @Published private(set) var locality: String?

    private let manager = CLLocationManager()
    private let geocoder = CLGeocoder()
    private var lastGeocodedLocation: CLLocation?

    override init() {
        authorizationStatus = manager.authorizationStatus
        super.init()

        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.distanceFilter = kCLDistanceFilterNone
        manager.headingFilter = 1
        manager.headingOrientation = .portrait
    }

    func requestAccessAndStart() {
        switch manager.authorizationStatus {
        case .notDetermined:
            manager.requestWhenInUseAuthorization()
        case .authorizedWhenInUse, .authorizedAlways:
            startUpdates()
        case .denied, .restricted:
            lastError = "Standortzugriff ist deaktiviert. Aktiviere ihn in den iPhone-Einstellungen für SalahPath."
        @unknown default:
            break
        }
    }

    func refresh() {
        guard manager.authorizationStatus == .authorizedWhenInUse || manager.authorizationStatus == .authorizedAlways else {
            requestAccessAndStart()
            return
        }
        manager.requestLocation()
    }

    private func startUpdates() {
        updateHeadingOrientation(for: UIDevice.current.orientation)
        manager.startUpdatingLocation()
        if CLLocationManager.headingAvailable() {
            manager.startUpdatingHeading()
        }
    }

    func updateHeadingOrientation(for orientation: UIDeviceOrientation) {
        switch orientation {
        case .portrait:
            manager.headingOrientation = .portrait
        case .portraitUpsideDown:
            manager.headingOrientation = .portraitUpsideDown
        case .landscapeLeft:
            manager.headingOrientation = .landscapeLeft
        case .landscapeRight:
            manager.headingOrientation = .landscapeRight
        default:
            break
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            self.authorizationStatus = manager.authorizationStatus
            switch manager.authorizationStatus {
            case .authorizedWhenInUse, .authorizedAlways:
                self.lastError = nil
                self.startUpdates()
            case .denied, .restricted:
                self.lastError = "Standortzugriff ist deaktiviert. Aktiviere ihn in den iPhone-Einstellungen für SalahPath."
            default:
                break
            }
        }
    }

    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        let now = Date()
        guard let newest = locations.last(where: {
            $0.horizontalAccuracy >= 0 &&
            $0.horizontalAccuracy <= 1_000 &&
            abs($0.timestamp.timeIntervalSince(now)) <= 120
        }) else { return }

        Task { @MainActor in
            self.location = newest
            self.lastError = nil
            self.updateLocalityIfNeeded(for: newest)
        }
    }

    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateHeading newHeading: CLHeading) {
        guard newHeading.headingAccuracy >= 0 else { return }
        Task { @MainActor in
            if newHeading.headingAccuracy <= 50 || self.heading == nil {
                self.heading = newHeading
            }
        }
    }

    private func updateLocalityIfNeeded(for location: CLLocation) {
        if let lastGeocodedLocation, lastGeocodedLocation.distance(from: location) < 1_000, locality != nil { return }
        lastGeocodedLocation = location
        Task {
            do {
                let placemarks = try await geocoder.reverseGeocodeLocation(location)
                guard let placemark = placemarks.first else { return }
                let value = placemark.locality ?? placemark.subLocality ?? placemark.administrativeArea ?? placemark.country
                if let value, !value.isEmpty { locality = value }
            } catch {
                // Prayer time calculation must continue even when reverse geocoding is unavailable.
            }
        }
    }

    nonisolated func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        if let clError = error as? CLError, clError.code == .locationUnknown {
            return
        }
        Task { @MainActor in
            self.lastError = error.localizedDescription
        }
    }
}
