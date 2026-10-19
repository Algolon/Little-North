import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const url=(process.env.QA_URL||'http://127.0.0.1:4173')+'/?qa=1';
const browser=await chromium.launch({headless:true,args:['--enable-webgl','--use-gl=angle','--use-angle=swiftshader']});
const out=process.env.QA_OUTPUT||'qa-evidence';
await fs.mkdir(out,{recursive:true});
const errors=[];
const state=page=>page.evaluate(()=>window.__LN_A01A__?.state());
// Visual-direction oracle: camera at (sin(yaw),cos(yaw)) means screen-up is (-sin,-cos).
function forwardAlignment(s){
 const fx=-Math.sin(s.yaw),fz=-Math.cos(s.yaw);
 return {forward:s.vx*fx+s.vz*fz,side:Math.abs(s.vx*(-fz)+s.vz*fx)};
}
async function checkOrbitAndMove(page,context,mobile){
 const before=await state(page);
 if(mobile){
  assert.equal(before.portraitTouch,true,'mobile art camera profile should be enabled');
  assert.ok(before.cameraDistance<7,'mobile camera must frame fox more closely');
  const b=await page.locator('#joystick').boundingBox();
  const x=b.x+b.width/2,y=b.y+b.height/2;
  const cdp=await context.newCDPSession(page);
  // Two simultaneous *touch* pointers: thumb stays on stick while the other
  // finger orbits the camera. Prior QA used mouse, missing this bug entirely.
  const stick={x,y:y-32,id:1},look={x:340,y:330,id:2};
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y,id:1}]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[stick]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[stick,look]});
  for(const stepX of [275,210,145,80]){
   look.x=stepX;
   await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[stick,look]});
   await page.waitForTimeout(70);
  }
  await page.waitForFunction(()=>{const s=window.__LN_A01A__?.state();return s?.yaw>.7 && s?.joyY>.45},null,{timeout:9000});
  await page.waitForFunction(()=>{
    const s=window.__LN_A01A__?.state();if(!s)return false;
    return s.vx*(-Math.sin(s.yaw))+s.vz*(-Math.cos(s.yaw))>1.5;
  },null,{timeout:9000});
  const moved=await state(page),a=forwardAlignment(moved);
  assert.ok(moved.yaw-before.yaw>.65,`dual-touch camera did not orbit: ${moved.yaw-before.y}`);
  assert.ok(a.forward>1.5 && a.side<1.3,`dual-touch joystick moves against view ${JSON.stringify({moved,a})}`);
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[stick]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 }else{
  const bounds=await page.locator('#scene').boundingBox();
  const x=bounds.x+bounds.width*.7,y=bounds.y+bounds.height*.5;
  await page.mouse.move(x,y);await page.mouse.down();
  await page.mouse.move(x-290,y,{steps:9});await page.mouse.up();
  const angle=(await state(page)).yaw;
  assert.ok(angle-before.yaw>.7,`desktop camera should orbit: ${angle-before.yaw}`);
  await page.keyboard.down('w');
  await page.waitForFunction(()=>{
    const s=window.__LN_A01A__?.state();return s && s.vx*(-Math.sin(s.yaw))+s.vz*(-Math.cos(s.yaw))>1.6;
  },null,{timeout:9000});
  const moved=await state(page),a=forwardAlignment(moved);
  assert.ok(a.forward>1.6&&a.side<1.3,`desktop orbit+W should move screen-up, ${JSON.stringify({a,moved})}`);
  await page.keyboard.up('w');
 }
 await page.waitForTimeout(250);
}

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
   await page.waitForFunction(()=>window.__LN_A01A__?.state()?.jumpCount===1,null,{timeout:9000});
 } else {
   await page.keyboard.down('w');await page.waitForTimeout(950);
   const moved=await state(page);
   assert.ok(moved.z<start.z-.8,`desktop W forward: ${moved.z} / ${start.z}`);
   await page.keyboard.up('w');
   await page.waitForFunction(()=>Math.abs(window.__LN_A01A__?.state()?.vz ?? 100)<.1,null,{timeout:9000});
   assert.ok(Math.abs((await state(page)).vz)<.1,`desktop stop should brake: ${JSON.stringify(await state(page))}`);
   await page.keyboard.press('Space');await page.waitForFunction(()=>window.__LN_A01A__?.state()?.jumpCount===1,null,{timeout:9000});
 }
 await page.waitForFunction(()=>{const s=window.__LN_A01A__?.state();return s?.grounded && s?.jumpCount===1},null,{timeout:9000});
 const landed=await state(page);
 assert.equal(landed.grounded,true,`${label} must land`);
 assert.equal(landed.jumpCount,1,`${label} must jump once`);
 assert.ok(landed.apex>start.y+.35,`${label} hop height insufficient: ${landed.apex} vs ${start.y}`);
 await page.getByRole('button',{name:/RESET/}).click();
 const reset=await state(page);
 assert.ok(Math.abs(reset.x+4)<.02&&Math.abs(reset.z-4)<.02,`${label} reset failed`);
 await checkOrbitAndMove(page,context,mobile);
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
