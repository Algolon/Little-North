"""Blender 4.2 mesh-first hero study. Run with blender -b -t 4 --python this_file.
No reference images are embedded. Coordinates are metres, Blender Z up.
"""
import bpy, math, random, json, os
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ROUND=2
r=random.Random(19031)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def material(name,color,rough):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough
 return m
bark=material('Warm carved cedar bark',(.24,.115,.058),.92)
pine=material('Deep glacial spruce',(.043,.155,.124),.88)
tips=material('Sage needle tips',(.125,.235,.123),.9)
snowmat=material('Porcelain snow',(.86,.93,.98),.8)
# Foliage uses two materials; wood and snow bring total to four.
verts=[[],[],[]]; faces=[[],[],[]]
def tube(points,radii,layer,sides=7):
 v=verts[layer];f=faces[layer];base=len(v)
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
  tangent.normalize();u=tangent.cross(Vector((0,0,1)))
  if u.length<.01:u=tangent.cross(Vector((0,1,0)))
  u.normalize();w=tangent.cross(u).normalized()
  for j in range(sides):
   a=2*math.pi*j/sides; q=Vector(p)+radii[i]*(1+.09*math.sin(j*4.1+i*.6))*(u*math.cos(a)+w*math.sin(a));v.append(tuple(q))
 for i in range(len(points)-1):
  for j in range(sides):
   a=base+i*sides+j;b=base+i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 f.append(tuple(base+j for j in reversed(range(sides))));f.append(tuple(base+(len(points)-1)*sides+j for j in range(sides)))
def needle(a,d,length,width,layer):
 # Small, curved, closed volumetric needle fingers, not broad branch sprays.
 d=Vector(d).normalized();a=Vector(a);u=d.cross(Vector((0,0,1)))
 if u.length<.001:u=Vector((1,0,0))
 u.normalize();w=d.cross(u).normalized();v=verts[layer];f=faces[layer];base=len(v);sides=6
 for k in range(5):
  t=k/4;profile=[.25,.82,1,.67,.12][k]
  center=a+d*length*t+Vector((0,0,-length*.27*t*t))
  for j in range(sides):
   ang=2*math.pi*j/sides
   v.append(tuple(center+u*math.cos(ang)*width*profile+w*math.sin(ang)*width*.48*profile))
 for k in range(4):
  for j in range(sides):
   p=base+k*sides+j;q=base+k*sides+(j+1)%sides;f.append((p,q,q+sides,p+sides))
 f.append(tuple(base+j for j in reversed(range(sides))));f.append(tuple(base+24+j for j in range(sides)))
def mesh(name,v,f,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 return ob
wood=[];snow=[]
def blob(c,scale,d=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=c);o=bpy.context.object;o.scale=scale
 if d is not None:o.rotation_euler=Vector(d).to_track_quat('X','Z').to_euler()
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);snow.append(o)
def trunk(z):return Vector((.10*math.sin(z*.66),.075*math.sin(z*.89),z))
tube([trunk(i*9.5/32) for i in range(33)],[.015+.30*(1-i/33)**1.2+.18*math.exp(-i*1.1) for i in range(33)],0,11)
for j in range(6):
 a=j*math.tau/6+r.uniform(-.3,.3);end=Vector((math.cos(a)*.85,math.sin(a)*.85,.025));tube([trunk(.65),end*.6+Vector((0,0,.13)),end],[.22,.14,.015],0,8)
# Golden-angle offsets and independently staggered heights avoid radial repeated tiers.
for bi in range(30):
 t=bi/29;z=1.5+t*7.65+r.uniform(-.12,.12);ang=bi*2.39996+r.uniform(-.27,.27)
 L=(3.25*(1-t)**.85+.16)*r.uniform(.83,1.12)
 direction=Vector((math.cos(ang),math.sin(ang),0));side=Vector((-math.sin(ang),math.cos(ang),0));origin=trunk(z)
 def path(u):return origin+direction*(L*u)+side*(.10*math.sin(u*3+bi)*u)+Vector((0,0,-L*(.23*u+.07*math.sin(math.pi*u))))
 pts=[path(i/9) for i in range(10)];tube(pts,[(.085*(1-t)+.016)*(1-i/10)**1.2+.006 for i in range(10)],0)
 # Paired featherlike secondary twigs connected to the main woody bough.
 twigpaths=[]
 for k in range(7):
  u=.22+k*.105
  for sign in [-1,1]:
   start=path(u);length=L*(.31*(1-u)+.11)*r.uniform(.85,1.15)
   d=(direction*.39+side*sign*.91+Vector((0,0,-.28-r.random()*.22))).normalized()
   def sub(v):return start+d*length*v+Vector((0,0,-.14*length*v*v))
   twigpaths.append((sub(0),sub(1),length,u))
   tube([sub(i/4) for i in range(5)],[.022*(1-i/4)+.004 for i in range(5)],0,6)
   # Several small fans along each twig, each with independent needles.
   for n in range(5):
    v=.13+n*.18;base=sub(v)
    for q in [-1,0,1]:
     nd=(d*.45+side*(q*.65+sign*.17)+Vector((0,0,-.45+r.random()*.20))).normalized()
     needle(base+side*r.uniform(-.035,.035),nd,r.uniform(.30,.46)*(1-.40*t),r.uniform(.050,.074)*(1-.22*t),1 if r.random()<.82 else 2)
 # Outer branch terminal is clothed with smaller trailing needles.
 for n in range(13):
  u=.22+n*.059
  for q in [-1,1]:needle(path(u),direction*.45+side*q*.35+Vector((0,0,-.8)),r.uniform(.29,.42)*(1-.35*t),.061,1)
 # Connected, conforming snow quilt: intersecting shapes are voxel-unioned,
 # smoothed and simplified into a single surface per bough.
 snow=[]
 for k in range(10):
  u=.14+k*.078;center=path(u)+Vector((0,0,.10+.035*math.sin(k*1.4+bi)))
  blob(center,(L*.074+.055,(L*.040+.05)*(1+.25*math.sin(k*1.8+bi)),(.12+.038*L)*(1+.15*math.cos(k))),direction)
 for start,end,length,u in twigpaths:
  if r.random()<.27:continue
  for v in [.18,.45,.73]:
   c=start.lerp(end,v)+Vector((0,0,.11-.085*v*v))
   blob(c,((.15+.025*L)*(1-.15*v),(.085+.014*L)*(1+.28*math.sin(u*31+bi)),.12+.025*L),end-start)
 bpy.ops.object.select_all(action='DESELECT')
 for o in snow:o.select_set(True)
 bpy.context.view_layer.objects.active=snow[0];bpy.ops.object.join();o=bpy.context.object;o.name=f'Snow quilt {bi:02d}'
 rem=o.modifiers.new('Unified conforming blanket','REMESH');rem.mode='VOXEL';rem.voxel_size=.068 if L>1 else .045;rem.use_smooth_shade=True
 bpy.ops.object.modifier_apply(modifier=rem.name)
 sm=o.modifiers.new('Soft snow lips','SMOOTH');sm.factor=1.1;sm.iterations=5;bpy.ops.object.modifier_apply(modifier=sm.name)
 dec=o.modifiers.new('Game mesh','DECIMATE');dec.ratio=.22;bpy.ops.object.modifier_apply(modifier=dec.name)
 o.data.materials.clear();o.data.materials.append(snowmat)
 for p in o.data.polygons:p.use_smooth=True
