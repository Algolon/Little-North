"""R01e: Blender-native volume sculpt study. No R01c/d geometry reused.
Authored architecture + local cage deformation + voxel fusion + surface needle relief.
Script-assisted sculptural construction, NOT recorded manual brush sculpting.
"""
import bpy, math, random, json, sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2]; OUT=R/'docs/r01e/evidence'; rng=random.Random(7814)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene
asset=bpy.data.collections.new('HERO • editable sculptural components');sc.collection.children.link(asset)

def mat(name,col,rough=.88):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True
 b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*col,1);b.inputs['Roughness'].default_value=rough
 b.inputs['Specular IOR Level'].default_value=.22
 return m
woodmat=mat('01 • warm carved umber',(.19,.079,.032));pine=mat('02 • deep spruce',(.023,.105,.073));sage=mat('03 • muted jade tips',(.061,.176,.111));snowmat=mat('04 • warm white snow / cool shadows',(.82,.9,.95),.84)
def move(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 asset.objects.link(o);return o
def mesh(name,v,f,m):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);asset.objects.link(o);o.data.materials.append(m)
 for p in me.polygons:p.use_smooth=True
 return o
def apply(o,typ,name,**kw):
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new(name,typ)
 for k,v in kw.items():setattr(m,k,v)
 bpy.ops.object.modifier_apply(modifier=m.name)
def join(obs,name):
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=obs[0];o.name=name;return o
def fuse(obs,name,voxel,smooth=3):
 o=join(obs,name);apply(o,'REMESH','Sculpt • voxel union',mode='VOXEL',voxel_size=voxel,use_smooth_shade=True)
 apply(o,'SMOOTH','Sculpt • soften transitions',factor=.65,iterations=smooth)
 return o
def ellipsoid(c,s,name,m,angle=0):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=c);o=move(bpy.context.object);o.name=name
 # Broad non-axisymmetric cushion cage; local lobes and pinches avoid a stock sphere.
 for v in o.data.vertices:
  x,y,z=v.co;n=1+.065*math.sin(5*x+3*y)+.04*math.cos(7*y-2*z)
  v.co=Vector((x*s[0]*n,y*s[1]*(1+.075*math.sin(x*5)),z*s[2]*(1+.07*math.sin(y*6+x*2))))
 o.rotation_euler.z=angle;o.data.materials.append(m)
 for p in o.data.polygons:p.use_smooth=True
 return o
def tube(points,radii,name):
 v=[];f=[];N=14
 for i,p in enumerate(points):
  t=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();u=t.cross(Vector((0,1,0))).normalized();w=t.cross(u)
  for j in range(N):
   a=j*math.tau/N;rad=radii[i]*(1+.12*math.sin(j*3+i*.6)+.05*math.cos(j*5-i*.8))
   v.append(p+rad*(u*math.cos(a)+w*math.sin(a)))
 for i in range(len(points)-1):
  for j in range(N):
   a=i*N+j;b=i*N+(j+1)%N;f.append((a,b,b+N,a+N))
 f.append(tuple(reversed(range(N))));f.append(tuple((len(points)-1)*N+j for j in range(N)))
 return mesh(name,v,f,woodmat)
def stem(z):return Vector((.09*math.sin(z*.9)+.018*z,.07*math.sin(z*1.4),z))
wood=[tube([stem(i*8.8/40) for i in range(41)],[.035+.28*(1-i/41)**1.2+.17*math.exp(-i*.8) for i in range(41)],'Trunk control surface')]
for a,l in [(0,1.0),(1.1,.75),(2.7,.95),(4,.7),(5.3,.88)]:
 d=Vector((math.cos(a),math.sin(a),0));wood.append(tube([stem(.9),d*.23+Vector((0,0,.36)),d*l*.65+Vector((0,0,.12)),d*l+Vector((0,0,.045))],[.22,.22,.12,.015],'Buttress'))
