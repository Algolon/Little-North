import * as THREE from 'three';
import { GeometryBatch, rng } from './procedural.js';

/**
 * LN-R01b — HERO SPRUCE v0.1 (reference-led, fully volumetric geometry).
 *
 * Source references: two owner-supplied snow-laden spruces, retained in chat.
 * Reference 1: fullness, thick softened snow and inviting sculptural character.
 * Reference 2: irregular side boughs, exposed trunk and readable joints.
 *
 * All branchlets, woody segments and snow caps are baked by material into
 * seven meshes. This is not a stack of cones or camera-facing foliage cards.
 * +Y up, trunk grounded at y=0, primary boughs grow along local +Z.
 */

const PALETTE = {
  trunk: 0x76503a, barkShadow: 0x503c35,
  pineDeep: 0x223e3d, pine: 0x315b53,
  pineWarm: 0x466f5d, pineTips: 0x65856a,
  snow: 0xf2f6f3, snowBlue: 0xd5e4eb
};
const mat = (color, opts = {}) =>
  new THREE.MeshStandardMaterial({ color, roughness: .94, metalness: 0, ...opts });
const materials = {
  trunk: mat(PALETTE.trunk),
  barkShadow: mat(PALETTE.barkShadow),
  pineDeep: mat(PALETTE.pineDeep),
  pine: mat(PALETTE.pine),
  pineWarm: mat(PALETTE.pineWarm),
  pineTips: mat(PALETTE.pineTips),
  snow: mat(PALETTE.snow, {roughness:.86}),
  snowBlue: mat(PALETTE.snowBlue, {roughness:.89})
};
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const qY = r => new THREE.Matrix4().makeRotationY(r);
const tMat = (x,y,z) => new THREE.Matrix4().makeTranslation(x,y,z);
function branchFrame(y, angle, x=0, rise=0, z=0, turn=0) {
  return tMat(0,y,0).multiply(qY(angle)).multiply(tMat(x,rise,z)).multiply(qY(turn));
}
function pushTri(indices,a,b,c){indices.push(a,b,c);}
function loftGeometry(count, sides, vertex){
  const p=[], uv=[], ix=[];
  for(let j=0;j<=count;j++)for(let k=0;k<sides;k++){
    const v=vertex(j/count,k/sides,j,k);
    p.push(...v);uv.push(j/count,k/sides);
  }
  for(let j=0;j<count;j++)for(let k=0;k<sides;k++){
    const a=j*sides+k,b=j*sides+(k+1)%sides;
    const c=a+sides,d=b+sides;
    // outward normals for +Z oriented taper
    pushTri(ix,a,b,c);pushTri(ix,b,d,c);
  }
  const g=new THREE.BufferGeometry();
  g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));
  g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
  g.setIndex(ix);g.computeVertexNormals();
  return g;
}
/** Distinctive taper + subtle bends + ground-level root flare. */
function sculptTrunk(height,rand){
  const phases=[rand()*6,rand()*6,rand()*6];
  const rings=17,sides=11;
  return loftGeometry(rings,sides,(u,v)=>{
    const y=u*height*.97, a=v*Math.PI*2;
    const taper=Math.pow(1-u,.79);
    const flare=1+.62*Math.exp(-u*30);
    const radius=(.055+.245*taper)*flare;
    const knots=1+.065*Math.sin(a*5+phases[0]+u*21)+.042*Math.sin(a*8-u*34);
    const xBend=.045*Math.sin(u*5.1+phases[1])-.045*Math.sin(phases[1]);
    const zBend=.034*Math.sin(u*4.4+phases[2])-.034*Math.sin(phases[2]);
    return [xBend+Math.cos(a)*radius*knots,y,zBend+Math.sin(a)*radius*knots];
  });
}
/** Tapered organic cylinder between two 3D points, with no per-piece draw call. */
function twig(a,b,startRadius,endRadius,facets=6){
  const A=new THREE.Vector3(...a),B=new THREE.Vector3(...b),d=B.clone().sub(A);
  const g=new THREE.CylinderGeometry(endRadius,startRadius,d.length(),facets,1);
  g.translate(0,d.length()/2,0);
  g.applyMatrix4(new THREE.Matrix4().makeRotationFromQuaternion(
    new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize())));
  g.translate(...a);
  return g;
}
/** Volumetric sculpted tapered leaf spray, softened/lobed not a flat ribbon. */
function needleSpray(length,width,depth,drop,seed){
  const random=rng(seed);
  const variant=random()*6.283;
  return loftGeometry(7,7,(u,v)=>{
    const a=v*Math.PI*2;
    const u2=Math.pow(u,.88),shape=Math.pow(Math.sin(Math.PI*clamp(u,.001,.999)),.72);
    const w=width*shape*(1+.07*Math.sin(u*13+variant));
    const thickness=depth*shape;
    const bend=.065*Math.sin(u*5.7+variant)-.065*Math.sin(variant);
    const serration=(.024+width*.065)*Math.max(0,u-.18)*Math.sin(u*46+variant);
    return [
      Math.cos(a)*(w+serration)+bend,
      -drop*u2*u2+Math.sin(a)*thickness+.04*Math.sin(Math.PI*u),
      length*u
    ];
  });
}
/** Thick snow *resting on* a branch. A soft asymmetric loft with hanging rounded lips. */
function snowMantle(length,width,drop,seed){
  const rand=rng(seed),phase=rand()*6.283,tipBias=.86+rand()*.12;
  return loftGeometry(7,9,(u,v)=>{
    const a=v*Math.PI*2;
    const shape=Math.pow(Math.sin(Math.PI*clamp(u,.001,.999)),.57);
    const bulge=(.8+.25*Math.sin(u*8+phase));
    const w=width*shape*bulge;
    const yPath=-drop*u*u+.13+.065*Math.sin(Math.PI*u);
    const thickness=(.13+width*.21)*shape;
    const drip=(.055+width*.065)*Math.max(0,Math.sin(u*12+phase))*shape;
    const edge=Math.abs(Math.cos(a));
    const under=Math.sin(a)<0?drip*Math.pow(edge,6):0;
    return [
      Math.cos(a)*w+.035*Math.sin(u*9+phase)*shape,
      yPath + Math.sin(a)*(Math.sin(a)>0?thickness:thickness*.46) - under,
      u*length*tipBias
    ];
  });
}
/** Small shaped snow tongue laid over a neighboring cluster, not a repeated white cone. */
function snowFinger(batch,level,angle,x,y,z,length,width,drop,seed){
  const cap=snowMantle(length,width,drop,seed);
  batch.add(cap,seed%13===0?'snowBlue':'snow',
    branchFrame(level,angle,x,y,z,0));
  cap.dispose();
}
/**
 * Build the hero spruce at its native height. Only this asset, not forest LOD.
 * @returns {THREE.Group} with .userData {triangles, drawCalls, styleVersion}
 */
