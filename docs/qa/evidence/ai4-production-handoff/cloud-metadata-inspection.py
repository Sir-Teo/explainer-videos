"""Metadata-only Part4 handoff; all cache producers fail on call."""
from pathlib import Path
import datetime,gzip,hashlib,importlib.metadata,json,platform,subprocess,sys
from unittest.mock import Mock,patch
ROOT=Path('/workspace/explainer-videos'); OUT=Path('/workspace/runtime/ai4-production-handoff-metadata'); PIN='1927e6b7a99192344bd4c00ca7aae3abdd499369'
sys.path.insert(0,str(ROOT))
from videos.ai.ai4 import compute

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def sig(p):
 p=Path(p)
 if not p.exists():return None
 st=p.stat();return dict(bytes=st.st_size,sha256=sha(p),mtime_ns=st.st_mtime_ns)
def git_bytes(rel):return subprocess.run(['git','show',PIN+':'+rel],cwd=ROOT,check=True,capture_output=True).stdout

tree=subprocess.run(['git','ls-tree','-r','--name-only',PIN,'videos/ai/ai4'],cwd=ROOT,check=True,capture_output=True,text=True).stdout.splitlines()
extra=['explainer/ai/autodiff.py','explainer/ai/viz.py','explainer/ai/cache.py','explainer/cache_lock.py','videos/ai/ai1/compute.py','videos/ai/ai_text_zh.json','pyproject.toml','requirements-lock.txt','tools/qa_series.py','tools/build.py','tools/qa_audio.py','tools/qa_motion.py','manim.cfg']
source=[]
for rel in tree+extra:
 raw=git_bytes(rel);p=ROOT/rel;source.append(dict(path=rel,pinned_bytes=len(raw),pinned_sha256=hashlib.sha256(raw).hexdigest(),working_tree=sig(p),working_matches_pin=p.exists() and p.read_bytes()==raw))
assert all(x['working_matches_pin'] for x in source if x['path'].startswith('videos/ai/ai4/'))
for rel in ['explainer/ai/autodiff.py','explainer/ai/viz.py','explainer/ai/cache.py','explainer/cache_lock.py','videos/ai/ai1/compute.py']:
 assert next(x for x in source if x['path']==rel)['working_matches_pin'],rel
names=list(compute.ITEMS);assert len(names)==23
paths=[p for n in names for p in [compute.CACHE.path(n),compute.CACHE.path(n).with_suffix('.npz')]]
before={str(p.relative_to(ROOT)):sig(p) for p in paths};parents={str(p.relative_to(ROOT)):sig(p) for p in [ROOT/'.cache/ai1/train.txt',ROOT/'.cache/ai1/valid.txt']}
fail=Mock(side_effect=AssertionError('Handoff forbids producer execution'));cases=[]
with patch.object(compute.CACHE,'_produce',fail),patch.object(compute.CACHE,'items',{name:fail for name in names}):
 for name in names:
  good=compute.cache_current(name);assert good is True,name
  loaded=compute.CACHE.load(name)
  raw=json.loads(compute.CACHE.path(name).read_text())
  cases.append(dict(item=name,current_at_inspection=good,actual_guarded_load=True,completion_metadata=raw['_cache'],payloads={str(p.relative_to(ROOT)):before[str(p.relative_to(ROOT))] for p in [compute.CACHE.path(name),compute.CACHE.path(name).with_suffix('.npz')]},top_level_keys=list(loaded),array_shapes={k:list(v.shape) for k,v in loaded.items() if hasattr(v,'shape')}))
 fail.assert_not_called()
after={str(p.relative_to(ROOT)):sig(p) for p in paths};assert before==after
assert parents=={p:sig(ROOT/p) for p in parents}
assert sum(v is not None for v in before.values())==42
map_path=ROOT/'docs/qa/ai4-final-preview-map.json';map_sha=sha(map_path);assert map_sha=='33071a124497a163341b0ddff5cbf3e6423a43fb1c2a412c8a48374346963656'
preview=json.loads(map_path.read_text())
assembly_path=ROOT/'docs/qa/evidence/ai4-history-qualified-assembly/receipts/summary.json.gz';assembly=json.loads(gzip.decompress(assembly_path.read_bytes()))
for case in assembly['cases']:
 path=Path(case['movie']);identity=sig(path);assert identity is not None and identity['bytes']==case['movie_bytes'] and identity['sha256']==case['movie_sha256']
 case['movie_identity_verified_at_handoff']=identity
