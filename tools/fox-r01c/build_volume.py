"""Generate a new whole-fox sculpt surface, independent of R01a/R01b meshes.
Smooth signed-distance volumes, localized form carving, marching cubes.
Run with system Python + numpy/scikit-image. Blender imports the resulting mesh.
"""
import numpy as np,json
from skimage.measure import marching_cubes
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/fox-r01c';OUT.mkdir(parents=True,exist_ok=True)
STEP=.0045
lo=np.array([-.39,-.79,-.02],dtype=np.float32);hi=np.array([.43,1.18,1.25],dtype=np.float32)
axes=[np.arange(a,b+STEP,STEP,dtype=np.float32) for a,b in zip(lo,hi)]
X,Y,Z=axes[0][:,None,None],axes[1][None,:,None],axes[2][None,None,:]
shape=tuple(len(a) for a in axes);D=np.full(shape,10,dtype=np.float32);operations=[]
def smin(a,b,k):
 h=np.clip(.5+.5*(b-a)/k,0,1);return b*(1-h)+a*h-k*h*(1-h)
def add(d,k,label,params):
 global D
 D=smin(D,d,k).astype(np.float32);operations.append({'kind':label,**params,'blend_m':k})
def ell(label,c,r,k=.025):
 q0=(X-c[0])/r[0];q1=(Y-c[1])/r[1];q2=(Z-c[2])/r[2]
 n=np.sqrt(q0*q0+q1*q1+q2*q2)
 grad=np.sqrt((q0/r[0])**2+(q1/r[1])**2+(q2/r[2])**2)
 d=n*(n-1)/np.maximum(grad,1e-6)
 add(d,k,label,{'center':c,'radii':r})
def capsule(label,a,b,r0,r1,k=.018):
 ab=np.array(b)-np.array(a);L=np.dot(ab,ab)
 t=np.clip(((X-a[0])*ab[0]+(Y-a[1])*ab[1]+(Z-a[2])*ab[2])/L,0,1)
 d=np.sqrt((X-a[0]-t*ab[0])**2+(Y-a[1]-t*ab[1])**2+(Z-a[2]-t*ab[2])**2)-(r0+(r1-r0)*t)
 add(d,k,label,{'from':a,'to':b,'r0':r0,'r1':r1})
# Winter-coat envelope: curved back, compact ribs, gently tucked loin.
ell('Ribcage',(0,.015,.535),(.210,.274,.208),.050)
ell('Loin',(0,.205,.540),(.174,.19,.174),.050)
ell('Croup',(0,.303,.522),(.185,.165,.180),.050)
ell('Shoulder coat',(0,-.17,.59),(.190,.158,.202),.050)
capsule('Rising neck',(0,-.18,.625),(0,-.327,.807),.151,.125,.045)
ell('Breast coat',(0,-.247,.535),(.150,.140,.180),.035)
# Rounded skull has MORE vertical than lateral extent; no broad cheek bags.
ell('Rounded cranium',(0,-.392,.892),(.155,.140,.155),.030)
ell('Forehead bridge',(0,-.462,.905),(.108,.079,.103),.026)
# Single tapered muzzle field: wider at the root and compact at the nose.
t=np.clip((Y+.640)/.135,0,1);ease=t*t*(3-2*t)
rx=.027+.058*ease;rz=.026+.033*ease;cz=.812+.012*ease
outside=np.maximum(-.640-Y,0)+np.maximum(Y+.505,0)
d=(np.sqrt((X/rx)**2+((Z-cz)/rz)**2+(outside/.027)**2)-1)*np.minimum(rx,rz)
add(d,.018,'Tapered muzzle wedge',{'nose_y':-.640,'root_y':-.505,'rx_tip':.027,'rx_root':.085})
ell('Lower jaw',(0,-.520,.778),(.068,.093,.039),.018)
for s in [-1,1]:
 ell('Small muzzle pad',(s*.034,-.556,.803),(.034,.043,.028),.013)
 ell('Cheek plane',(s*.091,-.363,.850),(.067,.110,.071),.027)
 # Compact upright pinnae: smoothly blended rounded triangular volumes.
 ell('Ear base',(s*.110,-.369,1.015),(.068,.045,.068),.014)
 ell('Ear taper',(s*.124,-.359,1.066),(.043,.032,.044),.010)
 ell('Rounded ear tip',(s*.132,-.352,1.103),(.016,.017,.019),.007)
 # Forelegs supported under shoulders, with small asymmetry in stance.
 fy=-.205+(.020 if s==-1 else 0)
 capsule('Fore upper',(s*.121,fy,.525),(s*.122,fy-.010,.323),.063,.044,.024)
 capsule('Fore pastern',(s*.122,fy-.010,.323),(s*.122,fy-.020,.087),.043,.032,.016)
 ell('Fore paw',(s*.122,fy-.048,.032),(.054,.078,.038),.014)
 # Fleshed thigh, forward knee, back hock; a real articulated quadruped profile.
 hy=.282+(.018 if s==-1 else 0)
 ell('Thigh',(s*.120,hy,.442),(.079,.106,.139),.028)
 capsule('Femur',(s*.120,hy,.440),(s*.128,hy-.092,.286),.070,.047,.022)
 capsule('Tibia',(s*.128,hy-.092,.286),(s*.130,hy+.036,.154),.046,.032,.014)
 capsule('Rear pastern',(s*.130,hy+.036,.154),(s*.130,hy+.010,.063),.032,.026,.012)
 ell('Rear paw',(s*.130,hy-.025,.030),(.050,.071,.036),.013)
