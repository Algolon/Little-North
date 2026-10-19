import * as THREE from 'three';
import {heightAt,makeWorld} from './world.js';
import {makeFox} from './fox.js';
import {createMovementState,advanceMovement,horizontalSpeed} from './controller.js';

// LN-A01a: movement is independent from graphics; fox remains the A01 art proxy.
const canvas=document.getElementById('scene');
const mobileInput=window.matchMedia('(pointer:coarse)').matches;
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,mobileInput?1.2:1.6));
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.14;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene();scene.background=new THREE.Color(0xbedde9);scene.fog=new THREE.FogExp2(0xb9d5e1,.019);
const camera=new THREE.PerspectiveCamera(56,window.innerWidth/window.innerHeight,.1,180);
scene.add(new THREE.HemisphereLight(0xf3f8fa,0x608398,2.0));
const sun=new THREE.DirectionalLight(0xffe2c5,2.3);sun.position.set(-18,32,8);sun.castShadow=true;
sun.shadow.mapSize.set(mobileInput?1024:2048,mobileInput?1024:2048);sun.shadow.camera.left=-36;sun.shadow.camera.right=36;
sun.shadow.camera.top=36;sun.shadow.camera.bottom=-36;sun.shadow.camera.near=1;sun.shadow.camera.far=85;
sun.shadow.bias=-.0002;sun.shadow.normalBias=.022;scene.add(sun);
const {update,getStats}=makeWorld(scene);
const fox=makeFox();scene.add(fox);

// Cabin and hero tree are simple controller colliders, not physics simulation.
const obstacles=[
  {type:'box',x:-9.6,z:-14,halfX:3.08,halfZ:2.34,rotation:Math.PI-.22},
  {type:'circle',x:8.6,z:-9.7,radius:.62},
  {type:'circle',x:12.3,z:-15.8,radius:.53},
];
const portraitTouch=window.matchMedia('(pointer:coarse)').matches && window.innerWidth<700;
 // Portrait needs the fox closer and the camera lower; the old 8.6m/.28 setup
 // combined with unrestricted swipe pitch became a high overhead view.
 const initial={x:-4,z:4,yaw:.08,pitch:portraitTouch?.16:.25,distance:portraitTouch?6.6:8.6};
let state=createMovementState(initial.x,initial.z,heightAt);
let yaw=initial.yaw,pitch=initial.pitch,cameraDistance=initial.distance,elapsed=0,last=0;
let frameRate=60;
const cameraLook=new THREE.Vector3(),targetLook=new THREE.Vector3(),desiredCamera=new THREE.Vector3();
const viewForward=new THREE.Vector3();
const keys=new Set();
let joyX=0,joyY=0,orbitPointer=null,lastX=0,lastY=0;
let joystickPointer=null,jumpQueued=false,showStats=false,started=false;
let jumpApex=-Infinity;
const controlsDebug=new URLSearchParams(window.location.search).has('controls');
if(controlsDebug)stats.hidden=false;

const instructions=document.getElementById('instructions');
const stats=document.getElementById('stats'),jump=document.getElementById('jump');
const joystick=document.getElementById('joystick'),nub=document.getElementById('joystick-nub');
const intro=document.getElementById('intro');

