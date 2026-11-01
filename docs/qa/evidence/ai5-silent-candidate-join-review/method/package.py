from pathlib import Path
import json,gzip,hashlib,shutil,datetime
from PIL import Image
b=Path(__file__).parent;src=Path('/workspace/runtime/ai5-silent-preview-assembly/current-candidate');out=Path('/workspace/explainer-videos/docs/qa/evidence/ai5-silent-candidate-join-review');assert not out.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def gz(p,data):
 p.parent.mkdir(parents=True,exist_ok=True)
 with gzip.GzipFile(filename=str(p),mode='wb',mtime=0) as f:f.write(data)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();summary=[];out.mkdir()
for lang in ['en','zh']:
 c=b/lang;p=c/'join-review.json';d=json.loads(p.read_text());v=json.loads((c/'validation.json').read_text());receipt=json.loads((c/'assembly-receipt.json').read_text())
 assert sha(Path(v['movie']))==v['movie_sha256']==receipt['final_sha256'];assert len(d['actual_pages_viewed'])==41 and d['accounted_for_selected_times']==342
 assert sum(f['coverage']=='actual-image-view' for f in d['selected_frames'])==325
 assert sum(f['coverage']=='exact-PNG-reuse' for f in d['selected_frames'])==17
 for f in d['selected_frames']:
  assert not f['coverage'].startswith('pending');assert sha(Path(f['path']))==f['sha256'];assert Image.open(f['path']).size==(854,480)
 for pg in d['pages']:assert sha(Path(pg['path']))==pg['sha256']
 joins=json.loads((c/'join-selection.json').read_text())['joins'];results=[]
 for j in joins:
  fs=[f for f in d['selected_frames']if f['join']==j['index']];assert len(fs)==19
  assert [f['relative_frame']for f in fs]==[-15,-12,-9,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,9,12,15]
  results.append({'index':j['index'],'outgoing_scene':j['outgoing_scene'],'incoming_scene':j['incoming_scene'],'chapter_marker_time':j['chapter_marker_time'],'first_incoming_pts':j['first_incoming_pts'],'marker_vs_frame_delta':j['marker_vs_frame_delta'],'reviewed_selected_times':19,'native_context_pair':d['native_pairs'][str(j['index'])]['actual_view']!='pending','observation':'Outgoing final composition fades out, next expected chapter title fades in (Outro: recap heading); no stray-frame flash, wrong chapter order or persistent outgoing overlay observed.','scope':'All encoded frame indices -6 through+6 around boundary, plus±9/12/15frames; intervening unselected frames outside that central window and rest of chapter not visually covered here.'})
 d.update(status='selected-join-window-review-complete',completed_utc=now,movie_sha256=v['movie_sha256'],movie=v['movie'],source_linkage='Frozen assembly input/source observations retained; not historical-import attestations.',joins=results,findings=[],original_size_followups=44//2,critical_native_pair_count=11,native_context_note='11critical pairs viewed at854x480 original. Other7optional native pairs remain unviewed; their19selected timestamps were all reviewed on640px tiles.',limits=['No continuous full-part perceptual playback.','No narration/listening/synchronization approval.','Silent854x48015fps candidate only, not production1080/4K.','Subtitle text/millisecond equality and full decoding are existing machine-validation results, not visual subtitle-player/audio review.','Only join windows inspected; chapter-level selected visual gates are owned separately and candidate remains subject to their closure.'])
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');dest=out/lang;dest.mkdir()
 for name in ['join-review.json','join-selection.json','validation.json','final-probe.json','extracted-soft-subtitles.srt','assembly-receipt.json','assembly-progress.json']:
  if(c/name).exists():gz(dest/(name+'.gz'),(c/name).read_bytes())
 for pg in d['pages']:
  pd=dest/'pages'/pg['file'];pd.parent.mkdir(exist_ok=True);shutil.copy2(pg['path'],pd)
 for key,pair in d['native_pairs'].items():
  if pair['actual_view']=='pending':continue
  for role in ['before','after']:
   f=pair[role];assert sha(Path(f['path']))==f['sha256'];pd=dest/'native'/f"join-{int(key):02d}-{role}.png";pd.parent.mkdir(exist_ok=True);shutil.copy2(f['path'],pd)
 for item in receipt['inputs']:
  rp=Path(item['frozen_record']);assert sha(rp)==item['record_sha256'];gz(dest/'chapter-records'/f"{item['index']:02d}-{item['scene']}.json.gz",rp.read_bytes())
 summary.append({'lang':lang,'movie_sha256':v['movie_sha256'],'duration':v['duration'],'video_frames':v['video_frames'],'chapters':19,'joins':18,'selected_times':342,'actual_unique_images':325,'exact_PNG_duplicate_times':17,'pages_viewed':41,'tile_width':640,'original_size':[854,480],'critical_native_pairs':11,'original_followups':22,'new_join_defects':0,'full_machine_decode':v['full_decode'],'first_pts':v['first_pts'],'last_pts':v['last_pts'],'min_frame_gap':v['minimum_frame_gap'],'max_frame_gap':v['maximum_frame_gap'],'packet_dts_monotonic':v['packet_dts_monotonic'],'subtitle_cues':v['subtitle_cues'],'soft_subtitles_exact_text_and_millisecond_timing':v['soft_subtitles_exact_text_and_millisecond_timing'],'input_raw_warning_cases':[{'scene':x['scene'],'status':x['record_status'],'warnings':x['record_warnings']}for x in receipt['inputs']if x['record_warnings']]})
freeze=json.loads((src/'input-freeze.json').read_text());gz(out/'assembly-input-freeze.json.gz',(src/'input-freeze.json').read_bytes());snapshot=[]
for item in freeze['source_observations']:
 p=Path(item['snapshot']);assert sha(p)==item['sha256'];dest=out/'sources'/(item['path']+'.gz');gz(dest,p.read_bytes());snapshot.append(item)
(out/'source-observations.json').write_text(json.dumps(snapshot,indent=2)+'\n')
shutil.copy2(b/'freeze.json',out/'review-freeze.json')
report={'scope':'Part5 current-candidate EN/ZH silent assembly selected joins only','completed_utc':now,'languages':summary,'total_selected_times':684,'actual_unique_images':650,'exact_duplicate_times':34,'pages_viewed':82,'critical_native_pairs':22,'original_followups':44,'candidate_status':'Not upgraded by this join review. Separate chapter-level FP gate and parent acceptance govern candidate closure.','no_continuous_perceptual_or_audio_approval':True,'scene_producer_cache_edits':False}
(out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(b/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(out/'README.md').write_text('''# Part5 silent candidate assembly: selected chapter joins

All18chapter joins in each English/Chinese silent candidate were reviewed chronologically: **684selected timestamps**, **650actually viewed distinct images**, and **34byte-identical PNG duplicate-time mappings**. All82pages were viewed at640px image width; an additional22critical before/after pairs (44images) were inspected at original854×480. No join-specific defect was found: outgoing compositions fade out, the expected next chapter title/recap fades in, and no wrong-order flash or persistent prior overlay appeared.

Each join includes every encoded frame from boundary index−6 through+6 (approximately±0.4seconds at15fps), plus−15/−12/−9/+9/+12/+15 (approximately±1.0/0.8/0.6seconds). Complete frame identities, exact PTS, hashes, coverage/duplicate mapping, page hashes, actual native context checks and unselected scope are in the compressed ledgers. The other7optional original-size pairs per language were not viewed separately; their selected images were covered on the declared pages.

Original-size contexts cover Hook→Bell, Gauss→Likelihood, Bayes→MaxEnt, Tails→Sampling, Sampling→Decoding, Decoding→Markov, ScoreFn→MCMC, MCMC→Brownian, Ito→SDE, SDE→FokkerPlanck and FokkerPlanck→Outro. All actual reviewed pages and these44native examples are retained, without full movies or data caches.

Machine validation was completed before consumption and movie/frame hashes were independently checked. English:3352.562542seconds/50288decodedframes/992subtitle cues. Chinese:3503.617125seconds/52554decodedframes/1013cues. Existing complete decode, monotonic packet timestamps, ~1/15second video gaps and exact soft-subtitle text/millisecond timing receipts are preserved; they are not substituted for perceptual or listening review. Original chapter raw source-change warnings remain in frozen chapter records and the summary.

Assembly movie SHA256:
- EN `d256356d20368c82c9b190c93c2a01453283626b4dffdf7642f0ced5477347ab`
- ZH `9dae141ad8fa31bee6f50ebed1a3f13ea5c3b060b5560fbb76822cb64e3f97d5`

**Scope and limits:** this is a silent854×48015fps **candidate join-window review**. It does not upgrade the candidate status, close another owner's chapter-level FP gate, approve whole-chapter/full-part continuous perceptual playback, narration/listening/synchronization, subtitle-player rendering, or production1080/4K output. Source snapshots in the assembly freeze are observations, not retrospective import proof. No scene, producer, numerical data/cache, translation/global table, or CI configuration changed. Runtime methods adapt the previously used Part4join-page/checkpoint workflow and render no new scene/movie.
''')
(out/'method').mkdir()
for name in ['prepare.py','track.py','package.py']:shutil.copy2(b/name,out/'method'/name)
manifest=[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(out.rglob('*'))if p.is_file()];(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'out':str(out),'files':len(manifest)+1,'bytes':sum(p.stat().st_size for p in out.rglob('*')if p.is_file()),'manifest_sha256':sha(out/'manifest.json'),'warning_cases':{x['lang']:len(x['input_raw_warning_cases'])for x in summary}}))
