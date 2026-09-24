#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

CASES = [
    ("male_intention", Path("SalahZeit/Assets.xcassets/male_intention.imageset/male_intention.png"), [280,300,320,340,360,380,400], range(330,366,2)),
    ("male_takbir", Path("SalahZeit/Assets.xcassets/male_takbir.imageset/male_takbir.png"), [280,300,320,340,360,380,400], range(340,382,2)),
    ("female_intention", Path("SalahZeit/Assets.xcassets/female_intention.imageset/female_intention.png"), [280,300,320,340,360,380,400], range(330,366,2)),
    ("female_takbir", Path("SalahZeit/Assets.xcassets/female_takbir.imageset/female_takbir.png"), [280,300,320,340,360,380,400], range(340,386,2)),
]

for name,path,rows,xs in CASES:
    im=Image.open(path).convert("RGBA")
    px=im.load()
    print("\nFILE",name)
    for y in rows:
        vals=[]
        for x in xs:
            r,g,b,a=px[x,y]
            if a:
                vals.append((x,(r,g,b,a)))
        print("ROW",y,vals)
