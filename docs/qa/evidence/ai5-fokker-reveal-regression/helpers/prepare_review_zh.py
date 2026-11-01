from pathlib import Path
import hashlib,json,sys,shutil
from PIL import Image,ImageDraw
R=Path('/workspace/explainer-videos');O=Path('/workspace/runtime/ai5-fokker-reveal-regression');B=Path('/workspace/runtime/ai5-ito-sde-fokker-motion-review');sys.path.insert(0,str(R))
from tools.qa_motion import probe,extract
OLD={'zh':B/'zh-FokkerPlanck/3e293d7b94b9ef8c28fc83fc90cd2b8c554acc79e88481ed21402270e993b43b'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for l,old in OLD.items():
 p=O/l;before=json.loads((old/'review.json').read_text());audit=json.loads((p/'audit/result.json').read_text());cmp=json.loads((p/'decoded-comparison.json').read_text());stream,times=probe(p/'FokkerPlanck.mp4');assert len(times)==cmp['decoded_frame_count']
 idx={f['source_frame'] for f in before['all_selected_time_mapping']}|{f['source_frame'] for f in audit['selected_frames']};windows=[];proof=set()
 for run in cmp['different_runs']:
  rr=list(range(max(0,run['first']-1),min(len(times),run['last']+2)));proof.update(rr);windows.append({'first_frame':rr[0],'last_frame':rr[-1],'start':times[rr[0]],'end':times[rr[-1]],'every_encoded_frame':rr,'different_frame_range':[run['first'],run['last']]})
 idx|=proof;selected=[{'source_frame':i,'time':times[i],'reasons':['every-encoded-proof-window' if i in proof else 'old/current-selected-cohort']} for i in sorted(idx)]
 assert shutil.disk_usage(R).free>768*1024**2
 existing={int(q.name.split('_')[0]):q for q in (p/'cohort-frames').glob('*.png')}
 if not all(i in existing for i in idx):
  assert not existing, 'partial extraction requires reconciliation before retry'
  extract(p/'FokkerPlanck.mp4',p/'cohort-frames',selected)
 files_by_index={int(q.name.split('_')[0]):q for q in (p/'cohort-frames').glob('*.png')}
 assert set(files_by_index)==idx
 oldhash={}
 for f in before['all_selected_time_mapping']:oldhash.setdefault(f['sha256'],[]).append(f)
 rows=[];novel=[]
 for f in selected:
  f['file']=str(files_by_index[f['source_frame']]);f['sha256']=sha(Path(f['file']));assert Image.open(f['file']).size==(854,480);matches=oldhash.get(f['sha256'],[]);f.update(proof_window=f['source_frame'] in proof,exact_old_actual_matches=[{'source_frame':x['source_frame'],'time':x['time'],'file':x['file'],'sha256':x['sha256'],'coverage':x['coverage']} for x in matches])
  if f['proof_window']:f['coverage']='pending actual every-encoded proof-window image view'
  elif matches:f['coverage']='exact-PNG inheritance from completed old actual selected-image review'
  else:f['coverage']='pending new selected-image view';novel.append(f)
  rows.append(f)
 pages=[]
 for kind,frames in [('proof',[f for f in rows if f['proof_window']]),('novel-cohort',novel)]:
  for a in range(0,len(frames),8):
   ff=frames[a:a+8];im=Image.new('RGB',(1708,520*((len(ff)+1)//2)),'#222832');d=ImageDraw.Draw(im)
   for k,f in enumerate(ff):
    x=k%2*854;y=k//2*520;d.text((x+8,y+5),f"{l} FokkerPlanck AFTER {kind} | {f['time']:.6f}s | encoded frame {f['source_frame']}",fill='white');im.paste(Image.open(f['file']).convert('RGB'),(x,y+40))
   q=p/'review-pages'/f'{kind}-{a//8+1:03d}.png';q.parent.mkdir(exist_ok=True);im.save(q);pages.append({'path':str(q),'sha256':sha(q),'kind':kind,'source_frames':[f['source_frame'] for f in ff],'times':[f['time'] for f in ff],'actually_viewed':False})
 # Endpoint captures are a distinct modality and inherit only real PNG matches.
 epold=Path('/workspace/runtime/ai5-ito-sde-fokker-endpoint-review/cases')
 epold=next(epold.glob(l+'-FokkerPlanck-*'));ee=json.loads((epold/'result.json').read_text());new=json.loads((p/'endpoints/result.json').read_text());old_ep_hash={sha(epold/f['file']):f for f in ee['frames']};ep=[]
 for f in new['frames']:
  h=sha(p/'endpoints'/f['file']);match=old_ep_hash.get(h);assert match is not None
  ep.append({**f,'sha256':h,'actual_old_match':match,'old_case':str(epold),'coverage':'exact-PNG inheritance from completed actual bilingual endpoint review','old_actual_review':str(epold.parent.parent/'review.json'),'old_actual_review_sha256':sha(epold.parent.parent/'review.json')})
 plan={'lang':l,'source_sha256':sha(p/'s19_fokker.py'),'movie_sha256':sha(p/'FokkerPlanck.mp4'),'render_record_sha256':sha(p/'render-record.json'),'before_actual_review':str(old/'review.json'),'before_actual_review_sha256':sha(old/'review.json'),'fresh_audit_sha256':sha(p/'audit/result.json'),'tool_sha256':audit['tool_sha256'],'old_and_new_selected_cohort_union_count':len(rows),'every_encoded_proof_window_frames':len(proof),'windows':windows,'nonwindow_exact_PNG_inherited_count':sum(not f['proof_window'] and bool(f['exact_old_actual_matches']) for f in rows),'new_nonwindow_selected_images_to_view':len(novel),'endpoint_exact_inherited_count':len(ep),'endpoints':ep,'pages':pages,'all_time_mapping':rows,'limits':'Every encoded frame in seven changed windows (six proof reveals and one caption-flow window) plus one neighbor each side is selected. Whole-file nativeRGB comparison is automatic. All other unselected frames remain not individually viewed; no continuous/audio/1080 approval.'}
 (p/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');print(l,'cohort',len(rows),'proof',len(proof),'novel',len(novel),'pages',len(pages),'endpoints',len(ep),flush=True)
