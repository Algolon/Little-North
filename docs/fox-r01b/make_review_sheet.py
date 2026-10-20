"""Compose a review sheet from actual PNG renders; does not synthesize 3D evidence.
Usage: python make_review_sheet.py OLD_DIR NEW_DIR OUTPUT.jpg
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import sys
old,new,out=map(Path,sys.argv[1:4]);im=Image.new('RGB',(1560,1180),'#202a31');d=ImageDraw.Draw(im)
fp='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';font=ImageFont.truetype(fp,20);title=ImageFont.truetype(fp,30);small=ImageFont.truetype(fp,16)
d.text((30,25),'LITTLE NORTH  /  LN-FOX-R01b',font=title,fill='#f1eee5')
d.text((30,68),'Actual Blender Cycles renders | Neutral head, chest and gaze study',font=small,fill='#b4c5ce')
def panel(path,x,y,w,h,label):
 pic=Image.open(path).convert('RGB');pic.thumbnail((w,h));im.paste(pic,(x+(w-pic.width)//2,y+(h-pic.height)//2));d.text((x,y+h+8),label,font=font,fill='#e4e8ea')
for i,(name,label) in enumerate([('head-front','HEAD / FRONT'),('head-three-quarter','HEAD / THREE-QUARTER'),('head-side','HEAD / SIDE')]):panel(new/(name+'.png'),30+i*510,110,490,490,label)
panel(old/'three-quarter.png',30,665,490,435,'R01a / PREVIOUS FORM STUDY')
panel(new/'three-quarter.png',540,665,490,435,'R01b / CURRENT FORM STUDY')
y=710
for line in ['NEUTRAL FORM REVIEW','Eyes / muzzle / ear bowls','Continuous chest surface','No premium coat pass','Overall ART REJECT','See REVIEW.md for findings']:
 d.text((1060,y),line,font=small,fill='#c4d0d7');y+=42
d.text((30,1150),'Studio views; comparison is illustrative, not a pixel-matched camera test. No gameplay integration.',font=small,fill='#a8bac4')
im.save(out,quality=89,optimize=True)
