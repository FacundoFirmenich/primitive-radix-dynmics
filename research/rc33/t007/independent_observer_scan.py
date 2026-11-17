from pathlib import Path
from math import comb
import numpy as np,json,time,platform
R=Path(__file__).resolve().parent
config={'arithmetic':'exact unsigned 16-bit arrays; provable bound comb(20,6)=38760<65536','equations':'S(wx)=S(w)*(1+x); append-Y selective probe adds N_w(XXXXX)','universe':'every binary word at each n=16..20','max_n':20,'numpy':np.__version__,'python':platform.python_version(),'zero-truncation_bound':comb(20,6),'memory_policy':'one prefix level; exact byte-record sorting; no hashes of signatures'}
print('CONFIGURATION BEFORE COMPUTATION\n'+json.dumps(config,indent=2),flush=True)
assert np.dtype(np.uint16).itemsize==2 and comb(20,6)<2**16
level=np.ones((1,63),dtype=np.uint16);level[:,1:]=0;probe=np.zeros(1,dtype=np.uint16);rows=[];start=time.monotonic()
for n in range(1,21):
 nxt=np.repeat(level,2,axis=0);q=np.repeat(probe,2)
 for i in range(31):
  nxt[0::2,2*i+1]+=level[:,i];nxt[1::2,2*i+2]+=level[:,i]
 q[1::2]+=level[:,31]
 level,probe=nxt,q
 if n>=16:
  a=np.ascontiguousarray(level[:,1:]);keys=a.view(np.dtype((np.void,a.dtype.itemsize*a.shape[1]))).reshape(-1)
  uniq,inv,counts=np.unique(keys,return_inverse=True,return_counts=True)
  repeated=np.flatnonzero(counts[inv]>1);buckets={}
  for i in repeated:buckets.setdefault(int(inv[i]),[]).append(int(probe[i]))
  assert all(len(x)==len(set(x)) for x in buckets.values())
  expected={16:65534,17:131064,18:262120,19:524212,20:1048360};assert len(uniq)==expected[n]
  row={'n':n,'histories':2**n,'O5_classes':len(uniq),'augmented_classes':2**n,'ambiguous_O5_fibres':len(buckets),'duplicate_O5_rows':len(repeated)};rows.append(row);print(row,flush=True)
  del a,keys,uniq,inv,counts,repeated,buckets
(R/'INDEPENDENT_OBSERVER_SCAN.json').write_text(json.dumps({'status':'PASS','config':config,'rows':rows,'runtime_seconds':time.monotonic()-start},indent=2)+'\n')
