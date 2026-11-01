from pathlib import Path
import json,datetime,argparse,hashlib
P=argparse.ArgumentParser();P.add_argument('lang');P.add_argument('scene');P.add_argument('first',type=int);P.add_argument('last',type=int);P.add_argument('--section',default='unique');P.add_argument('--note',required=True);a=P.parse_args();D=Path('/workspace/runtime/ai4-tail-motion-review')/a.lang/a.scene;path=D/'actual-views.json';r=json.loads(path.read_text()) if path.exists() else {'scope':'Manual page views only, all tiles inspected at declared tile scale; exactPNG groups in review-plan map duplicate selected times. No perceptual/continuous/audio claim.','page_views':[],'native_views':[]}
for i in range(a.first,a.last+1):
 p=D/a.section/f'sheet-{i:03d}.png';assert p.exists();r['page_views'].append({'viewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'section':a.section,'page':i,'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tile_scale':'640px wide; all tiles directly inspected','notes':a.note})
path.write_text(json.dumps(r,indent=2)+'\n');print(a.lang,a.scene,'logged',a.section,a.first,a.last)
