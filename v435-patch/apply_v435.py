from pathlib import Path
import json

assets_root = Path("SalahZeit/Assets.xcassets")
guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

INK = "#0A3F3C"
TEAL = "#0D6E69"
TEAL2 = "#2C8E88"
GOLD = "#D6AE52"
SKIN = "#D9AD85"
CREAM = "#FBF5E8"
WATER = "#5BAECA"

def drops(points):
    parts = []
    for x, y, s in points:
        parts.append(
            f'<path d="M {x} {y-s} C {x-s*.75} {y-s*.1}, {x-s*.7} {y+s*.7}, {x} {y+s} '
            f'C {x+s*.7} {y+s*.7}, {x+s*.75} {y-s*.1}, {x} {y-s} Z" fill="{WATER}" stroke="{INK}" stroke-width="2"/>'
        )
    return "\n".join(parts)

def face_base(back=False):
    if back:
        return f'''
  <circle cx="180" cy="145" r="69" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
  <path d="M 125 127 Q 180 72 235 127" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>
  <rect x="158" y="204" width="44" height="58" rx="18" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
'''
    return f'''
  <circle cx="180" cy="145" r="69" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
  <path d="M 128 105 Q 180 69 232 105" fill="none" stroke="{TEAL}" stroke-width="11" stroke-linecap="round"/>
  <path d="M 149 134 q 10 -8 20 0 M 191 134 q 10 -8 20 0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
  <path d="M 180 143 l 3 18" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  <path d="M 164 179 q 16 10 32 0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
'''

def hand(cx, cy, flip=False):
    sx = -1 if flip else 1
    # Stylised open hand with five fingers and wrist.
    return f'''
  <g transform="translate({cx} {cy}) scale({sx} 1)">
    <path d="M -25 56 L -27 4 Q -27 -7 -18 -7 Q -10 -7 -10 3 L -9 -35 Q -9 -46 0 -46 Q 9 -46 9 -35
             L 10 -4 L 16 -39 Q 18 -49 27 -47 Q 35 -45 33 -35 L 28 1 L 36 -29 Q 39 -39 47 -36
             Q 55 -33 52 -23 L 43 10 L 50 -11 Q 54 -20 62 -16 Q 69 -12 65 -4 L 48 42
             Q 42 58 25 69 L -4 77 Q -19 73 -25 56 Z"
          fill="{SKIN}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
  </g>
'''

def foot(cx, cy, flip=False):
    sx = -1 if flip else 1
    return f'''
  <g transform="translate({cx} {cy}) scale({sx} 1)">
    <path d="M -22 -87 Q 8 -103 30 -78 Q 47 -55 38 -16 Q 34 5 53 27 Q 72 49 55 70
             Q 40 88 5 73 Q -19 62 -28 26 Q -38 -10 -31 -45 Z"
          fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
    <circle cx="48" cy="39" r="7" fill="{SKIN}" stroke="{INK}" stroke-width="2"/>
    <circle cx="54" cy="25" r="6.5" fill="{SKIN}" stroke="{INK}" stroke-width="2"/>
    <circle cx="54" cy="11" r="6" fill="{SKIN}" stroke="{INK}" stroke-width="2"/>
    <circle cx="50" cy="-2" r="5.5" fill="{SKIN}" stroke="{INK}" stroke-width="2"/>
    <circle cx="44" cy="-14" r="5" fill="{SKIN}" stroke="{INK}" stroke-width="2"/>
  </g>
'''

def wrap(inner):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="300" viewBox="0 0 520 300">
  <rect width="520" height="300" rx="28" fill="{CREAM}"/>
  <rect x="7" y="7" width="506" height="286" rx="22" fill="none" stroke="{TEAL}" stroke-opacity=".16" stroke-width="3"/>
  {inner}
</svg>
'''

def svg_for(name):
    if name == "wudu_intention":
        inner = f'''
  <path d="M 182 247 Q 260 186 338 247" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>
  <circle cx="260" cy="107" r="61" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
  <path d="M 215 78 Q 260 43 305 78" fill="none" stroke="{TEAL}" stroke-width="10" stroke-linecap="round"/>
  <path d="M 238 101 q 9 -7 18 0 M 270 101 q 9 -7 18 0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
  <path d="M 249 130 Q 260 142 271 130" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
  <path d="M 260 196 C 226 163 195 207 260 254 C 325 207 294 163 260 196 Z" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>
''' + drops([(376, 87, 23)])
    elif name == "wudu_basmala":
        inner = face_base(False) + f'''
  <path d="M 260 91 Q 351 60 421 96 L 402 151 Q 336 130 267 149 Z" fill="white" stroke="{GOLD}" stroke-width="4"/>
  <path d="M 291 111 H 389 M 305 128 H 375" stroke="{TEAL}" stroke-width="5" stroke-linecap="round"/>
