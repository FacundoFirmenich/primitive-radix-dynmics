from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[2]; mf=ROOT/'outputs/checksums/SHA256SUMS.txt'; bad=[]; n=0
for line in mf.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    h,rel=line.split('  ',1);p=ROOT/rel;n+=1
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=h: bad.append(rel)
print(f'validated={n} bad={len(bad)}');
for x in bad: print('BAD',x)
raise SystemExit(1 if bad else 0)
