from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'/workspace/explainer-videos');from tools.qa_motion import probe,extract
P=Path(__file__).parent/'en';old=Path('/workspace/runtime/ai5-ito-sde-fokker-motion-review/en-FokkerPlanck/842896444f939e53af0608f2e0c212527abd73a090b707cad2303b589783cc3b/FokkerPlanck.mp4');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(old)=='842896444f939e53af0608f2e0c212527abd73a090b707cad2303b589783cc3b';_,ts=probe(old);selected=[{'source_frame':i,'time':ts[i],'reasons':['Extra changed histogram morph, boundary-neighbor pair review']} for i in range(898,924)];extract(old,P/'hist-before',selected);oldfiles={int(p.name.split('_')[0]):p for p in (P/'hist-before').glob('*.png')};new={x['source_frame']:x for x in json.loads((P/'plan.json').read_text())['all_time_mapping']};rows=[];pages=[]
for i in range(898,924):
 a=oldfiles[i];b=Path(new[i]['file']);x=np.asarray(Image.open(a).convert('RGB'),dtype=np.int16);y=np.asarray(Image.open(b).convert('RGB'),dtype=np.int16);diff=abs(x-y);rows.append({'source_frame':i,'time':ts[i],'before':str(a),'before_sha256':sha(a),'after':str(b),'after_sha256':sha(b),'max_channel_difference':int(diff.max()),'different_pixels':int(np.any(diff,axis=-1).sum()),'mean_channel_difference':float(diff.mean())})
for start in range(0,len(rows),4):
 rr=rows[start:start+4];im=Image.new('RGB',(1708,510*len(rr)),'#222832');d=ImageDraw.Draw(im)
 for j,r in enumerate(rr):
  for k,key in enumerate(['before','after']):d.text((k*854+8,j*510+5),f"{key} FokkerPlanck EN frame{r['source_frame']} time{r['time']:.6f}",fill='white');im.paste(Image.open(r[key]),(k*854,j*510+30))
 q=P/'hist-pair-pages'/f'page-{start//4+1:03d}.png';q.parent.mkdir(exist_ok=True);im.save(q);pages.append({'path':str(q),'sha256':sha(q),'frames':[r['source_frame'] for r in rr],'actually_viewed':False})
(P/'hist-comparison-plan.json').write_text(json.dumps({'before_movie_sha256':sha(old),'after_movie_sha256':sha(P/'FokkerPlanck.mp4'),'rows':rows,'pages':pages,'limits':'Decoded pixel statistics are automatic; paired page actual views recorded separately.'},indent=2)+'\n');print(len(rows),'pairs',len(pages),'pages; maxdelta',max(r['max_channel_difference'] for r in rows),'maxpixels',max(r['different_pixels'] for r in rows))
