from pathlib import Path
import json,sys,hashlib,shutil
B=Path('/workspace/explainer-videos');sys.path.insert(0,str(B));from tools.qa_motion import probe,extract,sheets
R=Path(__file__).parent;OLD=Path('/workspace/runtime/ai4-tail-motion-review');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for lang in ['en','zh']:
 p=R/lang/'Quadratic';b=OLD/lang/'Quadratic';a=json.loads((p/'audit/result.json').read_text());old=json.loads((b/'audit/result.json').read_text());orig=json.loads((b/'original-result.json').read_text());new=json.loads((p/'original-result.json').read_text());f=json.loads((p/'freeze.json').read_text());assert orig['duration']==new['duration'] and orig['narration']==new['narration'] and orig['inputs']==new['inputs'];assert [(x['time'],x['reason']) for x in orig['frames']]==[(x['time'],x['reason']) for x in new['frames']]
 source=json.loads((b/'freeze.json').read_text());assert {x['path']:x['sha256'] for x in source['inputs']}=={x['path']:x['sha256'] for x in f['inputs']}
 known={}
 for sub in ['audit','row-reveals']:
  for x in json.loads((b/sub/'result.json').read_text())['selected_frames']:known.setdefault(x['sha256'],[]).append({'source_frame':x['source_frame'],'time':x['time'],'file':str(b/sub/x['file'])})
 movie=Path(f['frozen_movie']);stream,times=probe(movie);assert len(times)==old['analysis']['decoded_frames'];newrows={x['source_frame']:{**x,'file':str(p/'audit'/x['file'])} for x in a['selected_frames']};missing=[{'source_frame':x['source_frame'],'time':times[x['source_frame']],'reasons':['complete-baseline-cohort-regression']} for x in old['selected_frames'] if x['source_frame'] not in newrows]
 out=p/'baseline-cohort-extra';out.mkdir();assert shutil.disk_usage(B).free>=512*1024**2
 if missing:
  extract(movie,out/'frames',missing)
  for x in missing:newrows[x['source_frame']]={**x,'file':str(out/x['file'])}
 (out/'result.json').write_text(json.dumps({'selected_frames':missing},indent=2)+'\n')
 union=sorted({x['source_frame'] for x in old['selected_frames']}|set(newrows));mapping=[];changed=[];seen={}
 for n in union:
  x=newrows[n];h=x['sha256'];entry={'source_frame':n,'time':x['time'],'file':x['file'],'sha256':h,'in_baseline_cohort':n in {q['source_frame'] for q in old['selected_frames']},'in_fresh_selected':n in {q['source_frame'] for q in a['selected_frames']}}
  if h in known:entry.update(visual_coverage='exactPNG-baseline-view-inherited',baseline_matches=known[h])
  else:
   if h not in seen:seen[h]=len(changed);changed.append({**x,'file':x['file']})
   entry.update(visual_coverage='new-representative-view-required',representative=seen[h],page=seen[h]//8+1,slot=seen[h]%8)
  mapping.append(entry)
 out=p/'changed';out.mkdir();pages=sheets(out,changed);report={'scope':'Complete baseline selected cohort plus full fresh selected cohort. Visual inheritance only exact PNG SHA matches to actually reviewed original baseline selected/reveal PNGs. No perceptual comparison. New representatives need actual views.','baseline_movie_sha256':json.loads((b/'freeze.json').read_text())['movie_sha256'],'fresh_movie_sha256':f['movie_sha256'],'baseline_selected_times':len(old['selected_frames']),'fresh_selected_times':len(a['selected_frames']),'cohort_union_times':len(union),'baseline_exactPNG_inherited_times':sum(x['visual_coverage']=='exactPNG-baseline-view-inherited' for x in mapping),'changed_unique':len(changed),'pages':pages,'mapping':mapping,'representative_frames':changed,'invariants':{'duration_exactly_identical':True,'full_narration_word_times_raw_text_exactly_identical':True,'all_endpoint_time_reason_pairs_identical':True,'raw_data_sha256_identical':True,'decoded_frame_counts_identical':True}}
 (out/'review-plan.json').write_text(json.dumps(report,indent=2)+'\n');print(lang,{k:report[k] for k in ['baseline_selected_times','fresh_selected_times','cohort_union_times','baseline_exactPNG_inherited_times','changed_unique']},'pages',len(pages),flush=True)
