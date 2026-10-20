"""Focused anatomical mesh editing on the preserved R01a .blend, Blender 4.2.
This uses scripted sculpt displacements, Boolean recesses and rooted lofts;
not a claim of manual brush sculpting. No gameplay changes or rigging.
"""
import bpy,math,json
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/fox-r01b';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/fox-r01a/fox-character-study.blend'))
bpy.context.preferences.filepaths.save_version=0
body=bpy.data.objects['FOX continuous anatomical clay']
for m in list(body.modifiers):body.modifiers.remove(m)
body.parent=None
bpy.context.view_layer.objects.active=body
bpy.ops.object.select_all(action='DESELECT');body.select_set(True)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
clay=bpy.data.materials['Neutral warm grey clay'];dark=bpy.data.materials['Eye and nose graphite']
# Remove the bead eyes and primitive nose; retain the editable anatomical mesh.
for o in list(bpy.data.objects):
 if o.name in ['Eye','Eye.001','Nose']:bpy.data.objects.remove(o,do_unlink=True)
# Localized smooth sculpt fields to break the flat mask/neck transition.
def g(x,y,z,c,s):return math.exp(-sum(((v-a)/r)**2 for v,a,r in zip((x,y,z),c,s))*1.8)
for v in body.data.vertices:
 x,y,z=v.co;sign=1 if x>=0 else -1
 # Zygomatic plane sweeps backward and outward, not down like a cheek pouch.
 w=g(x,y,z,(sign*.165,-.36,.797),(.105,.17,.11))
 v.co.x+=sign*.022*w;v.co.z+=.013*w
 # Chest breast tapers into the forelimbs rather than a vertical cylinder.
 w=g(x,y,z,(0,-.337,.605),(.18,.13,.18));v.co.y-=.018*w
 # Forehead bridge slightly fuller, with a calmer brow-to-muzzle transition.
 w=g(x,y,z,(0,-.486,.902),(.13,.13,.085));v.co.z+=.014*w
# Mesh-surface sampling in modeling coordinates.
def bvh():return BVHTree.FromPolygons([v.co.copy() for v in body.data.vertices],[tuple(p.vertices) for p in body.data.polygons])
surface=bvh()
def front_hit(x,z):
 h,n,idx,d=surface.ray_cast(Vector((x,-1.5,z)),Vector((0,1,0)),3)
 if h is None:raise RuntimeError('Facial surface sample missed: '+str((x,z)))
 return h,n

def mesh_obj(name,vs,fs,material=None):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o)
 if material:o.data.materials.append(material)
 for p in me.polygons:p.use_smooth=True
 return o

def apply_boolean(cutter,name):
 bpy.context.view_layer.objects.active=body
 m=body.modifiers.new(name,'BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter
 bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)
def ellipsoid(name,center,scale,axes=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=center);o=bpy.context.object;o.name=name;o.scale=scale
 if axes:o.rotation_euler=Matrix((axes[0],axes[1],axes[2])).transposed().to_euler()
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o
# Flowing ruff is sculpted directly into the existing skin, avoiding attached blocks.
for v in body.data.vertices:
 x,y,z=v.co
 w=g(x,y,z,(0,-.32,.655),(.225,.145,.195))
 v.co.y-=.046*w
 # Broad lateral neck envelope; smooth cheek-to-chest continuity.
 w=g(x,y,z,((1 if x>=0 else -1)*.16,-.28,.725),(.105,.16,.14))
 v.co.x+=(1 if x>=0 else -1)*.018*w
 # Unequal broad descending flow ridges, continuously rooted in the skin.
 if -.54<y<-.19 and .45<z<.77:
  for sign in [-1,1]:
   t=max(0,min(1,(.75-z)/.28));xc=sign*(.056+.074*t+.018*math.sin(t*math.pi))
   band=math.exp(-((x-xc)/(.035-.012*t))**2)*math.sin(math.pi*t)**.75
   front=math.exp(-((y+.38)/.13)**2)
   v.co.y-=.013*band*front
 # Muzzle pads: restrained paired fullness above the mouth corners.
 for sign in [-1,1]:
  w=g(x,y,z,(sign*.044,-.63,.785),(.05,.065,.038))
  v.co.y-=.007*w;v.co.x+=sign*.004*w
surface=bvh();features=[];eye_centers=[]
# Smooth orbital annuli are carved into the existing head skin.
eye_frames=[]
for sign in [-1,1]:
 hit,normal=front_hit(sign*.137,.873);N=normal.normalized()
 U=Vector((0,0,1)).cross(N).normalized();V=N.cross(U).normalized()
 eye_frames.append((sign,hit,N,U,V))
 for vert in body.data.vertices:
  delta=vert.co-hit;u=delta.dot(U);vv=delta.dot(V);depth=delta.dot(N)
  if abs(depth)<.045 and abs(u)<.083 and abs(vv)<.058:
   r=math.sqrt((u/.047)**2+(vv/.029)**2)
   ridge=.0085*math.exp(-((r-1.14)/.31)**2)
   if vv<0:ridge*=.60
   vert.co+=N*ridge*math.exp(-(depth/.036)**2)
