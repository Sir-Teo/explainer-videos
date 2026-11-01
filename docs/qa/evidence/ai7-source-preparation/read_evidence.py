#!/usr/bin/env python3
"""Read exact archived bytes: python read_evidence.py OWNER ORIGINAL_RELATIVE_PATH."""
from pathlib import Path
import sys,json,gzip,hashlib
root=Path(__file__).resolve().parent
if len(sys.argv)!=3:
    raise SystemExit(__doc__)
owner, name=sys.argv[1:]
if owner not in {p.name for p in (root/'owners').iterdir() if p.is_dir()}:
    raise SystemExit('unknown owner')
rows=json.loads((root/'owners'/owner/'index.json').read_text())['files']
row=next((x for x in rows if x['original_relative_path']==name),None)
if row is None:
    raise SystemExit('unknown original relative path')
path=root/'objects'/(row['original_sha256']+'.gz')
raw=gzip.decompress(path.read_bytes())
assert len(raw)==row['original_bytes'] and hashlib.sha256(raw).hexdigest()==row['original_sha256']
sys.stdout.buffer.write(raw)
