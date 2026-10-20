from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]/'artifacts/fox-r01a'
canvas=Image.new('RGB',(1560,1160),'#202a31');d=ImageDraw.Draw(canvas)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(font,22);title=ImageFont.truetype(font,32);small=ImageFont.truetype(font,17)
d.text((34,24),'LITTLE NORTH  /  HERO ARCTIC FOX',font=title,fill='#f0eee5')
d.text((34,68),'LN-FOX-R01a  |  Neutral form study  |  Actual Blender Cycles mesh renders',font=small,fill='#afc1cb')
for i,(name,label) in enumerate([('front','FRONT'),('side','SIDE'),('rear','REAR'),('three-quarter','THREE-QUARTER'),('gameplay','GAMEPLAY DISTANCE / STUDIO')]):
 x=30+(i%3)*510;y=115+(i//3)*510
 im=Image.open(root/(name+'.png')).convert('RGB');im.thumbnail((490,455));canvas.paste(im,(x+(490-im.width)//2,y))
 d.text((x,y+461),label,font=f,fill='#e0e6e8')
x=1050;y=660
for line in ['NEUTRAL FORM GATE','Grey clay, separable eyes and nose','No fur or premium material pass','Non-rigged sculpt foundation','Studio framing; no in-game capture','Art verdict: see REVIEW.md']:
 d.text((x,y),line,font=small,fill='#c1cdd3');y+=38
d.text((32,1120),'Editable .blend + test GLB  |  Source and review preserved on isolated art branch',font=small,fill='#9caeb9')
canvas.save(root/'neutral-review-sheet.png')
