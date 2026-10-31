"""Read-only comparison: current translation code, two shared caption tables."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='1'
import ast,collections,hashlib,json,subprocess,sys,time
from pathlib import Path
B=Path('/workspace/explainer-videos');sys.path.insert(0,str(B));start=time.monotonic()
from explainer import lang,zh_text
assert not any(name.startswith(('videos.ai.ai1','videos.ai.ai2','videos.ai.ai3')) for name in sys.modules),'production scene/compute import occurred'
sha=lambda b:hashlib.sha256(b).hexdigest()
commit=subprocess.run(['git','rev-parse','b352060'],cwd=B,check=True,capture_output=True,text=True).stdout.strip()
old_bytes=subprocess.run(['git','show',f'{commit}:videos/ai/ai_text_zh.json'],cwd=B,check=True,capture_output=True).stdout
current_path=B/'videos/ai/ai_text_zh.json';new_bytes=current_path.read_bytes();tables={'baseline':json.loads(old_bytes),'current':json.loads(new_bytes)}
out=Path('/workspace/runtime/ai12-shared-caption-regression');out.mkdir(exist_ok=True);(out/'baseline-ai_text_zh.json').write_bytes(old_bytes);(out/'current-ai_text_zh.json').write_bytes(new_bytes)
files=[];contexts=collections.defaultdict(list);occurrences=collections.Counter();case_counts={}
for part,expected in [('ai1',17),('ai2',16)]:
 candidates=[p for p in sorted((B/f'renders/qa/series/{part}/en').glob('*/text.jsonl')) if not p.parent.name.endswith('_motion')]
 assert len(candidates)==expected,(part,len(candidates));case_counts[part]=len(candidates)
 for path in candidates:
  raw=path.read_bytes();metadata=path.parent/'result.json';record=json.loads(metadata.read_text());rows=[json.loads(line) for line in raw.decode().splitlines() if line.strip()]
  files.append({'part':part,'scene':path.parent.name,'file':str(path),'sha256':sha(raw),'rows':len(rows),'record':str(metadata),'record_sha256':sha(metadata.read_bytes()),'record_fingerprint':record.get('fingerprint'),'record_warnings':record.get('warnings',[])})
  for n,r in enumerate(rows,1):
   s=r['s'];occurrences[s]+=1;contexts[s].append({'part':part,'scene':path.parent.name,'collection_line':n,'kind':r.get('kind'),'needs_translation':r.get('needs'),'context_classification':'prose-caption-needs-translation' if r.get('needs') else 'math-or-raw-symbol-caption-not-marked-as-needing-translation','file':str(path)})
# Add the current alpha-renaming caption from the actual AST if the endpoints predate it.
logic=B/'videos/ai/ai2/s09_logic.py';tree=ast.parse(logic.read_text());node=next(n.args[0] for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='label' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value.startswith('here the remaining variable is renamed'))
alpha=node.value;added=alpha not in contexts
if added:contexts[alpha].append({'part':'ai2','scene':'Logic','source':str(logic),'line':node.lineno,'kind':'label-source','needs_translation':True,'context_classification':'supplemental-current-static-caption-absent-from-collected-endpoints'});occurrences[alpha]+=1
outputs={};lang.LANG='zh'
for which,tab in tables.items():
 zh_text._TABLE=tab;zh_text._BY_NUMBERS=None;outputs[which]={s:zh_text.translate(s) for s in contexts}
differences=[]
for s,cs in contexts.items():
 if outputs['baseline'][s]!=outputs['current'][s]:differences.append({'english':s,'baseline_raw_translate_output':outputs['baseline'][s],'current_raw_translate_output':outputs['current'][s],'occurrences_in_collection_or_supplement':occurrences[s],'contexts':cs})
# All collected entries are passed through translate by their MathTex/Text wrappers;
# data_text/code verbatim Text is deliberately excluded by the collector. The
# needs flag is a heuristic, not evidence of data-versus-prose provenance.
proof_rows=[{'english':s,'baseline':outputs['baseline'][s],'current':outputs['current'][s],'occurrences':occurrences[s],'contexts':contexts[s]} for s in sorted(contexts)]
canonical=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
results_path=out/'used-caption-results.json';results_path.write_text(json.dumps(proof_rows,ensure_ascii=False,indent=2))
assert current_path.read_bytes()==new_bytes,'global table changed during comparison; rerun on a stable snapshot'
source_hashes={str(p.relative_to(B)):sha(p.read_bytes()) for p in [B/'explainer/zh_text.py',B/'explainer/lang.py',B/'explainer/zh_templates.py',logic]}
for part in ['ai1','ai2']:
 for p in sorted((B/f'videos/ai/{part}').glob('*.py')):source_hashes[str(p.relative_to(B))]=sha(p.read_bytes())
report={'baseline_commit':commit,'baseline_table_sha256':sha(old_bytes),'current_table_sha256':sha(new_bytes),'baseline_table_snapshot':str(out/'baseline-ai_text_zh.json'),'current_table_snapshot':str(out/'current-ai_text_zh.json'),'case_counts':case_counts,'collection_records':files,'collected_row_count':sum(f['rows'] for f in files),'unique_compared_strings_including_supplement':len(contexts),'comparison_occurrences_including_supplement':sum(occurrences.values()),'logic_alpha_rename_supplement':{'added':added,'english':alpha,'baseline_output':outputs['baseline'][alpha],'current_output':outputs['current'][alpha],'source':str(logic),'source_sha256':sha(logic.read_bytes()),'source_line':node.lineno},'changed_unique_strings':len(differences),'differences':differences,'baseline_output_map_sha256':sha(canonical(outputs['baseline'])),'current_output_map_sha256':sha(canonical(outputs['current'])),'used_caption_results':str(results_path),'used_caption_results_sha256':sha(results_path.read_bytes()),'source_sha256_at_comparison':source_hashes,'execution':{'pid':os.getpid(),'nice':os.getpriority(os.PRIO_PROCESS,0),'processes_used':1,'thread_env':{k:os.environ[k] for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']},'elapsed_s':time.monotonic()-start,'translator':'actual current explainer.zh_text.translate, lang zh, _TABLE and _BY_NUMBERS reset once per table pass','production_scene_or_compute_modules_imported':[]},'context_scope':['Raw translate() output is compared for every collected string, including needs=false math/raw-symbol candidates. Each difference retains its original record context.','The needs flag only says whether English prose was detected; it does not establish that a value is raw model data. Verbatim data_text/Code Text is skipped by this collector and is outside this used-caption sample.','No caption difference is dismissed as harmless raw data without source-context evidence.'],'limits':['This compares shared-table effects on these captured English strings using the current translation implementation for both passes.','This does not establish scene/data/narration equivalence, fresh production fingerprints, rendered geometry, continuous playback or audio.','Dynamic values or branches absent from the33endpoint text collections and the one static supplement are not exercised.','No production scene/data/model imports or loads; no table edit, compute or render. Source hashes are bytes at comparison time, not proof of code imported by historical render workers.']}
report_path=Path('/workspace/runtime/ai12-shared-caption-regression.json');report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2));lines=['# Shared Chinese caption regression: Parts 1 and 2','',f"Compared the shared caption table at `{commit}` with the current table using the actual current `explainer.zh_text.translate` in a single nice-{report['execution']['nice']} process. All17Part1 and16Part2 endpoint text collections were included.",'',f"Collected {report['collected_row_count']} rows; compared {len(contexts)} unique English strings including the Logic alpha-renaming supplement. Changed unique outputs: {len(differences)}.",'',f"Baseline output-map SHA256: `{report['baseline_output_map_sha256']}`.",f"Current output-map SHA256: `{report['current_output_map_sha256']}`.",'']
for diff in differences:lines += ['English: `'+diff['english']+'`','Baseline: `'+diff['baseline_raw_translate_output']+'`','Current: `'+diff['current_raw_translate_output']+'`','']
lines += ['The JSON report retains raw translator outputs, source/record/table hashes and every collected context. Full used-caption evidence is in `ai12-shared-caption-regression/used-caption-results.json`.','',*report['context_scope'],*report['limits']];text='\n'.join(lines).replace('All17Part1 and16Part2','All 17 Part 1 and 16 Part 2').replace('the33endpoint','the 33 endpoint');Path('/workspace/runtime/ai12-shared-caption-regression.md').write_text(text+'\n');print(json.dumps({'case_counts':case_counts,'rows':report['collected_row_count'],'unique':len(contexts),'supplement_added':added,'differences':len(differences),'nice':report['execution']['nice'],'elapsed_s':report['execution']['elapsed_s'],'output_hashes_equal':report['baseline_output_map_sha256']==report['current_output_map_sha256']},indent=2));print(json.dumps(differences,ensure_ascii=False,indent=2))