old_table=git_bytes('videos/ai/ai_text_zh.json');archived=ROOT/'docs/qa/evidence/ai5-source-review/prior-global-caption-table.json.gz';assert old_table==gzip.decompress(archived.read_bytes())
proof_paths=['docs/qa/evidence/ai5-source-review/prior-part-caption-comparison.json.gz','docs/qa/evidence/ai5-source-review/prior-part-observed-caption-keys.json.gz','docs/qa/evidence/ai5-visual-source-checks/hook-caption-merge.json.gz','docs/qa/evidence/ai5-visual-source-checks/caption-merge.json.gz']
proofs=[]
for rel in proof_paths:
 p=ROOT/rel;raw=gzip.decompress(p.read_bytes());proofs.append(dict(path=rel,compressed_sha256=sha(p),uncompressed_sha256=hashlib.sha256(raw).hexdigest()))
comparison=json.loads(gzip.decompress((ROOT/proof_paths[0]).read_bytes()));assert comparison['unique_keys']==4142 and not comparison['differences']
versions={p:importlib.metadata.version(p) for p in ['numpy','scipy','torch','manim','manimpango','Pillow','transformers','tokenizers']}
item_libraries={json.dumps(x['completion_metadata']['recipe']['libraries'],sort_keys=True) for x in cases};assert len(item_libraries)==1
params=json.loads((ROOT/'.cache/ai4/params.json').read_text());params.pop('_cache')
record=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Immutable metadata handoff only; no archive packaging/upload or production render. Compute/cache definitions and cached data were loaded with producers fail-on-call; no model was loaded. Scientific and preview acceptance scopes remain separate.',recommended_source_commit=PIN,source_inventory=source,items=cases,item_count=len(cases),present_payload_count=42,optional_npz_absence_items=[x['item'] for x in cases if any(v is None for k,v in x['payloads'].items() if k.endswith('.npz'))],total_payload_bytes=sum(v['bytes'] for v in before.values() if v is not None),producer_calls=0,payload_signatures_unchanged=True,needed_part1_corpus=parents,upstream_part1_historical_lineage_limit='These raw current bytes are exact dependencies consumed/recorded by freshPart4producer; this handoff does not reconstruct oldPart1artifact generation.',runtime=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),installed_distribution_versions=versions,cached_recipe_libraries=json.loads(next(iter(item_libraries))),lockfile_torch='2.14.1',lockfile_transformers='5.20.1',discrepancy='Reviewed cache recipes require torch2.15.0+cpu; exact2.14.1lock installation or GPU/cu-suffixed runtime makes currentness false. Do not fake version metadata, weaken guard, or retag caches. Reconcile renderer environment before any scene load.'),params_provenance=params,preview_map=dict(path=str(map_path.relative_to(ROOT)),sha256=map_sha,counts=preview['counts'],native_scope=preview['native_scope'],numeric_integrity_reference=preview['numeric_integrity_reference']),assembly=dict(path=str(assembly_path.relative_to(ROOT)),compressed_sha256=sha(assembly_path),uncompressed_sha256=hashlib.sha256(gzip.decompress(assembly_path.read_bytes())).hexdigest(),historical_source_commit=assembly['published_source_commit'],status=assembly['status'],cases=assembly['cases'],technical_verdict=assembly['technical_verdict'],join_verdict=assembly['join_verdict'],known_warnings_preserved=assembly['known_warnings_preserved'],remaining_gaps=assembly['remaining_gaps']),shared_global_table=dict(pin_sha256=hashlib.sha256(old_table).hexdigest(),current_working_sha256=sha(ROOT/'videos/ai/ai_text_zh.json'),working_matches_pin=False,prior4142_caption_lookup_differences=0,lookup_scope='142capturedPart1–4textcollections/4142observedkeys only; archived oldglobal equals1927pin. LaterPart5caption changes have scoped matching-rule supplements, not blanket currentHEAD approval.',prior_table_archive=dict(path=str(archived.relative_to(ROOT)),compressed_sha256=sha(archived),uncompressed_sha256=hashlib.sha256(gzip.decompress(archived.read_bytes())).hexdigest()),existing_scoped_proofs=proofs),limits=['Recommended commit binds reviewed Part4 source/global helpers. Whole currentHEAD has laterPart5 table additions and is not blanket certified.','Current schema/recipe/integrity checks and guarded loads are not new numerical scientific validation.','Selected preview image/joins and native1080 endpoints do not approve continuous perception, real narration, listening/synchronization, final4K/player delivery or any future output.','Production renderer must require current before every loader/upgrade and patch every producer fail-on-call before scene imports. Use strict environment and frozen payload identities, not normal auto-computing load.','Part4 models are numeric counts from pinned headers; cached rendering needs no fullQwen/GPT2weights or new header network access.','No public deployment, CI/local-computer tasks, upload or large archive copying occurred.'])
(OUT/'handoff-metadata.json').write_text(json.dumps(record,indent=2));print(json.dumps(dict(items=len(cases),payloads=42,payload_bytes=record['total_payload_bytes'],producer_calls=0,optional_npz_absence_items=record['optional_npz_absence_items'],all_part4_source_files_match_pin=True,working_pin_differences=[x['path'] for x in source if not x['working_matches_pin']],record_sha256=sha(OUT/'handoff-metadata.json')),indent=2))
