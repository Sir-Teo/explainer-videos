from pathlib import Path
import json,importlib.util,hashlib,os,datetime
B=Path('/workspace/runtime/ai5-bell-gauss-selected-motion-review');spec=importlib.util.spec_from_file_location('qm','/workspace/explainer-videos/tools/qa_motion.py');q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q);sha=q.sha256
for lang,ranges in [('en',[(835,868),(927,959),(1038,1073),(1184,1227)]),('zh',[(839,872),(939,972),(1036,1068),(1136,1179)])]:
 D=B/f'{lang}-Gauss-after';old=B/f'{lang}-Gauss';p=D/'changed-review/map.json';m=json.loads(p.read_text());m['viewed_pages']=[{'page':x['file'],'sha256':x['sha256'],'representative_indices':list(range(x['first_selected_frame'],x['first_selected_frame']+x['frames'])),'scale':'640x360 per image','observations':'All new selected images viewed. New target row Write keeps prior rows legible, intentional fourth-step old-row scroll preserved. No new defect.','viewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()} for x in m['pages']]
 for r in m['selected_time_map']:
  if r['coverage']=='new-image-pending-view':r['coverage']='directly-viewed-new-representative'
 p.write_text(json.dumps(m,indent=2)+'\n')
 lookup={}
 for base,sub,key in [(old,'unique-review','representatives'),(old,'dense-reveals-before','frames'),(D,'changed-review','representatives')]:
  mm=json.loads((base/sub/'map.json').read_text());assert len(mm['viewed_pages'])==len(mm['pages'])
  for r in mm[key]:
   src=base/('audit' if sub=='unique-review' else sub)/r['file'];lookup.setdefault(sha(src),{'case':base.name,'file':str(src.relative_to(base)),'source_frame':r['source_frame']})
 _,ts=q.probe(D/'movie.mp4');F=D/'dense-complete-reveals-after';frames=[{'source_frame':i,'time':ts[i],'reasons':[f'every-encoded-complete-reveal-{j+1}']} for j,(lo,hi) in enumerate(ranges) for i in range(lo,hi+1)];q.extract(D/'movie.mp4',F/'frames',frames);C=F/'new-images';C.mkdir(exist_ok=True);(C/'frames').mkdir(exist_ok=True);seen={};reps=[];mapping=[]
 for i,r in enumerate(frames):
  src=F/r['file'];h=sha(src);row=dict(r,sha256=h)
  if h in lookup:row.update(coverage='exact-PNG-inherited',original=lookup[h])
  else:
   if h not in seen:seen[h]=len(reps);reps.append(dict(r,sha256=h));os.link(src,C/r['file'])
   row.update(coverage='new-image-pending-view',representative_index=seen[h])
  mapping.append(row)
 pages=q.sheets(C,reps);(C/'map.json').write_text(json.dumps({'movie_sha256':sha(D/'movie.mp4'),'ranges_inclusive':ranges,'all_encoded_time_map':mapping,'representatives':reps,'pages':pages,'viewed_pages':[],'scope':'Full source-frame spans for four target-row reveals, including adjacent annotation/underline states and two-frame padding. Exact PNG inheritance only from actually viewed original or repaired selected representatives.'},indent=2)+'\n');print(lang,len(frames),sum(r['coverage']=='exact-PNG-inherited' for r in mapping),len(reps),len(pages),flush=True)
