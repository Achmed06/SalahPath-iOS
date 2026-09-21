from pathlib import Path
import json

assets_root = Path("SalahZeit/Assets.xcassets")
guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

names = [
    "male_intention", "male_takbir", "male_standing", "male_upright",
    "male_bowing", "male_sujud", "male_sitting", "male_final_sitting",
    "male_salam_right", "male_salam_left",
    "female_intention", "female_takbir", "female_standing", "female_upright",
    "female_bowing", "female_sujud", "female_sitting", "female_final_sitting",
    "female_salam_right", "female_salam_left",
]

INK = "#0A3F3C"
TEAL = "#0D6E69"
TEAL2 = "#2C8E88"
GOLD = "#D6AE52"
SKIN = "#D9AD85"
CREAM = "#FBF5E8"
MAT = "#DCEEEA"

def face(cx, cy, female=False, turn=0):
    tx = turn * 7
    hood = ""
    cap = ""
    if female:
        hood = f'''
  <path d="M {cx-41} {cy+9} Q {cx-39} {cy-45} {cx} {cy-49} Q {cx+39} {cy-45} {cx+41} {cy+9}
           Q {cx+31} {cy+37} {cx+23} {cy+45} L {cx-23} {cy+45} Q {cx-31} {cy+37} {cx-41} {cy+9} Z"
        fill="{TEAL2}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
  <circle cx="{cx}" cy="{cy}" r="29" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>'''
    else:
        cap = f'''
  <circle cx="{cx}" cy="{cy}" r="31" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  <path d="M {cx-23} {cy-22} Q {cx} {cy-38} {cx+23} {cy-22}" fill="none" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'''
    features = f'''
  <path d="M {cx-13+tx} {cy-7} q 6 -5 12 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  <path d="M {cx+5+tx} {cy-7} q 6 -5 12 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  <path d="M {cx+tx} {cy-1} l {3 if turn >= 0 else -3} 9" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M {cx-9+tx} {cy+15} q 9 6 18 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'''
    beard = "" if female else f'''
  <path d="M {cx-19+tx} {cy+17} Q {cx+tx} {cy+39} {cx+19+tx} {cy+17}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'''
    return hood + cap + features + beard

def mat():
    return f'''
  <rect x="28" y="344" width="304" height="48" rx="18" fill="{MAT}" stroke="{GOLD}" stroke-width="3"/>
  <path d="M 62 368 H 298" stroke="{TEAL}" stroke-opacity=".24" stroke-width="4" stroke-linecap="round"/>'''

def standing(female, mode):
    cx = 180
    head = face(cx, 72, female)
    if female:
        torso = f'''
  <path d="M 153 122 Q 180 108 207 122 L 231 326 Q 180 344 129 326 Z"
        fill="{TEAL}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 162 326 L 155 352 M 198 326 L 205 352" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'''
        sy = 137
        if mode == "takbir":
            arms = f'''
  <path d="M 151 {sy} Q 129 154 126 185" fill="none" stroke="{TEAL2}" stroke-width="18" stroke-linecap="round"/>
  <path d="M 209 {sy} Q 231 154 234 185" fill="none" stroke="{TEAL2}" stroke-width="18" stroke-linecap="round"/>
  <circle cx="126" cy="181" r="10" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <circle cx="234" cy="181" r="10" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'''
        elif mode == "bound":
            arms = f'''
  <path d="M 150 {sy} Q 148 184 176 196" fill="none" stroke="{TEAL2}" stroke-width="17" stroke-linecap="round"/>
  <path d="M 210 {sy} Q 212 184 184 196" fill="none" stroke="{TEAL2}" stroke-width="17" stroke-linecap="round"/>
  <ellipse cx="180" cy="198" rx="28" ry="11" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'''
        else:
            arms = f'''
  <path d="M 151 {sy} Q 140 210 147 287" fill="none" stroke="{TEAL2}" stroke-width="18" stroke-linecap="round"/>
  <path d="M 209 {sy} Q 220 210 213 287" fill="none" stroke="{TEAL2}" stroke-width="18" stroke-linecap="round"/>
  <circle cx="147" cy="288" r="9" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <circle cx="213" cy="288" r="9" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'''
    else:
        torso = f'''
  <path d="M 151 121 Q 180 108 209 121 L 207 264 Q 180 278 153 264 Z"
        fill="{TEAL}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 165 267 L 160 350 M 195 267 L 200 350" stroke="{INK}" stroke-width="17" stroke-linecap="round"/>
  <path d="M 148 350 H 171 M 189 350 H 212" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'''
        sy = 137
        if mode == "takbir":
            arms = f'''
  <path d="M 151 {sy} Q 128 143 129 92" fill="none" stroke="{TEAL2}" stroke-width="17" stroke-linecap="round"/>
  <path d="M 209 {sy} Q 232 143 231 92" fill="none" stroke="{TEAL2}" stroke-width="17" stroke-linecap="round"/>
  <circle cx="129" cy="93" r="10" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <circle cx="231" cy="93" r="10" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'''
        elif mode == "bound":
            arms = f'''
  <path d="M 150 {sy} Q 147 204 176 229" fill="none" stroke="{TEAL2}" stroke-width="16" stroke-linecap="round"/>
  <path d="M 210 {sy} Q 213 204 184 229" fill="none" stroke="{TEAL2}" stroke-width="16" stroke-linecap="round"/>
  <ellipse cx="180" cy="231" rx="28" ry="11" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'''
        else:
            arms = f'''
  <path d="M 151 {sy} Q 141 205 148 274" fill="none" stroke="{TEAL2}" stroke-width="17" stroke-linecap="round"/>
  <path d="M 209 {sy} Q 219 205 212 274" fill="none" stroke="{TEAL2}" stroke-width="17" stroke-linecap="round"/>
  <circle cx="148" cy="276" r="9" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <circle cx="212" cy="276" r="9" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'''
    return mat() + torso + arms + head

