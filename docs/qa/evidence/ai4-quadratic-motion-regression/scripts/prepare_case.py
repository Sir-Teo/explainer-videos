from pathlib import Path
import argparse,json,hashlib,shutil,subprocess,os,sys,datetime
P=argparse.ArgumentParser();P.add_argument('lang');P.add_argument('scene');a=P.parse_args();B=Path('/workspace/explainer-videos');O=Path('/workspace/runtime/ai4-quadratic-rendered-regression');src=B/f'renders/qa/series/ai4/{a.lang}/{a.scene}_motion';D=O/a.lang/a.scene
assert shutil.disk_usage(B).free>=512*1024**2,'Below512MiB: extraction not started'
assert not D.exists();D.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((src/'result.json').read_text());assert r['status'] in ['passed','needs-review'] and r['mode']=='motion'
movie=B/r['movie'];before=sha(movie);assert not r.get('movie_sha256') or r['movie_sha256']==before
frozen=D/movie.name;shutil.copyfile(movie,frozen);assert sha(frozen)==before
for name in ['result.json','text.jsonl','render.log']:
 if (src/name).exists():shutil.copyfile(src/name,D/('original-'+name))
module={'Quadratic':'s15_quadratic','Lagrange':'s16_lagrange','KKT':'s17_kkt','Implicit':'s18_implicit','Outro':'s19_outro'}[a.scene]
inputs=[]
for name,old in r['inputs'].items():
 p=B/name;st=p.stat();inputs.append({'path':name,'recorded_size_mtime_ns':old,'observed_size_mtime_ns':[st.st_size,st.st_mtime_ns],'metadata_matches':old==[st.st_size,st.st_mtime_ns],'sha256':sha(p)})
proof=[]
for name in [f'videos/ai/ai4/{module}.py','videos/ai/ai4/common.py','videos/ai/ai4/manifest.py','videos/ai/ai4/zh_lines.py','videos/ai/ai_text_zh.json','explainer/analysis/__init__.py','explainer/ai/viz.py','tools/qa_series.py','tools/qa_motion.py']:
 p=B/name;q=D/'source'/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);proof.append({'path':name,'sha256':sha(p),'bytes':p.stat().st_size})
freeze={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'language':a.lang,'scene':a.scene,'original_record':str(src/'result.json'),'original_record_sha256':sha(src/'result.json'),'original_movie':str(movie),'frozen_movie':str(frozen),'movie_sha256':before,'status':r['status'],'warnings':r['warnings'],'fingerprint':r['fingerprint'],'duration':r['duration'],'source_snapshots':proof,'inputs':inputs,'scope':'Exact frozen movie/result and current disk source/input identities, not loaded-module equivalence inferred from later hashes. Original broad warnings remain. Copied-movie qa_motion provenance may be null; this receipt binds the source record/movie hash explicitly.'}
(D/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
command=[sys.executable,str(B/'tools/qa_motion.py'),str(frozen),'-o',str(D/'audit'),'--dense','0.5','--max-gap','1']
with (D/'audit.log').open('w') as log:rc=subprocess.run(command,cwd=B,stdout=log,stderr=subprocess.STDOUT).returncode
assert rc==0,(D/'audit.log').read_text()[-3000:]
sys.path.insert(0,str(B));from tools.qa_motion import sheets
ar=json.loads((D/'audit/result.json').read_text());unique=[];groups={};mapping=[]
for n,f in enumerate(ar['selected_frames']):
 h=f['sha256']
 if h not in groups:
  groups[h]=len(unique);unique.append({**f,'file':'../audit/'+f['file']})
 mapping.append({'selected_index':n,'source_frame':f['source_frame'],'time':f['time'],'sha256':h,'representative':groups[h],'page':groups[h]//8+1,'slot':groups[h]%8})
u=D/'unique';u.mkdir();pages=sheets(u,unique)
plan={'scope':'Exact-PNG-SHA within-case grouping only, no perceptual equality. Every selected time maps to a representative; actual page views must be logged separately.','movie_sha256':before,'decoded_frames':ar['analysis']['decoded_frames'],'selected_times':len(ar['selected_frames']),'unique_pngs':len(unique),'selected_unviewed_pending':True,'pages':pages,'representative_frames':unique,'mapping':mapping,'max_selected_time_gap':ar['largest_selected_time_gap']}
(u/'review-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
assert sha(frozen)==before and sha(src/'result.json')==freeze['original_record_sha256']
print(json.dumps({'case':f'{a.lang}/{a.scene}','movie_sha256':before,'decoded':plan['decoded_frames'],'selected':plan['selected_times'],'unique':plan['unique_pngs'],'pages':len(pages),'audit':str(D/'audit/result.json'),'review_plan':str(u/'review-plan.json'),'free_bytes':shutil.disk_usage(B).free},indent=2))
