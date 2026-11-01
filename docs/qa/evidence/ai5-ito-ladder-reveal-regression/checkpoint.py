from pathlib import Path
import datetime,hashlib,json,sys
O=Path(__file__).parent;p=O/sys.argv[1];plan=json.loads((p/'plan.json').read_text());out=p/'view-progress.json';d=json.loads(out.read_text()) if out.exists() else {'actually_viewed_pages':{},'native_followups':[],'limits':'Selected native image review, not continuous perceptual playback/listening.'}
for i in map(int,sys.argv[2].split(',')):
 pg=plan['pages'][i-1];assert hashlib.sha256(Path(pg['path']).read_bytes()).hexdigest()==pg['sha256'];d['actually_viewed_pages'][str(i)]={**pg,'actually_viewed':True,'view_detail':'original;854x480 source tiles, host may scale sheet presentation','observations':sys.argv[3],'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
out.write_text(json.dumps(d,indent=2)+'\n');print(sys.argv[1],len(d['actually_viewed_pages']),'/',len(plan['pages']))
