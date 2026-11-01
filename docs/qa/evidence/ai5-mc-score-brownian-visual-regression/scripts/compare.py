import hashlib,json
from pathlib import Path
from PIL import Image
O=Path(__file__).parent;B=Path('/workspace/runtime/ai5-mc-score-mcmc-brownian-endpoint-review');review=json.loads((B/'report.json').read_text());baseline_views=json.loads((B/'view-receipts.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(p):
 with Image.open(p) as im:
  im=im.convert('RGB');return {'size':list(im.size),'sha256':hashlib.sha256(im.tobytes()).hexdigest()}
rows=[];cases=[]
for p in sorted((O/'cases').iterdir()):
 d=json.loads((p/'result.json').read_text());f=json.loads((p/'freeze.json').read_text());match=next(c for c in review['cases'] if c['lang']==d['lang'] and c['scene']==d['scene']);old=B/'cases'/match['case'];before=json.loads((old/'result.json').read_text())
 assert d['duration']==before['duration'];assert d['narration']==before['narration'];assert d['inputs']==before['inputs'];assert len(d['frames'])==len(before['frames'])
 states=[]
 for a,b in zip(before['frames'],d['frames']):
  assert (a['file'],a['time'],a['reason'])==(b['file'],b['time'],b['reason'])
  oldpng=old/a['file'];newpng=p/b['file'];oldrgb=rgb(oldpng);newrgb=rgb(newpng)
  byte_equal=sha(oldpng)==sha(newpng);rgb_equal=oldrgb==newrgb
  assert not byte_equal or rgb_equal
  v=[v for v in baseline_views if v['case']==match['case'] and a['file'] in v['frame_files']]
  assert v
  row={'case':p.name,'lang':d['lang'],'scene':d['scene'],'file':b['file'],'time':b['time'],'reason':b['reason'],'baseline_case':match['case'],'before_path':str(oldpng),'after_path':str(newpng),'before_png_sha256':sha(oldpng),'after_png_sha256':sha(newpng),'before_rgb':oldrgb,'after_rgb':newrgb,'png_byte_equal':byte_equal,'rgb_equal':rgb_equal,'review_status':'inherited-exact-png' if byte_equal else ('inherited-exact-RGB' if rgb_equal else 'pending-native-view'),'baseline_actual_view_receipts':v}
  rows.append(row);states.append(row)
 cases.append({'case':p.name,'baseline_case':match['case'],'raw_status':d['status'],'raw_warnings':d['warnings'],'states':len(states),'exact_png':sum(x['png_byte_equal'] for x in states),'exact_rgb':sum(x['rgb_equal'] for x in states),'changed':sum(not x['rgb_equal'] for x in states),'duration_identical':True,'narration_captures_identical':True,'times_reasons_identical':True,'inputs_signatures_identical':True,'all_inputs_current_at_freeze':all(i['signature_current'] for i in f['inputs']),'current_fingerprint':d['fingerprint'],'baseline_fingerprint':before['fingerprint']})
result={'scope':'Exact file/RGB comparisons only. Inheritance is limited to actual before-view scale; changed states require actual native inspection. Source snapshots are observations, not loaded-import proof.','cases':cases,'rows':rows,'totals':{'states':len(rows),'png_equal':sum(r['png_byte_equal'] for r in rows),'rgb_equal':sum(r['rgb_equal'] for r in rows),'changed':sum(not r['rgb_equal'] for r in rows)}}
(O/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'cases':cases,'totals':result['totals']},indent=2))
