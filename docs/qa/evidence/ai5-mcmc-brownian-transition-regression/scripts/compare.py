from pathlib import Path
import json, hashlib, sys, shutil, os, datetime
sys.path.insert(0,'/workspace/explainer-videos')
from tools.qa_motion import probe, extract, sheets
R=Path(__file__).parent
O=R.parent/'ai5-mc-score-mcmc-brownian-motion-review'
lang,scene=sys.argv[1:3];D=R/lang/scene;old=O/lang/scene
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert shutil.disk_usage(R).free>=512*1024**2
a=json.loads((D/'audit/result.json').read_text());b=json.loads((old/'audit/result.json').read_text())
v=json.loads((old/'views.json').read_text());p=json.loads((old/'unique/review-plan.json').read_text())
assert set(x['number'] for x in v['pages'])==set(range(1,len(p['pages'])+1))
for x in v['pages']: assert sha(old/'unique'/x['file'])==x['sha256']
assert a['analysis']['decoded_frames']==b['analysis']['decoded_frames']
assert abs(a['duration']-b['duration'])<1e-6
oldrecord=json.loads((old/'original-result.json').read_text());newrecord=json.loads((D/'original-result.json').read_text());assert oldrecord['narration']==newrecord['narration'];assert oldrecord['inputs']==newrecord['inputs']
stream,times=probe(D/f'{scene}.mp4')
assert len(times)==a['analysis']['decoded_frames']
intervals={'enMCMC':[29,31,34],'zhMCMC':[29,31,34],'enBrownian':[34,38],'zhBrownian':[31,34]}[lang+scene]
windows=[{'baseline_motion_index':i,'first_frame':b['motion_intervals'][i]['first_frame']-1,'last_frame':b['motion_intervals'][i]['last_frame']+6} for i in intervals]
origins={}
for kind,fs in [('fresh_primary',a['selected_frames']),('original_cohort',b['selected_frames'])]:
 for x in fs: origins.setdefault(x['source_frame'],[]).append(kind)
for j,w in enumerate(windows,1):
 for n in range(w['first_frame'],w['last_frame']+1):origins.setdefault(n,[]).append(f'all_encoded_reveal_{j}')
fresh={x['source_frame']:{**x,'path':str(D/'audit'/x['file'])} for x in a['selected_frames']}
missing=[{'source_frame':n,'time':times[n],'reasons':origins[n]} for n in sorted(origins) if n not in fresh]
U=D/'union';U.mkdir(exist_ok=True);assert not (D/'changed/review-plan.json').exists(),'Already prepared; preserve completed reviewplan'
if missing:
 import fcntl,time
 lock=open('/workspace/runtime/ai4-tail-motion-review/extract.lock','a')
 while True:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
  except BlockingIOError:
   assert shutil.disk_usage(R).free>=512*1024**2
   time.sleep(.5)
 expected=[U/'frames'/f"{x['source_frame']:07d}_{x['time']:010.3f}s.png"for x in missing]
 if all(p.exists() for p in expected):
  for x,existing_frame in zip(missing,expected):x.update(file='frames/'+existing_frame.name,sha256=sha(existing_frame))
 else:
  assert not any(p.exists()for p in expected),'Partial prior extraction needs explicit reconciliation'
  extract(D/f'{scene}.mp4',U/'frames',missing)
 fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
for x in missing:fresh[x['source_frame']]={**x,'path':str(U/x['file'])}
lookup={}
for n,x in enumerate(b['selected_frames']):
 assert sha(old/'audit'/x['file'])==x['sha256']
 m=p['mapping'][n]
 lookup.setdefault(x['sha256'],{'baseline_selected_index':n,'baseline_source_frame':x['source_frame'],'baseline_time':x['time'],'baseline_path':str(old/'audit'/x['file']),'baseline_page':m['page'],'baseline_page_receipt':next(z for z in v['pages'] if z['number']==m['page'])})
C=D/'changed';C.mkdir(exist_ok=True);reps=[];seen={};mapping=[]
for n in sorted(origins):
 x=fresh[n];assert sha(x['path'])==x['sha256'];m={**x,'origins':origins[n]}
 if x['sha256'] in lookup:m.update({'review':'exact_png_inherited','inheritance':lookup[x['sha256']]})
 else:
  if x['sha256'] not in seen:
   seen[x['sha256']]=len(reps);reps.append({**x,'file':os.path.relpath(x['path'],C),'reasons':origins[n]})
  k=seen[x['sha256']];m.update({'review':'actual_view_required','representative':k,'page':k//8+1,'slot':k%8})
 mapping.append(m)
pages=sheets(C,reps)
gaps=[{'after_frame':u['source_frame'],'before_frame':w['source_frame'],'start':u['time'],'end':w['time'],'unselected_frames':w['source_frame']-u['source_frame']-1} for u,w in zip(mapping,mapping[1:]) if w['source_frame']-u['source_frame']>1]
plan={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Fresh primary cohort UNION original selected cohort UNION every encoded frame in bounded repaired-reveal windows. Inheritance solely by exact decoded PNG SHA256 to actually viewed baseline pages; no temporal/semantic/source-only inheritance.',
      'movie_sha256':a['source_sha256'],'baseline_movie_sha256':b['source_sha256'],'decoded_frames':len(times),'fresh_primary_selected':len(a['selected_frames']),'original_selected':len(b['selected_frames']),
      'union_selected':len(mapping),'inherited_times':sum(x['review']=='exact_png_inherited' for x in mapping),'changed_times':sum(x['review']=='actual_view_required' for x in mapping),
      'changed_unique_pngs':len(reps),'pages':pages,'representative_frames':reps,'mapping':mapping,'all_encoded_reveal_windows':windows,'unselected_frames':len(times)-len(mapping),'unselected_gaps':gaps,
      'max_selected_time_gap':max(y['time']-x['time'] for x,y in zip(mapping,mapping[1:]))}
(C/'review-plan.json').write_text(json.dumps(plan,indent=2)+'\n');(D/'delta-views.json').write_text(json.dumps({'pages':[],'native':[]},indent=2)+'\n')
assert sha(D/f'{scene}.mp4')==a['source_sha256']
print(json.dumps({k:plan[k] for k in ['union_selected','inherited_times','changed_times','changed_unique_pngs','all_encoded_reveal_windows','unselected_frames']}|{'case':lang+'/'+scene,'pages':len(pages),'free_bytes':shutil.disk_usage(R).free},indent=2))
