"""LN-R01d isolated spruce bough. Reproducible, mesh-first procedural sculpture.
Requires numpy and trimesh. Export GLB in metres; glTF importer applies Z-up -> Y-up.
No whole tree, no environment or game assets affected.
"""
from __future__ import annotations
import json, math, random
from pathlib import Path
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'public/models/ln-r01d-hero-bough.glb'
METRICS=ROOT/'docs/r01d/mesh-metrics.json'
R = random.Random(24102026)
COLORS={
 'cedar': [103,58,37,255],
 'pine': [29,85,72,255],
 'teal': [43,102,92,255],
 'sage': [80,123,89,255],
 'snow': [227,235,244,255],
}
PARTS={k:[] for k in COLORS}

def vec(x): return np.array(x,dtype=float)
def normalize(v):
 v=vec(v); l=np.linalg.norm(v)
 return v/(l if l>1.e-8 else 1)
def lerp(a,b,t): return vec(a)*(1-t)+vec(b)*t
def smoothstep(x):
 x=min(1,max(0,x));return x*x*(3-2*x)

def ring_sweep(name,pts,rads,sides=9,vertical_factor=1,warp=0):
 """Closed variable cross section around continuous skeletal curves."""
 p=np.asarray(pts,float);v=[];faces=[]
 for i,center in enumerate(p):
  d=normalize(p[min(i+1,len(p)-1)]-p[max(0,i-1)])
  n=np.cross(d,[0,0,1]);n=normalize(n) if np.linalg.norm(n)>.05 else vec([0,1,0]);b=normalize(np.cross(d,n))
  for j in range(sides):
   a=j*math.tau/sides
   rr=rads[i]*(1+.055*math.sin(a*3+1.2*i)+warp*math.sin(i*.7+2*a))
   v.append(center+rr*(math.cos(a)*n+math.sin(a)*b*vertical_factor))
 for i in range(len(p)-1):
  for j in range(sides):
   k=i*sides+j;q=i*sides+(j+1)%sides;faces.extend(((k,q,q+sides),(k,q+sides,k+sides)))
 for j in range(1,sides-1):
  faces.append((0,j+1,j));end=(len(p)-1)*sides;faces.append((end,end+j,end+j+1))
 PARTS[name].append(trimesh.Trimesh(vertices=v,faces=faces,process=False))

def main(t):
 return vec([3.40*t, .048*math.sin(t*8)+.045*math.sin(t*3), -.05-.58*t**1.55+.045*math.sin(t*math.pi*2)])
ring_sweep('cedar',[main(i/28) for i in range(29)],[.095*(1-i/28)**1.18+.014 for i in range(29)],13,warp=.10)

# Frond: longitudinal taper and flattened (yet sculpturally volumetric) needles.
# The boundary is lobed at many scales; unlike R01c, there are no oversized leaf-fingers.
def foliage_frond(start,end,width,thickness,mat,seed):
 rng=random.Random(seed)
 start,end=vec(start),vec(end)
 d=normalize(end-start)
 lateral=normalize(np.cross([0,0,1],d))
 up=normalize(np.cross(d,lateral))
 if np.dot(up,[0,0,1])<0:up=-up
 steps=11;sides=10;vertices=[];faces=[]
 bend=rng.uniform(-.08,.08);roll=rng.uniform(-.22,.22)
 for i in range(steps+1):
  t=i/steps
  spine=lerp(start,end,t)+lateral*bend*math.sin(math.pi*t)+vec([0,0,-.065*t*t])
  taper=(math.sin(math.pi*(.16+.73*t)))**.42
  taper*= (.78+.22*smoothstep(t/.16)) * (1-.55*smoothstep((t-.86)/.14))
  for j in range(sides):
   a=j*math.tau/sides
   edge=1+.10*math.sin(5*math.pi*t+rng.uniform(-.08,.08))+.055*math.sin(a*4+t*40)
   spread=width*taper*edge*math.cos(a)
   height=thickness*taper*math.sin(a)
   height+=-.024*t*t*abs(math.cos(a))  # drooping foliage silhouette
   vertices.append(spine + lateral*spread + up*height + up*roll*spread)
 for i in range(steps):
  for j in range(sides):
   a=i*sides+j;b=i*sides+(j+1)%sides
   faces.extend(((a,b,b+sides),(a,b+sides,a+sides)))
 for j in range(1,sides-1):
  faces.append((0,j+1,j));endbase=steps*sides;faces.append((endbase,endbase+j,endbase+j+1))
 PARTS[mat].append(trimesh.Trimesh(vertices=vertices,faces=faces,process=False))

