from pathlib import Path
import datetime,gzip,hashlib,json,shutil,subprocess
R=Path('/workspace/explainer-videos');O=Path(__file__).parent;B=Path('/workspace/runtime/ai5-mc-score-mcmc-brownian-endpoint-review');FIX=Path('/workspace/runtime/ai5-local-plot-readability-repair');P=R/'docs/qa/evidence/ai5-mc-score-brownian-visual-regression'
P.mkdir(parents=True,exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def space():
 s=shutil.disk_usage(R)
 if s.free<512*1024**2:raise RuntimeError('Stop: less than512MiBfree')
def copy(src,relative):
 space();dst=P/relative;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);assert sha(src)==sha(dst);return str(dst.relative_to(P))
gzip_receipts=[]
def compressed(src,relative):
 space();src=Path(src);dst=P/relative;dst.parent.mkdir(parents=True,exist_ok=True);data=src.read_bytes()
 with gzip.GzipFile(filename=str(dst),mode='wb',mtime=0) as f:f.write(data)
 assert gzip.decompress(dst.read_bytes())==data
 gzip_receipts.append({'path':str(dst.relative_to(P)),'source_observation':str(src),'decoded_bytes':len(data),'decoded_sha256':hashlib.sha256(data).hexdigest()});return str(dst.relative_to(P))
assets={}
def asset(src):
 h=sha(src);dest='images/'+h+'.png'
 if h not in assets:copy(src,dest);assets[h]={'path':dest,'sha256':h,'bytes':Path(src).stat().st_size}
 return dest
review=json.loads((O/'report.json').read_text());comparison=json.loads((O/'comparison-reviewed.json').read_text());base_report=json.loads((B/'report.json').read_text());base_views=json.loads((B/'view-receipts.json').read_text());current_views=json.loads((O/'native-view-receipts.json').read_text())
# Every freshframe has a reviewable losslessPNG; exactbeforestates deduplicate.
for row in comparison['rows']:
 row['after_asset']=asset(Path(row['after_path']));row['before_asset']=asset(Path(row['before_path']))
for view in current_views:view['asset']=asset(Path(view['path']))
# Persist the actualprior sheets and32native views, includinghistoricalMCMC.
for view in base_views:
 view['asset']=asset(B/view['path'])
