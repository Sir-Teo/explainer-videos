import json,sys,hashlib
from pathlib import Path
p=Path(sys.argv[1]);plan=json.loads(p.read_text());progress=json.loads((p.parent/'review-progress.json').read_text());assert len(progress['viewed_pages'])==len(plan['pages'])
review={**plan,'status':'scoped-selected-time-native-image-review-complete','actual_review_pages':[progress['viewed_pages'][str(i)] for i in range(1,len(plan['pages'])+1)],'findings':progress.get('findings',[]),'native_followups':progress.get('native_followups',[]),'continuous_perceptual_playback':'unverified','narration_listening_and_synchronization':'unverified'}
viewed={f:page for page in review['actual_review_pages'] for f in page['source_frames']};byframe={}
for f in review['all_selected_time_mapping']:
 assert hashlib.sha256(Path(f['file']).read_bytes()).hexdigest()==f['sha256']
 if f['source_frame'] in viewed:
  page=viewed[f['source_frame']];f.update(coverage='direct-native854x480-image-viewed-on-unscaled-chronological-sheet',actual_page=page['file'],actual_page_sha256=page['sha256'])
 else:
  representative=byframe[f['representative_source_frame']];assert representative['sha256']==f['sha256'];f.update(coverage='exact-PNG-reuse-of-directly-viewed-representative',representative_sha256=representative['sha256'])
 byframe[f['source_frame']]=f
review['direct_unique_images']=len(viewed);review['exact_duplicate_times']=len(byframe)-len(viewed)
(p.parent/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False));(p.parent/'review.md').write_text(f"# {plan['scene']} {plan['lang']}: selected-time visual QA\n\n{len(byframe)} selected times: {len(viewed)} native unique images directly viewed on {len(plan['pages'])} chronological sheets, {len(byframe)-len(viewed)} exact duplicate reuse. Every file frame was automatically decoded ({plan['decoded_frames']} frames); this is not continuous perceptual playback/listening. Largest selected gap {plan['largest_selected_time_gap']:.6f}s.\n\nMovie SHA `{plan['movie_sha256']}`; tool SHA `{plan['tool_sha256']}`. Source/input/record/frame/page provenance and gaps remain in JSON.\n\n"+'\n\n'.join(f"Page {i}: {x['observations']}" for i,x in enumerate(review['actual_review_pages'],1))+'\n')
print(json.dumps({'review':str(p.parent/'review.json'),'selected':len(byframe),'direct':len(viewed),'duplicates':len(byframe)-len(viewed),'pages':len(plan['pages'])}))
