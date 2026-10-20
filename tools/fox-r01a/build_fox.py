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
def link(name,a,b,ra,rb):
 # Continuous anatomical volume sampled with overlapping cross sections.
 a,b=Vector(a),Vector(b)
 for i in range(7):
  t=i/6;p=a.lerp(b,t);r=ra*(1-t)+rb*t
  oval(name+str(i),p,(r,r,r*1.12))
# Compact ribcage, subtly tucked loin, rounded pelvis, raised neck.
oval('Ribcage',(0,.02,.60),(.205,.345,.235))
oval('Loin',(0,.27,.61),(.17,.24,.185))
oval('Pelvis',(0,.40,.59),(.205,.225,.23))
oval('Shoulder mantle',(0,-.20,.65),(.225,.215,.265))
link('Neck',(0,-.22,.66),(0,-.39,.87),.195,.17)
oval('Cranium',(0,-.405,.92),(.19,.185,.19))
oval('Forehead',(0,-.49,.96),(.15,.135,.12))
oval('Tapered muzzle',(0,-.585,.86),(.105,.155,.075))
oval('Muzzle bridge',(0,-.55,.90),(.102,.12,.078))
oval('Chin',(0,-.57,.818),(.085,.12,.04))
for s in [-1,1]:
 oval('Cheek', (s*.135,-.405,.86),(.10,.135,.13))
 # Shoulder -> elbow -> carpus. Hind femur slopes forward, hock bends back.
 link('Foreleg',(s*.145,-.23,.59),(s*.145,-.26,.30),.088,.055)
 link('Fore pastern',(s*.145,-.26,.30),(s*.145,-.27,.09),.055,.044)
 oval('Front paw',(s*.145,-.303,.055),(.065,.095,.055))
 oval('Haunch',(s*.15,.39,.49),(.115,.14,.19))
 link('Thigh',(s*.15,.39,.46),(s*.16,.29,.30),.09,.062)
 link('Hock',(s*.16,.29,.30),(s*.16,.46,.17),.062,.042)
 link('Hind pastern',(s*.16,.46,.17),(s*.16,.43,.065),.043,.039)
 oval('Rear paw',(s*.16,.391,.047),(.061,.087,.047))
 # Rounded triangular pinna constructed as a tapered loft, not a cone.
 v=[];f=[]
 rings=[(.0,.095,.067),(.045,.09,.052),(.115,.060,.031),(.175,.025,.014),(.192,.004,.004)]
 for z,w,d in rings:
  for j in range(20):
   a=j*math.tau/20;v.append((s*(.12+z*.20)+w*math.cos(a),-.384+d*math.sin(a)+z*.09,1.025+z))
 for k in range(len(rings)-1):
  for j in range(20):f.append((k*20+j,k*20+(j+1)%20,(k+1)*20+(j+1)%20,(k+1)*20+j))
 f.append(tuple(reversed(range(20))));f.append(tuple(range(80,100)))
 me=bpy.data.meshes.new('Pinna loft');me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new('Rounded ear',me);bpy.context.collection.objects.link(ob);parts.append(ob)
# Big descending brush, gentle lateral curl; all tail sections fused into core.
for i in range(17):
 t=i/16;y=.52+t*.63;z=.60-.31*t; x=.19*math.sin(t*2.1)
 r=.065+.17*math.sin(math.pi*t)**.72
 oval('Tail brush', (x,y,z),(r*.88,r*1.1,r))
# Merge and voxel-union: eliminate primitive intersections before assessment.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();body=bpy.context.object;body.name='FOX continuous anatomical clay'
r=body.modifiers.new('Fused sculpt volumes','REMESH');r.mode='VOXEL';r.voxel_size=.008;r.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=r.name)
s=body.modifiers.new('Organic junction relaxation','SMOOTH');s.factor=1.25;s.iterations=7;bpy.ops.object.modifier_apply(modifier=s.name)
for p in body.data.polygons:p.use_smooth=True
# Features remain separable for future facial retopology.
features=[]
for sign in [-1,1]:
 o=oval('Eye', (sign*.133,-.540,.943),(.035,.024,.030),features,dark)
 # Dark inset pinna is intentionally absent in clay pass: inspect ear form first.
oval('Nose',(0,-.722,.868),(.045,.027,.027),features,dark)
asset=[body]+features
# Zero ground contact, fixed origin, meters, no hidden proxy.
for o in asset:
 bpy.context.view_layer.objects.active=o;o.select_set(True)
bpy.context.scene.unit_settings.system='METRIC'
bpy.context.scene.unit_settings.scale_length=1
# Preserve raw editable mesh and unapplied sculpt subdivision.
sub=body.modifiers.new('Sculpt continuation','SUBSURF');sub.levels=1;sub.render_levels=1
bpy.ops.object.select_all(action='DESELECT')
for o in asset:o.select_set(True)
bpy.context.view_layer.objects.active=body
bpy.ops.export_scene.gltf(filepath=str(OUT/'fox-clay-test.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
# Studio outside export selection.
ground=mat('Studio ground',(.13,.16,.19))
bpy.ops.mesh.primitive_plane_add(size=200);bpy.context.object.data.materials.append(ground);bpy.context.object.location.z=-.007
sc=bpy.context.scene;sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.38,.43,.5,1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value=.4
for pos,power,size,col in [((-3,-4,5),450,4,(1,.89,.78)),((3,-1,3),300,3,(.72,.84,1)),((1,4,4),500,3,(1,.93,.85))]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=col;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;sc.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=2.05
sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=24;sc.cycles.use_denoising=True
sc.render.resolution_x=1000;sc.render.resolution_y=900;sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'fox-character-study.blend'),compress=True)
views={'front':(0,-4,1.3),'side':(4,0,1.3),'rear':(0,4,1.3),'three-quarter':(3,-4,2.0),'gameplay':(2.8,4.5,2.8)}
for name,pos in views.items():
 cam.location=pos;target=Vector((0,.12,.59));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=5.5 if name=='gameplay' else 2.05
 sc.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
metrics={'blender':bpy.app.version_string,'stage':'neutral anatomical form gate; no premium material pass','units':'meters','forward_blender':'-Y','forward_gltf':'-Z','height_m':max((body.matrix_world@Vector(v)).z for v in body.bound_box),'body_vertices':len(body.data.vertices),'body_polygons':len(body.data.polygons),'rigged':False,'views':list(views),'art_verdict':'PENDING_VISUAL_REVIEW'}
(OUT/'metrics.json').write_text(json.dumps(metrics,indent=2))
# Reimport test GLB separately to prove parser, dimensions and absence of armatures.
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'fox-clay-test.glb'))
report={'imported_meshes':sum(o.type=='MESH' for o in bpy.context.scene.objects),'armatures':sum(o.type=='ARMATURE' for o in bpy.context.scene.objects),'animations':len(bpy.data.actions),'bounds':{o.name:list(o.dimensions) for o in bpy.context.scene.objects if o.type=='MESH'}}
(OUT/'glb-roundtrip.json').write_text(json.dumps(report,indent=2))
