"""Compose actual whole-character Blender PNGs; no synthetic visual evidence."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import sys
root,out=map(Path,sys.argv[1:3]);sheet=Image.new('RGB',(1560,1160),'#202a31');d=ImageDraw.Draw(sheet)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,30);f=ImageFont.truetype(font,20);small=ImageFont.truetype(font,16)
d.text((30,24),'LITTLE NORTH / LN-FOX-R01c',font=title,fill='#f2eee5')
d.text((30,67),'New complete fox sculpt | Actual neutral Blender Cycles renders | See REVIEW.md for art verdict',font=small,fill='#bccbd3')
views=[('three-quarter','WHOLE CHARACTER / THREE-QUARTER'),('side','SIDE'),('front','FRONT'),('rear','REAR'),('head-three-quarter','HEAD / THREE-QUARTER'),('distance','DISTANCE / STUDIO')]
for i,(name,label) in enumerate(views):
 x=30+(i%3)*510;y=110+(i//3)*505
 im=Image.open(root/(name+'.png')).convert('RGB');im.thumbnail((490,450));sheet.paste(im,(x+(490-im.width)//2,y+(450-im.height)//2))
 d.text((x,y+459),label,font=f,fill='#e1e7eb')
d.text((30,1128),'Editable complete .blend + test GLB | Non-rigged study | No gameplay integration',font=small,fill='#a6b8c2')
sheet.save(out,quality=90,optimize=True)
