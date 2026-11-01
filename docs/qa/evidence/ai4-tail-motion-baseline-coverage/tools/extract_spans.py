from pathlib import Path
import sys,json,shutil
B=Path('/workspace/explainer-videos');sys.path.insert(0,str(B));from tools.qa_motion import probe,extract,sheets
D=Path(sys.argv[1]);windows=json.loads(sys.argv[2]);name=sys.argv[3];assert shutil.disk_usage(B).free>=512*1024**2
fr=json.loads((D/'freeze.json').read_text());movie=Path(fr['frozen_movie']);stream,times=probe(movie);selected=[]
for a,b in windows:
 for i in range(a,b+1):selected.append({'source_frame':i,'time':times[i],'reasons':['all-encoded-targeted-reveal']})
out=D/name;out.mkdir(exist_ok=False);extract(movie,out/'frames',selected);pages=sheets(out,selected)
(out/'result.json').write_text(json.dumps({'scope':'Every encoded frame in explicitly listed source-index windows; not a full-clip visual review. Actual sheet/native views recorded separately.','movie_sha256':fr['movie_sha256'],'windows':windows,'selected_frames':selected,'pages':pages,'source_width':stream['width'],'source_height':stream['height']},indent=2)+'\n');print(len(selected),'frames',len(pages),'pages',out)
