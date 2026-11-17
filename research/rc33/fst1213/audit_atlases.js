'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm');
const root=__dirname;
console.log('CONFIGURATION BEFORE COMPUTATION: received HTML scripts, Node VM with inert DOM; supplied selftests, literal words of lengths0..4, exact BigInt comparisons, declared empty-word display and unused-ceiling checks. No browser rendering or historical Python suites claimed. Node '+process.version);
function readSource(name){
 const original=path.join(root,'inputs',name);
 if(fs.existsSync(original))return fs.readFileSync(original,'utf8');
 const defaults=JSON.parse(fs.readFileSync(path.join(root,'extracted/DOM_DEFAULTS.json'),'utf8'))[name];
 return Object.entries(defaults).map(([k,v])=>`<input id="${k}" value="${v}">`).join('')+
 '<script>'+fs.readFileSync(path.join(root,'extracted',name.replace('.html','.js')),'utf8')+'</script>';
}
function load(name,override){
 const html=override===undefined?readSource(name):override,nodes={};
 for(const m of html.matchAll(/<input\b([^>]*)>/g)){
  const id=/\bid="([^"]+)"/.exec(m[1]),val=/\bvalue="([^"]*)"/.exec(m[1]);if(id)nodes[id[1]]={value:val?val[1]:''};
 }
 for(const m of html.matchAll(/<select\b[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/select>/g)){
  const opts=[...m[2].matchAll(/<option\b([^>]*)>([\s\S]*?)<\/option>/g)];const o=opts.find(x=>/selected/.test(x[1]))||opts[0];
  const val=o&&/value="([^"]*)"/.exec(o[1]);nodes[m[1]]={value:val?val[1]:o?.[2]||''};
 }
 const document={getElementById(id){if(!nodes[id])nodes[id]={value:''};return Object.assign(nodes[id],{addEventListener(){},classList:{toggle(){},add(){},remove(){}},style:{}})},querySelectorAll(){return []}};
 const context=vm.createContext({document,window:{},console});
 const js=[...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]).join('\n');
 vm.runInContext(js,context,{filename:name,timeout:10000});return {context,nodes};
}
const A=load('ATLAS_FST12_COMPLEJIDAD_HIPERACCESO.html'),B=load('ATLAS_FST13_INVERSO_OPTIMO.html');
const test12=A.context.window.FST12_SELFTEST(),test13=B.context.window.FST13.test();
if(test12.passed!==11||test13!==11)throw Error('received atlas selftest failure');
const extra=`
let count=0;
for(let ell=0;ell<=4;ell++)for(let n=0;n<10**ell;n++){
 const w=ell?String(n).padStart(ell,'0'):'';
 const o=encode(w);if(decode(o.h,ell,o.j)!==w)throw Error('rank roundtrip');count++;
}
if(fiberMax(1000)!==395||boundedSize(8n,1000)!==197913)throw Error('large exact table');
JSON.stringify({roundtrips:count,max1000:fiberMax(1000),bounded1000:boundedSize(8n,1000)});
`;
const round=JSON.parse(vm.runInContext(extra,B.context,{timeout:10000}));
B.nodes['mod-word'].value='';B.nodes['M-in'].value='1';vm.runInContext('showMod()',B.context);
const emptyDisplay=B.nodes['mod-result'].innerHTML;
if(!emptyDisplay.includes('<code>0</code>'))throw Error('expected received empty-word display issue changed');
const ceilReceived=vm.runInContext('divceil(5n,2n).toString()',B.context);
if(ceilReceived!=='2')throw Error('expected unused helper issue changed');
// Two forced local repairs are exercised without rewriting received inputs.
const corrected=readSource('ATLAS_FST13_INVERSO_OPTIMO.html')
 .replace("return -((-a)/b);","return a/b + (a%b>0n ? 1n : 0n);")
 .replace("ws.push(vv.toString().padStart(ell,'0'))","ws.push(ell===0?'ε':vv.toString().padStart(ell,'0'))");
const C=load('ATLAS_FST13_INVERSO_OPTIMO.html',corrected);
C.nodes['mod-word'].value='';C.nodes['M-in'].value='1';vm.runInContext('showMod()',C.context);
if(!C.nodes['mod-result'].innerHTML.includes('<code>ε</code>'))throw Error('empty-word correction');
for(let a=-20;a<=20;a++)for(let b=1;b<=10;b++){
 const v=vm.runInContext(`divceil(${a}n,${b}n).toString()`,C.context);
 if(Number(v)!==Math.ceil(a/b))throw Error('ceiling correction');
}
if(C.context.window.FST13.test()!==11)throw Error('patch regression');
fs.writeFileSync(path.join(root,'ATLAS_AUDIT.json'),JSON.stringify({status:'PASS',node:process.version,
 supplied_FST12_selftests:test12,supplied_FST13_selftests:test13,extended_exact_checks:round,
 received_limitations:[{issue:'Empty modular input displays 0 instead of the empty word.',impact:'Display only; arithmetic count is correct.'},
 {issue:'Unused divceil helper truncates positive nonintegral quotients instead of rounding up.',impact:'Helper is unused in the current active formulas; no current theorem invalidated.'}],
 forced_local_patch_checks:{fresh_VM:true,empty_witness:'ε',ceil_cases:410,selftest_regressions:11},
 provenance:'Actual received JavaScript executed in Node VM with an inert DOM; no browser or visual-interaction test claimed.'},null,2)+'\n');
console.log('PASS: both received 11-test suites, '+round.roundtrips+' inverse roundtrips, corrected 395/197913 examples; two scoped source limitations and their local fixes recorded.');
