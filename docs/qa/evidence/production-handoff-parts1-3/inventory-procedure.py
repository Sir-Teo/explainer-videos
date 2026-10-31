from pathlib import Path
import hashlib,json,datetime,stat,subprocess
B=Path('/workspace/explainer-videos');D=B/'docs/qa/evidence/production-handoff-parts1-3';D.mkdir(parents=True,exist_ok=False)
PIN='927fba668656a682b3e29a288de64130ddc680dd'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def row(p,role):
 st=p.stat();assert stat.S_ISREG(st.st_mode)
 return {'path':str(p.relative_to(B)),'bytes':st.st_size,'sha256':digest(p),'role':role}
files=[];excluded=[];totals=[];nonregular=[]
for part in ['ai1','ai2','ai3']:
 got=[]
 for p in sorted((B/'.cache'/part).rglob('*')):
  if p.is_dir():continue
  if p.is_symlink() or not p.is_file():nonregular.append(str(p.relative_to(B)));continue
  if p.name.endswith('.lock') or p.name=='.lock':excluded.append(row(p,'transient advisory lock; never transfer lock state'));continue
  role='cached numeric/completion/provenance JSON' if p.suffix=='.json' else 'compressed numeric array payload' if p.suffix=='.npz' else 'source/corpus text' if p.suffix=='.txt' else 'checkpoint/source/supporting cache file'
  if '_integrity' in p.parts:role='required Part3 integrity sidecar; preserve exact bytes, do not re-attest silently'
  r=row(p,role);got.append(r);files.append(r)
 totals.append({'part':part,'files':len(got),'bytes':sum(r['bytes'] for r in got)})
assert not nonregular,nonregular
core={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewed_source_commit':PIN,'cloud_repo_root':str(B),'scope':'Every regular non-lock file currently under.cache/ai1,.cache/ai2,.cache/ai3. This preserves complete observed source/data/sidecar/checkpoint sets; no deletion/minimization by guessing which result may be used. No data archives, transfers, loads, producer calls or model loads.','parts':totals,'total_files':len(files),'total_bytes':sum(r['bytes'] for r in files),'files':files,'excluded_transient_locks':excluded,'excluded_nonregular':nonregular,'not_sufficient_alone':'Unchanged Part3 current() additionally checks external dependency files and exact package versions; see external-validation-dependencies.json.'}
(D/'cache-inventory.json').write_text(json.dumps(core,indent=2)+'\n')
(D/'transfer-core-files.txt').write_text(''.join(r['path']+'\n' for r in files))
(D/'transfer-core.sha256').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in files))
# Strict validator inputs outside the three cache directories; no model loading.
extra=[]
for name in ['train.npy','valid.npy','tokenizer.json']:extra.append(row(B/'.cache/novels'/name,'required by unchanged galorectl sidecar dependency check; source tokens/tokenizer, not trained-model checkpoint'))
hf=Path('/workspace/runtime/huggingface/hub');repo=hf/'models--openai-community--gpt2';ref=repo/'refs/main';rev=ref.read_text().strip();assert rev=='607a30d783dfa663caf39e06633721c8d4cfcd7e'
hfiles=[]
for name in ['config.json','model.safetensors']:
 p=repo/'snapshots'/rev/name;hfiles.append({'source_snapshot_path':str(p),'resolved_regular_blob':str(p.resolve()),'snapshot_relative_path':f'models--openai-community--gpt2/snapshots/{rev}/{name}','bytes':p.stat().st_size,'sha256':digest(p),'role':'required only by unchanged Part3 Power dependency validation; no inference needed for completed cached-results rendering'})
