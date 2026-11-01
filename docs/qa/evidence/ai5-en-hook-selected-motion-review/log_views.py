from pathlib import Path
import json,hashlib,datetime,sys
D=Path(__file__).parent/'en/Hook';sec=sys.argv[1];first,last=map(int,sys.argv[2:4]);note=sys.argv[4];v=json.loads((D/'views.json').read_text());plan=json.loads((D/'unique/review-plan.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
if sec=='pages':
 for n in range(first,last+1):
  p=plan['pages'][n-1];path=D/'unique'/p['file'];assert sha(path)==p['sha256'];v['pages'].append({'page':n,'path':str(path),'sha256':p['sha256'],'viewed_utc':now,'scale':'contact-sheet640px tile, original sheet detail','note':note,'representatives':list(range(p['first_selected_frame'],p['first_selected_frame']+p['frames']))})
elif sec=='native':
 ar=json.loads((D/'audit/result.json').read_text())
 for n in range(first,last+1):
  f=ar['selected_frames'][n];path=D/'audit'/f['file'];assert sha(path)==f['sha256'];v['native'].append({'selected_index':n,'source_frame':f['source_frame'],'time':f['time'],'path':str(path),'sha256':f['sha256'],'viewed_utc':now,'scale':'original native854x480','note':note})
else:raise ValueError(sec)
(D/'views.json').write_text(json.dumps(v,indent=2)+'\n');print(sec,first,last,'actual views logged')
