// LN-A01a: deterministic, engine-independent third-person movement.
// All units are world metres; fox mesh faces local -Z. No THREE dependency.
export const MOTION = Object.freeze({
  walk: 3.8, run: 6.1, acceleration: 22, braking: 25, airAcceleration: 5.5,
  jumpSpeed: 5.25, gravity: 14, coyote: .11, jumpBuffer: .12,
  radius: .36, turnSpeed: 11, maxSlope: 1.10, minBound: -32.4, maxBound: 32.4,
});
const clamp=(v,lo,hi)=>Math.min(hi,Math.max(lo,v));
const hypot=(x,z)=>Math.hypot(x,z);
const shortest=(a,b)=>Math.atan2(Math.sin(b-a),Math.cos(b-a));

export function createMovementState(x,z,heightAt){
  return {x,y:heightAt(x,z)+.08,z,vx:0,vz:0,vy:0,grounded:true,
    heading:0, coyote:MOTION.coyote,jumpBuffer:0,jumpCount:0,landings:0, distance:0};
}
function resolveCircle(x,z,o){
  const dx=x-o.x,dz=z-o.z,r=MOTION.radius+o.radius,dist=hypot(dx,dz);
  if(dist>=r)return {x,z,hit:false};
  const scale=r/Math.max(.0001,dist);
  return {x:o.x+(dist<.0001?r:dx*scale),z:o.z+(dist<.0001?0:dz*scale),hit:true};
}
function resolveBox(x,z,o){
  const a=-(o.rotation||0),c=Math.cos(a),s=Math.sin(a),dx=x-o.x,dz=z-o.z;
  let lx=c*dx-s*dz,lz=s*dx+c*dz;
  const hx=o.halfX,hz=o.halfZ,r=MOTION.radius;
  const px=clamp(lx,-hx,hx),pz=clamp(lz,-hz,hz);
  const ox=lx-px,oz=lz-pz,d=hypot(ox,oz);
  if(d>=r)return {x,z,hit:false};
  if(d>.00001){lx=px+ox/d*r;lz=pz+oz/d*r;}
  else { // Box interior: leave by shortest route, accounting for player radius.
    const dl=hx+lx,dr=hx-lx,db=hz+lz,df=hz-lz;
    const nearest=Math.min(dl,dr,db,df);
    if(nearest===dl)lx=-hx-r;
    else if(nearest===dr)lx=hx+r;
    else if(nearest===db)lz=-hz-r;
    else lz=hz+r;
  }
  const inv=Math.cos(-a),ins=Math.sin(-a);
  return {x:o.x+inv*lx-ins*lz,z:o.z+ins*lx+inv*lz,hit:true};
}
function applyObstacles(x,z,objects=[]){
  let hit=false;
  for(const o of objects){
    const res=o.type==='box'?resolveBox(x,z,o):resolveCircle(x,z,o);
    x=res.x;z=res.z;hit ||= res.hit;
  }
  return {x,z,hit};
}
function moveAlongAxes(s,dx,dz,heightAt,obstacles){
  const prevGround=heightAt(s.x,s.z);
  function trial(nx,nz){
    nx=clamp(nx,MOTION.minBound,MOTION.maxBound);
    nz=clamp(nz,MOTION.minBound,MOTION.maxBound);
    const r=applyObstacles(nx,nz,obstacles);
    const diff=hypot(r.x-s.x,r.z-s.z);
    const heightDiff=heightAt(r.x,r.z)-heightAt(s.x,s.z);
    if(s.grounded && diff>.0001 && heightDiff > diff*MOTION.maxSlope+.05)return {x:s.x,z:s.z,hit:true};
    return {x:r.x,z:r.z,hit:r.hit};
  }
  const a=trial(s.x+dx,s.z);s.x=a.x;
  const b=trial(s.x,s.z+dz);s.z=b.z;
  if(a.hit)s.vx=0;if(b.hit)s.vz=0;
  if(s.grounded){const floor=heightAt(s.x,s.z)+.08;
    if(Math.abs(floor-s.y)<.4 || floor>s.y)s.y=floor;
  }
  s.distance+=hypot(dx,dz);
  return prevGround;
}
/** Advance by a single frame; subdivided for consistent jumps on slow devices.
 * input = {forward:-1..1,right:-1..1,yaw:radians,run:boolean,jumpPressed:boolean}
 */
export function advanceMovement(state,input,frameDt,heightAt,obstacles=[]){
  const dt=clamp(Number.isFinite(frameDt)?frameDt:0,0,.05);
  if(dt<=0)return state;
  const n=Math.ceil(dt/(1/60)),h=dt/n;
  for(let i=0;i<n;i++){
    const s=state;
    let f=clamp(input.forward||0,-1,1),right=clamp(input.right||0,-1,1);
    const stick=hypot(f,right);
    if(stick>1){f/=stick;right/=stick;}
    if(stick<.085){f=right=0;}
    const yaw=input.yaw||0;
    const sin=Math.sin(yaw),cos=Math.cos(yaw);
    const vx=(sin*f+cos*right)*(input.run?MOTION.run:MOTION.walk);
    const vz=(-cos*f+sin*right)*(input.run?MOTION.run:MOTION.walk);
    const diffX=vx-s.vx,diffZ=vz-s.vz,diffLength=hypot(diffX,diffZ);
    const accel=s.grounded?(stick>.085?MOTION.acceleration:MOTION.braking):MOTION.airAcceleration;
    const amount=Math.min(diffLength,accel*h);
    if(diffLength>.000001){s.vx+=diffX/diffLength*amount;s.vz+=diffZ/diffLength*amount;}
    if(Math.abs(s.vx)<.002)s.vx=0;
    if(Math.abs(s.vz)<.002)s.vz=0;
    s.coyote=s.grounded?MOTION.coyote:Math.max(0,s.coyote-h);
    s.jumpBuffer=Math.max(0,s.jumpBuffer-h);
    if(i===0 && input.jumpPressed)s.jumpBuffer=MOTION.jumpBuffer;
    if(s.jumpBuffer>0 && s.coyote>0){
      s.vy=MOTION.jumpSpeed;s.grounded=false;s.coyote=0;s.jumpBuffer=0;s.jumpCount++;
    }
    moveAlongAxes(s,s.vx*h,s.vz*h,heightAt,obstacles);
    if(!s.grounded || s.vy>0){
      s.vy-=MOTION.gravity*h;s.y+=s.vy*h;
      const floor=heightAt(s.x,s.z)+.08;
      if(s.y<=floor && s.vy<=0){
        s.y=floor;s.vy=0;s.grounded=true;s.landings++;
      }
    }else{
      s.y=heightAt(s.x,s.z)+.08;
    }
    const moveSpeed=hypot(s.vx,s.vz);
    if(moveSpeed>.12){
      const goal=Math.atan2(s.vx,-s.vz);
      s.heading+=clamp(shortest(s.heading,goal),-MOTION.turnSpeed*h,MOTION.turnSpeed*h);
    }
  }
  return state;
}
export const horizontalSpeed=s=>hypot(s.vx,s.vz);
