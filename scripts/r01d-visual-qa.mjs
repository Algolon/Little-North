import {chromium} from 'playwright';
import fs from 'node:fs/promises';
const base=process.env.QA_URL||'http://127.0.0.1:4174';const dir='docs/r01d/evidence';await fs.mkdir(dir,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader']});
const result={views:[],errors:[],renderer:'Headless Chromium / ANGLE SwiftShader (not a mobile GPU)'};
try{const page=await browser.newPage({viewport:{width:1100,height:820}});
page.on('pageerror',e=>result.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')result.errors.push(m.text())});
await page.goto(base+'/bough.html');await page.waitForFunction(()=>window.__LN_BOUGH__?.ready,{timeout:30000});
for(const [label,key] of [['three-quarter','1'],['top','2'],['side','3'],['closeup','4']]){
 await page.keyboard.press(key);await page.waitForTimeout(500);await page.screenshot({path:dir+'/webgl-'+label+'.png'});
 result.views.push({label,...await page.evaluate(()=>window.__LN_BOUGH__)});
}}finally{await browser.close();await fs.writeFile('docs/r01d/webgl-metrics.json',JSON.stringify(result,null,2));}
if(result.errors.length||result.views.length!==4)throw Error('GLB browser validation failed '+JSON.stringify(result.errors));
console.log(JSON.stringify(result));
