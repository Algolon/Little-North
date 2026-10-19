import * as THREE from 'three';
import {heightAt,makeWorld} from './world.js';
import {makeFox} from './fox.js';

const canvas=document.getElementById('scene');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.6));
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.14;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene();scene.background=new THREE.Color(0xbedde9);scene.fog=new THREE.FogExp2(0xb9d5e1,.019);
const camera=new THREE.PerspectiveCamera(56,window.innerWidth/window.innerHeight,.1,180);
const sky=new THREE.HemisphereLight(0xf3f8fa,0x608398,2.0);scene.add(sky);
const sun=new THREE.DirectionalLight(0xffe2c5,2.3);sun.position.set(-18,32,8);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-36;sun.shadow.camera.right=36;sun.shadow.camera.top=36;sun.shadow.camera.bottom=-36;
sun.shadow.camera.near=1;sun.shadow.camera.far=85;sun.shadow.bias=-.0002;sun.shadow.normalBias=.022;scene.add(sun);
const {hero,update,getStats}=makeWorld(scene);
const fox=makeFox();scene.add(fox);fox.position.set(-4,0,4);
const velocity=new THREE.Vector3();const dir=new THREE.Vector3();const targetCam=new THREE.Vector3();
let yaw=.08,pitch=.28, cameraDistance=8.6,vertical=0,onGround=true,elapsed=0,last=0,step=0;
const keyboard=new Set();let joyX=0,joyY=0,drag=false,lastX=0,lastY=0;
const instruct=document.querySelector('#instructions'),stats=document.querySelector('#stats'),jump=document.querySelector('#jump');
let showStats=false;
window.addEventListener('keydown',e=>{keyboard.add(e.code);if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();if(e.code==='KeyP'){showStats=!showStats;stats.hidden=!showStats;}});
window.addEventListener('keyup',e=>keyboard.delete(e.code));
const onJump=()=>{if(onGround){vertical=5.4;onGround=false;}};
jump?.addEventListener('pointerdown',e=>{e.preventDefault();onJump();});
renderer.domElement.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;drag=true;lastX=e.clientX;lastY=e.clientY;renderer.domElement.setPointerCapture(e.pointerId);});
renderer.domElement.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-lastX,dy=e.clientY-lastY;yaw-=dx*.004;pitch=THREE.MathUtils.clamp(pitch+dy*.0035,.08,.9);lastX=e.clientX;lastY=e.clientY;});
renderer.domElement.addEventListener('pointerup',()=>drag=false);
renderer.domElement.addEventListener('pointercancel',()=>drag=false);
renderer.domElement.addEventListener('wheel',e=>{cameraDistance=THREE.MathUtils.clamp(cameraDistance+Math.sign(e.deltaY)*.6,5.2,13);},{passive:true});
const joystick=document.querySelector('#joystick'),nub=document.querySelector('#joystick-nub');
let stickPointer=null;
function moveStick(e){const r=joystick.getBoundingClientRect();let dx=e.clientX-(r.left+r.width/2),dy=e.clientY-(r.top+r.height/2);const len=Math.max(1,Math.hypot(dx,dy));const scale=Math.min(len,38)/len;dx*=scale;dy*=scale;joyX=dx/38;joyY=-dy/38;nub.style.transform=`translate(${dx}px,${dy}px)`;}
joystick?.addEventListener('pointerdown',e=>{stickPointer=e.pointerId;joystick.setPointerCapture(e.pointerId);moveStick(e);});
joystick?.addEventListener('pointermove',e=>{if(e.pointerId===stickPointer)moveStick(e);});
const clearStick=()=>{stickPointer=null;joyX=joyY=0;nub.style.transform='translate(0,0)';};
joystick?.addEventListener('pointerup',clearStick);joystick?.addEventListener('pointercancel',clearStick);
const startPos=new THREE.Vector3(-4,0,4);
function tick(timeMs){
  requestAnimationFrame(tick);
  const now=timeMs*.001,dt=Math.min(.045,Math.max(0,now-last));last=now;elapsed+=dt;
  if(keyboard.has('Space')){keyboard.delete('Space');onJump();}
  const forward=Number(keyboard.has('KeyW')||keyboard.has('ArrowUp'))-Number(keyboard.has('KeyS')||keyboard.has('ArrowDown'))+joyY;
  const lateral=Number(keyboard.has('KeyD')||keyboard.has('ArrowRight'))-Number(keyboard.has('KeyA')||keyboard.has('ArrowLeft'))+joyX;
  dir.set(Math.sin(yaw)*forward+Math.cos(yaw)*lateral,0,-Math.cos(yaw)*forward+Math.sin(yaw)*lateral);
  const mag=Math.min(1,dir.length());if(mag>.01)dir.normalize();
  const running=keyboard.has('ShiftLeft')||keyboard.has('ShiftRight');const speed=running?6.4:4.2;
  const targetVelocity=dir.multiplyScalar(mag*speed);
  velocity.lerp(targetVelocity,Math.min(1,dt*(onGround?9:4)));
  fox.position.addScaledVector(velocity,dt);
  if(fox.position.length()>34){fox.position.x=THREE.MathUtils.clamp(fox.position.x,-33,33);fox.position.z=THREE.MathUtils.clamp(fox.position.z,-33,33);}
  vertical-=dt*13.0;fox.position.y+=vertical*dt;
  const floor=heightAt(fox.position.x,fox.position.z)+.08;
  if(fox.position.y<=floor){fox.position.y=floor;vertical=0;onGround=true;}else{onGround=false;}
  if(mag>.12){const theta=Math.atan2(velocity.x,-velocity.z);let diff=((theta-fox.rotation.y+Math.PI)%(Math.PI*2)+Math.PI*2)%(Math.PI*2)-Math.PI;fox.rotation.y+=diff*Math.min(1,dt*11);step+=dt;}
  fox.userData.animate(elapsed,velocity.length());
  const look=new THREE.Vector3(fox.position.x,fox.position.y+1.06,fox.position.z-.15);
  targetCam.set(look.x+Math.sin(yaw)*cameraDistance*Math.cos(pitch),look.y+cameraDistance*Math.sin(pitch),look.z+Math.cos(yaw)*cameraDistance*Math.cos(pitch));
  camera.position.lerp(targetCam,Math.min(1,dt*4.5));camera.lookAt(look);
  update(elapsed);
  if(showStats && Math.floor(now*2)!==Math.floor((now-dt)*2)){
    const s=getStats();stats.textContent=`Objects: ${s.drawables} · Triangles: ${s.triangles.toLocaleString()} · Hero tree: ${s.heroTriangles.toLocaleString()} tris · DPR ${renderer.getPixelRatio().toFixed(2)}`;
  }
  renderer.render(scene,camera);
}
fox.position.y=heightAt(startPos.x,startPos.z)+.08;
camera.position.set(-4,4.4,13);camera.lookAt(fox.position);
window.addEventListener('resize',()=>{camera.aspect=window.innerWidth/window.innerHeight;camera.updateProjectionMatrix();renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.6));renderer.setSize(window.innerWidth,window.innerHeight);});
document.getElementById('reset')?.addEventListener('click',()=>{fox.position.copy(startPos);fox.position.y=heightAt(startPos.x,startPos.z)+.08;velocity.set(0,0,0);vertical=0;});
const intro=document.getElementById('intro');
document.getElementById('begin')?.addEventListener('click',()=>{intro.hidden=true;instruct.classList.add('visible');setTimeout(()=>instruct.classList.remove('visible'),8000);});
document.getElementById('reference')?.addEventListener('click',()=>{window.location.href='sculpt.html';});
requestAnimationFrame(tick);
