import datetime,hashlib,json,shutil
from pathlib import Path
R=Path('/workspace/explainer-videos');O=Path(__file__).parent
SCENES={'MonteCarlo':'s13_montecarlo.py','ScoreFn':'s14_scorefn.py','Brownian':'s16_brownian.py'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p,kind):
 h=sha(p);out=O/kind/(h+p.suffix);out.parent.mkdir(exist_ok=True)
 if not out.exists():shutil.copy2(p,out)
 assert sha(out)==h
 return {'original_path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':h,'copy':str(out.relative_to(O))}
for lang in ['en','zh']:
 for scene,module in SCENES.items():
  p=R/'renders/qa/series/ai5'/lang/scene;record=p/'result.json'
  if not record.is_file():continue
  d=json.loads(record.read_text());names=['result.json','text.jsonl','render.log','sheet.png']+[f['file'] for f in d['frames']]
  if not all((p/n).is_file() for n in names):continue
  key=f'{lang}-{scene}-{sha(record)[:16]}';dest=O/'cases'/key
  if dest.exists():continue
  dest.mkdir(parents=True)
  files=[]
  for n in names:
   shutil.copy2(p/n,dest/n);files.append({'path':n,'sha256':sha(dest/n),'bytes':(dest/n).stat().st_size})
  assert sha(record)==sha(dest/'result.json')
  sources=[blob(R/'videos/ai/ai5'/module,'source-blobs')]
  for q in ['videos/ai/ai5/common.py','videos/ai/ai5/zh_lines.py','videos/ai/ai_text_zh.json','explainer/ai/viz.py','videos/ai/ai5/plotting.py','tools/qa_series.py','manim.cfg']:
   sources.append(blob(R/q,'source-blobs'))
  inputs=[]
  for q,signature in d['inputs'].items():
   item=blob(R/q,'input-blobs');item['record_signature']=signature
   st=(R/q).stat();item['signature_current']=[st.st_size,st.st_mtime_ns]==signature;inputs.append(item)
  receipt={'scene':scene,'lang':lang,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_fingerprint':d['fingerprint'],'raw_status':d['status'],'raw_warnings':d['warnings'],'duration':d['duration'],'frames':len(d['frames']),'copied_files':files,'source_observations':sources,'inputs':inputs,'limits':'Source bytes observed at snapshot, not proof of historical in-memory imports. Endpoint images only; no full motion, continuous playback, audio, native1080 or production approval.'}
  (dest/'freeze.json').write_text(json.dumps(receipt,indent=2)+'\n')
  print(key,len(d['frames']),d['status'],d['warnings'],all(x['signature_current'] for x in inputs))
