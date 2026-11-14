from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'outputs'; manifest=OUT/'checksums/SHA256SUMS.txt'; manifest.parent.mkdir(parents=True,exist_ok=True)
files=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p!=manifest and not p.name.endswith('.bin'):
        h=hashlib.sha256(p.read_bytes()).hexdigest(); files.append((h,p.relative_to(ROOT).as_posix()))
manifest.write_text(''.join(f'{h}  {p}\n' for h,p in files),encoding='utf-8');print(f'sealed={len(files)} manifest={manifest}')
