from pathlib import Path
import datetime,fcntl,gzip,hashlib,json,os,shutil,subprocess,sys,time
from PIL import Image,ImageDraw
R=Path('/workspace/explainer-videos');BASE=Path(__file__).parent;DR=Path('/workspace/runtime/ai6-remaining-qa-serial');MIN=768*1024**2;C=Path(sys.argv[1]);lang,scene=sys.argv[2:4]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
receipt=json.loads((C/'receipt.json').read_text());copies=json.loads((C/'completed/copy-manifest.json').read_text());assert receipt['runtime_completed'] and receipt['aborted'] is None
movies=[r for r in copies['artifacts'] if r['destination'].endswith('.mp4')];assert len(movies)==1;mrow=movies[0];movie=DR/mrow['destination'];assert sha(movie)==mrow['sha256'];canonical=R/mrow['source'];assert not os.path.samefile(movie,canonical) and movie.stat().st_nlink==1
O=BASE/f'{lang}-{scene}'/mrow['sha256'];O.mkdir(parents=True,exist_ok=True);assert not (O/'plan.json').exists(),'Existingplan: reconcile, do not rereview/extract'
for n in ('receipt.json','source-before.json','source-after.json','data-before.json','data-after.json','command.json'):
 (O/(n+'.gz')).write_bytes(gzip.compress((C/n).read_bytes(),mtime=0))
