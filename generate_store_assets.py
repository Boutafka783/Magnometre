#!/usr/bin/env python3
"""Generate temporary Play Store icon and feature graphic. Requires Pillow."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
OUT=Path("store-assets"); OUT.mkdir(exist_ok=True)
# Temporary icon; replace with the approved brand artwork before publishing.
im=Image.new("RGB",(512,512),(15,28,48)); d=ImageDraw.Draw(im)
d.rounded_rectangle((55,55,457,457),radius=90,outline=(60,210,190),width=18)
d.line((125,340,205,170,280,300,375,125),fill=(245,190,75),width=25)
d.ellipse((185,150,225,190),fill=(245,190,75)); d.ellipse((355,105,395,145),fill=(60,210,190))
im.save(OUT/"icon-512.png")
fg=Image.new("RGB",(1024,500),(15,28,48)); fd=ImageDraw.Draw(fg)
fd.rounded_rectangle((50,50,974,450),radius=40,outline=(60,210,190),width=8)
try: font=ImageFont.truetype("DejaVuSans-Bold.ttf",68)
except OSError: font=ImageFont.load_default()
fd.text((110,185),"GRADIOMETER",font=font,fill=(255,255,255))
fd.text((115,285),"Magnetic field mapping",font=ImageFont.load_default(),fill=(60,210,190))
fg.save(OUT/"feature-graphic-1024x500.png")
print("Generated temporary assets in",OUT)