# One continuous curved brush field: no capsule joints or segment swelling.
t=np.clip((Y-.415)/.66,0,1);ease=t*t*(3-2*t)
cx=.135*np.sin(math.pi*.90*t);cz=.535-.329*ease
radius=.055*(1-t)+.162*np.maximum(np.sin(math.pi*t),0)**.80+.006*t
outside=np.maximum(.415-Y,0)+np.maximum(Y-1.075,0)
d=np.sqrt(((X-cx)/.94)**2+(Z-cz)**2+outside**2)-radius
add(d,.018,'Continuous curved full brush',{'root_y':.415,'tip_y':1.075,'max_radius_approx':.193})
# Continuous sculpt fields: modest brow break and integrated cheek-to-neck sweep.
for s in [-1,1]:
 # Carve a shallow orbital plane, not a large drilled eye hole.
 w=np.exp(-(((X-s*.097)/.047)**2+((Y+.503)/.040)**2+((Z-.913)/.035)**2)*1.7)
 D+=.006*w.astype(np.float32)
# Flatten soles against the actual export ground plane, with a small softened edge.
D=-smin(-D,-(-Z),.003)
verts,faces,normals,values=marching_cubes(D,level=0,spacing=(STEP,STEP,STEP),allow_degenerate=False)
verts=(verts+lo).astype(np.float32)
np.savez_compressed(OUT/'whole-fox-sculpt-mesh.npz',vertices=verts,faces=faces.astype(np.int32))
meta={'method':'Smooth implicit whole-animal volume with local sculpt fields; new construction, no R01a/R01b mesh reuse','stage':'primary whole-character anatomy and silhouette gate','grid_step_m':STEP,'grid_shape':shape,'vertices':len(verts),'triangles':len(faces),'bounds_min':verts.min(axis=0).tolist(),'bounds_max':verts.max(axis=0).tolist(),'forms':operations,'head_targets':{'cranium_width':.310,'cranium_height':.310,'muzzle_length_envelope':.162,'note':'Construction envelopes, not accepted final measurements'},'correction_round':2,'art_verdict':'PENDING_VISUAL_REVIEW'}
(OUT/'construction.json').write_text(json.dumps(meta,indent=2));print(json.dumps({k:meta[k] for k in ['vertices','triangles','bounds_min','bounds_max']}))
