from pathlib import Path
import datetime,gzip,hashlib,json,shutil,sys
R=Path('/workspace/explainer-videos');O=Path(__file__).parent;P=R/'docs/qa/evidence/ai5-fokker-reveal-regression';P.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R))
from tools.qa_motion import probe
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
J=lambda p:json.loads(Path(p).read_text())
origin=[]
def cp(q,d):
 q=Path(q);t=P/d;t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,t);origin.append({'package_path':d,'original_path':str(q),'original_sha256':H(q),'encoding':'exact bytes'});return t
def gz(q,d):
 q=Path(q);t=P/d;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(gzip.compress(q.read_bytes(),mtime=0));origin.append({'package_path':d,'original_path':str(q),'original_sha256':H(q),'encoding':'gzip, original exact bytes after decompression'});return t
source='7e33904756d634c988cc6b3db97f29a851788d7d64d7a111a33df0f75983bca7';assert H(R/'videos/ai/ai5/s19_fokker.py')==source
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':source,'findings':{'FP-M01':'Resolved: six actual transient retained-row copy doubles; now independent new-row Write.','FP-M02':'Resolved: old and replacement captions no longer overprint; sequential fades inside unchanged5s nonlinear tracker play.'},'cases':{},'source_repair_freeze_sha256':H('/workspace/runtime/ai5-fokker-reveal-repair/freeze.json'),'limits':['Time-indexed still-image inspection and exact-PNG inheritance, not continuous perceptual playback/listening/narration synchronization or native1080 motion sign-off.','Every native frame decoded and hashed automatically; full-file equality/inequality does not imply full-file perceptual inspection.','Raw baseline warnings, aggregate-current false/unknown fields and preparation pending labels retained; completed-coverage-map supplies final assignments.','Exact direct source/data hashes observed at freeze, not proof of every historical imported byte or broad aggregate currency.','Copied-movie qa_motion sibling provenance null is explicitly bound to original record by separate freeze receipt.','Original whole-file diff run times are nominal frame_index/15; exact mux-quantized PTS appear in pts-comparison and time mappings.']}
for l in ('en','zh'):
 d=O/l;plan=J(d/'plan.json');rev=J(d/'review.json');old=Path(plan['before_actual_review']).parent;oldrev=J(old/'review.json');cmp=J(d/'decoded-comparison.json');audit=J(d/'audit/result.json');record=J(d/'render-record.json');oldrecord=J(old/'render-record.json')
 assert H(d/'FokkerPlanck.mp4')==plan['movie_sha256']==cmp['after_movie_sha256'];assert H(old/'FokkerPlanck.mp4')==cmp['before_movie_sha256']
 assert (d/'FokkerPlanck.mp4').stat().st_ino!=(old/'FokkerPlanck.mp4').stat().st_ino
 assert H(d/'s19_fokker.py')==source
 sb,tb=probe(old/'FokkerPlanck.mp4');sa,ta=probe(d/'FokkerPlanck.mp4');assert tb==ta and len(ta)==cmp['decoded_frame_count']
 pts={'every_decoded_pts_exactly_equal':True,'count':len(ta),'first':ta[0],'last':ta[-1],'all_pts_sha256':hashlib.sha256(json.dumps(ta,separators=(',',':')).encode()).hexdigest(),'fps_before':sb['fps'],'fps_after':sa['fps'],'changed_runs_actual_pts':[{'first_frame':w['first'],'last_frame':w['last'],'first_pts':ta[w['first']],'last_pts':ta[w['last']]} for w in cmp['different_runs']],'nominal_vs_actual_note':summary['limits'][-1]}
 (d/'pts-comparison.json').write_text(json.dumps(pts,indent=2)+'\n')
 pages=rev['pages'];assert len(pages)==(30 if l=='en' else 26);assert all(p['actually_viewed'] and H(p['path'])==p['sha256'] for p in pages)
 byframe={i:p for p in pages for i in p['source_frames']};rows=[]
 for f in plan['all_time_mapping']:
  assert H(f['file'])==f['sha256'];f=dict(f)
  if f['source_frame'] in byframe:f['coverage']='actual chronological sheet view';f['actual_view_page_sha256']=byframe[f['source_frame']]['sha256']
  else:assert f['exact_old_actual_matches'];f['coverage']='exact-PNG inheritance from completed original actual selected-image review'
  rows.append(f)
 times=[f['time'] for f in rows];selected={f['source_frame'] for f in rows};gap_runs=[];a=None
 for i,t in enumerate(ta):
  if i not in selected and a is None:a=i
  if a is not None and (i in selected or i==len(ta)-1):
   b=i-1 if i in selected else i;gap_runs.append({'first_frame':a,'last_frame':b,'first_pts':ta[a],'last_pts':ta[b],'count':b-a+1});a=None
 completed={'movie_sha256':plan['movie_sha256'],'source_sha256':source,'review_sha256':H(d/'review.json'),'actual_pages':pages,'all_time_mapping':rows,'unselected_encoded_frame_runs':gap_runs,'maximum_selected_pts_gap':max(b-a for a,b in zip(times,times[1:])),'all_decoded_frames':len(ta),'selected':len(rows),'unselected':len(ta)-len(rows),'automatic_diff_frames':len(cmp['different_rgb_frames']),'coverage_limits':summary['limits']}
 (d/'completed-coverage-map.json').write_text(json.dumps(completed,indent=2)+'\n')
 for name,dest in [('review.json','review.json.gz'),('freeze.json','freeze.json.gz'),('plan.json','preparation-plan.json.gz'),('render-record.json','raw-motion-record.json.gz'),('decoded-comparison.json','all-frame-rgb-comparison.json.gz'),('pts-comparison.json','pts-comparison.json.gz'),('completed-coverage-map.json','completed-coverage-map.json.gz')]:gz(d/name,f'{l}/{dest}')
 gz(d/'audit/result.json',f'{l}/fresh-temporal-audit.json.gz');gz(d/'endpoints/result.json',f'{l}/raw-endpoint-record.json.gz');cp(d/'review.md',f'{l}/review.md')
 for name in ['review.json','review-progress.json','audit.json','plan.json','render-record.json']:
  gz(old/name,f'{l}/before/{name}.gz')
 cp(old/'review.md',f'{l}/before/review.md')
 for name in ['hist-comparison-plan.json','view-progress.json']:
  if (d/name).exists():gz(d/name,f'{l}/{name}.gz')
 # Representative native original before and after, only views actually performed.
 before_idx={x['source_frame']:x for x in oldrev['native_followups']};final_idx={x['source_frame']:x for x in rev['native']}
 pairs=[(317,332),(1438,1453),(2521,2532)] if l=='en' else [(348,348),(1508,1508),(2642,2642),(2691,2678)]
 for n,(i,j) in enumerate(pairs,1):
  a=before_idx[i];b=final_idx[j];assert a['actually_viewed'] and b['actually_viewed'];assert H(a['file'])==a['sha256'] and H(b['file'])==b['sha256'];cp(a['file'],f'{l}/native-pairs/{n:02d}-before-f{i:07d}.png');cp(b['file'],f'{l}/native-pairs/{n:02d}-after-f{j:07d}.png')
 # Small chronological proof and caption page examples; complete page hashes/maps retained.
 for ix in ([1,20,27] if l=='en' else [1,17,25]):
  pg=pages[ix-1];cp(pg['path'],f'{l}/examples/page-{ix:03d}.png')
 if l=='en':cp(rev['hist_pair_pages'][3]['path'],f'{l}/examples/histogram-pairs-page004.png')
 assert oldrecord['duration']==record['duration'] and oldrecord['narration']==record['narration'] and oldrecord['inputs']==record['inputs']
 summary['cases'][l]={'before_movie_sha256':cmp['before_movie_sha256'],'movie_sha256':plan['movie_sha256'],'render_record_sha256':plan['render_record_sha256'],'raw_status':record['status'],'raw_warnings':record['warnings'],'direct_scene_sha256':source,'baseline_selected_times':oldrev['selected_time_count'],'baseline_unique_actual_images':oldrev['unique_frame_count'],'baseline_actual_pages':len(oldrev['actual_review_pages']),'baseline_native_checks':len(oldrev['native_followups']),'decoded_automatic':len(ta),'changed_rgb_automatic':len(cmp['different_rgb_frames']),'unchanged_rgb_automatic':len(ta)-len(cmp['different_rgb_frames']),'current_selected_times':len(rows),'current_every_encoded_window_actual_images':plan['every_encoded_proof_window_frames'],'current_novel_nonwindow_actual_images':plan['new_nonwindow_selected_images_to_view'],'current_exact_png_inherited_times':plan['nonwindow_exact_PNG_inherited_count'],'current_actual_pages':len(pages),'current_native_checks':len(rev['native']),'current_endpoint_exact_inherited_times':plan['endpoint_exact_inherited_count'],'current_unselected_decoded_frames':len(ta)-len(rows),'maximum_selected_pts_gap':completed['maximum_selected_pts_gap'],'pts_exactly_unchanged':True,'duration_narration_bookmarks_inputs_exactly_unchanged':True,'review_sha256':H(d/'review.json'),'extra_histogram_window':rev.get('extra_histogram_window')}
