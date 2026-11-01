from pathlib import Path
import json,hashlib,shutil,datetime,subprocess,sys
B=Path('/workspace/explainer-videos');R=Path(__file__).parent;D=R/'en/Hook';S=B/'renders/qa/series/ai5/en/Hook_motion';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert shutil.disk_usage(B).free>=512*1024**2
assert not D.exists();D.mkdir(parents=True)
r=json.loads((S/'result.json').read_text());assert r['status']=='needs-review' and r['mode']=='motion'
p=B/r['movie'];h=sha(p);assert h=='0bc48a3c64fac28f12bed8210800ff34c98bf7cd3fb2d38da04a694507cc213c';assert p.stat().st_size==3241006
shutil.copyfile(p,D/'Hook.mp4');assert sha(D/'Hook.mp4')==h
files=[]
for name in ['result.json','text.jsonl','render.log']:
 p=S/name
 if p.exists():
  q=D/('original-'+name);shutil.copyfile(p,q);assert sha(p)==sha(q);files.append({'path':str(p),'frozen':str(q),'sha256':sha(q),'bytes':q.stat().st_size})
sources=[]
for rel in ['videos/ai/ai5/s01_hook.py','videos/ai/ai5/common.py','videos/ai/ai5/compute.py','videos/ai/ai5/manifest.py','videos/ai/ai5/cache_contract.py','videos/ai/ai5/zh_lines.py','videos/ai/ai5/narration_zh.json','videos/ai/ai_text_zh.json','explainer/ai/viz.py','explainer/analysis/__init__.py','explainer/lang.py','explainer/zh_templates.py','explainer/zh_text.py','tools/qa_series.py','tools/qa_motion.py']:
 p=B/rel;q=D/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert sha(p)==sha(q);sources.append({'path':rel,'snapshot':str(q),'sha256':sha(q),'bytes':q.stat().st_size})
assert sources[0]['sha256'].startswith('5a5f0dc5')
inputs=[]
for rel,old in r['inputs'].items():
 p=B/rel;q=D/'inputs'/rel;st=p.stat();q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert sha(p)==sha(q);inputs.append({'path':rel,'snapshot':str(q),'sha256':sha(q),'recorded_size_mtime_ns':old,'observed_size_mtime_ns':[st.st_size,st.st_mtime_ns],'metadata_matches':old==[st.st_size,st.st_mtime_ns]})
assert all(x['metadata_matches'] for x in inputs)
f={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case':'en/Hook','original_movie':str(B/r['movie']),'movie':str(D/'Hook.mp4'),'movie_sha256':h,'movie_bytes':3241006,'original_record_sha256':sha(S/'result.json'),'raw_status':r['status'],'raw_warnings':r['warnings'],'recorded_fingerprint':r['fingerprint'],'recorded_duration':r['duration'],'original_files':files,'sources':sources,'inputs':inputs,'scope':'Frozen actual silent movie/raw record/text/log and on-disk source/input identities. No assertion of historical imported-module equivalence; source-changed-during-render warning preserved.'}
(D/'freeze.json').write_text(json.dumps(f,indent=2)+'\n')
with (D/'audit.log').open('w') as log:
 rc=subprocess.run([sys.executable,str(B/'tools/qa_motion.py'),str(D/'Hook.mp4'),'-o',str(D/'audit'),'--dense','0.25','--max-gap','1'],cwd=B,stdout=log,stderr=subprocess.STDOUT).returncode
assert rc==0,(D/'audit.log').read_text()[-4000:]
sys.path.insert(0,str(B));from tools.qa_motion import sheets
ar=json.loads((D/'audit/result.json').read_text());unique=[];groups={};mapping=[]
for n,x in enumerate(ar['selected_frames']):
 h=x['sha256']
 if h not in groups:
  groups[h]=len(unique);unique.append({**x,'file':'../audit/'+x['file']})
 mapping.append({'selected_index':n,'source_frame':x['source_frame'],'time':x['time'],'sha256':h,'representative':groups[h],'page':groups[h]//8+1,'slot':groups[h]%8})
u=D/'unique';u.mkdir();pages=sheets(u,unique)
plan={'scope':'Exact PNG SHA256 grouping only within this movie; chronological first representatives. All representative pages require actual view receipts.','movie_sha256':f['movie_sha256'],'decoded_frames':ar['analysis']['decoded_frames'],'selected_times':len(ar['selected_frames']),'unique_pngs':len(unique),'pages':pages,'representative_frames':unique,'mapping':mapping,'max_selected_time_gap':ar['largest_selected_time_gap']}
(u/'review-plan.json').write_text(json.dumps(plan,indent=2)+'\n');(D/'views.json').write_text(json.dumps({'pages':[],'native':[]},indent=2)+'\n')
assert sha(D/'Hook.mp4')==f['movie_sha256'] and sha(S/'result.json')==f['original_record_sha256']
print(json.dumps({'decoded':plan['decoded_frames'],'selected':plan['selected_times'],'unique':plan['unique_pngs'],'pages':len(pages),'free_bytes':shutil.disk_usage(B).free},indent=2))
