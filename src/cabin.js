import * as THREE from 'three';
import { palette, makeWoodPlank, createRock } from './procedural.js';
const mat=(color,roughness=1,other={})=>new THREE.MeshStandardMaterial({color,roughness,...other});
function box(parent,size,position,material,rotZ=0){const mesh=new THREE.Mesh(new THREE.BoxGeometry(...size),material);mesh.position.set(...position);mesh.rotation.z=rotZ;mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;}

export function makeCabin() {
  const house=new THREE.Group(); house.name='home-cove-cabin';
  const wall=mat(0x795644), timber=mat(0x594235), beam=mat(0x3f3a38), roof=mat(0x626f75),snow=mat(palette.snow,.86);
  const glass=mat(0xffca80,.3,{emissive:0xffa858,emissiveIntensity:1.9});
  box(house,[6,3.4,4.7],[0,1.85,0],wall);
  // Horizontal notched-log cladding, restrained enough not to become a noisy texture.
  for(let y=.38;y<3.45;y+=.34) {
    for(const z of [-2.35,2.35]) {
      const plank=makeWoodPlank(6.15,.17,.14,y%1>.5?0x83604b:0x6c4c3c);
      plank.position.set(0,y+.16,z);house.add(plank);
    }
  }
  for(const x of [-2.91,2.91]) for(const z of [-2.26,2.26]) box(house,[.26,3.6,.27],[x,1.82,z],beam);
  // Gable roof, one continuous upper apex and two coherent overlapping snow planes.
  const tilt=Math.atan2(2.15,3.6);
  const sideLength=Math.hypot(3.6,2.15);
  for(const s of [-1,1]) {
    const pane=box(house,[sideLength,.23,5.35],[s*1.70,4.35,0],roof,s*tilt);
    pane.rotation.z=-s*tilt;
    box(house,[sideLength+.11,.22,5.53],[s*1.70,4.52,0],snow,-s*tilt);
  }
  box(house,[.25,.3,5.55],[0,5.47,0],snow);
  // Front wall is -Z; carefully authored door and warm leaded-glass windows.
  box(house,[1.22,2.15,.12],[-.55,1.28,-2.42],mat(0x455c57));
  box(house,[1.40,.19,.18],[-.55,2.47,-2.48],beam);
  for(const x of [-1.29,.19]) box(house,[.15,2.3,.17],[x,1.34,-2.5],beam);
  box(house,[.095,.13,.065],[-.04,1.33,-2.55],mat(0xd0a36b,.45));
  const winX=1.68;box(house,[1.48,1.23,.13],[winX,2.02,-2.43],glass);
  for(const x of [winX-.81,winX,winX+.81]) box(house,[.13,1.48,.16],[x,2.02,-2.53],beam);
  for(const y of [1.32,2.73]) box(house,[1.76,.13,.16],[winX,y,-2.53],beam);
  box(house,[1.5,.07,.16],[winX,2.02,-2.55],beam);
  box(house,[6.5,.16,1.55],[0,.12,-3.12],timber);
  for(let i=0;i<6;i++)box(house,[.10,.23,1.6],[-3+i*1.2,.18,-3.12],beam);
  // Chimney through upper back roof and two warm window lights.
  box(house,[.7,1.55,.7],[1.35,5.37,1],mat(0x716c66));
  box(house,[.94,.15,.88],[1.35,6.17,1],snow);
  const windowLight=new THREE.PointLight(0xffa65c,15,11,2);windowLight.position.set(1.5,2.35,-2.9);house.add(windowLight);
  const pathRock=createRock({seed:14,width:1.8,height:.48,depth:1});pathRock.position.set(2.95,.05,-3.55);house.add(pathRock);
  const smoke=new THREE.Group();smoke.name='chimney-smoke';house.add(smoke);
  const fogMat=new THREE.MeshBasicMaterial({color:0xd4e0e2,transparent:true,opacity:.15,depthWrite:false});
  for(let i=0;i<7;i++){const m=new THREE.Mesh(new THREE.SphereGeometry(1,9,7),fogMat.clone());m.scale.setScalar(.22+i*.095);m.userData.offset=i/7;smoke.add(m);}
  house.userData.update=(t)=>{smoke.children.forEach(s=>{const f=(t*.075+s.userData.offset)%1;s.position.set(1.35+Math.sin(f*6)*.18,6.25+f*3.2,1);s.material.opacity=.18*(1-f);});};
  return house;
}
