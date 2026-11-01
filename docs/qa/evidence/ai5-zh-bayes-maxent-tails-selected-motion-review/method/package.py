import json,pathlib,hashlib,gzip,shutil,datetime
from PIL import Image
b=pathlib.Path('/workspace/runtime/ai5-zh-bayes-maxent-tails-selected-motion-review')
out=pathlib.Path('/workspace/explainer-videos/docs/qa/evidence/ai5-zh-bayes-maxent-tails-selected-motion-review')
assert not out.exists(), 'new evidence directory only'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
natives={
'Bayes':[
('0000891_000059.400s.png','Posterior ten-thousand-count readout, zoom ticks and Bayes identity remain separate.'),
('0001493_000099.533s.png','Three beta-prior rows, normalized priors and posterior means fit.'),
('0002187_000145.800s.png','MAP objective, Gaussian prior and likelihood rows remain legible.'),
('0002440_000162.666s.png','MLE/MAP curves leave viewport without flat caps; error axes and legend fit.')],
'MaxEnt':[
('0000573_000038.200s.png','Dice bars, mean/entropy figures and Jaynes card fit.'),
('0000993_000066.199s.png','Four retained derivation rows plus miniatures remain separate and readable.'),
('0001427_000095.133s.png','Lambda fit, mean, bars and entropy histogram maximum marker fit.'),
('0002231_000148.733s.png','Three family panels, beta=1/T qualification and exponential-family identity fit.')],
'Tails':[
('0000321_000021.400s.png','Independent [0,1] qualifier, histogram and right-tail threshold remain separate.'),
('0000930_000062.000s.png','Three inequality rows and reason labels fit; exponential illustration exits viewport without cap.'),
('0001170_000078.000s.png','Final four rows, lemma condition, t=4epsilon and both illustrations fit.'),
('0001563_000104.199s.png','Exact/simulation/bound legend and epsilon0.1 numeric values are readable and separated.'),
('0002085_000138.999s.png','Counts2000/600/599/262 fit; first262 versus all n>=281 distinction is readable.'),
('0002397_000159.799s.png','Settled guarantee heading, bar labels and integer-lattice qualification remain readable.')]
}
summaries=[]
for s in natives:
 c=b/'zh'/s; p=json.loads((c/'plan.json').read_text()); v=json.loads((c/'views.json').read_text()); f=json.loads((c/'freeze.json').read_text()); a=json.loads((c/'audit/result.json').read_text())
 assert len(v['pages'])==len(p['pages'])
 assert {x['page'] for x in v['pages']}==set(range(1,len(p['pages'])+1))
 # Correct overbroad batch wording; page receipts retain original view timestamps.
 if s=='MaxEnt':
  for row in v['pages']:
   if row['page']<=14:
    row['actual_observation']='Viewed chronological representatives on pages1–14: dice bars/entropy/mean morph fit below heading; Jaynes card fits; derivation starts with independent first Lagrangian Write. Subsequent normalized rows are covered by later page receipts.'
 v['native']=[]
 for fn,note in natives[s]:
  fp=c/'audit/frames'/fn
  rep=next(r for r in p['reps'] if pathlib.Path(r['file']).name==fn)
  with Image.open(fp) as im: size=list(im.size)
  assert size==[854,480]
  v['native'].append({'file':'audit/frames/'+fn,'sha256':sha(fp),'source_frame':rep['source_frame'],'time':rep['time'],'size':size,'actual_observation':note,'receipt_at':now,'viewed_before_receipt':True})
 for pg in p['pages']:
  assert sha(c/'unique'/pg['file'])==pg['sha256']
 for i,r in enumerate(p['reps']):
  assert sha(c/'unique'/r['file'])==r['sha256']
 for row in p['mapping']:
  assert row['sha256']==p['reps'][row['representative']]['sha256']
 assert sha(c/(s+'.mp4'))==f['movie_sha256']
 assert sha(c/'raw-result.json')==f['original_record_sha256']
 for entry in f['source_files']:
  fp=c/'source'/entry['path']
  if not fp.exists():
   matches=list((c/'source').rglob(pathlib.Path(entry['path']).name)); assert len(matches)==1,(s,entry['path']);fp=matches[0]
  assert sha(fp)==entry['sha256'],fp
 (c/'views.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 page_for_rep={r:pg['page'] for pg in v['pages'] for r in pg['representative_indices']}
 coverage=[]
 for row in p['mapping']:
  r=p['reps'][row['representative']]
  coverage.append({**row,'viewed_page':page_for_rep[row['representative']],'viewing':'direct representative at640x360' if row['source_frame']==r['source_frame'] else 'exact PNG SHA256 match to viewed representative','representative_source_frame':r['source_frame'],'representative_time':r['time']})
 review={'case':'zh/'+s,'review_completed':now,'scope':'All selected times through exact-PNG representative mapping; all unique representatives viewed chronologically on declared pages plus named native followups. No old ZH artifact inheritance.','decoded_frames':p['decoded'],'selected_times':p['selected'],'direct_unique_representatives':p['unique'],'direct_pages':len(v['pages']),'native_followups':len(v['native']),'duration':a['duration'],'largest_selected_time_gap':a['largest_selected_time_gap'],'unextracted_frame_gaps':p['gaps'],'raw_status':f['raw_status'],'raw_warnings':f['raw_warnings'],'artifact_provenance':f,'source_linkage_limit':'Source snapshots identify bytes present at freeze; broad source-changed warning is retained and does not prove every imported module during render. Parent supplied stable direct scene provenance.','visual_findings':[],'outcome':'No new corrective visual defect observed within selected-image scope.','coverage':coverage,'pages':v['pages'],'native':v['native'],'limits':['Unselected encoded frames not perceptually viewed; explicit gap ledger preserved.','No continuous perceptual playback, audio/listening/synchronization or native1080 full-motion approval.','Full file decoding and render status do not establish perceptual review.']}
 (c/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 summaries.append({k:review[k] for k in ['case','decoded_frames','selected_times','direct_unique_representatives','direct_pages','native_followups','duration','largest_selected_time_gap','raw_status','raw_warnings','outcome']})
 # Bounded repository proof. Full movies/raw caches remain runtime-only.
 dest=out/'zh'/s;dest.mkdir(parents=True)
 for name,src in [('review.json',c/'review.json'),('plan.json',c/'plan.json'),('views.json',c/'views.json'),('audit.json',c/'audit/result.json'),('raw-result.json',c/'raw-result.json'),('freeze.json',c/'freeze.json'),('raw-text.jsonl',c/'raw-text.jsonl'),('raw-render.log',c/'raw-render.log')]:
  with gzip.GzipFile(filename=str(dest/(name+'.gz')),mode='wb',mtime=0) as z:z.write(src.read_bytes())
 for fn,_ in natives[s]:
  (dest/'native').mkdir(exist_ok=True);shutil.copy2(c/'audit/frames'/fn,dest/'native'/fn)
 for pg in {'Bayes':[32,48],'MaxEnt':[18,40],'Tails':[21,41]}[s]:
  (dest/'examples').mkdir(exist_ok=True);shutil.copy2(c/'unique'/f'sheet-{pg:03d}.png',dest/'examples')
 # Preserve the actual local module and helper only; common/table/tool exact hashes are in receipts.
 for entry in f['source_files']:
  if pathlib.Path(entry['path']).name in {'s06_bayes.py','s07_maxent.py','s09_tails.py','plotting.py'}:
   matches=list((c/'source').rglob(pathlib.Path(entry['path']).name));assert len(matches)==1
   (dest/'source').mkdir(exist_ok=True);shutil.copy2(matches[0],dest/'source'/matches[0].name)
summary={'scope':'Part5 current ZH Bayes/MaxEnt/Tails only','cases':summaries,'total_selected_times':sum(r['selected_times'] for r in summaries),'total_unique_representatives':sum(r['direct_unique_representatives'] for r in summaries),'total_pages':sum(r['direct_pages'] for r in summaries),'total_native_followups':sum(r['native_followups'] for r in summaries),'no_source_edits':True,'no_old_unviewed_zh_inheritance':True,'created':now}
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(out/'README.md').write_text('''# Part5 Chinese Bayes / MaxEnt / Tails selected-motion review

All **1,383 selected times** are mapped to **1,113 actually viewed unique representatives** across **140 chronological pages**, with **14 native854×480 followups**. The selection used the frozen `qa_motion.py` SHA in each audit, explicit `--dense .25 --max-gap1`; all selected duplicates inherit only exact PNG SHA256 equality within the same current movie. No unviewed old Chinese baseline was used.

No new corrective visual defect was observed in this scope. Bayes posterior zoom, counts, prior rows, MAP derivation and clipped regression curves remain readable. MaxEnt retained-row reveals avoid duplicate glyphs; lambda fitting, histogram marker and inverse-temperature qualification fit. Tails retains independent/bounded assumptions, distinct inequality rows, correctly clipped illustrative curves and separate numeric bound labels. Its coin-count note distinguishes first qualifying n=262 from all n≥281.

Bayes and MaxEnt raw records remain **needs-review** with `source-changed-during-render`. Tails raw record is passed with zero warnings. These historical statuses/warnings are preserved; reviewed image identities and stable direct module handoff scope the visual finding. Source-at-freeze copies do not prove all modules imported earlier in a warned render.

Each case contains compressed full review/selection/gap ledgers, raw result/text/log, exact source/movie/input hashes, local source copies, representative pages and all critical native followups. Movie/cache files stay outside the repository. Every selected timestamp maps to its viewed page and exact representative hash; all unextracted frame intervals remain explicit in the audits/reviews.

This is selected-image QA of complete silent movie files. It does **not** establish continuous perceptual viewing, audio/listening/synchronization, native1080 full-motion or assembled-reel approval. No source, producer, cache, caption table or rendering changes were made for this review.
''')
(out/'method').mkdir()
for name in ['prepare.py','mark.py','package.py']:shutil.copy2(b/name,out/'method'/name)
manifest=[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'out':str(out),'files':len(manifest)+1,'bytes':sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),'manifest_sha256':sha(out/'manifest.json'),'summary':summary},ensure_ascii=False))