sidecars={name:json.loads((B/f'.cache/ai3/_integrity/{name}.json').read_text()) for name in ['power','galorectl','letters']}
external={'scope':'External strict-validator inputs observed from existing sidecars/source; copying the58.9MB core alone does not satisfy these checks. No download/load/re-attestation occurred.','extra_repo_relative_files':extra,'extra_repo_relative_bytes':sum(r['bytes'] for r in extra),'required_observed_packages':{'numpy':'2.5.4','torch':'2.15.0+cpu','transformers':'5.22.1'},'reviewed_lockfile_packages':{'numpy':'2.5.4','torch':'2.14.1','transformers':'5.20.1'},'stop_rule':'Install matching observed versions only where genuinely supported and verify before normal load. Different wheel tags/versions or missing/mismatched dependency files are a stop, never permission to weaken current(), regenerate numerical data or rewrite sidecars. A portable frozen-payload reader is a separate pipeline change requiring parent review.','gpt2':{'repo_id':'openai-community/gpt2','revision':rev,'ref_main_bytes':ref.stat().st_size,'ref_main_sha256':digest(ref),'files':hfiles,'total_required_bytes':sum(r['bytes'] for r in hfiles),'normal_download_alternative':'Use a fresh dedicated HF_HUB_CACHE and exact public revision; only config.json/model.safetensors. Existing _gpt2_files uses refs/main first, else requires exactly one snapshot, so another cached revision/ref is not equivalent.'},'sidecar_dependency_observations':{k:{'recipe':v['recipe'],'dependencies_observed_now':v['dependencies_observed_now'],'scope':v['dependency_scope']} for k,v in sidecars.items()},'source_inputs':[{'path':name,'bytes':len(subprocess.check_output(['git','show',PIN+':'+name],cwd=B)),'sha256':hashlib.sha256(subprocess.check_output(['git','show',PIN+':'+name],cwd=B)).hexdigest()} for name in ['videos/ai/ai1/compute.py','explainer/ai/novels.py','explainer/lm/pocket.py']]}
(D/'external-validation-dependencies.json').write_text(json.dumps(external,indent=2)+'\n');(D/'transfer-strict-extra-files.txt').write_text(''.join(r['path']+'\n' for r in extra));(D/'transfer-strict-extra.sha256').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in extra))
# Immutable reviewed source identities and manifest order; no source imports.
source_names=subprocess.check_output(['git','ls-tree','-r','--name-only',PIN,'--','videos/ai/ai1','videos/ai/ai2','videos/ai/ai3'],cwd=B,text=True).splitlines()
source_names += ['README.md','videos/ai/LECTURE_GUIDE.md','videos/ai/AI_ZH_GUIDE.md','videos/ai/ai_text_zh.json','tools/build.py','tools/make.py','tools/narrate.py','tools/tts_server.py','tools/voices.json','tools/zh_lines.py','tools/translate_narration.py','explainer/tts.py','explainer/voiceover.py','explainer/ai/cache.py','explainer/cache_lock.py','requirements-lock.txt','pyproject.toml','manim.cfg','tools/voice_refs/kokoro_en.wav','tools/voice_refs/serenaflat_zh.wav']
source=[]
for name in sorted(set(source_names)):
 data=subprocess.check_output(['git','show',PIN+':'+name],cwd=B);source.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'worktree_bytes_match_pin':(B/name).is_file() and (B/name).read_bytes()==data})
import ast
manifests=[]
for part in ['ai1','ai2','ai3']:
 data=subprocess.check_output(['git','show',PIN+f':videos/ai/{part}/manifest.py'],cwd=B);t=ast.parse(data);scenes=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='SCENES' for v in n.targets));manifests.append({'part':part,'scene_count':len(scenes),'bilingual_cases':2*len(scenes),'scenes':[{'position':i,'module':m,'scene':c,'title_en':title} for i,(m,c,title) in enumerate(scenes,1)]})
(D/'reviewed-source-inventory.json').write_text(json.dumps({'commit':PIN,'scope':'Exact git-show bytes at immutable review checkpoint. Worktree equality is an observation only; production uses the pin. Later Part4 global/source changes are intentionally excluded.38Part3 cases mean19scenes×2languages, not38source modules.','files':source,'manifests':manifests},indent=2)+'\n')
audio=Path('/workspace/runtime/production-handoff-parts1-3/real-information-audio.json');(D/'real-information-audio.json').write_bytes(audio.read_bytes());au=json.loads(audio.read_text());af=[f for b in au['blocks'] for f in b['files']];(D/'transfer-optional-real-audio-files.txt').write_text(''.join(r['path']+'\n' for r in af));(D/'transfer-optional-real-audio.sha256').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in af))
print(json.dumps({'dir':str(D),'core_parts':totals,'core_files':len(files),'core_bytes':core['total_bytes'],'excluded_locks':len(excluded),'extra_novel_files_bytes':external['extra_repo_relative_bytes'],'strict_gpt2_files_bytes':external['gpt2']['total_required_bytes'],'optional_real_audio_bytes':au['total_transfer_bytes'],'source_files':len(source),'manifests':[(x['part'],x['scene_count'],x['bilingual_cases']) for x in manifests]},indent=2))
