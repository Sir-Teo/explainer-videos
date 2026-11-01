from pathlib import Path
import json,hashlib,sys,datetime
B=Path(__file__).parent/'zh'/sys.argv[1];lo,hi=map(int,sys.argv[2:4]);note=sys.argv[4];p=B/'views.json';v=json.loads(p.read_text());plan=json.loads((B/'plan.json').read_text());done={x['page'] for x in v['pages']}
for i in range(lo,hi+1):
 r=plan['pages'][i-1];assert hashlib.sha256((B/'unique'/r['file']).read_bytes()).hexdigest()==r['sha256']
 if i in done:raise ValueError('already recorded page '+str(i))
 reps=plan['reps'][r['first_selected_frame']:r['first_selected_frame']+r['frames']];v['pages'].append({'page':i,'file':r['file'],'sha256':r['sha256'],'representative_indices':list(range(r['first_selected_frame'],r['first_selected_frame']+r['frames'])),'first_time':reps[0]['time'],'last_time':reps[-1]['time'],'scale':'640x360 per image','actual_observation':note,'viewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
p.write_text(json.dumps(v,indent=2)+'\n');print(sys.argv[1],len(v['pages']),'pages recorded')
