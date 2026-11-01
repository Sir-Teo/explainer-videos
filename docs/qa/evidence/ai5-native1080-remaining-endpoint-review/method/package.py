import pathlib,json,gzip,hashlib,shutil,datetime
from PIL import Image
b=pathlib.Path(__file__).parent;root=pathlib.Path('/workspace/explainer-videos');out=root/'docs/qa/evidence/ai5-native1080-remaining-endpoint-review'
assert not out.exists(),'new supplement only'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def gz(dest,data):
 dest.parent.mkdir(parents=True,exist_ok=True)
 with gzip.GzipFile(filename=str(dest),mode='wb',mtime=0) as f:f.write(data)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();summary=[];source_manifest={}
cases=[('en',s) for s in ['Bayes','MaxEnt','Tails']]+[(l,s) for s in ['Sampling','MonteCarlo','ScoreFn','MCMC','Brownian','Ito','SDE','FokkerPlanck','Outro'] for l in ['en','zh']]
for lang,s in cases:
 c=b/f'{lang}-{s}';p=json.loads((c/'plan.json').read_text());v=json.loads((c/'views.json').read_text());r=p['receipt'];raw=json.loads((c/'raw-result.json').read_text())
 assert len(v['pages'])==len(p['pages']);assert sorted(i for pg in v['pages'] for i in pg['frame_indices'])==list(range(len(p['frames'])))
 assert r['source_unchanged'];assert r['source_before']==r['source_after'];assert raw['manual_capture_configuration']['wrapper_sha256']=='87a00a2438f120958c658343893d6b0d36934a65d8438beb7790f77384f88a9d'
 assert sha(c/'raw-result.json')==r['record_sha256']
 for fr in p['frames']:
  path=c/'frames'/fr['file'];assert sha(path)==fr['sha256'];assert Image.open(path).size==(1920,1080)
 for pg in p['pages']:assert sha(c/pg['file'])==pg['sha256']
 for n in v['native']:assert sha(c/n['file'])==n['sha256']
 for inp in r['inputs']:
  assert inp['record_size_mtime']==inp['current_size_mtime'];assert sha(root/inp['path'])==inp['sha256']
 limitations=['Silent skipped-animation endpoint images only; no1080p full-motion, continuous perception, narration listening/synchronization or assembled-reel approval.','Every native endpoint was viewed on declared960x540 tiles; named critical followups were separately viewed at original1920x1080.','Input byte hashes were recorded after the completed capture, with captured size/mtime matching files then and package-time hash recheck.']
 known=[]
 if s=='Markov':known.append({'kind':'known-skipped-animation-updater-limitation','frame_index':8,'detail':'Step1 endpoint can retain old q=100% tag/bar with updated state. It is excluded from real-motion correctness conclusions; separate selected full-motion review handles actual animation.'})
 if s=='MaxEnt':known.append({'kind':'known-skipped-animation-updater-limitation','frame_index':9,'detail':'Step60 endpoint may retain uniform old bars while lambda/mean text is final; subsequent hold catches up. Excluded from real-motion correctness conclusions; separate selected full-motion case was reviewed.'})
 review={'case':f'{lang}/{s}','completed':now,'outcome':'No new corrective typography/geometry defect observed in native endpoint scope.','coverage':{'frames':len(p['frames']),'pages':len(v['pages']),'original_size_followups':len(v['native']),'all_native_sizes':[1920,1080],'all_endpoint_frame_indices':list(range(len(p['frames'])))},'frames':p['frames'],'pages':v['pages'],'native':v['native'],'capture_receipt':r,'raw_warnings':r['warnings'],'known_capture_limitations':known,'limits':limitations,'new_defects':[], 'reported_findings_history':v['findings'], 'native_crops':v.get('native_crops',[])}
 (c/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 d=out/lang/s;d.mkdir(parents=True)
 for name in ['review.json','plan.json','views.json','capture-start.json','capture-receipt.json','raw-result.json','raw-text.jsonl','raw-render.log','capture.log']:
  if (c/name).exists():gz(d/(name+'.gz'),(c/name).read_bytes())
 for old in sorted((c/'standard-before').glob('*')):gz(d/'standard-before'/(old.name+'.gz'),old.read_bytes())
 for n in v['native']:
  dest=d/'native'/pathlib.Path(n['file']).name;dest.parent.mkdir(exist_ok=True);shutil.copy2(c/n['file'],dest)
 for crop in v.get('native_crops',[]):
  assert sha(c/crop['file'])==crop['sha256'];shutil.copy2(c/crop['file'],d/crop['file'])
 # Full reviewed page identities are in review; one actual representative page per case is retained.
 page=v['pages'][-1];(d/'example').mkdir();shutil.copy2(c/page['file'],d/'example'/pathlib.Path(page['file']).name)
 for source in r['source_before']:
  fp=c/'source'/pathlib.Path(source['path']).name;assert sha(fp)==source['sha256'];key=source['sha256']
  if key not in source_manifest:
   name=f"{key[:16]}-{fp.name}.gz";gz(out/'sources'/name,fp.read_bytes());source_manifest[key]={'file':'sources/'+name,'source_sha256':key,'bytes':len(fp.read_bytes()),'original_paths':[]}
  if source['path'] not in source_manifest[key]['original_paths']:source_manifest[key]['original_paths'].append(source['path'])
 summary.append({'case':f'{lang}/{s}','frames':len(p['frames']),'pages':len(v['pages']),'original_size_followups':len(v['native']),'raw_status':r['status'],'raw_warnings':r['warnings'],'record_sha256':r['record_sha256'],'direct_source':r['source_before'][0],'known_capture_limitations':known,'visual_outcome':review['outcome']})
report={'scope':'Part5 remaining21 native1080 endpoint cases: EN Bayes/MaxEnt/Tails plus EN/ZH Sampling through Outro, complementing immutable first17case package.','completed':now,'cases':summary,'totals':{k:sum(x[k] for x in summary) for k in ['frames','pages','original_size_followups']},'source_snapshots_unchanged_during_all_cases':True,'shared_caption_table_sha256':'c2914a2973672064f4cc508af8659a00ad0a07bce7398490e157b49439c494ef','wrapper_sha256':'87a00a2438f120958c658343893d6b0d36934a65d8438beb7790f77384f88a9d','capture_session':{'id':78207,'exit_code':0,'serial':True,'nice':15,'numeric_threads':1,'disk_guard_bytes':512*1024**2},'no_source_core_producer_cache_edits':True,'no_full_motion_audio_approval':True}
(out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(b/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
start=json.loads((b/'shared-observed-start.json').read_text())
shared_end=[]
for sp in sorted((b/'shared-observed-start').rglob('*')):
 if sp.is_file():
  rel=sp.relative_to(b/'shared-observed-start'); current=root/rel
  assert sha(sp)==sha(current)
  shared_end.append({'path':str(rel),'observed_start_sha256':sha(sp),'package_time_sha256':sha(current),'unchanged':True})
  gz(out/'shared-observed-start'/(str(rel)+'.gz'),sp.read_bytes())
(out/'shared-observed-start.json').write_text(json.dumps(start,indent=2)+'\n')
(out/'shared-observed-end.json').write_text(json.dumps({'at':now,'entries':shared_end,'qualification':'Observed just after firstENBayes launch; not pre-import attestation.'},indent=2)+'\n')
(out/'sources.json').write_text(json.dumps(list(source_manifest.values()),indent=2)+'\n')
rows=['| Case | Native PNGs | Pages viewed | Original-size checks | Raw result |','|---|---:|---:|---:|---|']
for x in summary:rows.append(f"| {x['case']} | {x['frames']} | {x['pages']} | {x['original_size_followups']} | {x['raw_status']} |")
(out/'README.md').write_text("""# Part5 remaining native1080 endpoint review

All **305 native1920×1080 endpoints** in the **21 cases** below were inspected on **84 chronological pages at960×540 per image**, with **51 original1920×1080 followups** and two additional unscaled Brownian panel crops. These actual native captures complement the immutable first17case/299image package; together they cover all38Part5 language/chapter cases and604native endpoints. No new corrective typography/geometry defect was confirmed here.

"""+'\n'.join(rows)+"""

The unchanged private wrapper ran serially at nice15 with one numeric thread, cached-only data and a512MiB free-disk guard per case. Session78207 exited0. All21raw records passed with zero warnings. All21direct/scoped source snapshots matched before/after capture, and input SHA256/size/mtime matched preserved records and the package-time recheck. Every image timestamp/SHA256/size, all viewed-page identities, actual original-size followups, raw records/text/logs, standard480endpoint provenance and source snapshots are retained in compressed ledgers. No previous native case existed for this21case scope; no old native review was inherited.

**Provenance qualification:** the unchanged capture driver records direct modules, common.py, plotting.py, localZH/global tables and wrapper/QA scripts before each case. Its legacy optional shared-viz path was absent. The actual `explainer/ai` viz/lecture/fonts/init snapshots were separately observed immediately after the firstENBayes capture launched, before its result, then hash-compared at packaging. This shared observation is not represented as a pre-import snapshot. Parent attested those helpers frozen. Exact observed-start/end receipts are included.

**Known skipped-updater limitation:** ENMaxEnt step60 endpoint9 retains uniform old bars beside final lambda/mean text; the subsequent hold catches up. This endpoint is excluded from real-motion correctness conclusions; its actual original native and separate silent-motion review remain available. No source repair is inferred from this capture artifact.

**Withdrawn observation preserved:** I initially misread the large inline Brownian QV table as right-clipped (EN8/ZH9). Tight original-resolution panel crops show complete3.2values and all three rows with right margin; parent independently confirmed. The ledger retains the original report and withdrawal. No Brownian clipping repair is warranted. Its time label lies among expected plot ink but remains legible.

Critical originals cover posterior intervals/MAP, inverse-temperature/exponential-family derivation, concentration hypotheses/counts, sampling polar/Gumbel formulas, genuine rare-hit rugs and full-draw/subset labels, ESS proxy qualification, score derivatives/baseline variance/ES censoring, MH/MALA/halfspace statistics, Brownian QV/standard deviation, Ito nonanticipation, Euler strong/weak error, exact-bin/window-conditional histogram metrics, reverse-SDE scope and dense recap/exercise/bibliography pages.

Full native images/pages remain in `/workspace/runtime/ai5-production1080-remaining-review/` and separate canonical `renders/qa/production-endpoints-1080/ai5/`. This bounded supplement includes all51actually inspected original native PNGs, both Brownian crops, one reviewed page per case, complete compressed ledgers and deduplicated source snapshots. The first17case package is unchanged. No scene/scientific producer/cache/translation/CI was changed.

**Limits:** silent skipped-animation endpoints only; page views are960×540tiles, not every original inspected unscaled. Native1080full motion, continuous perceptual playback, audio/listening/synchronization and assembled-reel approval remain separate gates. Render success alone is not visual acceptance.
""")

(out/'method').mkdir()
for name in ['capture.py','mark.py','native.py','package.py']:shutil.copy2(b/name,out/'method'/name)
shutil.copy2(b/'queue.log',out/'method/queue.log')
manifest=[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'out':str(out),'files':len(manifest)+1,'bytes':sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),'manifest_sha256':sha(out/'manifest.json'),'totals':report['totals']}))