def bowing(female):
    if female:
        return mat() + f'''
  <path d="M 139 221 Q 173 195 222 190" fill="none" stroke="{TEAL}" stroke-width="38" stroke-linecap="round"/>
  <path d="M 140 224 L 145 350 M 168 219 L 173 350" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
  <path d="M 205 195 Q 187 231 164 252 M 218 197 Q 203 236 176 255"
        fill="none" stroke="{TEAL2}" stroke-width="16" stroke-linecap="round"/>
  <ellipse cx="164" cy="254" rx="12" ry="8" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <ellipse cx="177" cy="257" rx="12" ry="8" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <path d="M 132 214 Q 148 185 167 181 L 185 302 Q 155 322 126 303 Z" fill="{TEAL}" opacity=".92"/>
''' + face(251, 183, True)
    return mat() + f'''
  <path d="M 133 213 L 232 188" fill="none" stroke="{TEAL}" stroke-width="35" stroke-linecap="round"/>
  <path d="M 137 215 L 138 350 M 169 213 L 171 350" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
  <path d="M 210 192 L 172 249 M 224 189 L 182 251" fill="none" stroke="{TEAL2}" stroke-width="16" stroke-linecap="round"/>
  <ellipse cx="171" cy="251" rx="12" ry="8" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <ellipse cx="183" cy="253" rx="12" ry="8" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
''' + face(270, 181, False)

def sujud(female):
    if female:
        return mat() + f'''
  <path d="M 128 292 Q 160 236 205 270 Q 223 286 243 306" fill="none" stroke="{TEAL}" stroke-width="41" stroke-linecap="round"/>
  <path d="M 132 292 Q 108 316 91 329" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
  <path d="M 207 277 Q 222 315 238 328 M 221 281 Q 240 313 255 329" fill="none" stroke="{TEAL2}" stroke-width="15" stroke-linecap="round"/>
  <ellipse cx="237" cy="330" rx="13" ry="7" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <ellipse cx="255" cy="330" rx="13" ry="7" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
''' + face(282, 309, True)
    return mat() + f'''
  <path d="M 120 286 Q 151 211 210 261 Q 232 284 248 307" fill="none" stroke="{TEAL}" stroke-width="36" stroke-linecap="round"/>
  <path d="M 123 287 Q 94 312 77 330" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
  <path d="M 203 267 Q 217 306 230 329 M 220 269 Q 241 307 255 329" fill="none" stroke="{TEAL2}" stroke-width="15" stroke-linecap="round"/>
  <ellipse cx="230" cy="330" rx="13" ry="7" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <ellipse cx="255" cy="330" rx="13" ry="7" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
''' + face(285, 309, False)

