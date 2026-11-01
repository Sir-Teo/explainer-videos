import sys,json,hashlib,datetime
from pathlib import Path
plan=Path(sys.argv[1]);indices=[int(x) for x in sys.argv[2].split(',')];observation=sys.argv[3];out=plan.parent/'review-progress.json';d=json.loads(plan.read_text());r=json.loads(out.read_text()) if out.exists() else {'scope':'Actual native854x480 images on unscaled1708px chronological contact sheets; no continuous perceptual playback/listening.','plan':str(plan),'plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'viewed_pages':{},'findings':[]}
for number in indices:
 p=d['pages'][number-1];assert hashlib.sha256(Path(p['file']).read_bytes()).hexdigest()==p['sha256'];r['viewed_pages'][str(number)]={**p,'actually_viewed':True,'observations':observation,'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
out.write_text(json.dumps(r,indent=2));print('viewed',len(r['viewed_pages']),'of',len(d['pages']))
