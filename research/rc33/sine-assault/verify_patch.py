"""Exact reconstruction from the declared fifteen-family sine threshold model."""
from fractions import Fraction as F
from pathlib import Path
import csv,json,platform
import exact_inverse as E
from validate_sine_patch import verify as old_verify
R=Path(__file__).resolve().parent
M=[1,3,8,11,14,15,17,19,24,33,100,180,200,240,300]
config={'domain':'dimensionless exact phase/threshold arithmetic; beta in degrees, x in radians',
 'equations':['x_mn=pi*m/(1800000*10^n)','tau_mn=10^(3*n+10)*(x_mn-sin(x_mn))','b_m(xi)=1_{frac(m*xi)<tau_mn}','K(w)=8*10^7-9*val(w)'],
 'pi_identity':'pi=16*atan(1/5)-4*atan(1/239)','atan_terms':40,
 'A':'10^10*(pi*m/1800000)^3/6','B':'10^10*(pi*m/1800000)^5/120',
 'parameters':{'m':M,'beta_degrees':'m/10000','n':'all n>=0 by uniform Taylor enclosures','scale':10**10,'radian_denominator':1800000,'word_digits':7,'erased_prime':7,'phase_depths':[7,8,9]},'python':platform.python_version()}
print('CONFIG BEFORE CALCULATION:',json.dumps(config),flush=True)
def atan_bracket(inv):
 s=sum((F((-1)**k,(2*k+1)*inv**(2*k+1)) for k in range(40)),F(0));t=F(1,81*inv**81)
 return s,s+t
la,ha=atan_bracket(5);lb,hb=atan_bracket(239);pl,ph=16*la-4*hb,16*ha-4*lb
assert F(157,50)<pl<ph<F(22,7)
bounds={}
for m in M:
 xlo,xhi=pl*m/1800000,ph*m/1800000
 lo=10**10*(xlo**3/6-xhi**5/120);hi=10**10*xhi**3/6
 assert 0<lo<hi<1 and xhi<1;bounds[m]=(lo,hi)
rows=list(csv.DictReader((R/'inputs/15_PALABRAS_CRITICAS_VERIFICADAS.csv').open(newline='')));assert [int(r['m']) for r in rows]==M
checks=[]
for row in rows:
 m=int(row['m']);w=row['word'];assert len(w)==7 and w.isascii() and w.isdigit() and F(row['beta'])==F(m,10000)
 lo,hi=bounds[m];assert (lo*10**7).__floor__()==(hi*10**7).__floor__()==int(w)
 k=E.key(w);h=E.primitive(k,7);v=0;t=k
 while t%7==0:v+=1;t//=7
 assert k==int(row['K']) and h==int(row['h']) and E.fibre_count(h,7)==int(row['fiber_size'])==1
 assert k>58*10**6 and v<=1 and 343*k>8*10**7
 checks.append(dict(m=m,beta_degrees=row['beta'],word=w,K=k,h=h,v7=v,fibre_size=1,auxiliary_bits=0,threshold_interval=[str(lo),str(hi)]))
assert len({r['word'] for r in checks})==len({r['h'] for r in checks})==15 and len({r['word'][:6] for r in checks})<15
starts={F(j,m) for m in M for j in range(m)}
cuts=[dict(lo=x,hi=x,kind='start',families=[m for m in M if (m*x).denominator==1]) for x in starts]
for m in M:
 lo,hi=bounds[m];cuts.extend(dict(lo=(j+lo)/m,hi=(j+hi)/m,kind='end',families=[m]) for j in range(m))
cuts.append(dict(lo=F(1),hi=F(1),kind='sentinel',families=[]));cuts.sort(key=lambda c:c['lo'])
assert (len(starts),sum(M),len(cuts))==(756,1165,1922)
assert all(a['hi']<b['lo'] for a,b in zip(cuts,cuts[1:])), 'uniform cut envelopes overlap'
patterns=[]
for a,b in zip(cuts,cuts[1:]):
 x=(a['hi']+b['lo'])/2;p=''
 for m in M:
  u=m*x;u-=u.__floor__();lo,hi=bounds[m]
  if u<lo:p+='1'
  elif u>hi:p+='0'
  else:raise AssertionError(('undecided cell',x,m))
 patterns.append(p)
assert len(patterns)==1921 and len(set(patterns))==55
for left,right,c in zip(patterns,patterns[1:],cuts[1:-1]):
 changed={M[i] for i,(a,b) in enumerate(zip(left,right)) if a!=b};assert changed==set(c['families'])
 assert all((left[M.index(m)],right[M.index(m)])==(('0','1') if c['kind']=='start' else ('1','0')) for m in changed)
