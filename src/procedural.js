import * as THREE from 'three';

/** Little North procedural sculpting library. No downloaded meshes or textures. */
export function rng(seed = 1) {
  let state = seed >>> 0;
  return () => { state = (1664525 * state + 1013904223) >>> 0; return state / 4294967296; };
}
export const palette = {
  snow: 0xe8f1f2, frost: 0xbfdce7, shade: 0x91b6c5,
  pine: 0x244b48, pineLight: 0x3e7268, deepPine: 0x1b373e,
  rock: 0x617888, rockLight: 0x8399a7, wood: 0x76513d, woodDark: 0x483a36,
  amber: 0xffbb78,
};

/** Collapse many individual sculpted branch pieces into a handful of draw calls. */
export class GeometryBatch {
  constructor() { this.layers = new Map(); }
  add(geometry, materialKey, matrix = new THREE.Matrix4()) {
    const g = geometry.clone();
    g.applyMatrix4(matrix);
    const p = g.getAttribute('position');
    const n = g.getAttribute('normal');
    const indices = g.getIndex();
    if (!this.layers.has(materialKey)) this.layers.set(materialKey, { vertices: [], normals: [], triangles: [], count: 0 });
    const layer = this.layers.get(materialKey);
    for (let i = 0; i < p.count; i++) {
      layer.vertices.push(p.getX(i), p.getY(i), p.getZ(i));
      layer.normals.push(n ? n.getX(i) : 0, n ? n.getY(i) : 1, n ? n.getZ(i) : 0);
    }
    if (indices) {
      for (let i = 0; i < indices.count; i++) layer.triangles.push(layer.count + indices.getX(i));
    } else {
      for (let i = 0; i < p.count; i++) layer.triangles.push(layer.count + i);
    }
    layer.count += p.count;
    g.dispose();
  }
  build(materials) {
    const out = new THREE.Group();
    for (const [key, layer] of this.layers.entries()) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(layer.vertices, 3));
      g.setAttribute('normal', new THREE.Float32BufferAttribute(layer.normals, 3));
      g.setIndex(layer.triangles);
      const mesh = new THREE.Mesh(g, materials[key]);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      mesh.name = `batch-${key}`;
      out.add(mesh);
    }
    return out;
  }
}
const M = (x, y, z, ry = 0, sx = 1, sy = 1, sz = 1) =>
  new THREE.Matrix4().compose(new THREE.Vector3(x, y, z),
    new THREE.Quaternion().setFromEuler(new THREE.Euler(0, ry, 0)), new THREE.Vector3(sx, sy, sz));

/** A longitudinal, organic bough, not a stacked cone. Crown is built from asymmetric whorls. */
function bough(length, halfWidth, drop, snow = false, seed = 0) {
  const rand = rng(seed + 37);
  const stations = [0, .19, .42, .64, .81, 1];
  const taper = [.1, .64, 1, .96, .65, .09];
  const v = []; const indices = [];
  for (let i = 0; i < stations.length; i++) {
    const s = stations[i];
    let w = halfWidth * taper[i] * (snow ? .86 : 1);
    const sag = -drop * s * s - .07 * s;
    const height = sag + (snow ? .12 + .07 * Math.sin(s * Math.PI) : 0);
    const fringe = snow && i >= 3 ? .09 + rand() * .16 : .05;
    v.push(-w, height - fringe, s * length, 0, height + .06, s * length, w, height - fringe * (0.8 + rand()*.3), s * length);
  }
  for (let i = 0; i < stations.length - 1; i++) {
    const a = i * 3, b = (i + 1) * 3;
    indices.push(a, b, a + 1, a + 1, b, b + 1, a + 1, b + 1, a + 2, a + 2, b + 1, b + 2);
    // Single winding preserves valid smooth face normals; the material handles the back side.
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3));
  g.setIndex(indices); g.computeVertexNormals();
  return g;
}

