from pathlib import Path
import sys,json,hashlib,shutil,gzip
from PIL import Image,ImageDraw
R=Path('/workspace/runtime/ai6-newton-after-review');B=Path('/workspace/runtime/ai6-newton-motion-review');case=Path(sys.argv[1]);lang=sys.argv[2];baseline=json.loads((B/f'endpoints-{lang}/review.json').read_text());prior={x['sha256']:x for x in baseline['frames']};receipt=json.loads((case/'receipt.json').read_text());assert receipt['runtime_completed'] and receipt['aborted'] is None;D=case/'completed';record=json.loads((D/'result.json').read_text());O=R/f'after-{lang}-endpoints';O.mkdir(exist_ok=True);assert not (O/'plan.json').exists(),'Reconcile existing endpointplan first';rows=[];todo=[]
for i,f in enumerate(record['frames']):
 p=D/f['file'];h=hashlib.sha256(p.read_bytes()).hexdigest();row={'index':i,'file':str(p),'sha256':h,'time':f['time'],'coverage':'exact-prior-actually-reviewed-native-PNG' if h in prior else 'pending-actual-native-image-view'}
 if h in prior:row['prior']=prior[h]
 else:todo.append(row)
 rows.append(row)
pages=[]
for start in range(0,len(todo),8):
 chunk=todo[start:start+8];im=Image.new('RGB',(1708,520*((len(chunk)+1)//2)),'#202732');draw=ImageDraw.Draw(im)
 for j,row in enumerate(chunk):
  x=j%2*854;y=j//2*520;draw.text((x+8,y+8),f"{lang} Newton freshendpoint{row['index']:03d} {row['time']}",fill='white')
  with Image.open(row['file']) as p:assert p.size==(854,480);im.paste(p,(x,y+40))
 p=O/f'changed-{len(pages)+1:03d}.png';im.save(p);pages.append({'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indices':[r['index'] for r in chunk],'actually_viewed':False})
plan={'raw_record':str(D/'result.json'),'raw_record_sha256':hashlib.sha256((D/'result.json').read_bytes()).hexdigest(),'raw_status':record['status'],'raw_warnings':record['warnings'],'owner_receipt':str(case/'receipt.json'),'owner_receipt_sha256':hashlib.sha256((case/'receipt.json').read_bytes()).hexdigest(),'source_changed':receipt['source_changed'],'data_changed':receipt['data_changed'],'baseline':str(B/f'endpoints-{lang}/review.json'),'baseline_sha256':hashlib.sha256((B/f'endpoints-{lang}/review.json').read_bytes()).hexdigest(),'scope':'Endpoint-only actual native review pending changedimages; exact PNG inheritance only','frames':rows,'pages':pages};(O/'plan.json').write_text(json.dumps(plan,indent=2));print(json.dumps({'lang':lang,'images':len(rows),'exactprior':len(rows)-len(todo),'new':len(todo),'pages':len(pages)}))
