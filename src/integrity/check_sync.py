"""Cross-check metadata, claim evidence and immutable canonical alignment."""
from pathlib import Path
import csv,hashlib,json,re,tomllib
R=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((R/p).read_text())
def rows(p):
 with (R/p).open(newline='') as f:return list(csv.DictReader(f))
def check(ok,msg):
 if not ok:raise AssertionError(msg)
repo='https://github.com/FacundoFirmenich/primitive-radix-mobius-dynamics'
meta=read('metadata/PUBLICATION_STATE.json');doi=read('metadata/DOI_STATUS.json')
check(meta['repository']==repo and meta['version']=='RC3.3','current publication metadata')
check(meta['manuscript_embargo']=='ACTIVE' and not meta['manuscript_in_repository'],'publication boundary metadata')
check(doi['doi']=='10.5281/zenodo.24270311' and doi['archival_commit']=='7d94e81d06944f36640ab289b87473fc0292c6df','immutable archive scope')
check(not meta['current_continuation_archived_under_that_doi'],'continuation archival scope')
check((R/'VERSION').read_text().strip()=='RC3.3','scientific version')
package=tomllib.loads((R/'pyproject.toml').read_text())['project']
check(package['name']=='primitive-radix-mobius-dynamics' and package['version']=='0.3.3','package metadata')
check(read('codemeta.json')['codeRepository']==repo,'CodeMeta URL')
check(read('research/rc33/REPOSITORY_STATUS.json')['DOI']==doi['doi'],'RC3.3 DOI metadata')
oriented=rows('research/five-state/continuation/ORIENTED_STATUS.csv')
from collections import Counter
check(Counter(r['status'] for r in oriented)=={'EXCLUDED':37,'REALIZED_CONTAINING':1,'OPEN':2},'37/1/2 oriented frontier')
check({(r['form'],r['strict_letter'],r['factor']) for r in oriented if r['status']=='OPEN'}=={('DF015-0003','S','2'),('DF015-0007','T','3')},'open-row identifiers and factors')
claims=rows('data/claims.csv');ids=[c['claim_id'] for c in claims];check(len(set(ids))==len(ids),'duplicate claim identifiers')
new=read('research/rc33/recent/CLAIMS.json')['claims'];check(len(new)==24,'24 continuation claims')
text=(R/'research/rc33/recent/RESULTS.md').read_text()
for card in new:
 check(card['id'] in ids and f"## {card['id']}\n" in text,card['id']+' evidence anchor')
 c=next(c for c in claims if c['claim_id']==card['id'])
 path,anchor=c['primary_evidence'].split('#')
 check((R/path).exists() and anchor==card['id'].lower(),card['id']+' primary evidence')
for row in rows('data/dependencies.csv'):
 check(row['source'] in ids and row['target'] in ids,'missing claim dependency endpoint')
manifest=read('research/rc33/recent/SOURCE_MANIFEST.json')['files'];check(len(manifest)==31,'31 immutable imports')
for item in manifest:check(sha(R/item['public_path'])==item['sha256'],item['public_path'])
align=read('metadata/CANONICAL_ALIGNMENT.json')
for name,h in align['figure_assets'].items():
 check(sha(R/'outputs/figures'/name)==h,name+' approved output')
 check(sha(R/'research/rc33/recent/figure-assets'/name)==h,name+' source')
for lang in ['EN','ES']:
 p=R/f'outputs/interactive/rc33_epistemic_{lang}.html';html=p.read_text()
 for path in re.findall(r'<img[^>]*src="([^"]+)"',html):check((p.parent/path).exists(),path)
graph=read('outputs/interactive/epistemic_graph.json');nodes=[n['id'] for n in graph['nodes']]
check(len(nodes)==len(set(nodes)),'duplicate graph nodes')
check(set(ids)<set(nodes),'graph contains all claims')
for e in graph['edges']:check(e['source'] in nodes and e['target'] in nodes,'graph edge endpoint')
# The current RC3.3 manifest is distinct from the unchanged original archive list.
entries=0
for line in (R/'research/rc33/SHA256SUMS.txt').read_text().splitlines():
 h,p=line.split('  ',1);check(sha(R/'research/rc33'/p)==h,p+' current RC3.3 manifest');entries+=1
recent=read('outputs/reports/recent/RUN_MANIFEST.json')
check(recent['status']=='PASS' and len(recent['runs'])==10,'ten recent replays')
check(recent['new_full_T5000_run'] is False,'full census scope')
fst=read('research/rc33/fst11/CLAIMS.json')['claims']
check(len(fst)==5,'five FST11 claims')
for c in fst:check(c['id'] in ids and (R/c['public_evidence'].split('#')[0]).is_file(),c['id']+' FST11 evidence')
fst_run=read('outputs/reports/fst11/RUN_MANIFEST.json')
check(fst_run['status']=='PASS' and fst_run['source_engine_byte_identical'],'FST11 exact replay')
for path,h in fst_run['input_hashes_before'].items():check(sha(R/path)==h,path+' FST11 source hash')
t007=read('research/rc33/t007/CLAIMS.json')['claims']
check(len(t007)==7,'seven T007 claim cards')
for c in t007:check(c['id'] in ids and (R/c['public_evidence'].split('#')[0]).is_file(),c['id']+' T007 evidence')
r007=read('outputs/reports/t007/RUN_MANIFEST.json')
check(r007['status']=='PASS' and r007['good_primes']==43 and r007['coefficient_norm_improvement_factor']==172,'T007 exact replay')
for path,h in r007['input_hashes_before'].items():check(sha(R/path)==h,path+' T007 source hash')
fst13=read('research/rc33/fst1213/CLAIMS.json')['claims']
check(len(fst13)==9,'nine FST12/13 scoped cards')
for c in fst13:check(c['id'] in ids and (R/c['public_evidence'].split('#')[0]).is_file(),c['id']+' FST12/13 evidence')
r13=read('outputs/reports/fst1213/RUN_MANIFEST.json')
check(r13['status']=='PASS' and r13['run']['status']=='completed','FST12/13 completed exact replay')
for a in r13['input_artifacts']:check(sha(R/'research/rc33/fst1213'/a['path'])==a['sha256']==a['sha256_after'],a['path']+' FST12/13 source hash')
fst14=read('research/rc33/fst14/CLAIMS.json')['claims']
check(len(fst14)==4,'four FST14 scoped cards')
for c in fst14:check(c['id'] in ids and (R/c['public_evidence'].split('#')[0]).is_file(),c['id']+' FST14 evidence')
r14=read('outputs/reports/fst14/RUN_MANIFEST.json')
check(r14['status']=='PASS' and r14['run']['status']=='completed','FST14 exact replay')
for a in r14['input_artifacts']:check(sha(R/'research/rc33/fst14'/a['path'])==a['sha256']==a['sha256_after'],a['path']+' FST14 source hash')
receipt={'status':'PASS','edition':'RC3.3','package_version':'0.3.3','repository':repo,
         'claims':len(ids),'continuation_claims':len(new)+len(fst)+len(t007)+len(fst13)+len(fst14),'FST14_claims':len(fst14),'FST1213_claims':len(fst13),'T007_claims':len(t007),'FST11_claims':len(fst),'dependency_edges':len(rows('data/dependencies.csv')),
         'immutable_source_files':len(manifest),'aligned_figure_assets':len(align['figure_assets']),
         'current_rc33_checksum_entries':entries,'recent_scripts_passed':len(recent['runs']),
         'original_archive_commit':doi['archival_commit'],'full_manuscripts_public':False,
         'new_global_existence_rows_closed':0}
p=R/'outputs/reports/synchronization_audit.json';p.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
