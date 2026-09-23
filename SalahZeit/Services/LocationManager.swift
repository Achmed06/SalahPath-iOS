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
    @Published private(set) var usesManualLocation = false

    private enum ManualLocationKeys {
        static let latitude = "manualLocationLatitude"
        static let longitude = "manualLocationLongitude"
        static let locality = "manualLocationLocality"
        static let enabled = "manualLocationEnabled"
    }

    private let manager = CLLocationManager()
    private let searchGeocoder = CLGeocoder()
    private let reverseGeocoder = CLGeocoder()
    private var lastGeocodedLocation: CLLocation?
    private var pendingDeviceLocationSwitch = false
    private var locationIntentRevision = 0
    private var reverseGeocodeRevision = 0

    override init() {
        authorizationStatus = manager.authorizationStatus

        let defaults = UserDefaults.standard
        if defaults.bool(forKey: ManualLocationKeys.enabled) {
            let latitude = (defaults.object(forKey: ManualLocationKeys.latitude) as? NSNumber)?.doubleValue
            let longitude = (defaults.object(forKey: ManualLocationKeys.longitude) as? NSNumber)?.doubleValue

            if let latitude, let longitude {
                let coordinate = CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
                if latitude.isFinite, longitude.isFinite, CLLocationCoordinate2DIsValid(coordinate) {
                    location = CLLocation(latitude: latitude, longitude: longitude)
                    locality = defaults.string(forKey: ManualLocationKeys.locality)
                    usesManualLocation = true
                } else {
                    defaults.removeObject(forKey: ManualLocationKeys.latitude)
                    defaults.removeObject(forKey: ManualLocationKeys.longitude)
                    defaults.removeObject(forKey: ManualLocationKeys.locality)
                    defaults.removeObject(forKey: ManualLocationKeys.enabled)
                }
            } else {
                defaults.removeObject(forKey: ManualLocationKeys.latitude)
                defaults.removeObject(forKey: ManualLocationKeys.longitude)
                defaults.removeObject(forKey: ManualLocationKeys.locality)
                defaults.removeObject(forKey: ManualLocationKeys.enabled)
            }
        }

        super.init()

        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.distanceFilter = kCLDistanceFilterNone
        manager.headingFilter = 1
        manager.headingOrientation = .portrait
    }

    func requestAccessAndStart() {
        if usesManualLocation {
            return
        }

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
        if usesManualLocation { return }
        guard manager.authorizationStatus == .authorizedWhenInUse || manager.authorizationStatus == .authorizedAlways else {
            requestAccessAndStart()
            return
        }
        manager.requestLocation()
    }

    func requestQiblaDeviceLocationAccess() {
        switch manager.authorizationStatus {
        case .notDetermined:
            manager.requestWhenInUseAuthorization()
        case .authorizedWhenInUse, .authorizedAlways:
            prepareQiblaHeading()
        case .denied, .restricted:
            lastError = "Standortzugriff ist deaktiviert. Aktiviere ihn in den iPhone-Einstellungen für SalahPath."
        @unknown default:
            break
        }
    }

    func prepareQiblaHeading() {
        updateHeadingOrientation(for: UIDevice.current.orientation)
        startHeadingIfAvailable()

        if manager.authorizationStatus == .authorizedWhenInUse ||
            manager.authorizationStatus == .authorizedAlways {
            // A real device location lets Core Location convert magnetic heading to true north.
            // Manual prayer-time coordinates remain untouched in didUpdateLocations.
            manager.startUpdatingLocation()
        }
    }

    func stopQiblaHeading() {
        manager.stopUpdatingHeading()
        manager.stopUpdatingLocation()
    }

    func useDeviceLocation() {
        locationIntentRevision &+= 1
        lastError = nil
        pendingDeviceLocationSwitch = true

        switch manager.authorizationStatus {
        case .notDetermined:
            manager.requestWhenInUseAuthorization()
        case .authorizedWhenInUse, .authorizedAlways:
            manager.requestLocation()
        case .denied, .restricted:
            pendingDeviceLocationSwitch = false
            lastError = "Standortzugriff ist deaktiviert. Aktiviere ihn in den iPhone-Einstellungen für SalahPath."
        @unknown default:
            pendingDeviceLocationSwitch = false
        }
    }

    @discardableResult
    func setManualLocation(searchText: String) async -> Bool {
        locationIntentRevision &+= 1
        let revision = locationIntentRevision
        pendingDeviceLocationSwitch = false
        reverseGeocodeRevision &+= 1
        reverseGeocoder.cancelGeocode()

        let query = searchText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !query.isEmpty else {
            lastError = "Bitte Ort, Stadt oder Postleitzahl eingeben."
            return false
        }

        do {
            let placemarks = try await searchGeocoder.geocodeAddressString(query)
            guard revision == locationIntentRevision else { return false }
            guard let placemark = placemarks.first, let resolvedLocation = placemark.location else {
                lastError = "Ort wurde nicht gefunden."
                return false
            }

            let label = [
                placemark.locality,
                placemark.administrativeArea,
                placemark.country
            ]
            .compactMap { $0 }
            .filter { !$0.isEmpty }
            .reduce(into: [String]()) { result, item in
                if !result.contains(item) { result.append(item) }
            }
            .joined(separator: ", ")

            let resolvedLabel = label.isEmpty ? query : label
            location = resolvedLocation
            locality = resolvedLabel
            usesManualLocation = true
            lastError = nil

            let defaults = UserDefaults.standard
            defaults.set(resolvedLocation.coordinate.latitude, forKey: ManualLocationKeys.latitude)
            defaults.set(resolvedLocation.coordinate.longitude, forKey: ManualLocationKeys.longitude)
            defaults.set(resolvedLabel, forKey: ManualLocationKeys.locality)
            defaults.set(true, forKey: ManualLocationKeys.enabled)

            return true
        } catch {
            guard revision == locationIntentRevision else { return false }
            lastError = "Ort konnte nicht gefunden werden. Bitte Eingabe prüfen."
            return false
        }
    }

    func clearManualLocation() {
        locationIntentRevision &+= 1
        pendingDeviceLocationSwitch = false
        usesManualLocation = false
        clearManualLocationStorage()
        location = nil
        locality = nil
    }

    private func clearManualLocationStorage() {
        let defaults = UserDefaults.standard
        defaults.removeObject(forKey: ManualLocationKeys.latitude)
        defaults.removeObject(forKey: ManualLocationKeys.longitude)
        defaults.removeObject(forKey: ManualLocationKeys.locality)
        defaults.removeObject(forKey: ManualLocationKeys.enabled)
    }

    private func adoptDeviceLocation(_ newLocation: CLLocation) {
        pendingDeviceLocationSwitch = false
        usesManualLocation = false
        clearManualLocationStorage()
        location = newLocation
        lastError = nil
        updateLocalityIfNeeded(for: newLocation)
    }

    private func startUpdates() {
        manager.requestLocation()
    }

    private func startHeadingIfAvailable() {
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
                self.pendingDeviceLocationSwitch = false
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
            if self.pendingDeviceLocationSwitch {
                self.adoptDeviceLocation(newest)
                self.manager.stopUpdatingLocation()
                return
            }

            if self.usesManualLocation {
                // The location update was only needed so CLHeading can provide trueHeading.
                self.manager.stopUpdatingLocation()
                return
            }

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
        reverseGeocodeRevision &+= 1
        let revision = reverseGeocodeRevision

        Task {
            do {
                let placemarks = try await reverseGeocoder.reverseGeocodeLocation(location)
                guard revision == reverseGeocodeRevision,
                      !usesManualLocation,
                      let currentLocation = self.location,
                      currentLocation.distance(from: location) < 1_000,
                      let placemark = placemarks.first else { return }

                let value = placemark.locality ?? placemark.subLocality ?? placemark.administrativeArea ?? placemark.country
                if let value, !value.isEmpty {
                    locality = value
                }
            } catch {
                // Prayer time calculation must continue even when reverse geocoding is unavailable.
            }
        }
    }

    nonisolated func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        let isLocationUnknown = (error as? CLError)?.code == .locationUnknown

        Task { @MainActor in
            let wasSwitchingToDeviceLocation = self.pendingDeviceLocationSwitch
            if wasSwitchingToDeviceLocation {
                self.pendingDeviceLocationSwitch = false
            }

            if isLocationUnknown {
                if wasSwitchingToDeviceLocation {
                    self.lastError = "Aktueller Standort ist vorübergehend nicht verfügbar. Bitte erneut versuchen."
                }
                return
            }

            self.lastError = error.localizedDescription
        }
    }
}
