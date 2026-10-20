"""LN-FOX-R01a editable fused-volume proportion study. Blender 4.2, CPU.
X lateral; -Y forward; Z up; meters. No rig, no gameplay integration.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/fox-r01a';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,c,rough=.8):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough
 return m
clay=mat('Neutral warm grey clay',(.43,.46,.48));dark=mat('Eye and nose graphite',(.025,.031,.038),.3)
parts=[]
def oval(name,pos,scale,group=parts,material=clay):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=pos)
 o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 if group is not None:group.append(o)
 return o
def loft(name,sections,axis='Y'):
 # Authored continuous silhouette sections, Catmull-Rom interpolation.
 v=[];f=[];N=28;steps=6
 def cr(a,b,c,d,t):return .5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)
 sec=[]
 for k in range(len(sections)-1):
  a=sections[max(0,k-1)];b=sections[k];c=sections[k+1];d=sections[min(len(sections)-1,k+2)]
  for j in range(steps):sec.append([cr(a[q],b[q],c[q],d[q],j/steps) for q in range(5)])
 sec.append(sections[-1])
 for cx,cy,cz,rx,rz in sec:
  for j in range(N):
   t=math.tau*j/N
   if axis=='Y':v.append((cx+rx*math.cos(t),cy,cz+rz*math.sin(t)))
   else:v.append((cx+rx*math.cos(t),cy+rz*math.sin(t),cz))
 for k in range(len(sec)-1):
  for j in range(N):f.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
 f.append(tuple(reversed(range(N))));f.append(tuple(range((len(sec)-1)*N,len(sec)*N)))
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);parts.append(ob);return ob
# A single authored trunk silhouette: neck, breast, ribcage, loin, croup.
loft('Continuous neck and trunk',[
 (0,-.47,.84,.11,.12),(0,-.38,.77,.18,.20),(0,-.25,.66,.225,.245),
 (0,-.08,.62,.216,.225),(0,.14,.61,.205,.205),(0,.31,.61,.196,.203),
 (0,.45,.60,.186,.205),(0,.55,.59,.11,.12),(0,.58,.59,.015,.025)])
# Tapered muzzle and cranial wedge, with no pendulous cheek spheres.
loft('Cranium and muzzle wedge',[
 (0,-.715,.871,.026,.023),(0,-.665,.871,.062,.041),
 (0,-.595,.88,.091,.065),(0,-.535,.922,.133,.111),
 (0,-.45,.946,.180,.151),(0,-.35,.935,.177,.151),
 (0,-.275,.91,.112,.119),(0,-.245,.90,.025,.04)])
for sign in [-1,1]:
 # Flowing cheek plane widening toward the neck, no circular hanging pouch.
 loft('Lateral cheek wedge',[
  (sign*.105,-.535,.892,.031,.035),(sign*.148,-.45,.89,.063,.071),
  (sign*.158,-.345,.88,.073,.084),(sign*.135,-.265,.84,.043,.075),
  (sign*.09,-.23,.82,.014,.035)])
 # Forelimb swept sections remove spherical scalloping.
 loft('Forelimb',[(sign*.15,-.235,.66,.078,.09),(sign*.15,-.245,.48,.067,.065),
  (sign*.15,-.26,.33,.050,.048),(sign*.15,-.26,.17,.039,.041),
  (sign*.15,-.28,.065,.047,.052)],'Z')
 # Haunch follows the croup instead of cresting above the back.
 loft('Hind limb',[(sign*.14,.40,.62,.090,.104),(sign*.16,.36,.44,.093,.098),
  (sign*.16,.29,.31,.060,.061),(sign*.16,.43,.185,.039,.039),
  (sign*.16,.415,.067,.035,.040)],'Z')
 oval('Front paw',(sign*.15,-.31,.048),(.062,.086,.048))
 oval('Hind paw',(sign*.16,.38,.045),(.058,.080,.045))
 # Small rounded pinnae, broad base and curved tip.
 v=[];f=[]
 rings=[(0,.081,.052),(.035,.079,.047),(.085,.052,.030),(.125,.020,.012),(.137,.003,.003)]
 for z,w,d in rings:
  for j in range(24):
   t=j*math.tau/24;v.append((sign*(.125+z*.12)+w*math.cos(t),-.364+d*math.sin(t)+z*.12,1.035+z))
 for k in range(len(rings)-1):
  for j in range(24):f.append((k*24+j,k*24+(j+1)%24,(k+1)*24+(j+1)%24,(k+1)*24+j))
 f.append(tuple(reversed(range(24))));f.append(tuple(range(96,120)))
 me=bpy.data.meshes.new('Pinna loft');me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new('Rounded short ear',me);bpy.context.collection.objects.link(ob);parts.append(ob)
# Big descending brush, gentle lateral curl; all tail sections fused into core.
for i in range(17):
 t=i/16;y=.52+t*.63;z=.60-.31*t; x=.19*math.sin(t*2.1)
 r=.065+.17*math.sin(math.pi*t)**.72
 oval('Tail brush', (x,y,z),(r*.88,r*1.1,r))
# Merge and voxel-union: eliminate primitive intersections before assessment.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();body=bpy.context.object;body.name='FOX continuous anatomical clay'
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT')
r=body.modifiers.new('Fused sculpt volumes','REMESH');r.mode='VOXEL';r.voxel_size=.008;r.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=r.name)
s=body.modifiers.new('Organic junction relaxation','SMOOTH');s.factor=1.1;s.iterations=12;bpy.ops.object.modifier_apply(modifier=s.name)
for p in body.data.polygons:p.use_smooth=True
# Flatten paw soles gently for supported stance.
for vert in body.data.vertices:
 worldz=(body.matrix_world@vert.co).z
 if worldz<.022:vert.co.z += .008-worldz
# Features remain separable for future facial retopology.
features=[]
for sign in [-1,1]:
 o=oval('Eye', (sign*.124,-.548,.953),(.030,.015,.022),features,dark)
 # Dark inset pinna is intentionally absent in clay pass: inspect ear form first.
oval('Nose',(0,-.721,.874),(.033,.020,.023),features,dark)
asset=[body]+features
# Zero ground contact, fixed origin, meters, no hidden proxy.
for o in asset:
 bpy.context.view_layer.objects.active=o;o.select_set(True)
bpy.context.scene.unit_settings.system='METRIC'
bpy.context.scene.unit_settings.scale_length=1
# Preserve raw editable mesh and unapplied sculpt subdivision.
sub=body.modifiers.new('Sculpt continuation','SUBSURF');sub.levels=1;sub.render_levels=1
bpy.ops.object.select_all(action='DESELECT')
root=bpy.data.objects.new('FOX export root meters ground origin',None);bpy.context.collection.objects.link(root)
for o in asset:o.parent=root
root.rotation_euler.z=math.pi
root.select_set(True)
for o in asset:o.select_set(True)
bpy.context.view_layer.objects.active=body
bpy.ops.export_scene.gltf(filepath=str(OUT/'fox-clay-test.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
root.rotation_euler.z=0
# Studio outside export selection.
ground=mat('Studio ground',(.13,.16,.19))
bpy.ops.mesh.primitive_plane_add(size=200);bpy.context.object.data.materials.append(ground);bpy.context.object.location.z=-.007
sc=bpy.context.scene;sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.38,.43,.5,1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value=.4
for pos,power,size,col in [((-3,-4,5),450,4,(1,.89,.78)),((3,-1,3),300,3,(.72,.84,1)),((1,4,4),500,3,(1,.93,.85))]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=col;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;sc.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=2.65
sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=20;sc.cycles.use_denoising=True
sc.render.resolution_x=1000;sc.render.resolution_y=900;sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'fox-character-study.blend'),compress=True)
views={'front':(0,-4,1.3),'side':(4,0,1.3),'rear':(0,4,1.3),'three-quarter':(3,-4,2.0),'gameplay':(2.8,4.5,2.8)}
for name,pos in views.items():
 cam.location=pos;target=Vector((0,.12,.59));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=5.5 if name=='gameplay' else 2.65
 sc.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
metrics={'blender':bpy.app.version_string,'stage':'neutral anatomical form gate; no premium material pass','units':'meters','forward_blender':'-Y','forward_gltf':'-Z','height_m':max((body.matrix_world@Vector(v)).z for v in body.bound_box),'body_vertices':len(body.data.vertices),'body_polygons':len(body.data.polygons),'rigged':False,'views':list(views),'art_verdict':'PENDING_VISUAL_REVIEW','round':2}
(OUT/'metrics.json').write_text(json.dumps(metrics,indent=2))
# Reimport test GLB separately to prove parser, dimensions and absence of armatures.
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'fox-clay-test.glb'))
report={'imported_meshes':sum(o.type=='MESH' for o in bpy.context.scene.objects),'armatures':sum(o.type=='ARMATURE' for o in bpy.context.scene.objects),'animations':len(bpy.data.actions),'bounds':{o.name:list(o.dimensions) for o in bpy.context.scene.objects if o.type=='MESH'}}
(OUT/'glb-roundtrip.json').write_text(json.dumps(report,indent=2))
