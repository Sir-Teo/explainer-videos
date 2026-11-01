from pathlib import Path
import hashlib,json,gzip,shutil,sys,datetime
R=Path('/workspace/explainer-videos');O=Path(__file__).parent;sys.path.insert(0,str(R))
from tools.qa_motion import probe
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
oldbase=Path('/workspace/runtime/ai5-ito-sde-fokker-motion-review')
oldpaths={'en':oldbase/'en-Ito/959961e957831004e962bd0841e5fa978a350a91ece728f508cb2cf0bfcefa99','zh':oldbase/'zh-Ito/74d8917be2b3c0f1c55d69a2438aaa7bfc4de0eec6e728aa975c587d4318c1d3'}
P=R/'docs/qa/evidence/ai5-ito-ladder-reveal-regression';P.mkdir(parents=True,exist_ok=True)
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finding':'ITO-M01 retained-row copy doubling during four ladder reveals','outcome':'resolved in fresh bilingual silent 480p15 selected-image and every-encoded-proof-window regression','source_sha256':'3cbd2023cb1a0a969d542fe634cd814e3f7a69f46e1a62d0a11702a2b73fa08e','cases':{},'limits':['Still-image inspection; no continuous perceptual playback, listening, narration sync, or native1080 motion sign-off.','Whole-file RGB comparison and decode are automatic, not actual viewing of every frame.','Direct source hashes observed at freeze; no blanket historical imported-source or aggregate-current assertion.','Original after-plan pending labels preserved as preparation history; final mappings carry completed coverage.','Manual canonical freeze binds copied movie to raw render record; qa_motion sibling provenance on runtime copies is null.']}
assert H(R/'videos/ai/ai5/s17_ito.py')==summary['source_sha256']
for l,indices in [('en',[348,1080,1181]),('zh',[335,1117,1223])]:
 d=O/l;plan=json.loads((d/'plan.json').read_text());vp=json.loads((d/'view-progress.json').read_text());assert len(vp['actually_viewed_pages'])==len(plan['pages'])==11
 times_by_idx={f['source_frame']:f['time'] for f in plan['all_time_mapping']}
 natives=[]
 for i in indices:
  q=next((d/'cohort-frames').glob(f'{i:07d}_*.png'));natives.append({'path':str(q),'sha256':H(q),'source_frame':i,'actual_pts':times_by_idx[i],'actually_viewed':True,'detail':'original native854x480','observation':'New row writes independently below unchanged retained identities; clean retained glyphs; no chart/caption overlap.'})
 vp['native_followups']=natives;(d/'view-progress.json').write_text(json.dumps(vp,indent=2)+'\n')
 pages=list(vp['actually_viewed_pages'].values());assert all(H(x['path'])==x['sha256'] for x in pages)
 actual_by_frame={i:p for p in pages for i in p['source_frames']}
 rows=[]
 for f in plan['all_time_mapping']:
  assert H(f['file'])==f['sha256'];f=dict(f)
  if f['source_frame'] in actual_by_frame:f['coverage']='actual chronological sheet view';f['actual_view_page_sha256']=actual_by_frame[f['source_frame']]['sha256']
  else:assert f['exact_old_actual_matches'];f['coverage']='exact-PNG inheritance from completed original actual selected-image review'
  rows.append(f)
 beforemovie=oldpaths[l]/'movie.mp4'
 if not beforemovie.exists():
  movies=list(oldpaths[l].glob('*.mp4'));assert len(movies)==1;beforemovie=movies[0]
 sb,tb=probe(beforemovie);sa,ta=probe(d/'Ito.mp4');assert tb==ta
 pts={'every_decoded_pts_equal':True,'before_movie':str(beforemovie),'before_movie_sha256':H(beforemovie),'after_movie_sha256':H(d/'Ito.mp4'),'count':len(ta),'first':ta[0],'last':ta[-1],'all_pts_sha256':hashlib.sha256(json.dumps(ta,separators=(',',':')).encode()).hexdigest(),'actual_avg_fps_before':sb['fps'],'actual_avg_fps_after':sa['fps'],'different_run_actual_pts':[{'first':w['different_frame_range'][0],'last':w['different_frame_range'][1],'start':ta[w['different_frame_range'][0]],'end':ta[w['different_frame_range'][1]]} for w in plan['windows']],'original_decoded_comparison_time_note':'different_runs start/end are nominal frame_index/15; exact best-effort PTS recorded here and in final time mapping.'}
 (d/'pts-comparison.json').write_text(json.dumps(pts,indent=2)+'\n')
 freeze=json.loads((d/'freeze.json').read_text());cmp=json.loads((d/'decoded-comparison.json').read_text());assert len(cmp['different_rgb_frames'])==72
 review={'lang':l,'freeze':freeze,'preparation_plan_sha256':H(d/'plan.json'),'pages':pages,'native_followups':natives,'all_selected_time_mapping':rows,'automatic_pts_comparison':pts,'counts':{'decoded_automatic':len(ta),'different_rgb_frames_automatic':72,'identical_rgb_frames_automatic':len(ta)-72,'selected_union':len(rows),'actually_viewed_proof_window_frames':80,'actually_viewed_novel_nonwindow_images':plan['new_nonwindow_selected_images_to_view'],'exact_png_inherited_nonwindow':plan['nonwindow_exact_PNG_inherited_count'],'unselected_frames_not_individually_viewed':len(ta)-len(rows),'endpoint_exact_png_inherited':plan['endpoint_exact_inherited_count'],'actual_sheet_pages':11,'actual_native_followups':len(natives)},'endpoints':plan['endpoints'],'source_sha256':plan['source_sha256'],'movie_sha256':plan['movie_sha256'],'before_actual_review':plan['before_actual_review'],'before_actual_review_sha256':plan['before_actual_review_sha256'],'tool_sha256':plan['tool_sha256'],'limits':summary['limits'],'observations':'All four new lines write below stationary retained identities; no retained-copy doubling, clipping or new chart/caption collision in actual inspected states. Pink correction and bilingual reasons stay distinct. Ordinary partial glyphs during Write are intentional.'}
 (d/'review.json').write_text(json.dumps(review,indent=2)+'\n');summary['cases'][l]={'movie_sha256':plan['movie_sha256'],'record_sha256':plan['render_record_sha256'],'raw_status':freeze['raw_status'],'raw_warnings':freeze['raw_warnings'],'counts':review['counts'],'review_sha256':H(d/'review.json')}
 target=P/l;target.mkdir(exist_ok=True)
 paths=[d/'review.json',d/'freeze.json',d/'plan.json',d/'view-progress.json',d/'decoded-comparison.json',d/'pts-comparison.json',d/'render-record.json',d/'audit/result.json',oldpaths[l]/'review.json',oldpaths[l]/'plan.json']
 for n,q in enumerate(paths):
  name=['review','freeze','preparation-plan','actual-view-progress','decoded-comparison','pts-comparison','raw-render-record','fresh-audit','before-actual-review','before-preparation-plan'][n]+'.json.gz';(target/name).write_bytes(gzip.compress(q.read_bytes(),mtime=0))
 ep=d/'endpoints/result.json';(target/'raw-endpoint-record.json.gz').write_bytes(gzip.compress(ep.read_bytes(),mtime=0))
 for i,n in zip(indices,natives):
  after=target/f'after-{i:07d}.png';shutil.copyfile(n['path'],after)
  oldmap=json.loads((oldpaths[l]/'review.json').read_text())['all_selected_time_mapping'];prior=[x for x in oldmap if x['source_frame']==i]
  if prior:shutil.copyfile(prior[0]['file'],target/f'before-{i:07d}.png')
