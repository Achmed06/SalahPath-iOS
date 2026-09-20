from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

old = '''            ForEach(Array(lines.enumerated()), id: \\.offset) { index, line in
                HStack(alignment: .top, spacing: 10) {
                    Text("\\(index + 1)")
                        .font(.caption.bold())
                        .foregroundStyle(.white)
                        .frame(width: 24, height: 24)
                        .background(SalahTheme.teal, in: Circle())
                    Text(line)
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                    Spacer(minLength: 0)
                }
            }
'''
new = '''            ForEach(lines.indices, id: \\.self) { index in
                HStack(alignment: .top, spacing: 10) {
                    Text("\\(index + 1)")
                        .font(.caption.bold())
                        .foregroundStyle(.white)
                        .frame(width: 24, height: 24)
                        .background(SalahTheme.teal, in: Circle())
                    Text(lines[index])
                        .font(.subheadline)
                        .foregroundStyle(SalahTheme.ink)
                        .fixedSize(horizontal: false, vertical: true)
                    Spacer(minLength: 0)
                }
            }
'''
if old not in text:
    raise SystemExit("v399: Rak'a plan ForEach anchor missing")
guide.write_text(text.replace(old, new, 1), encoding="utf-8")
print("v399 applied: stable indexed ForEach for Rak'a plan cards")