# Recess eye sockets in the actual head mesh, then build almond-shaped eyes/lids.
for s,hit,N,U,V in eye_frames:
 C=hit-N*.004;eye_centers.append({'side':s,'surface':list(hit),'normal':list(N)})
 # A softly beveled almond aperture, instead of an ellipsoidal drilled socket.
 vs=[];fs=[];K=64
 for depth in [-.047,.055]:
  for j in range(K):
   t=math.tau*j/K;u=.043*math.cos(t);vv=.024*math.copysign(abs(math.sin(t))**1.35,math.sin(t))+s*.07*u
   vs.append(hit+U*u+V*vv+N*depth)
 fs=[tuple(reversed(range(K))),tuple(range(K,2*K))]
 for j in range(K):fs.append((j,(j+1)%K,(j+1)%K+K,j+K))
 cutter=mesh_obj('Almond orbit cutter',vs,fs)
 bpy.context.view_layer.objects.active=cutter;m=cutter.modifiers.new('Soft aperture perimeter','BEVEL');m.width=.003;m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 apply_boolean(cutter,'Sculpt almond eye aperture')
 # Closed almond lens, with outer corner slightly raised.
 vs=[C+N*.022];fs=[];A=.050;B=.031;K=64;R=8
 for k in range(1,R+1):
  r=k/R
  for j in range(K):
   t=math.tau*j/K;u=A*math.cos(t)*r;vv=B*math.copysign(abs(math.sin(t))**1.45,math.sin(t))*r+s*.10*u
   vs.append(C+U*u+V*vv+N*(.022*(1-r*r)))
 for j in range(K):fs.append((0,1+j,1+(j+1)%K))
 for k in range(R-1):
  for j in range(K):fs.append((1+k*K+j,1+(k+1)*K+j,1+(k+1)*K+(j+1)%K,1+k*K+(j+1)%K))
 back=len(vs);vs.append(C-N*.016)
 for j in range(K):fs.append((back,1+(R-1)*K+(j+1)%K,1+(R-1)*K+j))
 features.append(mesh_obj('Almond eye '+str(s),vs,fs,dark))
# Authored triangular nose, rounded edges; upper muzzle remains exposed.
hit,_=front_hit(0,.783);yc=hit.y
outline=[(-.030,.008),(-.024,.018),(.024,.018),(.030,.008),(.012,-.014),(0,-.019),(-.012,-.014)]
vs=[]
for y in [yc-.019,yc+.013]:
 for x,z in outline:vs.append((x,y,.783+z))
n=len(outline);fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]
for j in range(n):fs.append((j,(j+1)%n,(j+1)%n+n,j+n))
nose=mesh_obj('Rounded triangular nose',vs,fs,dark);features.append(nose)
bpy.context.view_layer.objects.active=nose;m=nose.modifiers.new('Soft nose perimeter','BEVEL');m.width=.006;m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
# Mouth incisions follow the pre-Boolean head surface; no floating painted smile.
for s in [-1,1]:
 pts=[]
 for x,z in [(0,.752),(.024,.747),(.049,.748),(.072,.752),(.091,.758)]:
  h,n=front_hit(s*x,z);pts.append(h-n*.001)
 cu=bpy.data.curves.new('Mouth groove cutter','CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=.0031;cu.bevel_resolution=3;cu.use_fill_caps=True
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for bp,p in zip(sp.bezier_points,pts):bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 ob=bpy.data.objects.new('Mouth incision tool',cu);bpy.context.collection.objects.link(ob)
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');apply_boolean(bpy.context.object,'Sculpt mouth line')
# Rounded triangular conchal bowls, rather than circular drilled holes.
for sign in [-1,1]:
 outline=[(-.027,-.031),(.025,-.031),(.028,-.009),(.010,.036),(0,.046),(-.015,.027),(-.028,-.008)]
 vs=[]
 for yy in [-.433,-.377]:
  for xx,zz in outline:vs.append((sign*.16+xx,yy,1.005+zz))
 nn=len(outline);fs=[tuple(reversed(range(nn))),tuple(range(nn,2*nn))]
 for j in range(nn):fs.append((j,(j+1)%nn,(j+1)%nn+nn,j+nn))
 cutter=mesh_obj('Conchal bowl cutter',vs,fs)
 bpy.context.view_layer.objects.active=cutter;m=cutter.modifiers.new('Rounded inner ear edge','BEVEL');m.width=.008;m.segments=4;bpy.ops.object.modifier_apply(modifier=m.name)
 apply_boolean(cutter,'Sculpt triangular inner ear bowl')
# Resurface the clay once after incisions, removing Boolean slivers and blending lids.
bpy.context.view_layer.objects.active=body
m=body.modifiers.new('Clean continuous facial sculpt surface','REMESH');m.mode='VOXEL';m.voxel_size=.0032;m.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=m.name)
m=body.modifiers.new('Relax incision edges','SMOOTH');m.factor=.55;m.iterations=2;bpy.ops.object.modifier_apply(modifier=m.name)
# Discard only tiny disconnected remnants, fail if a meaningful facial piece is detached.
import bmesh
bm=bmesh.new();bm.from_mesh(body.data);remaining=set(bm.verts);groups=[]
while remaining:
 seed=remaining.pop();stack=[seed];component=[seed]
 while stack:
  a=stack.pop()
  for e in a.link_edges:
   b=e.other_vert(a)
   if b in remaining:remaining.remove(b);stack.append(b);component.append(b)
 groups.append(component)
