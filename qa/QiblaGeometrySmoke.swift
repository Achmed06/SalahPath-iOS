import Foundation

func verify(_ bearing: Double, _ heading: Double, _ expected: Double?) {
    let actual = QiblaGeometry.arrowRotation(bearing: bearing, trueHeading: heading)
    precondition(actual == expected, "bearing \(bearing), heading \(heading): \(String(describing: actual))")
}

@main enum QiblaGeometrySmoke {
    static func main() {
        verify(0, 0, 0)
        verify(90, 0, 90)
        verify(0, 90, -90)
        verify(10, 350, 20)
        verify(350, 10, -20)
        verify(270, 90, 180)
        verify(90, -1, nil)
        verify(.nan, 90, nil)
        print("Qibla arrow geometry: OK")
    }
}
