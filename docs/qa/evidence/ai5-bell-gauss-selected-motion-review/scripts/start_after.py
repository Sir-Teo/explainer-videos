from pathlib import Path
import json,hashlib,shutil,datetime,sys
R=Path('/workspace/explainer-videos');B=Path('/workspace/runtime/ai5-bell-gauss-selected-motion-review');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
scene=sys.argv[1];module={'Bell':'s02_bell.py','Gauss':'s03_gauss.py'}[scene];expected={'Bell':'c4025027c65a62e4bb5f904802cacb357a2927b7f43434cda7adafe05dd42898','Gauss':'a913a45fd52683d2423e417262fa47588b165560335ae5e30957323630e44127'}[scene]
assert sha(R/f'videos/ai/ai5/{module}')==expected
for lang in ('en','zh'):
 old=B/f'{lang}-{scene}';D=B/f'{lang}-{scene}-after';D.mkdir(exist_ok=False);p=R/f'renders/qa/series/ai5/{lang}/{scene}_motion/result.json';d=json.loads(p.read_text());m=R/d['movie'];s=json.loads((old/'snapshot.json').read_text());assert sha(m)!=s['movie']['sha256'];shutil.copy2(p,D/'render-result.json');shutil.copy2(m,D/'movie.mp4')
 inp={i:{'sha256':sha(R/i),'bytes':(R/i).stat().st_size,'mtime_ns':(R/i).stat().st_mtime_ns,'raw_record_stat':v,'stat_matches':[(R/i).stat().st_size,(R/i).stat().st_mtime_ns]==v,'equals_before_sha256':sha(R/i)==s['inputs'][i]['sha256']} for i,v in d['inputs'].items()}
 files=[f'videos/ai/ai5/{module}','videos/ai/ai5/common.py','videos/ai/ai5/plotting.py','videos/ai/ai5/zh_lines.py','videos/ai/ai_text_zh.json','tools/qa_motion.py'];sources={}
 for rel in files:
  dst=D/'source-at-review'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dst);sources[rel]=sha(R/rel)
 snap={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'movie':{'path':str(m),'sha256':sha(m),'bytes':m.stat().st_size},'raw_record_sha256':sha(p),'raw_status':d['status'],'raw_warnings':d['warnings'],'raw_fingerprint':d['fingerprint'],'source_at_review':sources,'inputs':inp,'before_movie_sha256':s['movie']['sha256'],'source_linkage':'Parent current frozen scene; direct sources snapshotted before analysis. Historical aggregate warning retained; no blanket current-fingerprint assertion.','coverage':'Pending new selected-image review/exact SHA inheritance.'};(D/'snapshot.json').write_text(json.dumps(snap,indent=2)+'\n');print(lang,scene,sha(m),d['status'],d['warnings'],flush=True)