# Explicit art-directed skeleton: height, bearing degrees, length, arch, breadth.
layout=[(1.55,-135,2.75,.25,1),(1.8,-25,3.05,.18,1.1),(2.12,95,2.8,.2,.95),(2.35,175,2.35,.1,.95),(2.85,-75,2.65,.22,1),(3.18,42,2.7,.14,.95),(3.58,140,2.25,.2,.9),(3.85,-165,2.2,.13,.9),(4.18,-38,2.3,.2,.85),(4.6,75,2.05,.15,.8),(4.94,-110,1.95,.16,.8),(5.28,170,1.8,.18,.75),(5.62,5,1.8,.12,.72),(6.04,112,1.45,.12,.65),(6.37,-65,1.38,.1,.62),(6.69,-175,1.15,.12,.58),(7.04,48,1.1,.12,.55),(7.34,155,.88,.1,.5),(7.65,-70,.78,.09,.47),(7.98,50,.59,.06,.4),(8.28,-170,.46,.06,.36),(8.54,-40,.29,.04,.3)]
allfol=[];allsnow=[];nv=[];nf=[];ni=[]
def needle(a,d,length,width,index):
 d=d.normalized();u=d.cross(Vector((0,0,1))).normalized();w=d.cross(u);base=len(nv)
 # Short true needle wedge with soft-ish 3D diamond section. No leaf/feather lobes.
 for p in [a-u*width,a+w*width*.5,a+u*width,a-w*width*.5,a+d*length]:nv.append(tuple(p))
 for f in [(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)]:nf.append(tuple(base+i for i in f));ni.append(index)
for bi,(z,deg,L,arch,breadth) in enumerate(layout):
 a=math.radians(deg);d=Vector((math.cos(a),math.sin(a),0));s=Vector((-d.y,d.x,0));root=stem(z)
 def path(t):return root+d*L*t+s*(.12*math.sin(t*4+bi)*t)+Vector((0,0,arch*math.sin(t*math.pi)-.37*L*t*t))
 wood.append(tube([path(i/12) for i in range(13)],[(.105*(L/3)+.025)*(1-i/13)**1.3+.009 for i in range(13)],'Bough arm'))
 cushions=[];snow=[]
 # Irregular compact overlapping fans spread laterally, never long hanging leaves.
 sites=[(.28,-.19,.62),(.43,.29,.72),(.6,-.34,.74),(.7,.22,.69),(.86,-.13,.58),(1.0,.03,.38)]
 if bi%3==0:sites.insert(3,(.54,.04,.8))
 for j,(t,off,vol) in enumerate(sites):
  size=(.22+.14*L)*vol; c=path(t)+s*off*breadth+Vector((0,0,-.035))
  yaw=a+(.3 if j%2 else -.28);sx=size*1.28;sy=size*(.72+.16*math.sin(bi+j));sz=size*.46
  cushions.append(ellipsoid(c,(sx,sy,sz),'Foliage sculpt cage',pine,yaw))
  # Overlapping relief ridges cut the edge into compact stepped needle clusters.
  for k in range(3):
   side=(k-1)*sy*.66;cc=c+d*(sx*.25)+s*side+Vector((0,0,-sz*.22))
   cushions.append(ellipsoid(cc,(sx*.79,sy*.43,sz*.7),'Layered foliage ridge',pine,yaw+side*.4))
  # Snow carried by the broad cushion; bases overlap and are voxel-fused per arm.
  if j!=1 or bi%4!=0:
   cc=c+Vector((0,0,sz*.72+.035));snow.append(ellipsoid(cc,(sx*.91,sy*.93,sz*.65+.065),'Snow support volume',snowmat,yaw))
   # Uneven gravity-rounded lip; attached to parent dome, not a detached ball.
   lip=cc+d*sx*.35+s*sy*(.58 if (bi+j)%2 else -.65)-Vector((0,0,sz*.23))
   snow.append(ellipsoid(lip,(sx*.47,sy*.47,sz*.72+.03),'Gravity lip',snowmat,yaw-.2))
  wood.append(tube([path(t*.8),c,c+d*sx*.75-Vector((0,0,.08))],[.026,.018,.004],'Secondary joint'))
  for k in range(95):
   theta=rng.random()*math.tau;rr=math.sqrt(rng.uniform(.3,1));xx=math.cos(theta)*sx*rr;yy=math.sin(theta)*sy*rr
   zz=sz*math.sqrt(max(0,1-rr*rr))*(1 if k%4==0 else -.38)
   pos=c+d*xx+s*yy+Vector((0,0,zz))
   direction=(d*(.35+xx/sx*.4)+s*(yy/sy*.85)+Vector((0,0,-.25+rng.random()*.22)))
   needle(pos,direction,rng.uniform(.07,.16)*(.6+L*.14),rng.uniform(.009,.017),1 if rng.random()<.24 else 0)
 o=fuse(cushions,f'Foliage {bi:02d} • compact layered sculpt',.042 if L>1.5 else .028,2)
 apply(o,'DECIMATE','Preserve sculpt silhouette',ratio=.65);allfol.append(o)
 o=fuse(snow,f'Snow {bi:02d} • continuous supported mantle',.039 if L>1.5 else .025,5)
 apply(o,'SUBSURF','Rounded snow silhouette',levels=1,render_levels=1)
 apply(o,'DECIMATE','Snow surface economy',ratio=.46);allsnow.append(o)
 print('SCULPT_BOUGH',bi,flush=True)
