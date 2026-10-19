import test from 'node:test';
import assert from 'node:assert/strict';
import {createMovementState,advanceMovement,horizontalSpeed,MOTION} from '../src/controller.js';
const flat=()=>0;
const tick=(s,input={},n=60,dt=1/60,height=flat,obstacles=[])=>{
  for(let i=0;i<n;i++)advanceMovement(s,{forward:0,right:0,yaw:0,run:false,jumpPressed:false,...input,jumpPressed:!!input.jumpPressed&&i===0},dt,height,obstacles);
};
test('forward is camera-relative and stop does not drift',()=>{
  const s=createMovementState(0,0,flat);
  tick(s,{forward:1},60);
  assert.ok(s.z< -3.1,`z=${s.z}`);
  assert.ok(Math.abs(s.x)<.01);
  tick(s,{},40);
  assert.ok(horizontalSpeed(s)<.01,`speed=${horizontalSpeed(s)}`);
});
// IMPORTANT: the orbit camera sits (+sin(yaw), +cos(yaw) from the fox.
 // So screen-up points (-sin(yaw), -cos(yaw), not +sin(yaw)).
test('camera-relative forward remains screen-up at every quarter orbit',()=>{
 const cases=[
  [0,0,-1],
  [Math.PI/2,-1,0],
  [Math.PI,0,1],
  [Math.PI*1.5,1,0],
 ];
 for(const [yaw,fx,fz] of cases){
  const s=createMovementState(0,0,flat);
  tick(s,{forward:1,yaw},60);
  const dot=s.x*fx+s.z*fz;
  const cross=Math.abs(s.x*fz-s.z*fx);
  assert.ok(dot>3.1,`yaw=${yaw}: forward movement reversed or too slow, dot=${dot}`);
  assert.ok(cross<.01,`yaw=${yaw}: off-axis drift =${cross}`);
 }
});
test('camera-relative right always moves toward screen-right at every orbit',()=>{
 for(const yaw of [0,Math.PI/2,Math.PI,Math.PI*1.5]){
  const s=createMovementState(0,0,flat);
  tick(s,{right:1,yaw},60);
  const rx=Math.cos(yaw),rz=-Math.sin(yaw);
  const dot=s.x*rx+s.z*rz;
  const cross=Math.abs(s.x*rz-s.z*rx);
  assert.ok(dot>3.1,`yaw=${yaw}: joystick right reversed, dot=${dot}`);
  assert.ok(cross<.01,`yaw=${yaw}: screen-right drift=${cross}`);
 }
});
test('moving forward while rotating view follows the new camera direction',()=>{
 const s=createMovementState(0,0,flat);
 tick(s,{forward:1,yaw:0},45);
 const before={x:s.x,z:s.z};
 tick(s,{forward:1,yaw:Math.PI/2},60);
 assert.ok(s.x<before.x-3,`yaw turn should travel toward -X, x=${s.x}`);
 assert.ok(Math.abs(s.heading-Math.PI/2)<.04,`fox heading=${s.heading}`);
});
test('jump is discrete, lands, cannot chain without new press',()=>{
  const s=createMovementState(0,0,flat);
  let apex=s.y;
  for(let i=0;i<135;i++){
    advanceMovement(s,{forward:0,right:0,yaw:0,jumpPressed:i===0},1/60,flat);
    apex=Math.max(apex,s.y);
  }
  assert.ok(apex>.75,`apex=${apex}`);
  assert.equal(s.jumpCount,1);
  assert.equal(s.grounded,true);
  assert.ok(Math.abs(s.y-.08)<.001);
  assert.equal(s.vy,0);
});
test('jump buffer triggers when landing, only once',()=>{
  const s=createMovementState(0,0,flat);
  s.y=1;s.vy=-2;s.grounded=false;s.coyote=0;
  let double=false;
  for(let i=0;i<90;i++){
    advanceMovement(s,{forward:0,right:0,yaw:0,jumpPressed:i===11},1/60,flat);
    if(s.jumpCount>1)double=true;
  }
  assert.equal(double,false);
  assert.ok(s.jumpCount<=1);
});
test('cabin box and spruce circle stop player without walking through',()=>{
  const s=createMovementState(-4,0,flat);
  tick(s,{forward:1},110,1/60,flat,[{type:'box',x:-4,z:-6,halfX:2,halfZ:1,rotation:0}]);
  assert.ok(s.z>=-6+1+.36-.01,`position=${s.z}`);
  const tree=createMovementState(0,2,flat);
  tick(tree,{forward:1},120,1/60,flat,[{type:'circle',x:0,z:0,radius:.7}]);
  assert.ok(tree.z>=1.06-.01,`tree collision z=${tree.z}`);
});
test('movement remains close at 30 vs 60 frames per second',()=>{
  const slow=createMovementState(0,0,flat),fast=createMovementState(0,0,flat);
  tick(slow,{forward:1},30,1/30);
  tick(fast,{forward:1},60,1/60);
  assert.ok(Math.abs(slow.z-fast.z)<.025,`delta=${slow.z-fast.z}`);
});
test('slopes follow terrain, bound prevents exiting world',()=>{
  const terrain=(x,z)=>.11*Math.sin(z*.5)+.12*Math.sin(x*.3);
  const s=createMovementState(0,0,terrain);
  tick(s,{forward:1,run:true},250,1/60,terrain);
  assert.ok(s.z>=MOTION.minBound-.0001);
  assert.ok(Math.abs(s.y-terrain(s.x,s.z)-.08)<.02);
});
test('no-input and zero dt do not create NaN or movement',()=>{
  const s=createMovementState(1,1,flat);
  advanceMovement(s,{},0,flat);
  tick(s,{},60);
  assert.equal(s.x,1);assert.equal(s.z,1);
  assert.ok(Object.values(s).every(v=>typeof v!=='number'||Number.isFinite(v)));
});


