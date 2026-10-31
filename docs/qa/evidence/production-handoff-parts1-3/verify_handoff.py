#!/usr/bin/env python3
"""Read-only hash/version preflight; never imports scenes/producers or loads models.
Not a production loader guard. Use --strict-external before full-part expansion.
"""
import argparse,hashlib,importlib.metadata,json,os,subprocess
from pathlib import Path
P=argparse.ArgumentParser(description=__doc__);P.add_argument('--repo',type=Path,required=True);P.add_argument('--strict-external',action='store_true');P.add_argument('--optional-audio',action='store_true');a=P.parse_args()
D=Path(__file__).resolve().parent;R=a.repo.resolve();errors=[];checked=0
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def check(p,row):
 global checked
 try:
  if not p.is_file() or p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:errors.append(str(p)+': missing/size/hash mismatch')
  checked+=1
 except OSError as e:errors.append(str(p)+': '+type(e).__name__)
core=json.loads((D/'cache-inventory.json').read_text());sources=json.loads((D/'reviewed-source-inventory.json').read_text());external=json.loads((D/'external-validation-dependencies.json').read_text())
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
if head!=sources['commit']:errors.append('Full-part source HEAD must equal '+sources['commit']+'; this check is not the separate cache-independent SVD pilot proof.')
for row in core['files']+sources['files']:check(R/row['path'],row)
if a.strict_external:
 for row in external['extra_repo_relative_files']+external['source_inputs']:check(R/row['path'],row)
 for name,expected in external['required_observed_packages'].items():
  try:actual=importlib.metadata.version(name)
  except importlib.metadata.PackageNotFoundError:actual=None
  if actual!=expected:errors.append(f'Package {name}: expected exact {expected}, found {actual}; STOP, do not weaken current().')
 base=Path(os.environ.get('HF_HUB_CACHE',str(Path(os.environ.get('HF_HOME',str(Path.home()/'.cache/huggingface')))/'hub')))
 for row in external['gpt2']['files']:check(base/row['snapshot_relative_path'],row)
 repo=base/'models--openai-community--gpt2';ref=repo/'refs/main'
 if ref.is_file():
  if ref.read_text().strip()!=external['gpt2']['revision']:errors.append('GPT-2 refs/main points to a different revision.')
 elif sorted(p.name for p in (repo/'snapshots').glob('*'))!=[external['gpt2']['revision']]:errors.append('GPT-2 snapshot resolution is missing or ambiguous.')
if a.optional_audio:
 for block in json.loads((D/'real-information-audio.json').read_text())['blocks']:
  for row in block['files']:check(R/row['path'],row)
print(json.dumps({'scope':'Read-only source/cache/dependency file hashes and package metadata only; no scene/producer imports, normal loads or model loads. Not a runtime inherited producer guard or visual/audio approval.','strict_external_requested':a.strict_external,'checked_files':checked,'errors':errors,'next_gate':'If no errors, run existing cached-only QA with all source/data writers stopped; full production still requires an inherited fail-on-call producer guard coordinated with parent.'},indent=2))
raise SystemExit(1 if errors else 0)
