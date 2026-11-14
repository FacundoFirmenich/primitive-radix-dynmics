from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[2]
claims=list(csv.DictReader((ROOT/'data/claims.csv').open(encoding='utf-8', newline='')))
deps=list(csv.DictReader((ROOT/'data/dependencies.csv').open(encoding='utf-8', newline='')))
arts=list(csv.DictReader((ROOT/'data/artifacts.csv').open(encoding='utf-8', newline='')))
back={c['claim_id']:[] for c in claims}
for e in deps: back[e['source']].append(f"{e['relation']}:{e['target']}")
rows=['# Claim-to-evidence traceability','', '| ID | Status | Claim | Primary evidence | Dependencies |','|---|---|---|---|---|']
for c in claims:
    rows.append('| {claim_id} | `{status}` | {claim} | `{primary_evidence}` | {deps} |'.format(**c,deps='<br>'.join(back[c['claim_id']]) or '—'))
rows += ['','## Artifact registry','', '| ID | Type | Path | Supports |','|---|---|---|---|']
for a in arts: rows.append(f"| {a['artifact_id']} | `{a['type']}` | `{a['path']}` | {a['supports_claims']} |")
out=ROOT/'outputs/reports/claim_traceability.md'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text('\n'.join(rows)+'\n',encoding='utf-8'); print(out)