export function createHeroSpruce({seed=19,height=9.6,snowCover=.76}={}){
  const random=rng(seed), batch=new GeometryBatch();
  const trunk=sculptTrunk(height,random);
  batch.add(trunk,'trunk');trunk.dispose();
  // Unequal buttressed roots keep the massive trunk physically seated.
  for(let i=0;i<5;i++){
    const angle=i*Math.PI*2/5+random()*.6;
    const local=branchFrame(.36,angle).multiply(tMat(0,0,.16));
    const r=twig([0,0,0],[0,-.27,.38],.17,.03,7);
    batch.add(r,i===3?'barkShadow':'trunk',local);r.dispose();
  }

  const tiers=12;
  for(let tier=0;tier<tiers;tier++){
    const t=tier/(tiers-1),y=height*(.18+.69*t);
    const branchCount=clamp(Math.round(5+random()*2-t*2),3,7);
    const phase=random()*6.283;
    const tierLength=height*(.315*Math.pow(1-t,1.10)+.038);
    const stagger=(random()-.5)*height*.015;
    for(let arm=0;arm<branchCount;arm++){
      let az=phase+arm/branchCount*Math.PI*2+(random()-.5)*.35;
      const len=tierLength*(.78+random()*.34);
      const drop=len*(.16+random()*.16);
      const level=y+stagger+(random()-.5)*.14;
      const frame=branchFrame(level,az);
      // Visible main woody arm, organically curved/downward at the outer end.
      const b1=twig([0,0,.04],[.045,-drop*.2,len*.48],.079*(1-t*.6),.05*(1-t*.55));
      const b2=twig([.045,-drop*.2,len*.48],[.09,-drop,len*.99],.052*(1-t*.48),.008);
      batch.add(b1,'trunk',frame);batch.add(b2,'barkShadow',frame);
      b1.dispose();b2.dispose();

      // Central cluster: a three-dimensional, sagging long bough.
      const central=needleSpray(len*.98,len*(.16+random()*.04),
        .14+len*.058,drop*.92,seed+1000+tier*97+arm*67);
      const material=arm%4===0?'pineDeep':arm%3===0?'pineWarm':'pine';
      batch.add(central,material,branchFrame(level,az,0,-.10,len*.07));
      central.dispose();

      // Sprays fanning to both sides of each primary branch: organic outline.
      const sprayCount=tier<8?5:3;
      for(let s=0;s<sprayCount;s++){
        const u=(s+.65)/(sprayCount+1);
        const offset=(u-.1)*len;
        const lateralLen=len*(.43+random()*.18)*(1-u*.36);
        for(const side of [-1,1]){
          const rotation=side*(.43+random()*.39);
          const localY=-drop*u*u-.06;
          const spread=needleSpray(lateralLen,
            lateralLen*(.19+random()*.08),
            .09+lateralLen*.075,lateralLen*(.12+random()*.16),
            seed+tier*780+arm*103+s*29+(side+1)*23);
          const frameSide=branchFrame(level,az,0,localY,offset,rotation);
          const tint=(s+arm+side+tier)%5===0?'pineTips':(s+arm)%3===0?'pineWarm':'pine';
          batch.add(spread,tint,frameSide);spread.dispose();

          // 3D tuft fingers cut natural little notches into the outline.
          for(let leaf=0;leaf<1;leaf++){
            const leafLen=lateralLen*(.36+random()*.18);
            const twigLeaf=needleSpray(leafLen,leafLen*.19,.045+leafLen*.04,
              leafLen*.12,seed+40000+tier*1031+arm*103+s*13+leaf*3);
            batch.add(twigLeaf,(tier+arm+s)%3===0?'pineDeep':tint,
              branchFrame(level,az,side*len*.018,
                localY-.07,offset+lateralLen*(.28+leaf*.3),
                rotation+side*(leaf===0?.28:-.22)));
            twigLeaf.dispose();
          }

          // Snow is selectively placed on upper facing clusters.
          if(random()<snowCover*(t>.75?.55:1) && (s%2===0 || random()<.28)){
            const capLen=lateralLen*(.72+random()*.14);
            const cap=snowMantle(capLen,
              lateralLen*(.21+random()*.055),lateralLen*.18,
              seed+10000+tier*251+arm*53+s*11+side);
            batch.add(cap,(tier+arm+s)%14===0?'snowBlue':'snow',
              branchFrame(level,az,0,localY+.045,offset+.055*len,rotation));
            cap.dispose();
          }
        }
      }
      // Large irregular quilts of snow over the central primary boughs.
      if(random()<snowCover*(.94+t*.05)){
        snowFinger(batch,level,az,0,.015,len*.17,
          len*(.68+random()*.12),len*(.16+random()*.055),
          drop*.79,seed+1200+tier*125+arm*35);
      }
    }
  }

  // Crown remains continuous with primary branches, not an isolated spike.
  for(let i=0;i<5;i++){
    const y=height*(.879+i*.021);
    const count=i<3?5:4;
    for(let j=0;j<count;j++){
      const az=j*Math.PI*2/count+i*.38+(random()-.5)*.3;
      const len=height*(.103-i*.014);
      const tuft=needleSpray(len,len*.20,len*.09,len*.19,
        seed+80000+i*17+j*13);
      batch.add(tuft,(i+j)%3===0?'pineWarm':'pine',
        branchFrame(y,az));tuft.dispose();
      if((i+j)%3!==2){
        const cap=snowMantle(len*.72,len*.15,len*.16,seed+90000+i*13+j*19);
        batch.add(cap,'snow',branchFrame(y,az,0,.035,.045));
        cap.dispose();
      }
    }
  }
  // Small irregular last tip and soft cap; no cone primitives.
  const tip=needleSpray(height*.15,height*.035,height*.025,height*.035,seed+703);
  batch.add(tip,'pine',branchFrame(height*.861,0));
  tip.dispose();
  const topSnow=snowMantle(height*.105,height*.026,height*.026,seed+903);
  batch.add(topSnow,'snow',branchFrame(height*.887,0,0,.025,.018));
  topSnow.dispose();

  const object=batch.build(materials);
  object.name='LN-R01b-premium-hero-spruce';
  object.userData.styleVersion='LN-R01b-v0.1';
  object.userData.triangles=[...batch.layers.values()].reduce((n,l)=>n+l.triangles.length/3,0);
  object.userData.drawCalls=object.children.length;
  object.userData.seed=seed;
  return object;
}
