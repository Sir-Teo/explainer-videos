from pathlib import Path
import json,hashlib,gzip,shutil,datetime
R=Path('/workspace/explainer-videos');W=Path(__file__).parent;B=W.parent/'ai5-mc-score-mcmc-brownian-motion-review';O=R/'docs/qa/evidence/ai5-mcmc-brownian-transition-regression';assert not O.exists()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();cases=[];native={};sheets={};sources={}
for l in ['en','zh']:
 for s in ['MCMC','Brownian']:
  d=W/l/s;p=json.loads((d/'changed/review-plan.json').read_text());v=json.loads((d/'delta-views.json').read_text());f=json.loads((d/'freeze.json').read_text());review=json.loads((d/'review.json').read_text());a=json.loads((d/'audit/result.json').read_text())
  assert sha(d/(s+'.mp4'))==f['movie_sha256']==p['movie_sha256']==a['source_sha256'];assert sha(d/(s+'.mp4'))==sha(R/json.loads((d/'original-result.json').read_text())['movie'])
  assert sha(d/'original-result.json')==f['original_record_sha256'];assert len(v['pages'])==len(p['pages']);assert {x.get('number',x.get('page'))for x in v['pages']}==set(range(1,len(p['pages'])+1))
  for x in v['pages']:
   n=x.get('number',x.get('page'));q=d/'changed'/p['pages'][n-1]['file'];assert sha(q)==x['sha256']==p['pages'][n-1]['sha256'] and x['actual_view'];sheets[x['sha256']]=q
  for x in v['native']:
   q=Path(x.get('path',x.get('file')));q=q if q.is_absolute()else d/q;assert sha(q)==x['sha256'];native[x['sha256']]=q
  for x in f['sources']:
   q=d/'source'/x['path'];assert sha(q)==x['sha256'];sources[x['sha256']]=q
  old=json.loads((B/l/s/'original-result.json').read_text());new=json.loads((d/'original-result.json').read_text());assert old['narration']==new['narration'] and old['inputs']==new['inputs'] and old['duration']==new['duration']
  for x in f['inputs']:assert sha(R/x['path'])==x['sha256']
  frames={x['source_frame']for x in p['mapping']}
  for window in p['all_encoded_reveal_windows']:assert set(range(window['first_frame'],window['last_frame']+1))<=frames
  cases.append({'case':l+'/'+s,'movie_sha256':f['movie_sha256'],'movie_bytes':(d/(s+'.mp4')).stat().st_size,'record_sha256':f['original_record_sha256'],'direct_source_sha256':f['sources'][0]['sha256'],'raw_status':f['raw_status'],'raw_warnings':f['raw_warnings'],'decoded_frames':p['decoded_frames'],'fresh_primary_selected':p['fresh_primary_selected'],'old_selected':p['original_selected'],'union_selected':p['union_selected'],'inherited_times_exact_png':p['inherited_times'],'new_times_covered':p['changed_times'],'new_unique_pngs_actually_viewed':p['changed_unique_pngs'],'changed_pages_actually_viewed':len(v['pages']),'new_native_followups':len(v['native']),'all_encoded_repair_windows':p['all_encoded_reveal_windows'],'all_encoded_window_frames_covered':sum(x['last_frame']-x['first_frame']+1 for x in p['all_encoded_reveal_windows']),'unselected_frames':p['unselected_frames'],'max_union_selected_time_gap':p['max_selected_time_gap'],'narration_duration_inputs_identical':True,'case_report_sha256':sha(d/'review.json')})
O.mkdir(parents=True)
def cp(src,dest):
 p=O/dest;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,p)
def gz(src,dest):
 p=O/dest;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('wb')as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0)as z:z.write(Path(src).read_bytes())
