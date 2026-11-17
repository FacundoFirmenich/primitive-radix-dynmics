const fs=require('fs'),vm=require('vm');
console.log('CONFIG: BigInt; source atoms4777,6444,7444; externalB10000; complete words n0..6; inertDOM, no browser visual claim.');
const defaults={sequence:'XYZ',bound:'8'},nodes={};
const node=id=>({value:defaults[id]||'',textContent:'',className:'',dataset:{},append(){},replaceChildren(){},addEventListener(){}});
const document={getElementById(id){return nodes[id]??=(node(id));},createElement(){return node('');},querySelectorAll(){return [];}};
const ctx=vm.createContext({document,console});vm.runInContext(fs.readFileSync('atomic_atlas_original.js','utf8'),ctx,{timeout:10000});
const result=vm.runInContext(`(()=>{let count=0;function visit(w,n){if(decode(k('X',w),k('Y',w))!==w)throw Error(w);if(-3n*k('X',w)+8n*k('Y',w)-5n*k('Z',w)!==B**BigInt(w.length))throw Error('ternary');count++;if(n<6)for(const t of ['X','Y','Z'])visit(w+t,n+1);}visit('',0);return {status:'PASS',words:count,smoke:document.getElementById('smoke').textContent};})()`,ctx,{timeout:10000});
if(result.words!==1093||!result.smoke.includes('7/7'))throw Error(JSON.stringify(result));fs.writeFileSync('ATOMIC_ATLAS_AUDIT.json',JSON.stringify(result,null,2)+'\n');console.log(result);
