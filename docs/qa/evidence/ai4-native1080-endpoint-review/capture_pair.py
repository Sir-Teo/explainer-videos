import pathlib,subprocess,json,os,time,hashlib,datetime,sys,ast,shutil
root=pathlib.Path('/workspace/explainer-videos'); rt=pathlib.Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=ast.parse((root/'videos/ai/ai4/manifest.py').read_text()); scenes=ast.literal_eval(next(n.value for n in m.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SCENES' for t in n.targets)))
scene=sys.argv[1]; mod=next(x[0] for x in scenes if x[1]==scene)
for lang in ['en','zh']:
 out=root/'renders/qa/production-endpoints-1080/ai4'/lang/scene; result=out/'result.json'; case=rt/f'{lang}-{scene}';case.mkdir(exist_ok=True)
 paths=[root/f'videos/ai/ai4/{mod}.py',root/'videos/ai/ai4/common.py',root/'videos/ai/ai4/zh_lines.py',root/'videos/ai/ai_text_zh.json',pathlib.Path('/workspace/runtime/qa_production_endpoint.py'),root/'tools/qa_series.py']
 snapshot=lambda:[{'path':str(p.relative_to(root)) if p.is_relative_to(root) else str(p),'sha256':sha(p)} for p in paths]
 if result.exists():
  old=json.loads(result.read_text()); sizes=old.get('manual_capture_configuration',{}); assert old['mode']=='endpoints' and sizes.get('pixel_width')==1920 and old['status'] in ['passed','needs-review'];print('REUSE',lang,scene,flush=True);continue
 mem=int(next(s.split()[1] for s in pathlib.Path('/proc/meminfo').read_text().splitlines() if s.startswith('MemAvailable:')))*1024
 assert mem>=512*1024**2,mem
 disk=shutil.disk_usage("/workspace").free
 assert disk>=512*1024**2,disk
 before=snapshot(); stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
 (case/'capture-start.json').write_text(json.dumps({'utc':stamp,'MemAvailable_bytes':mem,'workspace_disk_free_bytes':disk,'sources':before,'command':['nice','-n','10','python','/workspace/runtime/qa_production_endpoint.py','ai4',lang,scene]},indent=2))
 with (case/'capture.log').open('w') as log:
  cp=subprocess.run(['nice','-n','10','python','/workspace/runtime/qa_production_endpoint.py','ai4',lang,scene],cwd=root,stdout=log,stderr=subprocess.STDOUT)
 receipt={'started_utc':stamp,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':cp.returncode,'source_before':before,'source_after':snapshot(),'result_exists':result.exists()}
 if result.exists():receipt.update(result_sha256=sha(result),status=json.loads(result.read_text())['status'])
 (case/'capture-receipt.json').write_text(json.dumps(receipt,indent=2)); print(json.dumps({'lang':lang,'scene':scene,**receipt}),flush=True)
 if cp.returncode not in [0,1] or not result.exists() or json.loads(result.read_text())['status'] not in ['passed','needs-review']:sys.exit(1)