for x in cases:
 l,s=x['case'].split('/');d=W/l/s
 for name in ['freeze.json','original-result.json','original-text.jsonl','original-render.log','audit.log','audit/result.json','changed/review-plan.json','delta-views.json','review.json','review.md']:
  gz(d/name,Path('receipts')/l/s/(name.replace('/','-')+'.gz'))
 for name in ['compare-initial-failure.txt','compare-resume.log','compare-resume2.log','compare.log']:
  if(d/name).exists():gz(d/name,Path('receipts')/l/s/(name+'.gz'))
for h,p in native.items():cp(p,'native/'+h+'.png')
for h,p in sheets.items():cp(p,'changed-sheets/'+h+'.png')
for h,p in sources.items():gz(p,'sources/'+h+p.suffix+'.gz')
for name in ['prepare.py','compare.py','log_delta_views.py','finalize_en.py','package.py']:cp(W/name,'scripts/'+name)
for name in ['ai5-mcmc-copy-transition-repair','ai5-brownian-copy-transition-repair']:
 d=W.parent/name
 for p in d.glob('*'):
  if p.is_file():
   if p.suffix=='.gz':cp(p,Path('source-repair-proof')/name/p.name)
   elif p.suffix in ['.py','.json','.md','.log']:gz(p,Path('source-repair-proof')/name/(p.name+'.gz'))
