import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const url=(process.env.QA_URL||'http://127.0.0.1:4173')+'/?qa=1';
const browser=await chromium.launch({headless:true,args:['--enable-webgl','--use-gl=angle','--use-angle=swiftshader']});
const out=process.env.QA_OUTPUT||'qa-evidence';
await fs.mkdir(out,{recursive:true});
const errors=[];
const state=page=>page.evaluate(()=>window.__LN_A01A__?.state());
async function check(label,viewport,mobile){
 const context=await browser.newContext({viewport,hasTouch:mobile,isMobile:mobile,deviceScaleFactor:1});
 const page=await context.newPage();
 page.on('pageerror',e=>errors.push(`${label}: ${e.message}`));
 page.on('console',e=>{if(e.type()==='error')errors.push(`${label}: ${e.text()}`)});
 await page.goto(url,{waitUntil:'networkidle',timeout:50000});
 await page.getByRole('button',{name:/EXPLORE THE SNOW/}).click();
 await page.waitForTimeout(300);
 const start=await state(page);
 assert.ok(start && start.started,`${label} debug probe unavailable`);
 if(mobile){
   const bounds=await page.locator('#joystick').boundingBox();
   assert.ok(bounds,`${label} joystick missing`);
   const x=bounds.x+bounds.width/2,y=bounds.y+bounds.height/2;
   await page.mouse.move(x,y);await page.mouse.down();await page.mouse.move(x,y-34,{steps:4});
   await page.waitForTimeout(950);
   const moved=await state(page);
   assert.ok(moved.z<start.z-.8,`mobile joystick forward: ${moved.z} / ${start.z}`);
   await page.mouse.up();
   await page.waitForFunction(()=>Math.abs(window.__LN_A01A__?.state()?.vz ?? 100)<.1,null,{timeout:9000});
   const stopped=await state(page);
   assert.ok(Math.abs(stopped.vz)<.1,`mobile stop failed: ${JSON.stringify(stopped)}`);
   await page.locator('#jump').click();
   await page.waitForTimeout(170);
   assert.ok(!(await state(page)).grounded,'mobile hop should leave ground');
 } else {
   await page.keyboard.down('w');await page.waitForTimeout(950);
   const moved=await state(page);
   assert.ok(moved.z<start.z-.8,`desktop W forward: ${moved.z} / ${start.z}`);
   await page.keyboard.up('w');
   await page.waitForFunction(()=>Math.abs(window.__LN_A01A__?.state()?.vz ?? 100)<.1,null,{timeout:9000});
   assert.ok(Math.abs((await state(page)).vz)<.1,`desktop stop should brake: ${JSON.stringify(await state(page))}`);
   await page.keyboard.press('Space');await page.waitForTimeout(170);
   assert.ok(!(await state(page)).grounded,'desktop hop should leave ground');
 }
 await page.waitForFunction(()=>{const s=window.__LN_A01A__?.state();return s?.grounded && s?.jumpCount===1},null,{timeout:9000});
 const landed=await state(page);
 assert.equal(landed.grounded,true,`${label} must land`);
 assert.equal(landed.jumpCount,1,`${label} must jump once`);
 await page.getByRole('button',{name:/RESET/}).click();
 const reset=await state(page);
 assert.ok(Math.abs(reset.x+4)<.02&&Math.abs(reset.z-4)<.02,`${label} reset failed`);
 await page.screenshot({path:`${out}/a01a-${label}.png`});
 await context.close();
 return {label,initial:{x:start.x,z:start.z},moved:true,jump:landed.jumpCount,reset:true};
}
const result={success:false,results:[],errors};
try{
 result.results.push(await check('desktop',{width:1280,height:720},false));
 result.results.push(await check('mobile',{width:390,height:844},true));
 if(errors.length)throw new Error(errors.join('\n'));
 result.success=true;
}catch(e){errors.push(String(e));process.exitCode=1;}
finally{await browser.close();await fs.writeFile(`${out}/controller-results.json`,JSON.stringify(result,null,2))}
console.log('LN-A01a controller QA',JSON.stringify(result));