woodobj=fuse(wood,'Wood • fused trunk roots and branch junctions',.035,3)
# Sculpt longitudinal bark valleys directly into fused wood vertices.
for v in woodobj.data.vertices:
 p=woodobj.matrix_world@v.co;rr=math.hypot(p.x-stem(p.z).x,p.y-stem(p.z).y)
 if rr<.48 and p.z>.2:
  a=math.atan2(p.y-stem(p.z).y,p.x-stem(p.z).x);depth=.009*math.sin(a*15+p.z*2)+.004*math.sin(a*27-p.z*5)
  v.co.x+=math.cos(a)*depth;v.co.y+=math.sin(a)*depth
apply(woodobj,'DECIMATE','Wood surface economy',ratio=.48)
needles=mesh('Needle relief • short embedded tips',nv,nf,pine);needles.data.materials.append(sage)
for p,i in zip(needles.data.polygons,ni):p.material_index=i
# Vertex colors survive glTF; broad handcrafted tonal modulation, not shader-only detail.
for o in [woodobj]+allfol+[needles]:
 ca=o.data.color_attributes.new(name='SculptTint',type='FLOAT_COLOR',domain='POINT')
 for v in o.data.vertices:
  p=o.matrix_world@v.co;t=.91+.08*math.sin(p.x*5+p.z*3)+.05*math.cos(p.y*8-p.z*2)
  ca.data[v.index].color=(t,t,t,1)
 for m in o.data.materials:
  if m.use_nodes and not m.node_tree.nodes.get('Sculpt vertex color'):
   n=m.node_tree.nodes.new('ShaderNodeVertexColor');n.name='Sculpt vertex color';n.layer_name='SculptTint'
   mix=m.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[1].default_value=m.diffuse_color
   m.node_tree.links.new(n.outputs['Color'],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
top=ellipsoid(stem(8.72),(.082,.09,.20),'Leader soft snow',snowmat)
# Keep source components editable. A temporary export collection batches by material only.
source=list(asset.objects);bpy.ops.object.select_all(action='DESELECT')
for o in source:o.select_set(True)
bpy.context.view_layer.objects.active=source[0]
bpy.ops.export_scene.gltf(filepath=str(R/'assets/r01e/hero-spruce.glb'),export_format='GLB',use_selection=True,export_materials='EXPORT')
metrics={'blender':bpy.app.version_string,'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in source),'vertices':sum(len(o.data.vertices) for o in source),'meshObjects':len(source),'materials':4,'glbBytes':(R/'assets/r01e/hero-spruce.glb').stat().st_size,'method':'Blender native authored cage deformation / voxel sculpt fusion / embedded short needle relief; no manual brush strokes'}
(R/'docs/r01e/mesh-metrics.json').write_text(json.dumps(metrics,indent=2));print(metrics,flush=True)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.04));g=bpy.context.object;g.name='STUDIO • excluded from GLB';g.data.materials.append(mat('Studio blue grey',(.22,.275,.34)))
sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.30,.37,.46,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.5
for name,loc,power,size,color in [('Warm key',(-5,-8,12),1700,7,(1,.86,.71)),('Cool fill',(7,-1,8),1000,6,(.65,.81,1)),('Soft rim',(1,6,12),1900,5,(.77,.87,1))]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector((0,0,4.2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;sc.camera=cam;cam.data.type='ORTHO'
sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=24;sc.cycles.use_denoising=True
sc.render.resolution_x=850;sc.render.resolution_y=1050;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.view_settings.view_transform='AgX'
def pose(loc,target,scale):
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
pose((11,-17,9),(0,0,4.2),10.3)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'assets/r01e/hero-spruce.blend'),compress=True)
for name,loc,target,scale in [('three-quarter',(11,-17,9),(0,0,4.2),10.3),('rear',(-12,16,8),(0,0,4.2),10.3),('side',(18,1,7),(0,0,4.2),10.3),('top',(1,-2,22),(0,0,4),8),('closeup',(8,-13,5),(1,-.7,2.6),4.2)]:
 pose(loc,target,scale);sc.render.filepath=str(OUT/f'blender-{name}.png');bpy.ops.render.render(write_still=True)
