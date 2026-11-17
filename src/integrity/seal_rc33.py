"""Seal current replay outputs separately from the immutable archive manifest."""
from pathlib import Path
import hashlib
R=Path(__file__).resolve().parents[2]/'research/rc33'
archive=R/'SHA256SUMS_ARCHIVE_2026-11-16.txt'
paths=[line.split('  ',1)[1] for line in archive.read_text().splitlines() if line.strip()]
(R/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256((R/p).read_bytes()).hexdigest()}  {p}\n' for p in paths))
print(f'RC3.3 current manifest: {len(paths)} paths; original archive manifest preserved')
