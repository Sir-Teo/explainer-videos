from pathlib import Path
import json,importlib.util,shutil
O=Path('/workspace/runtime/ai5-bell-gauss-selected-motion-review');spec=importlib.util.spec_from_file_location('qm','/workspace/explainer-videos/tools/qa_motion.py');qm=importlib.util.module_from_spec(spec);spec.loader.exec_module(qm)
for case,ranges in [('en-Gauss',[(835,854),(927,959),(1038,1061),(1184,1211)]),('zh-Gauss',[(839,857),(939,972),(1036,1055),(1136,1167)])]:
 assert shutil.disk_usage('/workspace').free>=512*2**20
 D=O/case;sn=json.loads((D/'snapshot.json').read_text());movie=D/'movie.before-review.mp4';assert qm.sha256(movie)==sn['movie']['sha256'];_,times=qm.probe(movie)
 frames=[{'source_frame':i,'time':times[i],'reasons':[f'every-encoded-reveal-{j+1}']} for j,(lo,hi) in enumerate(ranges) for i in range(lo,hi+1)];F=D/'dense-reveals-before';qm.extract(movie,F/'frames',frames);pages=qm.sheets(F,frames);(F/'map.json').write_text(json.dumps({'movie_sha256':qm.sha256(movie),'ranges_inclusive':ranges,'frames':frames,'pages':pages,'viewed_pages':[],'scope':'Every encoded frame across four copy-reveal windows, including two-frame padding. Original artifacts, before authorized local repair.'},indent=2)+'\n');print(case,len(frames),len(pages),flush=True)
