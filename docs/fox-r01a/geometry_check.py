"""Check indexed GLB triangle geometry for degenerate faces and body connectivity."""
import struct,json,sys,math
from pathlib import Path
raw=Path(sys.argv[1]).read_bytes();n,kind=struct.unpack_from('<II',raw,12);d=json.loads(raw[20:20+n]);off=20+n
blen,bkind=struct.unpack_from('<II',raw,off);buf=raw[off+8:off+8+blen]
def values(index):
 a=d['accessors'][index];v=d['bufferViews'][a['bufferView']];typ=a['componentType'];fmt={5121:'B',5123:'H',5125:'I',5126:'f'}[typ];dim={'SCALAR':1,'VEC3':3}[a['type']];size=struct.calcsize('<'+fmt*dim);stride=v.get('byteStride',size);start=v.get('byteOffset',0)+a.get('byteOffset',0)
 return [struct.unpack_from('<'+fmt*dim,buf,start+i*stride) for i in range(a['count'])]
result=[]
for mesh in d['meshes']:
 deg=0;nan=0;components=[]
 for p in mesh['primitives']:
  pos=values(p['attributes']['POSITION']);ind=[v[0] for v in values(p['indices'])];parent=list(range(len(pos)))
  def find(a):
   while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
   return a
  def union(a,b):parent[find(a)]=find(b)
  # Weld duplicate exported attribute splits by position for connectivity.
  seen={}
  for i,pt in enumerate(pos):
   key=tuple(round(x,6) for x in pt)
   if key in seen:union(i,seen[key])
   else:seen[key]=i
   nan+=not all(math.isfinite(x) for x in pt)
  for k in range(0,len(ind),3):
   a,b,c=ind[k:k+3];assert max(a,b,c)<len(pos)
   union(a,b);union(b,c)
   e=[pos[b][j]-pos[a][j] for j in range(3)];f=[pos[c][j]-pos[a][j] for j in range(3)]
   cr=[e[1]*f[2]-e[2]*f[1],e[2]*f[0]-e[0]*f[2],e[0]*f[1]-e[1]*f[0]]
   deg+=sum(x*x for x in cr)<1e-20
  components.append(len({find(i) for i in set(ind)}))
 result.append({'mesh':mesh.get('name'),'position_components_per_primitive':components,'degenerate_triangles':deg,'nonfinite_positions':nan})
print(json.dumps(result,indent=2))
