#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

PATHS = [
    Path("SalahZeit/Assets.xcassets/male_intention.imageset/male_intention.png"),
    Path("SalahZeit/Assets.xcassets/male_takbir.imageset/male_takbir.png"),
    Path("SalahZeit/Assets.xcassets/female_intention.imageset/female_intention.png"),
    Path("SalahZeit/Assets.xcassets/female_takbir.imageset/female_takbir.png"),
]

for path in PATHS:
    im=Image.open(path).convert("RGBA")
    a=im.getchannel("A")
    px=a.load()
    w,h=im.size
    print("\nFILE", path, w, h)
    for y in range(180, 501, 20):
        ints=[]
        x=0
        while x<w:
            while x<w and px[x,y] < 8:
                x+=1
            if x>=w: break
            s=x
            while x<w and px[x,y] >= 8:
                x+=1
            ints.append((s,x-1))
        print("ROW",y,ints)
