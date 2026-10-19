import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

// Genuine WebGL render evidence, captured from Vite in headless Chromium.
// File artifacts are the canonical proof, not images drawn by generative AI.
const base=process.env.QA_URL||'http://127.0.0.1:4173';
const folder=process.env.QA_OUTPUT||'qa-evidence';
await fs.mkdir(folder,{recursive:true});
const browser=await chromium.launch({headless:true,args:[
  '--enable-webgl','--use-gl=angle','--use-angle=swiftshader'
]});
const problems=[],shots=[];
let bench=null;
async function capture(label,route,{width=820,height=820,view}={}){
 const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1});
 const page=await context.newPage();
 page.on('pageerror',e=>problems.push(label+': '+e.message));
 page.on('console',m=>{if(m.type()==='error')problems.push(label+': '+m.text());});
 const response=await page.goto(base+'/'+route,{waitUntil:'networkidle',timeout:65000});
 if(!response||response.status()!==200)throw new Error(label+' page response '+response?.status());
 await page.waitForTimeout(1100);
 if(view)await page.keyboard.press(view);
 await page.waitForTimeout(450);
 const img=await page.screenshot({type:'jpeg',quality:83});
 if(img.length<18000)problems.push(label+' screenshot unexpectedly small ('+img.length+' bytes)');
 const filename=path.join(folder,'r01b-'+label+'.jpg');
 await fs.writeFile(filename,img);
 shots.push({label,bytes:img.length,filename});
 if(label==='three-quarter'){
   // Deliberately small reference image so reviewer can inspect actual CI render
   // via logs as well as downloadable screenshot artifacts.
   const thumb=await page.screenshot({type:'jpeg',quality:55});
   console.log('LN_R01B_VIEW_BEGIN');
   console.log(thumb.toString('base64'));
   console.log('LN_R01B_VIEW_END');
 }
 if(label==='three-quarter'){
   bench=await page.evaluate(async()=>{
     const {createHeroSpruce}=await import('/src/hero-spruce.js');
     const {Box3,Vector3}=await import('three');
     const o=createHeroSpruce({seed:19,height:9.6});
     const size=new Vector3();new Box3().setFromObject(o).getSize(size);
     const values={triangles:o.userData.triangles,materialBatches:o.children.length,
       size:{x:size.x,y:size.y,z:size.z},unindexedVertices:o.children.reduce((n,m)=>n+(m.geometry.getAttribute('position')?.count||0),0)};
     o.traverse(ch=>{if(ch.geometry)ch.geometry.dispose()});
     return values;
   });
 }
 await context.close();
}
try{
 for(const [label,view] of [['front','1'],['right','2'],['rear','3'],['left','4'],['three-quarter','5'],['detail','6'],['game-distance','7']])
   await capture(label,'sculpt.html?qa=1',{view});
 await capture('legacy-baseline','sculpt.html?legacy=1',{view:'5'});
 await capture('world','?heroReview=1',{width:1100,height:720});
 if(!bench||!Number.isFinite(bench.triangles))problems.push('no valid geometry statistics');
 else{
   if(bench.triangles>175000)problems.push('hero mesh triangle budget exceeded: '+bench.triangles);
   if(bench.materialBatches>10)problems.push('hero material batch budget exceeded: '+bench.materialBatches);
   if(bench.size.y<8.8||bench.size.y>10.5)problems.push('tree height mismatch '+bench.size.y);
   if(bench.size.x<3.2||bench.size.x>9.8)problems.push('silhouette unusually narrow or wide '+bench.size.x);
 }
} catch(err){problems.push(String(err));}
finally{
 await browser.close();
 await fs.writeFile(path.join(folder,'r01b-results.json'),JSON.stringify({ok:!problems.length,bench,shots,problems},null,2));
}
console.log('LN-R01b geometry report:',JSON.stringify(bench));
console.log('LN-R01b image labels:',shots.map(s=>s.label));
if(problems.length){console.error('LN-R01b QA FAILED',problems);process.exitCode=1;}
else console.log('LN-R01b QA PASS (technical only, visual approval outstanding)');