/** Reference-led, asymmetric spruce. 4-6 batches/draw calls rather than hundreds of branches. */
export function createSnowSpruce({ seed = 7, height = 8, snowy = true, hero = false } = {}) {
  const random = rng(seed); const batch = new GeometryBatch();
  const mats = {
    bark: new THREE.MeshStandardMaterial({ color: 0x564940, roughness: .97 }),
    needlesDark: new THREE.MeshStandardMaterial({ color: palette.deepPine, roughness: .94, side: THREE.DoubleSide }),
    needles: new THREE.MeshStandardMaterial({ color: palette.pine, roughness: .91, side: THREE.DoubleSide }),
    needlesLight: new THREE.MeshStandardMaterial({ color: palette.pineLight, roughness: .91, side: THREE.DoubleSide }),
    snow: new THREE.MeshStandardMaterial({ color: 0xeaf3f4, roughness: .83, side: THREE.DoubleSide }),
    frost: new THREE.MeshStandardMaterial({ color: 0xc7dce3, roughness: .87, side: THREE.DoubleSide }),
  };
  batch.add(new THREE.CylinderGeometry(.035, .18, height * .87, 7, 1), 'bark', M(0, height*.43, 0));
  // Reference study: broad hanging lower boughs, irregular middle silhouette,
  // thin pointed crown with selectively snow-capped shelves.
  const levels = hero ? 12 : 8;
  for (let layer = 0; layer < levels; layer++) {
    const t = layer / (levels - 1);
    const y = height * (.15 + .72 * t);
    const longest = (1 - t) * height * .23 + height*.032;
    const n = Math.round((hero ? 7 : 5) - t*2 + random()*1.2);
    const offset = random() * Math.PI * 2;
    for (let j = 0; j < n; j++) {
      const az = offset + j * Math.PI * 2 / n + (random() - .5) * .26;
      const len = longest * (.72 + random() * .49);
      const halfWidth = len * (.28 + random()*.13);
      const drop = len * (.23 + random() * .22);
      const matrix = M(0, y + (random()-.5)*.12, 0, az);
      const tint = random() > .66 ? 'needlesLight' : random() > .52 ? 'needlesDark' : 'needles';
      const foliage = bough(len, halfWidth, drop, false, seed + j*41 + layer*100);
      batch.add(foliage, tint, matrix); foliage.dispose();
      if (snowy && (hero || random() > .1)) {
        const mantle = bough(len*(.79 + random()*.12), halfWidth*.98, drop*.98, true, seed + 199 + j*23 + layer*37);
        batch.add(mantle, random() > .88 ? 'frost' : 'snow', matrix); mantle.dispose();
      }
      // Secondary boughs create fine-grained jagged edges instead of flat triangles.
      if (hero && layer < 8 && j % 2 === 0) {
        const sideMatrix = M(0, y-.10, 0, az+.25);
        const branch = bough(len*.74, halfWidth*.65, drop*1.04, false, seed + 400 + j*61);
        batch.add(branch, tint, sideMatrix); branch.dispose();
      }
    }
  }
  // Sculpt the crown out of continuous small whorls, not a visually detached cone.
  for (let layer = 0; layer < 4; layer++) {
    const y = height * (.879 + layer * .028);
    const len = height * (.09 - layer * .019);
    for(let j=0;j<5;j++) {
      const az = j * Math.PI * 2 / 5 + layer * .44;
      const shape=bough(len,len*.36,len*.24,false,seed+900+layer*5+j);
      const mat = (j + layer) % 3 === 0 ? 'needlesLight' : 'needles';
      batch.add(shape,mat,M(0,y,0,az));shape.dispose();
      if(snowy) {
        const cap=bough(len*.84,len*.30,len*.23,true,seed+1100+layer*5+j);
        batch.add(cap,'snow',M(0,y,0,az));cap.dispose();
      }
    }
  }
  batch.add(new THREE.ConeGeometry(height*.026,height*.11,6), 'needles', M(0,height*.981,0));
  if(snowy)batch.add(new THREE.ConeGeometry(height*.018,height*.09,6),'snow',M(0,height*.994,0));
  const out = batch.build(mats);
  out.name = hero ? 'hero-reference-sculpt-spruce' : 'forest-spruce';
  out.userData.triangles = Array.from(batch.layers.values()).reduce((s,v)=>s+v.triangles.length/3,0);
  return out;
}

export function createRock({ seed = 1, width = 2.2, height = 1.4, depth = 1.7 } = {}) {
  const rand=rng(seed); const root = new THREE.Group();
  const g=new THREE.IcosahedronGeometry(1,1); const p=g.getAttribute('position');
  for(let i=0;i<p.count;i++) {
    const x=p.getX(i), y=p.getY(i),z=p.getZ(i), m=.87+rand()*.25;
    p.setXYZ(i,x*width*.5*m,y*height*.5*m,z*depth*.5*m);
  }
  g.computeVertexNormals();
  const rock=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:seed%2?palette.rock:palette.rockLight,roughness:1,flatShading:true}));
  rock.castShadow=true;rock.receiveShadow=true;root.add(rock);
  const cap=new THREE.Mesh(new THREE.SphereGeometry(1,10,7),new THREE.MeshStandardMaterial({color:palette.snow,roughness:.9}));
  cap.scale.set(width*.52,.16+height*.08,depth*.48); cap.position.y=height*.4; cap.castShadow=true; root.add(cap);
  root.name='snow-capped-rock'; return root;
}

export function makeWoodPlank(width = 1, height = .15, depth = .16, color = palette.wood) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(width, height, depth),
    new THREE.MeshStandardMaterial({color, roughness:.94}));
  mesh.castShadow=true;mesh.receiveShadow=true;return mesh;
}
