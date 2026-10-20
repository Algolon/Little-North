"""Only run with real Blender 4.2+: import candidate GLB, save editable .blend,
render actual Cycles art-evidence. Never labels another renderer as Blender.
Run: blender -b -t 4 --python tools/r01d/render_blender.py
"""
import bpy, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
MODEL=ROOT/'public/models/ln-r01d-hero-bough.glb'
assert MODEL.exists(),MODEL
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(MODEL))
asset=[o for o in bpy.context.scene.objects if o.type=='MESH']
assert len(asset)>=4,'Missing imported bough geometry'
for ob in asset:
 for mat in ob.data.materials:
  mat.use_nodes=True
  bs=mat.node_tree.nodes.get('Principled BSDF')
  if bs:bs.inputs['Roughness'].default_value=.86
bbox=[ob.matrix_world@Vector(p) for ob in asset for p in ob.bound_box]
lo=Vector([min(p[i] for p in bbox) for i in range(3)])
hi=Vector([max(p[i] for p in bbox) for i in range(3)])
center=(lo+hi)/2
world=bpy.context.scene.world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.38,.45,.56,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.55
for label,power,size,pos,color in [('Key',1200,5,(-2,-4,6),(1,.88,.76)),('Fill',900,6,(5,-1,4),(.75,.85,1)),('Rim',1100,4,(1,6,5),(.87,.93,1))]:
 bpy.ops.object.light_add(type='AREA',location=pos);ob=bpy.context.object;ob.name=label;ob.data.energy=power;ob.data.shape='DISK';ob.data.size=size;ob.data.color=color;ob.rotation_euler=(center-ob.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';bpy.context.scene.camera=cam
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.device='CPU';scene.cycles.use_denoising=True
scene.render.resolution_x=1100;scene.render.resolution_y=820;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX'
blend=ROOT/'assets/r01d/hero-bough.blend';blend.parent.mkdir(parents=True,exist_ok=True)
views={'three-quarter':(Vector((5,-6,3)),4.5),'top':(Vector((1.65,0,7)),4.3),'side':(Vector((1.7,-7,.6)),4.5),'closeup':(Vector((2.6,-3.8,1)),2.5)}
out=ROOT/'docs/r01d/evidence';out.mkdir(parents=True,exist_ok=True)
for i,(name,(position,scale)) in enumerate(views.items()):
 cam.location=position;cam.data.ortho_scale=scale
 cam.rotation_euler=(center-position).to_track_quat('-Z','Y').to_euler()
 if i==0:bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
 scene.render.filepath=str(out/f'blender-{name}.png');bpy.ops.render.render(write_still=True)
print('LN_R01D_BLENDER_VIEWS',len(views),'blend',blend)