const damp=(speed,dt)=>1-Math.exp(-speed*dt);
function setFoxPose(){
  fox.position.set(state.x,state.y,state.z);
  fox.rotation.y=state.heading;
}
function desiredCameraAt(){
  targetLook.set(state.x,state.y+.98,state.z);
  desiredCamera.set(
    targetLook.x+Math.sin(yaw)*cameraDistance*Math.cos(pitch),
    targetLook.y+cameraDistance*Math.sin(pitch),
    targetLook.z+Math.cos(yaw)*cameraDistance*Math.cos(pitch)
  );
  // Terrain must not hide the camera under snow when navigating a hillside.
  const dx=desiredCamera.x-targetLook.x,dy=desiredCamera.y-targetLook.y,dz=desiredCamera.z-targetLook.z;
  let permitted=1;
  for(let i=2;i<=12;i++){
    const t=i/12,x=targetLook.x+dx*t,z=targetLook.z+dz*t,y=targetLook.y+dy*t;
    if(y<heightAt(x,z)+.48){permitted=Math.max(.23,(i-1.8)/12);break;}
  }
  if(permitted<1)desiredCamera.lerp(targetLook,1-permitted);
  desiredCamera.y=Math.max(desiredCamera.y,heightAt(desiredCamera.x,desiredCamera.z)+.67);
}
function snapCamera(){
  setFoxPose();desiredCameraAt();cameraLook.copy(targetLook);
  camera.position.copy(desiredCamera);camera.lookAt(cameraLook);
}
function clearJoystick(){
  joystickPointer=null;joyX=joyY=0;
  if(nub)nub.style.transform='translate(0,0)';
}
function resetGame(){
  state=createMovementState(initial.x,initial.z,heightAt);
  yaw=initial.yaw;pitch=initial.pitch;cameraDistance=initial.distance;
  jumpQueued=false;keys.clear();clearJoystick();jumpApex=state.y;snapCamera();
}
resetGame();

window.addEventListener('keydown',e=>{
  if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();
  if(!started || e.repeat)return;
  if(e.code==='Space')jumpQueued=true;
  if(e.code==='KeyR')resetGame();
  if(e.code==='KeyP'){showStats=!showStats;stats.hidden=!showStats;}
  keys.add(e.code);
});
window.addEventListener('keyup',e=>keys.delete(e.code));
window.addEventListener('blur',()=>{keys.clear();jumpQueued=false;clearJoystick();orbitPointer=null;});
document.addEventListener('visibilitychange',()=>{if(document.hidden){keys.clear();jumpQueued=false;clearJoystick();}});

jump?.addEventListener('pointerdown',e=>{
  if(!started)return;e.preventDefault();jumpQueued=true;
});
canvas.addEventListener('pointerdown',e=>{
  if(!started || (e.pointerType==='mouse'&&e.button!==0) || orbitPointer!==null)return;
  orbitPointer=e.pointerId;lastX=e.clientX;lastY=e.clientY;
  canvas.setPointerCapture(e.pointerId);
});
canvas.addEventListener('pointermove',e=>{
  if(e.pointerId!==orbitPointer)return;
  yaw-=THREE.MathUtils.clamp(e.clientX-lastX,-65,65)*(portraitTouch?.0032:.0043);
  pitch=THREE.MathUtils.clamp(
    pitch+(e.clientY-lastY)*(portraitTouch?.0019:.0038),
    .07,portraitTouch?.43:.64
  );
  lastX=e.clientX;lastY=e.clientY;
});
const finishOrbit=e=>{if(e.pointerId===orbitPointer)orbitPointer=null;};
canvas.addEventListener('pointerup',finishOrbit);
canvas.addEventListener('pointercancel',finishOrbit);
canvas.addEventListener('lostpointercapture',finishOrbit);
canvas.addEventListener('wheel',e=>{
  if(!started)return;e.preventDefault();
  cameraDistance=THREE.MathUtils.clamp(cameraDistance+Math.sign(e.deltaY)*.55,5.1,12);
},{passive:false});

function moveStick(e){
  const r=joystick.getBoundingClientRect();
  let dx=e.clientX-(r.left+r.width*.5),dy=e.clientY-(r.top+r.height*.5);
  const length=Math.max(.0001,Math.hypot(dx,dy)),radius=44,scale=Math.min(length,radius)/length;
  dx*=scale;dy*=scale;
  // Small circular deadzone; radial normalization prevents diagonal speed boosts.
  const magnitude=Math.min(1,length/radius), strength=magnitude<.12?0:(magnitude-.12)/.88;
  joyX=(dx/Math.max(1,Math.hypot(dx,dy)))*strength;
  joyY=(-dy/Math.max(1,Math.hypot(dx,dy)))*strength;
  nub.style.transform=`translate(${dx}px,${dy}px)`;
}
joystick?.addEventListener('pointerdown',e=>{
  if(!started || joystickPointer!==null)return;
  e.preventDefault();joystickPointer=e.pointerId;
  joystick.setPointerCapture(e.pointerId);moveStick(e);
});
joystick?.addEventListener('pointermove',e=>{if(e.pointerId===joystickPointer)moveStick(e);});
joystick?.addEventListener('pointerup',e=>{if(e.pointerId===joystickPointer)clearJoystick();});
joystick?.addEventListener('pointercancel',e=>{if(e.pointerId===joystickPointer)clearJoystick();});
joystick?.addEventListener('lostpointercapture',e=>{if(e.pointerId===joystickPointer)clearJoystick();});

