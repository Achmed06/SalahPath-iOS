import Foundation

/// All angles are clockwise from true north. The result rotates an arrow whose tip is at 12 o'clock.
enum QiblaGeometry {
    static func arrowRotation(bearing: Double, trueHeading: Double) -> Double? {
        guard bearing.isFinite, trueHeading.isFinite,
              (0..<360).contains(trueHeading) else { return nil }
        let difference = (bearing - trueHeading).truncatingRemainder(dividingBy: 360)
        return difference > 180 ? difference - 360 : (difference < -180 ? difference + 360 : difference)
    }
}