shutil.copyfile(C/'completed/result.json',O/'render-record.json');shutil.copyfile(C/'completed/copy-manifest.json',O/'owner-copy-manifest.json');shutil.copyfile(R/'tools/qa_motion.py',O/'qa_motion.py')
before=json.loads((C/'source-before.json').read_text());after=json.loads((C/'source-after.json').read_text());a={r['path']:r for r in before['files']};b={r['path']:r for r in after['files']};changed=[dict(path=p,before_sha256=a.get(p,{}).get('sha256'),after_sha256=b.get(p,{}).get('sha256')) for p in sorted(a.keys()|b.keys()) if a.get(p,{}).get('sha256')!=b.get(p,{}).get('sha256')]
freeze={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner_case':str(C),'owner_receipt_sha256':sha(C/'receipt.json'),'owner_copy_manifest_sha256':sha(C/'completed/copy-manifest.json'),'movie':str(movie),'movie_sha256':mrow['sha256'],'movie_bytes':movie.stat().st_size,'independent_movie_inode':movie.stat().st_ino,'canonical_movie_inode_at_observation':canonical.stat().st_ino,'movie_nlink':movie.stat().st_nlink,'source_before_sha256':sha(C/'source-before.json'),'source_after_sha256':sha(C/'source-after.json'),'direct_source_inventory':{p:v for p,v in a.items() if p in ('videos/ai/ai6/s07_newton.py','videos/ai/ai6/common.py','videos/ai/ai6/compute.py','videos/ai/ai6/contracts.py','videos/ai/ai6/cache_contract.py','videos/ai/ai_text_zh.json','videos/ai/ai6/zh_lines.py','explainer/ai/viz.py')},'source_differences_during_render':changed,'raw_status':receipt['runtime_record_status'],'raw_warnings':receipt['raw_warnings'],'source_changed':receipt['source_changed'],'data_changed':receipt['data_changed'],'record_input_signatures_current_at_owner_freeze':receipt['record_input_signatures_current'],'tool_sha256':sha(O/'qa_motion.py'),'free_before_lock':shutil.disk_usage(R).free,'limits':'Observed driver source/data snapshots; raw broadwarnings preserved. Current filesystem does not retrospectively prove every imported byte. No continuous/audio/production-resolution approval.'};(O/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
lockpath=Path('/workspace/runtime/ai4-tail-motion-review/extract.lock');lockpath.parent.mkdir(exist_ok=True,parents=True)
with lockpath.open('a') as lock:
 print('waiting_shared_extraction_lock',lang,scene,flush=True);fcntl.flock(lock,fcntl.LOCK_EX)
 free=shutil.disk_usage(R).free
 if free<MIN:
  (O/'capacity-pending.json').write_text(json.dumps({'state':'not started','free_bytes':free,'required_bytes':MIN,'target':str(movie),'reason':'Minimum768MiB required; thresholds unchanged'},indent=2));raise RuntimeError('capacity pending before extraction')
 env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1');command=['nice','-n','10',sys.executable,str(R/'tools/qa_motion.py'),str(movie),'-o',str(O/'audit'),'--dense','.25','--max-gap','1']
 (O/'audit-command.json').write_text(json.dumps({'argv':command,'minimum_free_bytes':MIN,'tool_sha256':sha(R/'tools/qa_motion.py'),'shared_lock':str(lockpath)},indent=2)+'\n')
 with (O/'audit.log').open('w') as log:
  p=subprocess.Popen(command,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
  while p.poll() is None:
   free=shutil.disk_usage(R).free
   if free<MIN:
    p.terminate();p.wait();(O/'capacity-pending.json').write_text(json.dumps({'state':'stopped during extraction; partial outputs retained, reconcile before retry','free_bytes':free,'required_bytes':MIN,'target':str(movie),'returncode':p.returncode},indent=2));raise RuntimeError('capacity pending during extraction')
   time.sleep(.5)
  if p.returncode:raise RuntimeError('audit failed; inspect exact log '+str(O/'audit.log'))
 audit=json.loads((O/'audit/result.json').read_text());assert audit['source_sha256']==mrow['sha256'];reps=[];seen={};mapping=[]
 for f in audit['selected_frames']:
  f=dict(f,file=str(O/'audit'/f['file']));assert sha(f['file'])==f['sha256']
  if f['sha256'] not in seen:seen[f['sha256']]=f;f['coverage']='pending actual native page view';reps.append(f)
  else:f['coverage']='pending exact-PNG representative view';f['representative_source_frame']=seen[f['sha256']]['source_frame']
  mapping.append(f)
 pages=[]
 for start in range(0,len(reps),8):
  if shutil.disk_usage(R).free<MIN:raise RuntimeError('capacity pending before next nativepage; rawPNG/audit preserved')
  chunk=reps[start:start+8];sheet=Image.new('RGB',(1708,520*((len(chunk)+1)//2)),'#202732');draw=ImageDraw.Draw(sheet)
  for j,f in enumerate(chunk):
   x=(j%2)*854;y=(j//2)*520;draw.text((x+8,y+6),f"{lang} {scene} {f['time']:.6f}s | source {f['source_frame']}",fill='white');draw.text((x+8,y+21),','.join(f['reasons']),fill='#c6d6e9')
   with Image.open(f['file']) as im:assert im.size==(854,480);sheet.paste(im.convert('RGB'),(x,y+40))
  path=O/f'review-{len(pages)+1:03d}.png';sheet.save(path);pages.append({'file':str(path),'sha256':sha(path),'source_frames':[f['source_frame'] for f in chunk],'times':[f['time'] for f in chunk],'actually_viewed':False})
 assert sha(movie)==mrow['sha256'];plan={'scope':'Actual854x480 source tiles, chronological exact-PNG unique representatives; no continuous/audio/production-resolution approval','scene':scene,'lang':lang,'movie':str(movie),'movie_sha256':mrow['sha256'],'freeze':str(O/'freeze.json'),'freeze_sha256':sha(O/'freeze.json'),'raw_record':str(O/'render-record.json'),'raw_record_sha256':sha(O/'render-record.json'),'raw_status':receipt['runtime_record_status'],'raw_warnings':receipt['raw_warnings'],'audit':str(O/'audit/result.json'),'audit_sha256':sha(O/'audit/result.json'),'tool_sha256':audit['tool_sha256'],'algorithm':audit['algorithm'],'color_space':audit['color_space'],'settings':audit['settings'],'decoded_frames':audit['analysis']['decoded_frames'],'duration':audit['duration'],'fps':audit['average_fps'],'largest_selected_time_gap':audit['largest_selected_time_gap'],'unextracted_frame_gaps':audit['unextracted_frame_gaps'],'selected_time_count':len(mapping),'unique_frame_count':len(reps),'duplicate_frame_count':len(mapping)-len(reps),'pages':pages,'all_selected_time_mapping':mapping};(O/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');print(json.dumps({'plan':str(O/'plan.json'),'selected':len(mapping),'unique':len(reps),'pages':len(pages),'decoded':audit['analysis']['decoded_frames'],'raw_status':receipt['runtime_record_status'],'warnings':len(receipt['raw_warnings']),'free_bytes':shutil.disk_usage(R).free}),flush=True)
