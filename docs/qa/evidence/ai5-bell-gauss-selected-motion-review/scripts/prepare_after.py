import sys,json,os,hashlib,importlib.util
from pathlib import Path
D=Path(sys.argv[1]);old=D.with_name(D.name.removesuffix('-after'));out=D/'changed-review';out.mkdir(exist_ok=True);(out/'frames').mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();oldmap=json.loads((old/'unique-review/map.json').read_text());assert len(oldmap['pages'])==len(oldmap['viewed_pages'])
lookup={r['sha256']:{'case':old.name,'file':'audit/'+r['file'],'original_viewed_representative_index':i} for i,r in enumerate(oldmap['representatives'])}
# Every-frame original windows were actually viewed separately.
p=old/'dense-reveals-before/map.json';dense=json.loads(p.read_text());assert len(dense['pages'])==len(dense['viewed_pages'])
for r in dense['frames']:
 h=sha(old/'dense-reveals-before'/r['file']);lookup.setdefault(h,{'case':old.name,'file':'dense-reveals-before/'+r['file'],'original_every_encoded_source_frame':r['source_frame']})
a=json.loads((D/'audit/result.json').read_text());seen={};reps=[];mapping=[]
for i,r in enumerate(a['selected_frames']):
 src=D/'audit'/r['file'];h=sha(src);m={'selected_index':i,'source_frame':r['source_frame'],'time':r['time'],'sha256':h}
 if h in lookup:m.update({'coverage':'exact-PNG-inherited','original':lookup[h]})
 else:
  if h not in seen:
   seen[h]=len(reps);reps.append(dict(r,sha256=h));dst=out/r['file'];os.link(src,dst)
  m.update({'coverage':'new-image-pending-view','representative_index':seen[h],'representative_file':reps[seen[h]]['file']})
 mapping.append(m)
spec=importlib.util.spec_from_file_location('qm','/workspace/explainer-videos/tools/qa_motion.py');qm=importlib.util.module_from_spec(spec);spec.loader.exec_module(qm)
pages=qm.sheets(out,reps);(out/'map.json').write_text(json.dumps({'audit':str(D/'audit/result.json'),'original_map_sha256':sha(old/'unique-review/map.json'),'original_every_encoded_map_sha256':sha(p),'selected_time_map':mapping,'representatives':reps,'pages':pages,'viewed_pages':[],'pixel_identity_rule':'Exact PNG SHA256 equality only against actually viewed original representatives or separately viewed every-encoded original window. No perceptual inheritance.'},indent=2)+'\n');print(D.name,len(mapping),sum(x['coverage']=='exact-PNG-inherited' for x in mapping),len(reps),len(pages))