(P/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n');compressed(P/'comparison.json','comparison.json.gz');(P/'comparison.json').unlink()
(P/'current-native-view-receipts.json').write_text(json.dumps(current_views,indent=2)+'\n');compressed(P/'current-native-view-receipts.json','current-native-view-receipts.json.gz');(P/'current-native-view-receipts.json').unlink()
(P/'baseline-view-receipts.json').write_text(json.dumps(base_views,indent=2)+'\n');compressed(P/'baseline-view-receipts.json','baseline-view-receipts.json.gz');(P/'baseline-view-receipts.json').unlink()
copy(O/'report.json','report.json');compressed(B/'report.json','baseline/report.json.gz');compressed(B/'readout-crosscheck.json','baseline/readout-crosscheck.json.gz');copy(B/'report.md','baseline/README.md')
raw_receipts=[]
for kind,root in [('before',B),('after',O)]:
 for case in sorted((root/'cases').iterdir()):
  f=json.loads((case/'freeze.json').read_text());prefix=f'{kind}/{f["lang"]}-{f["scene"]}'
  for name in ['result.json','text.jsonl','render.log','freeze.json']:compressed(case/name,'raw/'+prefix+'/'+name+'.gz')
  raw_receipts.append({'kind':kind,'case':case.name,'lang':f['lang'],'scene':f['scene'],'raw_status':f['raw_status'],'raw_warnings':f['raw_warnings'],'sheet_asset':asset(case/'sheet.png'),'source_observations':f['source_observations'],'inputs':f['inputs']})
# Exactdirect before/aftersource snapshots; source observations, not importproof.
for src in sorted((FIX/'before').glob('*.py')):compressed(src,'sources/before/'+src.name+'.gz')
for name in ['s13_montecarlo.py','s14_scorefn.py','s16_brownian.py','plotting.py']:compressed(R/'videos/ai/ai5'/name,'sources/after/'+name+'.gz')
# Sharedtable/localZHobservations from before/afterfreezes, deduplicatedbySHA.
for kind,root in [('before',B),('after',O)]:
 for file in sorted((root/'source-blobs').iterdir()):
  compressed(file,'source-observations/'+kind+'/'+file.name+'.gz')
for name in ['report.json','proposed-zh-overlay.json','geometry-results.json','tests-final.log','tests-caught-out-of-scope-spacing.log','test_and_geometry.py','make_overlay.py']:
 compressed(FIX/name,'source-repair/'+name+'.gz')
copy(FIX/'source-diff.patch.gz','source-repair/source-diff.patch.gz')
for name in ['full-unittest.log','receipt.json','source-before.json','source-after.json']:compressed(Path('/workspace/runtime/integrated-20261101-ai5-visual-repairs')/name,'root-integration/'+name+'.gz')
for name in ['freeze_cases.py','compare.py','finalize_review.py','package.py']:copy(O/name,'scripts/'+name)
critical=[]
selected=[('en','MonteCarlo','007_00060.5s.png'),('zh','MonteCarlo','007_00067.9s.png'),('en','ScoreFn','007_00062.2s.png'),('zh','ScoreFn','007_00060.9s.png'),('en','Brownian','008_00118.7s.png'),('zh','Brownian','009_00114.2s.png')]
for language,scene,name in selected:
 row=next(x for x in comparison['rows'] if x['lang']==language and x['scene']==scene and x['file']==name);critical.append({'lang':language,'scene':scene,'time':row['time'],'before':row['before_asset'],'after':row['after_asset']})
(P/'critical-before-after.json').write_text(json.dumps(critical,indent=2)+'\n');(P/'raw-provenance.json').write_text(json.dumps(raw_receipts,indent=2)+'\n');(P/'gzip-original-byte-receipts.json').write_text(json.dumps(gzip_receipts,indent=2)+'\n');(P/'image-assets.json').write_text(json.dumps(list(assets.values()),indent=2)+'\n')
rows='\n'.join(f'| {x["case"].split("-")[0].upper()} {x["case"].split("-")[1]} | {x["states"]} | {x["exact_png"]} | {x["changed"]} |' for x in review['cases'])
links='\n'.join(f'| {x["lang"].upper()} {x["scene"]} | [before]({x["before"]}) | [after]({x["after"]}) |' for x in critical)
(P/'README.md').write_text('''# Part 5 selected endpoint regression

**Accepted for the reviewed endpoint states.** All 93 fresh states are accounted for: 77 PNGs are byte-identical to previously viewed baseline states; all 16 changed images were actually inspected at native 854×480. No new endpoint defect was observed. This is not full motion or audio approval.

| Case | Captured states | Exact PNG inheritance | Changed states viewed native |
| --- | ---: | ---: | ---: |
'''+rows+'''

MonteCarlo now uses a clearly labelled 2.6–3.7 vertical window and outward triangle markers for estimates outside it. The data line has no fabricated flat caps. The final 3.158 readout, rare-hit cohorts and ESS panels remain unchanged. ScoreFn shows a straight score line cropped at the viewport; its ES smoothed-objective star and diagnostics remain unchanged. Brownian retains the raw extreme path values in the expanded local range and explicitly labels the mean/± across-path standard deviation in English and Chinese.

| Critical comparison | Before | After |
| --- | --- | --- |
'''+links+'''

Every fresh PNG is retained losslessly and deduplicated by SHA. `comparison.json.gz` maps all 93 before/after PNG and decoded RGB identities to actual baseline-view receipts. All 77 inherited images match both PNG bytes and RGB pixels; there are no RGB-only substitutions. Sixteen unchanged native followups inherit exact native-view evidence, in addition to the 16 newly viewed native states. The original eight-case baseline covers 130 states at 427×240 sheet-tile scale and 32 native followups. Historical MCMC baseline views remain historical; this package does not claim a fresh current-fingerprint MCMC review.

The six fresh raw runtime records report passed with zero warnings. Their original visual/full-playback/narrated-playback pending flags are preserved in compressed raw evidence. All narration captures, selected times/reasons, total durations and input signatures match the baseline exactly. Current canonical PNG/record/text/log/sheet bytes, source observations and consumed data bytes were verified unchanged after review. Broad fingerprints differ between baseline and fresh runs and remain explicit; source snapshots are observations, not proof of historical in-memory imports.

`raw/` preserves exact original records, text collections, render logs and freezes as lossless gzip. `sources/` and `source-repair/` preserve before/after code, the private caption proposal, geometry and focused tests. `root-integration/` retains the root-owned 507-test/47.923-second passing receipt and source inventory; the reviewer did not rerun that suite or numerical experiments. `gzip-original-byte-receipts.json` records decoded hashes. No movies or numerical-cache payload copies are included.

Remaining gates: full/dense motion and transition review; continuous perceptual playback; real narration/audio/listening/synchronization; native 1080p/4K; player/responsive behaviour. In particular, the first MonteCarlo 4.000 readout and early triangle entrance are absent from these endpoint captures and still need actual motion verification. No source, pipeline, cache or translation-table changes, renders, commits or uploads were performed during this regression review.
''')
files=[f for f in P.rglob('*') if f.is_file() and f.name!='manifest.json']
manifest={'schema':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Selected endpoint regression only; no full motion/audio/native1080/4K/production approval.','file_count':len(files),'payload_bytes':sum(f.stat().st_size for f in files),'files':[{'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(files)]}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for item in manifest['files']:assert sha(P/item['path'])==item['sha256']
print(json.dumps({'package':str(P),'files':len(files),'payload_bytes':manifest['payload_bytes'],'image_assets':len(assets),'manifest_sha256':sha(P/'manifest.json')},indent=2))