groups.sort(key=len,reverse=True);removed=[len(g) for g in groups[1:]]
if sum(removed)>len(groups[0])*.002:raise RuntimeError('Meaningful detached geometry: '+str(removed))
for group in groups[1:]:bmesh.ops.delete(bm,geom=group,context='VERTS')
bm.to_mesh(body.data);bm.free()
# Satin graphite keeps shape legible without mirror-like eye highlights.
dark.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.52
body.name='FOX R01b connected head and chest sculpt'
for p in body.data.polygons:p.use_smooth=True
asset=[body]+features
# Export a reduced selected-only study. Source retains the editable detailed mesh.
root=bpy.data.objects.new('FOX export root meters ground origin R01b',None);bpy.context.collection.objects.link(root)
for o in asset:o.parent=root
root.rotation_euler.z=math.pi
bpy.ops.object.select_all(action='DESELECT');root.select_set(True)
for o in asset:o.select_set(True)
# Export-only copy: preserve the full sculpt, clean reduced triangle geometry.
bpy.ops.object.select_all(action='DESELECT')
exp=body.copy();exp.data=body.data.copy();exp.name='FOX R01b reduced test mesh';bpy.context.collection.objects.link(exp)
exp.select_set(True);bpy.context.view_layer.objects.active=exp
m=exp.modifiers.new('Test export reduction','DECIMATE');m.ratio=.20;bpy.ops.object.modifier_apply(modifier=m.name)
export_removed={}
for ob in [exp]+features:
 bm=bmesh.new();bm.from_mesh(ob.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0000005)
 bmesh.ops.triangulate(bm,faces=list(bm.faces))
 tiny=[f for f in bm.faces if f.calc_area()<1e-13];export_removed[ob.name]=len(tiny)
 if tiny:bmesh.ops.delete(bm,geom=tiny,context='FACES_ONLY')
 bm.normal_update();bm.to_mesh(ob.data);bm.free()
bpy.ops.object.select_all(action='DESELECT');root.select_set(True);exp.select_set(True)
for ob in features:ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'fox-head-chest-test.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
bpy.data.objects.remove(exp,do_unlink=True)
root.rotation_euler.z=0
sc=bpy.context.scene;cam=sc.camera;sc.cycles.samples=20
sc.render.resolution_x=1000;sc.render.resolution_y=1000
sc.render.resolution_percentage=100
views={'head-three-quarter':((2.3,-3.8,1.6),(0,-.35,.79),.92),
 'head-front':((0,-4,1.25),(0,-.38,.80),.90),
 'head-side':((4,-.28,1.18),(0,-.37,.80),.95),
 'three-quarter':((3,-4,2),(0,.12,.55),2.6),
 'front':((0,-4,1.2),(0,.12,.55),2.6),
 'side':((4,0,1.2),(0,.12,.55),2.6),
 'rear':((0,4,1.2),(0,.12,.55),2.6)}
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'fox-head-chest-study.blend'),compress=True)
for name,(pos,target,scale) in views.items():
 cam.data.type='ORTHO';cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 sc.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
# Save with a useful head camera and the actual sculpt objects selected.
pos,target,scale=views['head-three-quarter'];cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'fox-head-chest-study.blend'),compress=True)
metrics={'blender':bpy.app.version_string,'source_checkpoint':'972cd78f08d67e03aa473df76a16e3acf650dfc2','method':'Direct continuous-skin ruff sculpt fields, anatomical orbital annuli, beveled almond apertures, triangular conchal bowls, clean resurfacing on preserved .blend mesh','correction_round':2,'removed_tiny_components':removed,'export_zero_area_faces_removed':export_removed,'body_vertices':len(body.data.vertices),'body_polygons':len(body.data.polygons),'eye_surface_samples':eye_centers,'views':list(views),'art_verdict':'PENDING_VISUAL_REVIEW','premium_materials':False,'rigged':False}
(OUT/'metrics.json').write_text(json.dumps(metrics,indent=2))
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'fox-head-chest-test.glb'))
(OUT/'glb-roundtrip.json').write_text(json.dumps({'mesh_objects':sum(o.type=='MESH' for o in bpy.context.scene.objects),'armatures':sum(o.type=='ARMATURE' for o in bpy.context.scene.objects),'animations':len(bpy.data.actions)},indent=2))
