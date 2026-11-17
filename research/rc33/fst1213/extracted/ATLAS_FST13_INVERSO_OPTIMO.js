
'use strict';
const $=id=>document.getElementById(id);
const abs=n=>n<0n?-n:n;
function mod(a,m){let r=a%m;return r<0n?r+m:r}
function gcd(a,b){a=abs(a);b=abs(b);while(b){let t=a%b;a=b;b=t;}return a}
function divceil(a,b){if(b<=0n)throw Error('Divisor');return -((-a)/b);}
// JS BigInt division truncates toward zero; for every needed divceil numerator is nonnegative.
function ceilPos(a,b){return (a+b-1n)/b}
function checkWord(w){if(typeof w!=='string'||!/^[0-9]*$/.test(w))throw Error('Se exige una palabra decimal literal (puede ser vacía).');return w}
function key(w){checkWord(w);const m=10n**BigInt(w.length);return 8n*m-9n*BigInt(w||'0')}
function primitive(K){let a=0;while(K%7n===0n){K/=7n;a++;}return {h:K,a}}
function validH(h){return h!==0n&&h%7n!==0n&&[2n,5n,8n].includes(mod(h,9n))}
function a0(h){if(!validH(h))throw Error('Etiqueta H inadmisible: no corresponde a ninguna palabra.');let x=h;for(let a=0;a<3;a++){if(mod(x,9n)===8n)return a;x*=7n}throw Error('Inconsistencia de la etiqueta')}
function K0(h){return h*7n**BigInt(a0(h))}
function canonical(K){let ell=0;let m=1n;if(mod(K,9n)!==8n)throw Error('K no pertenece a 8 + 9Z');if(K>0n){while(K>8n*m){ell++;m*=10n}}else{while(m<9n-K){ell++;m*=10n}}const v=(8n*m-K)/9n;const w=ell===0?'':v.toString().padStart(ell,'0');if(w.startsWith('8'))throw Error('Fallo de forma canónica');return w}
function fiberSize(h,ell){const base=abs(K0(h));const cap=h>0n?8n*(10n**BigInt(ell)):10n**BigInt(ell)-9n;let A=0,cur=base;while(cur<=cap){A++;cur*=343n}return A}
function fiberMax(ell){const m=10n**BigInt(ell);let q=1n,A=0;while(q<=m){A++;q*=343n}return A}
function boundedSize(h,L){let K=K0(h),cap=h>0n?8n*10n**BigInt(L):10n**BigInt(L)-9n;let sum=0;for(let cur=K;abs(cur)<=cap;cur*=343n){const c=canonical(cur);sum+=L-c.length+1;}return sum}
function bitWidth(A){if(A<=1)return 0;return (A-1).toString(2).length}
function decode(h,ell,j){const A=fiberSize(h,ell);if(!Number.isInteger(j)||j<0||j>=A)throw Error('Índice de rango fuera de la fibra');const c=canonical(K0(h)*343n**BigInt(j));const w='8'.repeat(ell-c.length)+c;return w}
function encode(w){const K=key(w), {h,a}=primitive(K), b=a0(h),j=(a-b)/3;if(j<0||3*j+b!==a)throw Error('Error en valoración normalizada');const A=fiberSize(h,w.length);if(decode(h,w.length,j)!==w)throw Error('Error en inversión');return {K,h,a,ell:w.length,j,A,bits:bitWidth(A)}}
function isAccepted(w,mode){if(mode==='no8')return !w.includes('8');if(mode==='even8')return [...w].filter(x=>x==='8').length%2===0;if(mode==='mod3')return [...w].reduce((s,x)=>s+Number(x),0)%3===0;return true}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]))}
function fmt(n){return typeof n==='bigint'?n.toLocaleString('es-ES'):Number(n).toLocaleString('es-ES')}
function preview(w){return w.length<=96?esc(w):esc(w.slice(0,46))+'…'+esc(w.slice(-42))+' <small class="muted">(visualización abreviada, cálculo íntegro)</small>'}
function metric(v,label){return `<div class="metric"><div class="num">${esc(v)}</div><small>${esc(label)}</small></div>`}
function output(id,html){$(id).innerHTML=html}
function guarded(id,fn){try{fn()}catch(e){output(id,`<div class="result err">${esc(e.message||String(e))}</div>`)}}
function showWord(){guarded('word-result',()=>{let w=checkWord($('word-input').value),o=encode(w),mode=$('filter-word').value;let matches=[];for(let j=0;j<o.A;j++){let cw=decode(o.h,o.ell,j);if(isAccepted(cw,mode))matches.push({j,cw})}
let r=`<div class="metrics">${metric(String(o.K),'K exacto')}${metric(String(o.h),'H exacto')}${metric(o.ell,'Longitud')}${metric(o.j,'Índice j')}${metric(o.A,'Fibra íntegra')}${metric(o.bits,'Bits auxiliares máximos para esta fibra')}</div>`;
r+=`<div class="result"><div class="math">K(w) = 8 × 10^${o.ell} − 9 × val(w) = ${o.K}
H(w) = K(w) / 7^${o.a} = ${o.h}
rank(w) = ${o.j}  |  rango admisible: 0…${o.A-1}</div></div>`;
r+=`<h3 style="margin-top:15px">Candidatos compatibles con el lenguaje elegido (${matches.length})</h3>`;
r+=matches.length?`<div class="tablewrap"><table class="table"><thead><tr><th>j</th><th>Palabra literal</th></tr></thead><tbody>${matches.slice(0,180).map(({j,cw})=>`<tr><td>${j}</td><td class="long">${preview(cw)}</td></tr>`).join('')}</tbody></table></div>${matches.length>180?'<p class="muted">La tabla presenta las primeras 180 de las '+matches.length+' palabras; el inversor permite acceder a cualquier rango.</p>':''}`:'<p class="warn">Ninguna palabra de la fibra pertenece al lenguaje seleccionado.</p>';
output('word-result',r)})}
function showInverse(){guarded('inverse-result',()=>{let raw=$('h-in').value.trim();if(!/^-?\d+$/.test(raw))throw Error('Etiqueta H inválida');let h=BigInt(raw);let ell=Number($('ell-in').value),j=Number($('rank-in').value);if(!Number.isInteger(ell)||ell<0||ell>5000)throw Error('Longitud entre 0 y 5000');let A=fiberSize(h,ell),max=fiberMax(ell);let matches=[];for(let k=0;k<A;k++){const w=decode(h,ell,k);if(isAccepted(w,$('filter-inverse').value))matches.push([k,w])}
let hdr=`<div class="metrics">${metric(A,'Candidatos sin restricción')}${metric(bitWidth(A),'Bits máximos para esta fibra')}${metric(max,'Máxima ambigüedad a esta longitud')}${metric(matches.length,'Candidatos admitidos por el lenguaje')}${metric(boundedSize(h,ell),'Candidatos si solo |w| ≤ ℓ')}${metric(bitWidth(boundedSize(h,ell)),'Bits si la longitud es solo una cota')}</div>`;
let status=matches.length===0?'INCONSISTENT':matches.length===1?'UNIQUE':'NOT_IDENTIFIABLE';
let r=hdr+`<div class="result"><strong>Certificación:</strong> ${status}; <strong>bits auxiliares óptimos restringidos:</strong> ${matches.length?bitWidth(matches.length):'no aplicable'}.</div>`;
if(j>=0&&j<A&&Number.isInteger(j)){const w=decode(h,ell,j);r+=`<div class="result"><strong>Reconstrucción exacta para j=${j}</strong><div class="math">${preview(w)}</div><span class="muted">Entrada completa: ${fmt(ell)} cifras; su precisión no se reduce.</span></div>`}else{r+='<p class="warn">El rango seleccionado no es admisible; modificá j.</p>'}
r+=`<div class="tablewrap"><table class="table"><thead><tr><th>Rango j</th><th>Palabra compatible</th></tr></thead><tbody>${matches.slice(0,200).map(([k,w])=>`<tr><td>${k}</td><td class="long">${preview(w)}</td></tr>`).join('')}</tbody></table></div>${matches.length>200?`<p class="muted">Se muestran 200 de ${matches.length} resultados. Cambiá j para consultar cualquier candidato.</p>`:''}`;
output('inverse-result',r)})}
function E(ell,j){let m=10n**BigInt(ell),q=343n**BigInt(j),lo=ceilPos(8n*m*(q-1n),9n*q),hi=(8n*m*q+m-9n)/(9n*q);return hi>=lo?hi-lo+1n:0n}
function multi(ell){let a=[],j=0;for(;;){let v=E(ell,j);a.push(v);if(v===0n)break;j++}a.push(0n,0n);let out=[];for(let f=1;f<a.length-1;f++){let nf=a[f-1]-2n*a[f]+a[f+1];if(nf<0n)throw Error('Segundas diferencias inconsistentes');if(nf>0n)out.push([f,nf])}return out}
function pct(a,b,dec=8){const scale=10n**BigInt(dec);let x=(100n*a*scale)/b;return (x/scale).toString()+','+(x%scale).toString().padStart(dec,'0')+' %'}
function showDist(){guarded('dist-result',()=>{let ell=Number($('dist-ell').value);if(!Number.isInteger(ell)||ell<0||ell>5000)throw Error('Longitud entre 0 y 5000');let m=10n**BigInt(ell),rows=multi(ell),total=rows.reduce((a,[f,v])=>a+v,0n),amb=rows.filter(([f])=>f>1).reduce((a,[f,v])=>a+BigInt(f)*v,0n);
let r=`<div class="metrics">${metric(fmt(m),'Palabras totales')}${metric(fmt(total),'Fibras distintas')}${metric(fmt(amb),'Palabras ambiguas')}${metric(fiberMax(ell),'Máximo tamaño de fibra')}</div>`;
r+=`<div class="result"><strong>Ambigüedad de esta longitud:</strong> ${pct(amb,m,10)} de las palabras; pares adyacentes E₁=${fmt(E(ell,1))}; número de clases = 10^ℓ − E₁.</div>`;
r+=`<div class="tablewrap"><table class="table"><thead><tr><th>Tamaño f</th><th>Número exacto de fibras</th><th>Palabras en esas fibras</th><th>Proporción entre palabras</th></tr></thead><tbody>${rows.map(([f,n])=>`<tr><td>${f}</td><td>${fmt(n)}</td><td>${fmt(BigInt(f)*n)}</td><td>${pct(BigInt(f)*n,m,9)}</td></tr>`).join('')}</tbody></table></div>`;
output('dist-result',r)})}
function showMod(){guarded('mod-result',()=>{let w=checkWord($('mod-word').value),raw=$('M-in').value.trim();if(!/^\d+$/.test(raw))throw Error('M debe ser entero positivo');let M=BigInt(raw);if(M<=0n)throw Error('M debe ser positivo');let ell=w.length,m=10n**BigInt(ell),K=key(w),r=mod(K,M),g=gcd(9n,M),Q=M/g;let v=BigInt(w||'0'),effective=v%Q,num=effective>=m?0n:1n+(m-1n-effective)/Q;
let rhtml=`<div class="metrics">${metric(String(r),'K mod M')}${metric(fmt(Q),'Módulo efectivo Q')}${metric(fmt(num),'Palabras compatibles')}${metric(Q>=m?'Sí':'No','Inyectividad uniforme en Σ^ℓ')}</div>`;
let ws=[];for(let i=0n;i<2n&&i<num;i++){let vv=effective+i*Q;ws.push(vv.toString().padStart(ell,'0'))}
rhtml+=`<div class="result"><strong>Estado:</strong> ${num===0n?'INCONSISTENT':num===1n?'UNIQUE':'NOT_IDENTIFIABLE'}.<div class="math">gcd(9,M) = ${g}
Q = M / gcd(9,M) = ${Q}
val(w) ≡ ${effective} (mod ${Q})
Módulo suficiente para todo Σ^ℓ ⇔ Q ≥ 10^${ell} (${m}).</div>${ws.length?`<p><strong>Testigos:</strong> ${ws.map(s=>`<code>${preview(s)}</code>`).join(' · ')}</p>`:''}</div>`;
output('mod-result',rhtml)})}
function test(){let asserts=[];const chk=(cond,name)=>{if(!cond)throw Error('Falló: '+name);asserts.push(name)};
chk(key('02')===782n,'02 literal');chk(key('889')===-1n,'889');chk(key('927')===-343n,'927');chk(encode('927').j===1,'j correcto');chk(decode(-1n,3,0)==='889','inversor');chk(fiberMax(1000)===395,'1000 cifras');chk(E(6,1)===2915n,'E1');chk(E(6,2)===8n,'E2');let d=multi(6);chk(d.length===3&&d[0][1]===994178n&&d[1][1]===2899n&&d[2][1]===8n,'distribución');chk(gcd(999n,9n)===9n,'módulo 999');chk(boundedSize(8n,1000)===197913,'longitud acotada');return asserts.length}
window.FST13={key,primitive,fiberSize,fiberMax,decode,encode,E,multi,gcd,test};
document.querySelectorAll('.nav button').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));document.querySelectorAll('section.section').forEach(s=>s.classList.remove('active'));button.classList.add('active');$(button.dataset.target).classList.add('active')}));
$('run-word').onclick=showWord;$('run-inverse').onclick=showInverse;$('run-dist').onclick=showDist;$('run-mod').onclick=showMod;
try{$('selftest').textContent=test()+' autotests internos superados'}catch(e){$('selftest').textContent=e.message;$('selftest').style.background='#ffeeee'}
showWord();showInverse();showDist();showMod();
