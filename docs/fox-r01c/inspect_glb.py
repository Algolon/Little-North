"""Independent GLB container, bounds, orientation and non-rigged study check."""
import struct,json,sys,math
from pathlib import Path
raw=Path(sys.argv[1]).read_bytes();magic,ver,total=struct.unpack_from('<4sII',raw);assert magic==b'glTF' and ver==2 and total==len(raw)
n,kind=struct.unpack_from('<II',raw,12);assert kind==0x4E4F534A;d=json.loads(raw[20:20+n]);assert not d.get('skins') and not d.get('animations')
root=next(n for n in d['nodes'] if n.get('name')=='FOX ground-origin export root -Z forward');q=root.get('rotation',[0,0,0,1]);assert abs(abs(q[1])-1)<1e-5 and abs(q[3])<1e-5
nose=next(n for n in d['nodes'] if n.get('name')=='Nose marker');assert nose['translation'][2]>.5
tri=0;vert=0;bounds={}
for m in d['meshes']:
 for p in m['primitives']:
  a=d['accessors'][p['attributes']['POSITION']];assert all(math.isfinite(x) for x in a['min']+a['max']);vert+=a['count'];tri+=d['accessors'][p['indices']]['count']//3
  bounds[m.get('name','mesh')]={'min':a['min'],'max':a['max']}
print(json.dumps({'container':'GLB 2.0','bytes':len(raw),'meshes':len(d['meshes']),'materials':len(d['materials']),'triangles':tri,'vertices':vert,'up':'+Y','forward':'-Z; root and nose verified','rigged':False,'animated':False,'mesh_local_bounds':bounds,'limitations':'Sculpt study only; no runtime/mobile or production topology certification'},indent=2))