def sitting(female, turn=0):
    head = face(180, 101, female, turn)
    if female:
        return mat() + f'''
  <path d="M 151 153 Q 180 139 209 153 L 214 273 Q 180 289 146 273 Z"
        fill="{TEAL}" stroke="{INK}" stroke-width="5"/>
  <path d="M 151 178 Q 147 231 162 247 M 209 178 Q 213 231 198 247" fill="none" stroke="{TEAL2}" stroke-width="16" stroke-linecap="round"/>
  <ellipse cx="163" cy="249" rx="16" ry="8" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <ellipse cx="197" cy="249" rx="16" ry="8" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <path d="M 165 279 Q 210 307 259 329 M 187 280 Q 224 323 276 336" fill="none" stroke="{TEAL}" stroke-width="19" stroke-linecap="round"/>
  <path d="M 251 333 H 291" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>
''' + head
    return mat() + f'''
  <path d="M 153 151 Q 180 139 207 151 L 205 273 Q 180 286 155 273 Z"
        fill="{TEAL}" stroke="{INK}" stroke-width="5"/>
  <path d="M 151 177 L 160 247 M 209 177 L 200 247" stroke="{TEAL2}" stroke-width="16" stroke-linecap="round"/>
  <ellipse cx="160" cy="249" rx="17" ry="8" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <ellipse cx="200" cy="249" rx="17" ry="8" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>
  <path d="M 165 278 Q 139 309 103 334 M 190 278 Q 218 311 255 334" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>
  <path d="M 92 336 H 124 M 244 336 H 278" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
''' + head

def make_svg(name):
    female = name.startswith("female_")
    pose = name.split("_", 1)[1]
    if pose in ("intention", "upright"):
        art = standing(female, "relaxed")
    elif pose == "takbir":
        art = standing(female, "takbir")
    elif pose == "standing":
        art = standing(female, "bound")
    elif pose == "bowing":
        art = bowing(female)
    elif pose == "sujud":
        art = sujud(female)
    elif pose in ("sitting", "final_sitting"):
        art = sitting(female, 0)
    elif pose == "salam_right":
        art = sitting(female, 1)
    elif pose == "salam_left":
        art = sitting(female, -1)
    else:
        raise RuntimeError(f"Unknown prayer pose: {pose}")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="420" viewBox="0 0 360 420">
  <rect width="360" height="420" rx="30" fill="{CREAM}"/>
  <rect x="7" y="7" width="346" height="406" rx="25" fill="none" stroke="{TEAL}" stroke-opacity=".16" stroke-width="3"/>
  {art}
</svg>
'''

for name in names:
    imageset = assets_root / f"{name}.imageset"
    imageset.mkdir(parents=True, exist_ok=True)
    svg_name = f"{name}.svg"
    (imageset / svg_name).write_text(make_svg(name), encoding="utf-8")
    contents = {
        "images": [{"filename": svg_name, "idiom": "universal"}],
        "info": {"author": "xcode", "version": 1},
        "properties": {"preserves-vector-representation": True},
    }
    (imageset / "Contents.json").write_text(
        json.dumps(contents, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

old = '''    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .fill(SalahTheme.softTeal.opacity(0.38))

            VStack {
                Spacer()
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(SalahTheme.teal.opacity(0.14))
                    .overlay {
                        RoundedRectangle(cornerRadius: 12, style: .continuous)
                            .stroke(SalahTheme.gold.opacity(0.34), lineWidth: 1)
                    }
                    .frame(height: 38)
                    .padding(.horizontal, 18)
                    .padding(.bottom, 10)
            }

            Canvas { context, size in
                drawPose(context: &context, size: size)
            }
            .padding(8)
        }
        .accessibilityHidden(true)
    }
'''
new = '''    var body: some View {
        Image(assetName)
            .resizable()
            .scaledToFit()
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .accessibilityHidden(true)
    }
'''
if old not in text:
    raise SystemExit("v434: PrayerPoseArtwork Canvas body anchor missing")

guide.write_text(text.replace(old, new, 1), encoding="utf-8")
print("v434 applied: dedicated male/female vector prayer-pose assets")