# Real short spruce needle tufts. Tiny downward-facing sprigs are subordinate to the body.
def sprig(start,end,radius,mat):
 ring_sweep(mat,[start,lerp(start,end,.48)+[0,0,-.015],end],[radius*.57,radius,radius*.05],5,.75)

# Secondary limbs connected along the main branch, fanning left and right.
branch_records=[]
# Asymmetric real bough: no paired whorls, no repeating fishbone tiers.
branch_specs=[(.16,-1,1.18),(.28,1,.94),(.34,-1,.85),(.43,1,1.14),(.52,-1,1.06),(.57,1,.67),(.65,-1,.84),(.73,1,1.12),(.80,-1,.66),(.86,1,.77),(.93,-1,.48)]
for bi,(t,side,scale) in enumerate(branch_specs):
 o=main(t)
 length=(1.35-.62*t)*scale*R.uniform(.89,1.12)
 direction=vec([.48+R.uniform(-.13,.16),side*(.81+R.uniform(-.19,.15)),-.12-R.uniform(0,.16)])
 end=o+normalize(direction)*length+vec([0,0,-.09])
 pts=[lerp(o,end,i/8)+vec([0,0,-.065*math.sin(math.pi*i/8)]) for i in range(9)]
 ring_sweep('cedar',pts,[.045*(1-i/8)**1.2+.005 for i in range(9)],8,warp=.07)
 branch_records.append((bi,side,t,o,end))
 # Dense organic volume: overlapping clusters distributed on staggered twiglets.
 # Short tapered subfronds and small needle scallops replace long paddle leaves.
 n=13 if t<.7 else 9
 for j in range(n):
  q=(j+.35)/n
  anchor=lerp(o,end,q)+vec([0,0,-.055*q*q])
  for fan_side in [-2,-1,0,1,2]:
   offset=vec([R.uniform(.03,.07),side*.14+fan_side*.10,R.uniform(-.045,-.005)])
   axis=normalize(end-o)
   delta=axis*R.uniform(.075,.12)+offset*R.uniform(.8,1.3)
   tip=anchor+delta
   width=R.uniform(.045,.075)*(1-.15*q)
   foliage_frond(anchor,tip,width,R.uniform(.035,.059),'pine' if R.random()<.58 else 'teal',bi*5000+(side+1)*1000+j*61+fan_side)
   # small twig silhouettes projecting below the overlapped foliage masses
   for k in range(2):
    p=lerp(anchor,tip,(k+1)/3)
    vecdir=normalize(tip-anchor+vec([R.uniform(-.16,.16),R.uniform(-.12,.12),-.22]))
    if k==1 or R.random()<.30:
     sprig(p,p+vecdir*R.uniform(.035,.067),R.uniform(.007,.012),'sage' if R.random()<.32 else 'teal')
 # Underbranch thin smaller foliage extensions, producing layered green edges.
 for j in range(5):
  q=.18+j*.16
  p=lerp(o,end,q)
  direction=normalize(vec([.24,side*.61+R.uniform(-.15,.15),-.55]))
  foliage_frond(p,p+direction*R.uniform(.085,.16),.045,.038,'sage' if R.random()<.24 else 'pine',23000+bi*100+side*21+j)

# Organic overlapping centre fill above and below the woody structure.
# Several spatial scales to avoid the 'row of separate tassels' failure.
for i in range(190):
 q=.12+.85*R.random();p=main(q)
 a=R.random()*math.tau
 radial=vec([.05+.11*R.random(),math.sin(a)*R.uniform(.10,.28),-.02-R.random()*.08])
 tip=p+radial
 foliage_frond(p+vec([0,R.uniform(-.03,.03),0]),tip,.049+R.random()*.047,.042+R.random()*.023,
               R.choices(['pine','teal','sage'],[.52,.39,.09])[0],40000+i)