// The core bug in the owner's footage: the visual fox faced opposite travel.
// A three.js object with local -Z forward rotated by heading has travel
// (-sin(heading), -cos(heading)). Its facing dot movement must be positive.
test('mesh local -Z forward matches velocity on every cardinal and diagonal move',()=>{
 for(const yaw of [0,Math.PI/4,Math.PI/2,Math.PI,Math.PI*1.5]){
  for(const stick of [{forward:1,right:0},{forward:0,right:1},{forward:.7,right:.7}]){
   const st=createMovementState(0,0,flat);
   tick(st,{...stick,yaw},70);
   const speed=horizontalSpeed(st);
   const alignment=(-Math.sin(st.heading)*st.vx-Math.cos(st.heading)*st.vz)/speed;
   assert.ok(alignment>.995,`yaw=${yaw} stick=${JSON.stringify(stick)} facing alignment=${alignment}`);
  }
 }
});
test('explicit visible-camera vector overrides stale desired yaw',()=>{
 const st=createMovementState(0,0,flat);
 // Desired yaw still 0, but the rendered camera has already orbited right.
 tick(st,{forward:1,yaw:0,viewForwardX:-1,viewForwardZ:0},60);
 assert.ok(st.x < -3.1,`actual view forward should be -X, got x=${st.x}`);
 assert.ok(Math.abs(st.z)<.01);
 const face={x:-Math.sin(st.heading),z:-Math.cos(st.heading)};
 assert.ok(face.x<-.99,`visual fox should face -X, heading=${st.heading}`);
});
test('step duration on 10fps mobile frame covers real elapsed time',()=>{
 const slow=createMovementState(0,0,flat),fast=createMovementState(0,0,flat);
 tick(slow,{forward:1},10,.1);
 tick(fast,{forward:1},60,1/60);
 assert.ok(Math.abs(slow.z-fast.z)<.025,`10fps time loss=${slow.z-fast.z}`);
});
