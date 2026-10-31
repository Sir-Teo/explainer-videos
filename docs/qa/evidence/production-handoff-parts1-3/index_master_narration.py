#!/usr/bin/env python3
"""Index completed CRF master narration metadata for existing zh_lines/narrate discovery.
Copies JSON only, never movies; no scene imports, model/data loads or source edits.
Run only after successful full English master + stream/audio validation.
"""
import argparse,ast,json,shutil
from pathlib import Path
P=argparse.ArgumentParser(description=__doc__);P.add_argument('--repo',type=Path,required=True);P.add_argument('--part',choices=['ai1','ai2','ai3'],required=True);P.add_argument('--crf',type=int,default=16);P.add_argument('--fps',type=int,default=60);a=P.parse_args();R=a.repo.resolve()
t=ast.parse((R/f'videos/ai/{a.part}/manifest.py').read_text());scenes=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='SCENES' for v in n.targets));plan=[]
for module,cls,_ in scenes:
 src=R/f'media/{a.part}/crf{a.crf}/videos/{module}/2160p{a.fps}/{cls}.narration.json';dst=R/f'media/{a.part}/videos/{module}/2160p{a.fps}/{cls}.narration.json'
 if not src.with_suffix('').with_suffix('.mp4').is_file():raise SystemExit('Missing actual master movie beside '+str(src))
 meta=json.loads(src.read_text())
 if meta.get('scene')!=cls or not meta.get('lines') or not all(line.get('raw') for line in meta['lines']):raise SystemExit('Missing scene/raw narration metadata: '+str(src))
 if dst.exists() and dst.read_bytes()!=src.read_bytes():raise SystemExit('Different existing metadata; preserve/reconcile before indexing: '+str(dst))
 plan.append((src,dst))
for src,dst in plan:
 dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():shutil.copyfile(src,dst)
print('Indexed',len(plan),'completed master narration JSONs only. No movie exists or is implied at the metadata-only index paths.')
