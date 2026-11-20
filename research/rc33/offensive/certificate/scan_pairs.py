from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,time,hashlib,os,platform
from paired_fibres import paired
from fibre_arithmetic import ArithmeticDeferred

ROOT=Path(__file__).resolve().parent
os.nice(10)
source=ROOT/'PAIR_CONTEXTS_SNAPSHOT.jsonl'
before=hashlib.sha256(source.read_bytes()).hexdigest()
contexts=[json.loads(line) for line in source.read_text().splitlines()]
print('BEFORE: exact paired completion; r=3 reflected; AC fixes (D,Q), DQ fixes (A,C); input',str(source),'sha256',before,'contexts',len(contexts),'; no extra height cutoff inside each fixed-pair fibre; complete all original core and E/CRT/ten-edge checks. Python',platform.python_version(),flush=True)
started=datetime.now(timezone.utc).isoformat();tic=time.monotonic();counts=Counter();cores={};hits={};deferred=[]
with (ROOT/'PAIR_CONTEXT_RESULTS.jsonl').open('w') as out:
    for i,ctx in enumerate(contexts,1):
        try:
            z=paired(ctx['r'],ctx['orientation'],ctx['unknown'],ctx['fixed'])
        except ArithmeticDeferred as e:
            deferred.append(dict(context=ctx,reason=str(e)))
            continue
        counts['contexts']+=1
        for k in ['cartesian_pairs','first_residue_pairs','second_residue_pairs','joint_pairs']:
            counts[k]+=z[k]
        for x in z['square_cores']:
            cores[tuple(x)]=dict(core=x,context=ctx)
        for hit in z['realizations']:
            hits[(*hit['core'],hit['E'])]=dict(hit=hit,context=ctx)
            print('PAIR_VERIFIED_REALIZATION',json.dumps(hit),flush=True)
        if z['joint_pairs'] or z['square_cores'] or z['realizations']:
            out.write(json.dumps(z)+'\n');out.flush()
        if i%5000==0:print('PAIR_SCAN_PROGRESS',i,dict(counts),'cores',len(cores),'seconds',round(time.monotonic()-tic,3),flush=True)
assert before==hashlib.sha256(source.read_bytes()).hexdigest()
result=dict(status='PASS' if not deferred else 'PARTIAL_WITH_DEFERRED',started_at=started,seconds=time.monotonic()-tic,input_sha256=before,declared_contexts=len(contexts),counts=dict(counts),square_cores=list(cores.values()),realizations=list(hits.values()),deferred=deferred,scope='Exact completion of the selected opposite-coordinate fibres only. Candidate-generation history is not independently replayed; no global nonexistence claim.')
(ROOT/'PAIR_SCAN_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PAIR_SCAN_FINISHED',json.dumps(result),flush=True)
