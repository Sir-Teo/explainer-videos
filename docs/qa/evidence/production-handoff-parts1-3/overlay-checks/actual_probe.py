"""Cloud-only preflight integration using an isolated shared-object Git clone."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,subprocess
ROOT=Path('/workspace/explainer-videos');OUT=Path(__file__).parent;R=OUT/'actual-927-checkout';D=ROOT/'docs/qa/evidence/production-handoff-parts1-3';BASE='927fba668656a682b3e29a288de64130ddc680dd';SVD='videos/ai/ai3/s08_svd.py';PATCH='7c47c11e3802390141c9551ac376ebe4ddf31e0e'
assert R.resolve()==Path('/workspace/runtime/svd-overlay-preflight-review/actual-927-checkout') and (R/'.git/objects/info/alternates').is_file()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();helper_before=sha(D/'verify_handoff.py')
spec=importlib.util.spec_from_file_location('actual_preflight',D/'verify_handoff.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
core=json.loads((D/'cache-inventory.json').read_text())['files'];extra=json.loads((D/'external-validation-dependencies.json').read_text())['extra_repo_relative_files']
for row in core+extra:
 p=R/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/row['path'],p)
results={}
def git(*args):return subprocess.run(['git',*args],cwd=R,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def run(name,**kwargs):
 x=m.verify(R,**kwargs);p=OUT/(name+'.json');p.write_text(json.dumps(x,indent=2)+'\n');results[name]={'errors':len(x['errors']),'checked_files':x['checked_files'],'result_sha256':sha(p)};return x
# Reset only this private disposable fixture; no worktree registration or shared-ref writes.
git('reset','--hard',BASE)
assert not run('actual-base-default')['errors']
(R/SVD).write_bytes((ROOT/SVD).read_bytes());assert sha(R/SVD)=='291bba0e7c180750274e2117114cc22382f3b9b81880db0a499791b4b2e3e322'
assert run('actual-after-without-overlay')['errors']
assert not run('actual-base-plus-exact-scene',overlay_id='svd-reveal-v1')['errors']
assert not run('actual-strict-external-complete',overlay_id='svd-reveal-v1',strict_external=True)['errors']
git('restore','--',SVD);git('-c','user.name=Cloud QA fixture','-c','user.email=qa@example.invalid','cherry-pick','--no-commit',PATCH)
assert not run('actual-reviewed-patch-staged',overlay_id='svd-reveal-v1',strict_external=True)['errors']
git('reset','--hard','f00be66a0b47954bbdfe00a03dba7ebfe6c6fc4b');(R/SVD).write_bytes((ROOT/SVD).read_bytes());bad=run('actual-f00-plus-scene-rejected',overlay_id='svd-reveal-v1');assert any('Overlay HEAD contains unrelated' in x for x in bad['errors'])
git('reset','--hard',BASE);(R/SVD).write_bytes((ROOT/SVD).read_bytes());assert not run('actual-final-accepted',overlay_id='svd-reveal-v1',strict_external=True)['errors']
assert helper_before==sha(D/'verify_handoff.py')
for row in core+extra:assert sha(ROOT/row['path'])==row['sha256'] and sha(R/row['path'])==row['sha256']
report={'scope':'Cloud-only isolated clone.141 actual core+3 actual novels files copied; all256 strict file checks exercised, exact package metadata/GPT2 cache bytes hashed without importing packages/scenes/producers or loading models. Actual7c47patch applied --no-commit in private clone only; no shared refs/source/cache edits/download/render/local execution.','helper_sha256':helper_before,'overlay_manifest_sha256':sha(D/'overlays/svd-reveal-v1.json'),'cases':results,'original_numerical_files_unchanged':True,'earlier_strict_failure':'Prior exploratory run intentionally lacked3novels extras; rawactual-strict-external.json preserves3errors. Final complete run copied exact inventoried extras and retained every strict gate.'};(OUT/'actual-integration-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
