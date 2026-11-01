from pathlib import Path
import json,hashlib,shutil,datetime,subprocess,sys
B=Path('/workspace/explainer-videos');R=Path(__file__).parent;lang,scene=sys.argv[1:3];assert lang in ['en','zh'] and scene in ['MCMC','Brownian'];D=R/lang/scene;S=B/f'renders/qa/series/ai5/{lang}/{scene}_motion';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert shutil.disk_usage(B).free>=512*1024**2
assert not D.exists()
r=json.loads((S/'result.json').read_text());assert r['status'] in ['passed','needs-review'] and r['mode']=='motion'
base=B.parent/'runtime/ai5-mc-score-mcmc-brownian-motion-review'/lang/scene
oldfreeze=json.loads((base/'freeze.json').read_text());assert sha(B/r['movie'])!=oldfreeze['movie_sha256'],'canonicalmovieisstillbaseline:waitforrootcompletion'
repair=B.parent/('runtime/ai5-mcmc-copy-transition-repair' if scene=='MCMC' else 'runtime/ai5-brownian-copy-transition-repair')/'freeze.json';assert (S/'result.json').stat().st_mtime>repair.stat().st_mtime,'rawrecordpredatesrepairfreeze'
D.mkdir(parents=True)
p=B/r['movie'];h=sha(p);moviebytes=p.stat().st_size
shutil.copyfile(p,D/f'{scene}.mp4');assert sha(D/f'{scene}.mp4')==h
files=[]
for name in ['result.json','text.jsonl','render.log']:
 p=S/name
 if p.exists():
  q=D/('original-'+name);shutil.copyfile(p,q);assert sha(p)==sha(q);files.append({'path':str(p),'frozen':str(q),'sha256':sha(q),'bytes':q.stat().st_size})
sources=[]
for rel in [f"videos/ai/ai5/{'s15_mcmc' if scene=='MCMC' else 's16_brownian'}.py",'videos/ai/ai5/common.py','videos/ai/ai5/compute.py','videos/ai/ai5/manifest.py','videos/ai/ai5/cache_contract.py','videos/ai/ai5/zh_lines.py','videos/ai/ai5/narration_zh.json','videos/ai/ai_text_zh.json','explainer/ai/viz.py','explainer/analysis/__init__.py','explainer/lang.py','explainer/zh_templates.py','explainer/zh_text.py','tools/qa_series.py','tools/qa_motion.py']:
 p=B/rel;q=D/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert sha(p)==sha(q);sources.append({'path':rel,'snapshot':str(q),'sha256':sha(q),'bytes':q.stat().st_size})
assert sources[0]['sha256']==({'MCMC':'95c38c1d058a07556f26dd86fd042dbdba8e137ff4083ea9350cbd0f919655af','Brownian':'780521544fd9ad5e9ab698bfeba6c8da2aa82b24b17433a93623dca69c444e9f'}[scene])
inputs=[]
for rel,old in r['inputs'].items():
 p=B/rel;st=p.stat();inputs.append({'path':rel,'snapshot':'hash-only-no-raw-cache-duplicate','sha256':sha(p),'recorded_size_mtime_ns':old,'observed_size_mtime_ns':[st.st_size,st.st_mtime_ns],'metadata_matches':old==[st.st_size,st.st_mtime_ns]})
assert all(x['metadata_matches'] for x in inputs)
f={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case':f'{lang}/{scene}','original_movie':str(B/r['movie']),'movie':str(D/f'{scene}.mp4'),'movie_sha256':h,'movie_bytes':moviebytes,'original_record_sha256':sha(S/'result.json'),'raw_status':r['status'],'raw_warnings':r['warnings'],'recorded_fingerprint':r['fingerprint'],'recorded_duration':r['duration'],'original_files':files,'sources':sources,'inputs':inputs,'scope':'Frozen actual silent-mode movie/raw record/text/log and on-disk source/input identities. No assertion of historical imported-module equivalence; all original warnings preserved.'}
(D/'freeze.json').write_text(json.dumps(f,indent=2)+'\n')
import fcntl,time,os,signal
lock=open('/workspace/runtime/ai4-tail-motion-review/extract.lock','a')
while True:
 try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
 except BlockingIOError:
  assert shutil.disk_usage(B).free>=512*1024**2
  time.sleep(.5)
with (D/'audit.log').open('w') as log:
 proc=subprocess.Popen([sys.executable,str(B/'tools/qa_motion.py'),str(D/f'{scene}.mp4'),'-o',str(D/'audit'),'--dense','0.25','--max-gap','1'],cwd=B,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 started=time.monotonic();last=started
 while proc.poll() is None:
  if shutil.disk_usage(B).free<512*1024**2:os.killpg(proc.pid,signal.SIGTERM);proc.wait();raise RuntimeError('diskbelow512MiB:auditstopped')
  if time.monotonic()-last>30:print(json.dumps({'stage':'audit','case':lang+'/'+scene,'pid':proc.pid,'seconds':time.monotonic()-started,'free_bytes':shutil.disk_usage(B).free}),flush=True);last=time.monotonic()
  time.sleep(.5)
 rc=proc.returncode
fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
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
assert sha(D/f'{scene}.mp4')==f['movie_sha256'] and sha(S/'result.json')==f['original_record_sha256']
print(json.dumps({'case':f'{lang}/{scene}','decoded':plan['decoded_frames'],'selected':plan['selected_times'],'unique':plan['unique_pngs'],'pages':len(pages),'free_bytes':shutil.disk_usage(B).free},indent=2))