repair=Path('/workspace/runtime/ai5-fokker-reveal-repair')
for name in ['freeze.json','before.json','validation.json','movie-preservation-reconciliation.json']:gz(repair/name,f'source-repair/{name}.gz')
for name in ['before.py','after.py','source.patch','validate.py']:cp(repair/name,f'source-repair/{name}')
for name in ['analyze.py','compare_decode.py','prepare_review_en.py','prepare_review_zh.py','checkpoint.py','close_root_en_review.py','close_zh_review.py','en_hist_compare.py','analyze.log','en-prepare-review-attempt1-storage-guard.log','en-prepare-review.log','en-prepare-review-attempt2.log','package.py']:
 cp(O/name,f'helpers/{name}')
assert H(R/'tools/qa_motion.py')==J(O/'zh/audit/result.json')['tool_sha256'];cp(R/'tools/qa_motion.py','helpers/qa_motion.py')
(O/'review.json').write_text(json.dumps(summary,indent=2)+'\n');gz(O/'review.json','review.json.gz')
(P/'README.md').write_text('''# Fokker–Planck reveal and caption regression

Source `7e33904756d634c988cc6b3db97f29a851788d7d64d7a111a33df0f75983bca7` fixes two actually observed transient presentation problems. Six proof appends now write only the new row, leaving prior identities stationary. The final green caption fades out before the gold caption appears, inside the same five-second nonlinear particle-flow play. Numerical inputs, narration/bookmarks, positions, curves and total duration are unchanged.

| Actual coverage | EN | ZH |
| --- | ---: | ---: |
| Original selected times | 510 | 530 |
| Original unique images actually viewed | 429 | 434 |
| Original chronological sheets viewed | 54 | 55 |
| Original individual native checks | 11 | 11 |
| Current automatically decoded frames | 2,675 | 2,832 |
| Current selected-time union | 659 | 656 |
| Every encoded changed-window frame plus neighbors actually viewed | 223 | 197 |
| Other novel selected images actually viewed | 10 | 3 |
| Remaining selected times inherited by exact PNG from actual original views | 426 | 456 |
| Current chronological sheets actually viewed | 30 | 26 |
| Current individual native checks | 9 | 9 |
| Current endpoint exact-PNG inheritances | 15 | 14 |
| Current encoded frames unselected in this pass | 2,016 | 2,176 |

All six proof reveals are clean in the inspected frames. The old footer clears before its replacement appears; particles continue moving during the intentional brief caption gap. Both fresh raw motion records are `passed`, warnings `[]`; raw endpoint records also pass. Historical warnings and conservative fingerprint fields remain in the original records. Source and data snapshots are direct observations, not blanket proof of historical imported bytes or aggregate-source currency.

EN has 207 RGB-different frames: six 18-frame proof runs, a 75-frame caption run and an additional 24-frame histogram interval. Root independently inspected every old/new histogram frame, plus one neighbor on each side, on seven paired sheets (26 pairs). Its density shapes, time/readouts and labels remain coherent. Maximum channel delta is 48, with at most 3,717 pixels differing. The rendering cause remains unisolated; no RGB-equality claim is made for that interval. ZH has only the expected 183 RGB-different frames (six 18-frame proof runs and the 75-frame caption run). All 5,117 other encoded frames are automatically RGB-identical to their original movies. Every old/current decoded PTS is exactly equal. These automatic checks are not perceptual review of every frame.

The original independent full movies, original complete selected-image reviews and fresh independent movies are retained in cloud runtime. Movie-preservation reconciliation verifies distinct canonical/witness inodes and original hashes; no movie in this scope was lost to canonical overwrites. This bounded Git package includes compressed complete historical/current per-time and page ledgers, explicit unselected runs, automatic full-frame RGB hashes, exact PTS, raw records and representative actual native/page examples. No movie is added to Git.

`source-repair/validation.json.gz` records AST equivalence after normalizing the six local flags and one caption Succession, unchanged VO/bookmarks, actual Manim schedule boundaries 0–2.5–5 seconds, and 1,001 nonlinear-progress checks without caption-opacity overlap. These are isolated geometry/schedule checks; fresh rendered views establish the scoped visual result. Preparation plans retain original pending labels; each `completed-coverage-map.json.gz` supplies final view-versus-exact-inheritance assignments. The first EN extraction storage guard failure and root helper/logs are preserved, followed by successful reconciled extraction.

This is silent480p15 time-indexed still-image review with every encoded frame inspected inside the changed windows. Continuous perceptual playback, listening/narrated synchronization, and native1080 full-motion QA remain unverified. The full-series and later-parts gates are separate.
''')
(P/'origin-manifest.json').write_text(json.dumps(origin,indent=2)+'\n');manifest=[{'path':str(q.relative_to(P)),'sha256':H(q),'bytes':q.stat().st_size} for q in sorted(P.rglob('*')) if q.is_file() and q.name!='manifest.json'];(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
size=sum(q.stat().st_size for q in P.rglob('*') if q.is_file());assert size<12_000_000,size
for q in P.rglob('*.gz'):gzip.decompress(q.read_bytes())
for x in origin:
 q=P/x['package_path'];data=gzip.decompress(q.read_bytes()) if x['encoding'].startswith('gzip') else q.read_bytes();assert hashlib.sha256(data).hexdigest()==x['original_sha256']
print(json.dumps({'package':str(P),'files':len(manifest)+1,'total_bytes':size,'manifest_sha256':H(P/'manifest.json'),'summary_sha256':H(O/'review.json'),'free_bytes':shutil.disk_usage(R).free}))
