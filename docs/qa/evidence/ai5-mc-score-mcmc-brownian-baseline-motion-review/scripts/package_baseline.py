from pathlib import Path
import json,hashlib,gzip,shutil,datetime,os
R=Path('/workspace/explainer-videos');W=Path(__file__).parent;O=R/'docs/qa/evidence/ai5-mc-score-mcmc-brownian-baseline-motion-review'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not O.exists(), 'Reconcile an existing package before publishing another snapshot'
CASES=[];SOURCES={};NATIVES={}
for l in ['en','zh']:
 for s in ['MonteCarlo','ScoreFn','MCMC','Brownian']:
  c=W/l/s;f=json.loads((c/'freeze.json').read_text());a=json.loads((c/'audit/result.json').read_text());p=json.loads((c/'unique/review-plan.json').read_text());v=json.loads((c/'views.json').read_text())
  assert {x['number'] for x in v['pages']}==set(range(1,len(p['pages'])+1))
  assert f['movie_sha256']==a['source_sha256']==p['movie_sha256']
  movie_now=sha(c/(s+'.mp4'));original_movie_retained=movie_now==f['movie_sha256']
  assert original_movie_retained or (W/'movie-reconciliation-search.json').exists()
  assert sha(c/'original-result.json')==f['raw_record_sha256']
  for x in v['pages']:assert sha(c/'unique'/x['file'])==x['sha256'] and x['actual_view']
  for x in v['native']:
   q=Path(x.get('path',x['file']));q=q if q.is_absolute() else c/q;assert sha(q)==x['sha256'];NATIVES[x['sha256']]=q
  for x in f['source_observations']:
   q=Path(x['copy']);assert sha(q)==x['sha256'];SOURCES[x['sha256']]=q
  CASES.append({'case':l+'/'+s,'movie_sha256':f['movie_sha256'],'original_movie_bytes_retained':original_movie_retained,'runtime_witness_current_sha256':movie_now,'raw_record_sha256':f['raw_record_sha256'],'raw_status':f['raw_status'],'raw_warnings':f['raw_warnings'],'decoded_frames':p['decoded_frames'],'selected_times':p['selected_times'],'unselected_frames':p['decoded_frames']-p['selected_times'],'exact_png_representatives_actually_viewed':p['unique_pngs'],'exact_png_reused_selected_times':p['selected_times']-p['unique_pngs'],'pages_actually_viewed':len(v['pages']),'native_followups':len(v['native']),'largest_selected_time_gap_seconds':a['largest_selected_time_gap'],'review_scale':'640x360 image tiles in original1280px-wide2x4sheets; native followups854x480','scope':'Every selected time covered by direct representative view or exact PNG SHA256 reuse within this movie. Full decode is technical evidence, not perception of unselected frames.'})
assert all(x['native_followups'] for x in CASES),'Native followups still pending'
O.mkdir(parents=True)
def gz(src,dest):
 p=O/dest;p.parent.mkdir(parents=True,exist_ok=True)
 with gzip.GzipFile(filename='',mode='wb',fileobj=p.open('wb'),mtime=0) as z:z.write(Path(src).read_bytes())
def cp(src,dest):
 p=O/dest;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,p)
for x in CASES:
 l,s=x['case'].split('/');c=W/l/s
 for file in ['freeze.json','original-result.json','original-text.jsonl','original-render.log','audit.log','audit/result.json','unique/review-plan.json','views.json']:
  gz(c/file,Path('receipts')/l/s/(file.replace('/','-')+'.gz'))
 for file in ['review-notes.json','review-notes.md']:
  if (c/file).exists():gz(c/file,Path('receipts')/l/s/(file+'.gz'))
for h,p in NATIVES.items():cp(p,'native/'+h+'.png')
for h,p in SOURCES.items():gz(p,'sources/'+h+p.suffix+'.gz')
for name in ['prepare.py','log_views.py','package_baseline.py']:cp(W/name,'scripts/'+name)
for name in ['movie-reconciliation-search.json','brownian-independent-copy-reconciliation.json']:gz(W/name,'reconciliation/'+name+'.gz')
repairs=[]
for name in ['ai5-mc-cohort-sync-repair','ai5-mcmc-copy-transition-repair','ai5-brownian-copy-transition-repair']:
 d=W.parent/name
 for file in d.glob('*'):
  if file.is_file() and file.suffix in ['.json','.md','.py','.gz','.log']:
   if file.suffix=='.gz':cp(file,Path('repair-receipts')/name/file.name)
   else:gz(file,Path('repair-receipts')/name/(file.name+'.gz'))
 repairs.append({'runtime':str(d),'freeze_sha256':sha(d/'freeze.json'),'scope':'Source repair evidence only. Fresh rendered regression lives separately and is not inherited from this baseline.'})
