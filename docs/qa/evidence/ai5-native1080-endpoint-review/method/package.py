import pathlib,json,gzip,hashlib,shutil,datetime
from PIL import Image
b=pathlib.Path(__file__).parent;root=pathlib.Path('/workspace/explainer-videos');out=root/'docs/qa/evidence/ai5-native1080-endpoint-review'
assert not out.exists(),'new supplement only'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def gz(dest,data):
 dest.parent.mkdir(parents=True,exist_ok=True)
 with gzip.GzipFile(filename=str(dest),mode='wb',mtime=0) as f:f.write(data)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();summary=[];source_manifest={}
cases=[(l,s) for s in ['Hook','Bell','Gauss','Likelihood','Fisher','Decoding','Markov'] for l in ['en','zh']]+[('zh',s) for s in ['Bayes','MaxEnt','Tails']]
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
 review={'case':f'{lang}/{s}','completed':now,'outcome':'No new corrective typography/geometry defect observed in native endpoint scope.','coverage':{'frames':len(p['frames']),'pages':len(v['pages']),'original_size_followups':len(v['native']),'all_native_sizes':[1920,1080],'all_endpoint_frame_indices':list(range(len(p['frames'])))},'frames':p['frames'],'pages':v['pages'],'native':v['native'],'capture_receipt':r,'raw_warnings':r['warnings'],'known_capture_limitations':known,'limits':limitations,'new_defects':[]}
 (c/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 d=out/lang/s;d.mkdir(parents=True)
 for name in ['review.json','plan.json','views.json','capture-start.json','capture-receipt.json','raw-result.json','raw-text.jsonl','raw-render.log','capture.log']:
  if (c/name).exists():gz(d/(name+'.gz'),(c/name).read_bytes())
 for old in sorted((c/'standard-before').glob('*')):gz(d/'standard-before'/(old.name+'.gz'),old.read_bytes())
 for n in v['native']:
  dest=d/'native'/pathlib.Path(n['file']).name;dest.parent.mkdir(exist_ok=True);shutil.copy2(c/n['file'],dest)
 # Full reviewed page identities are in review; one actual representative page per case is retained.
 page=v['pages'][-1];(d/'example').mkdir();shutil.copy2(c/page['file'],d/'example'/pathlib.Path(page['file']).name)
 for source in r['source_before']:
  fp=c/'source'/pathlib.Path(source['path']).name;assert sha(fp)==source['sha256'];key=source['sha256']
  if key not in source_manifest:
   name=f"{key[:16]}-{fp.name}.gz";gz(out/'sources'/name,fp.read_bytes());source_manifest[key]={'file':'sources/'+name,'source_sha256':key,'bytes':len(fp.read_bytes()),'original_paths':[]}
  if source['path'] not in source_manifest[key]['original_paths']:source_manifest[key]['original_paths'].append(source['path'])
 summary.append({'case':f'{lang}/{s}','frames':len(p['frames']),'pages':len(v['pages']),'original_size_followups':len(v['native']),'raw_status':r['status'],'raw_warnings':r['warnings'],'record_sha256':r['record_sha256'],'direct_source':r['source_before'][0],'known_capture_limitations':known,'visual_outcome':review['outcome']})
report={'scope':'Part5 authorized native1080 endpoints: seven EN/ZH chapter pairs plus ZH Bayes/MaxEnt/Tails;17cases only.','completed':now,'cases':summary,'totals':{k:sum(x[k] for x in summary) for k in ['frames','pages','original_size_followups']},'source_snapshots_unchanged_during_all_cases':True,'shared_caption_table_sha256':'c2914a2973672064f4cc508af8659a00ad0a07bce7398490e157b49439c494ef','wrapper_sha256':'87a00a2438f120958c658343893d6b0d36934a65d8438beb7790f77384f88a9d','capture_session':{'id':53772,'exit_code':0,'serial':True,'nice':15,'numeric_threads':1,'disk_guard_bytes':512*1024**2},'no_source_core_producer_cache_edits':True,'no_full_motion_audio_approval':True}
(out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(b/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(out/'sources.json').write_text(json.dumps(list(source_manifest.values()),indent=2)+'\n')
rows=['| Case | Native PNGs | Pages viewed | Original-size checks | Raw result |','|---|---:|---:|---:|---|']
for x in summary:rows.append(f"| {x['case']} | {x['frames']} | {x['pages']} | {x['original_size_followups']} | {x['raw_status']} |")
(out/'README.md').write_text('''# Part5 native1080 endpoint review

All **299 native1920×1080 endpoint images** across the authorized **17 cases** were inspected on **80 chronological pages** at960×540 per image, with **42 separately inspected original1920×1080 followups**. These are new native captures, not inferences from the earlier480p evidence. No new corrective typography/geometry defect was found in this scope.

'''+ '\n'.join(rows)+'''

The unchanged private wrapper ran serially at nice15 with one numeric thread, cached-only data and a512MiB free-disk guard before each case. The capture queue exited0. Before each capture, exact direct/shared source snapshots and standard endpoint result/text/log identities were preserved. Native raw records, every frame timestamp/SHA256/size, input hashes, page/view receipts and warnings are retained in compressed case ledgers. Source snapshots were identical before/after every case; the shared caption table was c2914a29…. Input byte hashes were taken after each capture with matching captured size/mtime, then rechecked when packaging.

**Raw warning preserved:** EN Bell is needs-review with `source-changed-during-render`, despite unchanged scoped source snapshots; the remaining16 native records passed with no warnings. This review does not silently rewrite that warning or assert an aggregate fingerprint is current solely from matching direct modules.

**Known endpoint-capture limitations preserved:** Markov EN/ZH step1 can retain an old100% q bar/tag after skipped animations; MaxEnt ZH step60 can show uniform old bars beside final lambda/mean text until a later hold. These exact native examples remain in the package. They are excluded from real-motion correctness conclusions; actual silent-motion reviews are separate evidence. No source repair is inferred from these known skipped-updater artifacts.

The original-size examples cover score-field legends, plan rows, convolution/conditional derivations, likelihood hill labels, Fisher benchmark/regularity/residual qualifications, decoding samples/metric definitions/SE disclaimer, detailed balance/mixing bounds, posterior intervals/MAP, inverse temperature, concentration bounds and the first262-versus-all-n≥281 coin-count distinction.

Full native images/pages remain in `/workspace/runtime/ai5-production1080-review/` and separate canonical `renders/qa/production-endpoints-1080/ai5/`. This bounded repository supplement retains all critical original-size PNGs, one actual page per case, complete compressed coverage/provenance and deduplicated source snapshots. It changes no scene, numerical core, producer, data/cache, translation table or CI configuration.

**Limits:** skipped-animation silent endpoints only. This does not approve1080p full motion, continuous perceptual playback, narration/listening/synchronization or assembled reels. It covers only the listed17 cases, not all Part5 chapters.
''')
(out/'method').mkdir()
for name in ['capture.py','mark.py','native.py','package.py']:shutil.copy2(b/name,out/'method'/name)
shutil.copy2(b/'queue.log',out/'method/queue.log')
manifest=[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'out':str(out),'files':len(manifest)+1,'bytes':sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),'manifest_sha256':sha(out/'manifest.json'),'totals':report['totals']}))
