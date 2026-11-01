from pathlib import Path
import ast,datetime,json,hashlib,shutil,subprocess,os
B=Path('/workspace/explainer-videos');D=Path('/workspace/runtime/ai4-silent-preview-assembly/current-reviewed');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();out=D/'input-freeze.json';assert not out.exists(),'Reconcile existing freeze before retry';assert shutil.disk_usage(B).free>=512*1024**2
manifest=B/'videos/ai/ai4/manifest.py';tree=ast.parse(manifest.read_text());scenes=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SCENES' for t in n.targets)));assert len(scenes)==19
receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Parent authorizes current canonical reviewed38silent480p cases; snapshots are observations, not historical loadedmodule proof. Structured warnings retained verbatim; no compute/render/import ofscenes orproducers.','prior_operations_reconciled':{'parent_reports_none_started':True,'prior_matching_runtime_files_before_creation':['attempt1-incomplete-optional-npz-marker/reconciliation.json: freeze-onlyfailurebeforeassembly; preserved and reconciled'],'prior_matching_assembly_processes':'None besides read-only discovery shell itself.'},'manifest_sha256':sha(manifest),'source_commit_observed_at_freeze':subprocess.check_output(['git','rev-parse','HEAD'],cwd=B,text=True).strip(),'source_observations':[],'cases':[],'raw_inputs':{},'disk_free_before':shutil.disk_usage(B).free,'scenes':scenes}
source_names=['tools/build.py','explainer/voiceover.py','explainer/lang.py','explainer/tts.py','tools/qa_series.py','tools/qa_motion.py','explainer/ai/viz.py','videos/ai/ai_text_zh.json']+[str(p.relative_to(B)) for p in sorted((B/'videos/ai/ai4').glob('*.py'))]
for rel in source_names:
 p=B/rel;q=D/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists() or sha(q)==sha(p);shutil.copyfile(p,q) if not q.exists() else None;receipt['source_observations'].append({'path':rel,'bytes':p.stat().st_size,'sha256':sha(p),'snapshot':str(q)})
for lang in ['en','zh']:
 for index,(module,scene,title) in enumerate(scenes):
  folder=B/f'renders/qa/series/ai4/{lang}/{scene}_motion';rp=folder/'result.json';r=json.loads(rp.read_text());assert r['scene']==scene and r['lang']==lang and r['mode']=='motion' and r['status'] in ['passed','needs-review'];assert r['frames'] and r['duration']>0
  movie=B/r['movie'];side=movie.with_suffix('.narration.json');meta=json.loads(side.read_text());assert meta['lines']==r['narration'] and meta['lines'];mh=sha(movie);rh=sha(rp);sh=sha(side)
  c=D/lang/'chapters'/f'{index:02d}-{scene}';c.mkdir(parents=True,exist_ok=True);target=c/movie.name
  for src,dst in [(movie,target),(side,target.with_suffix('.narration.json')),(rp,c/'result.json')]:
   assert not dst.exists() or sha(dst)==sha(src);shutil.copyfile(src,dst) if not dst.exists() else None
  assert sha(movie)==sha(target)==mh and sha(rp)==rh and sha(side)==sh
  inputs=[]
  for rel,sig in r['inputs'].items():
   p=B/rel
   if sig is None:
    assert not p.exists();item={'path':rel,'exists':False,'recorded_signature':None,'scope':'Expectedabsent optionalNPZ markerforJSONonlyproducer, confirmedstillabsent.'};receipt['raw_inputs'][rel]=item;inputs.append(item);continue
   st=p.stat();assert [st.st_size,st.st_mtime_ns]==sig;ih=sha(p);old=receipt['raw_inputs'].get(rel);item={'path':rel,'bytes':st.st_size,'mtime_ns':st.st_mtime_ns,'sha256':ih};assert old is None or old==item;receipt['raw_inputs'][rel]=item;inputs.append(item)
  receipt['cases'].append({'lang':lang,'index':index,'module':module,'scene':scene,'title_en':title,'source_file':f'videos/ai/ai4/{module}.py','source_sha256':sha(B/f'videos/ai/ai4/{module}.py'),'original_movie':str(movie),'frozen_movie':str(target),'movie_sha256':mh,'movie_bytes':target.stat().st_size,'original_record':str(rp),'frozen_record':str(c/'result.json'),'record_sha256':rh,'sidecar_sha256':sh,'record_status':r['status'],'record_warnings':r['warnings'],'record_fingerprint':r['fingerprint'],'duration':r['duration'],'consumed_inputs':r['inputs'],'input_identities':inputs})
for c in receipt['cases']:assert sha(c['original_movie'])==c['movie_sha256'] and sha(c['original_record'])==c['record_sha256']
for x in receipt['source_observations']:assert sha(B/x['path'])==x['sha256']
receipt['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();out.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n');print('frozen38cases',len(receipt['raw_inputs']),'rawinputs,',sum(c['movie_bytes'] for c in receipt['cases']),'moviebytes,',sum(bool(c['record_warnings']) for c in receipt['cases']),'warningcases; SHA',sha(out))
