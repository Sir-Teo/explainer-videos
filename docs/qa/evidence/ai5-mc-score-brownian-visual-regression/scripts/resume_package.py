from pathlib import Path
import datetime,gzip,hashlib,json,shutil
R=Path('/workspace/explainer-videos');O=Path(__file__).parent;P=R/'docs/qa/evidence/ai5-mc-score-brownian-visual-regression'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert P.is_dir() and not (P/'manifest.json').exists() and not (P/'README.md').exists()
receipts=json.loads((P/'gzip-original-byte-receipts.json').read_text())
for f in receipts:
 b=gzip.decompress((P/f['path']).read_bytes());assert len(b)==f['decoded_bytes'];assert hashlib.sha256(b).hexdigest()==f['decoded_sha256']
assets=json.loads((P/'image-assets.json').read_text())
for f in assets:assert sha(P/f['path'])==f['sha256']
old=P/'scripts/package.py';original=old.read_bytes()
with gzip.GzipFile(filename=str(P/'scripts/package-first-attempt.py.gz'),mode='wb',mtime=0) as f:f.write(original)
p=O/'package.py';s=p.read_text().replace('x["lang"].upper()', 'x["case"].split("-")[0].upper()').replace('x["scene"]} | {x["states"]}', 'x["case"].split("-")[1]} | {x["states"]}')
# Critical entries DO carry explicitlang/scene; restore their readablelabels.
s=s.replace("links='\\n'.join(f'| {x[\"case\"].split(\"-\")[0].upper()} {x[\"scene\"]}","links='\\n'.join(f'| {x[\"lang\"].upper()} {x[\"scene\"]}")
p.write_text(s);shutil.copy2(p,P/'scripts/package.py');shutil.copy2(Path(__file__),P/'scripts/resume_package.py')
(P/'package-reconciliation.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_attempt':'Local packaging stopped at README table construction: KeyError lang in aggregatecase entries. All immutable raw/image copies had alreadycompleted; no render/source/data mutation occurred.','original_script_sha256':hashlib.sha256(original).hexdigest(),'preserved_original_script':'scripts/package-first-attempt.py.gz','verified_prior_gzip_payloads':len(receipts),'verified_prior_image_assets':len(assets),'resolution':'Read lang/scene from aggregate caseidentifier; resume only README/manifest finalization after verifying every retained gzip/image byte identity. No productionoperation retry.','status':'reconciled-before-finalization'},indent=2)+'\n')
review=json.loads((O/'report.json').read_text());critical=json.loads((P/'critical-before-after.json').read_text())
exec(compile(s[s.index("rows='\\n'.join"):],'<package-finalization-only>','exec'),dict(globals(),assets=assets))
