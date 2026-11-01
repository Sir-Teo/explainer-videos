"""Read completed qa_motion plan, supplement every encoded repair-window frame, and map exact prior visual evidence. No scene/data loads."""
from pathlib import Path
import datetime,fcntl,hashlib,importlib.util,json,shutil,sys
from PIL import Image,ImageDraw
D=Path(sys.argv[1]);B=Path(sys.argv[2]) if sys.argv[2]!='-' else None
windows=json.loads(sys.argv[3]) if len(sys.argv)>3 else []
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
plan=json.loads((D/'plan.json').read_text());movie=Path(plan['movie']);assert sha(movie)==plan['movie_sha256'];MIN=768*1024**2
baseline=json.loads(B.read_text()) if B else None
prior={f['sha256']:f for f in baseline['all_selected_time_mapping']} if baseline else {}
assert not (D/'regression-plan.json').exists(),'reconcile existing plan before regenerating'
if baseline:
 assert baseline['status']=='scoped-selected-time-native-image-review-complete'
 for f in baseline['all_selected_time_mapping']:assert f['coverage'].startswith(('direct-native','exact-PNG'))
records={f['source_frame']:dict(f) for f in plan['all_selected_time_mapping']}
if windows:
 spec=importlib.util.spec_from_file_location('frozen_motion_tool',D/'qa_motion.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 lockpath=Path('/workspace/runtime/ai4-tail-motion-review/extract.lock')
 with lockpath.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);assert shutil.disk_usage(D).free>=MIN,'capacity pending; no extraction started'
  stream,times=m.probe(movie);extras=[{'source_frame':n,'time':t,'reasons':['every-encoded-repair-window']} for n,t in enumerate(times) if any(a<=t<=b for a,b in windows) and n not in records]
  if extras:
   m.extract(movie,D/'repair-extra/frames',extras)
   for f in extras:f['file']=str(D/'repair-extra'/f['file']);records[f['source_frame']]=f
allrows=[];novel=[];seen={}
for n,f in sorted(records.items()):
 f['file']=str(Path(f['file']));assert sha(f['file'])==f['sha256'];f['repair_window']=any(a<=f['time']<=b for a,b in windows)
 if f['sha256'] in prior:
  f.update(coverage='exact-prior-actually-reviewed-PNG',prior_movie_sha256=baseline['movie_sha256'],prior_source_frame=prior[f['sha256']]['source_frame'],prior_file=prior[f['sha256']]['file'])
 elif f['sha256'] in seen:f.update(coverage='pending-exact-new-representative',representative_source_frame=seen[f['sha256']]['source_frame'])
 else:seen[f['sha256']]=f;novel.append(f);f['coverage']='pending-new-native-sheet-view'
 allrows.append(f)
pages=[]
for i in range(0,len(novel),8):
 assert shutil.disk_usage(D).free>=MIN,'capacity pending before page; originals preserved'
 chunk=novel[i:i+8];im=Image.new('RGB',(1708,520*((len(chunk)+1)//2)),'#202732');draw=ImageDraw.Draw(im)
 for j,f in enumerate(chunk):
  x=j%2*854;y=j//2*520;draw.text((x+8,y+6),f"{plan['lang']} {plan['scene']} {f['time']:.6f}s | source {f['source_frame']}",fill='white');draw.text((x+8,y+21),'ALL-ENCODED REPAIR' if f['repair_window'] else 'selected temporal sample',fill='#c6d6e9')
  with Image.open(f['file']) as frame:assert frame.size==(854,480);im.paste(frame.convert('RGB'),(x,y+40))
 p=D/f'changed-{len(pages)+1:03d}.png';im.save(p);pages.append({'file':str(p),'sha256':sha(p),'source_frames':[f['source_frame'] for f in chunk],'times':[f['time'] for f in chunk],'actually_viewed':False})
assert sha(movie)==plan['movie_sha256']
result={**{k:v for k,v in plan.items() if k not in ['pages','all_selected_time_mapping']},'prior_actual_review':str(B) if B else None,'prior_actual_review_sha256':sha(B) if B else None,'all_encoded_windows_seconds':windows,'regression_helper':str(Path(__file__)),'regression_helper_sha256':sha(Path(__file__)),'selected_time_count':len(allrows),'unique_new_images':len(novel),'prior_exact_times':sum(f['coverage']=='exact-prior-actually-reviewed-PNG' for f in allrows),'new_duplicate_times':sum(f['coverage']=='pending-exact-new-representative' for f in allrows),'pages':pages,'all_selected_time_mapping':allrows,'largest_selected_time_gap':max((b['time']-a['time'] for a,b in zip(allrows,allrows[1:])),default=0),'unselected_frames':plan['decoded_frames']-len(allrows)}
(D/'regression-plan.json').write_text(json.dumps(result,indent=2));print(json.dumps({'plan':str(D/'regression-plan.json'),'selected':len(allrows),'prior_exact':result['prior_exact_times'],'new_unique':len(novel),'pages':len(pages),'all_encoded_windows':windows}),flush=True)
