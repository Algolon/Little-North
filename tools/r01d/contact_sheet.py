"""Create labeled contact sheets from actual evidence; do not pass off diagnostic renderers as Blender."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
directory=ROOT/'docs/r01d/evidence'
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
except OSError:font=ImageFont.load_default()
for prefix in ('blender','webgl'):
 names=['three-quarter','top','side','closeup']
 paths=[directory/f'{prefix}-{n}.png' for n in names]
 if not all(p.exists() for p in paths):continue
 sheet=Image.new('RGB',(1600,1160),'#263441')
 draw=ImageDraw.Draw(sheet)
 draw.text((22,8),'LN-R01d '+prefix.upper()+' ACTUAL MESH RENDERS | ART REJECT',fill='white',font=font)
 for i,(name,path) in enumerate(zip(names,paths)):
  x=16+(i%2)*800;y=58+(i//2)*546
  img=Image.open(path).convert('RGB');img.thumbnail((778,506))
  sheet.paste(img,(x,y+26));draw.text((x+5,y),name,fill='white',font=font)
 sheet.save(directory/f'{prefix}-contact-sheet.jpg',quality=86)
