// Run against an active Chrome debugging port: node tests/browser-results.mjs [base URL] [port]
import assert from 'node:assert/strict';
import {mkdir, writeFile, readdir, readFile} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';

const base = process.argv[2] || 'http://127.0.0.1:8093/';
const debuggerBase = `http://127.0.0.1:${process.argv[3] || 9333}`;
const output = join(tmpdir(), `rostering-browser-${Date.now()}`);
await mkdir(output, {recursive: true});
for (const width of [1440, 390]) {
  const tab = await fetch(`${debuggerBase}/json/new?about:blank`, {method:'PUT'}).then(r => r.json());
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  const pending = new Map(), errors = [];
  let sequence = 0;
  ws.onmessage = event => {
    const message = JSON.parse(event.data);
    if (message.id) {
      const task = pending.get(message.id);pending.delete(message.id);
      if (message.error) task.reject(Error(JSON.stringify(message.error)));else task.resolve(message.result);
    } else if (message.method === 'Runtime.exceptionThrown' || (message.method === 'Log.entryAdded' && message.params.entry.level === 'error')) errors.push(message);
  };
  await new Promise(resolve => {ws.onopen = resolve;});
  const send = (method, params = {}) => new Promise((resolve, reject) => {const id = ++sequence;pending.set(id, {resolve, reject});ws.send(JSON.stringify({id,method,params}));});
  const evaluate = async expression => {
    const result = await send('Runtime.evaluate', {expression,awaitPromise:true,returnByValue:true});
    if (result.exceptionDetails) throw Error(JSON.stringify(result.exceptionDetails));
    return result.result.value;
  };
  const until = async expression => {
    for (let i=0;i<160;i++) {if(await evaluate(expression))return;await new Promise(r=>setTimeout(r,100));}
    throw Error(`Timeout: ${expression}`);
  };
  const click = async (selector, fraction=.5) => {
    const position = await evaluate(`(()=>{const el=document.querySelector(${JSON.stringify(selector)});el.scrollIntoView({block:'center',behavior:'instant'});const r=el.getBoundingClientRect();return{x:r.left+r.width*${fraction},y:r.top+r.height/2}})()`);
    await send('Input.dispatchMouseEvent', {type:'mousePressed',button:'left',clickCount:1,...position});
    await send('Input.dispatchMouseEvent', {type:'mouseReleased',button:'left',clickCount:1,...position});
  };
  const screenshot = async name => {
    const image = await send('Page.captureScreenshot', {format:'png'});
    await writeFile(join(output, `${width}-${name}.png`), Buffer.from(image.data, 'base64'));
  };
  await send('Page.enable');await send('Runtime.enable');await send('Log.enable');
  await send('Emulation.setDeviceMetricsOverride', {width,height:1000,deviceScaleFactor:1,mobile:width<600});
  await send('Page.setDownloadBehavior', {behavior:'allow',downloadPath:join(output,String(width))});
  await send('Page.navigate', {url:base});
  await until(`document.querySelectorAll('.type-card').length===2`);
  await click('#solve');await until(`document.querySelectorAll('.timeline-row').length===9`);
  assert.equal(await evaluate(`document.querySelector('#error').textContent`), '');
  assert.equal(await evaluate(`document.querySelector('#kpis b').textContent`), '9');
  const geometry = await evaluate(`(()=>{
    const track=document.querySelector('.timeline-track'),r=track.getBoundingClientRect();
    const bars=[...track.children];
    return{overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,axis:getComputedStyle(document.querySelector('.timeline-axis')).display,row:getComputedStyle(document.querySelector('.timeline-row')).display,track:getComputedStyle(track).display,count:document.querySelectorAll('[data-segment]').length,expected:data.segments.length,width:r.width,totalWidth:bars.reduce((sum,b)=>sum+b.getBoundingClientRect().width,0),finalRight:bars.at(-1).getBoundingClientRect().right-r.right,axisText:document.querySelector('.timeline-axis').innerText};})()`);
  assert.equal(geometry.overflow,0);assert.equal(geometry.axis,'grid');assert.equal(geometry.row,'grid');assert.equal(geometry.track,'block');
  assert.equal(geometry.count,geometry.expected);assert.ok(Math.abs(geometry.finalRight)<1);assert.ok(Math.abs(geometry.totalWidth-geometry.width)<2);
  assert.match(geometry.axisText,/721h/);
  await click('.roster-panel h3');await screenshot('full-chart');
  await click('[data-window="72"]');assert.equal(await evaluate(`document.querySelector('#rangeLabel').textContent`),'0–72h');
  await click('#nextWindow');assert.equal(await evaluate(`document.querySelector('#rangeLabel').textContent`),'72–144h');
  await click('[data-window="24"]');assert.equal(await evaluate(`document.querySelector('#rangeLabel').textContent`),'72–96h');
  await click('#timelineRange',.9);
  assert.ok(await evaluate(`Number(document.querySelector('#timelineRange').value)>500`));
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'End',code:'End',windowsVirtualKeyCode:35});
  await send('Input.dispatchKeyEvent',{type:'keyUp',key:'End',code:'End',windowsVirtualKeyCode:35});
  assert.equal(await evaluate(`document.querySelector('#rangeLabel').textContent`),'697–721h');
  await click('.timeline-segment');assert.match(await evaluate(`document.querySelector('#chartDetail').textContent`),/持续.*小时/);
  await click('#coverageView');assert.equal(await evaluate(`document.querySelectorAll('.coverage-plot svg').length`),1);
  await click('.coverage-plot svg');assert.match(await evaluate(`document.querySelector('#chartDetail').textContent`),/实际服务.*需求.*缺口/);
  await click('[data-window="all"]');assert.match(await evaluate(`document.querySelector('#chartSummary').textContent`),/缺口 8 车/);
  await screenshot('coverage');
  await evaluate(`document.querySelector('[data-param="同时服务数量"]').value=10`);
  await click('[data-window="24"]');assert.match(await evaluate(`document.querySelector('#chartSummary').textContent`),/需求 2 辆/);
  await click('#vehicleView');await click('[data-window="all"]');await click('#expandChart');
  assert.equal(await evaluate(`document.querySelector('.roster-panel').classList.contains('chart-expanded')`),true);await screenshot('expanded');
  await click('#expandChart');assert.equal(await evaluate(`document.querySelector('.roster-panel').classList.contains('chart-expanded')`),false);
  const before=await evaluate(`document.querySelector('#table tbody').innerText`);await click('#nextPage');
  assert.notEqual(await evaluate(`document.querySelector('#table tbody').innerText`),before);
  assert.equal(await evaluate(`document.querySelector('#pageMeta').textContent`),'第 2 / 41 页');
  await evaluate(`document.querySelector('#activityFilter').value='维修';document.querySelector('#activityFilter').dispatchEvent(new Event('change'))`);
  assert.equal(await evaluate(`[...document.querySelectorAll('.activity-cell')].every(x=>x.textContent==='维修')`),true);
  assert.ok(await evaluate(`document.querySelector('#table').scrollHeight>document.querySelector('#table').clientHeight`));
  await click('#download');
  let files=[];for(let i=0;i<50;i++){files=await readdir(join(output,String(width))).catch(()=>[]);if(files.some(f=>f.endsWith('.csv')))break;await new Promise(r=>setTimeout(r,100));}
  const csv = await readFile(join(output,String(width),files.find(f=>f.endsWith('.csv'))),'utf8');assert.equal(csv.trim().split('\n').length,1224);
  assert.equal(await evaluate(`document.documentElement.scrollWidth-document.documentElement.clientWidth`),0);
  assert.deepEqual(errors,[]);
  console.log(JSON.stringify({base,width,runtime:await evaluate('data.runtime_seconds'),geometry,tests:'buttons, full range, 72/24h, slider to final hour, task detail, coverage, expand, paging, filter, internal scroll, CSV passed'}));
  ws.close();await fetch(`${debuggerBase}/json/close/${tab.id}`);
}
console.log(`Screenshots: ${output}`);
