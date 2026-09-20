from pathlib import Path

root = Path.cwd()
guide = root / "SalahZeit" / "Views" / "GuideView.swift"
s = guide.read_text(encoding="utf-8")

start = s.find("private struct ReferencePrayerPerson: View {")
if start < 0:
    raise SystemExit("v3.71: ReferencePrayerPerson start missing")
end = s.find("\n}\n\n", start)
if end < 0:
    raise SystemExit("v3.71: ReferencePrayerPerson end missing")
end += 3

old = s[start:end]
new = r'''private struct ReferencePrayerPerson: View {
    let imageName: String
    let rugWidth: CGFloat
    let rugRotation: Double

    var body: some View {
        PrayerPoseArtwork(assetName: imageName)
            .frame(maxWidth: .infinity, minHeight: 286, maxHeight: 286)
            .padding(.horizontal, 4)
    }
}
'''
s = s[:start] + new + s[end:]

guide.write_text(s, encoding="utf-8")
print("SalahPath v3.71 removed duplicate legacy rug layer from prayer hero")
