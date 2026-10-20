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
# Rooted swept volumes: broad directional ruff planes, no detached microtufts.
ruff=[]
def swept(name,points,widths,depths):
 vs=[];fs=[];N=20
 for k,p in enumerate(points):
  p=Vector(p);t=(Vector(points[min(k+1,len(points)-1)])-Vector(points[max(0,k-1)])).normalized()
  side=t.cross(Vector((0,1,0))).normalized()
  if side.length<.1:side=Vector((1,0,0))
  depth=t.cross(side).normalized()
  for j in range(N):
   a=math.tau*j/N;vs.append(p+side*widths[k]*math.cos(a)+depth*depths[k]*math.sin(a))
 for k in range(len(points)-1):
  for j in range(N):fs.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
 fs.append(tuple(reversed(range(N))));fs.append(tuple(range((len(points)-1)*N,len(points)*N)))
 o=mesh_obj(name,vs,fs,clay);ruff.append(o)
# Chest keel is rooted through its whole upper half, and fans into two side sweeps.
swept('Rooted central chest flow',[(0,-.33,.76),(0,-.414,.692),(0,-.435,.586),(0,-.395,.486)], [.064,.093,.078,.006],[.059,.047,.041,.005])
for s in [-1,1]:
 swept('Cheek-to-mane flow',[(s*.135,-.335,.831),(s*.208,-.297,.793),(s*.246,-.255,.713),(s*.243,-.178,.665)], [.057,.064,.054,.004],[.06,.047,.035,.004])
 swept('Outer breast flow',[(s*.116,-.29,.731),(s*.18,-.36,.658),(s*.219,-.31,.564),(s*.20,-.224,.522)], [.065,.061,.044,.004],[.065,.04,.031,.004])
 swept('Inner breast flow',[(s*.072,-.36,.708),(s*.106,-.425,.624),(s*.13,-.391,.542),(s*.12,-.31,.495)], [.053,.052,.035,.004],[.051,.037,.027,.004])
# Fuse the ruff into the existing surface before facial incisions.
bpy.ops.object.select_all(action='DESELECT');body.select_set(True)
for o in ruff:o.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join()
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT')
m=body.modifiers.new('Connected ruff sculpt surface','REMESH');m.mode='VOXEL';m.voxel_size=.0045;m.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=m.name)
m=body.modifiers.new('Ruff junction relaxation','SMOOTH');m.factor=.8;m.iterations=3;bpy.ops.object.modifier_apply(modifier=m.name)
surface=bvh();features=[];lid_parts=[];eye_centers=[]
# Recess eye sockets in the actual head mesh, then build almond-shaped eyes/lids.
for s in [-1,1]:
 hit,normal=front_hit(s*.137,.873);N=normal.normalized()
 U=Vector((0,0,1)).cross(N).normalized();V=N.cross(U).normalized()
 C=hit-N*.010;eye_centers.append({'side':s,'surface':list(hit),'normal':list(N)})
 cutter=ellipsoid('Eye socket cutter',hit+N*.012,(.055,.037,.036),(U,V,N));apply_boolean(cutter,'Sculpt recessed orbit')
 # Closed almond lens, with outer corner slightly raised.
 vs=[C+N*.015];fs=[];A=.045;B=.026;K=48;R=6
 for k in range(1,R+1):
  r=k/R
  for j in range(K):
   t=math.tau*j/K;u=A*math.cos(t)*r;vv=B*math.copysign(abs(math.sin(t))**1.45,math.sin(t))*r+s*.10*u
   vs.append(C+U*u+V*vv+N*(.015*(1-r*r)))
 for j in range(K):fs.append((0,1+j,1+(j+1)%K))
 for k in range(R-1):
  for j in range(K):fs.append((1+k*K+j,1+(k+1)*K+j,1+(k+1)*K+(j+1)%K,1+k*K+(j+1)%K))
 back=len(vs);vs.append(C-N*.016)
 for j in range(K):fs.append((back,1+(R-1)*K+(j+1)%K,1+(R-1)*K+j))
 features.append(mesh_obj('Almond eye '+str(s),vs,fs,dark))
 # Upper/lower lids are sculptural rims, closed into socket surroundings.
 for upper in [True,False]:
  pts=[]
  for j in range(17):
   t=(math.pi*j/16) if upper else (math.pi+math.pi*j/16)
   u=A*math.cos(t);vv=B*math.copysign(abs(math.sin(t))**1.45,math.sin(t))+s*.10*u
   pts.append(C+U*u+V*vv+N*.001)
  cu=bpy.data.curves.new('Formed eyelid','CURVE');cu.dimensions='3D';cu.resolution_u=12;cu.bevel_depth=.007 if upper else .005;cu.bevel_resolution=3
  sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
  for bp,p in zip(sp.bezier_points,pts):bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
  ob=bpy.data.objects.new(('Upper' if upper else 'Lower')+' eyelid '+str(s),cu);bpy.context.collection.objects.link(ob);cu.materials.append(clay)
  bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');lid_parts.append(bpy.context.object)
