const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--autoplay-policy=no-user-gesture-required']});
const ctx=await b.newContext({viewport:{width:720,height:1296},recordVideo:{dir:'rec',size:{width:720,height:1296}}});
const p=await ctx.newPage();const t0=Date.now();
p.on('console',m=>{if(m.text()==='START')console.log('start_ms',Date.now()-t0)});
await p.goto('file://'+process.argv[2]+'#render');
await p.waitForTimeout(1500+parseFloat(process.argv[3]||'72')*1000+1000);
await ctx.close();await b.close();})();
