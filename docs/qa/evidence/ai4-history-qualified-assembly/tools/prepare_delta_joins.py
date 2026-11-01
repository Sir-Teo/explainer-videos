from pathlib import Path
import sys,json,hashlib,datetime
B=Path('/workspace/explainer-videos');sys.path.insert(0,str(B));from tools.qa_motion import sheets
lang=sys.argv[1];R=Path('/workspace/runtime/ai4-silent-preview-assembly');base=R/'history-qualified'/lang/'validation';prior=R/'current-reviewed'/lang/'validation';p=base/'join-selection.json';raw=json.loads(p.read_text());old=json.loads((prior/'join-review.json').read_text());assert old['accounted_for_selected_times']==342 and old['native_pairs_viewed']==18;assert not (base/'join-review.json').exists();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();known={}
for x in old['selected_frames']:
 assert not x['coverage'].startswith('pending');assert sha(x['path'])==x['sha256'];known.setdefault(x['sha256'],[]).append({'source_frame':x['source_frame'],'time':x['time'],'path':x['path'],'sha256':x['sha256'],'actual_view_proof':x['proof']})
frames=[];unique=[];seen={};affected=[2,3]
for join in raw['joins']:
 for f in join['frames']:
  row=dict(f,index=len(frames),join=join['index'],reason=f"join{join['index']:02d}:{join['outgoing_scene']}->{join['incoming_scene']}:{f['relative_frame']:+d}");row['reasons']=[row['reason']]
  if join['index'] not in affected and row['sha256'] in known:row.update(coverage='exactPNG-baseline-join-inheritance',proof={'baseline_review':str(prior/'join-review.json'),'baseline_review_sha256':sha(prior/'join-review.json'),'witnesses':known[row['sha256']]})
  elif row['sha256'] in seen:row.update(coverage='pending-exact-duplicate',first_unique_index=seen[row['sha256']])
  else:seen[row['sha256']]=row['index'];row.update(coverage='pending-actual-view');unique.append(row)
  frames.append(row)
dest=base/'delta-review-pages';dest.mkdir();pages=sheets(dest,[dict(f,file=f['path']) for f in unique],tile_width=640)
for page in pages:
 offset=page['first_selected_frame'];page.update(path=str(dest/page['file']),actual_selected_indices=[f['index'] for f in unique[offset:offset+page['frames']]],actual_view='pending')
pairs={}
for join in raw['joins']:
 i=str(join['index']);before=next(f for f in join['frames'] if f['relative_frame']==-15);after=next(f for f in join['frames'] if f['relative_frame']==15);pair={'outgoing_scene':join['outgoing_scene'],'incoming_scene':join['incoming_scene'],'before':before,'after':after,'actual_view':'pending'}
 if join['index'] not in affected:
  op=old['native_pairs'][i];assert op['actual_view']!='pending'
  if all(pair[role]['sha256']==op[role]['sha256'] and sha(op[role]['path'])==op[role]['sha256'] for role in ['before','after']):pair.update(actual_view='exactPNG-baseline-native-pair-inheritance',baseline_native_pair=op,baseline_review_sha256=sha(prior/'join-review.json'))
 pairs[i]=pair
review={'scope':'All18joinwindows mapped;4affectedjoinsacrosslanguages(2/3each)requirefreshdirectviews evenifimagesmatchbaseline. Other32joinwindows inheritonlyexactPNGidentitywithfrozenbaselineactualviewproof. Notcontinuousplayback/audioapproval.','language':lang,'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':str(p),'selection_sha256':sha(p),'affected_join_indices':affected,'selected_frames':frames,'pages':pages,'selected_times':len(frames),'unique_images_requiring_direct_view':len(unique),'exactPNG_inherited_times':sum(f['coverage']=='exactPNG-baseline-join-inheritance' for f in frames),'actual_pages_viewed':[],'accounted_for_selected_times':sum(not f['coverage'].startswith('pending') for f in frames),'native_pairs':pairs,'native_pairs_viewed':sum(x['actual_view']!='pending' for x in pairs.values()),'findings':[],'status':'pending-affected-join-actual-review-and-Gradient-acceptance','continuous_playback':False,'audio_listening':False};(base/'join-review.json').write_text(json.dumps(review,indent=2)+'\n');print(lang,'freshdirectreps',len(unique),'pages',len(pages),'inheritedtimes',review['exactPNG_inherited_times'],'nativeinherited',review['native_pairs_viewed'],'pendingnative',[k for k,v in pairs.items() if v['actual_view']=='pending'])
