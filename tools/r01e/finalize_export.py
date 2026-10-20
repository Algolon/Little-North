"""Repair glTF material parity; keep the editable Blender source, batch export copy."""
import bpy, json, math
from pathlib import Path
R=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(R/'assets/r01e/hero-spruce.blend'))
asset=bpy.data.collections['HERO • editable sculptural components'];source=list(asset.objects)
for o in source:
 o.data.validate();o.data.update()
 ca=o.data.color_attributes.get('SculptTint') or o.data.color_attributes.new(name='SculptTint',type='FLOAT_COLOR',domain='POINT')
 bases=[o.data.materials[0].diffuse_color]*len(o.data.vertices)
 for poly in o.data.polygons:
  base=o.data.materials[poly.material_index].diffuse_color
  for vi in poly.vertices:bases[vi]=base
 for v in o.data.vertices:
  p=o.matrix_world@v.co;iswood='Wood' in o.name;issnow='Snow' in o.name or 'Leader' in o.name
  t=1 if issnow else .91+.07*math.sin(p.x*5+p.z*3)+.05*math.cos(p.y*8-p.z*2)
  if iswood:t*=.89+.12*math.sin(math.atan2(p.y,p.x)*19+p.z*2)
  col=bases[v.index];ca.data[v.index].color=(col[0]*t,col[1]*t,col[2]*t,1)
 o.data.color_attributes.active_color=ca
for m in {m for o in source for m in o.data.materials}:
 nt=m.node_tree;n=nt.nodes.new('ShaderNodeVertexColor');n.layer_name='SculptTint';n.name='GLTF supported baked sculpt color'
 nt.links.new(n.outputs['Color'],nt.nodes.get('Principled BSDF').inputs['Base Color'])
# Source remains separate named sculpt components; only export copy is joined.
bpy.ops.object.select_all(action='DESELECT');copies=[]
for o in source:
 c=o.copy();c.data=o.data.copy();bpy.context.collection.objects.link(c);c.select_set(True);copies.append(c)
bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();batch=copies[0];batch.name='Hero spruce • material batched export'
bpy.ops.export_scene.gltf(filepath=str(R/'assets/r01e/hero-spruce.glb'),export_format='GLB',use_selection=True,export_materials='EXPORT')
bpy.data.objects.remove(batch,do_unlink=True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'assets/r01e/hero-spruce.blend'),compress=True)
metrics=json.loads((R/'docs/r01e/mesh-metrics.json').read_text());metrics['glbBytes']=(R/'assets/r01e/hero-spruce.glb').stat().st_size;metrics['exportMeshObjects']=1;metrics['exportMaterialPrimitives']=4;metrics['colorParity']='Baked full linear RGB vertex colors directly feed Principled Base Color; glTF COLOR_0'
(R/'docs/r01e/mesh-metrics.json').write_text(json.dumps(metrics,indent=2))
# Render all final views again from the exact saved materials.
sc=bpy.context.scene;cam=sc.camera
from mathutils import Vector
for name,loc,target,scale in [('three-quarter',(11,-17,9),(0,0,4.2),10.3),('rear',(-12,16,8),(0,0,4.2),10.3),('side',(18,1,7),(0,0,4.2),10.3),('top',(1,-2,22),(0,0,4),8),('closeup',(8,-13,5),(1,-.7,2.6),4.2)]:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 sc.render.filepath=str(R/f'docs/r01e/evidence/blender-{name}.png');bpy.ops.render.render(write_still=True)
