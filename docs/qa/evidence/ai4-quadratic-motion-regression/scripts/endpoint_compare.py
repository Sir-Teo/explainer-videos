from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image
R=Path(__file__).parent;B=Path('/workspace/explainer-videos');OLD=Path('/workspace/runtime/ai4-tail-endpoint-review');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();result=[]
for lang in ['en','zh']:
 old=OLD/lang/'Quadratic';new=B/f'renders/qa/series/ai4/{lang}/Quadratic';out=R/lang/'Quadratic'/'endpoints';out.mkdir()
 nr=json.loads((new/'result.json').read_text());br=json.loads((old/'result.json').read_text());rows=[]
 for n,fr in enumerate(nr['frames']):
  npth=new/fr['file'];q=out/npth.name;shutil.copyfile(npth,q);bp=old/br['frames'][n]['file'];aa=np.asarray(Image.open(bp).convert('RGB'));bb=np.asarray(Image.open(q).convert('RGB'));assert aa.shape==bb.shape;delta=np.abs(aa.astype(int)-bb.astype(int));mask=np.any(delta!=0,axis=2);ys,xs=np.nonzero(mask)
  rows.append(dict(index=n,old_file=str(bp),old_sha256=sha(bp),new_file=str(q),new_sha256=sha(q),old_time=br['frames'][n]['time'],new_time=fr['time'],exact_pixels_equal=bool(np.array_equal(aa,bb)),different_pixels=int(mask.sum()),max_channel_delta=int(delta.max()),bbox=None if not len(xs) else [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
 for name in ['result.json','sheet.png','render.log','text.jsonl']:
  if (new/name).exists():shutil.copyfile(new/name,out/name)
 result.append(dict(lang=lang,fresh_status=nr['status'],fresh_warnings=nr['warnings'],fresh_result_sha256=sha(out/'result.json'),baseline_scope='Historical endpoint capture simulation timings differ slightly; capture order/content compared directly without treating these times as identical to fullmotion.',rows=rows))
(R/'endpoint-comparison.json').write_text(json.dumps(result,indent=2)+'\n');print([(x['lang'],[(y['index'],y['different_pixels'],y['bbox']) for y in x['rows'] if not y['exact_pixels_equal']]) for x in result])