T=W/'en/Brownian/dead-air-transition';transition=json.loads((T/'review.json').read_text());tp=json.loads((T/'plan.json').read_text())
for name in ['plan.json','review.json']:gz(T/name,'dead-air-transition/'+name+'.gz')
for p in tp['pages']:cp(T/p['file'],'dead-air-transition/'+p['file'])
mainset={x['source_frame']for x in json.loads((W/'en/Brownian/changed/review-plan.json').read_text())['mapping']};extra={x['source_frame']for x in tp['mapping']if x['variant']=='after'}-mainset
report={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Actual final EN/ZH MCMC and Brownian silent480p15 image regressions after only local retained-row direct Write changes. Every fresh-primary and original selected time, plus every encoded frame in ten bounded reveal windows, is covered by direct novel-image review or exact-PNG inheritance to fully viewed preserved original image ledgers.','cases':cases,'totals':{k:sum(x[k]for x in cases)for k in ['decoded_frames','fresh_primary_selected','old_selected','union_selected','inherited_times_exact_png','new_times_covered','new_unique_pngs_actually_viewed','changed_pages_actually_viewed','new_native_followups','all_encoded_window_frames_covered','unselected_frames']},'dead_air_additional_review':{'case':'en/Brownian','every_encoded_range_seconds':[125.8,128.4],'combined_before_after_times':80,'unique_images_actually_viewed':39,'pages_actually_viewed':5,'same_time_pairs_exact_png':39,'same_time_pairs_total':40,'additional_fresh_frames_beyond_main_union':len(extra),'assessment':'Intentional QV fade, coincident initial particle point, then spreading cloud. No missing-scene/render failure. Warning and narrated pacing limit remain explicit.','receipt_sha256':sha(T/'review.json')},'findings':['No new visual defect found in the covered final images. Direct Write removes transient copied-glyph interference while retaining prior equations and explanations.','Partial newly written glyphs are expected during Write. MCMC oldest-row fade and upward ladder shift are intentional and preserve the final hierarchy.','Narration objects, exact raw durations, data input signatures and current input bytes match the original captures; source AST differs only by three MCMC/two Brownian transform=False keywords.','The late Brownian initial-cloud state127.600s differs from its original by12pixels with maximum channel delta2; actually inspected, no factual/layout change.'],'source_invariants':{'MCMC_sha256':'95c38c1d058a07556f26dd86fd042dbdba8e137ff4083ea9350cbd0f919655af','Brownian_sha256':'780521544fd9ad5e9ab698bfeba6c8da2aa82b24b17433a93623dca69c444e9f','no_numeric_cache_or_producer_changes':True},'baseline_preservation_limitation':'Six older MC/ScoreFn/MCMC MP4 hardlink witnesses were overwritten by canonical rerenders and no independent original copy was found. Inheritance here binds preserved original decoded PNG/audit/page-view evidence, not those altered aliases. Both old Brownian movies were independently copied and verified before overwrite. All four fresh movies are independent byte copies with full SHA checks. See the historical baseline package reconciliation receipt.','limits':['No continuous perceptual playback or listening/narration synchronization approval.','No native1080 or4K motion approval.','Decoded unselected frames remain unreviewed; exact gap lists retained.','Source snapshots observe bytes and do not prove historical in-memory imports.','Original raw source-change and Brownian dead-air warnings are preserved, not promoted to runtime passed.','This image review does not rerun numerical experiments or grant full production signoff.']}
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
rows='\n'.join(f"|{x['case']}|{x['union_selected']}|{x['inherited_times_exact_png']}|{x['new_times_covered']}|{x['new_unique_pngs_actually_viewed']}|{x['changed_pages_actually_viewed']}|{x['new_native_followups']}|"for x in cases)
(O/'README.md').write_text('''# Part 5 MCMC and Brownian transition regression

Both languages pass this bounded image review after local direct Write repairs. All fresh and original selected-time cohorts were compared; every encoded frame in all ten repair windows was included. No further visual defect was found.

|Case|Union times|Exact PNG inherited|New times|New unique images viewed|Changed pages viewed|Native follows|
|---|---:|---:|---:|---:|---:|---:|
'''+rows+'''

The package contains every changed contact sheet, critical native views, full compressed mapping/audit/raw-result/viewing receipts, observed source snapshots and the source repair proofs. Tiles were 640×360; native follows were 854×480. It omits movies and raw numerical cache payloads; runtime originals remain under `/workspace/runtime/ai5-mcmc-brownian-transition-regression/`.

Narration objects, durations and numerical input bytes/signatures match. The direct Write reveals remove duplicated moving glyphs from retained equations without altering measured plots, values, bookmarks or explanation text.

The English Brownian raw dead-air warning remains. An additional every-frame comparison of125.8–128.4 seconds in independently preserved before/after movies covered80 frame times and39 exact-PNG representatives, all actually viewed on five pages. It shows the intentional QV fade, a coincident initial particle point and then the spreading cloud.39 of40 same-time pairs match exactly; the remaining pair differs in12 pixels by at most two channel levels. This is not a missing-scene or render failure. Narrated pacing/listening approval remains open.

Six old MC/ScoreFn/MCMC MP4 hardlink witnesses were overwritten during rerendering. Their original movie bytes are unavailable; the preserved old PNG/audit/viewing ledgers support the explicitly scoped image inheritance. Both old Brownian movies and all four fresh movies are independent verified copies. See the earlier baseline package's reconciliation receipt.

Raw source-change/dead-air warnings are retained. No continuous-perception, audio/narration synchronization, native1080 motion,4K or full production approval is claimed. Exact unselected gaps and counts remain in the receipts; full decoding does not imply those frames were perceived. Source snapshots are byte observations, not historical imported-module proof.
''')
payload=[]
for p in sorted(O.rglob('*')):
 if p.is_file():payload.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'sha256':sha(p)})
size=sum(x['bytes']for x in payload);assert size<=12*1024**2,size
(O/'manifest.json').write_text(json.dumps({'created_utc':report['created_utc'],'payload_bytes':size,'payloads':payload,'scope':'Bounded image/provenance package; no MP4 or raw cache data payloads.'},indent=2)+'\n')
for x in payload:
 p=O/x['path'];assert sha(p)==x['sha256']and p.stat().st_size==x['bytes']
 if p.suffix=='.gz':gzip.decompress(p.read_bytes())
print(json.dumps({'path':str(O),'payloads':len(payload),'bytes':size,'manifest_sha256':sha(O/'manifest.json'),'totals':report['totals'],'additional_transition_frames':len(extra)},indent=2))
