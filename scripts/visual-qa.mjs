import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const url=process.env.QA_URL || 'http://127.0.0.1:4173';
const out=process.env.QA_OUTPUT || 'qa-evidence';
await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--disable-web-security']});
const issues=[];
async function capturePage(label,route,viewport,actions) {
  const context=await browser.newContext({viewport,deviceScaleFactor:1,hasTouch:viewport.width<500,isMobile:viewport.width<500});
  const page=await context.newPage();
  page.on('pageerror',error=>issues.push(`${label}: ${error.message}`));
  page.on('console',message=>{if(message.type()==='error')issues.push(`${label} console: ${message.text()}`);});
  const response=await page.goto(`${url}/${route}`,{waitUntil:'networkidle',timeout:45000});
  if(!response||response.status()!==200)issues.push(`${label} response: ${response?.status()}`);
  await page.waitForTimeout(1400);
  if(actions) await actions(page);
  await page.waitForTimeout(1400);
  const bounds=await page.locator('#scene').boundingBox();
  if(!bounds||bounds.width<100||bounds.height<100)issues.push(`${label}: canvas missing / zero size`);
  await page.screenshot({path:path.join(out,`${label}.png`),animations:'disabled'});
  const text=await page.locator('body').innerText();
  await context.close();return {label,bounds,text:text.slice(0,190)};
}
const views=[];
try {
  views.push(await capturePage('world-desktop','',{width:1280,height:720},async page=>{
    await page.getByRole('button',{name:/EXPLORE THE SNOW/}).click();
    await page.keyboard.down('w');await page.waitForTimeout(1300);await page.keyboard.up('w');
    await page.keyboard.press('p');
  }));
  views.push(await capturePage('world-mobile','',{width:390,height:844},async page=>{
    await page.getByRole('button',{name:/EXPLORE THE SNOW/}).click();
    await page.getByRole('button',{name:'Hop'}).click();
  }));
  for(const [number,label] of [[1,'front'],[2,'right'],[3,'rear'],[4,'left']]) {
    views.push(await capturePage(`spruce-${label}`,'sculpt.html',{width:920,height:920},async page=>page.keyboard.press(String(number))));
  }
} finally {await browser.close();}
await fs.writeFile(path.join(out,'qa-results.json'),JSON.stringify({success:issues.length===0,views,issues},null,2));
if(issues.length){console.error('Visual QA errors:',issues);process.exitCode=1;}else{console.log('Visual QA captures completed:',views.map(v=>v.label));}
