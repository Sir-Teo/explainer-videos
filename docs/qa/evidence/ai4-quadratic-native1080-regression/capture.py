import pathlib,json,subprocess,shutil,hashlib,datetime,ast
repo=pathlib.Path('/workspace/explainer-videos');rt=pathlib.Path(__file__).parent;oldrt=rt.parent/'ai4-production1080-review';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'Quadratic':('s15_quadratic','8b387c3a6f707b35b275bfb56a2daba1219707bd6e8c573bbf8ca2456390d68e')}
for scene,(module,expectedsha) in expected.items():
 for lang in ['en','zh']:
  case=f'{lang}-{scene}';dst=rt/case;dst.mkdir(exist_ok=True);assert not (dst/'receipt.json').exists(),'reconcile existing receipt before rerun'
  canonical=repo/'renders/qa/production-endpoints-1080/ai4'/lang/scene;old=oldrt/case;before=dst/'before';before.mkdir(exist_ok=True)
  assert sha(canonical/'result.json')==sha(old/'render-result.json'),'canonical differs from prior reviewed record; reconcile'
  d=json.loads((old/'review.json').read_text());assert d['complete']
  for f in ['render-result.json','review.json','capture-start.json','capture-receipt.json']+[x['file'] for x in d['frames']]:shutil.copy2(old/f,before/f)
  paths=[repo/f'videos/ai/ai4/{module}.py',repo/'videos/ai/ai4/common.py',repo/'videos/ai/ai4/zh_lines.py',repo/'videos/ai/ai_text_zh.json',repo/'tools/qa_series.py',repo/'explainer/ai/viz.py',rt.parent/'qa_production_endpoint.py'];snapshot=lambda:[{'path':str(p),'sha256':sha(p)} for p in paths];source=snapshot();assert source[0]['sha256']==expectedsha
  mem=int(next(x.split()[1] for x in pathlib.Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024;disk=shutil.disk_usage('/workspace').free;assert min(mem,disk)>=512*1024**2
  start={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':source,'MemAvailable_bytes':mem,'workspace_disk_free_bytes':disk,'command':['nice','-n','10','python','/workspace/runtime/qa_production_endpoint.py','ai4',lang,scene]};(dst/'start.json').write_text(json.dumps(start,indent=2))
  with (dst/'capture.log').open('w') as log:cp=subprocess.run(start['command'],cwd=repo,stdout=log,stderr=subprocess.STDOUT)
  after=snapshot();r=json.loads((canonical/'result.json').read_text());assert r['status'] in ['passed','needs-review'] and cp.returncode in [0,1]
  fresh=dst/'after';fresh.mkdir(exist_ok=True);shutil.copy2(canonical/'result.json',fresh/'render-result.json')
  for f in r['frames']:shutil.copy2(canonical/f['file'],fresh/f['file'])
  for p in paths:shutil.copy2(p,dst/p.name)
  receipt={'started':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources_after':after,'sources_stable':source==after,'returncode':cp.returncode,'result_sha256':sha(fresh/'render-result.json'),'status':r['status'],'warnings':r['warnings']};(dst/'receipt.json').write_text(json.dumps(receipt,indent=2));print(case,cp.returncode,r['status'],len(r['frames']),r['warnings'],flush=True)
