from pathlib import Path
import sys,json,hashlib,datetime
ROOT=Path('/workspace/explainer-videos');sys.path.insert(0,str(ROOT))
from tools.qa_motion import sheets
language=sys.argv[1];base=Path('/workspace/runtime/ai5-assembly-join-review')/language;base.mkdir(exist_ok=True);p=Path('/workspace/runtime/ai5-silent-preview-assembly/current-candidate')/language/'validation/join-selection.json';raw=json.loads(p.read_text());dest=base/'review-pages';assert not (base/'join-review.json').exists();dest.mkdir(exist_ok=True);seen={};frames=[];unique=[]
for join in raw['joins']:
 for f in join['frames']:
  row=dict(f,index=len(frames),join=join['index'],reason=f"join{join['index']:02d}:{join['outgoing_scene']}->{join['incoming_scene']}:{f['relative_frame']:+d}")
  row['reasons']=[row['reason']]
  if row['sha256'] in seen:row.update(coverage='pending-exact-duplicate',first_unique_index=seen[row['sha256']])
  else:seen[row['sha256']]=row['index'];row.update(coverage='pending-actual-view');unique.append(row)
  frames.append(row)
pages=sheets(dest,[dict(f,file=f['path']) for f in unique],tile_width=640)
for page in pages:
 offset=page['first_selected_frame'];page.update(path=str(dest/page['file']),actual_selected_indices=[f['index'] for f in unique[offset:offset+page['frames']]],actual_view='pending')
review=dict(scope='All18join windows:19selectedframes each; not continuous full-part visual/listening approval',language=language,prepared_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),selection=str(p),selection_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),selected_frames=frames,pages=pages,selected_times=len(frames),unique_images=len(unique),duplicate_times=len(frames)-len(unique),actual_pages_viewed=[],accounted_for_selected_times=0,native_pairs={str(j['index']):{'outgoing_scene':j['outgoing_scene'],'incoming_scene':j['incoming_scene'],'before':next(f for f in j['frames'] if f['relative_frame']==-15),'after':next(f for f in j['frames'] if f['relative_frame']==15),'actual_view':'pending'} for j in raw['joins']},findings=[],status='pending-actual-view',continuous_playback=False,audio_listening=False)
(base/'join-review.json').write_text(json.dumps(review,indent=2)+'\n');print(language,'selected',len(frames),'unique',len(unique),'duplicates',len(frames)-len(unique),'pages',len(pages))
