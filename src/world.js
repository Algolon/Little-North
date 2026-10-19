import * as THREE from 'three';
import {rng, palette, createSnowSpruce, createRock} from './procedural.js';
import {makeCabin} from './cabin.js';

// A deterministic snowfield is shared by rendering, fox motion and scatter placement.
export function heightAt(x,z) {
  const slow = .34*Math.sin(x*.13+.6)*Math.cos(z*.12) + .20*Math.sin(x*.35+z*.15);
  const undulations = .16*Math.sin(x*.61)*Math.sin(z*.49) + .065*Math.cos(x*1.2+z*.8);
  const ridge = Math.max(0, Math.min(1,(-z-15)/19));
  return -.32+slow+undulations+ridge*ridge*5;
}
function material(color, options={}) {return new THREE.MeshStandardMaterial({color,roughness:.96,...options});}
function atGround(obj,x,z,offset=0){obj.position.set(x,heightAt(x,z)+offset,z);return obj;}

export function makeWorld(scene) {
  const world=new THREE.Group();scene.add(world);
  const iceBlue=new THREE.Color(0xa6cbd9);
  const snowWhite=new THREE.Color(0xecf4f4);
  const terrain=new THREE.PlaneGeometry(108,108,118,118);
  terrain.rotateX(-Math.PI/2);
  const p=terrain.getAttribute('position');const colors=[];
  for(let i=0;i<p.count;i++){
    const x=p.getX(i),z=p.getZ(i), h=heightAt(x,z);p.setY(i,h);
    const shade=Math.max(0,Math.min(1,.12+.13*Math.sin(x*.38+z*.29)+.08*Math.sin(x*.93-z*.73)+.10*h));
    const c=snowWhite.clone().lerp(iceBlue,shade);colors.push(c.r,c.g,c.b);
  }
  terrain.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));terrain.computeVertexNormals();
  const snowMaterial=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.96,metalness:0});
  const snow=new THREE.Mesh(terrain,snowMaterial);snow.name='heightfield-snow';snow.receiveShadow=true;world.add(snow);
  const ocean=new THREE.Mesh(new THREE.PlaneGeometry(190,190),material(0x588e9d,{metalness:.12,roughness:.4,transparent:true,opacity:.85}));
  ocean.rotation.x=-Math.PI/2;ocean.position.y=-1.2;ocean.receiveShadow=true;world.add(ocean);
  // Sculpted distant mountain shapes frame the vignette but do not form playable routes.
  const mountain=material(0x708d9e,{flatShading:true});const summit=material(0xe5edf0,{flatShading:true});
  [[-43,-33,20,22],[20,-38,23,29],[39,-31,16,19],[-16,-45,13,17],[9,-45,15,23]].forEach(([x,z,r,h],i)=>{
    const peak=new THREE.Mesh(new THREE.ConeGeometry(r,h,7,1),mountain);
    peak.position.set(x,h*.43-1.8,z);peak.rotation.y=i*.48;peak.receiveShadow=true;world.add(peak);
    const cap=new THREE.Mesh(new THREE.ConeGeometry(r*.46,h*.40,7),summit);
    cap.position.set(x,h*.81-1.8,z);cap.rotation.y=i*.48;world.add(cap);
  });
  const hero=createSnowSpruce({seed:19,height:9.6,hero:true});
  atGround(hero,8.6,-9.7,-.05);world.add(hero);
  const oak=createSnowSpruce({seed:123,height:7.4,hero:true});
  atGround(oak,12.3,-15.8,-.05);world.add(oak);
  const cabin=makeCabin();atGround(cabin,-9.6,-14,.16);cabin.rotation.y=-.22;world.add(cabin);
  const rand=rng(61);
  // Forest wraps the edge of the scene and forms an organic view corridor.
  const locations = [
    [-18,-21,6.9],[-15,-29,8.2],[-5,-30,7.0],[3,-26,9.4],[16,-26,7.5],
    [22,-12,9.2],[19,-3,6.3],[-19,-7,7.8],[-22,0,5.7],[-11,-28,5.4],
    [3,-19,5.2],[-3,-23,7.1],[-23,-24,8.2],[22,-22,7.3],
  ];
  locations.forEach(([x,z,height],i)=>{
    const tree=createSnowSpruce({seed:i*197+8,height:height*(.86+rand()*.26),snowy:true});
    atGround(tree,x,z,-.07);tree.rotation.y=rand()*Math.PI*2;world.add(tree);
  });
  const rocks=[[6,-5,2.6,1.4],[14,-10,2.0,1.4],[10,-16,3,2.4],[-1,-8,1.8,.8],[-13,-9,2.7,1.4],[-3,-23,3.4,2.2],[2,-18,1.6,.9],[13,-23,2.8,1.5],[22,-8,2.8,2.2]];
  rocks.forEach(([x,z,w,h],i)=>{let r=createRock({seed:i+9,width:w,height:h,depth:w*.8});atGround(r,x,z,h*.26);r.rotation.y=rand()*Math.PI;world.add(r);});
  const ice=new THREE.Mesh(new THREE.CircleGeometry(1,64),new THREE.MeshStandardMaterial({color:0x88bfd1,metalness:.13,roughness:.26,transparent:true,opacity:.78}));
  ice.rotation.x=-Math.PI/2;ice.scale.set(7.8,4.5,1);ice.position.set(-19,heightAt(-19,9)+.04,10);world.add(ice);
  // A light snowfall cue. Instancing avoids a draw call per flake.
  const particleGeo=new THREE.IcosahedronGeometry(.028,0);
  const snowflake=new THREE.InstancedMesh(particleGeo,new THREE.MeshBasicMaterial({color:0xeef6f8,transparent:true,opacity:.7,depthWrite:false}),120);
  snowflake.name='ambient-snowflakes';
  const dummy=new THREE.Object3D();const particleData=[];
  for(let i=0;i<120;i++)particleData.push({x:(rand()-.5)*40,z:(rand()-.5)*40,y:rand()*12,speed:.4+rand()*.55});
  world.add(snowflake);
  const update=(time)=>{
    cabin.userData.update(time);
    particleData.forEach((a,i)=>{let y=(a.y-time*a.speed)%12;if(y<0)y+=12;dummy.position.set(a.x+Math.sin(time*.4+i)*.22,y+heightAt(a.x,a.z),a.z);dummy.scale.setScalar(.7+i%3*.3);dummy.updateMatrix();snowflake.setMatrixAt(i,dummy.matrix);});
    snowflake.instanceMatrix.needsUpdate=true;
  };
  const getStats=()=>{let drawables=0,triangles=0; world.traverse(o=>{if(!o.isMesh&&!o.isInstancedMesh)return;drawables++;const g=o.geometry;const index=g.index;const n=index?index.count:g.attributes.position?.count||0;triangles+=n/3*(o.isInstancedMesh?o.count:1);});return{drawables,triangles:Math.round(triangles),heroTriangles:hero.userData.triangles};};
  return {world,hero,cabin,update,getStats};
}