function tick(timeMs){
  requestAnimationFrame(tick);
  const now=timeMs*.001,dt=Math.min(.10,Math.max(0,last?now-last:1/60));last=now;
  frameRate=frameRate*.95 + (dt>0?1/dt:60)*.05;
  elapsed+=dt;
  if(started){
    const forward=Number(keys.has('KeyW')||keys.has('ArrowUp'))-
      Number(keys.has('KeyS')||keys.has('ArrowDown'))+joyY;
    const right=Number(keys.has('KeyD')||keys.has('ArrowRight'))-
      Number(keys.has('KeyA')||keys.has('ArrowLeft'))+joyX;
    // Derive walking axes from the ACTUAL camera pose, not its desired yaw.
    // This keeps movement aligned with the visible screen while the orbit camera eases.
    camera.getWorldDirection(viewForward);
    advanceMovement(state,{
      forward,right,yaw,viewForwardX:viewForward.x,viewForwardZ:viewForward.z,
      run:keys.has('ShiftLeft')||keys.has('ShiftRight'),jumpPressed:jumpQueued
    },dt,heightAt,obstacles);
    jumpQueued=false;
  }
  jumpApex=Math.max(jumpApex,state.y);
  setFoxPose();
  fox.userData.animate(elapsed,horizontalSpeed(state));
  desiredCameraAt();
  camera.position.lerp(desiredCamera,damp(8,dt));
  cameraLook.lerp(targetLook,damp(11,dt));
  camera.position.y=Math.max(camera.position.y,heightAt(camera.position.x,camera.position.z)+.65);
  camera.lookAt(cameraLook);
  update(elapsed);
  renderer.render(scene,camera);
  if((showStats || controlsDebug) && Math.floor(now*2)!==Math.floor((now-dt)*2)){
    const s=getStats();
    const speed=horizontalSpeed(state);
    const facing=speed>.15?(-Math.sin(fox.rotation.y)*state.vx-Math.cos(fox.rotation.y)*state.vz)/speed:1;
    stats.textContent=`FPS≈${frameRate.toFixed(0)} · calls ${renderer.info.render.calls} · tris ${renderer.info.render.triangles.toLocaleString()} · speed ${speed.toFixed(1)} · alignment ${facing.toFixed(2)} · stick (${joyX.toFixed(2)},${joyY.toFixed(2)}) · yaw ${yaw.toFixed(2)}`;
  }
}
window.addEventListener('resize',()=>{
  camera.aspect=window.innerWidth/window.innerHeight;camera.updateProjectionMatrix();
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,mobileInput?1.2:1.6));
  renderer.setSize(window.innerWidth,window.innerHeight);
});
document.getElementById('reset')?.addEventListener('click',resetGame);
if(portraitTouch)instructions.textContent='Move: left joystick · Look: swipe on the snow · HOP to jump';
document.getElementById('begin')?.addEventListener('click',()=>{
  intro.hidden=true;started=true;instructions.classList.add('visible');
  setTimeout(()=>instructions.classList.remove('visible'),8000);
});
document.getElementById('reference')?.addEventListener('click',()=>{window.location.href='sculpt.html';});

// QA-only browser probe: movement, jump, reset and camera tests can verify actual frames.
if(new URLSearchParams(window.location.search).has('qa')){
  window.__LN_A01A__={
    state:()=>({...state,apex:jumpApex,yaw,pitch,portraitTouch,cameraDistance,frameRate,visualHeading:fox.rotation.y,viewForwardX:viewForward.x,viewForwardZ:viewForward.z,cameraX:camera.position.x,cameraY:camera.position.y,
      cameraZ:camera.position.z,started,joyX,joyY}),
    reset:resetGame
  };
}
requestAnimationFrame(tick);