# Connect lids by Boolean union, preserving eye recesses rather than remeshing them away.
for lid in lid_parts:
 bpy.context.view_layer.objects.active=body;m=body.modifiers.new('Connected anatomical eyelid','BOOLEAN');m.operation='UNION';m.solver='EXACT';m.object=lid;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(lid,do_unlink=True)
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
 for x,z in [(0,.752),(.024,.746),(.049,.747),(.077,.754),(.099,.766)]:
  h,n=front_hit(s*x,z);pts.append(h-n*.001)
 cu=bpy.data.curves.new('Mouth groove cutter','CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=.0038;cu.bevel_resolution=3;cu.use_fill_caps=True
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for bp,p in zip(sp.bezier_points,pts):bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 ob=bpy.data.objects.new('Mouth incision tool',cu);bpy.context.collection.objects.link(ob)
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');apply_boolean(bpy.context.object,'Sculpt mouth line')
# Shallow conchal depressions retain a thick outer ear rim.
for s in [-1,1]:
 cutter=ellipsoid('Ear bowl tool',(s*.16,-.399,1.005),(.039,.029,.051));apply_boolean(cutter,'Sculpt inner ear bowl')
body.name='FOX R01b connected head and chest sculpt'
for p in body.data.polygons:p.use_smooth=True
asset=[body]+features
# Export a reduced selected-only study. Source retains the editable detailed mesh.
root=bpy.data.objects.new('FOX export root meters ground origin R01b',None);bpy.context.collection.objects.link(root)
for o in asset:o.parent=root
root.rotation_euler.z=math.pi
bpy.ops.object.select_all(action='DESELECT');root.select_set(True)
for o in asset:o.select_set(True)
bpy.context.view_layer.objects.active=body
m=body.modifiers.new('Test export reduction','DECIMATE');m.ratio=.38
bpy.ops.export_scene.gltf(filepath=str(OUT/'fox-head-chest-test.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
body.modifiers.remove(m);root.rotation_euler.z=0
sc=bpy.context.scene;cam=sc.camera;sc.cycles.samples=24
sc.render.resolution_x=1000;sc.render.resolution_y=1000
sc.render.resolution_percentage=100
views={'head-three-quarter':((2.3,-3.8,1.6),(0,-.35,.79),.92),
 'head-front':((0,-4,1.25),(0,-.38,.80),.90),
 'head-side':((4,-.28,1.18),(0,-.37,.80),.95),
 'three-quarter':((3,-4,2),(0,.12,.55),2.6),
 'front':((0,-4,1.2),(0,.12,.55),2.6),
 'side':((4,0,1.2),(0,.12,.55),2.6),
 'rear':((0,4,1.2),(0,.12,.55),2.6)}
for name,(pos,target,scale) in views.items():
 cam.data.type='ORTHO';cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 sc.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
# Save with a useful head camera and the actual sculpt objects selected.
pos,target,scale=views['head-three-quarter'];cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'fox-head-chest-study.blend'),compress=True)
metrics={'blender':bpy.app.version_string,'source_checkpoint':'972cd78f08d67e03aa473df76a16e3acf650dfc2','method':'Local scripted sculpt fields, Boolean eye sockets/mouth/ear recesses, connected lids and rooted broad ruff lofts on existing .blend mesh','body_vertices':len(body.data.vertices),'body_polygons':len(body.data.polygons),'eye_surface_samples':eye_centers,'views':list(views),'art_verdict':'PENDING_VISUAL_REVIEW','premium_materials':False,'rigged':False}
(OUT/'metrics.json').write_text(json.dumps(metrics,indent=2))
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'fox-head-chest-test.glb'))
(OUT/'glb-roundtrip.json').write_text(json.dumps({'mesh_objects':sum(o.type=='MESH' for o in bpy.context.scene.objects),'armatures':sum(o.type=='ARMATURE' for o in bpy.context.scene.objects),'animations':len(bpy.data.actions)},indent=2))
