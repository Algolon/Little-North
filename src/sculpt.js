import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {createSnowSpruce} from './procedural.js';

// Dedicated rendering studio for LN-R01c. No perspective cheating or billboards.
const canvas=document.querySelector('#scene');
const mobile=matchMedia('(pointer:coarse)').matches;
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(devicePixelRatio,mobile?1.25:1.8));
renderer.setSize(innerWidth,innerHeight);
renderer.info.autoReset=false;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.10;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;

const scene=new THREE.Scene();scene.background=new THREE.Color(0x98a9bc);
const camera=new THREE.PerspectiveCamera(37,innerWidth/innerHeight,.1,110);
scene.add(new THREE.HemisphereLight(0xdceefd,0x637885,2.25));
const sun=new THREE.DirectionalLight(0xffdeb5,2.45);sun.position.set(-7,13,9);
sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.left=-14;sun.shadow.camera.right=14;
sun.shadow.camera.top=16;sun.shadow.camera.bottom=-14;sun.shadow.camera.far=55;
sun.shadow.normalBias=.015;scene.add(sun);
const rim=new THREE.DirectionalLight(0xb4d9e4,1.10);rim.position.set(8,9,-7);scene.add(rim);
const params=new URLSearchParams(location.search);
const legacy=params.has('legacy');
const object=legacy?createSnowSpruce({seed:19,height:9.6,hero:true}):
  (await new GLTFLoader().loadAsync(import.meta.env.BASE_URL+'models/ln-r01c-hero-spruce.glb')).scene;
let geometryBytes=0,assetVertices=0;
let assetTriangles=0;const assetMaterials=new Set();let assetMeshes=0;
object.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;assetMeshes++;assetVertices+=o.geometry.attributes.position.count;for(const a of Object.values(o.geometry.attributes))geometryBytes+=a.array.byteLength;geometryBytes+=o.geometry.index?.array.byteLength||0;assetTriangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;for(const m of (Array.isArray(o.material)?o.material:[o.material]))assetMaterials.add(m);}});
object.userData.triangles=assetTriangles;
const bounds=new THREE.Box3().setFromObject(object);
window.__LN_SCULPT__={ready:true,triangles:assetTriangles,materials:assetMaterials.size,meshes:assetMeshes,vertices:assetVertices,geometryBytes,bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()},legacy};
scene.add(object);
const ground=new THREE.Mesh(new THREE.CylinderGeometry(5.7,5.85,.48,68),
  new THREE.MeshStandardMaterial({color:0xeaf0f0,roughness:.94}));
ground.position.y=-.32;ground.receiveShadow=true;scene.add(ground);
const plaque=document.getElementById('study-meta');
if(plaque)plaque.textContent=legacy?'Original procedural tree · comparison only':'LN-R01c · Blender mesh calibration · unapproved';
const stats=document.querySelector('#stats');
const focus=new THREE.Vector3(0,4.8,0);
const shotViews={
  '1':{angle:0,dist:22.6,elev:8.6,look:4.8},
  '2':{angle:Math.PI/2,dist:22.6,elev:8.6,look:4.8},
  '3':{angle:Math.PI,dist:22.6,elev:8.6,look:4.8},
  '4':{angle:Math.PI*1.5,dist:22.6,elev:8.6,look:4.8},
  '5':{angle:Math.PI*.22,dist:20,elev:9.3,look:4.8},
  '6':{angle:Math.PI*.24,dist:8.4,elev:6.0,look:5.2},
  '7':{angle:Math.PI*.12,dist:25,elev:7.7,look:4.7}
};
let view={...shotViews[5]},locked=false,active='5',qaDirty=true;
function select(key){view={...shotViews[key]};active=key;locked=true;qaDirty=true;}
window.addEventListener('keydown',e=>{
  if(shotViews[e.key])select(e.key);
  if(e.key==='0')locked=false;
  if(e.code==='KeyP'){stats.hidden=!stats.hidden;}
});
let pointer=null,previousX=0,previousY=0;
canvas.addEventListener('pointerdown',e=>{
  if(e.pointerType==='mouse'&&e.button!==0)return;
  qaDirty=true;pointer=e.pointerId;previousX=e.clientX;previousY=e.clientY;locked=true;
  canvas.setPointerCapture(pointer);
});
canvas.addEventListener('pointermove',e=>{
  if(pointer!==e.pointerId)return;
  qaDirty=true;view.angle-=(e.clientX-previousX)*.005;
  view.elev=THREE.MathUtils.clamp(view.elev+(e.clientY-previousY)*.017,2,17);
  previousX=e.clientX;previousY=e.clientY;
});
for(const ev of ['pointerup','pointercancel','lostpointercapture'])
  canvas.addEventListener(ev,e=>{if(e.pointerId===pointer)pointer=null;});
canvas.addEventListener('wheel',e=>{
  qaDirty=true;e.preventDefault();view.dist=THREE.MathUtils.clamp(view.dist+Math.sign(e.deltaY)*.9,6.5,35);
  locked=true;
},{passive:false});
let lastUpdate=0;
function render(ms){
  requestAnimationFrame(render);
  if(params.has('qa')&&!qaDirty)return;
  qaDirty=false;
  if(!locked)view.angle=ms*.00014;
  focus.y=view.look;
  camera.position.set(Math.sin(view.angle)*view.dist,view.elev,Math.cos(view.angle)*view.dist);
  camera.lookAt(focus);
  renderer.info.reset();
  renderer.render(scene,camera);
  if(params.has('qa')){
    window.__LN_SCULPT__.drawCalls=renderer.info.render.calls;
    window.__LN_SCULPT__.drawingBuffer=renderer.getDrawingBufferSize(new THREE.Vector2()).toArray();
    window.__LN_SCULPT__.pixelRatio=renderer.getPixelRatio();
    window.__LN_SCULPT__.renderedTriangles=renderer.info.render.triangles;
    const gl=renderer.getContext(),debug=gl.getExtension('WEBGL_debug_renderer_info');
    window.__LN_SCULPT__.webglRenderer=debug?gl.getParameter(debug.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER);
    document.body.dataset.lnRenderCalls=String(renderer.info.render.calls);
    document.body.dataset.lnRenderedTriangles=String(renderer.info.render.triangles);
  }
  if(ms-lastUpdate>800){lastUpdate=ms;
    if(!stats.hidden)stats.textContent=`LN-R01c · ${Math.round(object.userData.triangles).toLocaleString()} tris · ${renderer.info.render.calls} renderer calls · ${assetMaterials.size} materials · view ${active}`;
  }
}
select(params.get('angle')||'5');
requestAnimationFrame(render);
window.addEventListener('resize',()=>{
  qaDirty=true;camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();
  renderer.setPixelRatio(Math.min(devicePixelRatio,mobile?1.25:1.8));renderer.setSize(innerWidth,innerHeight);
});
