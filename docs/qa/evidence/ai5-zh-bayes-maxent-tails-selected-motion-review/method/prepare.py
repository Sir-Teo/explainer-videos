from pathlib import Path
import sys,json,hashlib,shutil,subprocess,datetime,importlib.util
R=Path('/workspace/explainer-videos'); root=Path('/workspace/runtime/ai5-zh-bayes-maxent-tails-selected-motion-review');lang,scene=sys.argv[1:3];D=root/lang/scene;S=R/'renders/qa/series/ai5'/lang/(scene+'_motion');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert lang=='zh' and scene in ['Bayes','MaxEnt','Tails']
expected={'Bayes':('s06_bayes.py','64c18dce'),'MaxEnt':('s07_maxent.py','f77af534'),'Tails':('s09_tails.py','028b56fd')}
module,prefix=expected[scene];assert sha(R/'videos/ai/ai5'/module).startswith(prefix)
if (D/'plan.json').exists():print('already prepared',D);raise SystemExit
if shutil.disk_usage(R).free<768*1024**2:raise RuntimeError('insufficient free disk')
r=json.loads((S/'result.json').read_text());assert r['mode']=='motion' and r['status'] in ['passed','needs-review'];D.mkdir(parents=True,exist_ok=True)
frozen={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case':lang+'/'+scene,'raw_status':r['status'],'raw_warnings':r['warnings'],'source_files':[],'inputs':[]}
for name in ['result.json','text.jsonl','render.log']:
 p=S/name
 if p.exists():shutil.copy2(p,D/('raw-'+name))
p=R/r['movie'];q=D/(scene+'.mp4');shutil.copy2(p,q);assert sha(p)==sha(q);frozen.update(movie_sha256=sha(q),original_movie=str(p),frozen_movie=str(q),original_record_sha256=sha(S/'result.json'))
mod=next(n['module'] for n in json.loads((R/'docs/qa/ai5-chapter-checklist.json').read_text())['cases'] if n['scene']==scene)
for rel in ['videos/ai/ai5/'+mod+'.py','videos/ai/ai5/common.py','videos/ai/ai5/zh_lines.py','videos/ai/ai_text_zh.json','videos/ai/ai5/plotting.py','tools/qa_motion.py','tools/qa_series.py']:
 p=R/rel;q=D/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);frozen['source_files'].append({'path':rel,'sha256':sha(p),'bytes':p.stat().st_size})
for rel,old in r['inputs'].items():
 p=R/rel;st=p.stat();assert old==[st.st_size,st.st_mtime_ns];frozen['inputs'].append({'path':rel,'sha256':sha(p),'size_mtime_ns':old})
(D/'freeze.json').write_text(json.dumps(frozen,indent=2)+'\n')
with (D/'audit.log').open('w') as out:subprocess.run([sys.executable,str(R/'tools/qa_motion.py'),str(D/(scene+'.mp4')),'-o',str(D/'audit'),'--dense','.25','--max-gap','1'],stdout=out,stderr=subprocess.STDOUT,check=True,cwd=R)
spec=importlib.util.spec_from_file_location('qa_motion',R/'tools/qa_motion.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a=json.loads((D/'audit/result.json').read_text());reps=[];seen={};mapping=[]
for n,f in enumerate(a['selected_frames']):
 h=f['sha256']
 if h not in seen:seen[h]=len(reps);reps.append({**f,'file':'../audit/'+f['file']})
 mapping.append({'selected_index':n,'time':f['time'],'source_frame':f['source_frame'],'sha256':h,'representative':seen[h]})
U=D/'unique';U.mkdir(exist_ok=True);pages=m.sheets(U,reps)
plan={'case':lang+'/'+scene,'source_sha256':a['source_sha256'],'decoded':a['analysis']['decoded_frames'],'selected':len(a['selected_frames']),'unique':len(reps),'reps':reps,'mapping':mapping,'pages':pages,'gaps':a['unextracted_frame_gaps'],'max_gap':a['largest_selected_time_gap']}
(D/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');(D/'views.json').write_text('{"pages":[],"native":[],"findings":[]}\n');print(lang,scene,len(a['selected_frames']),len(reps),len(pages),flush=True)
