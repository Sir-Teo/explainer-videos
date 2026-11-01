from pathlib import Path
import json,hashlib,gzip,datetime,os
R=Path('/workspace/explainer-videos');O=R/'docs/qa/evidence/ai5-mcmc-brownian-transition-regression';B=O.parent/'ai5-mc-score-mcmc-brownian-baseline-motion-review';assert O.exists()and not(O/'manifest.json').exists();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();refs=[]
for folder in ['native','sources']:
 for p in sorted((O/folder).iterdir()):
  q=B/folder/p.name
  if not q.exists():continue
  assert sha(p)==sha(q)
  refs.append({'omitted_duplicate_path':str(p.relative_to(O)),'reused_path':os.path.relpath(q,O),'sha256':sha(q),'bytes':q.stat().st_size,'basis':'Exact file SHA256 equality; runtime original and earlier bounded package payload retained.'})
  p.unlink()
assert refs
(O/'exact-payload-reuse.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_manifest_sha256':sha(B/'manifest.json'),'reused_payloads':refs,'scope':'Only byte-identical duplicate copies omitted from this new unpublished package; no runtime originals or earlier evidence modified.'},indent=2)+'\n')
p=O/'README.md';s=p.read_text();s=s.replace('every changed contact sheet, critical native views,','every changed contact sheet, critical native views (with exact existing payload reuse listed in `exact-payload-reuse.json`),');s=s.replace('of125.8–128.4','of 125.8–128.4').replace('covered80 frame times and39','covered 80 frame times and 39').replace('density.39','density. 39').replace('viewed.39','viewed. 39').replace('pages.39','pages. 39').replace('of40 same-time','of 40 same-time').replace('in12 pixels','in 12 pixels').replace('native1080 motion,4K','native 1080 motion, 4K');p.write_text(s)
p=O/'report.json';d=json.loads(p.read_text());d['package_exact_existing_payload_reuse']={'receipt':'exact-payload-reuse.json','count':len(refs),'bytes_avoided':sum(x['bytes']for x in refs)};p.write_text(json.dumps(d,indent=2)+'\n')
for src in [Path(__file__),Path(__file__).parent/'package.py']:
 dest=O/'scripts'/src.name;dest.write_bytes(src.read_bytes())
payload=[]
for p in sorted(O.rglob('*')):
 if p.is_file():payload.append({'path':str(p.relative_to(O)),'sha256':sha(p),'bytes':p.stat().st_size})
size=sum(x['bytes']for x in payload);assert size<=12*1024**2,size
(O/'manifest.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'payload_bytes':size,'payloads':payload,'scope':'Bounded image/provenance package; all changed sheets included, byte-identical earlier payload reuse explicit. No MP4 or raw cache payload.'},indent=2)+'\n')
for x in payload:
 p=O/x['path'];assert sha(p)==x['sha256']and p.stat().st_size==x['bytes']
 if p.suffix=='.gz':gzip.decompress(p.read_bytes())
for x in refs:assert sha(O/x['reused_path'])==x['sha256']
print(json.dumps({'path':str(O),'payloads':len(payload),'bytes':size,'manifest_sha256':sha(O/'manifest.json'),'reused_exact_payloads':len(refs),'reused_bytes':sum(x['bytes']for x in refs)},indent=2))