report={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Eight original silent480p15 clips, before the MonteCarlocohort/ScoreFn/MCMC/Brownian transition repairs. All selected representative pages actually viewed chronologically; no perception claim for unselected frames.','cases':CASES,'totals':{k:sum(x[k] for x in CASES)for k in ['decoded_frames','selected_times','unselected_frames','exact_png_representatives_actually_viewed','exact_png_reused_selected_times','pages_actually_viewed','native_followups']},'findings':[{'scene':'MonteCarlo','severity':'visual/data-cohort synchronization','actual_before':'The24pictured darts were fullypresent while readout replay restarted atN1(4.000), e.gEN49.800s/ZH56.733s. Visible24darts contained15hits, giving2.5, not4.000. ForN>1500thepicturealso lacked subset disclosure.','repair':'One shared N tracker now controls visible dart prefix, liveN counter, estimate and curve; exactfirstmin(N,1500)picture/allNestimate caption. Data/VO/bookmarks/durations unchanged; initial full-size dot appearance and synchronizedrewind are intentional visual changes.','source_sha256':'34879d06284884ffc9f5ec5d11425c8ae94bbe05a30325a852fcaeabbeabaaa5','fresh_render_review':'parent-owned, separate'},{'scene':'ScoreFn','severity':'transient readability polish','actual_before':'Retained copied equations cross prior text during reveals, e.gEN48.933s/ZH46.066s; settled rows clear. Straight score and smoothedES contours/star/readouts are readable.','repair':'Onlyderive returnedstep1/2/3 transform=False.','source_sha256':'15a66c5cb423e2bd507ebe3af352e8907ae588c509fc4f4df39b9bfcd236e52c','fresh_render_review':'parent-owned, separate'},{'scene':'MCMC','severity':'transient readability polish','actual_before':'Three retained-copy reveals cross previous equation/why text, e.gEN95.198/98.531/104.998s andZH102.331/106.198/114.398s. Settled equations clear; no held factualbug claimed. Accepted/rejected moves,66.4%visits/66.5%target,Langevincohort/mesh notes and mixingcomparison were checked.','repair':'Onlyderive returnedstep1/2/3 transform=False.','source_sha256':'95c38c1d058a07556f26dd86fd042dbdba8e137ff4083ea9350cbd0f919655af','fresh_render_review':'pending separate regression'},{'scene':'Brownian','severity':'transient readability polish','actual_before':'Two retained-copy reveals overlap oldrows atEN98.400/101.400s, clearheld98.867/101.867s. RawQVpath,mean±acrosspathSD table and theoreticalfan envelope interpretation were checked; outliers beyond2SD are expected.','repair':'Onlyquadraticvar returnedstep1/2 transform=False.','source_sha256':'780521544fd9ad5e9ab698bfeba6c8da2aa82b24b17433a93623dca69c444e9f','fresh_render_review':'pending separate regression'}],'repairs':repairs,'limitations':['Silent preview placeholders; no audio quality/listening/narration synchronization approval.','No continuous perceptual playback claim. Selected-time gaps and unselected frame counts remain explicit in fullauditreceipts.','No native1080 or4K motion approval.','Source/input snapshots are observed bytes and do not prove historical in-memory imports.','Six original MC/ScoreFn/MCMC movie files are no longer retained: initial hardlink witnesses were overwritten by canonical rerenders. Original audit/native PNG/rawrecord/view ledgers are retained and hashes verified. Exact fullSHA search found no independent old movie copy. Brownian movies were converted to independently copied verified baseline bytes before overwrite. Fresh regressions use independent copies.','Original source-change warnings forMCMC and ENBrownian1.5s dead-air warning retained. ENBrownian flagged transition was inspected in selected frames asfade/smallinitialcloudsetup; narrated pacing remains open.','Beforefix findings remain historical; repairs require their own actual fresh-frame reviews.']}
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
rows='\n'.join(f"|{x['case']}|{x['decoded_frames']}|{x['selected_times']}|{x['exact_png_representatives_actually_viewed']}|{x['pages_actually_viewed']}|{x['native_followups']}|"for x in CASES)
(O/'README.md').write_text('''# Part5 MonteCarlo, ScoreFn, MCMC and Brownian baseline motion review

Eight original EN/ZH silent 480p15 clips were decoded and their full selected-time cohorts reviewed. This is the historical baseline before the synchronized dart prefix and local equation-reveal repairs. Fresh repair regressions are separate.

|Case|Decoded frames|Selected times|Exact PNG representatives viewed|Pages viewed|Native follows|
|---|---:|---:|---:|---:|---:|
'''+rows+'''

Every selected time maps to an actually viewed representative or an exact PNG SHA256 match within that movie. Contact tiles were 640×360; native checks 854×480. Compressed audit and mapping receipts preserve all selected times, unselected gaps, page/image hashes, movie/rawrecord/source/input hashes and raw warnings. Original decoded PNGs, audits, raw records, source observations and viewing receipts remain under `/workspace/runtime/ai5-mc-score-mcmc-brownian-motion-review/`; this bounded package omits movies, raw caches and duplicate full sheet/frame cohorts.

The main finding was MonteCarlo's mismatch between visible dart cohort and live estimate. ScoreFn, MCMC and Brownian received bounded transition polish for copied glyphs crossing retained equations; their settled reading states were clear. See `report.json` for exact observations, changes and repair-source hashes, and `native/` for the SHA-keyed critical views.

Six old MC/ScoreFn/MCMC MP4 witnesses were hardlinks overwritten during canonical rerenders; their original movie bytes are no longer retained. Exact SHA search found no independent copy. The verified old decoded images and original audit provenance remain intact; no movie was reconstructed. Both old Brownian MP4s were independently copied and verified before overwrite. See `reconciliation/` for exact receipts.

No continuous-perception, listening, narrated synchronization, native 1080 motion or 4K approval is claimed. Source snapshots are byte observations, not historical imported-module proof. Original source-change and dead-air warnings are retained.
''')
payloads=[]
for p in sorted(O.rglob('*')):
 if p.is_file():payloads.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'sha256':sha(p)})
size=sum(x['bytes']for x in payloads);assert size<=12*1024**2,size
(O/'manifest.json').write_text(json.dumps({'created_utc':report['created_utc'],'payload_bytes':size,'payloads':payloads,'scope':'No MP4 or raw cache payload. Original image/audit ledgers preserved; six old movie bytes unavailable as disclosed;  exact hashes bind compressedfullreceipts and criticalPNG copies.'},indent=2)+'\n')
print(json.dumps({'path':str(O),'payloads':len(payloads),'bytes':size,'manifest_sha256':sha(O/'manifest.json'),'totals':report['totals']},indent=2))
