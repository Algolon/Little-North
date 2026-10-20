import {chromium} from 'playwright';
import fs from 'node:fs/promises';
const dir='docs/r01e/evidence';const errors=[];
const browser=await chromium.launch({executablePath:'/Users/omarjolein/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell',headless:true,args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader']});
try {
 const page=await browser.newPage({viewport:{width:1000,height:1100}});page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 await page.goto('http://127.0.0.1:4176/assets/r01e/viewer.html');await page.waitForFunction(()=>window.__LN_HERO__?.ready,{timeout:60000});
 const views=[];
 for(const [label,key] of [['three-quarter','1'],['rear','2'],['side','3'],['closeup','4']]) {await page.keyboard.press(key);await page.waitForTimeout(700);await page.screenshot({path:`${dir}/webgl-${label}.png`});views.push({label,...await page.evaluate(()=>window.__LN_HERO__)});}
 await fs.writeFile('docs/r01e/webgl-metrics.json',JSON.stringify({views,errors,renderer:'Chromium ANGLE SwiftShader desktop software rendering; no mobile claim'},null,2));
 if(errors.length)throw Error(JSON.stringify(errors));console.log(JSON.stringify(views[0]));
} finally {await browser.close()}