# Keep wood editable in mesh form; material batches merged only for export.
mesh('Connected trunk roots and bough skeleton',verts[0],faces[0],bark)
fol=mesh('Layered sculpted needle fingers',verts[1],faces[1],pine)
bpy.context.view_layer.objects.active=fol
dec=fol.modifiers.new('Preserve needle volume with fewer facets','DECIMATE');dec.ratio=.52;bpy.ops.object.modifier_apply(modifier=dec.name)
fol=mesh('Subtle sage needle accents',verts[2],faces[2],tips)
bpy.context.view_layer.objects.active=fol
dec=fol.modifiers.new('Needle simplification','DECIMATE');dec.ratio=.52;bpy.ops.object.modifier_apply(modifier=dec.name)
# Single top leader snow hood.
snow=[];blob(trunk(9.36),(.105,.105,.27));snow[0].data.materials.append(snowmat)
asset=[o for o in bpy.context.scene.objects if o.type=='MESH']
for o in asset:o.select_set(False)
# Export merges snow surfaces by material, preserving disconnected bough blankets.
for mat in [snowmat]:
 obs=[o for o in asset if o.data.materials and o.data.materials[0]==mat]
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();bpy.ops.object.select_all(action='DESELECT')
asset=[o for o in bpy.context.scene.objects if o.type=='MESH']
for o in asset:o.select_set(True)
bpy.context.view_layer.objects.active=asset[0]
bpy.ops.export_scene.gltf(filepath=str(ROOT/'public/models/ln-r01c-hero-spruce.glb'),export_format='GLB',use_selection=True,export_materials='EXPORT')
metrics={'blender':bpy.app.version_string,'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in asset),'materials':len(set(m.name for o in asset for m in o.data.materials)),'meshObjects':len(asset),'seed':19031,'correctionRound':ROUND,'perMeshTriangles':{o.name:sum(len(p.vertices)-2 for p in o.data.polygons) for o in asset}}
(ROOT/'docs/r01c/mesh-metrics.json').write_text(json.dumps(metrics,indent=2))
# Neutral photographic studio; saved source retains lights, cameras and mesh.
bpy.ops.mesh.primitive_plane_add(size=200);ground=bpy.context.object;ground.name='Studio ground (not exported)';ground.data.materials.append(material('Studio',(.25,.30,.38),.95));ground.location.z=-.045
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.27,.32,.42,1);world.node_tree.nodes['Background'].inputs[1].default_value=.6
for name,loc,power,size,color in [('Key',(-5,-7,13),1900,7,(1,.83,.64)),('Fill',(6,-2,8),1100,6,(.65,.82,1)),('Rim',(2,6,12),1800,5,(.78,.88,1))]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector((0,0,5))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;bpy.context.scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=11.1
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=16;sc.cycles.use_denoising=True;sc.render.resolution_x=820;sc.render.resolution_y=1000;sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX';sc.render.image_settings.file_format='PNG'
cam.location=(11.5,-15.1,9.2);cam.rotation_euler=(Vector((0,0,4.65))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/r01c/hero-spruce.blend'),compress=True)
views=[('front',0),('right',math.pi/2),('rear',math.pi),('left',3*math.pi/2),('three-quarter',.65),('close-up',.65),('gameplay-distance',.65)]
for name,a in views:
 target=Vector((0,0,4.65));cam.location=(math.sin(a)*19,-math.cos(a)*19,9.2);cam.data.ortho_scale=11.1
 if name=='close-up':target=Vector((.7,-.5,3.1));cam.data.ortho_scale=4.0
 if name=='gameplay-distance':cam.data.type='PERSP';cam.data.lens=40;cam.location=(math.sin(a)*29,-math.cos(a)*29,3.0)
 else:cam.data.type='ORTHO'
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(ROOT/f'docs/r01c/evidence/blender-{name}.png');bpy.ops.render.render(write_still=True)
print('LN_R01C_METRICS',metrics)
