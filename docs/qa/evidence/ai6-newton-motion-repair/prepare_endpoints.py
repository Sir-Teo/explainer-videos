from pathlib import Path
import json,hashlib,shutil,gzip
from PIL import Image,ImageDraw
R=Path('/workspace/runtime/ai6-newton-motion-review');W=Path('/workspace/runtime/ai6-remaining-qa-serial/runs/20261101T055536/07-Newton')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for l in ['en','zh']:
 C=W/l/'endpoints';D=C/'completed';d=json.loads((D/'result.json').read_text());O=R/f'endpoints-{l}';O.mkdir(exist_ok=True);assert not (O/'plan.json').exists();rows=[]
 for i,f in enumerate(d['frames']):
  p=D/f['file'];rows.append({'index':i,'file':str(p),'sha256':sha(p),'time':f['time'],'texts':f['texts'],'coverage':'pending actualnativeview'})
 pages=[]
 for start in range(0,len(rows),8):
  chunk=rows[start:start+8];im=Image.new('RGB',(1708,520*((len(chunk)+1)//2)),'#202732');draw=ImageDraw.Draw(im)
  for j,row in enumerate(chunk):
   x=j%2*854;y=j//2*520;draw.text((x+8,y+8),f"{l} Newton endpoint{row['index']:03d} {row['time']:.6f}s",fill='white')
   with Image.open(row['file']) as frame:assert frame.size==(854,480);im.paste(frame,(x,y+40))
  p=O/f'page-{len(pages)+1:03d}.png';im.save(p);pages.append({'file':str(p),'sha256':sha(p),'indices':[x['index'] for x in chunk],'actually_viewed':False})
 for n in ['receipt.json','source-before.json','source-after.json','data-before.json','data-after.json','command.json']:(O/(n+'.gz')).write_bytes(gzip.compress((C/n).read_bytes(),mtime=0))
 shutil.copy2(D/'result.json',O/'render-record.json');shutil.copy2(D/'copy-manifest.json',O/'owner-copy-manifest.json');shutil.copy2(D/'text.jsonl',O/'text.jsonl')
 plan={'scene':'Newton','lang':l,'owner':str(C),'raw_record':str(O/'render-record.json'),'raw_record_sha256':sha(O/'render-record.json'),'raw_status':d['status'],'raw_warnings':d['warnings'],'frames':rows,'pages':pages,'scope':'Endpoint-only native854x480 original images on unscaled1708wide chronological sheets; no playback/audio claim'};(O/'plan.json').write_text(json.dumps(plan,indent=2));print(l,len(rows),'endpointimages',len(pages),'pages')
