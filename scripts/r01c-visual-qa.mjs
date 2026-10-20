import {chromium} from 'playwright';
import fs from 'node:fs/promises';
const base=process.env.QA_URL||'http://127.0.0.1:4174';
const dir='docs/r01c/evidence';await fs.mkdir(dir,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader']});
const results={errors:[],views:[],note:'Software WebGL; mobile viewport is not real-device performance evidence.'};
try{
 for(const mobile of [false,true]){
  const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:820,height:1000},deviceScaleFactor:mobile?2:1,isMobile:mobile,hasTouch:mobile});
  page.on('pageerror',e=>results.errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error')results.errors.push(m.text())});
  await page.goto(base+'/sculpt.html?qa=1');await page.waitForFunction(()=>window.__LN_SCULPT__?.ready);await page.waitForTimeout(500);
  for(const [label,key] of (mobile?[['mobile','5']]:[['front','1'],['right','2'],['rear','3'],['left','4'],['three-quarter','5'],['close-up','6'],['gameplay-distance','7']])){
   await page.keyboard.press(key);await page.waitForTimeout(180);
   await page.screenshot({path:`${dir}/webgl-${label}.png`});
   results.views.push({label,...await page.evaluate(()=>window.__LN_SCULPT__)});
  }
  await page.close();
 }
}finally{await browser.close();await fs.writeFile('docs/r01c/webgl-metrics.json',JSON.stringify(results,null,2));}
if(results.errors.length)throw Error(JSON.stringify(results.errors));
if(results.views.length!==8||results.views.some(v=>!v.triangles||v.drawCalls<1))throw Error('Incomplete render evidence');
console.log(JSON.stringify(results,null,2));
