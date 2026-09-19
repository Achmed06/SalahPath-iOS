from pathlib import Path

# SalahPath v3.37 — screenshot-driven Home polish from the successful v3.36 capture.
p = Path("SalahZeit/Views/HomeView.swift")
s = p.read_text(encoding="utf-8")

# Mosque: v3.36 is finally visible, but it overlaps the prayer sequence and quote.
# Move it upward/right and slightly shrink it so it sits behind the prayer info like the reference.
s = s.replace(
'''            ReferenceMosqueSkyline()
                .frame(width: 196, height: 122)
                .opacity(0.96)
                .offset(x: 9, y: -2)
                .accessibilityHidden(true)
''',
'''            ReferenceMosqueSkyline()
                .frame(width: 171, height: 104)
                .opacity(0.90)
                .offset(x: 7, y: -48)
                .accessibilityHidden(true)
''', 1)

# Tighten hero content vertically. The v3.36 screenshot had too much empty cream below the quote.
s = s.replace('.frame(minHeight: 200)', '.frame(minHeight: 184)', 1)
s = s.replace('.padding(.vertical, 7)', '.padding(.vertical, 6)', 1)

# Headline and date are slightly too heavy compared with the supplied poster.
s = s.replace('.font(.custom("AvenirNext-Bold", size: 11.1))',
              '.font(.custom("AvenirNext-DemiBold", size: 10.7))', 1)
s = s.replace('.font(.system(size: 8.4, weight: .bold))',
              '.font(.custom("AvenirNext-DemiBold", size: 7.8))', 1)
s = s.replace('.font(.system(size: 7.4, weight: .semibold))',
              '.font(.custom("AvenirNext-Medium", size: 7.0))', 1)

# Sequence strip is flatter in the reference.
s = s.replace('.padding(.vertical, 5)', '.padding(.vertical, 4)', 1)

# Dua card: reference title and Arabic are more delicate.
s = s.replace('.font(.custom("AvenirNext-Bold", size: 10.2))',
              '.font(.custom("AvenirNext-DemiBold", size: 9.7))', 1)
s = s.replace('.font(.system(size: 19.5, weight: .medium))',
              '.font(.system(size: 18.2, weight: .regular))', 1)

# Tracking card in the poster is flatter than v3.36.
s = s.replace('.frame(minHeight: 112)', '.frame(minHeight: 103)', 1)
s = s.replace('.frame(width: 0.7, height: 72)', '.frame(width: 0.7, height: 63)', 1)

# Dashboard: reduce oversized text/white-space and make cards a little squarer/denser.
start = s.index("private struct DashboardTile: View {")
end = s.index("\nprivate struct ReferenceDashboardGlyph", start)
tile = s[start:end]
tile = tile.replace('.frame(width: 31, height: 31)', '.frame(width: 29, height: 29)')
tile = tile.replace('.font(.custom("AvenirNext-Bold", size: 7.9))',
                    '.font(.custom("AvenirNext-DemiBold", size: 7.5))')
tile = tile.replace('.font(.custom("AvenirNext-DemiBold", size: 6.0))',
                    '.font(.custom("AvenirNext-Medium", size: 5.8))')
tile = tile.replace('.frame(maxWidth: .infinity, minHeight: 87, alignment: .center)',
                    '.frame(maxWidth: .infinity, minHeight: 82, alignment: .center)')
tile = tile.replace('.padding(.vertical, 5)', '.padding(.vertical, 4)')
s = s[:start] + tile + s[end:]

# Quote ribbon: lighter and flatter.
quote_start = s.index("    private var referenceQuoteStrip: some View {")
quote_end = s.index("\n    private func referenceSequence", quote_start)
quote = s[quote_start:quote_end]
quote = quote.replace('.frame(minHeight: 52)', '.frame(minHeight: 44)')
quote = quote.replace('.font(.custom("Georgia-Italic", size: 9.1))',
                      '.font(.custom("Georgia-Italic", size: 8.4))')
quote = quote.replace('.font(.system(size: 7.6, weight: .medium))',
                      '.font(.custom("AvenirNext-Medium", size: 6.9))')
s = s[:quote_start] + quote + s[quote_end:]

p.write_text(s, encoding="utf-8")

# Bottom navigation: reference bar is noticeably shorter than current v3.36.
root = Path("SalahZeit/Views/RootTabView.swift")
r = root.read_text(encoding="utf-8")
r = r.replace('.frame(width: 27, height: 27)', '.frame(width: 24, height: 24)', 1)
r = r.replace('.font(.system(size: 15, weight: selection == index ? .bold : .medium))',
              '.font(.system(size: 13.5, weight: selection == index ? .semibold : .regular))', 1)
r = r.replace('.font(.custom(selection == index ? "AvenirNext-Bold" : "AvenirNext-Medium", size: 7.2))',
              '.font(.custom(selection == index ? "AvenirNext-DemiBold" : "AvenirNext-Medium", size: 6.6))', 1)
r = r.replace('.frame(height: 20)', '.frame(height: 18)', 1)
r = r.replace('.padding(.top, 3)', '.padding(.top, 2)', 1)
r = r.replace('.padding(.bottom, 1)', '.padding(.bottom, 0)', 1)
root.write_text(r, encoding="utf-8")

b = Path("scripts/build_unsigned_ipa.sh")
t = b.read_text(encoding="utf-8")
t = t.replace('MARKETING_VERSION="3.36"', 'MARKETING_VERSION="3.37"')
t = t.replace('CURRENT_PROJECT_VERSION="41"', 'CURRENT_PROJECT_VERSION="42"')
b.write_text(t, encoding="utf-8")

print("SalahPath v3.37 screenshot-driven Home polish applied")
