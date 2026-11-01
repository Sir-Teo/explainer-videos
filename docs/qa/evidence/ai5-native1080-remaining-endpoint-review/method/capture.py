import pathlib,subprocess,json,os,hashlib,datetime,ast,shutil,sys
from PIL import Image,ImageDraw
root=pathlib.Path('/workspace/explainer-videos');rt=pathlib.Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=ast.parse((root/'videos/ai/ai5/manifest.py').read_text());scenes=ast.literal_eval(next(n.value for n in manifest.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SCENES' for t in n.targets)))
mods={s:m for m,s,_ in scenes}
cases=[('en',s) for s in ['Bayes','MaxEnt','Tails']]+[(l,s) for s in ['Sampling','MonteCarlo','ScoreFn','MCMC','Brownian','Ito','SDE','FokkerPlanck','Outro'] for l in ['en','zh']]
for lang,scene in cases:
 case=rt/f'{lang}-{scene}';case.mkdir(exist_ok=True)
 if (case/'plan.json').exists():print('ALREADY FROZEN',lang,scene,flush=True);continue
 out=root/'renders/qa/production-endpoints-1080/ai5'/lang/scene;result=out/'result.json'
 paths=[root/f'videos/ai/ai5/{mods[scene]}.py',root/'videos/ai/ai5/common.py',root/'videos/ai/ai5/plotting.py',root/'videos/ai/ai5/zh_lines.py',root/'videos/ai/ai_text_zh.json',pathlib.Path('/workspace/runtime/qa_production_endpoint.py'),root/'tools/qa_series.py',root/'videos/ai/viz.py']
 snapshot=lambda:[{'path':str(p.relative_to(root)) if p.is_relative_to(root) else str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in paths if p.exists()]
 sources=snapshot()
 for entry in sources:
  p=root/entry['path'] if not entry['path'].startswith('/') else pathlib.Path(entry['path']);dest=case/'source'/p.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(p,dest)
 standard=root/'renders/qa/series/ai5'/lang/scene
 prior={}
 for name in ['result.json','text.jsonl','render.log']:
  p=standard/name
  if p.exists():
   dest=case/'standard-before'/name;dest.parent.mkdir(exist_ok=True);shutil.copy2(p,dest);prior[name]={'sha256':sha(p),'bytes':p.stat().st_size}
 if (standard/'result.json').exists():
  sd=json.loads((standard/'result.json').read_text());prior['frames']=[{'file':f['file'],'time':f['time'],'sha256':sha(standard/f['file'])} for f in sd['frames']]
 disk=shutil.disk_usage('/workspace').free;assert disk>=512*1024**2,disk
 mem=int(next(s.split()[1] for s in pathlib.Path('/proc/meminfo').read_text().splitlines() if s.startswith('MemAvailable:')))*1024
 stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
 command=['nice','-n','15','python','/workspace/runtime/qa_production_endpoint.py','ai5',lang,scene]
 (case/'capture-start.json').write_text(json.dumps({'utc':stamp,'sources':sources,'standard_before':prior,'disk_free_bytes':disk,'MemAvailable_bytes':mem,'command':command},indent=2))
 reused=result.exists()
 if not reused:
  with (case/'capture.log').open('w') as log:cp=subprocess.run(command,cwd=root,stdout=log,stderr=subprocess.STDOUT)
  code=cp.returncode
 else:code=None
 assert result.exists(),(lang,scene,code)
 d=json.loads(result.read_text());assert d['status'] in ['passed','needs-review'],(lang,scene,d['status'])
 assert d['manual_capture_configuration']['pixel_width']==1920
 end=datetime.datetime.now(datetime.timezone.utc).isoformat();after=snapshot()
 inputs=[]
 for ip,stampmeta in d['inputs'].items():
  p=root/ip; inputs.append({'path':ip,'sha256':sha(p),'bytes':p.stat().st_size,'record_size_mtime':stampmeta,'current_size_mtime':[p.stat().st_size,p.stat().st_mtime_ns]})
 frames=[];(case/'frames').mkdir(exist_ok=True)
 for i,f in enumerate(d['frames']):
  p=out/f['file'];assert Image.open(p).size==(1920,1080)
  shutil.copy2(p,case/'frames'/p.name)
  frames.append({**f,'index':i,'sha256':sha(p),'bytes':p.stat().st_size,'size':[1920,1080]})
 for name in ['result.json','text.jsonl','render.log']:
  if (out/name).exists():shutil.copy2(out/name,case/('raw-'+name))
 (case/'pages').mkdir(exist_ok=True);pages=[]
 for start in range(0,len(frames),4):
  chosen=frames[start:start+4];sheet=Image.new('RGB',(1920,1144),(15,20,27));draw=ImageDraw.Draw(sheet)
  for pos,f in enumerate(chosen):
   x=(pos%2)*960;y=(pos//2)*572;draw.text((x+8,y+7),f"{lang}/{scene} endpoint{f['index']} {f['time']:.3f}s",fill='white')
   with Image.open(case/'frames'/f['file']) as im:sheet.paste(im.resize((960,540)),(x,y+32))
  dest=case/'pages'/f'page-{len(pages)+1:03d}.png';sheet.save(dest)
  pages.append({'page':len(pages)+1,'file':str(dest.relative_to(case)),'sha256':sha(dest),'frame_indices':[f['index'] for f in chosen],'tile_size':[960,540]})
 receipt={'case':f'{lang}/{scene}','started':stamp,'completed':end,'returncode':code,'existing_output_reused':reused,'source_before':sources,'source_after':after,'source_unchanged':sources==after,'inputs':inputs,'record_sha256':sha(result),'status':d['status'],'warnings':d['warnings'],'configuration':d['manual_capture_configuration'],'standard_before':prior}
 (case/'capture-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 (case/'plan.json').write_text(json.dumps({'case':f'{lang}/{scene}','frames':frames,'pages':pages,'receipt':receipt},ensure_ascii=False,indent=2)+'\n')
 (case/'views.json').write_text(json.dumps({'pages':[],'native':[],'findings':[]},indent=2)+'\n')
 print(json.dumps({'case':f'{lang}/{scene}','status':d['status'],'frames':len(frames),'pages':len(pages),'warnings':d['warnings'],'source_unchanged':sources==after}),flush=True)
