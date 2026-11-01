import hashlib,json,sys
from pathlib import Path
P=Path(sys.argv[1]);D=P.parent;plan=json.loads(P.read_text());progress=json.loads((D/'review-progress.json').read_text());assert len(progress['viewed_pages'])==len(plan['pages'])
viewed={f:p for p in progress['viewed_pages'].values() for f in p['source_frames']};done={}
for f in plan['all_selected_time_mapping']:
 assert hashlib.sha256(Path(f['file']).read_bytes()).hexdigest()==f['sha256']
 if f['coverage']=='exact-prior-actually-reviewed-PNG':pass
 elif f['source_frame'] in viewed:
  p=viewed[f['source_frame']];assert p['actually_viewed'];f.update(coverage='direct-new-original854x480-image-on-unscaled-chronological-sheet',actual_page=p['file'],actual_page_sha256=p['sha256'])
 else:
  rep=done[f['representative_source_frame']];assert rep['sha256']==f['sha256'] and rep['coverage'].startswith('direct-new-');f['coverage']='exact-new-actually-reviewed-representative-PNG'
 done[f['source_frame']]=f
plan.update(status='scoped-selected-time-native-image-regression-complete',actual_review_pages=[progress['viewed_pages'][str(i)] for i in range(1,len(plan['pages'])+1)],findings=progress.get('findings',[]),native_followups=progress.get('native_followups',[]),continuous_perceptual_playback='unverified',narration_listening_and_synchronization='unverified')
(D/'regression-review.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False));(D/'regression-review.md').write_text(f"# {plan['scene']} {plan['lang']} selected-image regression\n\n{plan['selected_time_count']}selected/{plan['decoded_frames']}decoded; {plan['unselected_frames']}unselected. {plan['unique_new_images']}newunique images actuallyviewed onall{len(plan['pages'])}unscaledchronologicalsheets; {plan['prior_exact_times']}exactpriorreviewedPNGtimes and {plan['new_duplicate_times']}exactnewrepresentative times. Maximumselectedgap{plan['largest_selected_time_gap']}s. Allencodedwindows:{plan['all_encoded_windows_seconds']}.\n\nRawstatus{plan['raw_status']}, warnings{plan['raw_warnings']}. Notcontinuousperceptualplayback/listening/nativeproductionresolutionapproval.\n\n"+'\n\n'.join(f"Page{i}: {x['observations']}" for i,x in enumerate(plan['actual_review_pages'],1)))
print(json.dumps({k:plan[k] for k in ['selected_time_count','unique_new_images','prior_exact_times','new_duplicate_times','unselected_frames']}))
