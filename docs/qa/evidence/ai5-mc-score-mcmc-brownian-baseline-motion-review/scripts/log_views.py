from pathlib import Path
import sys,json,hashlib,datetime
O=Path(__file__).parent;language,scene,start,end,*notes=sys.argv[1:];C=O/language/scene;plan=json.loads((C/'unique/review-plan.json').read_text());views=json.loads((C/'views.json').read_text());known={x['number'] for x in views['pages']}
for n in range(int(start),int(end)+1):
 if n in known:raise ValueError(f'Page{n} alreadylogged; do not silentlyduplicateactualviews')
 p=plan['pages'][n-1];file=C/'unique'/p['file'];assert hashlib.sha256(file.read_bytes()).hexdigest()==p['sha256'];chunk=plan['representatives'][p['first_selected_frame']:p['first_selected_frame']+p['frames']]
 views['pages'].append({'number':n,'file':p['file'],'sha256':p['sha256'],'viewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'view_scale':'640x360RGB image tiles in original1280px-wide2x4contactsheet','representative_indices':list(range(p['first_selected_frame'],p['first_selected_frame']+p['frames'])),'source_frames':[x['source_frame'] for x in chunk],'source_times':[x['time'] for x in chunk],'observation':' '.join(notes),'actual_view':True})
views['pages'].sort(key=lambda p:p['number']);(C/'views.json').write_text(json.dumps(views,indent=2)+'\n');print(language,scene,'loggedpages',len(views['pages']),'of',len(plan['pages']))
