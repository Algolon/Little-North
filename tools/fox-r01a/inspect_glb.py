"""Inspect the test GLB container, geometry counts, units and facing markers.
Usage: python inspect_glb.py path/to/fox-clay-test.glb
No external dependencies. Complements Blender roundtrip, not Khronos certification.
"""
import json,struct,sys,math
from pathlib import Path
raw=Path(sys.argv[1]).read_bytes()
magic,version,total=struct.unpack_from('<4sII',raw)
assert magic==b'glTF' and version==2 and total==len(raw),'Invalid GLB header'
n,kind=struct.unpack_from('<II',raw,12)
assert kind==0x4E4F534A,'First chunk must be JSON'
doc=json.loads(raw[20:20+n]);nodes=doc['nodes']
assert not doc.get('skins') and not doc.get('animations'),'Unexpected rig or animation'
assert len(doc['meshes'])==4,'Expected fused body, two eyes and nose'
triangles=0;vertices=0
for mesh in doc['meshes']:
 for p in mesh['primitives']:
  assert p.get('mode',4)==4,'Expected triangular export'
  a=doc['accessors'][p['attributes']['POSITION']]
  assert all(math.isfinite(v) for v in a['min']+a['max'])
  vertices+=a['count'];triangles+=doc['accessors'][p['indices']]['count']//3
nose=next(n for n in nodes if n.get('name')=='Nose')
root=next((n for n in nodes if n.get('name')=='FOX export root meters ground origin'),None)
# glTF translation is child-local; parent Y-axis half-turn reverses nose +Z.
assert root is not None,'Missing ground-origin conversion root'
q=root.get('rotation',[0,0,0,1]);assert abs(abs(q[1])-1)<1e-5 and abs(q[3])<1e-5,'Expected half-turn around glTF Y'
assert nose['translation'][2]>0,'Unexpected modeling-forward marker'
print(json.dumps({'container':'GLB 2.0','bytes':len(raw),'meshes':len(doc['meshes']),'materials':len(doc['materials']),'exported_vertices':vertices,'exported_triangles':triangles,'forward':'-Z after root rotation','up':'+Y','rigged':False,'animated':False,'limitations':'No runtime integration or full Khronos validator claimed'},indent=2))
