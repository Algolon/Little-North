import * as THREE from 'three';

const white = new THREE.MeshStandardMaterial({ color: 0xe9eff0, roughness: .95, flatShading: false });
const cheek = new THREE.MeshStandardMaterial({ color: 0xf6f7ed, roughness: .96 });
const shadow = new THREE.MeshStandardMaterial({ color: 0xbecbd0, roughness: .94 });
const eye = new THREE.MeshStandardMaterial({ color: 0x20292d, roughness: .39 });
function oval(parent, material, position, scale, segments = 12) {
  const o=new THREE.Mesh(new THREE.SphereGeometry(1, segments, 10),material);
  o.position.set(...position);o.scale.set(...scale);o.castShadow=true;parent.add(o);return o;
}

export function makeFox() {
  const root=new THREE.Group();root.name='arctic-fox-character-proxy';
  const frame=new THREE.Group();root.add(frame);
  oval(frame,white,[0,.55,0],[.40,.37,.63]);
  oval(frame,cheek,[0,.77,-.38],[.43,.42,.43]);
  oval(frame,white,[0,.64,-.64],[.24,.19,.32]);
  oval(frame,eye,[0,.69,-.93],[.065,.052,.055],10);
  for(const s of [-1,1]) {
    const ear=new THREE.Mesh(new THREE.ConeGeometry(.14,.38,5),shadow);
    ear.position.set(s*.30,1.21,-.39);ear.rotation.z=-s*.12;frame.add(ear);
    const inner=new THREE.Mesh(new THREE.ConeGeometry(.09,.29,5),white);
    inner.position.set(s*.30,1.22,-.448);frame.add(inner);
    oval(frame,eye,[s*.31,.88,-.67],[.059,.066,.044]);
    oval(frame,cheek,[s*.35,.62,-.52],[.15,.19,.19]);
  }
  const tail=new THREE.Group();tail.position.set(0,.59,.55);frame.add(tail);
  oval(tail,shadow,[0,.02,.34],[.27,.25,.49]);
  oval(tail,white,[0,.07,.73],[.35,.32,.45]);
  oval(tail,cheek,[0,.1,1.08],[.27,.24,.28]);
  const legs=[];
  for (const sx of [-1,1]) for (const sz of [-1,1]) {
    const leg=new THREE.Group();leg.position.set(sx*.28,.29,sz*.40);frame.add(leg);
    oval(leg,white,[0,-.11,0],[.145,.24,.15]);
    oval(leg,cheek,[0,-.24,-.075],[.15,.09,.21]);
    legs.push(leg);
  }
  root.userData.animate=(time,speed) => {
    const motion=Math.min(speed/4,1);const stride=Math.sin(time*11)*.38*motion;
    legs.forEach((leg,i)=>{leg.rotation.x=(i===0||i===3?stride:-stride);});
    frame.position.y=Math.abs(Math.sin(time*11))*.025*motion;
    tail.rotation.x=.12+Math.sin(time*2.5)*.075;
    tail.rotation.y=Math.sin(time*3.4)*.12;
  };
  return root;
}
