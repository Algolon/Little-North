"""Import and preserve the new continuous sculpt; actual neutral Blender renders."""
import bpy,numpy as np,math,json,bmesh
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/fox-r01c'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
mesh=np.load(OUT/'whole-fox-sculpt-mesh.npz');me=bpy.data.meshes.new('Implicit whole-fox sculpt');me.from_pydata(mesh['vertices'].tolist(),[],mesh['faces'].tolist());me.update()
body=bpy.data.objects.new('FOX R01c new continuous whole-character sculpt',me);bpy.context.collection.objects.link(body)
def material(name,col,rough=.8):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*col,1);p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;return m
clay=material('Neutral ivory-grey sculpt',(.48,.49,.485));graphite=material('Temporary facial graphite',(.035,.041,.045),.55)
body.data.materials.append(clay)
for p in me.polygons:p.use_smooth=True
# Recalculate orientation of the marching surface, preserve the complete mesh.
bpy.context.view_layer.objects.active=body;body.select_set(True)
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
bvh=BVHTree.FromPolygons([v.co.copy() for v in me.vertices],[tuple(p.vertices) for p in me.polygons])
features=[]
def oval(name,loc,scale,mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 features.append(o);return o
# Small temporary eye surfaces only; gaze and eyelid design remain unapproved.
for s in [-1,1]:
 h,n,idx,d=bvh.ray_cast(Vector((s*.094,-1.5,.913)),Vector((0,1,0)),3)
 if h is None:raise RuntimeError('Eye surface sample missed')
 N=n.normalized();U=Vector((0,0,1)).cross(N).normalized();V=N.cross(U).normalized()
 ob=oval('Temporary inset eye '+str(s),h-N*.009,(.025,.018,.013),graphite)
 ob.rotation_euler=Matrix((U,V,N)).transposed().to_euler()
h,n,idx,d=bvh.ray_cast(Vector((0,-1.5,.825)),Vector((0,1,0)),3)
if h is None:raise RuntimeError('Nose sample missed')
oval('Nose marker',h+Vector((0,-.007,0)),(.027,.018,.021),graphite)
root=bpy.data.objects.new('FOX ground-origin export root -Z forward',None);bpy.context.collection.objects.link(root)
asset=[body]+features
for o in asset:o.parent=root
root.rotation_euler.z=math.pi
bpy.ops.object.select_all(action='DESELECT');root.select_set(True)
for o in asset:o.select_set(True)
bpy.context.view_layer.objects.active=body
bpy.ops.export_scene.gltf(filepath=str(OUT/'whole-fox-form-study.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
root.rotation_euler.z=0
# Neutral studio; cameras are far enough that orthographic rays start above floor.
bpy.ops.mesh.primitive_plane_add(size=200);floor=bpy.context.object;floor.name='Studio floor, excluded from export';floor.location.z=-.001;floor.data.materials.append(material('Studio grey',(.14,.17,.20)))
sc=bpy.context.scene;sc.world=bpy.data.worlds.new('Neutral studio');sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.34,.39,.46,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.38
for pos,power,size,col in [((-3,-4,5),450,4,(1,.91,.82)),((3,-1,3),260,3,(.77,.86,1)),((1,4,4),450,3,(1,.95,.88))]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=col;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;sc.camera=cam;cam.data.type='ORTHO'
sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=16;sc.cycles.use_denoising=True
sc.render.resolution_x=900;sc.render.resolution_y=900;sc.render.resolution_percentage=100;sc.view_settings.view_transform='AgX'
views={'three-quarter':((3,-4,2),(0,.13,.57),2.26),'front':((0,-4,1.3),(0,.13,.57),2.26),'side':((4,0,1.3),(0,.13,.57),2.26),'rear':((0,4,1.3),(0,.13,.57),2.26),'head-three-quarter':((3,-4,1.9),(0,-.405,.88),.75),'head-front':((0,-4,1.5),(0,-.405,.88),.75),'distance':((3,4,2.8),(0,.13,.57),5.3)}
def camera(name):
 pos,target,scale=views[name];target=Vector(target);cam.location=target+(Vector(pos)-target)*2.5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
camera('three-quarter');bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'whole-fox-sculpt-study.blend'),compress=True)
for name in views:
 camera(name);sc.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
camera('three-quarter');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'whole-fox-sculpt-study.blend'),compress=True)
(OUT/'render-metrics.json').write_text(json.dumps({'blender':bpy.app.version_string,'views':list(views),'method':'New smooth implicit whole-animal sculpt volume, imported as actual editable Blender mesh','facial_details':'Temporary eye/nose markers; no iris/pupil or finished eyelid design','stage':'Neutral whole-character primary forms','art_verdict':'PENDING_VISUAL_REVIEW','rigged':False,'premium_materials':False},indent=2))
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'whole-fox-form-study.glb'))
(OUT/'glb-roundtrip.json').write_text(json.dumps({'meshes':sum(o.type=='MESH' for o in bpy.context.scene.objects),'armatures':sum(o.type=='ARMATURE' for o in bpy.context.scene.objects),'animations':len(bpy.data.actions)},indent=2))
