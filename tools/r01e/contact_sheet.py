from PIL import Image, ImageDraw, ImageOps
from pathlib import Path
R=Path(__file__).resolve().parents[2];d=R/'docs/r01e/evidence'
items=[('Blender / three-quarter','blender-three-quarter.png'),('Blender / rear','blender-rear.png'),('Blender / side','blender-side.png'),('Blender / top / support','blender-top.png'),('Blender / close-up','blender-closeup.png'),('Three.js / actual WebGL','webgl-three-quarter.png')]
w,h=1600,1420;sheet=Image.new('RGB',(w,h),'#202d38');draw=ImageDraw.Draw(sheet)
draw.text((24,16),'LITTLE NORTH / R01e - ACTUAL MESH RENDERS - ART REJECT / review candidate',fill='#eff4f5',font_size=25)
for i,(label,file) in enumerate(items):
 x=16+(i%3)*528;y=66+(i//3)*670
 draw.text((x,y),label,fill='#dce6ec',font_size=21)
 im=Image.open(d/file).convert('RGB');im=ImageOps.contain(im,(512,620));sheet.paste(im,(x+(512-im.width)//2,y+32))
sheet.save(d/'review-contact-sheet.jpg',quality=92)
