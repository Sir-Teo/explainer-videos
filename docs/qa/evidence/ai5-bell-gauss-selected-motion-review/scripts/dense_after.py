from pathlib import Path
import json,importlib.util,sys
B=Path('/workspace/runtime/ai5-bell-gauss-selected-motion-review');spec=importlib.util.spec_from_file_location('qm','/workspace/explainer-videos/tools/qa_motion.py');qm=importlib.util.module_from_spec(spec);spec.loader.exec_module(qm)
for lang in ('en','zh'):
 scene=sys.argv[1];old=B/f'{lang}-{scene}';D=B/f'{lang}-{scene}-after';prior=json.loads((old/'dense-reveals-before/map.json').read_text());movie=D/'movie.mp4';s,times=qm.probe(movie);_,ot=qm.probe(old/'movie.before-review.mp4');assert times==ot
 frames=[{'source_frame':r['source_frame'],'time':times[r['source_frame']],'reasons':r['reasons']} for r in prior['frames']];F=D/'dense-reveals-after';qm.extract(movie,F/'frames',frames);pages=qm.sheets(F,frames);(F/'map.json').write_text(json.dumps({'movie_sha256':qm.sha256(movie),'all_movie_encoded_timestamps_identical_before':True,'ranges_inclusive':prior['ranges_inclusive'],'frames':frames,'pages':pages,'viewed_pages':[],'scope':'Every encoded frame across changed reveal windows, same exact source-frame identities/times as original.'},indent=2)+'\n');print(D.name,len(frames),len(pages),flush=True)