# Sculpted caps: closed, thick contour shells that are integrally positioned against
# the underlying dense needle volumes. Undersides and lipped edge follow fan curvature.
def snow_quilt(start,end,width,seed,heavy=True):
 rng=random.Random(seed);start=vec(start);end=vec(end)
 axis=normalize(end-start)
 across=normalize(np.cross([0,0,1],axis));up=vec([0,0,1.0])
 rows=20;across_steps=14;points=[];tris=[]
 length=np.linalg.norm(end-start)
 for layer in [0,1]: # top and lower surface
  for i in range(rows+1):
   t=i/rows
   length_profile=(math.sin(math.pi*(.035+.93*t)))**.67
   length_profile*=1-.24*smoothstep((t-.79)/.21)
   c=lerp(start,end,t)+vec([0,0,-.042*t*t])
   for j in range(across_steps+1):
    u=2*j/across_steps-1
    natural_edge=1+.13*math.sin(t*7.1+seed*.75)+.055*math.sin(t*12.5+u*3)
    w=width*length_profile*natural_edge*u
    # Convex upper surface, irregular soft curling at the perimeter.
    upper=(.105 if heavy else .080)*length_profile + .042*math.cos(u*math.pi/2) + .011*math.sin(2.5*math.pi*t+u*2.3)
    lip=(.055+.021*math.sin(4.8*t+seed)) * smoothstep((abs(u)-.63)/.36)
    below=upper-(.085 if heavy else .063)-lip
    h=(upper if layer==0 else below)
    h-=.060*abs(u)**2
    points.append(c+across*w+up*h)
 pitch=(rows+1)*(across_steps+1)
 for i in range(rows):
  for j in range(across_steps):
   a=i*(across_steps+1)+j;b=a+across_steps+1
   tris.extend(((a,a+1,b+1),(a,b+1,b)))
   tris.extend(((pitch+a,pitch+b+1,pitch+a+1),(pitch+a,pitch+b,pitch+b+1)))
 # closed softly folded edges
 for i in range(rows):
  for j in [0,across_steps]:
   a=i*(across_steps+1)+j;b=(i+1)*(across_steps+1)+j
   tris.extend(((a,b,pitch+b),(a,pitch+b,pitch+a)))
 for j in range(across_steps):
  for i in [0,rows]:
   a=i*(across_steps+1)+j;b=a+1
   tris.extend(((a,pitch+a,pitch+b),(a,pitch+b,b)))
 PARTS['snow'].append(trimesh.Trimesh(vertices=points,faces=tris,process=False))

# Fourteen non-uniform caps on upper fan surfaces. Each foliage fan remains exposed
# beyond the snow perimeter; some gaps intentionally reveal the warm wooden skeleton.
for bi,side,t,o,end in branch_records:
 if bi in (2,7,9):continue
 start=lerp(o,end,.10+R.random()*.12)+vec([0,0,.075])
 finish=lerp(o,end,.65+R.random()*.23)+vec([0,0,.04])
 width=(.20 if t>.7 else .30)*(0.78+R.random()*.32)
 snow_quilt(start,finish,width,bi*10+side,heavy=bi<5)
 # Irregular shoulder, second smaller snowy mound (not every bough).
 if bi in (0,3,5) and side==1:
  a=lerp(o,end,.10)+vec([0,0,.10]);b=lerp(o,end,.43)+vec([0,0,.08]);snow_quilt(a,b,width*.68,90+bi)

# Central snow pillows break up a line of identical lateral caps.
for k in [1,4,7]:
 t=.12+.105*k;p=main(t)+vec([0,0,.08]);q=main(min(.98,t+.12))+vec([0,0,.07]);snow_quilt(p,q,.13,140+k,heavy=False)

scene=trimesh.Scene()
for mat,ls in PARTS.items():
 if not ls:continue
 combo=trimesh.util.concatenate(ls)
 combo.visual.vertex_colors=np.tile(np.array(COLORS[mat],dtype=np.uint8),(len(combo.vertices),1))
 scene.add_geometry(combo,geom_name=mat,node_name=mat)
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_bytes(scene.export(file_type='glb'))
meshes=list(scene.geometry.values())
metrics={
 'generator':'LN-R01d bough v3 / asymmetric branch study + compact overlapping foliage and snow geometry',
 'seed':24102026, 'triangles':sum(len(m.faces) for m in meshes),
 'vertices':sum(len(m.vertices) for m in meshes),
 'meshes':len(meshes),'materials':len(meshes),
 'fileBytes':OUT.stat().st_size,
 'geometryBytes':sum(m.vertices.nbytes+m.faces.nbytes for m in meshes),
 'bounds':[list(map(float,scene.bounds[0])),list(map(float,scene.bounds[1]))],
 'meshTriangles':{k:sum(len(m.faces) for m in v) for k,v in PARTS.items()},
 'note':'Python topology counts; WebGL draw calls require real Three.js capture. Includes unmerged intersections inside material batches.'
}
METRICS.parent.mkdir(parents=True,exist_ok=True);METRICS.write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