repair=Path('/workspace/runtime/ai5-ito-ladder-reveal-repair')
for name in ['freeze.json','before.json']:
 (P/('source-repair-'+name+'.gz')).write_bytes(gzip.compress((repair/name).read_bytes(),mtime=0))
for name in ['source.patch','validation.log','validate.py']:
 shutil.copyfile(repair/name,P/name)
for name in ['compare_decode.py','prepare_review.py','finalize.py','checkpoint.py','prepare-review-first-attempt-failure.json']:
 shutil.copyfile(O/name,P/name)
(O/'review.json').write_text(json.dumps(summary,indent=2)+'\n');(P/'review.json.gz').write_bytes(gzip.compress((O/'review.json').read_bytes(),mtime=0))
readme='''# Itô retained-row reveal regression

Source `3cbd2023…` uses local `transform=False` for four new-row reveals. Both original complete selected-image reviews remain historical. Fresh EN/ZH movies resolve the observed transient retained-row doubling.

| Scope | EN | ZH |
| --- | ---: | ---: |
| Automatically decoded native RGB frames | 2,399 | 2,485 |
| Changed frames (four 18-frame runs) | 72 | 72 |
| Current selected-time union | 468 | 460 |
| Every encoded proof-window frame actually viewed (includes neighbors) | 80 | 80 |
| Novel nonwindow images actually viewed | 3 | 4 |
| Other selected times inherited by exact PNG from completed actual review | 385 | 376 |
| Chronological sheets actually viewed | 11 | 11 |
| Additional native854×480 critical checks | 3 | 3 |
| Held endpoint exact-PNG inheritances | 14 | 15 |

All 4,740 other decoded frames are pixel-identical to the before movies; every old/new decoded PTS is exactly equal. This automatic whole-file comparison does not mean every frame was perceptually inspected. All four changed windows plus one encoded neighbor on each side were inspected as chronological still images. Every new selected image was viewed; unchanged selected images inherit only exact PNG matches to recorded actual prior views. The six native before/after pairs show new partial lines separated from clean retained identities. No further visual defect was found in this scoped regression.

EN raw status remains `needs-review` with `source-changed-during-render`; ZH is `passed`, no warnings. Both endpoint records passed without warnings. Raw records, direct source and data hashes remain preserved. These direct observations do not assert all historical imported bytes or broad aggregate-source currency.

Each language folder contains compressed exact per-time mappings, original actual review, current actual page receipts, all-frame RGB hashes, exact PTS comparison and raw records. The original decode comparison uses nominal frame-index/15 run times; `pts-comparison.json.gz` supplies actual mux-quantized PTS. A local extraction wrapper first failed on a logical `frames/` path mismatch; its failure is retained, complete existing EN PNGs were reconciled before continuation, and no producer/source/movie was modified.

This is silent480p15 selected-image/every-frame-window QA. Continuous perceptual playback, listening, narration sync and native1080 motion remain unverified. No movie is stored in this Git evidence package; frozen full movies and full selected PNGs remain in cloud runtime.
'''
(P/'README.md').write_text(readme);(O/'review.md').write_text(readme)
manifest=[{'path':str(q.relative_to(P)),'sha256':H(q),'bytes':q.stat().st_size} for q in sorted(P.rglob('*')) if q.is_file() and q.name!='manifest.json'];(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for q in P.rglob('*.gz'):gzip.decompress(q.read_bytes())
print(json.dumps({'directory':str(P),'files':len(manifest)+1,'payload_bytes':sum(x['bytes'] for x in manifest),'manifest_sha256':H(P/'manifest.json'),'review_sha256':H(O/'review.json'),'free_bytes':shutil.disk_usage(R).free}))