''' + drops([(424, 205, 22)])
    elif name == "wudu_hands":
        inner = hand(185, 151, False) + hand(335, 151, True) + drops([(225, 49, 15), (260, 37, 20), (295, 49, 15)])
    elif name in ("wudu_mouth", "wudu_nose", "wudu_face"):
        inner = face_base(False)
        if name == "wudu_mouth":
            inner += f'<ellipse cx="180" cy="179" rx="31" ry="17" fill="{GOLD}" fill-opacity=".35" stroke="{GOLD}" stroke-width="5"/>'
            inner += drops([(293, 153, 13), (323, 173, 17)])
        elif name == "wudu_nose":
            inner += f'<ellipse cx="182" cy="153" rx="22" ry="29" fill="{GOLD}" fill-opacity=".32" stroke="{GOLD}" stroke-width="5"/>'
            inner += drops([(294, 128, 13), (326, 146, 17)])
        else:
            inner += f'<ellipse cx="180" cy="149" rx="78" ry="83" fill="{GOLD}" fill-opacity=".12" stroke="{GOLD}" stroke-width="5"/>'
            inner += drops([(297, 93, 12), (330, 124, 17), (305, 172, 13)])
    elif name in ("wudu_rightarm", "wudu_leftarm"):
        mirror = name.endswith("leftarm")
        inner = f'''
  <g transform="translate(260 150) scale({-1 if mirror else 1} 1)">
    <path d="M -151 22 Q -110 -10 -54 -6 L 91 -27 Q 125 -31 143 -4 Q 151 19 128 35 L -55 57 Q -116 65 -151 22 Z"
          fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
    <circle cx="-60" cy="23" r="25" fill="{GOLD}" fill-opacity=".28" stroke="{GOLD}" stroke-width="5"/>
    <path d="M 104 -21 Q 139 -51 165 -17 Q 178 5 153 27" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
  </g>
''' + drops([(214 if not mirror else 306, 62, 14), (260, 45, 19), (306 if not mirror else 214, 62, 14)])
    elif name == "wudu_head":
        inner = face_base(False) + f'''
  <path d="M 117 103 Q 180 44 243 103" fill="{GOLD}" fill-opacity=".27" stroke="{GOLD}" stroke-width="6"/>
''' + hand(346, 119, True) + drops([(369, 45, 14)])
    elif name == "wudu_ears":
        inner = face_base(False) + f'''
  <ellipse cx="111" cy="150" rx="18" ry="30" fill="{GOLD}" fill-opacity=".32" stroke="{GOLD}" stroke-width="5"/>
  <ellipse cx="249" cy="150" rx="18" ry="30" fill="{GOLD}" fill-opacity=".32" stroke="{GOLD}" stroke-width="5"/>
''' + drops([(318, 101, 14), (346, 122, 12)])
    elif name == "wudu_neck":
        inner = face_base(True) + f'''
  <path d="M 158 228 Q 180 247 202 228" fill="none" stroke="{GOLD}" stroke-width="13" stroke-linecap="round"/>
''' + hand(117, 214, False) + hand(243, 214, True) + f'''
  <path d="M 100 251 Q 180 270 260 251" fill="none" stroke="{TEAL}" stroke-width="4" stroke-dasharray="8 8"/>
'''
    elif name == "wudu_rightfoot":
        inner = foot(260, 157, False) + f'''
  <circle cx="246" cy="85" r="23" fill="{GOLD}" fill-opacity=".25" stroke="{GOLD}" stroke-width="5"/>
''' + drops([(154, 61, 13), (185, 45, 18), (216, 61, 13)])
    elif name == "wudu_leftfoot":
        inner = foot(260, 157, True) + f'''
  <circle cx="274" cy="85" r="23" fill="{GOLD}" fill-opacity=".25" stroke="{GOLD}" stroke-width="5"/>
''' + drops([(304, 61, 13), (335, 45, 18), (366, 61, 13)])
    else:
        raise RuntimeError(name)
    return wrap(inner)

asset_names = [
    "wudu_intention", "wudu_basmala", "wudu_hands", "wudu_mouth", "wudu_nose",
    "wudu_face", "wudu_rightarm", "wudu_leftarm", "wudu_head", "wudu_ears",
    "wudu_neck", "wudu_rightfoot", "wudu_leftfoot",
]

for name in asset_names:
    imageset = assets_root / f"{name}.imageset"
    imageset.mkdir(parents=True, exist_ok=True)
    svg_name = f"{name}.svg"
    (imageset / svg_name).write_text(svg_for(name), encoding="utf-8")
    contents = {
        "images": [{"filename": svg_name, "idiom": "universal"}],
        "info": {"author": "xcode", "version": 1},
        "properties": {"preserves-vector-representation": True},
    }
    (imageset / "Contents.json").write_text(
        json.dumps(contents, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

struct_pos = text.index("private struct WuduInstructionVisual: View {")
body_start = text.index("    var body: some View {", struct_pos)
body_end = text.index("    private var intentionVisual: some View {", body_start)

new_body = '''    private var assetName: String {
        if key == "wudu_intention" {
            return stepNumber == 1 ? "wudu_intention" : "wudu_basmala"
        }
        return key
    }

    var body: some View {
        Image(assetName)
            .resizable()
            .scaledToFit()
            .frame(maxWidth: .infinity)
            .frame(height: 214)
            .accessibilityHidden(true)
    }

'''

text = text[:body_start] + new_body + text[body_end:]
guide.write_text(text, encoding="utf-8")
print("v435 applied: 13 dedicated Wudu/Abdest vector instruction assets")
