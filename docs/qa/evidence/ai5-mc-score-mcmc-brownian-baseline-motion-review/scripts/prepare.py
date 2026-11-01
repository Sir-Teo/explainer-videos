from pathlib import Path
import datetime,fcntl,hashlib,json,os,shutil,signal,subprocess,sys,time
R=Path('/workspace/explainer-videos');O=Path(__file__).parent
LANG,SCENE=sys.argv[1:];MODULE={'MonteCarlo':'s13_montecarlo.py','ScoreFn':'s14_scorefn.py','MCMC':'s15_mcmc.py','Brownian':'s16_brownian.py'}[SCENE]
C=O/LANG/SCENE;S=R/'renders/qa/series/ai5'/LANG/(SCENE+'_motion');MIN=512*1024**2
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def disk():
 f=shutil.disk_usage(R).free
 if f<MIN:raise RuntimeError(f'Disk guard: {f}bytes<512MiB; no additional extraction')
 return f
assert disk()>=MIN
assert not C.exists(),f'Existing operation must be reconciled before retry: {C}'
d=json.loads((S/'result.json').read_text());assert d['mode']=='motion' and d['status'] in ['passed','needs-review']
assert d['movie'] and d['inputs'];movie=R/d['movie'];movie_h=sha(movie)
C.mkdir(parents=True);witness=C/(SCENE+'.mp4');os.link(movie,witness);assert sha(witness)==movie_h
files=[]
for name in ['result.json','text.jsonl','render.log']:
 src=S/name
 if src.exists():
  dest=C/('original-'+name);shutil.copy2(src,dest);assert sha(src)==sha(dest);files.append({'path':str(src),'copy':str(dest),'sha256':sha(dest),'bytes':dest.stat().st_size})
sources=[]
for rel in ['videos/ai/ai5/'+MODULE,'videos/ai/ai5/common.py','videos/ai/ai5/compute.py','videos/ai/ai5/contracts.py','videos/ai/ai5/cache_contract.py','videos/ai/ai5/plotting.py','videos/ai/ai5/manifest.py','videos/ai/ai5/zh_lines.py','videos/ai/ai5/narration_zh.json','videos/ai/ai_text_zh.json','explainer/ai/viz.py','explainer/analysis/__init__.py','explainer/lang.py','explainer/zh_templates.py','explainer/zh_text.py','tools/qa_series.py','tools/qa_motion.py']:
 src=R/rel;h=sha(src);dest=O/'source-blobs'/(h+src.suffix);dest.parent.mkdir(exist_ok=True)
 if not dest.exists():shutil.copy2(src,dest)
 assert sha(dest)==h;sources.append({'path':rel,'copy':str(dest),'sha256':h,'bytes':src.stat().st_size})
inputs=[]
for rel,signature in d['inputs'].items():
 src=R/rel;st=src.stat();assert [st.st_size,st.st_mtime_ns]==signature
 inputs.append({'path':rel,'sha256':sha(src),'bytes':st.st_size,'size_mtime_ns':signature,'metadata_current':True})
frozen={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case':LANG+'/'+SCENE,'movie_original_path':str(movie),'movie_witness_hardlink':str(witness),'movie_sha256':movie_h,'movie_bytes':movie.stat().st_size,'movie_hardlink_same_inode':movie.stat().st_ino==witness.stat().st_ino,'raw_record_sha256':sha(S/'result.json'),'raw_status':d['status'],'raw_warnings':d['warnings'],'record_fingerprint':d['fingerprint'],'duration':d['duration'],'original_files':files,'source_observations':sources,'inputs':inputs,'limits':'Source/input observations bind bytes, not historical in-memory imports. Movie hardlink avoids duplicate storage; before/after hashes guard mutation. No full continuous/audio/native1080 approval.'}
(C/'freeze.json').write_text(json.dumps(frozen,indent=2)+'\n')
lock_path=Path('/workspace/runtime/ai4-tail-motion-review/extract.lock');lock_path.parent.mkdir(parents=True,exist_ok=True);lock=lock_path.open('a')
last_wait=time.monotonic()
while True:
 try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
 except BlockingIOError:
  disk()
  if time.monotonic()-last_wait>=30:print(json.dumps({'stage':'waiting-shared-extraction-lock','case':LANG+'/'+SCENE}),flush=True);last_wait=time.monotonic()
  time.sleep(.5)
start=time.monotonic()
with (C/'audit.log').open('w') as log:
 cmd=[sys.executable,str(R/'tools/qa_motion.py'),str(movie),'-o',str(C/'audit'),'--dense','0.25','--max-gap','1']
 proc=subprocess.Popen(cmd,cwd=R,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);last=time.monotonic()
 try:
  while proc.poll() is None:
   free=disk()
   if time.monotonic()-last>=30:print(json.dumps({'stage':'audit','case':LANG+'/'+SCENE,'pid':proc.pid,'elapsed':time.monotonic()-start,'free_bytes':free}),flush=True);last=time.monotonic()
   time.sleep(.5)
  assert proc.returncode==0,(C/'audit.log').read_text()[-3000:]
 except BaseException as exc:
  if proc.poll() is None:os.killpg(proc.pid,signal.SIGTERM);proc.wait()
  (C/'operation-stop.json').write_text(json.dumps({'stage':'audit','error':str(exc),'child_returncode':proc.returncode,'elapsed':time.monotonic()-start},indent=2)+'\n');raise
fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
assert sha(movie)==sha(witness)==movie_h;assert sha(S/'result.json')==frozen['raw_record_sha256']
sys.path.insert(0,str(R));from tools.qa_motion import sheets
ar=json.loads((C/'audit/result.json').read_text());groups={};reps=[];mapping=[]
for i,frame in enumerate(ar['selected_frames']):
 h=frame['sha256']
 if h not in groups:groups[h]=len(reps);reps.append({**frame,'file':'../audit/'+frame['file']})
 n=groups[h];mapping.append({'selected_index':i,'source_frame':frame['source_frame'],'time':frame['time'],'png_sha256':h,'representative':n,'page':n//8+1,'slot':n%8})
disk();u=C/'unique';u.mkdir();pages=sheets(u,reps)
plan={'scope':'Chronological first representatives grouped ONLY by exactPNG SHA256 withinthis movie. Every representative page requires actualview receipt.','movie_sha256':movie_h,'audit_sha256':sha(C/'audit/result.json'),'tool_sha256':ar['tool_sha256'],'decoded_frames':ar['analysis']['decoded_frames'],'selected_times':len(mapping),'unique_pngs':len(reps),'pages':pages,'representatives':reps,'mapping':mapping,'largest_selected_time_gap':ar['largest_selected_time_gap'],'settings':ar['settings']}
(u/'review-plan.json').write_text(json.dumps(plan,indent=2)+'\n');(C/'views.json').write_text(json.dumps({'pages':[],'native':[]},indent=2)+'\n')
print(json.dumps({'case':LANG+'/'+SCENE,'decoded':plan['decoded_frames'],'selected':len(mapping),'unique':len(reps),'pages':len(pages),'wall':time.monotonic()-start,'free_bytes':disk()},indent=2),flush=True)
