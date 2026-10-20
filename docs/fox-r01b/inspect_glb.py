"""R01b GLB container, axis and non-rigged study checks; no runtime certification."""
import struct,json,sys,math
from pathlib import Path
raw=Path(sys.argv[1]).read_bytes();magic,version,size=struct.unpack_from('<4sII',raw);assert magic==b'glTF' and version==2 and size==len(raw)
n,kind=struct.unpack_from('<II',raw,12);assert kind==0x4E4F534A;d=json.loads(raw[20:20+n])
assert not d.get('skins') and not d.get('animations')
root=next(n for n in d['nodes'] if n.get('name')=='FOX export root meters ground origin R01b');q=root.get('rotation',[0,0,0,1]);assert abs(abs(q[1])-1)<1e-5 and abs(q[3])<1e-5
nose=next(n for n in d['nodes'] if n.get('name')=='Rounded triangular nose');p=d['meshes'][nose['mesh']]['primitives'][0];a=d['accessors'][p['attributes']['POSITION']];assert a['min'][2]>.5
tri=0;vert=0
for m in d['meshes']:
 for p in m['primitives']:
  a=d['accessors'][p['attributes']['POSITION']];assert all(math.isfinite(x) for x in a['min']+a['max']);vert+=a['count'];tri+=d['accessors'][p['indices']]['count']//3
print(json.dumps({'container':'GLB 2.0','bytes':len(raw),'meshes':len(d['meshes']),'materials':len(d['materials']),'exported_vertices':vert,'exported_triangles':tri,'up':'+Y','forward':'-Z, root rotation and nose position verified','skins':0,'animations':0,'limitations':'No runtime/device or full Khronos validation'},indent=2))