profiles=[]
for d in [7,8,9]:
 bins={};scale=10**d
 for i,c in enumerate(cuts[1:-1],1):
  a,b=c['lo']*scale,c['hi']*scale
  if c['lo']==c['hi'] and a.denominator==1:continue
  assert a.__floor__()==b.__floor__() and a.denominator!=1 and b.denominator!=1,('straddles grid',d,c)
  bins.setdefault(a.__floor__(),[]).append(i)
 states=coordinates=0;witnesses={}
 for prefix,ids in bins.items():
  local=patterns[ids[0]-1:ids[-1]+1];distinct=set(local);varying=sum(len({p[i] for p in distinct})>1 for i in range(15))
  if len(distinct)>states:states=len(distinct);witnesses['states']={'prefix':str(prefix).zfill(d),'patterns':local}
  if varying>coordinates:coordinates=varying;witnesses['coordinates']={'prefix':str(prefix).zfill(d),'patterns':local}
 profiles.append(dict(digits=d,max_interior_cuts=max(map(len,bins.values())),max_joint_states=states,uniform_auxiliary_bits=(states-1).bit_length(),max_ambiguous_coordinates=coordinates,witnesses=witnesses))
assert [(p['max_interior_cuts'],p['max_joint_states'],p['max_ambiguous_coordinates']) for p in profiles]==[(2,3,7),(1,2,7),(1,2,7)]
i,c=next((i,c) for i,c in enumerate(cuts) if c['lo']==c['hi']==F(1,3));shared=[3,15,24,33,180,240,300]
assert c['families']==shared and sum(a!=b for a,b in zip(patterns[i-1],patterns[i]))==7
third={'coordinate':'1/3','families':shared,'left_pattern':patterns[i-1],'right_pattern':patterns[i],'never_on_finite_decimal_grid':True}
dataset={'critical_words':[r['word'] for r in rows],'endpoint_intervals':[[str(c['lo']),str(c['hi'])] for c in cuts]};previous=old_verify(dataset)
assert [p['max_interior_boundaries_per_cylinder'] for p in previous['phase_profiles']]==[2,1,1] and previous['phase_profiles'][-1]['all_endpoints_in_distinct_prefixes']
five=[100,180,200,240,300];projected=sorted({''.join(p[M.index(m)] for m in five) for p in patterns});assert len(projected)==13
cert={'status':'PASS','configuration':config,'pi_interval':[str(pl),str(ph)],'critical_words':checks,'critical_words_distinct_at7_not6':True,
 'rational_starts':len(starts),'moving_cuts':sum(M),'endpoints_with_sentinel':len(cuts),'interior_cuts':len(cuts)-2,'open_cells':len(patterns),'joint_patterns':sorted(set(patterns)),
 'natural_five_families':five,'natural_five_patterns':projected,'phase_profiles':profiles,'one_third_witness':third,'old_consequence_checker':previous,
 'all_finite_k_ge8':{'max_cuts':1,'max_joint_states':2,'uniform_auxiliary_bits':1,'max_ambiguous_coordinates':7,'proof':'Refinement preserves upper bounds from depth8;1/3 remains an interior cut at every finite depth and flips seven coordinates.'},
 'scope':'Uniform for n>=0 in the explicitly reconstructed tau_mn model and every potential phase; no empirical pi-orbit distribution assertion.',
 'unprovided_historical_replay_not_claimed':['verify_patch.py','certificado_exacto.json','G0/G1/G2v0.4.1','original FST13 motor ZIP'],
 'other_state_counts':{'13':{'status':'reconstructed natural five-family projection','bits':4},'55':{'status':'reconstructed fifteen-family model','bits':6},'21':{'status':'conditional coding cost; doubled model not supplied','bits':5},'150':{'status':'conditional coding cost; two-step model not supplied','bits':8}}}
(R/'PHASE_DATASET.json').write_text(json.dumps(dataset,indent=2)+'\n');(R/'EXACT_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
(R/'CELL_PATTERNS.csv').write_text('cell,pattern\n'+''.join(f'{i},{p}\n' for i,p in enumerate(patterns)))
print(json.dumps({k:cert[k] for k in ['status','rational_starts','moving_cuts','endpoints_with_sentinel','interior_cuts','open_cells','other_state_counts']},indent=2))
print('PASS:15 singleton fibres;1922 envelopes;55 patterns; cuts2/1/1; extra bits2/1/1; seven simultaneous variable coordinates.')
